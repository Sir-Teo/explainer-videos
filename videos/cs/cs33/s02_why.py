from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (BG, DATA, HEAD, KERN, NO, PART, T0C, T1C, YES, load)


def bar(x0, x1, y, color, text="", h=0.55):
    r = Rectangle(width=x1 - x0, height=h, stroke_width=0, fill_color=color, fill_opacity=0.8)
    r.move_to([(x0 + x1) / 2, y, 0])
    g = VGroup(r)
    if text:
        g.add(label(text, font_size=18, color=WHITE).move_to(r))
    return g


class Why(VoiceoverScene):
    def construct(self):
        self.card()
        self.overlap()
        self.threads()

    def card(self):
        card = chapter_card(1, r"Why concurrency", r"Why run more than one thing at a time?", lit=(1965, 2005),
                            extra=((1965, r"Dijkstra: \ cooperating processes"), (2005, r"multicore for everyone")),
                            part=PART)
        with self.voiceover("Chapter one. Why concurrency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def overlap(self):
        head = label(r"Two reasons", font_size=36).to_edge(UP, buff=0.3)
        s = 0.85
        x0 = -5.6
        top = VGroup(label(r"one thread serving two requests", font_size=21, color=GREY_A))
        segs1 = [(0, 1, DATA, "A"), (1, 5, GREY_D, "wait for disk"), (5, 6, DATA, "A"), (6, 7, HEAD, "B"),
                 (7, 11, GREY_D, "wait"), (11, 12, HEAD, "B")]
        row1 = VGroup(*[bar(x0 + a * s, x0 + b * s, 2.0, c, t) for a, b, c, t in segs1])
        top[0].next_to(row1, UP, buff=0.12).align_to(row1, LEFT)
        segs2 = [(0, 1, DATA, "A"), (1, 2, HEAD, "B"), (5, 6, DATA, "A"), (6, 7, HEAD, "B")]
        row2 = VGroup(*[bar(x0 + a * s, x0 + b * s, 0.7, c, t) for a, b, c, t in segs2])
        waits = VGroup(bar(x0 + 1 * s, x0 + 5 * s, 0.15, GREY_D, "A's disk", 0.38),
                       bar(x0 + 2 * s, x0 + 6 * s, -0.3, GREY_D, "B's disk", 0.38))
        l2 = label(r"two threads: \ while one waits, \ the other runs", font_size=21, color=GREY_A).next_to(
            row2, UP, buff=0.12).align_to(row2, LEFT)
        t1 = label(r"12 units", font_size=21, color=NO).next_to(row1, RIGHT, buff=0.2)
        t2 = label(r"7 units", font_size=21, color=YES).next_to(VGroup(row2, waits), RIGHT, buff=0.2).align_to(t1, LEFT)
        lines = VGroup(
            label(r"1. \ \textbf{overlap}: \ a server waits for disks and networks; \ other work fills the wait "
                  r"\ (Part 31's scheduler)", font_size=21, color=WHITE),
            label(r"2. \ \textbf{parallelism}: \ since about 2005 clock rates stopped rising; \ more speed means more "
                  r"cores \ (Part 10)", font_size=21, color=YES),
            label(r"either way, \ several threads of control touch the same data", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "There are two reasons to run more than one thing at once. <bookmark mark='a'/> The first is overlap. A "
            "server handling one request at a time spends most of its life waiting: for the disk, for the network. "
            "<bookmark mark='b'/> With two threads, while one waits, the other runs, and the same work finishes in "
            "seven units instead of twelve. That is Part 31's scheduler, used inside one program. <bookmark mark='c'/> "
            "The second is parallelism. Around 2005, processor clock rates stopped rising, and since then a faster "
            "computer means more cores, which only a program with several threads can use. <bookmark mark='d'/> "
            "Either way, several threads of control end up touching the same data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), LaggedStart(*[FadeIn(b) for b in row1], lag_ratio=0.2), FadeIn(t1))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(l2), LaggedStart(*[FadeIn(b) for b in row2], lag_ratio=0.2), FadeIn(waits), FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def threads(self):
        d = load("spawn")
        head = label(r"Processes and threads", font_size=36).to_edge(UP, buff=0.3)

        def space(title, color, inner, pos):
            r = RoundedRectangle(width=4.8, height=3.2, corner_radius=0.15, stroke_color=color, stroke_width=2,
                                 fill_color=BG, fill_opacity=1).move_to(pos)
            t = label(title, font_size=20, color=color).next_to(r.get_top(), DOWN, buff=0.12)
            return VGroup(r, t, inner.move_to(r).shift(DOWN * 0.2))

        def cell(t, c, w=1.9):
            r = RoundedRectangle(width=w, height=0.48, corner_radius=0.06, stroke_color=c, stroke_width=1.4,
                                 fill_color=c, fill_opacity=0.15)
            return VGroup(r, label(t, font_size=18, color=WHITE).move_to(r))
        procs = VGroup()
        for k, c in enumerate((T0C, T1C)):
            procs.add(VGroup(cell(r"code, \ data, \ heap", c), cell(r"page table", c), cell(r"registers, \ stack", c)
                             ).arrange(DOWN, buff=0.1))
        pa = space(r"two processes \ (Part 31)", KERN, procs.arrange(RIGHT, buff=0.35), [-3.4, 0.5, 0])
        shared = VGroup(cell(r"code, \ data, \ heap", YES, 4.0), cell(r"one page table", YES, 4.0))
        own = VGroup(cell(r"registers, \ stack", T0C), cell(r"registers, \ stack", T1C)).arrange(RIGHT, buff=0.2)
        ta = space(r"one process, \ two threads", YES, VGroup(*shared, own).arrange(DOWN, buff=0.1), [3.4, 0.5, 0])
        lines = VGroup(
            label(r"threads share the address space \ (Part 32): \ every variable is shared unless it is on a stack",
                  font_size=21, color=WHITE),
            label(rf"on this machine: \ a thread created and joined in {d['thread_us']:.0f} $\mu$s, \ a process forked "
                  rf"and reaped in {d['process_us']:.0f}", font_size=21, color=YES),
            label(r"cheap to make, \ cheap to talk \ (a store, \ not a pipe), \ and easy to get wrong", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Part 31 ran programs as processes, each with its own address space. <bookmark mark='a'/> Two processes "
            "share nothing unless they ask the kernel, through a pipe for instance. <bookmark mark='b'/> A thread is a "
            "second flow of control inside one process: its own registers and its own stack, but the same code, the "
            "same heap, the same page table. <bookmark mark='c'/> So every variable not on a stack is shared. "
            "<bookmark mark='d'/> On this machine, creating and joining a thread takes about forty microseconds; "
            "forking a process and waiting for it, about a hundred and eighty. <bookmark mark='e'/> Threads are cheap "
            "to make and cheap to communicate between, since a message is just a store. And, as the hook showed, "
            "easy to get wrong."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pa))
            vo.wait_until("b")
            self.play(FadeIn(ta))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
