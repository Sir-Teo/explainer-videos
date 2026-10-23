from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import (CI, EST, PART, TRUTH, hist_bars, interval_bar, load, stat_card, tagline,
                                   wrap_data)

A_COL, B_COL = C.COUNTING, C.MODEL_Q  # the four-character and five-character counting models


class Measure(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_number()
        self.bootstrap()
        self.two_models()
        self.paired()
        self.benchmarks()

    def card(self):
        card = chapter_card(1, r"Measuring a model", r"How sure is a single number?", lit=(1979,), part=PART)
        with self.voiceover("Chapter one. Measuring a model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def strip_axes(self, lo, hi, y=-0.6, length=11.0):
        return axes([lo, hi], [0, 1], x_length=length, y_length=0.01, xlabel=r"bits per character, \ one paragraph",
                    xticks=[x for x in range(int(np.ceil(lo)), int(hi) + 1)], center=[0, y, 0])

    def one_number(self):
        d = load("measure")
        k4 = d["orders"].index(4)
        bpc4 = d["bpc"][k4]
        pb, pn = np.asarray(d["par_bits_4"]), np.asarray(d["par_n_4"])
        per = pb / np.maximum(pn, 1)
        lo, hi = float(np.floor(per.min() * 2) / 2), float(np.ceil(per.max() * 2) / 2)
        big = stat_card(rf"{bpc4:.2f}", r"bits per character: \ Part 1's best counting model on the Falcon passage",
                        A_COL, width=7.4, value_size=60).to_edge(UP, buff=0.4)
        g = self.strip_axes(lo, hi)
        jit = np.random.default_rng(3).uniform(-0.45, 0.45, len(per))
        dots = VGroup(*[Dot(g.ax.c2p(v, 0) + UP * (0.55 + jit[k] * 0.8), radius=0.025 + 0.06 * np.sqrt(n / pn.max()),
                            color=A_COL, fill_opacity=0.75) for k, (v, n) in enumerate(zip(per, pn))])
        mean = DashedLine(g.ax.c2p(bpc4, 0), g.ax.c2p(bpc4, 0) + UP * 1.6, color=WHITE, dash_length=0.06)
        ml = label(r"the headline number: \ their average, \ weighted by length", font_size=22, color=GREY_A)
        ml.next_to(mean, UP, buff=0.1)
        tag = tagline(rf"computed: \ ${d['n_par']}$ paragraphs, \ ${d['chars']:,}$ characters".replace(",", "{,}"))
        from videos.ai.ai1 import compute as c1

        paras = [p_ for p_ in c1.text("passage").split("\n") if len(p_) > 120]
        text = wrap_data(paras[0][:330] + "...", chars=64, font_size=22, color=GREY_B, max_lines=5)
        text.next_to(big, DOWN, buff=0.6)
        src = label(r"\textit{The Maltese Falcon}, \ chapter 2: \ the passage", font_size=20, color=GREY_C)
        src.next_to(text, DOWN, buff=0.2)
        with self.voiceover(
            "Start with a number we have used since Part 1. The best of Part 1's counting models, which guesses each "
            f"character from the four before it, scores {bpc4:.2f} bits per character on the Falcon passage. "
            f"<bookmark mark='a'/> But that passage is one sample of English, {d['n_par']} paragraphs long. Here is "
            f"each paragraph's own score, one dot each, bigger for longer paragraphs: from {per.min():.1f} to "
            f"{per.max():.1f} bits. <bookmark mark='b'/> The headline number is their average, weighted by length. "
            "Had Hammett written a different chapter, it would have come out differently. How differently?"
        ) as vo:
            self.play(FadeIn(big, shift=DOWN * 0.2), FadeIn(tag), FadeIn(text), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeOut(text), FadeOut(src))
            self.play(FadeIn(g), LaggedStart(*[FadeIn(dt, scale=0.5) for dt in dots], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(ml))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bootstrap(self):
        d = load("measure")
        k4 = d["orders"].index(4)
        bpc4 = d["bpc"][k4]
        lo, hi = d["ci"][k4]
        r = np.asarray(d["boot_4"])
        defn = definition_card(r"the bootstrap \ (Efron, 1979)",
                               r"resample the data \textit{with replacement}, \ as many items as before; \ recompute "
                               r"the number; \ repeat. \ The spread of the results \ estimates the spread of the "
                               r"number itself.", color=CI, width=6.2, font_size=24).to_corner(UL, buff=0.35)
        x0, x1 = float(np.floor((r.min() - 0.02) * 20) / 20), float(np.ceil((r.max() + 0.02) * 20) / 20)
        g = axes([x0, x1], [0, 1.0], x_length=6.4, y_length=3.6, xlabel=r"bits per character of a resampled passage",
                 xticks=[round(x0 + (x1 - x0) * f, 2) for f in (0.0, 0.5, 1.0)], center=[3.3, -0.4, 0])
        bins = np.linspace(x0, x1, 40)
        stages = [20, 200, 1000, len(r)]
        hists = [hist_bars(g.ax, r[:n], bins, CI, scale=0.95 / np.histogram(r[:n], bins=bins, density=True)[0].max())
                 for n in stages]
        counter = [label(rf"${n:,}$ resamples".replace(",", "{,}"), font_size=22, color=GREY_A) for n in stages]
        for c_ in counter:
            c_.next_to(g.ax, UP, buff=0.2).align_to(g.ax, RIGHT)
        bracket = interval_bar(g.ax, 0.08, lo, hi, WHITE)
        bl = label(r"the middle $95\%$: \ a confidence interval", font_size=22, color=WHITE)
        bl.next_to(g.ax, DOWN, buff=1.0)
        vals = MathTex(rf"{lo:.2f} \;\text{{--}}\; {hi:.2f}", font_size=40, color=CI).next_to(bl, DOWN, buff=0.12)
        # a tiny picture of resampling: 12 paragraph chips drawn with replacement
        g2 = np.random.default_rng(7)
        chips = VGroup(*[RoundedRectangle(width=0.32, height=0.42, corner_radius=0.05, stroke_width=1.2,
                                          stroke_color=GREY_B, fill_color=TRUTH, fill_opacity=0.15 + 0.6 * (k / 12))
                         for k in range(12)]).arrange(RIGHT, buff=0.06)
        draws = g2.integers(0, 12, 12)
        resample = VGroup(*[chips[k].copy() for k in draws]).arrange(RIGHT, buff=0.06)
        chips.move_to([-3.6, -1.2, 0])
        resample.next_to(chips, DOWN, buff=0.55)
        arr = Arrow(chips.get_bottom(), resample.get_top(), buff=0.06, color=GREY_B, stroke_width=2.5)
        cl = label(r"the passage, \ paragraph by paragraph", font_size=20, color=GREY_A).next_to(chips, UP, buff=0.12)
        rl = label(r"one resample: \ some twice, \ some not at all", font_size=20, color=GREY_A)
        rl.next_to(resample, DOWN, buff=0.12)
        with self.voiceover(
            "Bradley Efron's answer, in 1979, was the bootstrap. <bookmark mark='a'/> Treat the sample as a stand-in "
            f"for the world. Draw {d['n_par']} paragraphs from it at random, with replacement, so that some come twice "
            "and some not at all, and score the model on that new passage. <bookmark mark='b'/> Then do it again, "
            "and again: here are twenty resamples, two hundred, a thousand, ten thousand. <bookmark mark='c'/> The "
            f"middle ninety-five percent of the results is a confidence interval: from {lo:.2f} to {hi:.2f} bits per "
            f"character. The headline {bpc4:.2f} is good to about plus or minus {(hi - lo) / 2:.2f}."
        ) as vo:
            self.play(FadeIn(defn, shift=DOWN * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(chips), FadeIn(cl))
            self.play(GrowArrow(arr), LaggedStart(*[TransformFromCopy(chips[k], resample[i]) for i, k in
                                                    enumerate(draws)], lag_ratio=0.1), FadeIn(rl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(hists[0]), FadeIn(counter[0]))
            for k in range(1, len(stages)):
                self.play(ReplacementTransform(hists[k - 1], hists[k]), ReplacementTransform(counter[k - 1], counter[k]),
                          run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(bracket), FadeIn(bl), Write(vals))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_models(self):
        d = load("measure")
        A, B = d["pair"]
        ka, kb = d["orders"].index(A), d["orders"].index(B)
        (la, ha), (lb, hb) = d["ci"][ka], d["ci"][kb]
        ba, bb = d["bpc"][ka], d["bpc"][kb]
        x0 = float(np.floor(min(la, lb) * 20 - 1) / 20)
        x1 = float(np.ceil(max(ha, hb) * 20 + 1) / 20)
        g = axes([x0, x1], [0, 3], x_length=9.0, y_length=2.4, xlabel=r"bits per character on the passage",
                 xticks=[round(x0 + (x1 - x0) * f, 2) for f in (0.0, 0.5, 1.0)], center=[0.6, 0.2, 0])
        ia = interval_bar(g.ax, 2.0, la, ha, A_COL, ba)
        ib = interval_bar(g.ax, 1.0, lb, hb, B_COL, bb)
        na = label(rf"the previous ${A}$ characters", font_size=24, color=A_COL).next_to(g.ax.c2p(x0, 2.0), LEFT,
                                                                                          buff=0.25)
        nb = label(rf"the previous ${B}$ characters", font_size=24, color=B_COL).next_to(g.ax.c2p(x0, 1.0), LEFT,
                                                                                          buff=0.25)
        pa_, pb_ = Dot(g.ax.c2p(ba, 2.0), radius=0.07, color=A_COL), Dot(g.ax.c2p(bb, 1.0), radius=0.07, color=B_COL)
        grp = VGroup(g, ia, ib, na, nb, pa_, pb_)
        if grp.get_left()[0] < -6.9:
            grp.shift(RIGHT * (-6.9 - grp.get_left()[0]))
        overlap = min(ha, hb) > max(la, lb)
        tag = tagline(r"computed: \ bootstrap over paragraphs, \ $95\%$ intervals")
        if overlap:
            verdict = ("Their intervals overlap. Read naively, that says we cannot tell them apart. But comparing two "
                       "separate intervals throws information away.")
        else:
            verdict = ("Their intervals don't even overlap here, but that is luck of the sizes: with a smaller gap, "
                       "two separate intervals would hide a real difference. Comparing them separately throws "
                       "information away.")
        with self.voiceover(
            f"Now compare two models: the {A}-character model, and one that looks back {B} characters. Looking "
            f"further back, it has seen too few examples of each long context, and here it does worse, by "
            f"{bb - ba:.3f} bits per character. Is that real? <bookmark mark='a'/> Bootstrap each one: "
            f"{la:.2f} to {ha:.2f}, <bookmark mark='b'/> and {lb:.2f} to {hb:.2f}. <bookmark mark='c'/> " + verdict
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(na), FadeIn(nb), FadeIn(pa_), FadeIn(pb_))
            vo.wait_until("a")
            self.play(Create(ia))
            vo.wait_until("b")
            self.play(Create(ib))
            vo.wait_until("c")
            if overlap:
                zone = Rectangle(width=abs(g.ax.c2p(min(ha, hb), 0)[0] - g.ax.c2p(max(la, lb), 0)[0]), height=1.6,
                                 stroke_width=0, fill_color=WHITE, fill_opacity=0.12)
                zone.move_to(g.ax.c2p((min(ha, hb) + max(la, lb)) / 2, 1.5))
                self.play(FadeIn(zone))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paired(self):
        d = load("measure")
        A, B = d["pair"]
        pa = np.asarray(d[f"par_bits_{A}"]) / np.maximum(np.asarray(d[f"par_n_{A}"]), 1)
        pb = np.asarray(d[f"par_bits_{B}"]) / np.maximum(np.asarray(d[f"par_n_{B}"]), 1)
        lo, hi = float(min(pa.min(), pb.min())), float(max(pa.max(), pb.max()))
        lo, hi = np.floor(lo * 2) / 2, np.ceil(hi * 2) / 2
        g = axes([lo, hi], [lo, hi], x_length=4.0, y_length=4.0, xlabel=rf"${A}$ characters", ylabel=rf"${B}$ characters",
                 xticks=[lo, hi], yticks=[lo, hi], center=[-4.3, -0.55, 0])
        diag = DashedLine(g.ax.c2p(lo, lo), g.ax.c2p(hi, hi), color=GREY_C, dash_length=0.06)
        pts = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.035, color=B_COL if y > x else A_COL, fill_opacity=0.85)
                       for x, y in zip(pa, pb)])
        head = label(r"each paragraph, \ scored by both", font_size=24, color=GREY_A).next_to(g, UP, buff=0.15)
        rows = [cmath(r"\mathrm{Var}(\hat B - \hat A)", r"=", r"\mathrm{Var}\,\hat A + \mathrm{Var}\,\hat B",
                      r"- 2\,\mathrm{Cov}(\hat A, \hat B)", font_size=34)]
        rows[0][3].set_color(CI)
        whys = [why(r"the variance of a difference")]
        step = ladder(self, rows, whys, keep=1, top=3.1, x=1.9, buff=0.5, edge=6.9)
        pl, ph = d["paired_ci"]
        ul, uh = d["unpaired_ci"]
        bd, bu = np.asarray(d["boot_diff"]), np.asarray(d["boot_diff_unpaired"])
        m = max(abs(bu).max(), abs(bd).max())
        x0, x1 = float(min(-0.02, bu.min() - 0.005)), float(max(bu.max() + 0.005, 0.02))
        h = axes([x0, x1], [0, 1.0], x_length=5.6, y_length=2.3, xlabel=r"difference, \ bits per character",
                 xticks=[0.0, round(x1 * 0.8, 2)], center=[2.9, -1.4, 0])
        bins = np.linspace(x0, x1, 46)
        dmax = max(np.histogram(bd, bins=bins, density=True)[0].max(), np.histogram(bu, bins=bins, density=True)[0].max())
        hu = hist_bars(h.ax, bu, bins, GREY_B, opacity=0.55, scale=0.95 / dmax)
        hp = hist_bars(h.ax, bd, bins, CI, opacity=0.85, scale=0.95 / dmax)
        zero = DashedLine(h.ax.c2p(0, 0), h.ax.c2p(0, 1.0), color=WHITE, dash_length=0.05)
        lg = legend([(GREY_B, r"unpaired"), (CI, r"paired: \ the same resample")], font_size=18)
        lg.next_to(h.ax, UP, buff=0.12).align_to(h.ax, LEFT)
        excl = pl > 0 or ph < 0
        uexcl = ul > 0 or uh < 0
        n_par = d["n_par"]
        tag = tagline(rf"computed: \ ${d['boots']:,}$ resamples".replace(",", "{,}"))
        if excl:
            verdict = (f"The paired interval runs from {pl:.3f} to {ph:.3f} and stays clear of zero: the "
                       f"{B}-character model really is worse on writing like this, and on {d['par_better']} of the "
                       f"{n_par} paragraphs.")
        else:
            verdict = (f"Even paired, the interval runs from {pl:.3f} to {ph:.3f} and includes zero: on this "
                       "passage we cannot say which model is better.")
        extra = ("The unpaired comparison, on the same data, could not see it." if not uexcl and excl else
                 "Pairing made the comparison sharper.")
        with self.voiceover(
            "The fix is to compare the models on the same paragraphs. <bookmark mark='a'/> Each dot is one paragraph, "
            f"scored by both: they lie along the diagonal. Both models find the same paragraphs hard, and their "
            f"scores correlate at {d['par_corr']:.2f}. <bookmark mark='b'/> The variance of a difference is the sum "
            "of the variances, minus twice the covariance. When the covariance is large, the difference is far more "
            "certain than either score. <bookmark mark='c'/> So resample the paragraphs once, score both models on "
            "that same resample, and take the difference. <bookmark mark='d'/> " + verdict + " <bookmark mark='e'/> "
            + extra
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            self.play(FadeIn(h), Create(zero), FadeIn(hu), FadeIn(lg[0]))
            vo.wait_until("d")
            self.play(FadeIn(hp), FadeIn(lg[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def benchmarks(self):
        m = load("measure")
        d = m["bench"]
        n, p1, p2 = d["n"], d["p1"], d["p2"]
        pm1, pm2 = np.asarray(m["bench_pmf1"]), np.asarray(m["bench_pmf2"])
        ks = np.arange(n + 1) / n
        sel = (ks > 0.6) & (ks < 0.8)
        g = axes([0.62, 0.80], [0, float(max(pm1.max(), pm2.max()) * 1.15)], x_length=6.0, y_length=2.6,
                 xlabel=rf"score on ${n}$ questions", xticks=[0.65, 0.70, 0.75], yticks=[],
                 xfmt=lambda v: rf"{int(round(v * 100))}\%", center=[-3.3, 0.6, 0])
        c1 = VMobject().set_points_as_corners([g.ax.c2p(x, y) for x, y in zip(ks[sel], pm1[sel])]).set_stroke(GREY_B, 3)
        c2 = VMobject().set_points_as_corners([g.ax.c2p(x, y) for x, y in zip(ks[sel], pm2[sel])]).set_stroke(EST, 3)
        lg = legend([(GREY_B, rf"true accuracy ${int(p1 * 100)}\%$"), (EST, rf"true accuracy ${int(p2 * 100)}\%$")],
                    font_size=18).next_to(g.ax, UP, buff=0.1).align_to(g.ax, RIGHT)
        tag = note(r"illustrative accuracies; \ the arithmetic is exact").next_to(g, DOWN, buff=0.15)
        s1 = stat_card(rf"\pm {d['se1'] * 100:.1f}\%", r"standard error of one score", GREY_B, width=3.6)
        s2 = stat_card(rf"{d['worse_ge'] * 100:.0f}\%", r"the worse model scores at least as high", C.PENALTY,
                       width=3.6)
        s3 = stat_card(rf"{d['se_unpaired'] * 100:.1f}\% \to {d['se_paired'] * 100:.1f}\%",
                       rf"error of the gap, \\ unpaired $\to$ paired \\ (the models disagree on ${int(d['disagree'] * 100)}\%$)",
                       CI, width=3.6, value_size=36)
        stats = VGroup(s1, s2, s3).arrange(DOWN, buff=0.25).move_to([3.9, 0.55, 0])
        cards = VGroup(
            history_card(2024, r"E.~Miller, \textit{Adding error bars to evals}", r"report standard errors; \ cluster "
                         r"them when questions come in groups \ (they can be $3\times$ larger); \ compare models question "
                         r"by question", width=6.5, color=CI, font_size=20),
            history_card(2023, r"M.~Sclar et al., \ prompt formatting", r"changing only the format of a few-shot prompt "
                         r"moved LLaMA-2-13B's accuracy by up to $76$ points", width=6.5, color=C.PENALTY, font_size=20),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The same arithmetic governs every benchmark. <bookmark mark='a'/> A test of five hundred questions, each "
            f"right or wrong, has a standard error of about {d['se1'] * 100:.0f} points at seventy percent. Take two "
            f"models whose true accuracies are {int(p1 * 100)} and {int(p2 * 100)} percent: <bookmark mark='b'/> the "
            f"worse one scores at least as high {d['worse_ge'] * 100:.0f} percent of the time. <bookmark mark='c'/> "
            "Compared question by question, where two similar models agree on most items, the error of the gap "
            f"falls from {d['se_unpaired'] * 100:.1f} points to {d['se_paired'] * 100:.1f}. <bookmark mark='d'/> "
            "Sampling is not the only noise: in a 2023 study, changing nothing but the format of a prompt moved "
            "one model's accuracy by up to seventy-six points. One number is a sample. Report the interval, pair "
            "the comparison, and vary the prompt."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), FadeIn(lg), FadeIn(s1))
            vo.wait_until("b")
            self.play(FadeIn(s2, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(s3, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.15) for c_ in cards], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()
