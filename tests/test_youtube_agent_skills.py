import contextlib
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import vas as VAS


class YoutubeAgentSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "data/youtube-agent-skills.json").read_text(encoding="utf-8")
        )
        cls.index = VAS.load_index()
        cls.by_id = {row["id"]: row for row in cls.index}

    def test_manifest_contains_11_skills(self):
        self.assertEqual(self.manifest["importedCount"], 11)
        self.assertEqual(len(self.manifest["skills"]), 11)
        self.assertEqual(self.manifest["author"], "Jake Schincariol")
        self.assertEqual(self.manifest["license"], "MIT")
        self.assertEqual(self.manifest["repository"], "https://github.com/Jakeschincariol/youtube-agent-skill")

    def test_all_11_skills_exist_and_have_valid_skill_md(self):
        for item in self.manifest["skills"]:
            skill_id = item["id"]
            skill_dir = ROOT / "skills" / skill_id
            skill_md = skill_dir / "SKILL.md"
            with self.subTest(skill_id=skill_id):
                self.assertTrue(skill_dir.is_dir(), f"Directory missing: {skill_dir}")
                self.assertTrue(skill_md.is_file(), f"SKILL.md missing: {skill_md}")
                content = skill_md.read_text(encoding="utf-8")
                self.assertIn("author: Jake Schincariol", content)
                self.assertIn("source_repo: Jakeschincariol/youtube-agent-skill", content)
                self.assertIn("license: MIT", content)
                self.assertIn("category: video", content)

    def test_all_11_skills_present_in_index_with_metadata(self):
        for item in self.manifest["skills"]:
            skill_id = item["id"]
            with self.subTest(skill_id=skill_id):
                self.assertIn(skill_id, self.by_id)
                meta = self.by_id[skill_id]
                self.assertEqual(meta["author"], "Jake Schincariol")
                self.assertEqual(meta["source_repo"], "Jakeschincariol/youtube-agent-skill")
                self.assertEqual(meta["license"], "MIT")
                self.assertEqual(meta["category"], "video")

    def test_python_tools_exist_and_self_contained(self):
        tools = [
            ("yt-package", "title.py"),
            ("yt-script", "hookscore.py"),
            ("yt-script", "hooks.json"),
            ("yt-edit", "deadair.py"),
            ("yt-chapters", "chapters.py"),
            ("yt-retention", "retention.py"),
            ("yt-viral", "swipe.py"),
            ("yt-viral", "hooks.json"),
        ]
        for skill_id, filename in tools:
            with self.subTest(skill_id=skill_id, file=filename):
                file_path = ROOT / "skills" / skill_id / filename
                self.assertTrue(file_path.is_file(), f"Missing tool file: {file_path}")

    def test_hookscore_execution(self):
        script_path = ROOT / "skills/yt-script/hookscore.py"
        result = subprocess.run(
            [sys.executable, str(script_path), "--hook", "I tested 100 AI tools so you don't waste your money"],
            text=True,
            capture_output=True,
            cwd=script_path.parent,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SPECIFICITY", result.stdout)
        self.assertIn("VERDICT", result.stdout)

    def test_title_linter_execution(self):
        script_path = ROOT / "skills/yt-package/title.py"
        result = subprocess.run(
            [sys.executable, str(script_path), "--title", "I Built 3,000 AI Agent Skills in 30 Days", "--thumb", "IT WORKED"],
            text=True,
            capture_output=True,
            cwd=script_path.parent,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("score 100/100", result.stdout)

    def test_search_by_author_finds_all_youtube_skills(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            VAS.cmd_search(Namespace(query="Jake Schincariol", limit=100))
        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", output.getvalue())
        for item in self.manifest["skills"]:
            skill_id = item["id"]
            with self.subTest(skill_id=skill_id):
                self.assertIn(f". {skill_id}", clean_output)

    def test_install_youtube_skill_link_and_copy(self):
        for mode in ("copy", "link"):
            with tempfile.TemporaryDirectory(prefix="vas-yt-") as temp:
                destination = Path(temp) / "skills"
                result = subprocess.run(
                    [
                        sys.executable, "-B", str(ROOT / "vas.py"), "install", "yt-script",
                        "--mode", mode, "--dest", str(destination),
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                installed_dir = destination / "yt-script"
                self.assertTrue(installed_dir.exists())
                self.assertEqual(installed_dir.is_symlink(), mode == "link")
                self.assertTrue((installed_dir / "SKILL.md").exists())
                self.assertTrue((installed_dir / "hookscore.py").exists())
                self.assertTrue((installed_dir / "hooks.json").exists())


if __name__ == "__main__":
    unittest.main()
