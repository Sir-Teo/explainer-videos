from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403
from explainer.philosophy.reasoner import syllogism as sy

FIG_TEX = {1: (r"M\text{--}P", r"S\text{--}M"), 2: (r"P\text{--}M", r"S\text{--}M"), 3: (r"M\text{--}P", r"M\text{--}S"),
           4: (r"P\text{--}M", r"M\text{--}S")}


class Moods(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Two hundred and fifty-six moods", r"Which syllogisms are valid? \ All of them, "
                            r"checked", lit=(-350,), part=PART)
        with self.voiceover("Chapter eight. Two hundred and fifty-six moods."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.figures()
        self.models()
        self.grid()
        self.reduction()

    def figures(self):
        figs = VGroup()
        for f in (1, 2, 3, 4):
            a, b = FIG_TEX[f]
            figs.add(VGroup(label(rf"figure {f}", font_size=26, color=GOAL),
                            MathTex(a, font_size=34), MathTex(b, font_size=34),
                            Line(LEFT * 0.8, RIGHT * 0.8, color=GREY_B), MathTex(r"S\text{--}P", font_size=34)).arrange(
                DOWN, buff=0.15))
        figs.arrange(RIGHT, buff=1.0).move_to([0, 0.8, 0])
        count = MathTex(r"4 \text{ figures} \times 4^3 \text{ choices of A, E, I, O} = 256 \text{ moods}",
                        font_size=36).to_edge(DOWN, buff=1.2)
        bar = label(r"Barbara: \ all $M$ are $P$; \ all $S$ are $M$; \ so all $S$ are $P$", font_size=28,
                    color=OK).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A syllogism has two premises and a conclusion, built from three terms. The conclusion joins S to P; "
            "the middle term M appears in both premises and links them. <bookmark mark='a'/>The middle term can sit "
            "in four positions, the four figures. <bookmark mark='b'/>Each of the three sentences can be A, E, I or "
            "O: sixty-four moods per figure, two hundred and fifty-six in all. <bookmark mark='c'/>The most famous is "
            "Barbara: all M are P, all S are M, so all S are P. Which of the two hundred and fifty-six are valid? For "
            "two thousand years the answer was learned by heart."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.2) for f in figs], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(Write(count))
            vo.wait_until("c")
            self.play(FadeIn(bar), Indicate(figs[0], color=OK))
        self.clear_scene()

    def models(self):
        d = load("moods")
        V = venn3(radius=1.2, center=[-3.4, -0.2, 0])
        regs = [r for r in sy.REGIONS]
        shapes = [V.region(r, color=GOAL, opacity=0.35) for r in regs]
        eight = label(r"8 regions, \ each inhabited or empty: \ $2^8 = 256$ possible worlds", font_size=26,
                      color=GOAL).to_edge(UP, buff=0.4)
        test = VGroup(label(r"a mood is valid if:", font_size=28),
                      label(r"in every one of the 256 arrangements", font_size=26, color=GREY_A),
                      label(r"where both premises hold,", font_size=26, color=GREY_A),
                      label(r"the conclusion holds too.", font_size=26, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.15)
        test.move_to([3.4, 0.3, 0])
        cm = d["undistributed"]
        cm_shapes = [V.region(tuple(r), color=BAD, opacity=0.55) for r in cm]
        cml = label(r"a countermodel for `all $P$ are $M$, all $S$ are $M$, so all $S$ are $P$'", font_size=24,
                    color=BAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "We can check them all, by machine, using Venn's picture. <bookmark mark='a'/>Three circles make eight "
            "regions. Each region can be inhabited or empty, so there are two to the eight, two hundred and "
            "fifty-six, possible arrangements of the world, as far as three terms can tell. "
            "<bookmark mark='b'/>A mood is valid if, in every arrangement where both premises hold, the conclusion "
            "holds too. It is a truth table for syllogisms. <bookmark mark='c'/>For an invalid mood the machine finds "
            "a countermodel: here, an arrangement where all P are M and all S are M, but some S is not P."
        ) as vo:
            self.play(FadeIn(V))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in shapes], lag_ratio=0.15), FadeIn(eight), run_time=2.5)
            self.play(*[FadeOut(s) for s in shapes])
            vo.wait_until("b")
            self.play(FadeIn(test, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(*[FadeIn(s) for s in cm_shapes], FadeIn(cml))
        self.clear_scene()

    def grid(self):
        d = load("moods")
        rows = d["rows"]
        cells = VGroup()
        idx = {}
        for f in (1, 2, 3, 4):
            for j, r in enumerate([r for r in rows if r["figure"] == f]):
                sq = Square(0.17, stroke_width=0.6, stroke_color=GREY_D, fill_color=GREY_E, fill_opacity=1)
                sq.move_to([-5.7 + j * 0.185, 1.9 - (f - 1) * 1.1, 0])
                cells.add(sq)
                idx[(f, r["mood"])] = sq
        flabs = VGroup(*[label(rf"fig.\ {f}", font_size=22, color=GREY_A).move_to([-6.45, 1.9 - (f - 1) * 1.1, 0])
                         for f in (1, 2, 3, 4)])
        flabs.shift(LEFT * 0.0)
        boolean = [(f, m) for f, m, _ in d["boolean"]]
        names = {(f, m): n for f, m, n in d["boolean"]}
        tags = VGroup()
        seen = {1: 0, 2: 0, 3: 0, 4: 0}
        for (f, m) in sorted(boolean, key=lambda k: (k[0], "AEIO".index(k[1][0]) * 16 + "AEIO".index(k[1][1]) * 4 +
                                                   "AEIO".index(k[1][2]))):
            sq = idx[(f, m)]
            tags.add(label(names[(f, m)], font_size=15, color=OK).next_to(sq, DOWN if seen[f] % 2 == 0 else UP,
                                                                          buff=0.06))
            seen[f] += 1
        cnt = label(rf"valid: \ {len(boolean)} of 256", font_size=34, color=OK).to_edge(DOWN, buff=1.0)
        verse = label(r"`Barbara, Celarent, Darii, Ferioque prioris \dots' \ (13th-century mnemonic verse)",
                      font_size=22, color=GREY_B).to_edge(DOWN, buff=0.35)
        by = d["by_figure"]
        with self.voiceover(
            "Here are all two hundred and fifty-six, one cell each, sixty-four to a figure. <bookmark mark='a'/>The "
            "Reasoner checks each against all two hundred and fifty-six arrangements of the regions. "
            f"<bookmark mark='b'/>{len(boolean)} pass: {by['1']['boolean']} in the first figure, "
            f"{by['2']['boolean']} in the second, {by['3']['boolean']} in the third, and {by['4']['boolean']} in "
            "the fourth. <bookmark mark='c'/>They are exactly the moods with the old Latin names, Barbara, Celarent, "
            "Darii, Ferio and the rest, which students chanted in a verse for six hundred years. Or rather, almost "
            "exactly. The verse has more names than our machine has valid moods."
        ) as vo:
            self.play(FadeIn(flabs), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.003), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[c.animate.set_fill(GREY_D) for c in cells], lag_ratio=0.002), run_time=2)
            vo.wait_until("b")
            self.play(*[idx[k].animate.set_fill(OK) for k in boolean], FadeIn(cnt))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in tags], lag_ratio=0.1), FadeIn(verse))
        self.clear_scene()

    def reduction(self):
        name = VGroup(*[MathTex(c, font_size=72, color=GOAL if c in "Ee" else (CONN if c in "Cs" else WHITE))
                        for c in "Cesare"]).arrange(RIGHT, buff=0.05).to_edge(UP, buff=0.5)
        key = VGroup(label(r"vowels \ \textit{e, a, e}: \ the mood EAE", font_size=24, color=GOAL),
                     label(r"first letter \textit{C}: \ reduce to Celarent", font_size=24, color=CONN),
                     label(r"\textit{s} after a vowel: \ convert that premise simply", font_size=24, color=CONN),
                     label(r"\textit{p}: per accidens; \ \textit{m}: swap premises; \ \textit{c}: by contradiction",
                           font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        key.next_to(name, DOWN, buff=0.4)
        before = VGroup(label(r"Cesare: \ No $P$ are $M$; \ all $S$ are $M$; \ so no $S$ are $P$", font_size=28),
                        label(r"Celarent: \ No $M$ are $P$; \ all $S$ are $M$; \ so no $S$ are $P$", font_size=28,
                              color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -1.6, 0])
        arr = Arrow(before[0].get_bottom(), before[1].get_top(), buff=0.08, color=CONN)
        arrl = label(r"convert the major premise", font_size=22, color=CONN).next_to(arr, RIGHT, buff=0.2)
        with self.voiceover(
            "Aristotle did not check moods with diagrams. He proved them, by reducing each one to the 'perfect' moods "
            "of the first figure, using conversion. <bookmark mark='a'/>And the medieval names are not arbitrary: "
            "they encode the proofs. Take Cesare. Its vowels, e, a, e, give the mood. <bookmark mark='b'/>Its first "
            "letter, C, says it reduces to Celarent. The s after the first vowel says: convert that premise simply. "
            "<bookmark mark='c'/>Convert 'no P are M' to 'no M are P', and Cesare becomes Celarent. The other "
            "letters say convert by limitation, swap the premises, or argue by contradiction. The chanted verse was a "
            "compressed proof system, the first in history."
        ) as vo:
            self.play(FadeIn(name))
            vo.wait_until("a")
            self.play(FadeIn(key[0]))
            vo.wait_until("b")
            self.play(FadeIn(key[1:]))
            vo.wait_until("c")
            self.play(FadeIn(before[0]))
            self.play(GrowArrow(arr), FadeIn(arrl), FadeIn(before[1]))
        self.clear_scene()
