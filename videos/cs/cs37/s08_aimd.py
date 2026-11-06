from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (DATA, HEAD, KERN, LAM, NO, PART, WIN, YES, axes, grid_table, load, trace)

RULEC = {"AIMD": YES, "AIAD": KERN, "MIAD": LAM, "MIMD": NO}


def phase_plane(center=ORIGIN, side=4.6):
    g = axes([0, 1.2, 0.2], [0, 1.2, 0.2], x_length=side, y_length=side, x_label=r"user 1's rate $x_1$",
             y_label=r"user 2's rate $x_2$", xticks=(0.5, 1.0), yticks=(0.5, 1.0), font=15).move_to(center)
    ax = g.ax
    eff = Line(ax.c2p(0, 1), ax.c2p(1, 0), color=WIN, stroke_width=2.5)
    fair = DashedLine(ax.c2p(0, 0), ax.c2p(1.15, 1.15), color=GREY_B, dash_length=0.1)
    opt = Dot(ax.c2p(0.5, 0.5), radius=0.08, color=WHITE)
    g.add(eff, fair, opt)
    g.eff, g.fair, g.opt = eff, fair, opt
    return g


class Aimd(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.trajectories()
        self.proof()

    def card(self):
        card = chapter_card(7, r"AIMD", r"Why add slowly and cut in half?", lit=(1989, 1989),
                            extra=((1989, r"Chiu and Jain: \ the phase plot"),), part=PART)
        with self.voiceover("Chapter seven. Additive increase, multiplicative decrease."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        head = label(r"Two users, \ one bit of feedback", font_size=36).to_edge(UP, buff=0.3)
        pp = phase_plane(center=[-3.0, -0.5, 0])
        ax = pp.ax
        el = label(r"efficient: \ $x_1 + x_2 = C$", font_size=18, color=WIN).next_to(ax.c2p(0.85, 0.15), RIGHT,
                                                                                  buff=0.1)
        fl = label(r"fair: \ $x_1 = x_2$", font_size=18, color=GREY_B).next_to(ax.c2p(1.1, 1.1), RIGHT, buff=0.05)
        ol = label(r"the goal", font_size=18, color=WHITE).next_to(pp.opt, LEFT, buff=0.12)
        side = VGroup(
            wrapped_label(r"each user only learns, \ each round, \ whether the link was overloaded: \ $x_1 + x_2 > "
                          r"C$ \ (a loss)", 5.6, font_size=21, color=WHITE),
            wrapped_label(r"each adjusts its own rate by a rule: \ increase if not, \ decrease if so", 5.6,
                          font_size=21, color=GREY_A),
            wrapped_label(r"\textbf{additive}: \ $x \to x + a$ \ \ moves along a 45$^\circ$ line", 5.6,
                          font_size=21, color=KERN),
            wrapped_label(r"\textbf{multiplicative}: \ $x \to b\,x$ \ \ moves along a line through the origin", 5.6,
                          font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, -0.3, 0])
        p = ax.c2p(0.2, 0.5)
        add = Arrow(p, ax.c2p(0.4, 0.7), buff=0, color=KERN, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        mul = Arrow(ax.c2p(0.6, 0.9), ax.c2p(0.3, 0.45), buff=0, color=LAM, stroke_width=4,
                    max_tip_length_to_length_ratio=0.2)
        with self.voiceover(
            "Why should a TCP add one packet per round trip but halve its window on a loss? In 1989 Dah-Ming Chiu "
            "and Raj Jain answered with a picture. Take two users sharing a link of capacity C. Plot user one's "
            "rate across, and user two's up. <bookmark mark='a'/> On the diagonal line where the rates sum to C, "
            "the link is exactly full: efficient. Below it the link is underused, and above it, overloaded. "
            "<bookmark mark='b'/> On the forty-five degree line through the origin, the two get equal shares: fair. "
            "The goal is where the lines cross. <bookmark mark='c'/> Neither user can see the other. All each "
            "learns, every round, is one bit: was the link overloaded? And each changes its own rate by a rule. "
            "<bookmark mark='d'/> Adding the same amount to both rates moves the point along a forty-five degree "
            "line. <bookmark mark='e'/> Multiplying both by the same factor moves it along a line through the "
            "origin. Those two facts are the whole proof."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pp[0]), *[FadeIn(m) for m in pp[1:5]])
            vo.wait_until("a")
            self.play(Create(pp.eff), FadeIn(el))
            vo.wait_until("b")
            self.play(Create(pp.fair), FadeIn(fl), FadeIn(pp.opt), FadeIn(ol))
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(GrowArrow(add), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(GrowArrow(mul), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def trajectories(self):
        c = load("chiujain")
        head = label(r"Four rules, \ from the same start", font_size=36).to_edge(UP, buff=0.3)
        planes = VGroup()
        paths = VGroup()
        names = VGroup()
        for k, rule in enumerate(("AIMD", "AIAD", "MIMD", "MIAD")):
            pp = phase_plane(center=[-4.9 + k * 3.27, -0.3, 0], side=2.7)
            ax = pp.ax
            pts = c[rule]["trajectory"][:80]
            path = trace(ax, pts, RULEC[rule], width=2.2)
            start = Dot(ax.c2p(*pts[0]), radius=0.06, color=RULEC[rule])
            planes.add(VGroup(pp[0], pp.eff, pp.fair, pp.opt))
            paths.add(VGroup(start, path))
            names.add(label(rf"\textbf{{{rule}}}", font_size=22, color=RULEC[rule]).next_to(pp[0], UP, buff=0.15))
        rows = [[r, f"{c[r]['fairness']:.3f}", f"{c[r]['efficiency']:.2f}"] for r in ("AIMD", "AIAD", "MIMD", "MIAD")]
        tab = grid_table([r"rule", r"fairness \ (Jain)", r"mean load"], rows, widths=[1.6, 2.2, 1.8], row_h=0.36,
                         font_size=18, mono_cols=())
        tab.to_edge(DOWN, buff=0.2).set_x(0)
        for k, r in enumerate(("AIMD", "AIAD", "MIMD", "MIAD"), start=1):
            for j in range(3):
                tab.cells[k][j].set_color(RULEC[r])
        with self.voiceover(
            "Here are four rules, each started with user one at a tenth of the link and user two at six tenths. "
            "<bookmark mark='a'/> Additive increase, multiplicative decrease. Each increase moves the point up the "
            "forty-five degree line until it crosses into overload; each halving pulls it toward the origin. The "
            "zig-zag closes in on the fairness line and oscillates around the goal. <bookmark mark='b'/> Additive "
            "increase and additive decrease slides up and down one forty-five degree line forever. The difference "
            "between the users never changes. <bookmark mark='c'/> Multiplicative both ways slides along one line "
            "through the origin. The ratio never changes: user two keeps six times user one's share. "
            "<bookmark mark='d'/> And multiplicative increase with additive decrease is worse than either: it "
            "drives user one to zero. <bookmark mark='e'/> Measured with Jain's fairness index, which is one when "
            "shares are equal, only AIMD reaches one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(planes), FadeIn(names))
            for mk, p in zip("abcd", paths):
                vo.wait_until(mk)
                self.play(FadeIn(p[0]), Create(p[1]), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        head = label(r"Why AIMD converges", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"Measure unfairness by the difference $d = x_2 - x_1$.", 12.4, font_size=25, color=WHITE),
            MathTex(r"\text{increase: } (x_2 + a) - (x_1 + a) = d \text{, unchanged}", font_size=36,
                    color=KERN),
            MathTex(r"\text{decrease: } b x_2 - b x_1 = b\,d \text{, halved when } b = \tfrac12",
                    font_size=36, color=LAM),
            wrapped_label(r"The increases always reach overload again \ (the sum grows by $2a$ a round), \ so "
                          r"decreases happen infinitely often, \ and after $k$ of them $d = b^k d_0 \to 0$. \ "
                          r"Meanwhile the sum oscillates between $bC$ and $C$: \ the load averages $(1 + b)C/2$.", 12.4,
                          font_size=24, color=YES),
            wrapped_label(r"Chiu and Jain prove more: \ of all linear rules, \ AIMD is the only one that converges "
                          r"to fair and efficient from every start. \ Jacobson's TCP was AIMD with $a = 1$ packet "
                          r"per round trip and $b = \tfrac12$.", 12.4, font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The proof fits in four lines. <bookmark mark='a'/> Measure the unfairness by the difference between "
            "the two rates. <bookmark mark='b'/> An additive increase adds the same to both, so the difference does "
            "not change. <bookmark mark='c'/> A multiplicative decrease multiplies both by b, so it multiplies the "
            "difference by b: it halves it. <bookmark mark='d'/> The increases always carry the sum back into "
            "overload, so the halvings never stop, and after k of them the difference is b to the k times what it "
            "was: it goes to zero. Meanwhile the total rises to C, falls to half of C, and rises again: on average "
            "three quarters full, exactly the mean load we measured. <bookmark mark='e'/> Chiu and Jain proved "
            "more: among all linear rules, only additive increase with multiplicative decrease converges to "
            "fairness and efficiency from every starting point. Jacobson had chosen it by engineering intuition a "
            "year before; it was the only answer."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, NO)
