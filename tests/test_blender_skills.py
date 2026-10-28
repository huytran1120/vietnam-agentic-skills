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


class BlenderSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "data/blender-skills.json").read_text(encoding="utf-8")
        )
        cls.index = VAS.load_index()
        cls.by_id = {row["id"]: row for row in cls.index}

    def test_manifest_contains_94_skills(self):
        self.assertEqual(self.manifest["importedCount"], 94)
        self.assertEqual(len(self.manifest["skills"]), 94)
        self.assertEqual(self.manifest["author"], "Arjun Shukla")
        self.assertEqual(self.manifest["license"], "MIT")
        self.assertEqual(self.manifest["repository"], "https://github.com/arjun988/blender-skills")

    def test_all_94_skills_exist_and_have_valid_skill_md(self):
        for item in self.manifest["skills"]:
            skill_id = item["id"]
            skill_dir = ROOT / "skills" / skill_id
            skill_md = skill_dir / "SKILL.md"
            with self.subTest(skill_id=skill_id):
                self.assertTrue(skill_dir.is_dir(), f"Directory missing: {skill_dir}")
                self.assertTrue(skill_md.is_file(), f"SKILL.md missing: {skill_md}")
                content = skill_md.read_text(encoding="utf-8")
                self.assertIn("author: Arjun Shukla", content)
                self.assertIn("source_repo: arjun988/blender-skills", content)
                self.assertIn("license: MIT", content)
                self.assertIn("category: design", content)

    def test_all_94_skills_present_in_index_with_metadata(self):
        for item in self.manifest["skills"]:
            skill_id = item["id"]
            with self.subTest(skill_id=skill_id):
                self.assertIn(skill_id, self.by_id)
                meta = self.by_id[skill_id]
                self.assertEqual(meta["author"], "Arjun Shukla")
                self.assertEqual(meta["source_repo"], "arjun988/blender-skills")
                self.assertEqual(meta["license"], "MIT")
                self.assertEqual(meta["category"], "design")

    def test_lookdev_collision_resolution(self):
        # Both lookdev (original lookdev-studio) and blender-lookdev must exist
        self.assertIn("lookdev", self.by_id)
        self.assertIn("blender-lookdev", self.by_id)
        # Original lookdev should not be Arjun Shukla
        self.assertNotEqual(self.by_id["lookdev"].get("author"), "Arjun Shukla")
        # blender-lookdev must be Arjun Shukla
        self.assertEqual(self.by_id["blender-lookdev"]["author"], "Arjun Shukla")

    def test_self_contained_references(self):
        # Skills that require reference tables should have them locally in references/
        skills_with_references = [
            "blender-modeler",
            "character-artist",
            "asset-optimization",
            "lod-pipeline",
            "prop-artist",
        ]
        for skill_id in skills_with_references:
            with self.subTest(skill_id=skill_id):
                ref_dir = ROOT / "skills" / skill_id / "references"
                self.assertTrue(ref_dir.is_dir(), f"Missing references/ in {skill_id}")
                ref_files = list(ref_dir.glob("*.md"))
                self.assertGreater(len(ref_files), 0)

    def test_search_by_author_finds_all_94_skills(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            VAS.cmd_search(Namespace(query="Arjun Shukla", limit=150))
        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", output.getvalue())
        for item in self.manifest["skills"]:
            skill_id = item["id"]
            with self.subTest(skill_id=skill_id):
                self.assertIn(f". {skill_id}", clean_output)

    def test_search_by_blender_keyword(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            VAS.cmd_search(Namespace(query="blender-modeler", limit=10))
        clean_output = re.sub(r"\x1b\[[0-9;]*m", "", output.getvalue())
        self.assertIn("blender-modeler", clean_output)

    def test_install_blender_skill_link_and_copy(self):
        for mode in ("copy", "link"):
            with tempfile.TemporaryDirectory(prefix="vas-blender-") as temp:
                destination = Path(temp) / "skills"
                result = subprocess.run(
                    [
                        sys.executable, "-B", str(ROOT / "vas.py"), "install", "blender-modeler",
                        "--mode", mode, "--dest", str(destination),
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                installed_dir = destination / "blender-modeler"
                self.assertTrue(installed_dir.exists())
                self.assertEqual(installed_dir.is_symlink(), mode == "link")
                self.assertTrue((installed_dir / "SKILL.md").exists())
                self.assertTrue((installed_dir / "references" / "asset-pipeline.md").exists())


if __name__ == "__main__":
    unittest.main()
