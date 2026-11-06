from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class ZD(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Zero-determinant strategies", r"Can one player dictate the other's score?",
                            lit=(2012,), part=PART)
        with self.voiceover("Chapter seven. Zero-determinant strategies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.memory()
        self.trick()
        self.checked()
        self.matches()

    def memory(self):
        head = label(r"Memory-one strategies", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pos = {"CC": [-3.6, 1.2, 0], "CD": [-1.0, 1.2, 0], "DC": [-3.6, -1.4, 0], "DD": [-1.0, -1.4, 0]}
        cols = {"CC": COOP, "CD": ROW, "DC": COL, "DD": DEFECT}
        nodes = VGroup(*[VGroup(Circle(radius=0.5, color=cols[k], fill_opacity=0.15),
                                label(k, font_size=22, color=cols[k])).move_to(p) for k, p in pos.items()])
        arrows = VGroup()
        keys = list(pos)
        for a in keys:
            for b in keys:
                if a != b:
                    pa, pb = np.array(pos[a]), np.array(pos[b])
                    u = (pb - pa) / np.linalg.norm(pb - pa)
                    off = np.array([-u[1], u[0], 0]) * 0.12
                    arrows.add(Arrow(pa + u * 0.55 + off, pb - u * 0.55 + off, buff=0, color=GREY_C,
                                     stroke_width=1.5, max_tip_length_to_length_ratio=0.12))
        f = MathTex(r"\mathbf{p} = (p_{CC},\, p_{CD},\, p_{DC},\, p_{DD})", font_size=32, color=ROW).move_to(
            [3.6, 1.6, 0])
        side = stack([(r"the chance of cooperating after each outcome of the last round", GREY_A),
                      (r"tit for tat: \ (1, 0, 1, 0); \ win-stay lose-shift: \ (1, 0, 0, 1)", ROW),
                      (r"two such strategies make the game a Markov chain on four states", INST),
                      (r"long-run payoffs: \ its stationary distribution $\mathbf{v}$, \ dotted with the payoffs",
                       GOAL)], font_size=18, aligned_edge=LEFT, width=5.4, buff=0.3).move_to([3.6, -0.6, 0])
        with self.voiceover(
            "In 2012 the physicist William Press and the mathematician Freeman Dyson found something every game "
            "theorist had missed. <bookmark mark='a'/>A memory-one strategy gives the probability of cooperating "
            "after each of the four outcomes of the last round. <bookmark mark='b'/>Tit for tat is one, zero, one, "
            "zero; win-stay lose-shift is one, zero, zero, one. <bookmark mark='c'/>Two such strategies turn the "
            "repeated game into a Markov chain on the four outcomes. <bookmark mark='d'/>Each player's long-run "
            "payoff is the chain's stationary distribution, dotted with that player's payoffs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(arrows), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def trick(self):
        head = label(r"Press and Dyson's determinant", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f1 = MathTex(r"\mathbf{v}\cdot\mathbf{f} \;=\; \frac{D(\mathbf{p}, \mathbf{q}, \mathbf{f})}{D(\mathbf{p}, "
                     r"\mathbf{q}, \mathbf{1})}", font_size=34, color=INST)
        f2 = MathTex(r"D \text{ has a column } \tilde{\mathbf{p}} = (p_{CC} - 1,\; p_{CD} - 1,\; p_{DC},\; p_{DD}) "
                     r"\text{ that } X \text{ alone controls}", font_size=26, color=ROW)
        f3 = MathTex(r"\tilde{\mathbf{p}} = \alpha\,\mathbf{S}_X + \beta\,\mathbf{S}_Y + \gamma\,\mathbf{1} \;"
                     r"\Longrightarrow\; \alpha\, s_X + \beta\, s_Y + \gamma = 0", font_size=30, color=GOAL)
        f4 = MathTex(r"\text{extortion: } \; s_X - P \;=\; \chi\,(s_Y - P), \quad \chi = 3:\;\; \mathbf{p} = "
                     r"\left(\tfrac{11}{13},\, \tfrac12,\, \tfrac{7}{26},\, 0\right)", font_size=28, color=DEFECT)
        g = VGroup(f1, f2, f3, f4).arrange(DOWN, buff=0.4).move_to([0, 0.1, 0])
        foot = label(r"whatever $Y$ does, \ the column of $D$ makes the determinant vanish: \ hence `zero-determinant'",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Their insight is a determinant. <bookmark mark='a'/>The dot product of the stationary distribution with "
            "any payoff vector f can be written as a ratio of two determinants. <bookmark mark='b'/>One column of "
            "those determinants depends only on player X's strategy. <bookmark mark='c'/>If X sets that column to a "
            "combination of the two players' payoff vectors and the vector of ones, the numerator vanishes, and X "
            "has forced a linear relation between the two long-run scores, whatever Y does. "
            "<bookmark mark='d'/>One choice makes X an extortioner: X's surplus over the punishment payoff is three "
            "times Y's. With the usual payoffs, that strategy cooperates with probability eleven thirteenths after "
            "mutual cooperation, a half after being exploited, seven twenty sixths after exploiting, and never after "
            "mutual defection."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcd", g):
                vo.wait_until(mk)
                self.play(Write(f))
            self.play(FadeIn(foot))
        self.clear_scene()

    def checked(self):
        d = load("zd")
        head = label(r"Checked against 2000 random opponents", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["opponents"] == 2000 and d["ratio_min"] == 2.99998 and d["ratio_max"] == 3.0
        assert d["equalized_min"] == 2.0 and d["equalized_max"] == 2.0
        rows = stack([(r"extortioner $(11/13,\ 1/2,\ 7/26,\ 0)$: \ $(s_X - 1)/(s_Y - 1)$ ranges from 2.99998 to "
                       r"3.00000", DEFECT),
                      (r"equalizer $(2/3,\ 0,\ 2/3,\ 1/3)$: \ the opponent's score is 2.0000 against all 2000",
                       INST),
                      (r"the opponents' strategies were drawn at random: \ none can escape the relation", GREY_A)],
                     font_size=21, buff=0.4).move_to([0, 0.6, 0])
        ax = NumberLine(x_range=[2.9, 3.1, 0.05], length=8, include_numbers=True, font_size=18, color=GREY_B,
                        decimal_number_config={"num_decimal_places": 2}).move_to([0, -2.0, 0])
        rng = np.random.default_rng(1)
        dots = VGroup(*[Dot(ax.n2p(3.0) + UP * (0.15 + 0.6 * rng.random()), radius=0.03, color=DEFECT)
                        for _ in range(120)])
        al = label(r"the measured ratio, \ opponent by opponent", font_size=16, color=GREY_A).next_to(ax, DOWN,
                                                                                                  buff=0.4)
        with self.voiceover(
            "The Reasoner checks the claim. <bookmark mark='a'/>Against two thousand random memory-one opponents, the "
            "extortioner's surplus over one is always three times the opponent's: the ratio ranges from two point "
            "nine nine nine nine eight to exactly three, the difference being the tiny error added to keep the chain "
            "well behaved. <bookmark mark='b'/>A different zero-determinant strategy, an equalizer, sets the "
            "opponent's score to exactly two, whatever the opponent does. <bookmark mark='c'/>No strategy of Y's "
            "escapes the relation. One player, with memory of a single round, controls a linear constraint on both "
            "scores."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(ax), FadeIn(al))
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def matches(self):
        d = load("zd")
        head = label(r"Win every match, \ lose the tournament", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        h = d["head_to_head"]
        assert h["always cooperate"] == [3.7273, 1.9091] and h["tit for tat"] == [1.0, 1.0]
        assert d["against_itself"] == 1.0
        hd = [r"\text{opponent}", r"\text{extortioner}", r"\text{opponent's score}"]
        order = ["always cooperate", "generous tit for tat", "win-stay lose-shift", "tit for tat", "always defect"]
        cells = [[label(n, font_size=18, color=STRAT_COL[n]), label(f"{h[n][0]:.2f}", font_size=19, color=DEFECT),
                  label(f"{h[n][1]:.2f}", font_size=19, color=GREY_A)] for n in order]
        cells.append([label(r"another extortioner", font_size=18, color=STRAT_COL["extortioner"]),
                      label(f"{d['against_itself']:.2f}", font_size=19, color=BAD), label(r"1.00", font_size=19)])
        grid = ValueGrid(hd, cells, col_w=[3.6, 2.4, 2.8], cell_h=0.55, font_size=18).move_to([-2.2, -0.3, 0])
        side = stack([(r"it never scores less than its opponent", DEFECT),
                      (r"but against tit for tat, \ or itself, \ it earns only 1", BAD),
                      (r"Stewart and Plotkin \ (2013): \ in evolving populations, \ generous ZD strategies win",
                       COOP),
                      (r"Hilbe et al. \ (2014): \ human subjects punish extortion", HIST)], font_size=18,
                     aligned_edge=LEFT, width=4.4, buff=0.3).move_to([4.6, -0.2, 0])
        with self.voiceover(
            "Is extortion a winning strategy, then? <bookmark mark='a'/>Head to head, the extortioner never scores "
            "less than its opponent. Against always cooperate it earns three point seven three to one point nine "
            "one. <bookmark mark='b'/>But against tit for tat both earn one, and two extortioners earn one each: "
            "the extortioner wins every match and loses the tournament. <bookmark mark='c'/>Alexander Stewart and "
            "Joshua Plotkin showed in 2013 that in evolving populations it is the generous zero-determinant "
            "strategies, which concede the larger share to the other, that prosper. <bookmark mark='d'/>And Christian "
            "Hilbe and colleagues found that human players facing extortioners refuse to be exploited, at a cost to "
            "both. The next chapter lets strategies evolve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for k in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.4)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            for k in range(3, 6):
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.4)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
