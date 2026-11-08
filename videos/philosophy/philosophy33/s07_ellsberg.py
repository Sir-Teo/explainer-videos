from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class Ellsberg(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Ellsberg", r"Is unknown risk worse than known risk?", lit=(1961,), part=PART)
        with self.voiceover("Chapter six. Ellsberg."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.urn()
        self.checked()
        self.maxmin()

    def urn(self):
        head = label(r"Ellsberg's urn \ (1961)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        urn = VGroup(RoundedRectangle(width=3.0, height=3.4, corner_radius=0.4, color=GREY_B))
        reds = VGroup(*[Dot([-5.9 + 0.3 * (k % 6), 1.9 - 0.3 * (k // 6), 0], radius=0.11, color="#E04040")
                        for k in range(30)])
        unk = VGroup(*[Dot([-5.9 + 0.3 * (k % 6), 0.3 - 0.3 * (k // 6), 0], radius=0.11, color=GREY_C)
                       for k in range(60)])
        urn.move_to(VGroup(reds, unk).get_center()).stretch_to_fit_height(VGroup(reds, unk).height + 0.6)
        urn.stretch_to_fit_width(VGroup(reds, unk).width + 0.6)
        lab = VGroup(label(r"30 red", font_size=19, color="#E04040").next_to(reds, RIGHT, buff=0.35),
                     wrapped_label(r"60 black or yellow, \ in unknown proportion", 2.2, 17, GREY_A).next_to(
                         unk, RIGHT, buff=0.35))
        hd = [r"\text{bet}", r"\text{red}", r"\text{black}", r"\text{yellow}"]
        rows = [(r"I: \ red", r"\$100", r"0", r"0"), (r"II: \ black", r"0", r"\$100", r"0"),
                (r"III: \ red or yellow", r"\$100", r"0", r"\$100"), (r"IV: \ black or yellow", r"0", r"\$100",
                                                                         r"\$100")]
        cells = [[label(a, font_size=18, color=PREF), label(b, font_size=18, color=GREY_A),
                  label(c, font_size=18, color=GREY_A), label(e, font_size=18, color=GREY_A)] for a, b, c, e in rows]
        grid = ValueGrid(hd, cells, col_w=[3.0, 1.4, 1.4, 1.4], cell_h=0.55, font_size=18).move_to([3.2, 0.4, 0])
        picks = VGroup(SurroundingRectangle(VGroup(*grid.cell[0]), color=OK, buff=0.05),
                       SurroundingRectangle(VGroup(*grid.cell[3]), color=OK, buff=0.05))
        foot = label(r"most prefer I to II, \ and IV to III: \ the known chance, \ both times", font_size=20,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1961 Daniel Ellsberg found a second violation. <bookmark mark='a'/>An urn holds ninety balls: thirty "
            "red, and sixty black or yellow in a proportion you are not told. <bookmark mark='b'/>Bet one pays a "
            "hundred dollars if the ball drawn is red; bet two if it is black. Most people prefer bet one. "
            "<bookmark mark='c'/>Bet three pays on red or yellow; bet four on black or yellow. Most people prefer bet "
            "four. <bookmark mark='d'/>In both pairs they choose the bet whose chance they know: a third in the first "
            "pair, two thirds in the second."
        ) as vo:
            self.play(FadeIn(head), Create(urn), FadeIn(reds), FadeIn(unk), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[0]], *[FadeIn(c) for c in grid.cell[1]])
            self.play(Create(picks[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[2]], *[FadeIn(c) for c in grid.cell[3]])
            self.play(Create(picks[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def checked(self):
        d = load("ellsberg")
        head = label(r"Every possible urn, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert d["urns"] == 61 and d["both_ok"] == 0
        f1 = MathTex(r"\text{I} \succ \text{II} \;\iff\; P(\text{red}) > P(\text{black})", font_size=32, color=PREF)
        f2 = MathTex(r"\text{IV} \succ \text{III} \;\iff\; P(\text{black}) > P(\text{red})", font_size=32,
                     color=PREF)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.35).move_to([0, 1.2, 0])
        rows = stack([(r"any single probability for black \ (0 to 60 balls, \ 61 urns): \ never both", BAD),
                      (r"the sure-thing principle fails: \ yellow pays the same within each pair", GREY_A),
                      (r"what people dislike is not risk but ambiguity: \ not knowing the chance", GOAL)],
                     font_size=21, buff=0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "No assignment of probabilities fits. <bookmark mark='a'/>With equal payoffs, preferring bet one to two "
            "means judging red more likely than black. <bookmark mark='b'/>Preferring four to three means judging "
            "black or yellow more likely than red or yellow, that is, black more likely than red. "
            "<bookmark mark='c'/>The Reasoner tries all sixty one possible urns, from no black balls to sixty, and "
            "none gives both preferences. <bookmark mark='d'/>The sure-thing principle fails again: yellow pays the "
            "same within each pair, yet changes the choice. <bookmark mark='e'/>What people avoid here is not risk "
            "but ambiguity: not knowing the chances at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(Write(f2))
            for mk, r in zip("cde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def maxmin(self):
        d = load("ellsberg")
        head = label(r"Maxmin expected utility \ (Gilboa and Schmeidler, \ 1989)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        mm = d["maxmin"]
        assert d["maxmin_pattern"] and mm == {"red": 0.3333, "black": 0.0, "black or yellow": 0.6667,
                                              "red or yellow": 0.3333}
        f = MathTex(r"V(f) \;=\; \min_{P \in \mathcal{C}} \; \mathbb{E}_P[u(f)]", font_size=38, color=PREF).move_to(
            [0, 2.0, 0])
        fl = label(r"$\mathcal{C}$: \ every urn consistent with what you know", font_size=19, color=GREY_A).next_to(
            f, DOWN, buff=0.2)
        hd = [r"\text{bet}", r"\text{worst-case chance of winning}"]
        names = [("red", r"I: \ red"), ("black", r"II: \ black"), ("red or yellow", r"III: \ red or yellow"),
                 ("black or yellow", r"IV: \ black or yellow")]
        cells = [[label(n, font_size=19, color=PREF), label(f"{mm[k]:.3f}", font_size=20,
                                                           color=OK if k in ("red", "black or yellow") else GREY_A)]
                 for k, n in names]
        grid = ValueGrid(hd, cells, col_w=[3.6, 4.6], cell_h=0.55, font_size=19).move_to([0, -0.6, 0])
        foot = label(r"I beats II, \ and IV beats III: \ ambiguity aversion, \ represented", font_size=20,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Itzhak Gilboa and David Schmeidler gave ambiguity aversion a theory in 1989. <bookmark mark='a'/>Instead "
            "of one probability, consider the whole set of distributions consistent with what you know, every "
            "possible urn, and value each act by its worst expected utility over the set. "
            "<bookmark mark='b'/>Bet one wins with a third, in every urn. Bet two could win with nothing. Bet four "
            "wins with two thirds in every urn; bet three could win with only a third. <bookmark mark='c'/>So the "
            "rule prefers one to two and four to three: exactly Ellsberg's subjects. Allais and Ellsberg together "
            "make the case against expected utility as a description of how people choose; whether they refute it "
            "as an account of how one ought to choose is the next chapter's question."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(4):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
