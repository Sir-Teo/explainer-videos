from __future__ import annotations

import numpy as np

from videos.stats.stats10.common import *  # noqa: F403


class Misreadings(VoiceoverScene):
    def construct(self):
        self.card()
        self.not_posterior()
        self.icons()
        self.dance()
        self.size_not_effect()
        self.difference()
        self.asa()

    def card(self):
        card = chapter_card(11, r"What $p$-values are not", r"Six misreadings, \ and a statement", lit=(2016,), part=PART)
        with self.voiceover("Chapter eleven. What p-values are not."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def not_posterior(self):
        rows = [
            cmath(r"p", r"=", r"P\big(\text{data this extreme} \mid H_0\big)", font_size=34),
            cmath(r"p", r"\ne", r"P\big(H_0 \mid \text{data}\big)", font_size=34),
            cmath(r"P(H_0 \mid \text{significant})", r"=", r"\frac{\alpha\,P(H_0)}{\alpha\,P(H_0) + (1 - \beta)\,P(H_1)}", font_size=32),
        ]
        rows[1][2].set_color(REJ)
        rows[2][2].set_color(OBS)
        whys = [why(r"a statement about the data, \ assuming $H_0$"), why(r"the transposed conditional (Part 2's screening test)"),
                why(r"Bayes' rule: \ it depends on how many tested hypotheses were true to begin with")]
        intro = label('A null tail probability is not a posterior probability', font_size=36)
        with self.voiceover(
            "The most common misreading first. <bookmark mark='a'/> A p-value is a probability about the data, computed "
            "assuming the null is true. <bookmark mark='b'/> It is not the probability that the null is true, given the "
            "data. Confusing the two is the transposed conditional, the same mistake as Part 2's screening test, where a "
            "positive result from an accurate test still usually meant no disease. <bookmark mark='c'/> The chance that "
            "a significant result is a false alarm comes from Bayes' rule, and it depends on something the p-value "
            "knows nothing about: what fraction of the hypotheses being tested were true to begin with."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.6, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def icons(self):
        n_real, power, alpha = 100, 0.8, 0.05
        tp, fp = int(n_real * power), int((1000 - n_real) * alpha)
        cols = [ALTC] * n_real + [NULLC] * (1000 - n_real)
        arr = icon_array(cols, cols=50, size=0.11, buff=0.03).move_to([-3.0, 0.6, 0])
        g = np.random.Generator(np.random.PCG64(2005))
        real_idx = list(range(n_real))
        null_idx = list(range(n_real, 1000))
        hits = set(g.choice(real_idx, tp, replace=False)) | set(g.choice(null_idx, fp, replace=False))
        rows = fit_rows(VGroup(
            label(r"1,000 hypotheses tested; \ 100 are real effects", font_size=24),
            label(rf"power 80\%: \ {tp} real effects are significant", font_size=24, color=ALTC),
            label(rf"$\alpha = 5\%$: \ {fp} of the 900 nulls are significant too", font_size=24, color=REJ),
            MathTex(rf"\frac{{{fp}}}{{{fp} + {tp}}} = {fp / (fp + tp):.0%}".replace("%", r"\%") + r"\ \text{of the significant results are false}",
                    font_size=28, color=OBS),
            label(r"with 1 real in 100, \ 86\%", font_size=22, color=GREY_A),
            label(r"Ioannidis (2005): \ ``Why most published research findings are false''", font_size=22, color=GREY_A),
        ), 5.0, 0.3, [4.4, 0.2, 0])
        intro = label('Expected outcomes among a thousand tested hypotheses', font_size=36)
        with self.voiceover(
            "Here it is in pictures. <bookmark mark='a'/> A thousand hypotheses are tested, in some field where one in "
            "ten is a real effect: the green squares. <bookmark mark='b'/> With eighty percent power, eighty real effects are significant in expectation. The picture fixes the expected counts for illustration. <bookmark mark='c'/> With a five percent false-alarm rate, "
            "forty-five of the nine hundred nulls are significant in expectation. <bookmark mark='d'/> So of the hundred and "
            "twenty-five significant results, forty-five, thirty-six percent, are false, even though every test was "
            "performed perfectly at the five percent level. <bookmark mark='e'/> If only one hypothesis in a hundred is "
            "real, the false share rises to eighty-six percent. John Ioannidis built a famous argument on exactly this "
            "arithmetic in 2005."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(arr, lag_ratio=0.001), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(*[arr[i].animate.set_fill(OBS) for i in hits if i < n_real], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[arr[i].animate.set_fill(REJ) for i in hits if i >= n_real], FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(*[arr[i].animate.set_opacity(0.15) for i in range(1000) if i not in hits], FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4:]))
        self.clear_scene()

    def dance(self):
        d = load("dance")
        reps = d["reps"]
        A = axes([-0.4, 1.3], [0, 26], x_length=6.6, y_length=5.6, xlabel=r"difference in means, \ 95\% interval", xticks=[0, 0.5, 1.0],
                 center=[-2.8, -0.1, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 26), color=GREY_B, stroke_width=1.5)
        truth = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 26), color=EXACT, stroke_width=2)
        bars = VGroup()
        for i, r in enumerate(reps):
            y = 25 - i
            sig = r["p"] < 0.05
            c = OBS if sig else NULLC
            bars.add(VGroup(Line(ax.c2p(max(r["lo"], -0.4), y), ax.c2p(min(r["hi"], 1.3), y), color=c, stroke_width=3),
                            Dot(ax.c2p(r["diff"], y), radius=0.05, color=c),
                            MathTex(rf"{r['p']:.3f}", font_size=18, color=c).move_to([ax.c2p(1.3, y)[0] + 0.5, ax.c2p(0, y)[1], 0])))
        q = d["p_quantiles"]
        nsig = sum(r["p"] < 0.05 for r in reps)
        rows = fit_rows(VGroup(
            label(r"25 identical experiments: \ true effect $0.5\sigma$, \ 32 per group", font_size=24),
            label(rf"power $\approx$ {100 * d['power_sim']:.0f}\%: \ {nsig} of 25 significant", font_size=24, color=OBS),
            MathTex(rf"p\text{{-values, 10\% to 90\%:}}\ {q[0]:.4f} \text{{ to }} {q[4]:.2f}", font_size=26),
            label(r"the $p$-value is a noisy statistic;", font_size=24, color=OBS),
            label(r"the interval shows the noise", font_size=24, color=OBS),
            label(r"Cumming (2008): \ ``the dance of the $p$ values''", font_size=22, color=GREY_A),
        ), 5.0, 0.32, [4.4, -0.1, 0])
        tag = simulated_tag(r"simulated", corner=UR)
        with self.voiceover(
            "Second misreading: that a p-value is a stable property of a phenomenon. <bookmark mark='a'/> Run the same "
            "experiment twenty-five times: a true effect of half a standard deviation, thirty-two subjects per group. "
            "Each row is one run, with its estimate, its ninety-five percent interval, and its p-value. "
            "<bookmark mark='b'/> The power is about fifty percent, so about half the runs are significant, and half "
            "aren't, by chance alone. <bookmark mark='c'/> The p-values jump from point zero zero one to point six. "
            "Across many runs, the middle eighty percent of p-values stretch from about point zero zero one to point "
            "four six. <bookmark mark='d'/> Geoff Cumming called it the dance of the p-values. The intervals dance "
            "too, but they show you how much: every one of them is wide, and that width is the honest message."
        ) as vo:
            self.play(FadeIn(A), Create(zero), Create(truth), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars], lag_ratio=0.15), FadeIn(rows[0]), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def size_not_effect(self):
        n = 1_000_000
        d_small = 0.005
        z = d_small * np.sqrt(n / 2)
        from scipy import stats
        p_big = 2 * stats.norm.sf(z)
        rows = fit_rows(VGroup(
            label(r"third: \ a small $p$ is not a large effect", font_size=28, color=OBS),
            MathTex(rf"n = 10^6 \text{{ per group}},\ \ \delta = 0.005\sigma:\ \ z = {z:.2f},\ \ p = {p_big:.1e}".replace("e-0", r"\times 10^{-").replace("e-", r"\times 10^{-") + "}",
                    font_size=30),
            label(r"in heights: \ a third of a millimetre, \ ``highly significant''", font_size=24, color=GREY_A),
            label(r"fourth: \ a large $p$ is not ``no effect'': \ ``absence of evidence is not evidence of absence''", font_size=28, color=OBS),
            label(r"the tea with 6 cups could never reach $p < 0.05$, \ however good the lady", font_size=24, color=GREY_A),
        ), 12.6, 0.38, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Third: a small p-value doesn't mean a large effect. <bookmark mark='b'/> With a "
            "million people per group, a difference of five thousandths of a standard deviation gives z of three point "
            "five and a p-value of about four in ten thousand. <bookmark mark='c'/> In heights, that's a difference of "
            "about a third of a millimetre: highly significant, and utterly unimportant. The p-value mixes the size of the "
            "effect with the size of the sample. <bookmark mark='d'/> Fourth: a large p-value doesn't mean no effect. "
            "Absence of evidence isn't evidence of absence. <bookmark mark='e'/> With six cups, the tea test cannot go below point zero five, however skilled the lady: its smallest possible p-value is exactly one in twenty."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def difference(self):
        A = axes([-0.5, 2.5], [-10, 55], x_length=5.0, y_length=4.2, ylabel=r"estimated effect", yticks=[0, 25, 50], center=[-3.6, -0.2, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(-0.5, 0), ax.c2p(2.5, 0), color=GREY_B, stroke_width=1.5)
        specs = [(0, 25, 10, OBS, r"A: estimate 25, SE 10; $p = 0.012$"), (2, 10, 10, NULLC, r"B: estimate 10, SE 10; $p = 0.32$")]
        est = VGroup()
        for x, m, s_, c, t in specs:
            est.add(VGroup(Line(ax.c2p(x, m - 1.96 * s_), ax.c2p(x, m + 1.96 * s_), color=c, stroke_width=4), Dot(ax.c2p(x, m), radius=0.08, color=c),
                           label(t, font_size=20, color=c).next_to(ax.c2p(x, m + 1.96 * s_), UP, buff=0.15).set_x(-3.8 if x == 0 else -1.2)))
        rows = fit_rows(VGroup(
            label(r"fifth: \ ``significant'' vs ``not significant''", font_size=26, color=OBS),
            label(r"need not be a significant difference", font_size=26, color=OBS),
            MathTex(r"A - B = 15 \pm \sqrt{10^2 + 10^2} = 15 \pm 14.1:\ \ z = 1.06,\ \ p = 0.29", font_size=28),
            label(r"Gelman \& Stern (2006)", font_size=22, color=GREY_A),
            label(r"sixth: \ $p$ depends on the stopping rule", font_size=26, color=OBS),
            label(r"and on the analyses tried (ch.~10, \ ch.~12)", font_size=26, color=OBS),
        ), 5.6, 0.34, [3.6, -0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fifth, and subtler: a significant result and a non-significant result need not differ significantly from one another. <bookmark mark='b'/> Study A estimates an effect of twenty-five, plus or "
            "minus ten: p equals point zero one two. Study B estimates ten, plus or minus ten: p equals point three two. "
            "It's tempting to say A found an effect and B didn't, so they disagree. <bookmark mark='c'/> But the "
            "difference between them is fifteen, assuming independent studies, with a standard error of fourteen: z of about one, p of point two nine. "
            "No evidence that they differ at all. Andrew Gelman and Hal Stern made the point in 2006. "
            "<bookmark mark='d'/> And sixth: a p-value depends not only on the data but on the stopping rule and on how "
            "many analyses were tried, as chapters ten and twelve show."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(rows[0:2]))
            vo.wait_until("b")
            self.play(FadeIn(est))
            vo.wait_until("c")
            self.play(FadeIn(rows[2:4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4:]))
        self.clear_scene()

    def asa(self):
        hc = history_card(2016, r"R. Wasserstein \& N. Lazar, \ for the American Statistical Association",
                          r"the first formal statement on a matter of statistical practice in the ASA's 177 years", color=OBS, width=9.4,
                          font_size=22).to_edge(UP, buff=0.4)
        items = [
            r"$p$-values can indicate how incompatible the data are with a specified statistical model",
            r"they do not measure the probability that the hypothesis is true, \ or that the data arose by chance alone",
            r"conclusions and decisions should not rest only on whether $p$ passes a threshold",
            r"proper inference requires full reporting and transparency",
            r"a $p$-value does not measure the size of an effect or the importance of a result",
            r"by itself, \ a $p$-value is not a good measure of evidence about a model or hypothesis",
        ]
        rows = fit_rows(VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=24) for i, t in enumerate(items)]), 12.6, 0.3, [0, -0.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2016 the American Statistical Association issued, for the first time in its "
            "history, a formal statement on a matter of statistical practice: on p-values. It has six principles. "
            "<bookmark mark='b'/> P-values can indicate how incompatible the data are with a specified model. They don't "
            "measure the probability that the hypothesis is true, or that the data were produced by chance alone. "
            "Decisions shouldn't rest only on whether a p-value passes a threshold. Proper inference requires full "
            "reporting and transparency. A p-value doesn't measure the size of an effect or its importance. And by "
            "itself, a p-value isn't a good measure of evidence. Every principle on this list is a chapter of this part."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6), run_time=16.0)
        self.clear_scene()
