from __future__ import annotations

import numpy as np

from explainer.stats.board import load_all
from videos.stats.stats13.common import *  # noqa: F403

WET, DRY = S.CTRL, S.POST


class SplitPlot(VoiceoverScene):
    def construct(self):
        self.card()
        self.layout()
        self.strata()
        self.two_analyses()
        self.size()
        self.why_split()
        self.industry()

    def card(self):
        card = chapter_card(10, r"Split plots", r"Two sizes of plot, \ two sizes of error", lit=(1935,), part=PART)
        with self.voiceover("Chapter ten. Split plots."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def layout(self):
        g = np.random.Generator(np.random.PCG64(1937))
        cell = 0.52
        blocks = VGroup()
        tags = VGroup()
        wps = VGroup()
        for b in range(4):
            order = g.permutation(2)
            for h, irr in enumerate(order):
                x0 = -4.6 + b * 2.45 + h * 1.12
                wp = Rectangle(width=1.04, height=4 * cell + 0.12, stroke_width=0, fill_color=[DRY, WET][irr], fill_opacity=0.22)
                wp.move_to([x0, 0.3, 0])
                wps.add(wp)
                vs = g.permutation(4)
                for r, v in enumerate(vs):
                    sq = Square(side_length=cell, stroke_width=1, stroke_color=GREY_D, fill_opacity=0)
                    sq.move_to([x0, 0.3 + (1.5 - r) * cell, 0])
                    blocks.add(sq)
                    tags.add(label("abcd"[v], font_size=22, color=TRT[v]).move_to(sq))
            frame = Rectangle(width=2.3, height=4 * cell + 0.35, color=BLOCK, stroke_width=2).move_to([-4.6 + b * 2.45 + 0.56, 0.3, 0])
            blocks.add(frame)
            blocks.add(label(rf"block {b + 1}", font_size=20, color=BLOCK).next_to(frame, UP, buff=0.1))
        key = VGroup(label(r"irrigated", font_size=22, color=WET), label(r"dry", font_size=22, color=DRY),
                     label(r"varieties a--d", font_size=22, color=GREY_B)).arrange(RIGHT, buff=0.6).move_to([0, -1.6, 0])
        rows = fit_rows(VGroup(
            label(r"irrigation is applied to a whole strip by a channel: \ it cannot be given plot by plot", font_size=24),
            label(r"so: \ randomize irrigation to whole plots, \ two per block", font_size=24, color=WET),
            label(r"then split each whole plot into 4 subplots, \ and randomize varieties within it", font_size=24),
            label(r"two randomizations, \ at two scales: \ a split-plot design (Yates 1935)", font_size=24, color=OBS),
        ), 12.6, 0.22, [0, -2.65, 0])
        with self.voiceover(
            "Some factors can only be applied to big pieces of land. <bookmark mark='a'/> Irrigation runs along a channel: you "
            "can water a whole strip, not one small plot here and another there. <bookmark mark='b'/> So randomize irrigation "
            "over large whole plots, two per block, one wet and one dry. <bookmark mark='c'/> Then split each whole plot into "
            "four subplots, and randomize four varieties of wheat among them, separately in each whole plot. "
            "<bookmark mark='d'/> Two randomizations, at two scales: a split-plot design, which Frank Yates described at "
            "Rothamsted in the 1930s. It's convenient, and very common. And it is very commonly analysed wrongly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(wps, lag_ratio=0.08), FadeIn(key[:2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(blocks), FadeIn(tags, lag_ratio=0.01), FadeIn(key[2]), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def strata(self):
        rows = [
            cmath(r"y_{bij}", r"=", r"\mu + \beta_b + \alpha_i + w_{bi} + \gamma_j + (\alpha\gamma)_{ij} + e_{bij}", font_size=32),
            cmath(r"w_{bi} \sim N(0, \sigma_w^2)", r",", r"e_{bij} \sim N(0, \sigma^2)", font_size=32),
            cmath(r"\mathrm{Var}(\bar y_{\text{wet}} - \bar y_{\text{dry}})", r"=", r"\frac{2}{b}\Big(\sigma_w^2 + \frac{\sigma^2}{4}\Big)", font_size=32),
            cmath(r"\mathrm{Var}(\bar y_{a} - \bar y_{c})", r"=", r"\frac{2\sigma^2}{2b}", font_size=32),
        ]
        rows[2][2].set_color(WET)
        rows[3][2].set_color(S.ALT)
        whys = [why(r"$w$: \ each whole plot's own error"), why(r"two error strata"),
                why(r"irrigation: \ compared between whole plots"), why(r"varieties: \ compared within them, \ $w$ cancels")]
        with self.voiceover(
            "<bookmark mark='a'/> The model has two error terms. Each whole plot has its own random error, w, shared by its four "
            "subplots: the soil of that strip, the way its channel ran. Each subplot also has its own error, e. "
            "<bookmark mark='b'/> Two strata of error, sigma w and sigma, taken independent and Gaussian here for the exact F references. <bookmark mark='c'/> Irrigation is compared between "
            "whole plots, so its comparison carries the whole-plot error: the variance involves sigma w squared, divided by "
            "the number of blocks, just four. <bookmark mark='d'/> Varieties are compared within whole plots, so w cancels, "
            "and only the small subplot error remains. The split plot measures the subplot factor precisely, and the "
            "whole-plot factor coarsely."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def two_analyses(self):
        d = load("splitplot")["example"]
        t1 = table_rows([
            [r"wrong: \ a CRD", r"df", r"MS", r"$F$", r"$p$"],
            [r"irrigation", r"1", r"", rf"{d['F_wrong']:.1f}", r"$8\times10^{-5}$"],
            [r"pooled error", rf"{d['df_e']}", rf"{d['ms_e']:.2f}", r"", r""],
        ], font_size=26, col_buff=0.6, row_buff=0.25, colors=[GREY_B, RES, RES]).move_to([-3.4, 1.0, 0])
        t2 = table_rows([
            [r"right: \ split plot", r"df", r"MS", r"$F$", r"$p$"],
            [r"irrigation", r"1", r"", rf"{d['F_right']:.2f}", rf"{d['p_right']:.2f}"],
            [r"whole-plot error", rf"{d['df_wp']}", rf"{d['ms_wp']:.2f}", r"", r""],
            [r"subplot error", rf"{d['df_e'] - 6}", r"", r"", r""],
        ], font_size=26, col_buff=0.6, row_buff=0.25, colors=[GREY_B, HIT, HIT, GREY_A]).move_to([3.4, 0.85, 0])
        foot = fit_rows(VGroup(
            label(r"the same data: \ a real irrigation effect of 2, \ $\sigma_w = 2$, \ $\sigma = 1$", font_size=24),
            label(r"the CRD divides by an error pooled mostly from subplots, \ and claims 24 df", font_size=24, color=RES),
            label(r"the right analysis uses the whole-plot error: \ 3 df, \ from 8 whole plots in 4 blocks", font_size=24, color=HIT),
            label(r"only 8 whole plots ever got irrigation or not: \ that is the real sample size", font_size=24, color=OBS),
        ), 12.6, 0.24, [0, -2.2, 0])
        with self.voiceover(
            "Here's one simulated split plot, with a real irrigation effect of two bushels. <bookmark mark='a'/> The common "
            "mistake: analyse it as if all thirty-two subplots had been randomized independently, a completely randomized "
            "design. Irrigation gets an F of twenty-two, on one and twenty-four degrees of freedom: p of eight in a hundred "
            "thousand. <bookmark mark='b'/> The right analysis compares irrigation with the variation between whole plots, the "
            "whole-plot error, which has just three degrees of freedom. F is six point eight; p is point zero eight. "
            "<bookmark mark='c'/> The effect is real here, but the first analysis claims far more certainty than the "
            "experiment contains, by dividing by an error made mostly of the small subplot variation, and by counting "
            "twenty-four degrees of freedom for a comparison that has three. <bookmark mark='d'/> Only eight whole plots were ever randomized to irrigation "
            "or not. That is the real sample size for irrigation, however many subplots each one holds."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(t1, lag_ratio=0.1), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(t2, lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[3]))
        self.clear_scene()

    def size(self):
        rb = {r.method: r for r in load_all(upto=13) if r.part == 13}
        wrong = rb[r"split plot as a CRD"].achieved
        right = rb[r"split plot, \ whole-plot error"].achieved
        A = axes([0, 1], [0, 0.32], x_length=6.0, y_length=4.0, xlabel=r"", ylabel=r"false rejections", xticks=[],
                 yticks=[0, 0.05, 0.1, 0.2, 0.3], center=[-2.6, 0.1, 0], yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        w = ax.c2p(0.25, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        for x, v, c in ((0.28, wrong, RES), (0.72, right, HIT)):
            h = ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
            bars.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(ax.c2p(x, 0), aligned_edge=DOWN))
        nom = DashedLine(ax.c2p(0, 0.05), ax.c2p(1, 0.05), color=EXACT, stroke_width=2)
        nl = label(r"5\% promised", font_size=20, color=EXACT).next_to(nom, RIGHT, buff=0.1)
        names = VGroup(label(r"as a CRD", font_size=22, color=RES).next_to(bars[0], DOWN, buff=0.15),
                       label(r"split-plot error", font_size=22, color=HIT).next_to(bars[1], DOWN, buff=0.15))
        vals = VGroup(label(rf"{100 * wrong:.1f}\%", font_size=24, color=RES).next_to(bars[0], UP, buff=0.1),
                      label(rf"{100 * right:.2f}\%", font_size=24, color=HIT).next_to(bars[1], UP, buff=0.1))
        rows = fit_rows(VGroup(
            label(r"10,000 split plots with no irrigation effect at all", font_size=24),
            label(rf"analysed as a CRD: \ ``significant'' {100 * wrong:.0f}\% of the time", font_size=24, color=RES),
            label(rf"with the whole-plot error: \ {100 * right:.2f}\%", font_size=24, color=HIT),
            label(r"both rows join the Coverage Board", font_size=22, color=GREY_A),
        ), 5.0, 0.36, [4.3, 0.3, 0])
        with self.voiceover(
            "How bad is the mistake? <bookmark mark='a'/> Simulate ten thousand split plots in which irrigation does nothing "
            "at all. <bookmark mark='b'/> Analysed as a completely randomized design, irrigation comes out significant at five "
            "percent in twenty-six percent of them: a five percent promise broken five times over. <bookmark mark='c'/> With "
            "the whole-plot error, the rate is five point oh one percent: kept. <bookmark mark='d'/> Both rows go on the "
            "Coverage Board. The general lesson is one of the most important in applied statistics: the error term must come "
            "from the scale at which the treatment was randomized. It returns with mixed models in Part 25, and with "
            "clustered data everywhere."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(names[0]), FadeIn(vals[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(names[1]), FadeIn(vals[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def why_split(self):
        rows = [
            cmath(r"\mathbb E[\text{MS}_{\text{irrigation}} \mid H_0]", r"=", r"\sigma^2 + 4\sigma_w^2 = 17", font_size=32),
            cmath(r"\mathbb E[\text{MS}_{\text{subplot}}]", r"=", r"\sigma^2 = 1", font_size=32),
            cmath(r"\text{CRD error}", r"=", r"\tfrac{1}{24}\big(3\,\text{MS}_{\text{block}} + 3\,\text{MS}_{\text{whole plot}} + 18\,\text{MS}_{\text{subplot}}\big)", font_size=28),
            cmath(r"\mathbb E[\text{CRD error}]", r"=", r"(3 \cdot 25 + 3 \cdot 17 + 18 \cdot 1)/24 = 6", font_size=30),
        ]
        rows[2][2].set_color(RES)
        rows[3][2].set_color(RES)
        whys = [why(r"each whole plot's mean carries its $w$; \ $\sigma_w = 2$, \ $\sigma = 1$"), why(r"within whole plots, \ $w$ cancels"),
                why(r"the CRD pools three strata into one error"), why(r"so $F \approx 17/6$ with no effect, \ judged on 24 df")]
        with self.voiceover(
            "Why does it fail? Look at what each mean square estimates. <bookmark mark='a'/> With no real effect, irrigation's "
            "mean square estimates sigma squared plus four sigma w squared, because each whole plot's mean carries its own w. "
            "With our values, seventeen. The right analysis divides it by the whole-plot error, which estimates the same "
            "seventeen. <bookmark mark='b'/> The subplot error estimates only sigma squared, one. <bookmark mark='c'/> The "
            "completely randomized analysis pools everything left over into one error: three degrees of freedom of blocks, "
            "three of whole-plot error, and eighteen of subplot error. <bookmark mark='d'/> Dominated by the subplots, it "
            "estimates about six, not seventeen. So with no effect at all, its ratio of expected mean squares is nearly three; this is not the exact expectation of the ratio, and it's judged "
            "against an F distribution with twenty-four denominator degrees of freedom instead of three. Both mistakes push "
            "the same way."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def industry(self):
        rows = fit_rows(VGroup(
            label(r"split plots hide everywhere a factor is hard to change", font_size=26),
            label(r"a furnace temperature set once per day, \ several recipes baked in it", font_size=24, color=WET),
            label(r"a classroom's teaching method, \ students within it", font_size=24, color=WET),
            label(r"a mouse's diet, \ several tissues measured from it", font_size=24, color=WET),
            label(r"the hard-to-change factor's sample size is the number of times it was set", font_size=24, color=OBS),
            label(r"analyse as you randomized: \ one error stratum per randomization", font_size=24, color=OBS),
        ), 12.4, 0.42, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Split plots hide wherever a factor is hard to change. <bookmark mark='b'/> In a factory, the "
            "furnace temperature is set once a day and several recipes are baked at it: temperature is a whole-plot factor. "
            "<bookmark mark='c'/> In education, a teaching method is given to a classroom, and the students in it are "
            "subplots. <bookmark mark='d'/> In biology, a diet is given to a mouse, and several tissues are measured from "
            "each one. <bookmark mark='e'/> In every case, the hard-to-change factor's real sample size is the number of "
            "times it was independently set: days, classrooms, mice. <bookmark mark='f'/> Analyse the experiment the way it was "
            "randomized, with one error stratum for each randomization. That's chapter one's last principle, and here is where "
            "ignoring it costs the most."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
