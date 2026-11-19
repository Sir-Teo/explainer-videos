from __future__ import annotations

from videos.economics.econ7.common import *  # noqa: F403
from videos.economics.econ7.compute import _eu_lines


class Lotteries(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Lotteries and expected utility", r"What does it mean to choose well among gambles, and what "
             r"follows?", "Chapter three. Lotteries and expected utility.",
             lit={1944: r"von Neumann and Morgenstern"})
        self.lotteries()
        self.axioms()
        self.triangle_lines()

    def lotteries(self):
        a = load("aversion")
        w = a["wealth"]
        reef = lottery_card([(r"for sure", rf"\${a['reef'] - w:.0f}")], r"the reef", color=SAFE, width=4.4,
                            font_size=32)
        sea = lottery_card([(r"$\tfrac12$", rf"\${a['sea'][0] - w:.0f}"), (r"$\tfrac12$", rf"\${a['sea'][1] - w:.0f}")],
                           r"the open sea", color=RISKY, width=4.4, font_size=32)
        VGroup(reef, sea).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.8)
        ev = VGroup(
            label(r"expected value: \ the open sea pays \$80 on average, \ the reef \$60", font_size=31),
            MathTex(r"\text{expected utility:}\quad EU(L) \;=\; \sum_i p_i\, u(x_i)", font_size=46, color=UTIL),
            label(r"with her \$40 at home, \ Ana compares $u(100)$ for sure \\ with $\tfrac12 u(60) + \tfrac12 "
                  r"u(180)$", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.5).next_to(VGroup(reef, sea), DOWN, buff=0.6)
        tag = island_tag(corner=DR, font_size=15)
        head = label(r"a lottery: \ prizes, \ and their chances", font_size=36, color=E.ACCENT).to_edge(UP, buff=0.35)
        VGroup(reef, sea).next_to(head, DOWN, buff=0.45)
        ev.next_to(VGroup(reef, sea), DOWN, buff=0.55)
        with self.voiceover(
            "Now risk. A lottery is a list of prizes with their chances. <bookmark mark='a'/> Ana can fish the reef, "
            "which pays sixty dollars for sure, or the open sea, which pays twenty or a hundred and forty with equal "
            "chances. <bookmark mark='b'/> The open sea pays eighty on average, twenty more than the reef. If people "
            "simply maximized the expected value, Ana would always take the sea, and nobody would ever buy "
            "insurance. <bookmark mark='c'/> Bernoulli's idea was to average utility instead: the expected utility of "
            "a lottery is the sum of each prize's utility weighted by its chance. <bookmark mark='d'/> Ana has forty "
            "dollars at home, so she compares the utility of a hundred for sure with half the utility of sixty plus "
            "half the utility of a hundred and eighty."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(reef, shift=UP * 0.2), FadeIn(sea, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(ev[0]))
            vo.wait_until("c")
            self.play(FadeIn(ev[1]))
            vo.wait_until("d")
            self.play(FadeIn(ev[2]))
        self.clear_scene()

    def axioms(self):
        rows = VGroup(
            label(r"\textbf{complete:} \ any two lotteries can be ranked", font_size=27),
            label(r"\textbf{transitive:} \ $L \succ M$ and $M \succ N$ \ $\Rightarrow$ \ $L \succ N$", font_size=27),
            label(r"\textbf{continuous:} \ no prize is infinitely good or bad", font_size=27),
            label(r"\textbf{independent:} \ $L \succ M$ \ $\Rightarrow$ \ $pL + (1-p)N \;\succ\; pM + (1-p)N$",
                  font_size=27, color=EUL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.8)
        thm = VGroup(
            label(r"then there is a $u$ with \ $L \succ M \iff \sum p_i u(x_i) > \sum q_i u(x_i)$", font_size=29,
                  color=UTIL),
            label(r"unique up to $a + b\,u$ with $b > 0$: \ only its shape matters", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(rows, DOWN, buff=0.6)
        head = VGroup(label(r"von Neumann and Morgenstern", font_size=38, color=E.ACCENT),
                      label(r"\emph{Theory of Games and Economic Behavior} (1944); \ the axioms in the 2nd edition "
                            r"(1947)", font_size=23, color=GREY_B)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Why weight utilities by chances? Two centuries after Bernoulli, John von Neumann and Oskar Morgenstern "
            "gave the answer, in the second edition of their book on games. <bookmark mark='a'/> Suppose a person's "
            "preferences over lotteries are complete and transitive, as in Part five, and continuous: no prize is "
            "infinitely good or bad. <bookmark mark='b'/> And suppose one more thing, the independence axiom: if you "
            "prefer lottery L to lottery M, you also prefer a coin flip between L and some N to the same coin flip "
            "between M and N. What the two mixtures share shouldn't change your ranking. <bookmark mark='c'/> Then, "
            "and only then, there is a utility function over prizes such that you choose as if maximizing expected "
            "utility. The function is unique up to its zero and its units: only its shape carries information. "
            "Independence is the axiom that does the work, and it's the one that will break."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows[:3]], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(thm))
            self.play(Indicate(rows[3], color=EUL, scale_factor=1.03))
        self.clear_scene()

    def triangle_lines(self):
        tr = triangle(center=LEFT * 3.2 + DOWN * 0.2, side=5.0)
        neutral = VGroup(*[tri_path(tr, pts, color=GREY_B, width=2) for pts in _eu_lines(0.25, 7)])
        averse = VGroup(*[tri_path(tr, pts, color=EUL, width=2.5) for pts in _eu_lines(9.0, 7)])
        pt = Dot(tr.p(0.3, 0.2), radius=0.09, color=WHITE)
        ptl = label(r"30\% \$0, \ 20\% \$5M, \\ 50\% \$1M", font_size=17).next_to(pt, RIGHT, buff=0.12)
        better = Arrow(tr.p(0.47, 0.34), tr.p(0.32, 0.54), color=GREY_A, buff=0, stroke_width=3,
                       max_tip_length_to_length_ratio=0.25)
        bl = label(r"better", font_size=18, color=GREY_A).next_to(better.get_end(), UP, buff=0.05)
        side = VGroup(
            label(r"three prizes: \ \$0, \ \$1 million, \ \$5 million", font_size=25),
            label(r"a lottery is a point: \ its chance of \$0 across, \\ of \$5M up, \ \$1M gets the rest",
                  font_size=23, color=GREY_A),
            MathTex(r"EU = p_0\,u(0) + p_1\,u(1\text{M}) + p_5\,u(5\text{M})", font_size=30),
            label(r"linear in the chances: \ its indifference curves \\ are \emph{straight} and \emph{parallel}",
                  font_size=24, color=EUL),
            label(r"slope $\dfrac{u(1\mathrm{M}) - u(0)}{u(5\mathrm{M}) - u(1\mathrm{M})}$: \ steeper for a more "
                  r"risk-averse chooser", font_size=23),
            label(r"grey: \ risk neutral \ (slope 0.25); \ teal: \ risk averse \ (slope 9)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "There's a picture of expected utility that will make the paradoxes easy to see. Take three prizes: "
            "nothing, a million dollars, and five million. <bookmark mark='a'/> Any lottery over them is a point in "
            "this triangle: its chance of nothing across, its chance of five million up, and the million gets what's "
            "left. The corners are the sure things. <bookmark mark='b'/> Expected utility adds up the three "
            "utilities weighted by the chances, so it's linear in the chances. Its indifference curves in the "
            "triangle are therefore straight lines, and they're parallel: that's the independence axiom as geometry. "
            "<bookmark mark='c'/> Better lotteries lie up and to the left, more chance of the best prize and less of "
            "the worst. <bookmark mark='d'/> The slope of the lines measures risk aversion. A risk-neutral chooser's "
            "lines are shallow, a slope of a quarter; a risk-averse chooser, who values the sure million almost as "
            "much as five, has steep lines: here a slope of nine. Keep this triangle in mind for the next chapter."
        ) as vo:
            self.play(FadeIn(tr), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(pt), FadeIn(ptl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]), LaggedStart(*[Create(l_) for l_ in averse], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(GrowArrow(better), FadeIn(bl))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(l_) for l_ in neutral], lag_ratio=0.2), FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()
