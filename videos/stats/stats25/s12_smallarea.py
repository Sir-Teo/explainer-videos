from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class SmallArea(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.model()
        self.errors()
        self.table()
        self.practice()

    def card(self):
        card = chapter_card(11, r"Small areas", r"A survey too thin for every town", lit=(1979,), part=PART)
        with self.voiceover("Chapter eleven. Small-area estimation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        d = load("smallarea")
        n_t = np.asarray(d["n_t"])
        ok = np.asarray(d["ok"], bool)
        rows = fit_rows(VGroup(
            label(r"a survey of 2,000 of the World's adults: \ mean income in each of 200 towns?", font_size=24),
            label(rf"eligible towns ($n_t\ge2$): \ median respondents {np.median(n_t[ok]):.0f}; \ {int(np.sum(n_t == 0))} towns with none, \ "
                  rf"{int(np.sum(n_t == 1))} with one", font_size=24, color=RES),
            label(rf"direct estimates range from {np.nanmin(np.asarray(d['direct'], float)):.0f} to "
                  rf"{np.nanmax(np.asarray(d['direct'], float)):.0f} thousand", font_size=24, color=RAW),
            label(rf"the true town means: \ {np.min(d['truth']):.0f} to {np.max(d['truth']):.0f} thousand", font_size=24, color=TRUE),
            label(r"Fay \& Herriot (1979): \ per-capita income for 39,000 US places, \ for revenue sharing", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A national survey is designed for national answers, but governments want local ones. A "
            "survey of two thousand of the World's adults asks their income; what is the mean income of each of its two "
            "hundred towns? <bookmark mark='b'/> The typical town has four respondents, eighteen have none, twenty-four have "
            "one. <bookmark mark='c'/> The direct estimates, each town's sample mean, range from eleven thousand to a hundred "
            "and thirty-three thousand, <bookmark mark='d'/> while the true town means lie between forty-six and sixty-one. "
            "<bookmark mark='e'/> Robert Fay and Roger Herriot faced exactly this in 1979, estimating income for tens of "
            "thousands of small American places, where federal revenue sharing depended on the answer."
        ) as vo:
            self.add(simulated_tag())
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"\bar y_t", r"=", r"\theta_t + e_t, \ \ e_t \sim N(0, D_t), \ D_t = \hat\sigma^2/n_t", font_size=28),
            cmath(r"\theta_t", r"=", r"x_t^\top\beta + v_t, \ \ v_t \sim N(0, A)", font_size=30),
            cmath(r"\tilde\theta_t", r"=", r"\gamma_t\,\bar y_t + (1 - \gamma_t)\,x_t^\top\hat\beta, \ \ \gamma_t = \tfrac{A}{A + D_t}", font_size=28),
            cmath(r"\mathrm{MSE}(\tilde\theta_t)", r"\approx", r"\gamma_t D_t + \text{terms for } \hat\beta, \ \hat A", font_size=28),
        ]
        rows[2][2].set_color(SHRUNK)
        whys = [why(r"working Gaussian model; \ pooled variance estimated"), why(r"the linking model: \ the town's region"),
                why(r"the EBLUP: \ direct and synthetic, \ weighted"), why(r"Prasad \& Rao (1990)")]
        intro = label('A working probability model states the assumptions behind shrinkage', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Fay and Herriot's model works with the town means themselves. Each direct estimate "
            "is the truth plus sampling error with a variance we can estimate, smaller for towns with more "
            "respondents. <bookmark mark='b'/> The true means follow a regression on what is known about every town, "
            "here its region, plus a town effect with variance A. <bookmark mark='c'/> The result is James–Stein once"
            " more: each town's estimate is a weighted average of its own direct estimate and the regression's "
            "synthetic prediction, with weight gamma, A over A plus the town's sampling variance. <bookmark "
            "mark='d'/> N. G. N. Prasad and J. N. K. Rao derived an approximate MSE including estimation of beta and "
            "A, treating the sampling variances as known. Here those variances are estimated from pooled incomes, "
            "requiring further allowance; normality is also a working approximation for towns with only two "
            "respondents."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def errors(self):
        d = load("smallarea")
        n_t = np.asarray(d["n_t"], float)
        ok = np.asarray(d["ok"], bool)
        tr = np.asarray(d["truth"], float)
        de = np.asarray(d["direct"], float) - tr
        ee = np.asarray(d["eblup"], float) - tr
        x = np.log2(n_t[ok])
        lo = float(10*np.floor(min(-45., np.nanmin(de[ok]), np.nanmin(ee[ok]))/10))
        hi = float(10*np.ceil(max(75., np.nanmax(de[ok]), np.nanmax(ee[ok]))/10))
        A = axes([0.8, 9], [lo, hi], x_length=7.4, y_length=4.6, xlabel=r"respondents in the town \ (log scale)",
                 ylabel=r"error, \ thousands", xticks=[1, 2, 3, 4, 5, 6, 7, 8], yticks=[-40, 0, 40],
                 xfmt=lambda v: f"{2 ** v:.0f}", center=[-2.0, 0.3, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(11))
        jit = 0.12 * (g.random(ok.sum()) - 0.5)
        dd = VGroup(*[Dot(ax.c2p(a + j, b), radius=0.045, color=RAW, fill_opacity=0.75) for a, j, b in zip(x, jit, de[ok])])
        ed = VGroup(*[Dot(ax.c2p(a + j, b), radius=0.045, color=SHRUNK, fill_opacity=0.9) for a, j, b in zip(x, jit, ee[ok])])
        zero = DashedLine(ax.c2p(0.8, 0), ax.c2p(9, 0), color=TRUE, stroke_width=2)
        big = int(np.argmax(n_t))
        rows = fit_rows(VGroup(
            label(rf"{d['towns_used']} towns with 2 or more respondents", font_size=22),
            label(r"blue: \ direct estimate minus truth", font_size=22, color=RAW),
            label(r"green: \ the EBLUP minus truth", font_size=22, color=SHRUNK),
            label(rf"$\hat A = {d['A']:.1f}$: \ $\gamma_t$ median {np.median(d['gamma']):.2f}", font_size=22, color=SHRUNK),
            label(rf"the largest town, \ {int(n_t[big])} respondents: \ $\gamma = {np.max(d['gamma']):.2f}$", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The hundred and fifty-eight towns with at least two respondents, placed by their sample "
            "size. <bookmark mark='b'/> The direct estimates' errors fan out, tens of thousands for towns with a handful of "
            "people. <bookmark mark='c'/> The EBLUPs' errors hug zero. <bookmark mark='d'/> The estimated town variance A is "
            "only nine, a standard deviation of three thousand, tiny next to a sample mean of four incomes, so the typical "
            "town gets a weight of point oh three on its own data: almost all synthetic. <bookmark mark='e'/> Only the largest "
            "town, with three hundred and eighty-five respondents, is trusted mostly on its own."
        ) as vo:
            self.add(simulated_tag())
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in dd], lag_ratio=0.01), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(dd.animate.set_opacity(0.25), LaggedStart(*[FadeIn(p) for p in ed], lag_ratio=0.01), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def table(self):
        d = load("smallarea")
        hdr = [r"\textbf{estimator}", r"\textbf{mean squared error}", r"\textbf{uses}"]
        body = [[r"direct: \ the town's sample mean", f"{d['mse_direct']:.0f}", r"only the town"],
                [r"synthetic: \ the region's prediction", f"{d['mse_synth']:.1f}", r"only the region"],
                [r"Fay--Herriot EBLUP", f"{d['mse_eblup']:.1f}", r"both, \ weighted by $\gamma_t$"]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A, RAW, POOLED, SHRUNK])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"direct is nearly 20 times worse", font_size=22, color=RES),
            label(r"single realization, eligible towns only: \ synthetic and EBLUP MSE close", font_size=22, color=POOLED),
            label(r"the EBLUP is the insurance: \ if a town is unusual and well sampled, \ it says so", font_size=22, color=HIT),
        ), 12.0, 0.22, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Against the World's true town means: <bookmark mark='b'/> the direct estimates have"
            " a mean squared error of three hundred and eighty-three, nearly twenty times the others. <bookmark "
            "mark='c'/> The purely synthetic regional prediction scores twenty point one, and the Fay–Herriot EBLUP "
            "twenty point six, close in this single realization. We have not computed uncertainty for this MSE "
            "comparison. Here the regions explain the towns well, so there is little left to learn from a town's own "
            "few respondents. <bookmark mark='d'/> The EBLUP is insurance: when a town is unusual and well sampled, "
            "it follows the town's own data, which a synthetic estimate never can. And because it is data-driven, the"
            " same formula decides how much to trust each town."
        ) as vo:
            self.add(simulated_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[1]), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(tb[2]), FadeIn(tb[3]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def practice(self):
        rows = fit_rows(VGroup(
            label(r"SAIPE: \ a family of small-area methods, \ not one identical model", font_size=24, color=PATH),
            label(r"linking covariates: \ tax records, \ benefit counts, \ the last census", font_size=24),
            label(r"benchmarking: \ population-weighted means match a national total", font_size=24),
            label(r"unit-level models: \ Battese, Harter \& Fuller (1988), \ individuals, \ not area means", font_size=24),
            label(r"Part 18's surveys, \ plus Part 25's shrinkage", font_size=24, color=HIT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> This is how official statistics are made locally. The US Census Bureau's small-area"
            " income and poverty estimates for every state and county, which feed the allocation of federal school "
            "funding, use a family of small-area methods related to this framework. State, county and school-district"
            " estimates do not all use one identical Fay–Herriot model. <bookmark mark='b'/> Their linking covariates"
            " are tax records, benefit counts and the last census. <bookmark mark='c'/> Benchmarking can constrain "
            "population-weighted area means to a reliable national total; simply adding unweighted town means would "
            "not give that total. <bookmark mark='d'/> George Battese, Rachel Harter and Wayne Fuller's unit-level "
            "version models individuals rather than area means, as this part's mixed models do. <bookmark mark='e'/> "
            "It is Part 18's survey sampling, joined to this part's shrinkage."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
