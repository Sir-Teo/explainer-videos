from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import HURDLE, PART, RAND_C, TRAIN_C, VALID_C, fit_right, load, tt


class RandomSearch(VoiceoverScene):
    def construct(self):
        r = load("random")
        self.card()
        self.draws(r)
        self.spread(r, load("noise"))
        self.scatter(r)
        self.best(r)
        self.curse(r)
        self.question()

    def card(self):
        c = chapter_card(3, r"Random search and the winner's curse", r"If you draw ten thousand formulas at random, how "
                         r"good does the best one look, and how good is it?", part=PART)
        with self.voiceover("Chapter three. The simplest miner draws formulas at random and keeps the best. How good does "
                            "the best of ten thousand look, and how good is it?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def draws(self, r):
        tops = r["top"][:8]
        rows = VGroup()
        for k, t in enumerate(tops):
            rows.add(VGroup(label(tt(t["formula"], 70), font_size=15, color=RAND_C),
                            MathTex(rf"{t['train']:.3f}", font_size=24, color=TRAIN_C)))
        for j, row in enumerate(rows):
            row[0].move_to([-1.2, 2.1 - 0.56 * j, 0]).align_to(np.array([-6.3, 0, 0]), LEFT)
            row[1].move_to([5.4, 2.1 - 0.56 * j, 0])
        head = VGroup(label(r"the best random formulas, by IC on 2018--19", font_size=20, color=GREY_B)
                      .move_to([-3.0, 2.75, 0]),
                      label(r"IC", font_size=20, color=TRAIN_C).move_to([5.4, 2.75, 0]))
        foot = wrapped_label(rf"{r['n']:,} trees drawn at random to depth 4 from the grammar of Chapter 2; each scored by its "
                             r"mean daily rank IC over the training days, and flipped if negative (a miner would trade a "
                             r"negative signal the other way)".replace(",", "{,}", 1), 12.0, 16, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"""We drew {r['n']:,} formulas at random, up to depth four, and scored each by its mean daily information coefficient on 2018 and 2019. The training score chooses the trading sign. <bookmark mark='a'/> Read the actual leading expressions: the winner smooths a recent minimum of typical price divided by the high. Several other entries repeat typical price divided by the low, directly or after ranking. These are related price-range expressions, but they are not all the same formula or necessarily identical signal vectors. Repeated strings and related syntax do not count independent ideas."""
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def spread(self, r, nz):
        tr = np.asarray(r["train"], float)
        tr = tr[np.isfinite(tr)]
        noise = np.abs(np.asarray(nz["train"], float))
        noise = noise[np.isfinite(noise)]
        top = float(np.ceil(max(tr.max(), noise.max()) * 100) / 100)
        bins = np.linspace(0, top, 31)
        h_r, _ = np.histogram(tr, bins)
        h_n, _ = np.histogram(noise, bins)
        f_r, f_n = h_r / h_r.sum(), h_n / h_n.sum()
        ym = float(np.ceil(max(f_r.max(), f_n.max()) * 20) / 20)
        g = axes([0, top], [0, ym], x_length=7.4, y_length=4.4, xlabel=r"$|$mean daily IC$|$ on 2018--19",
                 ylabel=r"share of formulas", xticks=[0, top / 2, top], yticks=[0, ym / 2, ym], font_size=15,
                 xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}").move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        w = bins[1] - bins[0]

        def bars(f, col, op):
            return VGroup(*[Rectangle(width=ax.c2p(w, 0)[0] - ax.c2p(0, 0)[0], height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1],
                                                                                          0.001),
                                      stroke_width=0, fill_color=col, fill_opacity=op).move_to(
                ax.c2p(b + w / 2, 0), aligned_edge=DOWN) for b, v in zip(bins[:-1], f) if v > 0])
        bn, br = bars(f_n, GREY_B, 0.6), bars(f_r, RAND_C, 0.85)
        leg = legend([(GREY_B, rf"{nz['n']} pure-noise signals"), (RAND_C, rf"{r['n']:,} random formulas".replace(",", "{,}"))],
                     font_size=15).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        med_r, med_n = float(np.median(tr)), float(np.median(noise))
        ratio = med_r / med_n
        side = VGroup(MathTex(rf"\text{{median, formulas}}: {med_r:.3f}", font_size=22, color=RAND_C),
                      MathTex(rf"\text{{median, noise}}: {med_n:.3f}", font_size=22, color=GREY_B),
                      wrapped_label(r"noise: a fresh random number for every coin and day, scored by the same code",
                                    3.4, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"""Before the winners, compare two chosen designs. <bookmark mark='a'/> Fresh independent normal numbers are assigned to each coin and day a few hundred times on the same grid. Their median absolute mean score is {med_n:.3f}. <bookmark mark='b'/> The training-signed random formulas have median {med_r:.3f}, about {ratio:.0f} times that benchmark. The grammar, missingness, repeated formulas and rank conventions differ from this noise design. This is descriptive evidence for the supplied archive and grammar, not a universal null test or a guarantee of tradable predictability."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bn], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in br], lag_ratio=0.03), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, r):
        tr = np.asarray(r["train"], float)
        va = np.asarray(r["valid"], float)
        ok = np.isfinite(tr) & np.isfinite(va)
        tr, va = tr[ok], va[ok]
        xm = float(np.ceil(tr.max() * 100) / 100)
        ym = float(np.ceil(np.abs(va).max() * 100) / 100)
        g = axes([0, xm], [-ym, ym], x_length=7.0, y_length=4.8, xlabel=r"IC on 2018--19 (sign chosen here)",
                 ylabel=r"IC on 2020, same sign", xticks=[0, xm / 2, xm], yticks=[-ym, 0, ym], font_size=15,
                 xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:+.2f}").move_to(LEFT * 1.9 + DOWN * 0.2)
        ax = g.ax
        rng = np.random.default_rng(0)
        idx = rng.choice(len(tr), min(1500, len(tr)), replace=False)
        idx = np.union1d(idx, np.argsort(-tr)[:40])
        dots = VGroup(*[Dot(ax.c2p(tr[i], va[i]), radius=0.025, color=RAND_C,
                            fill_opacity=0.55) for i in idx])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(xm, 0), color=GREY_B, stroke_width=1.5)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(min(xm, ym), min(xm, ym)), color=TRAIN_C, stroke_width=1.5)
        side = VGroup(MathTex(rf"\rho = {r['corr']:.2f}", font_size=30, color=HURDLE),
                      MathTex(rf"{100 * r['frac_same_sign']:.0f}\%\ \text{{kept their sign}}", font_size=24),
                      wrapped_label(r"each dot a formula (a sample of 1{,}500 plus the 40 best); on the dashed diagonal, "
                                    r"2020 would repeat 2018--19", 3.4, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            f"""Does the training score carry to the next labelled year? <bookmark mark='a'/> Each dot uses a formula's 2018-2019 mean score horizontally and its 2020 mean with the training-selected sign vertically. The formulas share data and many underlying expressions. <bookmark mark='b'/> The cross-formula correlation is {r['corr']:.2f}, and {100 * r['frac_same_sign']:.0f} percent keep a positive sign. These related observations do not supply ten thousand independent confirmations. Narrow ranges and low volatility recur in the formula family, but this comparison does not isolate a causal factor premium, remove the grid's availability limits or establish net trading performance."""
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.002, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def best(self, r):
        nz = load("noise")
        b = r["best_by_n"]
        Ns = np.array([x["n"] for x in b], float)
        xs = np.log10(Ns)
        trs = [x["train"] for x in b]
        vas = [x["valid"] for x in b]
        sd = nz["sd_train"]
        hurdle = [sd * math.sqrt(2 * math.log(2 * n)) for n in Ns]
        top = float(np.ceil(max(max(trs), max(vas), max(hurdle)) * 100) / 100)
        lo = float(np.floor(min(0.0, min(vas)) * 100) / 100)
        g = axes([1, 4], [lo, top], x_length=7.0, y_length=4.6, xlabel=r"formulas tried, $N$ (log scale)",
                 ylabel=r"IC of the best so far", xticks=[1, 2, 3, 4], yticks=sorted({lo, 0.0, top}), font_size=15,
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:.2f}").move_to(LEFT * 1.9 + DOWN * 0.2)
        ax = g.ax
        lt = curve(ax, xs, trs, TRAIN_C, stroke_width=3)
        lv = curve(ax, xs, vas, VALID_C, stroke_width=3)
        lh = DashedVMobject(curve(ax, xs, hurdle, HURDLE, stroke_width=2), num_dashes=30)
        zero = DashedLine(ax.c2p(1, 0), ax.c2p(4, 0), color=GREY_B, stroke_width=1.2)
        leg = legend([(TRAIN_C, r"its IC on 2018--19"), (VALID_C, r"the same formula on 2020"),
                      (HURDLE, r"$\sigma_e\sqrt{2\ln 2N}$: independent Gaussian reference scale")], font_size=15).to_edge(
            RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(rf"$\sigma_e = {sd:.4f}$: the spread of the mean training IC of {nz['n']} pure-noise "
                             r"signals on the same coins and days ($2N$: a sign is chosen for each formula)", 3.4, 15,
                             GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        last = b[-1]
        h_end = hurdle[-1]
        with self.voiceover(
            f"""Keep the largest training score so far. <bookmark mark='a'/> The winner rises to {last['train']:.3f} as ten thousand draws are inspected. <bookmark mark='b'/> A leading independent Gaussian absolute-maximum approximation, using the separately simulated noise spread and two-sided sign choice, gives {h_end:.3f}. This dashed bar is a reference scale, not a calibrated p-value for correlated, adaptive or non-Gaussian formula scores. <bookmark mark='c'/> The corresponding training-selected formula scores {last['valid']:+.3f} on the labelled 2020 validation period. That validation is repeatedly inspected in this lesson; it is not an untouched final test or proof of an executable edge."""
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lt), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lh))
            vo.wait_until("c")
            self.play(Create(lv), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def curse(self, r):
        a, v = r["top100_train_mean"], r["top100_valid_mean"]
        shrink = v / a if a else 0.0
        rows = [cmath(r"\widehat{IC}_i", r"=", r"IC_i + e_i,\qquad e_i \sim N(0, \sigma_e^2)", font_size=32,
                      colors={r"\widehat{IC}_i": TRAIN_C}),
                cmath(r"\mathbb E[\widehat{IC}_{(1)}]", r"\approx", r"IC + \sigma_e\sqrt{2\ln N}", font_size=32,
                      colors={r"\mathbb E[\widehat{IC}_{(1)}]": HURDLE}),
                cmath(r"\mathbb E[IC_i \mid \widehat{IC}_i]", r"=", r"\bar{IC} + \frac{\tau^2}{\tau^2 + \sigma_e^2}"
                      r"\big(\widehat{IC}_i - \bar{IC}\big)", font_size=30, colors={r"\mathbb E[IC_i \mid \widehat{IC}_i]":
                                                                                   VALID_C}),
                cmath(r"\text{here}", r":", rf"\text{{top 100}}\ \ {a:.3f}\ \to\ {v:+.3f},\quad \text{{kept}}\ "
                      rf"{100 * shrink:.0f}\%", font_size=30)]
        whys = [why(r"a measured score is the true one plus noise from a finite sample"),
                why(r"the winner of $N$ is selected partly for its noise: Part 26's expected maximum"),
                why(r"Gaussian prior, independent Gaussian noise and known variances: this conditional mean shrinks by the share "
                    r"of its spread that is real"),
                why(r"the hundred best formulas' mean IC on the training years and on 2020")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            f"""A winner can be selected partly for its estimation noise. <bookmark mark='a'/> A latent mean plus additive noise is a useful model. <bookmark mark='b'/> Under independent Gaussian noise with comparable means, the leading maximum grows like square root two log N; heterogeneous means and dependence change that argument. <bookmark mark='c'/> The displayed shrinkage is a conjugate Gaussian-prior conditional mean, with specified prior and noise variances. Those parameters are not estimated by dividing validation by training scores. <bookmark mark='d'/> Here the top hundred average {a:.3f} in training and {v:+.3f} in validation, retaining about {100 * shrink:.0f} percent. That ratio mixes selection, regime changes and measurement error. It does not identify what fraction of the spread is real. Related calm-coin formulas still provide far fewer distinct exposures than their string count suggests."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the search grows from 10{,}000 formulas to 1{,}000{,}000. By what factor does "
                       r"$\sqrt{2\ln N}$, the leading independent Gaussian reference scale, grow?")
        with self.voiceover(
            'Pause and predict. Under the leading independent Gaussian reference, the search grows from ten thousand formulas to a million. By what factor does square root two log N grow?'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
