from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Game(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"The CHSH game", r"Can entanglement win a game that no strategy can?",
                            lit=(1969,), part=PART)
        with self.voiceover("Chapter five. The CHSH game."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rules()
        self.classical()
        self.quantum()
        self.prbox()
        self.wall_brick()

    def rules(self):
        head = label(r"The rules", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        A = RoundedRectangle(width=2.0, height=1.3, corner_radius=0.15, color=ALICE).move_to([-4.0, 0.8, 0])
        B = RoundedRectangle(width=2.0, height=1.3, corner_radius=0.15, color=BOB).move_to([4.0, 0.8, 0])
        Al = label(r"Alice", font_size=22, color=ALICE).move_to(A)
        Bl = label(r"Bob", font_size=22, color=BOB).move_to(B)
        wall_ = DashedLine([0, 2.2, 0], [0, -0.6, 0], color=GREY_B)
        wl = label(r"no communication", font_size=17, color=GREY_A).next_to(wall_, DOWN, buff=0.1)
        xin = MathTex(r"x \in \{0, 1\}", font_size=28, color=ALICE).next_to(A, UP, buff=0.2)
        yin = MathTex(r"y \in \{0, 1\}", font_size=28, color=BOB).next_to(B, UP, buff=0.2)
        aout = MathTex(r"a", font_size=30, color=ALICE).next_to(A, DOWN, buff=0.25)
        bout = MathTex(r"b", font_size=30, color=BOB).next_to(B, DOWN, buff=0.25)
        win = MathTex(r"\text{win if } a \oplus b = x \wedge y", font_size=36, color=GOAL).move_to([0, -1.6, 0])
        note = label(r"answers must differ only when both questions are 1", font_size=20,
                     color=GREY_A).next_to(win, DOWN, buff=0.3)
        with self.voiceover(
            "Bell's theorem can be played as a game. <bookmark mark='a'/>Alice and Bob are separated and cannot "
            "communicate. <bookmark mark='b'/>A referee sends each a random bit, x to Alice and y to Bob. "
            "<bookmark mark='c'/>Each answers with a bit, a and b. <bookmark mark='d'/>They win if a exclusive-or "
            "b equals x and y: their answers must agree, unless both questions were one, in which case they must "
            "differ. They can plan beforehand, but not talk during the game."
        ) as vo:
            self.play(FadeIn(head), Create(A), Create(B), FadeIn(Al), FadeIn(Bl))
            vo.wait_until("a")
            self.play(Create(wall_), FadeIn(wl))
            vo.wait_until("b")
            self.play(FadeIn(xin), FadeIn(yin))
            vo.wait_until("c")
            self.play(FadeIn(aout), FadeIn(bout))
            vo.wait_until("d")
            self.play(Write(win), FadeIn(note))
        self.clear_scene()

    def classical(self):
        d = load("game")
        head = label(r"Every classical strategy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cells = VGroup()
        for i, s in enumerate(d["strategies"]):
            r, c = divmod(i, 4)
            w = s["wins_of_4"]
            col = OK if w == 3 else (BAD if w <= 1 else GREY_B)
            box = RoundedRectangle(width=2.2, height=0.95, corner_radius=0.1, color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.12)
            box.move_to([2.35 * c, -1.05 * r, 0])
            fa, fb = s["alice"], s["bob"]
            t = MathTex(rf"a = ({fa[0]}, {fa[1]}),\ b = ({fb[0]}, {fb[1]})", font_size=17).move_to(box.get_center()
                                                                                                + UP * 0.17)
            sc = MathTex(rf"{w}/4", font_size=22, color=col).move_to(box.get_center() + DOWN * 0.22)
            cells.add(VGroup(box, t, sc))
        cells.scale(0.9).move_to([-2.0, -0.3, 0])
        n3 = sum(1 for s in d["strategies"] if s["wins_of_4"] == 3)
        side = stack([(r"a strategy: \ Alice's answer to each question, \ Bob's to each", WHITE),
                      (rf"the Reasoner plays all 16 on all 4 question pairs", ABS),
                      (rf"best: \ {d['classical_best']:.2f}, \ reached by {n3} of them", OK),
                      (r"shared randomness only mixes these: \ still at most $\tfrac34$", CLASS)], font_size=20,
                     aligned_edge=LEFT, width=3.8, buff=0.3).move_to([5.1, -0.3, 0])
        assert d["classical_best"] == 0.75 and n3 == 8
        with self.voiceover(
            "What is the best plan? <bookmark mark='a'/>A deterministic strategy fixes Alice's answer to each "
            "question and Bob's answer to each: sixteen strategies in all. <bookmark mark='b'/>The Reasoner plays "
            "every one of them against all four question pairs. <bookmark mark='c'/>None wins all four. The best win "
            "three out of four, and eight strategies reach it: for instance, both always answer zero, and lose only "
            "when both questions are one. <bookmark mark='d'/>Sharing random numbers in advance only mixes "
            "deterministic strategies, so no classical plan wins more than three quarters of the time. This is "
            "Bell's inequality, in another costume."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.08), FadeIn(side[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def quantum(self):
        d = load("game")
        head = label(r"The quantum strategy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = NumberLine(x_range=[0, 1, 0.25], length=6.0, color=GREY_B, include_numbers=True, font_size=18,
                        decimal_number_config={"num_decimal_places": 2}).move_to([0, -1.6, 0])
        bar_c = Rectangle(width=6.0 * d["classical_best"], height=0.5, stroke_width=0, fill_color=CLASS,
                          fill_opacity=0.8).move_to(ax.n2p(d["classical_best"] / 2) + UP * 0.9)
        bar_q = Rectangle(width=6.0 * d["quantum_rate"], height=0.5, stroke_width=0, fill_color=WAVE,
                          fill_opacity=0.85).move_to(ax.n2p(d["quantum_rate"] / 2) + UP * 1.7)
        lc = label(rf"best classical: \ {d['classical_best']:.3f}", font_size=20, color=CLASS).next_to(bar_c, RIGHT,
                                                                                                    buff=0.2)
        lq = label(rf"quantum, \ {d['trials']:,} games: \ {d['quantum_rate']:.3f}".replace(
            f"{d['trials']:,}", f"{d['trials']:,}".replace(",", r"\,")),
                   font_size=20, color=WAVE).next_to(bar_q, RIGHT, buff=0.2)
        rows = stack([(r"share a pair of entangled qubits", WAVE),
                      (r"Alice measures at $0^\circ$ or $90^\circ$; \ Bob at $\pm 45^\circ$, \ by the question", WHITE),
                      (r"theory: \ $\cos^2(\pi/8) \approx 0.854$", ABS)], font_size=22, aligned_edge=LEFT,
                     width=10.0, buff=0.28).move_to([0, 1.6, 0])
        assert abs(d["quantum_rate"] - d["quantum_theory"]) < 0.02
        with self.voiceover(
            "Now give Alice and Bob a pair of entangled qubits. <bookmark mark='a'/>Each measures their qubit at an "
            "angle chosen by the question: Alice at zero or ninety degrees, Bob at plus or minus forty-five, and "
            "answers with the outcome. <bookmark mark='b'/>Theory says they win with probability cos squared of pi "
            "over eight, about eighty-five per cent. <bookmark mark='c'/>The Reasoner simulates twenty thousand games, "
            "drawing every outcome from the Born rule, and they win eighty-five and a half per cent of the time. "
            "No communication, no signal, just a shared quantum state, and they beat every classical strategy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), Create(ax))
            vo.wait_until("c")
            self.play(GrowFromEdge(bar_c, LEFT), FadeIn(lc))
            self.play(GrowFromEdge(bar_q, LEFT), FadeIn(lq))
        self.clear_scene()

    def prbox(self):
        d = load("prbox")
        head = label(r"Why not win every time?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        box = VGroup(RoundedRectangle(width=3.2, height=1.3, corner_radius=0.15, color=ABS, fill_opacity=0.12),
                     label(r"PR box", font_size=24, color=ABS)).move_to([-3.6, 1.6, 0])
        ins = VGroup(MathTex(r"x \to", font_size=28, color=ALICE).next_to(box, LEFT, buff=0.2),
                     MathTex(r"\leftarrow y", font_size=28, color=BOB).next_to(box, RIGHT, buff=0.2))
        rule = MathTex(r"a \oplus b = x \wedge y, \quad a \text{ uniformly random}", font_size=28,
                       color=GOAL).next_to(box, DOWN, buff=0.3)
        assert d["S"] == 4 and d["win"] == 1
        am, bm, qm = d["alice_marginal"], d["bob_marginal"], d["quantum_alice_marginal"]
        assert set(am.values()) == set(bm.values()) == set(qm.values()) == {0.5}
        hd = [r"(x, y)", r"P(a = 0)", r"P(b = 0)", r"\text{quantum } P(a = 0)"]
        keys = list(am)
        rows = [[MathTex(k.replace("x=", "").replace("y=", "").replace(", ", ",").join("()"), font_size=24),
                 MathTex(f"{am[k]:.2f}", font_size=24, color=ALICE), MathTex(f"{bm[k]:.2f}", font_size=24, color=BOB),
                 MathTex(f"{qm[k]:.2f}", font_size=24, color=WAVE)] for k in keys]
        grid = ValueGrid(hd, rows, col_w=[1.4, 1.5, 1.5, 2.4], cell_h=0.42, font_size=20).move_to([3.4, 1.2, 0])
        gtag = label(r"no signalling: \ one side's outputs ignore the other's input", font_size=18,
                     color=OK).next_to(grid, DOWN, buff=0.15)
        lad = d["ladder"]
        assert [r["S"] for r in lad] == [2.0, 2.8284, 4.0]
        ax = NumberLine(x_range=[0, 4, 1], length=6.0, color=GREY_B, include_numbers=True, font_size=18,
                        decimal_number_config={"num_decimal_places": 0}).move_to([-2.7, -2.9, 0])
        cols = [CLASS, WAVE, ABS]
        bars, tags = VGroup(), VGroup()
        for i, (r, c) in enumerate(zip(lad, cols)):
            bar = Rectangle(width=6.0 * r["S"] / 4, height=0.32, stroke_width=0, fill_color=c, fill_opacity=0.85)
            bar.move_to(ax.n2p(r["S"] / 2) + UP * (0.45 + 0.42 * (2 - i)))
            bars.add(bar)
            t = label(rf"{r['name']}: \ $S = {r['S']:g}$, \ wins {r['win']:.3f}", font_size=18, color=c).next_to(
                bar, RIGHT, buff=0.15)
            tags.add(t)
        sl = label(r"$S$", font_size=18, color=GREY_A).next_to(ax, RIGHT, buff=0.15)
        side = stack([(r"van Dam \ (2005): \ with perfect boxes, \ any distributed computation needs one bit", HIST),
                      (r"Paw\l{}owski et al. \ (2009): \ information causality \ $\Rightarrow$ \ Tsirelson's bound", HIST),
                      (r"why the world is exactly this nonlocal: \ open", GOAL)], font_size=18, aligned_edge=LEFT,
                     width=3.5, buff=0.22).move_to([5.25, -2.25, 0])
        with self.voiceover(
            "Why does quantum mechanics stop at eighty-five percent? <bookmark mark='a'/>In 1994 Sandu Popescu and "
            "Daniel Rohrlich described an imaginary box. Alice types a bit into her half and Bob into his; each gets "
            "a random bit out, but always with a XOR b equal to x AND y. <bookmark mark='b'/>It wins the CHSH game "
            "every time: S equals four, the largest value the expression can take. <bookmark mark='c'/>Yet it sends "
            "no message. The Reasoner checks: whatever Bob types, Alice's output is fifty-fifty, and the same for "
            "Bob. Quantum correlations pass the same test. <bookmark mark='d'/>So there is a ladder: local models "
            "reach two, quantum mechanics two root two, and no-signalling boxes four. Relativity alone does not say "
            "where nature stops. <bookmark mark='e'/>Wim van Dam showed in 2005 that with perfect boxes, any "
            "distributed computation could be settled with a single bit of communication. In 2009 Marcin Pawłowski "
            "and colleagues proposed a principle, information causality, from which Tsirelson's bound follows. "
            "Why the world is exactly this nonlocal, and no more, is still open."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(box), FadeIn(ins))
            self.play(Write(rule))
            vo.wait_until("b")
            self.play(Indicate(box, color=GOAL))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.35)
            self.play(FadeIn(gtag))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(sl))
            for b, t in zip(bars, tags):
                self.play(GrowFromEdge(b, LEFT), FadeIn(t), run_time=0.8)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(x) for x in side], lag_ratio=0.4), run_time=2)
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=26, current=26).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(26, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the twenty-sixth brick in the Wall. <bookmark mark='a'/>The dream was local, non-contextual "
            "hidden values: answers carried by each particle, fixed in advance, unaffected by what is done far away. "
            "Bell's theorem, and Kochen and Specker's, which chapter eight builds, rule them out. "
            "<bookmark mark='b'/>The way through costs something: non-locality, as in Bohm; many worlds, as in "
            "Everett; or giving up the idea that measurements reveal values at all."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[26], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
