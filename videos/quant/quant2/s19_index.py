from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, GAIN, LOSS, PART, TRADE, load, ro

C_ = {r"w_i": QC.HOUSE, r"A": CASH, r"\tau": QC.IDEA}


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class Index(VoiceoverScene):
    def construct(self):
        d = load("index_rd")
        self.card()
        self.weights()
        self.pour(d)
        self.evidence()
        self.rd(d)

    def card(self):
        c = chapter_card(15, r"Benchmarks and indices", r"Do demand curves for stocks slope down?", part=PART)
        with self.voiceover("Chapter fifteen. Benchmarks and indices."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def weights(self):
        rows = [
            row(r"w_i", r"=", r"\frac{f_i N_i P_i}{\sum_j f_j N_j P_j}"),
            row(r"I_{\text{price-weighted}}", r"=", r"\frac{\sum_i P_i}{\text{divisor}}"),
            row(r"Q_i", r"=", r"\frac{A\,w_i}{P_i} \ \Rightarrow\ \frac{\Delta Q_i}{f_i N_i} = \frac{A}{\text{index cap}}"),
            row(r"\frac{\Delta P}{P}", r"\approx", r"\frac{1}{\varepsilon}\,\frac{\Delta Q}{N}"),
        ]
        whys = [why(r"cap weights with a float factor $f_i$: only shares that can trade count (S\&P 500, Russell)",
                    font_size=20),
                why(r"the Dow: prices summed; the divisor is reset at splits so the index doesn't jump", font_size=20),
                why(r"passive assets $A$ buy every member in proportion: the same fraction of each one's float",
                    font_size=20),
                why(r"if demand slopes down with elasticity $\varepsilon$, that buying moves the price", font_size=20)]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-1.6, buff=0.45, edge=6.9)
        with self.voiceover(
            "An index is a recipe for a portfolio. Most weight each member by the value of its shares that can trade, the "
            "float. <bookmark mark='a'/> A few old ones, like the Dow, add prices and divide by a divisor, which is reset at "
            "every split so the index doesn't jump. <bookmark mark='b'/> Put passive money behind the recipe: a fund "
            "tracking the index buys the same fraction of every member's float, its assets over the index's value. "
            "<bookmark mark='c'/> Classical finance says that buying shouldn't move prices, because demand for a stock is "
            "flat at its value. If demand slopes down, it does. Which is it?"
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def pour(self, d):
        n = 3000
        caps = 1 / np.arange(1, n + 1) ** 1.1
        logc = np.log10(caps / caps[0])
        g = axes([0, n], [-4.2, 0.2], x_length=11.0, y_length=3.0, xlabel=r"stocks ranked by market value",
                 ylabel=r"market value (log)", xticks=[1, 1000, 2000, 3000], font_size=16).to_edge(UP, buff=0.6)
        ax = g.ax
        bars = VGroup(*[Line(ax.c2p(i, -4.2), ax.c2p(i, logc[i]), stroke_width=1,
                             color=TRADE if i < 1000 else QC.IDEA, stroke_opacity=0.5) for i in range(0, n, 6)])
        gate = DashedLine(ax.c2p(1000, -4.2), ax.c2p(1000, 0.2), color=YELLOW, stroke_width=3)
        gl = label(r"rank 1000: Russell 1000 above, Russell 2000 below", font_size=18, color=YELLOW).next_to(gate, UP, buff=0.05)
        # demand per share of float, if the same passive dollars track each index (illustrative)
        r1, r2 = d["cap_r1000"], d["cap_r2000"]
        dem = np.where(np.arange(n) < 1000, 1 / r1, np.where(np.arange(n) < 3000, 1 / r2, 0))
        dem = dem / dem.max()
        g2 = axes([0, n], [0, 1.1], x_length=11.0, y_length=2.2, xlabel=r"passive buying, as a share of each "
                  r"stock's float", xticks=[1000, 2000], font_size=16).next_to(g, DOWN, buff=0.5)
        k = ValueTracker(0)
        flow = always_redraw(lambda: VGroup(*[Line(g2.ax.c2p(i, 0), g2.ax.c2p(i, dem[i] * min(k.get_value(), 1)),
                                                   stroke_width=2, color=CASH, stroke_opacity=0.7)
                                              for i in range(0, n, 25)]))
        ratio = MathTex(rf"\text{{jump at the gate: }} \times {r1 / r2:.1f}", font_size=30, color=YELLOW)
        ratio.next_to(g2, DOWN, buff=0.25).shift(LEFT * 3)
        src = note(r"illustrative: a Zipf-like distribution of values, and equal passive dollars on each index; the "
                   r"real ratio depends on how much money tracks each", font_size=15).to_edge(DOWN, buff=0.1)
        with self.voiceover(
            "The Russell indices give a sharp test. Rank American stocks by value. The top thousand form the Russell one "
            "thousand; the next two thousand, the Russell two thousand. <bookmark mark='a'/> Pour passive money onto both. "
            "Within each index, every member gets the same fraction of its float bought. But the stock ranked one thousand is "
            "the smallest member of a giant index, and the stock ranked one thousand and one is the largest member of a small "
            "one. If the same dollars tracked each, the buying per share would jump about "
            f"{r1 / r2:.0f}-fold at the gate. <bookmark mark='b'/> Two almost identical companies, one rank apart, get very "
            "different index demand: a natural experiment, and the right tool for it is a regression discontinuity."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[Create(b) for b in bars], lag_ratio=0.002, run_time=3))
            self.play(Create(gate), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(g2), FadeIn(src))
            self.add(flow)
            self.play(k.animate.set_value(1), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(ratio))
        flow.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def evidence(self):
        cards = VGroup(
            definition_card(r"Shleifer (1986)", r"S\&P 500 additions, 1976--83: an announcement return of about "
                            r"+2.8\%, linked to index-fund buying; demand curves slope down", width=4.3,
                            color=QC.IDEA, font_size=19, kind=r"Journal of Finance"),
            definition_card(r"Harris and Gurel (1986)", r"the same period: much of the jump reverses within weeks; "
                            r"price pressure, not news", width=4.3, color=GREY_B, font_size=19, kind=r"Journal of Finance"),
            definition_card(r"Chang, Hong and Liskovich (2015)", r"at the Russell cutoff, stocks that just make the "
                            r"Russell 2000 earn more than those just in the Russell 1000: a regression discontinuity",
                            width=4.3, color=QC.HOUSE, font_size=19, kind=r"Review of Financial Studies"),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).shift(UP * 1.2)
        more = VGroup(
            label(r"Pavlova and Sikorskaya (2023): benchmarking intensity, the share of a stock held by funds tied "
                  r"to its benchmarks, predicts", font_size=19),
            label(r"lower demand elasticities and, after it rises, lower returns", font_size=19),
            label(r"Greenwood and Sammon (2025): the S\&P 500 inclusion effect fell from about 7.4\% in the 1990s to "
                  r"under 1\% in the last decade", font_size=19, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(cards, DOWN, buff=0.5)
        if more.width > 13.2:
            more.scale_to_fit_width(13.2)
        src = note(r"Shleifer's number as quoted in NBER w8654; Greenwood and Sammon, \textit{Journal of Finance} 80(2)",
                   font_size=15).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "The evidence. Shleifer found that stocks added to the S and P five hundred jumped almost three percent on the "
            "announcement, in years when index funds were growing, and argued that demand curves for stocks slope down. Harris "
            "and Gurel found that much of the jump faded within weeks: price pressure, not news. <bookmark mark='a'/> Chang, "
            "Hong and Liskovich used the Russell gate: stocks that just make the Russell two thousand outperform those that "
            "just miss it. <bookmark mark='b'/> The frontier asks how much of the market is tied to benchmarks. Pavlova and "
            "Sikorskaya measure benchmarking intensity and find it lowers demand elasticities. And Greenwood and Sammon show "
            "the famous S and P inclusion effect has nearly disappeared: about seven percent in the 1990s, under one percent "
            "lately, as the market learned to anticipate the changes."
        ) as vo:
            self.play(FadeIn(cards[0]), FadeIn(cards[1]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(cards[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in more], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def rd(self, d):
        cx = np.asarray(d["centers"], float)
        by = np.asarray(d["binned"], float)
        est = np.asarray(d["est"], float)
        bws = d["bw"]
        g = axes([500, 1500], [-0.012, 0.03], x_length=6.4, y_length=3.8, xlabel=r"rank (cutoff at 1000)",
                 ylabel=r"return after reconstitution (binned)", xticks=[500, 1000, 1500], yticks=[0, 0.01, 0.02],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=TRADE if x < 1000 else QC.IDEA) for x, y in zip(cx, by)])
        cut = DashedLine(ax.c2p(1000, -0.012), ax.c2p(1000, 0.03), color=YELLOW)
        b = ValueTracker(400)

        def fits():
            bw = b.get_value()
            lo = (cx > 1000 - bw) & (cx < 1000)
            hi = (cx > 1000) & (cx < 1000 + bw)
            out = VGroup()
            for m, col in ((lo, TRADE), (hi, QC.IDEA)):
                if m.sum() >= 2:
                    c = np.polyfit(cx[m] - 1000, by[m], 1)
                    xs = np.array([cx[m].min(), 1000])
                    out.add(Line(ax.c2p(xs[0], np.polyval(c, xs[0] - 1000)), ax.c2p(xs[1], np.polyval(c, 0)),
                                 color=col, stroke_width=4))
            return out
        fl = always_redraw(fits)
        bwr = ro(r"\text{bandwidth } b =", lambda: b.get_value(), digits=0, font_size=28).next_to(g, UP, buff=0.2)
        g2 = axes([0, 550], [0, 0.03], x_length=4.6, y_length=3.0, xlabel=r"bandwidth (ranks each side)",
                  ylabel=r"estimated jump, 8 seeds", xticks=[50, 200, 500], yticks=[0, 0.015, 0.03],
                  yfmt=lambda v: f"{100 * v:.1f}\\%", font_size=15).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        sb = VGroup(band(g2.ax, bws, est.mean(0) - est.std(0), est.mean(0) + est.std(0), QC.HOUSE, 0.25),
                    curve(g2.ax, bws, est.mean(0), QC.HOUSE))
        truth = DashedLine(g2.ax.c2p(0, d["jump"]), g2.ax.c2p(550, d["jump"]), color=YELLOW, stroke_width=2)
        rows = MathTex(r"\hat\tau = \lim_{x \downarrow c}\mathbb E[y\,|\,x] - \lim_{x \uparrow c}\mathbb E[y\,|\,x]",
                       font_size=30, color=QC.IDEA).next_to(g2, DOWN, buff=0.4)
        q = desk_question(r"Why does joining the Russell 2000 bring more buying than staying in the Russell 1000?",
                          r"weight is relative: the same company is a sliver of the 1000 but among the largest in the "
                          r"2000", width=5.8, font_size=19).to_corner(DR, buff=0.25)
        src = note(r"simulated: 30 reconstitutions of 3,000 stocks, a true jump of 1.5\% at the cutoff, noise rising "
                   r"with rank; local-linear fits on each side", font_size=15).to_edge(DOWN, buff=0.1)
        with self.voiceover(
            "How a regression discontinuity works, on simulated data with a true one and a half percent jump at the cutoff: "
            "fit a line on each side and read the gap at the gate. <bookmark mark='a'/> The one choice is the bandwidth. "
            "Narrow is noisy; wide lets distant stocks in. <bookmark mark='b'/> Over eight seeds the estimate centres on the "
            f"truth, its spread growing from {100 * est.std(0)[-1]:.2f} to {100 * est.std(0)[0]:.2f} points as the bandwidth "
            "shrinks. <bookmark mark='y'/> A question: why does joining the smaller index bring more buying? "
            "<bookmark mark='z'/> Because weight is relative. The smallest member of the Russell 1000 is a sliver of "
            "a big index; the same company is among the largest in the Russell 2000, and the money tracking it must "
            "hold far more. Index rules differ by country, and so does everything else. Next: markets around the "
            "world."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots), Create(cut), FadeIn(src))
            self.add(fl, bwr)
            vo.wait_until("a")
            self.play(b.animate.set_value(60), run_time=3)
            self.play(b.animate.set_value(480), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(g2), FadeIn(sb), Create(truth), Write(rows))
            vo.wait_until("y")
            q.answer.set_opacity(0)
            self.play(FadeIn(q))
            vo.wait_until("z")
            self.play(q.answer.animate.set_opacity(1))
        fl.clear_updaters()
        bwr.clear_updaters()
        self.wait(1.0)
        self.clear_scene()
