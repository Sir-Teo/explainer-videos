from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


def triangle_axes(origin=(-5.6, -2.4), size=4.4):
    """The Marschak-Machina triangle: p_low across, p_high up; the hypotenuse is p_mid = 0."""
    o = np.array([origin[0], origin[1], 0])
    tri = Polygon(o, o + RIGHT * size, o + UP * size, color=GREY_B, stroke_width=2)

    def P(pl, ph):
        return o + RIGHT * size * pl + UP * size * ph
    lab = VGroup(label(r"$p(\text{worst})$", font_size=17, color=GREY_A).next_to(P(0.5, 0), DOWN, buff=0.15),
                 label(r"$p(\text{best})$", font_size=17, color=GREY_A).rotate(PI / 2).next_to(P(0, 0.5), LEFT,
                                                                                            buff=0.15))
    return tri, lab, P


class VNM(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Expected utility", r"Which preferences over gambles can be represented by "
                                                   r"expected utility?", lit=(1944,), part=PART)
        with self.voiceover("Chapter three. Expected utility."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.construction()
        self.triangle()

    def axioms(self):
        hc = history_card(1944, r"John von Neumann and Oskar Morgenstern",
                          r"\textit{Theory of Games and Economic Behavior}", width=7.2, color=HIST).to_corner(UL,
                                                                                                         buff=0.3)
        rows = [(r"completeness \ and \ transitivity", r"over lotteries, \ as in chapter 1", PREF),
                (r"continuity", r"if $A \succ B \succ C$, \ some mixture of $A$ and $C$ is exactly as good as $B$",
                 RISK),
                (r"independence", r"$A \succeq B$ iff $pA + (1-p)C \succeq pB + (1-p)C$: \ a common part does not "
                                  r"matter", MONEY),
                (r"the theorem", r"exactly then there is a $u$ with $A \succeq B$ iff $\mathbb{E}_A[u] \ge "
                                 r"\mathbb{E}_B[u]$, \ unique up to $au + b$, \ $a > 0$", GOAL)]
        g = rows_table(rows, top=1.3, gap=0.5)
        with self.voiceover(
            "In 1944 John von Neumann and Oskar Morgenstern found the conditions. Options are now lotteries: "
            "probability mixtures of outcomes. <bookmark mark='a'/>Preferences between lotteries must be complete "
            "and transitive, as before. <bookmark mark='b'/>Continuity: if A is better than B and B better than C, "
            "some mixture of A and C is exactly as good as B. <bookmark mark='c'/>Independence: mixing both of two "
            "lotteries with the same third one, in the same proportion, does not change which you prefer; a common "
            "part does not matter. <bookmark mark='d'/>The theorem: preferences satisfy these axioms exactly when "
            "there is a utility function whose expectation ranks the lotteries, and that function is unique up to "
            "a choice of zero and unit, like a temperature scale."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def construction(self):
        head = label(r"Building $u$ from choices", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        best = label(r"the best outcome: \ $u = 1$", font_size=20, color=OK).move_to([3.4, 1.5, 0])
        worst = label(r"the worst outcome: \ $u = 0$", font_size=20, color=BAD).move_to([3.4, -1.5, 0])
        x = label(r"any outcome $x$", font_size=22, color=PREF).move_to([-3.6, 0, 0])
        gamble = VGroup(Line([0.4, 0, 0], [2.2, 1.3, 0], color=OK), Line([0.4, 0, 0], [2.2, -1.3, 0], color=BAD),
                        MathTex(r"p", font_size=26, color=OK).move_to([1.1, 0.95, 0]),
                        MathTex(r"1-p", font_size=26, color=BAD).move_to([1.0, -0.95, 0]))
        sim = MathTex(r"\sim", font_size=44, color=WHITE).move_to([-1.4, 0, 0])
        f = MathTex(r"u(x) \;:=\; \text{the } p \text{ at which you are indifferent}", font_size=30,
                    color=GOAL).to_edge(DOWN, buff=1.0)
        note = label(r"independence then makes $u$'s expectation rank every lottery", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The construction behind the theorem is simple. <bookmark mark='a'/>Fix the best and the worst outcomes, "
            "and give them utilities one and zero. <bookmark mark='b'/>For any outcome x, find the gamble between best "
            "and worst that you find exactly as good as x for sure; continuity guarantees there is one. "
            "<bookmark mark='c'/>Its probability p of the best outcome is x's utility. <bookmark mark='d'/>Independence "
            "then lets every lottery be rewritten as a gamble between best and worst, and its chance of the best is "
            "its expected utility."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(best), FadeIn(worst))
            vo.wait_until("b")
            self.play(FadeIn(x), FadeIn(sim), Create(gamble))
            vo.wait_until("c")
            self.play(Write(f))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()

    def triangle(self):
        d = load("triangle")
        head = label(r"Expected utility, \ drawn: \ parallel lines", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["slope"] == 1.5 and len(d["lines"]) >= 5
        tri, lab, P = triangle_axes()
        corners = VGroup(label(r"best for sure", font_size=16, color=OK).next_to(P(0, 1), UP, buff=0.1),
                         label(r"worst for sure", font_size=16, color=BAD).next_to(P(1, 0), DOWN, buff=0.1),
                         label(r"middle for sure", font_size=16, color=PREF).next_to(P(0, 0), DL, buff=0.05))
        lines = VGroup(*[VMobject(color=PREF, stroke_width=2.5).set_points_as_corners([P(a, b) for a, b in ln])
                         for ln in d["lines"]])
        arrow = Arrow(P(0.45, 0.2), P(0.25, 0.45), buff=0, color=GOAL)
        side = stack([(r"three outcomes, \ worst, \ middle, \ best: \ every lottery is a point", GREY_A),
                      (r"expected utility is linear in the probabilities: \ its indifference curves are straight "
                       r"and parallel", PREF),
                      (r"slope $(u_m - u_w)/(u_b - u_m)$: \ 1.5 for $u_m = 0.6$", RISK),
                      (r"preference rises toward the top left", GOAL)], font_size=19, aligned_edge=LEFT,
                     width=5.4, buff=0.3).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "The theory has a picture, due to Jacob Marschak and Mark Machina. <bookmark mark='a'/>With three "
            "outcomes, worst, middle and best, every lottery is a point in a triangle: its chance of the worst "
            "across, its chance of the best up, and the rest on the middle. <bookmark mark='b'/>Expected utility is "
            "linear in the probabilities, so its indifference curves are straight lines, and they are all parallel. "
            "<bookmark mark='c'/>Their slope depends only on the utility of the middle outcome: one point five when it "
            "is point six of the way from worst to best. <bookmark mark='d'/>Preference rises toward the top left. "
            "Independence is exactly the requirement that the lines be parallel, and the next chapter shows people "
            "who violate it."
        ) as vo:
            self.play(FadeIn(head), Create(tri), FadeIn(lab), FadeIn(corners))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2), FadeIn(side[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowArrow(arrow), FadeIn(side[3]))
        self.clear_scene()
