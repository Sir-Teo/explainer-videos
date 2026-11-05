from __future__ import annotations

import numpy as np

from videos.stats.stats18.common import *  # noqa: F403

BANDS = [r"under 30k", r"30--100k", r"over 100k"]


class Strata(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.bands()
        self.neyman()
        self.allocations()
        self.results()
        self.region_vote()
        self.post()

    def card(self):
        card = chapter_card(5, r"Stratification", r"Divide, \ then sample each part", part=PART)
        with self.voiceover("Chapter five. Stratification."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"\text{strata}", r":", r"\text{split the population into groups } h,\ \ W_h = N_h/N", font_size=30),
            cmath(r"\bar y_{\text{st}}", r"=", r"\textstyle\sum_h W_h\,\bar y_h", font_size=32),
            cmath(r"\mathrm{Var}(\bar y_{\text{st}})", r"=", r"\textstyle\sum_h W_h^2 \big(1 - \frac{n_h}{N_h}\big) \frac{S_h^2}{n_h}", font_size=30),
            cmath(r"\text{the gain}", r":", r"\text{only the variation \emph{within} strata remains}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"using what the frame already tells us"), why(r"an SRS in each stratum, \ combined"),
                why(r"strata are sampled independently"), why(r"the between-strata variation is removed by design")]
        with self.voiceover(
            "<bookmark mark='a'/> If the frame tells us something about everyone, we can use it before sampling. Split the "
            "population into groups, called strata, whose sizes we know. <bookmark mark='b'/> Take a simple random sample in "
            "each, and combine the stratum means with their population weights. <bookmark mark='c'/> The strata are sampled "
            "independently, so the variance is a weighted sum of within-stratum variances. <bookmark mark='d'/> The differences "
            "between strata, which an SRS has to estimate along with everything else, contribute nothing: the design has "
            "fixed each stratum's share exactly."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bands(self):
        d = load("strat")
        tab = table_rows([
            [r"income band", r"adults $N_h$", r"mean, \ thousands", r"SD $S_h$"],
            *[[BANDS[k], f"{int(d['Nh'][k]):,}", f"{d['means'][k]:.1f}", f"{d['Sh'][k]:.1f}"] for k in range(3)],
        ], font_size=28, colors=[GREY_B, None, None, RES]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"the tax register gives every adult's income band", font_size=24),
            label(r"the top band: \ 7.5\% of adults, \ but 28 times the spread of the bottom", font_size=24, color=RES),
        ), 12.4, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "An example where it matters. Suppose we want the World's mean income, from a sample of a thousand, "
            "<bookmark mark='a'/> and the tax register tells us everyone's income band: under thirty thousand, thirty to a "
            "hundred, over a hundred. <bookmark mark='b'/> The bands differ enormously. The top band holds seven and a half "
            "percent of adults, but its standard deviation is a hundred and sixty thousand, twenty-eight times the bottom "
            "band's, because the Pareto tail of Part 1 lives there."
        ) as vo:
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]), Indicate(tab[3], color=RES))
        self.clear_scene()

    def neyman(self):
        rows = [
            cmath(r"\min_{n_h}", r"\ ", r"\textstyle\sum_h W_h^2 S_h^2 / n_h\ \ \text{subject to}\ \sum_h n_h = n", font_size=30),
            cmath(r"-W_h^2 S_h^2 / n_h^2 + \lambda", r"=", r"0", font_size=30),
            cmath(r"n_h", r"=", r"n\,\frac{N_h S_h}{\sum_k N_k S_k}", font_size=34),
            cmath(r"\text{proportional}", r":", r"n_h = n\,N_h/N", font_size=30),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"ignore the fpc; \ fix the total"), why(r"a Lagrange multiplier"),
                why(r"Neyman allocation (Tschuprow 1923; \ Neyman 1934)"), why(r"the same if every $S_h$ is equal")]
        with self.voiceover(
            "How many to take from each band? <bookmark mark='a'/> Minimize the variance for a fixed total sample size. "
            "<bookmark mark='b'/> With a Lagrange multiplier, each stratum's term must have the same marginal value, "
            "<bookmark mark='c'/> which gives n h proportional to the stratum's size times its standard deviation. Alexander "
            "Tschuprow found it in 1923, and Neyman, independently, in 1934. <bookmark mark='d'/> Proportional allocation, "
            "sampling each stratum in proportion to its size, is the special case where every stratum is equally variable. "
            "Neyman's rule says: sample more where the population is more variable."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def allocations(self):
        d = load("strat")
        A = axes([-0.6, 2.6], [0, 650], x_length=7.2, y_length=4.0, xlabel=r"", ylabel=r"people sampled, \ of 1,000",
                 yticks=[0, 200, 400, 600], center=[-1.8, 0.4, 0])
        ax = A.ax
        w = ax.c2p(0.38, 0)[0] - ax.c2p(0, 0)[0]
        pb = VGroup(*[Rectangle(width=w, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=GREY_B, fill_opacity=0.85)
                      .move_to(ax.c2p(k - 0.2, 0), aligned_edge=DOWN) for k, v in enumerate(d["prop"])])
        nb = VGroup(*[Rectangle(width=w, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=OBS, fill_opacity=0.9)
                      .move_to(ax.c2p(k + 0.2, 0), aligned_edge=DOWN) for k, v in enumerate(d["ney"])])
        pv = VGroup(*[MathTex(f"{v:.0f}", font_size=22, color=GREY_B).next_to(b_, UP, buff=0.06) for b_, v in zip(pb, d["prop"])])
        nv = VGroup(*[MathTex(f"{v:.0f}", font_size=22, color=OBS).next_to(b_, UP, buff=0.06) for b_, v in zip(nb, d["ney"])])
        names = VGroup(*[label(t, font_size=20, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15) for k, t in enumerate(BANDS)])
        rows = fit_rows(VGroup(
            label(r"grey: \ proportional", font_size=22, color=GREY_B),
            label(r"gold: \ Neyman", font_size=22, color=OBS),
            label(r"Neyman takes half the sample from the richest 7.5\%", font_size=22),
            label(r"each of them then carries a small weight", font_size=20, color=GREY_A),
        ), 4.2, 0.4, [4.8, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Proportional allocation takes three hundred and thirty-four from the bottom band, five "
            "hundred and ninety-one from the middle and seventy-five from the top. <bookmark mark='b'/> Neyman's allocation "
            "takes eighty, four hundred and twenty-three, and four hundred and ninety-seven: <bookmark mark='c'/> half the "
            "sample from the richest seven and a half percent of adults, where all the uncertainty is. "
            "<bookmark mark='d'/> It isn't a biased sample: each of them carries a small weight in the estimate, their "
            "stratum's share divided by its sample size."
        ) as vo:
            self.play(FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in pb], lag_ratio=0.2), FadeIn(pv), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in nb], lag_ratio=0.2), FadeIn(nv), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Indicate(nb[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def results(self):
        d = load("strat")
        tab = table_rows([
            [r"design, \ $n = 1{,}000$", r"SE, \ formula", r"SD over 3,000 samples"],
            [r"simple random sample", f"{d['se_srs']:.2f}", f"{d['sim_sd']['srs']:.2f}"],
            [r"stratified, \ proportional", f"{d['se_prop']:.2f}", f"{d['sim_sd']['prop']:.2f}"],
            [r"stratified, \ Neyman", f"{d['se_ney']:.2f}", f"{d['sim_sd']['ney']:.2f}"],
        ], font_size=28, colors=[GREY_B, None, GREY_B, OBS]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"thousands of the World's currency; \ truth 49.48", font_size=22, color=GREY_A),
            label(r"Neyman halves the SE: \ as good as an SRS of about 5,600", font_size=24, color=OBS),
            label(r"the SRS's simulated SD is below its formula: \ the heavy tail again", font_size=20, color=GREY_B),
        ), 12.4, 0.3, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The results. A simple random sample of a thousand estimates mean income with a standard error "
            "of one point eight thousand. Stratifying with proportional allocation brings it to one point four five. "
            "Neyman's allocation: point seven six, <bookmark mark='b'/> less than half the SRS's, as good as a simple random "
            "sample of about fifty-six hundred. The simulation over three thousand samples agrees with the formulas. "
            "<bookmark mark='c'/> The SRS's simulated spread is a little below its formula, because with the Pareto tail a few "
            "enormous incomes dominate the variance; the stratified designs control exactly that."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def region_vote(self):
        from videos.stats.stats18.compute import adults
        P = adults()
        v, reg = P["vote"], P["region"]
        W = np.bincount(reg) / len(v)
        ph = np.array([v[reg == h].mean() for h in range(10)])
        p = v.mean()
        within = float(np.sum(W * ph * (1 - ph)))
        rows = [
            cmath(r"\text{the vote, \ strata = 10 regions}", r":", rf"p_h \text{{ from }} {100 * ph.min():.0f}\% \text{{ to }} {100 * ph.max():.0f}\%", font_size=28),
            cmath(r"\text{SRS}", r":", rf"p(1 - p) = {p * (1 - p):.4f}", font_size=30),
            cmath(r"\text{stratified}", r":", rf"\textstyle\sum_h W_h p_h(1 - p_h) = {within:.4f}", font_size=30),
            cmath(r"\text{gain}", r":", rf"{100 * (1 - within / (p * (1 - p))):.1f}\%\ \text{{of the variance}}", font_size=30),
        ]
        rows[3][2].set_color(GREY_A)
        whys = [why(r"real differences between regions"), why(r"per respondent"), why(r"proportional allocation, \ per respondent"),
                why(r"tiny: \ the regions differ far less than people do")]
        with self.voiceover(
            "Stratification isn't always dramatic. <bookmark mark='a'/> Stratify the vote by the World's ten regions: Blue's "
            "share ranges from thirty to forty-six percent across them, a real difference. <bookmark mark='b'/> An SRS's "
            "variance per respondent is p times one minus p. <bookmark mark='c'/> A proportionally stratified sample's is the "
            "weighted average of the within-region values, <bookmark mark='d'/> and the gain is just one and a half percent. "
            "However different the regions' averages, the people within each region differ far more. Stratification pays when "
            "the strata explain a large share of the variance, as the income bands did for income."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def post(self):
        rows = [
            cmath(r"\text{strata known only after sampling}", r":", r"\text{post-stratify}", font_size=30),
            cmath(r"w_i", r"=", r"\frac{W_h}{n_h/n}\ \ \text{for } i \text{ in group } h", font_size=32),
            cmath(r"\bar y_{\text{ps}}", r"=", r"\textstyle\sum_h W_h \bar y_h", font_size=32),
            cmath(r"\text{needs}", r":", r"\text{known population shares } W_h", font_size=30),
        ]
        rows[1][2].set_color(WEIGHT)
        whys = [why(r"e.g. age or region, \ asked in the interview"), why(r"each group weighted to its true share"),
                why(r"the stratified estimator, \ after the fact"), why(r"from a census: \ chapter nine builds on it")]
        with self.voiceover(
            "<bookmark mark='a'/> Often the grouping is known only after the interview: a person's age, or region, isn't on "
            "the frame. Then we post-stratify. <bookmark mark='b'/> Give each respondent a weight: their group's population share "
            "divided by its share of the sample. <bookmark mark='c'/> The weighted mean is the stratified estimator, built after "
            "the fact, and nearly as good as stratifying in advance. <bookmark mark='d'/> It needs the groups' population "
            "shares, usually from a census. Chapter nine extends it to many variables at once, and to samples that weren't "
            "random to begin with."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
