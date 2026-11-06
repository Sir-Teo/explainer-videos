from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Hierarchy(VoiceoverScene):
    def construct(self):
        self.card()
        self.time()
        self.zoo()
        self.savitch()

    def card(self):
        card = chapter_card(2, r"More time, more problems", r"Does extra time always buy extra power?",
                            lit=(1965, 1970), extra=((1965, r"Hartmanis--Stearns"), (1970, r"Savitch")), part=PART)
        with self.voiceover("Chapter two. More time, more problems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def time(self):
        head = label(r"The time hierarchy theorem", font_size=34).to_edge(UP, buff=0.35)
        thm = MathTex(r"\mathrm{TIME}(f(n)) \subsetneq \mathrm{TIME}\big(f(n)\log f(n)\big)", font_size=40,
                      color=HEAD).next_to(head, DOWN, buff=0.35)
        code_lines = [
            "def D(<M>):",
            "    run M on input <M>, with a clock:",
            "        stop after f(n) steps",
            "    if M accepted: reject",
            "    else:          accept",
        ]
        prog = VGroup(*[mono(ln, 22, LAM) for ln in code_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        prog.next_to(thm, DOWN, buff=0.45).to_edge(LEFT, buff=1.2)
        frame = SurroundingRectangle(prog, color=LAM, buff=0.2, corner_radius=0.08)
        lines = VGroup(
            label(r"$D$ runs in time about $f(n) \log f(n)$: \ simulation with a clock", font_size=21, color=WHITE),
            label(r"suppose some $M$ decides the same language in time $f(n)$", font_size=21, color=DATA),
            label(r"run $D$ on $\langle M \rangle$: \ the clock is enough, \ so $D$ does the \textbf{opposite} of "
                  r"$M$", font_size=21, color=NO),
            label(r"so no $f(n)$-time machine decides $D$'s language", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(frame, RIGHT, buff=0.6)
        if lines.get_right()[0] > 6.9:
            lines.width = 6.9 - lines.get_left()[0]
            lines.next_to(frame, RIGHT, buff=0.6)
        cons = label(r"so $\mathrm{P} \subsetneq \mathrm{EXP}$: \ some problems need exponential time, \ provably",
                     font_size=24, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Can we prove that some problems need more time than others? <bookmark mark='a'/> Yes, by Part 1's "
            "diagonal argument with a clock attached. Juris Hartmanis and Richard Stearns proved it in 1965. "
            "<bookmark mark='b'/> Build a machine D. Given the description of a machine M, it runs M on that "
            "description, but stops after f of n steps. If M accepted, D rejects; otherwise it accepts. "
            "<bookmark mark='c'/> Simulating with a clock costs a logarithmic factor, so D runs in a little more "
            "than f of n. <bookmark mark='d'/> Now suppose some machine M decided D's language within f of n "
            "steps. <bookmark mark='e'/> Run D on M's description. The clock gives M enough time, so D finishes "
            "M's computation and does the opposite. <bookmark mark='f'/> They disagree, so no machine that fast "
            "decides it. <bookmark mark='g'/> In particular, P is strictly smaller than exponential time. Some "
            "problems provably need exponential time; we just cannot prove that any NP problem is one of them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(Create(frame), FadeIn(prog))
            for mk, ln in zip("cdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(cons))
        self.wait(0.3)
        self.clear_scene()

    def zoo(self):
        head = label(r"The classes, \ nested", font_size=34).to_edge(UP, buff=0.3)
        names = [("L", YES), ("NL", YES), ("P", DATA), ("NP", HEAD), ("PSPACE", LAM), ("EXP", CTRL),
                 ("EXPSPACE", NO)]
        rings = VGroup()
        for i, (nm, col) in enumerate(names):
            w, h = 1.0 + 0.95 * i, 0.6 + 0.6 * i
            e = Ellipse(width=w, height=h, color=col, stroke_width=2.2).move_to([0, h / 2, 0])
            t = label(nm, font_size=20, color=col).move_to(e.get_top() + DOWN * 0.2)
            rings.add(VGroup(e, t))
        rings.move_to(LEFT * 3.4 + DOWN * 0.4)
        notes = VGroup(
            label(r"$\mathrm{L} \subseteq \mathrm{NL} \subseteq \mathrm{P} \subseteq \mathrm{NP} \subseteq "
                  r"\mathrm{PSPACE} \subseteq \mathrm{EXP}$", font_size=24, color=WHITE),
            label(r"known to be \textbf{different}: \ P $\ne$ EXP, \ NL $\ne$ PSPACE, \ PSPACE $\ne$ EXPSPACE",
                  font_size=21, color=YES),
            label(r"so at least one $\subseteq$ in each pair is strict, \\ but nobody knows \textbf{which}",
                  font_size=21, color=NO),
            label(r"space can be reused; \ time cannot: \\ time $t$ needs space $\le t$, \ space $s$ needs time "
                  r"$\le 2^{O(s)}$", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        if notes.width > 6.3:
            notes.width = 6.3
            notes.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here is the map of the classes this part needs. <bookmark mark='a'/> Logarithmic space, its "
            "nondeterministic version, polynomial time, NP, polynomial space, exponential time, exponential space. "
            "Each sits inside the next. <bookmark mark='b'/> The hierarchy theorems prove that some of these are "
            "different. P is not exponential time; logarithmic space is not polynomial space. <bookmark "
            "mark='c'/> So between P and exponential time at least one inclusion is strict, but nobody knows which. "
            "Every one of them might be strict. <bookmark mark='d'/> Space behaves differently from time because "
            "it can be reused. A machine that runs for t steps can visit at most t cells, and a machine using s "
            "cells has at most exponentially many configurations in s, so it either halts within that many steps "
            "or loops forever."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rings], lag_ratio=0.2), FadeIn(notes[0]), run_time=2.5)
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def savitch(self):
        s = load("savitch")
        head = label(r"Savitch \ (1970): \ $\mathrm{NSPACE}(s) \subseteq \mathrm{SPACE}(s^2)$", font_size=32).to_edge(
            UP, buff=0.35)
        code_lines = [
            "def can_yield(a, b, t):    # reach b from a in <= t steps?",
            "    if t <= 1: return a == b or step(a, b)",
            "    for m in all_configurations():",
            "        if can_yield(a, m, t/2) and can_yield(m, b, t/2):",
            "            return True",
            "    return False",
        ]
        prog = VGroup(*[mono(ln, 19, LAM) for ln in code_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        prog.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        frame = SurroundingRectangle(prog, color=LAM, buff=0.18, corner_radius=0.08)
        rows = [[str(r["n"]), words(r["calls"]), str(r["depth"])] for r in s["rows"]]
        tab = grid_table([r"path of $n$ nodes", r"calls", r"recursion depth"], rows, widths=[2.6, 2.0, 2.6],
                         row_h=0.42, font_size=20, mono_cols=(), colors=[[WHITE, NO, YES]] * len(rows))
        tab.next_to(frame, DOWN, buff=0.4).to_edge(LEFT, buff=0.9)
        notes = VGroup(
            label(r"\textbf{depth}: \ $t$ halves each level, \ so $\log_2 t$ levels", font_size=21, color=YES),
            label(r"\textbf{each level} remembers $a, b, m$: \ $O(s)$ cells", font_size=21, color=DATA),
            label(r"a nondeterministic machine in space $s$ has $2^{O(s)}$ configurations: \\ $t = 2^{O(s)}$, \ so "
                  r"space $O(s) \cdot O(s) = O(s^2)$", font_size=21, color=HEAD),
            label(rf"the time explodes \ ({words(s['rows'][-1]['calls'])} calls for {s['rows'][-1]['n']} nodes); \\ space "
                  r"is what we saved", font_size=21,
                  color=NO),
            label(r"so $\mathrm{PSPACE} = \mathrm{NPSPACE}$: \\ for space, \ guessing is free", font_size=23,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        if notes.get_right()[0] > 6.9:
            notes.width = 6.9 - notes.get_left()[0]
            notes.next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        with self.voiceover(
            "For space, nondeterminism can be removed at a modest price. <bookmark mark='a'/> Walter Savitch, 1970. "
            "To decide whether a configuration b can be reached from a in t steps, try every possible midpoint m, "
            "and ask recursively whether m can be reached from a in half the time, and b from m. <bookmark "
            "mark='b'/> We ran it on paths of four, eight and sixteen nodes. The recursion depth grows by one each "
            "time n doubles. <bookmark mark='c'/> Each level of recursion only remembers three configurations, "
            "<bookmark mark='d'/> and a nondeterministic machine using space s has exponentially many "
            "configurations in s, so the depth is order s, and the total space order s squared. <bookmark "
            "mark='e'/> Time is another matter: forty-seven thousand calls for sixteen nodes, growing faster than any "
            "polynomial. Savitch saves space, not time. <bookmark mark='f'/> The consequence: polynomial space with "
            "guessing equals polynomial space without it. Whether the same holds for time is the question of this "
            "part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(frame), FadeIn(prog))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(notes[0]))
            for mk, n_ in zip("cdef", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
