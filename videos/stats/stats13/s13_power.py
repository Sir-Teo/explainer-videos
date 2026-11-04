from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403


class Power(VoiceoverScene):
    def construct(self):
        self.card()
        self.curves()
        self.formula()
        self.mde_curve()
        self.cohen()
        self.curse_scatter()
        self.curse_table()
        self.planning()

    def card(self):
        card = chapter_card(12, r"Power and sample size", r"How big must the experiment be?", part=PART)
        with self.voiceover("Chapter twelve. Power and sample size."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def curves(self):
        d = load("power")
        ns = np.asarray(d["ns"])
        A = axes([0, 80], [0, 1], x_length=7.4, y_length=4.4, xlabel=r"plots per variety, \ $n$", ylabel=r"power",
                 xticks=[0, 20, 40, 60, 80], yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], center=[-2.2, 0.0, 0],
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        crd, blk = d["curves"]["crd"], d["curves"]["blocked"]
        c1 = curve(ax, ns, np.asarray(crd["power"]), RES, 3)
        c2 = curve(ax, ns, np.asarray(blk["power"]), OBS, 3)
        line80 = DashedLine(ax.c2p(0, 0.8), ax.c2p(80, 0.8), color=GREY_C, stroke_width=2)
        m1 = DashedLine(ax.c2p(crd["n80"], 0), ax.c2p(crd["n80"], 0.8), color=RES, stroke_width=2)
        m2 = DashedLine(ax.c2p(blk["n80"], 0), ax.c2p(blk["n80"], 0.8), color=OBS, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"detect 2.5 bushels \ (5\%), \ $\alpha = 0.05$", font_size=24),
            label(r"power: \ P(significant $\mid$ real)", font_size=24),
            label(rf"CRD, \ $\sigma = 4$: \ {crd['n80']} plots each", font_size=24, color=RES),
            label(rf"blocked, \ $\sigma = 2$: \ {blk['n80']} plots each", font_size=24, color=OBS),
            label(r"half the $\sigma$, \ a quarter the plots", font_size=24, color=OBS),
        ), 4.6, 0.36, [4.6, 0.2, 0])
        with self.voiceover(
            "Every design decision in this part was really about one question: will the experiment see the effect if it's "
            "there? <bookmark mark='a'/> Say we want to detect a five percent yield gain, two and a half bushels, with a "
            "five percent test. <bookmark mark='b'/> The power is the chance the experiment declares the gain significant when "
            "it really exists. <bookmark mark='c'/> On a completely randomized field with a plot standard deviation of four "
            "bushels, the power climbs slowly with the number of plots: forty-two plots of each variety for eighty percent. "
            "<bookmark mark='d'/> If blocking halves the standard deviation to two, twelve plots each are enough. "
            "<bookmark mark='e'/> Halving the noise cuts the plots needed by a factor of four, because the number needed "
            "grows like sigma squared. Good design is cheaper than more data."
        ) as vo:
            self.play(FadeIn(A), Create(line80))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c1), run_time=2.0)
            self.play(Create(m1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(c2), run_time=2.0)
            self.play(Create(m2), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def formula(self):
        rows = [
            cmath(r"\text{reject if}", r"\ ", r"|\bar y_B - \bar y_A| > z_{1-\alpha/2}\,\sigma\sqrt{2/n}", font_size=32),
            cmath(r"\text{power}", r"\approx", r"\Phi\Big(\frac{\delta}{\sigma\sqrt{2/n}} - z_{1-\alpha/2}\Big)", font_size=32),
            cmath(r"n", r"=", r"\frac{2\,(z_{1-\alpha/2} + z_{1-\beta})^2\,\sigma^2}{\delta^2}", font_size=34),
            cmath(r"80\%,\ \alpha = 0.05", r":", r"n \approx 15.7\,(\sigma/\delta)^2 = 15.7/d^2", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the test, \ Part 10"), why(r"Part 10's power; \ exact: \ the noncentral $t$"),
                why(r"solve for $n$"), why(r"$d = \delta/\sigma$: \ Cohen's standardized effect")]
        with self.voiceover(
            "<bookmark mark='a'/> The arithmetic, from Part 10. The test rejects when the difference exceeds z times its "
            "standard error, sigma root two over n. <bookmark mark='b'/> If the true gain is delta, the power is approximately "
            "Phi of delta over the standard error, minus z. The curves on the last screen used the exact version, with the "
            "noncentral t distribution. <bookmark mark='c'/> Solve for n: two times the sum of two normal quantiles, "
            "squared, times sigma squared over delta squared. <bookmark mark='d'/> For eighty percent power at the five percent "
            "level, that's about fifteen point seven over d squared, where d is delta over sigma: the effect measured in "
            "standard deviations, Jacob Cohen's standardized effect size."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.0, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mde_curve(self):
        d = load("power")
        n = np.asarray(d["mde_n"])
        m = np.asarray(d["mde"])
        A = axes([0, 200], [0, 8], x_length=7.4, y_length=4.4, xlabel=r"plots per variety, \ $n$", ylabel=r"MDE, \ bushels",
                 xticks=[0, 20, 50, 80, 100, 150, 200], yticks=[0, 2, 4, 6, 8], center=[-2.2, 0.0, 0])
        ax = A.ax
        cv = curve(ax, n, m, OBS, 3)
        d20 = Dot(ax.c2p(20, d["mde_20"]), radius=0.09, color=S.ALT)
        d80 = Dot(ax.c2p(80, d["mde_80"]), radius=0.09, color=S.ALT)
        rows = fit_rows(VGroup(
            label(r"the smallest gain seen 80\% of the time", font_size=24),
            MathTex(r"\text{MDE} = (z_{1-\alpha/2} + z_{0.8})\,\sigma\sqrt{2/n}", font_size=28),
            MathTex(rf"n = 20:\ {d['mde_20']:.2f};\qquad n = 80:\ {d['mde_80']:.2f}", font_size=28, color=S.ALT),
            label(r"4$\times$ the plots, \ half the MDE", font_size=24, color=OBS),
            label(r"the square-root law", font_size=22, color=GREY_A),
        ), 4.6, 0.36, [4.6, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Or turn it around. Given the plots we can afford, what's the smallest gain we'd detect "
            "eighty percent of the time? <bookmark mark='b'/> That's the minimum detectable effect: the sum of the two quantiles "
            "times the standard error. <bookmark mark='c'/> With twenty plots per variety and sigma four, it's three and a half "
            "bushels, seven percent. With eighty plots, one point seven seven. <bookmark mark='d'/> Four times the plots buys "
            "half the detectable effect. <bookmark mark='e'/> The square-root law, again: precision is expensive, which is "
            "why reducing sigma by design beats adding plots."
        ) as vo:
            self.play(FadeIn(A), Create(cv))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 2:
                    self.play(FadeIn(d20, scale=2), FadeIn(d80, scale=2))
                self.play(FadeIn(rows[k]))
        self.clear_scene()

    def cohen(self):
        d = load("power")
        nc = d["n_cohen"]
        hc = history_card(1962, r"Jacob Cohen, \ ``The statistical power of abnormal-social psychological research''",
                          r"a year of a leading psychology journal: \ for effects of medium size, \ the typical study had less "
                          r"than an even chance of detecting them", color=S.PRIOR, width=10.4, font_size=22).move_to([0, 1.8, 0])
        tab = table_rows([[r"effect", r"$d$", r"$n$ per group for 80\%"],
                          [r"small", r"0.2", rf"{nc['small']}"],
                          [r"medium", r"0.5", rf"{nc['medium']}"],
                          [r"large", r"0.8", rf"{nc['large']}"]], font_size=26, col_buff=1.0, row_buff=0.25,
                         colors=[GREY_B, S.ALT, OBS, RES]).move_to([0, -0.7, 0])
        foot = label(r"Cohen's labels are conventions, \ not laws: \ the effect that matters depends on the problem",
                     font_size=22, color=GREY_A).move_to([0, -2.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1962 the psychologist Jacob Cohen surveyed a year of a leading journal and found that, for "
            "effects of medium size, the typical study had less than an even chance of detecting them, even if they were "
            "real. <bookmark mark='b'/> To make the problem concrete, he offered conventions: a small effect is a fifth of a "
            "standard deviation, needing nearly four hundred subjects per group for eighty percent power; a medium effect, "
            "half a standard deviation, sixty-three; a large one, twenty-five. <bookmark mark='c'/> They're conventions, "
            "not laws. The effect worth detecting depends on the problem: a two percent yield gain is enormous on a national "
            "scale."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(tab, lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def curse_scatter(self):
        d = load("power")
        est = np.asarray(d["est10"])
        sig = np.asarray(d["sig10"], bool)
        A = axes([-6, 10], [0, 1], x_length=10.0, y_length=2.2, xlabel=r"estimated gain, \ bushels", ylabel=r"", xticks=[-4, 0, 2.5, 8],
                 yticks=[], center=[0, 0.8, 0])
        ax = A.ax
        g = np.random.Generator(np.random.PCG64(4))
        jit = g.uniform(0.1, 0.9, len(est))
        dots = VGroup(*[Dot(ax.c2p(e, j), radius=0.05, color=OBS if s_ else GREY_D) for e, j, s_ in zip(est, jit, sig)])
        tl = DashedLine(ax.c2p(2.5, 0), ax.c2p(2.5, 1), color=EXACT, stroke_width=3)
        tlab = label(r"truth 2.5", font_size=20, color=EXACT).next_to(tl, UP, buff=0.08)
        rows = fit_rows(VGroup(
            label(r"300 underpowered experiments: \ 10 plots each, \ power 27\%", font_size=24),
            label(r"gold: \ the ones that came out ``significant''", font_size=24, color=OBS),
            MathTex(rf"\text{{mean significant estimate}} = {est[sig].mean():.2f}\ \ \text{{vs truth}}\ 2.5", font_size=30, color=RES),
            label(r"only the lucky overestimates clear the bar: \ the winner's curse", font_size=24, color=RES),
        ), 12.4, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "Low power does a second kind of damage, less obvious than missing real effects. <bookmark mark='a'/> Here are three "
            "hundred simulated experiments with ten plots per variety, where the true gain is two and a half bushels. Their "
            "power is twenty-seven percent. <bookmark mark='b'/> The gold ones are the experiments that came out significant. "
            "<bookmark mark='c'/> Their average estimate is four point five, nearly twice the truth. <bookmark mark='d'/> With "
            "so much noise, only the experiments that happened to overestimate the gain could clear the significance bar. If "
            "only significant results are published, the published effects are exaggerated. That's the winner's curse."
        ) as vo:
            self.play(FadeIn(A), Create(tl), FadeIn(tlab))
            vo.wait_until("a")
            self.play(FadeIn(dots, lag_ratio=0.005), FadeIn(rows[0]), run_time=2.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def curse_table(self):
        d = load("power")
        c = d["curse"]
        rows_ = [[r"$n$ per variety", r"power", r"exaggeration", r"wrong sign"]]
        for n in ("5", "10", "20", "42", "80"):
            rows_.append([n, rf"{100 * c[n]['power']:.0f}\%", rf"{c[n]['ratio']:.2f}$\times$", rf"{100 * c[n]['wrong_sign']:.1f}\%"])
        tab = table_rows(rows_, font_size=26, col_buff=0.7, row_buff=0.26, colors=[GREY_B] + [None] * 5).move_to([-2.5, 0.4, 0])
        for i in range(1, 6):
            tab[i][2].set_color(RES if c[rows_[i][0]]["ratio"] > 1.2 else HIT)
        rows = fit_rows(VGroup(
            label(r"20,000 experiments per row", font_size=22, color=GREY_A),
            label(r"exaggeration: \ mean $|$estimate$|$", font_size=24),
            label(r"of significant results, \ over the truth", font_size=24),
            label(r"Gelman \& Carlin (2014): \ type M, \ type S", font_size=24, color=OBS),
            label(r"power makes estimates honest", font_size=24, color=OBS),
        ), 4.4, 0.34, [4.7, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Across sample sizes: with five plots per variety, the power is fourteen percent, and a "
            "significant result exaggerates the true gain two point four times; one significant result in seventy-five even "
            "has the wrong sign. <bookmark mark='b'/> With twenty plots, power is half and the exaggeration one point four. "
            "<bookmark mark='c'/> At forty-two, our planned eighty percent, the exaggeration is twelve percent; by eighty plots "
            "it's gone. Andrew Gelman and John Carlin called these type M errors, of magnitude, and type S errors, of sign. "
            "<bookmark mark='d'/> An adequately powered experiment isn't only more likely to find a real effect. When it does, "
            "its estimate can be believed."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab[4]), FadeIn(tab[5]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def planning(self):
        rows = fit_rows(VGroup(
            label(r"a power calculation needs the effect worth detecting, \ and $\sigma$", font_size=26),
            label(r"$\sigma$ comes from a pilot or past trials, \ and is itself uncertain: \ plan for a range", font_size=24),
            label(r"the effect should be the smallest that matters, \ not the one you hope for", font_size=24, color=OBS),
            label(r"``post hoc power'' from the observed effect is a function of the $p$-value: \ it adds nothing", font_size=24, color=RES),
            label(r"design reduces $\sigma$; \ only the budget increases $n$", font_size=26, color=OBS),
        ), 12.4, 0.46, [0, 0, 0])
        with self.voiceover(
            "Some practical rules. <bookmark mark='a'/> A power calculation needs two inputs: the effect worth detecting, and "
            "the noise. <bookmark mark='b'/> The noise comes from a pilot study or past trials, and it's uncertain itself, so "
            "plan for a range of values, not one. <bookmark mark='c'/> The effect should be the smallest one that would matter "
            "in practice, not the one you hope to find; plugging in an optimistic effect is the commonest way to design an "
            "underpowered study. <bookmark mark='d'/> And don't compute power after the fact from the effect you observed: "
            "that number is just a transformation of the p-value, and tells you nothing new. <bookmark mark='e'/> Finally, "
            "remember the trade: design reduces sigma, and only money increases n."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
