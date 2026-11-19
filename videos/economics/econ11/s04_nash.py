from __future__ import annotations

from videos.economics.econ11.common import *  # noqa: F403


class Nash(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Nash equilibrium", r"If nobody wants to change their choice alone, is that what we will see?",
             "Chapter three. Nash equilibrium.", lit={1950: r"Nash's equilibrium"}, scale=("person", "market"))
        self.definition()
        self.curves()
        self.existence()

    def definition(self):
        head = label(r"a Nash equilibrium", font_size=34, color=EQ).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"a choice for each player such that \\ nobody can do better by changing their own choice alone",
                  font_size=27),
            MathTex(r"u_i(s_i^*, s_{-i}^*) \;\ge\; u_i(s_i, s_{-i}^*) \quad \text{for every player } i "
                    r"\text{ and every } s_i", font_size=36, color=EQ),
            label(r"the prisoner's dilemma: \ defect, defect"
                  r"\qquad the game of chapter two: \ up, middle", font_size=23, color=GREY_A),
            label(r"each player's choice is a best response to the others' \\ \emph{and} each player's beliefs about "
                  r"the others are correct", font_size=24, color=LEVEL),
            label(r"a theory of what is stable, \ not of how anyone gets there", font_size=24, color=HOLD),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "John Nash's idea is simple to state. <bookmark mark='a'/> A Nash equilibrium is a choice for each player "
            "such that nobody can do better by changing their own choice, given what the others are doing. "
            "<bookmark mark='b'/> In symbols: each player's payoff at the equilibrium is at least what any other "
            "strategy would give them, holding the others fixed. <bookmark mark='c'/> In the prisoner's dilemma the "
            "only equilibrium is that both defect; in the game of the last chapter, up and middle. "
            "<bookmark mark='d'/> Two things are packed into it: everyone is playing a best response, and everyone "
            "is right about what the others will do. <bookmark mark='e'/> It is a theory of which outcomes are "
            "stable, not of how players find them. The guessing game showed how much that second part matters."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def curves(self):
        n = load("nash")
        A, B = np.array(n["A"]), np.array(n["B"])
        mat = matrix(A, B, [r"regatta", r"market"], [r"regatta", r"market"], cell_w=1.6, cell_h=0.85,
                     font_size=24, labels_size=19).scale(0.95).to_corner(UL, buff=0.45).shift(RIGHT * 0.5)
        ax = plane([0, 1], [0, 1], center=RIGHT * 2.2 + DOWN * 0.4, x_length=5.0, y_length=5.0,
                   xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], xlabel=r"$q$: \ chance Bo goes to the regatta",
                   ylabel=r"$p$: \ chance Ana does", font_size=16)
        a = ax.ax
        eqs = n["equilibria"]
        mix = [e for e in eqs if 0 < e["p"] < 1][0]
        qs, ps = mix["q"], mix["p"]
        # Ana's best p against q: 0 below qs, 1 above; Bo's best q against p: 0 below ps, 1 above
        ana = VMobject(stroke_color=ANA, stroke_width=5).set_points_as_corners(
            [a.c2p(0, 0), a.c2p(qs, 0), a.c2p(qs, 1), a.c2p(1, 1)])
        bo = VMobject(stroke_color=BO, stroke_width=5).set_points_as_corners(
            [a.c2p(0, 0), a.c2p(0, ps), a.c2p(1, ps), a.c2p(1, 1)])
        dots = VGroup(*[Dot(a.c2p(e["q"], e["p"]), radius=0.11, color=EQ) for e in eqs])
        lab_a = label(r"Ana's best response", font_size=17, color=ANA).next_to(a.c2p(qs, 0.5), RIGHT, buff=0.1)
        lab_b = label(r"Bo's best response", font_size=17, color=BO).next_to(a.c2p(0.6, ps), UP, buff=0.08)
        side = VGroup(
            label(r"Ana prefers the regatta, \ Bo the market, \\ but both would rather be together", font_size=21),
            label(r"two equilibria in pure strategies: \\ both at the regatta, \ or both at the market", font_size=21,
                  color=EQ),
            label(rf"and a third, mixed: \ Ana goes with chance {ps:.2f}, \\ Bo with chance {qs:.2f}", font_size=21,
                  color=EQ),
            label(rf"in the mixed one, \ each expects only {mix['row']:.2f}: \\ less than the worse of the pure ones",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(mat, DOWN, buff=0.45).align_to(mat, LEFT)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Equilibria are where best responses cross. <bookmark mark='a'/> Ana and Bo want to spend Saturday "
            "together, but Ana would rather go to the regatta and Bo to the market. Game theorists call this the "
            "battle of the sexes. <bookmark mark='b'/> Let each of them choose with some probability: p is the "
            "chance Ana goes to the regatta, q the chance Bo does. Ana's best response jumps from the market to the "
            "regatta once Bo is likely enough to be there; Bo's does the same. <bookmark mark='c'/> The two "
            "best-response curves cross three times. Two crossings are the pure equilibria: both at the regatta, or "
            "both at the market. <bookmark mark='d'/> The third is mixed: Ana goes to the regatta two times in three, "
            "Bo one time in three. <bookmark mark='e'/> Then they often miss each other, and each expects only two "
            "thirds, less than in either pure equilibrium."
        ) as vo:
            self.play(FadeIn(mat), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(ax), Create(ana), Create(bo), FadeIn(lab_a), FadeIn(lab_b), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(dots[0]), FadeIn(dots[1]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(dots[2]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def existence(self):
        hc = history_card(1950, r"John Nash, \ \emph{Proceedings of the National Academy of Sciences}", r"one page: \ "
                          r"every game with finitely many players and strategies \\ has at least one equilibrium, \ "
                          r"if mixed strategies are allowed", color=EQ, width=11.4, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the proof: \ the map from strategies to best responses has a fixed point \\ (Kakutani's "
                  r"theorem; \ the next year, \ Brouwer's)", font_size=23),
            label(r"the same tool as Part 9's existence of prices, \ on the same kind of simplex", font_size=23,
                  color=GREY_A),
            label(r"von Neumann's minimax theorem (1928) had covered two-player zero-sum games", font_size=23,
                  color=GREY_A),
            label(r"existence is not prediction: \ a game can have many equilibria, \\ and players may not find any "
                  r"of them", font_size=24, color=HOLD),
        ).arrange(DOWN, buff=0.35).next_to(hc, DOWN, buff=0.55)
        tag = published_tag(r"Nash, PNAS 36(1): 48-49 (1950); \ Annals of Mathematics 54(2) (1951)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Nash's paper of 1950 was one page long. <bookmark mark='a'/> It proved that every game with finitely "
            "many players and strategies has at least one equilibrium, once players are allowed to randomize. "
            "<bookmark mark='b'/> The proof is a fixed-point argument: the map from a profile of strategies to the "
            "players' best responses must have a point that maps to itself. <bookmark mark='c'/> It is the same kind "
            "of argument, on the same kind of simplex, that proved equilibrium prices exist in Part nine. "
            "<bookmark mark='d'/> John von Neumann had proved it in 1928 for two players whose gains are each "
            "other's losses. <bookmark mark='e'/> But existence is not prediction. Some games have many equilibria, "
            "and nothing guarantees that the players will find one, as the guessing game showed."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
