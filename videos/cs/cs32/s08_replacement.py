from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, HEAD, NO, PART, YES, grid_table, load, mono)


def fifo_grid(steps, k, cw=0.62, ch=0.42):
    """One column per reference: the page on top, then the k frames (oldest at the top); faults in red."""
    cols = VGroup()
    for s in steps:
        top = mono(str(s["p"]), 20, WHITE)
        cells = VGroup()
        for i in range(k):
            v = s["frames"][i] if i < len(s["frames"]) else ""
            r = Rectangle(width=cw, height=ch, stroke_color=GREY_D, stroke_width=1, fill_color=BG, fill_opacity=1)
            cells.add(VGroup(r, mono(str(v), 18, GREY_A).move_to(r)))
        cells.arrange(DOWN, buff=0)
        mark = Dot(radius=0.07, color=NO if not s["hit"] else YES)
        cols.add(VGroup(top, cells, mark).arrange(DOWN, buff=0.1))
    cols.arrange(RIGHT, buff=0.06)
    return cols


def opt_steps(string, k):
    """Belady's OPT on ``string`` with k frames; each page keeps its slot, so a column shows one replacement."""
    slots, out = [], []
    for i, p in enumerate(string):
        hit = p in slots
        if not hit:
            if len(slots) < k:
                slots.append(p)
            else:
                def nxt(q):
                    rest = string[i + 1:]
                    return rest.index(q) if q in rest else len(rest) + 1
                slots[slots.index(max(slots, key=nxt))] = p
        out.append({"p": p, "frames": list(slots), "hit": hit})
    return out


def lru_steps(string, k):
    mem, out = [], []
    for p in string:
        hit = p in mem
        if hit:
            mem.remove(p)
        elif len(mem) == k:
            mem.pop(0)
        mem.append(p)
        out.append({"p": p, "frames": list(mem), "hit": hit})
    return out


def fmt_k(v):
    return f"{v:,}".replace(",", "{,}")


