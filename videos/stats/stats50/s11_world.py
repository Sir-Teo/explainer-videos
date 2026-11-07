from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class HonestIntervals(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.chart()
        self.honest()
        self.bias_aware_example()
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
            cmath(r"h \text{ undersmoothed}", r":", r"\text{bias} \ll \mathrm{SD}: \ \text{can be honest with uniform bias control; wider}", font_size=32),
            cmath(r"\text{adaptive}", r":", r"\text{Low (1997): \ limits over unrestricted nested smoothness classes}", font_size=34),
        ]
        rows[1][-1].set_color(LOWC)
        rows[2][-1].set_color(ADAPTC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"Part 29's band"), why(r"the trade-off is balanced"), why(r"Hall (1992); \ Part 37's bias correction"), why(r"the price of adaptation, \ for intervals")]
        heading = label('Bandwidth bias and data selection affect interval coverage', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The usual pointwise interval for a smoother, the estimate plus or minus one point nine six standard deviations, ignores the bias. <bookmark mark='b'/> At the bandwidth that minimizes mean squared error, the bias is the same order as the standard deviation, so the interval is off-centre by a fixed fraction of its width, and generally undercovers if the limiting standardized bias is nonzero. The conclusion depends on the actual bias, not just the bandwidth label. <bookmark mark='c'/> An undersmoothing sequence can make bias negligible when its bandwidth shrinks sufficiently faster than the MSE-optimal one while the effective sample size diverges. A fixed division by four need not do that asymptotically. <bookmark mark='d'/> And Mark Low proved in 1997 that over suitable unrestricted nested smoothness classes, uniformly honest intervals generally cannot also attain the smoother-class adaptive lengths. Extra separation or self-similarity assumptions can change that conclusion. Adaptation, which is nearly free for estimation, is not free for inference."
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
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact Gaussian fixed-design MSE")))
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
            cmath(r"\text{Armstrong \& Kolesár (2018)}", r":", r"\text{sharp bias-aware critical values; additive radius is conservative}", font_size=32),
            cmath(r"\text{the catch}", r":", r"\text{you must name the class: \ honesty is relative to an assumption}", font_size=32),
        ]
        rows[1][-1].set_color(ADAPTC)
        rows[3][-1].set_color(LOWC)
        whys = [why(r"Li (1989)'s definition"), why(r"Part 37's RD intervals"), why(r"a simple valid construction; not the sharp length formula"), why(r"no free lunch")]
        heading = label('Honesty means coverage uniformly over a stated function class', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> What should an honest interval promise? Its coverage should hold uniformly over the whole class of functions, not just for one well-behaved truth. <bookmark mark='b'/> A bias-aware interval achieves this by widening the usual interval by the largest bias any function in the class could produce at the chosen bandwidth. <bookmark mark='c'/> Timothy Armstrong and Michal Kolesár showed in 2018 how to choose the bandwidth to optimize honest interval length using an appropriate bias-aware critical value. The simple additive worst-bias radius displayed here is valid but generally conservative, and used them for Part thirty-seven's regression discontinuities. <bookmark mark='d'/> The catch is that the worst bias depends on the class, so you must say how smooth the function is allowed to be. Low's theorem limits adaptation over unrestricted classes; additional structural assumptions can permit it, so honesty is always relative to an assumption."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bias_aware_example(self):
        d = load("board")
        rows = [
            cmath(r"Y_i=f(x_i)+Z_i", r",", r"Z_i\overset{\mathrm{iid}}\sim N(0,1):\ \text{fixed design, known noise}", font_size=30),
            cmath(r"|f'(x)|\le L_1,\ |f''(x)|\le L_2", r":", rf"L_1={d['derivative_bounds']['L1']:.2f},\ L_2={d['derivative_bounds']['L2']:.2f}", font_size=30),
            cmath(r"B_h", r"=", r"L_1|\overline{x-x_0}|+\tfrac12L_2\overline{(x-x_0)^2}:\ \text{Taylor bias bound}", font_size=30),
            cmath(r"\overline Y_h\pm(B_h+1.96/\sqrt{k_h})", r":", rf"h={d['h_bias_aware']},\ B_h={d['bias_bound']:.3f},\ \text{{radius}}={d['bias_aware_radius']:.3f}", font_size=28),
        ]
        whys = [why(r"finite Gaussian noise law"), why(r"a stated class containing the peak"), why(r"actual window design moments"), why(r"at least 95\% coverage for fixed bandwidth")]
        heading = label('A derivative bound gives a constructive uniform Gaussian interval', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A constructive comparison: fixed design and independent Gaussian errors with known variance one. "
            "<bookmark mark='b'/> State bounds on the first and second derivatives that contain our example. "
            "<bookmark mark='c'/> Taylor's theorem bounds the local-average bias using the actual window's first two design moments. "
            "<bookmark mark='d'/> Add that worst-case bias to a two-sided Gaussian radius, and choose the bandwidth deterministically "
            "to minimize this conservative radius. This gives at least ninety-five percent coverage uniformly over the stated class. "
            "An outcome-selected bandwidth would need an additional selection or simultaneous-coverage argument."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, mark in enumerate("abcd"):
                vo.wait_until(mark)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        rows = board_rows("pointwise CI")
        d = load("board")
        vals = [x["achieved"] for x in d["rows"][:4]]
        show_board(self, rows,
            f"<bookmark mark='a'/> At the MSE-optimal bandwidth the nominal ninety-five percent interval covers {100*vals[0]:.1f} percent. "
            f"<bookmark mark='b'/> At a quarter of that bandwidth it covers {100*vals[1]:.1f} percent in this example; one function does not prove honesty. "
            f"<bookmark mark='c'/> At Lepski's selected bandwidth it covers {100*vals[2]:.1f} percent, because bias and selection are ignored. "
            f"<bookmark mark='d'/> The fixed-bandwidth bias-aware interval covers {100*vals[3]:.1f} percent here. Its class-wide guarantee "
            f"comes from the derivative bound and Gaussian noise calculation, separately from this simulation. Monte Carlo errors are recorded on the Board.",
            [("a", [0]), ("b", [1]), ("c", [2]), ("d", [3])])

    def hcboard(self):
        rows = board_rows("higher criticism")
        d = load("board")
        hc = [x for x in d["rows"] if "higher" in x["method"]]
        show_board(self, rows,
                   f"<bookmark mark='a'/> And a test. Higher criticism, using only the leading null scale, rather than a calibrated five-percent critical value, the root of two log log n, about {say(d['asym'], 1)}, rejects pure noise {100 * hc[0]['achieved']:.0f} percent of the time at two thousand statistics: the leading scale alone has no five-percent level guarantee. Both the omitted level-specific correction and finite-sample behaviour matter. <bookmark mark='b'/> With a critical value simulated from the null, {say(d['sim_crit'], 2)}, the size is {100 * hc[1]['achieved']:.1f} percent in the independent evaluation simulation, with uncertainty from the evaluation and the separate calibration sample.",
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
