from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class CLTProof(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.expand()
        self.seen()
        self.assumed()
        self.names()

    def card(self):
        card = chapter_card(5, r"The central limit theorem, proved", r"Three lines of Taylor expansion", part=PART)
        with self.voiceover("Chapter five. The central limit theorem, proved."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_(self):
        rows = [
            cmath(r"Z_n", r"=", r"\frac{S_n - n\mu}{\sigma\sqrt n}", r"=", r"\frac{1}{\sqrt n}\sum_{i=1}^n Y_i,\quad Y_i = \frac{X_i - \mu}{\sigma}",
                  font_size=32),
            cmath(r"M_{Z_n}(t)", r"=", r"E\, e^{t Z_n}", r"=", r"\prod_{i=1}^n E\, e^{(t/\sqrt n) Y_i}", r"=", r"M_Y(t/\sqrt n)^n",
                  font_size=32),
            cmath(r"\log M_{Z_n}(t)", r"=", r"n \log M_Y(t/\sqrt n)", font_size=34),
        ]
        rows[1][6].set_color(SIM)
        rows[2][2].set_color(SIM)
        whys = [why(r"standardize each term: \ $E Y = 0$, \ $E Y^2 = 1$"), why(r"independence: \ the expectation of a product "
                                                                              r"factors (Part 3)"),
                why(r"so we need $\log M_Y$ near $0$")]
        with self.voiceover(
            "Here is the theorem: for independent, identically distributed variables with a finite variance, the "
            "standardized sum converges in distribution to the standard normal. We'll prove it assuming a little "
            "more, that the moment generating function exists near zero. <bookmark mark='a'/> Standardize each term "
            "first: Y has mean zero and variance one, and Z n is the sum of the Y's divided by root n. "
            "<bookmark mark='b'/> The moment generating function of Z n is the expectation of e to the t Z n. "
            "Because the terms are independent, the expectation of the product is the product of the expectations: "
            "the MGF of Y at t over root n, raised to the n-th power. <bookmark mark='c'/> Take logarithms. Everything "
            "now depends on the log-MGF of Y at a point that's approaching zero."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.6, buff=0.8, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def expand(self):
        rows = [
            cmath(r"\log M_Y(u)", r"=", r"\kappa_1 u + \kappa_2 \frac{u^2}{2} + \kappa_3 \frac{u^3}{6} + \cdots", r"=",
                  r"\frac{u^2}{2} + \kappa_3 \frac{u^3}{6} + O(u^4)", font_size=30),
            cmath(r"n \log M_Y(t/\sqrt n)", r"=", r"n\Big(\frac{t^2}{2n} + \kappa_3\frac{t^3}{6 n^{3/2}} + O(n^{-2})\Big)", font_size=30),
            cmath(r"n \log M_Y(t/\sqrt n)", r"=", r"\frac{t^2}{2} + \frac{\kappa_3 t^3}{6\sqrt n} + O(1/n)", r"\ \to\ ", r"\frac{t^2}{2}",
                  font_size=32),
            cmath(r"M_{Z_n}(t)", r"\to", r"e^{t^2/2}", r"\ =\ M_{N(0,1)}(t)", font_size=34),
        ]
        rows[2][4].set_color(EXACT)
        rows[3][2].set_color(EXACT)
        whys = [why(r"the cumulant series (Part 3): \ $\kappa_1 = 0$, \ $\kappa_2 = 1$"), why(r"put $u = t/\sqrt n$"),
                why(r"the skewness term is the last to vanish: \ $1/\sqrt n$"),
                why(r"and MGFs that converge near $0$ determine the limit law (Curtiss 1942)")]
        with self.voiceover(
            "<bookmark mark='a'/> Expand the log-MGF in its cumulant series, from Part 3. The first cumulant, the "
            "mean, is zero; the second, the variance, is one. So it starts u squared over two, then the third "
            "cumulant times u cubed over six, and so on. <bookmark mark='b'/> Put u equal to t over root n and "
            "multiply by n. <bookmark mark='c'/> The n cancels against the u squared, leaving t squared over two. "
            "The next term, from the skewness, shrinks like one over root n; the rest faster. "
            "<bookmark mark='d'/> So the MGF of Z n converges to e to the t squared over two, the MGF of the standard "
            "normal. Finally, a theorem of John Curtiss from 1942: if MGFs converge on an interval around zero, the "
            "distributions converge. And that's the proof. Notice that the error term, kappa three over six root n, "
            "is the same skewness we saw dying in chapter four."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-1.0, buff=0.62, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k, transform=False)
        self.clear_scene()

    def seen(self):
        d = load("mgf")
        t = np.asarray(d["t"])
        cols = {"1": GREY_C, "2": S.PRIOR, "5": S.LIK, "20": SIM, "100": S.POST}
        panels = VGroup()
        for k, (key, title) in enumerate((("exp", r"centred exponential"), ("lop", r"the lopsided law"))):
            A = axes([-2.5, 2.5], [-0.5, 4.0], x_length=5.4, y_length=4.0, xlabel=r"$t$", xticks=[-2, -1, 0, 1, 2],
                     yticks=[0, 1, 2, 3], center=[-3.4 + 6.6 * k, -0.6, 0])
            ax = A.ax
            tgt = curve(ax, t, np.asarray(d["target"]), EXACT, 4)
            cvs = VGroup()
            for n, c in cols.items():
                y = np.asarray(d[key][n], float)
                ok = np.isfinite(y) & (y < 4.0) & (y > -0.5)
                if ok.sum() > 2:
                    cvs.add(polyline(ax, t[ok], y[ok], c, 2.5))
            ttl = label(title, font_size=26).next_to(A, UP, buff=0.1)
            panels.add(VGroup(A, ttl, cvs, tgt))
        leg = legend([(c, rf"$n = {n}$") for n, c in cols.items()] + [(EXACT, r"$t^2/2$")], font_size=20)
        leg.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        lab = MathTex(r"n \log M_Y(t/\sqrt n)", font_size=30).to_edge(UP, buff=0.35)
        note_ = label(r"for the exponential, $M_Y(u)$ is infinite for $u \ge 1$: \ at $n = 1$ the curve stops at $t = 1$", font_size=20,
                      color=GREY_B).next_to(lab, DOWN, buff=0.12)
        with self.voiceover(
            "Here's the convergence itself. <bookmark mark='a'/> On the left, a centred exponential; on the right, "
            "our lopsided law. Each coloured curve is n times the log-MGF at t over root n, for n equal to one, two, "
            "five, twenty and a hundred. <bookmark mark='b'/> They close in on the gold parabola, t squared over two. "
            "The exponential's skewness is two, so it approaches from above on the right and below on the left, "
            "and it gets there slowly. <bookmark mark='c'/> Its MGF is infinite beyond one, so for a single term the "
            "curve simply stops: a reminder that this proof leans on an assumption we'll want to drop."
        ) as vo:
            self.play(FadeIn(lab), *[FadeIn(p[:2]) for p in panels])
            vo.wait_until("a")
            self.play(*[LaggedStart(*[Create(c) for c in p[2]], lag_ratio=0.3) for p in panels], FadeIn(leg[:-1]), run_time=3)
            vo.wait_until("b")
            self.play(*[Create(p[3]) for p in panels], FadeIn(leg[-1]))
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.clear_scene()

    def assumed(self):
        thm = theorem_card(r"Lindeberg--L\'evy central limit theorem", r"$X_i$ i.i.d.\ with mean $\mu$ and variance $\sigma^2 < \infty$: "
                           r"\ $\dfrac{S_n - n\mu}{\sigma\sqrt n} \xrightarrow{d} N(0, 1)$", who=r"no MGF needed", color=EXACT,
                           width=8.4, font_size=26).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"our proof assumed an MGF near $0$: \ the lognormal and Student's $t$ have none", font_size=24, color=BOUND),
            label(r"the repair: \ characteristic functions $E e^{itX}$ (Part 3) always exist; \ the same three lines work", font_size=24),
            label(r"terms not identically distributed: \ Lyapunov (1901), \ Lindeberg's condition (1922)", font_size=24),
            label(r"no single term may dominate: \ Feller (1935) showed Lindeberg's condition is then necessary", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(thm, DOWN, buff=0.5)
        for r in rows:
            if r.width > 12.6:
                r.width = 12.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(thm, DOWN, buff=0.5)  # re-align after clamping
        flag = note(r"proved in full in Part 43").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> The full theorem needs only a finite variance. <bookmark mark='b'/> Our proof "
            "assumed more: an MGF near zero. The lognormal's MGF is infinite for every positive t, and so is Student's t's, so the "
            "proof as given doesn't cover them, though the theorem does. <bookmark mark='c'/> The repair is to "
            "replace e to the t X by e to the i t X: the characteristic function of Part 3, which always exists, "
            "since its size is one. The same three lines of expansion go through. <bookmark mark='d'/> Nor do the "
            "terms need to be identically distributed. Aleksandr Lyapunov proved a version in 1901, and Jarl "
            "Lindeberg found the right condition in 1922: roughly, that no single term contributes a noticeable "
            "share of the variance. <bookmark mark='e'/> William Feller showed in 1935 that, when no term dominates, "
            "Lindeberg's condition is also necessary. Part 43 proves all of it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=DOWN * 0.2), FadeIn(flag))
            for k, m in enumerate("bcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def names(self):
        hc = history_card(1920, r"George P\'olya, \ ``\"Uber den zentralen Grenzwertsatz''", r"the theorem is \emph{central}: "
                          r"\ of central importance to probability, \ which is how it got its name", color=S.MUSEUM, width=7.6,
                          font_size=24).move_to([0, 1.2, 0])
        rows = VGroup(label(r"de Moivre (1733): \ coin tosses", font_size=26, color=GREY_A),
                      label(r"Laplace (1810): \ sums of almost anything", font_size=26, color=GREY_A),
                      label(r"Lyapunov (1901), \ Lindeberg (1922), \ L\'evy, \ Feller: \ the conditions", font_size=26, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(hc, DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> The name comes from George Pólya, who in 1920 called it the central limit theorem "
            "of probability: central as in of central importance. <bookmark mark='b'/> It had taken almost two "
            "centuries, from de Moivre's coins, through Laplace, to Lyapunov, Lindeberg, Lévy and Feller, who "
            "pinned down exactly when it holds. Every confidence interval and every test in the next fifteen parts leans "
            "on it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.4))
        self.clear_scene()
