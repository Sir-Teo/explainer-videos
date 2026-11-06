from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class Support(VoiceoverScene):
    def construct(self):
        self.card()
        self.condition()
        self.witness()
        self.chart()
        self.failure()
        self.betamin()

    def card(self):
        card = chapter_card(2, r"Support recovery", r"Finding the right variables, \ not just a good fit", lit=(2009,), part=PART)
        with self.voiceover("Chapter two. Support recovery: finding the right variables, not just a good fit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def condition(self):
        rows = [
            cmath(r"\text{goal}", r":", r"\mathrm{sign}(\hat\beta) = \mathrm{sign}(\beta^*): \ \text{exactly the right variables, \ right signs}", font_size=30),
            cmath(r"\text{irrepresentability}", r":", r"\big\|X_{S^c}^\top X_S (X_S^\top X_S)^{-1}\, \mathrm{sign}(\beta^*_S)\big\|_\infty < 1", font_size=30),
            cmath(r"\text{read}", r":", r"\text{no noise variable is well explained by the signal variables}", font_size=30),
            cmath(r"\text{necessary}", r":", r"\text{if it fails, \ the lasso picks a wrong variable at every } \lambda", font_size=30),
        ]
        rows[1][-1].set_color(LASSOC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"model selection consistency"), why(r"Zhao \& Yu (2006); \ Zou (2006)"), why(r"a regression of $X_{S^c}$ on $X_S$"), why(r"not just sufficient")]
        with self.voiceover(
            "<bookmark mark='a'/> A small estimation error is not the same as finding the right variables. The stronger goal "
            "is exact support recovery: the lasso's non-zero coefficients are exactly the true ones, with the right signs. "
            "<bookmark mark='b'/> Peng Zhao and Bin Yu, and independently Hui Zou, found the condition in 2006: the "
            "irrepresentable condition. <bookmark mark='c'/> Regress each noise variable on the signal variables, and weight "
            "the coefficients by the true signs. The result must be less than one in absolute value: no noise variable may be "
            "too well explained by the signals. <bookmark mark='d'/> And the condition is necessary: if it fails, then at "
            "every value of lambda, the lasso includes a wrong variable or drops a right one."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def witness(self):
        rows = [
            cmath(r"\text{step 1}", r":", r"\text{solve the lasso restricted to } S: \ \check\beta_S, \ \check z_S = \mathrm{sign}(\check\beta_S)", font_size=30),
            cmath(r"\text{step 2}", r":", r"\text{set } \check z_{S^c} \text{ from the KKT equations}", font_size=32),
            cmath(r"\text{step 3}", r":", r"\|\check z_{S^c}\|_\infty < 1 \Rightarrow (\check\beta_S, 0) \text{ is the lasso, \ uniquely}", font_size=32),
            cmath(r"\text{Wainwright (2009)}", r":", r"n > 2\,s\log(p - s)\,(1 + o(1)) \text{ suffices; \ fewer fails}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        rows[3][-1].set_color(SPIKEC)
        whys = [why(r"an oracle problem"), why(r"the subgradient off $S$"), why(r"strict dual feasibility"), why(r"Gaussian design, \ $\Sigma = I$")]
        with self.voiceover(
            "<bookmark mark='a'/> Martin Wainwright's primal–dual witness of 2009 is the standard proof. First solve the lasso "
            "as if the support were known, and record the signs. <bookmark mark='b'/> Then construct the subgradient on the "
            "other coordinates from the optimality conditions. <bookmark mark='c'/> If every one of those is strictly less than "
            "one in absolute value, the witness is the lasso solution, and it is unique, so the lasso has exactly the right "
            "support. Bounding them needs the irrepresentable condition and a union bound over the noise variables. <bookmark "
            "mark='d'/> For Gaussian designs the result is sharp: n greater than two s log of p minus s observations suffice, "
            "and with fewer the lasso fails with high probability."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("support")
        th = np.asarray(d["thetas"])
        A = axes([0.3, 2.1], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$\theta = n \,/\, \big(2s\log(p - s)\big)$", ylabel=r"P(exact signed support on the path)",
                 xticks=[0.5, 1, 1.5, 2], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"128": GREY_B, "256": BULKC, "512": LASSOC}
        cs = {k: VGroup(polyline(ax, th, v, cols[k], 4), *[Dot(ax.c2p(a, b), radius=0.08, color=cols[k]) for a, b in zip(th, v)])
              for k, v in d["curves"].items()}
        one = DashedLine(ax.c2p(1, 0), ax.c2p(1, 1.05), color=SPIKEC, stroke_width=2.5)
        c = d["curves"]
        side = fit_rows(VGroup(
            label(rf"$s = {d['s']}$, \ $\beta_j = \pm 0.5$, \ $\sigma = 0.5$, \ 30 trials a point", font_size=22),
            label(r"grey, \ teal, \ blue: \ $p = 128$, \ 256, \ 512", font_size=22, color=LASSOC),
            label(r"success: \ some $\lambda$ on the exact LARS path is right", font_size=22),
            label(rf"at $\theta = 1$: \ {100 * c['128'][3]:.0f}\%, \ {100 * c['256'][3]:.0f}\%, \ {100 * c['512'][3]:.0f}\%", font_size=22, color=SPIKEC),
            label(r"the curves collapse, \ and sharpen with $p$", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test of the threshold, with eight true variables. For each problem, we compute the "
            f"lasso's entire path exactly, by LARS, and ask whether any value of lambda gives exactly the right signed support. "
            f"<bookmark mark='b'/> Three dimensions, a hundred and twenty-eight, two hundred and fifty-six and five hundred and "
            f"twelve, plotted against Wainwright's rescaled sample size. <bookmark mark='c'/> At theta one half, success is "
            f"rare; at theta two, certain. <bookmark mark='d'/> At theta one, the three curves are at {100 * c['128'][3]:.0f}, "
            f"{100 * c['256'][3]:.0f} and {100 * c['512'][3]:.0f} percent. <bookmark mark='e'/> After rescaling, the "
            f"curves collapse onto one another and steepen as p grows, the signature of a sharp threshold at two s log p."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[Create(v) for v in cs.values()], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(one), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def failure(self):
        d = load("support")["irr"]
        rows = [[r"design", r"irrepresentable value", r"recovered, \ some $\lambda$"],
                [r"independent columns", f"{d['irr_good']:.2f}", f"{100 * d['good']:.0f}\\%"],
                [r"column 4 $\approx$ the signals' average", f"{d['irr_bad']:.2f}", f"{100 * d['bad']:.0f}\\%"]]
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.45, colors=[GREY_B, GOODC, BADC])
        tab.move_to([0, 0.9, 0])
        foot = label(rf"$n = {d['n']}$, \ $p = {d['p']}$, \ three true variables; \ 30 designs each", font_size=24, color=GREY_A).move_to([0, -1.0, 0])
        foot2 = label(r"more data does not help: \ the lasso prefers the impostor at every $\lambda$", font_size=24, color=BADC).move_to([0, -1.8, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> And when the condition fails? Three true variables among fifty, four hundred observations. "
            f"With independent columns, the irrepresentable value is {say(d['irr_good'], 2)}, and the right support appears "
            f"on the path every time. Now make the fourth, irrelevant column nearly the average of the three true ones: the "
            f"value becomes {say(d['irr_bad'], 2)}, above one, and the right support never appears. <bookmark mark='b'/> "
            f"Thirty designs of each kind. <bookmark mark='c'/> More data would not help: the impostor summarizes the truth so "
            f"well that the lasso includes it at every lambda. The adaptive lasso of Part thirty-two, or a non-convex penalty, "
            f"can escape; the lasso cannot."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def betamin(self):
        rows = fit_rows(VGroup(
            label(r"two more requirements for support recovery:", font_size=28, color=GREY_A),
            label(r"beta-min: \ $\min_{j \in S}|\beta^*_j| \gtrsim \sigma\sqrt{\log p/n}$, \ or small effects are invisible", font_size=26, color=LASSOC),
            label(r"and that is untestable from the data: \ a small $\beta_j$ looks just like zero", font_size=26, color=BADC),
            label(r"so: \ prediction and estimation need far less than selection", font_size=26, color=GOODC),
            label(r"which is why chapter 11 builds intervals that do not need the support", font_size=26, color=SPIKEC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two more requirements stand between the lasso and the right variables. <bookmark mark='b'/> "
            "The beta-min condition: every true coefficient must be larger than the noise level, sigma times the root of log "
            "p over n, or it is indistinguishable from zero. <bookmark mark='c'/> And whether it holds cannot be checked from "
            "the data, because a small coefficient looks exactly like a zero one. <bookmark mark='d'/> So good prediction and "
            "estimation need much less than correct selection. <bookmark mark='e'/> That is why chapter eleven builds "
            "confidence intervals that do not depend on selecting the right model."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
