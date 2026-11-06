from __future__ import annotations

from videos.philosophy.philosophy16.common import *  # noqa: F403


class PValue(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"What a $p$-value is", r"And what is it not?", lit=(1925, 2016), part=PART)
        with self.voiceover("Chapter two. What a p-value is."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.define()
        self.wrong_a()
        self.wrong_b()
        self.intervals()
        self.asa()

    def define(self):
        d = load("pdist")
        head = label(r"The distribution of $p$", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"p = P\big(T \ge t_{\text{obs}} \mid H_0\big)", font_size=36, color=WHITE).next_to(head, DOWN,
                                                                                                         buff=0.3)
        axes = []
        for i, (title, counts, col) in enumerate(((r"if $H_0$ is true", d["null_hist"], NULLC),
                                                   (rf"if the effect is {d['effect']} \ (n = {d['n']})",
                                                    d["alt_hist"], ALTC))):
            ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 13, 4], x_length=5.4, y_length=3.2, tips=False,
                      axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to(
                [-3.4 + 6.8 * i, -1.2, 0])
            bars = hist_bars(ax, counts, col)
            t = label(title, font_size=21, color=col).next_to(ax, UP, buff=0.15)
            xl = label(r"$p$", font_size=19, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
            line = DashedLine(ax.c2p(0.05, 0), ax.c2p(0.05, 13), color=BAD, stroke_width=2)
            axes.append(VGroup(ax, t, xl, line, bars))
        n0 = label(rf"{100 * d['null_below_05']:.1f}\% \ below 0.05: \ uniform", font_size=20, color=NULLC).next_to(
            axes[0][0], DOWN, buff=0.55)
        n1 = label(rf"{100 * d['power']:.0f}\% \ below 0.05: \ the power", font_size=20, color=ALTC).next_to(
            axes[1][0], DOWN, buff=0.55)
        with self.voiceover(
            "The p-value is the probability, computed as if the null hypothesis were true, of a test statistic at "
            "least as extreme as the one observed. <bookmark mark='a'/>Simulate a hundred thousand studies in which "
            "the null is true. Their p-values are spread evenly between zero and one: under the null, p is uniform, "
            "and five percent of studies fall below point zero five by construction. <bookmark mark='b'/>Now "
            "simulate studies with a real effect of half a standard deviation and twenty subjects. The p-values "
            "pile up near zero; sixty-one percent fall below point zero five. That share is the test's power. "
            "<bookmark mark='c'/>A single p-value is one draw from one of these distributions. Almost every "
            "misreading of p comes from forgetting which."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            vo.wait_until("a")
            a = axes[0]
            self.play(FadeIn(a[0]), FadeIn(a[1]), FadeIn(a[2]), Create(a[3]),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in a[4]], lag_ratio=0.05))
            self.play(FadeIn(n0))
            vo.wait_until("b")
            a = axes[1]
            self.play(FadeIn(a[0]), FadeIn(a[1]), FadeIn(a[2]), Create(a[3]),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in a[4]], lag_ratio=0.05))
            self.play(FadeIn(n1))
            vo.wait_until("c")
            self.play(Indicate(VGroup(n0, n1), color=GOAL, scale_factor=1.05))
        self.clear_scene()

    def wrong_a(self):
        d = load("misread")
        head = label(r"Six misreadings, \ simulated \ (I)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = [
            (r"1. \ `$p$ is the probability that $H_0$ is true'",
             r"among studies with $0.04 < p < 0.05$: \ $H_0$ true in " +
             f"{100 * d['null_given_p_near_05_50']:.0f}" + r"\% \ if half of all nulls are true; \ in " +
             f"{100 * d['null_given_p_near_05_90']:.0f}" + r"\% \ if 90\% are", BAD),
            (r"2. \ `$p > 0.05$ means there is no effect'",
             r"a real effect of 0.2 with 20 subjects: \ $p > 0.05$ in " + f"{100 * d['real_effect_p_above_05']:.0f}"
             + r"\% \ of studies: \ absence of evidence", BAD),
            (r"3. \ `a smaller $p$ means a bigger effect'",
             r"effect 0.02, \ $n = 100{,}000$: \ $p = " + f"{d['tiny_effect_huge_n']['p']:.1e}".replace("e-", r"\times "
                                                                                                     r"10^{-")
             + r"}$; \ \ effect 0.8, \ $n = 10$: \ $p = " + f"{d['big_effect_small_n']['p']:.3f}" + r"$", BAD),
        ]
        g = VGroup()
        top = 1.8
        for a, b, c in rows:
            x = wrapped_label(a, 4.4, 21, c)
            y = wrapped_label(b, 7.6, 21, WHITE)
            x.move_to([-6.5 + x.width / 2, top - x.height / 2, 0])
            y.move_to([-1.6 + y.width / 2, top - y.height / 2, 0])
            g.add(VGroup(x, y))
            top -= max(x.height, y.height) + 0.55
        with self.voiceover(
            "Six common misreadings, and a simulation that refutes each. <bookmark mark='a'/>First: that p is the "
            "probability that the null hypothesis is true. Take all simulated studies whose p-value landed between "
            "point zero four and point zero five. If half of all tested nulls are true, about a fifth of these "
            "studies have a true null; if ninety percent of nulls are true, seventy percent of them do. The "
            "probability of the null depends on what else is being tested, and p does not see it. "
            "<bookmark mark='b'/>Second: that p above point zero five means there is no effect. With a real but "
            "small effect and twenty subjects, eighty-five percent of studies give p above point zero five. Absence "
            "of evidence is not evidence of absence. <bookmark mark='c'/>Third: that a smaller p means a bigger "
            "effect. A tiny effect in a sample of a hundred thousand gives a p-value of ten to the minus ten; a "
            "large effect in a sample of ten gives one percent."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=LEFT * 0.1))
        self.clear_scene()

    def wrong_b(self):
        d = load("misread")["two_studies"]
        head = label(r"Six misreadings, \ simulated \ (II)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = [
            (r"4. \ `$p = 0.05$ means a 5\% chance of a false positive'",
             r"the share of false positives \textit{among significant results} depends on the base rate and power: "
             r"\ often far above 5\% \ (next chapter)", BAD),
            (r"5. \ `$p$ is the probability the result is due to chance'",
             r"$p$ is computed \textit{assuming} chance alone; \ it cannot also be the probability of that "
             r"assumption", BAD),
            (r"6. \ `$p = 0.03$ and $p = 0.07$ disagree'",
             r"estimates " + f"{d['est_a']:.2f}" + r" and " + f"{d['est_b']:.2f}" + r", \ each $\pm$ " +
             f"{d['se']:.2f}" + r": \ the test of their difference gives $p = " + f"{d['diff_p']:.2f}" + r"$", BAD),
        ]
        g = VGroup()
        top = 1.8
        for a, b, c in rows:
            x = wrapped_label(a, 4.4, 21, c)
            y = wrapped_label(b, 7.6, 21, WHITE)
            x.move_to([-6.5 + x.width / 2, top - x.height / 2, 0])
            y.move_to([-1.6 + y.width / 2, top - y.height / 2, 0])
            g.add(VGroup(x, y))
            top -= max(x.height, y.height) + 0.55
        foot = label(r"Gelman and Stern \ (2006): \ the difference between `significant' and `not significant' "
                     r"is not itself significant", font_size=20, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "<bookmark mark='a'/>Fourth: that p equal to point zero five means a five percent chance that the "
            "result is a false positive. The share of false positives among significant results depends on how "
            "many of the tested hypotheses are true and on the power, and it is often far above five percent. The "
            "next chapter computes it. <bookmark mark='b'/>Fifth: that p is the probability that the result is due "
            "to chance. But p is computed by assuming that chance alone is at work; it cannot also be the "
            "probability of that assumption. <bookmark mark='c'/>Sixth: that one study with p of point zero three "
            "and another with point zero seven disagree. Their estimates are point two two and point one eight, "
            "each with a standard error of point one. A test of their difference gives p of point eight. "
            "<bookmark mark='d'/>As Andrew Gelman and Hal Stern put it, the difference between significant and not "
            "significant is not itself statistically significant."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def intervals(self):
        d = load("pdist")["ci"]
        head = label(r"Confidence intervals: \ what the 95\% belongs to", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.3)
        sub = label(r"Neyman \ (1937): \ " + str(d["reps"]) + r" samples of " + str(d["n"]) +
                    r", \ each with its interval $\bar x \pm 1.96/\sqrt{n}$", font_size=21, color=GREY_A).next_to(
            head, DOWN, buff=0.2)
        ax = Axes(x_range=[0, d["reps"], 20], y_range=[-1, 1, 0.5], x_length=11.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": False}).move_to([0, -0.9, 0])
        truth = DashedLine(ax.c2p(0, 0), ax.c2p(d["reps"], 0), color=GOAL, stroke_width=2)
        tl = label(r"true $\mu$", font_size=18, color=GOAL).next_to(truth, LEFT, buff=0.1)
        bars = VGroup(*[Line(ax.c2p(i + 0.5, r["lo"]), ax.c2p(i + 0.5, r["hi"]), color=ALTC if r["covers"] else BAD,
                             stroke_width=3) for i, r in enumerate(d["intervals"])])
        foot = stack([(str(d["covered"]) + r" of " + str(d["reps"]) + r" cover $\mu$; \ in the long run, \ " +
                       f"{100 * d['long_run']:.0f}" + r"\%", ALTC),
                      (r"`this interval contains $\mu$ with probability 95\%' \ is a misreading: \ it does or it "
                       r"doesn't \ (Morey et al., \ 2016)", BAD),
                      (r"the 95\% belongs to the procedure; \ a Bayesian credible interval gives the other "
                       r"statement", GREY_A)], font_size=21).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Confidence intervals, Neyman's invention of 1937, are often offered as the cure for p-values. But they "
            "have their own misreading. <bookmark mark='a'/>Draw a hundred samples of twenty, and compute each "
            "sample's ninety-five percent interval. <bookmark mark='b'/>Ninety-five of the hundred cover the true "
            "mean; five, in red, miss it. In the long run the procedure succeeds ninety-five percent of the time. "
            "<bookmark mark='c'/>But it is a misreading to say that a particular interval, once computed, contains "
            "the mean with probability ninety-five percent. It either does or it does not; Richard Morey and his "
            "colleagues call this the fundamental confidence fallacy. <bookmark mark='d'/>The ninety-five percent "
            "belongs to the procedure. The statement people want to make is a Bayesian one, about a credible "
            "interval, and it needs a prior."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(ax), Create(truth), FadeIn(tl))
            self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.02), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]), *[Indicate(b, color=BAD, scale_factor=1.3) for b, r in
                                         zip(bars, d["intervals"]) if not r["covers"]])
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def asa(self):
        hc = history_card(2016, r"The American Statistical Association", r"Statement on $p$-values \ (Wasserstein "
                          r"and Lazar)", width=7.6, color=HIST).to_corner(UL, buff=0.35)
        rows = stack([
            (r"1. \ $p$-values can indicate how incompatible the data are with a specified model", OK),
            (r"2. \ they do not measure the probability that a hypothesis is true", BAD),
            (r"3. \ conclusions should not rest only on whether $p$ passes a threshold", BAD),
            (r"4. \ proper inference requires full reporting and transparency", WHITE),
            (r"5. \ a $p$-value does not measure the size or importance of an effect", BAD),
            (r"6. \ by itself, \ a $p$-value is not a good measure of evidence", GOAL),
        ], font_size=22, buff=0.3, aligned_edge=LEFT).next_to(hc, DOWN, buff=0.45).set_x(0)
        foot = label(r"2019: \ `Moving to a world beyond $p < 0.05$'; \ others proposed $p < 0.005$ \ (Benjamin et al.,"
                     r" \ 2018)", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 2016 the American Statistical Association issued its first statement on a matter of statistical "
            "practice. <bookmark mark='a'/>P-values can indicate how incompatible the data are with a specified "
            "model. <bookmark mark='b'/>They do not measure the probability that a hypothesis is true. "
            "<bookmark mark='c'/>Conclusions should not rest only on whether p crosses a threshold. "
            "<bookmark mark='d'/>Proper inference requires full reporting. <bookmark mark='e'/>A p-value does not "
            "measure the size or importance of an effect. <bookmark mark='f'/>And by itself a p-value is not a good "
            "measure of evidence. <bookmark mark='g'/>Three years later its editors urged a world beyond p less "
            "than point zero five; others proposed instead a stricter threshold, point zero zero five."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(foot))
        self.clear_scene()
