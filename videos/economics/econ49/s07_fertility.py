from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403

SERIES_COLS = {"World": WHITE, "China": "#F25F5C", "South Korea": "#C9A0FF", "India": "#F2C14E",
               "United States": "#7EC8F5", "Japan": "#7FD1B9"}


class Fertility(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Children: \ how many, \ and how much for each", r"Why do richer families have fewer "
             r"children?", "Chapter six. Children: how many, and how much for each.",
             lit={1973: r"Becker and Lewis", 1998: r"Angrist and Evans", 2002: r"Goldin and Katz"},
             scale=("household", "nation"), horizon=("a decade", "a century"))
        self.quality()
        self.record()
        self.siblings()
        self.pill()

    def quality(self):
        Q = load("qq")
        w = np.array(Q["wage"])
        ax = plane([0, 3.1], [0, 6], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[0, 1, 2, 3], yticks=[0, 2, 4, 6], xlabel=r"the mother's wage", ylabel=r"children",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        n = path(ax, w, Q["n"], CHILD, 3.4)
        q = path(ax, w, 10 * np.array(Q["q"]), SCHOOL, 3.4)
        eq = MathTex(r"\max\; \log c + a \log n + b \log q \quad \text{s.t.} \quad c + n\,(\pi + q) = Y",
                     font_size=30, color=THEORY).to_edge(UP, buff=0.5)
        side = VGroup(
            label(r"each child costs time \\ (at the mother's wage) \\ and goods, \ $\pi$", font_size=17,
                  color=WHITE),
            label(r"gold: \ the number \\ of children", font_size=17, color=CHILD),
            label(r"green: \ spending on \\ each child \ (times 10)", font_size=17, color=SCHOOL),
            label(r"quality makes quantity \\ dearer, \ and quantity \\ makes quality dearer", font_size=17,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Why do richer families, and richer countries, have fewer children? Becker's answer, with Gregg Lewis, "
            "was that parents choose both how many children to have and how much to spend on each, their "
            "quality, in the economist's cold word. <bookmark mark='a'/> A child costs goods, and time, valued at "
            "the wage of the parent who gives it, most often the mother. <bookmark mark='b'/> As her wage rises, "
            f"each child costs more, and the number of children falls, here from {Q['n'][0]:.1f} to "
            f"{Q['n'][-1]:.1f}. <bookmark mark='c'/> Spending on each child rises. <bookmark mark='d'/> The two "
            "choices feed each other: spending more on each child makes another child dearer, since it too would "
            "get that spending, and fewer children make spending on each one cheaper. Small changes in wages can "
            "start a large shift, from many children with little each to few with much."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(n), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(q), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(VGroup(n, q), color=WHITE))
        self.clear_scene()

    def record(self):
        F = load("fertility")
        T = tables.FERTILITY_49.data
        ax = plane([1950, 2025], [0, 7], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.8, y_length=4.4,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0, 1, 2, 3, 4, 5, 6, 7], ylabel=r"children per woman",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        lines = {}
        for e, d in F["series"].items():
            lines[e] = path(ax, d["year"], d["value"], SERIES_COLS[e], 3.4 if e in ("China", "World") else 2.4,
                            smooth=False)
        rep = DashedLine(ax.ax.c2p(1950, 2.1), ax.ax.c2p(2025, 2.1), color=GREY_B, stroke_width=1.4)
        rep_l = label(r"2.1: \ replacement", font_size=14, color=GREY_B).next_to(ax.ax.c2p(2025, 2.1), UP, buff=0.05)
        rep_l.shift(LEFT * 0.8)
        pol = vline(ax, T["one_child"], 0, 7, LOSS)
        pol_l = label(r"1980: \ one child", font_size=15, color=LOSS).next_to(ax.ax.c2p(T["one_child"], 6.8), RIGHT,
                                                                             buff=0.08)
        keys = VGroup(*[label(e, font_size=15, color=c) for e, c in SERIES_COLS.items()]).arrange(DOWN,
                                                                                                aligned_edge=LEFT,
                                                                                                buff=0.12)
        side = VGroup(
            keys,
            label(rf"China: \ {F['china_1970']:.1f} in 1970, \\ {F['china_1979']:.1f} in 1979, \\ before the "
                  rf"policy; \\ {F['china_last']:.1f} in {F['last_year']}", font_size=17, color=SERIES_COLS["China"]),
            label(rf"South Korea, \ no such \\ policy: \ {F['korea_last']:.2f}", font_size=17,
                  color=SERIES_COLS["South Korea"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"UN World Population Prospects, \ via Our World in Data", corner=DL, font_size=12)
        with self.voiceover(
            "Here is the record. <bookmark mark='a'/> Children per woman since 1950: the world's average fell from "
            f"{F['world_first']:.1f} to {F['world_last']:.1f}. <bookmark mark='b'/> China is the famous case, "
            "because of its one-child policy of 1980. But look where China's line was by then. It had already "
            f"fallen from {F['china_1970']:.1f} children in 1970 to {F['china_1979']:.1f} in 1979, during a "
            "campaign for later marriage, longer gaps and fewer children, and as incomes and schooling rose. "
            f"<bookmark mark='c'/> Today it is {F['china_last']:.1f}. <bookmark mark='d'/> South Korea, which never "
            f"had a one-child rule, is at {F['korea_last']:.2f}, the lowest in the world. Japan and the United "
            "States are below replacement too. The policy surely mattered; but the fall that Becker's model "
            "predicts as women's time grows dearer went on everywhere, with or without it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(rep), FadeIn(rep_l), FadeIn(keys), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(lines["World"]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(lines["China"]), Create(pol), FadeIn(pol_l), run_time=2.5)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines["India"]), Create(lines["Japan"]), Create(lines["United States"]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(lines["South Korea"]), FadeIn(side[2]), run_time=2.0)
        self.clear_scene()

    def siblings(self):
        A = load("angrist")
        W = A["wald"]
        by = A["by"]
        ax = plane([-0.5, 2.5], [0, 0.5], center=LEFT * 3.4 + DOWN * 0.4, x_length=5.2, y_length=4.2, xticks=[],
                   yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], ylabel=r"had a third child", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        bars = VGroup()
        for i, (nm, col) in enumerate((("two boys", MEN), ("two girls", WOMEN), ("a boy and a girl", GREY_B))):
            v = by[nm]["third"]
            p0, p1 = ax.ax.c2p(i - 0.32, 0), ax.ax.c2p(i + 0.32, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(rf"{100 * v:.1f}\%", font_size=15, color=WHITE).next_to(r, UP, buff=0.05),
                            label(nm.replace("a boy and a girl", r"a boy and \\ a girl"), font_size=15,
                                  color=col).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.15)))
        steps = VGroup(
            label(rf"{A['n']:,} mothers, \ 1980 census".replace(",", "{,}"), font_size=19, color=WHITE),
            label(rf"same sex: \ {100 * W['first_stage']:.1f} points more \\ likely to have a third", font_size=19,
                  color=CHILD),
            label(rf"and they worked {abs(W['reduced_form']):.2f} weeks \\ less in 1979", font_size=19,
                  color=WOMEN),
            MathTex(rf"\frac{{{W['reduced_form']:.2f}}}{{{W['first_stage']:.3f}}} = {W['wald']:.1f}"
                    r"\ \text{weeks}", font_size=34, color=E.ACCENT),
            label(rf"a third child: \ about {abs(W['wald']):.0f} weeks less work a year \\ (s.e. {W['se']:.1f} in "
                  r"this sample)", font_size=18, color=E.ACCENT),
            label(r"Angrist and Evans, \ all 250{,}000: \ real, \\ but smaller than the naive comparison, "
                  r"\\ and absent for more educated women", font_size=17, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 2.8)
        tag = data_tag(r"Angrist and Evans (1998): \ 1980 US Census, \ AER's subsample", corner=DL, font_size=12)
        with self.voiceover(
            "Do children reduce their mothers' work, or do women who plan to work less have more children? Joshua "
            "Angrist and William Evans found a lever chosen by nature. <bookmark mark='a'/> Here are "
            f"{A['n']:,} American mothers of at least two children in 1980. <bookmark mark='b'/> Parents of two "
            "boys or two girls are more likely to try for a third than parents of one of each: "
            f"{100 * by['two boys']['third']:.0f} and {100 * by['two girls']['third']:.0f} percent against "
            f"{100 * by['a boy and a girl']['third']:.0f}. And the sexes of the first two children are as good as "
            f"random. <bookmark mark='c'/> So same-sex mothers had a third child "
            f"{100 * W['first_stage']:.1f} points more often, <bookmark mark='d'/> and worked "
            f"{abs(W['reduced_form']):.2f} weeks less in 1979. <bookmark mark='e'/> Divide one by the other: a "
            f"third child cut its mother's work by about {abs(W['wald']):.0f} weeks a year. <bookmark mark='f'/> "
            f"In this sample of thirty thousand the estimate is noisy, with a standard error of {W['se']:.1f} "
            "weeks. With all a quarter of a million, Angrist and Evans found the effect real but smaller than "
            "the naive comparison suggests, and absent for more educated women."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(steps[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(VGroup(b[1], b[2])) for b in bars], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(VGroup(bars[0], bars[1]), color=WHITE, scale_factor=1.04), run_time=1.2)
            self.play(Indicate(bars[2], color=WHITE, scale_factor=1.04), run_time=1.0)
            for mk, r_ in zip("cdef", steps[1:5]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
            self.play(FadeIn(steps[5]))
        self.clear_scene()

    def pill(self):
        chain = flow_chain([(r"the 1960s: \\ the pill", CHILD), (r"states lower the \\ age of majority", WOMEN),
                            (r"young single women \\ can get it", WOMEN),
                            (r"later marriage, \\ more law and \\ medical school", GAIN)],
                           notes=[r"reliable, \ and \\ in the woman's hands", r"to 18 or 21, \ state \\ by state",
                                  r"plans that take \\ years become safe", r"Goldin and Katz"], box_w=2.9,
                           font_size=19, note_size=17).move_to(UP * 0.8)
        foot = label(r"a technology that lowered the cost of planning a career", font_size=24,
                     color=E.ACCENT).to_edge(DOWN, buff=1.2)
        tag = published_tag(r"Goldin and Katz, \ JPE (2002)", corner=DR, font_size=11)
        with self.voiceover(
            "One more lever changed the price of children. <bookmark mark='a'/> The pill, from the 1960s, put "
            "reliable contraception in women's hands. <bookmark mark='b'/> At first many states denied it to young "
            "unmarried women, until they lowered the age of majority, at different times. <bookmark mark='c'/> "
            "Claudia Goldin and Lawrence Katz used those differences. <bookmark mark='d'/> Where young single women "
            "could get the pill earlier, they married later and entered law and medical schools in larger numbers: "
            "careers that take years of training became safe to plan. <bookmark mark='e'/> In Becker's terms, a "
            "new technology lowered the cost of controlling the timing of children, and with it the cost of a "
            "career."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]), Indicate(chain.boxes[0], color=WHITE, scale_factor=1.04))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
