from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Jury(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Do crowds know?", r"When is a majority more likely to be right than its members?", lit=(1785, 2004), part=PART)
        with self.voiceover("Chapter nine. Do crowds know?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.influence()
        self.epistemic()
        self.markets()
        self.diversity()

    def epistemic(self):
        head = label(r"Epistemic democracy", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Galton \ (1907)", r"787 guesses of an ox's weight: \ the median was within 1\% of the truth", SCORE),
                (r"Estlund \ (2008)", r"\textit{Democratic Authority}: \ democracy is better than random at getting things right, \ and acceptable to all reasonable views", TRUTH),
                (r"Landemore \ (2013)", r"\textit{Democratic Reason}: \ many minds, \ diverse and inclusive, \ beat the few", MAJ),
                (r"Brennan \ (2016)", r"\textit{Against Democracy}: \ voters are often ignorant; \ consider epistocracy", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "A school of democratic theory builds on these results. <bookmark mark='a'/>Francis Galton reported in "
            "1907 that the median of seven hundred and eighty seven guesses of an ox's weight at a country fair was "
            "within one percent of the truth. <bookmark mark='b'/>David Estlund's Democratic Authority argued that "
            "democracy deserves authority because it does better than chance at getting things right, by procedures "
            "all reasonable people can accept. <bookmark mark='c'/>Hélène Landemore's Democratic Reason argued that "
            "many diverse minds outperform a few experts. <bookmark mark='d'/>Jason Brennan's Against Democracy "
            "replied that voters are often badly informed, and that rule by the knowledgeable deserves consideration. "
            "Which side the jury theorem supports depends on whether its conditions hold."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def theorem(self):
        j = load("jury")
        ns = j["ns"]
        i55, i60, cor = j["independent"]["0.55"], j["independent"]["0.6"], j["correlated"]
        assert ns[-1] == 201 and i55[-1] == 0.9226 and i60[-1] == 0.9979 and cor[-1] == 0.6045
        assert (j["q1"], j["q0"]) == (0.72, 0.42)
        head = label(r"The jury theorem \ (Condorcet, \ 1785)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 201, 50], y_range=[0.5, 1.0, 0.1], x_length=7.4, y_length=4.2,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 18},
                  x_axis_config={"numbers_to_include": [50, 100, 150, 200]},
                  y_axis_config={"numbers_to_include": [0.6, 0.7, 0.8, 0.9, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.4, -0.4, 0])
        xl = label(r"voters", font_size=18, color=VOTE).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"P(the majority is right)", font_size=18, color=TRUTH).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)

        def curve(ys, c):
            return VMobject(color=c, stroke_width=4).set_points_as_corners([ax.c2p(n, y) for n, y in zip(ns, ys)])

        c60, c55, cc = curve(i60, MAJ), curve(i55, SCORE), curve(cor, CYC)
        side = stack([(r"each voter right with $p = 0.6$, \ independently: \ 0.998 at 201", MAJ),
                      (r"$p = 0.55$: \ 0.923 at 201", SCORE),
                      (r"30\% copy an opinion leader who is right 60\% of the time: \ stuck near 0.60", CYC),
                      (r"given the leader, \ voters are right with 0.72 or 0.42: \ the crowd follows the leader",
                       GREY_A)],
                     font_size=19, buff=0.3, aligned_edge=LEFT, width=4.4).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "Condorcet had a second, more hopeful theorem. Suppose a question has a right answer, and each voter is "
            "independently more likely than not to get it right. <bookmark mark='a'/>Then the probability that the "
            "majority is right grows with the number of voters, toward certainty. The Reasoner computes it exactly: "
            "with each voter right sixty percent of the time, two hundred and one voters are right as a majority with "
            "probability point nine nine eight. <bookmark mark='b'/>Even at fifty five percent, the majority of two "
            "hundred and one is right ninety two percent of the time. <bookmark mark='c'/>But independence is doing "
            "the work. Let each voter, with probability thirty percent, copy an opinion leader who is right sixty "
            "percent of the time. <bookmark mark='d'/>Given the leader's answer, voters are right with probability "
            "point seven two or point four two, and the crowd simply follows the leader: however large it grows, it "
            "is right about sixty percent of the time. Krishna Ladha in 1992, and Franz Dietrich and Kai Spiekermann "
            "in 2013, made such results precise."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(c60), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c55), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cc), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def diversity(self):
        h = load("hongpage")
        f, fs = h["first"], h["first_smooth"]
        assert (f["agents"], f["best_team"], f["random_team"]) == (1320, 89.45, 94.2)
        assert (f["best_distinct_steps"], f["random_distinct_steps"]) == (5, 12)
        rug = [r for r in h["runs"] if r["smooth"] == 0]
        smo = [r for r in h["runs"] if r["smooth"] == 25]
        assert all(r["random_team"] > r["best_team"] for r in rug) and all(abs(r["random_team"] - r["best_team"]) < 0.2
                                                                             for r in smo)
        head = label(r"Diversity and ability \ (Hong and Page, \ 2004), \ rebuilt", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{landscape}", r"\text{seed}", r"\text{the 10 best}", r"\text{10 at random}"]
        cells = []
        for r in rug + smo:
            win = r["random_team"] > r["best_team"] + 0.2
            cells.append([label(r"rugged" if r["smooth"] == 0 else r"smooth", font_size=18,
                                color=CYC if r["smooth"] == 0 else MAJ),
                          label(str(r["seed"]), font_size=18, color=GREY_A),
                          label(f"{r['best_team']:.2f}", font_size=18),
                          label(f"{r['random_team']:.2f}", font_size=18, color=GOAL if win else WHITE)])
        grid = ValueGrid(hd, cells, col_w=[2.0, 1.4, 2.0, 2.2], cell_h=0.36, font_size=17).move_to([-3.0, -0.5, 0])
        side = stack([(r"a ring of 2,000 points with random values; \ an agent is a sequence of 3 step sizes from "
                       r"1 to 12: \ 1,320 agents", GREY_A),
                      (r"teams search in relay; \ score: \ mean value reached from every start", GREY_A),
                      (r"rugged: \ the random team wins in all 5 runs; \ the 10 best use only 5 step sizes, \ the random "
                       r"10 use all 12", GOAL),
                      (r"smooth \ (a 25-point average): \ the advantage vanishes", MAJ),
                      (r"Thompson \ (2014): \ the theorem is trivial, \ and the slogan does not follow", BAD)],
                     font_size=18, buff=0.24, aligned_edge=LEFT, width=5.6).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "A second argument for crowds concerns diversity. Lu Hong and Scott Page argued in 2004 that diversity "
            "trumps ability, and the Reasoner rebuilds their model. <bookmark mark='a'/>Values are scattered at "
            "random on a ring of two thousand points. An agent searches by trying three step sizes in a fixed order, "
            "moving whenever it finds a higher value; there are one thousand three hundred and twenty such agents. "
            "<bookmark mark='b'/>Teams work in relay, each member continuing from where the last one stopped. "
            "<bookmark mark='c'/>On this rugged landscape, a team of ten agents drawn at random beats the team of the "
            "ten best individuals in all five runs, ninety four to eighty nine in the first. The ten best are too "
            "alike: together they use only five step sizes, the random ten all twelve. <bookmark mark='d'/>Smooth the "
            "landscape, and the advantage vanishes. <bookmark mark='e'/>The mathematician Abigail Thompson argued in "
            "2014 that Hong and Page's theorem is mathematically trivial and does not support the slogan; the "
            "simulation shows that the result depends on the problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(5)], lag_ratio=0.2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(5, 10)], lag_ratio=0.2),
                      FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def influence(self):
        head = label(r"When crowds stop being wise", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Lorenz et al. \ (2011)", r"seeing others' estimates narrowed the crowd's range without improving its accuracy", BAD),
                (r"herding", r"information cascades: \ each follows those before, \ and private evidence is lost \ (Bikhchandani, \ Hirshleifer, \ Welch, \ 1992)", CYC),
                (r"the remedy", r"independent first judgments, \ then discussion: \ the jury theorem's condition, \ engineered", MAJ)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The jury theorem's fragility can be measured. <bookmark mark='a'/>Jan Lorenz and colleagues showed in "
            "2011 that when participants saw each other's estimates, the crowd's range narrowed while its accuracy "
            "did not improve: people became more confident, not more right. <bookmark mark='b'/>Economists call the "
            "extreme case an information cascade: each person follows those before, and private evidence is lost. "
            "<bookmark mark='c'/>The remedy is to collect independent judgments first and discuss afterwards, "
            "engineering the very condition the theorem needs."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def markets(self):
        head = label(r"Markets as aggregators", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Hayek \ (1945)", r"``The Use of Knowledge in Society'': \ prices gather knowledge no one person has", SCORE),
                (r"prediction markets", r"contracts that pay \$1 if an event happens trade at about its probability \ (Iowa Electronic Markets, \ 1988)", MAJ),
                (r"track record", r"Wolfers and Zitzewitz \ (2004): \ often as accurate as polls or experts, \ sometimes more", TRUTH),
                (r"limits", r"thin markets, \ long shots overpriced, \ and attempts at manipulation", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Markets are another way to pool judgments. <bookmark mark='a'/>Friedrich Hayek argued in 1945 that "
            "prices gather knowledge that no single person has. <bookmark mark='b'/>In a prediction market, a "
            "contract that pays a dollar if an event happens trades at roughly its probability; the Iowa Electronic "
            "Markets began trading on elections in 1988. <bookmark mark='c'/>Justin Wolfers and Eric Zitzewitz "
            "reviewed the record in 2004 and found such markets often as accurate as polls or experts, and sometimes "
            "more. <bookmark mark='d'/>Their limits are thin trading, a tendency to overprice long shots, and "
            "occasional attempts at manipulation."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
