import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import md_links  # noqa: E402
import md_tables  # noqa: E402
import plugin_table  # noqa: E402
import pr_scope  # noqa: E402
import showcase_table  # noqa: E402
import skill_budget  # noqa: E402

GOOD = "| a | b |\n|---|:-:|\n| 1 | 2 |\n"


class TableTests(unittest.TestCase):
    def test_good_table(self):
        self.assertEqual(md_tables.check_text(GOOD), [])

    def test_double_pipe_row(self):
        self.assertTrue(md_tables.check_text("| a | b |\n|---|---|\n|| 1 | 2 |\n"))

    def test_column_mismatch(self):
        self.assertTrue(md_tables.check_text("| a | b | c |\n|---|---|\n| 1 | 2 | 3 |\n"))

    def test_empty_delimiter_cell(self):
        self.assertTrue(md_tables.check_text("| a | b |\n|---| |\n| 1 | 2 |\n"))

    def test_fenced_ignored(self):
        self.assertEqual(md_tables.check_text("```\n|| x\n```\n"), [])


class LinkTests(unittest.TestCase):
    def setUp(self):
        md_links._anchor_cache.clear()
        self.d = tempfile.TemporaryDirectory()
        self.addCleanup(self.d.cleanup)

    def write(self, name, text):
        p = os.path.join(self.d.name, name)
        open(p, "w").write(text)
        return p

    def test_slug(self):
        self.assertEqual(md_links.slugify("Hello, World! `x` (v2)"), "hello-world-x-v2")

    def test_ok_and_duplicate_heading(self):
        p = self.write("a.md", "# A\n## Same\n## Same\n[x](#a) [y](#same-1) [z](b.md)\n")
        self.write("b.md", "x")
        self.assertEqual(md_links.check_text(open(p).read(), p), [])

    def test_broken(self):
        p = self.write("a.md", "# A\n[x](#nope) [y](missing.md) [z](https://e.com/x) `[c](zzz.md)`\n")
        self.assertEqual(len(md_links.check_text(open(p).read(), p)), 2)

    def test_cross_file_anchor(self):
        self.write("b.md", "# Bee\n")
        p = self.write("a.md", "[ok](b.md#bee) [bad](b.md#ant)\n")
        self.assertEqual(len(md_links.check_text(open(p).read(), p)), 1)


class BudgetTests(unittest.TestCase):
    def test_over_and_under(self):
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            os.chdir(d)
            try:
                open("S.md", "w").write("one two three")
                cfg = os.path.join(d, "c.json")
                json.dump({"file": "S.md", "max_words": 3}, open(cfg, "w"))
                self.assertEqual(skill_budget.check(cfg), [])
                json.dump({"file": "S.md", "max_words": 2}, open(cfg, "w"))
                self.assertEqual(len(skill_budget.check(cfg)), 1)
            finally:
                os.chdir(cwd)


class ScopeTests(unittest.TestCase):
    def test_type(self):
        self.assertEqual(pr_scope.commit_type("docs(readme): x"), "docs")
        self.assertEqual(pr_scope.commit_type("feat!: x"), "feat")
        self.assertIsNone(pr_scope.commit_type("Update stuff"))

    def test_docs_pr_with_code_fails(self):
        self.assertTrue(pr_scope.scope_problems("docs: add sponsor", ["README.md", "forge/x.py"]))

    def test_docs_pr_clean(self):
        self.assertEqual(pr_scope.scope_problems("docs(x): y", ["README.md", "docs/a/b.md", "assets/i.png"]), [])

    def test_non_docs_title_unrestricted(self):
        self.assertEqual(pr_scope.scope_problems("feat: y", ["forge/x.py"]), [])

    def test_stacked_overlap(self):
        r = pr_scope.stacked_overlap(["a", "b"], [{"number": 5, "commits": ["b", "z"]}, {"number": 6, "commits": ["q"]}])
        self.assertEqual(r, {5: ["b"]})


def _plugin(i, access="public"):
    return {"id": i, "description": f"{i} desc", "source": f"org/plugin-{i}", "access": access, "npmCli": None}


