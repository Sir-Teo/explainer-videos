from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Judgment(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Group minds and seats", r"Can a group be rational when its members are?", lit=(1986, 2002), part=PART)
        with self.voiceover("Chapter ten. Group minds and seats."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.doctrinal()
        self.impossibility()
        self.pooling()
        self.seats()
        self.districts()

    def doctrinal(self):
        d = load("judgment")["doctrinal"]
        assert d["majority"] == {"p": 1, "q": 1, "r": 0} and d["premise_based"] == 1 and d["conclusion_based"] == 0
        head = label(r"The doctrinal paradox \ (Kornhauser and Sager, \ 1986)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        hd = [r"", r"p:\ \text{breach?}", r"q:\ \text{damage?}", r"r = p \wedge q:\ \text{liable?}"]
        cells = [[label(r0["judge"], font_size=20, color=TRUTH)] + [mark(bool(r0[k]), 26) for k in ("p", "q", "r")]
                 for r0 in d["rows"]]
        cells.append([label(r"majority", font_size=20, color=GOAL)] + [mark(bool(d["majority"][k]), 30)
                                                                       for k in ("p", "q", "r")])
        grid = ValueGrid(hd, cells, col_w=[2.6, 2.8, 2.8, 3.4], cell_h=0.62, font_size=20).move_to([0, 0.9, 0])
        box = SurroundingRectangle(VGroup(*grid.cell[3]), color=BAD, buff=0.08)
        foot = stack([(r"every judge is consistent; \ the majority accepts p and q but rejects p and q", BAD),
                      (r"premise-based: \ liable; \ \ conclusion-based: \ not liable", SCORE),
                      (r"Pettit \ (2001): \ the discursive dilemma, \ for any group that must give reasons", TRUTH)],
                     font_size=21, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Groups do not only rank options; they also make judgments. Lewis Kornhauser and Lawrence Sager described "
            "this case in 1986. <bookmark mark='a'/>A court of three judges must decide whether a defendant is "
            "liable, which by law holds exactly when a valid contract was breached, p, and damage resulted, q. The "
            "first judge says yes to both, so liable. The second says breach but no damage; the third damage but no "
            "breach. <bookmark mark='b'/>Majorities: breach, yes, two to one. Damage, yes, two to one. Liability, no, "
            "two to one. <bookmark mark='c'/>The majority accepts p, accepts q, and rejects p and q. <bookmark "
            "mark='d'/>Voting on the premises finds the defendant liable; voting on the conclusion does not. Philip "
            "Pettit called the general problem the discursive dilemma: any group that must give reasons for its "
            "decisions faces it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i])) for i in range(3)], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[3]])
            vo.wait_until("c")
            self.play(Create(box), FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]), FadeIn(foot[2]))
        self.clear_scene()

    def impossibility(self):
        d = load("judgment")["list_pettit"]
        assert d["n"] == 3 and len(d["rules"]) == 4 and not d["any_ok"]
        head = label(r"No consistent rule: \ List and Pettit \ (2002), \ checked", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        desc = {(0, 0, 1, 1): r"majority", (1, 1, 0, 0): r"accept iff 0 or 1 judges do",
                (0, 1, 0, 1): r"accept iff 1 or 3 do", (1, 0, 1, 0): r"accept iff 0 or 2 do"}
        hd = [r"\text{systematic, anonymous rule}", r"\text{a profile that breaks it}", r"\text{group: } p, q, p \wedge q"]
        cells = []
        for r0 in d["rules"]:
            ce = r0["counterexample"]
            prof = r"; \ ".join(f"({a},{b})" for a, b in ce["profile"])
            cells.append([label(desc[tuple(r0["g"])], font_size=19, color=TRUTH),
                          label(prof, font_size=19, color=GREY_A),
                          label(r", \ ".join(r"yes" if v else r"no" for v in ce["collective"]), font_size=19, color=BAD)])
        grid = ValueGrid(hd, cells, col_w=[4.6, 3.8, 3.8], cell_h=0.55, font_size=18).move_to([0, 0.9, 0])
        foot = stack([(r"systematic: \ one rule $g(k)$ for every proposition, \ $k$ = how many judges accept it", GREY_A),
                      (r"complete: \ accept each proposition or its negation, \ so $g(3 - k) = 1 - g(k)$: \ "
                       r"4 rules, \ all inconsistent somewhere", BAD),
                      (r"escape: \ drop systematicity \ (premise-based voting), \ anonymity \ (a dictator), \ or the "
                       r"domain", GOAL)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Christian List and Philip Pettit proved in 2002 that the problem is general. The Reasoner checks the "
            "smallest case. <bookmark mark='a'/>Ask for a rule that treats judges equally and every proposition "
            "alike: whether the group accepts a proposition depends only on how many judges accept it. With three "
            "judges, such a rule is a function of a number from zero to three. <bookmark mark='b'/>Completeness means "
            "the group accepts each proposition or its negation, which leaves four rules: majority voting, and three "
            "stranger ones. <bookmark mark='c'/>For each, the Reasoner searches the sixty four profiles of consistent "
            "judges, and finds one where the group's judgments are inconsistent. <bookmark mark='d'/>So the group "
            "must give up something: treating propositions alike, as premise-based voting does; treating judges "
            "alike, by following one of them; or the freedom of judges to hold any consistent view. List and Pettit's "
            "Group Agency, of 2011, argued that groups that manage this are agents in their own right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]), *[FadeIn(grid.cell[i][0]) for i in range(4)])
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[i][1:])) for i in range(4)], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def seats(self):
        s = load("seats")
        a, q = s["alabama"], s["quota"]
        assert a["hamilton"] == [[4, 3, 2], [5, 4, 1]] and a["webster"] == [[4, 3, 2], [4, 4, 2]]
        assert q["jefferson"][0] == 8 and q["quota"][0] == 6.89
        head = label(r"Dividing seats: \ the Alabama paradox", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{state}", r"\text{population}", r"\text{quota, 9 seats}", r"\text{Hamilton}",
              r"\text{quota, 10 seats}", r"\text{Hamilton}", r"\text{Webster, 9}\to\text{10}"]
        cells = []
        for i, st in enumerate(["X", "Y", "Z"]):
            lost = a["hamilton"][1][i] < a["hamilton"][0][i]
            cells.append([label(st, font_size=20, color=VOTE), label(str(a["pops"][i]), font_size=19),
                          label(f"{a['quotas'][0][i]:.3f}", font_size=19, color=GREY_A),
                          label(str(a["hamilton"][0][i]), font_size=20),
                          label(f"{a['quotas'][1][i]:.3f}", font_size=19, color=GREY_A),
                          label(str(a["hamilton"][1][i]), font_size=20, color=BAD if lost else WHITE),
                          label(rf"{a['webster'][0][i]} $\to$ {a['webster'][1][i]}", font_size=19, color=MAJ)])
        grid = ValueGrid(hd, cells, col_w=[1.0, 1.7, 2.1, 1.6, 2.2, 1.6, 2.4], cell_h=0.55,
                         font_size=16).move_to([0, 1.2, 0])
        foot = stack([(r"Hamilton: \ give each state the whole part of its quota, \ then the largest remainders", GREY_A),
                      (r"the house grows by one seat, \ and Z loses one: \ found in the 1880 census for Alabama", BAD),
                      (rf"Jefferson's divisor method avoids this, \ but can break quota: \ {q['quota'][0]} $\to$ "
                       rf"{q['jefferson'][0]} seats, \ found by search", CYC),
                      (r"Balinski--Young \ (1982): \ no method both stays within quota and avoids such paradoxes", GOAL)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A last problem of democratic arithmetic: dividing a parliament's seats among states in proportion to "
            "population. <bookmark mark='a'/>Three states with populations twenty, sixteen and seven. Each state's "
            "quota is its exact share of the seats. Alexander Hamilton's method gives each state the whole part of "
            "its quota, then hands the remaining seats to the largest fractional parts. With nine seats, Z gets two. "
            "<bookmark mark='b'/>Now enlarge the house to ten seats. Every quota grows, but Z's remainder is now the "
            "smallest, and Z drops to one seat. In 1880 the Census Office found that Alabama would lose a seat in "
            "exactly this way. Webster's divisor method gives Z two seats both times. <bookmark mark='c'/>But divisor "
            "methods have their own flaw: by search, the Reasoner finds a case where Jefferson's method gives a state "
            "eight seats when its quota is six point eight nine. <bookmark mark='d'/>Michel Balinski and Peyton Young "
            "proved in 1982 that no method both stays within quota and avoids such paradoxes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for row in grid.cell for c in row[:4]], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for row in grid.cell for c in row[4:]], FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[3]))
        self.clear_scene()

    def pooling(self):
        head = label(r"Pooling probabilities", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"linear pooling", r"average the probabilities: \ the only rule that is independent and unanimity-preserving \ (McConway, \ 1981)", SCORE),
                (r"its flaw", r"it does not commute with learning: \ pool then update differs from update then pool", BAD),
                (r"geometric pooling", r"average the log-probabilities: \ externally Bayesian, \ but not independent", TRUTH),
                (r"Dietrich--List", r"each pooling rule trades one desideratum for another: \ Arrow, \ again, \ for credences", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Groups also pool degrees of belief, the subject of Part 13. <bookmark mark='a'/>Averaging the members' "
            "probabilities, linear pooling, is the only rule that treats each event separately and preserves "
            "unanimity, as Kevin McConway proved in 1981. <bookmark mark='b'/>But it does not commute with learning: "
            "pooling and then updating on evidence gives a different answer from updating and then pooling. <bookmark "
            "mark='c'/>Averaging log-probabilities instead, geometric pooling, commutes with learning but gives up "
            "independence. <bookmark mark='d'/>Franz Dietrich and Christian List showed that every pooling rule "
            "trades one desideratum for another: Arrow's theorem again, now for credences."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def districts(self):
        head = label(r"Drawing districts", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"gerrymandering", r"pack your opponents into a few districts, \ crack the rest: \ seats without votes", CYC),
                (r"the efficiency gap", r"Stephanopoulos and McGhee \ (2015): \ compare each party's wasted votes", SCORE),
                (r"ensembles", r"generate thousands of random lawful maps by Markov chain; \ an enacted map that is an extreme outlier is suspect", MACH),
                (r"in court", r"such analyses were offered in many recent cases, \ with mixed success", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Seats depend not only on how many each state gets, but on how districts are drawn. <bookmark "
            "mark='a'/>Gerrymandering packs opponents into a few districts and cracks the rest among many, winning "
            "seats without winning votes. <bookmark mark='b'/>Nicholas Stephanopoulos and Eric McGhee proposed in "
            "2015 to measure it by comparing each party's wasted votes, the efficiency gap. <bookmark "
            "mark='c'/>Mathematicians, including Moon Duchin's group, generate thousands of random lawful maps by "
            "Markov chain sampling; an enacted map that is an extreme outlier among them is suspect. <bookmark "
            "mark='d'/>Such analyses have been offered in many recent court cases, with mixed success."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
