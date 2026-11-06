from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403
from videos.philosophy.philosophy33.s04_vnm import triangle_axes


class Allais(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Allais", r"Is it irrational to prefer certainty?", lit=(1953,), part=PART)
        with self.voiceover("Chapter four. Allais."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.choices()
        self.checked()
        self.fanning()

    def choices(self):
        head = label(r"Two choices \ (Allais, \ 1953)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"", r"\text{\$0}", r"\text{\$1 million}", r"\text{\$5 million}"]
        rows = [(r"1A", r"---", r"100\%", r"---"), (r"1B", r"1\%", r"89\%", r"10\%"),
                (r"2A", r"89\%", r"11\%", r"---"), (r"2B", r"90\%", r"---", r"10\%")]
        cells = [[label(a, font_size=21, color=PREF), label(b, font_size=20, color=GREY_A),
                  label(c, font_size=20, color=GREY_A), label(e, font_size=20, color=GREY_A)] for a, b, c, e in rows]
        grid = ValueGrid(hd, cells, col_w=[1.4, 2.0, 2.6, 2.6], cell_h=0.6, font_size=19).move_to([-1.6, 0.2, 0])
        picks = VGroup(SurroundingRectangle(VGroup(*grid.cell[0]), color=OK, buff=0.06),
                       SurroundingRectangle(VGroup(*grid.cell[3]), color=OK, buff=0.06))
        side = stack([(r"most people choose 1A: \ the certain million", OK),
                      (r"and 2B: \ the extra 4 million is worth the extra 1\% risk", OK),
                      (r"Kahneman and Tversky \ (1979) \ found the same pattern", HIST)], font_size=19,
                     aligned_edge=LEFT, width=4.4, buff=0.3).move_to([4.6, 0.2, 0])
        with self.voiceover(
            "In 1953 Maurice Allais, later a Nobel laureate in economics, posed two choices. "
            "<bookmark mark='a'/>In the first, 1A is a million dollars for certain; 1B is a ten percent chance of "
            "five million, an eighty nine percent chance of one million, and a one percent chance of nothing. Most "
            "people take the certain million. <bookmark mark='b'/>In the second, 2A is an eleven percent chance of a "
            "million, and 2B a ten percent chance of five million. Here most people take 2B: the extra four million "
            "seems worth one more percent of risk. <bookmark mark='c'/>Daniel Kahneman and Amos Tversky found the "
            "same pattern in 1979. It seems entirely reasonable. It is inconsistent with expected utility."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0]], *[FadeIn(c) for c in grid.cell[1]])
            self.play(Create(picks[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[2]], *[FadeIn(c) for c in grid.cell[3]])
            self.play(Create(picks[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def checked(self):
        d = load("allais")
        head = label(r"Every utility, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["grid"] == 201 and d["both_ok"] == 0
        f1 = MathTex(r"\mathbb{E}u(1A) - \mathbb{E}u(1B) \;=\; 0.11\,u(1) - 0.10", font_size=32, color=PREF)
        f2 = MathTex(r"\mathbb{E}u(2A) - \mathbb{E}u(2B) \;=\; 0.11\,u(1) - 0.10", font_size=32, color=PREF)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.3).move_to([0, 1.6, 0])
        fl = label(r"with $u(0) = 0$, \ $u(5) = 1$: \ the same number, \ so 1A $\succ$ 1B forces 2A $\succ$ 2B",
                   font_size=19, color=GREY_A).next_to(fs, DOWN, buff=0.25)
        ax = NumberLine(x_range=[0, 1, 0.1], length=9.0, include_numbers=True, font_size=18,
                        decimal_number_config={"num_decimal_places": 1}, color=GREY_B).move_to([0, -0.9, 0])
        cut = 0.10 / 0.11
        left = Line(ax.n2p(0), ax.n2p(cut), color=EVID, stroke_width=8)
        right = Line(ax.n2p(cut), ax.n2p(1), color=RISK, stroke_width=8)
        ll = label(r"2B $\succ$ 2A, \ but then 1B $\succ$ 1A", font_size=17, color=EVID).next_to(left, DOWN, buff=0.4)
        rl = label(r"1A $\succ$ 1B, \ but 2A $\succ$ 2B", font_size=17, color=RISK).next_to(right, UP, buff=0.3)
        al = label(r"$u(\$1\text{ million})$", font_size=18, color=GREY_A).next_to(ax, LEFT, buff=0.2)
        foot = label(r"201 values of $u(1)$ tried: \ none gives both common choices", font_size=20,
                     color=BAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why inconsistent? <bookmark mark='a'/>Set the utility of nothing to zero and of five million to one. "
            "Then the expected utility of 1A minus 1B is point one one times the utility of a million, minus point "
            "one. And the expected utility of 2A minus 2B is exactly the same expression. "
            "<bookmark mark='b'/>The two choices differ only by an eighty nine percent chance of a million, common "
            "to both options in the first pair and removed from both in the second: independence says that should "
            "not matter. <bookmark mark='c'/>The Reasoner tries two hundred and one values for the utility of a "
            "million. Below point nine one, both preferences go to the risky option; above it, both go to the safe "
            "one. <bookmark mark='d'/>None gives the common pair of choices. No utility function, however shaped, "
            "makes Allais's subjects expected utility maximizers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1))
            self.play(Write(f2))
            vo.wait_until("b")
            self.play(FadeIn(fl))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(al))
            self.play(Create(left), FadeIn(ll))
            self.play(Create(right), FadeIn(rl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def fanning(self):
        d = load("allais")
        head = label(r"In the triangle: \ fanning out", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pts = d["points"]
        assert pts == {"1A": [0, 0], "1B": [0.01, 0.1], "2A": [0.89, 0], "2B": [0.9, 0.1]}
        tri, lab, P = triangle_axes(origin=(-6.4, -1.4), size=3.6)
        corners = VGroup(label(r"\$5M", font_size=15, color=OK).next_to(P(0, 1), UP, buff=0.08),
                         label(r"\$0", font_size=15, color=BAD).next_to(P(1, 0), DOWN, buff=0.08),
                         label(r"\$1M", font_size=15, color=PREF).next_to(P(0, 0), DOWN, buff=0.08))
        win = 0.12
        boxes = VGroup(Rectangle(width=3.6 * win, height=3.6 * win, color=MONEY, stroke_width=2).move_to(
            (P(-0.01, -0.01) + P(0.11, 0.11)) / 2),
            Rectangle(width=3.6 * win, height=3.6 * win, color=MONEY, stroke_width=2).move_to(
            (P(0.85, -0.01) + P(0.97, 0.11)) / 2))
        side_w = 2.6

        def panel(x_lo, centre):
            o = np.array(centre) - np.array([side_w / 2, side_w / 2, 0])

            def Q(pl, ph):
                return o + RIGHT * side_w * (pl - x_lo) / win + UP * side_w * (ph + 0.01) / win
            frame = Rectangle(width=side_w, height=side_w, color=MONEY, stroke_width=2).move_to(centre)
            edges = VGroup(Line(Q(max(x_lo, 0), 0), Q(min(x_lo + win, 1), 0), color=GREY_B))
            if x_lo < 0:
                edges.add(Line(Q(0, 0), Q(0, 0.11), color=GREY_B))
            if x_lo + win > 0.89:
                edges.add(Line(Q(0.89, 0.11), Q(min(x_lo + win, 1.0), 1 - min(x_lo + win, 1.0)), color=GREY_B))
            return frame, edges, Q

        def lines(Q, x_lo, x0s, slope, col):
            g = VGroup()
            for x0 in x0s:
                t = min(0.11 / slope, x_lo + win - x0, (1 - x0) / (1 + slope))
                g.add(Line(Q(x0, 0), Q(x0 + t, slope * t), color=col, stroke_width=2.5))
            return g
        f1, e1, Q1 = panel(-0.02, [-0.6, 0.5, 0])
        f2, e2, Q2 = panel(0.85, [3.0, 0.5, 0])
        dots = VGroup()
        for k, Q in (("1A", Q1), ("1B", Q1), ("2A", Q2), ("2B", Q2)):
            x, y = pts[k]
            dots.add(VGroup(Dot(Q(x, y), radius=0.07, color=MONEY), label(k, font_size=17, color=MONEY).next_to(
                Q(x, y), RIGHT if k.startswith("1") else LEFT, buff=0.1)))
        segs = VGroup(Line(Q1(*pts["1A"]), Q1(*pts["1B"]), color=MONEY, stroke_width=3),
                      Line(Q2(*pts["2A"]), Q2(*pts["2B"]), color=MONEY, stroke_width=3))
        steep = lines(Q1, -0.02, [0.0, 0.025, 0.05, 0.075], 25.0, RISK)
        flat = lines(Q2, 0.85, [0.86, 0.875, 0.89, 0.905], 4.0, EVID)
        cap = VGroup(label(r"near 1A, \ zoomed", font_size=16, color=GREY_A).next_to(f1, UP, buff=0.1),
                     label(r"near 2A, \ same zoom", font_size=16, color=GREY_A).next_to(f2, UP, buff=0.1))
        side = stack([(r"the two pairs are parallel segments, \ slope 10", MONEY),
                      (r"parallel indifference lines must rank both pairs the same way", PREF),
                      (r"the common choices need lines steeper than 10 near 1A \ (so 1A $\succ$ 1B), \ flatter "
                       r"near 2A \ (so 2B $\succ$ 2A): \ they fan out \ (Machina, \ 1982)", RISK),
                      (r"independence is the axiom that fails", BAD)], font_size=18, buff=0.16,
                     width=9.4).to_edge(DOWN, buff=0.3).shift(RIGHT * 1.2)
        with self.voiceover(
            "The triangle shows what goes wrong. <bookmark mark='a'/>Plot the four lotteries over nothing, a million "
            "and five million. The segment from 1A to 1B and the segment from 2A to 2B are parallel. "
            "<bookmark mark='b'/>Parallel indifference lines must therefore rank both pairs the same way. "
            "<bookmark mark='c'/>To prefer 1A but 2B, the lines must be steep near the corner of certainty, where a "
            "little risk is felt sharply, and flatter near the corner of nothing: indifference curves that fan out, "
            "as Mark Machina described them in 1982. <bookmark mark='d'/>The axiom that fails is independence. That "
            "makes Allais's choices one half of this part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head), Create(tri), FadeIn(lab), FadeIn(corners), Create(boxes))
            vo.wait_until("a")
            self.play(Create(f1), Create(f2), FadeIn(e1), FadeIn(e2), FadeIn(cap))
            self.play(FadeIn(dots), Create(segs), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(l) for l in steep], lag_ratio=0.2),
                      LaggedStart(*[Create(l) for l in flat], lag_ratio=0.2), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
