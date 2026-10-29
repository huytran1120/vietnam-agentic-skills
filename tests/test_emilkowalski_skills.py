import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import vas as VAS


class EmilKowalskiSkillsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "data/emilkowalski-skills.json").read_text(encoding="utf-8")
        )
        cls.aliases = json.loads(
            (ROOT / "data/aliases.json").read_text(encoding="utf-8")
        )
        cls.index = VAS.load_index()
        cls.by_id = {row["id"]: row for row in cls.index}

    def test_manifest_metadata(self):
        self.assertEqual(self.manifest["importedCount"], 16)
        self.assertEqual(len(self.manifest["skills"]), 16)
        self.assertEqual(self.manifest["author"], "Emil Kowalski")
        self.assertEqual(self.manifest["license"], "MIT")
        self.assertEqual(self.manifest["repository"], "https://github.com/emilkowalski/skills")
        self.assertEqual(self.manifest["revision"], "a81dbca07f2217b7103e510c0f13f8d5b017afc9")

    def test_all_16_skills_exist_and_have_valid_skill_md(self):
        for item in self.manifest["skills"]:
            skill_id = item["id"]
            skill_dir = ROOT / "skills" / skill_id
            skill_md = skill_dir / "SKILL.md"
            with self.subTest(skill_id=skill_id):
                self.assertTrue(skill_dir.is_dir(), f"Directory missing: {skill_dir}")
                self.assertTrue(skill_md.is_file(), f"SKILL.md missing: {skill_md}")
                content = skill_md.read_text(encoding="utf-8")
                self.assertIn("author: \"Emil Kowalski\"", content)
                self.assertIn("source_repo: \"emilkowalski/skills\"", content)
                self.assertIn("license: \"MIT\"", content)
                self.assertTrue((skill_dir / "UPSTREAM-NOTICE.md").is_file())
                self.assertTrue((skill_dir / "UPSTREAM-LICENSE.txt").is_file())

    def test_companion_files_and_references(self):
        self.assertTrue((ROOT / "skills/animate/RECIPES.md").is_file())
        self.assertTrue((ROOT / "skills/animate-expo/RECIPES.md").is_file())
        self.assertTrue((ROOT / "skills/ask-sonner/API.md").is_file())
        self.assertTrue((ROOT / "skills/break-ui/CATALOG.md").is_file())
        self.assertTrue((ROOT / "skills/improve-animations/AUDIT.md").is_file())
        self.assertTrue((ROOT / "skills/improve-animations/PLAN-TEMPLATE.md").is_file())
        self.assertTrue((ROOT / "skills/review-animations/STANDARDS.md").is_file())
        self.assertTrue((ROOT / "skills/emil-prototype/PICKER.md").is_file())
        self.assertTrue((ROOT / "skills/emil-design-eng/references/performance-cheatsheet.md").is_file())
        self.assertTrue((ROOT / "skills/emil-design-eng/references/ui-cheatsheet.md").is_file())

    def test_prototype_collision_resolution_preserves_mattpocock(self):
        # Matt Pocock's prototype skill must remain untouched
        matt_proto = ROOT / "skills/prototype/SKILL.md"
        self.assertTrue(matt_proto.is_file())
        matt_content = matt_proto.read_text(encoding="utf-8")
        self.assertIn("author: \"Matt Pocock\"", matt_content)
        self.assertIn("mattpocock/skills", matt_content)

        # Emil Kowalski's prototype is safely namespaced to emil-prototype
        emil_proto = ROOT / "skills/emil-prototype/SKILL.md"
        self.assertTrue(emil_proto.is_file())
        emil_content = emil_proto.read_text(encoding="utf-8")
        self.assertIn("author: \"Emil Kowalski\"", emil_content)
        self.assertIn("emilkowalski/skills", emil_content)

    def test_aliases_registered(self):
        self.assertEqual(self.aliases.get("prototype-variants"), "emil-prototype")
        self.assertEqual(self.aliases.get("ui-prototype"), "emil-prototype")
        self.assertEqual(self.aliases.get("emil-animations"), "emil-design-eng")
        self.assertEqual(self.aliases.get("sonner"), "ask-sonner")
        self.assertEqual(self.aliases.get("swift"), "write-swift")
        self.assertEqual(self.aliases.get("swift-concurrency"), "write-swift")

    def test_all_16_skills_present_in_index_with_metadata(self):
        for item in self.manifest["skills"]:
            skill_id = item["id"]
            with self.subTest(skill_id=skill_id):
                self.assertIn(skill_id, self.by_id, f"Missing from index: {skill_id}")
                row = self.by_id[skill_id]
                self.assertEqual(row.get("category"), item["category"])
                self.assertEqual(row.get("author"), "Emil Kowalski")
                self.assertEqual(row.get("license"), "MIT")

    def test_cli_search_and_show(self):
        res = subprocess.run(
            [sys.executable, "vas.py", "search", "sonner"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("ask-sonner", res.stdout)

        res_swift = subprocess.run(
            [sys.executable, "vas.py", "search", "write-swift"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("write-swift", res_swift.stdout)

        res_show = subprocess.run(
            [sys.executable, "vas.py", "show", "emil-prototype"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("emil-prototype", res_show.stdout)
        self.assertIn("Emil Kowalski", res_show.stdout)

    def test_install_emil_skill_link_and_copy(self):
        for mode in ("copy", "link"):
            with tempfile.TemporaryDirectory(prefix="vas-emil-") as temp:
                destination = Path(temp) / "skills"
                result = subprocess.run(
                    [
                        sys.executable, "-B", str(ROOT / "vas.py"), "install", "ask-sonner",
                        "--mode", mode, "--dest", str(destination),
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                installed_dir = destination / "ask-sonner"
                self.assertTrue(installed_dir.exists())
                self.assertEqual(installed_dir.is_symlink(), mode == "link")
                self.assertTrue((installed_dir / "SKILL.md").exists())
                self.assertTrue((installed_dir / "API.md").exists())


if __name__ == "__main__":
    unittest.main()
