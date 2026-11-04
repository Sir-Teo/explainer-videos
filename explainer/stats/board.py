"""The Coverage Board: every statistical promise in the series, tested on the World (videos/stats/SYLLABUS.md, §3).

    from explainer.stats.board import Row, verdict, save_rows, load_all, coverage_board

A row records one method in one setting: its nominal level (0.95 for an interval's coverage, 0.05 for a test's
size), what it actually achieved over R seeded replications, the Monte Carlo band, and a mean width (or power).

Verdicts, against the nominal level with Monte Carlo standard error se = sqrt(p(1 - p)/R):

* **kept**: within 3 se of nominal;
* **broken**: an interval covering less (a test rejecting more) than 3 se beyond nominal;
* **conservative**: covering more (rejecting less) than 3 se beyond nominal.

Each part writes its rows to ``.cache/statsN/board.json`` (``save_rows``); ``load_all`` gathers every part's rows in
part order, which is how the Board on screen grows.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass

from explainer.tts import REPO_ROOT

KEPT, BROKEN, CONSERVATIVE = "kept", "broken", "conservative"


@dataclass
class Row:
    part: int
    method: str  # TeX, as it appears on the board
    setting: str  # TeX: the data and sample size
    kind: str  # "coverage" (an interval) or "size" (a test)
    nominal: float  # 0.95, or 0.05
    achieved: float  # coverage, or rejection rate under the null
    reps: int
    width: float | None = None  # mean interval width (or power, for a test, in ``extra``)
    extra: str = ""

    @property
    def se(self) -> float:
        return math.sqrt(self.nominal * (1 - self.nominal) / self.reps)

    @property
    def verdict(self) -> str:
        return verdict(self.kind, self.nominal, self.achieved, self.reps)


def verdict(kind: str, nominal: float, achieved: float, reps: int, k: float = 3.0) -> str:
    se = math.sqrt(nominal * (1 - nominal) / reps)
    if abs(achieved - nominal) <= k * se:
        return KEPT
    worse = achieved < nominal if kind == "coverage" else achieved > nominal
    return BROKEN if worse else CONSERVATIVE


def save_rows(part: int, rows: list[Row]) -> None:
    path = REPO_ROOT / ".cache" / f"stats{part}" / "board.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps([asdict(r) for r in rows], indent=1))
    tmp.replace(path)


def load_all(upto: int | None = None) -> list[Row]:
    rows = []
    for p in sorted((REPO_ROOT / ".cache").glob("stats*/board.json"),
                    key=lambda q: int(q.parent.name.removeprefix("stats"))):
        part = int(p.parent.name.removeprefix("stats"))
        if upto is not None and part > upto:
            continue
        rows += [Row(**r) for r in json.loads(p.read_text())]
    return rows


def coverage_board(rows: list[Row], lit_part: int | None = None, placeholders: int = 0, font_size=20,
                   width=12.6, row_h=0.46, scale_lo=0.80, scale_hi=1.0):
    """The board on screen.  Each row: the method and setting; a coverage scale from ``scale_lo`` to 1 with the
    nominal line, the achieved value as a dot coloured by verdict, its MC band; the number; the verdict.  Rows of
    ``lit_part`` are bright, earlier ones dim.  ``placeholders`` adds empty rows (the board waiting to be filled)."""
    from manim import DOWN, LEFT, RIGHT, UP, Dot, Line, Rectangle, VGroup, GREY_B, GREY_C, GREY_D, WHITE

    from explainer.analysis import label, note
    from explainer.stats.style import S

    color = {KEPT: S.KEPT, BROKEN: S.BROKEN, CONSERVATIVE: S.CONS}
    name_w, scale_w = 5.0, 4.4
    x_name = -width / 2
    x_scale = x_name + name_w + 0.4

    def X(v):
        return x_scale + scale_w * (min(max(v, scale_lo), scale_hi) - scale_lo) / (scale_hi - scale_lo)

    head = VGroup(
        label(r"The Coverage Board", font_size=font_size + 12),
        note(r"each promise tested on the World: \ the nominal level, \ what was achieved", font_size=font_size - 2),
    ).arrange(DOWN, buff=0.12)
    body = VGroup()
    n = len(rows) + placeholders
    for i in range(n):
        y = -i * row_h
        if i < len(rows):
            r = rows[i]
            on = lit_part is None or r.part == lit_part
            op = 1.0 if on else 0.45
            ach = r.achieved if r.kind == "coverage" else 1 - r.achieved
            nom = r.nominal if r.kind == "coverage" else 1 - r.nominal
            name = VGroup(label(r.method, font_size=font_size), label(r.setting, font_size=font_size, color=GREY_B)).arrange(RIGHT, buff=0.18)
            if name.width > name_w:
                name.width = name_w
            name.move_to([x_name + name.width / 2, y, 0]).set_opacity(op)
            line = Line([X(scale_lo), y, 0], [X(scale_hi), y, 0], color=GREY_D, stroke_width=2)
            nomline = Line([X(nom), y - 0.16, 0], [X(nom), y + 0.16, 0], color=GREY_B, stroke_width=2)
            se = r.se
            band = Rectangle(width=max(X(ach + 2 * se) - X(ach - 2 * se), 0.02), height=0.16, stroke_width=0,
                             fill_color=color[r.verdict], fill_opacity=0.3 * op).move_to([X(ach), y, 0])
            dot = Dot([X(ach), y, 0], radius=0.075, color=color[r.verdict]).set_opacity(op)
            val = label(rf"{100 * r.achieved:.1f}\%", font_size=font_size, color=color[r.verdict])
            val.move_to([X(scale_hi) + 0.75, y, 0]).set_opacity(op)
            ver = label(r.verdict, font_size=font_size, color=color[r.verdict])
            ver.move_to([X(scale_hi) + 1.95, y, 0]).set_opacity(op)
            row = VGroup(name, line, nomline, band, dot, val, ver)
            row.dot, row.value, row.verdict_label = dot, val, ver
        else:
            name = label(r"\textit{a promise from a later part}", font_size=font_size, color=GREY_D)
            name.move_to([x_name + name.width / 2, y, 0])
            line = Line([X(scale_lo), y, 0], [X(scale_hi), y, 0], color=GREY_D, stroke_width=1.5,
                        stroke_opacity=0.5)
            q = label(r"?", font_size=font_size + 2, color=GREY_D).move_to([X(scale_hi) + 0.75, y, 0])
            row = VGroup(name, line, q)
        body.add(row)
    axis_y = -(n - 1) * row_h - 0.45
    axis = VGroup(Line([X(scale_lo), axis_y, 0], [X(scale_hi), axis_y, 0], color=GREY_C, stroke_width=1.5))
    for v in (scale_lo, 0.9, 0.95, 1.0):
        if scale_lo <= v <= scale_hi:
            axis.add(Line([X(v), axis_y, 0], [X(v), axis_y - 0.08, 0], color=GREY_C, stroke_width=1.5))
            axis.add(label(rf"{int(round(100 * v))}\%", font_size=font_size - 2, color=GREY_B)
                     .move_to([X(v), axis_y - 0.3, 0]))
    axis.add(note(r"coverage (for a test: $1 -$ its false-alarm rate)", font_size=font_size - 4)
             .move_to([X((scale_lo + scale_hi) / 2), axis_y - 0.65, 0]))
    legend = VGroup()
    for key in (KEPT, CONSERVATIVE, BROKEN):
        legend.add(VGroup(Dot(radius=0.07, color=color[key]), label(key, font_size=font_size - 2, color=color[key]))
                   .arrange(RIGHT, buff=0.12))
    legend.arrange(RIGHT, buff=0.5)
    g = VGroup(body, axis)
    head.next_to(g, UP, buff=0.45)
    legend.next_to(axis, DOWN, buff=0.55)
    out = VGroup(head, g, legend)
    out.head, out.body, out.axis, out.legend = head, body, axis, legend
    out.move_to([0, 0, 0])
    if out.height > 7.4:
        out.height = 7.4
    return out
