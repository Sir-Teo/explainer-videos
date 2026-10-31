import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

import numpy as np

from explainer import tts


class SpeechCacheTests(unittest.TestCase):
    def test_simultaneous_first_use_synthesizes_once(self):
        ready = threading.Barrier(2)

        def synthesize(_):
            time.sleep(0.05)
            return np.ones(2400, dtype=np.float32) * 0.1, [("hello", 0, 0.1)]

        def request():
            ready.wait()
            return tts.synthesize("hello")

        with tempfile.TemporaryDirectory() as directory:
            with patch.object(tts, "CACHE_DIR", Path(directory)), patch.object(tts, "BACKEND", "silent"), \
                    patch.object(tts, "_synth_silent", side_effect=synthesize) as engine:
                with ThreadPoolExecutor(max_workers=2) as pool:
                    results = list(pool.map(lambda _: request(), range(2)))
                self.assertEqual(engine.call_count, 1)
                self.assertEqual(results[0].audio_path, results[1].audio_path)
                self.assertEqual(results[0].duration, results[1].duration)
                self.assertEqual(results[0].words, results[1].words)


if __name__ == "__main__":
    unittest.main()
