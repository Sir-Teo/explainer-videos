"""Tests for Part 41's version-control, build, dependency and delivery instruments (explainer/cs/vcs)."""

import os
import subprocess
import tempfile
import unittest

from explainer.cs.vcs import build, ci, deps, git


class TestGit(unittest.TestCase):
    def test_ids_match_real_git(self):
        files = {"a.txt": b"hello\n", "d/b.txt": b"world\n"}
        s = git.Store()
        root = s.write_files(files)
        commit = s.commit(root, [], "m")
        env = dict(os.environ, GIT_AUTHOR_NAME="Ada", GIT_AUTHOR_EMAIL="ada@example.com", GIT_COMMITTER_NAME="Ada",
                   GIT_COMMITTER_EMAIL="ada@example.com", GIT_AUTHOR_DATE="1700000000 +0000",
                   GIT_COMMITTER_DATE="1700000000 +0000", GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
        with tempfile.TemporaryDirectory() as t:
            def g(*a):
                return subprocess.run(["git", "-C", t, "-c", "commit.gpgsign=false", *a], capture_output=True,
                                      text=True, env=env, check=True).stdout.strip()
            g("init", "-q")
            for p, d in files.items():
                os.makedirs(os.path.join(t, os.path.dirname(p)), exist_ok=True)
                with open(os.path.join(t, p), "wb") as f:
                    f.write(d)
            g("add", "-A")
            g("commit", "-q", "-m", "m")
            self.assertEqual(g("rev-parse", "HEAD^{tree}"), root)
            self.assertEqual(g("rev-parse", "HEAD"), commit)

    def test_corruption_detected(self):
        self.assertTrue(git.corruption_demo()["detected"])

    def test_merge_bases_criss_cross(self):
        self.assertEqual(git.merge_bases(git.criss_cross(), 5, 6), [1, 2])

    def test_bisect_steps(self):
        for n in (2, 10, 1000):
            for bad in (1, n // 2, n - 1):
                r = git.bisect(n, bad)
                self.assertEqual(r["first_bad"], bad)
                self.assertLessEqual(r["steps"], (n - 1).bit_length())

    def test_merge3(self):
        base = list("abcde")
        out, c = git.merge3(base, list("aBcde"), list("abcDe"))
        self.assertEqual((out, c), (list("aBcDe"), 0))
        out, c = git.merge3(base, list("aXcde"), list("aYcde"))
        self.assertEqual(c, 1)

    def test_edit_graph(self):
        e = git.edit_graph()
        self.assertEqual((e["D"], e["lcs"]), (5, 4))


class TestBuild(unittest.TestCase):
    def test_scenarios(self):
        rows = {r["edit"]: r for r in build.scenarios(n=40, headers=5)["rows"]}
        self.assertEqual(rows["nothing changed"]["make"], 0)
        self.assertEqual(rows["a comment in one source"]["traces"], 1)
        self.assertEqual(rows["every file touched \\ (fresh checkout)"]["traces"], 0)

    def test_shared_cache(self):
        r = build.shared_cache_story(n=30, headers=4)["rows"]
        self.assertEqual(r[1]["ran"], 0)
        self.assertEqual(r[3]["ran"], 0)

    def test_brent(self):
        p = build.parallel_times(n=50)
        for row in p["rows"]:
            self.assertLessEqual(row["lower"] - 1e-9, row["time"])
            self.assertLessEqual(row["time"], row["upper"] + 1e-9)


class TestDeps(unittest.TestCase):
    def test_missing_packages_are_unsatisfiable(self):
        u = deps.Universe({"app": {1: [("missing", {1})]}})
        for root in ([("missing", {1})], [("app", {1})]):
            self.assertIsNone(u.solve(root)[0])
            self.assertIsNone(deps.backtracking_trace(u, root)["result"])
        for literal in (0, 3, -3):
            with self.assertRaises(ValueError):
                deps.from_3sat(2, [[literal]])

    def test_diamond(self):
        u, r = deps.diamond()
        self.assertEqual(u.solve(r)[0]["B"], 11)

    def test_reduction(self):
        sat = [[1, -2, 3], [-1, 2, -3], [2, 3, -4]]
        u, r = deps.from_3sat(4, sat)
        ch = u.solve(r)[0]
        self.assertTrue(deps.check_assignment(sat, ch))
        unsat = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
        u2, r2 = deps.from_3sat(2, unsat)
        self.assertIsNone(u2.solve(r2)[0])


class TestCi(unittest.TestCase):
    def test_queue_lands_all_good_changes(self):
        r = ci.merge_queue(8, p_bad=0.05, changes=2000)
        self.assertEqual(r["landed"] + r["rejected"], 2000)

    def test_canary_power_grows(self):
        c = ci.canary(requests=(1000, 100000), trials=500)
        self.assertLess(c["rows"][0]["power"], c["rows"][1]["power"])


if __name__ == "__main__":
    unittest.main()
