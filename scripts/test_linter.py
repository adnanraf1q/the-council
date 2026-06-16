import os
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch
import sys

# Add current directory to path so we can import lint_frontmatter
sys.path.append(os.path.dirname(__file__))
import lint_frontmatter

# Eight role descriptions, defined once and rendered into both files so the
# fixtures stay in sync the same way the real repo does.
ROLE_DESCS = [
    "structure, coupling, dead code, and dependency bloat",
    "secrets in repo, injection surfaces, and authz gaps",
    "hot paths, caching opportunities, and what breaks first under growth",
    "can someone resume this cold? failure modes and logging",
    "is it converging on its stated goal? where is the moat",
    "both audiences: the operator and the end user, including accessibility",
    "data handling and privacy obligations, licensing, secrets hygiene",
    "exempt from the diplomacy expected elsewhere: one blunt paragraph",
]
ROLE_NAMES = [
    "Architect", "Security reviewer", "Performance, infra & scale",
    "Reliability (operator + QA)", "Product & market", "Experience",
    "Compliance reviewer", "The Critic (no filter)",
]
VERDICT = "Verdict, plus all actions ranked by (impact ÷ effort)."
REPORT_LINE = "Write the full report to council-reviews/REVIEW_<date>.md."


def council_skill_body():
    eng = "\n".join(f"- **{ROLE_NAMES[i]}** — {ROLE_DESCS[i]}" for i in range(4))
    prod = "\n".join(f"- **{ROLE_NAMES[i]}** *(merged)* — {ROLE_DESCS[i]}" for i in range(4, 8))
    return (
        "# App Review\n\n## Phase 1 — Panel review\n\n"
        "### Engineering panel\n\n" + eng + "\n\n"
        "### Product panel\n\n" + prod + "\n\n"
        "## Phase 2 — Output\n\n- " + VERDICT + "\n- " + REPORT_LINE + "\n"
    )


def matching_prompt():
    roles = "\n".join(f"- {ROLE_NAMES[i]}: {ROLE_DESCS[i]}" for i in range(8))
    return roles + "\n" + VERDICT + "\n" + REPORT_LINE + "\n"


class TestLinter(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def write_skill(self, folder, name, desc, body="body content"):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write(f"---\nname: {name}\ndescription: {desc}\n---\n{body}")

    def write_council(self, version=None):
        os.makedirs('council', exist_ok=True)
        version_line = f"version: {version}\n" if version else ""
        with open(os.path.join('council', 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write(f"---\nname: council\ndescription: Multi-role review\n{version_line}---\n{council_skill_body()}")

    def write_prompt(self, content):
        with open('PROMPT.md', 'w', encoding='utf-8') as f:
            f.write(content)

    def write_plugin(self, version):
        with open('plugin.json', 'w', encoding='utf-8') as f:
            json.dump({"name": "the-council", "version": version, "description": "x"}, f)

    def link_skill(self):
        os.makedirs('skills', exist_ok=True)
        try:
            os.symlink(os.path.join('..', 'council'), os.path.join('skills', 'council'))
        except (OSError, NotImplementedError):
            self.skipTest("symlinks not supported on this platform")

    # --- frontmatter checks -------------------------------------------------

    @patch('sys.exit')
    def test_valid_skill(self, mock_exit):
        # Valid skill, no PROMPT.md/plugin.json -> cross-file checks skip cleanly.
        self.write_skill('council', 'council', 'Multi-role review')
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(0)

    @patch('sys.exit')
    def test_missing_frontmatter_name(self, mock_exit):
        self.write_skill('council', '', 'Multi-role review')
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)

    @patch('sys.exit')
    def test_mismatched_folder_name(self, mock_exit):
        self.write_skill('council', 'different', 'Multi-role review')
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)

    # --- PROMPT.md sync (derived from SKILL.md) -----------------------------

    @patch('sys.exit')
    def test_sync_success(self, mock_exit):
        self.write_council()
        self.write_prompt(matching_prompt())
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(0)

    @patch('sys.exit')
    def test_sync_failure(self, mock_exit):
        # PROMPT.md drops one role's wording -> sync must fail.
        self.write_council()
        prompt = matching_prompt().replace(ROLE_DESCS[2], "totally different perf wording")
        self.write_prompt(prompt)
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)

    # --- output contract ----------------------------------------------------

    @patch('sys.exit')
    def test_output_contract_failure(self, mock_exit):
        # PROMPT.md loses the report destination -> contract must fail.
        self.write_council()
        prompt = matching_prompt().replace("council-reviews/REVIEW_<date>.md", "the repo root")
        self.write_prompt(prompt)
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)

    # --- plugin manifest / version sync -------------------------------------

    @patch('sys.exit')
    def test_version_match(self, mock_exit):
        self.write_council(version="1.3.0")
        self.write_prompt(matching_prompt())
        self.write_plugin("1.3.0")
        self.link_skill()
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(0)

    @patch('sys.exit')
    def test_version_drift(self, mock_exit):
        self.write_council(version="1.3.0")
        self.write_prompt(matching_prompt())
        self.write_plugin("1.2.0")  # stale manifest
        self.link_skill()
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)

    @patch('sys.exit')
    def test_plugin_missing_field(self, mock_exit):
        self.write_skill('council', 'council', 'Multi-role review')
        with open('plugin.json', 'w', encoding='utf-8') as f:
            json.dump({"name": "the-council"}, f)  # missing version + description
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)


if __name__ == '__main__':
    unittest.main()
