from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ ambiguity, robustness, beliefs", r"What do people do when they don't know the "
             r"odds, and can we just ask them?", "Chapter fifteen. Frontier: ambiguity, robustness, beliefs.",
             lit={2008: r"Hansen and Sargent, \emph{Robustness}"}, scale=("person", "market", "nation"))
        self.robust()
        self.beliefs()
        self.open_questions()

    def robust(self):
        r = load("robust")
        eps, mm = np.array(r["eps"]), np.array(r["maxmin"])
        th, hs = np.log10(np.array(r["thetas"])), np.array(r["multiplier"])
        ax = plane([0, 0.2], [0, 1.0], center=LEFT * 4.0 + DOWN * 0.6, x_length=4.4, y_length=3.8,
                   xticks=[0, 0.1, 0.2], yticks=[0, 0.5, 1.0], xlabel=r"doubt: \ chance of a good year in "
                   r"$0.5 \pm \varepsilon$", ylabel=r"share in the venture", font_size=15, xfmt=lambda v: f"{v:g}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%")
        bx = plane([th.min(), th.max()], [0, 1.0], center=RIGHT * 0.9 + DOWN * 0.6, x_length=4.4, y_length=3.8,
                   xticks=[-3, -2, -1], yticks=[0, 0.5, 1.0], xlabel=r"$\theta$: \ trust in the model \ (log)",
                   ylabel=r"share in the venture", font_size=15, xfmt=lambda v: f"10^{{{v:.0f}}}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%")
        c1 = path(ax, eps, mm, color=AMBIG, width=3.5, smooth=False)
        c2 = path(bx, th, hs, color=LATER, width=3.5, smooth=False)
        base = VGroup(DashedLine(ax.ax.c2p(0, r["base"]), ax.ax.c2p(0.2, r["base"]), color=GREY_C, stroke_width=1.5),
                      DashedLine(bx.ax.c2p(th.min(), r["base"]), bx.ax.c2p(th.max(), r["base"]), color=GREY_C,
                                 stroke_width=1.5))
        bl = label(rf"expected utility: \ {100 * r['base']:.0f}\%", font_size=17, color=GREY_B).next_to(
            ax.ax.c2p(0.2, r["base"]), UP, buff=0.06).shift(LEFT * 1.0)
        t1 = label(r"maxmin \ (Gilboa--Schmeidler)", font_size=21, color=AMBIG).next_to(ax, UP, buff=0.15)
        t2 = label(r"multiplier \ (Hansen--Sargent)", font_size=21, color=LATER).next_to(bx, UP, buff=0.15)
        side = VGroup(
            label(r"Dara's venture again, \ $\gamma = 2$", font_size=23),
            label(r"unsure of the odds, \ choose against \\ the worst case you can't rule out", font_size=21,
                  color=AMBIG),
            label(r"or: \ let nature tilt the odds \\ against you, \ at a cost $\theta$ \\ per unit of distance "
                  r"from \\ your model", font_size=21, color=LATER),
            label(r"more doubt, \ less risk taken: \\ ambiguity looks like \\ extra risk aversion", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Ellsberg's urn has become a research programme. The question is what people do when they don't trust "
            "the odds. <bookmark mark='a'/> Take Dara's venture, but suppose the chance of a good year is only known "
            "to lie within some distance of a half. A maxmin chooser picks the share that does best against the worst "
            "chance she can't rule out. With no doubt she puts in eighty-two percent; as the doubt grows, the share "
            "falls, and at fifteen points of doubt, when the worst case pays no more than the safe deposit, she stays out altogether. <bookmark mark='b'/> Lars Peter "
            "Hansen and Thomas Sargent built a smoother version from engineering's robust control: the chooser lets "
            "an imagined adversary tilt the odds against her, at a cost, theta, for every step away from her model. "
            "The less she trusts the model, the smaller theta, and the less she invests. <bookmark mark='c'/> In both, "
            "doubt about the model behaves like extra risk aversion. That's one reason asset-pricing models with "
            "fear of misspecification can explain premia without absurd values of gamma."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(bx), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(t1), Create(base[0]), FadeIn(bl), Create(c1), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(t2), Create(base[1]), Create(c2), FadeIn(side[2]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def beliefs(self):
        c1 = history_card(2004, r"Manski: \ ``Measuring Expectations''", r"stop inferring beliefs from choices; \ "
                          r"ask people for probabilities, \ and test the answers", color=LATER, width=12.0,
                          font_size=23)
        c2 = history_card(2002, r"Hurd and McGarry: \ the chance of living to 75", r"in the Health and Retirement "
                          r"Study, those still alive years later had reported survival chances about 50\% higher "
                          r"than those who died; \ people revised them after a new diagnosis", color=SAFE,
                          width=12.0, font_size=23)
        c3 = history_card(2018, r"Falk and colleagues: \ the Global Preference Survey",
                          r"risk taking, patience, trust and more, \ for about 80{,}000 people in 76 countries; \ "
                          r"preferences differ across countries, \ and differ more within them", color=TODAY,
                          width=12.0, font_size=23)
        g = VGroup(c1, c2, c3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.1)
        tag = published_tag(r"Manski, Econometrica (2004); Hurd and McGarry, EJ (2002); Falk et al., QJE (2018)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The other frontier is measurement. Everything in this part inferred beliefs and preferences from "
            "choices. <bookmark mark='a'/> Charles Manski argued in 2004 that economists should simply ask people "
            "for probabilities, and test the answers. <bookmark mark='b'/> The answers turn out to carry real "
            "information. In the Health and Retirement Study, people who were still alive years later had, at the "
            "start, reported chances of living to seventy-five about fifty percent higher than those who died; and "
            "they revised their chances down after a new diagnosis. <bookmark mark='c'/> And preferences themselves "
            "can now be measured at the scale of the world. The Global Preference Survey of Armin Falk and his "
            "colleagues measured risk taking, patience, trust and other preferences for about eighty thousand people "
            "in seventy-six countries. Preferences differ across countries, and differ even more within them."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(c1, color=LATER, scale_factor=1.02))
            for mk, c in zip("bc", (c2, c3)):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.2))
        self.clear_scene()

    def open_questions(self):
        head = label(r"Open questions", font_size=40, color=E.ACCENT).to_edge(UP, buff=0.6)
        rows = VGroup(
            label(r"is a person's risk aversion one trait, \ or different for money, health and careers?",
                  font_size=27),
            label(r"how much of present bias is in preferences, \ and how much in what people know and expect?",
                  font_size=27),
            label(r"when the odds themselves are unknown, \ what is a rational choice, \ and whose model of "
                  r"the odds counts?", font_size=27),
            label(r"which of these should enter policy, \ where one rate or one $\gamma$ must stand for everyone?",
                  font_size=27, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "So the frontier is full of open questions. <bookmark mark='a'/> Is risk aversion one trait of a "
            "person, or different for money, for health, for a career? <bookmark mark='b'/> How much of present "
            "bias is really in preferences, and how much in what people know and expect? <bookmark mark='c'/> When "
            "the odds themselves are unknown, what is a rational choice, and whose model of the odds should count? "
            "<bookmark mark='d'/> And when a policy must use a single discount rate, or a single gamma, for "
            "everyone, which of all these numbers should it be?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()
