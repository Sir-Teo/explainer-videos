"""Resume must invalidate evidence when the requested series changes."""

from unittest.mock import patch

from tools import qa_series


def test_philosophy_fingerprint_tracks_sources_translations_and_dependencies(tmp_path):
    series = tmp_path / "videos/philosophy"
    part = series / "philosophy1"
    dependency = series / "philosophy2"
    unrelated = series / "philosophy3"
    for directory in (part, dependency, unrelated, tmp_path / "explainer", tmp_path / "tools"):
        directory.mkdir(parents=True)
    scene = part / "scene.py"
    scene.write_text("from videos.philosophy.philosophy2 import compute\n")
    other = dependency / "compute.py"
    other.write_text("value = 1\n")
    unused = unrelated / "scene.py"
    unused.write_text("value = 1\n")
    translations = series / "philosophy_text_zh.json"
    translations.write_text("{}")
    (tmp_path / "tools/dead_air.py").touch()
    script = tmp_path / "tools/qa_series.py"
    script.touch()
    (tmp_path / "manim.cfg").touch()
    with patch.object(qa_series, "ROOT", tmp_path), patch.object(qa_series, "__file__", str(script)), \
            patch("explainer.paths.video_dir", return_value=part):
        initial = qa_series.fingerprint("philosophy1")
        unused.write_text("value = 2\n")
        assert qa_series.fingerprint("philosophy1") == initial
        other.write_text("value = 2\n")
        changed_dependency = qa_series.fingerprint("philosophy1")
        assert changed_dependency != initial
        translations.write_text('{"strings": {"hello": "你好"}}')
        changed_translation = qa_series.fingerprint("philosophy1")
        assert changed_translation != changed_dependency
        scene.write_text(scene.read_text() + "value = 3\n")
        assert qa_series.fingerprint("philosophy1") != changed_translation
