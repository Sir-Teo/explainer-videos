from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class GHZ(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"GHZ: \ Bell without inequalities", r"Can one run refute local values?",
                            lit=(1989,), part=PART)
        with self.voiceover("Chapter seven. Bell without inequalities."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.state()
        self.contradiction()
        self.checked()
        self.game()

    def state(self):
        d = load("ghz")
        hc = history_card(1989, r"Greenberger, \ Horne and Zeilinger", r"`Going Beyond Bell's Theorem'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"|\text{GHZ}\rangle = \tfrac{1}{\sqrt2}\big(|000\rangle + |111\rangle\big)", font_size=40,
                    color=WAVE).move_to([0, 1.3, 0])
        hd = [r"\text{measure}", r"\text{product of the three outcomes}"]
        rows = [[MathTex(k, font_size=28), MathTex(f"{v:+.0f}", font_size=28, color=OK if v > 0 else BAD)]
                for k, v in d["eigenvalues"].items()]
        grid = ValueGrid(hd, rows, col_w=[2.6, 5.2], cell_h=0.52, font_size=24).move_to([0, -1.1, 0])
        note = label(r"computed: \ each is an eigenvalue, \ so the product is certain, \ every run", font_size=20,
                     color=ABS).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1989 Daniel Greenberger, Michael Horne and Anton Zeilinger found a version of Bell's theorem with no "
            "statistics at all. <bookmark mark='a'/>Three particles share this state: all zero, plus all one. "
            "<bookmark mark='b'/>Each experimenter measures either X or Y on their particle. If all three measure X, "
            "the product of their three outcomes is always plus one. If one measures X and two measure Y, in any of "
            "the three arrangements, the product is always minus one. <bookmark mark='c'/>The Reasoner computes "
            "these: each combination is an eigenvalue of the state, so the product is certain on every single run."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()

    def contradiction(self):
        head = label(r"Suppose the answers were there all along", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lines = VGroup(
            MathTex(r"x_1 x_2 x_3 = +1", font_size=34, color=OK),
            MathTex(r"x_1 y_2 y_3 = -1,\quad y_1 x_2 y_3 = -1,\quad y_1 y_2 x_3 = -1", font_size=34, color=BAD),
            MathTex(r"\text{multiply the last three:}\quad x_1 x_2 x_3\,(y_1 y_2 y_3)^2 = -1", font_size=32),
            MathTex(r"(y_1 y_2 y_3)^2 = 1 \;\Rightarrow\; x_1 x_2 x_3 = -1", font_size=34, color=BAD),
            MathTex(r"\text{contradiction with the first line}", font_size=34, color=GOAL),
        ).arrange(DOWN, buff=0.35).move_to([0, -0.4, 0])
        with self.voiceover(
            "Now suppose, as EPR would, that each particle carries predetermined answers: x and y for particle one, "
            "for two, and for three. <bookmark mark='a'/>The first fact says x one x two x three is plus one. "
            "<bookmark mark='b'/>The other three say each mixed product is minus one. <bookmark mark='c'/>Multiply "
            "those three equations together. Each y appears twice, so the y's square away, <bookmark mark='d'/>"
            "leaving x one x two x three equal to minus one. <bookmark mark='e'/>That contradicts the first line. "
            "No assignment of answers in advance can reproduce four perfectly certain quantum predictions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(Write(l))
        self.clear_scene()

    def checked(self):
        d = load("ghz")
        head = label(r"Checked by brute force", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        grid = VGroup()
        for i in range(64):
            r, c = divmod(i, 16)
            grid.add(Square(side_length=0.55, color=BAD, fill_color=BAD, fill_opacity=0.25, stroke_width=1.5).move_to(
                [-4.6 + 0.62 * c, 1.2 - 0.62 * r, 0]))
        grid.move_to([0, 0.4, 0])
        rows = stack([(rf"{d['assignments']} ways to assign six answers: \ {d['consistent_assignments']} satisfy all "
                       r"four facts", BAD),
                      (r"one run with all-$X$ settings refutes local values: \ no statistics needed", GOAL),
                      (r"seen in the lab with three entangled photons \ (Pan et al., \ 2000)", HIST)],
                     font_size=22, aligned_edge=LEFT, width=11.0, buff=0.3).to_edge(DOWN, buff=0.5)
        assert d["consistent_assignments"] == 0
        with self.voiceover(
            "The Reasoner checks it the dull way. <bookmark mark='a'/>There are sixty-four ways to assign six "
            "answers. It tries each against the four facts. Not one satisfies all four. <bookmark mark='b'/>Where "
            "Bell's theorem needs many runs and an inequality, GHZ needs a contradiction: local values are refuted "
            "by certainties. <bookmark mark='c'/>Jian-Wei Pan and colleagues observed the GHZ correlations with "
            "entangled photons in 2000."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.02), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def game(self):
        d = load("ghzgame")
        head = label(r"The GHZ game", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["strategies"] == 64 and d["classical_best"] == 0.75 and d["quantum_win"] == 1.0
        assert {int(k): v for k, v in d["histogram"].items()} == {1: 32, 3: 32}
        players = VGroup(*[VGroup(RoundedRectangle(width=1.6, height=0.9, corner_radius=0.12, color=c),
                                  label(n, font_size=20, color=c)) for n, c in
                           ((r"Alice", ALICE), (r"Bob", BOB), (r"Carol", CLASS))]).arrange(RIGHT, buff=1.4).move_to(
            [0, 1.9, 0])
        for p_ in players:
            p_[1].move_to(p_[0])
        rule = MathTex(r"x \oplus y \oplus z = 0: \quad \text{win if } a \oplus b \oplus c = x \vee y \vee z",
                       font_size=30, color=GOAL).next_to(players, DOWN, buff=0.35)
        hd = [r"(x, y, z)", r"\text{need } a \oplus b \oplus c", r"\text{GHZ strategy wins}"]
        rows = []
        for k, v in d["quantum"].items():
            need = int(any(ch == "1" for ch in k))
            rows.append([MathTex("(" + ",".join(k) + ")", font_size=24), MathTex(str(need), font_size=24),
                         MathTex(f"{v:.0f}", font_size=24, color=OK)])
        grid = ValueGrid(hd, rows, col_w=[1.8, 2.6, 2.8], cell_h=0.45, font_size=20).move_to([-2.8, -1.4, 0])
        side = stack([(r"every one of the 64 classical strategies: \ 32 win $\tfrac34$, \ 32 win $\tfrac14$", CLASS),
                      (r"share $|\text{GHZ}\rangle$; \ measure $X$ on input 0, \ $Y$ on input 1", WAVE),
                      (r"the four facts of this chapter make it win every time", OK),
                      (r"Mermin \ (1990): \ a game with no quantum losses at all", HIST)], font_size=20,
                     aligned_edge=LEFT, width=5.2, buff=0.28).move_to([4.0, -1.3, 0])
        with self.voiceover(
            "GHZ also makes a game, with three players this time. <bookmark mark='a'/>Alice, Bob and Carol each get "
            "a bit, chosen so that the three bits have even parity, and each answers with a bit, without "
            "communicating. They win if the parity of their answers equals the OR of the questions. "
            "<bookmark mark='b'/>The Reasoner plays every one of the sixty-four classical strategies on all four "
            "questions. Half of them win three times in four, and none does better. <bookmark mark='c'/>Now share a "
            "GHZ state, and measure X on question zero and Y on question one. The four facts of this chapter are "
            "exactly the four winning conditions. <bookmark mark='d'/>The quantum players win every time. Where the "
            "CHSH game gives quantum mechanics an edge, the GHZ game gives it certainty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(players))
            vo.wait_until("a")
            self.play(Write(rule))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            self.play(FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("d")
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            self.play(FadeIn(side[3]))
        self.clear_scene()
