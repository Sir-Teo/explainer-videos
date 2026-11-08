from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Cardinal(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Beyond rankings", r"Can votes measure how much we care?", lit=(2011, 2018), part=PART)
        with self.voiceover("Chapter eight. Beyond rankings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.grades()
        self.mj()
        self.qv()
        self.budget()
        self.utility()

    def grades(self):
        head = history_card(2011, r"Balinski and Laraki", r"\textit{Majority Judgment}", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"range voting", r"score every candidate, \ say 0 to 9; \ the highest total wins", SCORE),
                (r"approval voting", r"approve as many as you like \ (Brams and Fishburn, \ 1978); \ used in Fargo \ (2018) \ and St. Louis \ (2020)", VOTE),
                (r"majority judgment", r"grade each candidate in words; \ the highest median grade wins \ (Balinski and Laraki)", MAJ),
                (r"and Arrow?", r"these rules use grades, \ not rankings: \ Arrow's theorem does not apply to them as stated", TRUTH)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "One response to Arrow is to ask voters for more than a ranking. <bookmark mark='a'/>Range voting asks "
            "for a score for every candidate, and the highest total wins. <bookmark mark='b'/>Approval voting, "
            "studied by Steven Brams and Peter Fishburn in 1978, lets voters approve as many candidates as they like; "
            "Fargo, North Dakota adopted it in 2018 and St. Louis in 2020. <bookmark mark='c'/>Michel Balinski and "
            "Rida Laraki's majority judgment asks voters to grade each candidate in words, from excellent to reject, "
            "and elects the one with the highest median grade. <bookmark mark='d'/>These rules take grades rather "
            "than rankings as input, so Arrow's theorem does not apply to them as stated. Whether grades mean the "
            "same to different voters is the question that remains."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def utility(self):
        head = label(r"Comparing utilities", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Arrow's input", r"rankings only: \ no information about intensity, \ or about comparisons between people", TRUTH),
                (r"Sen \ (1970); \ d'Aspremont--Gevers \ (1977)", r"with comparable utilities, \ the utilitarian sum and the leximin rule satisfy all of Arrow's other conditions", SCORE),
                (r"the link", r"Harsanyi's theorem of Part 35 and the veil of Part 38 are aggregation theorems of this kind", MAJ),
                (r"the cost", r"someone must decide how to compare one person's gain with another's loss", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The deepest escape changes the input. <bookmark mark='a'/>Arrow's rules see only rankings: no "
            "intensities, and no comparisons between people. <bookmark mark='b'/>Sen showed in 1970, and Claude "
            "d'Aspremont and Louis Gevers in 1977, that once utilities can be compared across people, the utilitarian "
            "sum and the leximin rule, which maximizes the position of the worst off, satisfy all of Arrow's other "
            "conditions. <bookmark mark='c'/>Harsanyi's theorem in Part 35 and the veil of ignorance in Part 38 are "
            "aggregation theorems of exactly this kind. <bookmark mark='d'/>The cost is that someone must decide how "
            "one person's gain compares with another's loss, and that is not a matter that voting can settle."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def qv(self):
        d = load("qv")
        assert d["votes"] == [5.0, 5.0, 5.0, -25.0] and d["majority"] == "pass" and d["qv"] == "fail"
        head = label(r"Quadratic voting \ (Lalley and Weyl, \ 2018)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f1 = MathTex(r"\text{cost}(v) = v^2", font_size=36, color=SCORE).move_to([-3.4, 2.1, 0])
        f2 = MathTex(r"\max_v \; u\,v - v^2 \;\;\Rightarrow\;\; v = \tfrac{u}{2}", font_size=36,
                     color=WHITE).move_to([2.8, 2.1, 0])
        hd = [r"\text{voter}", r"\text{stake } u", r"\text{votes } u/2", r"\text{pays } v^2"]
        cells = []
        for i, (u, v, c) in enumerate(zip(d["values"], d["votes"], d["costs"])):
            col = MAJ if u > 0 else CYC
            cells.append([label(rf"voter {i + 1}", font_size=20, color=col), label(f"{u:+.0f}", font_size=20, color=col),
                          label(f"{v:+.0f}", font_size=20, color=col), label(f"{c:.0f}", font_size=20, color=GREY_A)])
        grid = ValueGrid(hd, cells, col_w=[2.2, 2.2, 2.4, 2.2], cell_h=0.5, font_size=19).move_to([0, 0.0, 0])
        foot = stack([(r"one person, \ one vote: \ 3 to 1, \ the measure passes", VOTE),
                      (rf"quadratic voting: \ $+15 - 25 = {d['qv_total']:+.0f}$, \ it fails, \ as the stakes "
                       rf"\ ({d['net_value']:+.0f}) \ say it should", GOAL),
                      (r"used by the Colorado House \ (2019) \ and in quadratic funding for open-source software", GREY_A)],
                     font_size=21, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Rankings cannot express how much a voter cares. Quadratic voting can. <bookmark mark='a'/>Each voter may "
            "cast as many votes as she likes, for or against, but v votes cost v squared. <bookmark mark='b'/>A voter "
            "who gains u if a measure passes buys the number of votes that maximizes u v minus v squared, which is u "
            "over two: votes in proportion to the stakes. <bookmark mark='c'/>Three voters gain ten each from a "
            "measure; one loses fifty. They buy five votes each; she buys twenty five against, at a cost of six "
            "hundred and twenty five. <bookmark mark='d'/>One person, one vote passes the measure, three to one. "
            "<bookmark mark='e'/>Quadratic voting rejects it, fifteen to twenty five, as the total stakes, minus "
            "twenty, say it should. Steven Lalley and Glen Weyl proved in 2018 that in large populations the outcome "
            "tends to maximize total value. <bookmark mark='f'/>Democrats in the Colorado House used it to rank bills "
            "in 2019, and quadratic funding allocates donations to open-source software. The objections: it lets "
            "money matter, and the rich can buy more votes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(Write(f2))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell],
                                                                         lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
            vo.wait_until("f")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def budget(self):
        head = label(r"Proportionality: \ participatory budgeting", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Porto Alegre \ (1989)", r"citizens vote directly on part of the city budget; \ now used in thousands of cities", VOTE),
                (r"justified representation", r"Aziz et al. \ (2017): \ a large enough group that agrees deserves some of what it wants", MAJ),
                (r"equal shares", r"Peters and Skowron: \ give each voter an equal share of the budget to spend on projects they approve", SCORE),
                (r"in use", r"the method of equal shares decided budgets in Wieliczka, \ Poland \ (2023), \ and Aarau, \ Switzerland", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Approval ballots also power a newer practice. <bookmark mark='a'/>In participatory budgeting, begun in "
            "Porto Alegre, Brazil, in 1989, citizens vote directly on part of a city's budget. <bookmark "
            "mark='b'/>Haris Aziz and colleagues defined justified representation in 2017: any large enough group of "
            "voters who agree on projects deserves some of what it wants. <bookmark mark='c'/>Dominik Peters and "
            "Piotr Skowron's method of equal shares gives each voter an equal share of the budget, to be spent only "
            "on projects that voter approves. <bookmark mark='d'/>It decided real budgets in Wieliczka, Poland, in "
            "2023, and in Aarau, Switzerland."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def mj(self):
        head = label(r"Grades in practice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Orsay \ (2007)", r"Balinski and Laraki ran majority judgment alongside the French presidential election", MAJ),
                (r"strategy", r"no rule escapes Gibbard--Satterthwaite; \ medians blunt exaggeration, \ approval rewards sincere top choices", CYC),
                (r"common scales", r"whether `good' means the same to every voter is assumed, \ not shown", BAD),
                (r"Arrow, \ revisited", r"with grades on a common scale, \ Arrow's independence can hold: \ the theorem's force was the poverty of rankings", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Grading rules have been tried in the field. <bookmark mark='a'/>Balinski and Laraki ran majority "
            "judgment alongside the 2007 French presidential election in polling stations at Orsay, and found that "
            "voters used the grades readily. <bookmark mark='b'/>No rule escapes manipulation entirely; medians blunt "
            "the effect of exaggeration, and approval voting rewards a sincere vote for one's top choices. <bookmark "
            "mark='c'/>All of these rules assume that a grade such as good means the same to every voter, which is "
            "assumed rather than shown. <bookmark mark='d'/>If it does, independence can hold: Arrow's theorem had "
            "its force because rankings carry so little information."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
