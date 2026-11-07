from __future__ import annotations

import numpy as np

from videos.stats.stats33.common import *  # noqa: F403


class Problem(VoiceoverScene):
    def construct(self):
        self.card()
        self.study()
        self.sea()
        self.uncorrected()
        self.histogram()
        self.uniform()
        self.table()
        self.rates()

    def card(self):
        card = chapter_card(1, r"The problem", r"Five thousand genes, \ one study", lit=(1995,), part=PART)
        with self.voiceover("Chapter one. The problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def study(self):
        d = load("genes")
        rows = fit_rows(VGroup(
            label(r"the World's gene-expression study", font_size=26),
            label(r"25 patients, \ 25 healthy controls, \ 5{,}000 genes each", font_size=26, color=BHC),
            label(r"for each gene: \ a two-sample $t$-test, \ patient vs control", font_size=26),
            label(rf"the truth, \ known only to us: \ {d['m1']} genes really differ", font_size=26, color=TRUEC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World has a gene-expression study. <bookmark mark='b'/> Twenty-five patients and "
            "twenty-five healthy controls, with the expression of five thousand genes measured in each. Genes come in "
            "pathways of twenty-five whose expression is correlated. <bookmark mark='c'/> For each gene, a two-sample "
            "t-test asks whether patients and controls differ. <bookmark mark='d'/> Because this is the World, we know the "
            "truth: two hundred and fifty genes, in ten pathways, really differ; the other four thousand seven hundred and "
            "fifty do not."
        ) as vo:
            self.add(genes_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sea(self):
        d = load("genes")
        p = np.asarray(d["p_all"])
        g = PValueSea.grid(p, cols=100, cell=0.075, center=[-1.6, 0.2, 0])
        rows = fit_rows(VGroup(
            label(r"5{,}000 $p$-values, \ one cell per gene", font_size=22),
            label(r"brighter for smaller $p$", font_size=22, color=SIGC),
            label(r"real effects come in pathways of 25", font_size=22, color=TRUEC),
            label(r"but noise lights up cells too", font_size=22, color=FALSEC),
        ), 3.6, 0.42, [5.1, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are all five thousand p-values, one cell per gene, in pathway order. "
            "<bookmark mark='b'/> Brighter cells have smaller p-values. <bookmark mark='c'/> The real effects show up as "
            "bright runs, whole pathways at a time. <bookmark mark='d'/> But scattered bright cells appear everywhere else "
            "too: noise, answering some of our five thousand questions."
        ) as vo:
            self.add(genes_tag())
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in g], lag_ratio=0.0005), FadeIn(rows[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def uncorrected(self):
        d = load("genes")
        r = d["res"]["uncorrected"]
        rows = fit_rows(VGroup(
            label(r"reject every gene with $p < 0.05$", font_size=28),
            label(rf"{r['R']} discoveries", font_size=28, color=SIGC),
            label(rf"{r['S']} real \ \ +\ \ {r['V']} false", font_size=28, color=FALSEC),
            label(r"about half the list is noise: \ $0.05 \times 4{,}750 \approx 238$ expected", font_size=28, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The naive analysis declares every gene with p below five percent a discovery. "
            "<bookmark mark='b'/> That gives four hundred and thirty discoveries. <bookmark mark='c'/> Two hundred "
            "and sixteen are real, and two hundred and fourteen are false. <bookmark mark='d'/> Half this particular "
            "list is noise. Across repeated studies, five percent of four thousand seven hundred and fifty null genes"
            " is about two hundred and thirty-eight."
        ) as vo:
            self.add(genes_tag())
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def histogram(self):
        d = load("genes")
        h = np.asarray(d["hist"], float)
        edges = np.linspace(0, 1, 21)
        dens = h / (h.sum() * 0.05)
        A = axes([0, 1], [0, 5.2], x_length=7.4, y_length=4.4, xlabel=r"$p$-value", ylabel=r"density",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 1, 2, 4], center=[-2.0, 0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, edges, dens, color=BHC, opacity=0.7)
        flat = DashedLine(ax.c2p(0, d["pi0"]), ax.c2p(1, d["pi0"]), color=NULLC, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"null $p$-values are uniform", font_size=22),
            label(r"real effects pile up near 0", font_size=22, color=TRUEC),
            label(rf"the flat floor's height: \ $\pi_0 \approx {d['pi0']:.3f}$", font_size=22, color=NULLC),
            label(r"requires few alternative $p$-values near 1", font_size=22, color=GREY_A),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The histogram of all five thousand p-values tells the story. Under a true null, a "
            "p-value is uniformly distributed, so null genes fill a flat floor. <bookmark mark='b'/> Real effects "
            "pile up near zero. <bookmark mark='c'/> If alternatives rarely produce large p-values, the upper "
            "histogram estimates the null share, about point nine six here, against a truth of point nine five. "
            "<bookmark mark='d'/> Chapter four uses exactly this idea."
        ) as vo:
            self.add(genes_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(bars[0], color=TRUEC), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(flat), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def table(self):
        hdr = [r"", r"\textbf{not rejected}", r"\textbf{rejected}", r"\textbf{total}"]
        body = [[r"true null", r"$U$", r"$V$ \ (false discoveries)", r"$m_0$"],
                [r"false null", r"$T$", r"$S$ \ (true discoveries)", r"$m_1$"],
                [r"total", r"$m - R$", r"$R$", r"$m$"]]
        tb = table_rows([hdr] + body, font_size=28, col_buff=1.0, row_buff=0.4, colors=[GREY_A, None, None, GREY_A])
        tb[1][2].set_color(FALSEC)
        tb[2][2].set_color(TRUEC)
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"only $R$ is observed; \ $V$ and $S$ are hidden", font_size=24),
            label(r"genes: \ $R = 430$, \ $V = 214$, \ $S = 216$", font_size=24, color=SIGC),
        ), 12.0, 0.25, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The bookkeeping, in Benjamini and Hochberg's notation. Of m hypotheses, m zero are true "
            "nulls and m one are not. Of the R we reject, V are false discoveries and S are true ones. "
            "<bookmark mark='b'/> Only R is ever observed. V and S are hidden, and every error rate in this part is a "
            "promise about them. <bookmark mark='c'/> For the genes: R four hundred and thirty, V two hundred and "
            "fourteen, S two hundred and sixteen."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def rates(self):
        rows = [
            cmath(r"\text{per comparison}", r":", r"E(V)/m \le \alpha", font_size=32),
            cmath(r"\text{FWER}", r"=", r"P(V \ge 1)", font_size=34),
            cmath(r"\text{FDR}", r"=", r"E\big(V / \max(R, 1)\big)", font_size=34),
            cmath(r"\text{FDP}", r"=", r"V / \max(R, 1): \ \text{random; \ FDR is its mean}", font_size=30),
        ]
        rows[2][-1].set_color(BHC)
        whys = [why(r"what uncorrected tests control"), why(r"any false positive at all"),
                why(r"the share of false positives"), why(r"chapter six")]
        with self.voiceover(
            "<bookmark mark='a'/> Three promises one can make. Testing each hypothesis at level alpha controls the expected "
            "share of all m hypotheses that are falsely rejected, which says almost nothing about the list. "
            "<bookmark mark='b'/> The family-wise error rate is the probability of even one false discovery. "
            "<bookmark mark='c'/> The false discovery rate is the expected proportion of discoveries that are false. "
            "<bookmark mark='d'/> That proportion itself, the FDP, is random; the FDR is only its average, a distinction "
            "chapter six takes seriously."
        ) as vo:
            intro=label('Error rates differ in their denominator and averaging',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def uniform(self):
        rows = [
            cmath(r"P(p \le u)", r"=", r"P(1-F_0(T) \le u) = u", font_size=32),
            cmath(r"\text{so}", r":", r"p \sim U(0, 1) \ \text{under } H_0", font_size=32),
            cmath(r"\text{alternative}", r":", r"\text{well-powered signals often yield small }p", font_size=30),
            cmath(r"\text{discrete tests}", r":", r"p \text{ is super-uniform: \ } P(p \le u) \le u", font_size=30),
        ]
        rows[1][-1].set_color(BHC)
        whys = [why(r"the probability integral transform"), why(r"for a continuous test statistic"), why(r"the spike near 0"), why(r"conservative, \ never anti-conservative")]
        with self.voiceover(
            "<bookmark mark='a'/> Why is a null p-value uniform? For a one-sided test, the p-value is one minus the "
            "null distribution function at the observed statistic, and the chance that this is at most u is exactly "
            "u, the probability integral transform of Part 7. <bookmark mark='b'/> So under the null, p-values are "
            "uniform on zero to one. <bookmark mark='c'/> For these well-powered alternatives, small p-values are "
            "more common. A decreasing density is not a universal property of alternatives. <bookmark mark='d'/> For "
            "discrete tests, like Fisher's exact test, the p-value is super-uniform: the chance it is below u is at "
            "most u, This supports p-value error bounds when each procedure’s other assumptions, including dependence"
            " conditions, hold."
        ) as vo:
            intro=label('Valid null p-values need a specified sampling distribution',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
