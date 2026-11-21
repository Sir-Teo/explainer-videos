from __future__ import annotations

from videos.economics.econ53.common import *  # noqa: F403


class Design(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Information design for many", r"What if the audience is several people who affect each "
                                                           r"other?",
             "Chapter six. Information design for many.", lit={2016: r"Bergemann and Morris"},
             scale=("person", "market"), horizon=("a year",))
        self.game()
        self.three()
        self.bce()

    def game(self):
        D = load("design")
        rows = VGroup(
            label(r"two investors, \ each decides whether to invest in a project", font_size=23, color=RECEIVER),
            label(rf"the project is good \ ({100 * D['p_good']:.0f}\%): \ investing pays {D['good']:.0f}; \ bad: "
                  rf"\ it pays {D['bad']:.0f}".replace("-", "{-}"), font_size=23, color=WHITE),
            label(rf"each gains {D['together']:.0f} more if the other also invests", font_size=23, color=SIGNAL),
            label(r"a designer, \ who wants investment, \ chooses what each investor is told", font_size=23,
                  color=SENDER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.3)
        tag = published_tag(r"Bergemann and Morris, \ Theoretical Economics (2016); \ JEL 57(1) (2019)",
                            corner=DR, font_size=12)
        hc = history_card(2016, r"Dirk Bergemann and Stephen Morris", r"``Bayes correlated equilibrium and the "
                          r"comparison of information structures in games''", color=SENDER, width=10.0,
                          font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "Now the audience is not one judge but several people whose choices affect each other: depositors in "
            "a bank, buyers of a new asset, investors in a project. Dirk Bergemann and Stephen Morris built the "
            "theory. Take the simplest case. <bookmark mark='a'/> Two investors each decide whether to invest. "
            f"<bookmark mark='b'/> The project is good forty percent of the time, when investing pays "
            f"{D['good']:.0f}; when it is bad, investing pays {say_num(D['bad'], 0)}. <bookmark mark='c'/> Each "
            f"gains {D['together']:.0f} more if the other invests too. <bookmark mark='d'/> A designer, a "
            "promoter or a regulator who wants the investment to happen, chooses what each investor is told."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(hc))
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def three(self):
        D = load("design")
        ax = plane([-0.5, 2.5], [0, 2.0], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.4, y_length=4.6, xticks=[],
                   yticks=[0, 0.5, 1.0, 1.5, 2.0], ylabel=r"expected number investing", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        vals = [(r"tell nothing", D["none"], GRID), (r"tell everything", D["full"], RECEIVER),
                (r"the best design", D["best"], SENDER)]
        bars = VGroup()
        for i, (nm, v, c) in enumerate(vals):
            p0, p1 = ax.ax.c2p(i - 0.3, 0), ax.ax.c2p(i + 0.3, max(v, 0.005))
            b = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=c,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            vl = label(f"{v:.1f}", font_size=18, color=WHITE).next_to(b, UP, buff=0.08)
            nl = label(nm, font_size=17, color=c).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.2)
            bars.add(VGroup(b, vl, nl))
        side = VGroup(
            label(rf"nothing: \ a project that \\ pays {say_num(D['pool_payoff'], 1)} on average, \\ even if both "
                  r"invest: \ no one does".replace("minus ", "{-}"), font_size=18, color=GRID),
            label(r"everything: \ both invest \\ only when it is good", font_size=18, color=RECEIVER),
            label(rf"best: \ recommend investing \\ always when good, \ and \\ {100 * D['recommend_bad']:.0f}\% of the "
                  r"time \\ when bad", font_size=18, color=SENDER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Three policies. <bookmark mark='a'/> Tell them nothing, and each sees a project worth "
            f"{say_num(D['pool_payoff'], 1)} on average even if the other invests: nobody invests. <bookmark "
            f"mark='b'/> Tell them everything, and both invest when the project is good: {D['full']:.1f} "
            "investors on average. <bookmark mark='c'/> The best design does twice as well. It sends both "
            "investors the same recommendation: invest whenever the project is good, and also "
            f"{100 * D['recommend_bad']:.0f} percent of the time when it is bad. An investor told to invest knows "
            "the project is good with just enough probability, and knows the other was told the same, so "
            f"following the advice pays. Expected investment: {D['best']:.1f}."
        ) as vo:
            self.play(FadeIn(ax))
            for mk, b, s_ in zip("abc", bars, side):
                vo.wait_until(mk)
                self.play(FadeIn(b, shift=UP * 0.1), FadeIn(s_))
        self.clear_scene()

    def bce(self):
        rows = VGroup(
            label(r"recommend an action to each player, \ depending on the state", font_size=23, color=SENDER),
            label(r"obedience: \ given what the recommendation reveals, \ following it is best", font_size=23,
                  color=RECEIVER),
            label(r"every such rule is a Bayes correlated equilibrium, \ found by a linear programme", font_size=23,
                  color=THEORY),
            label(r"with no state, \ it is Aumann's correlated equilibrium of Part 11", font_size=23,
                  color=GREY_A),
            label(r"the same arithmetic designs stress-test disclosures, \ ratings and alerts", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"Bayes correlated equilibrium", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "The general method has a simple shape. <bookmark mark='a'/> Think of any information policy as "
            "recommending an action to each player, depending on the state. <bookmark mark='b'/> It works only if "
            "it is obedient: given what the recommendation reveals about the state and about what the others were "
            "told, each player wants to follow it. <bookmark mark='c'/> Bergemann and Morris called the "
            "outcomes Bayes correlated equilibria; finding the best one is a linear programme, which is how the "
            "numbers here were computed. <bookmark mark='d'/> Without a state, it is Robert Aumann's correlated "
            "equilibrium from Part eleven. <bookmark mark='e'/> The same arithmetic is used to think about what "
            "regulators should disclose about banks' stress tests, how ratings should be designed, and when "
            "alerts should sound."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
