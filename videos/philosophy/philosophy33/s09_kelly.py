from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403

FCOL = {"0.1": CAUSE, "0.2": MONEY, "0.4": RISK, "0.6": BAD}


class Kelly(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The Kelly criterion", r"How much should you bet, again and again?", lit=(1956,),
                            part=PART)
        with self.voiceover("Chapter eight. The Kelly criterion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.derive()
        self.curve()
        self.paths()
        self.mean_median()
        self.practice()

    def derive(self):
        hc = history_card(1956, r"John L. Kelly Jr., \ Bell Labs", r"``A New Interpretation of Information Rate''",
                          width=6.6, color=HIST).to_corner(UL, buff=0.3)
        f1 = MathTex(r"W_n \;=\; W_0 \,(1+f)^{S}\,(1-f)^{n-S}", font_size=34, color=MONEY)
        f2 = MathTex(r"\tfrac{1}{n}\log \tfrac{W_n}{W_0} \;\longrightarrow\; g(f) \;=\; p\log(1+f) + (1-p)\log(1-f)",
                     font_size=32, color=PREF)
        f3 = MathTex(r"g'(f) = \frac{p}{1+f} - \frac{1-p}{1-f} = 0 \;\Longrightarrow\; f^* = 2p - 1", font_size=32,
                     color=GOAL)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.4).move_to([0, -0.4, 0])
        notes = VGroup(label(r"$S$ wins in $n$ even-money bets, \ each staking a fraction $f$", font_size=17,
                             color=GREY_A).next_to(f1, RIGHT, buff=0.3),
                       label(r"law of large numbers: \ $S/n \to p$", font_size=17, color=GREY_A).next_to(
                           f2, DOWN, buff=0.12).align_to(f2, RIGHT),
                       label(r"$p = 0.6$: \ bet 20\% of what you have", font_size=19, color=GOAL).next_to(
                           f3, DOWN, buff=0.25))
        notes[0].next_to(f1, DOWN, buff=0.1)
        VGroup(f2, notes[1], f3, notes[2]).shift(DOWN * 0.3)
        with self.voiceover(
            "In 1956 John Kelly, an engineer at Bell Labs, asked how a gambler with an edge should size his bets. "
            "<bookmark mark='a'/>Bet a fixed fraction f of your wealth, at even money, on a coin that wins with "
            "probability p. After n bets with S wins, your wealth has been multiplied by one plus f, S times, and by "
            "one minus f, the other times. <bookmark mark='b'/>Wealth compounds, so take logarithms. By the law of "
            "large numbers the growth rate per bet tends to g of f: p times the log of one plus f, plus one minus p "
            "times the log of one minus f. <bookmark mark='c'/>Set its derivative to zero, and the best fraction is "
            "two p minus one. With a sixty percent coin, bet twenty percent of what you have, every time. "
            "Maximizing growth is maximizing the expectation of log wealth: Bernoulli's utility from chapter two, "
            "reached by a different road."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(f1), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(f3))
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def curve(self):
        d = load("kelly")
        head = label(r"The growth rate, \ drawn", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["p"] == 0.6 and d["f_star"] == 0.2
        bf = d["by_f"]
        assert [bf[k]["g"] for k in ("0.1", "0.2", "0.4", "0.6")] == [0.01504, 0.02014, -0.00245, -0.08451]
        ax = Axes(x_range=[0, 0.6, 0.1], y_range=[-0.09, 0.03, 0.03], x_length=7.2, y_length=4.4, tips=False,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True,
                               "decimal_number_config": {"num_decimal_places": 2}}).move_to([-2.5, -0.4, 0])
        xl = label(r"fraction bet, \ $f$", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = label(r"growth per bet, \ $g(f)$", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.15)
        g = VMobject(color=PREF, stroke_width=3).set_points_smoothly([ax.c2p(f, y) for f, y in d["g_curve"]])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.6, 0), color=GREY_C)
        dots = VGroup(*[Dot(ax.c2p(float(k), bf[k]["g"]), radius=0.08, color=FCOL[k]) for k in bf])
        top = label(r"$f^* = 0.2$: \ $g = 0.0201$", font_size=18, color=MONEY).next_to(dots[1], UP, buff=0.15)
        side = stack([(r"$f = 0.1$: \ $g = 0.0150$", CAUSE), (r"$f = 0.2$: \ $g = 0.0201$, \ the peak", MONEY),
                      (r"$f = 0.4$: \ $g = -0.0025$", RISK), (r"$f = 0.6$: \ $g = -0.0845$", BAD),
                      (r"half Kelly keeps three quarters of the growth", GOAL)], font_size=18, aligned_edge=LEFT,
                     width=3.6, buff=0.25).move_to([4.9, -0.2, 0])
        with self.voiceover(
            "Here is the growth rate for the sixty percent coin. <bookmark mark='a'/>It rises from zero, peaks at "
            "f equal to point two, where wealth grows by about two percent per bet in the long run, "
            "<bookmark mark='b'/>and falls. At about twice the Kelly fraction the growth rate crosses zero: at point "
            "four it is already negative. At point six it is minus eight percent per bet. "
            "<bookmark mark='c'/>Every one of these bets has positive expected value: the coin favours you. Yet "
            "betting too much of your wealth on it makes you poorer, in the long run, with probability one. "
            "<bookmark mark='d'/>Near the top the curve is flat: betting half the Kelly fraction keeps three quarters "
            "of the growth with far smaller swings, which is why practitioners prefer fractions of Kelly."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(zero))
            vo.wait_until("a")
            self.play(Create(g), run_time=2)
            self.play(FadeIn(dots[0]), FadeIn(dots[1]), FadeIn(top), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots[2]), FadeIn(dots[3]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(dots[2], dots[3]), color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def paths(self):
        d = load("kelly")
        head = label(r"A thousand fortunes, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        bf = d["by_f"]
        assert d["bets"] == 1000 and d["paths"] == 1000
        assert [bf[k]["median_log10"] for k in ("0.1", "0.2", "0.4", "0.6")] == [6.445, 8.569, -1.431, -37.306]
        assert [bf[k]["ruined"] for k in ("0.1", "0.2", "0.4", "0.6")] == [0, 0, 457, 1000]
        lo, hi = -12, 12
        ax = Axes(x_range=[0, 1000, 200], y_range=[lo, hi, 4], x_length=7.6, y_length=4.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-2.0, -0.5, 0])
        xl = label(r"bets", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"$\log_{10}$ wealth", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.12)
        start = DashedLine(ax.c2p(0, 0), ax.c2p(1000, 0), color=GREY_C)

        def path(seq, col):
            pts = [ax.c2p(0, 0)]
            for j, y in enumerate(seq):
                if y < lo:
                    break
                pts.append(ax.c2p(1 + 20 * j, min(y, hi)))
            return VMobject(color=col, stroke_width=2.2, stroke_opacity=0.9).set_points_as_corners(pts)
        groups = {k: VGroup(*[path(s, FCOL[k]) for s in bf[k]["sample"]]) for k in ("0.1", "0.2", "0.4", "0.6")}
        side = stack([(r"$f = 0.1$: \ median $10^{6.4}$ times the stake; \ none ruined", CAUSE),
                      (r"$f = 0.2$: \ median $10^{8.6}$; \ none ruined", MONEY),
                      (r"$f = 0.4$: \ median $10^{-1.4}$; \ 457 of 1000 ruined", RISK),
                      (r"$f = 0.6$: \ median $10^{-37}$; \ all 1000 ruined", BAD)], font_size=18, aligned_edge=LEFT,
                     width=4.2, buff=0.3).move_to([4.4, -0.3, 0])
        note = label(r"five paths of each; \ ruined: \ below 1\% of the stake after 1000 bets", font_size=16,
                     color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The Reasoner gives a thousand gamblers the sixty percent coin and a thousand bets each, at four "
            "fractions. Five paths of each are drawn, on a log scale. <bookmark mark='a'/>Betting a tenth, the median "
            "fortune grows about three million fold, and no one is ruined. <bookmark mark='b'/>Betting the Kelly "
            "fifth, the median grows by a factor of about four hundred million. <bookmark mark='c'/>Betting four "
            "tenths, the paths swing wildly and the median ends below where it began; four hundred and fifty seven "
            "of the thousand gamblers are left with less than one percent of their stake. "
            "<bookmark mark='d'/>Betting six tenths, every one of the thousand is ruined: the median is ten to the "
            "minus thirty seven."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(start), FadeIn(note))
            for mk, k, row in zip("abcd", ("0.1", "0.2", "0.4", "0.6"), side):
                vo.wait_until(mk)
                self.play(LaggedStart(*[Create(p) for p in groups[k]], lag_ratio=0.15), FadeIn(row), run_time=2)
        self.clear_scene()

    def mean_median(self):
        d = load("kelly")
        head = label(r"Expectation against the typical life", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        bf = d["by_f"]
        assert [bf[k]["mean_log10_of_mean"] for k in ("0.1", "0.2", "0.4", "0.6")] == [8.6, 17.03, 33.42, 49.22]
        hd = [r"f", r"\log_{10}\,\mathbb{E}[W_{1000}]", r"\log_{10}\,\text{median}\,W_{1000}", r"\text{ruined}"]
        cells = []
        for k in ("0.1", "0.2", "0.4", "0.6"):
            cells.append([label(k, font_size=20, color=FCOL[k]),
                          label(f"{bf[k]['mean_log10_of_mean']:.1f}", font_size=20, color=MONEY),
                          label(f"{bf[k]['median_log10']:.1f}", font_size=20, color=OK if bf[k]['median_log10'] > 0
                                else BAD),
                          label(f"{bf[k]['ruined']}", font_size=20, color=GREY_A)])
        grid = ValueGrid(hd, cells, col_w=[1.2, 3.4, 3.8, 1.8], cell_h=0.6, font_size=19).move_to([0, 0.7, 0])
        f = MathTex(r"\mathbb{E}[W_n] = W_0\,\big(1 + f(2p-1)\big)^n", font_size=30, color=MONEY).next_to(
            grid, DOWN, buff=0.4)
        foot = stack([(r"expected wealth rises with $f$ all the way: \ $10^{49}$ at $f = 0.6$", MONEY),
                      (r"maximize $\mathbb{E}[W]$ and you are ruined almost surely: \ the St Petersburg lesson "
                       r"again", GOAL)], font_size=19, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why not just maximize expected wealth? <bookmark mark='a'/>Each bet multiplies expected wealth by one "
            "plus f times the edge, so expected wealth after a thousand bets rises with f all the way: ten to the "
            "forty nine times the stake at six tenths. <bookmark mark='b'/>Yet the median, the fortune of the "
            "typical gambler, is ten to the minus thirty seven, and all thousand simulated gamblers are ruined. "
            "<bookmark mark='c'/>The expectation is carried by extremely rare histories with many more wins than a "
            "typical gambler sees. <bookmark mark='d'/>An agent who maximizes expected money in "
            "repeated bets is ruined almost surely. Paul Samuelson objected that Kelly is only right for log "
            "utility, and he was correct as a matter of theory. In practice, what one cares about over a lifetime of "
            "bets is the typical outcome, and that is what Kelly maximizes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(Write(f))
            for k in range(4):
                self.play(FadeIn(grid.cell[k][0]), FadeIn(grid.cell[k][1]), run_time=0.4)
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            for k in range(4):
                self.play(FadeIn(grid.cell[k][2]), FadeIn(grid.cell[k][3]), run_time=0.4)
            vo.wait_until("c")
            self.play(Indicate(grid.cell[3][1], color=MONEY))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def practice(self):
        head = label(r"Kelly in industry", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Thorp", r"blackjack card counting \ (1962), \ then a hedge fund that sized positions by Kelly",
                 HIST),
                (r"portfolios", r"for many assets: \ maximize $\mathbb{E}[\log(1 + w^\top r)]$, \ the growth-optimal "
                                r"portfolio", MONEY),
                (r"fractional Kelly", r"estimates of $p$ are noisy; \ over-betting is punished far more than "
                                      r"under-betting, \ so bet a half or a quarter", RISK),
                (r"information", r"Kelly's own result: \ the best growth rate equals the information the tip carries, "
                                 r"\ in Shannon's sense", PREF)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6)
        with self.voiceover(
            "Kelly's rule left the casino quickly. <bookmark mark='a'/>Edward Thorp used it to size bets when he "
            "showed that blackjack could be beaten by counting cards, in 1962, and later to size the positions of a "
            "hedge fund. <bookmark mark='b'/>For many assets, the rule picks the portfolio that maximizes expected "
            "log return, the growth optimal portfolio. <bookmark mark='c'/>Because the probabilities are only "
            "estimated, and because the curve punishes over-betting far more than under-betting, practitioners bet "
            "a half or a quarter of the Kelly amount. <bookmark mark='d'/>And the title of Kelly's paper explains its "
            "origin: the best achievable growth rate equals the information that a gambler's private tip carries, "
            "in Claude Shannon's sense. Decision theory and information theory meet here."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
