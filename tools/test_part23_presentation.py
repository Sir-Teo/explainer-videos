"""No-model regressions: optional execution guards, scoped credits and rate units."""
from pathlib import Path
from types import SimpleNamespace
import ast
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from videos.ai.ai23 import presentation as p


class PresentationContracts(unittest.TestCase):
    @staticmethod
    def method_nodes(filename, class_name, method_name):
        root = Path(__file__).resolve().parents[1] / "videos/ai/ai23"
        tree = ast.parse((root/filename).read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name)
        return next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == method_name)

    @staticmethod
    def spoken_expression(method):
        return next(n.args[0] for n in ast.walk(method) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == "voiceover")

    @staticmethod
    def evaluate(node, values):
        return eval(compile(ast.Expression(node), "<source narration only>", "eval"), {}, values)

    def test_optional_record_never_discovers_or_runs_assets(self):
        with patch.object(Path, "exists", side_effect=AssertionError("asset discovery")), \
             patch.object(Path, "read_text", side_effect=AssertionError("asset read")), \
             patch.object(subprocess, "run", side_effect=AssertionError("subprocess")):
            record = p.narrator_presentation()
        self.assertFalse(record["available"])
        self.assertEqual(record["execution"], "not_run")
        self.assertFalse(any(k in record for k in ["ref_codes", "gen_codes", "ref_mel", "seconds"]))

    def test_legacy_optional_producer_stops_before_import_or_asset_access(self):
        source = Path(__file__).resolve().parents[1] / "videos/ai/ai23/compute.py"
        fn = next(n for n in ast.parse(source.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == "compute_narrator")
        namespace = {"os": SimpleNamespace(environ={})}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), str(source), "exec"), namespace)
        with self.assertRaisesRegex(RuntimeError, "AI23_NARRATOR_EXECUTE=1"):
            namespace["compute_narrator"]()

    def test_silent_credit_cannot_claim_kokoro_or_speech(self):
        with patch.object(p.tts, "BACKEND", "silent"), patch.object(p.tts, "narration_credit", side_effect=AssertionError("production credit")):
            self.assertIn("Silent QA", p.narration_credit())
            self.assertIn("no speech", p.narration_credit())
            self.assertNotIn("Kokoro", p.narration_credit())
            self.assertTrue(p.is_silent_qa())

    def test_other_backend_credit_is_delegated_unchanged(self):
        with patch.object(p.tts, "BACKEND", "server"), patch.object(p.tts, "narration_credit", return_value="selected-model"):
            self.assertEqual(p.narration_credit(), "selected-model")
            self.assertFalse(p.is_silent_qa())

    def test_nominal_rate_counts_codebook_indices(self):
        config = p.published_narrator_config()
        self.assertEqual(config["frame_hz"] * config["codebooks"], 200)
        self.assertEqual(config["codebook_size"], 2048)

    def test_measured_budget_requires_accepted_complete_bundle(self):
        for data in [{}, {"products": {"whisper": {}}}, {"numerical_acceptance": {"status": "passed"}, "products": {"whisper": {}}}]:
            with self.assertRaises(ValueError):p.budget_products(data)

    def test_scenes_never_load_optional_narrator_or_old_budget_products(self):
        root = Path(__file__).resolve().parents[1] / "videos/ai/ai23"
        for name in ["s14_tts.py", "s17_omni.py"]:
            tree = ast.parse((root/name).read_text())
            keys = [n.args[0].value for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                    and n.func.id == "load" and n.args and isinstance(n.args[0], ast.Constant)]
            self.assertNotIn("narrator", keys)
            self.assertFalse(set(keys) & {"whisper", "codec"})

    def test_both_narrator_status_branches_translate_with_bookmarks(self):
        from explainer.zh_templates import Translator
        from explainer.lang import BOOKMARK
        method = self.method_nodes("s14_tts.py", "TTS", "narrator")
        expression = self.spoken_expression(method)
        status_node = next(n.value for n in ast.walk(method) if isinstance(n, ast.Assign)
                           and any(isinstance(t, ast.Name) and t.id == "status" for t in n.targets))
        own = "No verified narrator-code result is selected for this optional experiment; codec execution and Qwen synthesis were not run."
        tr = Translator("ai23")
        for silent in [True, False]:
            status = self.evaluate(status_node, {"is_silent_qa": lambda: silent, "narration_credit": lambda: "selected-model"})
            en = self.evaluate(expression, {"own": own, "status": status})
            zh = tr(en)
            self.assertIsNotNone(zh)
            self.assertEqual(BOOKMARK.findall(en), BOOKMARK.findall(zh))
            self.assertNotIn("isn't installed", en)
            self.assertNotIn("No verified", zh)
            self.assertNotIn("This copy uses", zh)
            if silent:self.assertIn("未生成语音", zh)
            else:self.assertIn("selected-model", zh)

    def test_optional_server_workflow_is_not_claimed_as_execution(self):
        from explainer.zh_templates import Translator
        from explainer.lang import BOOKMARK
        method = self.method_nodes("s13_whisper.py", "Whisper", "today")
        expression = self.spoken_expression(method)
        workflow_node = next(n.value for n in ast.walk(method) if isinstance(n, ast.Assign)
                             and any(isinstance(t, ast.Name) and t.id == "workflow" for t in n.targets))
        tr = Translator("ai23")
        for silent in [True, False]:
            workflow = self.evaluate(workflow_node, {"is_silent_qa": lambda: silent})
            en = self.evaluate(expression, {"workflow": workflow})
            zh = tr(en)
            self.assertIsNotNone(zh)
            self.assertEqual(BOOKMARK.findall(en), BOOKMARK.findall(zh))
            self.assertNotIn("It also works on this series", en)
            self.assertNotIn("server workflow", zh)
            if silent:self.assertIn("时序是估计值", zh)

    def test_part23_credit_imports_use_scoped_status(self):
        root = Path(__file__).resolve().parents[1] / "videos/ai/ai23"
        for source in root.glob("s??_*.py"):
            for node in ast.walk(ast.parse(source.read_text())):
                if isinstance(node, ast.ImportFrom) and node.module == "explainer":
                    self.assertNotIn("narration_credit", [a.name for a in node.names])

    def test_dense_hook_map_and_objectives_do_not_crossfade(self):
        method = self.method_nodes("s01_hook.py", "Hook", "plan")
        plays = [n for n in ast.walk(method) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute) and n.func.attr == "play"]
        def has(call, animation, target):
            return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == animation
                       and n.args and isinstance(n.args[0], ast.Name) and n.args[0].id == target
                       for n in ast.walk(call))
        out = next(i for i, call in enumerate(plays) if has(call, "FadeOut", "smap"))
        incoming = next(i for i, call in enumerate(plays) if has(call, "FadeIn", "obj"))
        self.assertLess(out, incoming, "Clear the dense map before revealing objectives")

    def test_hook_question_has_no_duplicate_roadmap_layer(self):
        method = self.method_nodes("s01_hook.py", "Hook", "question")
        copies = [n for n in ast.walk(method) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute) and n.func.attr == "copy"
                  and isinstance(n.func.value, ast.Name) and n.func.value.id == "path"]
        self.assertFalse(copies, "A static roadmap copy ghosts behind the shifted reveal")


if __name__ == "__main__":unittest.main(verbosity=2)
