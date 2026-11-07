from __future__ import annotations

import numpy as np

from videos.stats.stats28.common import *  # noqa: F403


class Subsets(VoiceoverScene):
    def construct(self):
        self.card()
        self.sins()
        self.search()
        self.race()
        self.prostate_test()
        self.stability()
        self.lesson()

    def card(self):
        card = chapter_card(10, r"Subset selection", r"Best subsets, \ stepwise, \ and the lasso", lit=(2020,), part=PART)
        with self.voiceover("Chapter ten. Subset selection."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def sins(self):
        rows = fit_rows(VGroup(
            label(r"stepwise $p$-values and $F$-tests ignore the search", font_size=24, color=RES),
            label(r"coefficients biased away from zero; \ intervals too narrow", font_size=24, color=RES),
            label(r"unstable: \ a small change in the data, \ a different model", font_size=24, color=RES),
            label(r"greedy: \ forward steps can miss the best pair", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Stepwise regression has a long charge sheet, set out by Frank Harrell among others. Its "
            "p-values and F-tests ignore the search that produced them, chapter nine's problem. <bookmark mark='b'/> The "
            "chosen coefficients are biased away from zero and their intervals are too narrow. <bookmark mark='c'/> It is "
            "unstable, Breiman's complaint: perturb the data slightly and a different model comes out. "
            "<bookmark mark='d'/> And it is greedy: adding one variable at a time can miss a pair that only works together."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def search(self):
        rows = [
            cmath(r"\min_\beta \|y - X\beta\|^2", r"\text{ s.t. }", r"\|\beta\|_0 \le s", font_size=32),
            cmath(r"\text{all subsets}", r":", r"2^p \ \text{fits: \ NP-hard}", font_size=30),
            cmath(r"\text{leaps and bounds}", r":", r"\text{prune whole branches by RSS}", font_size=30),
            cmath(r"\text{mixed-integer optimization}", r":", r"p \text{ in the hundreds, \ with a certificate}", font_size=30),
        ]
        rows[0][2].set_color(PATH)
        whys = [why(r"best subset of size $s$"), why(r"Natarajan (1995)"), why(r"Furnival \& Wilson (1974)"),
                why(r"Bertsimas, King \& Mazumder (2016)")]
        with self.voiceover(
            "<bookmark mark='a'/> The alternative to greed is to search everything: the subset of size s with the "
            "smallest residual sum of squares. <bookmark mark='b'/> There are two to the p subsets, and the problem "
            "is NP-hard in general. <bookmark mark='c'/> George Furnival and Robert Wilson's leaps and bounds prunes "
            "whole branches of the search tree, since adding variables can only lower the RSS; it handles thirty or "
            "forty predictors. <bookmark mark='d'/> Dimitris Bertsimas, Angela King and Rahul Mazumder used modern "
            "mixed-integer solvers to reach hundreds, with an optimality certificate when the solver closes the gap; "
            "difficulty and running time depend on the design. Statkit's best_subset enumerates, which is enough for "
            "the prostate data's eight."
        ) as vo:
            intro=label('Best-subset optimization trades computation for a search guarantee',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def race(self):
        d = load("subsets")
        snr = np.log10(np.asarray(d["snrs"], float))
        A = axes([-1.5, 1.0], [-2.2, 0.4], x_length=7.4, y_length=4.4, xlabel=r"signal-to-noise ratio \ (log scale)",
                 ylabel=r"relative excess risk \ (log scale)", xticks=[np.log10(0.05), np.log10(0.25), 0, np.log10(6)],
                 yticks=[-2, -1, 0], xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, 0.3, 0])
        ax = A.ax
        cols = (("best", PATH), ("forward", AICC), ("lasso", HIT))
        lines = {k: polyline(ax, snr, np.log10(d[k]), c, 3) for k, c in cols}
        dots = {k: VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=c) for a, b in zip(snr, np.log10(d[k]))]) for k, c in cols}
        rows = fit_rows(VGroup(
            label(r"$n = 100$, \ $p = 10$, \ 5 true, \ correlation $0.35^{|i-j|}$", font_size=22),
            label(r"gold: \ best subset; \ blue: \ forward stepwise", font_size=22, color=PATH),
            label(r"green: \ the lasso, \ tuned on a validation set", font_size=22, color=HIT),
            label(rf"low SNR: \ lasso {d['lasso'][0]:.2f} vs best subset {d['best'][0]:.2f}", font_size=22, color=HIT),
            label(rf"high SNR: \ best subset {d['best'][-1]:.3f} vs lasso {d['lasso'][-1]:.3f}", font_size=22, color=PATH),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Which wins? Trevor Hastie, Robert Tibshirani and Ryan Tibshirani ran the race in "
            "2020; here is a small version: a hundred observations, ten correlated predictors of which five matter, "
            "and four signal-to-noise ratios. The plotted metric is prediction risk above irreducible noise, divided "
            "by the signal variance, so the zero predictor has relative excess risk one. <bookmark mark='b'/> Best "
            "subset and forward stepwise, each tuned on a validation set, run almost together. <bookmark mark='c'/> "
            "The lasso is green. <bookmark mark='d'/> When the signal is weak, the lasso wins clearly: its shrinkage "
            "tames the variance that subset selection's all-or-nothing choices add. <bookmark mark='e'/> When the "
            "signal is strong, best subset wins: unshrunk subset estimates can have less bias, while lasso shrinkage "
            "can cost accuracy. These are twenty-five-replication point estimates for one design, not a universal "
            "winner."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lines["best"]), FadeIn(dots["best"]), Create(lines["forward"]), FadeIn(dots["forward"]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lines["lasso"]), FadeIn(dots["lasso"]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Indicate(dots["lasso"][0], scale_factor=1.8), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Indicate(dots["best"][-1], scale_factor=1.8), FadeIn(rows[4]))
        self.clear_scene()

    def prostate_test(self):
        d = load("prostate")
        t, pen = d["tests"], d["pen"]
        hdr = [r"\textbf{prostate: \ method}", r"\textbf{predictors}", r"\textbf{test error (30 men)}"]
        body = [
            [r"null model", "0", f"{t['null']['test']:.3f}"],
            [r"full least squares", "8", f"{t['full']['test']:.3f}"],
            [r"AIC $=$ CV best subset", f"{t['aic']['size']}", f"{t['aic']['test']:.3f}"],
            [r"BIC $=$ CV one-SE", f"{t['bic']['size']}", f"{t['bic']['test']:.3f}"],
            [r"lasso, \ 10-fold CV", f"{pen['lasso']['nonzero']}", f"{pen['lasso']['test']:.3f}"],
            [r"ridge, \ 10-fold CV", "8", f"{pen['ridge']['test']:.3f}"],
        ]
        hdr.append(r"\textbf{paired MSE difference vs full $\pm$ SE}")
        for row,record in zip(body,[t['null'],t['full'],t['aic'],t['bic'],pen['lasso'],pen['ridge']]):
            row.append(rf"${record['paired_difference_full']:.3f}\pm{record['paired_se_full']:.3f}$")
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.28, colors=[GREY_A, RES, GREY_B, AICC, BICC, HIT, HIT])
        if tb.width>13.:tb.width=13.
        tb.move_to([0,0.7,0])
        foot = fit_rows(VGroup(
            label(r"Hastie, Tibshirani \& Friedman's train/test split: \ 67 and 30", font_size=22),
            label(r"observed nonnull gaps about 0.03; \ compare paired test-case differences, \ not marginal SE overlap", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And the prostate data's verdict, on the thirty men held out. The null model's error"
            " is one point oh six. <bookmark mark='b'/> Full least squares: point five two. AIC's and CV's seven "
            "predictors: point five two. BIC's and the one-SE rule's two: point four nine. The lasso and ridge: point"
            " five oh. <bookmark mark='c'/> The nonnull methods' observed errors differ by about three hundredths. We"
            " now also compute paired test-case differences against full least squares: their standard errors range "
            "from about point oh oh five to point oh six five. A large individual-error SE is not itself evidence "
            "that two methods are equivalent. Chapter four's flat CV curve was telling the truth: on these data the "
            "choice hardly matters, and a confident claim that one model is best would be noise."
        ) as vo:
            self.add(prostate_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[2:]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"low signal: \ shrink \ (lasso, \ ridge, \ Part 25)", font_size=24, color=HIT),
            label(r"high signal, \ sparse truth: \ best subset can win", font_size=24, color=PATH),
            label(r"relaxed lasso: \ select with the lasso, \ shrink less", font_size=24, color=AICC),
            label(r"either way: \ tune by CV, \ and don't trust the chosen model's $p$-values", font_size=24, color=RES),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson. With weak signals, shrink: the lasso, ridge, and Part 25's James–Stein. "
            "<bookmark mark='b'/> With strong signals and a truly sparse truth, best subset can win. <bookmark mark='c'/> "
            "Hastie and the Tibshiranis found the relaxed lasso, which selects with the lasso and then shrinks less, close to "
            "the best of both. <bookmark mark='d'/> Tune any of them by cross-validation, and don't believe the chosen model's "
            "p-values."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def stability(self):
        d = load("stability")
        names = d["names"]
        A = axes([-0.6, 7.6], [0, 1.05], x_length=7.6, y_length=4.2, xlabel=r"", ylabel=r"share of bootstrap selections",
                 xticks=[], yticks=[0, 0.5, 1], center=[-2.0, 0.5, 0])
        ax = A.ax
        wid = ax.c2p(0.36, 0)[0] - ax.c2p(0, 0)[0]

        def bars(v, dx, col):
            return VGroup(*[Rectangle(width=wid, height=max(ax.c2p(0, x)[1] - ax.c2p(0, 0)[1], 1e-3), fill_color=col,
                                      fill_opacity=0.85, stroke_width=1).move_to(ax.c2p(k + dx, x / 2)) for k, x in enumerate(v)])

        ba = bars(d["aic"]["inclusion"], -0.19, AICC)
        bb = bars(d["bic"]["inclusion"], 0.19, BICC)
        nm = VGroup(*[label(names[k], font_size=20, color=GREY_A).rotate(PI / 6).next_to(ax.c2p(k, 0), DOWN, buff=0.25)
                      for k in range(8)])
        a, b = d["aic"], d["bic"]
        rows = fit_rows(VGroup(
            label(rf"{d['R']} bootstrap resamples; \ search redone", font_size=22),
            label(r"share kept: \ blue AIC, \ purple BIC", font_size=22),
            label(rf"AIC: \ {a['distinct']} models; \ its pick {100 * a['original_share']:.0f}\%", font_size=22, color=AICC),
            label(rf"BIC: \ {b['distinct']} models; \ its pick {100 * b['original_share']:.0f}\%", font_size=22, color=BICC),
            label(r"only lcavol is kept every time", font_size=22, color=RES),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How stable are the prostate selections? Resample the sixty-seven men with "
            "replacement four hundred times and redo the best-subset search each time. <bookmark mark='b'/> The bars "
            "show how often each predictor is kept, blue for AIC and purple for BIC. <bookmark mark='c'/> AIC "
            "produced sixty-six different models, and its original seven-predictor choice came back only fifteen "
            "percent of the time. <bookmark mark='d'/> BIC produced sixty-two, and its pair came back eighteen "
            "percent of the time. <bookmark mark='e'/> Only cancer volume is kept every time. This is Breiman's "
            "instability, measured; Nicolai Meinshausen and Peter Bühlmann's stability selection uses structured "
            "subsampling and additional assumptions to obtain error control. These ordinary bootstrap frequencies are"
            " a descriptive stability check, not that guarantee."
        ) as vo:
            self.add(prostate_tag())
            self.play(FadeIn(A), FadeIn(nm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in ba], lag_ratio=0.08),
                      LaggedStart(*[GrowFromEdge(x, DOWN) for x in bb], lag_ratio=0.08), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Indicate(VGroup(ba[0], bb[0]), scale_factor=1.15), FadeIn(rows[4]))
        self.clear_scene()
