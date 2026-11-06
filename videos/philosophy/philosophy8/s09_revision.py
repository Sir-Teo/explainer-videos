from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Revision(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Revision", r"What if truth is a rule for changing your mind?", lit=(1993,),
                            part=PART)
        with self.voiceover("Chapter eight. Revision."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rule()
        self.grid()
        self.verdicts()
        self.limits()

    def rule(self):
        hcs = VGroup(history_card(1982, r"Anil Gupta; \ Hans Herzberger", r"revision sequences, \ independently",
                                  width=5.6, color=HIST),
                     history_card(1993, r"Gupta \& Nuel Belnap", r"\textit{The Revision Theory of Truth}", width=5.6,
                                  color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        rows = VGroup(label(r"start from any guess about which sentences are true \ (every sentence true or false)",
                            font_size=26),
                      label(r"revise: \ a sentence is true at the next stage \ iff \ it comes out true under the "
                            r"current guess", font_size=26, color=GOAL),
                      label(r"repeat, \ and watch what settles", font_size=26),
                      label(r"classical logic is kept: \ there are no gaps, \ only instability", font_size=26,
                            color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(hcs, DOWN, buff=0.6)
        with self.voiceover(
            "A different idea came in 1982, from Anil Gupta and, independently, Hans Herzberger, and was developed "
            "by Gupta and Nuel Belnap in 1993. <bookmark mark='a'/>Start with any guess about which sentences are "
            "true, giving every sentence one of the two classical values. <bookmark mark='b'/>Then revise: at the "
            "next stage, call a sentence true exactly when it comes out true under the current guess. "
            "<bookmark mark='c'/>Repeat, and watch which sentences settle. <bookmark mark='d'/>There are no gaps "
            "and no third value. Truth is a rule of revision, and paradox shows up as instability."
        ) as vo:
            self.play(FadeIn(hcs))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

    def grid(self):
        d = load("revision")
        names = ["s1", "s3", "s5", "L", "H", "s8", "A", "B"]
        seq = d["seqs"]["all false"]
        seq2 = d["seqs"]["all true"]
        head = label(r"Two revision sequences, \ run by the Reasoner", font_size=30, color=CONN).to_edge(UP, buff=0.35)

        def block(sq, x0, title):
            g = VGroup()
            g.cells = {}
            t = label(title, font_size=22, color=GREY_A).move_to([x0 + 1.9, 2.55, 0])
            g.add(t)
            for j in range(len(sq)):
                g.add(label(rf"{j}", font_size=18, color=GREY_B).move_to([x0 + 0.55 * j, 2.15, 0]))
            for i, n in enumerate(names):
                y = 1.65 - 0.55 * i
                for j, h in enumerate(sq):
                    v = "t" if h[n] else "f"
                    c = RoundedRectangle(width=0.46, height=0.42, corner_radius=0.05, stroke_width=0,
                                         fill_color=VCOL[v], fill_opacity=0.8).move_to([x0 + 0.55 * j, y, 0])
                    g.cells[(n, j)] = c
                    g.add(c)
            return g

        left = block(seq, -4.3, r"start: \ everything false")
        right = block(seq2, 1.7, r"start: \ everything true")
        labs = VGroup(*[label(rf"\textbf{{{n}}}", font_size=22).move_to([-5.2, 1.65 - 0.55 * i, 0])
                        for i, n in enumerate(names)])
        rl = label(r"stage", font_size=18, color=GREY_B).move_to([-5.2, 2.15, 0])
        with self.voiceover(
            "Here are two revision sequences for our small world, one starting from 'everything false', one from "
            "'everything true'. <bookmark mark='a'/>Each column is a stage, each row a sentence, green for true and "
            "red for false. <bookmark mark='b'/>The grounded sentences settle within a few stages, and settle the "
            "same way in both. <bookmark mark='c'/>The liar flickers, true, false, true, false, for ever, and so do "
            "A and B. <bookmark mark='d'/>The truth-teller keeps whatever value it started with: false on the left, "
            "true on the right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(labs), FadeIn(rl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.01), run_time=3)
            self.play(LaggedStart(*[FadeIn(m) for m in right], lag_ratio=0.01), run_time=3)
            vo.wait_until("b")
            self.play(*[Indicate(VGroup(*[g.cells[(n, j)] for j in range(len(seq))]), color=OK, scale_factor=1.04)
                        for g in (left, right) for n in ("s1", "s3", "s5")])
            vo.wait_until("c")
            for _ in range(2):
                self.play(*[Indicate(VGroup(*[g.cells[(n, j)] for j in range(len(seq))]), color=SELF,
                                     scale_factor=1.06) for g in (left, right) for n in ("L", "A", "B")])
            vo.wait_until("d")
            self.play(*[Indicate(VGroup(*[g.cells[("H", j)] for j in range(len(seq))]), color=GOAL, scale_factor=1.06)
                        for g in (left, right)])
        self.clear_scene()

    def verdicts(self):
        d = load("revision")
        head = label(rf"Over all {d['starts']:,} starting guesses".replace(",", "{,}"), font_size=32,
                     color=CONN).to_edge(UP, buff=0.45)
        groups = {}
        for n, v in d["verdicts"].items():
            groups.setdefault(v, []).append(n)
        rows = VGroup()
        for v, c, desc in (("stably true", OK, r"true from some stage on, \ whatever the start"),
                           ("stably false", BAD, r"false from some stage on, \ whatever the start"),
                           ("depends", GOAL, r"stable, \ but on its starting value"),
                           ("unstable", SELF, r"never settles in some sequence")):
            rows.add(VGroup(label(v, font_size=28, color=c), label(desc, font_size=22, color=GREY_A),
                            label(", ".join(rf"\textbf{{{n}}}" for n in groups.get(v, [])), font_size=24)).arrange(
                RIGHT, buff=0.5))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.3, 0])
        diff = label(r"`the liar is true or not true' \ (\textbf{s8}) \ is stably true: \ unlike Kripke, \ excluded "
                     r"middle survives", font_size=24, color=OK).to_edge(DOWN, buff=0.5)
        assert d["verdicts"]["s8"] == "stably true" and d["verdicts"]["L"] == "unstable"
        with self.voiceover(
            "The Reasoner runs every one of the eight thousand, one hundred and ninety-two starting guesses. "
            "<bookmark mark='a'/>Some sentences are stably true: true from some stage on, whatever the start. Some "
            "are stably false. Some are stable but depend on the start, like the truth-teller. And some never "
            "settle: the liar, the cycle, and 's2 or the liar'. <bookmark mark='b'/>Now look at the sentence 'the "
            "liar is true or not true'. In Kripke's theory it had no value. Here it is stably true, because at "
            "every stage it is a classical instance of excluded middle. Revision theory keeps classical logic, and "
            "pays with a notion of truth that is never finished being revised."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.4), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(diff))
        self.clear_scene()

    def limits(self):
        hc = history_card(1982, r"Hans Herzberger", r"`Notes on naive semantics'", width=5.6, color=HIST).to_corner(
            UL, buff=0.35)
        rows = VGroup(
            label(r"over an infinite language, \ revision runs into the transfinite", font_size=26),
            label(r"at a limit stage $\omega$: \ a sentence that had settled keeps its value", font_size=26, color=GOAL),
            label(r"one that had not: \ Herzberger resets it to false; \ Gupta lets it be anything", font_size=26),
            label(r"every sequence eventually cycles; \ `categorically true' \ = \ stably true in all of them",
                  font_size=26, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.3, 0])
        with self.voiceover(
            "For an infinite language, revision has to continue into the transfinite. <bookmark mark='a'/>What "
            "happens at a limit stage, after infinitely many revisions? <bookmark mark='b'/>A sentence that had "
            "settled keeps its settled value. <bookmark mark='c'/>One that had not settled must be given some "
            "value: Herzberger reset such sentences to false; Gupta allowed any value. <bookmark mark='d'/>Every "
            "revision sequence eventually cycles, and a sentence is categorically true if it is stably true in "
            "every one of them. In our finite world, the Reasoner could check all of them at once."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
