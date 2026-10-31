import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from explainer.ai.cache import Cache
from videos.ai.ai14 import compute, lm


class LineageCacheTests(unittest.TestCase):
    def test_concurrent_consumers_train_a_family_member_once(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Cache("qa-lineage")
            cache.dir = Path(directory)
            calls = []
            start = threading.Barrier(2)

            def train():
                calls.append("trained")
                time.sleep(0.05)
                (cache.dir / "model.pt").write_text("complete weights")
                return {"name": "model"}

            def consume():
                start.wait()
                return compute._trained("model")

            def load(name, folder):
                self.assertTrue(cache.path(name).exists())
                return (folder / f"{name}.pt").read_text()

            with patch.object(compute, "CACHE", cache), patch.object(compute, "ITEMS", {"model": train}), \
                    patch.object(lm, "load_trained", side_effect=load), ThreadPoolExecutor(2) as pool:
                futures = [pool.submit(consume) for _ in range(2)]
                self.assertEqual([f.result() for f in futures], ["complete weights"] * 2)
            self.assertEqual(calls, ["trained"])

    def test_interrupted_retraining_withdraws_the_old_completion_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Cache("qa-lineage")
            cache.dir = Path(directory)
            cache.save("model", {"name": "old"})
            with patch.object(compute, "CACHE", cache), patch.object(lm, "train", side_effect=RuntimeError("interrupted")):
                with self.assertRaisesRegex(RuntimeError, "interrupted"):
                    compute._train("model", "gpt", {})
            self.assertFalse(cache.path("model").exists())


if __name__ == "__main__":
    unittest.main()
