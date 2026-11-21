from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"Two consumers have $u_A = 4 \ln x_A + y_A$ and $u_B = 4 \ln x_B + y_B - 0.5\, x_A$: \ A's consumption of $x$ "
    r"harms B, \ like smoke. \ There are 10 units of $x$ and 20 of $y$, \ and each consumer owns half of each.",
    r"(a) \ Find the competitive equilibrium. \quad (7 marks)",
    r"(b) \ Characterize the set of Pareto-efficient allocations. \quad (9 marks)",
    r"(c) \ Find a tax that decentralizes an efficient allocation, \ and the gain in welfare. \quad (9 marks)",
]


class Micro2(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Micro: \ an externality in an exchange economy", r"Is the market's allocation efficient "
             r"when one person's consumption harms another?", "Question two. Microeconomics: an externality in an "
             "exchange economy.", lit={1920: r"Pigou", 1960: r"Coase"}, scale=("person", "market"),
             horizon=("a year",))
        self.statement()
        self.solve()
        self.box()
        self.is_ought()
        self.marks()

    def statement(self):
        paper = exam_paper(2, "micro", r"an externality", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question two. Two consumers have quasilinear utility in a good x and money y, and A's consumption of "
            "x harms B, half a unit of money per unit, like smoke from a fire. There are ten units of x and twenty "
            "of y, and each owns half. <bookmark mark='a'/> Part a: the competitive equilibrium. <bookmark "
            "mark='b'/> Part b: the Pareto set. <bookmark mark='c'/> Part c: a tax that gets there, and what it "
            "is worth. Pause, and set up part b before you watch it."
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("abc", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def solve(self):
        M = load("micro2")
        tag = part_tag(2, "a--c", "micro")
        rows = steps([
            (rf"\frac{{4}}{{x_A}} = p = \frac{{4}}{{x_B}}, \ \ x_A + x_B = 10 \ \Rightarrow\ x_A = x_B = 5, \ \ p = "
             rf"{M['p_eq']:.1f}", r"each consumer's first-order condition, \ and market clearing; \ $y$ is the "
             r"numeraire"),
            (r"\text{no one trades: the endowment is the equilibrium}", r"A ignores the harm to B"),
            (r"\max\ u_A \ \text{ s.t. } u_B \ge \bar u \iff \max\ u_A + u_B",
             r"quasilinear: \ $y$ moves utility one for one"),
            (rf"\frac{{4}}{{x_A}} - 0.5 = \frac{{4}}{{10 - x_A}} \ \Rightarrow\ x_A = {M['xa_po']:.2f}",
             r"A's marginal benefit, \ less the harm, \ equals B's", GAIN),
            (rf"\text{{Pareto set: }} x_A = {M['xa_po']:.2f}, \ \text{{any feasible split of }} y",
             r"a vertical line in the box"),
            (rf"\frac{{4}}{{x_A}} = p + t, \ \ \frac{{4}}{{x_B}} = p \ \Rightarrow\ t = {M['tax']:.1f}, \ \ "
             rf"p = {M['p_tax']:.2f}", r"a tax on A equal to the marginal harm, \ the revenue returned to A", GAIN),
            (rf"\Delta W = W({M['xa_po']:.2f}) - W(5) = {M['gain']:.2f}", r"in units of $y$"),
        ], math_size=28, buff=0.26)
        rows.move_to(DOWN * 0.15)
        boxes = [answer_box(rows[3][0]), answer_box(rows[5][0])]
        with self.voiceover(
            "Part a. <bookmark mark='a'/> Each consumer sets the marginal utility of x, four over x, equal to its "
            f"price; with ten units to share, each takes five, at a price of {M['p_eq']:.1f}. <bookmark mark='b'/> "
            "No one trades: the endowment already is the equilibrium, because A pays no attention to the smoke. "
            "<bookmark mark='c'/> Part b. With quasilinear utility, money moves utility one for one between the "
            "two, so an allocation is efficient exactly when it maximizes the sum of utilities. <bookmark "
            "mark='d'/> That sets A's marginal benefit, less the harm it does, equal to B's marginal benefit: "
            f"A should have {M['xa_po']:.2f} units, not five. <bookmark mark='e'/> The Pareto set is every "
            f"allocation with {M['xa_po']:.2f} units for A, whatever the split of money. <bookmark mark='f'/> Part "
            f"c. A tax of {M['tax']:.1f} on each unit A consumes, equal to the marginal harm, with the revenue "
            f"handed back, does it: the market price falls to {M['p_tax']:.2f} and A pays "
            f"{M['p_tax'] + M['tax']:.2f}. <bookmark mark='g'/> The total gain is {M['gain']:.2f} units of money."
        ) as vo:
            self.play(FadeIn(tag))
            for k, (mk, r_) in enumerate(zip("abcdefg", rows)):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if k == 3:
                    self.play(Create(boxes[0]))
                if k == 5:
                    self.play(Create(boxes[1]))
        self.clear_scene()

    def box(self):
        M = load("micro2")
        a, e, X, Y = M["a"], M["e"], M["X"], M["Y"]
        ax = plane([0, X], [0, Y], center=LEFT * 1.6 + DOWN * 0.2, x_length=6.0, y_length=5.8, xticks=[0, 5, 10],
                   yticks=[0, 10, 20], xlabel=r"$x_A \ \rightarrow$", ylabel=r"$y_A \ \uparrow$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        frame = Rectangle(width=6.0, height=5.8, stroke_color=GREY_B, stroke_width=2).move_to(ax.ax.c2p(X / 2, Y / 2))
        xs = np.linspace(0.3, X - 0.3, 300)

        def curve_a(x0, y0):
            u = a * np.log(x0) + y0
            return u - a * np.log(xs)

        def curve_b(x0, y0):
            # B's utility in A's coordinates: 4 ln(10 - x_A) + (20 - y_A) - 0.5 x_A
            u = a * np.log(X - x0) + (Y - y0) - e * x0
            return a * np.log(X - xs) + Y - e * xs - u

        endow = dot(ax, X / 2, Y / 2, WHITE)
        ia, ib = path(ax, xs, curve_a(X / 2, Y / 2), MICRO, 2.4, yr=(0, Y)), path(
            ax, xs, curve_b(X / 2, Y / 2), RATE, 2.4, yr=(0, Y))
        po = vline(ax, M["xa_po"], 0, Y, GAIN, 3.0)
        po0 = vline(ax, X / 2, 0, Y, GREY_C, 1.6)
        tax_pt = dot(ax, M["xa_po"], M["ya_tax"], GAIN)
        ia2 = path(ax, xs, curve_a(M["xa_po"], M["ya_tax"]), MICRO, 2.0, yr=(0, Y)).set_opacity(0.7)
        ib2 = path(ax, xs, curve_b(M["xa_po"], M["ya_tax"]), RATE, 2.0, yr=(0, Y)).set_opacity(0.7)
        ob = label(r"$O_B$", font_size=20, color=RATE).next_to(ax.ax.c2p(X, Y), UR, buff=0.08)
        oa = label(r"$O_A$", font_size=20, color=MICRO).next_to(ax.ax.c2p(0, 0), DL, buff=0.08)
        side = VGroup(
            label(r"white: \ the endowment, \\ also the equilibrium", font_size=19, color=WHITE),
            label(r"blue and pink: \ A's and B's \\ indifference curves", font_size=19, color=GREY_A),
            label(r"they cross: \ a lens of \\ better allocations", font_size=19, color=GREY_A),
            label(rf"green: \ the Pareto set, \ $x_A = {M['xa_po']:.2f}$; \\ grey: \ where it would be \\ "
                  r"without the smoke", font_size=19, color=GAIN),
            label(rf"after the tax: \ $({M['xa_po']:.2f}, \ {M['ya_tax']:.2f})$, \\ tangent", font_size=19,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The box. <bookmark mark='a'/> A's origin is bottom left and B's top right; the endowment, in the "
            "middle, is also the equilibrium. <bookmark mark='b'/> Through it, A's indifference curve and B's, "
            "and B's is tilted by the smoke. <bookmark mark='c'/> They cross, so there is a lens of allocations "
            "both prefer: A uses less x and is paid for it. <bookmark mark='d'/> The Pareto set is the vertical "
            f"line at {M['xa_po']:.2f}; without the externality it would be the line at five. <bookmark mark='e'/> "
            "After the tax, A sells B about one and a half units, and there the two curves are tangent."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(frame), FadeIn(oa), FadeIn(ob))
            vo.wait_until("a")
            self.play(FadeIn(endow), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ia), Create(ib), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Indicate(VGroup(ia, ib), color=WHITE, scale_factor=1.0))
            vo.wait_until("d")
            self.play(Create(po0), Create(po), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(tax_pt), Create(ia2), Create(ib2), FadeIn(side[4]), run_time=1.5)
        self.clear_scene()

    def is_ought(self):
        M = load("micro2")
        c_ = is_ought_card(
            rf"the tax moves the economy onto the Pareto set; \ total surplus rises by {M['gain']:.2f} units of $y$",
            r"tax A, \ and give the revenue to A, \ to B, \ or to someone else",
            r"efficiency says nothing about where on the Pareto line to stop: \ that is a judgment about "
            r"distribution, \ and about who has the right to the clean air \ (Coase, \ Part 15)",
            width=12.0, font_size=23).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here the question steps from is to ought. <bookmark mark='a'/> What is: the tax moves the economy onto "
            f"the Pareto set, and total surplus rises by {M['gain']:.2f}. <bookmark mark='b'/> What it does not "
            "settle: every point on that vertical line is efficient, and they differ only in who has the money. "
            "Whether the revenue goes to A, to B or elsewhere, and whether B has a right to clean air in the first "
            "place, as Coase asked, is a judgment, not a theorem. <bookmark mark='c'/> A full answer says so in "
            "one sentence, and earns the mark for it."
        ) as vo:
            self.play(FadeIn(c_.card), FadeIn(c_.is_row))
            vo.wait_until("b")
            self.play(FadeIn(c_.judgment))
            vo.wait_until("c")
            self.play(FadeIn(c_.ought))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"calling the equilibrium efficient because no one wants to trade: \ the first welfare theorem needs no "
            r"externalities",
            r"setting each MRS equal to the price to find the Pareto set: \ that is the equilibrium again",
            r"taxing B, \ or every unit of $x$: \ the harm comes from A's consumption",
            r"keeping the revenue: \ without the lump-sum return, \ the tax also moves A along the Pareto line",
        ]).move_to(UP * 0.2)
        take = label(r"tax the source at the marginal harm, \ evaluated at the efficient allocation", font_size=23,
                     color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Calling the equilibrium efficient because no one wants to "
            "trade. <bookmark mark='b'/> Finding the Pareto set from each consumer's first-order condition, which "
            "only finds the equilibrium again. <bookmark mark='c'/> Taxing the wrong person or the wrong good. "
            "<bookmark mark='d'/> And forgetting to return the revenue. <bookmark mark='e'/> The idea to keep: tax "
            "the source at the marginal harm, evaluated at the efficient allocation; here the harm is constant, "
            "so that is easy, but in general it is not."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
