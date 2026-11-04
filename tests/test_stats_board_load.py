"""load_all reads both forms a part's board.json can take: save_rows' list, or the compute cache's {"rows": [...]}."""

import json

from explainer.stats import board
from explainer.stats.board import Row, load_all


def test_load_all_reads_both_forms(tmp_path, monkeypatch):
    monkeypatch.setattr(board, "REPO_ROOT", tmp_path)
    r8 = Row(8, "a", "b", "coverage", 0.95, 0.94, 1000)
    r10 = Row(10, "c", "d", "size", 0.05, 0.06, 1000)
    board.save_rows(8, [r8])
    p = tmp_path / ".cache" / "stats10" / "board.json"
    p.parent.mkdir(parents=True)
    from dataclasses import asdict
    p.write_text(json.dumps({"rows": [asdict(r10) | {"verdict": r10.verdict, "se": r10.se}]}))
    rows = load_all()
    assert [r.part for r in rows] == [8, 10]
    assert rows[1] == r10
    assert [r.part for r in load_all(upto=9)] == [8]


def test_load_all_skips_unrelated_board_items(tmp_path, monkeypatch):
    monkeypatch.setattr(board, "REPO_ROOT", tmp_path)
    for part, payload in ((6, {"rows": 12, "balls": 600}), (9, {"rows": {"uniform": {}}})):
        p = tmp_path / ".cache" / f"stats{part}" / "board.json"
        p.parent.mkdir(parents=True)
        p.write_text(json.dumps(payload))
    board.save_rows(8, [Row(8, "a", "b", "coverage", 0.95, 0.94, 1000)])
    assert [r.part for r in load_all()] == [8]
