from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Evolution(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Evolution of cooperation", r"Does cooperation last?", lit=(2005,), part=PART)
        with self.voiceover("Chapter eight. Evolution of cooperation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.model()
        self.path()
        self.stationary()

    def model(self):
        head = label(r"A finite population, \ rare mutations \ (Imhof, \ Fudenberg and Nowak, \ 2005)",
                     font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = [(r"population", r"50 players, \ each playing one memory-one strategy against all the others, \ "
                                r"with 1\% errors", GREY_A),
                (r"selection", r"the Moran process: \ a player reproduces with probability rising with its payoff, \ "
                               r"and replaces a random other", COOP),
                (r"mutation", r"rare: \ a new strategy appears, \ and either takes over or dies out before the next "
                              r"one", INST),
                (r"computed", r"the probability that each strategy, \ arriving alone, \ takes over each other: \ a "
                              r"Markov chain on six strategies", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6)
        f = MathTex(r"\rho_{A \to B} = \Big(1 + \sum_{k=1}^{N-1} \prod_{m=1}^{k} e^{-w\,(f_B(m) - f_A(m))}\Big)^{-1}",
                    font_size=28, color=COOP).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Part 19 showed cooperation spreading by kin and reciprocity. Here the Reasoner asks whether it lasts. "
            "<bookmark mark='a'/>A population of fifty players, each with a memory-one strategy, plays everyone "
            "else, with one percent errors. <bookmark mark='b'/>In each step a player reproduces with probability "
            "rising with its payoff, and its offspring replaces someone at random: the Moran process. "
            "<bookmark mark='c'/>Mutations are rare, so a newcomer either takes over or dies out before the next one "
            "arrives. <bookmark mark='d'/>Then all that matters is the probability that one strategy, arriving "
            "alone, takes over another, and there is a formula for it. The population becomes a Markov chain on "
            "six strategies: always defect, always cooperate, tit for tat, win-stay lose-shift, generous tit for "
            "tat, and the extortioner."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(Write(f))
        self.clear_scene()

    def path(self):
        d = load("evolution")
        head = label(r"Cooperation rises, \ and collapses", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        names = d["names"]
        assert d["N"] == 50 and d["steps"] == 3000 and len(names) == 6
        runs = d["runs"]
        W, H = 12.0, 0.9
        x = -6.0
        band = VGroup()
        for s, n in runs:
            w = W * n / d["steps"]
            band.add(Rectangle(width=w, height=H, stroke_width=0, fill_color=STRAT_COL[names[s]],
                               fill_opacity=0.9).move_to([x + w / 2, 0.8, 0]))
            x += w
        coop = [d["coop_self"][s] for s, _ in runs]
        ax = Axes(x_range=[0, d["steps"], 1000], y_range=[0, 1, 0.5], x_length=W, y_length=2.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True}).move_to([0, -1.8, 0])
        pts, t = [], 0
        for (s, n), c in zip(runs, coop):
            pts += [ax.c2p(t, c), ax.c2p(t + n, c)]
            t += n
        line = VMobject(color=COOP, stroke_width=2.5).set_points_as_corners(pts)
        yl = label(r"cooperation rate", font_size=15, color=COOP).next_to(ax.y_axis, UP, buff=0.1)
        xl = label(r"mutation events", font_size=15, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.35)
        legend = VGroup(*[VGroup(Square(0.16, stroke_width=0, fill_color=STRAT_COL[n], fill_opacity=0.9),
                                 label(n, font_size=14, color=STRAT_COL[n])).arrange(RIGHT, buff=0.08)
                          for n in names]).arrange(RIGHT, buff=0.3).next_to(band, UP, buff=0.3)
        with self.voiceover(
            "Here is one history of three thousand mutations. <bookmark mark='a'/>The band shows which strategy "
            "rules the population, and the line below shows how much it cooperates. <bookmark mark='b'/>Always "
            "defect rules at first, until tit for tat drifts in and takes over. Tit for tat cannot hold its ground "
            "with errors, so generous tit for tat replaces it, and cooperation is high. <bookmark mark='c'/>But "
            "cooperative regimes do not last. Generous tit for tat gives way to win-stay lose-shift, which falls to "
            "defectors; now and then unconditional cooperators drift in and are exploited; and the cycle begins "
            "again. "
            "<bookmark mark='d'/>Cooperation is not an end state but a phase, which repeatedly rises and collapses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in band], lag_ratio=0.01), run_time=2.5)
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), Create(line), run_time=2)
            vo.wait_until("b")
            self.play(Indicate(VGroup(*band[:4]), color=WHITE))
            vo.wait_until("c")
            self.wait(0.5)
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def stationary(self):
        d = load("evolution")
        head = label(r"Where the population spends its time", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        names, st = d["names"], d["stationary"]
        assert st == [0.3079, 0.013, 0.0318, 0.2176, 0.4179, 0.0118] and d["avg_cooperation"] == 0.6494
        fx = d["fixation_from_alld"]
        assert fx["tit for tat"] == 0.104481
        bars = VGroup()
        for k, (n, s) in enumerate(zip(names, st)):
            b = Rectangle(width=0.9, height=4.0 * s / 0.45, stroke_width=0, fill_color=STRAT_COL[n], fill_opacity=0.85)
            b.move_to([-5.4 + 1.25 * k, -2.2 + b.height / 2, 0])
            bars.add(VGroup(b, label(f"{100 * s:.1f}\\%", font_size=16, color=STRAT_COL[n]).next_to(b, UP, buff=0.08),
                            wrapped_label(n, 1.2, 13, STRAT_COL[n]).next_to([-5.4 + 1.25 * k, -2.2, 0], DOWN,
                                                                           buff=0.12)))
        side = stack([(r"generous tit for tat 41.8\%, \ win-stay lose-shift 21.8\%", COOP),
                      (r"always defect 30.8\%; \ the extortioner 1.2\%", DEFECT),
                      (r"average cooperation: \ 65\%", GOAL),
                      (r"from always defect, \ only tit for tat invades easily \ (fixation 0.104 against "
                       r"$1/N = 0.02$): \ the stepping stone", INST)], font_size=18, aligned_edge=LEFT, width=4.6,
                     buff=0.3).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "In the long run, the chain's stationary distribution says where the population spends its time. "
            "<bookmark mark='a'/>Generous tit for tat, forty two percent, and win-stay lose-shift, twenty two. "
            "<bookmark mark='b'/>Always defect, thirty one percent. The extortioner barely appears. "
            "<bookmark mark='c'/>On average the population cooperates sixty five percent of the time. "
            "<bookmark mark='d'/>And the route out of defection runs through tit for tat: arriving alone in a "
            "population of defectors, it takes over with probability point one, five times the neutral chance; the "
            "forgiving strategies cannot invade defectors directly, but can replace tit for tat. Retaliation opens "
            "the door; forgiveness walks through it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.15), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
