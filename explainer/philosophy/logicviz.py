"""Logic, drawn: truth tables that fill, Fitch proofs with their scope bars, formula trees that evaluate from the
leaves up, argument maps with a validity verdict, and clause lists. Exported by :mod:`explainer.philosophy.studio`.

Formulas are the Reasoner's tuples (:mod:`explainer.philosophy.reasoner.prop`); :func:`ftex` typesets one.
"""

from __future__ import annotations

import numpy as np
from manim import *  # noqa: F401,F403

from explainer.analysis import label, note, wrapped_label
from explainer.ai.games import SearchTree
from explainer.philosophy.reasoner import prop

TRUE_C, FALSE_C = "#7BD389", "#FF6B6B"
CLAIM_C, CONCL_C, RULE_C = "#6FB7FF", "#FFD166", "#C3A6FF"
CELL_FILL = "#0B0F17"


def ftex(f) -> str:
    """A Reasoner formula (tuple, or text to parse) as TeX."""
    if isinstance(f, str):
        f = prop.parse(f)
    return prop.show(f, tex=True)


def fmath(f, font_size=36, color=WHITE) -> MathTex:
    return MathTex(ftex(f), font_size=font_size, color=color)


def tv(b: bool, font_size=26) -> MathTex:
    """A truth value as a coloured T or F (the same letters in the Chinese edition, as in Chinese logic texts)."""
    return MathTex(r"\mathrm{T}" if b else r"\mathrm{F}", font_size=font_size, color=TRUE_C if b else FALSE_C)


class TruthTable(VGroup):
    """A truth table for ``columns`` (formulas) over the atoms ``names``: header row, then one row per valuation.

    ``self.head[c]``, ``self.cell[r][c]`` (atoms first, then the columns), ``self.rows_bg[r]``. Cells start
    hidden-friendly: animate with :meth:`reveal_column` or :meth:`reveal_row`."""

    def __init__(self, columns, names=None, cell_w=None, cell_h=0.42, font_size=26, max_width=12.6,
                 center=ORIGIN, atom_color=CLAIM_C, highlight_col: int | None = None):
        super().__init__()
        cols = [prop.parse(c) if isinstance(c, str) else c for c in columns]
        names = names or prop.atoms_of(cols)
        self.names, self.columns = names, cols
        heads = [MathTex(n if len(n) == 1 else rf"\mathit{{{n}}}", font_size=font_size + 2, color=atom_color)
                 for n in names]
        heads += [fmath(c, font_size=font_size + 2, color=CONCL_C if i == highlight_col else WHITE)
                  for i, c in enumerate(cols)]
        widths = [max(h.width + 0.35, 0.62) if cell_w is None else cell_w for h in heads]
        total = sum(widths)
        if total > max_width:
            k = max_width / total
            widths = [w * k for w in widths]
            for h, w in zip(heads, widths):
                if h.width > w - 0.1:
                    h.width = w - 0.1
        xs = np.cumsum([0] + widths[:-1]) + np.array(widths) / 2 - total * min(1, max_width / total) / 2
        self.head = VGroup()
        for h, x in zip(heads, xs):
            self.head.add(h.move_to([x, 0, 0]))
        self.rows = list(prop.valuations(names))
        self.values = [[v[n] for n in names] + [prop.evaluate(c, v) for c in cols] for v in self.rows]
        self.cell = []
        self.rows_bg = VGroup()
        body = VGroup()
        for r, vals in enumerate(self.values):
            y = -(r + 1) * cell_h - 0.12
            bg = Rectangle(width=sum(widths) + 0.1, height=cell_h * 0.94, stroke_width=0,
                           fill_color=WHITE, fill_opacity=0.035 if r % 2 else 0.0).move_to([0, y, 0])
            self.rows_bg.add(bg)
            row = []
            for c, (b, x) in enumerate(zip(vals, xs)):
                m = tv(b, font_size)
                m.move_to([x, y, 0])
                row.append(m)
                body.add(m)
            self.cell.append(row)
        rule = Line([xs[0] - widths[0] / 2, -0.32, 0], [xs[-1] + widths[-1] / 2, -0.32, 0], color=GREY_C,
                    stroke_width=1.5)
        sep_x = xs[len(names) - 1] + widths[len(names) - 1] / 2
        sep = Line([sep_x, 0.25, 0], [sep_x, -(len(self.rows)) * cell_h - 0.35, 0], color=GREY_C, stroke_width=1.5)
        self.rule, self.sep = rule, sep
        self.add(self.rows_bg, self.head, rule, sep, body)
        self.body = body
        self.move_to(center)

    def column(self, c) -> VGroup:
        return VGroup(*[row[c] for row in self.cell])

    def row(self, r) -> VGroup:
        return VGroup(*self.cell[r])

    def reveal_column(self, c, lag=0.08, run_time=1.2):
        return LaggedStart(*[FadeIn(m, scale=1.3) for m in self.column(c)], lag_ratio=lag, run_time=run_time)

    def row_box(self, r, color=CONCL_C) -> SurroundingRectangle:
        return SurroundingRectangle(self.rows_bg[r], buff=0.02, color=color, stroke_width=2.5, corner_radius=0.05)


