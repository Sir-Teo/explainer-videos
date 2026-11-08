from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


def eu_tex(v) -> str:
    return r"+\infty" if v == float("inf") else f"{v:g}"


class Wager(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Pascal's wager", r"Is it rational to bet on God?", lit=(1670, 2003), part=PART)
        with self.voiceover("Chapter eight. Pascal's wager."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.matrix()
        self.mixed()
        self.petersburg()
        self.gods()

    def matrix(self):
        d = load("wager")
        hc = history_card(1670, r"Blaise Pascal", r"\textit{Pensées}, \ fragment 233", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        hd = [r"", r"\text{God exists}", r"\text{God does not exist}"]
        rows = [[MathTex(r"\text{wager for God}", font_size=22, color=DIV), MathTex(r"+\infty", font_size=30, color=OK),
                 MathTex(r"-c", font_size=26, color=GREY_A)],
                [MathTex(r"\text{wager against}", font_size=22, color=ARG), MathTex(r"f_1", font_size=26,
                                                                                     color=GREY_A),
                 MathTex(r"f_2", font_size=26, color=GREY_A)]]
        grid = ValueGrid(hd, rows, col_w=[3.4, 2.8, 3.4], cell_h=0.7, font_size=21).move_to([0, 0.7, 0])
        eu = VGroup(MathTex(r"EU(\text{for}) = p \cdot \infty + (1 - p)(-c) = \infty", font_size=30, color=DIV),
                    MathTex(r"EU(\text{against}) = p f_1 + (1 - p) f_2 \quad \text{(finite)}", font_size=30,
                            color=ARG)).arrange(DOWN, buff=0.2).next_to(grid, DOWN, buff=0.4)
        note = label(r"for any probability $p > 0$: \ here $p = " + f"{d['p_god']}" + r"$, \ and the answer is the "
                     r"same", font_size=20, color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Blaise Pascal changed the question: not whether God exists, but whether it is rational to wager that God "
            "does. <bookmark mark='a'/>Two acts, two states. If you wager for God and God exists, the reward is "
            "infinite: an eternity of happiness. If God does not exist, you have lost some finite pleasures, c. If you "
            "wager against, the outcomes are finite either way. <bookmark mark='b'/>Now take expected utilities. For "
            "any probability p greater than zero that God exists, the expected utility of wagering for God is p "
            "times infinity, which is infinite. Wagering against has a finite expected utility. "
            "<bookmark mark='c'/>So, said Pascal, you must wager for God, however improbable you think God is: one "
            "in a hundred, or one in a billion."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for r in grid.cell for c in r])
            vo.wait_until("b")
            self.play(Write(eu[0]), Write(eu[1]))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()

    def mixed(self):
        d = load("wager")
        hc = history_card(2003, r"Alan Hájek", r"`Waging War on Pascal's Wager'", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        hd = [r"\text{strategy}", r"\text{expected utility}"]
        rows = [[label(r["strategy"], font_size=20), MathTex(eu_tex(r["eu"]), font_size=26,
                                                              color=OK if r["eu"] == float("inf") else GREY_A)]
                for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[5.6, 3.2], cell_h=0.52, font_size=20).move_to([-1.6, -0.3, 0])
        side = stack([(r"any strategy with some chance of ending in a wager for God \ has infinite expected utility",
                       WHITE),
                      (r"so wagering outright does no better than flipping a coin, \ or than waiting for a lottery "
                       r"win", BAD),
                      (r"infinity swamps the probabilities: \ decision theory with infinite utilities cannot rank "
                       r"the options", ABS)], font_size=20, aligned_edge=LEFT, width=4.4).move_to([4.6, -0.3, 0])
        with self.voiceover(
            "Alan Hájek found a flaw in the reasoning itself. <bookmark mark='a'/>Consider mixed strategies. Flip a "
            "coin, and wager for God if it lands heads. Or wager only if a die shows six; or only if you win the "
            "lottery. <bookmark mark='b'/>Each gives some positive probability of ending up wagering for God, and so "
            "an expected utility of p times infinity, which is infinite. The Reasoner computes all five strategies: "
            "four of them tie at infinity. <bookmark mark='c'/>So wagering for God outright is no better than "
            "flipping a coin, or than doing nothing and hoping you are somehow brought to belief. "
            "<bookmark mark='d'/>The deeper lesson is about decision theory: when one outcome is infinitely good, "
            "infinity swamps the probabilities, and expected utility can no longer rank the options."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][1]) for r in range(len(rows))], lag_ratio=0.2),
                      FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def petersburg(self):
        d = load("petersburg")
        head = label(r"Infinity misbehaves elsewhere too", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"E = \sum_{k \ge 1} \frac{1}{2^k}\, 2^k = 1 + 1 + 1 + \cdots = \infty", font_size=36,
                    color=ABS).next_to(head, DOWN, buff=0.35)
        fl = label(r"Bernoulli's St. Petersburg game \ (1738): \ toss until heads; \ $k$ tosses pay $2^k$",
                   font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.15)
        hd = [r"\text{games played}", r"\text{average prize}", r"\log_2(\text{games})"]
        rows = [[MathTex(f"{r['games']:,}".replace(",", r"\,"), font_size=22),
                 MathTex(f"{r['average']:.2f}", font_size=22, color=WARM),
                 MathTex(f"{r['log2']:.1f}", font_size=22, color=GREY_A)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[2.8, 2.8, 2.6], cell_h=0.46, font_size=19).move_to([-2.4, -1.4, 0])
        side = stack([(r"an infinite expectation, \ yet a hundred thousand plays average about 22", WHITE),
                      (r"the average creeps up roughly like $\log_2 n$, \ erratically", WARM),
                      (r"no one would pay a large fee to play", BAD),
                      (r"decision theory with unbounded utility is fragile: \ Part 33", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=4.6).move_to([4.6, -1.3, 0])
        with self.voiceover(
            "Pascal is not the only place where infinity breaks expected utility. <bookmark mark='a'/>In Daniel "
            "Bernoulli's St. Petersburg game, a fair coin is tossed until it lands heads, and if that takes k tosses "
            "you win two to the k ducats. The expected prize is a half times two, plus a quarter times four, and so "
            "on: one plus one plus one, forever. Infinite. <bookmark mark='b'/>The Reasoner plays the game. After "
            "ten games the average prize is about four; after a hundred thousand, about twenty-two. "
            "<bookmark mark='c'/>The average creeps up roughly like the logarithm of the number of games, and "
            "erratically, since rare huge prizes dominate. <bookmark mark='d'/>No sensible person would pay a large "
            "fee to play, though the expectation is infinite. Decision theory with unbounded utilities is fragile, "
            "a theme for Part 33."
        ) as vo:
            self.play(FadeIn(head), Write(f), FadeIn(fl))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            self.play(FadeIn(side[0]))
            for mk, r in zip("cd", side[1:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def gods(self):
        head = label(r"Many gods, \ and the will to believe", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"many gods", r"two jealous gods, \ each rewarding only its own worshippers: \ both wagers have "
                           r"infinite expected utility", BAD),
            (r"belief is not chosen", r"Pascal's answer: \ act as if you believe, \ `take holy water', \ and belief "
                                      r"will follow", HUM),
            (r"the rewarded believer", r"would a just God reward belief adopted as a bet?", GREY_A),
            (r"James \ (1896)", r"`The Will to Believe': \ when an option is live, \ forced and momentous, \ and "
                                r"evidence cannot decide, \ we may let passion choose", WARM),
            (r"Clifford \ (1877)", r"`it is wrong always, \ everywhere, \ and for anyone, \ to believe anything upon "
                                   r"insufficient evidence'", ARG),
        ]
        g = rows_table(rows, top=1.9, gap=0.42, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "There are older objections too. <bookmark mark='a'/>The many-gods problem: imagine two jealous gods, "
            "each rewarding only those who worship it. Each wager has infinite expected utility, and the matrix "
            "cannot choose between them. <bookmark mark='b'/>Belief is not chosen like an action. Pascal answered "
            "that one can act as if one believed, take holy water, have masses said, and belief will follow. "
            "<bookmark mark='c'/>Would a just God reward belief adopted as a bet? <bookmark mark='d'/>William James "
            "defended a cousin of the wager: when a choice between beliefs is live, forced and momentous, and the "
            "evidence cannot decide it, we may let our passional nature choose. <bookmark mark='e'/>He was answering "
            "W. K. Clifford, who held that it is wrong always, everywhere, and for anyone, to believe anything upon "
            "insufficient evidence."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
