from __future__ import annotations

import numpy as np

from videos.stats.stats5.common import *  # noqa: F403

RED, BLUE = "#F26D6D", "#5DADEC"


def urn_mob(r, b, center, w=1.6, h=2.0) -> VGroup:
    body = RoundedRectangle(width=w, height=h, corner_radius=0.3, stroke_color=GREY_B, stroke_width=2.5).move_to(center)
    n = r + b
    cols = 5
    balls = VGroup(*[Dot(radius=0.09, color=RED if i < r else BLUE) for i in range(n)])
    rows = int(np.ceil(n / cols))
    balls.arrange_in_grid(rows, min(cols, n), buff=0.06)
    if balls.height > h - 0.3:
        balls.height = h - 0.3
    balls.move_to(body.get_bottom() + UP * (balls.height / 2 + 0.15))
    return VGroup(body, balls)


class Exchange(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.limits()
        self.exchangeable()
        self.definetti()
        self.finite()

    def card(self):
        card = chapter_card(12, r"Exchangeability", r"P\'olya's urn, \ and why de Finetti needed it", lit=(1931,), part=PART)
        with self.voiceover("Chapter twelve. Exchangeability."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def machine(self):
        g = np.random.Generator(np.random.PCG64(11))
        r, b = 1, 1
        u = urn_mob(r, b, [-4.6, -0.2, 0])
        rule = VGroup(label(r"draw a ball at random;", font_size=26), label(r"put it back \emph{with another of its colour}", font_size=26,
                                                                            color=S.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rule.to_edge(UP, buff=0.5).shift(LEFT * 2.0)
        A = axes([0, 30], [0, 1], x_length=6.0, y_length=3.4, xlabel=r"draws", ylabel=r"share red", xticks=[0, 10, 20, 30],
                 yticks=[0, 0.5, 1], center=[2.6, -0.6, 0])
        ax = A.ax
        seq = []
        hc = note(r"G. P\'olya \& F. Eggenberger (1923): \ contagion").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here's the second build: Pólya's urn, a model of contagion that George Pólya and Florian Eggenberger "
            "studied in 1923. <bookmark mark='a'/> Start with one red ball and one blue. Draw one at random, look "
            "at it, and put it back together with another of the same colour. <bookmark mark='b'/> Each draw makes "
            "its own colour more likely next time: the rich get richer. Watch thirty draws, and the share of red."
        ) as vo:
            self.play(FadeIn(u), FadeIn(rule[0]), FadeIn(rule[1]), FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(A))
            prev = ax.c2p(0, 0.5)
            for t in range(30):
                red = g.random() < r / (r + b)
                if red:
                    r += 1
                else:
                    b += 1
                seq.append(red)
                nu = urn_mob(r, b, [-4.6, -0.2, 0])
                pt = ax.c2p(t + 1, r / (r + b))
                seg = Line(prev, pt, color=S.ACCENT, stroke_width=3)
                prev = pt
                self.play(Transform(u, nu), Create(seg), run_time=0.35 if t > 4 else 0.7)
        self.clear_scene()

    def limits(self):
        d = load("polya")
        runs = np.asarray(d["runs"])
        lim = np.asarray(d["limits"])
        A = axes([0, 1000], [0, 1], x_length=6.0, y_length=4.0, xlabel=r"draws", ylabel=r"share red", xticks=[0, 500, 1000],
                 yticks=[0, 0.5, 1], center=[-3.2, -0.4, 0])
        ax = A.ax
        xs = np.arange(runs.shape[1]) * 5 + 1
        cols = [interpolate_color(ManimColor(BLUE), ManimColor(RED), k / len(runs)) for k in range(len(runs))]
        paths = VGroup(*[curve(ax, xs, r_, c, 1.6) for r_, c in zip(runs[np.argsort(runs[:, -1])], cols)])
        B = axes([0, 1], [0, 1.6], x_length=4.4, y_length=3.0, xlabel=r"limiting share", xticks=[0, 0.5, 1], yticks=[0, 1],
                 center=[3.6, -0.4, 0])
        ed = np.linspace(0, 1, 21)
        hb = hist_bars(B.ax, ed, np.histogram(lim, ed)[0] / (len(lim) * np.diff(ed)), color=S.ACCENT)
        flat = DashedLine(B.ax.c2p(0, 1), B.ax.c2p(1, 1), color=EXACT, stroke_width=2.5)
        fl = label(r"uniform $=$ beta$(1, 1)$", font_size=22, color=EXACT).next_to(B, UP, buff=0.15)
        tag = note(r"simulated: 30 urns of 1,000 draws; \ 4,000 urns of 500").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Run thirty urns for a thousand draws each. <bookmark mark='a'/> Each share wanders early, then freezes: "
            "after a few hundred draws, one more ball hardly changes it. But different urns freeze at different "
            "values, anywhere from nearly zero to nearly one. <bookmark mark='b'/> Collect the final shares of four "
            "thousand urns. They're spread evenly across the interval: the limit of Pólya's urn, starting from one "
            "ball of each colour, is uniformly distributed, a beta of one and one. Start with a red and b blue and "
            "the limit is a beta of a and b."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.05), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(hb), Create(flat), FadeIn(fl))
        self.clear_scene()

    def exchangeable(self):
        d = load("polya")
        rows = VGroup(*[MathTex(rf"P({s[0]}, {s[1]}, {s[2]}) = " + (r"\tfrac12 \cdot \tfrac23 \cdot \tfrac14" if s == "RRB" else
                                                                     r"\tfrac12 \cdot \tfrac13 \cdot \tfrac24" if s == "RBR" else
                                                                     r"\tfrac12 \cdot \tfrac13 \cdot \tfrac24") + rf" = {v.replace('/', '/')}",
                                font_size=30) for s, v in d["perms"].items()])
        rows = VGroup(MathTex(r"P(\text{R, R, B}) = \tfrac12 \cdot \tfrac23 \cdot \tfrac14 = \tfrac1{12}", font_size=32),
                      MathTex(r"P(\text{R, B, R}) = \tfrac12 \cdot \tfrac13 \cdot \tfrac24 = \tfrac1{12}", font_size=32),
                      MathTex(r"P(\text{B, R, R}) = \tfrac12 \cdot \tfrac13 \cdot \tfrac24 = \tfrac1{12}", font_size=32))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.4, 0])
        eng = note(r"checked exactly with Fractions in \texttt{compute.py}").next_to(rows, DOWN, buff=0.2)
        dfn = definition_card(r"Exchangeable", r"$P(X_1, \dots, X_n)$ is unchanged by any reordering: \ the order carries no "
                              r"information; \ not independent: \ an early red makes a later red likelier", color=S.ACCENT,
                              width=8.4, font_size=24).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The draws are clearly not independent: each one changes the urn. Yet they have a beautiful symmetry. "
            "<bookmark mark='a'/> The chance of red, red, blue is a half times two thirds times a quarter: one "
            "twelfth. <bookmark mark='b'/> Red, blue, red: a half times a third times two quarters: also a twelfth. "
            "And blue, red, red: the same. <bookmark mark='c'/> Only the number of reds matters, not their order. "
            "Sequences like this are called exchangeable: any reordering has the same probability. Exchangeable is "
            "weaker than independent, and it's exactly the right assumption for a lot of real data."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:]), FadeIn(eng))
            vo.wait_until("c")
            self.play(FadeIn(dfn, shift=UP * 0.2))
        self.clear_scene()

    def definetti(self):
        th = theorem_card(r"de Finetti's theorem (1931)", r"an infinite exchangeable sequence of $0$s and $1$s is a mixture of "
                          r"independent ones: \ there is a random $p$ such that, given $p$, the $X_i$ are independent Bernoulli$(p)$",
                          who=r"proved in Part 44", color=S.PRIOR, width=9.6, font_size=24).move_to([0, 1.4, 0])
        f = MathTex(r"P(X_1 = x_1, \dots, X_n = x_n)", r"=", r"\int_0^1 p^{\sum x_i}(1 - p)^{n - \sum x_i}\, \pi(dp)", font_size=34)
        f.next_to(th, DOWN, buff=0.5)
        f[2].set_color(S.PRIOR)
        polya = label(r"P\'olya's urn: \ $p$ is the urn's limiting share, \ and $\pi$ is beta$(1, 1)$", font_size=26, color=S.ACCENT)
        polya.next_to(f, DOWN, buff=0.4)
        why_ = label(r"believing only that order doesn't matter \ $\Rightarrow$ \ acting as if there is an unknown $p$ with a prior: "
                     r"\ Part 15", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        if why_.width > 13:
            why_.width = 13
        with self.voiceover(
            "And exchangeability has a stunning consequence. <bookmark mark='a'/> Bruno de Finetti proved in 1931 that "
            "any infinite exchangeable sequence of zeros and ones behaves as if there were an unknown probability p, "
            "drawn once from some distribution, with the observations independent given p. <bookmark mark='b'/> In "
            "symbols, the probability of any sequence is an average of independent Bernoulli probabilities over a "
            "distribution for p. <bookmark mark='c'/> For Pólya's urn, p is the urn's limiting share, and its "
            "distribution is uniform. <bookmark mark='d'/> De Finetti, a subjectivist, read this as a justification "
            "for Bayesian statistics: if you believe only that the order of the data doesn't matter, you must act as "
            "though there's an unknown parameter with a prior distribution. Part 15 begins there; Part 44 proves "
            "the theorem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Write(f))
            vo.wait_until("c")
            self.play(FadeIn(polya))
            vo.wait_until("d")
            self.play(FadeIn(why_))
        self.clear_scene()

    def finite(self):
        e = load("extras")["finite"]
        rows = VGroup(
            label(r"an urn of 2 red and 2 blue, \ drawn \emph{without} replacement:", font_size=26),
            MathTex(rf"P(\text{{R, R}}) = {e['p_rr']}\ \ne\ P(\text{{R}})^2 = {e['p_r2']}", r",\qquad \operatorname{corr} = "
                    rf"{e['corr']:.2f}", font_size=30),
            label(r"exchangeable, \ but \emph{negatively} correlated: \ no mixture of i.i.d.\ sequences can do that", font_size=24,
                  color=S.RESID),
            VGroup(label(r"de Finetti needs an \emph{infinite} sequence;", font_size=24, color=GREY_A),
                   label(r"for $n$ draws from an exchangeable sequence of length $N$, \ the error is at most about $n^2/N$ \ "
                         r"(Diaconis \& Freedman 1980)", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 0.4, 0])
        for r in rows:
            if r.width > 12.8:
                r.width = 12.8
        with self.voiceover(
            "There's a fine print to de Finetti's theorem. <bookmark mark='a'/> Draw without replacement from an urn "
            "of two red and two blue balls. The sequence is exchangeable, since every order of the colours is "
            "equally likely, <bookmark mark='b'/> but the draws are negatively correlated: a red first makes red "
            "less likely second. <bookmark mark='c'/> No mixture of independent sequences can produce negative "
            "correlation, so the theorem fails here. <bookmark mark='d'/> It needs the sequence to go on forever, "
            "or at least to be much longer than the part we see: Persi Diaconis and David Freedman showed in 1980 "
            "that the error is at most about n squared over N for n draws from an exchangeable sequence of length N."
        ) as vo:
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
