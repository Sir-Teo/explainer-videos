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
                cmath(r"\Pr\Big(\bigcup_i \{p_i \le \tfrac{\alpha}{m}\}\Big)", r"\le", r"\textstyle\sum_i \frac{\alpha}{m} = "
                      r"\alpha", font_size=38),
                cmath(r"m = 212", r"\Rightarrow", r"p \le 0.000236,\ \ |t| \ge 3.68", font_size=38,
                      colors={r"m = 212": HURDLE})]
        whys = [why(r"the familywise error rate: the probability that any of the $m$ discoveries is false"),
                why(r"Bonferroni: test each hypothesis at $\alpha/m$. By the union bound the chance of any false rejection "
                    r"is at most $\alpha$, whatever the dependence between tests"),
                why(r"for the zoo, a two-sided 5\% test needs $|t| \ge 3.68$: safe, and so strict that true factors with a "
                    r"modest $t$ are missed")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "The strictest goal: control the familywise error rate, the probability that even one of your "
            "discoveries is false. <bookmark mark='a'/> Carlo Bonferroni's answer is to test each of the m hypotheses "
            "at alpha over m. The chance that any one of them is falsely rejected is at most the sum of their chances, "
            "which is alpha, whatever the dependence between the tests. <bookmark mark='b'/> For two hundred and "
            "twelve predictors that means a p-value below about two in ten thousand, a t-statistic of three point "
            "seven. Safe, and so strict that genuine factors with modest t-statistics are thrown away."
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
            "Sture Holm improved it for free. Sort the p-values from smallest to largest. Test the smallest at alpha "
            "over m; if it passes, test the next at alpha over m minus one, and so on, stopping at the first one that "
            "fails. Each rejection removes one hypothesis from the family, so the next bar can be a little lower. The "
            "guarantee is the same as Bonferroni's, and it never finds fewer discoveries."
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
                why(r"Benjamini and Hochberg (1995): compare the sorted $p$-values with a line rising from $q/m$ to $q$; "
                    r"reject everything up to the last crossing. Controls the FDR at $q$ for independent or positively "
                    r"dependent tests")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Yoav Benjamini and Yosef Hochberg changed the question. Instead of the chance of any false discovery, "
            "control the false discovery rate: the expected share of your discoveries that are false. A field that "
            "acts on many findings can live with a few duds, as long as they are a small share. <bookmark mark='a'/> "
            "Their procedure: sort the p-values, draw a line rising from q over m to q, and reject every hypothesis up "
            "to the last one below the line."
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
        g = axes([0, K + 1], [0, 0.06], x_length=8.0, y_length=4.4, xlabel=r"rank $k$ (smallest $p$ first), first 80",
                 ylabel=r"$p$-value after publication", xticks=[1, 20, 40, 60, 80], yticks=[0, 0.02, 0.04, 0.06],
                 font_size=13).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        nb = m["post"]["bh"]
        dots = VGroup(*[Dot(ax.c2p(i + 1, min(v, 0.06)), radius=0.045, color=TRUE if i < nb else NOISE)
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
            "Here is the procedure on the zoo, with a test that is honest: each predictor's returns after its paper was "
            "published, through 2020, tested in the direction the paper claimed. <bookmark mark='a'/> The smallest "
            "eighty p-values, sorted. The Benjamini-Hochberg line rises from the origin; the last crossing is at "
            f"{nb}. Bonferroni's bar is almost flat on the axis, and only a handful get under it."
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
        foot = wrapped_label(r"in sample, almost everything passes the looser tests, as it must: the predictors were "
                             r"chosen because they passed. After publication, a fair test, about a quarter are significant "
                             r"at 5\% one by one, an eighth survive the false discovery rate, and only seven survive "
                             r"Bonferroni", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The counts. <bookmark mark='a'/> In the original samples, a hundred and eighty-five of two hundred and "
            "twelve are significant one by one, and the false-discovery procedure keeps a hundred and eighty-four. "
            "That is circular: these samples are where the predictors were found. <bookmark mark='b'/> After "
            "publication, on returns nobody had seen, fifty-nine are significant at five percent one at a time, "
            "twenty-four survive the false discovery rate, and just seven survive Bonferroni. Notice that this is not "
            "the same as saying the rest are false: after publication the samples are shorter and the premia smaller, "
            "so the tests have less power. Multiple testing is about what you can claim, not what is true."
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
                why(r"the hurdle is the 95th percentile of the best resampled $t$: Bonferroni's guarantee, without its "
                    r"assumption that the tests are unrelated. Romano and Wolf (2005) make it step-down, like Holm")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "A better hurdle uses the data's own dependence. Halbert White's reality check subtracts each strategy's "
            "mean, so every null hypothesis is true by construction, and then resamples whole months, the same months "
            "for every strategy, so their correlations are kept. <bookmark mark='a'/> The hurdle is the ninety-fifth "
            "percentile of the best resampled t-statistic. Correlated strategies share their luck, so the hurdle comes "
            "out lower than Bonferroni's, with the same guarantee. Joseph Romano and Michael Wolf made it step-down, "
            "as Holm did for Bonferroni."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def qchoice(self):
        rows = [cmath(r"q = 5\%,\ R = 24", r"\Rightarrow", r"\mathbb{E}[V] \lesssim 1.2", font_size=42, colors={r"q = 5\%,\ R = 24": GOOD}),
                cmath(r"q = 20\%", r"\Rightarrow", r"\text{more discoveries, up to a fifth of them false}", font_size=38)]
        whys = [why(r"the false discovery rate is a promise about the expected share: of the 24 post-publication "
                    r"discoveries, about one is expected to be false"),
                why(r"a looser $q$ admits more candidates and more duds. For a diversified book of many weak signals, a "
                    r"few duds cost little; for a single concentrated bet, they cost everything")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "What does q mean in practice? <bookmark mark='a'/> At five percent, of the twenty-four post-publication "
            "discoveries about one is expected to be false. <bookmark mark='b'/> A looser q, say a fifth, admits more "
            "candidates, and up to a fifth of them may be duds. For a diversified book of many weak signals, a few "
            "duds cost little. For one concentrated bet, a dud costs everything. The right q depends on how the "
            "discoveries will be used."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        cards = VGroup(
            desk_question(r"which error?", r"FWER for a single claim you will stake a reputation on; FDR for a "
                          r"portfolio of many signals, where a few duds dilute rather than ruin", width=12.0, font_size=20),
            desk_question(r"dependence", r"factors are correlated: bootstrap methods (White 2000; Romano and Wolf 2005; "
                          r"Harvey and Liu 2020) resample them jointly and are less conservative than Bonferroni",
                          width=12.0, font_size=20),
            desk_question(r"the missing denominator", r"every method needs $m$, the number of tests. Only the researcher "
                          r"knows it, which is why the House counts its own trials", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Which to use? <bookmark mark='a'/> The familywise rate for a single claim on which you would stake your "
            "reputation; the false discovery rate for a portfolio of many signals, where a few duds dilute rather than "
            "ruin. <bookmark mark='b'/> Factors are correlated, and bootstrap methods, from Halbert White to Joseph "
            "Romano and Michael Wolf and to Harvey and Liu, resample them jointly and are less conservative. "
            "<bookmark mark='c'/> And every method needs the number of tests, which only the researcher knows. That "
            "is why the House counts its own."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
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
