"""QA resume and report routing cover each series and transitive dependencies."""

from unittest.mock import patch

from tools import qa_series
from explainer import paths


def test_statistics_fingerprint_tracks_local_shared_and_cross_series_sources(tmp_path, monkeypatch):
    monkeypatch.setattr(qa_series, "ROOT", tmp_path)
    monkeypatch.setattr(qa_series, "__file__", str(tmp_path / "tools/qa_series.py"))
    for name in ("explainer/base.py", "tools/qa_series.py", "tools/dead_air.py", "manim.cfg",
                 "videos/stats/__init__.py", "videos/stats/stats_text_zh.json",
                 "videos/stats/stats1/manifest.py", "videos/stats/stats2/manifest.py",
                 "videos/stats/stats3/manifest.py", "videos/ai/__init__.py",
                 "videos/ai/ai1/manifest.py"):
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("{}" if p.suffix == ".json" else "# source\n")

    def video_dir(part):
        return tmp_path / "videos" / ("ai" if part.startswith("ai") else "stats") / part

    monkeypatch.setattr(paths, "video_dir", video_dir)
    local = video_dir("stats1") / "scene.py"
    local.write_text('from videos.ai.ai1 import compute\nCache("stats2")\n# Example: videos.stats.statsN.compute\n')
    previous = qa_series.fingerprint("stats1")
    for p in (local, video_dir("stats1").parent / "stats_text_zh.json",
              video_dir("stats2") / "manifest.py", video_dir("ai1") / "manifest.py"):
        p.write_text(p.read_text() + "\n")
        current = qa_series.fingerprint("stats1")
        assert current != previous, p
        previous = current
    unrelated = video_dir("stats3") / "manifest.py"
    unrelated.write_text("# unrelated edit\n")
    assert qa_series.fingerprint("stats1") == previous


def test_statistics_report_uses_statistics_manifest_and_preserves_ai_index(tmp_path, monkeypatch):
    from tools import qa_report

    monkeypatch.setattr(qa_report, "OUT", tmp_path)
    monkeypatch.setattr(qa_report, "fingerprint", lambda _: "current")
    existing = tmp_path / "index.html"
    existing.write_text("existing AI report")
    qa_report.main(video="stats1")
    report = (tmp_path / "index_stats.html").read_text()
    assert "Statistics, Built" in report
    assert "32 language/chapter cases" in report
    assert "The Shape of Data" in report
    assert existing.read_text() == "existing AI report"


def test_philosophy_fingerprint_tracks_sources_translations_and_dependencies(tmp_path):
    series = tmp_path / "videos/philosophy"
    part = series / "philosophy1"
    dependency = series / "philosophy2"
    unrelated = series / "philosophy3"
    for directory in (part, dependency, unrelated, tmp_path / "explainer", tmp_path / "tools"):
        directory.mkdir(parents=True)
    for directory in (part, dependency, unrelated):
        (directory / "manifest.py").write_text("# source\n")
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
            patch("explainer.paths.video_dir", side_effect=lambda name: series / name):
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
