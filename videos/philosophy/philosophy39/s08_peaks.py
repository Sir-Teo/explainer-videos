from __future__ import annotations

from videos.philosophy.philosophy39.common import *  # noqa: F403


class Peaks(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Single peaks", r"When does majority rule make sense?", lit=(1948,), part=PART)
        with self.voiceover("Chapter seven. Single peaks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.curves()
        self.check()
        self.downs()
        self.nominate()
        self.restrict()

    def downs(self):
        head = label(r"The median voter in politics", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Hotelling \ (1929)", r"two shops on a street crowd together at its middle", SCORE),
                (r"Downs \ (1957)", r"\textit{An Economic Theory of Democracy}: \ two parties converge on the median voter", MAJ),
                (r"the evidence", r"parties often do not converge: \ turnout, \ activists, \ primaries, \ and more than one dimension", BAD),
                (r"two dimensions", r"with a second issue, \ a median in every direction rarely exists \ (Plott, \ 1967): \ McKelvey's chaos returns", CYC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The median voter became a cornerstone of political science. <bookmark mark='a'/>Harold Hotelling "
            "observed in 1929 that two shops competing along a street will crowd together at its middle. <bookmark "
            "mark='b'/>Anthony Downs's An Economic Theory of Democracy, of 1957, applied the idea to two parties, who "
            "should converge on the median voter's position. <bookmark mark='c'/>Real parties often do not converge, "
            "because of turnout, activists, primaries, and politics having more than one dimension. <bookmark "
            "mark='d'/>With two or more issues, Charles Plott showed in 1967 that a point that beats every other by "
            "majority requires an improbable symmetry among voters, and McKelvey's chaos returns."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def restrict(self):
        head = label(r"Other restrictions that work", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Sen \ (1966)", r"value restriction: \ in each triple, \ some option is never ranked first, \ or never middle, \ or never last", TRUTH),
                (r"single-crossing", r"voters can be ordered so that each pair's supporters form an interval: \ a median voter again", SCORE),
                (r"Moulin \ (1980)", r"on single peaks, \ the median of reported peaks is strategy-proof", MAJ),
                (r"List et al. \ (2013)", r"deliberation made preferences more single-peaked in deliberative polls", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Other restrictions also work. <bookmark mark='a'/>Amartya Sen's value restriction of 1966 requires only "
            "that, in each triple of options, all voters agree that some option is not best, or not middle, or not "
            "worst. <bookmark mark='b'/>Single-crossing preferences, where voters can be lined up so that each pair's "
            "supporters form an interval, again yield a median voter. <bookmark mark='c'/>Hervé Moulin showed in 1980 "
            "that on single peaks, choosing the median of the reported peaks is also strategy-proof. <bookmark "
            "mark='d'/>And Christian List, Robert Luskin, James Fishkin and Iain McLean found in 2013 that "
            "deliberation made participants' preferences more single-peaked: talking may make democracy coherent."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def curves(self):
        axis = ["L", "CL", "C", "CR", "R"]
        head = label(r"Single-peaked preferences \ (Black, \ 1948)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        xs = [-4.0 + 2.0 * i for i in range(5)]
        base = -2.2
        line = Line([xs[0] - 0.8, base, 0], [xs[-1] + 0.8, base, 0], color=GREY_B, stroke_width=2)
        ticks = VGroup(*[label(a, font_size=22, color=GREY_A).move_to([x, base - 0.35, 0]) for a, x in zip(axis, xs)])
        voters = [(1, VOTE, r"voter 1"), (2, MAJ, r"voter 2"), (3, SCORE, r"voter 3")]
        curves, peaks_m = VGroup(), VGroup()
        for pk, c, nm in voters:
            pts = [np.array([x, base + 0.3 + 3.2 * math.exp(-0.5 * ((i - pk) / 1.1) ** 2), 0]) for i, x in enumerate(xs)]
            cv = VMobject(color=c, stroke_width=4).set_points_smoothly(pts)
            curves.add(VGroup(cv, label(nm, font_size=18, color=c).next_to(pts[pk], UP, buff=0.15)))
            peaks_m.add(Dot(pts[pk], radius=0.08, color=c))
        med = DashedLine([xs[2], base, 0], [xs[2], 2.0, 0], color=GOAL, stroke_width=3)
        medl = label(r"the median peak", font_size=20, color=GOAL).move_to([xs[2] + 1.4, 1.9, 0])
        foot = stack([(r"each voter has one peak, \ and likes options less the further they are from it", GREY_A),
                      (r"the median peak beats every other option by majority", GOAL)],
                     font_size=20, buff=0.18).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Arrow's first condition was that any profile of rankings may occur. Often they cannot. <bookmark "
            "mark='a'/>Line the options up from left to right, here five positions from left to right in politics. "
            "Duncan Black, in 1948, called a voter's preferences single-peaked if she has a favourite position and "
            "likes the others less the further away they are. <bookmark mark='b'/>Three voters, with peaks at centre "
            "left, centre and centre right. <bookmark mark='c'/>Black proved that the median peak, here the centre, "
            "beats every other option by majority. Anything to its right is opposed by the median voter and everyone "
            "to her left, and anything to its left by the median voter and everyone to her right."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(ticks))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c[0]) for c in curves], lag_ratio=0.4), *[FadeIn(c[1]) for c in curves],
                      FadeIn(peaks_m), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(Create(med), FadeIn(medl), FadeIn(foot[1]))
        self.clear_scene()

    def check(self):
        b = load("black")
        assert (b["single_peaked"], b["all_orders"], b["profiles"]) == (16, 120, 4096)
        assert b["with_winner"] == b["winner_is_median"] == 4096 and b["random_no_winner"] == 0.1551
        head = label(r"Black's theorem, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lines = stack([(r"of the 120 rankings of 5 positions, \ 16 are single-peaked on the axis", GREY_A),
                       (r"every profile of 3 single-peaked voters: \ $16^3 = 4{,}096$", VOTE),
                       (r"a Condorcet winner in all 4,096", MAJ),
                       (r"and it is the median voter's peak in all 4,096", GOAL),
                       (r"10,000 unrestricted random profiles: \ 15.5\% have no Condorcet winner", CYC)],
                      font_size=24, buff=0.4).move_to([0, 0.0, 0])
        with self.voiceover(
            "The Reasoner checks the theorem on every case. <bookmark mark='a'/>Of the hundred and twenty rankings of "
            "five positions, sixteen are single-peaked on this axis. <bookmark mark='b'/>Three voters with "
            "single-peaked rankings give sixteen cubed, four thousand and ninety six profiles. <bookmark "
            "mark='c'/>Every one of them has a Condorcet winner, <bookmark mark='d'/>and in every one it is the "
            "median voter's peak. <bookmark mark='e'/>Drop the restriction and draw ten thousand profiles at random: "
            "fifteen and a half percent have no Condorcet winner at all. Restricting the domain is the classic escape "
            "from Arrow's theorem: on single-peaked profiles, pairwise majority is transitive."
        ) as vo:
            self.play(FadeIn(head))
            for mk, i in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(FadeIn(lines[i], shift=RIGHT * 0.2))
        self.clear_scene()

    def nominate(self):
        head = label(r"How many dimensions does politics have?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Poole--Rosenthal \ (1985)", r"NOMINATE: \ place every legislator and roll call in a space that best explains the votes", MAJ),
                (r"one dimension", r"for most of US congressional history, \ one dimension explains most roll-call votes", VOTE),
                (r"polarization", r"the parties' positions on it have moved apart since the 1970s", CYC),
                (r"the implication", r"close to one dimension, \ cycles are unlikely and the median matters", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "How close is real politics to a single dimension? <bookmark mark='a'/>Keith Poole and Howard Rosenthal's "
            "NOMINATE method, from 1985, places every legislator and every roll call in the space that best explains "
            "the votes. <bookmark mark='b'/>For most of the history of the United States Congress, a single "
            "dimension, roughly left to right on economics, explains most roll-call votes. <bookmark mark='c'/>The "
            "two parties' positions on it have moved steadily apart since the 1970s. <bookmark mark='d'/>Close to one "
            "dimension, cycles are unlikely and the median voter matters, which is one reason majority rule works as "
            "well as it does."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
