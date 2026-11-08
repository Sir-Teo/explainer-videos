from __future__ import annotations

from videos.philosophy.philosophy34.common import *  # noqa: F403


class Axelrod(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Tournaments", r"Which strategy wins when the game is repeated?", lit=(1980, 1984),
                            part=PART)
        with self.voiceover("Chapter six. Tournaments."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.shadow()
        self.folk()
        self.zoo()
        self.noiseless()
        self.noisy()
        self.river()

    def shadow(self):
        d = load("shadow")
        head = label(r"The shadow of the future", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ds = d["deltas"]
        assert (d["grim"]["threshold_grid"], d["tft"]["threshold_grid"]) == (0.5, 0.67)
        assert abs(d["tft"]["threshold"] - 2 / 3) < 1e-12 and d["grim"]["threshold"] == 0.5
        mid = [i for i, x in enumerate(ds) if 0.25 < x < 0.67]
        assert all(abs(d["tft"]["best"][i] - 5 / (1 + ds[i])) < 1e-5 for i in mid)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[1, 5, 1], x_length=6.0, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True},
                  x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                  y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-3.3, -0.6, 0])
        xl = label(r"$\delta$: \ the chance the game goes on, \ or the discount factor", font_size=16,
                   color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.42)
        yl = label(r"average payoff per round", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(
            ax, LEFT)

        def curve(key, col, w=3):
            return VMobject(color=col, stroke_width=w).set_points_as_corners(
                [ax.c2p(x, y) for x, y in zip(ds, d["curves"][key])])

        coop, alld, alt = curve("cooperate", COOP), curve("always_defect", DEFECT), curve("alternate", MONEY)
        lc = label(r"cooperate: \ $R = 3$", font_size=16, color=COOP).next_to(ax.c2p(0.95, 3), UP, buff=0.1).shift(
            LEFT * 0.5)
        ld = label(r"defect for ever: \ $(1-\delta)T + \delta P$", font_size=16, color=DEFECT).next_to(
            ax.c2p(0.47, 2.0), LEFT, buff=0.05)
        la = label(r"alternate D, C: \ $\frac{T + \delta S}{1 + \delta}$", font_size=16, color=MONEY).next_to(
            ax.c2p(0.7, 3.9), RIGHT, buff=0.05)
        env = VGroup(*[Dot(ax.c2p(x, y), radius=0.03, color=WHITE) for k, (x, y) in
                       enumerate(zip(ds, d["tft"]["best"])) if k % 3 == 0])
        v1 = DashedLine(ax.c2p(0.5, 1), ax.c2p(0.5, 5), color=DEFECT, stroke_width=1.6)
        v2 = DashedLine(ax.c2p(2 / 3, 1), ax.c2p(2 / 3, 5), color=MONEY, stroke_width=1.6)
        t1 = MathTex(r"\tfrac12", font_size=30, color=DEFECT).next_to(v1, UP, buff=0.08)
        t2 = MathTex(r"\tfrac23", font_size=30, color=MONEY).next_to(v2, UP, buff=0.08)
        side = stack([(r"after each round the game goes on with probability $\delta$", GREY_A),
                      (r"against grim: \ cooperate iff $\delta \ge \frac{T - R}{T - P} = \frac12$", DEFECT),
                      (r"against tit for tat the best deviation alternates: \ $\delta \ge \frac{T - R}{R - S} = "
                       r"\frac23$", MONEY),
                      (r"all 32 deterministic memory-one strategies, \ played at every $\delta$: \ the same two "
                       r"thresholds", WHITE),
                      (r"the shadow of the future \ (Axelrod): \ your own future is the hostage", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=5.0, buff=0.3).move_to([3.9, -0.3, 0])
        with self.voiceover(
            "Before the tournaments, the theory. A single prisoner's dilemma has one equilibrium, mutual defection. "
            "But suppose that after each round the game goes on with probability delta, or, equivalently, that the "
            "players discount the future by delta. <bookmark mark='a'/>Cooperating for ever with a partner who does "
            "the same earns R every round: three. <bookmark mark='b'/>Against grim trigger, the best deviation "
            "defects at once: the temptation, five, now, and the punishment, one, for ever after. Averaged with "
            "weights one minus delta, that is five minus four delta, which falls below three exactly when delta "
            "passes one half; in general, when delta is at least T minus R over T minus P. "
            "<bookmark mark='c'/>Tit for tat forgives, and forgiveness changes the best deviation. Defect, accept "
            "the sucker's payoff when it retaliates, and defect again as it forgives: alternating earns five over "
            "one plus delta, which beats cooperation until delta reaches two thirds, T minus R over R minus S. "
            "<bookmark mark='d'/>The Reasoner does not trust the algebra. It plays all thirty-two deterministic "
            "memory-one strategies against grim and against tit for tat at every delta, and finds the same two "
            "thresholds, a half and two thirds, with alternation the best reply from a quarter up to two thirds. "
            "<bookmark mark='e'/>Axelrod called this the shadow of the future. When it is long enough, cooperation "
            "needs no sovereign: each player's own future is the hostage."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(coop), FadeIn(lc))
            vo.wait_until("b")
            self.play(Create(alld), FadeIn(ld), FadeIn(side[1]))
            self.play(Create(v1), FadeIn(t1))
            vo.wait_until("c")
            self.play(Create(alt), FadeIn(la), FadeIn(side[2]))
            self.play(Create(v2), FadeIn(t2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in env], lag_ratio=0.03), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def folk(self):
        d = load("folk")
        head = label(r"The folk theorem", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pts = {tuple(p["u"]): p["delta"] for p in d["points"]}
        assert d["n_points"] == 156 and d["max_len"] == 7
        assert pts[(3.0, 3.0)] == 0.5 and pts[(2.5, 2.5)] == 0.25
        assert min(pts.values()) == 0.25 and 0.95 < max(pts.values()) < 0.96
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1], x_length=4.6, y_length=4.6, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True}).move_to([-3.6, -0.55, 0])
        xl = label(r"row's average payoff", font_size=15, color=ROW).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"column's", font_size=15, color=COL).next_to(ax.y_axis, UP, buff=0.12)
        feas = Polygon(*[ax.c2p(*q) for q in d["feasible_polygon"]], color=GREY_B, stroke_width=2,
                       fill_color=GREY_B, fill_opacity=0.08)
        corners = VGroup(*[label(t, font_size=15, color=c).next_to(ax.c2p(*q), dr, buff=0.08) for t, c, q, dr in [
            (r"CC \ (3, 3)", COOP, (3, 3), UR), (r"DD \ (1, 1)", DEFECT, (1, 1), DL),
            (r"CD \ (0, 5)", COL, (0, 5), RIGHT), (r"DC \ (5, 0)", ROW, (5, 0), UR)]])
        mm = VGroup(DashedLine(ax.c2p(1, 1), ax.c2p(1, 13 / 3), color=GREY_A, stroke_width=1.6),
                    DashedLine(ax.c2p(1, 1), ax.c2p(13 / 3, 1), color=GREY_A, stroke_width=1.6))
        ir = Polygon(*[ax.c2p(*q) for q in d["ir_polygon"]], stroke_width=0, fill_color=GOAL, fill_opacity=0.10)

        def col(x):
            t = (x - 0.25) / 0.7
            return interpolate_color(ManimColor(COOP), ManimColor(MONEY), min(1, 2 * t)) if t < 0.5 else \
                interpolate_color(ManimColor(MONEY), ManimColor(BAD), min(1, 2 * t - 1))

        dots = VGroup(*[Dot(ax.c2p(*u), radius=0.045, color=col(v)) for u, v in sorted(pts.items())])
        bar = VGroup(*[Rectangle(width=0.25, height=0.06, stroke_width=0, fill_color=col(0.25 + 0.7 * k / 40),
                                 fill_opacity=1).move_to([-0.8, -2.4 + 0.06 * k, 0]) for k in range(41)])
        bar_t = VGroup(label(r"$\delta$ needed", font_size=15, color=GREY_A).next_to(bar, UP, buff=0.12),
                       label(r"0.25", font_size=14, color=COOP).next_to(bar[0], RIGHT, buff=0.1),
                       label(r"0.95", font_size=14, color=BAD).next_to(bar[-1], RIGHT, buff=0.1))
        ring_cc = Circle(radius=0.16, color=WHITE, stroke_width=2).move_to(ax.c2p(3, 3))
        ring_t = Circle(radius=0.16, color=WHITE, stroke_width=2).move_to(ax.c2p(2.5, 2.5))
        side = stack([(r"feasible: \ every average that mixing the four outcomes over time can give", GREY_A),
                      (r"minmax: \ each player can guarantee herself 1 by always defecting", GREY_A),
                      (r"Friedman \ (1971); \ Fudenberg and Maskin \ (1986): \ every feasible point above the "
                       r"minmax is an equilibrium, \ for patient enough players", GOAL),
                      (r"156 cyclic plans of up to 7 rounds, \ deviations punished by grim trigger: \ the least "
                       r"$\delta$ for each", WHITE),
                      (r"mutual cooperation: \ $\delta \ge 0.5$; \ near the minmax lines: \ up to 0.95", COOP),
                      (r"taking turns, \ CD then DC: \ $\delta \ge 0.25$, \ and worse for both: \ 2.5 against 3",
                       MONEY),
                      (r"the selection problem: \ repetition can sustain almost anything", BAD)],
                     font_size=17, aligned_edge=LEFT, width=5.2, buff=0.24).move_to([3.75, -0.35, 0])
        with self.voiceover(
            "How much can the shadow of the future hold up? <bookmark mark='a'/>Plot every pair of average payoffs "
            "the two players could get by mixing the four outcomes over time: a kite, with corners at mutual "
            "cooperation, three and three, mutual defection, one and one, and the two exploitations. "
            "<bookmark mark='b'/>Neither player can be held below one, which she can guarantee herself by always "
            "defecting: her minmax. <bookmark mark='c'/>The folk theorem, so called because game theorists knew it "
            "before anyone published it, says that every feasible pair giving each player more than her minmax is "
            "an equilibrium of the repeated game, if the players are patient enough. James Friedman proved in 1971 "
            "that payoffs better for everyone than a Nash equilibrium can be held up by the threat of returning to "
            "it; Drew Fudenberg and Eric Maskin extended it in 1986 to everything above the minmax. "
            "<bookmark mark='d'/>The Reasoner builds the equilibria. A plan is a cycle of outcomes, up to seven "
            "rounds long, repeated for ever, with any deviation punished by mutual defection for ever after. For "
            "each of the hundred and fifty-six payoff points such plans reach, it finds the least patience that "
            "makes the plan self-enforcing. <bookmark mark='e'/>Mutual cooperation needs a half. Points crowding "
            "the minmax lines need the most, up to point nine five. <bookmark mark='f'/>And a surprise: taking "
            "turns, I am exploited this round and you the next, needs only a quarter. It is worse for both than "
            "cooperating, two and a half against three, yet easier to keep, because the only temptation is to "
            "refuse your turn to lose, which gains one point now and forfeits every turn to win. "
            "<bookmark mark='g'/>So the folk theorem is a triumph and an embarrassment. Repetition can sustain "
            "cooperation; it can also sustain almost anything, including grossly unequal conventions. Which "
            "equilibrium a society lands in is the selection problem, and the rest of this part is about the "
            "forces that select: tournaments, evolution and bargaining."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(DrawBorderThenFill(feas), FadeIn(corners), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mm), FadeIn(ir), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x, scale=0.4) for x in dots], lag_ratio=0.015, run_time=3),
                      FadeIn(side[3]), FadeIn(bar), FadeIn(bar_t))
            vo.wait_until("e")
            self.play(Create(ring_cc), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(Create(ring_t), FadeIn(side[5]))
            vo.wait_until("g")
            self.play(FadeIn(side[6]))
        self.clear_scene()

    def zoo(self):
        head = label(r"Axelrod's tournaments \ (1980), \ rerun", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = [(r"tit for tat", r"cooperate first, \ then copy the other's last move \ (Rapoport)",
                 STRAT_COL["tit for tat"]),
                (r"generous tit for tat", r"like tit for tat, \ but forgive a defection a third of the time",
                 STRAT_COL["generous tit for tat"]),
                (r"win-stay lose-shift", r"repeat your move after a good outcome, \ switch after a bad one \ (Pavlov)",
                 STRAT_COL["win-stay lose-shift"]),
                (r"grim; \ tit for two tats", r"defect for ever after one defection; \ retaliate only after two",
                 STRAT_COL["grim"]),
                (r"Joss; \ random", r"tit for tat with a 10\% sneaky defection; \ a coin flip", STRAT_COL["Joss"]),
                (r"always cooperate; \ always defect", r"the two unconditional strategies",
                 STRAT_COL["always defect"])]
        g = rows_table(rows, top=1.7, gap=0.36, width=8.0, x_text=-1.8, label_size=20, text_size=19)
        foot = label(r"200 rounds per match, \ every pair and every strategy against its twin, \ 20 repetitions",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1980 Robert Axelrod invited game theorists to submit programs to play the repeated prisoner's "
            "dilemma against each other. The winner, submitted by Anatol Rapoport, was the shortest. "
            "<bookmark mark='a'/>Tit for tat: cooperate first, then copy the other's last move. The Reasoner "
            "assembles a zoo of nine strategies. <bookmark mark='b'/>Generous tit for tat forgives a defection a "
            "third of the time. <bookmark mark='c'/>Win-stay lose-shift, also called Pavlov, repeats its move after a "
            "good outcome and switches after a bad one. <bookmark mark='d'/>Grim never forgives; tit for two tats "
            "retaliates only after two defections. <bookmark mark='e'/>Joss, from the first tournament, plays tit for "
            "tat but sneaks in a defection a tenth of the time. <bookmark mark='f'/>And the unconditional "
            "strategies. Every pair plays two hundred rounds, twenty times over."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(FadeIn(foot))
        self.clear_scene()

    def ranking(self, rows, x, title, col):
        t = label(title, font_size=21, color=col)
        names = [label(f"{k + 1}. {n}", font_size=16, color=STRAT_COL[n]) for k, (n, _) in enumerate(rows)]
        maxw = max(m.width for m in names)
        items = VGroup()
        for k, ((n, s), nm) in enumerate(zip(rows, names)):
            y = -0.36 * k
            nm.move_to([nm.width / 2, y, 0])
            bar = Rectangle(width=2.6 * s / 3, height=0.26, stroke_width=0, fill_color=STRAT_COL[n], fill_opacity=0.8)
            bar.move_to([maxw + 0.2 + bar.width / 2, y, 0])
            sc = label(f"{s:.3f}", font_size=15, color=GREY_A).next_to(bar, RIGHT, buff=0.12)
            items.add(VGroup(nm, bar, sc))
        return VGroup(t, items).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([x, -0.4, 0])

    def noiseless(self):
        d = load("tournament")
        head = label(r"Without noise", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        r0 = d["by_noise"]["0.0"]["ranking"]
        assert [n for n, _ in r0[:5]] == ["tit for two tats", "generous tit for tat", "grim", "win-stay lose-shift",
                                          "tit for tat"]
        assert r0[-1][0] == "Joss" and r0[-2][0] == "always defect"
        panel = self.ranking(r0, -2.6, r"mean payoff per round", GOAL)
        side = stack([(r"the nice strategies, \ never first to defect, \ take the top six places", COOP),
                      (r"always defect and Joss come last", DEFECT),
                      (r"Axelrod's lessons: \ be nice, \ retaliate, \ forgive, \ be clear", INST)], font_size=18,
                     aligned_edge=LEFT, width=4.4, buff=0.3).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "Without noise, the results echo Axelrod's. <bookmark mark='a'/>The top six places go to nice strategies, "
            "those never first to defect: tit for two tats, generous tit for tat, grim, win-stay lose-shift, tit for "
            "tat and always cooperate. <bookmark mark='b'/>Always defect and Joss come last: Joss's occasional "
            "betrayal sets off long feuds with every retaliator. <bookmark mark='c'/>Axelrod drew four lessons: be "
            "nice, retaliate, forgive, and be clear enough that others can learn what you are doing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(panel[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i) for i in panel[1]], lag_ratio=0.15), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def noisy(self):
        d = load("tournament")
        head = label(r"With 5\% noise", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        r5 = d["by_noise"]["0.05"]["ranking"]
        assert r5[0][0] == "win-stay lose-shift" and r5[-1][0] == "always cooperate"
        assert [n for n, _ in r5].index("tit for tat") == 4
        panel = self.ranking(r5, -2.6, r"each intended move flipped with probability 0.05", GOAL)
        side = stack([(r"win-stay lose-shift rises to first", STRAT_COL["win-stay lose-shift"]),
                      (r"tit for tat falls: \ one error starts an echo of retaliation", STRAT_COL["tit for tat"]),
                      (r"always cooperate falls to last: \ exploited by everyone", STRAT_COL["always cooperate"]),
                      (r"Nowak and Sigmund \ (1993): \ Pavlov corrects mistakes \ that tit for tat cannot", HIST)],
                     font_size=18, aligned_edge=LEFT, width=4.4, buff=0.3).move_to([4.4, -0.2, 0])
        with self.voiceover(
            "Real players make mistakes. The Reasoner flips each intended move with probability five percent. "
            "<bookmark mark='a'/>Win-stay lose-shift rises to first place. <bookmark mark='b'/>Tit for tat falls to "
            "fifth: between two tit for tat players, one accidental defection starts an echo, each retaliating for "
            "the other's retaliation. <bookmark mark='c'/>Always cooperate falls to last, exploited by everyone. "
            "<bookmark mark='d'/>Martin Nowak and Karl Sigmund showed in 1993 why win-stay lose-shift does well: "
            "after a mutual defection it returns to cooperation, so it corrects mistakes that tit for tat cannot. "
            "Which strategy is best depends on the environment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(panel[0]))
            self.play(LaggedStart(*[FadeIn(i) for i in panel[1]], lag_ratio=0.15), run_time=2)
            for mk, r in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def river(self):
        d = load("tournament")
        head = label(r"The ecological tournament: \ a population river", font_size=30, color=CONN).to_edge(UP,
                                                                                                        buff=0.3)
        eco = d["ecology"]["0.05"]
        names, shares = eco["names"], eco["shares"]
        final = dict(zip(names, shares[-1]))
        assert final["generous tit for tat"] > 0.4 and final["win-stay lose-shift"] > 0.35
        assert final["always defect"] < 0.001
        gens = len(shares) - 1
        ax_x, ax_y, W, H = -6.0, -2.6, 8.4, 4.6
        layers = VGroup()
        cum = np.zeros(len(shares))
        for k, n in enumerate(names):
            col = np.array([s[k] for s in shares])
            lower = cum.copy()
            cum = cum + col
            pts = [[ax_x + W * t / gens, ax_y + H * lower[t], 0] for t in range(gens + 1)]
            pts += [[ax_x + W * t / gens, ax_y + H * cum[t], 0] for t in reversed(range(gens + 1))]
            layers.add(Polygon(*pts, stroke_width=0, fill_color=STRAT_COL[n], fill_opacity=0.85))
        frame = Rectangle(width=W, height=H, color=GREY_B, stroke_width=1).move_to([ax_x + W / 2, ax_y + H / 2, 0])
        xl = label(r"generations: \ each strategy's share grows with its score against the population", font_size=16,
                   color=GREY_A).next_to(frame, DOWN, buff=0.15)
        legend = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=STRAT_COL[n], fill_opacity=0.9),
                                 label(f"{n}: \\ {100 * final[n]:.1f}\\%", font_size=15, color=STRAT_COL[n])).arrange(
            RIGHT, buff=0.12) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.8, -0.3, 0])
        with self.voiceover(
            "Axelrod also ran an ecological tournament: strategies reproduce in proportion to their scores. "
            "<bookmark mark='a'/>Here is the noisy zoo over sixty generations, each band a strategy's share of the "
            "population. <bookmark mark='b'/>Always defect shrinks from the start: among retaliators it finds few "
            "victims. Always cooperate, exploited by everyone, shrinks with it; grim, which never forgives an "
            "accident, falls from a ninth of the population to almost nothing; Joss and random fade. "
            "<bookmark mark='c'/>The river ends dominated by two "
            "forgiving strategies: generous tit for tat with forty four percent, and win-stay lose-shift with "
            "thirty six. In a noisy world, the strategies that survive are nice, retaliatory, and quick to forgive."
        ) as vo:
            self.play(FadeIn(head), Create(frame), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l) for l in layers], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(legend))
            vo.wait_until("c")
            self.play(Indicate(legend[1], color=WHITE), Indicate(legend[2], color=WHITE))
        self.clear_scene()
