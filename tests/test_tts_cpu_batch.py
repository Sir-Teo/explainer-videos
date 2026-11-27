"""Exercise the production TorchEngine methods without loading speech models."""

import ast
import __future__
import re
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest


def server_definitions(*names, **values):
    # Importing the standalone server installs a lightweight explainer package.
    # Load the production definitions without replacing the test process's package.
    source = Path(__file__).resolve().parents[1] / "tools/tts_server.py"
    tree = ast.parse(source.read_text())
    nodes = [node for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef))
             and node.name in names]
    namespace = {"Engine": object, "np": np, "re": re, "ROOT": Path("/voice-fixture"),
                 "LANG_NAME": {"en": "English", "zh": "Chinese"}, **values}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), "exec",
                 flags=__future__.annotations.compiler_flag), namespace)
    return namespace


def engine_class(name):
    return server_definitions(name)[name]


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


@pytest.mark.parametrize("sentence", [
    "C. P. E. Bach's sonata of 1765 stays inside the old compass.",
    "R. H. M. Bosanquet's keyboard put fifty-three steps under the fingers.",
    "In 1963 Nazir Jairazbhoy and A. W. Stone measured the intonation.",
    "W. C. Handy published The Memphis Blues in 1912 and St. Louis Blues in 1914.",
])
def test_narration_keeps_initials_with_names_and_preserves_note_boundaries(sentence):
    split = server_definitions("sentences", L=SimpleNamespace(norm=lambda text: text))["sentences"]
    text = f"{sentence} The piece begins on C. Then the next passage starts."
    assert split(text, "en", 260) == [
        (sentence, "sentence"), ("The piece begins on C.", "sentence"),
        ("Then the next passage starts.", "sentence"),
    ]
    assert split("第一句。第二句。", "zh", 90) == [("第一句。", "sentence"), ("第二句。", "sentence")]


@pytest.mark.parametrize("retry_recovers", [True, False])
def test_mlx_empty_generation_retries_without_reaching_asr(tmp_path, retry_recovers):
    normalizer = SimpleNamespace(norm=lambda text: text, tokens=lambda text, lang: text.split())
    server = server_definitions(
        "Engine", "sentences", "trim", "narrate",
        L=normalizer, PAUSE={"sentence": 0.38, "clause": 0.22}, QA_LOG=tmp_path / "qa.jsonl",
        comparable=lambda text, lang: text, similarity=lambda left, right: float(left == right),
    )
    engine = server["Engine"].__new__(server["Engine"])
    engine.sr, engine.batch_size = 24000, 1
    engine.profile = {"name": "test"}
    engine.voice_options = lambda lang: {"temperature": 0.7}
    audio = np.full(2400, 0.2, dtype=np.float32)
    generated, transcribed, aligned = [], [], []

    def generate(text, temperature):
        generated.append((text, temperature))
        if retry_recovers and len(generated) == 2:
            yield SimpleNamespace(audio=audio)

    def transcribe(samples, sr, lang):
        transcribed.append(samples)
        return "Listen."

    def align(samples, sr, sentence, lang):
        aligned.append(samples)
        return [("Listen.", 0.0, 0.10)]

    engine.model = SimpleNamespace(generate=generate)
    checker = SimpleNamespace(transcribe=transcribe, align=align)
    if retry_recovers:
        samples, marks = server["narrate"](engine, checker, "Listen.", "en", max_tries=2)
        assert transcribed == aligned and len(aligned) == 1
        np.testing.assert_array_equal(samples[2880:5280], audio)
        assert marks == [("Listen.", 0.12, 0.22)]
    else:
        with pytest.raises(RuntimeError, match="No usable narration after 2 takes for 'Listen.'"):
            server["narrate"](engine, checker, "Listen.", "en", max_tries=2)
        assert not transcribed and not aligned
    assert [label for label, _ in generated] == ["Listen.", "Listen."]
    assert [temperature for _, temperature in generated] == pytest.approx([0.7, 0.6])
