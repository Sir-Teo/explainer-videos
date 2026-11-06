from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, module_box)


class Parnas(VoiceoverScene):
    def construct(self):
        self.card()
        self.complexity()
        self.two_ways()
        self.changes()
        self.rule()

    def card(self):
        card = chapter_card(1, r"Complexity, \ and Parnas' rule", r"How should a program be divided into modules?",
                            lit=(1972, 1986), extra=((1972, r"Parnas: \ On the Criteria"),
                                                     (1986, r"Brooks: \ No Silver Bullet")), part=PART)
        with self.voiceover("Chapter one. Complexity, and Parnas' rule."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def complexity(self):
        head = label(r"No silver bullet", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{essential} complexity: \ in the problem itself \ (the tax code, \ the protocol, \ "
                          r"the physics); \ no tool removes it", 12.4, font_size=25, color=HEAD),
            wrapped_label(r"\textbf{accidental} complexity: \ in how we build it \ (memory management by hand, \ slow "
                          r"builds, \ tangled code); \ tools and languages have removed much of it", 12.4,
                          font_size=25, color=DATA),
            wrapped_label(r"Brooks \ (1986): \ once the accidental part is small, \ no single technique can give an "
                          r"order-of-magnitude gain in a decade", 12.4, font_size=25, color=NO),
            wrapped_label(r"what remains is managing the essential complexity: \ dividing a system so each part can be "
                          r"understood, \ built and changed on its own", 12.4, font_size=25, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Eighteen years after Garmisch, Brooks wrote an essay called No Silver Bullet. He split the difficulty "
            "of software in two. <bookmark mark='a'/> Essential complexity lives in the problem itself: the tax "
            "code, the network protocol, the physics being simulated. No tool removes it. <bookmark mark='b'/> "
            "Accidental complexity lives in how we build: managing memory by hand, waiting for slow builds, "
            "untangling code. High-level languages, Part 13's compilers and Part 15's garbage collectors removed a "
            "great deal of it. <bookmark mark='c'/> Brooks argued that once the accidental part is small, no single "
            "technique can deliver a tenfold gain within a decade. <bookmark mark='d'/> What remains is the "
            "essential complexity, and the main tool for it is division: splitting a system into parts that can "
            "each be understood, built and changed on their own. But split along which lines?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def _d1(self):
        names = ["Input", "Circular Shift", "Alphabetizer", "Output"]
        mods = VGroup(*[module_box(n, DATA, w=1.85, font=17) for n in names]).arrange(RIGHT, buff=0.22)
        master = module_box("Master", GREY_B, w=1.6, font=17)
        data = module_box(r"shared data: \ words, \ line starts, \ shifts", NO, w=7.6, h=0.6, font=16)
        master.next_to(mods, UP, buff=0.55)
        data.next_to(mods, DOWN, buff=0.7)
        arrows = VGroup(*[Line(m.get_bottom(), [m.get_x(), data.get_top()[1], 0], color=NO, stroke_width=2.5)
                          for m in mods])
        calls = VGroup(*[Line(master.get_bottom(), m.get_top(), color=GREY_C, stroke_width=1.5) for m in mods])
        g = VGroup(calls, arrows, master, mods, data)
        g.mods = {n: m for n, m in zip(names, mods)}
        return g

    def _d2(self):
        inp = module_box("Input", DATA, w=1.6, font=17)
        sh = module_box("Circular Shifter", YES, w=2.1, font=17)
        al = module_box("Alphabetizer", YES, w=1.85, font=17)
        out = module_box("Output", DATA, w=1.6, font=17)
        row = VGroup(inp, sh, al, out).arrange(RIGHT, buff=0.45)
        master = module_box("Master", GREY_B, w=1.6, font=17).next_to(row, UP, buff=0.55)
        st = module_box("Line Storage", YES, w=2.6, font=17).next_to(row, DOWN, buff=0.7)
        st.set_x((inp.get_x() + sh.get_x()) / 2)

        def uses(a, b, start=None, end=None):
            return Arrow(start if start is not None else a.get_bottom(), end if end is not None else b.get_top(),
                         buff=0.06, stroke_width=2.5, color=GREY_B, max_tip_length_to_length_ratio=0.15)
        arrows = VGroup(uses(inp, st, end=st.get_top() + LEFT * 0.5), uses(sh, st, end=st.get_top() + RIGHT * 0.5),
                        uses(al, sh, start=al.get_left(), end=sh.get_right()),
                        uses(out, al, start=out.get_left(), end=al.get_right()),
                        CurvedArrow(out.get_bottom() + LEFT * 0.2, sh.get_bottom() + RIGHT * 0.3, angle=-0.9,
                                    color=GREY_B, stroke_width=2))
        calls = VGroup(*[Line(master.get_bottom(), m.get_top(), color=GREY_C, stroke_width=1.5) for m in row])
        g = VGroup(calls, arrows, master, row, st)
        g.mods = {"Line Storage": st, "Input": inp, "Circular Shifter": sh, "Alphabetizer": al, "Output": out}
        return g

    def two_ways(self):
        k = load("kwic")
        head = label(r"KWIC, \ built twice", font_size=36).to_edge(UP, buff=0.3)
        sample = code_block(k["index"][:6], size=16).to_corner(UL, buff=0.5).shift(DOWN * 0.6)
        sl = label(r"a keyword-in-context index: \ every circular shift of every title, \ sorted", font_size=19,
                   color=GREY_A).next_to(sample, UP, buff=0.15).align_to(sample, LEFT)
        d1 = self._d1().scale(0.78).move_to([-3.55, -1.0, 0])
        d2 = self._d2().scale(0.78).move_to([3.55, -1.0, 0])
        l1 = label(r"1. \ the flowchart: \ one module per step", font_size=21, color=NO).next_to(d1, UP, buff=0.3)
        l2 = label(r"2. \ one module per design decision", font_size=21, color=YES).next_to(d2, UP, buff=0.3)
        with self.voiceover(
            "In 1972 David Parnas answered with an experiment on paper, and we will run it for real. "
            "<bookmark mark='a'/> The program is a keyword-in-context index: take a list of titles, form every "
            "circular shift of each one, and print them all in alphabetical order, so that every word can be looked "
            "up in context. <bookmark mark='b'/> The obvious decomposition follows the flowchart: one module per "
            "processing step, input, shifting, sorting, output, all reading and writing shared tables of words and "
            "positions. <bookmark mark='c'/> Parnas' decomposition looks almost the same but cuts differently. One "
            "module, line storage, owns how lines are stored, and nobody else knows. Another owns how a circular "
            "shift is represented; another, when and how sorting happens. We wrote both, in this repository, and "
            "they produce the same thirty-one lines."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sl), FadeIn(sample))
            vo.wait_until("b")
            self.play(FadeOut(sample), FadeOut(sl), FadeIn(l1), FadeIn(d1))
            vo.wait_until("c")
            self.play(FadeIn(l2), FadeIn(d2))
        self.wait(0.3)
        self.d1, self.d2, self.heads = d1, d2, VGroup(head, l1, l2)

    def changes(self):
        k = load("kwic")
        d1, d2 = self.d1, self.d2
        r0 = k["rows"][0]
        lit1 = [d1.mods[m][0].animate.set_fill(NO, 0.55) for m in r0["d1"]["modules"]]
        lit2 = [d2.mods[m][0].animate.set_fill(NO, 0.55) for m in r0["d2"]["modules"]]
        cap = label(r"change: \ store each word as a number in a vocabulary", font_size=22, color=HEAD).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Now change one design decision, as Parnas did. <bookmark mark='a'/> Store each word as a number in a "
            "vocabulary, to save memory. <bookmark mark='b'/> In the flowchart design, three of the five modules "
            "read the word tables directly, so all three must be rewritten, sixteen lines in all. "
            "<bookmark mark='c'/> In Parnas' design, one module changes: line storage, nine lines. Nobody else knew "
            "how words were stored."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(*lit1)
            vo.wait_until("c")
            self.play(*lit2)
        self.wait(0.4)
        self.clear_scene()
        head = label(r"Four changes, \ both designs, \ every output checked", font_size=34).to_edge(UP, buff=0.3)
        rows = []
        for r in k["rows"]:
            rows.append([r["change"], rf"{r['d1']['n']} of {r['d1']['of']}", f"{r['d1']['lines']}",
                         rf"{r['d2']['n']} of {r['d2']['of']}", f"{r['d2']['lines']}",
                         r"yes" if r["d1"]["same_output"] and r["d2"]["same_output"] else r"no"])
        tab = grid_table([r"change", r"flowchart: \ modules", r"lines", r"Parnas: \ modules", r"lines",
                          r"same index"], rows, widths=[3.8, 2.3, 1.1, 2.2, 1.1, 1.7], row_h=0.5, font_size=21,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for i in range(1, len(rows) + 1):
            tab.cells[i][1].set_color(NO if k["rows"][i - 1]["d1"]["n"] > 1 else WHITE)
            tab.cells[i][3].set_color(YES)
        foot = wrapped_label(r"the input format is a decision both designs hid in one module, \ so both change in one "
                             r"place; \ every decision the flowchart exposed in its shared tables costs two or three "
                             r"modules", 12.4, font_size=21, color=WHITE).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "We made four of Parnas' changes to both programs and checked every variant against the original index. "
            "<bookmark mark='a'/> Changing the input format touches one module in both designs, because both kept "
            "reading input in one place. Storing shifts in full instead of as positions: three modules against one. "
            "Sorting on demand instead of all at once: two against one. <bookmark mark='b'/> Each time, the cost of a "
            "change is the number of modules that knew about the decision being changed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def rule(self):
        head = label(r"Information hiding", font_size=36).to_edge(UP, buff=0.3)
        quote = wrapped_label(r"``We propose instead that one begins with a list of difficult design decisions or "
                              r"design decisions which are likely to change. \ Each module is then designed to hide "
                              r"such a decision from the others.'' \ --- \ Parnas, 1972", 12.0, font_size=25,
                              color=HEAD).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            wrapped_label(r"an \textbf{interface} is what a module promises; \ its \textbf{secret} is everything else",
                          12.4, font_size=24, color=WHITE),
            wrapped_label(r"\textbf{deep modules} \ (Ousterhout, 2018): \ a small interface over a lot of "
                          r"functionality, \ like Unix's five-call file API over Part 34's whole file system", 12.4,
                          font_size=24, color=YES),
            wrapped_label(r"the rest of this part is variations on this theme: \ contracts state the interface, \ "
                          r"coupling measures how much leaks, \ tests pin it down", 12.4, font_size=24, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(quote, DOWN, buff=0.55)
        with self.voiceover(
            "Parnas stated the principle in one sentence. <bookmark mark='a'/> Begin with a list of difficult design "
            "decisions, or decisions likely to change, and design each module to hide one of them from the others. "
            "<bookmark mark='b'/> What a module promises is its interface; everything else is its secret. "
            "<bookmark mark='c'/> John Ousterhout calls the best modules deep: a small interface over a lot of "
            "functionality, like the handful of Unix calls, open, read, write, seek and close, in front of the whole "
            "file system of Part 34. <bookmark mark='d'/> Most of this part is variations on Parnas: contracts state "
            "the interface precisely, coupling measures how much leaks through it, and tests pin it down."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote))
            for mk, l in zip("bcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
