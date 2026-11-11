from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (DATA, HEAD, KERN, NO, PART, YES, load)


def space(title, parts, color, pos, w=3.2):
    """An address space drawn as a column: (label, height, colour, opacity)."""
    col = VGroup()
    for t, h, c, op in parts:
        r = Rectangle(width=w, height=h, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=op)
        col.add(VGroup(r, label(t, font_size=18, color=WHITE).move_to(r)))
    col.arrange(DOWN, buff=0).move_to(pos)
    return VGroup(label(title, font_size=20, color=color).next_to(col, UP, buff=0.12), col)


class KernelMap(VoiceoverScene):
    def construct(self):
        self.card()
        self.shared()
        self.meltdown()

    def card(self):
        card = chapter_card(10, r"The kernel's own mapping", r"Where does the kernel live?", lit=(2018,),
                            extra=((2018, r"Meltdown; \ KPTI"),), part=PART)
        with self.voiceover("Chapter ten. The kernel's own mapping."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def shared(self):
        p = load("protect")
        head = label(r"The kernel, \ in every address space", font_size=34).to_edge(UP, buff=0.3)
        a = space(r"process 1", [(r"process 1 \ (U pages)", 2.2, DATA, 0.25), (r"kernel \ (no U)", 1.4, KERN, 0.35)],
                  DATA, [-3.6, 0.6, 0])
        b = space(r"process 2", [(r"process 2 \ (U pages)", 2.2, HEAD, 0.25), (r"kernel \ (no U)", 1.4, KERN, 0.35)],
                  HEAD, [3.6, 0.6, 0])
        link = DashedLine(a[1][1].get_right(), b[1][1].get_left(), color=KERN)
        ll = label(r"the same frames, \ the same entry", font_size=18, color=KERN).next_to(link, UP, buff=0.08)
        lines = VGroup(
            label(r"a trap needs no change of table: \ the kernel is already mapped, \ supervisor-only", font_size=23,
                  color=WHITE),
            label(rf"in PebbleOS: \ entry 0 of every L1 table, \ one 4 MiB superpage; \ a user read of it faults "
                  rf"\ (exit {p['kread_exit']})", font_size=23, color=YES),
            label(r"and the kernel reaches user buffers by their virtual addresses, \ through the current table",
                  font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Where does the kernel itself live? <bookmark mark='a'/> In every process's address space. The same "
            "kernel pages appear in every page table, marked supervisor-only: user mode cannot touch them, but they "
            "are always there. <bookmark mark='b'/> So a trap needs no change of page table: the kernel's code and "
            "data are already mapped. <bookmark mark='c'/> In our PebbleOS it is entry zero of every first-level "
            "table, a single four-mebibyte page. A user program that reads it faults and is killed. <bookmark "
            "mark='d'/> And because the process's pages are mapped too, the kernel can copy a process's buffers "
            "using the very addresses the process passed it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b), Create(link), FadeIn(ll))
            for mk, ln in zip("bcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def meltdown(self):
        k = load("kernelmap")
        head = label(r"Meltdown, \ 2018, \ and KPTI", font_size=36).to_edge(UP, buff=0.3)
        u = space(r"user mode", [(r"process", 2.0, DATA, 0.25), (r"a few kernel entry pages", 0.5, KERN, 0.35)],
                  DATA, [-3.6, 0.7, 0])
        kk = space(r"kernel mode", [(r"process", 2.0, DATA, 0.25), (r"the whole kernel", 1.3, KERN, 0.35)],
                   KERN, [3.6, 0.7, 0])
        sw = DoubleArrow(u[1].get_right(), kk[1].get_left(), buff=0.2, color=NO, stroke_width=2.5)
        swl = label(r"every trap: \ switch tables", font_size=18, color=NO).next_to(sw, UP, buff=0.08)
        lines = VGroup(
            label(r"Meltdown: \ on many Intel processors a user load of a kernel address faulted, \ but only after the "
                  r"data was used \textit{speculatively} \ (Part 8)", font_size=21, color=NO),
            label(r"the leak went through the cache, \ so the U bit alone no longer protected the kernel", font_size=21,
                  color=NO),
            label(r"the fix, \ \textbf{KPTI}: \ two tables per process; \ in user mode almost none of the kernel is "
                  r"mapped", font_size=21, color=YES),
            label(r"each system call now switches tables: \ cheap with PCIDs \ (chapter 5), \ expensive without",
                  font_size=21, color=HEAD),
            label(rf"this machine: \ Meltdown ``{k['vulnerabilities']['meltdown']}'': \ newer processors fixed it in "
                  r"silicon, \ and the kernel skips KPTI", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 2018 that arrangement broke. <bookmark mark='a'/> Meltdown, which Part 8 previewed: on many Intel "
            "processors, a user-mode load from a kernel address did fault, but only after the out-of-order core had "
            "already used the data speculatively. <bookmark mark='b'/> The data leaked through the cache, so the "
            "supervisor bit alone no longer kept the kernel secret. <bookmark mark='c'/> The fix was kernel page-table "
            "isolation. Each process gets two tables: in user mode almost none of the kernel is mapped, just the few "
            "pages that handle the entry. <bookmark mark='d'/> Every system call and interrupt must now switch tables. "
            "With address-space tags the switch is cheap; without them, it flushes the TLB each time, and some "
            "workloads slowed by a third. <bookmark mark='e'/> This machine's processor reports itself not affected, "
            "because newer chips fixed the flaw in hardware, and Linux skips the isolation here."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(u), FadeIn(kk), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(GrowArrow(sw), FadeIn(swl), FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()