class FitchView(VGroup):
    """A Fitch-style proof: line number, scope bars (one per open subproof, with a short foot under each
    assumption), the formula, and its justification. ``lines`` as for ``prop.check_fitch``:
    ``(depth, formula, rule, refs)``. ``self.line[i]`` is (number, formula, justification) of line i (0-based)."""

    RULE_TEX = {"premise": r"premise", "assume": r"assumption", "reit": r"R", "andI": r"$\land$I",
                "andE": r"$\land$E", "orI": r"$\lor$I", "orE": r"$\lor$E", "impI": r"$\to$I", "impE": r"$\to$E",
                "notI": r"$\lnot$I", "notE": r"$\lnot$E", "botE": r"$\bot$E", "dne": r"$\lnot\lnot$E",
                "iffI": r"$\leftrightarrow$I", "iffE": r"$\leftrightarrow$E"}

    def __init__(self, lines, font_size=28, line_h=0.52, indent=0.42, center=ORIGIN, just_x=3.2):
        super().__init__()
        self.line = []
        self.bars = VGroup()
        n = len(lines)
        x0 = -3.6
        depth_start: dict[int, int] = {}
        spans = []  # (depth, start, end)
        for i, (d, f, r, refs) in enumerate(lines):
            if r == "assume":
                for dd in [k for k in depth_start if k >= d]:
                    spans.append((dd, depth_start.pop(dd), i - 1))
                depth_start[d] = i
            else:
                for dd in [k for k in depth_start if k > d]:
                    spans.append((dd, depth_start.pop(dd), i - 1))
        for dd, s in depth_start.items():
            spans.append((dd, s, n - 1))
        y = lambda i: -i * line_h  # noqa: E731
        base = Line([x0 - 0.05, y(0) + line_h / 2, 0], [x0 - 0.05, y(n - 1) - line_h / 2, 0], color=GREY_B,
                    stroke_width=2)
        self.bars.add(base)
        for dd, s, e in spans:
            x = x0 - 0.05 + dd * indent
            bar = Line([x, y(s) + line_h / 2 - 0.04, 0], [x, y(e) - line_h / 2 + 0.04, 0], color=RULE_C, stroke_width=2)
            foot = Line([x, y(s) - line_h / 2 + 0.06, 0], [x + 0.5, y(s) - line_h / 2 + 0.06, 0], color=RULE_C,
                        stroke_width=2)
            self.bars.add(bar, foot)
        self.spans = spans
        prem_end = max([i for i, l in enumerate(lines) if l[2] == "premise"], default=-1)
        if prem_end >= 0:
            self.bars.add(Line([x0 - 0.05, y(prem_end) - line_h / 2 + 0.06, 0],
                               [x0 + 0.55, y(prem_end) - line_h / 2 + 0.06, 0], color=GREY_B, stroke_width=2))
        rows = VGroup()
        for i, (d, f, r, refs) in enumerate(lines):
            num = MathTex(str(i + 1), font_size=font_size - 4, color=GREY_B).move_to([x0 - 0.45, y(i), 0])
            fm = fmath(f, font_size=font_size, color=CONCL_C if i == n - 1 and d == 0 else WHITE)
            fm.move_to([x0 + 0.15 + d * indent, y(i), 0], aligned_edge=LEFT)
            ref_s = ", ".join(f"{a}" if isinstance(a, int) else f"{a[0]}–{a[1]}" for a in refs)
            jt = self.RULE_TEX.get(r, r) + (rf"\ {ref_s}" if ref_s else "")
            js = label(jt, font_size=font_size - 6, color=RULE_C).move_to([x0 + just_x + 3.0, y(i), 0],
                                                                           aligned_edge=LEFT)
            self.line.append((num, fm, js))
            rows.add(num, fm, js)
        self.add(self.bars, rows)
        self.move_to(center)


