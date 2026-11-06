from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class Discount(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Discounting the future", r"Is a harm in a century worth less than a harm today?",
                            lit=(1928, 2006), part=PART)
        with self.voiceover("Chapter six. Discounting the future."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ramsey()
        self.stern()
        self.policy()
        self.hazard()
        self.weitzman()

    def ramsey(self):
        head = label(r"The Ramsey rule \ (1928), \ derived", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f1 = MathTex(r"\max \int_0^\infty e^{-\delta t}\, u(c_t)\, dt, \qquad u(c) = \frac{c^{1-\eta}}{1-\eta}",
                     font_size=32, color=WHITE)
        f2 = MathTex(r"u'(c_0) \;=\; e^{-\delta t}\, e^{r t}\, u'(c_t)", font_size=32, color=FUT)
        f3 = MathTex(r"c_0^{-\eta} \;=\; e^{(r - \delta) t}\, c_0^{-\eta} e^{-\eta g t} \;\;\Longrightarrow\;\; "
                     r"r \;=\; \delta + \eta\, g", font_size=34, color=GOAL)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.45).move_to([0, 0.9, 0])
        notes = stack([(r"give up a unit now, \ invest it at rate $r$, \ consume $e^{rt}$ at time $t$: \ at the optimum "
                        r"you are indifferent", FUT),
                       (r"$\delta$: \ pure time preference; \ $\eta$: \ how fast marginal utility falls; \ $g$: \ "
                        r"growth, \ so the future is richer", GREY_A),
                       (r"Ramsey on $\delta > 0$: \ ``ethically indefensible and arises merely from the weakness of "
                        r"the imagination''", RISK)],
                      font_size=19, aligned_edge=LEFT, width=11.4, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Climate policy weighs costs now against harms a century away, and the weighing runs through a discount "
            "rate. Frank Ramsey derived it in 1928. <bookmark mark='a'/>A planner maximizes the sum over time of "
            "utility from consumption, discounted at a rate delta, with a utility function whose curvature is eta. "
            "<bookmark mark='b'/>Give up one unit of consumption now, invest it at rate r, and consume e to the r t "
            "at time t. At the optimum the planner is indifferent, so the marginal utility now equals the discounted "
            "marginal utility of the return. <bookmark mark='c'/>With consumption growing at rate g, the marginal "
            "utilities cancel, and out comes the Ramsey rule: r equals delta plus eta times g. "
            "<bookmark mark='d'/>Two very different reasons to discount appear. Eta times g says the future will be "
            "richer, and a dollar matters less to the rich: that is Part 35's diminishing marginal utility, applied "
            "across time. Delta says the future matters less just because it is later. <bookmark mark='e'/>Ramsey "
            "himself called that ethically indefensible, a practice that arises merely from the weakness of the "
            "imagination."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Write(f3))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def stern(self):
        d = load("ramsey")
        s, n = d["views"]["Stern"], d["views"]["Nordhaus"]
        head = label(r"Stern against Nordhaus", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (s["delta"], s["eta"], s["g"], s["r"]) == (0.1, 1.0, 1.3, 1.4)
        assert (n["delta"], n["eta"], n["g"], n["r"]) == (1.5, 2.0, 2.0, 5.5)
        assert (s["pv"]["100"], n["pv"]["100"], d["ratio_100"]) == (249003, 4729, 52.7)
        ax = Axes(x_range=[0, 200, 50], y_range=[0, 1, 0.25], x_length=6.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True},
                  y_axis_config={"decimal_number_config": {"num_decimal_places": 2}}).move_to([-3.3, -0.9, 0])
        xl = label(r"years from now", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.42)
        yl = label(r"weight on a dollar of damage", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        ts = list(range(0, 201, 5))
        cs = VMobject(color=WELL, stroke_width=3).set_points_smoothly([ax.c2p(t, v) for t, v in zip(ts, s["curve"])])
        cn = VMobject(color=MONEY, stroke_width=3).set_points_smoothly([ax.c2p(t, v) for t, v in zip(ts, n["curve"])])
        ls = label(r"Stern: \ 1.4\%", font_size=16, color=WELL).next_to(ax.c2p(150, s["curve"][30]), UP, buff=0.12)
        ln = label(r"Nordhaus: \ 5.5\%", font_size=16, color=MONEY).next_to(ax.c2p(60, n["curve"][12]), UR,
                                                                            buff=0.1)
        hd = [r"", r"\delta", r"\eta", r"g", r"r", r"\$1\text{M in 100 years}"]
        cells = [[label(k, font_size=18, color=c), label(f"{v['delta']:g}\\%", font_size=18),
                  label(f"{v['eta']:g}", font_size=18), label(f"{v['g']:g}\\%", font_size=18),
                  label(f"{v['r']:g}\\%", font_size=18, color=c), label(f"\\${v['pv']['100']:,.0f}", font_size=18, color=c)]
                 for k, v, c in (("Stern", s, WELL), ("Nordhaus", n, MONEY))]
        grid = ValueGrid(hd, cells, col_w=[1.7, 0.9, 0.8, 0.9, 1.0, 2.3], cell_h=0.5, font_size=17).move_to(
            [3.6, 1.0, 0])
        side = stack([(r"the same damage, \ weighed 53 times more heavily by Stern", GOAL),
                      (r"Stern Review \ (2006): \ about \$85 a tonne of CO$_2$; \ Nordhaus's figure a small fraction "
                       r"of that", GREY_A),
                      (r"US EPA \ (2023): \ \$190 a tonne at a 2\% rate \ (2020 dollars)", GREY_A),
                      (r"the gap is mostly ethics, \ $\delta$ and $\eta$: \ not climate science", RISK)],
                     font_size=17, aligned_edge=LEFT, width=5.6, buff=0.22).move_to([3.6, -1.5, 0])
        with self.voiceover(
            "Two famous reports disagreed by an order of magnitude. <bookmark mark='a'/>Nicholas Stern's review of "
            "2006 set delta at a tenth of a percent, only to allow for extinction, eta at one, and growth at one point "
            "three: a rate of one point four percent. <bookmark mark='b'/>William Nordhaus, calibrating to market "
            "interest rates, used delta one and a half, eta two and growth two: five and a half percent. "
            "<bookmark mark='c'/>The curves show what that does. A million dollars of damage in a hundred years is "
            "worth two hundred and forty nine thousand dollars today to Stern, and four thousand seven hundred to "
            "Nordhaus: fifty three times less. <bookmark mark='d'/>Stern put the social cost of carbon at about "
            "eighty five dollars a tonne of carbon dioxide; Nordhaus's figure was a small fraction of that. In 2023 "
            "the United States Environmental Protection Agency used a hundred and ninety dollars a tonne, at a two "
            "percent rate. <bookmark mark='e'/>The disagreement is mostly not about climate science. It is about "
            "delta and eta: whether later people matter less, and how much inequality between generations matters."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0][:5]])
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[1][:5]])
            vo.wait_until("c")
            self.play(Create(cs), Create(cn), FadeIn(ls), FadeIn(ln), run_time=2)
            self.play(FadeIn(grid.cell[0][5]), FadeIn(grid.cell[1][5]), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def policy(self):
        d = load("policy")
        s, n = d["Stern"], d["Nordhaus"]
        head = label(r"One policy, \ two verdicts", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (s["gdp_later"], s["benefit"], s["pv"], s["worth_it"]) == (363.9, 18.19, 4.53, True)
        assert (n["gdp_later"], n["benefit"], n["pv"], n["worth_it"]) == (724.5, 36.22, 0.171, False)
        f = MathTex(r"\text{worth it} \iff \frac{0.05 \times Y_{100}}{(1 + r)^{100}} \;>\; 0.01 \times Y_0",
                    font_size=34, color=WHITE).move_to([0, 1.9, 0])
        hd = [r"", r"\text{output in 100 years}", r"\text{damage avoided}", r"\text{its value today}",
              r"\text{cost today}", r"\text{verdict}"]
        cells = [[label(k, font_size=19, color=c), label(f"{v['gdp_later']:.1f}", font_size=19),
                  label(f"{v['benefit']:.2f}", font_size=19), label(f"{v['pv']:.3f}", font_size=19, color=c),
                  label(f"{v['cost']:.0f}", font_size=19),
                  label(r"act" if v["worth_it"] else r"wait", font_size=19, color=OK if v["worth_it"] else BAD)]
                 for k, v, c in (("Stern", s, WELL), ("Nordhaus", n, MONEY))]
        grid = ValueGrid(hd, cells, col_w=[1.8, 2.8, 2.4, 2.2, 1.8, 1.4], cell_h=0.58, font_size=17).move_to(
            [0, 0.2, 0])
        foot = stack([(r"today's output 100; \ spend 1 now to avoid losing 5\% of output in a century", GREY_A),
                      (r"faster growth makes Nordhaus's future richer, \ so the damage is larger in dollars, \ and "
                       r"still worth less today", MONEY),
                      (r"Stern: \ the benefit is worth 4.5 times the cost; \ Nordhaus: \ a sixth of it", GOAL)],
                     font_size=19, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is what the disagreement does to a single decision. <bookmark mark='a'/>Today's output is a hundred. "
            "A policy costs one percent of it now, and avoids a loss of five percent of output a century from now. "
            "<bookmark mark='b'/>With Stern's growth, output in a hundred years is three hundred and sixty four, so "
            "the damage avoided is eighteen; discounted at one point four percent it is worth four and a half today, "
            "four and a half times the cost. Act. <bookmark mark='c'/>With Nordhaus's faster growth, the future is "
            "richer and the damage larger, thirty six; but discounted at five and a half percent it is worth less "
            "than a fifth of the cost. Wait. <bookmark mark='d'/>The same science, the same policy, opposite "
            "verdicts, from two choices about ethics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def hazard(self):
        d = load("hazard")
        head = label(r"Stern's $\delta$ as a chance of extinction", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert (d["delta"], d["survive_100"], d["survive_1000"]) == (0.1, 0.9048, 0.3677)
        assert (d["ord_annual"], d["ord_survive_100"]) == (0.1823, 0.8333)
        f = MathTex(r"e^{-\delta t}\;\approx\;(1 - h)^t:\quad \text{a weight on the future} \;=\; "
                    r"\text{the chance there is one}", font_size=32, color=FUT).move_to([0, 1.8, 0])
        hd = [r"", r"\text{annual rate}", r"\text{survive a century}", r"\text{survive a millennium}"]
        cells = [[label(r"Stern's $\delta$", font_size=19, color=WELL), label(r"0.1\%", font_size=19),
                  label(r"0.905", font_size=19), label(r"0.368", font_size=19)],
                 [label(r"Ord's 1 in 6 a century", font_size=19, color=RISK), label(r"0.18\%", font_size=19),
                  label(r"0.833", font_size=19), label(r"--", font_size=19, color=GREY_A)]]
        grid = ValueGrid(hd, cells, col_w=[3.6, 2.2, 2.8, 3.0], cell_h=0.6, font_size=17).move_to([0, 0.1, 0])
        foot = stack([(r"Stern defended $\delta > 0$ only as the risk that there will be no future generations", WELL),
                      (r"read that way, \ $\delta$ is not impatience but probability, \ and Ramsey's objection "
                       r"does not apply", FUT),
                      (r"an estimate like Ord's would justify nearly twice Stern's $\delta$: \ the long future and "
                       r"the discount rate are one question", GOAL)],
                     font_size=19, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Stern's small delta has a second reading, which connects this chapter to the next. "
            "<bookmark mark='a'/>He defended a positive pure rate only as the chance that there will be no future "
            "generations at all. A weight on the future, read this way, is the probability that there is one. "
            "<bookmark mark='b'/>A tenth of a percent a year means a ninety point five percent chance that humanity "
            "survives the next century, and thirty seven percent that it survives a thousand years. "
            "<bookmark mark='c'/>Toby Ord's estimate of one in six this century corresponds to an annual rate of "
            "about point one eight percent, nearly twice Stern's. <bookmark mark='d'/>On this reading delta is not "
            "impatience but probability, and Ramsey's objection does not apply. How much the far future should count "
            "and how likely it is to exist turn out to be one question, which the next chapter takes up."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("d")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
        self.clear_scene()

    def weitzman(self):
        d = load("ramsey")
        w = d["weitzman"]
        head = label(r"Uncertain rates decline \ (Weitzman, \ 1998)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        at = {int(k): v for k, v in w["at"].items()}
        assert at == {1: 2.98, 50: 2.132, 100: 1.675, 400: 1.173}
        ax = Axes(x_range=[0, 400, 100], y_range=[0, 3.5, 1], x_length=6.2, y_length=3.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True}).move_to([-3.2, -0.6, 0])
        xl = label(r"horizon, \ years", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.42)
        yl = label(r"certainty-equivalent rate, \ \%", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)
        c = VMobject(color=FUT, stroke_width=3).set_points_smoothly([ax.c2p(t, r) for t, r in zip(w["t"], w["rate"])])
        lo = DashedLine(ax.c2p(0, 1), ax.c2p(400, 1), color=GREY_B, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(t, at[t]), radius=0.06, color=WHITE) for t in (1, 100, 400)])
        tags = VGroup(label(r"2.98\%", font_size=15).next_to(dots[0], RIGHT, buff=0.1),
                      label(r"1.68\% at 100", font_size=15).next_to(dots[1], UP, buff=0.1),
                      label(r"1.17\% at 400", font_size=15).next_to(dots[2], UP, buff=0.1))
        f = MathTex(r"\bar r(t) \;=\; -\frac{1}{t}\ln\!\Big(\tfrac12 e^{-0.01 t} + \tfrac12 e^{-0.05 t}\Big)",
                    font_size=30, color=FUT).move_to([3.6, 1.6, 0])
        side = stack([(r"the rate is 1\% or 5\%, \ equally likely", GREY_A),
                      (r"average the discount factors, \ not the rates: \ the low rate dominates the far future", FUT),
                      (r"Weitzman \ (2001): \ a survey of over 2000 economists, \ turned into a declining schedule",
                       GREY_A),
                      (r"UK Treasury Green Book: \ 3.5\% for 30 years, \ falling to 1\% beyond 300", WELL)],
                     font_size=18, aligned_edge=LEFT, width=5.2, buff=0.25).move_to([3.6, -0.6, 0])
        with self.voiceover(
            "Martin Weitzman added a twist in 1998. <bookmark mark='a'/>Suppose we do not know the right rate: it is "
            "one percent or five percent, equally likely. <bookmark mark='b'/>What we should average is not the "
            "rates but the discount factors, and as the horizon grows the factor at five percent vanishes, leaving "
            "the one percent to dominate. <bookmark mark='c'/>The certainty-equivalent rate starts near three percent "
            "and declines, to one point six eight percent at a hundred years and one point one seven at four hundred, "
            "approaching the lowest possible rate. <bookmark mark='d'/>Weitzman later surveyed more than two thousand "
            "economists and turned their disagreement into a declining schedule. <bookmark mark='e'/>Britain's "
            "Treasury uses one: three and a half percent for the first thirty years, falling to one percent beyond "
            "three hundred. Uncertainty about how much the future counts makes the far future count more."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(f))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(lo))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c), run_time=2)
            self.play(FadeIn(dots), FadeIn(tags))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
