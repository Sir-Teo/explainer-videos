from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis1.common import partial_curve, polyline, saw_axes, saw_graph


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.ledger_row()
        self.next_time()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        items = [
            (r"$\Q$ has holes: \ $\{p : p^2 < 2\}$ has no supremum in $\Q$", C.HOLE),
            (r"$\R$ = Dedekind cuts; \ the supremum is the union", C.CUT_LOW),
            (r"Archimedes, density of $\Q$, nested intervals, bisection", C.COMPACT_SET),
            (r"$\Q$ is countable, $\R$ is not \ (the diagonal; perfect sets)", C.EPS),
            (r"metric spaces: three axioms; \ functions as points", C.DIST),
            (r"open, closed, closure; \ open is relative", C.OPEN_SET),
            (r"compact: every open cover has a finite subcover", C.COMPACT_SET),
            (r"Heine--Borel: in $\R^k$, compact $=$ closed and bounded", C.COMPACT_SET),
            (r"the Cantor set: uncountable, length $0$", WHITE),
            (r"connected subsets of $\R$ are the intervals", C.CONNECTED_SET),
            (r"in $C[0,1]$, closed and bounded is \emph{not} compact", C.PATHOLOGY),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\; {t}", font_size=27, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 0.15)
        head = label(r"Part 1, in eleven lines", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. We found that the rationals have holes, and filled them in a way that turns having no "
            "holes into a theorem: every nonempty set that's bounded above has a least upper bound. We used that to prove the Archimedean "
            "property, density, and the nested interval theorem, and we built the bisection engine. We learned that the "
            "rationals, dense as they are, are countable, while the reals are not. Then we stepped back to metric "
            "spaces, where a function can be a point, and built the vocabulary: open, closed, compact, connected. We "
            "proved Heine–Borel by bisection, met the Cantor set, and found that our first function space already breaks "
            "Heine–Borel."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger_row(self):
        empty = ledger(filled=0, highlight=1).scale(0.95)
        full = ledger(filled=1, highlight=1).scale(0.95)
        with self.voiceover(
            "And the ledger gets its first row. <bookmark mark='a'/> The space: the real line, and k-dimensional space. "
            "Complete because we built it so, with least upper bounds. Compact means closed and bounded. Which limits may "
            "we swap? None yet. And Fourier's question: we can't even ask it yet, because we haven't said what it means "
            "for a sequence of functions to converge."
        ) as vo:
            self.play(FadeIn(empty))
            vo.wait_until("a")
            self.play(LaggedStart(*[TransformFromCopy(full.rows[0][i], full.rows[0][i]) for i in range(len(full.rows[0]))],
                                  lag_ratio=0.5), FadeOut(empty.rows[0]), run_time=4)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        ax = saw_axes(x_length=9.0, y_length=3.2).shift(UP * 0.6)
        saw = saw_graph(ax, stroke_width=3)
        S = partial_curve(ax, 30, stroke_width=2.5, samples=1800)
        head = label(r"Next: Part 2, \ Limits", font_size=44).to_edge(UP, buff=0.35)
        rearr = MathTex(r"1 - \tfrac12 + \tfrac13 - \tfrac14 + \cdots = \ln 2", font_size=40)
        rearr2 = label(r"\ldots and, rearranged, $= \pi$. \ Or $-1$. \ Or anything.", font_size=32, color=C.EPS)
        bottom = VGroup(rearr, rearr2).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        # the alternating harmonic series, in order and rearranged (positive terms until the sum passes pi,
        # then negative terms until it drops below, and so on): the same terms, two different sums
        N = 3000  # by then the rearranged sums dip less than 0.03 below pi
        alt = np.cumsum([(-1) ** (k + 1) / k for k in range(1, N + 1)])
        pos, neg, s_, rear, used = 1, 2, 0.0, [], set()
        for _ in range(N):
            if s_ <= np.pi:
                s_ += 1 / pos
                used.add(pos)
                pos += 2
            else:
                s_ -= 1 / neg
                used.add(neg)
                neg += 2
            rear.append(s_)
        rear = np.array(rear)
        assert len(used) == N  # each term used once
        assert abs(alt[-1] - np.log(2)) < 1 / (N + 1) and abs(rear[-1] - np.pi) < 0.05
        pax = Axes(x_range=[0, N, 500], y_range=[0, 3.5, 1], x_length=9.0, y_length=3.2, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).shift(UP * 0.6)
        ns = np.arange(1, N + 1)
        alt_c = polyline(pax, ns, alt, color=C.SEQ, stroke_width=2.5)
        rear_c = polyline(pax, ns, rear, color=C.APPROX, stroke_width=2.5)
        ln2 = VGroup(DashedLine(pax.c2p(0, np.log(2)), pax.c2p(N, np.log(2)), color=C.SEQ, stroke_width=1.5),
                     MathTex(r"\ln 2", font_size=26, color=C.SEQ).next_to(pax.c2p(N, np.log(2)), RIGHT, buff=0.15))
        pi_l = VGroup(DashedLine(pax.c2p(0, np.pi), pax.c2p(N, np.pi), color=C.APPROX, stroke_width=1.5),
                      MathTex(r"\pi", font_size=28, color=C.APPROX).next_to(pax.c2p(N, np.pi), RIGHT, buff=0.15))
        n_l = MathTex(r"n", font_size=24, color=GREY_B).next_to(pax.c2p(N, 0), RIGHT, buff=0.15)
        s_l = label(r"partial sums", font_size=22, color=GREY_B).next_to(pax.c2p(0, 3.5), RIGHT, buff=0.15)
        with self.voiceover(
            "Next time, in Part 2, we put the new real numbers to work: <bookmark mark='a'/> sequences, series, "
            "continuity and the derivative, the limits behind Fourier's sum. <bookmark mark='b'/> It opens with a shock: "
            "the alternating harmonic series adds up to the natural log of two, but rearrange its terms and you can make "
            "it add up to pi, or minus one, or anything you like."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(saw))
            vo.wait_until("a")
            self.play(Create(S), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(ax, saw, S)), Create(pax), FadeIn(n_l), FadeIn(s_l), run_time=0.8)
            self.play(Write(rearr), Create(alt_c), FadeIn(ln2), run_time=1.6)
            self.play(FadeIn(rearr2), Create(rear_c), FadeIn(pi_l), run_time=2.0)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Following W.~Rudin, \textit{Principles of Mathematical Analysis}, 3rd ed.\ (1976), chapters 1--2", font_size=24),
            label(r"R.~Dedekind, \textit{Stetigkeit und irrationale Zahlen} (1872) \quad G.~Cantor (1874, 1883, 1891)",
                  font_size=24, color=GREY_A),
            label(r"E.~Heine (1872), \ E.~Borel (1895), \ M.~Fr\'echet (1906), \ F.~Hausdorff (1914)", font_size=24,
                  color=GREY_A),
            label(r"Companions: S.~Abbott, \textit{Understanding Analysis}; \ C.~Pugh, \textit{Real Mathematical Analysis};"
                  r" \ T.~Tao, \textit{Analysis I}", font_size=24, color=GREY_A),
            label(r"Every number on screen is computed and checked; schematics are labeled.", font_size=24, color=C.EPS),
            label(rf"Animated with Manim Community; narrated by {narration_credit()}.", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        with self.voiceover(
            "This part followed the first two chapters of Rudin's Principles of Mathematical Analysis. Thanks for "
            "watching, and see you in Part 2."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(l_, shift=UP * 0.1) for l_ in lines], lag_ratio=0.25), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(lines))
