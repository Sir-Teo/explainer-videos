from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class StPetersburg(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"St Petersburg", r"How much would you pay for an infinite expectation?",
                            lit=(1738,), part=PART)
        with self.voiceover("Chapter two. St Petersburg."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.game()
        self.simulated()
        self.bernoulli()

    def game(self):
        head = label(r"The St Petersburg game", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"\text{first heads on toss}", r"\text{probability}", r"\text{prize}", r"\text{contribution}"]
        cells = [[label(str(k), font_size=20, color=WHITE), MathTex(rf"1/{2 ** k}", font_size=26, color=RISK),
                  MathTex(rf"{2 ** k}", font_size=26, color=MONEY), MathTex(r"1", font_size=26, color=GOAL)]
                 for k in range(1, 6)]
        cells.append([label(r"\dots", font_size=20), label(r"\dots", font_size=20), label(r"\dots", font_size=20),
                      label(r"\dots", font_size=20)])
        grid = ValueGrid(hd, cells, col_w=[3.2, 2.4, 1.8, 2.6], cell_h=0.52, font_size=19).move_to([0, 0.3, 0])
        f = MathTex(r"\mathbb{E}[\text{prize}] \;=\; 1 + 1 + 1 + \cdots \;=\; \infty", font_size=36,
                    color=BAD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Nicolaus Bernoulli posed a puzzle in 1713, and his cousin Daniel published an answer in St Petersburg "
            "in 1738. <bookmark mark='a'/>Toss a fair coin until it lands heads. If the first heads comes on toss k, "
            "you win two to the k ducats: two, four, eight, sixteen. <bookmark mark='b'/>Each row contributes its "
            "probability times its prize, and every one of those contributions is one ducat. "
            "<bookmark mark='c'/>So the expected prize is one plus one plus one, for ever: infinite. If you should "
            "maximize expected money, you should pay any finite price to play. Almost no one would pay more than a "
            "few ducats."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for r in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[r][:3]], run_time=0.5)
            vo.wait_until("b")
            for r in range(6):
                self.play(*[FadeIn(c) for c in grid.cell[r][(3 if r < 3 else 0):]], run_time=0.35)
            vo.wait_until("c")
            self.play(Write(f))
        self.clear_scene()

    def simulated(self):
        d = load("stpete")
        head = label(r"A million games, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["checkpoints"] == [10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6]
        assert d["means"] == [6.4, 9.26, 12.51, 14.01, 22.72, 24.64]
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 30, 10], x_length=7.8, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 18}, y_axis_config={"include_numbers": True}
                  ).move_to([-1.8, -0.5, 0])
        xs = VGroup(*[MathTex(rf"10^{k}", font_size=20, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k in range(1, 7)])
        xl = label(r"games played", font_size=17, color=GREY_A).next_to(xs, DOWN, buff=0.2)
        yl = label(r"average prize", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.12)
        pts = [ax.c2p(k + 1, m) for k, m in enumerate(d["means"])]
        curve = VMobject(color=MONEY, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.07, color=MONEY) for p in pts])
        guide = DashedLine(ax.c2p(1, 1.66), ax.c2p(6, 9.97 * 2 + 2), color=GREY_C)
        side = stack([(r"the average never settles: \ it creeps up, \ roughly with $\log_2$ of the number of games",
                       MONEY),
                      (r"one rare long run of tails can double it", RISK),
                      (r"the largest prize in a million games: \ $2^{22} = 4\,194\,304$", GREY_A)], font_size=19,
                     aligned_edge=LEFT, width=4.2, buff=0.3).move_to([4.6, -0.2, 0])
        with self.voiceover(
            "The Reasoner plays a million games. <bookmark mark='a'/>After ten, the average prize is six point four "
            "ducats; after a thousand, twelve and a half; after a million, about twenty five. "
            "<bookmark mark='b'/>It never settles. It creeps upward, roughly with the logarithm of the number of "
            "games, and one rare run of tails can double it at a stroke. <bookmark mark='c'/>The largest prize in a "
            "million games was two to the twenty second: four million ducats. An infinite expectation is made of "
            "enormous prizes that almost never come."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xs), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(curve), LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.2), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def bernoulli(self):
        d = load("stpete")
        head = label(r"Bernoulli's answer: \ utility, \ not money", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert d["eu_log2"] == 2.0 and d["ce"] == 4.0 and d["menger_terms"] == [1.0] * 5
        f1 = MathTex(r"u(x) = \log_2 x", font_size=36, color=PREF)
        f2 = MathTex(r"\mathbb{E}[u] \;=\; \sum_{k \ge 1} 2^{-k} \log_2 2^k \;=\; \sum_{k \ge 1} k\,2^{-k} \;=\; 2",
                     font_size=34, color=PREF)
        f3 = MathTex(r"u^{-1}(2) \;=\; 4 \text{ ducats}", font_size=34, color=GOAL)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.35).move_to([0, 1.0, 0])
        rows = stack([(r"diminishing marginal utility: \ a ducat matters less to the rich", GREY_A),
                      (r"Menger \ (1934): \ prizes of $2^{2^k}$ make $\mathbb{E}[\log_2]$ infinite too: \ "
                       r"1 + 1 + 1 + \dots", BAD),
                      (r"so utility must be bounded, \ or such games ruled out", GOAL)], font_size=20,
                     buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Daniel Bernoulli's answer was that money is not what we value. <bookmark mark='a'/>Utility grows with "
            "the logarithm of wealth: each doubling adds the same amount. <bookmark mark='b'/>Then the expected "
            "utility of the game is the sum of k over two to the k, which is exactly two, <bookmark mark='c'/>the "
            "utility of four ducats. So, from nothing, the game is worth four ducats to you, about what people say. "
            "<bookmark mark='d'/>The idea behind it is diminishing marginal utility: a ducat matters less to someone "
            "who already has many. <bookmark mark='e'/>But Karl Menger pointed out in 1934 that prizes of two to the "
            "two to the k make the expected logarithm infinite again, one plus one plus one. "
            "<bookmark mark='f'/>So either utility is bounded, or such games must be excluded: a choice the theory "
            "has never quite settled."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(Write(f3))
            for mk, r in zip("def", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
