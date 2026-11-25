"""Exercise the production TorchEngine methods without loading speech models."""

import ast
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np


def engine_class(name):
    # Importing the server replaces explainer's package for its standalone env.
    # Compile the actual class instead, preserving test-process package state.
    source = Path(__file__).resolve().parents[1] / "tools/tts_server.py"
    tree = ast.parse(source.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == name)
    namespace = {"Engine": object, "np": np, "ROOT": Path("/voice-fixture"),
                 "LANG_NAME": {"en": "English", "zh": "Chinese"}}
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), "exec"), namespace)
    return namespace[name]


class SpeechBatchTests(unittest.TestCase):
    def engine(self, device):
        cls = engine_class("TorchEngine")
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


def test_mlx_length_groups_restore_order_and_recover_missing_takes():
    cls = engine_class("Engine")
    engine = cls.__new__(cls)
    engine.batch_size = 2
    engine.voice_options = lambda lang: {}
    texts = ["a", "four", "three", "zz", "123456"]
    groups, singles = [], []

    def batch(texts):
        groups.append(texts)
        # Return out of order. The backend occasionally yields empty audio.
        for i in (1, 0):
            data = [] if texts[i] == "four" else [len(texts[i])]
            yield SimpleNamespace(sequence_idx=i, audio=np.array(data))

    def take(text, lang, attempt):
        singles.append(text)
        return np.array([len(text)])

    engine.model = SimpleNamespace(batch_generate=batch)
    engine.take = take
    result = engine.takes(texts, "en", 0)
    assert groups == [["123456", "three"], ["four", "zz"]]
    assert singles == ["a", "four"]
    assert [row.item() for row in result] == list(map(len, texts))
    engine.takes(texts, "en", 1)
    assert singles[2:] == texts