class FormulaTree(VGroup):
    """The parse tree of a formula: atoms at the leaves, connectives above. ``self.node[i]`` (a dot with its symbol)
    and ``self.sub[i]`` (the subformula there), in breadth-first order; :meth:`values` gives each node's truth
    value under a valuation, and :meth:`value_tags` the coloured T/F tags to fade in, leaves first."""

    SYM = {"not": r"\lnot", "and": r"\land", "or": r"\lor", "imp": r"\to", "iff": r"\leftrightarrow",
           "top": r"\top", "bot": r"\bot"}

    def __init__(self, f, width=7.0, level_height=1.05, center=ORIGIN, font_size=34):
        super().__init__()
        f = prop.parse(f) if isinstance(f, str) else f

        def build(g):
            kids = [build(a) for a in g[1:]] if g[0] not in ("var", "top", "bot") else []
            return {"children": kids, "f": g}

        self.tree = SearchTree(build(f), width=width, level_height=level_height, radius=0.0, center=center)
        self.sub = [self.tree.node_data[i]["f"] for i in range(len(self.tree.nodes))]
        self.node = VGroup()
        for i, g in enumerate(self.sub):
            sym = g[1] if g[0] == "var" else self.SYM[g[0]]
            col = CLAIM_C if g[0] == "var" else RULE_C
            disc = Circle(radius=0.3, stroke_color=col, stroke_width=2, fill_color=CELL_FILL, fill_opacity=1)
            t = MathTex(sym, font_size=font_size, color=col)
            self.node.add(VGroup(disc, t.move_to(disc)).move_to(self.tree.pos[i]))
        for e in self.tree.edges:
            if e is not None:
                e.set_stroke(GREY_C, 2)
        self.edges = VGroup(*[e for e in self.tree.edges if e is not None])
        self.add(self.edges, self.node)

    def values(self, v: dict) -> list[bool]:
        return [prop.evaluate(g, v) for g in self.sub]

    def order_bottom_up(self) -> list[int]:
        return sorted(range(len(self.sub)), key=lambda i: -self.tree.level[i])

    def value_tags(self, v: dict, font_size=24) -> dict:
        tags = {}
        for i, b in enumerate(self.values(v)):
            tags[i] = tv(b, font_size).next_to(self.node[i], RIGHT, buff=0.08)
        return tags


class ArgumentMap(VGroup):
    """An argument: premises stacked over the inference bar, the conclusion under it, and (after
    :meth:`verdict`) a badge saying valid, or invalid with the countermodel the Reasoner found."""

    def __init__(self, premises, conclusion, width=6.4, font_size=30, center=ORIGIN, words=None):
        super().__init__()
        self.fs = [prop.parse(p) if isinstance(p, str) else p for p in premises]
        self.cf = prop.parse(conclusion) if isinstance(conclusion, str) else conclusion
        self.words = words
        prem = VGroup()
        for i, f in enumerate(self.fs):
            m = fmath(f, font_size=font_size)
            if words:
                w = label(words[i], font_size=font_size - 8, color=GREY_A)
                m = VGroup(m, w).arrange(RIGHT, buff=0.4)
            prem.add(m)
        prem.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        bar = Line(LEFT * width / 2, RIGHT * width / 2, color=GREY_B, stroke_width=2.5)
        therefore = MathTex(r"\therefore", font_size=font_size + 4, color=CONCL_C)
        cm = fmath(self.cf, font_size=font_size + 2, color=CONCL_C)
        if words and len(words) > len(self.fs):
            cm = VGroup(cm, label(words[-1], font_size=font_size - 8, color=GREY_A)).arrange(RIGHT, buff=0.4)
        concl = VGroup(therefore, cm).arrange(RIGHT, buff=0.3)
        self.premises, self.bar, self.conclusion = prem, bar, concl
        VGroup(prem, bar, concl).arrange(DOWN, buff=0.28)
        prem.align_to(bar, LEFT).shift(RIGHT * 0.3)
        concl.align_to(bar, LEFT).shift(RIGHT * 0.3)
        self.add(prem, bar, concl)
        self.move_to(center)
        self.valid, self.countermodel = prop.entails(self.fs, self.cf)

    def verdict(self, font_size=26) -> VGroup:
        if self.valid:
            b = VGroup(MathTex(r"\checkmark", font_size=font_size + 10, color=TRUE_C),
                       label(r"valid", font_size=font_size, color=TRUE_C)).arrange(RIGHT, buff=0.15)
        else:
            cm = r",\ ".join(rf"{k}={'T' if v else 'F'}" for k, v in self.countermodel.items())
            b = VGroup(MathTex(r"\times", font_size=font_size + 10, color=FALSE_C),
                       label(r"invalid", font_size=font_size, color=FALSE_C),
                       MathTex(rf"({cm})", font_size=font_size - 2, color=FALSE_C)).arrange(RIGHT, buff=0.15)
        return b.next_to(self.bar, RIGHT, buff=0.35)


