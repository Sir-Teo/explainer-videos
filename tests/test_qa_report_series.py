"""The philosophy evidence index must use its own manifests and destination."""

import hashlib
import json
from types import SimpleNamespace
from unittest.mock import patch

from tools import qa_report


def test_philosophy_report_uses_requested_series(tmp_path):
    for lang in ("en", "zh"):
        folder = tmp_path / "philosophy1" / lang / "Hook"
        folder.mkdir(parents=True)
        (folder / "result.json").write_text(json.dumps({
            "status": "passed", "fingerprint": "now", "inputs": {}, "warnings": [],
        }))
    manifest = SimpleNamespace(TITLE="Philosophy, Built", SCENES=[("hook", "Hook", "Calculemus")])
    with patch.object(qa_report, "OUT", tmp_path), \
            patch.object(qa_report, "all_videos", return_value=["philosophy1"]) as videos, \
            patch.object(qa_report, "fingerprint", return_value="now"), \
            patch.object(qa_report.importlib, "import_module", return_value=manifest) as imported:
        qa_report.main(series="philosophy")
    videos.assert_called_once_with("philosophy")
    imported.assert_called_with("videos.philosophy.philosophy1.manifest")
    page = (tmp_path / "index_philosophy.html").read_text()
    assert "Philosophy series QA evidence" in page
    assert "2 current cases without automated warnings" in page
    assert not (tmp_path / "index.html").exists()


def test_reviewed_sample_must_belong_to_current_capture_and_match_bytes(tmp_path):
    image = tmp_path / "001.png"
    image.write_bytes(b"fixture frame")
    result = tmp_path / "result.json"
    result.write_text(json.dumps({"frames": [{"file": image.name}]}))
    proof = {"frame_sha256": {image.name: hashlib.sha256(image.read_bytes()).hexdigest()}}
    assert qa_report.visual_evidence_reviewed(tmp_path, proof)
    image.write_bytes(b"changed frame")
    assert not qa_report.visual_evidence_reviewed(tmp_path, proof)
    proof["frame_sha256"][image.name] = hashlib.sha256(image.read_bytes()).hexdigest()
    result.write_text(json.dumps({"frames": [{"file": "002.png"}]}))
    assert not qa_report.visual_evidence_reviewed(tmp_path, proof)
    assert not qa_report.visual_evidence_reviewed(tmp_path, proof, motion=True)
