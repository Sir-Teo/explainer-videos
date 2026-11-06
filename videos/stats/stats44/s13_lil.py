from __future__ import annotations

import numpy as np

from videos.stats.stats44.common import *  # noqa: F403


class IteratedLogarithm(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.proof()
        self.paths()
        self.meaning()

    def card(self):
        card = chapter_card(12, r"The law of the iterated logarithm", r"How far does a random walk stray?", lit=(1924,), part=PART)
        with self.voiceover("Chapter twelve. The law of the iterated logarithm: exactly how far a random walk strays."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def statement(self):
        rows = [
            cmath(r"\text{CLT}", r":", r"S_n / \sqrt n \Rightarrow N(0, 1): \ \text{at each } n, \ \text{a few } \sqrt n", font_size=32),
            cmath(r"\text{LIL}", r":", r"\limsup_n \frac{S_n}{\sqrt{2 n \log\log n}} = 1 \ \ \text{almost surely}", font_size=34),
            cmath(r"\text{and}", r":", r"\liminf = -1; \ \text{every point of } [-1, 1] \text{ is a limit point}", font_size=32),
            cmath(r"\text{for}", r":", r"\text{i.i.d.\ steps with variance } 1: \ \text{Hartman \& Wintner (1941)}", font_size=30),
        ]
        rows[1][-1].set_color(MARTC)
        whys = [why(r"one time at a time"), why(r"Khinchin (1924), \ coins"), why(r"Strassen (1964)"), why(r"necessary and sufficient")]
        with self.voiceover(
            "<bookmark mark='a'/> The central limit theorem describes S n over root n at one time at a time. But a path is "
            "checked at every time, and at some times it will be unusually far out. <bookmark mark='b'/> Aleksandr "
            "Khinchin's law of the iterated logarithm, for coin tosses in 1924, says exactly how far: the upper limit of S n "
            "over the root of two n log log n is one, almost surely. <bookmark mark='c'/> The lower limit is minus one, and, "
            "as Volker Strassen showed, the path visits every point in between infinitely often. <bookmark mark='d'/> Philip "
            "Hartman and Aurel Wintner extended it in 1941 to any independent identically distributed steps with finite "
            "variance."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def paths(self):
        d = load("lil")
        n = np.log10(np.asarray(d["idx"], float))
        env = np.asarray(d["env"])
        clt = np.asarray(d["clt"])
        A = axes([0.5, 6], [-3, 3], x_length=7.4, y_length=4.4, xlabel=r"$n$", ylabel=r"$S_n / \sqrt n$", xticks=[1, 2, 3, 4, 5, 6],
                 yticks=[-3, -2, -1, 0, 1, 2, 3], log_x=True, xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        scale = np.sqrt(np.asarray(d["idx"], float))
        cols = [CHAINC, MARTC, S.ALT, S.PRIOR, S.KEPT, S.RESID]
        ps = VGroup(*[polyline(ax, n, np.clip(np.asarray(p) / scale, -3, 3), cols[i], 1.6, 0.85) for i, p in enumerate(d["paths"])])
        e_up = polyline(ax, n, env / scale, LIMC, 3)
        e_dn = polyline(ax, n, -env / scale, LIMC, 3)
        c_up = DashedLine(ax.c2p(0.5, 1.645), ax.c2p(6, 1.645), color=GREY_B, stroke_width=2)
        c_dn = DashedLine(ax.c2p(0.5, -1.645), ax.c2p(6, -1.645), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"six walks of a million steps, \ scaled by $\sqrt n$", font_size=22),
            label(r"grey: \ $\pm 1.645$, \ the CLT's 90\% at each $n$", font_size=22, color=GREY_A),
            label(r"gold: \ $\pm\sqrt{2 \log\log n}$, \ the LIL envelope", font_size=22, color=LIMC),
            label(rf"largest ratio to it, \ $n > 1{{,}}000$: \ {min(d['ratios']):.2f} to {max(d['ratios']):.2f}", font_size=22, color=MARTC),
            label(r"the envelope grows, \ but only like $\sqrt{\log\log n}$", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Six random walks of a million steps, divided by root n. <bookmark mark='b'/> At any fixed n, "
            f"the central limit theorem puts ninety percent of walks inside the grey lines. <bookmark mark='c'/> But each path, "
            f"followed over time, keeps escaping them, out to the gold envelope, the root of two log log n, which grows "
            f"without bound. <bookmark mark='d'/> The largest excursion of each path relative to the envelope, after the first "
            f"thousand steps, is between {say(min(d['ratios']), 2)} and {say(max(d['ratios']), 2)}: the theorem's limit of one "
            f"is approached from both sides. <bookmark mark='e'/> Log log n grows so slowly that, for a million steps, the "
            f"envelope is only about two point three standard deviations."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: six walks, $10^6$ steps")))
            vo.wait_until("a")
            self.play(Create(ps), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(c_up), Create(c_dn), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(e_up), Create(e_dn), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def meaning(self):
        rows = fit_rows(VGroup(
            label(r"a confidence interval valid at one $n$ \ is not valid at every $n$ at once", font_size=26),
            label(r"monitoring a fixed-$n$ interval forever: \ it is eventually violated, \ surely", font_size=26, color=BADC),
            label(r"intervals that hold at all $n$ must widen by about $\sqrt{\log\log n}$", font_size=26, color=MARTC),
            label(r"confidence sequences, \ built from Ville's inequality: \ Part 58", font_size=26, color=GOODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The statistical lesson is the one chapter four drew from Ville. An interval valid at one "
            "sample size is not valid at every sample size simultaneously. <bookmark mark='b'/> Watch a fixed-sample interval "
            "forever and, by the iterated logarithm, it will eventually exclude the truth, almost surely. <bookmark "
            "mark='c'/> An interval that holds at all times at once must be wider, by roughly the root of log log n, the "
            "smallest possible price. <bookmark mark='d'/> Such intervals, confidence sequences, are built from Ville's "
            "inequality in Part fifty-eight."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"n_k", r"=", r"\lfloor \theta^k \rfloor, \ \theta > 1: \ \text{check only at geometric times}", font_size=32),
            cmath(r"P\big(\max_{n \le n_{k+1}} S_n \ge c\, h(n_k)\big)", r"\le", r"e^{-c^2 h(n_k)^2 / 2 n_{k+1}} \ \ \text{(L\'evy's maximal inequality)}", font_size=28),
            cmath(r"\phantom{P}", r"=", r"(k \log\theta)^{-c^2/\theta}: \ \text{summable when } c^2 > \theta", font_size=30),
            cmath(r"\text{BC I}", r":", r"\limsup S_n / h(n) \le c, \ \text{then let } c \downarrow 1, \ \theta \downarrow 1", font_size=32),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"the Etemadi trick again"), why(r"$h(n) = \sqrt{2n\log\log n}$"), why(r"the iterated log appears here"), why(r"the upper half")]
        with self.voiceover(
            "<bookmark mark='a'/> The upper half of the proof is the strong law's trick again. Check the walk only at "
            "geometric times, theta to the k. <bookmark mark='b'/> Between two such times, a maximal inequality bounds the "
            "chance of ever exceeding c times the envelope by a Gaussian tail. <bookmark mark='c'/> Because the envelope "
            "contains log log n, that tail is a power of k: k log theta to the minus c squared over theta, which is "
            "summable exactly when c squared exceeds theta. That is where the iterated logarithm comes from. <bookmark "
            "mark='d'/> Borel–Cantelli then bounds the upper limit by c, and letting c and theta shrink to one gives one. "
            "The lower half uses the second Borel–Cantelli lemma on nearly independent blocks."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
