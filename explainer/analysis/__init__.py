"""Shared visual instruments for the analysis series (videos/analysis1 ... analysis10).

    from explainer.analysis import *

Everything here is reused across parts so that a device introduced in Part 1 looks identical in Part 8:

* text helpers (``label``, ``note``, ``mtex``, ``why``, ``boxed``, ``num``) on a wide TeX template that never wraps;
* :func:`ladder`, the line-by-line derivation reveal (each line grows out of the previous one, with a grey note
  saying why it follows);
* :func:`chapter_card` with the **timeline strip**, the history of the ideas lit up as the series reaches them;
* :func:`museum_card`, the label next to every counterexample (who, when, what it breaks, where it is in Rudin);
* :func:`ledger`, the table that grows by one row per part (the series' recap device);
* :func:`rational_dust`, the rational numbers drawn as a ruler whose tick for p/q has height ~ q^-0.6, so the
  density of Q and its hierarchy are both visible (reused for Thomae's function in Part 2);
* :func:`dictionary_card`, the two-column "R^n <-> function space" card.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

from explainer import *  # noqa: F403

# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
WIDE_TEX = TEX_TEMPLATE.copy()
WIDE_TEX.add_to_preamble(r"\setlength{\textwidth}{40cm}")
WIDE_TEX.add_to_preamble(r"\newcommand{\R}{\mathbb{R}}\newcommand{\Q}{\mathbb{Q}}\newcommand{\N}{\mathbb{N}}"
                         r"\newcommand{\Z}{\mathbb{Z}}\newcommand{\C}{\mathbb{C}}")
MathTex.set_default(tex_template=WIDE_TEX)
Tex.set_default(tex_template=WIDE_TEX)
MAX_TEXT_WIDTH = 13.6


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    """A Tex label that never wraps on its own (line breaks are explicit) and shrinks to fit the frame."""
    t = Tex(text, color=color, font_size=font_size, **kw)
    if t.width > MAX_TEXT_WIDTH:
        t.width = MAX_TEXT_WIDTH
    return t


def nz(x, digits):
    """x rounded for display, with -0 turned into 0 (so a readout never shows -0.000)."""
    return round(float(x), digits) + 0.0


def regrid(tab, gap=0.45, center=False, max_width=None):
    """Put a table's rows (MathTex rows split into the same parts, header first) on a real grid: each column as
    wide as its widest entry, ``gap`` apart, entries left-aligned (or centred). The table keeps its centre, is
    scaled down to ``max_width`` if given, and is kept inside the frame."""
    c = tab.get_center()
    ncol = min(len(r) for r in tab)
    w = [max(r[j].width for r in tab) for j in range(ncol)]
    x = tab.get_left()[0]
    for j in range(ncol):
        for r in tab:
            r[j].set_x(x + (w[j] if center else r[j].width) / 2)
        x += w[j] + gap
    tab.move_to(c)
    if max_width is not None and tab.width > max_width:
        tab.width = max_width
    if tab.get_right()[0] > 6.95:
        tab.shift((6.95 - tab.get_right()[0]) * RIGHT)
    if tab.get_left()[0] < -6.95:
        tab.shift((-6.95 - tab.get_left()[0]) * RIGHT)
    return tab


def note(text: str, font_size=22, color=GREY_B) -> Tex:
    """Small grey caption, e.g. a source line, 'computed' or 'schematic'."""
    return label(text, font_size=font_size, color=color)


def why(text: str, font_size=24) -> Tex:
    """The grey 'why this line follows' note of a derivation."""
    return label(text, font_size=font_size, color=GREY_B)


def mtex(tex, color=WHITE, font_size=36, **kw) -> MathTex:
    if isinstance(tex, (list, tuple)):
        return MathTex(*tex, color=color, font_size=font_size, **kw)
    return MathTex(tex, color=color, font_size=font_size, **kw)


def tagged(text: str, color=WHITE, font_size=28, opacity=0.85) -> Tex:
    t = label(text, color=color, font_size=font_size)
    t.add_background_rectangle(color=BACKGROUND, opacity=opacity, buff=0.06)
    return t


def boxed(mob: Mobject, color=YELLOW, buff=0.25, fill=0.0, stroke_width=2.5) -> VGroup:
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12, stroke_width=stroke_width)
    if fill:
        box.set_fill(color, opacity=fill)
    return VGroup(box, mob)


def num(x: float, digits=3, sign=False) -> str:
    s = f"{x:+.{digits}f}" if sign else f"{x:.{digits}f}"
    return s.replace("-", "{-}")


def sci(x: float, digits=1) -> str:
    """2.5e-06 -> '2.5 \\times 10^{-6}' for MathTex; numbers between 0.01 and 1000 stay plain."""
    if x == 0:
        return "0"
    if 0.01 <= abs(x) < 1000:
        return f"{x:.{max(0, digits + 1 - int(math.floor(math.log10(abs(x)))) - 1)}f}"
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10**e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    ms = f"{m:.{digits}f}"
    if digits and float(ms) == int(float(ms)):
        ms = str(int(float(ms)))
    return (rf"10^{{{e}}}" if ms == "1" else rf"{ms} \times 10^{{{e}}}")


_SUP = str.maketrans("-0123456789", "\u207b\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079")


def sci_text(x: float, digits=1) -> str:
    """Like :func:`sci`, as plain Unicode (for Text mobjects redrawn every frame, which must not call LaTeX)."""
    t = sci(x, digits)
    if "10^" not in t:
        return t
    e = t.split("10^{")[1].rstrip("}")
    head = t.split("10^{")[0].replace(r"\times", "\u00d7").strip()
    return (head + " " if head else "") + "10" + e.translate(_SUP)


def fmt_int(n: int) -> str:
    """12345678 -> '12{,}345{,}678' for MathTex."""
    return f"{int(n):,}".replace(",", "{,}")


def frac_tex(fr: Fraction) -> str:
    return rf"\tfrac{{{fr.numerator}}}{{{fr.denominator}}}" if fr.denominator != 1 else str(fr.numerator)


def computed_tag(text=r"computed", corner=DR) -> Tex:
    return note(text).to_corner(corner, buff=0.3)


def schematic_tag(corner=UR) -> Tex:
    return note(r"schematic").to_corner(corner, buff=0.3)


# ---------------------------------------------------------------------------
# Derivations
# ---------------------------------------------------------------------------
def changed_parts(prev: Mobject, row: Mobject) -> list:
    """The parts of a MathTex row whose TeX does not occur in the previous row (what a derivation step changed)."""
    if not isinstance(row, MathTex) or not isinstance(prev, MathTex):
        return []
    old = {t.strip() for t in prev.tex_strings}
    relations = {"=", "<", ">", r"\le", r"\ge", r"\leq", r"\geq", r"\Rightarrow", r"\iff", r"\in", r"\ne"}
    return [part for part, t in zip(row, row.tex_strings)
            if t.strip() and t.strip() not in old and t.strip() not in relations and len(part) > 0]


def ladder(scene, rows, whys, keep=4, top=2.9, buff=0.48, x=0.0, align_index=1, edge=6.6, highlight=True):
    """Reveal derivation rows one at a time, keeping at most ``keep`` on screen (older rows scroll off the top).
    Each row's ``align_index`` part (usually '=') is lined up at ``x``.  Returns ``step(i)``: the first row is
    written, each later one grows out of a copy of the previous one, and its grey 'why' note fades in beside it
    (or under it when there is no room)."""
    for r, w in zip(rows, whys):
        if align_index is not None:
            r.shift((x - r[align_index].get_center()[0]) * RIGHT)
        else:
            r.set_x(x)
        lo, hi = r.get_left()[0], r.get_right()[0]
        f = 1.0
        if hi > edge:
            f = min(f, (edge - r.get_center()[0]) / (hi - r.get_center()[0]))
        if lo < -edge:
            f = min(f, (r.get_center()[0] + edge) / (r.get_center()[0] - lo))
        if f < 1.0:
            r.scale(f)
        if w is not None:
            w.next_to(r, RIGHT, buff=0.4)
            if w.get_right()[0] > edge:
                w.next_to(r, DOWN, buff=0.22)
                w.set_x(min(r.get_right()[0], edge) - w.width / 2)
                w.set_x(max(w.get_x(), -edge + w.width / 2))
    offs = [0.0 if w is None else w.get_y() - r.get_y() for r, w in zip(rows, whys)]
    extra = [0.0 if w is None else max(0.0, r.get_bottom()[1] - w.get_bottom()[1]) for r, w in zip(rows, whys)]

    def step(i, run_time=1.2, transform=True):
        anims = []
        shown = rows[max(0, i - keep + 1): i]
        if i >= keep:
            anims.append(FadeOut(rows[i - keep], shift=UP * 0.3))
            if whys[i - keep] is not None:
                anims.append(FadeOut(whys[i - keep], shift=UP * 0.3))
        y = top
        targets = []
        for r in list(shown) + [rows[i]]:
            targets.append(y - r.height / 2)
            y -= r.height + buff + extra[rows.index(r)]
        for r, ty in zip(shown, targets[:-1]):
            anims.append(r.animate.set_y(ty))
            j = rows.index(r)
            if whys[j] is not None:
                anims.append(whys[j].animate.set_y(ty + offs[j]))
        rows[i].set_y(targets[-1])
        if whys[i] is not None:
            whys[i].set_y(targets[-1] + offs[i])
        if anims:
            scene.play(*anims, run_time=0.6)
        if i == 0 or not transform:
            scene.play(Write(rows[i]), run_time=run_time)
        else:
            scene.play(TransformMatchingTex(rows[i - 1].copy(), rows[i]), run_time=run_time)
        anims = [FadeIn(whys[i])] if whys[i] is not None else []
        changed = changed_parts(rows[i - 1], rows[i]) if i > 0 else []
        if highlight and changed:
            # a yellow underline sweeps under the parts that are new in this line
            anims += [ShowPassingFlash(Underline(m, buff=0.06, stroke_width=4).set_color(C.EPS), time_width=0.6)
                      for m in changed]
        if anims:
            scene.play(*anims, run_time=0.8 if highlight and changed else 0.5)

    return step


# ---------------------------------------------------------------------------
# The timeline strip: the history of the ideas, lit as the series reaches them
# ---------------------------------------------------------------------------
TIMELINE = [
    (1807, r"Fourier"),
    (1817, r"Bolzano"),
    (1821, r"Cauchy's \emph{Cours}"),
    (1829, r"Dirichlet"),
    (1854, r"Riemann's integral"),
    (1872, r"Dedekind, Cantor, Weierstrass"),
    (1874, r"$\R$ is uncountable"),
    (1883, r"the Cantor set"),
    (1895, r"Heine--Borel"),
    (1902, r"Lebesgue"),
    (1906, r"Fr\'echet: metric spaces"),
    (1907, r"Riesz--Fischer"),
    (1932, r"Banach"),
    (1945, r"Schwartz"),
    (1966, r"Carleson"),
]
T0, T1 = 1800, 1970


def timeline(lit=(), width=12.0, show_labels=True, font_size=18) -> VGroup:
    """The strip from 1800 to 1970; years in ``lit`` glow and get their names."""
    x0 = -width / 2

    def X(y):
        return x0 + width * (y - T0) / (T1 - T0)

    g = VGroup()
    line = Line([X(T0), 0, 0], [X(T1), 0, 0], color=GREY_D, stroke_width=2)
    g.add(line)
    for yr in (1800, 1850, 1900, 1950):
        g.add(Line([X(yr), -0.06, 0], [X(yr), 0.06, 0], color=GREY_D, stroke_width=1.5))
        g.add(Text(str(yr), font_size=14, color=GREY_D).next_to([X(yr), 0, 0], DOWN, buff=0.12))
    labels = VGroup()
    side = 1
    for yr, name in TIMELINE:
        on = yr in lit
        d = Dot([X(yr), 0, 0], radius=0.065 if on else 0.04, color=C.EPS if on else GREY_C)
        g.add(d)
        if on and show_labels:
            t = label(rf"{yr}\; {name}", font_size=font_size, color=C.EPS)
            t.next_to(d, UP if side > 0 else DOWN, buff=0.14 if side > 0 else 0.4)
            side = -side
            labels.add(t)
    g.add(labels)
    g.labels = labels
    return g


def chapter_card(number, title: str, question: str = "", lit=(), part: int | None = None) -> VGroup:
    """Chapter title, the question it answers, and the timeline strip with this chapter's years lit."""
    head = label(rf"{'Part ' + str(part) + r' \textperiodcentered\ ' if part else ''}Chapter {number}", font_size=28,
                 color=GREY_B)
    t = label(title, font_size=54)
    g = VGroup(head, t)
    if question:
        g.add(label(question, font_size=30, color=GREY_A))
    g.arrange(DOWN, buff=0.3).shift(UP * 0.6)
    strip = timeline(lit=lit).to_edge(DOWN, buff=0.9)
    return VGroup(g, strip)


