from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Cooperation(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Evolution and cooperation", r"Can nice strategies win?", lit=(1980, 2006),
                            part=PART)
        with self.voiceover("Chapter eleven. Evolution and cooperation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dilemma()
        self.tournament()
        self.shadow()
        self.rules()

    def dilemma(self):
        head = label(r"The prisoner's dilemma", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        hd = [r"", r"\text{they cooperate}", r"\text{they defect}"]
        rows = [[MathTex(r"\text{you cooperate}", font_size=24, color=ALT), MathTex(r"3, \ 3", font_size=26),
                 MathTex(r"0, \ 5", font_size=26)],
                [MathTex(r"\text{you defect}", font_size=24, color=SELF), MathTex(r"5, \ 0", font_size=26),
                 MathTex(r"1, \ 1", font_size=26)]]
        grid = ValueGrid(hd, rows, col_w=[3.0, 2.6, 2.4], cell_h=0.7, font_size=22).move_to([0, 1.0, 0])
        side = stack([(r"whatever they do, \ you do better by defecting", BAD),
                      (r"so both defect, \ and both get 1 instead of 3", BAD),
                      (r"played once, \ defection is the only equilibrium", GREY_A),
                      (r"played again and again, \ the future casts a shadow", OK)], font_size=21, aligned_edge=LEFT,
                     width=9.0).move_to([0, -1.7, 0])
        with self.voiceover(
            "Cooperation between unrelated individuals is the next puzzle. <bookmark mark='a'/>In the prisoner's "
            "dilemma, each player does better by defecting whatever the other does: five instead of three if the "
            "other cooperates, one instead of nothing if the other defects. <bookmark mark='b'/>So both defect, and "
            "both get one, when they could have had three. <bookmark mark='c'/>Played once, mutual defection is the "
            "only equilibrium. <bookmark mark='d'/>But animals, like people, meet again, and the shadow of the future "
            "changes the game."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])),
                      FadeIn(VGroup(*grid.cell[1])))
            for mk, r in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tournament(self):
        d = load("axelrod")
        hc = history_card(1980, r"Robert Axelrod", r"computer tournaments; \ \textit{The Evolution of Cooperation}",
                          width=7.0, color=HIST).to_corner(UL, buff=0.3)
        sc = d["scores"]
        names = list(sc)
        top = max(sc.values())
        bars = VGroup()
        for i, n in enumerate(names):
            v = sc[n]
            nice = n not in ("always defect", "random")
            col = ALT if nice else SELF
            b = Rectangle(width=v / top * 5.6, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.75)
            b.move_to([-1.6 + b.width / 2, 1.2 - i * 0.62, 0])
            nm = label(n, font_size=18, color=col).next_to(b, LEFT, buff=0.2)
            val = label(f"{v:.2f}", font_size=18, color=WHITE).next_to(b, RIGHT, buff=0.12)
            bars.add(VGroup(b, nm, val))
        cap = label(r"the Reasoner's round robin: \ six strategies, \ " + f"{d['rounds']}" + r" rounds each, \ mean "
                    r"payoff per round", font_size=18, color=GREY_A).next_to(bars, UP, buff=0.3)
        rows = stack([(r"Axelrod's winners were \textit{nice} \ (never defect first), \ \textit{retaliatory} \ and "
                       r"\textit{forgiving}: \ tit for tat won both tournaments", OK),
                      (r"here grim trigger edges tit for tat: \ the ranking depends on who else is playing", GOAL),
                      (r"always defect finishes last, \ though it never loses a single game", BAD)], font_size=19,
                     width=12.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1980 Robert Axelrod invited game theorists to submit strategies for a repeated prisoner's dilemma, "
            "and played them against one another. <bookmark mark='a'/>The Reasoner runs a small version: six "
            "strategies, every pair playing two hundred rounds. <bookmark mark='b'/>In Axelrod's tournaments the "
            "winner, both times, was the simplest entry, Anatol Rapoport's tit for tat: cooperate first, then copy "
            "the opponent's last move. Successful strategies were nice, never defecting first; retaliatory; and "
            "forgiving. <bookmark mark='c'/>In this small field, grim trigger, which never forgives a defection, "
            "edges tit for tat: rankings depend on the population of opponents. <bookmark mark='d'/>And always "
            "defect comes last, although it never loses an individual game, because it denies itself the rewards "
            "of mutual cooperation."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.2))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rules(self):
        head = label(r"Five routes to cooperation \ (Nowak, \ 2006)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"kin selection", r"help relatives: \ $r b > c$ \ (Chapter 5)", GENE),
            (r"direct reciprocity", r"help those who will meet you again: \ $w > c/b$", ALT),
            (r"indirect reciprocity", r"help those with a good reputation: \ $q > c/b$", ORG),
            (r"network reciprocity", r"cooperators in clusters help one another: \ $b/c > k$", GROUP),
            (r"group selection", r"cooperative groups out-produce others \ (Chapter 6)", OK),
            (r"onward", r"social contracts \ (Part 34); \ evolutionary debunking of morality \ (Part 37)", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.0, x_text=-2.2)
        with self.voiceover(
            "Martin Nowak catalogued five mechanisms by which cooperation can evolve, each with its own threshold. "
            "<bookmark mark='a'/>Kin selection: Hamilton's rule. <bookmark mark='b'/>Direct reciprocity: cooperate "
            "if the probability of meeting again exceeds the cost-to-benefit ratio. <bookmark mark='c'/>Indirect "
            "reciprocity: help those with a good reputation, if reputations are known reliably enough. "
            "<bookmark mark='d'/>Network reciprocity: cooperators in clusters, when the benefit-to-cost ratio exceeds "
            "the number of neighbours. <bookmark mark='e'/>And group selection, as in chapter six. "
            "<bookmark mark='f'/>These results lead outward: to the social contract in Part 34, and to the worry, in "
            "Part 37, that if evolution shaped our moral sense, it may have shaped it for fitness rather than truth."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def shadow(self):
        d = load("shadow")
        head = label(r"The shadow of the future", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        (a, b), (c, dd) = d["payoffs"]
        hd = [r"", r"\text{vs TFT}", r"\text{vs ALLD}"]
        rows = [[MathTex(r"\text{TFT}", font_size=24, color=ALT), MathTex(r"\tfrac{R}{1 - w} = " + f"{a:.0f}",
                                                                          font_size=24),
                 MathTex(r"S + \tfrac{wP}{1 - w} = " + f"{b:.0f}", font_size=24)],
                [MathTex(r"\text{ALLD}", font_size=24, color=SELF),
                 MathTex(r"T + \tfrac{wP}{1 - w} = " + f"{c:.0f}", font_size=24),
                 MathTex(r"\tfrac{P}{1 - w} = " + f"{dd:.0f}", font_size=24)]]
        grid = ValueGrid(hd, rows, col_w=[1.6, 2.8, 3.0], cell_h=0.7, font_size=20).move_to([-3.0, 1.3, 0])
        wl = label(r"the game goes on with probability $w = " + f"{d['w']:g}" + r"$ \ (T, R, P, S = 5, 3, 1, 0)",
                   font_size=16, color=GREY_A).next_to(grid, UP, buff=0.12)
        cond = MathTex(r"\text{TFT resists ALLD} \iff w > \frac{T - R}{T - P} = " + f"{d['threshold']:g}",
                       font_size=30, color=OK).next_to(grid, DOWN, buff=0.35)
        ax = Axes(x_range=[0, 400, 100], y_range=[0, 1, 0.5], x_length=5.0, y_length=2.6,
                  axis_config={"color": GREY_B, "font_size": 14, "include_ticks": False},
                  y_axis_config={"include_numbers": True}).move_to([3.6, 1.0, 0])
        al = label(r"share of TFT, \ replicator dynamics", font_size=15, color=GREY_A).next_to(ax, UP, buff=0.08)
        xs = d["xstar"]
        thr = DashedLine(ax.c2p(0, xs), ax.c2p(400, xs), color=GOAL, stroke_width=2)
        tl = label(r"$x^* = " + f"{xs:.2f}" + r"$", font_size=15, color=GOAL).next_to(thr, RIGHT, buff=0.08)
        cols = [SELF, SELF, ALT, ALT]
        trajs = VGroup(*[series_plot(ax, t, col, width=3) for t, col in zip(d["trajs"], cols)])
        rows2 = stack([(r"above $x^* = " + f"{xs:.2f}" + r"$ \ tit for tat takes over; \ below it, \ defection does",
                        GOAL),
                       (r"Trivers \ (1971): \ reciprocal altruism; \ Axelrod and Hamilton \ (1981): \ but ALLD is "
                        r"stable too, \ so cooperators need a foothold", WHITE),
                       (r"clusters of kin, \ or of neighbours, \ supply it: \ vampire bats share blood with those who "
                        r"shared before \ (Wilkinson, \ 1984)", ALT)], font_size=18, aligned_edge=LEFT,
                      width=12.4).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Why does tit for tat do so well? Because the game goes on. <bookmark mark='a'/>Suppose that after each "
            "round, the players meet again with probability w, here three in four. Add up the expected payoffs of "
            "the whole relationship. Two tit-for-tat players cooperate for as long as they meet and earn twelve; "
            "tit for tat loses the first round to a defector, and then they both defect. <bookmark mark='b'/>Tit for tat resists "
            "invasion by defectors exactly when the shadow of the future is long enough: when w exceeds the "
            "temptation gain over the punishment gap, here one half. <bookmark mark='c'/>The Reasoner runs the "
            "replicator dynamics. There is a tipping point at one fifth. Start below it, and defectors "
            "take over; <bookmark mark='d'/>start above it, and tit for tat sweeps the population. The longer the "
            "shadow of the future, the lower the tipping point: at nine in ten it falls to one seventeenth. "
            "<bookmark mark='e'/>Robert Trivers had proposed reciprocal altruism in 1971; Axelrod and William "
            "Hamilton noted that always defecting is also stable, so cooperators need a foothold. "
            "<bookmark mark='f'/>Clusters of kin or neighbours can supply one. Vampire bats, which share blood "
            "meals with roost-mates who shared before, are the classic case."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(wl), FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])),
                      FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("b")
            self.play(Write(cond))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(al), Create(thr), FadeIn(tl), Create(trajs[0]), Create(trajs[1]),
                      run_time=2)
            vo.wait_until("d")
            self.play(Create(trajs[2]), Create(trajs[3]), FadeIn(rows2[0]), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(rows2[1]))
            vo.wait_until("f")
            self.play(FadeIn(rows2[2]))
        self.clear_scene()
