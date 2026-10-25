import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from collections import Counter
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("vas", ROOT / "vas.py")
VAS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VAS)


class MattPocockCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (ROOT / "data/mattpocock-skills.json").read_text(encoding="utf-8")
        )
        cls.index = VAS.load_index()
        cls.by_id = {row["id"]: row for row in cls.index}

    def test_only_missing_stable_skills_were_added(self):
        self.assertEqual(len(self.manifest["imported"]), 16)
        self.assertEqual(len(self.manifest["stable_upstream_ids"]), 31)
        for skill_id in self.manifest["stable_upstream_ids"]:
            with self.subTest(skill_id=skill_id):
                self.assertIn(skill_id, self.by_id)
        for skill_id in self.manifest["excluded_in_progress_ids"]:
            with self.subTest(excluded=skill_id):
                self.assertNotIn(skill_id, self.by_id)

    def test_existing_customized_skills_are_unchanged(self):
        self.assertEqual(len(self.manifest["preserved"]), 19)
        for skill in self.manifest["preserved"]:
            with self.subTest(skill_id=skill["id"]):
                path = ROOT / self.by_id[skill["id"]]["path"] / "SKILL.md"
                self.assertEqual(
                    hashlib.sha256(path.read_bytes()).hexdigest(),
                    skill["skill_sha256"],
                )

    def test_imported_files_and_licenses_match_the_manifest(self):
        for skill in self.manifest["imported"]:
            directory = ROOT / "skills" / skill["id"]
            with self.subTest(skill_id=skill["id"]):
                license_path = directory / "UPSTREAM-LICENSE.txt"
                self.assertEqual(
                    hashlib.sha256(license_path.read_bytes()).hexdigest(),
                    self.manifest["license_sha256"],
                )
                self.assertIn(
                    self.manifest["revision"],
                    (directory / "UPSTREAM-NOTICE.md").read_text(encoding="utf-8"),
                )
            for file in skill["files"]:
                with self.subTest(skill_id=skill["id"], file=file["path"]):
                    local_hash = hashlib.sha256(
                        (directory / file["path"]).read_bytes()
                    ).hexdigest()
                    self.assertEqual(local_hash, file["imported_sha256"])
                    if file["path"] != "SKILL.md":
                        self.assertEqual(local_hash, file["upstream_sha256"])

    def test_new_metadata_survives_catalog_scanning(self):
        scanned = {row["id"]: row for row in VAS.scan_skills_locally()}
        source = {
            row["id"]: row
            for row in json.loads(
                (ROOT / "data/catalog.json").read_text(encoding="utf-8")
            )["skills"]
        }
        for skill in self.manifest["imported"]:
            with self.subTest(skill_id=skill["id"]):
                metadata = scanned[skill["id"]]
                self.assertEqual(metadata, self.by_id[skill["id"]])
                self.assertEqual(metadata["source_repo"], "mattpocock/skills")
                self.assertEqual(metadata["source_revision"], self.manifest["revision"])
                self.assertEqual(metadata["author"], "Matt Pocock")
                self.assertEqual(metadata["license"], "MIT")
                self.assertIn("mattpocock", metadata["tags"])
                self.assertEqual(
                    metadata["description"], source[skill["id"]]["description"]
                )

    def test_source_and_author_search_find_all_preserved_and_new_skills(self):
        expected = {
            skill["id"]
            for group in ("preserved", "imported")
            for skill in self.manifest[group]
        }
        for query in ("mattpocock/skills", "Matt Pocock"):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                VAS.cmd_search(Namespace(query=query, limit=100))
            for skill_id in expected:
                with self.subTest(query=query, skill_id=skill_id):
                    self.assertIn(f". {skill_id}", output.getvalue())

    def test_show_includes_author_source_and_license(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            VAS.cmd_show(Namespace(skill_id="code-review"))
        self.assertIn("Matt Pocock", output.getvalue())
        self.assertIn("mattpocock/skills", output.getvalue())
        self.assertIn("License:", output.getvalue())

    def test_pages_and_cli_use_the_same_generated_index(self):
        website = json.loads(
            (ROOT / "docs/skills.min.json").read_text(encoding="utf-8")
        )
        self.assertEqual(website, self.index)
        self.assertGreaterEqual(len(website), 2921)

    def test_pages_and_documentation_counts_match_the_catalog(self):
        counts = Counter(row["category"] for row in self.index)
        page = (ROOT / "docs/index.html").read_text(encoding="utf-8")
        for label, category in (("DevOps", "devops"), ("Development", "development")):
            self.assertIn(f"{label} ({counts[category]})", page)
        for filename in ("README.md", "README_EN.md", "docs/index.html"):
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn(f"{len(self.index):,}", text)
                if filename.endswith(".md"):
                    for label, category in (
                        ("Development", "development"),
                        ("DevOps", "devops"),
                        ("Testing & QA", "testing"),
                    ):
                        self.assertRegex(
                            text, rf"{label}\s*:\s*{counts[category]} skills"
                        )

    def test_imported_skills_can_be_installed_with_support_files(self):
        ids = [skill["id"] for skill in self.manifest["imported"]]
        for mode in ("copy", "link"):
            with tempfile.TemporaryDirectory(prefix="vas-mattpocock-") as temp:
                destination = Path(temp) / "skills"
                result = subprocess.run(
                    [
                        sys.executable, "-B", str(ROOT / "vas.py"), "install", *ids,
                        "--mode", mode, "--dest", str(destination),
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for skill in self.manifest["imported"]:
                    with self.subTest(mode=mode, skill_id=skill["id"]):
                        self.assertEqual(
                            (destination / skill["id"]).is_symlink(), mode == "link"
                        )
                    for file in skill["files"]:
                        with self.subTest(
                            mode=mode, skill_id=skill["id"], file=file["path"]
                        ):
                            self.assertEqual(
                                (destination / skill["id"] / file["path"]).read_bytes(),
                                (ROOT / "skills" / skill["id"] / file["path"]).read_bytes(),
                            )

    def test_pre_commit_instructions_use_installed_executables(self):
        text = (ROOT / "skills/setup-pre-commit/SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("npx ", text)
        self.assertIn("./node_modules/.bin/husky init", text)
        self.assertIn("./node_modules/.bin/lint-staged", text)


class ProvenanceMetadataTests(unittest.TestCase):
    def test_frontmatter_provenance_is_available_without_a_source_catalog(self):
        with tempfile.TemporaryDirectory(prefix="vas-metadata-") as temp:
            root = Path(temp)
            skill_md = root / "skills" / "example" / "SKILL.md"
            skill_md.parent.mkdir(parents=True)
            skill_md.write_text(
                "---\nname: example\ndescription: Example\ncategory: workflow\n"
                "tags: [workflow]\nsource_repo: mattpocock/skills\n"
                "author: Matt Pocock\nlicense: MIT\n---\n",
                encoding="utf-8",
            )
            with patch.object(VAS, "REPO_ROOT", root):
                metadata = VAS.extract_skill_metadata(
                    skill_md, "example", catalog_by_key={}, overrides={}
                )
            self.assertEqual(metadata["source_repo"], "mattpocock/skills")
            self.assertEqual(metadata["author"], "Matt Pocock")
            self.assertEqual(metadata["license"], "MIT")

    def test_missing_provenance_does_not_create_empty_fields(self):
        with tempfile.TemporaryDirectory(prefix="vas-metadata-") as temp:
            root = Path(temp)
            skill_md = root / "SKILL.md"
            skill_md.write_text(
                "---\nname: example\ndescription: Example\n---\n",
                encoding="utf-8",
            )
            with patch.object(VAS, "REPO_ROOT", root):
                metadata = VAS.extract_skill_metadata(
                    skill_md, "example", catalog_by_key={}, overrides={}
                )
            self.assertNotIn("source_repo", metadata)
            self.assertNotIn("author", metadata)
            self.assertNotIn("license", metadata)


if __name__ == "__main__":
    unittest.main()