# ---------------------------------------------------------------------------
# The counterexample museum
# ---------------------------------------------------------------------------
def _tex_words(text: str):
    """Split a Tex string into (separator, word) pairs at the spaces (plain or ``\ ``) that lie outside math and
    braces, so a line can be broken there without breaking the TeX."""
    out, cur, sep, depth, math, i = [], "", "", 0, False, 0
    while i < len(text):
        two = text[i:i + 2]
        if two == "\\ " and depth == 0 and not math:
            if cur:
                out.append((sep, cur))
                cur = ""
            sep, i = "\\ ", i + 2
            continue
        if text[i] == "\\" and i + 1 < len(text):
            cur, i = cur + two, i + 2
            continue
        ch = text[i]
        if ch == "$":
            math = not math
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if ch == " " and depth == 0 and not math:
            if cur:
                out.append((sep, cur))
                cur, sep = "", " "
        else:
            cur += ch
        i += 1
    if cur:
        out.append((sep, cur))
    return out


def wrapped_label(text: str, max_width: float, font_size=22, color=WHITE) -> Tex:
    """A label broken into left-aligned lines no wider than ``max_width`` (at word boundaries outside math), rather
    than shrunk; only a single word too wide for a line is ever scaled down."""
    t = label(text, font_size=font_size, color=color)
    if t.width <= max_width:
        return t
    words = _tex_words(text)
    lines, cur = [], words[0][1]
    for sep, w in words[1:]:
        trial = cur + sep + w
        if label(trial, font_size=font_size).width <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) == 1:
        t.width = max_width
        return t
    t = Tex(r"\begin{tabular}{@{}l@{}}" + r"\\".join(lines) + r"\end{tabular}", color=color, font_size=font_size)
    if t.width > max_width:
        t.width = max_width
    return t


