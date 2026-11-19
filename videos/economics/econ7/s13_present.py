from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403


class Present(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Present bias", r"Why do plans for saving and dieting so often fail when the day comes?",
             "Chapter eleven. Present bias.", lit={1955: r"Strotz on inconsistency"}, horizon=("a day", "a year"))
        self.thaler()
        self.reversal()
        self.store()
        self.commitment()

    def thaler(self):
        p = load("present")
        th = p["thaler"]
        head = label(r"Thaler (1981): \ how much later would make up for \$15 now?", font_size=32,
                     color=E.ACCENT).to_edge(UP, buff=0.5)
        cols = VGroup()
        for m, eq, rate in zip(th["months"], th["median_equivalent"], p["rates"]):
            when = {1: r"in a month", 12: r"in a year", 120: r"in ten years"}[m]
            cols.add(VGroup(label(when, font_size=27, color=GREY_A), label(rf"\${eq}", font_size=44, color=TODAY),
                            label(rf"{100 * rate:.0f}\% a year", font_size=30, color=BIAS)).arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=1.6).next_to(head, DOWN, buff=0.8)
        lab = VGroup(label(r"median answer", font_size=21, color=GREY_B).next_to(cols[0][1], LEFT, buff=0.6),
                     label(r"implied rate", font_size=21, color=GREY_B).next_to(cols[0][2], LEFT, buff=0.6))
        foot = VGroup(
            label(r"exponential discounting would give one rate for all three", font_size=27),
            label(r"instead the rate falls with the delay: \ impatience is concentrated in the near future",
                  font_size=27, color=BIAS),
        ).arrange(DOWN, buff=0.25).next_to(cols, DOWN, buff=0.7)
        tag = published_tag(r"Thaler, Economics Letters (1981), via Frederick, Loewenstein and O'Donoghue, JEL (2002), "
                            r"p.\ 360", corner=DR, font_size=13)
        with self.voiceover(
            "In 1981 Richard Thaler asked people a simple question: if you've won fifteen dollars, how much would you "
            "need to get instead, later, to be just as happy? <bookmark mark='a'/> The median answers: twenty dollars "
            "in a month, fifty in a year, a hundred in ten years. <bookmark mark='b'/> Turn those into annual "
            "interest rates: three hundred and forty-five percent for the month, a hundred and twenty for the year, "
            "nineteen for the decade. <bookmark mark='c'/> Exponential discounting would give the same rate for all "
            "three. Instead, the rate falls as the delay grows. People are hugely impatient about the near future, "
            "and much more patient about the far future."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c[0]), FadeIn(c[1])) for c in cols], lag_ratio=0.5),
                      FadeIn(lab[0]), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c[2]) for c in cols], lag_ratio=0.5), FadeIn(lab[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def reversal(self):
        th = tables.THALER_1981.data
        today = VGroup(lottery_card([(r"today", r"\$100")], r"A", color=TODAY, width=3.0, font_size=28),
                       label(r"or", font_size=28, color=GREY_B),
                       lottery_card([(r"tomorrow", r"\$110")], r"B", color=LATER, width=3.0, font_size=28)).arrange(
            RIGHT, buff=0.5)
        later = VGroup(lottery_card([(r"in 30 days", r"\$100")], r"A$'$", color=TODAY, width=3.0, font_size=28),
                       label(r"or", font_size=28, color=GREY_B),
                       lottery_card([(r"in 31 days", r"\$110")], r"B$'$", color=LATER, width=3.0, font_size=28)).arrange(
            RIGHT, buff=0.5)
        VGroup(today, later).arrange(DOWN, buff=0.7).to_edge(LEFT, buff=0.7).shift(UP * 0.4)
        pick1 = SurroundingRectangle(today[0], color=WHITE, buff=0.08)
        pick2 = SurroundingRectangle(later[2], color=WHITE, buff=0.08)
        side = VGroup(
            label(r"many people choose A today, \\ and B$'$ a month ahead", font_size=26),
            label(r"the same one-day wait, \ two answers", font_size=25, color=BIAS),
            label(r"in 30 days the B$'$-chooser becomes \\ an A-chooser: \ the plan is broken", font_size=24),
            label(r"Strotz (1955--56): \ with any discounting \\ but exponential, \ today's self and \\ tomorrow's "
                  r"disagree", font_size=23, color=GREY_A),
            MathTex(r"1,\;\; \beta\delta,\;\; \beta\delta^2,\;\; \beta\delta^3,\;\ldots", font_size=38, color=BIAS),
            label(r"beta--delta (Laibson, 1997): \ $\beta < 1$ \\ is a one-off discount on everything \\ that isn't now",
                  font_size=23, color=BIAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The consequence is the preference reversal. <bookmark mark='a'/> A hundred dollars today or a hundred and "
            "ten tomorrow? Many people take the hundred today. A hundred in thirty days or a hundred and ten in "
            "thirty-one? Many of the same people wait for the hundred and ten. <bookmark mark='b'/> It's the same "
            "one-day wait, for the same ten dollars. <bookmark mark='c'/> But in thirty days, the person who chose "
            "to wait will face the first choice, and take the hundred. Their plan breaks. "
            "<bookmark mark='d'/> Robert Strotz showed in 1955 that this happens with any discounting except the "
            "exponential: today's self and tomorrow's self disagree, and each knows it. <bookmark mark='e'/> The "
            "simplest model of it is beta-delta: full weight on now, and everything later discounted by an extra "
            "factor beta. <bookmark mark='f'/> David Laibson made it a workhorse in 1997. Beta below one is a one-off "
            "penalty on everything that isn't now."
        ) as vo:
            self.play(FadeIn(today), FadeIn(later))
            vo.wait_until("a")
            self.play(Create(pick1), Create(pick2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def store(self):
        p = load("present")
        T = p["weeks"]
        ax = plane([0.4, T + 0.6], [0, 80], center=LEFT * 2.6 + DOWN * 0.3, x_length=7.2, y_length=5.0,
                   xticks=list(range(1, T + 1)), yticks=[0, 20, 40, 60, 80], xlabel=r"week of the dry season",
                   ylabel=r"coconuts eaten", font_size=17)
        a = ax.ax

        def barset(vals, color, dx):
            g = VGroup()
            for k, v in enumerate(vals):
                h = a.c2p(0, v)[1] - a.c2p(0, 0)[1]
                g.add(Rectangle(width=0.32, height=h, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to(
                    a.c2p(k + 1, 0) + RIGHT * dx, aligned_edge=DOWN))
            return g

        plan = barset(p["plan"], LATER, -0.18)
        did = barset(p["naive"], BIAS, 0.18)
        leg = VGroup(label(r"the plan made in week 1", font_size=20, color=LATER),
                     label(r"what each week's Chidi eats", font_size=20, color=BIAS)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(a.c2p(T + 0.5, 80), DL, buff=0.05)
        side = VGroup(
            label(rf"Chidi's store: \ {p['store']:.0f} coconuts for {T} weeks", font_size=25),
            label(rf"beta--delta with $\beta = {p['beta']}$, \ $\delta = 1$, \ log utility", font_size=23,
                  color=GREY_A),
            label(rf"week 1's plan: \ {p['plan'][0]:.1f} now, \\ then {p['plan'][1]:.1f} a week", font_size=24,
                  color=LATER),
            label(r"but each week's Chidi is a new ``now'': \\ he eats more than was planned for him", font_size=24,
                  color=BIAS),
            label(rf"the last week: \ {p['naive'][-1]:.1f} coconuts, \ not {p['plan'][-1]:.1f}", font_size=24,
                  color=BIAS),
            label(r"with log utility, knowing it makes no difference \\ (Pollak, 1968)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "What does present bias do to a plan? <bookmark mark='a'/> Chidi has three hundred coconuts to last the "
            "six weeks of the dry season. Give him a beta of nought point seven, no other discounting, and logarithmic "
            "utility. <bookmark mark='b'/> In week one he plans to eat sixty-seven coconuts now, and then, since all "
            "the later weeks look alike to him from here, forty-seven in each. <bookmark mark='c'/> But in week two, "
            "week two is now. The extra weight that week one gave itself, week two gives itself, and he eats "
            "sixty-one, not forty-seven. Week three eats fifty-five, and so on down. <bookmark mark='d'/> In the last "
            "week there are twenty-eight coconuts left instead of the forty-seven his first self planned. "
            "<bookmark mark='e'/> Would it help if he knew his later selves would do this? With logarithmic utility, "
            "Robert Pollak showed in 1968, it makes no difference to what he eats. With other utilities, knowing can "
            "make it better or worse."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in plan], lag_ratio=0.2), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in did], lag_ratio=0.4), FadeIn(leg[1]),
                      FadeIn(side[3]), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(side[4]), Indicate(did[-1], color=WHITE))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def commitment(self):
        p = load("present")
        hc = history_card(r"commitment", r"Dara's locked store", r"Chidi puts the coconuts in a box that opens a week's "
                          r"share at a time: \ the plan of week 1, \ enforced", color=LATER, width=9.0,
                          font_size=25).move_to(UP * 1.9)
        rows = VGroup(
            label(rf"week 1's Chidi would give up {100 * p['commit_worth']:.1f}\% of the whole store for the box",
                  font_size=27, color=E.ACCENT),
            label(r"a demand for commitment: \ something expected utility with exponential discounting \\ can never "
                  r"produce, \ since it never wants fewer options", font_size=24),
            label(r"Laibson (1997), \ ``Golden Eggs'': \ illiquid saving, \ a house, \ a pension, \ as the box",
                  font_size=24, color=GREY_A),
            label(r"how big is $\beta$? \ meta-analysis: \ about 0.95--0.97 once publication bias is removed \\ "
                  r"(Imai, Rutter and Camerer, 2021): \ smaller than our 0.7, \ not negligible", font_size=23,
                  color=BIAS),
            label(r"behavioural economics, \ Part 45, \ takes it further", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(hc, DOWN, buff=0.45)
        tag = published_tag(r"Imai et al.\ (2021), via Elminejad, Havranek and Irsova (2025)", corner=DR, font_size=13)
        with self.voiceover(
            "Present bias creates something expected utility with exponential discounting never can: a demand for "
            "commitment. <bookmark mark='a'/> Suppose Dara offers a locked box that releases one week's share at a "
            "time, enforcing week one's plan. <bookmark mark='b'/> Week one's Chidi would give up almost three percent "
            "of the whole store to have it. A chooser who never disagrees with his future self never wants fewer "
            "options; Chidi does. <bookmark mark='c'/> Laibson's paper was called Golden Eggs: illiquid assets, a "
            "house, a pension that can't be touched, work as the box. <bookmark mark='d'/> How large is beta, really? "
            "A meta-analysis by Taisuke Imai, Tom Rutter and Colin Camerer put it at about nought point nine five to "
            "nought point nine seven once publication bias is removed: much closer to one than the illustration here, "
            "but not negligible when it applies every single day. <bookmark mark='e'/> Part forty-five comes back to "
            "it, and chapter fourteen shows what pension design has done with it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0], shift=UP * 0.1))
            self.play(FadeIn(rows[1], shift=UP * 0.1))
            for mk, r_ in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
