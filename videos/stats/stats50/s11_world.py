from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class HonestIntervals(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.chart()
        self.honest()
        self.board()
        self.hcboard()
        self.lesson()

    def card(self):
        card = chapter_card(10, r"The Board: \ adaptation and honest intervals", r"What a minimax view does to confidence", part=PART)
        with self.voiceover("Chapter ten. The Board: adaptation and honest intervals, or what a minimax view does to confidence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"\hat f_h(x_0) \pm 1.96\, \mathrm{SD}_h", r":", r"\text{ignores the bias}", font_size=34),
            cmath(r"h \text{ MSE-optimal}", r":", r"\text{bias} \asymp \mathrm{SD}: \ \text{the interval is off-centre by a fixed fraction}", font_size=30),
            cmath(r"h \text{ undersmoothed}", r":", r"\text{bias} \ll \mathrm{SD}: \ \text{honest, \ but wider}", font_size=32),
            cmath(r"\text{adaptive}", r":", r"\text{Low (1997): \ not honest and adaptive at once}", font_size=34),
        ]
        rows[1][-1].set_color(LOWC)
        rows[2][-1].set_color(ADAPTC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"Part 29's band"), why(r"the trade-off is balanced"), why(r"Hall (1992); \ Part 37's bias correction"), why(r"the price of adaptation, \ for intervals")]
        with self.voiceover(
            "<bookmark mark='a'/> The usual pointwise interval for a smoother, the estimate plus or minus one point nine six "
            "standard deviations, ignores the bias. <bookmark mark='b'/> At the bandwidth that minimizes mean squared error, "
            "the bias is the same order as the standard deviation, so the interval is off-centre by a fixed fraction of its "
            "width, and cannot cover at the nominal rate. <bookmark mark='c'/> Undersmoothing makes the bias negligible, at "
            "the cost of a wider interval. <bookmark mark='d'/> And Mark Low proved in 1997 that no interval can both keep "
            "its coverage over a range of smoothness classes and shrink at the adaptive rate. Adaptation, which is nearly free "
            "for estimation, is not free for inference."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("board")
        lh = np.log10(d["hs"])
        A = axes([-2.7, -0.7], [-3.6, -0.6], x_length=7.4, y_length=4.4, xlabel=r"bandwidth $h$ \ (log scale)", ylabel=r"$\log_{10}$ MSE at the peak",
                 xticks=[np.log10(0.005), np.log10(0.02), np.log10(0.08)], xfmt=lambda v: f"{10 ** v:.3f}", yticks=[-3.5, -3, -2.5, -2, -1.5, -1], center=[-2.5, 0.2, 0])
        ax = A.ax
        y = np.log10(d["risk_by_h"])
        c = VGroup(polyline(ax, lh, y, UPC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=UPC) for a, b in zip(lh, y)])
        opt = Dot(ax.c2p(np.log10(d["h_opt"]), y[list(d["hs"]).index(d["h_opt"])]), radius=0.13, color=LOWC)
        und = Dot(ax.c2p(np.log10(d["h_under"]), y[list(d["hs"]).index(d["h_under"])]), radius=0.13, color=ADAPTC)
        side = fit_rows(VGroup(
            label(r"a sine plus a sharp peak at $x_0 = 0.5$, \ $n = 2{,}000$", font_size=22),
            label(r"blue: \ MSE of the box estimate by bandwidth", font_size=22, color=UPC),
            label(rf"red: \ the MSE-optimal $h = {d['h_opt']}$", font_size=22, color=LOWC),
            label(rf"green: \ undersmoothed, \ $h = {d['h_under']}$", font_size=22, color=ADAPTC),
            label(r"Lepski picks from the whole grid, \ data-driven", font_size=22, color=HYPC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The test case: a sine wave with a sharp peak added at the point of interest, two thousand "
            f"observations. <bookmark mark='b'/> The mean squared error of the local average at the peak, by bandwidth. "
            f"<bookmark mark='c'/> In red, the bandwidth that minimizes it, {d['h_opt']}. <bookmark mark='d'/> In green, a "
            f"quarter of that. <bookmark mark='e'/> And Lepski's method chooses from the grid on each sample."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(opt), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(und), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def honest(self):
        rows = [
            cmath(r"\text{honest}", r":", r"\inf_{f \in \mathcal F} P_f(f(x_0) \in CI) \ge 0.95: \ \text{uniformly over the class}", font_size=30),
            cmath(r"\text{bias-aware}", r":", r"\hat f_h(x_0) \pm \big(\overline{\text{bias}}_h + 1.96\,\mathrm{SD}_h\big), \ \ \overline{\text{bias}} \text{ from the class}", font_size=30),
            cmath(r"\text{Armstrong \& Kolesár (2018)}", r":", r"\text{widen by the worst bias; \ } h \text{ for length}", font_size=32),
            cmath(r"\text{the catch}", r":", r"\text{you must name the class: \ honesty is relative to an assumption}", font_size=32),
        ]
        rows[1][-1].set_color(ADAPTC)
        rows[3][-1].set_color(LOWC)
        whys = [why(r"Li (1989)'s definition"), why(r"Part 37's RD intervals"), why(r"minimax length"), why(r"no free lunch")]
        with self.voiceover(
            "<bookmark mark='a'/> What should an honest interval promise? Its coverage should hold uniformly over the whole "
            "class of functions, not just for one well-behaved truth. <bookmark mark='b'/> A bias-aware interval achieves "
            "this by widening the usual interval by the largest bias any function in the class could produce at the chosen "
            "bandwidth. <bookmark mark='c'/> Timothy Armstrong and Michal Kolesár showed in 2018 how to choose the bandwidth "
            "to make such intervals as short as possible, and used them for Part thirty-seven's regression discontinuities. "
            "<bookmark mark='d'/> The catch is that the worst bias depends on the class, so you must say how smooth the "
            "function is allowed to be. Low's theorem says the data cannot tell you that, so honesty is always relative to an "
            "assumption."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("pointwise CI")
        d = load("board")
        r = {x["method"]: x for x in d["rows"]}
        vals = [x["achieved"] for x in d["rows"][:3]]
        show_board(self, rows,
                   f"<bookmark mark='a'/> On the Coverage Board, nominal ninety-five percent. The interval at the MSE-optimal "
                   f"bandwidth covers {100 * vals[0]:.1f} percent, a few points short, because of its bias. <bookmark mark='b'/> "
                   f"Undersmoothed, it covers {100 * vals[1]:.1f} percent: honest. <bookmark mark='c'/> At Lepski's data-chosen "
                   f"bandwidth it covers only {100 * vals[2]:.0f} percent. Lepski stops smoothing when the bias becomes "
                   f"detectable, which means the bias is, by design, about as large as the noise: the adaptive interval is "
                   f"dishonest, as Low's theorem says it must be.",
                   [("a", [0]), ("b", [1]), ("c", [2])])

    def hcboard(self):
        rows = board_rows("higher criticism")
        d = load("board")
        hc = [x for x in d["rows"] if "higher" in x["method"]]
        show_board(self, rows,
                   f"<bookmark mark='a'/> And a test. Higher criticism, with the asymptotic critical value the theory suggests, "
                   f"the root of two log log n, about {say(d['asym'], 1)}, rejects pure noise {100 * hc[0]['achieved']:.0f} percent "
                   f"of the time at two thousand statistics: the null distribution converges extremely slowly. <bookmark "
                   f"mark='b'/> With a critical value simulated from the null, {say(d['sim_crit'], 2)}, the size is "
                   f"{100 * hc[1]['achieved']:.1f} percent, as promised.",
                   [("a", [0]), ("b", [1])])

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"what minimax theory says about practice:", font_size=28, color=GREY_A),
            label(r"rates tell you how much data a question needs, \ before you collect it", font_size=26, color=UPC),
            label(r"adaptation is nearly free for estimation, \ and not free for inference", font_size=26, color=HYPC),
            label(r"asymptotic critical values for sup-type statistics can be very slow: \ simulate", font_size=26, color=LOWC),
            label(r"and some problems may be solvable only slowly, \ by any algorithm", font_size=26, color=ADAPTC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What the theory says about practice, now that its main tools are on the table. <bookmark mark='b'/> Rates tell you how much data a "
            "question needs before you collect it: a factor of two in accuracy costs four times the data parametrically, and "
            "much more nonparametrically. <bookmark mark='c'/> Adaptation is nearly free for estimation and not free for "
            "inference. <bookmark mark='d'/> Asymptotic critical values for maxima and suprema can be useless at realistic "
            "sizes; simulate them. <bookmark mark='e'/> And some problems may be solvable only slowly, by any algorithm at "
            "all."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