def museum_card(name: str, who: str, breaks: str, where: str = "", width=4.6, font_size=22) -> VGroup:
    """A small card with a red corner tag: name; who and when; what it breaks; where it is in Rudin. Long rows wrap
    onto further lines (never shrink), and every row keeps the card's left edge."""
    inner = width - 0.6
    rows = [wrapped_label(name, inner, font_size + 6), wrapped_label(who, inner, font_size, GREY_A),
            wrapped_label(r"\textit{breaks:} " + breaks, inner, font_size, WHITE)]
    if where:
        rows.append(wrapped_label(where, inner, font_size - 2, GREY_B))
    body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    box = RoundedRectangle(width=width, height=body.height + 0.5, corner_radius=0.12, stroke_color=GREY_C,
                           stroke_width=2, fill_color="#151A22", fill_opacity=0.95)
    body.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
    c = box.get_corner(UR)
    # the tag is the corner triangle cut by the card's own rounded outline, so it never pokes past the corner
    tri = Polygon(c, c + LEFT * 0.55, c + DOWN * 0.55)
    tag = Intersection(tri, box.copy(), stroke_width=0, fill_color=C.PATHOLOGY, fill_opacity=1)
    card = VGroup(box, tag, body)
    card.box, card.body = box, body
    return card


# ---------------------------------------------------------------------------
# The ledger
# ---------------------------------------------------------------------------
LEDGER_HEAD = [r"Part", r"space", r"complete because", r"compact means", r"limits we may swap", r"Fourier, so far"]
PART_NAMES = [
    r"the real line", r"limits", r"$C(X)$", r"$\R^n$", r"measure", r"$L^p$, $H$", r"$H(\Omega)$", r"Banach",
    r"distributions", r"spectra",
]
LEDGER_ROWS = {
    1: [r"1", r"$\R$, $\R^k$", r"built so: least upper bounds", r"closed and bounded", r"none yet",
        r"cannot ask yet"],
    2: [r"2", r"sequences, series", r"Cauchy $\Rightarrow$ convergent", r"subsequences converge",
        r"reorder $\sum |a_n| < \infty$", r"converges at each $x$"],
    3: [r"3", r"$C(X)$, sup norm", r"uniform limits are continuous", r"+ equicontinuity (Ascoli)",
        r"$\lim \int = \int \lim$ if uniform", r"in mean square; Gibbs at jumps"],
    4: [r"4", r"$\R^n$; $C[a, b]$ again", r"so contractions have fixed points", r"(as in Parts 1 and 3)",
        r"$\frac{d}{dt}\int = \int \frac{\partial}{\partial t}$", r"(unchanged)"],
    5: [r"5", r"$(X, \mathfrak M, \mu)$", r"(Part 6: $L^1$ is complete)", r"regular: compact sets fill",
        r"$\lim \int = \int \lim$ under a lid", r"term by term, by Fubini"],
    6: [r"6", r"$L^p(\mu)$; \ Hilbert $H$", r"Riesz--Fischer: summable increments", r"not the ball: $\|e_m - e_n\| = \sqrt 2$",
        r"$\frac{d}{dx}\int_a^x f = f$ a.e.", r"$s_N \to f$ in $L^2$; \ Fej\'er: uniform"],
    7: [r"7", r"$H(\Omega)$, \ locally uniform", r"local uniform limits holomorphic", r"bounded families: Montel",
        r"$\frac{d}{dz}\sum = \sum \frac{d}{dz}$; \ $\oint$ and $\lim$", r"$H^2$: \ $\hat f(n) = 0$ for $n < 0$"],
    8: [r"8", r"Banach; \ Fr\'echet", r"Baire: no countable union of thin sets", r"weak-* compact (Alaoglu)",
        r"pointwise bounds are uniform", r"diverges for most $f \in C$; \ a.e.\ for $L^2$"],
    9: [r"9", r"$\mathcal D'$, \ $\mathcal S'$", r"Fr\'echet pieces; \ weak-$*$ limits", r"(bounded sets, \ Montel-like)",
        r"$\partial$ commutes with every limit", r"every series converges in $\mathcal D'$"],
    10: [r"10", r"$B(H)$; \ $C^*$-algebras", r"closed in norm; \ Gelfand--Naimark", r"Alaoglu again: \ $\Delta$ compact",
         r"$f(T)$ for every Borel $f$", r"$\mathcal F$ is the spectral theorem"],
}


