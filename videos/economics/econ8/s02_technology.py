from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class Technology(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Technology: \ what a firm can make", r"How do inputs become output, and how far can one input "
             r"stand in for another?", "Chapter one. Technology: what a firm can make.", scale=("firm",),
             horizon=("a year",))
        self.yard()
        self.marginal()
        self.isoquants()

    def yard(self):
        t = load("techs")
        y = t["yard"]
        ways = VGroup(*[slipway(1.3) for _ in range(4)]).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.9)
        men = VGroup(*[person(0.5, color=LAB) for _ in range(4)]).arrange(RIGHT, buff=0.55).next_to(ways, DOWN,
                                                                                                   buff=0.35)
        eq = MathTex(r"q \;=\; 2\,K^{0.25}\,L^{0.5}", font_size=54, color=OUT).next_to(men, DOWN, buff=0.6)
        rows = VGroup(
            label(r"$K$: \ slipways \ (capital), \ \$400 a month each", font_size=26, color=CAP),
            label(r"$L$: \ shipwrights \ (labour), \ \$1{,}000 a month each", font_size=26, color=LAB),
            label(r"$q$: \ boats a month; \ with 4 and 4, \ 5.66 boats", font_size=26, color=OUT),
            label(r"a production function: \ the most that can be made from given inputs", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(eq, DOWN, buff=0.4)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "On the Island, Crusoe now runs a boatyard. <bookmark mark='a'/> It has slipways, its capital, which "
            "rent for four hundred dollars a month each, <bookmark mark='b'/> and shipwrights, its labour, at a "
            "thousand dollars a month. <bookmark mark='c'/> The yard's technology says how many boats a month it "
            "can build from given inputs: two times slipways to the one quarter times shipwrights to the one half. "
            "With four of each, five point six six boats. <bookmark mark='d'/> A production function is a "
            "description of what is possible: the most output the inputs can make, with nothing wasted."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w_, shift=UP * 0.1) for w_ in ways], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in men], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def marginal(self):
        t = load("techs")
        inc = np.array(t["inc"])
        out = np.r_[0, np.cumsum(inc)]
        ax = plane([0, 12.5], [0, 11], center=LEFT * 2.8 + DOWN * 0.3, x_length=7.0, y_length=5.2,
                   xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"shipwrights, \ with 4 slipways",
                   ylabel=r"boats a month", font_size=17)
        a = ax.ax
        curve = path(ax, np.linspace(0.01, 12.5, 200), 2 * 4 ** 0.25 * np.linspace(0.01, 12.5, 200) ** 0.5,
                     color=OUT, width=3.5)
        steps = VGroup()
        for n in range(1, 7):
            steps.add(VGroup(Line(a.c2p(n - 1, out[n - 1]), a.c2p(n, out[n - 1]), color=GREY_C, stroke_width=1.5),
                             Line(a.c2p(n, out[n - 1]), a.c2p(n, out[n]), color=LAB, stroke_width=4),
                             label(f"{inc[n - 1]:.2f}", font_size=16, color=LAB).next_to(a.c2p(n, (out[n - 1] +
                                                                                                    out[n]) / 2), RIGHT,
                                                                                       buff=0.06)))
        side = VGroup(
            label(r"the marginal product of labour:", font_size=25),
            label(r"the extra boats from one more shipwright", font_size=23, color=LAB),
            label(rf"{inc[0]:.2f}, \ then {inc[1]:.2f}, \ {inc[2]:.2f}, \ {inc[3]:.2f}, \ \ldots", font_size=25,
                  color=LAB),
            label(r"diminishing returns: \ with the slipways fixed, \\ each new hand has less to work with",
                  font_size=23, color=GREY_A),
            MathTex(r"MP_L = \frac{\partial q}{\partial L} = \frac{b\,q}{L}", font_size=36, color=LAB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Hold the slipways at four and add shipwrights one at a time. <bookmark mark='a'/> Output rises, but "
            "less with each one. <bookmark mark='b'/> The first shipwright adds two point eight three boats a month; "
            "the second, one point one seven; the third, nought point nine; the fourth, nought point seven six. "
            "<bookmark mark='c'/> That extra output is the marginal product of labour, and it falls because the "
            "slipways are fixed: each new hand has less capital to work with. This is the law of diminishing "
            "returns, and it's a statement about holding something fixed, not about the firm growing. "
            "<bookmark mark='d'/> In symbols, for small changes, the marginal product is the derivative of output "
            "with respect to labour, which for this technology is half of output per worker."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(curve), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), FadeIn(side[1]), FadeIn(side[2]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def isoquants(self):
        t = load("techs")
        Lg = np.array(t["Lg"])
        ax = plane([0, 12], [0, 12], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.8, y_length=5.8,
                   xticks=[0, 4, 8, 12], yticks=[0, 4, 8, 12], xlabel=r"shipwrights $L$", ylabel=r"slipways $K$",
                   font_size=18)
        a = ax.ax
        curves = VGroup()
        labs = VGroup()
        for q, col in (("4", ISO), ("5.66", ISO), ("8", ISO)):
            Ks = np.array(t["iso"][q])
            curves.add(path(ax, Lg, Ks, color=col, width=3, xr=(0, 12), yr=(0, 12)))
            j = np.where(np.isfinite(Ks) & (Ks <= 12))[0][0]
            labs.add(label(rf"{q} boats", font_size=18, color=ISO).next_to(a.c2p(Lg[j], Ks[j]), RIGHT, buff=0.1))
        P = Dot(a.c2p(4, 4), radius=0.09, color=WHITE)
        trs = t["trs_at"]["trs"]
        tang = Line(a.c2p(4 - 1.6, 4 + 1.6 * trs), a.c2p(4 + 1.6, 4 - 1.6 * trs), color=E.ACCENT, stroke_width=3)
        side = VGroup(
            label(r"an isoquant: \ every mix that makes \\ the same output", font_size=24, color=ISO),
            label(r"further out, \ more boats", font_size=23, color=GREY_A),
            label(rf"its slope: \ the technical rate of substitution, \\ $MP_L/MP_K$ = {trs:.0f} at 4 and 4", font_size=24,
                  color=E.ACCENT),
            label(r"one more shipwright can replace two slipways \\ and keep output the same", font_size=23),
            label(r"the curves bow in: \ the more shipwrights, \\ the fewer slipways each one can replace",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now let both inputs vary. <bookmark mark='a'/> An isoquant joins every combination of shipwrights and "
            "slipways that builds the same number of boats: here four, five point six six and eight a month. "
            "<bookmark mark='b'/> Further out means more boats. <bookmark mark='c'/> The slope of an isoquant is "
            "the technical rate of substitution: how many slipways one more shipwright can stand in for, keeping "
            "output the same. It's the ratio of the two marginal products. At four of each, it's two. "
            "<bookmark mark='d'/> One more shipwright can replace two slipways. <bookmark mark='e'/> The isoquants "
            "bow in toward the origin because substitution gets harder: when the yard already has many "
            "shipwrights, each additional one can replace fewer slipways. It's the same geometry as the indifference "
            "curves of Part five, with output, which can be measured, in place of satisfaction, which can't."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(curves[1]), FadeIn(labs[1]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(curves[0]), Create(curves[2]), FadeIn(labs[0]), FadeIn(labs[2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(P), Create(tang), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
