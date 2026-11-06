from __future__ import annotations

from videos.stats.stats57.common import *  # noqa: F403


class Outliers(VoiceoverScene):
    def construct(self):
        self.card()
        self.pvalues()
        self.hist()
        self.prds()
        self.bh_worked()
        self.scores()
        self.example()

    def card(self):
        card = chapter_card(7, r"Conformal $p$-values and outlier testing", r"Is this point from the same distribution?", lit=(2023,), part=PART)
        with self.voiceover("Chapter seven. Conformal p-values and outlier testing: is this point from the same distribution?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pvalues(self):
        rows = [
            cmath(r"\text{inliers}", r":", r"Z_1, \dots, Z_n \sim P \ \text{(a clean reference set)}", font_size=36),
            cmath(r"\text{a score}", r":", r"s(z) \text{ large for unusual } z, \ \text{trained on separate inliers}", font_size=34),
            cmath(r"p_j", r"=", r"\frac{1 + \#\{i: s(Z_i) \ge s(Z_{n+j})\}}{n + 1}", font_size=38),
            cmath(r"\text{if } Z_{n+j} \sim P", r":", r"P(p_j \le t) \le t: \ \text{marginally valid}", font_size=36),
        ]
        rows[3][-1].set_color(COVC)
        whys = [why(r"novelty detection"), why(r"one-class model, \ distance"), why(r"its rank among the inliers"), why(r"the quantile lemma again")]
        with self.voiceover(
            "<bookmark mark='a'/> Outlier detection turns the lemma into a test. There is a clean reference set of inliers. "
            "<bookmark mark='b'/> A score, trained on separate inliers, is large for unusual points: a distance from the bulk, "
            "or a one-class classifier's output. <bookmark mark='c'/> A test point's conformal p-value is one plus the number of "
            "reference points scoring at least as high, over n plus one. <bookmark mark='d'/> If the test point really is an "
            "inlier, the p-value is valid, by the quantile lemma."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hist(self):
        d = load("pvals")
        pin, pout = np.asarray(d["inlier"]), np.asarray(d["outlier"])
        edges = np.linspace(0, 1, 11)
        A = axes([0, 1], [0, 0.3], x_length=5.2, y_length=3.6, xlabel=r"conformal $p$-value", ylabel=r"fraction, \ benign test biopsies",
                 xticks=[0, 0.5, 1], yticks=[0, 0.1, 0.2, 0.3], center=[-3.4, 0.5, 0])
        B = axes([0, 1], [0, 1.0], x_length=5.2, y_length=3.6, xlabel=r"conformal $p$-value", ylabel=r"fraction, \ malignant test biopsies",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1.0], center=[3.4, 0.5, 0])
        hin = hist_bars(A.ax, edges, np.histogram(pin, edges)[0] / len(pin), color=COVC, opacity=0.7)
        hout = hist_bars(B.ax, edges, np.histogram(pout, edges)[0] / len(pout), color=MISSC, opacity=0.7)
        flat = DashedLine(A.ax.c2p(0, 0.1), A.ax.c2p(1, 0.1), color=GREY_B, stroke_width=2)
        small = np.mean(pout <= 0.02)
        foot = fit_rows(VGroup(
            label(rf"left: \ {len(pin):,} benign tests, \ flat as promised; \ right: \ {len(pout):,} malignant, \ {100 * small:.0f}\% at $p \le 0.02$", font_size=24, color=GREY_A),
            label(r"20 random splits, \ pooled: \ 150 benign fit the score, \ 157 are the reference set", font_size=22, color=CALC),
        ), 12.4, 0.2, [0, -2.9, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> What the p-values look like, pooled over twenty random splits of the Wisconsin biopsies. <bookmark mark='b'/> "
            f"For the {len(pin):,} benign test biopsies, the inliers, the histogram is flat, as the theory promises: each tenth "
            f"of the unit interval holds about a tenth of them. <bookmark mark='c'/> For the {len(pout):,} malignant ones, the outliers, "
            f"{100 * small:.0f} percent sit at p-values of two hundredths or less, near the smallest value a reference set of a "
            f"hundred and fifty-seven allows, one in a hundred and fifty-eight. <bookmark mark='d'/> Flat for the null, piled at zero for the alternative: the picture every "
            f"multiple-testing method of Part thirty-three wants."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(museum_tag(r"Wolberg, \ Street \& Mangasarian (1995)")))
            vo.wait_until("a")
            self.play(FadeIn(foot[1]))
            vo.wait_until("b")
            self.play(FadeIn(hin, lag_ratio=0.1), Create(flat), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(hout, lag_ratio=0.1), FadeIn(foot[0]), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(hout[0], color=MISSC))
        self.clear_scene()

    def prds(self):
        rows = [
            cmath(r"\text{many test points}", r":", r"\text{the } p_j \text{ share the reference set: \ dependent}", font_size=34),
            cmath(r"\text{Bates et al. (2023)}", r":", r"\text{the inliers' } p\text{-values are PRDS}", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\text{BH on } p_1, \dots, p_m \text{ controls the FDR}", font_size=36),
            cmath(r"\text{and}", r":", r"\text{calibration-conditional guarantees, \ with a slightly stricter level}", font_size=32),
        ]
        rows[2][-1].set_color(COVC)
        whys = [why(r"Part 56's issue"), why(r"Bates, \ Cand\`es, \ Lei, \ Romano \& Sesia"), why(r"Benjamini \& Yekutieli (2001)"), why(r"given the reference set")]
        with self.voiceover(
            "<bookmark mark='a'/> With many test points, the p-values share one reference set and are dependent. <bookmark "
            "mark='b'/> Stephen Bates, Candès, Lihua Lei, Yaniv Romano and Matteo Sesia proved that the inliers' p-values are "
            "positively dependent in the required sense. <bookmark mark='c'/> So Benjamini–Hochberg on them controls the false "
            "discovery rate: the fraction of flagged points that are really inliers. <bookmark mark='d'/> They also gave "
            "guarantees conditional on the reference set, at a slightly stricter level, which is the practitioner's real "
            "situation: one reference set, many uses."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def bh_worked(self):
        rows = [
            cmath(r"\text{smallest possible } p", r"=", r"1/(n + 1)", font_size=38),
            cmath(r"\text{BH rejects } k", r":", r"\text{needs } p_{(k)} \le qk/m", font_size=38),
            cmath(r"\Rightarrow", r"\;", r"n + 1 \ge m/(qk) \text{ to find } k \text{ outliers at all}", font_size=36),
            cmath(r"m = 10{,}000, \ k = 10, \ q = 0.1", r":", r"n \ge 10{,}000 \text{ reference points}", font_size=34),
        ]
        rows[2][-1].set_color(WEIGHTC)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"the resolution"), why(r"Part 33"), why(r"a design rule"), why(r"rare outliers, \ big screens")]
        with self.voiceover(
            "<bookmark mark='a'/> A practical limit. The smallest conformal p-value is one over n plus one. <bookmark "
            "mark='b'/> Benjamini–Hochberg rejects k hypotheses only if the k-th smallest p-value is at most q k over "
            "m. <bookmark mark='c'/> So to find k outliers at all, the reference set needs at least m over q k points. "
            "<bookmark mark='d'/> Screening ten thousand points for ten outliers at q a tenth needs ten thousand "
            "reference inliers. Our biopsies make the point: with a hundred reference points and a hundred and "
            "forty-seven tests, at least fifteen outliers had to reach the smallest p-value, and some splits rejected "
            "nothing; with a hundred and fifty-seven reference points and ninety tests, six suffice."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def scores(self):
        rows = [
            cmath(r"\text{scores}", r":", r"\text{distances, \ forests, \ autoencoders, \ SVMs}", font_size=36),
            cmath(r"\text{validity}", r":", r"\text{any score, \ trained on separate inliers}", font_size=34),
            cmath(r"\text{power}", r":", r"\text{depends on how well the score separates the outliers}", font_size=34),
            cmath(r"\text{never}", r":", r"\text{train the score on the reference set itself}", font_size=34),
        ]
        rows[1][-1].set_color(COVC)
        rows[3][-1].set_color(MISSC)
        whys = [why(r"any novelty detector"), why(r"exchangeability again"), why(r"the model's job"), why(r"it breaks the exchangeability")]
        with self.voiceover(
            "<bookmark mark='a'/> The score can be any novelty detector: a distance from the bulk, an isolation "
            "forest, the reconstruction error of an autoencoder, or a one-class support vector machine. <bookmark "
            "mark='b'/> Validity holds for any of them, as long as it is trained on inliers separate from the "
            "reference set. <bookmark mark='c'/> Power depends on how well the score separates the outliers. <bookmark "
            "mark='d'/> What must never happen is training the score on the reference set itself, because the "
            "reference scores would then be systematically smaller than a new inlier's."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def example(self):
        d = load("outliers")
        rows = fit_rows(VGroup(
            label(r"the Wisconsin biopsies: \ treat benign as inliers, \ malignant as outliers", font_size=28, color=GREY_A),
            label(r"score: \ standardized distance from 150 benign biopsies; \ 157 more as the reference set", font_size=26, color=CALC),
            label(rf"test: \ the other {d['n_test_in']} benign and 40 malignant; \ BH at $q = 0.1$", font_size=26, color=GREY_A),
            label(rf"false discovery rate {100 * d['fdr']:.1f}\%, \ power {100 * d['power']:.0f}\%, \ over 50 splits", font_size=28, color=COVC),
            label(r"no model of what malignant looks like was used", font_size=26, color=TESTPT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The Wisconsin biopsies again, now as outlier detection: benign tissue is the reference "
            f"population, malignant the outliers. <bookmark mark='b'/> The score is the distance from the centre of a hundred and "
            f"fifty benign biopsies, each feature in their standardized units, with a hundred and fifty-seven more as the "
            f"reference set. <bookmark mark='c'/> The test set holds the other "
            f"{d['n_test_in']} benign biopsies and forty malignant ones, and Benjamini–Hochberg runs at a tenth. <bookmark "
            f"mark='d'/> Over fifty splits the false discovery rate is {100 * d['fdr']:.1f} percent and the power "
            f"{100 * d['power']:.0f} percent. <bookmark mark='e'/> No model of what malignant tissue looks like was used: only "
            f"what benign tissue looks like."
        ) as vo:
            self.play(FadeIn(museum_tag(r"Wolberg, \ Street \& Mangasarian (1995)")))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
