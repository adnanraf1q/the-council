import os
import shutil
import tempfile
import unittest
from unittest.mock import patch
import sys

# Add current directory to path so we can import lint_frontmatter
sys.path.append(os.path.dirname(__file__))
import lint_frontmatter

class TestLinter(unittest.TestCase):
    def setUp(self):
        # Create a temp directory
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
    def tearDown(self):
        # Restore cwd and remove temp directory
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def write_skill(self, folder, name, desc, body="body content"):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write(f"---\nname: {name}\ndescription: {desc}\n---\n{body}")

    def write_prompt(self, content):
        with open('PROMPT.md', 'w', encoding='utf-8') as f:
            f.write(content)

    @patch('sys.exit')
    def test_valid_skill(self, mock_exit):
        # Setup a valid skill directory structure
        self.write_skill('council', 'council', 'Multi-role review')
        
        # We don't have PROMPT.md so sync check should skip (warning only, no failure)
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(0)

    @patch('sys.exit')
    def test_missing_frontmatter_name(self, mock_exit):
        # Name is empty
        self.write_skill('council', '', 'Multi-role review')
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)

    @patch('sys.exit')
    def test_mismatched_folder_name(self, mock_exit):
        # Folder is 'council', name is 'different'
        self.write_skill('council', 'different', 'Multi-role review')
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)

    @patch('sys.exit')
    def test_sync_success(self, mock_exit):
        # Valid skill and prompt with same roles and instructions
        roles_text = (
            "structure, coupling, dead code, duplication, whether the docs still match the code, and CI/CD or dependency bloat. "
            "secrets in repo/configs, injection surfaces, authz gaps, exposed services/endpoints, token handling, and prompt injection/AI risks. "
            "hot paths, caching opportunities, redundant work; Cost/FinOps (inefficient resources, token bloat, 'what bankrupts you'); and what breaks first under growth (N+1 queries, missing indexes, unbounded queues, all-in-memory processing, single points of failure, per-tenant isolation under load) — name the breaking point and a rough threshold, not \"consider caching\". "
            "can someone resume this cold? failure modes, logging, doc drift, onboarding time; what validates outputs today, where would a silent regression hide, which ONE test/gate would catch the most damage (name the specific risk and the specific check). "
            "is it converging on its stated goal? smallest next step that produces real user feedback? what should deliberately NOT be built? what does a competent rival do better or cheaper today (competitive landscape), and where is the moat (or state plainly that there is none)? "
            "both audiences: whoever operates/administers it (first-run experience, friction, error opacity) and the end user (where they bounce, what feels off even if they couldn't name it). Includes accessibility (a11y — WCAG, screen readers, keyboard navigation) and visual/output quality where the app produces something visible. "
            "data handling and privacy obligations, licensing, platform/policy exposure, secrets hygiene. "
            "exempt from the diplomacy expected elsewhere: one blunt paragraph saying what everyone is politely not saying. Must still be specific to THIS app — cruelty without evidence is noise. "
            "verdict, plus all actions ranked by (impact ÷ effort)."
        )
        self.write_skill('council', 'council', 'Multi-role review', body=roles_text)
        self.write_prompt(roles_text)
        
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(0)

    @patch('sys.exit')
    def test_sync_failure(self, mock_exit):
        # Missing role descriptions in prompt
        self.write_skill('council', 'council', 'Multi-role review', 
                         body="structure, coupling, dead code, duplication, whether the docs still match the code, and CI/CD or dependency bloat. verdict, plus all actions ranked by (impact ÷ effort).")
        self.write_prompt("Some completely different prompt text. verdict, plus all actions ranked by (impact ÷ effort).")
        
        lint_frontmatter.lint_skills()
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
