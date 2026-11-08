from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class StagHunt(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"The stag hunt", r"Which equilibrium will people find?", lit=(1755,), part=PART)
        with self.voiceover("Chapter three. The stag hunt."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rousseau()
        self.basins()
        self.selection()
        self.kmr()

    def rousseau(self):
        q = quote_card(r"If it was a matter of hunting a deer, \ everyone well realized that he must remain faithfully "
                       r"at his post; \ but if a hare happened to pass within reach of one of them, \ we cannot doubt "
                       r"that he would have gone off in pursuit of it without scruple.", r"Jean-Jacques Rousseau",
                       r"\textit{Discourse on the Origin of Inequality} \ (1755)", width=10.4,
                       font_size=26).move_to([0, 1.4, 0])
        d = load("equilibria")["stag hunt"]
        bm = bimatrix(d["A"], d["B"], d["acts"], font_size=20, cell=1.15, center=[-2.6, -2.0, 0])
        side = stack([(r"two pure equilibria: \ (stag, stag) pays 4, \ (hare, hare) pays 3", GOAL),
                      (r"no one is tempted to defect from the stag hunt: \ it is not a dilemma", COOP),
                      (r"but stag is risky: \ alone, \ the stag hunter gets nothing", BAD)], font_size=18,
                     aligned_edge=LEFT, width=5.2, buff=0.22).move_to([3.4, -2.0, 0])
        with self.voiceover(
            "In 1755 Jean-Jacques Rousseau told a story of hunters. <bookmark mark='a'/>If it was a matter of hunting "
            "a deer, everyone well realized that he must remain faithfully at his post; but if a hare happened to "
            "pass within reach of one of them, he would have gone off after it without scruple. "
            "<bookmark mark='b'/>In the game, hunting stag together pays four each; a hare pays three whatever the "
            "other does; and a lone stag hunter gets nothing. <bookmark mark='c'/>There are two equilibria. Unlike "
            "the dilemma, no one is tempted to leave the stag hunt if the others stay: cooperation is stable. "
            "<bookmark mark='d'/>The problem is trust. Hunting stag pays only if enough others do."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(bm))
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def basins(self):
        d = load("stag")
        head = label(r"Two basins", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert d["threshold"] == 0.75 and d["basin_stag"] == 0.25
        f = MathTex(r"u(\text{stag}) = 4x, \qquad u(\text{hare}) = 3 \qquad\Rightarrow\qquad \text{stag pays iff } "
                    r"x > \tfrac{3}{4}", font_size=32, color=COOP).move_to([0, 1.8, 0])
        line = NumberLine(x_range=[0, 1, 0.25], length=10, include_numbers=True, font_size=20, color=GREY_B,
                          decimal_number_config={"num_decimal_places": 2}).move_to([0, 0, 0])
        xl = label(r"$x$: \ share of the population hunting stag", font_size=18, color=GREY_A).next_to(line, DOWN,
                                                                                                   buff=0.5)
        cut = line.n2p(0.75)
        tick = Line(cut + UP * 0.4, cut + DOWN * 0.4, color=WHITE, stroke_width=4)
        left = VGroup(*[Arrow(line.n2p(x) + UP * 0.6, line.n2p(x - 0.12) + UP * 0.6, buff=0, color=DEFECT,
                              stroke_width=4, max_tip_length_to_length_ratio=0.3) for x in (0.2, 0.4, 0.6)])
        right = Arrow(line.n2p(0.82) + UP * 0.6, line.n2p(0.95) + UP * 0.6, buff=0, color=COOP, stroke_width=4,
                      max_tip_length_to_length_ratio=0.3)
        bl = VGroup(label(r"basin of hare: \ 3/4 of the line", font_size=18, color=DEFECT).next_to(line.n2p(0.37),
                                                                                                 UP, buff=1.0),
                    label(r"basin of stag: \ 1/4", font_size=18, color=COOP).next_to(line.n2p(0.88), UP, buff=1.0))
        foot = label(r"under any dynamics that moves toward the better reply, \ the population ends at an extreme",
                     font_size=19, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Put the game in a population. <bookmark mark='a'/>If a share x of the population hunts stag, a stag "
            "hunter earns four x on average and a hare hunter three. Stag pays only when x exceeds three quarters. "
            "<bookmark mark='b'/>Below that point the population drifts toward hare; above it, toward stag. "
            "<bookmark mark='c'/>The basin of hunting hare is three quarters of all starting points; the basin of the "
            "better outcome only a quarter. <bookmark mark='d'/>Under any dynamics in which people move toward the "
            "better reply, the population ends at one extreme or the other, and which one depends on where it "
            "starts."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(xl), Create(tick))
            self.play(*[GrowArrow(a) for a in left], GrowArrow(right))
            vo.wait_until("c")
            self.play(FadeIn(bl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def selection(self):
        head = label(r"Payoff dominance against risk dominance \ (Harsanyi and Selten, \ 1988)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        rows = [(r"payoff dominance", r"(stag, stag) is better for everyone than (hare, hare): \ choose it", COOP),
                (r"risk dominance", r"compare the losses from deviating: \ $(3 - 0)(3 - 0) > (4 - 3)(4 - 3)$, \ so "
                                    r"(hare, hare) is less risky", DEFECT),
                (r"equivalently", r"against a partner who is equally likely to do either, \ hare earns 3, \ "
                                  r"stag only 2", GREY_A),
                (r"Skyrms \ (2004)", r"\textit{The Stag Hunt and the Evolution of Social Structure}: \ the social "
                                     r"contract is a stag hunt, \ and the question is how trust is built", HIST)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6)
        with self.voiceover(
            "Which equilibrium is rational? John Harsanyi and Reinhard Selten wrote a book in 1988 to answer such "
            "questions, and found two competing criteria. <bookmark mark='a'/>Payoff dominance: the stag "
            "equilibrium is better for everyone, so rational players should coordinate on it. "
            "<bookmark mark='b'/>Risk dominance: compare the losses from a unilateral mistake at each equilibrium. "
            "The product of those losses is nine at hare and one at stag, so hare is less risky. "
            "<bookmark mark='c'/>Equivalently, against a partner equally likely to do either, hare earns three and "
            "stag only two. <bookmark mark='d'/>Brian Skyrms argued in 2004 that the social contract is better "
            "modelled by the stag hunt than by the dilemma: cooperation can be stable, and the problem of politics "
            "is how to build the trust that reaches it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def kmr(self):
        d = load("stag")
        head = label(r"The long run: \ stochastic stability \ (Kandori, \ Mailath and Rob, \ 1993)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        runs = d["runs"]
        assert d["N"] == 10 and [r["eps"] for r in runs] == [0.1, 0.05, 0.02]
        assert [r["share_time_hare"] for r in runs] == [0.9998, 0.9993, 0.9934]
        hd = [r"\text{mutation rate } \varepsilon", r"\text{share of time at all-hare}"]
        cells = [[label(f"{r['eps']:g}", font_size=20, color=GREY_A),
                  label(f"{100 * r['share_time_hare']:.1f}\\%", font_size=20, color=DEFECT)] for r in runs]
        grid = ValueGrid(hd, cells, col_w=[3.4, 4.2], cell_h=0.6, font_size=19).move_to([-2.4, 0.2, 0])
        side = stack([(r"10 hunters best-respond; \ each errs with probability $\varepsilon$", GREY_A),
                      (r"leaving all-stag takes 3 simultaneous errors; \ leaving all-hare takes 8", GOAL),
                      (r"as $\varepsilon \to 0$ the population is almost always at the risk-dominant equilibrium",
                       DEFECT),
                      (r"started at all-stag; \ 1\,000\,000 periods", GREY_A)], font_size=18, aligned_edge=LEFT,
                     width=5.0, buff=0.3).move_to([4.0, 0.0, 0])
        with self.voiceover(
            "Evolution gives its own answer. <bookmark mark='a'/>Michihiro Kandori, George Mailath and Rafael Rob "
            "studied a population that best-responds, but in which each member occasionally errs at random. The "
            "Reasoner runs ten hunters for a million periods, starting from everyone hunting stag. "
            "<bookmark mark='b'/>To knock the population out of all-stag takes three simultaneous errors; to knock "
            "it out of all-hare takes eight. <bookmark mark='c'/>So the population spends more than ninety nine percent "
            "of its time hunting hare, at every error rate tried; once it reaches all-hare it almost never leaves. "
            "<bookmark mark='d'/>The stochastically stable equilibrium is the risk-dominant one. Trust is fragile in "
            "a precise sense: it takes fewer mistakes to lose it than to win it back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Indicate(grid.cell[2][1], color=WHITE))
        self.clear_scene()
