from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class May(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Majority rule, \ characterized", r"What is special about majority rule?", lit=(1952,), part=PART)
        with self.voiceover("Chapter three. Majority rule, characterized."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.statement()
        self.search()
        self.proof()
        self.meaning()

    def statement(self):
        head = history_card(1952, r"Kenneth May", r"``A Set of Independent Necessary and Sufficient Conditions for Simple Majority Decision''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"anonymity", r"every voter counts the same: \ permuting the voters changes nothing", VOTE),
                (r"neutrality", r"the two alternatives are treated alike: \ no built-in status quo", TRUTH),
                (r"positive responsiveness", r"if the result is a tie or a win for $x$, \ and one voter moves toward $x$, \ $x$ wins", SCORE),
                (r"the theorem", r"for two alternatives, \ a rule satisfies all three \ (on every profile) \ if and only if it is simple majority", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Before the impossibility, a possibility. In 1952 Kenneth May asked what is special about majority rule, "
            "when there are only two alternatives. <bookmark mark='a'/>Anonymity: every voter counts the same, so "
            "permuting the voters changes nothing. <bookmark mark='b'/>Neutrality: the alternatives are treated "
            "alike, with no built-in advantage for the status quo. <bookmark mark='c'/>Positive responsiveness: if "
            "the result is a tie or a win for x, and one voter moves toward x, then x wins. <bookmark mark='d'/>May "
            "proved that a rule has all three properties, on every profile, if and only if it is simple majority "
            "rule."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def meaning(self):
        head = label(r"What May's theorem says, \ and does not", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"supermajorities", r"two-thirds rules favour the status quo: \ they give up neutrality, \ deliberately", SCORE),
                (r"weighted votes", r"shareholder votes give up anonymity, \ deliberately", VOTE),
                (r"Dasgupta--Maskin \ (2008)", r"majority rule satisfies the key conditions on more kinds of electorate than any other rule", MAJ),
                (r"three or more", r"with three alternatives, \ majority rule can cycle: \ the next chapter's theorem", CYC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "May's theorem explains both the appeal of majority rule and its departures. <bookmark "
            "mark='a'/>Supermajority rules, such as a two-thirds vote to amend a constitution, give up neutrality on "
            "purpose, to protect the status quo. <bookmark mark='b'/>Shareholder votes, weighted by shares, give up "
            "anonymity on purpose. <bookmark mark='c'/>Partha Dasgupta and Eric Maskin showed in 2008 that majority "
            "rule satisfies the key conditions on a wider range of electorates than any other rule. <bookmark "
            "mark='d'/>But May's theorem is about two alternatives. With three or more, majority rule can cycle, and "
            "the next chapter asks whether any rule can do better."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def search(self):
        d = load("may")
        assert d["rules"] == 59049 and d["survivors"] == 1 and d["is_majority"] and d["profiles"] == 10
        head = label(r"Every anonymous rule for 3 voters, \ searched", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{for}", r"\text{abstain}", r"\text{against}", r"\text{the one survivor}"]
        word = {1: r"x wins", 0: r"tie", -1: r"y wins"}
        col = {1: MAJ, 0: GREY_A, -1: CYC}
        cells = [[label(str(c[0]), font_size=19), label(str(c[1]), font_size=19), label(str(c[2]), font_size=19),
                  label(word[v], font_size=19, color=col[v])] for c, v in zip(d["counts"], d["rule"])]
        grid = ValueGrid(hd, cells, col_w=[1.5, 1.6, 1.6, 2.8], cell_h=0.38, font_size=18).move_to([-2.6, -0.3, 0])
        side = stack([(r"10 possible vote counts", GREY_A),
                      (r"$3^{10} = 59{,}049$ rules on them", VOTE),
                      (r"neutral: \ swapping $x$ and $y$ swaps the result", TRUTH),
                      (r"positively responsive: \ one more vote for $x$ breaks a tie, \ or keeps a win", SCORE),
                      (r"survivors: \ 1, \ and it is simple majority", GOAL)],
                     font_size=20, buff=0.32, aligned_edge=LEFT).move_to([3.7, 0.0, 0])
        for s in side:
            if s.width > 5.6:
                s.width = 5.6
        side.move_to([3.7, 0.0, 0])
        with self.voiceover(
            "The Reasoner checks May's theorem by brute force, for three voters. <bookmark mark='a'/>An anonymous "
            "rule can only look at the counts: how many vote for x, how many abstain, how many vote for y. There are "
            "ten possible counts. <bookmark mark='b'/>A rule assigns each count a result, x, y or a tie, so there are "
            "three to the tenth, fifty nine thousand and forty nine rules. <bookmark mark='c'/>Keep those that are "
            "neutral: swapping the names of x and y swaps the result. <bookmark mark='d'/>And keep those that are "
            "positively responsive: if one voter moves toward x, a tie becomes a win for x, and a win stays a win. "
            "<bookmark mark='e'/>Exactly one rule survives, and it is simple majority: x wins when more vote for x "
            "than for y."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            self.play(*[FadeIn(c) for row in grid.cell for c in row[:3]])
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), LaggedStart(*[FadeIn(row[3]) for row in grid.cell], lag_ratio=0.1))
        self.clear_scene()

    def proof(self):
        head = label(r"Why only majority?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"anonymity", r"the result depends only on the counts: \ how many for $x$, \ how many for $y$", VOTE),
                (r"neutrality", r"if $x$ wins with counts $(a, b)$, \ then $y$ wins with $(b, a)$; \ so equal counts must tie", TRUTH),
                (r"responsiveness", r"from a tie, \ one more vote for $x$ makes $x$ win, \ and every further vote keeps it winning", SCORE),
                (r"so", r"$x$ wins exactly when it has more votes than $y$", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The proof for any number of voters is short. <bookmark mark='a'/>Anonymity means the result depends only "
            "on how many vote for x and how many for y. <bookmark mark='b'/>Neutrality means that swapping the counts "
            "swaps the result, so when the counts are equal, neither side can win: it must be a tie. <bookmark "
            "mark='c'/>Positive responsiveness then means that from a tie, one more vote for x makes x win, and every "
            "further vote keeps x winning. <bookmark mark='d'/>So x wins exactly when it has more votes than y: "
            "simple majority, and nothing else."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
