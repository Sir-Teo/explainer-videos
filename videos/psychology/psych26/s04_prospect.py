from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Prospect(VoiceoverScene):
    def construct(self):
        self.card()
        self.reflection()
        self.value_curve()
        self.weighting()
        self.cumulative()

    def card(self):
        card = chapter_card(3, r"Prospect theory", r"What curve turns these choices into a theory?",
                            lit={1979: r"Kahneman \& Tversky", 1992: r"Tversky \& Kahneman", 1998: r"Prelec"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter three. Prospect theory."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def reflection(self):
        d = load("fourfold")
        head = heading(r"The reflection effect")
        pct_ = d["kt_pct"]
        n = d["kt_n"]
        def pair(title, risky, sure, rp, col):
            w = 5.2
            r1 = Rectangle(width=w * rp / 100, height=0.45, fill_color=RISKY, fill_opacity=0.9, stroke_width=0)
            r2 = Rectangle(width=w * (100 - rp) / 100, height=0.45, fill_color=SURE, fill_opacity=0.9, stroke_width=0)
            bar = VGroup(r1, r2).arrange(RIGHT, buff=0)
            l1 = label(rf"{rp}\%", font_size=20, color=BLACK).move_to(r1)
            l2 = label(rf"{100 - rp}\%", font_size=20, color=BLACK).move_to(r2)
            t = label(title, font_size=24, color=col)
            opts = VGroup(label(risky, font_size=21, color=RISKY), label(sure, font_size=21, color=SURE)).arrange(
                RIGHT, buff=0.6)
            return VGroup(t, opts, VGroup(bar, l1, l2)).arrange(DOWN, buff=0.18)
        g = pair(rf"gains \ ($N = {n['P3']}$)", r"4{,}000 at .80", r"3{,}000 for sure", pct_["P3"], GAIN)
        l_ = pair(rf"losses \ ($N = {n['P3neg']}$)", r"$-$4{,}000 at .80", r"$-$3{,}000 for sure", pct_["P3neg"],
                  LOSS)
        VGroup(g, l_).arrange(RIGHT, buff=1.0).move_to([0, 1.1, 0])
        rows = rows_of([
            (r"the same choice with the signs flipped: \ risk aversion for gains becomes risk seeking for losses",
             WHITE),
            (r"people respond to changes from a reference point, \ not to final states of wealth; \ the disease "
             r"problem moved the reference point with words", MODEL),
            (r"Kahneman and Tversky, \ 1979: \ \emph{prospect theory}, \ in Econometrica, \ one of the most cited "
             r"papers in economics", GREY_A),
        ], 11.8, 25, 0.32).move_to([0, -1.9, 0])
        tag = published_tag(r"Kahneman \& Tversky (1979), \ Problems 3 and 3$'$")
        assert d["kt_verdict"] == {"P3": "other", "P4": "risky", "P3neg": "risky"}
        with self.voiceover(
            "Kahneman and Tversky's first step was to flip the signs. <bookmark mark='a'/> Offered four thousand "
            f"with probability point eight, or three thousand for sure, {100 - pct_['P3']} percent of their "
            f"{n['P3']} respondents took the sure three thousand. Offered a point eight chance of losing four "
            f"thousand, or a sure loss of three thousand, {pct_['P3neg']} percent took the gamble. "
            "<bookmark mark='b'/> The same choice, reflected through zero, reverses the preference: risk aversion "
            "for gains, risk seeking for losses. <bookmark mark='c'/> And it shows what people respond to: not "
            "their final wealth, which Bernoulli's utility is defined on, but changes from a reference point, "
            "usually where they stand now. The disease problem moved that reference point with words, from "
            "everyone dead to everyone alive. <bookmark mark='d'/> The theory they built on these observations "
            "appeared in Econometrica in 1979."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g))
            self.play(FadeIn(l_))
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def value_curve(self):
        d = load("curves")
        head = heading(r"The value function")
        A = axes([-100, 100], [-140, 70], x_length=6.0, y_length=4.6, xticks=[-100, -50, 0, 50, 100],
                 yticks=[-120, -60, 0, 60], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"change from the reference point", ylabel=r"value", center=[-3.2, -0.3, 0], font_size=16)
        ax = A.ax
        x0 = Line(ax.c2p(-100, 0), ax.c2p(100, 0), color=GREY_D, stroke_width=1.5)
        y0 = Line(ax.c2p(0, -140), ax.c2p(0, 70), color=GREY_D, stroke_width=1.5)
        x, v = d["x"], d["v"]
        g = curve(ax, x[x >= 0], v[x >= 0], GAIN, 4)
        l_ = curve(ax, x[x <= 0], v[x <= 0], LOSS, 4)
        m100 = DashedLine(ax.c2p(100, 0), ax.c2p(100, d["gain_100"]), color=GAIN, stroke_width=2)
        mm100 = DashedLine(ax.c2p(-100, 0), ax.c2p(-100, -d["loss_100"]), color=LOSS, stroke_width=2)
        eq = MathTex(r"v(x) = \begin{cases} x^{\alpha} & x \ge 0 \\ -\lambda\,(-x)^{\beta} & x < 0 \end{cases}",
                     font_size=34, color=MODEL).move_to([3.4, 2.0, 0])
        rows = rows_of([
            (r"reference dependence: \ value is defined on gains and losses", WHITE),
            (r"diminishing sensitivity: \ concave for gains, \ convex for losses; \ the first 100 matters more than "
             r"the next", MODEL),
            (rf"loss aversion: \ losses loom larger; \ with $\lambda = {d['lam']}$, \ losing 100 weighs "
             rf"{d['loss_100'] / d['gain_100']:.2f} times as much as winning 100", LOSS),
            (rf"a 50--50 bet to lose 100: \ with the 1992 values the win must be {d['break_even']:.0f} before it "
             r"is worth taking", RISKY),
        ], 5.8, 22, 0.28).move_to([3.4, -0.9, 0])
        tag = psyche_tag(r"\texttt{choice.value}: \ Tversky \& Kahneman's (1992) $\alpha = \beta = 0.88$, "
                         r"\ $\lambda = 2.25$")
        with self.voiceover(
            "The first of prospect theory's two curves is the value function. <bookmark mark='a'/> It is defined "
            "on gains and losses from the reference point, not on wealth. <bookmark mark='b'/> It shows diminishing "
            "sensitivity both ways: concave for gains, so the first hundred won matters more than the next hundred, "
            "and convex for losses, for the same reason. Convexity for losses is what makes people gamble to avoid a "
            "sure loss. <bookmark mark='c'/> And it has a kink at zero. Losses loom larger than gains. In the "
            f"parameters Tversky and Kahneman estimated in 1992, the loss branch is {d['lam']} times as steep, so "
            f"losing a hundred weighs {d['loss_100'] / d['gain_100']:.2f} times as much as winning a hundred. "
            "<bookmark mark='d'/> Offer a fifty-fifty bet to lose a hundred, and with those values the win would "
            f"have to reach about {d['break_even']:.0f} before the bet is worth taking. Asked directly, most people "
            "want somewhere around twice the stake."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(x0), FadeIn(y0), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(g), Create(l_), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(m100), Create(mm100), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def weighting(self):
        d = load("curves")
        head = heading(r"The weighting function")
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=4.6, xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"stated probability $p$",
                 ylabel=r"decision weight $w(p)$", center=[-3.5, -0.3, 0], font_size=16)
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_B, stroke_width=2)
        wg = curve(ax, d["p"], d["w_gain"], GAIN, 4)
        wl = curve(ax, d["p"], d["w_loss"], LOSS, 3)
        key = legend([(GAIN, r"gains, \ $\gamma = 0.61$"), (LOSS, r"losses, \ $\delta = 0.69$"),
                      (GREY_B, r"$w(p) = p$")], font_size=17).move_to(ax.c2p(0.73, 0.2))
        eq = MathTex(r"w(p) = \frac{p^{\gamma}}{\big(p^{\gamma} + (1-p)^{\gamma}\big)^{1/\gamma}}", font_size=34,
                     color=MODEL).move_to([3.4, 2.0, 0])
        rows = rows_of([
            (r"small probabilities are overweighted: \ $w(0.01) \approx 0.06$ for gains", RISKY),
            (r"moderate and large ones are underweighted, \ and the jump from 0.99 to 1 is huge: \ the certainty "
             r"effect", SURE),
            (r"an inverse S: \ sensitivity is greatest near impossibility and certainty, \ diminishing in between",
             MODEL),
            (r"Prelec, \ 1998, \ derived another inverse S from axioms; \ the data rarely tell the two apart", GREY_A),
        ], 5.8, 22, 0.28).move_to([3.4, -0.9, 0])
        tag = psyche_tag(r"\texttt{choice.w\_tk}, \ \texttt{w\_prelec}")
        w01 = float(np.interp(0.01, d["p"], d["w_gain"]))
        with self.voiceover(
            "The second curve is about probability. Prospect theory doesn't weight outcomes by their probabilities, "
            "but by decision weights that are a bent function of them. <bookmark mark='a'/> Small probabilities "
            f"are overweighted. A one percent chance of a gain gets a weight of about {w01:.2f}, more than five times its "
            "size. That is the lottery ticket. <bookmark mark='b'/> Moderate and large probabilities are "
            "underweighted, and the step from ninety-nine percent to certainty is enormous. That is the certainty "
            "effect from Allais's problem. <bookmark mark='c'/> The result is an inverse S, flatter in the middle "
            "and steepest at the ends. Like the value function, it shows diminishing sensitivity, here away from "
            "the reference points of impossible and certain. <bookmark mark='d'/> Drazen Prelec derived a "
            "different inverse S from axioms in 1998; in data, the two shapes are hard to tell apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(diag), FadeIn(eq))
            self.play(Create(wg), Create(wl), FadeIn(key), run_time=2)
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def cumulative(self):
        head = heading(r"Derivation: \ cumulative prospect theory")
        eq1 = MathTex(r"V = \sum_i \pi_i\, v(x_i)", font_size=42, color=MODEL)
        eq2 = MathTex(r"\pi_i^{+} = w^{+}\!\big(P(X \ge x_i)\big) - w^{+}\!\big(P(X > x_i)\big)", font_size=36,
                      color=GAIN)
        eq3 = MathTex(r"\pi_i^{-} = w^{-}\!\big(P(X \le x_i)\big) - w^{-}\!\big(P(X < x_i)\big)", font_size=36,
                      color=LOSS)
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.35).move_to([-2.6, 0.8, 0])
        rows = rows_of([
            (r"1979: \ weight each probability separately; \ but then a lottery can be worth more than a better "
             r"one, \ splitting an outcome in two raises its weight", LOSS),
            (r"1992: \ weight the cumulative probability instead: \ an outcome's weight is how much it raises the "
             r"weighted chance of doing at least that well", MODEL),
            (r"the weights then never violate dominance, \ and still overweight the extremes: \ the best and worst "
             r"outcomes, \ when rare", GAIN),
            (r"Quiggin's rank-dependent utility, \ 1982, \ is the same idea without the kink", GREY_A),
        ], 5.9, 22, 0.3).move_to([3.4, 0.3, 0])
        cap = wrapped_label(r"the 1992 values: \ $\alpha = \beta = 0.88$, \ $\lambda = 2.25$, \ $\gamma = 0.61$, "
                            r"\ $\delta = 0.69$, \ medians of graduate students' certainty equivalents", 12.0, 24,
                            RISKY).to_edge(DOWN, buff=0.75)
        tag = published_tag(r"Tversky \& Kahneman (1992); \ Quiggin (1982)")
        with self.voiceover(
            "There's a technical problem in the 1979 version, and the fix is worth seeing. <bookmark mark='a'/> If "
            "each probability is weighted on its own, then splitting one outcome into two nearly equal ones raises "
            "its total weight, and a lottery can come out worth more than another that's better in every way. "
            "<bookmark mark='b'/> In 1992 Tversky and Kahneman weighted cumulative probabilities instead. Rank the "
            "outcomes. A gain's decision weight is how much it raises the weighted chance of doing at least that "
            "well; a loss's, how much it raises the weighted chance of doing at least that badly. "
            "<bookmark mark='c'/> These weights never violate dominance, and they still overweight the extremes: the "
            "best and the worst outcomes, when they're rare. <bookmark mark='d'/> John Quiggin had proposed the "
            "same rank-dependent idea in 1982, without the kink at zero. <bookmark mark='e'/> And the 1992 paper "
            "gave the parameters we've been using, medians of certainty equivalents that graduate students gave "
            "for dozens of gambles: point eight eight for the curvature, two point two five for loss aversion, "
            "and point six one and point six nine for the weights."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq1))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq2), Write(eq3), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(cap))
        self.clear_scene()
