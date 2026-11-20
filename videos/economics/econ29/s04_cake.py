from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Cake(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Dynamic programming: \ the cake", r"How do you solve a problem that never ends?",
             "Chapter three. Dynamic programming: the cake.", lit={1957: r"Bellman"}, scale=("person",),
             horizon=("a day", "for ever"))
        self.problem()
        self.bellman()
        self.solve()
        self.path_()

    def problem(self):
        K = load("cake")
        cake = VGroup(Circle(radius=1.3, stroke_color=E.ACCENT, stroke_width=3, fill_color=E.ACCENT,
                             fill_opacity=0.35)).move_to(LEFT * 4.2 + DOWN * 0.2)
        cap = label(r"a cake of size $w = 1$", font_size=22, color=E.ACCENT).next_to(cake, DOWN, buff=0.3)
        eq = MathTex(r"\max_{c_0, c_1, \dots}\ \sum_{t=0}^{\infty} \beta^t \log c_t", r"\quad\text{subject to}\quad",
                     r"\sum_{t=0}^{\infty} c_t \le w", font_size=34).move_to(RIGHT * 1.6 + UP * 1.6)
        side = VGroup(
            label(r"eat some today, \ save the rest for tomorrow, \ for ever", font_size=21, color=GREY_A),
            label(rf"patience $\beta = {K['beta']}$: \ tomorrow's slice is worth {K['beta']} of today's",
                  font_size=21, color=VALUE),
            label(r"$\log$: \ the first bite of the day is worth the most, \\ and a day with nothing is a disaster",
                  font_size=21, color=GREY_A),
            label(r"infinitely many choices at once: \ too many to search", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(eq, DOWN, buff=0.6)
        if side.get_right()[0] > 7.0:
            side.shift(LEFT * (side.get_right()[0] - 6.95))
        tag = island_tag(corner=DR, font_size=14)
        head = label(r"a small problem that contains the whole method", font_size=26, color=E.ACCENT).to_edge(
            UP, buff=0.35)
        with self.voiceover(
            "Before an economy with shocks, a much smaller problem, which contains the whole method. "
            "<bookmark mark='a'/> You have a cake of size one, and it has to last for ever. <bookmark mark='b'/> "
            "Each day you choose how much to eat, and you want to make the discounted sum of your enjoyment as large "
            "as possible, subject to never eating more cake than there is. <bookmark mark='c'/> Eat some today, and "
            f"save the rest. <bookmark mark='d'/> Your patience is {K['beta']}: a slice tomorrow is worth "
            f"{K['beta']} of the same slice today. <bookmark mark='e'/> Enjoyment is the logarithm of what you eat, "
            "so the first bite of a day is worth the most, and a day with nothing at all is a disaster. "
            "<bookmark mark='f'/> Written like this, it is a choice of infinitely many numbers at once, far too many "
            "to search."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromCenter(cake), FadeIn(cap), FadeOut(head))
            vo.wait_until("b")
            self.play(Write(eq), run_time=1.5)
            for mk, r_ in zip("cdef", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def bellman(self):
        eq = MathTex(r"V(w)", r"=", r"\max_{0 < c \le w}", r"\Big\{", r"\log c", r"+", r"\beta\, V(w - c)",
                     r"\Big\}", font_size=46).move_to(UP * 1.9)
        eq[0].set_color(VALUE)
        eq[4].set_color(E.ACCENT)
        eq[6].set_color(VALUE)
        b1 = Brace(eq[4], DOWN, color=E.ACCENT)
        t1 = label(r"today", font_size=20, color=E.ACCENT).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(eq[6], DOWN, color=VALUE)
        t2 = label(r"everything after, \\ at its best", font_size=20, color=VALUE).next_to(b2, DOWN, buff=0.1)
        quote = VGroup(
            label(r"Richard Bellman, \ \emph{Dynamic Programming}, \ 1957: \ the principle of optimality", font_size=21,
                  color=E.ACCENT),
            label(r"``An optimal policy has the property that whatever the initial state and initial decision are, "
                  r"\\ the remaining decisions must constitute an optimal policy \ with regard to the state resulting "
                  r"from the first decision.''", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 1.6)
        if quote.width > 13.0:
            quote.width = 13.0
        side = label(r"one choice, \ one number, \ and an unknown function on both sides", font_size=22,
                     color=HOLD).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Bellman, \ \emph{Dynamic Programming} (1957), \ ch.\ 3", corner=DR, font_size=12)
        head = label(r"Bellman's trick: \ one day at a time", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Richard Bellman's trick, from the 1950s, is to stop thinking about the whole path. "
            "<bookmark mark='a'/> Let V of w be the best you can do, in total, starting with a cake of size w. "
            "Then V of w is the best choice of today's slice, c, of today's enjoyment, <bookmark mark='b'/> plus "
            "beta times the best you can do from tomorrow on, starting with what is left, w minus c. "
            "<bookmark mark='c'/> That is the Bellman equation. It rests on what Bellman called the principle of "
            "optimality: whatever you do today, an optimal plan must behave optimally from tomorrow on, given where "
            "today left you. <bookmark mark='d'/> The infinite choice has become one choice and one number, at the "
            "price of an unknown function, V, that appears on both sides."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq[:5]), GrowFromCenter(b1), FadeIn(t1), FadeOut(head), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(eq[5:]), GrowFromCenter(b2), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(quote, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.clear_scene()

    def solve(self):
        K = load("cake")
        b = K["beta"]
        steps = VGroup(
            MathTex(r"\text{guess: } V(w) = a + b \log w", font_size=34),
            MathTex(r"\text{first-order condition: } \frac{1}{c} = \frac{\beta b}{w - c}"
                    r"\quad\Rightarrow\quad c = \frac{w}{1 + \beta b}", font_size=34),
            MathTex(r"\text{match the }\log w\text{ terms: } b = 1 + \beta b \quad\Rightarrow\quad "
                    r"b = \frac{1}{1-\beta}", font_size=34),
            MathTex(r"c = (1-\beta)\, w", font_size=44, color=POLICY),
            label(rf"with $\beta = {b}$: \ eat {100 * (1 - b):.0f}\% of whatever is left, \ every day", font_size=25,
                  color=POLICY),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "For this problem the unknown function can be found by hand. <bookmark mark='a'/> Guess that V is a "
            "constant plus some number b times the log of the cake. <bookmark mark='b'/> Then today's choice must "
            "balance the last bite eaten today, one over c, against the value of saving it, beta b over what is "
            "left. That gives c as w over one plus beta b. <bookmark mark='c'/> Put this back into the equation and "
            "match the terms in log w on both sides: b must equal one plus beta b, so b is one over one minus "
            "beta. <bookmark mark='d'/> And the rule is beautifully simple: eat one minus beta of whatever is left. "
            f"<bookmark mark='e'/> With patience {b}, eat {100 * (1 - b):.0f} percent of the cake every day, for "
            "ever. The rule is a policy function: it tells you what to do in every state you could find yourself in, "
            "not just along one path."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def path_(self):
        K = load("cake")
        b = K["beta"]
        days = np.arange(0, 21)
        left = b ** days
        eat = (1 - b) * left
        ax = plane([-0.5, 20.5], [0, 1.05], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"day",
                   ylabel=r"cake", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=15)
        bars, slices = VGroup(), VGroup()
        for d, l_, e in zip(days, left, eat):
            p0, p1 = ax.ax.c2p(d - 0.32, 0), ax.ax.c2p(d + 0.32, l_)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=E.ACCENT, fill_opacity=0.35,
                               stroke_width=0).move_to((p0 + p1) / 2))
            q1 = ax.ax.c2p(d + 0.32, e)
            slices.add(Rectangle(width=q1[0] - p0[0], height=q1[1] - p0[1], fill_color=POLICY, fill_opacity=0.95,
                                 stroke_width=0).move_to((p0 + q1) / 2))
        side = VGroup(
            label(r"pale: \ cake at the start of the day", font_size=19, color=E.ACCENT),
            label(rf"bright: \ eaten that day, \ {100 * (1 - b):.0f}\% of it", font_size=19, color=POLICY),
            label(rf"after 20 days: \ {left[-1]:.2f} left", font_size=19, color=GREY_A),
            label(r"never all gone: \\ the cake shrinks by a tenth \\ a day, \ for ever", font_size=19,
                  color=VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the plan in action. <bookmark mark='a'/> The pale bars are the cake at the start of each day. "
            f"<bookmark mark='b'/> The bright ones are what you eat: {100 * (1 - b):.0f} percent of it. "
            f"<bookmark mark='c'/> After twenty days, {left[-1]:.2f} of the cake remains. "
            "<bookmark mark='d'/> It never runs out: it shrinks by a tenth a day, for ever, and consumption shrinks "
            "with it. Most problems in this part cannot be solved by hand, so the next chapter does it the way a "
            "computer does, and the cake is the test that the computer gets right."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars], lag_ratio=0.08), FadeIn(side[0]),
                      run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in slices], lag_ratio=0.08), FadeIn(side[1]),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