def ledger(filled=1, highlight=None, font_size=19, width=13.4) -> VGroup:
    """The series' running table. Rows 1..filled come from LEDGER_ROWS; later rows show only the part's name, dim."""
    col_w = np.array([0.6, 1.9, 2.8, 2.3, 2.6, 3.2])
    col_w = col_w * width / col_w.sum()
    xs = -width / 2 + np.concatenate([[0], np.cumsum(col_w)[:-1]]) + col_w / 2
    row_h = 0.46
    def cells_row(cells, y, size, color):
        # one Tex per row, so every cell sits on the row's baseline; each cell is then moved (sideways only) to its
        # column, and shrunk about that baseline if it is too wide
        t = Tex(*cells, arg_separator=r"\quad ", font_size=size, color=color)
        t.shift(UP * (y - t.get_y()))
        base = t.get_y()
        for part, x, w in zip(t, xs, col_w):
            part.shift(RIGHT * (x - part.get_x()))
            if part.width > w - 0.12:
                part.scale((w - 0.12) / part.width, about_point=np.array([x, base, 0.0]))
        return t

    g = VGroup()
    head = cells_row(LEDGER_HEAD, 0.0, font_size + 1, GREY_A)
    g.add(head)
    rows = VGroup()
    for p in range(1, 11):
        y = -(p) * row_h
        if p <= filled and p in LEDGER_ROWS:
            row = cells_row(LEDGER_ROWS[p], y, font_size, WHITE)
        else:  # the part being announced is legible; parts still to come stay dim
            row = cells_row([str(p), PART_NAMES[p - 1]], y, font_size, WHITE if p == highlight else GREY_D)
        rows.add(row)
    g.add(rows)
    rule = Line([-width / 2, -row_h / 2, 0], [width / 2, -row_h / 2, 0], color=GREY_C, stroke_width=1.5)
    g.add(rule)
    if highlight is not None:
        r = rows[highlight - 1]
        hl = Rectangle(width=width + 0.1, height=row_h * 0.92, stroke_width=0, fill_color=C.EPS, fill_opacity=0.12)
        hl.move_to([0, r.get_y(), 0])
        g.add_to_back(hl)
    g.head, g.rows = head, rows
    return g.move_to(ORIGIN)


