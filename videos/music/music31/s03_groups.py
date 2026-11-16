from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403


class Groups(SoundScene):
    def construct(self):
        chapter(self, 2, r"Two groups, \ one duality", r"What do all the moves together form?", extra=((2009, r"Crans, \ Fiore and Satyendra"),))
        self.build()
        self.duality()
        self.square()
        self.relations()
        self.distance()
        self.meaning()

    # ------------------------------------------------------------------
    def build(self):
        d = load("groups")
        rows_ = text_rows([
            (r"write each move as a permutation of the 24 triads", WHITE),
            (r"compose P, \ L and R in every way, \ until nothing new appears", WHITE),
            (rf"the PLR group: \ {d['plr']} elements", TUNE),
            (rf"do the same with $T_1$ and $I_0$ \ (Part 29): \ the T/I group, \ {d['ti']} elements", BLUE),
            (r"both are the symmetries of a 12-sided polygon: \ the dihedral group", GREY_A),
        ], font_size=24)
        head = label(r"building the groups by brute force", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What do all the moves together form? The program finds out by brute force. <bookmark mark='a'/> Each move is "
            "written as a permutation of the twenty-four major and minor triads. <bookmark mark='b'/> Then P, L and R are "
            "composed in every possible order, until no new permutation appears. <bookmark mark='c'/> There are "
            f"{say(d['plr'])}: the PLR group. <bookmark mark='d'/> Doing the same with Part 29's transposition and "
            f"inversion gives the T and I group, also {say(d['ti'])} elements. <bookmark mark='e'/> Both have the shape of "
            "the symmetries of a twelve-sided polygon, the dihedral group."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duality(self):
        d = load("groups")
        rows_ = text_rows([
            (rf"every PLR move commutes with every T/I move: \ checked, \ all $24 \times 24$ pairs: \ {d['commute']}", TUNE),
            (r"P then $T_3$ \ = \ $T_3$ then P: \ transposing a parallel move gives the parallel move transposed", WHITE),
            (rf"each group reaches every triad from any triad in exactly one way: \ {d['simple_plr']} and {d['simple_ti']}", WHITE),
            (r"Lewin's duality: \ each group is exactly the set of moves that commute with the other", EAR),
            (r"proved in general by Crans, \ Fiore and Satyendra \ (2009)", GREY_A),
        ], font_size=24)
        head = label(r"the two groups are dual", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now the surprise. <bookmark mark='a'/> Every PLR move commutes with every transposition and inversion: the "
            "program checks all five hundred and seventy-six pairs. <bookmark mark='b'/> For instance, doing P and then "
            "transposing by three gives the same result as transposing by three and then doing P. <bookmark mark='c'/> "
            "And each group reaches every triad from any starting triad in exactly one way. <bookmark mark='d'/> Lewin "
            "called this duality: each group is precisely the set of moves that commute with the other. "
            "<bookmark mark='e'/> Thomas Fiore and colleagues proved it in general in 2009."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def distance(self):
        d = load("groups")
        ks = sorted(int(k) for k in d["dist"])
        bars = columns([d["dist"][str(k)] for k in ks], [str(k) for k in ks], width=6.0, height=2.6, color=TUNE, fmt="{:.0f}", font_size=19)
        bars.move_to(LEFT * 3.0 + DOWN * 0.4)
        t = label(r"triads at each number of P, \ L, \ R steps from C major", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.35)
        ex = d["examples"]
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (rf"E major: \ {ex['E']} \ (two steps)", WHITE),
            (rf"A$\flat$ major: \ {ex['Ab']}", WHITE),
            (rf"A$\flat$ minor: \ {ex['Abm']} \ (three)", EAR),
            (rf"the farthest, \ five steps: \ {tex_triad(d['farthest'][0])}", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        side.move_to(RIGHT * 3.6 + DOWN * 0.2)
        with self.voiceover(
            "A group gives a distance: the fewest moves from one triad to another. A breadth-first search from C major finds "
            "them all. <bookmark mark='a'/> E major is two steps away, L then P. <bookmark mark='b'/> A flat major is two "
            "steps, P then L. <bookmark mark='c'/> A flat minor, which shares no note with C major, is three. "
            f"<bookmark mark='d'/> And the farthest triad of all, five steps away, is {spoken(d['farthest'][0])}."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        items = [
            (r"two descriptions of the same 24 triads: \ by key and transposition, \ or by smooth moves", WHITE),
            (r"T/I sees C major and E major as related by $T_4$: \ a third away", WHITE),
            (r"PLR sees them as L then P: \ two smooth steps", WHITE),
            (r"a composer can think in either; \ the duality says they never conflict", TUNE),
            (r"duality here requires mutual centralizers and simply transitive actions", GREY_A),
        ]
        rows_scene(self, r"why it matters", items,
                   "Why does it matter? <bookmark mark='b'/> The two groups are two descriptions of the same twenty-four triads. <bookmark mark='c'/> Transposition sees C major and E major as related by a move up a major third. <bookmark mark='d'/> The PLR group sees the same pair as two smooth steps, L and then P. <bookmark mark='e'/> A composer can think in either way, and the duality specifies how their actions commute. <bookmark mark='f'/> This duality requires the stronger mutual-centralizer relationship, with simply transitive actions; commuting alone does not establish it.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def square(self):
        d = load("commute")
        c = clip("commute.two")
        def node(n, pos, col=WHITE):
            return label(tex_triad(n), font_size=34, color=col).move_to(pos)
        A = node("C", LEFT * 3 + UP * 1.2, TUNE)
        B = node(d["TP"][1], RIGHT * 3 + UP * 1.2)
        Cc = node(d["PT"][1], LEFT * 3 + DOWN * 1.6)
        Dd = node(d["TP"][2], RIGHT * 3 + DOWN * 1.6, EAR)
        arrows = VGroup(Arrow(A.get_right(), B.get_left(), color=BLUE), Arrow(A.get_bottom(), Cc.get_top(), color=TUNE),
                        Arrow(B.get_bottom(), Dd.get_top(), color=TUNE), Arrow(Cc.get_right(), Dd.get_left(), color=BLUE))
        labs = VGroup(label(r"$T_3$", font_size=24, color=BLUE).next_to(arrows[0], UP, buff=0.1), label(r"P", font_size=24, color=TUNE).next_to(arrows[1], LEFT, buff=0.1),
                      label(r"P", font_size=24, color=TUNE).next_to(arrows[2], RIGHT, buff=0.1), label(r"$T_3$", font_size=24, color=BLUE).next_to(arrows[3], DOWN, buff=0.1))
        head = label(r"the square commutes", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the duality in one square. From C major: transpose up three semitones to E flat major, then P, to E flat "
            "minor. Then the other way round: P first, to C minor, then transpose up three, to E flat minor again. Both "
            "routes arrive at the same chord, as they must for every one of the five hundred and seventy-six pairs."
        ):
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(Cc), FadeIn(Dd), FadeIn(arrows), FadeIn(labs))
        with self.listen(c) as snd:
            window(snd, r"$T_3$ then P; \ P then $T_3$", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            u = d["unit"]
            seqA = [A, B, Dd]
            seqB = [A, Cc, Dd]
            for i in range(3):
                pulse(snd, seqA[i], d["starts"]["TP"] + i * u, d["starts"]["TP"] + (i + 1) * u - 0.05, buff=0.1)
                pulse(snd, seqB[i], d["starts"]["PT"] + i * u, d["starts"]["PT"] + (i + 1) * u - 0.05, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relations(self):
        d = load("relations")
        o = d["orders"]
        rows_ = text_rows([
            (rf"each move undoes itself: \ P, \ L and R each have order {o['P']}", WHITE),
            (rf"PL has order {o['PL']}: \ six chords, \ the hexatonic cycle; \ PR has order {o['PR']}: \ eight, \ the octatonic", WHITE),
            (rf"LR has order {o['LR']}: \ alternating L and R visits all 24 triads", WHITE),
            (r"and P \ = \ R L R L R L R: \ P is not needed; \ L and R alone make all 24 elements", TUNE),
            (r"two reflections whose product has order 12: \ the dihedral group of order 24, \ the symmetries of a 12-gon", GREY_A),
        ], font_size=23)
        head = label(r"what kind of group?", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "What kind of group is it? The computer can find out by multiplying. <bookmark mark='a'/> Each move undoes "
            "itself: P, L and R each have order two. <bookmark mark='b'/> P then L has order three, which is why the "
            "hexatonic cycle has six chords; P then R has order four, giving the octatonic cycle's eight. "
            "<bookmark mark='c'/> L then R has order twelve, so alternating them visits all twenty-four triads. "
            "<bookmark mark='d'/> And P equals R, L, R, L, R, L, R, checked on every triad: P is not needed, and L and R "
            "alone generate all twenty-four elements. <bookmark mark='e'/> Two reflections whose product has order twelve "
            "make the dihedral group of order twenty-four, the symmetries of a regular twelve-sided polygon. The same group "
            "as transposition and inversion, acting the other way round."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
