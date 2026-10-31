import unittest

from tools.make import depends_on


class DependencyTests(unittest.TestCase):
    def test_finale_precomputes_models_for_its_scoreboard(self):
        deps = depends_on("ai31")
        self.assertIn("scoreboard", deps["ai1"])
        self.assertIn("kn", deps["ai7"])
        self.assertIn("lm", deps["ai9"])
        self.assertIn("tf", deps["ai13"])


if __name__ == "__main__":
    unittest.main()
