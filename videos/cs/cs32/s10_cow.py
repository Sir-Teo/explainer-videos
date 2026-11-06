from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, DATA, HEAD, NO, PART, YES, load, mono)


def ptable(title, color, entries, pos):
    rows = VGroup(*[VGroup(Rectangle(width=2.8, height=0.52, stroke_color=color, stroke_width=1.2, fill_color=BG,
                                     fill_opacity=1), mono(e, 19, WHITE)) for e in entries])
    for r in rows:
        r[1].move_to(r[0])
    rows.arrange(DOWN, buff=0).move_to(pos)
    return VGroup(label(title, font_size=19, color=color).next_to(rows, UP, buff=0.1), rows)


class Cow(VoiceoverScene):
    def construct(self):
        self.card()
        self.cow()
        self.measured()
        self.mmap()

    def card(self):
        card = chapter_card(9, r"Copy-on-write, \ zero pages and mmap", r"How can fork copy nothing?",
                            lit=(1987,), extra=((1987, r"Mach: \ copy-on-write"),), part=PART)
        with self.voiceover("Chapter nine. Copy-on-write, zero pages, and memory-mapped files."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cow(self):
        head = label(r"fork without copying", font_size=36).to_edge(UP, buff=0.3)
        par = ptable(r"parent's table", DATA, ["page 0 -> A  RO", "page 1 -> B  RO", "page 2 -> C  RO"], [-4.9, 1.0, 0])
        chi = ptable(r"child's table", HEAD, ["page 0 -> A  RO", "page 1 -> B  RO", "page 2 -> C  RO"], [4.9, 1.0, 0])
        frames = VGroup(*[VGroup(Square(1.0, stroke_color=YES, fill_color=BG, fill_opacity=1), label(t, font_size=30,
                                                                                                   color=YES))
                          for t in ("A", "B", "C")]).arrange(RIGHT, buff=0.5).move_to([0, 1.0, 0])
        for f in frames:
            f[1].move_to(f[0])
        links = VGroup()
        for t in (par, chi):
            for row, f in zip(t[1], frames):
                links.add(Line(row.get_center(), f.get_center(), color=GREY_D, stroke_width=1.2).set_z_index(-1))
        newb = VGroup(Square(1.0, stroke_color=HEAD, fill_color=BG, fill_opacity=1), label(r"B$'$", font_size=30,
                                                                                            color=HEAD)).move_to(
            [2.4, -0.9, 0])
        newb[1].move_to(newb[0])
        wl = label(r"the child writes page 1: \ a fault; \ the kernel copies B to B$'$, \ maps it writable",
                   font_size=22, color=HEAD).next_to(newb, DOWN, buff=0.25)
        nl = Line(chi[1][1].get_center(), newb.get_center(), color=HEAD, stroke_width=2).set_z_index(-1)
        lines = VGroup(
            label(r"fork copies the \textbf{tables}, \ marks every page read-only in both, \ and shares the frames",
                  font_size=21, color=WHITE),
            label(r"only pages someone writes are ever copied; \ a fork followed by exec copies almost nothing",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Fork promises the child a copy of all the parent's memory. Virtual memory lets it keep that promise "
            "without copying. <bookmark mark='a'/> Fork copies only the page tables, so both processes point at the "
            "same frames, and it marks every page read-only in both. <bookmark mark='b'/> Reading costs nothing. "
            "<bookmark mark='c'/> When either process writes a page, the write faults. The kernel sees a page that is "
            "shared, not truly read-only, copies it into a fresh frame, maps the copy writable for the writer, and "
            "lets the write go ahead. <bookmark mark='d'/> Only pages that are actually written are ever copied. A "
            "fork followed at once by exec, the shell's pattern, copies almost nothing. The Mach kernel made this "
            "standard in the late nineteen-eighties."
        ) as vo:
            self.play(FadeIn(head), FadeIn(par), FadeIn(frames))
            vo.wait_until("a")
            self.play(FadeIn(chi), Create(links), FadeIn(lines[0]), run_time=2.0)
            vo.wait_until("b")
            self.wait(0.2)
            vo.wait_until("c")
            self.play(FadeIn(newb), FadeIn(wl), FadeOut(links[4]), Create(nl), chi[1][1][1].animate.become(
                mono("page 1 -> B' RW", 19, HEAD).move_to(chi[1][1][0])))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("cow")
        head = label(r"Measured on this machine", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(*[label(t, font_size=24, color=c) for t, c in (
            (rf"a parent using {d['mib']} MiB forks: \ {d['fork_ms']:.1f} ms \ (copying tables, \ not memory)", WHITE),
            (rf"the child's first write to each page: \ {d['cow_ns'] / 1000:.1f} $\mu$s \ (a fault and a 4 KiB copy)",
             NO),
            (rf"its second write: \ {d['after_ns']:.0f} ns \ (an ordinary store)", YES),
            (r"Part 31: \ fork with 1 GiB in use took 33 ms; \ the cost is the tables, \ and it grows with memory",
             GREY_A),
            (r"so a forked child that writes all its memory pays the copy anyway, \ one fault at a time", HEAD))]
                     ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "On this machine: <bookmark mark='a'/> a parent using two hundred and fifty-six mebibytes forks in under "
            "six milliseconds, because only the tables are copied. <bookmark mark='b'/> Then the child writes one byte "
            "in every page. Each first write takes three microseconds: a fault, and a copy of four kibibytes. <bookmark "
            "mark='c'/> A second write to the same page takes twenty-six nanoseconds, an ordinary store. <bookmark "
            "mark='d'/> Part 31's fork with a gibibyte took thirty-three milliseconds, all of it tables. <bookmark "
            "mark='e'/> And a child that writes all its memory still pays for the copy in the end, one fault at a time."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def mmap(self):
        head = label(r"The same machinery, \ three more uses", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(*[VGroup(label(t, font_size=26, color=c), label(s, font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1) for t, s, c in (
            (r"the zero page", r"untouched anonymous memory reads as zeros from one shared frame; \ the first write "
                               r"gives a private copy", YES),
            (r"\texttt{mmap} of a file", r"the file's pages, \ from the kernel's page cache, \ appear in the address "
                                        r"space: \ a load is a read", DATA),
            (r"shared libraries", r"\texttt{libc}'s code is mapped read-only into every process from the same frames "
                                  r"\ (Part 11's linker, \ made cheap)", HEAD),
            (r"and the cost", r"a mapped file that faults reads the disk in the middle of an ordinary load", NO))]
                      ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The same machinery, mapping and faulting, serves three more purposes. <bookmark mark='a'/> Memory a "
            "process has asked for but never written reads as zeros from one shared frame of zeros, and the first "
            "write gives it a private page. <bookmark mark='b'/> m-map puts a file's pages into the address space, so "
            "reading the file is just a load; the pages come from the kernel's cache of the disk. <bookmark mark='c'/> "
            "Shared libraries, the libc of Part 11, are mapped read-only into every process from the same frames, so a "
            "hundred processes hold one copy. <bookmark mark='d'/> The price is that a load from a mapped file can, "
            "invisibly, wait for the disk."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
