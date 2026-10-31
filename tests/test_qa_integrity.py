"""Coverage/provenance regressions use fixtures instead of renders or neural TTS."""

import hashlib
import importlib
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import qa_audio, qa_report, qa_series


class PreflightVerdictTests(unittest.TestCase):
    def test_changed_measurement_keeps_approved_latin_data_in_chinese_caption(self):
        from explainer import lang, zh_text

        table = json.loads((qa_series.ROOT / "videos/ai/ai_text_zh.json").read_text())
        with patch.object(lang, "LANG", "zh"), patch.object(zh_text, "_TABLE", table), \
                patch.object(zh_text, "_BY_NUMBERS", None):
            targets = {zh_text._NUM.sub("\0", zh_text.translate(s)) for s in table["strings"]}
            caption = r"Qwen3-4B on this paragraph alone: \ \texttt{telephone} costs $13.0$ bits"
            translated = zh_text.translate(caption)
            self.assertTrue(qa_series.approved_numeric_caption(translated, targets))
            self.assertFalse(qa_series.approved_numeric_caption(caption, targets))
            self.assertFalse(qa_series.approved_numeric_caption(translated + " untranslated extra words", targets))

    def test_warning_bearing_legacy_pass_is_review_required(self):
        result = {"status": "passed", "warnings": [{"kind": "text-outside-frame"}]}
        self.assertFalse(qa_series.preflight_passed(result))
        self.assertEqual(qa_series.check_status(result), "needs-review")
        self.assertTrue(qa_series.runtime_completed(result))

    def test_warned_render_remains_usable_but_not_a_clean_preflight(self):
        result = {"status": "needs-review", "warnings": [{"kind": "dead-air-review"}]}
        self.assertTrue(qa_series.runtime_completed(result))
        self.assertFalse(qa_series.preflight_passed(result))

    def test_resume_keeps_warned_capture_but_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            folder = out / "ai1/en/Hook"
            folder.mkdir(parents=True)
            (folder / "result.json").write_text(json.dumps({"video": "ai1", "scene": "Hook", "lang": "en",
                "fingerprint": "now", "inputs": {}, "status": "passed", "warnings": [{}], "frames": []}))
            with patch.object(qa_series, "OUT", out), patch.object(qa_series, "fingerprint", return_value="now"), \
                    patch.object(qa_series.subprocess, "Popen") as render, \
                    patch.object(sys, "argv", ["qa_series.py", "ai1", "--only", "Hook", "--resume"]):
                self.assertEqual(qa_series.main(), 1)
                render.assert_not_called()
            summary = json.loads((out / "summary_en.json").read_text())
            self.assertEqual(summary[0]["status"], "needs-review")

    def test_crashed_motion_worker_stays_in_motion_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            with patch.object(qa_series, "OUT", out), patch.object(qa_series, "fingerprint", return_value="now"), \
                    patch.object(qa_series.subprocess, "Popen") as render, \
                    patch.object(sys, "argv", ["qa_series.py", "ai1", "--only", "Hook", "--motion"]):
                render.return_value.wait.return_value = 1
                self.assertEqual(qa_series.main(), 1)
            result = json.loads((out / "ai1/en/Hook_motion/result.json").read_text())
            self.assertEqual(result["mode"], "motion")
            summary = json.loads((out / "summary_en_motion.json").read_text())
            self.assertEqual(summary[0]["status"], "crashed")


