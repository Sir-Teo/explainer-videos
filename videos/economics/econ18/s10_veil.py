from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


def society(incomes, name, color, w=4.6):
    people = VGroup()
    for y in incomes:
        p = person(0.55 + 0.016 * y, color=color)
        people.add(VGroup(p, label(rf"{y:.0f}", font_size=20, color=WHITE).next_to(p, DOWN, buff=0.08)))
    people.arrange(RIGHT, buff=0.28, aligned_edge=DOWN)
    box = RoundedRectangle(width=w, height=people.height + 1.0, corner_radius=0.15, stroke_color=color,
                           stroke_width=2)
    people.move_to(box).shift(DOWN * 0.15)
    return VGroup(box, people, label(name, font_size=22, color=color).next_to(box, UP, buff=0.1))


class Veil(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Two veils: \ Harsanyi and Rawls", r"If you didn't know who you would be, \ which society would "
             r"you choose?", "Chapter eight. Two veils: Harsanyi and Rawls.",
             lit={1955: r"Harsanyi", 1971: r"Rawls", 1975: r"Harsanyi's critique"}, scale=("person", "nation"),
             horizon=("a lifetime",))
        self.idea()
        self.choice()
        self.debate()

    def idea(self):
        rows = VGroup(
            label(r"choose the rules of a society \ before you know who in it you will be", font_size=25),
            label(r"John Harsanyi, \ 1953 and 1955: \ any member, \ with equal chance", font_size=24, color=HARS),
            label(r"a rational chooser maximizes expected utility, \ which is average utility: \ Bentham's sum, "
                  r"\ derived", font_size=23, color=HARS),
            label(r"John Rawls, \ 1971: \ behind the veil you would not gamble with your one life", font_size=24,
                  color=RAWLS),
            label(r"you would secure the worst position: \ the difference principle", font_size=23, color=RAWLS),
            label(r"the same thought experiment, \ two answers", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Harsanyi, JPE 61(5) (1953) and 63(4) (1955); \ Rawls, \emph{A Theory of Justice} "
                            r"(1971)", corner=DR, font_size=12)
        with self.voiceover(
            "Two philosophers proposed the same test for fairness. <bookmark mark='a'/> Choose the rules of a society "
            "before you know who in it you will be. <bookmark mark='b'/> The economist John Harsanyi, in 1953 and "
            "1955, said: behind that veil you are equally likely to be anyone. <bookmark mark='c'/> A rational "
            "chooser maximizes expected utility, and with equal chances, expected utility is average utility. "
            "Bentham's sum falls out of prudence. <bookmark mark='d'/> John Rawls, in 1971, said that behind the "
            "veil, choosing the basic structure of the society you must live in for life, you would not gamble. "
            "<bookmark mark='e'/> You would make the worst position as good as possible. Inequalities are just only "
            "if they benefit the least advantaged: the difference principle. "
            "<bookmark mark='f'/> The same thought experiment gave two answers."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def choice(self):
        v = load("veil")
        eps = np.array(v["eps"])
        a = society(v["A"], r"society A: \ equal", RAWLS).move_to(LEFT * 3.6 + UP * 2.0)
        b = society(v["B"], r"society B: \ richer, \ one left behind", HARS).move_to(RIGHT * 3.6 + UP * 2.0)
        means = VGroup(label(rf"mean {v['mean_A']:.0f}, \ minimum {min(v['A']):.0f}", font_size=19,
                             color=GREY_A).next_to(a, DOWN, buff=0.1),
                       label(rf"mean {v['mean_B']:.1f}, \ minimum {min(v['B']):.0f}", font_size=19,
                             color=GREY_A).next_to(b, DOWN, buff=0.1))
        ax = plane([0, 8], [0, 30], center=DOWN * 1.75 + LEFT * 1.5, x_length=7.2, y_length=2.9,
                   xticks=[0, 2, 4, 6, 8], yticks=[0, 10, 20, 30], xlabel=r"inequality aversion behind the veil \ "
                   r"$\varepsilon$", ylabel=r"equally distributed equivalent", font_size=17)
        ca = path(ax, eps, v["ede_A"], color=RAWLS, width=4, smooth=False)
        cb = path(ax, eps, v["ede_B"], color=HARS, width=4)
        cross = VGroup(DashedLine(ax.ax.c2p(v["cross"], 0), ax.ax.c2p(v["cross"], 30), color=E.ACCENT,
                                  stroke_width=2),
                       label(rf"$\varepsilon \approx {v['cross']:.1f}$", font_size=19,
                             color=E.ACCENT).next_to(ax.ax.c2p(v["cross"], 30), RIGHT, buff=0.08))
        verdict = VGroup(
            label(r"Rawls: \ A, \ whatever $\varepsilon$", font_size=21, color=RAWLS),
            label(rf"Harsanyi: \ B below {v['cross']:.1f}, \ A above", font_size=21, color=HARS),
            label(r"the veils differ by one number: \ how much you fear the bottom", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, RIGHT, buff=0.5).shift(UP * 0.3)
        with self.voiceover(
            "Put the two veils to work on two islands of five. <bookmark mark='a'/> In society A, everyone has "
            "twenty baskets. In society B, four have thirty and one has eight: more in total, a mean of twenty-five "
            "point six, but one islander left behind. <bookmark mark='b'/> Rawls chooses A, since its worst "
            "position, twenty, beats eight. <bookmark mark='c'/> Harsanyi's chooser compares expected utilities, and "
            "the answer depends on how fast utility flattens, the epsilon of chapter seven, which here is aversion "
            "to risk behind the veil. <bookmark mark='d'/> Below about one point nine, B's extra income wins; above "
            "it, the risk of being the one with eight dominates, and Harsanyi chooses A too. "
            "<bookmark mark='e'/> So the two veils differ by a single number: how much you fear the bottom."
        ) as vo:
            self.play(FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(FadeIn(means))
            vo.wait_until("b")
            self.play(FadeIn(ax), Indicate(a[0], color=RAWLS), FadeIn(verdict[0]))
            vo.wait_until("c")
            self.play(Create(ca), Create(cb), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(cross[0]), FadeIn(cross[1]), FadeIn(verdict[1]))
            vo.wait_until("e")
            self.play(FadeIn(verdict[2]))
        self.clear_scene()

    def debate(self):
        rows = VGroup(
            label(r"Harsanyi, \ 1975: \ maximin is infinitely risk averse", font_size=24, color=HARS),
            label(r"it would turn down a better life elsewhere for fear of the smallest chance of disaster",
                  font_size=22, color=GREY_A),
            label(r"Rawls: \ the original position is no ordinary gamble", font_size=24, color=RAWLS),
            label(r"it is one choice, \ for life, \ with no probabilities you could trust, \ and it must be lived with",
                  font_size=22, color=GREY_A),
            label(r"in the laboratory, \ groups behind a veil mostly chose the highest average income with a floor",
                  font_size=22, color=WELF),
            label(r"neither pure answer: \ a minimum, \ then growth", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Harsanyi, APSR 69(2) (1975); \ Frohlich and Oppenheimer, \emph{Choosing Justice} "
                            r"(1992)", corner=DR, font_size=12)
        with self.voiceover(
            "The two argued for years. <bookmark mark='a'/> Harsanyi said maximin is infinitely risk averse: "
            "<bookmark mark='b'/> someone who lived by it would turn down a better life elsewhere for fear of the "
            "smallest chance of disaster on the way. <bookmark mark='c'/> Rawls answered that the original position "
            "is no ordinary gamble. <bookmark mark='d'/> It is one choice, made once, for a whole life, with no "
            "probabilities anyone could trust, and its result must be lived with. "
            "<bookmark mark='e'/> When Norman Frohlich and Joe Oppenheimer put groups of students behind a veil "
            "in the laboratory, most groups chose neither rule. They chose the highest average income subject to a "
            "floor. <bookmark mark='f'/> A minimum first, then growth."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
