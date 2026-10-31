"""Exercise the production TorchEngine methods without loading speech models."""

import ast
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np


def torch_engine_class():
    # Importing the server replaces explainer's package for its standalone env.
    # Compile the actual class instead, preserving test-process package state.
    source = Path(__file__).resolve().parents[1] / "tools/tts_server.py"
    tree = ast.parse(source.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "TorchEngine")
    namespace = {"Engine": object, "np": np, "ROOT": Path("/voice-fixture"),
                 "LANG_NAME": {"en": "English", "zh": "Chinese"}}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), namespace)
    return namespace["TorchEngine"]


class SpeechBatchTests(unittest.TestCase):
    def engine(self, device):
        cls = torch_engine_class()
        engine = cls.__new__(cls)
        engine.device, engine.sr = device, 24000
        engine.profile = {"voices": {"en": {"ref_audio": "reference.wav", "ref_text": "same voice",
                                             "params": {"temperature": .7}}}}
        calls = []

        def generate(**kwargs):
            calls.append(kwargs)
            return [np.full(len(text), i) for i, text in enumerate(kwargs["text"])], 24000

        engine.model = SimpleNamespace(generate_voice_clone=generate)
        return engine, calls

    def test_cpu_chunks_keep_order_and_never_share_an_inference_batch(self):
        engine, calls = self.engine("cpu")
        texts = ["first sentence", "a longer second sentence", "last"]
        result = engine.takes(texts, "en", 0)
        self.assertEqual([len(wave) for wave in result], list(map(len, texts)))
        self.assertEqual([call["text"] for call in calls], [[text] for text in texts])
        self.assertTrue(all(call["ref_text"] == "same voice" for call in calls))
        self.assertTrue(all(call["language"] == ["English"] for call in calls))
        self.assertTrue(all(call["temperature"] == .7 for call in calls))

    def test_gpu_retains_batching_and_retry_temperature(self):
        engine, calls = self.engine("cuda:0")
        result = engine.takes(["first", "second"], "en", 1)
        self.assertEqual(len(result), 2)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["text"], ["first", "second"])
        self.assertAlmostEqual(calls[0]["temperature"], .6)
