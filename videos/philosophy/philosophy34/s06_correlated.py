from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Correlated(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Correlated equilibrium", r"Can a shared signal do better than any equilibrium?",
                            lit=(1974,), part=PART)
        with self.voiceover("Chapter five. Correlated equilibrium."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.chicken()
        self.lp()
        self.conventions()

    def chicken(self):
        d = load("correlated")
        head = label(r"Chicken, \ and a traffic light \ (Aumann, \ 1974)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        A, B, acts = G.GAMES["chicken"]
        assert [e["payoff"] for e in d["nash"]] == [[7.0, 2.0], [2.0, 7.0], [4.6667, 4.6667]]
        assert d["uniform_payoff"] == [5.0, 5.0]
        bm = bimatrix(A, B, acts, font_size=22, cell=1.4, center=[-3.6, 0.2, 0])
        side = stack([(r"pure equilibria: \ one dares, \ one swerves: \ (7, 2) \ or \ (2, 7)", GREY_A),
                      (r"mixed: \ each dares with probability 1/3: \ 4.67 each, \ with a 1/9 chance of a crash", BAD),
                      (r"a light that says `go' or `stop', \ choosing (swerve, swerve), \ (swerve, dare), \ "
                       r"(dare, swerve) \ each with probability 1/3", INST),
                      (r"told `dare', \ you know the other swerves; \ told `swerve', \ daring would risk a crash: \ "
                       r"obeying is a best response", GOAL),
                      (r"5 each, \ and never a crash", OK)], font_size=18, aligned_edge=LEFT, width=6.0,
                     buff=0.26).move_to([3.0, 0.0, 0])
        with self.voiceover(
            "Robert Aumann found a way past the limits of Nash equilibrium in 1974. <bookmark mark='a'/>In chicken, "
            "two drivers head toward each other. If both dare, they crash. The pure equilibria have one dare and "
            "the other swerve, seven to two. <bookmark mark='b'/>The symmetric equilibrium has each dare a third of "
            "the time: four and two thirds each, with a one in nine chance of a crash. <bookmark mark='c'/>Now add a "
            "traffic light: a device that picks one of three recommendations with equal chance, both swerve, or one "
            "of them dares, and tells each driver only their own instruction. <bookmark mark='d'/>Told to dare, you "
            "know the other was told to swerve. Told to swerve, you know the other dares half the time, so daring "
            "would risk a crash. Obeying is a best response either way. <bookmark mark='e'/>Each earns five, more "
            "than in the symmetric equilibrium, and there is never a crash. A correlated equilibrium is a "
            "distribution over profiles that everyone is willing to obey."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bm))
            for mk, r in zip("abcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def lp(self):
        d = load("correlated")
        head = label(r"The best signal, \ by linear programming", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["best"] == [0.0, 0.25, 0.25, 0.5] and d["best_payoff"] == [5.25, 5.25]
        f1 = MathTex(r"\max_{\mu \ge 0} \;\sum_{s} \mu(s)\,\big(u_1(s) + u_2(s)\big)", font_size=30, color=INST)
        f2 = MathTex(r"\text{s.t. } \sum_{s_{-i}} \mu(a, s_{-i})\,\big(u_i(a, s_{-i}) - u_i(a', s_{-i})\big) \ge 0 "
                     r"\;\; \forall i, a, a'", font_size=28, color=GREY_A)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.25).move_to([0, 1.5, 0])
        A, B, acts = G.GAMES["chicken"]
        cell, o = 1.4, np.array([-3.6, -1.2, 0])
        boxes = VGroup()
        for i in range(2):
            for j in range(2):
                p = d["best"][2 * i + j]
                sq = Square(cell, color=GREY_B, stroke_width=1.5, fill_color=INST, fill_opacity=0.15 + 0.7 * p).move_to(
                    o + np.array([j * cell, -i * cell, 0]))
                boxes.add(VGroup(sq, label(f"{p:.2f}", font_size=22, color=WHITE).move_to(sq)))
        rl = VGroup(*[label(a, font_size=17, color=ROW).next_to(boxes[2 * i], LEFT, buff=0.2) for i, a in
                      enumerate(acts)])
        cl = VGroup(*[label(a, font_size=17, color=COL).next_to(boxes[j], UP, buff=0.12) for j, a in enumerate(acts)])
        side = stack([(r"obedience: \ linear inequalities in the probabilities", GREY_A),
                      (r"best: \ both swerve 1/2, \ each dares 1/4", INST),
                      (r"5.25 each, \ beyond every Nash equilibrium's 4.67", OK),
                      (r"computable in polynomial time, \ unlike Nash equilibrium", GOAL)], font_size=18,
                     aligned_edge=LEFT, width=5.4, buff=0.28).move_to([3.2, -1.4, 0])
        with self.voiceover(
            "Which signal is best? <bookmark mark='a'/>Obedience is a set of linear inequalities in the probabilities "
            "of the recommended profiles: for each player and each recommendation, obeying must be at least as good "
            "as any deviation. <bookmark mark='b'/>So the best correlated equilibrium is the solution of a linear "
            "program, and the Reasoner solves it. Both swerve half the time, and each dares a quarter of the time. "
            "<bookmark mark='c'/>That gives five and a quarter each, more than any Nash equilibrium of the game. "
            "<bookmark mark='d'/>And unlike Nash equilibrium, correlated equilibria can be computed in polynomial "
            "time; simple regret-minimizing learning rules converge to them, a result of Sergiu Hart and Andreu "
            "Mas-Colell in 2000."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), Write(f2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(boxes), FadeIn(rl), FadeIn(cl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def conventions(self):
        head = label(r"Signals, \ conventions, \ institutions", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Hume \ (1739)", r"two men who pull the oars of a boat do it by an agreement or convention, \ "
                                   r"though they have never given promises to each other", HIST),
                (r"Lewis \ (1969)", r"a convention is a regularity everyone follows because the others do: \ "
                                    r"Part 12's common knowledge at work", ROW),
                (r"Gintis \ (2009)", r"social norms as choreographers: \ correlation devices that make cooperation "
                                     r"an equilibrium", INST),
                (r"the point", r"institutions need not change anyone's payoffs; \ a public signal can be enough", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6)
        with self.voiceover(
            "Philosophers had seen the idea before the mathematics. <bookmark mark='a'/>David Hume wrote in 1739 that "
            "two men who pull the oars of a boat do it by an agreement or convention, though they have never given "
            "promises to each other. <bookmark mark='b'/>David Lewis's Convention, of 1969, analysed it as a "
            "regularity that each follows because the others do, sustained by the common knowledge of Part 12. "
            "<bookmark mark='c'/>Herbert Gintis has argued that social norms are choreographers: correlation "
            "devices that tell each person their part. <bookmark mark='d'/>The lesson for the social contract is "
            "that an institution need not change anyone's payoffs, as Hobbes's sovereign did. Sometimes a public "
            "signal, a red light or a custom, is enough."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
