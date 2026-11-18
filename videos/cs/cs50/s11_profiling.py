from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, mono

FLAME = (KERN, HEAD, NO, "#E8A33D", "#D9663A", "#C9503A")


def flame_graph(frames, x0=-6.3, width=12.6, base=-2.9, row_h=0.56, size=17, names=None):
    """Frames of a flame graph ({name, x, w, depth, path}) as rectangles stacked from ``base`` upwards; a frame wide
    enough is labelled.  Returns the group with ``.boxes`` (by path) and ``.depths`` (one VGroup per depth)."""
    g = VGroup()
    g.boxes = {}
    depth_max = max(f["depth"] for f in frames)
    g.depths = [VGroup() for _ in range(depth_max + 1)]
    for i, f in enumerate(frames):
        w = max(0.02, f["w"] * width - 0.03)
        col = FLAME[(sum(map(ord, f["name"])) + f["depth"]) % len(FLAME)]
        r = Rectangle(width=w, height=row_h - 0.05, stroke_color=BG, stroke_width=1, fill_color=col,
                      fill_opacity=0.9)
        r.move_to([x0 + f["x"] * width + w / 2 + 0.015, base + row_h * (f["depth"] + 0.5), 0])
        cell = VGroup(r)
        nm = (names or {}).get(f["name"], f["name"])
        t = label(rf"\texttt{{{nm}}}", font_size=size, color=BLACK) if nm else None
        if t is not None and t.width < w - 0.12:
            t.move_to(r)
            cell.add(t)
        g.boxes[f["path"]] = cell
        g.depths[f["depth"]].add(cell)
        g.add(cell)
    return g


