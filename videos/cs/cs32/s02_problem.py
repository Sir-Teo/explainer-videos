from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES)


def region_bar(parts, y, total=6.0, x0=-5.5, h=0.6):
    g = VGroup()
    x = x0
    for name, size, color in parts:
        w = 11.0 * size / total
        r = Rectangle(width=w, height=h, stroke_color=BG, stroke_width=1.5, fill_color=color, fill_opacity=0.8)
        r.move_to([x + w / 2, y, 0])
        g.add(VGroup(r, label(name, font_size=18, color=BG).move_to(r)))
        x += w
    return g


class Problem(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.atlas()

    def card(self):
        card = chapter_card(1, r"Protection and relocation", r"Why not let programs use physical addresses?",
                            lit=(1962,), extra=((1962, r"Atlas: \ paging"),), part=PART)
        with self.voiceover("Chapter one. Protection, and relocation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def why(self):
        head = label(r"What Part 31's PebbleOS could not do", font_size=34).to_edge(UP, buff=0.3)
        bar = region_bar([(r"kernel", 1, KERN), (r"tok \ (linked at 1 MiB)", 1, DATA), (r"job \ (linked at 2 MiB)", 1,
                                                                                          HEAD),
                          (r"free", 2, GREY_D)], 1.6, total=5.0)
        bl = label(r"physical memory, \ 5 MiB:\ each program compiled for its own region", font_size=19,
                   color=GREY_B).next_to(bar, DOWN, buff=0.12)
        rows = VGroup(*[label(t, font_size=22, color=c) for t, c in (
            (r"\textbf{relocation}: \ a program runs only where it was linked; \ a second copy needs a second "
             r"compile, \ and \texttt{fork} is impossible", NO),
            (r"\textbf{protection}: \ bounds protect one contiguous range; \ no sharing a library, \ no read-only "
             r"code", NO),
            (r"\textbf{size}: \ a program can never be bigger than the memory it is given", NO),
            (r"\textbf{fragmentation}: \ free memory in pieces too small to use \ (chapter 2)", NO),
            (r"the fix: \ give every process its own \textbf{virtual} addresses, \ and translate each one", YES))]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(bl, DOWN, buff=0.55)
        with self.voiceover(
            "In Part 31, PebbleOS gave each process its own region of physical memory. <bookmark mark='a'/> The tokenizer "
            "was compiled to run at one mebibyte and the job at two, and each program worked only there. That caused "
            "four problems. <bookmark mark='b'/> Relocation: a program runs only where it was linked, so a second copy "
            "needs a second compile, and fork, which copies a process, is impossible. <bookmark mark='c'/> Protection: "
            "the bounds guard one contiguous range, so two processes cannot share a library, and code cannot be "
            "read-only. <bookmark mark='d'/> Size: a program can never be bigger than its region. <bookmark "
            "mark='e'/> And fragmentation, which the next chapter shows. <bookmark mark='f'/> The fix for all four is "
            "the same: give each process its own virtual addresses, and have the hardware translate every one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bar], lag_ratio=0.2), FadeIn(bl))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def atlas(self):
        head = label(r"Atlas, \ Manchester, \ 1962: \ the one-level store", font_size=34).to_edge(UP, buff=0.3)
        core = Rectangle(width=2.6, height=1.6, stroke_color=YES, stroke_width=2.5, fill_color=BG, fill_opacity=1)
        drum = Rectangle(width=5.2, height=1.6, stroke_color=LAM, stroke_width=2.5, fill_color=BG, fill_opacity=1)
        VGroup(core, drum).arrange(RIGHT, buff=1.4).move_to([0, 1.2, 0])
        ct = VGroup(label(r"core", font_size=24, color=YES), label(r"16K words, \ fast", font_size=18,
                                                                    color=GREY_A)).arrange(DOWN, buff=0.1).move_to(core)
        dt = VGroup(label(r"drum", font_size=24, color=LAM), label(r"96K words, \ far slower", font_size=18,
                                                                    color=GREY_A)).arrange(DOWN, buff=0.1).move_to(drum)
        a1 = CurvedArrow(core.get_top() + RIGHT * 0.4, drum.get_top() + LEFT * 1.0, angle=-0.6, color=GREY_B)
        a2 = CurvedArrow(drum.get_bottom() + LEFT * 1.0, core.get_bottom() + RIGHT * 0.4, angle=-0.6, color=GREY_B)
        pl = label(r"pages of 512 words, \ moved automatically", font_size=18, color=GREY_B).next_to(a1, UP, buff=0.05)
        lines = VGroup(
            label(r"programs saw one large memory; \ the hardware and supervisor moved \textbf{pages} between core "
                  r"and drum", font_size=21, color=WHITE),
            label(r"a page-address register per core page: \ match the page number, \ or trap to fetch it", font_size=21,
                  color=GREY_A),
            label(r"Kilburn, \ Edwards, \ Lanigan and Sumner, \ ``One-level storage system'' \ (1962)", font_size=21,
                  color=HEAD),
            label(r"every phone, \ laptop and server since does the same, \ with RAM and flash", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The idea came from Manchester. <bookmark mark='a'/> The Atlas computer had a small fast core memory, and a "
            "drum six times larger and far slower. <bookmark mark='b'/> Its designers let programs "
            "address one large memory, and had the machine move fixed-size pages of five hundred and twelve words "
            "between core and drum, automatically, as they were needed. <bookmark mark='c'/> Each page of core had a "
            "register holding the number of the page it currently held. An address whose page matched one of them ran "
            "at full speed; otherwise the machine trapped and fetched the page. <bookmark mark='d'/> Tom Kilburn and "
            "his colleagues called it a one-level storage system, in 1962. <bookmark mark='e'/> Every phone, laptop and "
            "server since works the same way, with RAM and flash in place of core and drum."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(core), FadeIn(ct), FadeIn(drum), FadeIn(dt))
            vo.wait_until("b")
            self.play(Create(a1), Create(a2), FadeIn(pl), FadeIn(lines[0]))
            for mk, ln in zip("cde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
