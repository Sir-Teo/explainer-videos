from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from explainer.analysis import TIMELINE


def _appear(e):
    return AnimationGroup(Create(e[0]), FadeIn(e[1], scale=0.5), FadeIn(e[2], shift=UP * 0.1))


def place_labels(xs, widths, tiers, allowed, limit=20000):
    """Tier and centre for each label (time order), by depth-first search: labels on a tier don't touch, and no
    leader crosses a label nearer the axis on its side. Nearest tiers are tried first."""
    place, count = [], [0]

    def clash(a, b):
        (xa, ta, la, ha), (xb, tb, lb, hb) = a, b
        if ta == tb:
            return not (ha < lb or la > hb)
        if ta * tb < 0:
            return False
        if abs(ta) > abs(tb):
            return lb - 0.05 < xa < hb + 0.05
        return la - 0.05 < xb < ha + 0.05

    def search(k):
        count[0] += 1
        if count[0] > limit:
            raise ValueError("timeline labels: search limit")
        if k == len(xs):
            return True
        w = widths[k]
        for ty in tiers:
            for cx in (xs[k], xs[k] + w / 2 - 0.3, xs[k] - w / 2 + 0.3):
                cx = min(max(cx, -7.0 + w / 2), 7.0 - w / 2)
                cand = (xs[k], ty, cx - w / 2 - 0.12, cx + w / 2 + 0.12)
                if allowed(ty, cand[2], cand[3]) and not any(clash(cand, p_) for p_ in place):
                    place.append(cand)
                    if search(k + 1):
                        return True
                    place.pop()
        return False

    if not search(0):
        raise ValueError("timeline labels do not fit")
    return [(ty, (lo + hi) / 2) for _, ty, lo, hi in place]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.timeline_()
        self.beyond()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"Banach algebras: \ the Neumann series; \ the invertibles are open", C.OPERATOR),
            (r"the spectrum: \ compact, \ nonempty (Liouville); \ $\rho = \lim\|x^n\|^{1/n}$; \ the Volterra operator",
             C.SPECTRUM),
            (r"functions of operators by Cauchy's formula; \ spectral mapping", C.EPS),
            (r"Gelfand: \ elements become functions; \ Wiener's $1/f$ in three lines; \ $C^*$-algebras", C.FREQ),
            (r"Hilbert space: \ adjoints, \ projections, \ the numerical range", C.INNER),
            (r"compact self-adjoint: \ an eigenbasis; \ the string's sines; \ the heat equation", C.APPROX),
            (r"multiplication by $x$: \ a spectrum without eigenvectors; \ the Born rule", C.MEASURE),
            (r"the spectral theorem: \ $T = \int \lambda\, dE$, \ proved with the whole series", C.SPECTRUM),
            (r"unbounded operators: \ domains, \ a circle of self-adjoint extensions", C.PATHOLOGY),
            (r"the Cayley transform; \ momentum diagonalized by the Fourier transform", C.OPERATOR),
            (r"Stone's theorem: \ time evolution is a unitary group", C.EPS),
            (r"quantum mechanics' assumptions, \ now theorems", C.CONNECTED_SET),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=25, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to(DOWN * 0.35)
        for r_ in rows:
            if r_.width > 13.0:
                r_.width = 13.0
        head = label(r"Part 10, in twelve lines", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Let's take stock one last time. Banach algebras gave operators an arithmetic, with the Neumann series "
            "and an open set of invertibles. The spectrum is compact and never empty, and Gelfand's formula measures "
            "it. Cauchy's formula gave functions of operators, and Gelfand's transform turned commutative algebras "
            "into functions. In Hilbert space, compact self-adjoint operators have eigenbases, multiplication by x "
            "has none and is still diagonal, and the spectral theorem handles every normal operator, then every "
            "self-adjoint one, through the Cayley transform. Stone's theorem closed the loop with quantum mechanics."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        before = ledger(filled=9, highlight=10).scale(0.95)
        after = ledger(filled=10, highlight=10).scale(0.95)
        full = ledger(filled=10).scale(0.95)
        with self.voiceover(
            "The ledger's last row. <bookmark mark='a'/> The space: bounded operators, and the C-star algebras they "
            "generate. <bookmark mark='c2'/> Completeness: they're closed in norm, and Gelfand-Naimark makes them function algebras. "
            "<bookmark mark='c3'/> Compactness: Alaoglu again, behind the maximal ideal space. <bookmark mark='c4'/> The interchange: f of T for every Borel "
            "function f, so limits of functions become limits of operators. <bookmark mark='c5'/> And the Fourier answer: the Fourier "
            "transform is the spectral theorem, for momentum. <bookmark mark='b'/> And that's the whole ledger: ten "
            "rows, from the least upper bound property to the spectral theorem."
        ) as vo:
            self.play(FadeIn(before))
            vo.wait_until("a")
            self.play(FadeOut(before.rows[9]), *[TransformFromCopy(after.rows[9][i], after.rows[9][i]) for i in (0, 1)],
                      Indicate(before.head[1], color=C.EPS), run_time=1.5)
            for k_ in range(2, len(after.rows[9])):  # each cell arrives with its sentence
                vo.wait_until(f"c{k_}")
                self.play(TransformFromCopy(after.rows[9][k_], after.rows[9][k_]),
                          Indicate(before.head[k_], color=C.EPS), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeOut(before), FadeOut(after.rows[9]), FadeIn(full))
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def timeline_(self):
        """All fifteen dates: the strip, with the crowded years 1866--1912 magnified in a panel below it."""
        W, y0, Z0, Z1, zw, zy = 12.8, 1.0, 1866, 1912, 12.0, -1.95

        def X(yr):
            return -W / 2 + W * (yr - 1800) / 170

        def Xz(yr):
            return -zw / 2 + zw * (yr - Z0) / (Z1 - Z0)

        def strip(x_of, y, years, ticks):
            g = VGroup(Line([x_of(years[0]), y, 0], [x_of(years[1]), y, 0], color=GREY_C, stroke_width=2))
            for yr in ticks:
                g.add(Line([x_of(yr), y - 0.06, 0], [x_of(yr), y + 0.06, 0], color=GREY_C, stroke_width=1.5))
                g.add(Text(str(yr), font_size=14, color=GREY_C).next_to([x_of(yr), y, 0], DOWN, buff=0.12))
            return g

        def events(items, x_of, y, tiers, allowed):
            labs = [label(rf"{yr}\; {name}", font_size=19, color=C.EPS) for yr, name in items]
            spots = place_labels([x_of(yr) for yr, _ in items], [t.width for t in labs], tiers, allowed)
            out = []
            for (yr, _), t, (ty, cx) in zip(items, labs, spots):
                t.move_to([cx, y + ty, 0])
                end = t.get_bottom() if ty > 0 else t.get_top()
                lead = Line([x_of(yr), y, 0], [x_of(yr), end[1] + (-0.06 if ty > 0 else 0.06), 0], color=C.EPS,
                            stroke_width=1.2, stroke_opacity=0.6)
                out.append(VGroup(lead, Dot([x_of(yr), y, 0], radius=0.065, color=C.EPS), t))
            return out

        # the magnifier: band on the strip, a cone, and the panel
        pan = RoundedRectangle(width=13.6, height=2.35, corner_radius=0.15, stroke_color=C.EPS, stroke_width=1.5,
                               stroke_opacity=0.5, fill_color="#151A22", fill_opacity=0.6).move_to([0, zy + 0.12, 0])
        band = Rectangle(width=X(Z1) - X(Z0), height=0.24, stroke_color=C.EPS, stroke_width=1.2, fill_color=C.EPS,
                         fill_opacity=0.15).move_to([(X(Z0) + X(Z1)) / 2, y0, 0])
        a_l, a_r = np.array([X(Z0), y0 - 0.12, 0]), np.array([X(Z1), y0 - 0.12, 0])
        b_l, b_r = pan.get_corner(UL), pan.get_corner(UR)
        cone = VGroup(Polygon(a_l, a_r, b_r, b_l, stroke_width=0, fill_color=C.EPS, fill_opacity=0.05),
                      Line(a_l, b_l, color=C.EPS, stroke_width=1.2, stroke_opacity=0.45),
                      Line(a_r, b_r, color=C.EPS, stroke_width=1.2, stroke_opacity=0.45))

        def outside_cone(ty, lo, hi):  # labels under the strip stay clear of the cone's edges
            if ty > 0:
                return True
            yb = y0 + ty - 0.15
            t = (a_l[1] - yb) / (a_l[1] - b_l[1])
            return hi < a_l[0] + t * (b_l[0] - a_l[0]) or lo > a_r[0] + t * (b_r[0] - a_r[0])

        crowded = [(yr, n) for yr, n in TIMELINE if Z0 <= yr <= Z1]
        early = [(yr, n) for yr, n in TIMELINE if yr < Z0]
        late = [(yr, n) for yr, n in TIMELINE if yr > Z1]
        sparse = events(early + late, X, y0, [0.45, -0.5, 0.95, 1.45], outside_cone)
        dense = events(crowded, Xz, zy, [0.5, -0.55, 1.0, -1.0], lambda ty, lo, hi: lo > -6.6 and hi < 6.6)
        base = strip(X, y0, (1800, 1970), (1800, 1850, 1900, 1950))
        zbase = strip(Xz, zy, (Z0, Z1), (1870, 1880, 1890, 1900, 1910))
        mag = (zw / (Z1 - Z0)) / (W / 170)
        tag = label(rf"{Z0}--{Z1}, \ magnified $\times{mag:.1f}$", font_size=18, color=GREY_B).move_to(
            pan.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=UL)
        head = label(r"The Fourier thread, \ from 1807 to 1966", font_size=36).to_edge(UP, buff=0.3)
        with self.voiceover(
            "And the timeline is complete: from Fourier's claim in 1807 that every function is a sum of sines, "
            "through Dirichlet and Riemann; <bookmark mark='z'/> then forty crowded years: Dedekind and Cantor, "
            "Heine and Borel, Lebesgue, Fréchet, Riesz and Fischer; <bookmark mark='l'/> then Banach and Schwartz, "
            "to Carleson's theorem in 1966. Every idea in the series was invented to answer a question about "
            "Fourier series."
        ) as vo:
            self.play(FadeIn(head), Create(base), run_time=1.0)
            self.play(LaggedStart(*[_appear(e) for e in sparse[:len(early)]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("z")
            self.play(FadeIn(band), FadeIn(cone), FadeIn(pan), Create(zbase), FadeIn(tag), run_time=1.2)
            self.play(LaggedStart(*[_appear(e) for e in dense], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("l")
            self.play(LaggedStart(*[_appear(e) for e in sparse[len(early):]], lag_ratio=0.5), run_time=2.5)
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beyond(self):
        items = [
            (r"operator algebras: \ von Neumann algebras, \ noncommutative geometry", C.INNER),
            (r"index theory: \ Fredholm operators, \ Atiyah--Singer", C.OPERATOR),
            (r"nonlinear analysis: \ fixed points, \ variational methods, \ Sobolev spaces at work", C.APPROX),
            (r"partial differential equations: \ distributions, \ Fourier, \ and spectra, \ together", C.FREQ),
            (r"harmonic analysis: \ Carleson's theorem, \ singular integrals, \ wavelets", C.EPS),
        ]
        rows = VGroup(*[label(t, font_size=28, color=c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.move_to(DOWN * 0.2)
        head = label(r"Where the road goes next", font_size=38).to_edge(UP, buff=0.4)
        with self.voiceover(
            "From here the road divides. Operator algebras and noncommutative geometry. Index theory. Nonlinear "
            "analysis, where Sobolev spaces do their real work. Partial differential equations, which use all of it. "
            "And harmonic analysis, which is still answering Fourier's question."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.5),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Functional Analysis}, 2nd ed.\ (1991), chapters 4 and 10--13, \ and "
                  r"\textit{Real and Complex Analysis}, chapter 18", font_size=22),
            label(r"I.~Gelfand (1941), \ M.~Naimark, \ J.~von Neumann (1929--32), \ M.~H.~Stone (1932), \ "
                  r"H.~Wielandt (1949), \ V.~Lomonosov (1973)", font_size=22, color=GREY_A),
            label(r"D.~Hilbert, \ E.~Schmidt, \ F.~Riesz, \ C.~Neumann, \ V.~Volterra, \ A.~Cayley, \ J.~Rydberg",
                  font_size=22, color=GREY_A),
            label(r"Companions: \ M.~Reed and B.~Simon, \textit{Methods of Modern Mathematical Physics I}; \ "
                  r"J.~Conway, \textit{A Course in Functional Analysis}", font_size=22, color=GREY_A),
            label(r"Toured, \ not proved: \ GNS, \ Lomonosov, \ Fuglede--Putnam, \ Hille--Yosida, \ deficiency-index "
                  r"classification", font_size=22, color=GREY_B),
            label(r"Every number on screen is computed and checked; \ the pictures marked schematic are the exceptions.",
                  font_size=24, color=C.EPS),
            label(rf"Animated with Manim Community; narrated by {narration_credit()}.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.28).move_to(UP * 0.1)
        for l_ in lines:
            if l_.width > 13.2:
                l_.width = 13.2
        with self.voiceover(
            "This part followed chapters ten to thirteen of Functional Analysis and chapter eighteen of Real and "
            "Complex Analysis. That's the end of the series. Thanks for watching all of it."
        ):
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.5)
        self.play(FadeOut(lines))
