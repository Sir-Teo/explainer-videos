from __future__ import annotations

import numpy as np

from videos.stats.stats19.common import *  # noqa: F403

ROWS, COLS = 24, 60  # the corner of the 60 x 2,000 matrix that is drawn
CELL = 0.13


def box(text, color, width=3.6, height=0.9, font_size=22):
    r = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                         fill_color=color, fill_opacity=0.12)
    t = label(text, font_size=font_size)
    if t.width > width - 0.3:
        t.width = width - 0.3
    return VGroup(r, t.move_to(r))


class Leakage(VoiceoverScene):
    def construct(self):
        self.card()
        self.experiment()
        self.two_ways()
        self.reps()
        self.why_leaks()
        self.catalogue()
        self.reuse()
        self.nested()
        self.protocol()
        self.closing()

    def card(self):
        card = chapter_card(10, r"Leakage and honest evaluation", r"When the test has seen the answers", lit=(2002,), part=PART)
        with self.voiceover("Chapter ten. Leakage, and honest evaluation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def matrix(self):
        g = np.random.default_rng(60)  # decoration only: the shading of the drawn cells
        vals = g.normal(size=(ROWS, COLS))
        cells = VGroup()
        for i in range(ROWS):
            for j in range(COLS):
                v = 0.5 + 0.18 * float(np.clip(vals[i, j], -2.5, 2.5))
                cells.add(Square(CELL, stroke_width=0, fill_color=interpolate_color(BLACK, GREY_A, v), fill_opacity=1)
                          .move_to([j * CELL, -i * CELL, 0]))
        lab = g.integers(0, 2, ROWS)
        ycol = VGroup(*[Square(CELL, stroke_width=0, fill_color=BLUE if lab[i] else RED, fill_opacity=1)
                        .move_to([(COLS + 1.5) * CELL, -i * CELL, 0]) for i in range(ROWS)])
        grid = VGroup(cells, ycol).move_to([0, 0.3, 0])
        chosen = sorted(g.choice(COLS, 8, replace=False).tolist())
        return grid, cells, ycol, chosen

    def experiment(self):
        d = load("leakage")
        grid, cells, ycol, chosen = self.matrix()
        top = label(rf"{d['n']} people $\times$ {d['p']:,} measurements: \ pure noise", font_size=26).next_to(grid, UP, buff=0.35)
        xl = label(r"(a corner of the matrix)", font_size=20, color=GREY_B).next_to(grid, DOWN, buff=0.2).align_to(grid, LEFT)
        yl = label(r"$y$: \ coin flips", font_size=20, color=GREY_A).next_to(ycol, DOWN, buff=0.2)
        cols = VGroup(*[SurroundingRectangle(VGroup(*[cells[i * COLS + j] for i in range(ROWS)]), buff=0.01,
                                             stroke_color=OBS, stroke_width=2.5) for j in chosen])
        msg = fit_rows(VGroup(
            label(r"every rule is truly 50\% accurate: \ there is nothing to learn", font_size=24, color=HIT),
            label(rf"step 1: \ keep the {d['k']} measurements most correlated with $y$", font_size=24, color=OBS),
            label(r"step 2: \ 5-fold CV of 5-nearest neighbours on those", font_size=24, color=CVC),
        ), 12.0, 0.25, [0, -2.6, 0])
        tag = simulated_tag(r"simulated: \ pure noise")
        with self.voiceover(
            "Here's an experiment, adapted from Hastie, Tibshirani and Friedman's textbook. <bookmark mark='a'/> Sixty people, "
            "two thousand measurements on each, like a gene-expression study, and a yes-or-no outcome. But every measurement "
            "is pure noise and the outcome is a coin flip. <bookmark mark='b'/> So there is nothing to learn: every rule, "
            "however clever, is right exactly half the time on new people. <bookmark mark='c'/> A natural analysis: first, keep "
            "the twenty measurements most correlated with the outcome, since two thousand is far too many. <bookmark mark='d'/> "
            "Then estimate the error of a five-nearest-neighbour classifier on those twenty, by five-fold cross-validation, "
            "exactly as chapter three taught."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(top), FadeIn(xl), FadeIn(yl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(msg[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(Create(cols), FadeIn(msg[1], shift=UP * 0.1), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(msg[2], shift=UP * 0.1))
        self.wait(1.0)
        self.clear_scene()

    def two_ways(self):
        d = load("leakage")
        head_w = label(r"the wrong way", font_size=28, color=RES)
        w1 = box(r"select 20 using all 60 people", OBS)
        w2 = box(r"5-fold CV: \ fit 5-NN, \ predict the fold", CVC)
        w3 = MathTex(rf"\text{{CV error}} = {100 * d['wrong']:.1f}\%", font_size=34, color=RES)
        wrong = VGroup(head_w, w1, w2, w3).arrange(DOWN, buff=0.45).move_to([-3.4, 0, 0])
        aw = VGroup(Arrow(w1.get_bottom(), w2.get_top(), buff=0.06, stroke_width=3, color=GREY_B),
                    Arrow(w2.get_bottom(), w3.get_top(), buff=0.06, stroke_width=3, color=GREY_B))
        head_r = label(r"the right way", font_size=28, color=HIT)
        r1 = box(r"select 20 using the training folds only", OBS, width=3.4, height=0.8, font_size=20)
        r2 = box(r"fit 5-NN on the training folds", CVC, width=3.4, height=0.8, font_size=20)
        loop = VGroup(r1, r2).arrange(DOWN, buff=0.4)
        frame = SurroundingRectangle(loop, buff=0.3, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2)
        ftag = label(r"repeated inside each of the 5 folds", font_size=18, color=GREY_B).next_to(frame, UP, buff=0.1)
        r3 = MathTex(rf"\text{{CV error}} = {100 * d['right']:.1f}\%", font_size=34, color=HIT)
        right = VGroup(head_r, VGroup(ftag, frame, loop), r3).arrange(DOWN, buff=0.4).move_to([3.4, 0, 0])
        ar = VGroup(Arrow(r1.get_bottom(), r2.get_top(), buff=0.06, stroke_width=3, color=GREY_B),
                    Arrow(frame.get_bottom(), r3.get_top(), buff=0.06, stroke_width=3, color=GREY_B))
        foot = label(r"the truth: \ 50\%", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='a'/> Do it that way and cross-validation reports an error of eleven point three percent. "
            "A classifier that's right nearly nine times in ten, from pure noise. <bookmark mark='b'/> The right way puts the "
            "selection inside the loop: in each fold, choose the twenty measurements using only the four training folds, "
            "fit on those folds, and predict the fold that was held out. <bookmark mark='c'/> Now cross-validation reports "
            "fifty point one percent, <bookmark mark='d'/> which is the truth. Same data, same classifier, same folds. The only "
            "difference is whether the held-out people helped choose the measurements."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head_w), FadeIn(w1), GrowArrow(aw[0]), FadeIn(w2), GrowArrow(aw[1]), FadeIn(w3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(head_r), Create(frame), FadeIn(ftag), FadeIn(r1), GrowArrow(ar[0]), FadeIn(r2), run_time=2.5)
            vo.wait_until("c")
            self.play(GrowArrow(ar[1]), FadeIn(r3))
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.1), Indicate(r3, color=HIT))
        self.wait(1.0)
        self.clear_scene()

    def reps(self):
        d = load("leakage")
        w, r = np.asarray(d["wrong_all"]), np.asarray(d["right_all"])
        edges = np.linspace(0, 0.8, 33)
        hw, _ = np.histogram(w, edges)
        hr, _ = np.histogram(r, edges)
        A = axes([0, 0.8], [0, 40], x_length=8.4, y_length=4.2, xlabel=r"CV error estimate", ylabel=r"data sets",
                 xticks=[0, 0.2, 0.4, 0.5, 0.6, 0.8], yticks=[0, 10, 20, 30, 40], center=[-1.5, 0.2, 0],
                 xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        bw = hist_bars(ax, edges, hw, color=RES)
        br = hist_bars(ax, edges, hr, color=HIT)
        truth = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 40), color=GREY_A, stroke_width=2.5)
        rows = fit_rows(VGroup(
            label(r"100 noise data sets", font_size=22),
            label(rf"red: \ selection outside, \ mean {100 * d['wrong']:.1f}\%", font_size=22, color=RES),
            label(rf"green: \ selection inside, \ mean {100 * d['right']:.1f}\%", font_size=22, color=HIT),
            label(r"dashed: \ the truth", font_size=22, color=GREY_A),
            label(r"not one red estimate above 30\%", font_size=22, color=RES),
        ), 3.45, 0.38, [5.1, 0.3, 0])
        cite = note(r"Ambroise \& McLachlan (2002): \ the selection bias in gene-expression classifiers", color=GREY_B)
        cite.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One data set could be a fluke, so here are a hundred, each pure noise. <bookmark mark='a'/> In red, the wrong way's "
            "estimates: every one far below fifty percent, most around ten. <bookmark mark='b'/> In green, the right way's: "
            "scattered around fifty, as an honest estimate from sixty people should be. <bookmark mark='c'/> This is not a "
            "contrived trap. In 2002 Christophe Ambroise and Geoffrey McLachlan showed that several published classifiers of "
            "cancer from gene expression reported near-zero error this way; done properly, the error was far higher."
        ) as vo:
            self.play(FadeIn(A), Create(truth), FadeIn(rows[0]), FadeIn(rows[3]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bw], lag_ratio=0.05), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in br], lag_ratio=0.05), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[4]), FadeIn(cite))
        self.wait(1.0)
        self.clear_scene()

    def why_leaks(self):
        rows = [
            cmath(r"\text{among 2,000 noise columns}", r":", r"\text{some correlate with } y \text{ by chance}", font_size=28),
            cmath(r"\text{choosing them used}", r":", r"y \text{ for every person, \ the test fold too}", font_size=28),
            cmath(r"\text{so in the test fold}", r":", r"\text{they still predict } y", font_size=28),
            cmath(r"\text{CV then measures}", r":", r"\text{memory, \ not prediction}", font_size=30),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"the top 20 of 2,000: \ $|r| \approx 0.33$ to $0.45$, \ $n = 60$"), why(r"the answers leaked into the rule"),
                why(r"their chance correlation includes those people"), why(r"held out in name only")]
        with self.voiceover(
            "Why does it happen? <bookmark mark='a'/> Among two thousand noise columns, a few correlate with the outcome by "
            "chance; with sixty people the top twenty have correlations between about point three and point four five. <bookmark mark='b'/> But those "
            "correlations were computed on all sixty people, including whoever later sits in the test fold. <bookmark mark='c'/> "
            "So in that fold the chosen columns still line up with the outcome: the chance pattern they were picked for includes "
            "those very people. <bookmark mark='d'/> Cross-validation then measures how well the rule remembers, not how well "
            "it predicts. The held-out fold was held out in name only."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def catalogue(self):
        items = [
            (r"preprocessing", r"scaling, \ imputing, \ PCA fitted on all the data", OBS),
            (r"selection", r"variables or features chosen with every outcome", RES),
            (r"tuning on the test set", r"the dial turned until the test error looks good", CVC),
            (r"duplicates and groups", r"the same patient, \ the same author, \ in both", BLUE),
            (r"time", r"tomorrow's data used to predict today", TEST),
            (r"target leakage", r"a feature recorded because of the outcome", RED),
        ]
        rows = VGroup(*[VGroup(label(a, font_size=24, color=c), label(b, font_size=22, color=GREY_A)) for a, b, c in items])
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.4)
        lefts = VGroup(*[r[0] for r in rows])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        w = max(r[0].width for r in rows)
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.4).align_to(lefts[0].get_left() + RIGHT * (w + 0.4), LEFT)
        rows.move_to([0, -0.3, 0])
        head = label(r"Six ways the answers leak", font_size=36).to_edge(UP, buff=0.6)
        cite = note(r"Kaufman, \ Rosset, \ Perlich \& Stitelman (2012): \ leakage in data mining", color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Selection is one leak among many. <bookmark mark='a'/> Preprocessing: standardizing, filling in missing values or "
            "computing principal components on all the data, before splitting. The effect is usually small, but it's the same "
            "mistake. <bookmark mark='b'/> Selection, as we've just seen. <bookmark mark='c'/> Tuning on the test set: trying "
            "settings until the test error looks good, which turns the test set into a training set. <bookmark mark='d'/> "
            "Duplicates and groups: the same patient's two scans, or two essays by the same author, one in training and one in "
            "test. <bookmark mark='e'/> Time: using tomorrow's information to predict today, which a random split of a time "
            "series does quietly. <bookmark mark='f'/> And target leakage: a feature recorded because of the outcome, like a "
            "treatment that's only given once the disease is diagnosed. A model that uses it predicts perfectly in the data and "
            "uselessly in practice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite))
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def reuse(self):
        d = load("reuse")
        acc = np.asarray(d["acc"])
        edges = np.linspace(0.44, 0.76, 33)
        h, _ = np.histogram(acc, edges)
        A = axes([0.44, 0.76], [0, 260], x_length=8.4, y_length=4.0, xlabel=r"accuracy on the holdout",
                 ylabel=r"submissions", xticks=[0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75], yticks=[0, 100, 200],
                 center=[-1.5, 0.4, 0], xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        bars = hist_bars(ax, edges, h, color=GREY_B)
        best = Line(ax.c2p(d["best"], 0), ax.c2p(d["best"], 100), color=OBS, stroke_width=4)
        vote = Line(ax.c2p(d["vote_acc"], 0), ax.c2p(d["vote_acc"], 200), color=RES, stroke_width=5)
        rows = fit_rows(VGroup(
            label(rf"{d['m']:,} random guesses, \ {d['n']:,} coin-flip labels", font_size=22),
            label(rf"the best guess: \ {100 * d['best']:.1f}\%", font_size=22, color=OBS),
            label(rf"vote of the {d['n_good']} above 50\%: \ {100 * d['vote_acc']:.1f}\%", font_size=22, color=RES),
            label(rf"that vote on fresh labels: \ {100 * d['vote_fresh']:.1f}\%", font_size=22, color=HIT),
            label(r"each score was honest; \ the reuse was not", font_size=22, color=GREY_A),
        ), 3.45, 0.38, [5.1, 0.4, 0])
        cite = note(r"Blum \& Hardt (2015): \ the leaderboard attack; \ Dwork et al.\ (2015): \ the reusable holdout",
                    color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "There's a subtler leak, which catches people who never touch the test set by hand. <bookmark mark='a'/> Picture a "
            "prediction competition with a leaderboard: you submit predictions, it reports your accuracy on a holdout of a "
            "thousand cases. Suppose the labels are coin flips, and you submit a thousand random guesses. <bookmark mark='b'/> "
            "Their scores scatter around fifty percent, and the best is fifty-five. <bookmark mark='c'/> Now combine the five "
            "hundred and thirteen that scored above fifty percent by majority vote. That one submission scores seventy-two point "
            "four percent on the leaderboard. <bookmark mark='d'/> On fresh labels, it's fifty point four, as it must be. "
            "<bookmark mark='e'/> Every score the leaderboard reported was honest; using them to choose and combine was not. "
            "Avrim Blum and Moritz Hardt described this attack in 2015, and Cynthia Dwork and colleagues showed how to build a "
            "holdout that can be safely reused, by adding noise to its answers."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.04), run_time=2.0)
            self.play(Create(best), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(vote), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]), FadeIn(cite))
        self.wait(1.0)
        self.clear_scene()

    def nested(self):
        d = load("nested")
        vals = [(r"min of the CV curve", d["min_cv"], RES), (r"true test error", d["true"], GREY_A),
                (r"nested CV", d["nested"], HIT)]
        A = axes([0, 3], [0.09, 0.12], x_length=6.0, y_length=4.0, xlabel=r"", ylabel=r"mean squared error",
                 xticks=[], yticks=[0.09, 0.1, 0.11, 0.12], center=[-2.6, 0.2, 0], yfmt=lambda v: f"{v:.2f}")
        ax = A.ax
        bars = VGroup()
        names = VGroup()
        for i, (t, v, c) in enumerate(vals):
            x0 = i + 0.5
            bot, top_ = ax.c2p(x0, 0.09), ax.c2p(x0, v)
            bars.add(Rectangle(width=1.1, height=top_[1] - bot[1], stroke_width=0, fill_color=c, fill_opacity=0.85)
                     .move_to(bot, aligned_edge=DOWN))
            names.add(label(t, font_size=18, color=c).next_to(bot, DOWN, buff=0.2))
        nums = VGroup(*[label(f"{v:.4f}", font_size=20, color=c).next_to(b, UP, buff=0.1) for b, (_, v, c) in zip(bars, vals)])
        rows = fit_rows(VGroup(
            label(rf"{d['reps']} training sets of 100; \ $k$ tuned over {len(d['ks'])} values", font_size=22),
            label(r"the minimum of noisy estimates is biased down", font_size=22, color=RES),
            label(r"nested: \ tune inside each outer fold", font_size=22, color=HIT),
            label(r"small here; \ large when the search is large", font_size=22, color=GREY_A),
        ), 5.0, 0.42, [3.9, 0.3, 0])
        with self.voiceover(
            "Even a careful analysis leaks a little in one more way. <bookmark mark='a'/> Chapter three chose k by minimizing "
            "the cross-validated error and then, tempting as it is, one reports that minimum as the error of the chosen rule. "
            "Here are two hundred training sets of a hundred, with k tuned over nine values. <bookmark mark='b'/> The minimum of "
            "the CV curve averages point one oh seven five. <bookmark mark='c'/> The true test error of the rule it picks "
            "averages point one one three five. The minimum of several noisy estimates is biased down, the winner's curse "
            "again. <bookmark mark='d'/> Nested cross-validation fixes it: an outer loop holds out a fold, an inner loop tunes "
            "k on the rest, and the outer fold scores the tuned rule. It averages point one one five three, slightly "
            "pessimistic, as cross-validation on smaller training sets should be. <bookmark mark='e'/> Here the optimism is five "
            "percent; with thousands of settings, or a whole menu of models, it can be most of the reported accuracy."
        ) as vo:
            self.play(FadeIn(A), FadeIn(rows[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(GrowFromEdge(bars[k], DOWN), FadeIn(names[k]), FadeIn(nums[k]),
                          *([FadeIn(rows[k])] if k else []))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.wait(1.0)
        self.clear_scene()

    def protocol(self):
        strip = VGroup(
            Rectangle(width=6.0, height=0.7, stroke_width=0, fill_color=TRAIN, fill_opacity=0.8),
            Rectangle(width=2.0, height=0.7, stroke_width=0, fill_color=CVC, fill_opacity=0.8),
            Rectangle(width=2.0, height=0.7, stroke_width=0, fill_color=TEST, fill_opacity=0.8),
        ).arrange(RIGHT, buff=0.06).move_to([0, 2.3, 0])
        names = VGroup(label(r"train: \ fit", font_size=22), label(r"validate: \ choose", font_size=22),
                       label(r"test: \ once", font_size=22))
        for n_, r in zip(names, strip):
            n_.move_to(r)
        rows = fit_rows(VGroup(
            label(r"split first; \ lock the test set away before looking", font_size=24, color=TEST),
            label(r"everything learned from data goes inside the loop: \ scaling, \ selection, \ tuning", font_size=24, color=CVC),
            label(r"split by the structure: \ people, \ authors, \ time", font_size=24, color=BLUE),
            label(r"report the test error once, \ with its uncertainty", font_size=24, color=HIT),
            label(r"the same discipline as a preregistered trial (Part 10's forking paths)", font_size=22, color=GREY_A),
        ), 12.4, 0.42, [0, -0.7, 0])
        with self.voiceover(
            "So here is the discipline. <bookmark mark='a'/> Split the data first, into a part for fitting, a part for "
            "choosing among fits, and a test set, and lock the test set away before you look at anything. With little data, "
            "cross-validation plays the first two roles, nested if it must also report. <bookmark mark='b'/> Everything "
            "learned from data, scaling, selection, tuning, goes inside the loop. <bookmark mark='c'/> Split along the data's "
            "structure, so that whole people, whole authors, or whole stretches of time are held out together. "
            "<bookmark mark='d'/> And use the test set once, reporting its error with a standard error, since a test set of "
            "two hundred measures an error rate of twenty percent with a standard error of about three points. <bookmark mark='e'/> It's the same discipline as "
            "a preregistered trial. Part 10's garden of forking paths, and this chapter's leaks, are the same problem: the "
            "data has been used to choose what it is then asked to judge."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in strip], lag_ratio=0.3), FadeIn(names), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1], shift=RIGHT * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def closing(self):
        rows = fit_rows(VGroup(
            label(r"Mosteller \& Wallace chose their words on some papers, \ then checked them on others", font_size=24, color=MAD),
            label(r"words picked for discriminating looked weaker on new papers: \ the selection effect, \ measured", font_size=22),
            label(r"our 91 words: \ their list, \ fixed before we looked", font_size=22, color=GREY_A),
            label(r"an error estimate is only as honest as the separation behind it", font_size=26, color=OBS),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Mosteller and Wallace knew all this. They chose their discriminating words using some papers "
            "and checked them on others. <bookmark mark='b'/> And they found exactly what this chapter predicts: words chosen "
            "because they separated the authors separated them less well on fresh papers. They measured the selection effect "
            "and allowed for it. <bookmark mark='c'/> Our ninety-one words are their list, fixed before we looked at our "
            "counts, which is why chapter nine's leave-one-out errors could be trusted. <bookmark mark='d'/> The lesson of the "
            "whole part, in a sentence: an error estimate is only as honest as the separation between what was learned and "
            "what it's tested on."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(1.0)
        self.clear_scene()
