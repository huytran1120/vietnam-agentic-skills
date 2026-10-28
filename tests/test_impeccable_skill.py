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


class ImpeccableSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "data/impeccable.json").read_text(encoding="utf-8")
        )
        cls.index = VAS.load_index()
        cls.by_id = {row["id"]: row for row in cls.index}

    def test_manifest_metadata(self):
        self.assertEqual(self.manifest["author"], "Paul Bakaus")
        self.assertEqual(self.manifest["license"], "Apache-2.0")
        self.assertEqual(self.manifest["version"], "4.8.0")
        self.assertEqual(self.manifest["engineVersion"], "0.1.18")
        self.assertEqual(self.manifest["repository"], "https://github.com/pbakaus/impeccable")
        self.assertEqual(self.manifest["category"], "design")

    def test_skill_md_frontmatter_and_content(self):
        skill_dir = ROOT / "skills/impeccable"
        skill_md = skill_dir / "SKILL.md"
        self.assertTrue(skill_dir.is_dir())
        self.assertTrue(skill_md.is_file())
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("author: Paul Bakaus", content)
        self.assertIn("source_repo: pbakaus/impeccable", content)
        self.assertIn("license: Apache-2.0", content)
        self.assertIn("category: design", content)
        self.assertIn("version: 4.8.0", content)

    def test_engine_scripts_and_checksums(self):
        scripts_dir = ROOT / "skills/impeccable/scripts"
        self.assertTrue((scripts_dir / "impeccable").is_file())
        self.assertTrue((scripts_dir / "engine-checksums.txt").is_file())
        self.assertTrue((scripts_dir / "VERSION").is_file())
        
        version_text = (scripts_dir / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version_text, "0.1.18")
        
        checksums = (scripts_dir / "engine-checksums.txt").read_text(encoding="utf-8")
        self.assertIn("0.1.18 impeccable-darwin-arm64", checksums)
        self.assertIn("0.1.18 impeccable-linux-x64", checksums)
        self.assertIn("0.1.18 impeccable-windows-x64.exe", checksums)

    def test_notices_and_licenses_exist(self):
        skill_dir = ROOT / "skills/impeccable"
        self.assertTrue((skill_dir / "UPSTREAM-LICENSE.txt").is_file())
        self.assertTrue((skill_dir / "UPSTREAM-NOTICE.md").is_file())
        notice = (skill_dir / "UPSTREAM-NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("Paul Bakaus", notice)
        self.assertIn("4.8.0", notice)

    def test_index_metadata(self):
        self.assertIn("impeccable", self.by_id)
        meta = self.by_id["impeccable"]
        self.assertEqual(meta["author"], "Paul Bakaus")
        self.assertEqual(meta["source_repo"], "pbakaus/impeccable")
        self.assertEqual(meta["license"], "Apache-2.0")
        self.assertEqual(meta["category"], "design")

    def test_search_by_author_and_anti_slop(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            VAS.cmd_search(Namespace(query="Paul Bakaus", limit=10))
        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", output.getvalue())
        self.assertIn("impeccable", clean_output)

        with contextlib.redirect_stdout(io.StringIO()) as output:
            VAS.cmd_search(Namespace(query="anti-slop", limit=10))
        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", output.getvalue())
        self.assertIn("impeccable", clean_output)

    def test_install_impeccable_link_and_copy(self):
        for mode in ("copy", "link"):
            with tempfile.TemporaryDirectory(prefix="vas-impeccable-") as temp:
                destination = Path(temp) / "skills"
                result = subprocess.run(
                    [
                        sys.executable, "-B", str(ROOT / "vas.py"), "install", "impeccable",
                        "--mode", mode, "--dest", str(destination),
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                installed_dir = destination / "impeccable"
                self.assertTrue(installed_dir.exists())
                self.assertEqual(installed_dir.is_symlink(), mode == "link")
                self.assertTrue((installed_dir / "SKILL.md").exists())
                self.assertTrue((installed_dir / "scripts" / "impeccable").exists())
                self.assertTrue((installed_dir / "scripts" / "engine-checksums.txt").exists())


if __name__ == "__main__":
    unittest.main()
