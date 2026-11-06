from __future__ import annotations

from videos.philosophy.philosophy14.common import *  # noqa: F403


class McGee(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"When modus ponens fails", r"Is `if $A$ then $B$; $A$; so $B$' always valid?",
                            lit=(1985,), part=PART)
        with self.voiceover("Chapter nine. When modus ponens fails."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.election()
        self.why()
        self.miners()

    def election(self):
        d = load("mcgee")
        hc = history_card(1985, r"Vann McGee", r"`A Counterexample to Modus Ponens'", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        polls = bar_row([0.80, 0.18, 0.02], [r"Reagan \ (Republican)", r"Carter \ (Democrat)",
                                              r"Anderson \ (Republican)"], [OUT_C, "#6FB7FF", BEL], width=2.8,
                        font_size=20, vmax=0.8, fmt=lambda v: f"{v:.2f}").move_to([-4.1, 0.4, 0])
        pl = label(r"the 1980 polls \ (illustrative)", font_size=20, color=GREY_B).next_to(polls, UP, buff=0.2)
        rows = VGroup(
            VGroup(label(r"1. \ `If a Republican wins, \ then if Reagan doesn't, \ Anderson will.'", font_size=21),
                   MathTex(rf"P = {d['P(if R then (if not Reagan then Anderson))']:.0f}", font_size=24,
                           color=OK)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"2. \ `A Republican will win.'", font_size=21),
                   MathTex(rf"P = {d['P(Republican)']:.2f}", font_size=24, color=OK)).arrange(RIGHT, buff=0.3),
            VGroup(label(r"3. \ so: \ `If Reagan doesn't win, \ Anderson will.'", font_size=21),
                   MathTex(rf"P = {d['P(if not Reagan then Anderson)']:.1f}", font_size=24, color=BAD)).arrange(
                RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        for r in rows:
            if r.width > 6.4:
                r.width = 6.4
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, 0.1, 0])
        foot = label(r"believe 1 and 2, \ and reject 3: \ modus ponens, \ apparently, \ leads from truths to a "
                     r"falsehood", font_size=22, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Vann McGee published a counterexample to modus ponens in 1985. <bookmark mark='a'/>Before the 1980 "
            "election, polls showed Ronald Reagan, a Republican, well ahead; Jimmy Carter, the Democrat, a distant "
            "second; and John Anderson, a Republican running independently, far behind. <bookmark mark='b'/>Consider: "
            "if a Republican wins, then if Reagan doesn't win, Anderson will. That is certain: they are the only "
            "Republicans. <bookmark mark='c'/>And: a Republican will win. Very likely. <bookmark mark='d'/>Modus ponens "
            "gives: if Reagan doesn't win, Anderson will. But that is very unlikely: if Reagan doesn't win, Carter "
            "almost certainly will. <bookmark mark='e'/>You may believe both premises and reject the conclusion. And "
            "Reagan did win; so the premises were true, and the conclusion, it seems, false."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(r) for r in polls], lag_ratio=0.3))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def why(self):
        head = label(r"What is going on?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ie = MathTex(r"A \to (B \to C) \ \equiv\ (A \land B) \to C", font_size=36, color=BEL).next_to(head, DOWN,
                                                                                                buff=0.45)
        iel = label(r"import--export: \ nested conditionals flatten", font_size=22, color=GREY_A).next_to(ie, DOWN,
                                                                                                    buff=0.15)
        rows = stack([
            (r"McGee: \ any conditional with import--export \ and Adams's probabilities must fail modus ponens", WHITE),
            (r"the material conditional keeps modus ponens, \ and the paradoxes", GREY_A),
            (r"Kratzer \ (1986): \ `if' is not a connective; \ it \textit{restricts} a modal: \ "
             r"`if $A$, \ (must) $C$'", NEW),
            (r"then premise 1 is about the Republican-win worlds, \ the conclusion about all worlds", GOAL),
        ], font_size=23, buff=0.3, width=12.4).next_to(iel, DOWN, buff=0.5)
        with self.voiceover(
            "What has gone wrong? <bookmark mark='a'/>The first premise is a nested conditional, and nested "
            "conditionals obey import and export: if A, then if B, C, says the same as if A and B, C. "
            "<bookmark mark='b'/>McGee showed that any conditional with import and export, whose probability is "
            "Adams's conditional probability, must fail modus ponens somewhere. <bookmark mark='c'/>The material "
            "conditional keeps modus ponens, at the price of its paradoxes. <bookmark mark='d'/>Angelika Kratzer's "
            "linguistics offers a diagnosis: if is not a connective at all. An if-clause restricts a modal, stated or "
            "implicit. <bookmark mark='e'/>Then McGee's first premise quantifies over the worlds where a Republican "
            "wins, and the conclusion over all the worlds, and the argument was never an instance of modus ponens."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(ie), FadeIn(iel))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def miners(self):
        hc = history_card(2010, r"Kolodny and MacFarlane", r"`Ifs and Oughts'", width=5.0, color=HIST).to_corner(
            UL, buff=0.35)
        shafts = VGroup(*[VGroup(Rectangle(width=1.6, height=2.0, color=GREY_B, stroke_width=3),
                                 label(t, font_size=22)).arrange(DOWN, buff=0.15) for t in (r"shaft A", r"shaft B")])
        shafts.arrange(RIGHT, buff=0.8).move_to([-3.4, -0.6, 0])
        q = MathTex(r"?", font_size=60, color=BEL).move_to(shafts[0][0])
        q2 = MathTex(r"?", font_size=60, color=BEL).move_to(shafts[1][0])
        rows = stack([
            (r"ten miners are in one shaft; \ we don't know which", WHITE),
            (r"block A: \ if they're in A, all saved; \ if in B, all die. \ Same for B", WHITE),
            (r"block neither: \ one dies, \ whichever it is", WHITE),
            (r"`if they're in A, we ought to block A'; \ `if they're in B, we ought to block B'", BEL),
            (r"they're in A or B: \ so we ought to block A or B?", BAD),
            (r"but we ought to block neither", OK),
        ], font_size=21, aligned_edge=LEFT, width=6.8).move_to([3.2, -0.4, 0])
        with self.voiceover(
            "A second puzzle, from Niko Kolodny and John MacFarlane. <bookmark mark='a'/>Ten miners are trapped in one "
            "of two shafts, and we don't know which. <bookmark mark='b'/>If we block shaft A and they are in A, all are "
            "saved; if they are in B, all die. Likewise for B. <bookmark mark='c'/>If we block neither, one miner dies, "
            "wherever they are. <bookmark mark='d'/>It seems true that if they are in A, we ought to block A, and if "
            "they are in B, we ought to block B. <bookmark mark='e'/>They are in one or the other; so, by reasoning by "
            "cases, we ought to block A or we ought to block B. <bookmark mark='f'/>But clearly we ought to block "
            "neither. Conditional oughts, like McGee's conditionals, depend on what is known, and the classical rules "
            "of inference do not survive the dependence unchanged."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(shafts), FadeIn(q), FadeIn(q2))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
