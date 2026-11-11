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
        thm = MathTex('f\\log f=o(g)\\ \\Longrightarrow\\ \\mathrm{TIME}(f)\\subsetneq\\mathrm{TIME}(g)', font_size=40,
                      color=HEAD).next_to(head, DOWN, buff=0.35)
        code_lines = ['def D(x):  # padded machine description', '    M = decode_prefix(x)', '    simulate M(x) with a chosen clock', '    reject if M accepted; else accept']
        prog = VGroup(*[mono(ln, 22, LAM) for ln in code_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        prog.next_to(thm, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        frame = SurroundingRectangle(prog, color=LAM, buff=0.2, corner_radius=0.08)
        lines = VGroup(
            label('constructible $f,g\\ge n$; \\\\ deterministic multitape model; \\\\ clock fits $g$ after overhead', font_size=21, color=WHITE),
            label('suppose a decider uses $O(f(n))$ time \\\\ choose an arbitrarily long padded description', font_size=21, color=DATA),
            label('past its constants and finite exceptions, \\\\ the simulation completes and reverses the answer', font_size=21, color=NO),
            label('contradiction: the diagonal language \\\\ lies in TIME$(g)$ and outside TIME$(f)$', font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(frame, RIGHT, buff=0.6)
        if lines.get_right()[0] > 6.9:
            lines.width = 6.9 - lines.get_left()[0]
            lines.next_to(frame, RIGHT, buff=0.6)
        lines.align_to(frame, UP)
        cons = label('$\\mathrm{P}\\subsetneq\\mathrm{EXP}$: some EXP languages are outside P; no P/NP separation follows',
                     font_size=24, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Can extra time provably add power? <bookmark mark='a'/> Yes. In a standard deterministic multitape model, for constructible bounds f and g at least n, f times log f being little-o of g gives a strict inclusion from TIME f to TIME g. The gap condition matters. <bookmark mark='b'/> Here is the diagonal idea, with technical clock choices suppressed. Decode a machine from a padded input, simulate that machine on the entire input, and reverse acceptance after a clock expires. <bookmark mark='c'/> Choose the clock so simulation fits the larger budget while eventually exceeding every fixed constant times the smaller one. <bookmark mark='d'/> Suppose a smaller-time decider recognized this diagonal language. <bookmark mark='e'/> It has arbitrarily long padded descriptions, so choose one beyond its runtime constants and finite exceptions. On that input the simulation finishes and reverses its answer. <bookmark mark='f'/> That contradiction proves a separation. Padding and overhead are essential parts of the theorem, not optional details. <bookmark mark='g'/> One consequence is P strictly contained in EXP. This does not separate P from NP."
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
            label('with read-only input and $s\\ge\\log n$: \\\\ space $s$ gives $2^{O(s)}$ configurations', font_size=21, color=GREY_A),
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
        head = label('Savitch (1970): $\\mathrm{NSPACE}(s)\\subseteq\\mathrm{SPACE}(s^2)$, $s\\ge\\log n$', font_size=32).to_edge(
            UP, buff=0.35)
        code_lines = ['def can_yield(a, b, t):', '    if t == 0: return a == b', '    if t == 1: return a == b or step(a, b)', '    h = (t + 1) // 2', '    for m in all_configurations():', '        if can_yield(a,m,h) and can_yield(m,b,t-h):', '            return True', '    return False']
        prog = VGroup(*[mono(ln, 16, LAM) for ln in code_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        prog.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        frame = SurroundingRectangle(prog, color=LAM, buff=0.18, corner_radius=0.08)
        rows = [[str(r["n"]), words(r["calls"]), str(r["depth"])] for r in s["rows"]]
        tab = grid_table([r"path of $n$ nodes", r"calls", r"recursion depth"], rows, widths=[2.6, 2.0, 2.6],
                         row_h=0.42, font_size=20, mono_cols=(), colors=[[WHITE, NO, YES]] * len(rows))
        tab.next_to(frame, DOWN, buff=0.4).to_edge(LEFT, buff=0.9)
        notes = VGroup(
            label(r"\textbf{depth}: \ $t$ halves each level, \ so $\log_2 t$ levels", font_size=21, color=YES),
            label('each theoretical frame: $O(s)$ bits; \\\\ displayed three-slot count excludes graph/Python storage', font_size=21, color=DATA),
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
            "Savitch's theorem removes nondeterminism at a space cost. <bookmark mark='a'/> For a suitable space bound s at least log n, nondeterministic space s is contained in deterministic space of order s squared. To test reachability within t edges, use zero edges for equality, one for an edge or equality, and otherwise try every midpoint with integer half-budgets. <bookmark mark='b'/> Our path examples measure actual recursive calls and depths. <bookmark mark='c'/> A theoretical recursive frame stores only a constant number of configurations, the midpoint iterator and a budget. The displayed three-slot count is illustrative, excluding the already stored graph and Python overhead. <bookmark mark='d'/> With a read-only input and s at least log n, the configuration count is exponential in s. Logarithmically many recursive levels therefore use order s squared space. <bookmark mark='e'/> Time can be very large; these finite path counts illustrate that cost without proving a growth law. <bookmark mark='f'/> Consequently PSPACE equals NPSPACE. The analogous polynomial-time question is still open."
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