def clause_tex(c, names) -> str:
    """An integer clause (frozenset of ±(index+1)) as TeX: (a ∨ ¬b); the empty clause is □."""
    if not c:
        return r"\square"
    lits = sorted(c, key=lambda l: (abs(l), l < 0))
    s = r" \lor ".join((r"\lnot " if l < 0 else "") + names[abs(l) - 1] for l in lits)
    return s if len(lits) == 1 else f"({s})"


def clause_list(clauses, names, font_size=30, cols=1, buff=0.18) -> VGroup:
    g = VGroup(*[MathTex(clause_tex(c, names), font_size=font_size) for c in clauses])
    if cols == 1:
        g.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    else:
        g.arrange_in_grid(cols=cols, buff=(0.5, buff), cell_alignment=LEFT)
    return g


class ValueGrid(VGroup):
    """A table of cells: ``headers`` (TeX strings or mobjects) and ``rows`` of cells (bool -> a coloured T/F, str ->
    MathTex, Mobject as is). ``self.cell[r][c]``, ``self.head[c]``, ``self.rows_bg[r]``; :meth:`strike` crosses a row
    out and :meth:`row_box` frames one."""

    def __init__(self, headers, rows, col_w=None, cell_h=0.46, font_size=26, center=ORIGIN, head_color=CLAIM_C):
        super().__init__()

        def mob(x, head=False):
            if isinstance(x, Mobject):
                return x
            if isinstance(x, bool):
                return tv(x, font_size)
            return MathTex(str(x), font_size=font_size + (2 if head else 0), color=head_color if head else WHITE)

        heads = [mob(h, True) for h in headers]
        ws = col_w or [max(0.7, max([h.width] + [mob(r[c]).width for r in rows]) + 0.35) for c, h in enumerate(heads)]
        if isinstance(ws, (int, float)):
            ws = [ws] * len(heads)
        total = sum(ws)
        xs = np.cumsum([0] + list(ws[:-1])) + np.array(ws) / 2 - total / 2
        self.head = VGroup(*[h.move_to([x, 0, 0]) for h, x in zip(heads, xs)])
        self.cell, self.rows_bg = [], VGroup()
        body = VGroup()
        for r, row in enumerate(rows):
            y = -(r + 1) * cell_h - 0.12
            self.rows_bg.add(Rectangle(width=total + 0.1, height=cell_h * 0.94, stroke_width=0, fill_color=WHITE,
                                       fill_opacity=0.035 if r % 2 else 0.0).move_to([0, y, 0]))
            cells = []
            for x, v in zip(xs, row):
                m = mob(v).move_to([x, y, 0])
                cells.append(m)
                body.add(m)
            self.cell.append(cells)
        self.rule = Line([-total / 2, -0.3, 0], [total / 2, -0.3, 0], color=GREY_C, stroke_width=1.5)
        self.add(self.rows_bg, self.head, self.rule, body)
        self.body = body
        self.width_total = total
        self.move_to(center)

    def row(self, r) -> VGroup:
        return VGroup(*self.cell[r])

    def column(self, c) -> VGroup:
        return VGroup(*[row[c] for row in self.cell])

    def strike(self, r, color=FALSE_C) -> Line:
        bg = self.rows_bg[r]
        return Line(bg.get_left() + RIGHT * 0.05, bg.get_right() + LEFT * 0.05, color=color, stroke_width=3)

    def row_box(self, r, color=TRUE_C) -> SurroundingRectangle:
        return SurroundingRectangle(self.rows_bg[r], buff=0.02, color=color, stroke_width=2.5, corner_radius=0.05)
