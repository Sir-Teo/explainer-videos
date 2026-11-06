from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


def envelope(txt, col, pos):
    r = Rectangle(width=2.2, height=1.4, color=col, fill_opacity=0.12, stroke_width=3).move_to(pos)
    flap = VMobject(color=col, stroke_width=2).set_points_as_corners(
        [r.get_corner(UL), r.get_center() + DOWN * 0.1, r.get_corner(UR)])
    return VGroup(r, flap, label(txt, font_size=22, color=col).move_to(r.get_center() + DOWN * 0.35))


class Envelopes(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Two envelopes", r"Where does an argument for always switching go wrong?",
                            lit=(1953, 1995), part=PART)
        with self.voiceover("Chapter fifteen. Two envelopes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.proper()
        self.broome()

    def argument(self):
        head = label(r"The two-envelope argument", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        e1 = envelope(r"yours: \ $a$", MONEY, [-4.4, 1.0, 0])
        e2 = envelope(r"other: \ $?$", GREY_B, [-1.4, 1.0, 0])
        rule = label(r"one holds $x$, \ the other $2x$; \ you picked one at random", font_size=19,
                     color=GREY_A).next_to(VGroup(e1, e2), DOWN, buff=0.3)
        f = MathTex(r"\mathbb{E}[\text{other}] \;=\; \tfrac12 \cdot 2a + \tfrac12 \cdot \tfrac{a}{2} \;=\; "
                    r"\tfrac54\,a \;>\; a", font_size=34, color=RISK).move_to([0, -1.0, 0])
        side = stack([(r"so switch; \ and by the same argument, \ switch back", BAD),
                      (r"the argument works for any $a$: \ so switch without looking, \ for ever", BAD)],
                     font_size=20, buff=0.25).to_edge(DOWN, buff=0.6)
        hist = label(r"Kraitchik \ (1953); \ made famous by Nalebuff \ (1989)", font_size=17, color=HIST).move_to(
            [3.6, 1.0, 0])
        with self.voiceover(
            "The last puzzle goes back to Maurice Kraitchik in 1953. <bookmark mark='a'/>Two envelopes hold money, "
            "one twice as much as the other. You pick one at random and find a dollars in it. "
            "<bookmark mark='b'/>Should you switch? The other envelope holds either twice a or half a, with equal "
            "chances, so its expected value is five quarters of a, more than you have. Switch. "
            "<bookmark mark='c'/>But the same argument, applied to the other envelope, tells you to switch back. "
            "<bookmark mark='d'/>And since it works for any amount a, you should switch without even looking, and "
            "keep switching for ever. Something is wrong; the question is exactly what."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hist))
            vo.wait_until("a")
            self.play(FadeIn(e1), FadeIn(e2), FadeIn(rule))
            vo.wait_until("b")
            self.play(Write(f))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def proper(self):
        d = load("envelopes")
        head = label(r"A real prior, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["q"] == 0.4 and d["proper_total"] == 0.0
        rows = d["proper"]
        assert [r["gain"] for r in rows[:4]] == [1.0, -0.1429, -0.2857, -0.5714]
        f = MathTex(r"P(x = 2^k) \;\propto\; 0.4^k, \qquad k = 0, 1, 2, \dots", font_size=30, color=PREF).next_to(
            head, DOWN, buff=0.3)
        hd = [r"\text{you see } a", r"P(a \text{ is the smaller})", r"\text{expected gain from switching}"]
        cells = []
        for r in rows[:6]:
            cells.append([label(f"{r['amount']}", font_size=20, color=MONEY),
                          label(f"{r['p_smaller']:.4f}", font_size=20, color=PREF),
                          label(f"{r['gain']:+.4f}", font_size=20, color=OK if r["gain"] > 0 else BAD)])
        grid = ValueGrid(hd, cells, col_w=[1.8, 3.2, 4.0], cell_h=0.5, font_size=18).move_to([-1.6, -0.6, 0])
        side = stack([(r"at 1 you know you hold the smaller", OK),
                      (r"above it, \ $P(\text{smaller}) = 0.4/1.4 = 0.286$, \ not $\tfrac12$", PREF),
                      (r"averaged over what you might see: \ exactly 0", GOAL)], font_size=18, aligned_edge=LEFT,
                     width=3.3, buff=0.3).move_to([4.95, -0.6, 0])
        with self.voiceover(
            "The argument assumed that, whatever you see, the other envelope is equally likely to be larger or "
            "smaller. <bookmark mark='a'/>Give the Reasoner a real prior: the smaller amount is two to the k "
            "dollars, with probability proportional to point four to the k. <bookmark mark='b'/>If you see one "
            "dollar, you certainly hold the smaller, and switching gains a dollar. <bookmark mark='c'/>If you see "
            "any larger amount, the chance that you hold the smaller is not a half but point two eight six, and "
            "switching loses on average: point one four at two dollars, point two nine at four, and so on, "
            "doubling. <bookmark mark='d'/>Averaged over everything you might see, the expected gain from switching "
            "is exactly zero, as symmetry demands. No prior over amounts can make every amount equally likely to "
            "be the smaller; the argument's premise is a prior that does not exist."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[0]], FadeIn(side[0]))
            vo.wait_until("c")
            for k in range(1, 6):
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.4)
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def broome(self):
        d = load("envelopes")
        head = label(r"Broome's prior \ (1995)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["broome"]
        assert all(r["gain"] > 0 for r in rows) and [r["p_smaller"] for r in rows[1:]] == [0.4] * 6
        f1 = MathTex(r"P(x = 2^k) \;\propto\; \left(\tfrac23\right)^k", font_size=30, color=PREF)
        f2 = MathTex(r"\mathbb{E}[x] \;=\; \sum_k \left(\tfrac23\right)^k 2^k \;\propto\; \sum_k \left(\tfrac43"
                     r"\right)^k \;=\; \infty", font_size=30, color=BAD)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.3).move_to([2.8, 1.4, 0])
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 7, 2], x_length=5.0, y_length=3.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16}, y_axis_config={"include_numbers": True}
                  ).move_to([-3.6, -0.6, 0])
        bars = VGroup()
        for k, r in enumerate(rows):
            b = Rectangle(width=0.5, height=ax.c2p(0, r["gain"])[1] - ax.c2p(0, 0)[1], color=OK, fill_opacity=0.6)
            bars.add(b.move_to(ax.c2p(k + 0.5, r["gain"] / 2)))
        xs = VGroup(*[label(str(r["amount"]), font_size=15, color=MONEY).next_to(ax.c2p(k + 0.5, 0), DOWN,
                                                                                buff=0.12)
                      for k, r in enumerate(rows)])
        xl = label(r"amount seen", font_size=16, color=GREY_A).next_to(xs, DOWN, buff=0.15)
        yl = label(r"expected gain from switching", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.1)
        side = stack([(r"switching gains at every amount you could see", OK),
                      (r"yet the two envelopes are symmetric", GREY_A),
                      (r"because the expected amount is infinite: \ St Petersburg again", BAD),
                      (r"the lesson: \ conditional expectations can mislead when the unconditional one is infinite, "
                       r"\ or the prior improper", GOAL)], font_size=18, aligned_edge=LEFT, width=5.4,
                     buff=0.25).move_to([2.8, -1.4, 0])
        with self.voiceover(
            "John Broome found a prior that brings the paradox back. <bookmark mark='a'/>Make the smaller amount "
            "two to the k with probability proportional to two thirds to the k. <bookmark mark='b'/>Then, for every "
            "amount you could see above one dollar, the chance that you hold the smaller is point four, and "
            "switching gains a tenth of what you see: twenty cents at two dollars, forty cents at four, and growing. "
            "<bookmark mark='c'/>Switching is better whatever you see, and yet the situation is symmetric. "
            "<bookmark mark='d'/>The way out is the expected amount in an envelope: a sum of four thirds to the k, "
            "which is infinite. This is St Petersburg again, from chapter two. <bookmark mark='e'/>When the "
            "unconditional expectation is infinite, or the prior is improper, reasoning by conditional expectations "
            "can lead anywhere. Infinity, in this part, has broken expected utility three times."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), FadeIn(xs), FadeIn(xl),
                      FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Write(f2), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