class PluginTableTests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.cat = os.path.join(self.d, "catalog.json")
        self.readme = os.path.join(self.d, "README.md")
        with open(self.readme, "w") as f:
            f.write("intro\n<!-- plugins:start -->\nold\n<!-- plugins:end -->\noutro\n")

    def _cat(self, *plugins):
        with open(self.cat, "w") as f:
            json.dump({"schema": 1, "plugins": list(plugins)}, f)

    def _run(self, *flags):
        return plugin_table.main(["--catalog", self.cat, "--readme", self.readme, *flags])

    def _text(self):
        with open(self.readme) as f:
            return f.read()

    def test_write_then_check_clean(self):
        self._cat(_plugin("b"), _plugin("a", "private"))
        self.assertEqual(self._run("--check"), 1)
        self.assertEqual(self._run("--write"), 0)
        self.assertEqual(self._run("--check"), 0)
        t = self._text()
        self.assertTrue(t.startswith("intro\n") and t.endswith("outro\n"))
        self.assertIn("[a](https://github.com/org/plugin-a)", t)
        self.assertIn("`img2 add b --yes`", t)
        self.assertIn("**Private", t)
        self.assertLess(t.index("[a]"), t.index("[b]"))
        self.assertEqual(md_tables.check_text(t), [])

    def test_add_and_remove_change_table(self):
        self._cat(_plugin("a"))
        self._run("--write")
        self._cat(_plugin("a"), _plugin("c"))
        self.assertEqual(self._run("--check"), 1)
        self._run("--write")
        self.assertIn("img2 add c --yes", self._text())
        self._cat(_plugin("a"))
        self.assertEqual(self._run("--check"), 1)
        self._run("--write")
        self.assertNotIn("img2 add c", self._text())

    def test_missing_markers_and_bad_catalog(self):
        with open(self.readme, "w") as f:
            f.write("no markers\n")
        self._cat(_plugin("a"))
        self.assertEqual(self._run("--check"), 2)
        with open(self.cat, "w") as f:
            f.write("{}")
        self.assertEqual(self._run("--check"), 2)

    def test_pipe_in_description_escaped(self):
        p = _plugin("a")
        p["description"] = "x | y"
        self.assertIn("x \\| y", plugin_table.render([p]))


def _demo(i, date, status="final", version="v1.5.2"):
    return {"id": f"d{i}", "title": f"Demo {i}", "subjectClass": "object", "status": status,
            "updatedAt": date, "version": version, "url": f"https://x/#/demo/d{i}",
            "sourceUrl": f"https://x/src/d{i}.ts"}


class ShowcaseTableTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.cat = os.path.join(self.d, "demos.json")
        self.readme = os.path.join(self.d, "README.md")
        with open(self.readme, "w") as f:
            f.write("a\n<!-- showcase:start -->\nold\n<!-- showcase:end -->\nb\n")

    def _cat(self, *demos):
        with open(self.cat, "w") as f:
            json.dump({"schema": 1, "demos": list(demos)}, f)

    def _run(self, *flags):
        return showcase_table.main(["--catalog", self.cat, "--readme", self.readme, *flags])

    def test_newest_final_only_and_limit(self):
        demos = [_demo(i, f"2026-01-{i + 1:02d}") for i in range(14)] + [_demo(99, "2026-12-31", "placeholder")]
        table = showcase_table.render(demos, limit=12)
        self.assertNotIn("Demo 99", table)
        self.assertIn("Demo 13", table)
        self.assertNotIn("Demo 1 |", table)
        self.assertLess(table.index("Demo 13"), table.index("Demo 12"))
        self.assertEqual(len(table.splitlines()), 14)
        self.assertEqual(md_tables.check_text(table + "\n"), [])

    def test_missing_version_and_pipe(self):
        d = _demo(1, "2026-01-01", version=None)
        d["title"] = "Knife | Fade"
        table = showcase_table.render([d])
        self.assertIn("| — |", table)
        self.assertIn("Knife \\| Fade", table)

    def test_write_check_and_new_demo(self):
        self._cat(_demo(1, "2026-01-01"))
        self.assertEqual(self._run("--check"), 1)
        self.assertEqual(self._run("--write"), 0)
        self.assertEqual(self._run("--check"), 0)
        self._cat(_demo(1, "2026-01-01"), _demo(2, "2026-02-01"))
        self.assertEqual(self._run("--check"), 1)

    def test_bad_catalog(self):
        with open(self.cat, "w") as f:
            f.write('{"demos": [{"id": "x"}]}')
        self.assertEqual(self._run("--check"), 2)


if __name__ == "__main__":
    unittest.main()
