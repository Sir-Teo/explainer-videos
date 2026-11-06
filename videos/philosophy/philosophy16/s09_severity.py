from __future__ import annotations

from videos.philosophy.philosophy16.common import *  # noqa: F403


class Severity(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Severe testing", r"When has a claim been well tested?", lit=(2018,), part=PART)
        with self.voiceover("Chapter eight. Severe testing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.rejection()
        self.acceptance()
        self.compare()

    def idea(self):
        hc = history_card(2018, r"Deborah Mayo", r"\textit{Statistical Inference as Severe Testing}", width=7.0,
                          color=HIST).to_corner(UL, buff=0.35)
        req = stack([(r"the severity requirement:", WHITE),
                     (r"data are good evidence for $H$ only if $H$ passed a test", NEYP),
                     (r"that would very probably have failed, \ were $H$ false", NEYP)], font_size=24).next_to(
            hc, DOWN, buff=0.5).set_x(0)
        eq = MathTex(r"\mathrm{SEV}(\mu > \mu_1) = P\big(\bar X \le \bar x_{\text{obs}};\ \mu = \mu_1\big)",
                     font_size=36, color=GOAL).next_to(req, DOWN, buff=0.5)
        note = label(r"error probabilities used to assess \textit{this} inference, \ not only the long run",
                     font_size=21, color=GREY_A).next_to(eq, DOWN, buff=0.3)
        with self.voiceover(
            "Deborah Mayo has spent forty years defending error statistics against the likelihood principle, and "
            "she reinterprets what tests are for. <bookmark mark='a'/>Her severity requirement: data are good "
            "evidence for a claim only if the claim passed a test that would very probably have failed, had the "
            "claim been false. <bookmark mark='b'/>For a normal mean, the severity with which the claim mu greater "
            "than mu one passes is the probability of a result no bigger than the one observed, if mu were exactly "
            "mu one. <bookmark mark='c'/>Error probabilities are then used to assess this particular inference, not "
            "just the long-run behaviour of a rule. That answers Neyman's critics, and it depends on what other "
            "results could have occurred."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in req], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()

    def _axes(self, title, color):
        ax = Axes(x_range=[-0.2, 0.8, 0.2], y_range=[0, 1, 0.25], x_length=7.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-2.2, -1.0, 0])
        xl = label(r"$\mu_1$", font_size=20, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        yl = label(title, font_size=19, color=color).next_to(ax.y_axis, UP, buff=0.1).align_to(ax.y_axis, LEFT)
        return ax, xl, yl

    def rejection(self):
        d = load("severity")
        s = d["significant"]
        head = label(r"A significant result: \ $\bar x = " + f"{s['xbar']}" + r"$, \ $n = " + str(d["n"]) +
                     r"$, \ $z = " + f"{s['z']:.1f}" + r"$", font_size=28, color=CONN).to_edge(UP, buff=0.3)
        ax, xl, yl = self._axes(r"severity of `$\mu > \mu_1$'", NEYP)
        curve = series_plot(ax, s["sev_greater"], NEYP, xs=d["mus"], width=4)
        mus = d["mus"]

        def at(m):
            return s["sev_greater"][min(range(len(mus)), key=lambda i: abs(mus[i] - m))]
        dots = VGroup(*[Dot(ax.c2p(m, at(m)), radius=0.07, color=c) for m, c in ((0.0, OK), (0.1, OK), (0.4, FISH),
                                                                                (0.6, BAD))])
        side = stack([(r"$\mu > 0$: \ severity " + f"{at(0.0):.2f}" + r": \ well warranted", OK),
                      (r"$\mu > 0.1$: \ " + f"{at(0.1):.2f}", OK),
                      (r"$\mu > 0.4$: \ " + f"{at(0.4):.2f}" + r": \ a coin flip", FISH),
                      (r"$\mu > 0.6$: \ " + f"{at(0.6):.2f}" + r": \ poorly warranted", BAD),
                      (r"the fallacy of rejection: \ `significant' is not `large'", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=4.6).move_to([4.5, -0.6, 0])
        with self.voiceover(
            "Take a significant result: an observed mean of point four, with twenty-five observations, so z is two. "
            "<bookmark mark='a'/>Plot, for each mu one, the severity with which the claim mu greater than mu one has "
            "passed. <bookmark mark='b'/>That mu is positive passed with severity point nine eight: had mu been "
            "zero, so large a result would have been very unlikely. <bookmark mark='c'/>That mu exceeds point one, "
            "with severity point nine three. <bookmark mark='d'/>That mu exceeds point four, only point five: a coin "
            "flip. <bookmark mark='e'/>That it exceeds point six, point one six: poorly warranted. "
            "<bookmark mark='f'/>Mayo calls the mistake of reading a significant result as a large effect the "
            "fallacy of rejection. Severity says how large an effect the data actually warrant."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(curve), run_time=2)
            for mk, i in zip("bcde", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(dots[i], scale=1.5), FadeIn(side[i]))
            vo.wait_until("f")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def acceptance(self):
        d = load("severity")
        s = d["not significant"]
        head = label(r"A non-significant result: \ $\bar x = " + f"{s['xbar']}" + r"$, \ $z = " + f"{s['z']:.1f}" +
                     r"$, \ $p = " + f"{s['p_one_sided']:.2f}" + r"$", font_size=28, color=CONN).to_edge(UP, buff=0.3)
        ax, xl, yl = self._axes(r"severity of `$\mu < \mu_1$'", ALTC)
        curve = series_plot(ax, s["sev_less"], ALTC, xs=d["mus"], width=4)
        mus = d["mus"]

        def at(m):
            return s["sev_less"][min(range(len(mus)), key=lambda i: abs(mus[i] - m))]
        side = stack([(r"$\mu < 0.6$: \ " + f"{at(0.6):.2f}" + r": \ large effects ruled out", OK),
                      (r"$\mu < 0.4$: \ " + f"{at(0.4):.2f}", FISH),
                      (r"$\mu < 0.1$: \ " + f"{at(0.1):.2f}" + r": \ `no effect' is \textit{not} shown", BAD),
                      (r"the fallacy of acceptance: \ `not significant' is not `no effect'", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=4.6).move_to([4.5, -0.6, 0])
        with self.voiceover(
            "Now a result that is not significant: an observed mean of point two, z of one, p of point one six. "
            "<bookmark mark='a'/>Here the question is which upper bounds on mu passed severely. "
            "<bookmark mark='b'/>That mu is below point six passed with severity point nine eight: large effects are "
            "ruled out. <bookmark mark='c'/>That mu is below point four, only point eight four. "
            "<bookmark mark='d'/>And that mu is below point one, a third: the data come nowhere near showing that "
            "there is no effect. <bookmark mark='e'/>This is the fallacy of acceptance, misreading number two from "
            "chapter two, now with a number attached."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(curve), run_time=2)
            for mk, i in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(side[i]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def compare(self):
        head = label(r"Severity and the posterior", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        eq = MathTex(r"\mathrm{SEV}(\mu > \mu_1) = \Phi\!\Big(\frac{\bar x - \mu_1}{\sigma/\sqrt n}\Big) = "
                     r"P_{\text{flat prior}}(\mu > \mu_1 \mid \bar x)", font_size=32, color=GOAL).next_to(head, DOWN,
                                                                                                    buff=0.4)
        rows = [
            (r"the same number", r"for a normal mean, \ severity equals the posterior under a flat prior", WHITE),
            (r"Bayesians", r"so severity is a posterior in disguise, \ and should obey the likelihood principle", BAYC),
            (r"Mayo", r"the numbers agree here by accident; \ under optional stopping, \ severity changes and the "
                      r"posterior does not", NEYP),
            (r"the stakes", r"whether evidence depends on the experiment that could have been, \ or only on the one "
                            r"that was", GOAL),
        ]
        g = rows_table(rows, top=0.6, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "There is a twist. <bookmark mark='a'/>For a normal mean, the severity of the claim mu greater than mu "
            "one equals the posterior probability of that claim under a flat prior. <bookmark mark='b'/>Bayesians "
            "conclude that severity is a posterior in disguise, and should therefore obey the likelihood principle. "
            "<bookmark mark='c'/>Mayo replies that the agreement is a coincidence of this simple case: once the "
            "experimenter may stop optionally, severity changes and the posterior does not, and that difference is "
            "the whole point. <bookmark mark='d'/>The stakes are the same as in chapter six: whether evidence "
            "depends on the experiment that could have been run, or only on the one that was."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
