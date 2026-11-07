from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403


class Blocking(VoiceoverScene):
    def construct(self):
        self.card()
        self.field()
        self.two_tables()
        self.power()
        self.model()
        self.darwin()
        self.fisher_zea()
        self.when()

    def card(self):
        card = chapter_card(5, r"Blocking", r"Compare like with like, \ and take the soil out of the error", lit=(1935,), part=PART)
        with self.voiceover("Chapter five. Blocking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def field(self):
        d = load("blocking")
        y = np.asarray(d["y"])
        alloc = np.asarray(d["alloc"])
        fp = field_from(np.asarray(d["fertility"]), cell=0.8, center=[-3.1, 0.5, 0], lo=40, hi=60)
        frames = VGroup(*[fp.outline(0, 3, c, c, color=BLOCK, stroke_width=3) for c in range(6)])
        blab = VGroup(*[label(rf"block {c + 1}", font_size=18, color=BLOCK).next_to(fp.cells[0][c], UP, buff=0.15) for c in range(6)])
        tags = fp.tags(alloc, names="ABCD", colors=TRT, font_size=24)
        yfp = field_from(y, cell=0.8, center=[-3.1, 0.5, 0], lo=40, hi=60)
        rows = fit_rows(VGroup(
            label(r"a field with a steep east--west slope in fertility", font_size=24),
            label(r"blocks: \ the six north--south strips, \ each nearly uniform", font_size=24, color=BLOCK),
            label(r"all four treatments in every block, \ shuffled within it", font_size=24),
            label(r"a randomized complete block design (RCBD)", font_size=26, color=OBS),
            label(r"true gains: \ 0, \ 2, \ 3, \ 1.5 bushels", font_size=22, color=GREY_A),
        ), 5.0, 0.34, [4.2, 0.4, 0])
        tag = simulated_tag(r"the field-trial simulator", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Here's a field with a steep slope in fertility, from about forty-two bushels on the west "
            "edge to fifty-eight on the east. Four treatments, A to D, six plots each. <bookmark mark='b'/> The slope runs east "
            "to west, so each north-to-south strip of four plots is nearly uniform. Make each strip a block. "
            "<bookmark mark='c'/> Put all four treatments in every block, and randomize their order within it, separately for "
            "each block. <bookmark mark='d'/> That's a randomized complete block design: complete, because every block holds "
            "every treatment. <bookmark mark='e'/> The true gains over A are two, three and one and a half bushels. "
            "Here's the harvest."
        ) as vo:
            self.play(FadeIn(fp, lag_ratio=0.02), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(frames, lag_ratio=0.15), FadeIn(blab), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(tags, lag_ratio=0.03), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            self.play(*[fp.cells[r][c].animate.set_fill(yfp.cells[r][c].get_fill_color()) for r in range(4) for c in range(6)], run_time=1.5)
        self.clear_scene()

    def two_tables(self):
        d = load("blocking")
        rb, ig = d["rcbd"], d["ignore"]
        t1 = table_rows([
            [r"ignoring the blocks", r"df", r"SS", r"MS", r"$F$", r"$p$"],
            [r"treatment", r"3", rf"{ig['ssb']:.1f}", rf"{ig['ssb'] / 3:.1f}", rf"{ig['F']:.2f}", rf"{ig['p']:.2f}"],
            [r"residual", r"20", rf"{ig['ssw']:.1f}", rf"{ig['mse']:.1f}", r"", r""],
        ], font_size=24, col_buff=0.55, row_buff=0.22, colors=[GREY_B, DATA, RES]).move_to([0, 2.0, 0])
        t2 = table_rows([
            [r"with the blocks", r"df", r"SS", r"MS", r"$F$", r"$p$"],
            [r"block", r"5", rf"{rb['ss_block']:.1f}", rf"{rb['ss_block'] / 5:.1f}", r"", r""],
            [r"treatment", r"3", rf"{rb['ss_treat']:.1f}", rf"{rb['ss_treat'] / 3:.1f}", rf"{rb['F']:.2f}", rf"{rb['p']:.3f}"],
            [r"residual", r"15", rf"{rb['sse']:.1f}", rf"{rb['mse']:.2f}", r"", r""],
        ], font_size=24, col_buff=0.55, row_buff=0.22, colors=[GREY_B, BLOCK, OBS, RES]).move_to([0, -0.6, 0])
        foot = fit_rows(VGroup(
            label(r"the same 24 numbers, \ the same treatment SS", font_size=24),
            label(r"the blocks take 829 of the 859 residual SS, \ into a row of their own", font_size=24, color=BLOCK),
        ), 12.0, 0.22, [0, -2.7, 0])
        intro = label('Analyse the same harvest with and without its blocks', font_size=36)
        with self.voiceover(
            "Analyse the harvest two ways. <bookmark mark='a'/> Ignore the blocks, and run Chapter three's one-way analysis. "
            "The treatment sum of squares is ten point nine, but the residual is eight hundred and fifty-nine: the soil's slope is in the "
            "error. F is point zero eight, p point nine seven. Nothing to see. <bookmark mark='b'/> Now include the blocks, as the "
            "design says we must. The block row takes eight hundred and twenty-nine of the sum of squares. The treatment sum of "
            "squares is exactly the same ten point nine, but the residual has fallen to thirty, the error mean square from "
            "forty-three to two point zero one. F is one point eight one, p point one nine. This is the first seeded harvest, chosen before seeing its result. Better precision still does not guarantee significance. <bookmark mark='c'/> The same "
            "twenty-four numbers, the same treatment comparison. <bookmark mark='d'/> The difference is that the design "
            "measured the soil, and the analysis took it out of the error."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(t1, lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(t2, lag_ratio=0.1))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(foot[k]))
        self.clear_scene()

    def power(self):
        d = load("blocking")
        A = axes([0, 1], [0, 1], x_length=6.0, y_length=4.2, xlabel=r"", ylabel=r"power", xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1],
                 center=[-2.8, 0.0, 0], yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        w = ax.c2p(0.25, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup()
        for x, v, c in ((0.28, d["power_crd"], RES), (0.72, d["power_rcbd"], OBS)):
            h = ax.c2p(0, v)[1] - ax.c2p(0, 0)[1]
            bars.add(Rectangle(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to(ax.c2p(x, 0), aligned_edge=DOWN))
        names = VGroup(label(r"completely randomized", font_size=20, color=RES).next_to(bars[0], DOWN, buff=0.15),
                       label(r"randomized blocks", font_size=20, color=OBS).next_to(bars[1], DOWN, buff=0.15))
        vals = VGroup(label(rf"{100 * d['power_crd']:.0f}\%", font_size=24, color=RES).next_to(bars[0], UP, buff=0.1),
                      label(rf"{100 * d['power_rcbd']:.0f}\%", font_size=24, color=OBS).next_to(bars[1], UP, buff=0.1))
        rows = fit_rows(VGroup(
            label(r"4,000 repetitions of each design on this field", font_size=24),
            MathTex(rf"\text{{mean error MS:}}\ {d['mse_crd']:.1f}\ \to\ {d['mse_rcbd']:.2f}", font_size=30),
            MathTex(rf"\text{{relative efficiency}} \approx {d['mse_crd'] / d['mse_rcbd']:.0f}", font_size=30, color=OBS),
            label(r"blocking here is worth fifteen times the plots", font_size=24, color=OBS),
            label(r"the gain is the soil's variation between blocks", font_size=22, color=GREY_A),
        ), 5.0, 0.34, [4.3, 0.2, 0])
        with self.voiceover(
            "The first harvest did not detect the real differences. How often does each design succeed? <bookmark mark='a'/> Repeat each design four thousand times on this field. "
            "<bookmark mark='b'/> The completely randomized design, analysed one way, detects the treatment differences ten "
            "percent of the time. The block design detects them seventy-four percent of the time. <bookmark mark='c'/> The "
            "average error mean square falls from thirty-three to two point two five. <bookmark mark='d'/> Since variance "
            "falls like one over the number of plots, the block design is about as precise as a completely randomized one "
            "with fifteen times as many plots. <bookmark mark='e'/> Blocking also costs planning and error degrees of freedom; here its precision gain is worth "
            "fifteen fields."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(names[0]), FadeIn(vals[0]))
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(names[1]), FadeIn(vals[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"y_{tb}", r"=", r"\mu + \tau_t + \beta_b + \varepsilon_{tb}", font_size=34),
            cmath(r"\text{SST}", r"=", r"\text{SS}_{\text{treat}} + \text{SS}_{\text{block}} + \text{SSE}", font_size=34),
            cmath(r"\text{df}", r":", r"tb - 1 = (t - 1) + (b - 1) + (t - 1)(b - 1)", font_size=32),
            cmath(r"\bar y_{t\cdot} - \bar y_{t'\cdot}", r"=", r"\tau_t - \tau_{t'} + \bar\varepsilon_{t\cdot} - \bar\varepsilon_{t'\cdot}", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"additive: \ a block shifts every treatment equally"), why(r"three perpendicular pieces"),
                why(r"unreplicated: noise and treatment $\times$ block variation mix"), why(r"the block effects $\beta_b$ cancel exactly")]
        intro = label('The additive block model and its error assumptions', font_size=36)
        with self.voiceover(
            "The additive model behind the block design. Its exact F reference assumes independent Gaussian errors of equal variance; unreplicated interactions cannot be separately estimated. <bookmark mark='a'/> A yield is a grand mean, plus a treatment effect, plus a "
            "block effect, plus noise. The block effect shifts every treatment in that block by the same amount. "
            "<bookmark mark='b'/> The total sum of squares now splits into three perpendicular pieces: treatments, blocks and "
            "error. <bookmark mark='c'/> So do the degrees of freedom. The error is whatever's left: how far the treatment "
            "differences vary from block to block. <bookmark mark='d'/> And the key line: a difference between two "
            "treatment means contains no block effects at all. Every treatment saw every block once, so the soil cancels "
            "exactly, the same reason the pairs in chapter one worked."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.8, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def darwin(self):
        d = load("blocking")
        z = np.asarray(d["zea"])
        hc = history_card(1876, r"Charles Darwin, \ \emph{The Effects of Cross and Self Fertilisation in the Vegetable Kingdom}",
                          r"\emph{Zea mays}: \ 15 pairs of seedlings, \ one cross- and one self-fertilized, \ planted side by side in "
                          r"four pots; \ Francis Galton helped with the analysis", color=DATA, width=10.6, font_size=22).move_to([0, 2.2, 0])
        A = axes([-80, 90], [0, 1], x_length=10.0, y_length=1.4, xlabel=r"crossed minus selfed, \ eighths of an inch", ylabel=r"",
                 xticks=[-60, -30, 0, 30, 60], yticks=[], center=[0, -0.2, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(v, 0.5), radius=0.1, color=S.TREAT if v > 0 else S.CTRL) for v in z])
        zl = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1), color=GREY_B)
        rows = fit_rows(VGroup(
            label(r"each pair is a block of two: \ the same soil, \ light and water", font_size=24, color=BLOCK),
            label(rf"13 of 15 differences positive; \ mean {d['zea_mean']:.1f} eighths of an inch", font_size=24),
            label(r"two pairs strongly favour the selfed plant", font_size=24, color=S.CTRL),
        ), 12.0, 0.25, [0, -2.4, 0])
        tag = historical_tag(r"Darwin (1876), \ via Fisher (1935)", corner=DR)
        intro = label('Darwin compared plants within pairs', font_size=36)
        with self.voiceover(
            "Blocking is older than Fisher. <bookmark mark='a'/> In 1876 Charles Darwin published his experiments on cross- and "
            "self-fertilization. For maize, he grew fifteen pairs of seedlings, one from a crossed parent and one from a "
            "self-fertilized parent, planted side by side in four pots, and later measured their heights. He asked his "
            "half-cousin Francis Galton for help with the "
            "numbers. <bookmark mark='b'/> Each pair is a block of two: the two plants share the same soil, light and watering. "
            "<bookmark mark='c'/> Here are the fifteen differences, crossed minus selfed, in eighths of an inch. Thirteen are "
            "positive; their mean is twenty point nine. <bookmark mark='d'/> But two pairs strongly favour the self-fertilized "
            "plant. Is the difference real?"
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(A), Create(zl))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.6) for d_ in dots], lag_ratio=0.12), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), *[d_.animate.scale(1.5) for d_, v in zip(dots, z) if v < 0])
        self.clear_scene()

    def fisher_zea(self):
        d = load("blocking")
        rows = [
            cmath(r"\text{paired } t", r"=", rf"\bar d\,/\,(s_d/\sqrt{{15}}) = {d['zea_t']:.2f},\quad p = {d['zea_p']:.4f}", font_size=32),
            cmath(r"\text{under } H_0", r":", r"\text{null model: independent, symmetric paired differences}", font_size=30),
            cmath(r"2^{15}", r"=", r"32{,}768\ \text{sign patterns}", font_size=32),
            cmath(r"\#\{\textstyle\sum \pm|d_i| \ge \sum d_i\}", r"=", rf"{d['zea_count']}\quad\Rightarrow\quad p = 2 \times \tfrac{{{d['zea_count']}}}{{32768}} = {d['zea_p_perm']:.3f}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the analysis that respects the pairs"), why(r"documented randomization or a sign-symmetry assumption"),
                why(r"every way the pairs could have been labelled"), why(r"Fisher, \ \emph{The Design of Experiments} (1935), \ ch.~3")]
        with self.voiceover(
            "<bookmark mark='a'/> The analysis must respect the blocks: compare within each pair. The paired t statistic is two "
            "point one five, with p just under point zero five. <bookmark mark='b'/> Fisher re-analysed Darwin's data in 1935 "
            "as a randomization test within blocks. If crossing did nothing, each pair's two labels could equally well have "
            "been swapped, which flips the sign of that pair's difference. <bookmark mark='c'/> Fifteen pairs give two to the "
            "fifteenth, thirty-two thousand eight hundred and twenty-nine, sign patterns. <bookmark mark='d'/> Eight hundred "
            "and sixty-three of them give a total at least as large as Darwin's, so the two-sided p-value is point zero five "
            "three, close to the t-test's. Part 10 met this test; here it's the analysis that matches a block design. Darwin "
            "hadn't randomized which seedling went where in the pot, so this historical sign-flip calculation assumes independent differences with signs equally likely under the null; assuming merely that placement "
            "didn't matter is insufficient on its own."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def when(self):
        rows = fit_rows(VGroup(
            label(r"block on what you know varies: \ soil strips, \ days, \ batches, \ litters, \ operators, \ patients", font_size=26),
            label(r"each block should be as uniform as possible inside, \ however different from the next", font_size=26, color=BLOCK),
            label(r"blocks cost degrees of freedom: \ $b - 1$ of them leave the error", font_size=26),
            label(r"useless blocks lose a little precision; \ ignored blocks can lose a great deal", font_size=26, color=RES),
            label(r"incomplete blocks (Yates 1936): \ when a block cannot hold every treatment", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0, 0])
        intro = label('Block on known sources of variation', font_size=36)
        with self.voiceover(
            "When should you block? <bookmark mark='a'/> Whenever you know something varies: strips of soil, days of the week, "
            "batches of material, litters of mice, the technician running the assay, the patient in a crossover trial. "
            "<bookmark mark='b'/> A good block is as uniform as possible inside, however different blocks are from each other. "
            "<bookmark mark='c'/> Blocks cost degrees of freedom: b minus one of them leave the error. <bookmark mark='d'/> "
            "So a useless block loses a little precision, but an important source of variation that's ignored can lose a great "
            "deal, as we just saw. <bookmark mark='e'/> And when a block is too small to hold every treatment, a pot with room "
            "for two of four varieties, say, Frank Yates's balanced incomplete block designs of 1936 arrange the treatments so "
            "that every pair meets equally often."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