class Replacement(VoiceoverScene):
    def construct(self):
        self.card()
        self.opt()
        self.anomaly()
        self.lru()
        self.competitive()
        self.clock()

    def card(self):
        card = chapter_card(7, r"Which page to evict", r"When memory is full, which page should go?",
                            lit=(1966, 1969, 2003), extra=((1966, r"Belady: \ OPT"), (1969, r"Belady's anomaly"),
                                                          (2003, r"ARC")), part=PART)
        with self.voiceover("Chapter seven. Which page to evict."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def opt(self):
        d = load("belady")
        head = label(r"The optimum: \ evict the page needed latest", font_size=34).to_edge(UP, buff=0.3)
        top = VGroup(
            label(r"memory is full; \ a fault needs a frame: \ which page goes?", font_size=23, color=WHITE),
            label(r"\textbf{OPT} \ (Belady, \ 1966): \ the page whose next use is farthest in the future", font_size=23,
                  color=YES),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.35)
        steps = opt_steps(d["string"], 3)
        g = fifo_grid(steps, 3).next_to(top, DOWN, buff=0.35)
        nopt = sum(not st["hit"] for st in steps)
        gl = label(rf"OPT, \ 3 frames: \ {nopt} faults", font_size=20, color=YES).next_to(g, LEFT, buff=0.2)
        if gl.get_left()[0] < -6.9:
            VGroup(gl, g).shift(RIGHT * (-6.9 - gl.get_left()[0]))
        lines = VGroup(
            label(r"the exchange: \ a schedule evicts $f$ where OPT evicts $e$, \ and $f$ is needed before $e$",
                  font_size=21, color=GREY_A),
            label(r"evict $e$ instead, \ then copy it: \ at the next use of $f$ we hit, \ or pay the one fault it "
                  r"would have paid", font_size=21, color=GREY_A),
            label(r"but OPT needs the future: \ a yardstick, \ not a policy; \ real policies guess the future from "
                  r"the past", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "When memory is full and a fault needs a frame, some page must go. <bookmark mark='a'/> Which one? "
            "<bookmark mark='b'/> László Belady showed in 1966 that the best choice is the page whose next use lies "
            "farthest in the future. <bookmark mark='c'/> Here it is on the reference string Belady used, with three "
            "frames: seven faults, and no policy can do better. <bookmark mark='d'/> The proof is an exchange, like "
            "the one for shortest-first scheduling in Part 31. Suppose some schedule, at a fault, evicts a page f, "
            "where the optimum would evict e, so f is needed again before e. <bookmark mark='e'/> Change it to evict e, "
            "and then copy the old schedule. When f is next requested, the new schedule either hits, or pays the "
            "single fault the old one would have paid anyway. So the new schedule is never worse, and agrees with the "
            "optimum one step longer. <bookmark mark='f'/> But this optimum needs to know the future. It is a "
            "yardstick, not a policy. Real policies guess the future from the past."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top[0]))
            vo.wait_until("b")
            self.play(FadeIn(top[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in g], lag_ratio=0.1), FadeIn(gl), run_time=2.5)
            for mk, ln in zip("def", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def anomaly(self):
        d = load("belady")
        head = label(r"Belady's anomaly: \ more memory, \ more faults", font_size=34).to_edge(UP, buff=0.25)
        g3 = fifo_grid(d["fifo3"], 3).next_to(head, DOWN, buff=0.35)
        g4 = fifo_grid(d["fifo4"], 4).next_to(g3, DOWN, buff=0.35)
        t3 = next(r for r in d["table"] if r["k"] == 3)
        t4 = next(r for r in d["table"] if r["k"] == 4)
        l3 = label(rf"FIFO, \ 3 frames: \ {t3['fifo']} faults", font_size=20, color=NO).next_to(g3, LEFT, buff=0.2)
        l4 = label(rf"FIFO, \ 4 frames: \ {t4['fifo']} faults", font_size=20, color=NO).next_to(g4, LEFT, buff=0.2)
        for lab, g in ((l3, g3), (l4, g4)):
            if lab.get_left()[0] < -6.9:
                VGroup(lab, g).shift(RIGHT * (-6.9 - lab.get_left()[0]))
        trials = f"{d['random_trials']:,}".replace(",", "{,}")
        lines = VGroup(
            label(r"first in, \ first out: \ evict the page loaded longest ago \ (red dots: \ faults)", font_size=20,
                  color=WHITE),
            label(r"Belady, \ Nelson and Shedler \ (1969): \ FIFO can fault \textbf{more} with more frames", font_size=20,
                  color=NO),
            label(rf"rare: \ {d['found4']} random strings in {trials} show it \ (length 20, \ 6 pages, \ 4 frames)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The simplest guess is first in, first out: evict the page that was loaded longest ago. <bookmark "
            "mark='a'/> Here is the reference string Belady used, with three frames. Each column is one reference; the "
            "red dots are faults. Nine faults. <bookmark mark='b'/> Now give FIFO a fourth frame. Ten faults. More "
            "memory, more faults. <bookmark mark='c'/> Belady, Nelson and Shedler published this in 1969, and it "
            "shocked people, because it means buying memory can make a machine slower. <bookmark mark='d'/> It is "
            "rare: we found two such strings in twenty thousand random ones. But it can happen, and some policies "
            "cannot do it at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in g3], lag_ratio=0.1), FadeIn(l3), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in g4], lag_ratio=0.1), FadeIn(l4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def lru(self):
        d = load("belady")
        head = label(r"LRU, \ and the stack property", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"frames", r"FIFO", r"LRU", r"OPT"],
                         [[str(r["k"]), str(r["fifo"]), str(r["lru"]), str(r["opt"])] for r in d["table"]],
                         widths=[2.0, 1.8, 1.8, 1.8], row_h=0.46, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        tab.cells[4][1].set_color(NO)
        notes = VGroup(
            label(r"\textbf{LRU}: \ evict the page used least recently: \\ the past as a guess at the future", font_size=21,
                  color=WHITE),
            label(r"the \textbf{inclusion property}: \ the pages LRU holds \\ with $k$ frames are always among those "
                  r"it \\ holds with $k + 1$", font_size=21, color=YES),
            label(r"proof: \ both hold the $k$ (or $k+1$) most recently \\ used pages, \ and the $k$ most recent are among "
                  r"\\ the $k+1$ most recent", font_size=21, color=GREY_A),
            label(r"so a hit with $k$ frames is a hit with $k+1$: \\ no anomaly, \ ever; \ OPT has the property too",
                  font_size=21, color=YES),
            label(rf"checked: \ {d['lru_anomalies']} anomalies for LRU \\ in 5{{,}}000 random strings", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(tab, RIGHT, buff=0.6).align_to(tab, UP)
        with self.voiceover(
            "A better guess: the past predicts the future. Evict the page used least recently. <bookmark mark='a'/> On "
            "Belady's string, least recently used is worse than FIFO at three frames, but never shows the anomaly. "
            "<bookmark mark='b'/> The reason is the inclusion property. <bookmark mark='c'/> With k frames, LRU holds "
            "exactly the k pages used most recently; with k plus one, the k plus one most recent, which include them. "
            "<bookmark mark='d'/> So any reference that hits with k frames also hits with more, and adding memory can "
            "never add faults. Algorithms with this property are called stack algorithms, and OPT is one too. "
            "<bookmark mark='e'/> We checked five thousand random strings: no anomalies for LRU."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), FadeIn(notes[0]))
            for mk, n_ in zip("abcde", notes):
                vo.wait_until(mk)
                if n_ is not notes[0]:
                    self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def competitive(self):
        d = load("competitive")
        head = label(r"How bad can LRU be?", font_size=36).to_edge(UP, buff=0.3)
        string = [i % 4 for i in range(24)]
        rows = VGroup()
        for name, steps, c in ((r"LRU", lru_steps(string, 3), NO), (r"OPT", opt_steps(string, 3), YES)):
            dots = VGroup(*[Dot(radius=0.09, color=NO if not st["hit"] else YES) for st in steps]).arrange(RIGHT,
                                                                                                    buff=0.32)
            nf = sum(not st["hit"] for st in steps)
            rows.add(VGroup(label(rf"{name}: \ {nf} faults", font_size=20, color=c), dots))
        refs = VGroup(*[mono(str(p + 1), 18, WHITE) for p in string]).arrange(RIGHT, buff=0.21)
        for r in rows:
            for dt, rf_ in zip(r[1], refs):
                dt.set_x(rf_.get_x())
        refs.next_to(head, DOWN, buff=0.6)
        for i, r in enumerate(rows):
            r[1].next_to(refs, DOWN, buff=0.35 + 0.5 * i).set_x(refs.get_x())
            for dt, rf_ in zip(r[1], refs):
                dt.set_x(rf_.get_x())
            r[0].next_to(r[1], LEFT, buff=0.3)
        g = VGroup(refs, rows)
        if g.get_left()[0] < -6.9:
            g.shift(RIGHT * (-6.9 - g.get_left()[0]))
        rl = label(r"4 pages in a cycle, \ 3 frames", font_size=18, color=GREY_A).next_to(refs, UP, buff=0.12)
        cy = d["cyclic"]
        tab = grid_table([r"$h$", r"OPT, \ $h$ frames", r"LRU, \ $2h$ frames", r"ratio", r"bound $\frac{k}{k-h+1}$"],
                         [[str(r["h"]), fmt_k(r["opt_h"]), fmt_k(r["lru_k"]), f"{r['ratio']:.2f}",
                           f"{r['bound']:.2f}"] for r in d["rows"]],
                         widths=[0.9, 2.5, 2.6, 1.4, 2.6], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(rows, DOWN, buff=0.45).set_x(0)
        lines = VGroup(
            label(rf"over {d['cyc_len']} references: \ LRU {cy['lru']}, \ FIFO {cy['fifo']}, \ OPT {cy['opt']}: \ "
                  r"worse by about $k$", font_size=20, color=NO),
            label(r"Sleator and Tarjan \ (1985): \ with $k$ frames against OPT's $h$, \ LRU and FIFO are within "
                  r"$\frac{k}{k-h+1}$, \ and no deterministic policy does better", font_size=20, color=WHITE),
            label(r"on the Job's real trace, \ LRU with twice the memory beats the optimum outright", font_size=20,
                  color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "How far from the optimum can LRU be? <bookmark mark='a'/> Take four pages used in a cycle, with three "
            "frames. LRU always evicts exactly the page that comes next, so it faults on every single reference. "
            "<bookmark mark='b'/> The optimum, knowing the future, faults only once in every three. Over a hundred "
            "and twenty references: a hundred and twenty faults against forty-two. With k frames, an adversary can "
            "make any deterministic policy fault about k times as often as the optimum. <bookmark mark='c'/> Sleator and "
            "Tarjan proved in 1985 that this is the worst: LRU, and FIFO too, are within a factor k of the optimum, "
            "and no deterministic policy can promise better. More usefully, give LRU k frames and the optimum only h: "
            "the factor falls to k over k minus h plus one, under two when LRU has twice the memory. <bookmark "
            "mark='d'/> On the Job's real trace it is better still. With twice the memory, LRU does not merely come "
            "within a factor of two. It beats the optimum outright. Real programs are not adversaries."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rl), FadeIn(refs))
            self.play(FadeIn(rows[0][0]), LaggedStart(*[FadeIn(x) for x in rows[0][1]], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1][0]), LaggedStart(*[FadeIn(x) for x in rows[1][1]], lag_ratio=0.05), run_time=1.5)
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def clock(self):
        d = load("belady")
        head = label(r"CLOCK: \ LRU, \ approximately and cheaply", font_size=34).to_edge(UP, buff=0.3)
        trace = d["clock"]
        k = 4
        import math
        centre = [-3.3, -0.2, 0]
        R = 1.7
        pos = [[centre[0] + R * math.sin(2 * math.pi * i / k), centre[1] + R * math.cos(2 * math.pi * i / k), 0]
               for i in range(k)]
        ring = Circle(radius=R, stroke_color=GREY_D, stroke_width=1.5).move_to(centre)

        def frames(hand, fr, ref):
            g = VGroup()
            for i in range(k):
                c = Circle(radius=0.42, stroke_color=YES if ref[i] else GREY_B, stroke_width=3,
                           fill_color=BG, fill_opacity=1).move_to(pos[i])
                t = mono(str(fr[i]) if fr[i] is not None else "", 22, WHITE).move_to(pos[i])
                b = label(rf"ref {ref[i]}", font_size=15, color=YES if ref[i] else GREY_B).next_to(c, DOWN, buff=0.05)
                g.add(VGroup(c, t, b))
            arrow = Arrow(centre, pos[hand], buff=0.45, color=HEAD, stroke_width=4)
            return VGroup(g, arrow)
        state = frames(*trace[0])
        refs = VGroup(*[mono(str(p), 22, GREY_A) for p in d["clock_string"]]).arrange(RIGHT, buff=0.25).next_to(
            head, DOWN, buff=0.35).shift(RIGHT * 2.0)
        notes = VGroup(
            label(r"each frame has the hardware's \textbf{accessed} bit", font_size=20, color=WHITE),
            label(r"on a fault, \ the hand sweeps: \ a set bit is cleared \\ (a second chance), \ the first clear "
                  r"frame is evicted", font_size=20, color=HEAD),
            label(r"no list to reorder on every access: \ only on faults", font_size=20, color=YES),
            label(r"Linux keeps active and inactive lists in this spirit; \\ \textbf{2Q}, \ \textbf{ARC} \ (2003) "
                  r"\ and \textbf{LIRS} \ (2002) \\ also resist scans, \ as the next chapter shows", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.0, -0.6, 0])
        with self.voiceover(
            "True LRU would reorder a list on every memory access, far too often for hardware or software. The "
            "practical approximation is CLOCK. <bookmark mark='a'/> Each frame keeps the accessed bit the hardware "
            "sets. <bookmark mark='b'/> On a fault, a hand sweeps around the frames. A frame whose bit is set gets a "
            "second chance: the bit is cleared and the hand moves on. The first frame found with its bit clear is "
            "evicted. <bookmark mark='c'/> Nothing happens on ordinary accesses, only on faults. <bookmark mark='d'/> "
            "Real kernels refine the idea, and newer policies, 2Q, ARC and LIRS, also defend against a single scan "
            "flushing everything useful, as the next chapter shows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(refs), Create(ring), FadeIn(state))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            for st in trace[1:]:
                new = frames(*st)
                self.play(Transform(state, new), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
