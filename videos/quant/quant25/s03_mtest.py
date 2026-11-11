from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.quant import *  # noqa: F403
from videos.quant.quant25.common import BAD, FALSE, GOOD, HURDLE, NOISE, PART, TRUE, ask, fit_right, illustration, load


class MTest(VoiceoverScene):
    def construct(self):
        m = load("mtest")
        self.card()
        self.fwer()
        self.holm()
        self.fdr()
        self.table()
        self.byhand()
        self.bhplot(m)
        self.results(m)
        self.bootstrap()
        self.qchoice()
        self.reading()

    def card(self):
        c = chapter_card(2, r"Multiple testing: FWER and FDR", r"What error rate should a researcher control?",
                         lit=(1995,), part=PART)
        with self.voiceover("Chapter two. Three corrections for many tests, and what each one promises."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fwer(self):
        rows = [cmath(r"\text{FWER}", r"=", r"\Pr(\text{at least one false discovery})", font_size=40,
                      colors={r"\text{FWER}": BAD}),
                cmath('\\Pr\\Big(\\bigcup_{i\\in\\mathcal H_0} \\{p_i \\le \\tfrac{\\alpha}{m}\\}\\Big)', r"\le", '\\textstyle\\sum_{i\\in\\mathcal H_0} \\frac{\\alpha}{m} \\le \\alpha', font_size=38),
                cmath(r"m = 212", r"\Rightarrow", r"p \le 0.000236,\ \ |t| \ge 3.68", font_size=38,
                      colors={r"m = 212": HURDLE})]
        whys = [why('the familywise error rate: the probability of at least one false rejection in a fixed family'),
                why(r"Bonferroni: test each hypothesis at $\alpha/m$. By the union bound the chance of any false rejection "
                    r"is at most $\alpha$, whatever the dependence between tests"),
                why('for the zoo, a two-sided 5\\% test needs $|t| \\ge 3.68$: under valid normal null calibration; true factors with a modest $t$ are missed')]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "The familywise error rate is the probability of at least one false rejection in a fixed family. <bookmark mark='a'/> Bonferroni tests each hypothesis at alpha divided by the family size. Valid marginal null p-values and the union bound give control under arbitrary dependence. <bookmark mark='b'/> For two hundred and twelve hypotheses the five-percent two-sided normal critical value is about three point seven. The return-based p-values shown later use naive iid mean t statistics and normal tails, so this algebra does not certify their empirical error rate under serial dependence or publication selection."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def holm(self):
        rows = [cmath(r"p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}", r":", r"\text{reject } H_{(k)} \text{ while } p_{(k)} \le "
                      r"\frac{\alpha}{m - k + 1}", font_size=36, colors={r"p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}": HURDLE})]
        whys = [why(r"Holm (1979): sort the $p$-values; test the smallest at $\alpha/m$, the next at $\alpha/(m-1)$, and "
                    r"so on, stopping at the first failure. The same guarantee as Bonferroni, never fewer discoveries")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Holm's step-down procedure retains family-error control. Sort the p-values; compare the smallest with alpha over m, then alpha over m minus one, stopping at the first failure. For a fixed family and valid marginal p-values it works under arbitrary dependence and rejects every hypothesis that ordinary Bonferroni rejects, possibly more. Neither procedure repairs invalid p-values or an undisclosed search."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def fdr(self):
        rows = [cmath(r"\text{FDR}", r"=", r"\mathbb{E}\Big[\frac{\text{false discoveries}}{\max(\text{discoveries}, 1)}\Big]",
                      font_size=40, colors={r"\text{FDR}": BAD}),
                cmath(r"k^*", r"=", r"\max\Big\{k:\ p_{(k)} \le \frac{k}{m}\,q\Big\},\ \ \text{reject } H_{(1)}, \dots, H_{(k^*)}",
                      font_size=36, colors={r"k^*": GOOD})]
        whys = [why(r"the false discovery rate: the expected share of discoveries that are false. A looser goal, suited to "
                    r"a field that will act on many findings and can tolerate a few duds"),
                why('Benjamini and Hochberg (1995): compare the sorted $p$-values with a line rising from $q/m$ to $q$; reject everything up to the last crossing. Controls FDR at $q$ for valid null p-values under independence or the specific PRDS condition; arbitrary positive correlation alone is insufficient')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Benjamini and Hochberg control the false discovery rate: the expected false share, with the share defined as zero when there are no discoveries. This is an expectation over repeated samples, not a bound on every realised false share or on a portfolio's loss. <bookmark mark='a'/> Sort the p-values and reject through the last crossing of the rising line. The guarantee needs valid null p-values and independence or the specific positive-regression-dependence condition called PRDS. Arbitrary correlation, publication selection or invalid time-series p-values do not automatically satisfy it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def table(self):
        hx = [-3.0, 0.2, 2.8, 5.0]
        tab = VGroup(VGroup(label(r"", font_size=18).move_to([hx[0], 1.8, 0]),
                            label(r"declared significant", font_size=18, color=GREY_A).move_to([hx[1], 1.8, 0]),
                            label(r"not declared", font_size=18, color=GREY_A).move_to([hx[2], 1.8, 0]),
                            label(r"total", font_size=18, color=GREY_A).move_to([hx[3], 1.8, 0])))
        for i, (nm, a, b, c, col) in enumerate(((r"no true premium", r"V", r"U", r"m_0", BAD),
                                                (r"true premium", r"S", r"T", r"m_1", GOOD),
                                                (r"total", r"R", r"m - R", r"m", WHITE))):
            y = 1.1 - 0.7 * i
            tab.add(VGroup(label(nm, font_size=19, color=col).move_to([hx[0], y, 0]),
                           MathTex(a, font_size=32, color=BAD if a == "V" else WHITE).move_to([hx[1], y, 0]),
                           MathTex(b, font_size=32).move_to([hx[2], y, 0]), MathTex(c, font_size=32).move_to([hx[3], y, 0])))
        eqs = VGroup(MathTex(r"\text{FWER} = \Pr(V \ge 1)", font_size=32, color=BAD),
                     MathTex(r"\text{FDR} = \mathbb{E}[V / \max(R, 1)]", font_size=32, color=GOOD)).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "The two error rates, in one table. Of m tests, some have no true premium and some do. We declare R of "
            "them significant; V of those are false discoveries. <bookmark mark='a'/> The familywise error rate is the "
            "chance that V is at least one. The false discovery rate is the expected value of V over R: the share of "
            "what we declare that is wrong. With hundreds of tests and many true effects, the first is almost "
            "impossible to keep small without discarding nearly everything; the second is not."
        ) as vo:
            self.play(FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(eqs))
        self.wait(0.4)
        self.clear_scene()

    def byhand(self):
        ps = [0.001, 0.008, 0.012, 0.03, 0.2]
        hx = [-4.2, -2.6, -0.6, 1.6, 4.0]
        heads = [r"rank $k$", r"$p_{(k)}$", r"Bonferroni: $0.05/5$", r"Holm: $0.05/(6-k)$", r"BH: $0.05\,k/5$"]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, 2.2, 0]) for h_, x in zip(heads, hx)]))
        holm_ok = True
        for k, p in enumerate(ps, 1):
            y = 1.6 - 0.55 * (k - 1)
            b = p <= 0.01
            h = holm_ok and p <= 0.05 / (6 - k)
            holm_ok = h
            bh = k <= 4
            tab.add(VGroup(MathTex(str(k), font_size=24).move_to([hx[0], y, 0]), MathTex(f"{p}", font_size=24).move_to([hx[1], y, 0]),
                           MathTex(r"\checkmark" if b else r"\times", font_size=24, color=GOOD if b else BAD).move_to([hx[2], y, 0]),
                           MathTex(rf"{0.05 / (6 - k):.4f}\ " + (r"\checkmark" if h else r"\times"), font_size=22,
                                   color=GOOD if h else BAD).move_to([hx[3], y, 0]),
                           MathTex(rf"{0.01 * k:.2f}\ " + (r"\checkmark" if bh else r"\times"), font_size=22,
                                   color=GOOD if bh else BAD).move_to([hx[4], y, 0])))
        foot = MathTex(r"\text{rejections}:\ \ \text{Bonferroni } 2,\quad \text{Holm } 3,\quad \text{BH } 4", font_size=30,
                       color=HURDLE).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "By hand, on five p-values. <bookmark mark='a'/> Bonferroni tests each at one percent: two pass. "
            "<bookmark mark='b'/> Holm tests the smallest at one percent, the next at one and a quarter, the third at "
            "one and two thirds, the fourth at two and a half: three pass, and the fourth fails at zero point zero "
            "three. <bookmark mark='c'/> Benjamini and Hochberg compare the k-th smallest with k percent: the fourth, "
            "at three percent, is under its four percent line, so four are rejected. The looser the goal, the more "
            "discoveries, and the more of them may be false."
        ) as vo:
            self.play(FadeIn(tab[0]), *[FadeIn(r_[:2]) for r_ in tab[1:]])
            vo.wait_until("a")
            self.play(*[FadeIn(r_[2]) for r_ in tab[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r_[3]) for r_ in tab[1:]])
            vo.wait_until("c")
            self.play(*[FadeIn(r_[4]) for r_ in tab[1:]], FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def bhplot(self, m):
        tp = np.asarray(m["t_post"])
        p = np.sort(stats.norm.sf(tp))
        M = len(p)
        K = 80
        g = axes([0, K + 1], [0, 0.12], x_length=8.0, y_length=4.4, xlabel=r"rank $k$ (smallest $p$ first), first 80",
                 ylabel=r"$p$-value after publication", xticks=[1, 20, 40, 60, 80], yticks=[0, 0.04, 0.08, 0.12],
                 font_size=13).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        nb = m["post"]["bh"]
        dots = VGroup(*[Dot(ax.c2p(i + 1, v), radius=0.045, color=TRUE if i < nb else NOISE)
                        for i, v in enumerate(p[:K])])
        line = Line(ax.c2p(0, 0), ax.c2p(K, 0.05 * K / M), color=GOOD, stroke_width=2.5)
        bonf = DashedLine(ax.c2p(0, 0.05 / M), ax.c2p(K, 0.05 / M), color=HURDLE, stroke_width=2)
        side = VGroup(
            legend([(GOOD, r"Benjamini--Hochberg line, $q = 5\%$"), (HURDLE, r"Bonferroni, $0.05/m$")], font_size=15),
            MathTex(rf"\text{{BH discoveries}}:\ {nb}\ \text{{of}}\ {M}", font_size=24, color=TRUE),
            wrapped_label(r"each predictor's one-sided $p$-value from its returns after publication, to 2020 (the sign its "
                          r"paper claimed). Bonferroni's line is nearly on the axis", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The chart retains the smallest eighty post-publication p-values, with their full observed range. They use next-calendar-year returns through 2020 and the published direction. The selected published collection and modern data reconstruction remain. <bookmark mark='a'/> Under these approximate normal p-values the BH last crossing is the twenty-fourth, and Bonferroni admits seven. The normal calibration and dependence requirements are not certified by placing the observations after a publication date. The first-eighty view is labelled; all two hundred and eight p-values enter the saved procedure."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02), Create(line), Create(bonf), run_time=2.5)
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def results(self, m):
        hx = [-4.4, -1.6, 0.6, 2.6, 4.6]
        heads = [r"", r"raw, 5\%", r"Bonferroni", r"Holm", r"BH, $q$ = 5\%"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.0, 0]) for h_, x in zip(heads, hx)]))
        for i, (k, nm) in enumerate((("in", r"in the original sample"), ("post", r"after publication"))):
            d = m[k]
            y = 1.3 - 0.75 * i
            tab.add(VGroup(label(rf"{nm} ({d['n']})", font_size=19).move_to([hx[0], y, 0]),
                           *[MathTex(str(d[c]), font_size=30, color=TRUE if c != "raw" else WHITE).move_to([hx[j + 1], y, 0])
                             for j, c in enumerate(("raw", "bonferroni", "holm", "bh"))]))
        foot = wrapped_label('in sample, almost everything passes the looser tests, as it must: the predictors were chosen because they passed. After publication, a selected modern reconstruction, about a quarter are significant at 5\\% one by one, an eighth survive the false discovery rate, and only seven survive Bonferroni', 12.0, 17, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The counts are descriptive. <bookmark mark='a'/> In original paper windows, one hundred and eighty-five of two hundred and twelve pass nominal tests, and BH keeps one hundred and eighty-four. These observations inherit discovery and publication selection. <bookmark mark='b'/> In the next-year post-publication windows through 2020, the saved one-sided procedure gives fifty-nine raw crossings, twenty-four BH rejections and seven Bonferroni rejections among two hundred and eight. These are not certified fresh discoveries under arbitrary return dependence or modern selection. Shorter samples, changing effects and power also matter; nonrejection does not establish that a predictor is false."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def bootstrap(self):
        rows = [cmath(r"\tilde r^{(b)}_{it}", r"=", r"r_{i,t^{(b)}} - \bar r_i", font_size=40, colors={r"\tilde r^{(b)}_{it}": NOISE}),
                cmath(r"c_{0.95}", r"=", r"\text{95th percentile of } \max_i |t_i^{(b)}|\ \text{over } b", font_size=38,
                      colors={r"c_{0.95}": HURDLE})]
        whys = [why(r"White's (2000) reality check: demean every strategy so all nulls are true, then resample whole months "
                    r"(the same rows for every strategy), keeping their correlation"),
                why('valid max-statistic resampling requires suitable dependence, studentisation and regularity; Bonferroni itself permits arbitrary dependence. No market bootstrap executed here')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A dependence-aware bootstrap requires its own design and assumptions. Common-time resampling preserves contemporaneous cross-strategy dependence; block or other time-series schemes may be needed for serial dependence. Recentering can impose a null for the chosen statistic. <bookmark mark='a'/> Reality-check and step-down methods use maxima, appropriate studentisation and valid resampling approximations. Their finite-sample guarantee is not automatic, and the resulting critical value need not always be below Bonferroni's. This chapter describes those methods; it does not execute a corrected market bootstrap or substitute a new inference result."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def qchoice(self):
        rows = [cmath('q=5\\%', r"\Rightarrow", '\\mathbb E[V/\\max(R,1)]\\le0.05', font_size=42, colors={'q=5\\%': GOOD}),
                cmath(r"q = 20\%", r"\Rightarrow", '\\text{expected ratio target; no realised loss bound}', font_size=38)]
        whys = [why('FDR bounds an expected ratio across repetitions; multiplying the realised discovery count by q is not a conditional error-count guarantee'),
                why('q changes a statistical error objective; losses still depend on common exposures, tails, costs, funding and portfolio constraints')]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Choose q before viewing discoveries, for a declared statistical objective. <bookmark mark='a'/> Under valid assumptions, five-percent FDR bounds the expected false-rejection fraction across repetitions. Multiplying a realised twenty-four discoveries by point zero five is not a conditional expected error count guaranteed by that theorem. <bookmark mark='b'/> A looser q changes the error objective and discoveries, but no q alone controls economic losses, common exposures, tail events or funding risk. A diversified-looking list can still share the same risks. Statistical discovery and portfolio construction require distinct decisions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"which error?", 'choose an explicit scientific error objective; FWER applies to families and FDR does not certify portfolio safety', width=12.0, font_size=20),
            desk_question(r"dependence", 'joint-time resampling may model dependence under suitable assumptions; valid calibration and a lower hurdle are not automatic',
                          width=12.0, font_size=20),
            desk_question(r"the missing denominator", 'record the declared search family and variants; a local ledger cannot enumerate every inherited unpublished search', width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Three habits. <bookmark mark='a'/> Choose a stated error objective for a fixed family: FWER or FDR answers different statistical questions, and neither directly controls economic loss. <bookmark mark='b'/> Dependence-aware resampling needs valid time-series design and regularity; it is not automatically safer or less conservative. <bookmark mark='c'/> Retain the search family, variants and inherited selection. The local ledger helps document declared choices but is not a complete count of all unpublished research."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"you have 100 candidate signals and will trade the ten best equally. Which error rate should you control, "
                r"and at what level?")
        with self.voiceover("You have a hundred candidate signals and will trade the ten best, equally weighted. Which "
                            "error rate should you control, and at what level?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
