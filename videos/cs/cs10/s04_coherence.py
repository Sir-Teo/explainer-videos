from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, STATE_COLOR, STATE_NAME, YES,
                                   CacheLine, core_box, load)


class Coherence(WatchScene):
    def construct(self):
        self.card()
        self.problem()
        self.rules()
        self.diagram()

    def card(self):
        self.chapter(3, r"Cache coherence", r"What if two caches disagree about one address?", lit=(1984,), extra=((1984, r"Papamarcos and Patel: \ MESI"),), part=PART, said="Chapter three. Cache coherence.")

    # ------------------------------------------------------------------
    def problem(self):
        self.ask(r"Two cores have cached $x = 0$. Core 0 writes $x = 1$. \\ With no coherence, core 1 reads...",
                 [r"1", r"0, from its stale copy"], 1,
                 say="Two cores have x, zero, in their caches. Core zero writes one. Without coherence, what does core one read?",
                 reveal="Zero, from its stale copy. Coherence exists to stop exactly that.")
        head = label(r"Without coherence: \ two stale private copies", font_size=34).to_edge(UP, buff=0.35)
        c0 = core_box(0).move_to(LEFT * 3 + UP * 1.4)
        c1 = core_box(1).move_to(RIGHT * 3 + UP * 1.4)
        mem = VGroup(RoundedRectangle(width=3.2, height=0.7, corner_radius=0.08, stroke_color=GREY_B),
                     Text("memory:  x = 0", font="DejaVu Sans Mono", font_size=20, color=WHITE)).move_to(DOWN * 2.2)
        mem[1].move_to(mem[0])

        def cachebox(core):
            b = RoundedRectangle(width=2.2, height=0.6, corner_radius=0.06, stroke_color=GREY_C).next_to(core, DOWN,
                                                                                                       buff=0.5)
            return b

        b0, b1 = cachebox(c0), cachebox(c1)
        v0 = Text("x = 0", font="DejaVu Sans Mono", font_size=20, color=WHITE).move_to(b0)
        v1 = Text("x = 0", font="DejaVu Sans Mono", font_size=20, color=WHITE).move_to(b1)
        lines = VGroup(Line(b0.get_bottom(), mem[0].get_top() + LEFT * 0.8, color=GREY_D),
                       Line(b1.get_bottom(), mem[0].get_top() + RIGHT * 0.8, color=GREY_D))
        steps = VGroup(
            label(r"1. \ both cores read $x$: \ each cache keeps a copy", font_size=22, color=GREY_A),
            label(r"2. \ core 0 writes $x = 1$: \ into its own cache \ (write-back)", font_size=22, color=DATA),
            label(r"3. \ core 1 reads $x$ again: \ a hit, \ and the old value 0", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(head, DOWN, buff=0.15)
        v0n = Text("x = 1", font="DejaVu Sans Mono", font_size=20, color=DATA).move_to(b0)
        with self.voiceover(
            (
            "First imagine private caches without a working coherence protocol. Two cores, each with a private "
            "cache, and one variable x in memory, holding zero. <bookmark mark='a'/> Both cores read x. Each "
            "cache now keeps its own copy. <bookmark mark='b'/> Core zero writes one to x. With a write-back "
            "cache, the new value goes into core zero's cache, and memory still says zero. <bookmark mark='c'/> "
            "Now core one reads x again. It finds x in its own cache, a hit, and gets zero: a value that was "
            "overwritten some time ago. If x were a flag saying the data is ready, a cached stale copy could "
            "prevent progress. This deliberately broken example does not describe correctly synchronized code on "
            "a coherent machine. Caches made private copies of a shared memory, and the copies have come apart."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(c0), FadeIn(c1), FadeIn(b0), FadeIn(b1), Create(lines), FadeIn(mem))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(v0, shift=UP * 0.3), FadeIn(v1, shift=UP * 0.3))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), Transform(v0, v0n), Indicate(b0, color=DATA))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), Indicate(b1, color=NO), v1.animate.set_color(NO))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        head = label(r"What coherence promises", font_size=36).to_edge(UP, buff=0.35)
        rules = VGroup(
            label(r"\textit{single writer, \ or many readers}: \ at any moment, \ for each line, \ either one cache may "
                  r"write it, \ or any number may read it", font_size=23, color=DATA),
            label(r"\textit{coherent order}: \ reads respect the per-address write order and required synchronization",
                  font_size=23, color=YES),
            label(r"to keep the first, \ a cache must hear what the others do: \ \textit{snooping} on a shared bus, \ "
                  r"or a \textit{directory}", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.2)
        cite = note(r"the invariants as Sorin, \ Hill and Wood state them, \ \textit{A Primer on Memory Consistency "
                    r"and Cache Coherence}", font_size=18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "A coherence protocol makes the copies behave as if there were only one. It keeps two promises. "
            "<bookmark mark='a'/> The first: at any moment, for each cache line, either a single cache is allowed "
            "to write it, or any number of caches may read it, but never both. <bookmark mark='b'/> The second: "
            "writes to one address have a coherent order, and reads respect that order and the required "
            "synchronization. Our sequential simulator returns the last completed write. This does not impose a "
            "single order across different addresses. <bookmark mark='c'/> To keep them, every cache must learn "
            "what the others are doing to the lines it holds. On a small chip every cache can watch, or snoop on, "
            "a shared bus that carries every miss. On a big one, a directory keeps track of who holds what."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite), run_time=0.5)
            for mk, r in zip('abc', rules):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.6 if mk == 'a' else 1.0)
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diagram(self):
        head = label(r"MESI: \ four states for every line in every cache", font_size=32).to_edge(UP, buff=0.3)
        pos = {"I": (-4.0, 0.0), "E": (0.0, 1.7), "S": (0.0, -1.7), "M": (4.0, 0.0)}
        edges = [("I", "E", "read, no one else has it", 0), ("I", "S", "read, others have it", -0.3),
                 ("I", "M", "write", 0), ("E", "M", "write (silently)", 0), ("S", "M", "write: invalidate others", 0.3),
                 ("M", "S", "another core reads", 0.3), ("E", "S", "-", 0),
                 ("S", "I", "another core writes", -0.3)]
        sd = StateDiagram(pos, edges, radius=0.5, font_size=30, edge_font=15).shift(DOWN * 0.3)
        for k, (_, _, text, _) in enumerate(edges):  # translatable labels in place of the verbatim ones
            old = sd.edge[k][1]
            sd.edge[k].remove(old)
            if text != "-":
                sd.edge[k].add(label(text, font_size=17, color=GREY_A).move_to(old))
        for name in pos:
            sd.node[name].circle.set_stroke(STATE_COLOR[name]).set_fill(STATE_COLOR[name], 0.15)
        local = [0, 1, 2, 3, 4]
        snoop = [5, 6, 7]
        for k in snoop:
            for part in sd.edge[k]:
                part.set_color(FUNC)
        names = VGroup(*[label(rf"\textbf{{{s}}}{STATE_NAME[s][1:]}", font_size=20, color=STATE_COLOR[s]).next_to(
            sd.node[s], LEFT if pos[s][0] < 0 else RIGHT, buff=0.15) for s in pos])
        mean = VGroup(
            label(r"M: \ dirty, \ the only copy", font_size=19, color=STATE_COLOR["M"]),
            label(r"E: \ clean, \ the only copy", font_size=19, color=STATE_COLOR["E"]),
            label(r"S: \ clean, \ maybe other copies", font_size=19, color=STATE_COLOR["S"]),
            label(r"I: \ not here", font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.35)
        leg = VGroup(label(r"grey: \ this core's own reads and writes", font_size=18, color=GREY_B),
                     label(r"green: \ what it sees other cores do on the bus", font_size=18, color=FUNC)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.35)
        also = note(r"also: \ E $\to$ S when another core reads; \\ M or E $\to$ I when another core writes",
                    font_size=16).next_to(leg, UP, buff=0.15)
        with self.voiceover(
            "The protocol inside most multicore chips descends from MESI, published by Mark Papamarcos and Janak "
            "Patel in 1984. Each line in each cache is in one of four states. <bookmark mark='a'/> Modified: this "
            "cache has the only copy, and it is newer than memory. Exclusive: the only copy, but clean. Shared: "
            "clean, and other caches may have it too. Invalid: not here at all. <bookmark mark='b'/> Now the "
            "transitions for this core's own accesses. A read miss asks the bus: if no one else has the line, it "
            "arrives Exclusive; if others do, Shared. A write needs the only copy: from Invalid, a read for ownership; "
            "from Shared, an invalidation of every other copy; and from Exclusive, nothing at all. That silent "
            "upgrade is why E exists: most data is private, and a private line can be written without asking anyone. "
            "<bookmark mark='c'/> And the transitions forced by other cores. When another core reads a line this "
            "cache holds Modified, this cache supplies the data and both end Shared. When another core writes, every "
            "other copy becomes Invalid."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd.nodes))
            vo.wait_until("a")
            self.play(FadeIn(names), FadeIn(mean))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(sd.edge[k]) for k in local], lag_ratio=0.5), FadeIn(leg[0]), run_time=4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(sd.edge[k]) for k in snoop], lag_ratio=0.5), FadeIn(leg[1]),
                      FadeIn(also), run_time=3)
        self.wait(0.3)
        self.clear_scene()


