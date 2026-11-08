from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.teaser()
        self.questions()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"The general will is always right, \ but the judgment which guides it is not always "
                       r"enlightened.", r"Jean-Jacques Rousseau", r"\textit{The Social Contract} \ (1762), \ II.6",
                       width=8.8, font_size=30).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Part 38 asked what a society owes its members. This part asks how a society decides anything at all. "
            "<bookmark mark='a'/>Rousseau wrote that the general will is always right, but the judgment which guides "
            "it is not always enlightened. <bookmark mark='b'/>Two centuries of mathematics have asked whether there "
            "is any such thing as a general will to be found, and whether counting votes can find it."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=MAJ, scale_factor=1.03))
        self.clear_scene()

    def teaser(self):
        z = load("zoo")
        winners = [z["plurality"]["winner"], z["runoff"]["winner"], z["irv"]["winner"], z["borda"]["winner"],
                   z["condorcet"]]
        assert winners == ["A", "B", "C", "D", "E"]
        head = label(r"One election, \ five winners", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        bal = VGroup(*[ballot(r, count=c, font_size=20, w=0.8, h=0.36) for c, r in z["profile"]]).arrange(RIGHT, buff=0.3)
        bal.move_to([0, 1.1, 0])
        names = [r"plurality", r"runoff", r"instant runoff", r"Borda", r"Condorcet"]
        tags = VGroup(*[VGroup(label(n, font_size=19, color=GREY_A),
                               label(w, font_size=34, color=ALT[w])).arrange(DOWN, buff=0.15)
                        for n, w in zip(names, winners)]).arrange(RIGHT, buff=0.7).move_to([0, -2.0, 0])
        with self.voiceover(
            "Here is the problem in one picture. <bookmark mark='a'/>Fifty five voters rank five candidates, A to E. "
            "<bookmark mark='b'/>Count their ballots in five standard ways, and you get five different winners: A, B, "
            "C, D and E. Every one of these counting rules is used somewhere in the world. <bookmark mark='c'/>So "
            "which candidate did the voters want? This part shows that the question has no rule-free answer, proves "
            "why, and builds every theorem it uses."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bal], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tags], lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(Indicate(tags, color=CYC, scale_factor=1.04))
        self.clear_scene()

    def questions(self):
        head = label(r"Four questions about counting", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"aggregation", r"can individual rankings be combined into a social ranking, \ fairly?", MAJ),
                (r"strategy", r"can a rule make honesty every voter's best policy?", CYC),
                (r"truth", r"when is a majority more likely to be right than its members?", TRUTH),
                (r"judgment", r"can a group hold consistent views when its members do?", SCORE)]
        g = rows_table(rows, top=1.5, gap=0.55, width=8.4, x_text=-2.4)
        with self.voiceover(
            "Four questions run through the part. <bookmark mark='a'/>Aggregation: can individual rankings be "
            "combined into a social ranking fairly? <bookmark mark='b'/>Strategy: can any rule make honesty every "
            "voter's best policy? <bookmark mark='c'/>Truth: when is a majority more likely to be right than its "
            "members? <bookmark mark='d'/>And judgment: can a group hold consistent views when each of its members "
            "does? Three impossibility theorems answer the first, second and fourth: Arrow's, Gibbard and "
            "Satterthwaite's, and List and Pettit's. Together they are this part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Condorcet's paradox; \ the chance of a cycle, \ exact and simulated",
            r"five rules, \ five winners; \ instant runoff; \ agenda control",
            r"May's theorem, \ by search over 59,049 rules",
            r"Arrow's theorem: \ the pivotal voter; \ IIA broken by Borda \ (the Wall)",
            r"Arrow by SAT: \ 992 clauses; \ the Price List of conditions",
            r"manipulation: \ every small profile searched; \ single peaks and the median",
            r"grades and quadratic voting; \ the jury theorem; \ diversity, \ rebuilt",
            r"the discursive dilemma; \ seats; \ deliberation; \ what reward models aggregate",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Condorcet's paradox, and the chance of a cycle, computed exactly and by "
            "simulation. <bookmark mark='b'/>Five rules with five winners, instant runoff, and the power of whoever "
            "sets the agenda. <bookmark mark='c'/>May's theorem on majority rule, checked against every rule there "
            "is. <bookmark mark='d'/>Arrow's theorem, with the pivotal voter proof, and the Borda count breaking "
            "independence. <bookmark mark='e'/>Arrow's theorem proved again by a SAT solver, and its Price List. "
            "<bookmark mark='f'/>Manipulation, searched on every small profile, and single-peaked preferences. "
            "<bookmark mark='g'/>Grades and quadratic voting, the jury theorem, and diversity, rebuilt. <bookmark "
            "mark='h'/>And the logic of group judgments, the arithmetic of seats, deliberation, and what today's "
            "reward models are really counting."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
