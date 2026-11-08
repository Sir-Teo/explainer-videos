from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Strategy(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Manipulation", r"Can any rule make honesty the best policy?", lit=(1973, 1975), part=PART)
        with self.voiceover("Chapter six. Manipulation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theorem()
        self.search()
        self.hardness()
        self.duverger()
        self.money()

    def theorem(self):
        head = history_card(1973, r"Allan Gibbard", r"``Manipulation of Voting Schemes: \ A General Result''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"strategy-proof", r"no voter can ever gain by misreporting her ranking", VOTE),
                (r"the theorem", r"every rule with three or more possible winners that is strategy-proof is a dictatorship", CYC),
                (r"the proof", r"strategy-proofness implies Arrow-like conditions on the rule: \ Arrow's theorem then applies", TRUTH),
                (r"in practice", r"tactical voting: \ deserting a hopeless favourite, \ burying a rival", BAD)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Allan Gibbard in 1973 and Mark Satterthwaite in 1975 proved the second impossibility of this part. "
            "<bookmark mark='a'/>Call a rule strategy-proof if no voter can ever gain by misreporting her ranking. "
            "<bookmark mark='b'/>Every strategy-proof rule with three or more possible winners is a dictatorship. "
            "<bookmark mark='c'/>The proof shows that strategy-proofness forces conditions very like Arrow's, and "
            "then Arrow's theorem applies. <bookmark mark='d'/>In practice this is tactical voting: deserting a "
            "favourite who cannot win, or burying a rival at the bottom of one's ballot."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def hardness(self):
        head = label(r"Hard to manipulate?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Bartholdi, \ Tovey, \ Trick \ (1989)", r"some rules are NP-hard to manipulate; \ and finding the Kemeny winner is NP-hard too", MACH),
                (r"Conitzer, \ Sandholm, \ Lang \ (2007)", r"coalitional manipulation is hard even with few candidates", CYC),
                (r"Friedgut, \ Kalai, \ Nisan \ (2008)", r"but at random profiles, \ a random manipulation succeeds with noticeable probability", BAD),
                (r"Faliszewski--Procaccia \ (2010)", r"``AI's War on Manipulation: \ Are We Winning?'': \ worst-case hardness is a weak shield", TRUTH)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "If manipulation cannot be prevented, perhaps it can be made hard. <bookmark mark='a'/>John Bartholdi, "
            "Craig Tovey and Michael Trick showed in 1989 that for some rules, finding a manipulation is NP-hard, and "
            "that even finding the winner under Kemeny's rule is NP-hard. <bookmark mark='b'/>Vincent Conitzer, "
            "Tuomas Sandholm and Jérôme Lang showed that coalitions face hard problems even with few candidates. "
            "<bookmark mark='c'/>But Ehud Friedgut, Gil Kalai and Noam Nisan proved in 2008 that at random profiles, "
            "a random manipulation succeeds with noticeable probability. <bookmark mark='d'/>Piotr Faliszewski and "
            "Ariel Procaccia's survey of 2010, AI's War on Manipulation: Are We Winning?, concluded that worst-case "
            "hardness is a weak shield."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def money(self):
        head = label(r"Where strategy-proofness is possible", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"single peaks", r"the median of reported peaks is strategy-proof \ (Moulin, \ 1980): \ the next chapter", MAJ),
                (r"two outcomes", r"majority vote between two options is strategy-proof", VOTE),
                (r"with money", r"Vickrey \ (1961), \ Clarke, \ Groves: \ pay for the effect your vote has on others, \ and honesty is optimal", SCORE),
                (r"randomization", r"Gibbard \ (1977): \ lotteries over dictators and pairwise votes are the strategy-proof random rules", TRUTH)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The theorem has escape routes, each with a price. <bookmark mark='a'/>If preferences are single-peaked, "
            "electing the median of the reported peaks is strategy-proof, as Hervé Moulin showed in 1980: the next "
            "chapter. <bookmark mark='b'/>With only two options, majority voting is strategy-proof. <bookmark "
            "mark='c'/>With money, the mechanisms of William Vickrey, Edward Clarke and Theodore Groves charge each "
            "person for the effect of their report on everyone else, and make honesty optimal. <bookmark "
            "mark='d'/>And Gibbard showed in 1977 that the strategy-proof random rules are lotteries over dictators "
            "and over pairwise votes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def search(self):
        m = load("manip")
        counts = {k: m[k]["manipulable"] for k in m}
        assert counts == {"plurality": 36, "borda": 51, "irv": 24, "copeland": 24, "dictator": 0, "a_or_b": 0}
        head = label(r"Every profile of 3 voters and 3 candidates, \ searched", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        names = {"plurality": r"plurality", "borda": r"Borda", "irv": r"instant runoff", "copeland": r"Copeland",
                 "dictator": r"dictatorship", "a_or_b": r"majority, \ a or b only"}
        hd = [r"\text{rule}", r"\text{manipulable profiles}", r"\text{possible winners}"]
        cells = []
        for k in ("plurality", "borda", "irv", "copeland", "dictator", "a_or_b"):
            v = m[k]
            cells.append([label(names[k], font_size=20, color=VOTE if v["manipulable"] else GREY_A),
                          label(rf"{v['manipulable']} of {v['of']}", font_size=20,
                                color=CYC if v["manipulable"] else OK),
                          label(r", \ ".join(v["range"]), font_size=20, color=GREY_A)])
        grid = ValueGrid(hd, cells, col_w=[4.0, 3.6, 3.2], cell_h=0.5, font_size=19).move_to([0, 1.0, 0])
        ex = m["plurality"]["example"]
        exl = label(rf"plurality: \ ballots {', '.join(''.join(o) for o in ex['profile'])}; \ ties broken "
                    rf"alphabetically, \ {ex['honest_winner']} wins; \ voter {ex['voter']} \ ({''.join(ex['truth'])}) "
                    rf"votes {''.join(ex['lie'])} \ and {ex['new_winner']} wins", font_size=19, color=CYC)
        if exl.width > 13:
            exl.width = 13
        foot = VGroup(exl, label(r"the two rules that cannot be manipulated: \ a dictator, \ or only two possible "
                                 r"winners", font_size=20, color=OK)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "The Reasoner searches for manipulations directly. <bookmark mark='a'/>With three voters and three "
            "candidates there are two hundred and sixteen profiles. For each rule and each profile, it asks whether "
            "some voter, by reporting a different ranking, can get an outcome she truly prefers. <bookmark "
            "mark='b'/>Plurality can be manipulated at thirty six profiles, the Borda count at fifty one, instant "
            "runoff and Copeland at twenty four each. <bookmark mark='c'/>Here is one: three ballots, a b c, b a c "
            "and c b a. Every candidate has one first place, the tie is broken alphabetically, and a wins. The third "
            "voter, whose favourite c cannot win, votes for b instead, and b wins, which she prefers to a. <bookmark "
            "mark='d'/>Only two rules are never manipulable: a dictatorship, and a rule that only ever elects a or b. "
            "Exactly as the theorem says."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[i][0]) for i in range(6)])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i][1:])) for i in range(4)], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(exl))
            vo.wait_until("d")
            self.play(*[FadeIn(VGroup(*grid.cell[i][1:])) for i in (4, 5)], FadeIn(foot[1]))
        self.clear_scene()

    def duverger(self):
        head = label(r"Strategy in real elections", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Duverger \ (1951)", r"plurality rule tends to produce two parties: \ voters desert third parties that cannot win", VOTE),
                (r"the spoiler", r"a third candidate splits a majority and elects the candidate it opposes", CYC),
                (r"Cox \ (1997)", r"\textit{Making Votes Count}: \ at most $M + 1$ viable candidates in a district of $M$ seats", SCORE),
                (r"approval and runoff", r"rules that let voters support a favourite without wasting their vote, \ at least partly", MAJ)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Manipulation is not only a theorem; it shapes party systems. <bookmark mark='a'/>Maurice Duverger "
            "observed in 1951 that plurality voting tends to produce two parties, because voters desert third parties "
            "that cannot win. <bookmark mark='b'/>A third candidate who splits a majority can elect the candidate "
            "that majority opposes: the spoiler effect. <bookmark mark='c'/>Gary Cox's Making Votes Count, of 1997, "
            "generalized the law: in a district electing M members, strategic voting leaves at most M plus one viable "
            "candidates. <bookmark mark='d'/>Rules such as approval voting and runoffs let voters support a favourite "
            "without wasting their vote, at least partly; none escapes the theorem completely."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
