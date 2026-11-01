"""Chinese prose baseline/leading for the three reviewed Part 6 cards.

This is deliberately opt-in: equations and the shared lecture helpers keep their
original rendering. Latin/math spans retain their outlines, size and x positions.
"""
from functools import lru_cache
import re

from manim import DOWN, LEFT, RIGHT, Tex, UP, VGroup

_CJK = re.compile(r"[\u3000-\u303f\u3400-\u9fff\uf900-\ufaff\uff00-\uffef]")
_TABULAR = r"\begin{tabular}{@{}l@{}}"


@lru_cache(maxsize=32)
def _baseline(font_size):
    # Measure the active XeTeX fonts, rather than assuming host font metrics.
    probe = Tex("口", "H", "$H$", arg_separator="", font_size=font_size)
    return tuple(float(probe[i].get_bottom()[1] - probe[0].get_bottom()[1]) for i in (1, 2))


def _spans(line):
    """Keep math and balanced TeX groups intact; split only at script changes."""
    atoms = []
    i = 0
    while i < len(line):
        start = i
        if line[i] == "$":
            i += 1
            while i < len(line) and (line[i] != "$" or line[i-1] == "\\"):
                i += 1
            assert i < len(line), "Unbalanced inline math"
            i += 1
        elif line[i] == "\\":
            match = re.match(r"\\(?:[A-Za-z]+|.)", line[i:])
            i += len(match.group()) if match else 1
            if i < len(line) and line[i] == "{":
                depth = 1; i += 1
                while i < len(line) and depth:
                    if line[i] == "{" and line[i-1] != "\\": depth += 1
                    if line[i] == "}" and line[i-1] != "\\": depth -= 1
                    i += 1
                assert depth == 0, "Unbalanced TeX command"
        elif line[i] == "{":
            depth = 1; i += 1
            while i < len(line) and depth:
                if line[i] == "{": depth += 1
                if line[i] == "}": depth -= 1
                i += 1
            assert depth == 0, "Unbalanced TeX group"
        else:
            i += 1
        atom = line[start:i]
        script = bool(_CJK.search(atom)) or any("\u3000" <= c <= "\u303f" or "\uff00" <= c <= "\uffef" for c in atom)
        if not re.search(r"[A-Za-z0-9$]", atom) and not script:
            script = None
        atoms.append((atom, script))
    spans, current, script = [], "", None
    for atom, kind in atoms:
        # Keep each math span independent, so descenders and superscripts move as a unit.
        if atom.startswith("$"):
            if current: spans.append(current)
            spans.append(atom); current = ""; script = None
        elif kind is not None and script is not None and kind != script:
            spans.append(current); current = atom; script = kind
        else:
            current += atom
            if kind is not None: script = kind
    if current:
        if not re.search(r"[A-Za-z0-9]", current) and not _CJK.search(current) and spans:
            spans[-1] += current
        else: spans.append(current)
    assert "".join(spans) == line
    return spans


def prose(mob, leading=0.10):
    """Adjust an existing prose Tex or text-only group, preserving its text."""
    if getattr(mob, "_zh_prose_done", False): return mob.copy()
    if type(mob) is Tex:
        text = mob.get_tex_string()
        if not _CJK.search(text): return mob.copy()
        if text.startswith(_TABULAR) and text.endswith(r"\end{tabular}"):
            text = text[len(_TABULAR):-len(r"\end{tabular}")]
        lines = text.split(r"\\")
        rows = []
        for line in lines:
            spans = _spans(line)
            row = Tex(*spans, arg_separator="", font_size=mob.font_size, color=mob.get_color())
            assert len(row) == len(spans)
            plain, math = _baseline(float(mob.font_size))
            for part, span in zip(row, spans):
                if not _CJK.search(span) and re.search(r"[A-Za-z0-9$]", span):
                    part.shift(DOWN * (math if span.startswith("$") else plain))
            rows.append(row)
        out = rows[0] if len(rows) == 1 else VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=leading)
        # Preserve the full translated source for QA inspection, including wraps.
        out.prose_source = mob.get_tex_string()
        out._zh_prose_done = True
        return out.move_to(mob)
    if type(mob) is VGroup and len(mob):
        old = list(mob)
        new = [prose(child, leading) for child in old]
        if len(old) > 1:
            delta = old[-1].get_center() - old[0].get_center()
            # Left-aligned rows can have very different widths; their centre
            # displacement therefore does not identify the stacking direction.
            left_aligned = abs(old[-1].get_left()[0] - old[0].get_left()[0]) < 1e-7
            bottom_aligned = abs(old[-1].get_bottom()[1] - old[0].get_bottom()[1]) < 1e-7
            horizontal = not left_aligned and (bottom_aligned or abs(delta[0]) > abs(delta[1]))
            for i in range(1, len(new)):
                if horizontal:
                    gap = old[i].get_left()[0] - old[i-1].get_right()[0]
                    new[i].next_to(new[i-1], RIGHT, buff=gap, aligned_edge=DOWN)
                else:
                    gap = old[i-1].get_bottom()[1] - old[i].get_top()[1]
                    new[i].next_to(new[i-1], DOWN, buff=gap, aligned_edge=LEFT)
        return VGroup(*new).move_to(mob)
    return mob.copy()


def card(mob):
    """Rebuild only the box around polished prose, retaining existing padding."""
    from explainer.ai.lecture import _card
    return _card(prose(mob.head), prose(mob.body), mob.box.get_stroke_color(), mob.box.width)


def references(mob):
    """Keep the existing bibliography order and font sizes, with measured gaps."""
    bh, books, ph, papers = mob
    books = VGroup(*[prose(row) for row in books]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    papers = VGroup(*[prose(row) for row in papers]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    out = VGroup(bh, books, ph, papers).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    ph.shift(DOWN * 0.15); papers.shift(DOWN * 0.15)
    if out.height > 7.4: out.height = 7.4
    return out.move_to(mob)
