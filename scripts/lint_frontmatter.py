import os
import re
import sys
import json
import yaml


def normalize(text):
    """Lowercase, strip punctuation, collapse whitespace — so wording can be
    compared across files without tripping on markup or line wrapping."""
    text = text.replace('\r\n', '\n').replace('\r', '\n').lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return ' '.join(text.split())


def read_frontmatter(skill_path):
    """Return (data, error_message). data is the parsed YAML frontmatter dict."""
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n').replace('\r', '\n')
    if not content.startswith('---\n'):
        return None, f"{skill_path} must start with frontmatter delimiters '---'"
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return None, f"{skill_path} is missing closing frontmatter delimiter '---'"
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return None, f"Failed to parse YAML frontmatter in {skill_path}: {exc}"
    if not data:
        return None, f"Frontmatter in {skill_path} is empty"
    return data, None


def extract_role_descriptions(skill_content):
    """Derive each role's description straight from SKILL.md so the linter never
    holds a second copy of the prose. SKILL.md is the single source of truth;
    the sync check only verifies PROMPT.md carries the SAME text."""
    content = skill_content.replace('\r\n', '\n').replace('\r', '\n')
    lines = content.split('\n')

    # Restrict to the panel region: "### Engineering panel" up to the next "## " heading.
    start = None
    end = len(lines)
    for i, line in enumerate(lines):
        if start is None and line.strip().lower().startswith('### engineering panel'):
            start = i
        elif start is not None and line.startswith('## '):
            end = i
            break
    if start is None:
        return []

    # Accumulate each "- **Role** ... — description" bullet, including wrapped lines.
    blocks = []
    current = None
    for line in lines[start:end]:
        if re.match(r'^- \*\*', line):
            if current is not None:
                blocks.append(current)
            current = line
        elif current is not None:
            if line.startswith('#'):
                blocks.append(current)
                current = None
            elif line.strip() == '':
                continue
            else:
                current += ' ' + line
    if current is not None:
        blocks.append(current)

    descriptions = []
    for block in blocks:
        # Description is everything after the first " — " (em dash) following the role name.
        parts = re.split(r'\s—\s', block, maxsplit=1)
        desc = parts[1] if len(parts) == 2 else block
        norm = normalize(desc)
        if norm:
            descriptions.append(norm)
    return descriptions


def check_prompt_sync():
    """Verify PROMPT.md still carries every role description and the verdict
    instruction defined in council/SKILL.md (the canonical source)."""
    skill_path = 'council/SKILL.md'
    prompt_path = 'PROMPT.md'

    if not os.path.exists(skill_path) or not os.path.exists(prompt_path):
        print(f"  [WARNING] Sync check skipped: {skill_path} or {prompt_path} not found.")
        return 0

    print("Checking synchronization between council/SKILL.md and PROMPT.md...")
    errors = 0
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            skill_raw = f.read()
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_norm = normalize(f.read())

        descriptions = extract_role_descriptions(skill_raw)
        if len(descriptions) < 8:
            print(f"  [ERROR] Expected 8 role descriptions in {skill_path}, found {len(descriptions)}")
            errors += 1

        for desc in descriptions:
            if desc not in prompt_norm:
                snippet = desc[:60]
                print(f"  [ERROR] Role description missing or mismatched in PROMPT.md: \"{snippet}...\"")
                errors += 1

        # The verdict instruction is the one shared output contract worth pinning by line.
        skill_norm = normalize(skill_raw)
        verdict = normalize('verdict, plus all actions ranked by (impact ÷ effort)')
        if verdict not in skill_norm:
            print(f"  [ERROR] Verdict instructions missing or mismatched in {skill_path}")
            errors += 1
        if verdict not in prompt_norm:
            print(f"  [ERROR] Verdict instructions missing or mismatched in PROMPT.md")
            errors += 1

    except Exception as e:
        print(f"  [ERROR] Unexpected error verifying synchronization: {e}")
        errors += 1

    return errors


def check_output_contract():
    """Guard the report-writing contract: a prompt regression that drops the
    'write to council-reviews/REVIEW_*' instruction would otherwise pass CI."""
    skill_path = 'council/SKILL.md'
    prompt_path = 'PROMPT.md'
    if not (os.path.exists(skill_path) and os.path.exists(prompt_path)):
        return 0

    print("Checking output contract (report destination)...")
    errors = 0
    required = ['council-reviews/', 'REVIEW_']
    for path in (skill_path, prompt_path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        for token in required:
            if token not in content:
                print(f"  [ERROR] {path} no longer mentions '{token}' — report-writing contract broken")
                errors += 1
    return errors


def check_plugin_manifest():
    """Validate the agy plugin layout (Option E): plugin.json is well-formed and
    its version matches every SKILL.md the plugin exposes under skills/."""
    manifest_path = 'plugin.json'
    if not os.path.exists(manifest_path):
        return 0

    print("Checking agy plugin manifest (plugin.json)...")
    errors = 0
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as exc:
        print(f"  [ERROR] plugin.json is not valid JSON: {exc}")
        return 1

    for field in ('name', 'version', 'description'):
        if not manifest.get(field):
            print(f"  [ERROR] plugin.json is missing required field '{field}'")
            errors += 1

    plugin_version = manifest.get('version')
    skills_dir = 'skills'
    if plugin_version and os.path.isdir(skills_dir):
        found_skill = False
        for entry in sorted(os.listdir(skills_dir)):
            # Follow the symlink (skills/<name> -> ../<name>) to the real SKILL.md.
            skill_path = os.path.realpath(os.path.join(skills_dir, entry, 'SKILL.md'))
            if not os.path.exists(skill_path):
                print(f"  [ERROR] skills/{entry} does not resolve to a SKILL.md (agy plugin layout broken)")
                errors += 1
                continue
            found_skill = True
            data, err = read_frontmatter(skill_path)
            if err:
                print(f"  [ERROR] {err}")
                errors += 1
                continue
            skill_version = str(data.get('version', '')).strip()
            if skill_version != str(plugin_version).strip():
                print(f"  [ERROR] Version drift: plugin.json is {plugin_version} but skills/{entry} SKILL.md is {skill_version or '(unset)'}")
                errors += 1
        if not found_skill:
            print(f"  [ERROR] plugin.json declares a plugin but skills/ exposes no SKILL.md")
            errors += 1

    return errors


def lint_skills():
    errors = 0
    # Search for all SKILL.md files
    for root, dirs, files in os.walk('.'):
        # Skip .git and hidden folders
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if 'SKILL.md' in files:
            skill_path = os.path.join(root, 'SKILL.md')
            folder_name = os.path.basename(root)
            print(f"Checking {skill_path}...")

            data, err = read_frontmatter(skill_path)
            if err:
                print(f"  [ERROR] {err}")
                errors += 1
                continue

            # Check name matches folder name
            name = data.get('name')
            if not name:
                print(f"  [ERROR] Missing 'name' in frontmatter of {skill_path}")
                errors += 1
            elif name != folder_name:
                print(f"  [ERROR] Skill name '{name}' in frontmatter does not match folder name '{folder_name}'")
                errors += 1

            # Check description exists
            if not data.get('description'):
                print(f"  [ERROR] Missing 'description' in frontmatter of {skill_path}")
                errors += 1

    errors += check_prompt_sync()
    errors += check_output_contract()
    errors += check_plugin_manifest()

    if errors > 0:
        print(f"\nLint failed with {errors} errors.")
        sys.exit(1)
    else:
        print("\nAll skills passed linting!")
        sys.exit(0)


if __name__ == '__main__':
    lint_skills()
