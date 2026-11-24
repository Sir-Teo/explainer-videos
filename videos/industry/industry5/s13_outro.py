from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        # the castle the whole part has been about, with the answers built round it
        keep = draw.castle(2.4, moat=0.9).move_to([-3.9, -0.3, 0])
        gold = VGroup(*[draw.coin(0.12) for _ in range(12)]).arrange_in_grid(rows=2, cols=6, buff=0.05).next_to(
            keep, UP, buff=0.15)
        head = tx("The moat", 40, GOLD, bold=True).to_edge(UP, buff=0.45)
        lines = VGroup(
            tx("Some industries earn far more than their capital costs,", 24),
            tx("and the gap fades only slowly.", 24, GREY_A),
            tx("The industry explains about a fifth of the differences", 24),
            tx("in profit; the company more.", 24, GREY_A),
            tx("A few firms earn high returns only if newcomers", 24),
            tx("are kept out and the few do not fight.", 24, GREY_A),
            tx("The walls: cost, habit, networks and law.", 24),
            tx("Five forces can drain what they protect.", 24, GREY_A),
            tx("No wall survives the day customers stop wanting", 24),
            tx("what is inside.", 21, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([2.9, -0.2, 0])
        pairs = [VGroup(lines[2 * k], lines[2 * k + 1]) for k in range(5)]
        raiders = VGroup(*[draw.person(0.4, color=ENTRANT) for _ in range(4)]).arrange(RIGHT, buff=0.15).move_to(
            [-1.4, -2.75, 0])
        with self.voiceover(
            "The moat. <bookmark mark='a'/> Some industries earn far more than their capital costs, and the gap "
            "fades only slowly. <bookmark mark='b'/> The industry a business is in explains about a fifth of the "
            "differences in profit; the business itself explains more. <bookmark mark='c'/> A few firms earn high "
            "returns only if newcomers are kept out and the few do not fight. <bookmark mark='d'/> The walls are made "
            "of cost, habit, networks and law, and five forces can drain what they protect. <bookmark mark='e'/> And "
            "no wall survives the day customers stop wanting what is inside it. <bookmark mark='f'/> When you look "
            "at an industry, ask what its castles are made of, who could walk round the walls, and what the "
            "customers would do if they could leave."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keep, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, scale=1.4) for c_ in gold], lag_ratio=0.05), FadeIn(pairs[0]))
            vo.wait_until("b")
            self.play(FadeIn(pairs[1]))
            vo.wait_until("c")
            self.play(FadeIn(pairs[2]), FadeIn(raiders, shift=LEFT * 0.4))
            self.play(raiders.animate.shift(RIGHT * 0.6), rate_func=there_and_back, run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(pairs[3]), Indicate(keep.moat, color="#7EC8F5"))
            vo.wait_until("e")
            self.play(FadeIn(pairs[4]), keep.moat.animate.set_opacity(0.15),
                      *[c_.animate.set_opacity(0.25) for c_ in gold[6:]], run_time=1.6)
            vo.wait_until("f")
            self.play(Indicate(VGroup(keep, gold), color=WHITE, scale_factor=1.03))
        self.clear_scene()
        # next: a wave of booms and busts, with ships riding it
        wave = FunctionGraph(lambda x: 0.7 * np.sin(0.9 * x), x_range=[-7, 7], color=ENTRANT, stroke_width=4).shift(
            DOWN * 1.9)
        ships = VGroup(*[draw.ship(0.9) for _ in range(3)])
        for k, s_ in enumerate(ships):
            x = -4.5 + 4.5 * k
            s_.move_to([x, 0.7 * np.sin(0.9 * x) - 1.9 + 0.2, 0])
        nxt = VGroup(tx("Next: Part 6", 26, GREY_B), tx("The Cycle", 64, WHITE, bold=True),
                     tx("Why do industries keep building too much at the top?", 26, GREY_A, italic=True)).arrange(
            DOWN, buff=0.3).move_to(UP * 1.4)
        with self.voiceover(
            "Which leads to the next question. When the castle is full of treasure, everyone builds, and the new "
            "plants arrive just as the boom ends. Part six: the cycle."
        ):
            self.play(Create(wave), LaggedStart(*[FadeIn(s_, shift=UP * 0.2) for s_ in ships], lag_ratio=0.3),
                      run_time=1.8)
            self.play(FadeIn(nxt[0]), FadeIn(nxt[1], scale=1.1), run_time=1.5)
            self.play(FadeIn(nxt[2], shift=UP * 0.1))
        self.wait(1.0)
        self.clear_scene()
