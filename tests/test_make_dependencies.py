import unittest
from unittest.mock import patch

from tools.make import compute, depends_on


class DependencyTests(unittest.TestCase):
    def test_classical_ml_declares_raw_corpus_prerequisite(self):
        self.assertEqual(depends_on("ai6")["ai1"], {"corpus"})

    def test_selected_pages_schedule_only_corpus_before_pages_once(self):
        with patch("tools.make.run") as run:
            done = set()
            compute("ai6", done, {"pages"})
            compute("ai6", done, {"pages"})
        commands = [call.args[0][2:] for call in run.call_args_list]
        self.assertEqual(commands, [
            ["videos.ai.ai1.compute", "corpus"],
            ["videos.ai.ai6.compute", "pages"],
        ])

    def test_full_classical_ml_schedules_corpus_before_own_compute(self):
        with patch("tools.make.run") as run:
            compute("ai6", set())
        commands = [call.args[0][2:] for call in run.call_args_list]
        self.assertEqual(commands, [
            ["videos.ai.ai1.compute", "corpus"],
            ["videos.ai.ai6.compute"],
        ])

    def test_finale_precomputes_models_for_its_scoreboard(self):
        deps = depends_on("ai31")
        self.assertIn("scoreboard", deps["ai1"])
        self.assertIn("kn", deps["ai7"])
        self.assertIn("lm", deps["ai9"])
        self.assertIn("tf", deps["ai13"])


if __name__ == "__main__":
    unittest.main()
