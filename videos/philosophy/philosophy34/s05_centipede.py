from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Centipede(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Backward induction", r"Should you take the money at once?", lit=(1981, 1995),
                            part=PART)
        with self.voiceover("Chapter four. Backward induction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.game()
        self.qre()
        self.paradox()
        self.wall_brick()

    def tree(self, d, y=0.6):
        n = d["nodes"]
        xs = [-5.6 + 1.9 * k for k in range(n)]
        nodes, takes, labels = VGroup(), VGroup(), VGroup()
        for k, x in enumerate(xs):
            col = ROW if k % 2 == 0 else COL
            nodes.add(Circle(radius=0.28, color=col, fill_opacity=0.3).move_to([x, y, 0]))
            nodes[-1].add(label("1" if k % 2 == 0 else "2", font_size=16, color=WHITE).move_to([x, y, 0]))
            a, b = d["take_payoffs"][k]
            takes.add(Line([x, y - 0.28, 0], [x, y - 1.3, 0], color=GREY_B))
            labels.add(VGroup(MathTex(f"{a:g}", font_size=20, color=ROW), MathTex(f"{b:g}", font_size=20, color=COL)
                              ).arrange(DOWN, buff=0.06).next_to([x, y - 1.3, 0], DOWN, buff=0.08))
        passes = VGroup(*[Line(nodes[k].get_right(), nodes[k + 1].get_left(), color=GREY_B) for k in range(n - 1)])
        endx = xs[-1] + 1.5
        passes.add(Line(nodes[-1].get_right(), [endx, y, 0], color=GREY_B))
        a, b = d["end"]
        end = VGroup(MathTex(f"{a:g}", font_size=20, color=ROW), MathTex(f"{b:g}", font_size=20, color=COL)).arrange(
            DOWN, buff=0.06).next_to([endx, y, 0], RIGHT, buff=0.1)
        return VGroup(nodes, takes, labels, passes, end), xs

    def game(self):
        d = load("centipede")
        head = label(r"The centipede \ (Rosenthal, \ 1981)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["nodes"] == 6 and d["backward_takes_everywhere"] and d["spe_payoff"] == [3.2, 0.8]
        assert d["end"] == [204.8, 51.2]
        tr, xs = self.tree(d)
        cap = label(r"right: \ pass, \ and the pot doubles; \ down: \ take the larger share", font_size=18,
                    color=GREY_A).to_edge(DOWN, buff=1.6)
        bi = VGroup(*[Arrow([x, 1.6, 0], [x, 1.05, 0], buff=0, color=DEFECT, stroke_width=4) for x in xs])
        order = label(r"backward induction: \ at the last node, \ take; \ so at the one before, \ take; \ \dots",
                      font_size=19, color=DEFECT).to_edge(DOWN, buff=1.0)
        res = label(r"the unique subgame-perfect equilibrium: \ take at once, \ (3.2, 0.8), \ though (204.8, 51.2) "
                    r"was on offer", font_size=19, color=BAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Robert Rosenthal described this game in 1981. <bookmark mark='a'/>Two players take turns. At each node "
            "the mover can take the larger share of a pot, ending the game, or pass, and the pot doubles. After six "
            "passes, the pot of two hundred and fifty six is split, with the larger share going to the first "
            "player. <bookmark mark='b'/>Reason backward. At the last node the second player takes, getting a "
            "hundred and two rather than fifty one. Knowing that, the first player takes at the node before, and so "
            "on down to the first node. <bookmark mark='c'/>The unique subgame perfect equilibrium is to take at "
            "once: three point two and point eight, when two hundred and five and fifty one were on offer to the "
            "same two players."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tr), FadeIn(cap))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in reversed(bi)], lag_ratio=0.3), FadeIn(order), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.clear_scene()

    def qre(self):
        d = load("centipede")
        head = label(r"Noisy players pass", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["qre"]
        assert [r["lambda"] for r in rows] == [0.0, 0.5, 1.0, 2.0, 5.0, 20.0]
        assert rows[-1]["ends_at"][0] == 1.0
        f = MathTex(r"P(\text{take}) = \frac{1}{1 + e^{-\lambda g}}, \quad g = \text{relative gain from taking}",
                    font_size=28, color=GOAL).next_to(head, DOWN, buff=0.3)
        show = [rows[0], rows[3], rows[4], rows[5]]
        ax_w, ax_h = 9.0, 0.5
        bars = VGroup()
        for k, r in enumerate(show):
            y = 0.9 - 0.9 * k
            x = -3.6
            seg = VGroup()
            for j, share in enumerate(r["ends_at"]):
                w = ax_w * share
                if w > 0.005:
                    col = (ROW if j % 2 == 0 else COL) if j < 6 else COOP
                    seg.add(Rectangle(width=w, height=ax_h, stroke_width=0.5, stroke_color=BLACK, fill_color=col,
                                      fill_opacity=0.25 + 0.12 * j).move_to([x + w / 2, y, 0]))
                x += w
            lab = label(rf"$\lambda = {r['lambda']:g}$", font_size=18, color=WHITE).next_to([-3.6, y, 0], LEFT,
                                                                                        buff=0.2)
            bars.add(VGroup(lab, seg))
        key = label(r"where the game ends: \ node 1, \ 2, \ \dots, \ 6, \ or after all six passes \ (green)",
                    font_size=17, color=GREY_A).next_to(bars, DOWN, buff=0.35)
        side = label(r"McKelvey and Palfrey \ (1992): \ in the laboratory, \ few take at once", font_size=19,
                     color=HIST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In the laboratory almost no one takes at once. Richard McKelvey and Thomas Palfrey found in 1992 that "
            "most games run several nodes. <bookmark mark='a'/>One explanation: players are noisy. The Reasoner "
            "lets each mover take with a probability that rises with the relative gain from taking, sharpened by a "
            "rationality parameter lambda, and solves the game backward. <bookmark mark='b'/>With lambda zero, "
            "choices are coin flips. <bookmark mark='c'/>With lambda two, games end all along the centipede. "
            "<bookmark mark='d'/>With lambda five, players pass early and take near the end, the pattern of "
            "experiments: since the other might pass, passing is worth a lot. <bookmark mark='e'/>Only with lambda "
            "twenty does everyone take at once. A little doubt about the other's rationality makes passing "
            "rational."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side))
            vo.wait_until("a")
            self.play(Write(f))
            for mk, b in zip("bcde", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b[0]), LaggedStart(*[GrowFromEdge(s, LEFT) for s in b[1]], lag_ratio=0.1))
                if mk == "b":
                    self.play(FadeIn(key))
        self.clear_scene()

    def paradox(self):
        head = label(r"The paradox of backward induction", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the argument", r"at node 3, \ player 1 takes, \ because player 2 would take at node 4 \dots", GREY_A),
                (r"but", r"node 3 is reached only if player 2 passed at node 2: \ which a backward-inductive player "
                         r"would never do", BAD),
                (r"Binmore; \ Bicchieri; \ Reny", r"reasoning that assumes rationality at nodes it shows unreachable "
                                                   r"undermines itself \ (1987; \ 1989; \ 1992)", DEFECT),
                (r"Aumann \ (1995)", r"with common knowledge of rationality, \ backward induction is right: \ the "
                                     r"contradiction never arises, \ because those nodes are never reached", HIST),
                (r"Stalnaker \ (1998)", r"it depends how players would revise their beliefs off the path: \ "
                                        r"Part 14's belief revision, \ in a game", INST)]
        g = rows_table(rows, top=1.7, gap=0.42, width=8.2, x_text=-1.8)
        with self.voiceover(
            "The theory is not only refuted in the laboratory. It may be incoherent. <bookmark mark='a'/>Backward "
            "induction says that at node three player one takes, because player two would take at node four. "
            "<bookmark mark='b'/>But node three is reached only if player two passed at node two, which a "
            "backward-inductive player never does. Why expect rationality at node four from someone who has just "
            "shown she does not follow it? <bookmark mark='c'/>Ken Binmore, Cristina Bicchieri and Philip Reny "
            "argued that the reasoning undermines itself. <bookmark mark='d'/>Robert Aumann proved in 1995 that "
            "common knowledge of rationality does imply backward induction; the contradiction never arises, because "
            "the strange nodes are never reached. <bookmark mark='e'/>Robert Stalnaker replied that everything turns "
            "on how players would revise their beliefs if they were reached: Part 14's theory of belief revision, "
            "inside a game."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=34, current=34).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(34, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty fourth brick in the Wall. <bookmark mark='a'/>The dream was that individual "
            "rationality, practised by everyone, would be collectively rational. The prisoner's dilemma shows "
            "rational players reaching an outcome every one of them regrets, and backward induction shows the "
            "theory recommending, against a cooperative partner, a move that throws almost everything away, by "
            "reasoning that may not even be coherent. <bookmark mark='b'/>What it forces is a choice: change the "
            "game, with institutions, repetition and enforcement, or change our idea of what rationality requires."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[34], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
