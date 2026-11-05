from __future__ import annotations

import numpy as np

from videos.stats.stats19.common import *  # noqa: F403


class Metrics(VoiceoverScene):
    def construct(self):
        self.card()
        self.confusion()
        self.threshold()
        self.roc()
        self.pr()
        self.calibration()
        self.costs()
        self.lessons()

    def card(self):
        card = chapter_card(8, r"Classification metrics", r"Right for the right reasons", part=PART)
        with self.voiceover("Chapter eight. Classification metrics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def matrix(self, c, center):
        cells = VGroup()
        vals = [[c["tp"], c["fn"]], [c["fp"], c["tn"]]]
        cols = [[HIT, RES], [RES, HIT]]
        for i in range(2):
            for j in range(2):
                sq = Square(1.4, stroke_color=GREY_C, stroke_width=1.5, fill_color=cols[i][j], fill_opacity=0.25)
                sq.move_to(np.asarray(center) + np.array([(j - 0.5) * 1.45, (0.5 - i) * 1.45, 0]))
                cells.add(VGroup(sq, MathTex(f"{vals[i][j]:,}", font_size=30).move_to(sq)))
        rl = VGroup(label(r"voted Blue", font_size=18, color=BLUE).next_to(cells[0], LEFT, buff=0.15),
                    label(r"voted Red", font_size=18, color=RED).next_to(cells[2], LEFT, buff=0.15))
        cl = VGroup(label(r"predicted Blue", font_size=18, color=GREY_A).next_to(cells[0], UP, buff=0.12),
                    label(r"predicted Red", font_size=18, color=GREY_A).next_to(cells[1], UP, buff=0.12))
        return VGroup(cells, rl, cl)

    def confusion(self):
        d = load("metrics")
        c = d["conf"]
        M = self.matrix(c, [-2.8, 0.2, 0])
        rows = fit_rows(VGroup(
            label(r"logistic regression on income and age; \ 2,000 held-out adults", font_size=22),
            MathTex(rf"\text{{accuracy}} = {100 * c['accuracy']:.1f}\%", font_size=28),
            MathTex(rf"\text{{always Red}}: {100 * (1 - d['base']):.1f}\%", font_size=26, color=GREY_B),
            MathTex(rf"\text{{recall}} = \frac{{TP}}{{TP + FN}} = {100 * c['recall']:.1f}\%", font_size=26, color=RES),
            MathTex(rf"\text{{precision}} = \frac{{TP}}{{TP + FP}} = {100 * c['precision']:.1f}\%", font_size=26),
        ), 5.2, 0.4, [3.6, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fit a logistic regression for the World's vote on income and age, and classify two thousand "
            "held-out adults, predicting Blue when the probability exceeds a half. The confusion matrix counts the four outcomes. "
            "<bookmark mark='b'/> The accuracy is sixty-five percent. <bookmark mark='c'/> That sounds respectable until you "
            "notice that predicting Red for everyone scores sixty-three. <bookmark mark='d'/> Of the Blue voters, the rule finds "
            "only twenty-four percent: its recall, or sensitivity, from Part 2. <bookmark mark='e'/> Of those it calls Blue, "
            "fifty-seven percent are: its precision. With an unbalanced outcome, accuracy alone hides almost everything."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(M), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def threshold(self):
        d = load("metrics")
        c = d["conf35"]
        M = self.matrix(c, [-2.8, 0.2, 0])
        rows = fit_rows(VGroup(
            label(r"lower the threshold to 0.35", font_size=24),
            MathTex(rf"\text{{recall}}: {100 * d['conf']['recall']:.0f}\% \to {100 * c['recall']:.0f}\%", font_size=26, color=HIT),
            MathTex(rf"\text{{precision}}: {100 * d['conf']['precision']:.0f}\% \to {100 * c['precision']:.0f}\%", font_size=26, color=RES),
            MathTex(rf"\text{{accuracy}}: {100 * d['conf']['accuracy']:.0f}\% \to {100 * c['accuracy']:.0f}\%", font_size=26),
            label(r"the right threshold depends on what each mistake costs", font_size=22, color=OBS),
        ), 5.2, 0.4, [3.6, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The threshold is a choice. Call Blue whenever the probability exceeds thirty-five percent. "
            "<bookmark mark='b'/> Recall rises from twenty-four to sixty-four percent: most Blue voters are now found. "
            "<bookmark mark='c'/> Precision falls from fifty-seven to forty-eight. <bookmark mark='d'/> And accuracy falls too, "
            "from sixty-five to sixty-one. <bookmark mark='e'/> Which is better depends entirely on what the two kinds of mistake "
            "cost: a campaign mailing leaflets cares about missing supporters; a screening test, Part 2's problem, about false "
            "alarms. Decision theory, Part 45, makes the choice formal."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(M), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def roc(self):
        d = load("metrics")
        A = axes([0, 1], [0, 1], x_length=4.8, y_length=4.8, xlabel=r"false positive rate", ylabel=r"true positive rate (recall)",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.2, 0.2, 0], font_size=18)
        ax = A.ax
        c = polyline(ax, d["fpr"], d["tpr"], OBS, 3.5)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_C, stroke_width=2)
        p5 = Dot(ax.c2p(d["conf"]["fp"] / (d["conf"]["fp"] + d["conf"]["tn"]), d["conf"]["recall"]), radius=0.09, color=RES)
        p3 = Dot(ax.c2p(d["conf35"]["fp"] / (d["conf35"]["fp"] + d["conf35"]["tn"]), d["conf35"]["recall"]), radius=0.09, color=HIT)
        rows = fit_rows(VGroup(
            label(r"every threshold at once", font_size=22),
            label(r"red: \ 0.5; \ green: \ 0.35", font_size=22, color=GREY_A),
            MathTex(rf"\text{{AUC}} = {d['auc']:.3f}", font_size=30, color=OBS),
            label(r"the chance a random Blue voter scores above a random Red one", font_size=20),
            label(r"Part 16's Mann--Whitney $U$, \ and Part 14's Challenger", font_size=20, color=GREY_A),
        ), 5.2, 0.4, [3.4, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> To see every threshold at once, plot the true positive rate against the false positive rate as "
            "the threshold sweeps from one to zero: the ROC curve, from Part 14. <bookmark mark='b'/> Our two thresholds are two "
            "points on it. <bookmark mark='c'/> The area under the curve is point six six. <bookmark mark='d'/> It's the "
            "probability that a random Blue voter gets a higher score than a random Red voter, <bookmark mark='e'/> Part 16's "
            "Mann–Whitney statistic again. Point five is guessing; one is perfect. Point six six says income and age carry real "
            "but limited information about the vote."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(p5), FadeIn(p3), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def pr(self):
        d = load("metrics")
        A = axes([0, 1], [0, 1], x_length=4.8, y_length=4.8, xlabel=r"recall", ylabel=r"precision", xticks=[0, 0.5, 1],
                 yticks=[0, 0.5, 1], center=[-3.2, 0.2, 0], font_size=18)
        ax = A.ax
        c = polyline(ax, d["rec"], d["prec"], S.CTRL, 3.5)
        base = DashedLine(ax.c2p(0, d["base"]), ax.c2p(1, d["base"]), color=GREY_C, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"precision against recall", font_size=22),
            MathTex(rf"\text{{baseline}}: \text{{the share of Blue}} = {d['base']:.2f}", font_size=24, color=GREY_B),
            label(r"precision starts high among the richest, \ then falls", font_size=22, color=S.CTRL),
            label(r"the curve of choice when positives are rare", font_size=22, color=OBS),
        ), 5.2, 0.4, [3.4, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A second view plots precision against recall. <bookmark mark='b'/> Guessing gives precision "
            "equal to the share of Blue voters, thirty-seven percent, whatever the recall. <bookmark mark='c'/> The model's "
            "precision starts near eighty percent among the very highest scores, the richest adults, and falls toward the "
            "baseline as the threshold drops. <bookmark mark='d'/> When the positives are rare, a rare disease or a fraudulent "
            "transaction, this curve shows what the ROC curve can hide: how many of the flagged cases are real."
        ) as vo:
            self.play(FadeIn(A), Create(base))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def calibration(self):
        d = load("metrics")
        pred, obs, cnt = (np.asarray(v) for v in d["calibration"])
        A = axes([0, 0.8], [0, 0.8], x_length=4.8, y_length=4.8, xlabel=r"predicted probability of Blue", ylabel=r"observed share",
                 xticks=[0, 0.4, 0.8], yticks=[0, 0.4, 0.8], center=[-3.2, 0.2, 0], font_size=18)
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(0.8, 0.8), color=GREY_C, stroke_width=2)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=HIT) for a, b in zip(pred, obs)])
        rows = fit_rows(VGroup(
            label(r"ten groups of 200, \ by predicted probability", font_size=22),
            label(r"on the diagonal: \ calibrated", font_size=22, color=HIT),
            MathTex(rf"\text{{Brier score}} = {d['brier']:.3f}", font_size=26),
            label(r"probabilities that mean what they say: \ Part 14", font_size=20, color=GREY_A),
            label(r"naive Bayes would fail this badly: \ chapter five", font_size=20, color=RES),
        ), 5.2, 0.4, [3.4, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Finally, are the probabilities honest? Group the held-out adults by their predicted probability, "
            "ten groups of two hundred, and compare each group's average prediction with the share who actually voted Blue. "
            "<bookmark mark='b'/> The points lie close to the diagonal: when the model says forty percent, about forty percent "
            "vote Blue. That's calibration. <bookmark mark='c'/> The Brier score, Part 14's mean squared error of the "
            "probabilities, is point two one five. <bookmark mark='d'/> A calibrated model's probabilities can be used directly "
            "for decisions. <bookmark mark='e'/> Chapter five's naive Bayes, with its odds of ten to the twenty, would fail this "
            "test spectacularly, while still classifying well."
        ) as vo:
            self.play(FadeIn(A), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, scale=1.5) for x in dots], lag_ratio=0.1), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def costs(self):
        d = load("costs")
        ths = np.asarray(d["ths"])
        runs = d["runs"]
        cols = {"1": GREY_A, "2": OBS, "5": RES}
        A = axes([0, 1], [0.2, 1.0], x_length=8.0, y_length=4.4, xlabel=r"threshold: \ call if $\hat p \ge t$",
                 ylabel=r"expected cost per adult", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0.2, 0.4, 0.6, 0.8, 1.0],
                 center=[-1.6, 0.3, 0])
        ax = A.ax
        curves, marks = VGroup(), VGroup()
        for c in ("1", "2", "5"):
            r = runs[c]
            cv = np.minimum(np.asarray(r["cost"]), 1.0)
            curves.add(polyline(ax, ths, cv, cols[c], 3.5))
            marks.add(VGroup(Dot(ax.c2p(r["best_t"], r["best_cost"]), radius=0.08, color=cols[c]),
                             DashedLine(ax.c2p(r["theory_t"], 0.2), ax.c2p(r["theory_t"], r["best_cost"]), color=cols[c],
                                        stroke_width=1.8)))
        rows = fit_rows(VGroup(
            label(r"a missed Blue voter costs $c$; \ a wasted call costs 1", font_size=22),
            label(rf"$c = 1$: \ best $t = {runs['1']['best_t']:.2f}$", font_size=22, color=GREY_A),
            label(rf"$c = 2$: \ best $t = {runs['2']['best_t']:.2f}$", font_size=22, color=OBS),
            label(rf"$c = 5$: \ best $t = {runs['5']['best_t']:.2f}$", font_size=22, color=RES),
            MathTex(r"\text{theory: } t^* = \frac{1}{1 + c}", font_size=30, color=HIT),
            label(r"dashed: \ $\tfrac12$, \ $\tfrac13$, \ $\tfrac16$; \ it works because $\hat p$ is calibrated", font_size=20, color=GREY_B),
        ), 3.45, 0.36, [5.1, 0.3, 0])
        with self.voiceover(
            "Calibration also settles the question we left open: where should the threshold go? "
            "<bookmark mark='a'/> Suppose a campaign phones the people it predicts will vote Blue. Missing a Blue voter costs c; "
            "a wasted call on a Red voter costs one. <bookmark mark='b'/> With equal costs, the expected cost per adult is "
            "smallest near a threshold of a half, as accuracy suggested. <bookmark mark='c'/> If a missed voter costs twice as "
            "much, the best threshold falls to about a third, <bookmark mark='d'/> and at five times, to about a sixth. "
            "<bookmark mark='e'/> Decision theory predicts exactly this. Call a person when the expected cost of not calling, c "
            "times p, exceeds the cost of calling, one minus p: that is, when p is above one over one plus c. <bookmark mark='f'/> "
            "The empirical minima sit on the dashed lines because the probabilities are calibrated. With naive Bayes's "
            "probabilities, the formula would put the threshold in the wrong place, however good the ranking."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(Create(curves[k]), FadeIn(marks[k][0]), FadeIn(rows[k + 1]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(*[Create(m[1]) for m in marks], FadeIn(rows[5]))
        self.wait(1.0)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"accuracy hides imbalance: \ always compare with the base rate", font_size=24),
            label(r"recall and precision trade off through the threshold", font_size=24, color=OBS),
            label(r"ROC and AUC: \ ranking quality, \ threshold-free", font_size=24, color=HIT),
            label(r"precision--recall: \ when positives are rare", font_size=24, color=S.CTRL),
            label(r"calibration and the Brier score: \ are the probabilities honest?", font_size=24, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: accuracy hides imbalance, so always compare with the base rate. <bookmark mark='b'/> Recall "
            "and precision trade off through the threshold, which costs should set. <bookmark mark='c'/> The ROC curve and its "
            "area measure ranking quality, free of any threshold. <bookmark mark='d'/> Precision–recall curves matter when "
            "positives are rare. <bookmark mark='e'/> And calibration asks whether the probabilities themselves can be trusted."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
