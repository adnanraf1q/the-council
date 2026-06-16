import os
import re
import sys
import yaml

def check_prompt_sync():
    """Verify that council/SKILL.md and PROMPT.md are synchronized in their core roles and instructions."""
    skill_path = 'council/SKILL.md'
    prompt_path = 'PROMPT.md'
    
    if not os.path.exists(skill_path) or not os.path.exists(prompt_path):
        print(f"  [WARNING] Sync check skipped: {skill_path} or {prompt_path} not found.")
        return 0

    print("Checking synchronization between council/SKILL.md and PROMPT.md...")
    errors = 0
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            skill_content = f.read().replace('\r\n', '\n').lower()
            skill_content = re.sub(r'[^a-z0-9\s]', ' ', skill_content)
            skill_content = ' '.join(skill_content.split())
            
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read().replace('\r\n', '\n').lower()
            prompt_content = re.sub(r'[^a-z0-9\s]', ' ', prompt_content)
            prompt_content = ' '.join(prompt_content.split())
            
        role_descriptions = {
            'Architect': 'structure, coupling, dead code, duplication, whether the docs still match the code, and CI/CD or dependency bloat',
            'Security': 'secrets in repo/configs, injection surfaces, authz gaps, exposed services/endpoints, token handling, and prompt injection/AI risks',
            'Performance': 'hot paths, caching opportunities, redundant work; Cost/FinOps (inefficient resources, token bloat, \'what bankrupts you\'); and what breaks first under growth (N+1 queries, missing indexes, unbounded queues, all-in-memory processing, single points of failure, per-tenant isolation under load) — name the breaking point and a rough threshold, not "consider caching"',
            'Reliability': 'can someone resume this cold? failure modes, logging, doc drift, onboarding time; what validates outputs today, where would a silent regression hide, which ONE test/gate would catch the most damage (name the specific risk and the specific check)',
            'Product & Market': 'is it converging on its stated goal? smallest next step that produces real user feedback? what should deliberately NOT be built? what does a competent rival do better or cheaper today (competitive landscape), and where is the moat (or state plainly that there is none)?',
            'Experience': 'both audiences: whoever operates/administers it (first-run experience, friction, error opacity) and the end user (where they bounce, what feels off even if they couldn\'t name it). Includes accessibility (a11y — WCAG, screen readers, keyboard navigation) and visual/output quality where the app produces something visible',
            'Compliance': 'data handling and privacy obligations, licensing, platform/policy exposure, secrets hygiene',
            'Critic': 'exempt from the diplomacy expected elsewhere: one blunt paragraph saying what everyone is politely not saying. Must still be specific to THIS app — cruelty without evidence is noise'
        }
        
        for name, desc in role_descriptions.items():
            norm_desc = re.sub(r'[^a-z0-9\s]', ' ', desc.lower())
            norm_desc = ' '.join(norm_desc.split())
            
            if name == 'Experience':
                alt_desc = norm_desc.replace('includes accessibility', 'include accessibility')
                in_skill = (norm_desc in skill_content) or (alt_desc in skill_content)
                in_prompt = (norm_desc in prompt_content) or (alt_desc in prompt_content)
            else:
                in_skill = norm_desc in skill_content
                in_prompt = norm_desc in prompt_content
                
            if not in_skill:
                print(f"  [ERROR] Role '{name}' description is missing or mismatched in council/SKILL.md")
                errors += 1
            if not in_prompt:
                print(f"  [ERROR] Role '{name}' description is missing or mismatched in PROMPT.md")
                errors += 1
                
        verdict_instr = 'verdict, plus all actions ranked by (impact ÷ effort)'
        norm_verdict = re.sub(r'[^a-z0-9\s]', ' ', verdict_instr.lower())
        norm_verdict = ' '.join(norm_verdict.split())
        if norm_verdict not in skill_content:
            print(f"  [ERROR] Verdict instructions missing or mismatched in council/SKILL.md")
            errors += 1
        if norm_verdict not in prompt_content:
            print(f"  [ERROR] Verdict instructions missing or mismatched in PROMPT.md")
            errors += 1
            
    except Exception as e:
        print(f"  [ERROR] Unexpected error verifying synchronization: {e}")
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
            
            try:
                with open(skill_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Robust to CRLF/CR/LF line endings by converting all to LF
                content = content.replace('\r\n', '\n').replace('\r', '\n')
                
                # Extract frontmatter
                if not content.startswith('---\n'):
                    print(f"  [ERROR] {skill_path} must start with frontmatter delimiters '---'")
                    errors += 1
                    continue
                
                parts = content.split('---\n', 2)
                if len(parts) < 3:
                    print(f"  [ERROR] {skill_path} is missing closing frontmatter delimiter '---'")
                    errors += 1
                    continue
                
                frontmatter_text = parts[1]
                try:
                    data = yaml.safe_load(frontmatter_text)
                except yaml.YAMLError as exc:
                    print(f"  [ERROR] Failed to parse YAML frontmatter in {skill_path}: {exc}")
                    errors += 1
                    continue
                
                if not data:
                    print(f"  [ERROR] Frontmatter in {skill_path} is empty")
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
                    
            except Exception as e:
                print(f"  [ERROR] Unexpected error reading {skill_path}: {e}")
                errors += 1

    # Run the prompt synchronization check
    sync_errors = check_prompt_sync()
    errors += sync_errors

    if errors > 0:
        print(f"\nLint failed with {errors} errors.")
        sys.exit(1)
    else:
        print("\nAll skills passed linting!")
        sys.exit(0)

if __name__ == '__main__':
    lint_skills()
