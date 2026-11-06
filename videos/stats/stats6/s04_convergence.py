from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


def typewriter(n: int) -> tuple[float, float]:
    """The n-th block (n >= 1): level k has 2^k blocks of width 2^-k sweeping [0, 1]."""
    k = int(np.floor(np.log2(n)))
    j = n - 2 ** k
    return j / 2 ** k, (j + 1) / 2 ** k


class Convergence(VoiceoverScene):
    def construct(self):
        self.card()
        self.definitions()
        self.mirror()
        self.typewriter()
        self.strong()
        self.hierarchy()

    def card(self):
        card = chapter_card(3, r"Kinds of convergence", r"What does it mean for a random quantity to settle?", part=PART)
        with self.voiceover("Chapter three. What it means for random things to converge."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definitions(self):
        dfs = VGroup(
            definition_card(r"In probability", r"$X_n \xrightarrow{P} X$: \ for every $\varepsilon > 0$, \ "
                            r"$P(|X_n - X| > \varepsilon) \to 0$", color=SIM, width=6.0, font_size=24),
            definition_card(r"In distribution", r"$X_n \xrightarrow{d} X$: \ $P(X_n \le x) \to P(X \le x)$ \ at every $x$ where "
                            r"the limit's CDF is continuous", color=EXACT, width=6.0, font_size=24),
            definition_card(r"Almost surely", r"$X_n \xrightarrow{a.s.} X$: \ $P(X_n \to X) = 1$: \ for almost every outcome, "
                            r"the sequence of numbers converges", color=S.PRIOR, width=6.0, font_size=24),
        ).arrange(DOWN, buff=0.35).move_to([-3.2, -0.1, 0])
        side = VGroup(label(r"the weak law: \ in probability", font_size=26, color=SIM),
                      label(r"the CLT: \ in distribution", font_size=26, color=EXACT),
                      label(r"the strong law: \ almost surely", font_size=26, color=S.PRIOR))
        for s_, d_ in zip(side, dfs):
            s_.move_to([3.8, d_.get_center()[1], 0])
        intro = label('Three meanings of convergence', font_size=36)
        with self.voiceover(
            "A sequence of numbers converges if it gets and stays close to its limit. For random variables there "
            "are several ways to say that, and the difference matters. <bookmark mark='a'/> In probability: the "
            "chance of being more than epsilon away goes to zero. That's what the weak law gave us. "
            "<bookmark mark='b'/> In distribution: the CDFs converge, at least where the limit's CDF has no jump. "
            "This only compares the shapes of the distributions, and it's what the central limit theorem will "
            "deliver. <bookmark mark='c'/> Almost surely: for almost every outcome of the whole infinite experiment, "
            "the sequence of numbers it produces converges. That's the strong law."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(dfs[k], shift=RIGHT * 0.2), FadeIn(side[k]))
        self.clear_scene()

    def mirror(self):
        g = np.random.Generator(np.random.PCG64(7))
        x = g.standard_normal(800)
        A = axes([-3.2, 3.2], [-3.2, 3.2], x_length=4.4, y_length=4.4, xlabel=r"$X$", ylabel=r"$X_n = -X$", xticks=[-2, 0, 2],
                 yticks=[-2, 0, 2], center=[-4.0, -0.4, 0])
        pts = scatter(A.ax, x, -x, color=SIM, radius=0.022, opacity=0.6)
        B = axes([-3.5, 3.5], [0, 0.55], x_length=4.4, y_length=2.6, xlabel=r"both histograms", xticks=[-2, 0, 2],
                 center=[2.6, 1.3, 0])
        ed = np.linspace(-3.5, 3.5, 29)
        h1 = hist_bars(B.ax, ed, np.histogram(x, ed, density=True)[0], color=SIM, opacity=0.5)
        h2 = hist_bars(B.ax, ed, np.histogram(-x, ed, density=True)[0], color=EXACT, opacity=0.35)
        rows = VGroup(label(r"$X_n = -X$ has exactly the law of $X$: \ in distribution, trivially", font_size=24, color=EXACT),
                      label(r"but $|X_n - X| = 2|X|$ never shrinks: \ not in probability", font_size=24, color=BOUND),
                      label(r"in distribution says nothing about the values, \ only their shape", font_size=24,
                            color=S.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -1.9, 0])
        for r in rows:
            if r.width > 7.4:
                r.width = 7.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -1.9, 0])  # re-align after clamping
        tag = note(r"simulated: 800 standard normals").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Convergence in distribution is the weakest of the three. <bookmark mark='a'/> Take a standard normal X, "
            "and let every X n be minus X. Minus X has exactly the same distribution as X, so the sequence converges "
            "to X in distribution: trivially, it's already there. <bookmark mark='b'/> But X n and X are never "
            "close: they're mirror images, and the gap, twice the size of X, never shrinks. <bookmark mark='c'/> "
            "Convergence in distribution is a statement about the shape of a histogram, not about the values. That's "
            "exactly what we need to compute probabilities, and nothing more."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h1), FadeIn(h2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts, lag_ratio=0.002), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def typewriter(self):
        x0, x1, y0 = -5.0, 5.0, 0.6
        L = Line([x0, y0, 0], [x1, y0, 0], color=GREY_B, stroke_width=2)
        ticks = VGroup(MathTex("0", font_size=24, color=GREY_B).next_to([x0, y0, 0], DOWN, buff=0.15),
                       MathTex("1", font_size=24, color=GREY_B).next_to([x1, y0, 0], DOWN, buff=0.15))
        omega = 0.62
        wx = x0 + omega * (x1 - x0)
        wdot = Dot([wx, y0, 0], radius=0.08, color=S.ACCENT)
        wl = MathTex(r"\omega", font_size=30, color=S.ACCENT).next_to(wdot, DOWN, buff=0.35)
        blk = Rectangle(width=x1 - x0, height=0.5, stroke_width=0, fill_color=BOUND, fill_opacity=0.6)
        blk.move_to([(x0 + x1) / 2, y0 + 0.3, 0])
        nlab = MathTex(r"n = 1", font_size=30).move_to([0, 2.4, 0])
        hits = VGroup()
        strip_y = -1.4
        title = label(r"$0\le\omega<1$: $X_n(\omega) = 1$ if $\omega$ is under block $n$, \ else $0$", font_size=26).move_to([0, 3.3, 0])
        rows = VGroup(label(r"$P(X_n = 1) = $ the block's width $\to 0$: \ $X_n \to 0$ in probability", font_size=24, color=SIM),
                      label(r"but every $\omega$ is hit once in every sweep: \ $X_n(\omega) = 1$ infinitely often", font_size=24,
                            color=BOUND),
                      label(r"so $X_n(\omega)$ converges for \emph{no} $\omega$: \ not almost surely", font_size=24, color=S.PRIOR)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)
        cap = label(r"$X_n(\omega)$:", font_size=24, color=GREY_B).move_to([x0 - 0.8, strip_y, 0])
        with self.voiceover(
            "And convergence in probability is weaker than almost sure convergence. Here's the classic example, "
            "sometimes called the typewriter. <bookmark mark='a'/> Pick a uniform random point omega in the unit interval. "
            "A block sweeps across the interval: first one block the whole width, then two halves in turn, then four "
            "quarters, then eight eighths. X n is one if omega is under the n-th block. <bookmark mark='b'/> The "
            "blocks shrink, so the chance that X n is one goes to zero: X n converges to zero in probability. "
            "<bookmark mark='c'/> But every sweep passes over every point, so for every omega, X n keeps returning "
            "to one, forever, however rarely. <bookmark mark='d'/> The sequence of values converges for no omega at "
            "all. A small chance at each time is not the same as eventually never."
        ) as vo:
            self.play(Create(L), FadeIn(ticks), FadeIn(wdot), FadeIn(wl), FadeIn(title), FadeIn(cap))
            vo.wait_until("a")
            self.add(blk, nlab)
            for n in range(1, 32):
                a, b = typewriter(n)
                tgt = Rectangle(width=(b - a) * (x1 - x0), height=0.5, stroke_width=0, fill_color=BOUND, fill_opacity=0.6)
                tgt.move_to([x0 + (a + b) / 2 * (x1 - x0), y0 + 0.3, 0])
                hit = a <= omega < b
                mark = Square(side_length=0.13, stroke_width=0, fill_color=BOUND if hit else GREY_D, fill_opacity=1)
                mark.move_to([x0 + 0.1 + 0.3 * (n - 1), strip_y, 0])
                hits.add(mark)
                self.play(Transform(blk, tgt), Transform(nlab, MathTex(rf"n = {n}", font_size=30).move_to(nlab)), FadeIn(mark),
                          run_time=0.45 if n < 8 else 0.25)
                if n == 7:
                    vo.wait_until("b")
                    self.play(FadeIn(rows[0]))
                if n == 15:
                    vo.wait_until("c")
                    self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def strong(self):
        d = load("paths")
        ms, late, at = np.asarray(d["ms"]), np.asarray(d["late"]), np.asarray(d["at"])
        A = axes([1.8, 4.2], [0, 1.05], x_length=6.6, y_length=4.2, xlabel=r"$m$ (log scale)",
                 ylabel=r"share of 2,000 sequences", xticks=[2, 3, 4], yticks=[0, 0.5, 1], xfmt=lambda v: f"10^{{{int(v)}}}",
                 center=[-2.6, -0.4, 0])
        ax = A.ax
        c_at = VGroup(polyline(ax, np.log10(ms), at, SIM, 3), *[Dot(ax.c2p(np.log10(m), v), radius=0.06, color=SIM)
                                                                 for m, v in zip(ms, at)])
        c_late = VGroup(polyline(ax, np.log10(ms), late, S.PRIOR, 3), *[Dot(ax.c2p(np.log10(m), v), radius=0.06, color=S.PRIOR)
                                                                         for m, v in zip(ms, late)])
        leg = legend([(SIM, r"outside $\tfrac12 \pm 0.02$ \emph{at} toss $m$"),
                      (S.PRIOR, r"outside it \emph{after} $m$ through toss 20,000")], font_size=22).move_to([3.9, 1.8, 0])
        thm = theorem_card(r"The strong law", r"if $X_i$ are i.i.d.\ with $E|X| < \infty$, \ then $\bar X_n \to \mu$ almost "
                           r"surely", who=r"Borel 1909 (coins); \ Kolmogorov, 1930s (general)", color=S.PRIOR, width=5.6,
                           font_size=22).move_to([3.9, -0.6, 0])
        flag = note(r"proved in Part 43, \ with measure theory").next_to(thm, DOWN, buff=0.2)
        tag = note(r"simulated: 2,000 sequences of 20,000 fair tosses").to_corner(DR, buff=0.3)
        with self.voiceover(
            "For averages, the stronger statement is also true. <bookmark mark='a'/> Toss two thousand coins twenty "
            "thousand times each. In blue, the share of sequences whose running share of heads is outside a half, "
            "plus or minus point oh two, at toss m: the weak law says this goes to zero. <bookmark mark='b'/> In "
            "purple, the share that stray outside after m but before our finite run ends. The corresponding infinite-horizon probability goes to zero by the strong law. That's a much bigger event, but "
            "it goes to zero too: after ten thousand tosses, only one sequence in two thousand leaves the band again "
            "before the run ends. <bookmark mark='c'/> That's the strong law of large numbers: almost every sequence "
            "eventually stays inside any band. Émile Borel proved it for coins in 1909 and Andrey Kolmogorov in "
            "general around 1930; the proof needs the measure theory of Part 43."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c_at), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(c_late), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(thm), FadeIn(flag))
        self.clear_scene()

    def hierarchy(self):
        box = lambda t, c: VGroup(RoundedRectangle(width=3.2, height=0.9, corner_radius=0.15, stroke_color=c, stroke_width=2.5),  # noqa: E731
                                  label(t, font_size=26, color=c))
        AS = box(r"almost surely", S.PRIOR).move_to([-4.2, 1.2, 0])
        L2 = box(r"in mean square", S.LIK).move_to([-4.2, -1.2, 0])
        P = box(r"in probability", SIM).move_to([0, 0, 0])
        D = box(r"in distribution", EXACT).move_to([4.2, 0, 0])
        arr = VGroup(Arrow(AS.get_right(), P.get_left() + UP * 0.2, buff=0.1, color=GREY_B),
                     Arrow(L2.get_right(), P.get_left() + DOWN * 0.2, buff=0.1, color=GREY_B),
                     Arrow(P.get_right(), D.get_left(), buff=0.1, color=GREY_B))
        notes = VGroup(note(r"bounded convergence of indicators"), note(r"Chebyshev, \ as in the weak law"), note(r"the converse fails: \ the mirror"))
        notes[0].next_to(arr[0], UP, buff=0.05).shift(RIGHT * 0.3)
        notes[1].next_to(arr[1].get_center(), DR, buff=0.12)
        notes[2].next_to(D, DOWN, buff=0.25)
        no = label(r"the typewriter: \ in probability, \ not almost surely", font_size=22, color=BOUND).to_edge(DOWN, buff=1.0)
        exc = label(r"one exception: \ in distribution to a \emph{constant} implies in probability", font_size=22,
                    color=GREY_A).to_edge(DOWN, buff=0.5)
        intro = label('How the modes of convergence relate', font_size=36)
        with self.voiceover(
            "Here's how they fit together. <bookmark mark='a'/> Almost sure convergence implies convergence in "
            "probability. <bookmark mark='b'/> So does convergence in mean square, that the expected squared distance "
            "goes to zero, by Chebyshev's argument. <bookmark mark='c'/> And convergence in probability implies "
            "convergence in distribution. <bookmark mark='d'/> None of the arrows reverses: the mirror and the "
            "typewriter give two counterexamples. For convergence in probability without mean-square convergence, take square root n times the indicator that a uniform U is below one over n: the event gets rare but its expected square stays one. With one useful exception: if the limit is a constant, convergence "
            "in distribution does imply convergence in probability, and chapter nine will use that."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(AS), FadeIn(P), GrowArrow(arr[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(L2), GrowArrow(arr[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(D), GrowArrow(arr[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]), FadeIn(no), FadeIn(exc))
        self.clear_scene()
