from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class Risk(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Risk and its rivals", r"Can caring about risk itself be rational?",
                            lit=(1979, 2013), part=PART)
        with self.voiceover("Chapter seven. Risk and its rivals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.reu_formula()
        self.reu_allais()
        self.prospect_curves()
        self.fourfold()
        self.framing()

    def reu_formula(self):
        head = label(r"Risk-weighted expected utility \ (Buchak, \ 2013)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        f1 = MathTex(r"\mathbb{E}u \;=\; u(x_1) + \sum_{i \ge 2} P(\text{at least } x_i)\,\big(u(x_i) - u(x_{i-1})"
                     r"\big)", font_size=32, color=PREF)
        f2 = MathTex(r"\mathrm{REU} \;=\; u(x_1) + \sum_{i \ge 2} r\big(P(\text{at least } x_i)\big)\,\big(u(x_i) - "
                     r"u(x_{i-1})\big)", font_size=32, color=RISK)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.45).move_to([0, 1.5, 0])
        # a three-step staircase: guaranteed level, then increments weighted by chance of reaching them
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=4.2, y_length=2.6, tips=False,
                  axis_config={"color": GREY_B}).move_to([-3.6, -1.6, 0])
        xl = label(r"$p$", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.1)
        lines = VGroup(ax.plot(lambda p: p, color=PREF), ax.plot(lambda p: p ** 2, color=RISK))
        ll = VGroup(label(r"$r(p) = p$: \ expected utility", font_size=16, color=PREF),
                    label(r"$r(p) = p^2$: \ risk-avoidant", font_size=16, color=RISK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, RIGHT, buff=0.3).shift(UP * 0.5)
        side = stack([(r"order outcomes worst to best; \ start from the worst", GREY_A),
                      (r"each improvement counts by the chance of getting at least that much", PREF),
                      (r"$r$ says how much a chance is worth to you", RISK)], font_size=18, aligned_edge=LEFT,
                     width=4.6, buff=0.25).move_to([3.4, -2.3, 0])
        with self.voiceover(
            "Lara Buchak argued in 2013 that Allais's subjects need not be confused. They may care about risk "
            "itself. <bookmark mark='a'/>Expected utility can be written as a staircase: start from the utility of "
            "the worst outcome, then add each step up, weighted by the probability of getting at least that much. "
            "<bookmark mark='b'/>Risk-weighted expected utility puts a function r on those probabilities. "
            "<bookmark mark='c'/>If r of p is p, it is expected utility. If r of p is p squared, a ninety percent "
            "chance of an improvement counts for only eighty one percent of it: the agent gives more weight to how "
            "things go if they go badly. <bookmark mark='d'/>Utility says how much you value outcomes; r says how "
            "much a chance is worth to you, a separate attitude that Buchak argues reason leaves open."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), Create(lines[0]), FadeIn(ll[0]))
            self.play(Create(lines[1]), FadeIn(ll[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def reu_allais(self):
        d = load("allais")
        head = label(r"Allais, \ accommodated", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        r = d["reu"]
        assert d["u1_demo"] == 0.8 and d["reu_pattern"]
        assert r == {"1A": 0.8, "1B": 0.7861, "2A": 0.0097, "2B": 0.01}
        hd = [r"\text{lottery}", r"\text{expected utility}", r"\text{REU}, \ r(p) = p^2"]
        eu = {"1A": 0.8, "1B": 0.01 * 0 + 0.89 * 0.8 + 0.10 * 1.0, "2A": 0.11 * 0.8, "2B": 0.10}
        cells = []
        for k in ("1A", "1B", "2A", "2B"):
            cells.append([label(k, font_size=21, color=PREF), label(f"{eu[k]:.3f}", font_size=20, color=GREY_A),
                          label(f"{r[k]:.4f}", font_size=20, color=RISK)])
        grid = ValueGrid(hd, cells, col_w=[1.8, 3.0, 3.4], cell_h=0.6, font_size=19).move_to([0, 0.4, 0])
        win = VGroup(SurroundingRectangle(grid.cell[0][2], color=OK, buff=0.06),
                     SurroundingRectangle(grid.cell[3][2], color=OK, buff=0.06))
        note = label(r"$u(\$0) = 0$, \ $u(\$1\text{M}) = 0.8$, \ $u(\$5\text{M}) = 1$", font_size=18,
                     color=GREY_A).next_to(grid, UP, buff=0.3)
        foot = stack([(r"expected utility: \ the risky option in both pairs \ (or, \ above 0.91, \ the safe one in both)",
                       GREY_A),
                      (r"REU: \ 1A over 1B and 2B over 2A, \ exactly the common choices", OK)], font_size=19,
                     buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The Reasoner tests it on Allais's lotteries. <bookmark mark='a'/>Give a million dollars utility point "
            "eight, between nothing at zero and five million at one. <bookmark mark='b'/>Expected utility ranks 1B "
            "above 1A, point eight one two against point eight, and 2B above 2A: the risky option both times, as it "
            "must for any utility below point nine one. <bookmark mark='c'/>With "
            "r of p equal to p squared, 1A scores point eight and 1B only point seven eight six, because 1B's "
            "improvements are discounted for being uncertain. In the second pair 2B edges 2A, point zero one "
            "against point zero zero nine seven. <bookmark mark='d'/>That is exactly the common pattern. Allais's "
            "subjects maximize risk-weighted expected utility, and Buchak defends them as rational. Her critics "
            "answer that such agents violate the sure-thing principle, and can be led to refuse free information; "
            "chapter fourteen builds that case."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            for k in range(4):
                self.play(FadeIn(grid.cell[k][0]), FadeIn(grid.cell[k][1]), run_time=0.4)
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            for k in range(4):
                self.play(FadeIn(grid.cell[k][2]), run_time=0.4)
            self.play(Create(win))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def prospect_curves(self):
        d = load("prospect")
        prm = d["params"]
        assert prm == {"alpha": 0.88, "lambda": 2.25, "gamma": 0.61, "delta": 0.69}
        head = label(r"Prospect theory \ (Kahneman and Tversky, \ 1979; \ 1992)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        ax1 = Axes(x_range=[-100, 100, 50], y_range=[-130, 60, 50], x_length=5.0, y_length=3.8, tips=False,
                   axis_config={"color": GREY_B, "font_size": 16}, x_axis_config={"include_numbers": True}
                   ).move_to([-3.5, -0.5, 0])
        v = VMobject(color=MONEY, stroke_width=3).set_points_smoothly([ax1.c2p(x, y) for x, y in d["v_curve"]])
        t1 = label(r"value $v(x)$", font_size=20, color=MONEY).next_to(ax1, UP, buff=0.15)
        f1 = MathTex(r"v(x) = \begin{cases} x^{0.88} & x \ge 0 \\ -2.25\,(-x)^{0.88} & x < 0 \end{cases}",
                     font_size=24, color=MONEY).next_to(ax1, DOWN, buff=0.25)
        ax2 = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=3.8, y_length=3.8, tips=False,
                   axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([3.4, -0.5, 0])
        diag = DashedLine(ax2.c2p(0, 0), ax2.c2p(1, 1), color=GREY_C)
        w = VMobject(color=RISK, stroke_width=3).set_points_smoothly([ax2.c2p(p, q) for p, q in d["w_curve"]])
        t2 = label(r"decision weight $w(p)$", font_size=20, color=RISK).next_to(ax2, UP, buff=0.15)
        f2 = MathTex(r"w(p) = \frac{p^{0.61}}{\big(p^{0.61} + (1-p)^{0.61}\big)^{1/0.61}}", font_size=24,
                     color=RISK).next_to(ax2, DOWN, buff=0.25)
        with self.voiceover(
            "Kahneman and Tversky's prospect theory, of 1979, and its cumulative form of 1992, set out to describe "
            "how people actually choose. <bookmark mark='a'/>Outcomes are gains and losses from a reference point, "
            "not final wealth. The value function is concave for gains and convex for losses, and steeper for "
            "losses: in their estimates a loss counts two and a quarter times as much as an equal gain. That is "
            "loss aversion. <bookmark mark='b'/>Probabilities are replaced by decision weights. Small probabilities "
            "are overweighted and large ones underweighted: the curve lies above the diagonal near zero, and below "
            "it for most of the rest. <bookmark mark='c'/>The weights are applied, as in Buchak's theory, to "
            "cumulative probabilities: the formal core of prospect theory and of risk-weighted utility is the same, "
            "rank-dependent utility, first proposed by John Quiggin in 1982."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax1), FadeIn(t1))
            self.play(Create(v), Write(f1))
            vo.wait_until("b")
            self.play(Create(ax2), FadeIn(t2), Create(diag))
            self.play(Create(w), Write(f2))
            vo.wait_until("c")
            self.play(Indicate(f2, color=WHITE))
        self.clear_scene()

    def fourfold(self):
        d = load("prospect")
        head = label(r"The fourfold pattern, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ff = d["fourfold"]
        assert [r["ce"] for r in ff] == [9.98, 76.85, -8.26, -83.12]
        hd = [r"\text{prospect}", r"\text{expected value}", r"\text{certainty equivalent}", r"\text{attitude}"]
        att = [(r"risk-seeking: \ lotteries", RISK), (r"risk-averse: \ settlements", EVID),
               (r"risk-averse: \ insurance", EVID), (r"risk-seeking: \ gambling to avoid a loss", RISK)]
        names = [r"5\% chance of \$100", r"95\% chance of \$100", r"5\% chance of $-$\$100",
                 r"95\% chance of $-$\$100"]
        cells = []
        for row, nm, (a, c) in zip(ff, names, att):
            cells.append([label(nm, font_size=18, color=MONEY), label(f"{row['ev']:.0f}", font_size=19,
                                                                      color=GREY_A),
                          label(f"{row['ce']:.2f}", font_size=19, color=WHITE), label(a, font_size=17, color=c)])
        grid = ValueGrid(hd, cells, col_w=[3.4, 2.4, 3.2, 3.8], cell_h=0.62, font_size=18).move_to([0, 0.3, 0])
        foot = stack([(r"certainty equivalent: \ the sure amount valued the same as the prospect", GREY_A),
                      (r"industry: \ insurance pricing, \ default options, \ framing of pensions and offers", GOAL)],
                     font_size=19, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "From these two curves follows a famous pattern. <bookmark mark='a'/>A five percent chance of a hundred "
            "dollars has expected value five, but in the theory it is worth ten dollars for sure: people overpay "
            "for long shots, which is why lotteries sell. <bookmark mark='b'/>A ninety five percent chance of a "
            "hundred is worth only seventy seven: people accept settlements below the expected award. "
            "<bookmark mark='c'/>A five percent chance of losing a hundred is as bad as a sure loss of eight: people "
            "insure. <bookmark mark='d'/>A ninety five percent chance of losing a hundred is only as bad as a sure "
            "loss of eighty three: facing likely losses, people gamble to escape them. <bookmark mark='e'/>Risk "
            "attitudes flip between gains and losses, and between small and large chances. Insurers, regulators "
            "and anyone designing a default pension scheme now rely on this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.6)
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def framing(self):
        d = load("framing")
        head = label(r"The same choice, \ framed twice \ (Tversky and Kahneman, \ 1981)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        assert (d["A"], d["B"], d["C"], d["D"]) == (105.9, 93.55, -438.53, -353.15)
        assert d["gain_frame_choice"] == "A" and d["loss_frame_choice"] == "D"
        rep = d["reported"]
        assert (rep["A"], rep["D"], rep["n_gain"], rep["n_loss"]) == (0.72, 0.78, 152, 155)
        intro = label(r"600 people face a disease; \ two programs", font_size=20, color=GREY_A).next_to(
            head, DOWN, buff=0.3)
        hd = [r"\text{frame}", r"\text{program}", r"\text{prospect theory value}", r"\text{chosen by}"]
        rows = [(r"lives saved", r"A: \ 200 saved for sure", f"{d['A']:.1f}", r"72\% \ (of 152)", OK),
                (r"lives saved", r"B: \ 1/3 chance all 600 saved", f"{d['B']:.1f}", r"28\%", GREY_A),
                (r"deaths", r"C: \ 400 die for sure", f"{d['C']:.1f}", r"22\%", GREY_A),
                (r"deaths", r"D: \ 2/3 chance all 600 die", f"{d['D']:.1f}", r"78\% \ (of 155)", OK)]
        cells = [[label(a, font_size=18, color=EVID if a == r"lives saved" else BAD), label(b, font_size=18),
                  label(c, font_size=19, color=PREF), label(e, font_size=18, color=col)]
                 for a, b, c, e, col in rows]
        grid = ValueGrid(hd, cells, col_w=[2.2, 4.4, 3.4, 2.6], cell_h=0.58, font_size=18).move_to([0, -0.2, 0])
        picks = VGroup(SurroundingRectangle(VGroup(*grid.cell[0]), color=OK, buff=0.05),
                       SurroundingRectangle(VGroup(*grid.cell[3]), color=OK, buff=0.05))
        foot = stack([(r"A is C, \ and B is D: \ the options are identical", GOAL),
                      (r"concave for gains: \ take the sure thing; \ convex and loss-averse for losses: \ gamble",
                       PREF),
                      (r"for a theory of rational choice: \ descriptions should not matter \ (extensionality)",
                       BAD)], font_size=18, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Prospect theory's most famous prediction is the framing effect. <bookmark mark='a'/>In 1981 Tversky "
            "and Kahneman told subjects that six hundred people face a disease, and offered two programs. Framed in "
            "lives saved: program A saves two hundred for sure; program B saves all six hundred with probability one "
            "third. Seventy two percent of a hundred and fifty two subjects chose A. <bookmark mark='b'/>Framed in "
            "deaths: under C four hundred die for sure; under D, with probability two thirds all six hundred die. "
            "Seventy eight percent of another group chose D. <bookmark mark='c'/>But A is C and B is D, described "
            "differently. <bookmark mark='d'/>The Reasoner values all four with prospect theory's parameters. In the "
            "frame of gains the sure thing is worth more, a hundred and six against ninety four; in the frame of "
            "losses the gamble is less bad, minus three hundred and fifty three against minus four hundred and "
            "thirty nine. The theory predicts the flip. <bookmark mark='e'/>For a theory of how one ought to choose, "
            "this is the clearest mistake in the catalogue: a choice should not depend on how the same options are "
            "described. Kenneth Arrow called that principle extensionality."
        ) as vo:
            self.play(FadeIn(head), FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            self.play(*[FadeIn(grid.cell[0][k]) for k in (0, 1, 3)], *[FadeIn(grid.cell[1][k]) for k in (0, 1, 3)])
            self.play(Create(picks[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[2][k]) for k in (0, 1, 3)], *[FadeIn(grid.cell[3][k]) for k in (0, 1, 3)])
            self.play(Create(picks[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[r][2]) for r in range(4)], FadeIn(foot[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot[2]))
        self.clear_scene()
