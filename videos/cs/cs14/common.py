"""Helpers shared by the scenes of Part 14 ("Lambda and Types")."""

from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono as _mono
from explainer import zh_text
from videos.cs.cs8.common import bar_chart  # noqa: F401
from videos.cs.cs11.common import region  # noqa: F401
from videos.cs.cs12.common import tree  # noqa: F401

from .compute import load  # noqa: F401

PART = 14

DATA = C.CS_DATA
CTRL = C.CS_CONTROL
HEAD = C.CS_HEAD
CODE = C.CS_CODE
FUNC = C.CS_FUNC
COST = C.CS_COST
YES = C.CS_TRUE
NO = C.CS_FALSE
BG = "#121722"
LAM = "#9b8cd6"      # λ nodes
APP = "#5fb7a8"      # application nodes


def literal_text(text, **kwargs):
    """Source tokens, IR operands and machine output are data, not UI prose."""
    with zh_text.verbatim():
        return Text(text, **kwargs)


def mono(s, size=19, color=CODE):
    with zh_text.verbatim():
        return _mono(s, size, color)


def code(lines, size=18, color=CODE, buff=0.07):
    return VGroup(*[mono(l if l else " ", size, color) for l in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=buff)


def grid_table(header, rows, widths, row_h=0.42, font_size=18, header_color=GREY_B, colors=None, mono_cols=(0,)):
    """``header``: column titles (Tex); ``rows``: lists of strings (Tex, or monospaced in ``mono_cols``).
    Returns a VGroup with ``.cells[r][c]`` (r = 0 is the header) and ``.rule``."""
    g = VGroup()
    g.cells = []
    xs = np.cumsum([0] + list(widths[:-1])) + np.array(widths) / 2
    for r, row in enumerate([header] + rows):
        line = []
        for c, txt in enumerate(row):
            if r > 0 and c in mono_cols:
                m = (literal_text(txt, font="DejaVu Sans Mono", font_size=font_size - 3, color=CODE) if txt.strip()
                     else VectorizedPoint())
            else:
                col = header_color if r == 0 else (colors[r - 1][c] if colors else WHITE)
                m = label(txt, font_size=font_size, color=col) if txt else VectorizedPoint()
            if m.width > widths[c] - 0.1:
                m.width = widths[c] - 0.1
            m.move_to([xs[c], -r * row_h, 0])
            if r > 0 and c in mono_cols:
                m.align_to([xs[c] - widths[c] / 2 + 0.05, 0, 0], LEFT)
            line.append(m)
            g.add(m)
        g.cells.append(line)
    g.rule = Line([0, -row_h / 2, 0], [sum(widths), -row_h / 2, 0], color=GREY_D, stroke_width=1.5)
    g.add(g.rule)
    return g


def lam_tree(t, dx=0.7, dy=0.75, font_size=20, highlight=None):
    """A λ-term (Part 1's tuples) as its syntax tree: λx nodes, @ for application, variables as leaves.
    ``highlight`` is a path (as used by explainer.cs.lam) whose subtree is drawn in HEAD."""
    def conv(t, path=()):
        k = t[0]
        if k == "var":
            return t[1]
        if k == "lam":
            return ("λ" + t[1], [conv(t[2], path + (1,))])
        return ("@", [conv(t[1], path + (0,)), conv(t[2], path + (1,))])
    g = tree(conv(t), dx=dx, dy=dy, font_size=font_size, leaf_color=CODE, node_color=GREY_A)
    for m, _ in g.nodes:
        s = m.text if hasattr(m, "text") else ""
        if s.startswith("λ"):
            m.set_color(LAM)
        elif s == "@":
            m.set_color(APP)
    return g


def church_boxes(n, f="f", x="x", w=0.9, h=0.6, color=FUNC):
    """The numeral n as nested boxes: f (f (... (f x)))."""
    inner = VGroup(RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=CODE, fill_color=CODE,
                                    fill_opacity=0.15), mono(x, 18, CODE))
    inner[1].move_to(inner[0])
    g = inner
    for k in range(n):
        lab = mono(f, 18, color)
        gg = g.copy()
        lab.next_to(gg, LEFT, buff=0.14)
        frame = SurroundingRectangle(VGroup(lab, gg), buff=0.13, corner_radius=0.1, color=color, stroke_width=1.6)
        frame.set_fill(color, 0.06)
        g = VGroup(frame, lab, gg)
    return g


def term_tex(s: str) -> str:
    """A simply typed term as printed by stlc.show, in math mode."""
    import re
    kw = {"succ", "pred", "iszero", "if", "then", "else", "true", "false", "fix", "Nat", "Bool"}
    out, prev = [], None
    for tok in re.findall(r"λ|→|[A-Za-z_][\w']*|\d+|[():.]", s):
        if tok == "λ":
            piece = r"\lambda "
        elif tok == "→":
            piece = r"\to "
        elif tok in kw:
            piece = rf"\mathsf{{{tok}}}"
        elif tok == ":":
            piece = "{:}"
        elif tok == ".":
            piece = r".\,"
        else:
            piece = tok
        word = re.fullmatch(r"[\w']+", tok) or tok in ("(", "λ")
        if prev not in (None, "λ") and word and (re.fullmatch(r"[\w']+", prev) or prev == ")"):
            out.append(r"\;")
        out.append(piece)
        prev = tok
    return "".join(out)


def judgement(ctx: dict, term: str, typ: str, font_size=26):
    """Γ ⊢ t : T with the context written out."""
    c = ", ".join(rf"{k}{{:}}{v}" for k, v in ctx.items())
    t = term_tex(term)
    return MathTex(rf"{c} \vdash {t} : {typ}" if c else rf"\vdash {t} : {typ}", font_size=font_size)


def deriv_tree(d: dict, font_size=22, gap=0.45):
    """A derivation (compute.stlc's view) drawn as nested inference rules: premises over a line over the
    conclusion, the rule's name to the right of the line."""
    concl = judgement(d["ctx"], d["term"], d["type"], font_size)
    if d["premises"]:
        prem = VGroup(*[deriv_tree(p, font_size, gap) for p in d["premises"]]).arrange(RIGHT, buff=gap,
                                                                                       aligned_edge=DOWN)
        prem.next_to(concl, UP, buff=0.32)
    else:
        prem = VGroup()
    w = max(concl.width, prem.width if len(prem) else 0) + 0.2
    line = Line(LEFT * w / 2, RIGHT * w / 2, color=GREY_B, stroke_width=1.5).next_to(concl, UP, buff=0.12)
    rule = MathTex(r"\textsc{" + d["rule"].replace("T-", "") + "}", font_size=font_size - 6,
                   color=HEAD).next_to(line, RIGHT, buff=0.1)
    g = VGroup(prem, line, rule, concl)
    g.concl, g.line, g.rule, g.prem = concl, line, rule, prem
    return g
