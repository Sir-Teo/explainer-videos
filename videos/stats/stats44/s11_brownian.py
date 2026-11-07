from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class Brownian(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.construction()
        self.properties()
        self.exits()
        self.variation()

    def card(self):
        card = chapter_card(10, r"Brownian motion", r"A continuous path made of independent pieces", lit=(1923,), part=PART)
        with self.voiceover("Chapter ten. Brownian motion: a continuous path made of independent pieces."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"B_0 = 0", r";", r"\ B_t - B_s \sim N(0, t - s), \ \ \text{independent of } (B_u)_{u \le s}", font_size=32),
            cmath(r"\text{paths}", r":", r"t \mapsto B_t \text{ continuous}", font_size=34),
            cmath(r"\text{Kolmogorov}", r":", r"\text{the extension theorem gives the laws, \ but cannot see continuity}", font_size=28),
            cmath(r"\text{Wiener (1923)}", r":", r"\text{a measure on continuous paths, \ built directly}", font_size=32),
        ]
        rows[0][-1].set_color(CHAINC)
        whys = [why(r"independent Gaussian increments"), why(r"the extra requirement"), why(r"Part 43's warning"), why(r"Wiener measure")]
        with self.voiceover(
            "<bookmark mark='a'/> Brownian motion starts at zero and has independent Gaussian increments, each with variance "
            "equal to the time elapsed. <bookmark mark='b'/> And its paths are continuous. <bookmark mark='c'/> Kolmogorov's "
            "extension theorem builds a process with the right finite-dimensional laws, but, as Part forty-three warned, its "
            "sigma-algebra cannot even ask whether a path is continuous. <bookmark mark='d'/> Norbert Wiener built the "
            "measure on continuous paths directly in 1923. The simplest construction is Lévy's, refined by Ciesielski."
        ) as vo:
            heading=label('Gaussian increments and continuity define Brownian motion',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def construction(self):
        d = load("bm")
        t = np.asarray(d["t"])
        A = axes([0, 1], [-2.5, 2.5], x_length=7.4, y_length=4.4, xlabel=r"$t$", ylabel=r"$B_t$", xticks=[0, 0.25, 0.5, 0.75, 1],
                 yticks=[-2, -1, 0, 1, 2], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"0": GREY_C, "1": GREY_B, "2": GREY_A, "3": CHAINC, "5": S.ALT, "10": MARTC}
        lines = {k: polyline(ax, t, d["levels"][k], c, 2.5 if k != "10" else 2.0) for k, c in cols.items()}
        side = fit_rows(VGroup(
            label(r"level 0: \ $Z_0\, t$, \ the right value at $t = 1$", font_size=22, color=GREY_B),
            label(r"each level adds tents $Z_{n,k} S_{n,k}(t)$ at midpoints", font_size=22, color=CHAINC),
            label(r"$S_{n,k}$: \ Schauder tents, \ integrated Haar wavelets", font_size=22, color=GREY_A),
            label(r"gold: \ 10 levels, \ 1,024 pieces", font_size=22, color=MARTC),
            label(r"uniform convergence, \ a.s.: \ a continuous limit", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Start with a straight line from zero to a normal value at time one. <bookmark mark='b'/> At "
            "the midpoint, add a tent whose height is an independent normal scaled so that the midpoint has the right "
            "conditional variance; then add tents at the quarter points, the eighths, and so on. <bookmark mark='c'/> The "
            "tents are Schauder functions, the integrals of the Haar wavelets of Part twenty-nine. <bookmark mark='d'/> Here "
            "are levels zero, one, two, three, five and ten. <bookmark mark='e'/> Because the tents at level n are of size "
            "two to the minus n over two, and normal maxima grow only like root log, the series converges uniformly, almost "
            "surely: the limit is continuous, and it is Brownian motion."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: one path, \ ten levels")))
            vo.wait_until("a")
            self.play(Create(lines["0"]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines["1"]), Create(lines["2"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines["3"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(lines["5"]), Create(lines["10"]), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def properties(self):
        rows = [
            cmath(r"\text{scaling}", r":", r"(c^{-1/2} B_{ct})_t \overset{d}{=} (B_t)_t", font_size=34),
            cmath(r"\text{roughness heuristic}", r":", r"\frac{B_{t+h} - B_t}{h} \sim N(0, 1/h) \ \text{explodes as } h \to 0", font_size=30),
            cmath(r"\text{Paley--Wiener--Zygmund}", r":", r"\text{almost surely, \ no } t \text{ at which } B \text{ is differentiable}", font_size=28),
            cmath(r"\text{Markov and martingale}", r":", r"B_t, \ \ B_t^2 - t, \ \ e^{\lambda B_t - \lambda^2 t/2}", font_size=32),
        ]
        rows[1][-1].set_color(BADC)
        rows[3][-1].set_color(MARTC)
        whys = [why(r"self-similar"), why(r"heuristically"), why(r"(1933), \ for all $t$ at once"), why(r"three martingales")]
        with self.voiceover(
            "<bookmark mark='a'/> Brownian motion is self-similar: speed up time by c and shrink space by root c, and"
            " the process is unchanged in law. <bookmark mark='b'/> Its difference quotients over a step h are normal"
            " with variance one over h, which explodes as h shrinks: this suggests roughness at a fixed time, but it "
            "does not by itself prove nowhere differentiability. <bookmark mark='c'/> Paley, Wiener and Zygmund "
            "proved in 1933 that, almost surely, there is no time at all at which it is differentiable: a continuous,"
            " nowhere differentiable function, chosen at random. <bookmark mark='d'/> It is a Markov process, and "
            "three martingales come with it: B itself, B squared minus t, and the exponential martingale, the "
            "continuous-time likelihood ratio."
        ) as vo:
            heading=label('Scaling and martingales describe Brownian paths',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def variation(self):
        d = load("bm")
        q = d["qfine"]
        rows = [[r"pieces", r"$\sum (\Delta B)^2$", r"$\sum |\Delta B|$"]] + [[f"{r['pieces']:,}", f"{r['qv']:.3f}", f"{r['tv']:.1f}"] for r in q]
        tab = table_rows(rows, font_size=26, col_buff=0.9, row_buff=0.18, colors=[GREY_A] + [None] * len(q)).move_to([-2.6, 0.2, 0])
        side = fit_rows(VGroup(
            label(r"cut $[0, 1]$ into $N$ pieces", font_size=24),
            label(r"$\sum (\Delta B)^2 \to t = 1$: \ the quadratic variation", font_size=24, color=MARTC),
            label(r"$\sum |\Delta B| \to \infty$, \ growing like $\sqrt N$", font_size=24, color=BADC),
            label(r"so $(dB)^2 = dt$: \ the rule behind It\^o's calculus", font_size=24, color=S.ACCENT),
            label(r"see \emph{Stochastic Calculus, Visualized}", font_size=20, color=GREY_B),
        ), 4.6, 0.45, [4.45, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> One more property makes Brownian motion unlike any smooth path. Cut the unit "
            "interval into N pieces and add up the squared increments: <bookmark mark='b'/> along deterministic "
            "partitions whose mesh tends to zero the sum converges in probability to one; along nested dyadic "
            "partitions it converges almost surely. The displayed quadratic-variation calculation uses a separate "
            "simulated fine path. That is the quadratic variation. <bookmark mark='c'/> The absolute increments, by "
            "contrast, add up to something growing like root N: the path has infinite length. <bookmark mark='d'/> In"
            " shorthand, dB squared equals dt, the rule from which Itô's stochastic calculus grows, <bookmark "
            "mark='e'/> and the subject of this channel's series Stochastic Calculus, Visualized."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.3), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def exits(self):
        rows = [
            cmath(r"\tau", r"=", r"\text{the first time } B \text{ hits } a > 0 \text{ or } -b < 0", font_size=32),
            cmath(r"E B_\tau = 0", r"\Rightarrow", r"a\, P(\text{hit } a) - b\,(1 - P(\text{hit } a)) = 0: \ \ P = \frac{b}{a + b}", font_size=30),
            cmath(r"E[B_\tau^2 - \tau] = 0", r"\Rightarrow", r"E\tau = E B_\tau^2 = ab", font_size=32),
            cmath(r"\text{the same answers}", r":", r"\text{as chapter 3's gambler, \ with steps of size } 0", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"an exit time"), why(r"optional stopping, \ bounded path"), why(r"the second martingale"), why(r"Donsker, \ in advance")]
        with self.voiceover(
            "<bookmark mark='a'/> The martingales give exit problems at once. Let tau be the first time Brownian "
            "motion leaves the interval from minus b to a. <bookmark mark='b'/> The stopped path is bounded, so "
            "optional stopping applies: the expected exit position is zero, and the chance of leaving at the top is b"
            " over a plus b. <bookmark mark='c'/> For B squared minus t, first stop at tau or n, whichever comes "
            "first. The bounded exit interval bounds the expected stopped time; monotone convergence gives an "
            "integrable exit time, and dominated convergence then gives the expected exit time, a times b. <bookmark "
            "mark='d'/> These are exactly chapter three's gambler's-ruin answers, for a game whose steps have shrunk "
            "to nothing: a preview of the next chapter."
        ) as vo:
            heading=label('Bounded-time stopping first justifies the Brownian exit identities',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