class AudioVerdictTests(unittest.TestCase):
    def test_missing_and_incomplete_audio_do_not_pass(self):
        self.assertEqual(qa_audio.audio_status({"source_current": False}), "stale-capture")
        self.assertEqual(qa_audio.audio_status({"source_current": True, "expected_lines": 2,
                                               "lines": [{}], "issues": []}), "failed")

    def test_signal_failure_and_asr_lead_require_follow_up(self):
        report = {"source_current": True, "expected_lines": 1, "lines": [{}], "issues": ["silence"]}
        self.assertEqual(qa_audio.audio_status(report), "failed")
        report.update(issues=[], lines=[{"asr_review_leads": [{"text": "misheard"}]}])
        self.assertEqual(qa_audio.audio_status(report), "needs-review")
        report["lines"] = [{}]
        self.assertEqual(qa_audio.audio_status(report), "completed")

    def test_current_capture_is_preferred_over_newer_stale_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            current, stale = Path(tmp) / "current", Path(tmp) / "stale"
            current.touch()
            stale.touch()
            os.utime(current, ns=(1, 1))
            os.utime(stale, ns=(2, 2))
            records = [(current, {"status": "needs-review", "fingerprint": "now", "narration": [{}]}),
                       (stale, {"status": "passed", "fingerprint": "old", "narration": [{}]})]
            self.assertEqual(qa_audio.select_capture(records, "now", lambda _: True)[0], current)
            self.assertIsNone(qa_audio.select_capture(records, "now", lambda _: False))

    def test_missing_capture_is_recorded_and_command_fails_without_synthesis(self):
        # No Manim or neural model is needed to report a missing prerequisite.
        from explainer import tts

        with tempfile.TemporaryDirectory() as tmp, patch.object(qa_series, "OUT", Path(tmp)), \
                patch.object(qa_series, "fingerprint", return_value="current"), \
                patch.object(tts, "BACKEND", "server"), patch.object(tts, "synthesize") as synthesize, \
                patch.dict(sys.modules, {"soundfile": types.SimpleNamespace()}), \
                patch.object(sys, "argv", ["qa_audio.py", "ai1", "--only", "Hook"]), \
                patch.dict(os.environ, {}, clear=False):
            self.assertEqual(qa_audio.main(), 1)
            synthesize.assert_not_called()
            report = json.loads((Path(tmp) / "ai1/en/Hook/audio_result.json").read_text())
            self.assertEqual(report["status"], "missing-capture")
            self.assertEqual(report["listening_review"], "pending")
            summary = json.loads((Path(tmp) / "ai1/en/audio_summary.json").read_text())
            self.assertEqual(summary, [{"scene": "Hook", "status": "missing-capture"}])

    def test_stale_capture_is_recorded_without_synthesis(self):
        from explainer import tts

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            folder = out / "ai1/en/Hook"
            folder.mkdir(parents=True)
            (folder / "result.json").write_text(json.dumps({"status": "passed", "fingerprint": "old",
                                                           "inputs": {}, "narration": [{"raw": "A line"}]}))
            with patch.object(qa_series, "OUT", out), patch.object(qa_series, "fingerprint", return_value="now"), \
                    patch.object(tts, "BACKEND", "server"), patch.object(tts, "synthesize") as synthesize, \
                    patch.dict(sys.modules, {"soundfile": types.SimpleNamespace()}), \
                    patch.object(sys, "argv", ["qa_audio.py", "ai1", "--only", "Hook"]), \
                    patch.dict(os.environ, {}, clear=False):
                self.assertEqual(qa_audio.main(), 1)
                synthesize.assert_not_called()
            report = json.loads((folder / "audio_result.json").read_text())
            self.assertEqual(report["status"], "stale-capture")

    def test_waveform_failure_affects_exit_status_and_completed_audio_keeps_review_pending(self):
        import numpy as np
        from explainer import lang, tts

        for samples, expected_status, expected_exit in [(np.zeros(100), "failed", 1),
                                                        (np.full(100, .1), "completed", 0)]:
            with self.subTest(status=expected_status), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp)
                folder = out / "ai1/en/Hook"
                folder.mkdir(parents=True)
                (folder / "result.json").write_text(json.dumps({"status": "passed", "fingerprint": "now",
                    "inputs": {}, "narration": [{"raw": "A line"}]}))
                utterance = types.SimpleNamespace(audio_path=out / "audio.wav", duration=1,
                    words=[types.SimpleNamespace(start=0, end=1)])
                with patch.object(qa_series, "OUT", out), patch.object(qa_audio, "ROOT", out), \
                        patch.object(qa_series, "fingerprint", return_value="now"), \
                        patch.object(tts, "BACKEND", "server"), patch.object(tts, "CACHE_DIR", out), \
                        patch.object(tts, "synthesize", return_value=utterance), \
                        patch.object(tts, "cache_key", return_value=("unused", "A line")), \
                        patch.object(lang, "translate", return_value="A line"), \
                        patch.dict(sys.modules, {"soundfile": types.SimpleNamespace(read=lambda _: (samples, 100))}), \
                        patch.object(sys, "argv", ["qa_audio.py", "ai1", "--only", "Hook"]), \
                        patch.dict(os.environ, {}, clear=False):
                    self.assertEqual(qa_audio.main(), expected_exit)
                report = json.loads((folder / "audio_result.json").read_text())
                self.assertEqual(report["status"], expected_status)
                self.assertEqual(report["listening_review"], "pending")


class ReportCoverageTests(unittest.TestCase):
    def test_audio_requires_complete_unflagged_lines(self):
        self.assertFalse(qa_report.audio_checks_completed({"expected_lines": 0, "lines": []}))
        self.assertFalse(qa_report.audio_checks_completed({"expected_lines": 2, "lines": [{}]}))
        self.assertFalse(qa_report.audio_checks_completed({"expected_lines": 1, "lines": [
            {"asr_review_leads": [{}]}]}))
        self.assertTrue(qa_report.audio_checks_completed({"expected_lines": 1, "lines": [{}]}))

    def test_audio_provenance_is_rechecked_after_source_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "capture.json"
            raw = json.dumps({"fingerprint": "now", "inputs": {}, "status": "needs-review"}).encode()
            source.write_bytes(raw)
            audio = {"source_current": True, "input_record": str(source),
                     "input_sha256": hashlib.sha256(raw).hexdigest()}
            self.assertTrue(qa_report.audio_evidence_current(audio, "now"))
            source.write_text("{}")
            self.assertFalse(qa_report.audio_evidence_current(audio, "now"))

    def test_report_does_not_count_warning_pass_as_clean_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            folder = out / "ai1/en/Hook"
            folder.mkdir(parents=True)
            (folder / "result.json").write_text(json.dumps({"status": "passed", "fingerprint": "now",
                "inputs": {}, "warnings": [{"kind": "clipped"}]}))
            manifest = types.SimpleNamespace(TITLE="Test part", SCENES=[("hook", "Hook", "Chapter")])
            with patch.object(qa_report, "OUT", out), patch.object(qa_report, "all_videos", return_value=["ai1"]), \
                    patch.object(qa_report, "fingerprint", return_value="now"), \
                    patch.object(importlib, "import_module", return_value=manifest):
                qa_report.main()
            page = (out / "index.html").read_text()
            self.assertIn("0 current cases without automated warnings", page)
            self.assertIn("needs-review", page)
            self.assertIn("Silent motion renders: 0/2 attempted", page)
            self.assertIn("Full playback review, listening, and production approval remain pending", page)


if __name__ == "__main__":
    unittest.main()
