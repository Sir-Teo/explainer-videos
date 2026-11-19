from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class CostMin(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Cost minimization and the cost function", r"What is the cheapest way to build eight boats a "
             r"month?", "Chapter four. Cost minimization and the cost function.", scale=("firm",))
        self.tangency()
        self.demands()
        self.cost_function()

    def tangency(self):
        c = load("costmin")
        ax = plane([0, 16], [0, 24], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.6, y_length=5.8,
                   xticks=[0, 4, 8, 12, 16], yticks=[0, 6, 12, 18, 24], xlabel=r"shipwrights $L$",
                   ylabel=r"slipways $K$", font_size=18)
        a = ax.ax
        iso = path(ax, c["Lg"], c["iso"], color=ISO, width=3.5, xr=(0, 16), yr=(0, 24))
        lines = VGroup()
        for k, col, op in ((f"{0.75 * c['cost']:g}", GREY_B, 0.7), (f"{c['cost']:g}", COST, 1.0),
                           (f"{1.3 * c['cost']:g}", GREY_B, 0.7)):
            (x0, y0), (x1, y1) = c["lines"][k]
            lines.add(Line(a.c2p(x0, min(y0, 24)) if y0 <= 24 else a.c2p((y0 - 24) * c["r"] / c["w"], 24),
                           a.c2p(x1, y1), color=col, stroke_width=3, stroke_opacity=op))
        P = Dot(a.c2p(c["L"], c["K"]), radius=0.1, color=WHITE)
        Pl = label(rf"{c['L']:.2f} shipwrights, \\ {c['K']:.2f} slipways", font_size=18).move_to(a.c2p(12.5, 17.5))
        Pl = VGroup(Pl, Line(Pl.get_corner(DL) + DOWN * 0.05, P.get_center(), color=GREY_B, stroke_width=1.2,
                             buff=0.1))
        side = VGroup(
            label(r"eight boats a month: \ the isoquant", font_size=25, color=ISO),
            label(r"isocost lines: \ $wL + rK$ = constant, \\ slope $-w/r = -1000/400 = -2.5$", font_size=24,
                  color=COST),
            label(rf"the cheapest point touches the isoquant: \\ \${c['cost']:,.2f} a month".replace(",", "{,}"),
                  font_size=24, color=COST),
            MathTex(r"\frac{MP_L}{MP_K} = \frac{w}{r}", font_size=40, color=E.ACCENT),
            label(r"the last dollar on each input \\ buys the same extra output", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Suppose Crusoe has orders for eight boats a month. <bookmark mark='a'/> Every point on this isoquant "
            "builds them; which is cheapest? <bookmark mark='b'/> A shipwright costs a thousand dollars a month and "
            "a slipway four hundred, so the combinations that cost the same lie on straight lines with slope minus "
            "two and a half: isocost lines. Lower lines are cheaper. <bookmark mark='c'/> The cheapest way to build "
            "eight boats is where an isocost line just touches the isoquant: five point eight nine shipwrights and "
            "seven point three seven slipways, for eight thousand eight hundred and forty-two dollars a month. "
            "<bookmark mark='d'/> At that point the technical rate of substitution equals the ratio of the input "
            "prices. <bookmark mark='e'/> Equivalently, the last dollar spent on shipwrights buys as much extra "
            "output as the last dollar spent on slipways. It's the consumer's tangency of Part five, with the "
            "firm minimizing cost where the consumer maximized satisfaction."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(iso), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lines[0]), Create(lines[2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines[1]), FadeIn(P), FadeIn(Pl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def demands(self):
        c = load("costmin")
        ratios = np.array(c["ratios"])
        ax = plane([0.5, 5], [0, 25], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[1, 2, 3, 4, 5], yticks=[0, 5, 10, 15, 20, 25], xlabel=r"the wage relative to the rent, "
                   r"$w/r$", ylabel=r"inputs for 8 boats", font_size=17)
        kc = path(ax, ratios, c["K_of_ratio"], color=CAP, width=3.5)
        lc = path(ax, ratios, c["L_of_ratio"], color=LAB, width=3.5)
        now = DashedLine(ax.ax.c2p(2.5, 0), ax.ax.c2p(2.5, 25), color=GREY_C, stroke_width=1.5)
        kl = label(r"slipways", font_size=20, color=CAP).next_to(ax.ax.c2p(5, c["K_of_ratio"][-1]), UP, buff=0.1)
        ll = label(r"shipwrights", font_size=20, color=LAB).next_to(ax.ax.c2p(5, c["L_of_ratio"][-1]), DOWN,
                                                                     buff=0.12)
        side = VGroup(
            label(r"conditional factor demands: \\ the least-cost inputs for a given output", font_size=24),
            label(r"dearer labour: \ fewer shipwrights, \ more slipways", font_size=23, color=LAB),
            MathTex(r"\frac{K}{L} = \frac{a}{b}\cdot\frac{w}{r}", font_size=38, color=E.ACCENT),
            label(r"the ratio moves one for one with $w/r$: \\ an elasticity of substitution of 1", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Change the input prices and the cheapest mix changes. <bookmark mark='a'/> These are the conditional "
            "factor demands: the inputs that build eight boats at least cost, as the wage rises relative to the rent "
            "of a slipway. <bookmark mark='b'/> Dearer labour means fewer shipwrights and more slipways. "
            "<bookmark mark='c'/> For this technology the ratio of capital to labour is a fixed multiple of the "
            "ratio of wage to rent: <bookmark mark='d'/> a one percent rise in the relative wage raises capital per "
            "worker by one percent. That's an elasticity of substitution of exactly one, the Cobb–Douglas case."
        ) as vo:
            self.play(FadeIn(ax), Create(now), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(kc), Create(lc), FadeIn(kl), FadeIn(ll), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def cost_function(self):
        c = load("costmin")
        qs = np.array(c["qs"])
        ax = plane([0, 20], [0, 30000], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 10000, 20000, 30000], xlabel=r"boats a month $q$",
                   ylabel=r"least cost, \ \$ a month", font_size=17, yfmt=lambda v: f"{v / 1000:.0f}k")
        cc = path(ax, qs, c["cost_curve"], color=COST, width=3.5)
        P = Dot(ax.ax.c2p(8, c["cost"]), radius=0.09, color=WHITE)
        err = max(c["shephard"].values())
        side = VGroup(
            label(r"the cost function: \ $c(w, r, q)$, \\ the least cost of each output", font_size=24, color=COST),
            label(r"decreasing returns make it bend up: \\ $c \propto q^{4/3}$ for the yard", font_size=23),
            MathTex(r"\frac{\partial c}{\partial w} = L(w, r, q), \qquad \frac{\partial c}{\partial r} = K(w, r, q)",
                    font_size=32, color=E.ACCENT),
            label(rf"Shephard's lemma again (Part 6): \\ checked numerically, \ largest error {err:.0e}",
                  font_size=22, color=GREY_A),
            label(r"everything the firm's technology says about costs \\ is in this one function", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Do this for every output, and you have the cost function: the least it costs to build each number of "
            "boats, at given input prices. <bookmark mark='a'/> For Crusoe's yard it bends upward, because of the "
            "decreasing returns: cost rises with output to the power four thirds. <bookmark mark='b'/> And it "
            "carries everything the technology says about costs. Differentiate it with respect to the wage and you "
            "get the number of shipwrights the yard hires; with respect to the rent, the slipways. "
            "<bookmark mark='c'/> That's Shephard's lemma, the same lemma that gave compensated demand in Part six, "
            "here checked to ten decimal places on three technologies. Economists who study an industry often "
            "estimate its cost function rather than its technology, because costs are what firms record."
        ) as vo:
            self.play(FadeIn(ax), Create(cc), FadeIn(P), FadeIn(side[0]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()
