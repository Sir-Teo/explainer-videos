from __future__ import annotations

from videos.philosophy.philosophy32.common import *  # noqa: F403


class Luck(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Moral luck", r"Can we be blamed for what was not in our control?", lit=(1976,),
                            part=PART)
        with self.voiceover("Chapter thirteen. Moral luck."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.drivers()
        self.kinds()
        self.ledgers()

    def drivers(self):
        d = load("luck")
        head = label(r"Ten thousand careless drivers", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["drivers"], d["killed"], d["home"]) == (10000, 6, 9994)
        rng = np.random.default_rng(7)
        n_side = 100
        hit_idx = sorted(rng.choice(n_side * n_side, size=d["killed"], replace=False).tolist())
        rgb = np.full((n_side, n_side, 3), 70, dtype=np.uint8)
        for k in hit_idx:
            rgb[k // n_side, k % n_side] = [232, 90, 90]
        rgb = np.kron(rgb, np.ones((6, 6, 1), dtype=np.uint8))
        grid = ImageMobject(rgb)
        grid.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        grid.height = 4.6
        grid.move_to([-3.6, -0.1, 0])
        side = grid.height / n_side
        tl = grid.get_corner(UL)
        rings = VGroup(*[Circle(radius=0.16, color=BAD, stroke_width=3).move_to(
            tl + np.array([(k % n_side + 0.5) * side, -(k // n_side + 0.5) * side, 0])) for k in hit_idx])
        gl = label(r"all ten thousand, \ one square each", font_size=16, color=GREY_A).next_to(grid, DOWN, buff=0.15)
        rows = stack([(r"each equally careless: \ one red light, \ run", GREY_A),
                      (r"6 had a child on the crossing; \ 9\,994 went home", BAD),
                      (r"same choice, \ same character: \ we blame the 6 far more", BLAME),
                      (r"the control principle: \ we are blameworthy only for what is in our control", LAW),
                      (r"the paradox: \ our practice and the principle disagree", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=6.2, buff=0.3).move_to([3.0, 0.2, 0])
        with self.voiceover(
            "Even without determinism, control has limits. <bookmark mark='a'/>Imagine ten thousand drivers, each "
            "equally careless: each runs one red light. The Reasoner gives each a one in two thousand chance that a "
            "child is on the crossing. <bookmark mark='b'/>Six of them kill a child. Nine thousand nine hundred and "
            "ninety four go home and forget about it. <bookmark mark='c'/>Their choices and characters were the "
            "same; only luck differed. Yet we blame the six, and they blame themselves, far more. "
            "<bookmark mark='d'/>That conflicts with a principle most of us also accept: we are morally assessable "
            "only for what is within our control. <bookmark mark='e'/>Bernard Williams and Thomas Nagel named the "
            "conflict moral luck, in a symposium of 1976."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(rings))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def kinds(self):
        head = label(r"Four kinds of luck \ (Nagel, \ 1979)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"resultant", r"how things turn out: \ the drivers; \ Williams's painter Gauguin, \ vindicated only "
                               r"by success", BAD),
                (r"circumstantial", r"the situations we face: \ a citizen of 1930s Germany, \ tested as others never "
                                    r"were", WILL),
                (r"constitutive", r"the kind of person one is: \ temperament, \ inclinations, \ capacities", SELF),
                (r"causal", r"how one is determined by antecedent circumstances: \ the free will problem itself", LAW),
                (r"responses", r"deny it \ (judge only the will); \ accept it; \ or distinguish blame from regret",
                 GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "Nagel distinguished four kinds. <bookmark mark='a'/>Resultant luck, in how things turn out: the "
            "drivers, or Williams's painter, Gauguin, who abandoned his family to paint, and whose choice only "
            "success could vindicate. <bookmark mark='b'/>Circumstantial luck, in the situations we face: an "
            "ordinary citizen of Germany in the 1930s was tested in ways others never are. "
            "<bookmark mark='c'/>Constitutive luck, in the kind of person one is: temperament, inclinations, "
            "capacities. <bookmark mark='d'/>And causal luck, in how one is determined by what came before, which "
            "Nagel saw as the free will problem itself. <bookmark mark='e'/>The responses: deny moral luck and "
            "judge only the will, as Kant would; accept it as part of morality; or, with Williams, separate the "
            "agent-regret of the unlucky driver from blame."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ledgers(self):
        d = load("ledgers")
        head = label(r"Two ledgers for the same drivers", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["drivers"], d["killed"], d["outcome_total"], d["risk_total"]) == (10000, 6, 6.0, 5.0)
        assert d["p_some_victim"] == 0.9933 and d["risk_each"] == 0.0005
        f = MathTex(r"P(\text{some child is hit}) \;=\; 1 - (1 - 0.0005)^{10\,000} \;=\; 0.9933", font_size=32,
                    color=CHANCE).next_to(head, DOWN, buff=0.35)
        unit = 1.25
        x0 = -2.3
        bar1 = VGroup(*[Rectangle(width=unit, height=0.6, stroke_color=BAD, stroke_width=2, fill_color=BAD,
                                  fill_opacity=0.75).move_to([x0 + unit * (k + 0.5), 0.6, 0]) for k in range(6)])
        bar2 = Rectangle(width=unit * 5, height=0.6, stroke_color=GREY_B, stroke_width=2, fill_color=GREY_B,
                         fill_opacity=0.35).move_to([x0 + unit * 2.5, -1.0, 0])
        ticks = VGroup(*[Line([x0 + unit * 5 * j / 60, -1.3, 0], [x0 + unit * 5 * j / 60, -0.7, 0], color=GREY_D,
                              stroke_width=1) for j in range(1, 60)])
        l1 = VGroup(label(r"by outcome", font_size=20, color=BAD),
                    label(r"6 drivers carry 1 unit each; \ 9994 carry none", font_size=16, color=GREY_A)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.08).next_to(bar1, LEFT, buff=0.3)
        l2 = VGroup(label(r"by risk", font_size=20, color=GREY_A),
                    label(r"all 10\,000 carry 0.0005 each", font_size=16, color=GREY_A)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.08).next_to(bar2, LEFT, buff=0.3)
        t1 = label(r"total 6", font_size=18, color=BAD).next_to(bar1, RIGHT, buff=0.2)
        t2 = label(r"total 5 \ = the expected harm", font_size=18, color=GREY_A).next_to(bar2, RIGHT, buff=0.2)
        side = stack([(r"Zimmerman \ (2002): \ luck changes what we are responsible for, \ not how much", SELF),
                      (r"the law mostly keeps the first ledger: \ an attempt is punished less than the deed", LAW),
                      (r"Enoch and Marmor \ (2007): \ the law's reasons need not be moral reasons", GOAL)],
                     font_size=18, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner keeps two ledgers for the ten thousand drivers. <bookmark mark='a'/>First, notice what is "
            "not luck. With ten thousand drivers each taking a one in two thousand chance, the probability that some "
            "child is hit is ninety nine point three percent. That there will be victims is close to certain. Which "
            "drivers kill is luck. <bookmark mark='b'/>The first ledger blames by outcome. Six drivers carry a full "
            "unit of blame each, and the other nine thousand nine hundred and ninety four carry none. "
            "<bookmark mark='c'/>The second blames by the risk each driver imposed. Every one of the ten thousand "
            "carries one two-thousandth of a unit, and the total is five, the expected harm. "
            "<bookmark mark='d'/>Michael Zimmerman defended the second in 2002: luck changes what we are responsible "
            "for, but not how responsible we are. Each careless driver is as blameworthy as the others. "
            "<bookmark mark='e'/>The law mostly keeps the first ledger: an attempt is usually punished less than a "
            "completed crime, though the agent did all he could. <bookmark mark='f'/>David Enoch and Andrei Marmor "
            "argued that this can be defended without moral luck, since the law has reasons of its own, such as "
            "evidence and the costs of punishing, that moral blame does not share."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar1], lag_ratio=0.2), FadeIn(l1), FadeIn(t1))
            vo.wait_until("c")
            self.play(GrowFromEdge(bar2, LEFT), FadeIn(ticks), FadeIn(l2), FadeIn(t2))
            for mk, r in zip("def", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
