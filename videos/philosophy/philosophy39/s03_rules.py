from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Rules(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Five rules, \ five winners", r"Does the result depend on the counting?", lit=(1770,), part=PART)
        with self.voiceover("Chapter two. Five rules, five winners."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.five()
        self.instant()
        self.monotone()
        self.heads()
        self.agenda()
        self.debate()
        self.stv()

    def five(self):
        z = load("zoo")
        assert [z["plurality"]["winner"], z["runoff"]["winner"], z["irv"]["winner"], z["borda"]["winner"],
                z["condorcet"]] == ["A", "B", "C", "D", "E"] and z["voters"] == 55
        assert z["borda"]["scores"]["D"] == 136 and z["borda"]["scores"]["E"] == 134 and z["runoff"]["votes"] == [18, 37]
        head = label(r"55 voters, \ 5 candidates, \ 6 kinds of ballot", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        bal = VGroup(*[ballot(r, count=c, font_size=20, w=0.8, h=0.36) for c, r in z["profile"]]).arrange(RIGHT, buff=0.3)
        bal.move_to([0, 1.2, 0])
        rows = [(r"plurality", r"most first places", r"A \ (18)"),
                (r"plurality with runoff", r"top two, \ then head to head", r"B \ (37 to 18)"),
                (r"instant runoff", r"drop the weakest, \ repeatedly", r"C"),
                (r"Borda count", r"4 points for first, \ 3 for second, \dots", r"D \ (136 to 134)"),
                (r"Condorcet", r"beats every other head to head", r"E")]
        hd = [r"\text{rule}", r"\text{how}", r"\text{winner}"]
        cells = [[label(a, font_size=19, color=VOTE), label(b, font_size=18, color=GREY_A),
                  label(c, font_size=20, color=ALT[c[0]])] for a, b, c in rows]
        grid = ValueGrid(hd, cells, col_w=[3.6, 4.6, 2.6], cell_h=0.42, font_size=18).move_to([0, -1.9, 0])
        with self.voiceover(
            "Condorcet and Borda disagreed about how to count. Here is why it matters. <bookmark mark='a'/>Fifty five "
            "voters rank five candidates; there are six kinds of ballot, with eighteen, twelve, ten, nine, four and "
            "two voters. <bookmark mark='b'/>Count first places, and A wins with eighteen: plurality. <bookmark "
            "mark='c'/>Hold a runoff between the top two, and B beats A thirty seven to eighteen. <bookmark "
            "mark='d'/>Eliminate the weakest candidate one at a time, transferring their ballots, and C wins: instant "
            "runoff. <bookmark mark='e'/>Give four points for a first place, three for a second, and so on, and D "
            "wins, a hundred and thirty six to E's hundred and thirty four: the Borda count. <bookmark mark='f'/>And "
            "E beats every other candidate head to head, so E is the Condorcet winner. The same ballots elect any of "
            "the five, depending on the rule."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bal], lag_ratio=0.15))
            self.play(FadeIn(grid.head), Create(grid.rule))
            for mk, i in zip("bcdef", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[i]])
        self.clear_scene()

    def instant(self):
        z = load("zoo")
        rounds = z["irv"]["rounds"]
        assert len(rounds) == 4 and rounds[-1] == {"A": 18, "C": 37}
        head = label(r"Instant runoff, \ round by round", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        alts = ["A", "B", "C", "D", "E"]
        hd = [r"\text{candidate}"] + [rf"\text{{round {k + 1}}}" for k in range(len(rounds))]
        cells = []
        for a in alts:
            row = [label(a, font_size=22, color=ALT[a])]
            for k, r in enumerate(rounds):
                if a in r:
                    out = k + 1 < len(rounds) and a not in rounds[k + 1]
                    row.append(label(str(r[a]), font_size=21, color=BAD if out else WHITE))
                else:
                    row.append(label(r"--", font_size=21, color=GREY_D))
            cells.append(row)
        grid = ValueGrid(hd, cells, col_w=[2.4, 1.9, 1.9, 1.9, 1.9], cell_h=0.55, font_size=19).move_to([0, 0.6, 0])
        foot = stack([(r"red: \ eliminated, \ its ballots pass to their next surviving choice", GREY_A),
                      (r"C wins with 37 of 55, \ though C had only 10 first places", ALT["C"]),
                      (r"used in Australia, \ Ireland, \ and since 2018 in Maine; \ in Alaska from 2022", VOTE)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Instant runoff deserves a closer look, because it is used for real elections. <bookmark mark='a'/>In "
            "round one, E has the fewest first places, six, and is eliminated; E's ballots pass to their next "
            "choices, four to B and two to C. <bookmark mark='b'/>In round two D goes, and D's nine voters move to C. "
            "In round three B goes, and all sixteen of B's ballots now prefer C to A. <bookmark mark='c'/>C wins with "
            "thirty seven of fifty five, though C had only ten first places at the start. <bookmark mark='d'/>The "
            "method is used in Australia and Ireland, and in Maine since 2018 and Alaska since 2022. Yet E, "
            "eliminated first, beats every other candidate head to head."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), *[FadeIn(grid.cell[i][0]) for i in range(5)])
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[i][1]) for i in range(5)], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[i][2]) for i in range(5)])
            self.play(*[FadeIn(grid.cell[i][3]) for i in range(5)])
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[i][4]) for i in range(5)], FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def heads(self):
        z = load("zoo")
        N = z["pairwise"]
        alts = ["A", "B", "C", "D", "E"]
        assert all(N["E" + b] > N[b + "E"] for b in "ABCD") and (N["ED"], N["DE"]) == (28, 27)
        assert z["kemeny"]["ranking"] == ["E", "D", "C", "B", "A"] and z["schulze"]["winner"] == "E"
        head = label(r"Head to head", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{row beats column?}"] + [rf"\text{{{a}}}" for a in alts]
        cells = []
        for a in alts:
            row = [label(a, font_size=22, color=ALT[a])]
            for b in alts:
                if a == b:
                    row.append(label(r"--", font_size=19, color=GREY_D))
                else:
                    win = N[a + b] > N[b + a]
                    row.append(label(f"{N[a + b]}--{N[b + a]}", font_size=19, color=MAJ if win else GREY_B))
            cells.append(row)
        grid = ValueGrid(hd, cells, col_w=[3.0, 1.4, 1.4, 1.4, 1.4, 1.4], cell_h=0.5, font_size=18).move_to([0, 0.9, 0])
        box = SurroundingRectangle(VGroup(*grid.cell[4]), color=ALT["E"], buff=0.08)
        foot = stack([(r"E beats everyone, \ D by just 28 to 27", ALT["E"]),
                      (r"Copeland, \ Kemeny \ (E D C B A) \ and Schulze \ (Wikipedia, \ Debian) \ all elect E", MAJ),
                      (r"A, \ the plurality winner, \ loses every head-to-head contest, \ 18 to 37", BAD)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is every head-to-head contest. <bookmark mark='a'/>E's row is all wins: E beats A, B and C easily, "
            "and D by the narrowest margin, twenty eight to twenty seven. <bookmark mark='b'/>Rules built on "
            "head-to-head contests agree: Copeland counts pairwise wins; Kemeny finds the ranking that agrees with "
            "the most pairwise preferences, E, D, C, B, A; and Schulze's method, used by the Wikimedia Foundation and "
            "the Debian project, also elects E. <bookmark mark='c'/>And A, the plurality winner, loses every "
            "head-to-head contest, eighteen to thirty seven: Borda's complaint of 1770, exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(Create(box), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]), Indicate(VGroup(*grid.cell[0]), color=BAD, scale_factor=1.03))
        self.clear_scene()

    def agenda(self):
        d = load("agenda")
        assert d["winners"] == ["A", "B", "C"]
        head = label(r"Whoever sets the agenda chooses the winner", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = VGroup()
        for r in d["results"]:
            a, b, c = r["agenda"]
            line = label(rf"{a} against {b}, \ the winner against {c}: \ $\Rightarrow$ \ {r['winner']}", font_size=24,
                         color=ALT[r["winner"]])
            rows.add(line)
        rows.arrange(DOWN, buff=0.4).move_to([0, 0.9, 0])
        foot = stack([(r"the same three voters as before; \ every agenda elects someone different", GREY_A),
                      (r"McKelvey \ (1976): \ with two or more issues, \ majority voting can lead anywhere", CYC),
                      (r"Riker \ (1982): \ so `the will of the people' is an artefact of the procedure", BAD)],
                     font_size=21, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A cycle hands power to whoever controls the order of voting. <bookmark mark='a'/>Take Condorcet's three "
            "voters and vote in pairs, the winner meeting the next candidate. A against B first: A wins, then loses "
            "to C. A against C first: C wins, then loses to B. B against C first: B wins, then loses to A. <bookmark "
            "mark='b'/>Every agenda elects someone different. <bookmark mark='c'/>Richard McKelvey proved in 1976 "
            "that with two or more issues, a skilled agenda setter can lead a majority from almost any point to "
            "almost any other. <bookmark mark='d'/>William Riker's Liberalism against Populism, of 1982, concluded "
            "that the will of the people is an artefact of the procedure, and that democracy can only promise the "
            "power to remove rulers, not to express a general will."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.6), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def debate(self):
        head = label(r"Borda or Condorcet, \ today", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Young \ (1975)", r"the scoring rules are exactly the rules that are consistent across separate electorates", SCORE),
                (r"Saari \ (1990s)", r"the Borda count alone avoids certain paradoxes of subsets of candidates", SCORE),
                (r"Young \ (1988)", r"Condorcet's own probabilistic argument, \ done right, \ yields Kemeny's rule", MAJ),
                (r"the trade-off", r"no rule is both Condorcet-consistent and consistent in Young's sense", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The old debate is still live, now with theorems. <bookmark mark='a'/>Peyton Young proved in 1975 that "
            "the scoring rules, like Borda's, are exactly the rules that are consistent: if two separate electorates "
            "both choose a candidate, so does their union. <bookmark mark='b'/>Donald Saari argued through the 1990s "
            "that the Borda count alone avoids a family of paradoxes that arise when candidates are added or removed. "
            "<bookmark mark='c'/>Young also showed in 1988 that Condorcet's own probabilistic argument, done "
            "correctly, yields Kemeny's rule, the most likely true ranking if each voter is more often right than "
            "wrong. <bookmark mark='d'/>But no rule is both Condorcet-consistent and consistent in Young's sense, so "
            "the choice between the two traditions is a choice between principles."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def monotone(self):
        m = load("mono")
        assert m["n"] == 21 and m["moved"] == 2 and (m["winner_before"], m["winner_after"]) == ("C", "A")
        assert m["rounds_before"] == [{"A": 6, "B": 7, "C": 8}, {"B": 7, "C": 14}]
        assert m["rounds_after"] == [{"A": 6, "B": 5, "C": 10}, {"A": 11, "C": 10}]
        head = label(r"More votes, \ and a loss", font_size=30, color=CONN).to_edge(UP, buff=0.3)

        def panel(prof, rounds, title, w, x):
            t = label(title, font_size=21, color=GREY_A)
            bal = VGroup(*[ballot(r, count=c, font_size=18, w=0.7, h=0.34) for c, r in prof]).arrange(RIGHT, buff=0.25)
            r1 = label(r", \ ".join(rf"{k}: \ {v}" for k, v in rounds[0].items()), font_size=19)
            r2 = label(r", \ ".join(rf"{k}: \ {v}" for k, v in rounds[1].items()), font_size=19)
            res = label(rf"winner: \ {w}", font_size=24, color=ALT[w])
            g = VGroup(t, bal, label(r"round 1:", font_size=18, color=GREY_B), r1, label(r"round 2:", font_size=18,
                                                                                        color=GREY_B), r2, res)
            g.arrange(DOWN, buff=0.2).move_to([x, -0.2, 0])
            return g

        left = panel(m["before"], m["rounds_before"], r"21 voters", m["winner_before"], -3.4)
        right = panel(m["after"], m["rounds_after"], r"2 voters move C up", m["winner_after"], 3.4)
        arrow = Arrow([-0.6, 0.6, 0], [0.6, 0.6, 0], color=CYC, stroke_width=5)
        foot = label(r"found by searching every tie-free electorate up to 25 voters; \ the smallest has 21",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Instant runoff has a stranger flaw, which the Reasoner finds by search. <bookmark mark='a'/>Twenty one "
            "voters: six rank A, C, B; five B, A, C; two B, C, A; and eight C, B, A. In the first round A has six, B "
            "seven and C eight, so A is eliminated, A's voters move to C, and C wins fourteen to seven. <bookmark "
            "mark='b'/>Now two of the B, C, A voters decide they like C even more, and move C to the top. C has "
            "gained support, and nothing else has changed. <bookmark mark='c'/>The first round is now A six, B five, "
            "C ten. B is eliminated, B's five ballots go to A, and A beats C eleven to ten. More votes for C made C "
            "lose. <bookmark mark='d'/>This is called a failure of monotonicity, and the search shows the smallest "
            "tie-free example needs twenty one voters. Plurality and Borda never do this."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(right[:2]))
            vo.wait_until("c")
            self.play(FadeIn(right[2:]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def stv(self):
        head = label(r"Electing many: \ proportional representation", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Hare \ (1857)", r"the single transferable vote: \ elect anyone who reaches a quota, \ transfer surpluses and the weakest's ballots", VOTE),
                (r"the Droop quota", r"$\lfloor V / (S + 1) \rfloor + 1$ votes: \ the fewest that only $S$ candidates can reach", SCORE),
                (r"list systems", r"seats to parties in proportion to votes: \ D'Hondt and Sainte-Laguë, \ the divisor methods of chapter ten", MAJ),
                (r"the trade-off", r"proportional parliaments represent minorities, \ and need coalitions to govern", TRUTH)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Electing a parliament raises a different question: not who is best, but who represents. <bookmark "
            "mark='a'/>Thomas Hare proposed the single transferable vote in 1857: any candidate who reaches a quota "
            "is elected, surplus votes and the weakest candidates' ballots are transferred, and the count repeats. "
            "<bookmark mark='b'/>The usual quota, Henry Droop's, is the smallest number of votes that no more than S "
            "candidates can reach when S seats are filled. <bookmark mark='c'/>List systems give parties seats in "
            "proportion to their votes, by the divisor methods of D'Hondt and Sainte-Laguë that chapter ten meets "
            "again. <bookmark mark='d'/>Proportional parliaments represent minorities, and usually need coalitions to "
            "govern."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
