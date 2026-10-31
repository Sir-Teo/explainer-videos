import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import torch

from explainer.ai import novels
from explainer.lm import pocket


class NovelsCacheTests(unittest.TestCase):
    def test_concurrent_base_requests_train_once_and_publish_metadata_before_weights(self):
        ready = threading.Barrier(2)

        def train(*args, **kwargs):
            time.sleep(0.05)
            return {"score": 1, "_model": torch.nn.Linear(1, 1), "_opts": []}

        def request():
            ready.wait()
            return novels.train_base()

        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            replace = Path.replace
            metadata_at_publication = []

            def publish(path, target):
                if Path(target) == out / "base.pt":
                    metadata_at_publication.append((out / "base.json").exists())
                return replace(path, target)

            with patch.object(novels, "OUT", out), \
                    patch.object(novels, "tokenizer", return_value=SimpleNamespace(get_vocab_size=lambda: 16)), \
                    patch.object(novels, "token_arrays", return_value=(np.arange(8), np.arange(4))), \
                    patch.object(pocket, "TokenStream"), patch.object(pocket, "train", side_effect=train) as engine, \
                    patch.object(Path, "replace", new=publish):
                with ThreadPoolExecutor(max_workers=2) as pool:
                    results = list(pool.map(lambda _: request(), range(2)))
                self.assertEqual(engine.call_count, 1)
                self.assertEqual(results[0], results[1])
                self.assertTrue((out / "base.json").exists())
                self.assertTrue((out / "base.pt").exists())
                self.assertEqual(results[0]["train_tokens"], 8)
                self.assertEqual(metadata_at_publication, [True])


if __name__ == "__main__":
    unittest.main()
