from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403

NAMES = {"explosion": r"explosion", "LEM": r"excluded middle", "noncontradiction": r"non-contradiction",
         "identity": r"identity", "MP": r"modus ponens", "DS": r"disjunctive syllogism"}


class Gaps(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Gaps and gluts", r"Neither true nor false, or both?", lit=(1938, 1979), part=PART)
        with self.voiceover("Chapter two. Gaps and gluts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.two_readings()
        self.grid()
        self.why()
        self.duality()

    def two_readings(self):
        d = load("tables")
        T = d["K3"]
        left = VGroup(label(r"K3: \ designate $\{1\}$", font_size=30, color=P.CLAIM),
                      ConnTable("imp", T["values"], T["imp"], designated=["1"], size=0.62),
                      label(r"$\tfrac12$ is a \textit{gap}: \ neither true nor false", font_size=24, color=HALF),
                      label(r"Kleene 1938", font_size=20, color=GREY_B)).arrange(DOWN, buff=0.35)
        right = VGroup(label(r"LP: \ designate $\{1, \tfrac12\}$", font_size=30, color=P.CLAIM),
                       ConnTable("imp", T["values"], T["imp"], designated=["1", "1/2"], size=0.62),
                       label(r"$\tfrac12$ is a \textit{glut}: \ both true and false", font_size=24, color=HALF),
                       label(r"Asenjo 1966; \ Priest, `The logic of paradox' 1979", font_size=20, color=GREY_B)
                       ).arrange(DOWN, buff=0.35)
        pair = VGroup(left, right).arrange(RIGHT, buff=2.2).move_to([0, 0.1, 0])
        bar = Line(UP * 2.6, DOWN * 2.6, color=GREY_D).move_to([0, 0.1, 0])
        same = label(r"the same tables; \ only what counts as `holding' changes", font_size=26, color=GOAL).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Kleene's tables can be read in two opposite ways, and the difference is only which values are "
            "designated. <bookmark mark='a'/>Designate one alone, and the middle value is a gap: a sentence that is "
            "neither true nor false. That is K3, Kleene's strong three-valued logic. <bookmark mark='b'/>Designate "
            "one and one half, and the middle value is a glut: a sentence that is both true and false, and so "
            "counts as holding. That is LP, the logic of paradox, proposed by Florencio Asenjo in 1966 and named "
            "and defended by Graham Priest in 1979. <bookmark mark='c'/>Same tables, opposite logics."
        ) as vo:
            self.play(FadeIn(left), Create(bar))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(same), Indicate(left[1].designated), Indicate(right[1].designated))
        self.clear_scene()

    def grid(self):
        d = load("compare")
        hd = [label(r"inference", font_size=22, color=P.CLAIM)] + [label(n, font_size=24, color=P.CLAIM)
                                                                    for n in d["logics"]]
        rows = []
        for r in d["rows"]:
            rows.append([MathTex(arg_tex(r["premises"], r["conclusion"]), font_size=30)] +
                        [c["valid"] for c in r["cells"]])
        grid = ValueGrid(hd, rows, col_w=[4.2, 1.4, 1.4, 1.4, 1.4, 1.4], cell_h=0.62, font_size=28).move_to([0.6, 0.5, 0])
        names = VGroup(*[label(NAMES[r["key"]], font_size=20, color=GREY_B).next_to(grid.cell[i][0], LEFT, buff=0.3)
                         for i, r in enumerate(d["rows"])])
        lp = d["logics"].index("LP")
        ex = d["rows"][0]["cells"][lp]["cm"]
        cmn = label(rf"LP's countermodel to explosion: \ ${cm_tex(ex)}$: \ $p$ and $\lnot p$ both hold, \ $q$ does "
                    r"not", font_size=24, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Reasoner checks six famous inferences in five logics, row by row. <bookmark mark='a'/>Classical "
            "logic validates them all. <bookmark mark='b'/>K3 keeps explosion, modus ponens and disjunctive "
            "syllogism, but loses excluded middle, non-contradiction, and even 'if p then p'. "
            "<bookmark mark='c'/>LP is the mirror image. It keeps every classical tautology, and loses explosion, "
            "modus ponens and disjunctive syllogism. <bookmark mark='d'/>Łukasiewicz's logic keeps 'if p then p', "
            "but not excluded middle. <bookmark mark='e'/>And the four-valued logic of the next chapter loses "
            "everything here. <bookmark mark='f'/>Every failure comes with a countermodel. Here is LP's against "
            "explosion: p takes the middle value, so p and not p both hold; q is false. From a contradiction, "
            "nothing in particular follows."
        ) as vo:
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))], FadeIn(names))
            for mk, c in zip("abcde", range(1, 6)):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(grid.cell[r][c], scale=0.6) for r in range(len(rows))],
                                      lag_ratio=0.12))
            vo.wait_until("f")
            self.play(FadeIn(cmn), Indicate(grid.cell[0][lp + 1], color=GOAL))
        self.clear_scene()

    def why(self):
        k3 = VGroup(label(r"K3 has no tautologies", font_size=30, color=P.CLAIM),
                    label(r"set every atom to $\tfrac12$: \ every connective maps $\tfrac12$s to $\tfrac12$", font_size=24),
                    MathTex(r"\lnot\tfrac12 = \tfrac12 \quad \tfrac12 \land \tfrac12 = \tfrac12 \quad "
                            r"\tfrac12 \lor \tfrac12 = \tfrac12 \quad \tfrac12 \to \tfrac12 = \tfrac12", font_size=32,
                            color=HALF),
                    label(r"so every formula gets $\tfrac12$, \ and $\tfrac12$ is not designated", font_size=24)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        lp = VGroup(label(r"LP has no contradictions that explode", font_size=30, color=P.CLAIM),
                    label(r"the same valuation makes every formula $\tfrac12$, \ which LP designates:", font_size=24),
                    label(r"so every set of premises can hold at once: \ no contradiction explodes", font_size=24),
                    MathTex(r"p = \tfrac12,\ q = 0:\quad p \to q = \max(1 - \tfrac12,\ 0) = \tfrac12 \ \ "
                            r"\text{holds, yet } q \text{ fails}", font_size=30, color=BAD),
                    label(r"so modus ponens fails in LP", font_size=24, color=BAD)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.22)
        g = VGroup(k3, lp).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to([0, 0, 0])
        with self.voiceover(
            "Why these patterns? <bookmark mark='a'/>In K3, set every atom to one half. Every connective sends "
            "halves to a half, so every formula gets one half, which is not designated. So no formula is true on "
            "every row: K3 has no tautologies at all. Its valid arguments are inferences, not laws. "
            "<bookmark mark='b'/>In LP, the same valuation makes everything a half, and now a half is designated. So "
            "any premises whatever can all hold together: no set of premises explodes, and from a contradiction "
            "nothing in particular follows. "
            "<bookmark mark='c'/>The price shows in modus ponens. Let p be a half and q false. 'If p then q' is a "
            "half, so it holds; p holds; q does not. An LP reasoner who accepts a conditional cannot simply detach "
            "its consequent."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in k3], lag_ratio=0.35), run_time=3)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in lp[:3]], lag_ratio=0.35), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(lp[3]), FadeIn(lp[4]))
        self.clear_scene()

    def duality(self):
        d = load("duality")
        thm = theorem_card(r"duality", MathTex(r"A \models_{K3} B \quad\iff\quad \lnot B \models_{LP} \lnot A",
                                                font_size=40), who=r"see Priest, \textit{An Introduction to Non-Classical Logic}", width=8.4,
                           font_size=24).to_edge(UP, buff=0.6)
        chk = label(rf"the Reasoner: \ all {d['pairs']} pairs from 12 formulas, \ {d['mismatches']} exceptions "
                    r"$\checkmark$", font_size=26, color=OK).next_to(thm, DOWN, buff=0.5)
        why = label(r"why: \ negation swaps `designated in K3' with `undesignated in LP'", font_size=24,
                    color=GREY_A).next_to(chk, DOWN, buff=0.3)
        gap = d["fde_gaps"][0]
        note_ = VGroup(label(r"but valid in both is not valid in every logic between them:", font_size=24,
                             color=GOAL),
                       MathTex(arg_tex([gap["A"]], gap["B"]), font_size=36),
                       label(r"holds in K3 \ (the premise never holds) \ and in LP \ (the conclusion always holds)",
                             font_size=22, color=GREY_A),
                       label(rf"and fails in the four-valued FDE: \ ${cm_tex(gap['cm'])}$ \ (next chapter)",
                             font_size=22, color=BAD)).arrange(DOWN, buff=0.18).next_to(why, DOWN, buff=0.55)
        with self.voiceover(
            "K3 and LP are exact mirror images, and there is a theorem that says so. <bookmark mark='a'/>A entails "
            "B in K3 if and only if not B entails not A in LP. <bookmark mark='b'/>The Reasoner checked it on all "
            f"{d['pairs']} pairs drawn from twelve formulas, and found no exception. <bookmark mark='c'/>The reason "
            "is that negation turns 'designated in K3' into 'undesignated in LP'. <bookmark mark='d'/>One warning. "
            "This argument is valid in both: in K3 because its premise can never hold, in LP because its "
            "conclusion always does. Yet it fails in the four-valued logic of the next chapter, which contains "
            "gaps and gluts at once: p both true and false, q neither."
        ) as vo:
            self.play(FadeIn(thm))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(chk))
            vo.wait_until("c")
            self.play(FadeIn(why))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x) for x in note_], lag_ratio=0.3))
        self.clear_scene()
