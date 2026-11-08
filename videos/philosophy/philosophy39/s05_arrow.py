from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Arrow(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Arrow's theorem", r"Can any rule add up rankings fairly?", lit=(1951,), part=PART)
        with self.voiceover("Chapter four. Arrow's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.conditions()
        self.iia()
        self.pivotal()
        self.reception()
        self.cousins()
        self.wall_brick()

    def conditions(self):
        head = history_card(1951, r"Kenneth Arrow", r"\textit{Social Choice and Individual Values}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"unrestricted domain", r"the rule accepts every profile of individual rankings", VOTE),
                (r"a social ordering", r"its output is a complete, \ transitive ranking", MAJ),
                (r"Pareto", r"if everyone prefers $x$ to $y$, \ so does society", SCORE),
                (r"independence \ (IIA)", r"society's ranking of $x$ and $y$ depends only on individuals' rankings of $x$ and $y$", TRUTH),
                (r"non-dictatorship", r"no voter whose strict preference always becomes society's", CYC)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Kenneth Arrow's Social Choice and Individual Values, of 1951, his doctoral thesis, asked for a rule that "
            "turns individual rankings into a social ranking. He asked for five things. <bookmark mark='a'/>The rule "
            "must accept any profile of individual rankings. <bookmark mark='b'/>Its output must be a complete and "
            "transitive ranking. <bookmark mark='c'/>If everyone prefers x to y, so must society. <bookmark "
            "mark='d'/>Society's ranking of x and y must depend only on how individuals rank x and y. <bookmark "
            "mark='e'/>And there must be no dictator, no voter whose strict preference always becomes society's. With "
            "three or more alternatives, Arrow proved, no rule satisfies all five."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def reception(self):
        head = label(r"After Arrow", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the Nobel prize \ (1972)", r"with Hicks: \ the theorem founded social choice theory", HIST),
                (r"Sen \ (1970)", r"\textit{Collective Choice and Social Welfare}: \ with comparable utilities, \ utilitarian and leximin rules escape", SCORE),
                (r"Riker \ (1982)", r"democracy as the power to remove rulers, \ not to express a general will", CYC),
                (r"G. Mackie \ (2003); \ Dryzek", r"the conditions are idealized: \ deliberation can change the profile itself", TRUTH)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The theorem's reception shaped the field. <bookmark mark='a'/>Arrow shared the Nobel prize in economics "
            "in 1972, and the theorem founded social choice theory. <bookmark mark='b'/>Amartya Sen's Collective "
            "Choice and Social Welfare, of 1970, showed that the impossibility depends on using rankings alone: if "
            "utilities can be compared between people, utilitarian and leximin rules satisfy versions of all the "
            "conditions. <bookmark mark='c'/>William Riker drew a pessimistic conclusion for democratic theory, as "
            "chapter two showed. <bookmark mark='d'/>Gerry Mackie, John Dryzek and others replied that Arrow's "
            "conditions are idealized, and that deliberation can change the profile itself, a reply chapter eleven "
            "will test."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def iia(self):
        d = load("iia")
        assert d["winner_before"] == "D" and d["winner_after"] == "E" and d["DE"] == [27, 28]
        head = label(r"Independence, \ violated: \ the Borda count", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        alts = ["A", "B", "C", "D", "E"]
        hd = [r"\text{Borda score}"] + [rf"\text{{{a}}}" for a in alts]
        cells = [[label(r"all five run", font_size=19, color=GREY_A)] +
                 [label(str(d["before"][a]), font_size=20, color=SCORE if a == d["winner_before"] else WHITE)
                  for a in alts],
                 [label(r"C withdraws", font_size=19, color=GREY_A)] +
                 [label(str(d["after"][a]), font_size=20, color=SCORE if a == d["winner_after"] else WHITE)
                  if a in d["after"] else label(r"--", font_size=20, color=GREY_D) for a in alts]]
        grid = ValueGrid(hd, cells, col_w=[3.0, 1.4, 1.4, 1.4, 1.4, 1.4], cell_h=0.62, font_size=19).move_to([0, 1.2, 0])
        foot = stack([(r"D 136, \ E 134: \ D wins", SCORE),
                      (r"C, \ an also-ran, \ withdraws: \ E 98, \ D 93: \ E wins", BAD),
                      (r"no voter changed their mind about D and E", GREY_A),
                      (r"IIA: \ the social ranking of two candidates may depend only on how voters rank those two", TRUTH)],
                     font_size=21, buff=0.22).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "The condition that does the most work is the independence of irrelevant alternatives. <bookmark "
            "mark='a'/>On the fifty five voter ballots, the Borda count ranks D first, a hundred and thirty six to "
            "E's hundred and thirty four. <bookmark mark='b'/>Now candidate C, who was never going to win, withdraws. "
            "Recount: E has ninety eight, D ninety three, and E wins. <bookmark mark='c'/>No voter changed their mind "
            "about D and E; twenty eight voters prefer E to D before and after. Only an irrelevant alternative left. "
            "<bookmark mark='d'/>Independence forbids exactly this: society's ranking of two candidates may depend "
            "only on how voters rank those two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0]], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[3]))
        self.clear_scene()

    def pivotal(self):
        n = 5
        head = label(r"The pivotal voter \ (Geanakoplos, \ 2005)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        xs = [-5.4 + 1.55 * i for i in range(n)] + [3.6]
        hdr = VGroup(*[label(rf"voter {i + 1}", font_size=18, color=VOTE).move_to([xs[i], 2.4, 0]) for i in range(n)],
                     label(r"society", font_size=20, color=GOAL).move_to([xs[n], 2.4, 0]))
        others = [("a", "c"), ("c", "a"), ("a", "c"), ("c", "a"), ("a", "c")]

        def col(i, top):
            o = others[i]
            r = ("b",) + o if top else o + ("b",)
            return ballot(r, font_size=20, w=0.9, h=0.42).move_to([xs[i], 0.9, 0])

        def soc(top):
            r = ("b", "a", "c") if top else ("a", "c", "b")
            return ballot(r, font_size=20, w=1.1, h=0.42).move_to([xs[n], 0.9, 0])

        cols = [col(i, False) for i in range(n)]
        s = soc(False)
        k = 2       # the voter at whom the social position of b flips (illustrative)
        steps = stack([(r"1. \ everyone ranks b last: \ by Pareto, \ society does too", GREY_A),
                       (r"2. \ move b to the top, \ one voter at a time: \ by IIA, \ b stays at the bottom or the top of "
                        r"society, \ never the middle", TRUTH),
                       (r"3. \ by Pareto, \ b is on top when all have moved: \ some voter $k$ flips it", SCORE),
                       (r"4. \ IIA then shows $k$ decides every pair not involving b, \ and b's pairs too: \ $k$ is a "
                        r"dictator", BAD)],
                      font_size=19, buff=0.18, aligned_edge=LEFT).move_to([0, -2.4, 0])
        for t in steps:
            if t.width > 13.0:
                t.width = 13.0
        steps.move_to([0, -2.4, 0])
        with self.voiceover(
            "Arrow's proof can be drawn. Here is John Geanakoplos's version, from 2005, with five voters. <bookmark "
            "mark='a'/>Start with every voter ranking candidate b last. By the Pareto principle, society ranks b last "
            "too. <bookmark mark='b'/>Now move b to the top of the voters' rankings, one voter at a time. Using "
            "independence, one can show that b must always be either at the very top or the very bottom of society's "
            "ranking, never in the middle. <bookmark mark='c'/>When every voter has moved b to the top, Pareto puts b "
            "on top of society. So at some voter, the pivotal voter, b jumps from the bottom to the top. <bookmark "
            "mark='d'/>Two more applications of independence show that this pivotal voter decides every other pair as "
            "well. The pivotal voter is a dictator. Any rule with Arrow's conditions hides one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in cols], FadeIn(s), FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            for i in range(k):
                self.play(Transform(cols[i], col(i, True)), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            self.play(Transform(cols[k], col(k, True)), Transform(s, soc(True)), run_time=1.2)
            mark_k = SurroundingRectangle(VGroup(cols[k], hdr[k]), color=BAD, buff=0.1)
            self.play(Create(mark_k))
            vo.wait_until("d")
            self.play(FadeIn(steps[3]), *[Transform(cols[i], col(i, True)) for i in range(k + 1, n)])
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=39, current=39).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(39, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirty ninth brick in the Wall. <bookmark mark='a'/>The dream was a fair way to add up "
            "preferences: a rule that turns any set of individual rankings into a social ranking, respects unanimity, "
            "judges each pair on its own merits, and gives no one the last word. Arrow proved there is none, and two "
            "further theorems in this part, Gibbard and Satterthwaite's on manipulation and List and Pettit's on "
            "judgments, build the same wall elsewhere. <bookmark mark='b'/>What it forces is a choice of which "
            "condition to give up, and every real voting system has made one."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[39], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def cousins(self):
        head = label(r"A family of impossibilities", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Wilson \ (1972)", r"drop Pareto: \ a rule with IIA is imposed, \ dictatorial, \ or inversely dictatorial", CYC),
                (r"Sen \ (1970)", r"the Paretian liberal of Part 38: \ even minimal rights conflict with Pareto", SCORE),
                (r"Kirman--Sondermann \ (1972)", r"with infinitely many voters, \ an `invisible dictator': \ a decisive ultrafilter", TRUTH),
                (r"Arrow's verdict", r"no rule is guaranteed to work at every profile; \ every rule can fail at some", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Arrow's theorem has relatives. <bookmark mark='a'/>Robert Wilson showed in 1972 that without Pareto, a "
            "rule satisfying independence is either imposed, dictatorial, or inversely dictatorial, always doing the "
            "opposite of one voter. <bookmark mark='b'/>Sen's liberal paradox, from Part 38, shows that even minimal "
            "rights conflict with Pareto. <bookmark mark='c'/>And Alan Kirman and Dieter Sondermann showed in 1972 "
            "that with infinitely many voters, Arrow's conditions can be met, but only by an invisible dictator: a "
            "decisive family of coalitions called an ultrafilter. <bookmark mark='d'/>The lesson is not that every "
            "rule always fails, but that every rule can fail at some profile."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