# ---------------------------------------------------------------------------
# Rational dust: Q drawn as a ruler
# ---------------------------------------------------------------------------
def rationals_in(a: float, b: float, qmax: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """All p/q in [a, b] (a >= 0) in lowest terms with 1 <= q <= qmax: (values, p, q).

    A Stern-Brocot search in exact integer arithmetic: every fraction in lowest terms is a node of the tree, and a
    run of steps in one direction is taken in a single jump (the continued-fraction trick), so the cost is about
    the number of fractions found, even for windows of width 1e-12 and denominators near 10^8."""
    A, B = Fraction(a), Fraction(b)
    an, ad, bn, bd = A.numerator, A.denominator, B.numerator, B.denominator
    out_p, out_q = [], []
    # fractions <= the integer part are handled by shifting: work on [a - n0, b - n0] with n0 = floor(a)
    n0 = math.floor(a)
    an -= n0 * ad
    bn -= n0 * bd
    stack = [(0, 1, 1, 0)]  # the open interval (p1/q1, p2/q2), starting from (0/1, 1/0)
    if an == 0:  # a itself is an integer: 0/1 is in the window
        out_p.append(0)
        out_q.append(1)
    while stack:
        p1, q1, p2, q2 = stack.pop()
        pm, qm = p1 + p2, q1 + q2
        if qm > qmax:
            continue
        if pm * ad < an * qm:  # mediant below a: slide the left end toward the right one in one jump
            # largest k with (p1 + k p2)/(q1 + k q2) < a, i.e. k (p2 ad - an q2) < an q1 - p1 ad
            num_, den_ = an * q1 - p1 * ad, p2 * ad - an * q2
            k = (num_ - 1) // den_ if den_ > 0 else qmax
            k = max(1, min(k, (qmax - q1) // q2 if q2 else qmax))
            stack.append((p1 + k * p2, q1 + k * q2, p2, q2))
            continue
        if pm * bd > bn * qm:  # mediant above b: slide the right end toward the left one
            num_, den_ = p2 * bd - bn * q2, bn * q1 - p1 * bd
            k = (num_ - 1) // den_ if den_ > 0 else qmax
            k = max(1, min(k, (qmax - q2) // q1 if q1 else qmax))
            stack.append((p1, q1, p2 + k * p1, q2 + k * q1))
            continue
        out_p.append(pm)
        out_q.append(qm)
        stack.append((p1, q1, pm, qm))
        stack.append((pm, qm, p2, q2))
    if not out_p:
        return np.zeros(0), np.zeros(0, np.int64), np.zeros(0, np.int64)
    pp = np.array(out_p, dtype=np.int64) + n0 * np.array(out_q, dtype=np.int64)
    qq = np.array(out_q, dtype=np.int64)
    v = pp / qq
    keep = (v >= a) & (v <= b)
    return v[keep], pp[keep], qq[keep]


def qmax_for(a: float, b: float, target: int = 1400) -> int:
    """Largest denominator so that about ``target`` fractions fall in [a, b] (their count is ~ 3 q^2 (b-a) / pi^2)."""
    return max(1, int(math.sqrt(target * math.pi**2 / (3 * max(b - a, 1e-15)))))


def segments_points(x0, y0, x1, y1) -> np.ndarray:
    """Bezier control points for many disjoint straight segments (x0, y0) -> (x1, y1), for one VMobject: each
    segment is a cubic with its control points on the line, and a gap between segments starts a new subpath."""
    x0, y0, x1, y1 = (np.asarray(v, float) for v in (x0, y0, x1, y1))
    n = len(x0)
    P0 = np.stack([x0, y0, np.zeros(n)], 1)
    P1 = np.stack([x1, y1, np.zeros(n)], 1)
    pts = np.stack([P0, P0 + (P1 - P0) / 3, P0 + 2 * (P1 - P0) / 3, P1], 1)
    return pts.reshape(-1, 3)


def rational_dust(a: float, b: float, x_left: float, x_right: float, y: float = 0.0, height=0.9, target=1400,
                  color=None, stroke_width=2.0, exponent=0.6, qmax=None, bands=6, qref=None, hmax=1.8,
                  split=None, color_hi=None) -> VGroup:
    """The rationals in [a, b] drawn on the screen segment [x_left, x_right] at height y: the tick of p/q (lowest
    terms) rises height * (q / q_ref)^-exponent above the axis (at most hmax * height), so small denominators stand
    tall.  q_ref defaults to the smallest denominator in the window; pass ``qref`` ~ 1/sqrt(b - a) for a picture
    that changes smoothly while zooming.  With ``split`` (a function of the values returning a boolean mask), the
    ticks where it is True are drawn in ``color_hi``.  Ticks are grouped into a few VMobjects by size."""
    color = color or C.RATIONAL
    qmax = qmax or qmax_for(a, b, target)
    v, p, q = rationals_in(a, b, qmax)
    g = VGroup()
    if len(v) == 0:
        return g
    if split is not None:
        mask = np.asarray(split(v, p, q), bool)
        lo = rational_dust_from(v[~mask], q[~mask], a, b, x_left, x_right, y, height, color, stroke_width, exponent,
                                bands, qref or q.min(), hmax)
        hi = rational_dust_from(v[mask], q[mask], a, b, x_left, x_right, y, height, color_hi, stroke_width, exponent,
                                bands, qref or q.min(), hmax)
        g.add(lo, hi)
        g.values, g.q = v, q
        return g
    g = rational_dust_from(v, q, a, b, x_left, x_right, y, height, color, stroke_width, exponent, bands,
                           qref or q.min(), hmax)
    g.values, g.q = v, q
    return g


def rational_dust_from(v, q, a, b, x_left, x_right, y, height, color, stroke_width, exponent, bands, qref, hmax):
    g = VGroup()
    if len(v) == 0:
        return g
    h = height * np.minimum(hmax, (q / qref) ** (-exponent))
    xs = x_left + (v - a) / (b - a) * (x_right - x_left)
    edges = np.quantile(h, np.linspace(0, 1, bands + 1)) if len(h) > bands else np.array([h.min()] * bands + [h.max()])
    for k in range(bands):
        sel = (h >= edges[k]) & ((h < edges[k + 1]) if k < bands - 1 else (h <= edges[k + 1]))
        if not sel.any():
            continue
        m = VMobject(stroke_color=color, stroke_width=stroke_width * (0.55 + 0.45 * k / max(1, bands - 1)),
                     stroke_opacity=0.35 + 0.65 * k / max(1, bands - 1))
        m.set_points(segments_points(xs[sel], np.full(sel.sum(), y), xs[sel], y + h[sel]))
        g.add(m)
    return g


# ---------------------------------------------------------------------------
# The dictionary card: the same theorem in R^n and in a function space
# ---------------------------------------------------------------------------
def dictionary_card(left_title: str, right_title: str, pairs, font_size=26, width=12.4, strike=()) -> VGroup:
    """Two columns of statements.  ``strike`` lists row indices whose right-hand side is crossed out (a theorem that
    fails in the function space)."""
    lt = label(left_title, font_size=font_size + 4, color=GREY_A)
    rt = label(right_title, font_size=font_size + 4, color=GREY_A)
    lx, rx = -width / 4, width / 4
    lt.move_to([lx, 0, 0])
    rt.move_to([rx, 0, 0])
    rows = VGroup()
    y = -0.75
    for i, (l, r) in enumerate(pairs):
        lm = label(l, font_size=font_size).move_to([lx, y, 0])
        rm = label(r, font_size=font_size).move_to([rx, y, 0])
        for m in (lm, rm):  # keep clear of the arrow in the middle
            if m.width > width / 2 - 1.3:
                m.width = width / 2 - 1.3
        row = VGroup(lm, rm)
        if i in strike:
            row.add(Line(rm.get_left() + LEFT * 0.1, rm.get_right() + RIGHT * 0.1, color=C.PATHOLOGY, stroke_width=4))
        rows.add(row)
        y -= max(lm.height, rm.height) + 0.45
    arrows = VGroup(*[MathTex(r"\longleftrightarrow", color=GREY_C, font_size=34).move_to([0, r[0].get_y(), 0])
                      for r in rows])
    mid = Line([0, 0.3, 0], [0, y + 0.3, 0], color=GREY_D, stroke_width=1.5)
    g = VGroup(lt, rt, rows, arrows)
    g.titles, g.rows, g.arrows, g.mid = VGroup(lt, rt), rows, arrows, mid
    return g.move_to(ORIGIN)


def magnifier(src_ax: Axes, x_window, y_window, center, width=3.4, height=2.4, color=GREY_B, tag=None) -> tuple:
    """A magnified view of the window x_window × y_window of ``src_ax``, drawn as a framed inset at ``center``.

    Returns ``(inset_ax, decor)``: draw on ``inset_ax`` with the same functions and trackers as on the source (it
    has invisible axes, so nothing but your drawings and the frame show); ``decor`` holds the small frame on the
    source, the inset's frame, the two guide lines between them, and the magnification tag."""
    x0, x1 = x_window
    y0, y1 = y_window
    inset = Axes(x_range=[x0, x1, x1 - x0], y_range=[y0, y1, y1 - y0], x_length=width, y_length=height, tips=False,
                 axis_config={"stroke_opacity": 0, "include_ticks": False}).move_to(center)
    p0, p1 = src_ax.c2p(x0, y0), src_ax.c2p(x1, y1)
    src = Rectangle(width=max(p1[0] - p0[0], 0.04), height=max(p1[1] - p0[1], 0.04), color=color, stroke_width=2)
    src.move_to((p0 + p1) / 2)
    dst = Rectangle(width=width, height=height, color=color, stroke_width=2).move_to(center)
    dst.set_fill(BACKGROUND, opacity=1.0)
    if center[0] >= src.get_center()[0]:
        pairs = ((src.get_corner(UR), dst.get_corner(UL)), (src.get_corner(DR), dst.get_corner(DL)))
    else:
        pairs = ((src.get_corner(UL), dst.get_corner(UR)), (src.get_corner(DL), dst.get_corner(DR)))
    guides = VGroup(*[DashedLine(a, b, color=color, stroke_width=1.5, dash_length=0.08) for a, b in pairs])
    k = (width / max(p1[0] - p0[0], 1e-9))
    tag = tag if tag is not None else rf"\times {k:.0f}"
    t = MathTex(tag, font_size=24, color=color).next_to(dst, UP, buff=0.08).align_to(dst, LEFT)
    decor = VGroup(src, guides, dst, t)
    decor.src, decor.guides, decor.frame, decor.tag = src, guides, dst, t
    return inset, decor


from .gameboard import FunctionBoard, SequenceBoard, largest_delta  # noqa: E402,F401
from .dashboard import Dashboard, FunctionCamera, fast_graph, runs  # noqa: E402,F401
from .proofmap import ProofMap  # noqa: E402,F401
from .contours import contour_mobject, contour_segments, contours  # noqa: E402,F401
from .complexplot import domain_image, domain_rgb, hue_rgb  # noqa: E402,F401