class Profiling(WatchScene):
    def construct(self):
        self.card()
        self.sampling()
        self.flame()
        self.offcpu()

    def card(self):
        self.chapter(10, r"Profiling and flame graphs", r"Where does the time go?", lit=(2011,), extra=((2011, r"Gregg: \ flame graphs"),), part=PART, said="Chapter ten. Profiling: finding where the time goes, and drawing it as a flame graph.")

    def sampling(self):
        p = load("profile")
        head = label(r"A sampling profiler", font_size=36).to_edge(UP, buff=0.3)
        # the instruction stream: every interval-th instruction is sampled
        strip = VGroup(*[Line([-6.4 + 0.08 * k, 2.25, 0], [-6.4 + 0.08 * k, 2.55, 0], color=GREY_D, stroke_width=1.5)
                         for k in range(161)])
        hits = VGroup(*[strip[k] for k in range(9, 161, 19)])
        strip_l = wrapped_label(rf"Pebble runs the Job on {p['bytes']:,} bytes of a novel: \ {p['instructions']:,} "
                        rf"instructions; \ every {p['interval']}th, \ the profiler reads the program counter",
                                12.6, font_size=19, color=GREY_A).next_to(strip, DOWN, buff=0.15)
        code = code_block(["scan: beq  a2, s1, insert", "      lw   t1, 4(t0)", "      bne  t1, a1, next",
                           "      ...", "cmp:  beq  a3, a1, found", "      ...", "      bne  a4, a5, next",
                           "      addi a3, a3, 1", "      j    cmp", "next: addi t0, t0, 12",
                           "      addi a2, a2, 1", "      j    scan"], size=18)
        code.move_to([-4.3, -1.0, 0]).to_edge(LEFT, buff=0.9)
        frame = SurroundingRectangle(code, color=GREY_C, buff=0.18, corner_radius=0.08, stroke_width=1.5)
        title = label(r"the Job's \texttt{word} routine: \ look the word up in the table", font_size=18,
                      color=GREY_A).next_to(frame, UP, buff=0.1).align_to(frame, LEFT)
        ptr = Triangle(color=HEAD, fill_color=HEAD, fill_opacity=1).scale(0.09).rotate(-PI / 2)
        jumps = (0, 9, 4, 10, 2, 6, 0, 9)
        # the tally of folded stacks
        fo = p["folded"]
        top = sorted(fo.items(), key=lambda kv: -kv[1])[:5]
        rest = p["samples"] - sum(c for _, c in top)
        items = [(s, c) for s, c in top] + [(r"everything else", rest)]
        tally = VGroup()
        cmax = max(c for _, c in items)
        for i, (s_, c) in enumerate(items):
            y = 0.85 - i * 0.62
            nm = mono(s_, size=16, color=GREY_A) if ";" in s_ else label(s_, font_size=18, color=GREY_A)
            nm.move_to([0.5, y, 0], aligned_edge=LEFT)
            bar = Rectangle(width=max(0.03, 2.3 * c / cmax), height=0.3, stroke_width=0, fill_color=KERN,
                            fill_opacity=0.85).move_to([3.35, y, 0], aligned_edge=LEFT)
            val = label(rf"{c:,}", font_size=17, color=KERN).next_to(bar, RIGHT, buff=0.1)
            tally.add(VGroup(nm, bar, val))
        tally_t = label(rf"{p['samples']:,} samples, \ by stack", font_size=19, color=WHITE).next_to(
            tally, UP, buff=0.25).align_to(tally, LEFT)
        with self.voiceover(
            "A sampling profiler does not trace every step. Now and then it interrupts the program and asks where "
            "it is. <bookmark mark='a'/> Pebble runs version zero of the Job over twenty thousand bytes of a novel: "
            "six point three million instructions. Every nine hundred and ninety-seventh, a prime, so that it "
            "cannot fall into step with a loop, the profiler reads the program counter. <bookmark mark='b'/> It "
            "maps the address to its routine, and the routine to its callers: main, then word, then scan. <bookmark "
            "mark='c'/> Counting the stacks gives a folded profile of six thousand three hundred and eleven "
            "samples, more than four in five of them in scan and next, the loop that walks the table."
        ) as vo:
            self.play(FadeIn(head), Create(strip, lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(strip_l), *[h.animate.set_color(HEAD).set_stroke(width=3) for h in hits])
            vo.wait_until("b")
            self.play(FadeIn(frame), FadeIn(code), FadeIn(title))
            ptr.next_to(code[jumps[0]], LEFT, buff=0.12)
            self.play(FadeIn(ptr))
            for j in jumps[1:]:
                self.play(ptr.animate.next_to(code[j], LEFT, buff=0.12), run_time=0.35)
            vo.wait_until("c")
            self.play(FadeIn(tally_t), *[FadeIn(r[0]) for r in tally])
            self.play(LaggedStart(*[GrowFromEdge(r[1], LEFT) for r in tally], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(r[2]) for r in tally], lag_ratio=0.15), run_time=2)
        self.wait(0.4)
        self.clear_scene()


    def flame(self):
        self.ask(r"In a flame graph, the horizontal axis is...", [r"time", r"share of samples"], 1,
                 say="A flame graph stacks frames on frames. What does its horizontal axis show?",
                 reveal="Share of samples, sorted alphabetically, not time. Width is cost.")
        p = load("profile")
        fr = p["flame"]
        head = label(r"A flame graph", font_size=36).to_edge(UP, buff=0.3)
        fg = flame_graph(fr, base=-3.2, row_h=0.8, size=19)
        w = {f["path"]: f["w"] for f in fr}
        notes = VGroup(
            wrapped_label(r"\textbf{width}: \ the share of samples in that frame and everything above it", 4.0,
                          font_size=19, color=WHITE),
            wrapped_label(r"\textbf{up}: \ the call stack; \ the top edge is where the processor actually was", 4.0,
                          font_size=19, color=WHITE),
            wrapped_label(r"\textbf{across}: \ alphabetical, \ not time, \ so equal stacks merge", 4.0,
                          font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(head, DOWN, buff=0.35)
        word = fg.boxes["main;word"]
        scan, nxt, cmp = (fg.boxes[k] for k in ("main;word;scan", "main;word;next", "main;word;cmp"))
        verdict = VGroup(
            label(rf"\texttt{{word}}: \ {100 * w['main;word']:.1f}\% of all samples", font_size=21, color=HEAD),
            label(rf"\texttt{{scan}} $+$ \texttt{{next}}: \ {100 * (w['main;word;scan'] + w['main;word;next']):.0f}\%, "
                  r"\ walking an unsorted table entry by entry", font_size=21, color=HEAD),
            label(r"the fix is not a faster loop but no loop: \ Part 17's hash table", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(notes, DOWN, buff=0.4).align_to(notes, LEFT)
        with self.voiceover(
            "In 2011 Brendan Gregg found a way to see a profile at a glance: the flame graph. <bookmark mark='a'/> "
            "Each box is a frame, as wide as the share of samples with that frame on the stack. <bookmark "
            "mark='b'/> Callers sit below their callees, so the top edge is where the processor actually was. "
            "<bookmark mark='c'/> Left to right is alphabetical, not time, so identical stacks merge. <bookmark "
            "mark='d'/> Read ours from the bottom. Word takes ninety-four and a half percent of all samples. Above "
            "it, scan and next take eighty-two, and cmp, comparing letters, most of the rest. The Job walks its "
            "table, entry by entry, for every word. <bookmark mark='e'/> The profile does not say make this loop "
            "faster. It says do not loop: Part 17's hash table finds a word in one probe."
        ) as vo:
            self.play(FadeIn(head))
            for d in fg.depths:
                self.play(LaggedStart(*[GrowFromEdge(c, DOWN) for c in d], lag_ratio=0.05), run_time=0.7)
            for mk, nt in zip("abc", notes):
                vo.wait_until(mk)
                self.play(FadeIn(nt))
            vo.wait_until("d")
            self.play(Indicate(word, color=WHITE, scale_factor=1.03), FadeIn(verdict[0]))
            self.play(Indicate(VGroup(scan, nxt), color=WHITE, scale_factor=1.05), FadeIn(verdict[1]))
            self.play(Indicate(cmp, color=WHITE, scale_factor=1.05))
            vo.wait_until("e")
            self.play(FadeIn(verdict[2]))
        self.wait(0.4)
        self.clear_scene()


    def offcpu(self):
        head = label(r"Off-CPU time, \ and eBPF", font_size=36).to_edge(UP, buff=0.3)
        x0, x1, y = -5.2, 6.4, 0.9
        segs = ((0.0, 0.14, "on"), (0.14, 0.36, r"disk"), (0.36, 0.47, "on"), (0.47, 0.62, r"lock"),
                (0.62, 0.70, "on"), (0.70, 0.92, r"network"), (0.92, 1.0, "on"))
        bars = VGroup()
        for a, b, kind in segs:
            on = kind == "on"
            r = Rectangle(width=(b - a) * (x1 - x0) - 0.02, height=0.45, stroke_width=0,
                          fill_color=KERN if on else DATA, fill_opacity=0.85 if on else 0.35)
            r.move_to([x0 + (a + b) / 2 * (x1 - x0), y, 0])
            cell = VGroup(r)
            if not on:
                cell.add(label(rf"waiting: \ {kind}", font_size=17, color=WHITE).move_to(r))
            bars.add(cell)
        thr = label(r"one thread", font_size=19, color=GREY_A).next_to(bars, LEFT, buff=0.25)
        ticks = VGroup()
        for k in range(30):
            t = (k + 0.5) / 30
            on = any(a <= t < b and kind == "on" for a, b, kind in segs)
            if on:
                xx = x0 + t * (x1 - x0)
                ticks.add(Line([xx, y + 0.35, 0], [xx, y + 0.6, 0], color=HEAD, stroke_width=3))
        tick_l = label(r"CPU samples land only here", font_size=17, color=HEAD).next_to(ticks, UP, buff=0.1)
        sw = VGroup(*[DashedLine([x0 + a * (x1 - x0), y - 0.3, 0], [x0 + a * (x1 - x0), y - 0.75, 0], color=DATA,
                                 stroke_width=2) for a, b, kind in segs if kind != "on"])
        sw_l = label(r"the scheduler switches the thread out: \ record its stack and how long until it runs "
                     r"again", font_size=18, color=DATA).next_to(sw, DOWN, buff=0.12).set_x(0.6)
        ill = note(r"illustrative", font_size=16).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        notes = VGroup(
            wrapped_label(r"\textbf{on-CPU} \ $+$ \ \textbf{off-CPU} \ $=$ \ wall-clock time: \ a request that waits "
                          r"on a lock is slow while its CPU profile looks idle", 5.8, font_size=19, color=WHITE),
            wrapped_label(r"\textbf{eBPF} \ (Part 31): \ a small verified program attached to the scheduler's "
                          r"tracepoint sums the waits by stack inside the kernel; \ only the totals reach user "
                          r"space", 5.8, font_size=19, color=YES),
        ).arrange(RIGHT, buff=0.5, aligned_edge=UP).next_to(sw_l, DOWN, buff=0.7)
        with self.voiceover(
            "A profiler that samples the processor sees only time spent running. <bookmark mark='a'/> Real requests "
            "also wait: for a disk, a lock, a reply from the network. <bookmark mark='b'/> Timer samples land only "
            "where the thread was running, so a request stuck behind a lock can look idle. <bookmark mark='c'/> "
            "Off-CPU analysis catches the rest. Each time the scheduler switches a thread out, record its stack, "
            "and when it runs again, charge the time away to that stack. On-CPU plus off-CPU is wall-clock time. "
            "<bookmark mark='d'/> eBPF, from Part 31, makes this cheap: a small verified program on the scheduler's "
            "tracepoint sums the waits inside the kernel, and only the totals reach user space."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill), FadeIn(thr), *[FadeIn(b[0]) for b in bars if len(b) == 1])
            vo.wait_until("a")
            self.play(*[FadeIn(b) for b in bars if len(b) > 1])
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.05), FadeIn(tick_l), run_time=1.5)
            vo.wait_until("c")
            self.play(*[Create(s) for s in sw], FadeIn(sw_l))
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, LAM, NO, YES)
