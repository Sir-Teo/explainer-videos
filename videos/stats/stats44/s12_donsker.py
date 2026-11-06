from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats44.common import *  # noqa: F403


class Donsker(VoiceoverScene):
    def construct(self):
        self.card()
        self.walks()
        self.theorem()
        self.reflection()
        self.bridge()
        self.df()

    def card(self):
        card = chapter_card(11, r"Donsker's invariance principle", r"Every random walk, \ seen from far away", lit=(1951,), part=PART)
        with self.voiceover("Chapter eleven. Donsker's invariance principle: every random walk, seen from far away."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def walks(self):
        d = load("donsker")
        A = axes([0, 1], [-2.5, 2.5], x_length=7.4, y_length=4.4, xlabel=r"$t$", ylabel=r"$S_{\lfloor nt \rfloor} / \sqrt n$",
                 xticks=[0, 0.5, 1], yticks=[-2, 0, 2], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"10": GREY_B, "100": CHAINC, "1000": MARTC}
        lines = VGroup()
        for k, c in cols.items():
            w = d["walks"][k]
            t, s = np.asarray(w["t"]), np.asarray(w["s"])
            pts = []
            for i in range(len(t) - 1):
                pts += [(t[i], s[i]), (t[i + 1], s[i])]
            m = VMobject(stroke_color=c, stroke_width=2.5 if k != "1000" else 1.8)
            m.set_points_as_corners([ax.c2p(a, np.clip(b, -2.5, 2.5)) for a, b in pts])
            lines.add(m)
        side = fit_rows(VGroup(
            label(r"a $\pm 1$ walk, \ time squeezed by $n$, \ space by $\sqrt n$", font_size=22),
            label(r"grey, \ blue, \ gold: \ $n = 10, \ 100, \ 1{,}000$", font_size=22, color=GREY_A),
            label(r"the steps vanish; \ the wiggles stay the same size", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Take a random walk of n steps of plus or minus one, squeeze its time axis by n and its "
            "space axis by root n. <bookmark mark='b'/> Here it is with ten, a hundred and a thousand steps. <bookmark "
            "mark='c'/> The individual steps disappear, but the wiggles remain of the same size at every scale: the "
            "picture converges to a Brownian path."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.5), FadeIn(side[1]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"W_n(t)", r"=", r"S_{\lfloor nt \rfloor} / (\sigma \sqrt n), \ \ \text{i.i.d.\ steps, mean } 0, \ \text{variance } \sigma^2", font_size=30),
            cmath(r"\text{Donsker}", r":", r"W_n \Rightarrow B \ \text{ in the space of paths on } [0, 1]", font_size=32),
            cmath(r"\text{so}", r":", r"g(W_n) \Rightarrow g(B) \ \text{ for every continuous functional } g", font_size=32),
            cmath(r"\text{proof}", r":", r"\text{Skorokhod: \ embed the walk in one Brownian path at stopping times}", font_size=30),
        ]
        rows[1][-1].set_color(MARTC)
        whys = [why(r"any step law"), why(r"Donsker (1951)"), why(r"continuous mapping"), why(r"Skorokhod embedding")]
        with self.voiceover(
            "<bookmark mark='a'/> Monroe Donsker's theorem makes that exact, for steps of any law with finite variance. "
            "<bookmark mark='b'/> The rescaled walks converge weakly to Brownian motion, as random elements of the space of "
            "paths: a central limit theorem for whole functions, and the reason Brownian motion appears whatever the steps. "
            "<bookmark mark='c'/> By the continuous mapping theorem, every continuous functional of the walk, its maximum, "
            "its time above zero, its integral, converges to the same functional of Brownian motion. <bookmark mark='d'/> One "
            "proof embeds the walk in a single Brownian path, observed at a sequence of stopping times, Skorokhod's "
            "embedding, which makes the walk and the path close almost surely."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def reflection(self):
        d = load("donsker")
        xs = np.asarray(d["xs"])
        A = axes([0, 3], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"$P(\max_{t \le 1} W_n(t) \ge x)$",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        emp = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=CHAINC) for a, b in zip(xs[::2], np.asarray(d["max_emp"])[::2])])
        refl = curve(ax, xs, d["max_refl"], LIMC, 3.5)
        side = fit_rows(VGroup(
            label(r"reflect the path after it first hits $x$:", font_size=22),
            label(r"$P(\max B \ge x) = 2 P(B_1 \ge x)$", font_size=26, color=LIMC),
            label(r"blue: \ 20,000 walks of 1,000 steps", font_size=22, color=CHAINC),
            label(rf"at $x = 1$: \ {d['max_emp'][20]:.3f} \ vs \ {d['max_refl'][20]:.3f}", font_size=22, color=GREY_A),
            label(r"the walk's maximum, \ known from Brownian motion's", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> An example. Reflect a Brownian path in the level x after it first touches it; by symmetry "
            f"the reflected path is just as likely, <bookmark mark='b'/> so the chance that the maximum up to time one "
            f"exceeds x is twice the chance that the endpoint does. <bookmark mark='c'/> By Donsker, the maximum of a long "
            f"random walk obeys the same law. Twenty thousand walks of a thousand steps agree: <bookmark mark='d'/> at x "
            f"equal to one, {say(d['max_emp'][20], 3)} against {say(d['max_refl'][20], 3)}. <bookmark mark='e'/> A hard "
            f"combinatorial question about walks is answered by a one-line symmetry of Brownian motion."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 20,000 walks")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(refl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(emp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def df(self):
        d = load("donsker")
        edges = np.linspace(-4.5, 3, 51)
        mid = (edges[:-1] + edges[1:]) / 2
        A = axes([-4.5, 3], [0, 0.6], x_length=7.4, y_length=4.4, xlabel=r"the Dickey--Fuller $t$ statistic under a unit root",
                 ylabel=r"density", xticks=[-4, -2, 0, 2], yticks=[0, 0.3, 0.6], center=[-2.5, 0.2, 0])
        ax = A.ax
        bars = bars_at(ax, mid, d["df_t_hist"], edges[1] - edges[0], CHAINC, opacity=0.75)
        xs = np.linspace(-4.5, 3, 200)
        nc = curve(ax, xs, stats.norm.pdf(xs), LIMC, 3)
        q = DashedLine(ax.c2p(d["df_t_q05"], 0), ax.c2p(d["df_t_q05"], 0.45), color=MARTC, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"$\rho = 1$: \ $n(\hat\rho - 1) \Rightarrow \dfrac{B_1^2 - 1}{2\int_0^1 B_t^2\, dt}$", font_size=24, color=MARTC),
            label(r"a functional of $B$: \ Donsker + continuous mapping", font_size=22, color=GREY_A),
            label(rf"simulated: \ {100 * d['df_t_frac_neg']:.0f}\% of $t$'s negative; \ 5\% point ${d['df_t_q05']:.2f}$", font_size=22, color=CHAINC),
            label(r"MacKinnon (no constant): \ $-1.94$; \ normal: \ $-1.645$", font_size=22, color=S.ACCENT),
            label(r"Part 38's tables, \ explained", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> And the promise from Part thirty-eight. Under a unit root, the least-squares estimate of "
            f"rho, scaled by n rather than root n, converges to B one squared minus one, over twice the integral of B "
            f"squared. <bookmark mark='b'/> Numerator and denominator are both continuous functionals of the rescaled "
            f"random walk, so Donsker's theorem gives the limit directly. <bookmark mark='c'/> Twenty thousand simulated "
            f"random walks of two hundred and fifty steps: the Dickey–Fuller t statistic is skewed left, negative "
            f"{100 * d['df_t_frac_neg']:.0f} percent of the time, with a five percent point of {say(d['df_t_q05'], 2)}. "
            f"<bookmark mark='d'/> MacKinnon's table gives minus one point nine four; the normal would say minus one point six "
            f"four five. <bookmark mark='e'/> The critical values of Part thirty-eight are quantiles of Brownian functionals."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 20,000 random walks")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars), Create(nc), Create(q), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def bridge(self):
        rows = [
            cmath(r"\sqrt n (F_n(x) - F(x))", r"=", r"\tfrac{1}{\sqrt n} \textstyle\sum_i \big(1(U_i \le u) - u\big), \ \ u = F(x)", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"B^\circ(u) = B(u) - u B(1): \ \text{the Brownian bridge}", font_size=32),
            cmath(r"\sqrt n \sup_x |F_n - F|", r"\Rightarrow", r"\sup_u |B^\circ(u)|", font_size=34),
            cmath(r"P(\sup|B^\circ| > x)", r"=", r"2 \textstyle\sum_{k \ge 1} (-1)^{k-1} e^{-2k^2x^2}: \ \text{Kolmogorov's law}", font_size=30),
        ]
        rows[3][-1].set_color(S.ACCENT)
        whys = [why(r"the empirical process"), why(r"tied down at $u = 1$"), why(r"the KS statistic"), why(r"Part 48 proves it")]
        with self.voiceover(
            "<bookmark mark='a'/> Donsker's theorem has a second form, the one he proved it for. The empirical CDF's error, "
            "scaled by root n, is a normalized sum of centred indicators, a random function of u. <bookmark mark='b'/> It "
            "converges to the Brownian bridge: Brownian motion tied back down to zero at time one. <bookmark mark='c'/> So "
            "the Kolmogorov–Smirnov statistic converges to the maximum of the bridge, <bookmark mark='d'/> whose law, "
            "Kolmogorov's alternating series, gives the KS test of Part sixteen its critical values, the same for every "
            "continuous F. Part forty-eight builds the general theory: empirical processes."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
