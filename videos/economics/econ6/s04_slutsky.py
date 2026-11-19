from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


class Slutsky(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Two effects of one price: \ the Slutsky equation", r"How much of a response is "
             r"``cheaper'' and how much is ``richer''?", "Chapter three. Two effects of one price: the Slutsky "
             "equation.")
        self.hicks()
        self.slutsky()
        self.equation()
        self.elasticity_form()

    def base(self):
        b = load("bo")
        ax = goods_axes(center=LEFT * 3.0 + DOWN * 0.3, top=11, x_length=5.8, y_length=5.8, ticks=(0, 2, 4, 6, 8, 10))
        a = ax.ax
        xs = np.array(b["xs"])
        ic0 = curve(ax, xs, np.array(b["ic0"]), color=IC, width=3, top=11)
        ic1 = curve(ax, xs, np.array(b["ic1"]), color=IC, width=3, top=11)
        old = budget_line(ax, b["m"] / b["p0"], b["m"] / b["py"], color=BUDGET)
        new = budget_line(ax, b["m"] / b["p1"], b["m"] / b["py"], color=NEWB)
        A, C = Dot(a.c2p(*b["A"]), radius=0.1, color=CHOICE), Dot(a.c2p(*b["C"]), radius=0.1, color=CHOICE)
        lA = label(r"A", font_size=24).next_to(A, DL, buff=0.06)
        lC = label(r"C", font_size=24).next_to(C, UR, buff=0.06)
        return b, ax, a, ic0, ic1, old, new, A, C, lA, lC

    def hicks(self):
        b, ax, a, ic0, ic1, old, new, A, C, lA, lC = self.base()
        k = b["m_hicks"]
        comp = budget_line(ax, k / b["p1"], k / b["py"], color=SUB, width=3)
        comp_d = DashedVMobject(comp, num_dashes=30)
        B = Dot(a.c2p(*b["B_hicks"]), radius=0.1, color=SUB)
        lB = label(r"B", font_size=24, color=SUB).next_to(B, DL, buff=0.06)
        s_ar = arrow_between(ax, b["A"], b["B_hicks"], SUB, width=5)
        i_ar = arrow_between(ax, b["B_hicks"], b["C"], INC, width=5)
        side = VGroup(
            label(r"fish \$10 $\to$ \$6; \ coconuts \$6; \ \$60", font_size=27, color=NEWB),
            label(rf"A $\to$ C: \ {b['A'][0]:.1f} $\to$ {b['C'][0]:.1f} fish, \ +{b['C'][0] - b['A'][0]:.1f}",
                  font_size=29),
            label(rf"take away \${b['m'] - k:.2f}: \\ Bo is back on his old curve, at B", font_size=27, color=SUB),
            label(rf"A $\to$ B: \ substitution, \ +{b['sub_hicks']:.2f} fish \\ cheaper relative to coconuts",
                  font_size=27, color=SUB),
            label(rf"B $\to$ C: \ income, \ +{b['inc_hicks']:.2f} fish \\ give the \${b['m'] - k:.2f} back",
                  font_size=27, color=INC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        tag = label(r"Hicks's compensation", font_size=26, color=SUB).next_to(ax, UP, buff=0.12)
        with self.voiceover(
            "Back to Bo. The price of fish falls from ten dollars to six. <bookmark mark='a'/> His budget line "
            "swings out, and he moves from bundle A to bundle C: from three point six fish to six. "
            "<bookmark mark='b'/> That move mixes two things. Fish are now cheaper relative to coconuts, and Bo is "
            "richer: his sixty dollars buy more than before. To separate them, imagine taking money away from him "
            "after the price falls, just enough to put him back on his old indifference curve. "
            "<bookmark mark='c'/> That takes fifteen dollars and eighty-four cents. With the new prices and the "
            "smaller income, his budget is this dashed line, parallel to the new one, just touching the old curve "
            "at B. <bookmark mark='d'/> The move from A to B is the substitution effect: same satisfaction, new "
            "relative prices, and Bo slides round his curve toward the good that got cheaper, nought point eight two "
            "more fish. <bookmark mark='e'/> Now give the money back. The move from B to C is the income effect: "
            "one point five eight more fish, just from being richer. John Hicks drew it this way in 1939."
        ) as vo:
            self.play(FadeIn(ax), Create(ic0), Create(old), FadeIn(A), FadeIn(lA), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(TransformFromCopy(old, new), Create(ic1), FadeIn(C), FadeIn(lC), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(tag))
            vo.wait_until("c")
            self.play(Create(comp_d), FadeIn(B), FadeIn(lB), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowArrow(s_ar), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(GrowArrow(i_ar), FadeIn(side[4]))
        self.clear_scene()

    def slutsky(self):
        b, ax, a, ic0, ic1, old, new, A, C, lA, lC = self.base()
        k = b["m_slutsky"]
        piv = budget_line(ax, k / b["p1"], k / b["py"], color=SUB, width=3)
        piv_d = DashedVMobject(piv, num_dashes=30)
        B = Dot(a.c2p(*b["B_slutsky"]), radius=0.1, color=SUB)
        lB = label(r"B$'$", font_size=24, color=SUB).next_to(B, DL, buff=0.06)
        s_ar = arrow_between(ax, b["A"], b["B_slutsky"], SUB, width=5)
        i_ar = arrow_between(ax, b["B_slutsky"], b["C"], INC, width=5)
        rows = VGroup(
            label(r"Slutsky's compensation", font_size=31, color=SUB),
            label(rf"leave him just enough to buy A: \ \${k:.2f}", font_size=27),
            label(r"the line pivots through A", font_size=25, color=GREY_A),
            label(rf"substitution \ +{b['sub_slutsky']:.2f}, \ income \ +{b['inc_slutsky']:.2f}", font_size=28,
                  color=SUB),
            label(rf"Hicks: \ +{b['sub_hicks']:.2f} and +{b['inc_hicks']:.2f}", font_size=26, color=GREY_A),
            label(r"Slutsky's needs only prices and the old bundle: \\ it can be computed from data; \ for small "
                  r"changes \\ the two agree", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Slutsky had compensated differently, and more practically. <bookmark mark='a'/> Instead of holding "
            "Bo's satisfaction fixed, which nobody can observe, hold fixed what he can afford: leave him just enough "
            "money to buy his old bundle A at the new prices, forty-five dollars and sixty cents. "
            "<bookmark mark='b'/> The budget line pivots through A. Bo can still have A, but he doesn't want it: "
            "at the new prices he moves to B prime, with nought point nine six more fish. "
            "<bookmark mark='c'/> The rest, one point four four fish, is the income effect. The split is a little "
            "different from Hicks's, because Slutsky's compensation is a little more generous. "
            "<bookmark mark='d'/> But it needs nothing except prices and the old bundle, so it can be computed from "
            "data, and for small price changes the two splits become the same."
        ) as vo:
            self.play(FadeIn(ax), Create(ic0), Create(old), Create(new), Create(ic1), FadeIn(A), FadeIn(lA),
                      FadeIn(C), FadeIn(lC), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Create(piv_d), FadeIn(B), FadeIn(lB), GrowArrow(s_ar), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(GrowArrow(i_ar), FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def equation(self):
        b = load("bo")
        sc = b["slutsky_check"]
        eq = MathTex(r"\frac{\partial x}{\partial p_x}", r"\qquad=\qquad", r"\frac{\partial h}{\partial p_x}",
                     r"\qquad-\qquad", r"x\,\frac{\partial x}{\partial m}", font_size=60).move_to(UP * 1.9)
        eq[2].set_color(SUB)
        eq[4].set_color(INC)
        names = VGroup(label(r"what you see", font_size=25).next_to(eq[0], DOWN, buff=0.35),
                       label(r"substitution: \\ compensated \\ demand", font_size=25, color=SUB).next_to(
                           eq[2], DOWN, buff=0.35),
                       label(r"income: \ how demand \\ responds to money, \\ times how much \\ you buy",
                             font_size=25, color=INC).next_to(eq[4], DOWN, buff=0.35))
        nums = MathTex(rf"{sc['dx_dp']:.3f}", r"\;=\;", rf"{sc['dh_dp']:.3f}", r"\;-\;",
                       rf"{sc['x0']:.1f} \times {sc['x_dx_dm'] / sc['x0']:.2f}", font_size=46).next_to(names, DOWN,
                                                                                                 buff=0.45)
        nums[2].set_color(SUB)
        nums[4].set_color(INC)
        unit = label(r"Bo at fish \$10: \ fish per dollar of price", font_size=22, color=GREY_B).next_to(nums, DOWN,
                                                                                                       buff=0.3)
        sign = label(r"the substitution term is never positive: \ compensated demand always slopes down",
                     font_size=28, color=SUB).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In symbols, for a small price change, this is the Slutsky equation. <bookmark mark='a'/> On the left, "
            "how the quantity bought responds to the price: what you actually see. <bookmark mark='b'/> First on "
            "the right, the substitution effect: the response of Hicks's compensated demand, written h, which holds "
            "satisfaction fixed. <bookmark mark='c'/> Then minus the income effect: how much the good responds to "
            "income, times how much of it the consumer buys. The more of a good you buy, the more a rise in its "
            "price makes you poorer. <bookmark mark='d'/> Bo's numbers, at a fish price of ten dollars: his fish "
            "fall by nought point three six for each dollar the price rises; nought point one four four of that is "
            "substitution, and three point six fish times nought point nought six, nought point two one six, is "
            "income. <bookmark mark='e'/> And one sign is guaranteed. The substitution term can never be positive: "
            "holding satisfaction fixed, a dearer good is always bought less, or no more. We'll see why in chapter "
            "five."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(eq[0]), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(Write(eq[1]), Write(eq[2]), FadeIn(names[1]))
            vo.wait_until("c")
            self.play(Write(eq[3]), Write(eq[4]), FadeIn(names[2]))
            vo.wait_until("d")
            self.play(FadeIn(nums), FadeIn(unit))
            vo.wait_until("e")
            self.play(FadeIn(sign, shift=UP * 0.1))
        self.clear_scene()

    def elasticity_form(self):
        b = load("bo")
        d = load("diet")
        eq = MathTex(r"\varepsilon", r"\;=\;", r"\varepsilon^{h}", r"\;-\;", r"w\,\eta", font_size=66).to_edge(
            UP, buff=0.6)
        eq[2].set_color(SUB)
        eq[4].set_color(INC)
        legend = label(r"$\varepsilon$: price elasticity; \ $\varepsilon^h$: compensated; \ $w$: budget share; "
                       r"\ $\eta$: income elasticity", font_size=26, color=GREY_B).next_to(eq, DOWN, buff=0.3)
        rows = VGroup(
            VGroup(label(r"Bo, fish", font_size=30, color=WHO["bo"]),
                   MathTex(rf"{b['own']:.1f} = {b['hicks_own']:.1f} - {b['share']:.1f}\times {b['income_el']:.0f}",
                           font_size=42)).arrange(RIGHT, buff=0.5),
            VGroup(label(r"Play it, coconuts", font_size=30, color=GIFF),
                   MathTex(rf"+{d['eps']:.2f} = {abs(d['eps_hicks']):.2f} - {d['share']:.2f}\times"
                           rf"({d['eta']:.2f})", font_size=42)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(legend, DOWN, buff=0.55)
        recipe = VGroup(
            label(r"demand slopes up only if:", font_size=31, color=GIFF),
            label(r"the good is inferior \ ($\eta < 0$)", font_size=28),
            label(r"it takes a large share of the budget \ ($w$ large)", font_size=28),
            label(r"and there is little room to substitute \ ($\varepsilon^h$ near 0)", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "Divide through and you get the same equation in elasticities, which is how it's used. "
            "<bookmark mark='a'/> The price elasticity equals the compensated elasticity minus the budget share "
            "times the income elasticity. <bookmark mark='b'/> For Bo: minus one equals minus nought point four, "
            "his substitution, minus nought point six of his budget times an income elasticity of one. "
            "<bookmark mark='c'/> Now the household from Play it, buying coconuts. Pinned at the corner between "
            "its budget and its calories, it has no room to substitute at all: give it just enough money to buy "
            "last week's basket, and it buys exactly that basket again. Its compensated elasticity is zero. "
            "Coconuts are thirty-nine percent of its budget, and they're inferior: one percent more income would "
            "buy one point one percent fewer coconuts. So the total is plus nought point four three. "
            "<bookmark mark='d'/> That's the whole recipe for demand that slopes up. The good must be inferior, it "
            "must take a large share of the budget, so that a price rise makes the household much poorer, and there "
            "must be little room to substitute away from it. Which kind of household fits that recipe is the next "
            "chapter."
        ) as vo:
            self.play(Write(eq[0]), Write(eq[1]), run_time=1.0)
            vo.wait_until("a")
            self.play(Write(eq[2:]), FadeIn(legend))
            vo.wait_until("b")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in recipe], lag_ratio=0.5), run_time=3)
        self.clear_scene()
