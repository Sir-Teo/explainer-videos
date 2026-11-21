from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"A consumer has $u(x, y) = 0.4 \ln x + 0.6 \ln y$ and income 100. \ Good $y$ costs 1. \ Good $x$ costs 1 for "
    r"each of the first 20 units and 2 for each unit beyond: \ an increasing block tariff, \ like many "
    r"electricity and water bills.",
    r"(a) \ Find the consumer's demand. \quad (8 marks)",
    r"(b) \ Decompose the effect of a small rise in the second price into substitution and income effects. "
    r"\quad (9 marks)",
    r"(c) \ The second price rises to 2.5. \ Find the compensating variation, \ and compare it with the "
    r"Laspeyres approximation. \quad (8 marks)",
]


class Micro1(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Micro: \ a kinked budget", r"What does a consumer buy when the price changes at 20 units?",
             "Question one. Microeconomics: a kinked budget.", lit={1915: r"Slutsky", 1978: r"Burtless and Hausman"},
             scale=("person", "household"), horizon=("a day",))
        self.statement()
        self.demand()
        self.picture()
        self.slutsky()
        self.welfare()
        self.marks()

    def statement(self):
        paper = exam_paper(1, "micro", r"a kinked budget", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question one. A consumer has Cobb-Douglas utility, 0.4 log x plus 0.6 log y, and an income of 100. "
            "Good y costs one. Good x costs one for each of the first twenty units, and two for each unit beyond: "
            "an increasing block tariff, like many electricity and water bills. <bookmark mark='a'/> Part a: find "
            "the demand. <bookmark mark='b'/> Part b: decompose the effect of a small rise in the second price "
            "into substitution and income effects. <bookmark mark='c'/> Part c: the second price rises to 2.5; "
            "find the compensating variation and compare it with the Laspeyres approximation. This is your turn: "
            "pause, and try part a before the solution."
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 8.0)
        self.clear_scene()

    def demand(self):
        M = load("micro1")
        tag = part_tag(1, "a", "micro")
        rows = steps([
            (rf"\text{{segment 1}}\ (p = 1):\quad x = \frac{{0.4 \times 100}}{{1}} = {M['x_first']:.0f} > 20",
             r"Cobb--Douglas spends 40\% on $x$; \ but this is off the segment"),
            (r"m' = 100 + (2 - 1) \times 20 = 120",
             r"virtual income: \ the straight budget that runs through segment 2"),
            (rf"\text{{segment 2}}\ (p = 2):\quad x = \frac{{0.4 \times 120}}{{2}} = {M['x']:.0f} > 20, \quad "
             rf"y = {M['y']:.0f}", r"on the segment: \ accept", GAIN),
            (r"\text{otherwise: the kink, } x = 20, \ \text{ with } 1 \le \mathrm{MRS} \le 2",
             r"a corner of a convex budget set"),
            (rf"\text{{check: }} 20 \times 1 + {M['x'] - 20:.0f} \times 2 + {M['y']:.0f} = 100",
             r"the budget is spent"),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[2][0])
        with self.voiceover(
            "Part a. A kinked budget has more than one candidate, so check each piece. <bookmark mark='a'/> On the "
            "first segment the price is one, and Cobb-Douglas spends forty percent of income on x: forty units. "
            "But the first segment stops at twenty, so the consumer is not there. <bookmark mark='b'/> The second "
            "segment is part of a straight line with price two that would cut the y axis at 120: the virtual "
            "income, 100 plus the twenty units bought one cheaper than the margin. <bookmark mark='c'/> Against "
            f"that line, demand is 0.4 times 120 over 2: {M['x']:.0f} units of x, which is beyond twenty, so it "
            f"is on the segment, with {M['y']:.0f} of y. That is the answer; box it. <bookmark mark='d'/> Had "
            "both candidates failed, the answer would be the kink itself, twenty units, with a marginal rate of "
            "substitution between the two prices. <bookmark mark='e'/> And check: twenty at one, four at two, "
            "seventy-two of y: exactly 100."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "c":
                    self.play(Create(box))
        self.clear_scene()

    def picture(self):
        M = load("micro1")
        xs, ic, ick = np.array(M["xs"]), np.array(M["ic"]), np.array(M["ic_kink"])
        ax = plane([0, 62], [0, 130], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=5.6,
                   xticks=[0, 20, 40, 60], yticks=[0, 40, 80, 120], xlabel=r"$x$", ylabel=r"$y$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        bud = VGroup(seg(ax, 0, 100, 20, 80, WHITE, 3.5), seg(ax, 20, 80, 60, 0, WHITE, 3.5))
        virt = seg(ax, 0, 120, 20, 80, GREY_B, 2.0, dashed=True)
        icur = path(ax, xs, ic, MICRO, 2.6, yr=(0, 130))
        opt = dot(ax, M["x"], M["y"], MICRO)
        icur_k = path(ax, xs, ick, EST, 2.6, yr=(0, 130))
        kink = dot(ax, 20, 80, EST)
        lab_v = label(r"virtual income 120", font_size=16, color=GREY_B).next_to(ax.ax.c2p(0, 120), RIGHT,
                                                                                    buff=0.15)
        side = VGroup(
            label(r"white: \ the kinked budget", font_size=19, color=WHITE),
            label(r"dashed: \ segment 2 extended", font_size=19, color=GREY_B),
            label(rf"blue: \ $\alpha = 0.4$, \ at $({M['x']:.0f}, {M['y']:.0f})$", font_size=19, color=MICRO),
            label(rf"gold: \ $\alpha = 0.3$, \ at the kink: \\ MRS {M['kink_case']['mrs']:.2f}, \ between 1 and 2",
                  font_size=19, color=EST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> The budget has two pieces: slope minus one to twenty units, then "
            "slope minus two. <bookmark mark='b'/> Extend the second piece and it meets the y axis at the virtual "
            "income, 120. <bookmark mark='c'/> The indifference curve through twenty-four and seventy-two is "
            "tangent to the second piece. <bookmark mark='d'/> Lower the taste for x to 0.3 and the consumer "
            f"bunches at the kink: there the marginal rate of substitution is {M['kink_case']['mrs']:.2f}, between "
            "the two prices, so neither moving left nor right pays. Bunching at kinks is how Part forty-one "
            "measured how people respond to taxes."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(bud), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(virt), FadeIn(lab_v), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(icur), FadeIn(opt), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(icur_k), FadeIn(kink), FadeIn(side[3]), run_time=1.5)
        self.clear_scene()

    def slutsky(self):
        M = load("micro1")
        tag = part_tag(1, "b", "micro")
        rows = steps([
            (r"x = \frac{0.4\, m'}{p_2}, \qquad m' = m + (p_2 - p_1)\,\bar x",
             r"demand on segment 2"),
            (rf"\frac{{\partial h}}{{\partial p_2}} = \frac{{\partial x}}{{\partial p_2}}\Big|_{{m'}} + "
             rf"x\,\frac{{\partial x}}{{\partial m}} = -12 + 24 \times 0.2 = {M['substitution']:.1f}",
             r"the substitution effect: \ Slutsky's equation, \ at fixed virtual income"),
            (rf"\frac{{dx}}{{dp_2}} = \frac{{\partial h}}{{\partial p_2}} - (x - \bar x)\,\frac{{\partial x}}"
             rf"{{\partial m}} = {M['substitution']:.1f} - 4 \times 0.2 = {M['total']:.1f}",
             r"the income effect falls only on the $x - \bar x$ units bought at $p_2$", GAIN),
            (rf"\text{{check: }} x(p_2) = 0.4\,(80/p_2 + 20) \ \Rightarrow\ x'(2) = -32/4 = {M['total']:.0f}",
             r"differentiate the demand directly"),
            (rf"\text{{wrong: }} {M['substitution']:.1f} - 24 \times 0.2 = {M['wrong_total']:.0f}",
             r"Slutsky's equation with the income effect on all 24 units", ERR),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[2][0])
        with self.voiceover(
            "Part b. <bookmark mark='a'/> On the second segment demand is 0.4 times virtual income over the "
            "second price, and virtual income itself depends on that price. <bookmark mark='b'/> The substitution "
            "effect is the Hicksian slope: the change at fixed virtual income, minus twelve, plus x times the "
            f"income derivative, 24 times 0.2: {say_num(M['substitution'], 1)}. <bookmark mark='c'/> The income "
            "effect is the subtle part. A higher second price makes the consumer poorer only on the units bought "
            "at that price, x minus twenty, so the income effect is four times 0.2, and the total is "
            f"{say_num(M['total'], 1)}. <bookmark mark='d'/> Check by differentiating demand directly: 0.4 times "
            "80 over p, plus 20; its slope at two is minus eight. <bookmark mark='e'/> The answer most often "
            "written puts the income effect on all twenty-four units and gets minus twelve."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "c":
                    self.play(Create(box))
        self.clear_scene()

    def welfare(self):
        M = load("micro1")
        tag = part_tag(1, "c", "micro")
        rows = steps([
            (rf"\text{{at }} p_2 = 2.5:\quad m' = 130, \quad x = \frac{{0.4 \times 130}}{{2.5}} = {M['x_new']:.1f}",
             r"still on segment 2"),
            (rf"\mathrm{{CV}}:\ \ 120 \times 1.25^{{0.4}} - 130 = {M['cv']:.2f}",
             r"the income that restores the old utility: \ $V = \ln m' - 0.4 \ln p_2 + $ const", GAIN),
            (rf"\text{{Laspeyres: }} (x - \bar x)\,\Delta p_2 = 4 \times 0.5 = {M['laspeyres']:.1f}",
             r"the old bundle at the new prices: \ an upper bound, \ with no substitution"),
            (rf"\text{{wrong: }} x\,\Delta p_2 = 24 \times 0.5 = {M['wrong_laspeyres']:.0f}",
             r"the price rose only on the units beyond 20", ERR),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[1][0])
        with self.voiceover(
            "Part c. <bookmark mark='a'/> At a second price of 2.5, virtual income is 130 and demand "
            f"{M['x_new']:.1f}, still on the second segment. <bookmark mark='b'/> On that segment the indirect "
            "utility is log of virtual income minus 0.4 log of the price, so the income that restores the old "
            f"utility is 120 times 1.25 to the 0.4, minus 130: a compensating variation of {M['cv']:.2f}. "
            "<bookmark mark='c'/> The Laspeyres approximation, the extra cost of the old bundle, is four units "
            "times half a unit of money: 2.0. It is larger because it ignores substitution, and here substitution "
            "is large: the marginal units fall from four to about one. <bookmark mark='d'/> The tempting wrong "
            "answer charges the rise on all twenty-four units: twelve, six times too much."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "b":
                    self.play(Create(box))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"checking one segment and stopping: \ a kinked budget needs every piece, \ and the kink",
            r"Slutsky's equation with the income effect on all units: \ only $x - \bar x$ are bought at $p_2$",
            r"forgetting that virtual income moves with $p_2$",
            r"welfare from the full price change on every unit: \ inframarginal units did not get dearer",
        ]).move_to(UP * 0.2)
        take = label(r"a kink is two straight budgets and a corner: \ solve all three, \ keep the one that is "
                     r"feasible", font_size=23, color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Checking one segment and stopping. <bookmark mark='b'/> "
            "Putting the income effect on every unit. <bookmark mark='c'/> Forgetting that virtual income moves "
            "with the price. <bookmark mark='d'/> And measuring welfare as if every unit had become dearer. "
            "<bookmark mark='e'/> The idea to keep: a kinked budget is two straight budgets and a corner; solve "
            "all three and keep the one that is feasible."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
