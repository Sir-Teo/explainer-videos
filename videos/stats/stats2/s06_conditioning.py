from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403

URN_COLS = {"I": "#9FB4C7", "II": "#B48EF0", "III": "#4FD1C5"}
RED, BLUE = "#F26D6D", "#5DADEC"


def urn(name, reds, n=8, color=GREY_B) -> VGroup:
    body = RoundedRectangle(width=1.5, height=1.8, corner_radius=0.3, stroke_color=color, stroke_width=2.5)
    k = int(round(reds * n))
    balls = VGroup(*[Dot(radius=0.13, color=RED if i < k else BLUE) for i in range(n)]).arrange_in_grid(4, 2, buff=0.12)
    balls.move_to(body)
    nm = label(rf"urn {name}", font_size=24, color=color).next_to(body, UP, buff=0.12)
    return VGroup(body, balls, nm)


class Conditioning(VoiceoverScene):
    def construct(self):
        self.card()
        self.slice()
        self.definition()
        self.multiply()
        self.total()
        self.children()

    def card(self):
        card = chapter_card(5, r"Conditioning", r"What changes when we learn something?", lit=(1654,), part=PART)
        with self.voiceover("Chapter five. Conditioning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def slice(self):
        d = load("conditioning")
        grid = outcome_grid(size=0.68, buff=0.06, dice_size=0.24).move_to([-3.4, -0.2, 0])
        xl = label(r"first die", font_size=22, color=GREY_B).next_to(grid, UP, buff=0.15)
        yl = label(r"second die", font_size=22, color=GREY_B).rotate(PI / 2).next_to(grid, LEFT, buff=0.15)
        heard = label(r"you are told: \ \emph{the sum is $8$}", font_size=32, color=EVENT).move_to([3.4, 2.6, 0])
        q = MathTex(r"P(\text{a six})", r"=", r"\tfrac{11}{36}", font_size=36).move_to([3.4, 1.5, 0])
        q[2].set_color(EXACT)
        sixes = lambda i, j: i == 6 or j == 6  # noqa: E731
        eight = lambda i, j: i + j == 8  # noqa: E731
        slice8 = [tuple(p) for p in d["slice8"]]
        row = VGroup(*[grid.cell[k].copy() for k in slice8])
        target = VGroup(*[c.copy().scale(1.35) for c in row]).arrange(RIGHT, buff=0.12).move_to([3.4, -0.4, 0])
        each = MathTex(r"\text{each } \tfrac15", font_size=30, color=EVENT).next_to(target, DOWN, buff=0.3)
        q2 = MathTex(r"P(\text{a six} \mid \text{sum } 8)", r"=", r"\tfrac25", font_size=36).next_to(each, DOWN, buff=0.4)
        q2[2].set_color(EXACT)
        with self.voiceover(
            "Two dice are rolled out of your sight. <bookmark mark='a'/> Thirty-six equally likely outcomes. "
            "<bookmark mark='b'/> What's the chance that at least one die shows a six? Eleven of the thirty-six "
            "cells. <bookmark mark='c'/> Now someone tells you the sum is eight. <bookmark mark='d'/> Most of the "
            "grid is now impossible. Only five outcomes are left: two-six, three-five, four-four, five-three and "
            "six-two. <bookmark mark='e'/> Nothing you've heard favours one of them over another, so they stay "
            "equally likely, and since one of them certainly happened, each now has probability one fifth. "
            "<bookmark mark='f'/> Two of the five contain a six. The chance of a six has gone from eleven "
            "thirty-sixths, about thirty percent, to two fifths, forty percent. Learning something has changed the "
            "probability."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.85) for c in grid], lag_ratio=0.01), FadeIn(xl), FadeIn(yl),
                      run_time=1.6)
            vo.wait_until("b")
            self.play(*light(grid, sixes, color=SIM, opacity=0.5), FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(heard, shift=DOWN * 0.2))
            self.play(*[grid.cell[k][0].animate.set_fill(CELL, opacity=1) for k in grid.cell])
            vo.wait_until("d")
            self.play(*light(grid, eight, color=EVENT, opacity=0.6),
                      *[grid.cell[k].animate.set_opacity(0.25) for k in grid.cell if not eight(*k)])
            vo.wait_until("e")
            self.play(TransformFromCopy(VGroup(*[grid.cell[k] for k in slice8]), target), run_time=1.6)
            self.play(FadeIn(each))
            vo.wait_until("f")
            self.play(*[Indicate(target[i], color=SIM) for i, k in enumerate(slice8) if 6 in k])
            self.play(Write(q2))
        self.clear_scene()

    def definition(self):
        sq = Square(side_length=3.6, stroke_color=GREY_A, stroke_width=2.5, fill_color=CELL, fill_opacity=1)
        sq.move_to([-3.6, -0.4, 0])
        cb = Ellipse(width=2.6, height=2.0, stroke_color=EVENT, stroke_width=2.5, fill_color=EVENT,
                     fill_opacity=0.25).move_to(sq.get_center() + RIGHT * 0.35 + DOWN * 0.3)
        ca = Ellipse(width=1.8, height=1.4, stroke_color=SIM, stroke_width=2.5).move_to(sq.get_center() +
                                                                                       LEFT * 0.6 + UP * 0.5)
        both = Intersection(ca, cb, stroke_width=0, fill_color=SIM, fill_opacity=0.7)
        la = MathTex(r"A", font_size=32, color=SIM).move_to(ca.get_center() + UL * 0.45)
        lb = MathTex(r"B", font_size=32, color=EVENT).move_to(cb.get_center() + DR * 0.55)
        dfn = definition_card(r"Conditional probability", r"for $P(B) > 0$, \quad $P(A \mid B) = "
                              r"\dfrac{P(A \cap B)}{P(B)}$: \ \ the share of $B$ that is also $A$", color=EXACT,
                              width=6.2, font_size=25).move_to([3.4, 1.4, 0])
        zoom = label(r"$B$ becomes the whole world, \ rescaled to area $1$", font_size=26, color=EVENT)
        zoom.move_to([3.4, -0.6, 0])
        eng = code_block(["two.given(lambda r: sum(r) == 8)", "   .P(lambda r: 6 in r)        # 2/5"],
                         font_size=22).move_to([3.4, -2.2, 0])
        with self.voiceover(
            "That's the whole idea of conditioning, and it has a picture. <bookmark mark='a'/> In the square of "
            "outcomes, learning that B happened throws away everything outside B. <bookmark mark='b'/> What's left "
            "of A is the part of A inside B. <bookmark mark='c'/> So the probability of A given B is the share of B "
            "that's also A: the probability of A and B, divided by the probability of B. Dividing by P of B rescales "
            "B to have total probability one; B becomes the whole world. <bookmark mark='d'/> In the engine, that's "
            "one operation: given, which keeps the outcomes in the event and rescales them."
        ) as vo:
            self.play(FadeIn(sq), FadeIn(ca), FadeIn(la), FadeIn(cb), FadeIn(lb))
            vo.wait_until("a")
            outside = Difference(sq, cb, stroke_width=0, fill_color=BLACK, fill_opacity=0.65)
            self.play(FadeIn(outside))
            vo.wait_until("b")
            self.play(FadeIn(both))
            vo.wait_until("c")
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            self.play(FadeIn(zoom))
            vo.wait_until("d")
            self.play(FadeIn(eng, shift=UP * 0.2))
        self.clear_scene()

    def multiply(self):
        rows = [
            cmath(r"P(A \cap B)", r"=", r"P(B)\, P(A \mid B)", font_size=40),
            cmath(r"P(\text{two aces})", r"=", r"\tfrac{4}{52} \cdot \tfrac{3}{51}", r"=", r"\tfrac{1}{221}", font_size=40),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"the definition, \ multiplied out"), why(r"an ace; \ then, given that, another")]
        title = label(r"The multiplication rule", font_size=38).to_edge(UP, buff=0.5)
        cards = VGroup(*[RoundedRectangle(width=0.9, height=1.3, corner_radius=0.08, fill_color="#EDEDED", fill_opacity=1,
                                          stroke_color=GREY_B) for _ in range(2)]).arrange(RIGHT, buff=0.4)
        for c in cards:
            c.add(MathTex(r"A\spadesuit", font_size=34, color=BLACK).move_to(c))
        cards.to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Multiply the definition out and it becomes a rule for building probabilities in stages. "
            "<bookmark mark='a'/> The chance of A and B is the chance of B, times the chance of A once B is known. "
            "<bookmark mark='b'/> Deal two cards from a shuffled deck. The first is an ace with probability four in "
            "fifty-two. Given that, three aces remain among fifty-one cards. So both are aces with probability four "
            "fifty-seconds times three fifty-firsts: one in two hundred and twenty-one. Chains like this, each "
            "factor conditional on everything before it, are how every complicated probability model is built, "
            "from a card game to a weather forecast."
        ) as vo:
            self.play(FadeIn(title))
            step = ladder(self, rows, whys, keep=2, top=1.8, x=0.0, buff=0.9)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            self.play(FadeIn(cards, shift=UP * 0.2))
            step(1, transform=False)
        self.clear_scene()

    def total(self):
        d = load("conditioning")
        urns = VGroup(*[urn(n, fval(d["reds"][n]), color=URN_COLS[n]) for n in ("I", "II", "III")])
        urns.arrange(RIGHT, buff=0.6).move_to([-4.4, 1.6, 0]).scale(0.8)
        lv = ["", "", WHITE, [
            (r"\text{I}", r"\tfrac13", URN_COLS["I"], [(r"\text{red}", r"\tfrac14", RED, []), (r"\text{blue}", r"\tfrac34", BLUE, [])]),
            (r"\text{II}", r"\tfrac13", URN_COLS["II"], [(r"\text{red}", r"\tfrac12", RED, []), (r"\text{blue}", r"\tfrac12", BLUE, [])]),
            (r"\text{III}", r"\tfrac13", URN_COLS["III"], [(r"\text{red}", r"\tfrac34", RED, []), (r"\text{blue}", r"\tfrac14", BLUE, [])]),
        ]]
        tree = prob_tree(lv, x0=-6.2, dx=2.3, height=4.4, font_size=26)
        tree.move_to([-3.0, -1.6, 0])
        reds = [(i, 0) for i in range(3)]
        eq = MathTex(r"P(\text{red})", r"=", r"\sum_i P(\text{urn } i)\, P(\text{red} \mid \text{urn } i)", font_size=32)
        eq.move_to([3.6, 1.2, 0])
        eq2 = MathTex(r"=", r"\tfrac13 \cdot \tfrac14 + \tfrac13 \cdot \tfrac12 + \tfrac13 \cdot \tfrac34", r"=",
                      r"\tfrac12", font_size=32).next_to(eq, DOWN, buff=0.35).align_to(eq[1], LEFT)
        eq2[3].set_color(EXACT)
        name = label(r"the law of total probability", font_size=26, color=S.ACCENT).next_to(eq, UP, buff=0.35)
        back = label(r"and backwards: \ given red, \ which urn?", font_size=28, color=S.POST).move_to([3.6, -1.4, 0])
        post = MathTex(r"\tfrac16,\ \ \tfrac13,\ \ \tfrac12", font_size=36, color=S.POST).next_to(back, DOWN, buff=0.3)
        with self.voiceover(
            "The multiplication rule runs along a tree; adding over branches gives the law of total probability. "
            "<bookmark mark='a'/> Three urns, holding a quarter, a half and three quarters red balls. Pick an urn "
            "at random, then a ball from it. <bookmark mark='b'/> The tree has one branch for each urn, then one for "
            "each colour. The chance of any path is the product of the probabilities along it. <bookmark mark='c'/> "
            "Red can happen along three paths. Add them: a third times a quarter, plus a third times a half, plus a "
            "third times three quarters. One half. <bookmark mark='d'/> Now turn the question around. You drew a "
            "red ball: which urn did it probably come from? Of the half of the probability that ends in red, the "
            "third urn's path carries the most. The answer is a sixth, a third and a half. That reversal, from the "
            "chance of the evidence given the cause to the chance of the cause given the evidence, has a name: "
            "Bayes' theorem."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u, shift=UP * 0.2) for u in urns], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tree, lag_ratio=0.05), run_time=2.0)
            vo.wait_until("c")
            for p in reds:
                self.play(tree.edges[p[:1]].animate.set_color(RED).set_stroke(width=5),
                          tree.edges[p].animate.set_color(RED).set_stroke(width=5), run_time=0.5)
            self.play(FadeIn(name), Write(eq))
            self.play(Write(eq2))
            vo.wait_until("d")
            self.play(FadeIn(back), FadeIn(post))
        self.clear_scene()

    def children(self):
        d = load("conditioning")
        fams = ["BB", "BG", "GB", "GG"]
        boxes = VGroup()
        for f in fams:
            kids = VGroup(*[label(ch, font_size=36, color=PB if ch == "B" else PA) for ch in f]).arrange(RIGHT, buff=0.3)
            sq = RoundedRectangle(width=1.8, height=1.1, corner_radius=0.12, stroke_color=GREY_C, stroke_width=2,
                                  fill_color=CELL, fill_opacity=1)
            boxes.add(VGroup(sq, kids.move_to(sq)))
        boxes.arrange(RIGHT, buff=0.35).move_to([-2.8, 1.4, 0])
        cap = label(r"elder, younger: \ four equally likely families", font_size=24, color=GREY_B).next_to(boxes, UP,
                                                                                                         buff=0.25)
        c1 = label(r"``at least one is a boy''", font_size=30, color=EVENT).move_to([-2.8, -0.2, 0])
        r1 = MathTex(r"P(\text{BB} \mid \ge 1\ \text{boy})", r"=", r"\tfrac13", font_size=36).next_to(c1, DOWN, buff=0.3)
        r1[2].set_color(EXACT)
        c2 = label(r"``the elder is a boy''", font_size=30, color=EVENT).move_to([3.6, -0.2, 0])
        r2 = MathTex(r"P(\text{BB} \mid \text{elder boy})", r"=", r"\tfrac12", font_size=36).next_to(c2, DOWN, buff=0.3)
        r2[2].set_color(EXACT)
        sim = MathTex(rf"\text{{simulated, {fmt_int(d['sim_n'])} families}}\ \ {d['sim_bb_one']:.3f}", font_size=26,
                      color=SIM).next_to(r1, DOWN, buff=0.3)
        warn = label(r"what you condition on is \emph{how you learned it}: \ next, three doors", font_size=28,
                     color=S.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Conditioning is simple to state and easy to get wrong, because you must condition on exactly what you "
            "learned. <bookmark mark='a'/> A family has two children. Elder and younger, each a boy or a girl, gives "
            "four equally likely families. <bookmark mark='b'/> You learn that at least one of them is a boy. What's "
            "the chance both are? Three families survive, and only one is two boys: one third, not one half. "
            "<bookmark mark='c'/> Simulated families agree. <bookmark mark='d'/> But if you learn instead that the "
            "elder child is a boy, two families survive, and the answer is a half. Two pieces of news that sound "
            "almost the same are different events, with different answers. <bookmark mark='e'/> In real life we "
            "rarely learn a clean event. We learn that someone told us something, and the way the information "
            "reached us is part of what we learned. We'll meet that again with three doors and a game-show host."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in boxes], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(c1), boxes[3].animate.set_opacity(0.2))
            self.play(Write(r1))
            vo.wait_until("c")
            self.play(FadeIn(sim))
            vo.wait_until("d")
            self.play(boxes[3].animate.set_opacity(1))
            self.play(FadeIn(c2), boxes[2].animate.set_opacity(0.2), boxes[3].animate.set_opacity(0.2))
            self.play(Write(r2))
            vo.wait_until("e")
            self.play(FadeIn(warn, shift=UP * 0.2))
        self.clear_scene()
