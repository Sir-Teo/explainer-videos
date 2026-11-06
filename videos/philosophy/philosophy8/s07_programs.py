from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Programs(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"The liar as a program", r"What does a computer make of the liar?",
                            part=PART)
        with self.voiceover("Chapter six. The liar as a program."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.code()
        self.runs()
        self.semantics()

    def code(self):
        head = label(r"Every sentence, \ a little recursive function", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        lines = ["def s1():  return True              # snow is white",
                 "def s3():  return s1()              # 's1' is true",
                 "def s9():  return s1() or L()       # 's1' or the liar",
                 "def L():   return not L()           # the liar",
                 "def H():   return H()               # the truth-teller"]
        code = code_block(lines, font_size=24, color=GREY_A)
        box = SurroundingRectangle(code, buff=0.35, corner_radius=0.12, stroke_color=GREY_C, stroke_width=2,
                                   fill_color="#0F141C", fill_opacity=1)
        prog = VGroup(box, code).move_to([0, 0.5, 0])
        note = label(r"`is true' becomes a call: \ to ask whether $A$ is true, \ run $A$", font_size=26,
                     color=GOAL).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "There is another way to see Kripke's construction, which any programmer will recognise. "
            "<bookmark mark='a'/>Turn each sentence into a little function. Snow is white returns true. ''s1' is "
            "true' calls s1. ''s1' or the liar' calls s1, or else the liar. The liar returns the opposite of "
            "itself. The truth-teller returns itself. <bookmark mark='b'/>Asking whether a sentence is true becomes "
            "running it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(box), LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.1) for l_ in code], lag_ratio=0.4),
                      run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.clear_scene()

    def runs(self):
        d = load("programs")
        head = label(r"The Reasoner runs the sentences as programs", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        hd = [label(r"sentence", font_size=22, color=P.CLAIM), label(r"run as a program", font_size=22,
                                                                      color=P.CLAIM),
              label(r"Kripke's least fixed point", font_size=22, color=P.CLAIM)]
        names = ["s1", "s2", "s3", "s5", "s9", "s10", "L", "H", "A"]
        rows = []
        for n in names:
            r = d["runs"][n]
            rows.append([label(rf"\textbf{{{n}}}: \ {Tr.GLOSS[n].replace('‘', '`').replace('’', chr(39))}",
                               font_size=20),
                         label(r"never returns" if r == "never returns" else r, font_size=21,
                               color=SELF if r == "never returns" else (OK if r == "true" else BAD)),
                         value_chip(d["lfp"][n], 20)])
        grid = ValueGrid(hd, rows, col_w=[5.0, 3.4, 3.6], cell_h=0.46, font_size=21).move_to([0, -0.35, 0])
        assert all((d["runs"][n] == "never returns") == (d["lfp"][n] == "n") for n in d["lfp"])
        with self.voiceover(
            "The Reasoner turns every sentence of the small world into a program and runs it, with a limit on how "
            "deep the calls may go. <bookmark mark='a'/>The grounded sentences return true or false. The liar never "
            "returns: it calls itself for ever. So does the truth-teller, and the cycle, and every sentence that "
            "depends on them. <bookmark mark='b'/>Put the results beside Kripke's least fixed point, and they "
            "match exactly. Neither true nor false, for a sentence, is never returning, for a program. Ungrounded "
            "means non-terminating."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][1]) for r in range(len(rows))], lag_ratio=0.25), run_time=4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][2], scale=0.7) for r in range(len(rows))], lag_ratio=0.2))
        self.clear_scene()

    def semantics(self):
        hcs = VGroup(history_card(1955, r"Alfred Tarski", r"every monotone map on a complete lattice has a least "
                                  r"fixed point", width=5.8, color=HIST),
                     history_card(1969, r"Dana Scott", r"the meaning of a recursive program is a least fixed point",
                                  width=5.8, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"Kripke's `neither' \ is the computer scientist's $\bot$, \ `undefined'", font_size=26, color=GOAL),
            label(r"strong Kleene `or' is \textit{parallel} or: \ true if either side is, \ even if the other never "
                  r"returns", font_size=24),
            label(r"Python's \texttt{or} is sequential: \ `the liar or $s_1$' would loop \ (a weaker logic: \ "
                  r"McCarthy's)", font_size=24, color=GREY_A),
            label(r"the same mathematics gives meaning to recursion, \ and to truth", font_size=26,
                  color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(hcs, DOWN, buff=0.5)
        with self.voiceover(
            "This is no accident. <bookmark mark='a'/>Kripke's 'neither' is what computer scientists write as "
            "bottom, 'undefined'. In 1969 Dana Scott gave recursive programs their meaning as least fixed points, "
            "using the theorem, proved in general by Tarski in 1955, that every monotone map on a complete lattice "
            "has one. Kripke's construction is the same theorem, applied to truth. <bookmark mark='b'/>There is "
            "one subtlety. The strong Kleene 'or' is true if either side is true, even if the other side never "
            "returns: a parallel 'or'. <bookmark mark='c'/>Python's 'or' is sequential, so 'the liar or s1' would "
            "loop for ever, even though s1 is true. That matches a weaker three-valued logic, due to John McCarthy. "
            "<bookmark mark='d'/>The same mathematics gives meaning to recursion and to truth."
        ) as vo:
            self.play(FadeIn(hcs))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
