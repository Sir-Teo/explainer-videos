from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, flow_box, grid_table, load)


def fmt_n(v):
    return f"{v:,}".replace(",", "{,}")


class Faults(VoiceoverScene):
    def construct(self):
        self.card()
        self.flow()
        self.swap()
        self.costs()

    def card(self):
        card = chapter_card(6, r"Page faults", r"What happens when the page is not there?", lit=(1962,),
                            extra=((1962, r"Atlas: \ demand paging"),), part=PART)
        with self.voiceover("Chapter six. Page faults."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def flow(self):
        p = load("protect")
        head = label(r"A page fault, \ end to end", font_size=36).to_edge(UP, buff=0.3)
        steps = [(r"\texttt{sw t1, 0(t0)}", DATA), (r"TLB miss", GREY_B), (r"walk: \ entry not valid", NO),
                 (r"trap: \ cause 15", KERN), (r"kernel: \ in range? \ get a frame", KERN),
                 (r"zero it \ (or read it from disk)", LAM), (r"write the entry", KERN), (r"\texttt{eret}: \ retry", YES)]
        seq = [flow_box(t, c, 2.9, 0.62, 17) for t, c in steps]
        grid = VGroup(*(seq[:4] + seq[4:][::-1]))           # a snake: the second row runs right to left
        grid.arrange_in_grid(rows=2, cols=4, buff=(0.45, 0.7)).next_to(head, DOWN, buff=0.6)
        boxes = VGroup(*seq)
        arrs = VGroup()
        for a, b in zip(seq[:3], seq[1:4]):
            arrs.add(Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2))
        arrs.add(Arrow(seq[3].get_bottom(), seq[4].get_top(), buff=0.08, color=GREY_B, stroke_width=2))
        for a, b in zip(seq[4:7], seq[5:8]):
            arrs.add(Arrow(a.get_left(), b.get_right(), buff=0.08, color=GREY_B, stroke_width=2))
        lines = VGroup(
            label(r"the faulting instruction never happened: \ the kernel fixes the mapping, \ and the hardware runs it "
                  r"again", font_size=21, color=WHITE),
            label(r"\textbf{demand paging}: \ map nothing until it is touched; \ zero pages for the heap and stack, "
                  r"\ file pages read from disk", font_size=21, color=YES),
            label(rf"in PebbleOS: \ a program touching 16 new heap pages takes {p['page_faults']} faults, \ about "
                  r"3{,}300 kernel instructions each, \ mostly zeroing", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "What happens when a program touches a page that is not mapped? <bookmark mark='a'/> It executes a store. "
            "The TLB has no entry, so the hardware walks the table, and finds the entry not valid. <bookmark mark='b'/> "
            "It traps, with cause fifteen and the address in t-val. <bookmark mark='c'/> The kernel checks that the "
            "address lies inside the process's memory, and takes a free frame. It fills the frame: with zeros for a new "
            "page of heap or stack, or with data read from the disk. It writes the entry, and returns with e-ret to the "
            "very same store, which now succeeds. <bookmark mark='d'/> The faulting instruction never happened, so it "
            "can simply happen again. <bookmark mark='e'/> This is demand paging: map nothing until it is touched. "
            "<bookmark mark='f'/> PebbleOS now does it. A program that touches sixteen new pages of heap takes "
            "sixteen faults, each about three thousand three hundred kernel instructions, nearly all of them writing "
            "the zeros."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), GrowArrow(arrs[0]), FadeIn(boxes[1]), GrowArrow(arrs[1]), FadeIn(boxes[2]))
            vo.wait_until("b")
            self.play(GrowArrow(arrs[2]), FadeIn(boxes[3]))
            vo.wait_until("c")
            self.play(GrowArrow(arrs[3]), LaggedStart(*[FadeIn(boxes[i]) for i in (4, 5, 6, 7)], lag_ratio=0.4),
                      LaggedStart(*[GrowArrow(a) for a in arrs[4:]], lag_ratio=0.4), run_time=2.5)
            for mk, ln in zip("def", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def swap(self):
        d = load("dirty")
        r8 = next(r for r in d["rows"] if r["k"] == 8)
        head = label(r"Where an evicted page goes", font_size=36).to_edge(UP, buff=0.3)
        frames = VGroup()
        marks = ["", "D", "", "D", "D", "", "", "D"]
        for i, m in enumerate(marks):
            sq = Square(0.8, stroke_color=DATA, stroke_width=1.6, fill_color=DATA, fill_opacity=0.18)
            g = VGroup(sq, label(rf"page {i}", font_size=16, color=WHITE).move_to(sq).shift(UP * 0.12))
            if m:
                g.add(label(r"D", font_size=18, color=NO).move_to(sq).shift(DOWN * 0.2))
            frames.add(g)
        frames.arrange(RIGHT, buff=0.15).next_to(head, DOWN, buff=0.5)
        fl = label(r"physical frames \ (D: \ written since loaded)", font_size=18, color=GREY_A).next_to(frames, UP,
                                                                                                       buff=0.1)
        fl.next_to(head, DOWN, buff=0.12)
        frames.next_to(fl, DOWN, buff=0.15)
        disk = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.12, stroke_color=LAM, fill_color=BG,
                                       fill_opacity=1), label(r"swap space \ (a disk partition or file)", font_size=18,
                                                              color=LAM))
        disk[1].move_to(disk[0])
        disk.move_to([2.6, -0.6, 0])
        fil = VGroup(RoundedRectangle(width=3.6, height=1.0, corner_radius=0.12, stroke_color=YES, fill_color=BG,
                                      fill_opacity=1), label(r"the file it came from", font_size=18, color=YES))
        fil[1].move_to(fil[0])
        fil.move_to([-2.6, -0.6, 0])
        a_clean = Arrow(frames[2].get_bottom(), fil.get_top(), buff=0.1, color=YES, stroke_width=2.5)
        a_dirty = Arrow(frames[3].get_bottom(), disk.get_top(), buff=0.1, color=NO, stroke_width=2.5)
        cl = label(r"clean: \ just drop it, \ read it again later", font_size=18, color=YES).next_to(a_clean, LEFT,
                                                                                                    buff=0.1)
        dl = label(r"dirty: \ write it out first", font_size=18, color=NO).next_to(a_dirty, RIGHT, buff=0.1)
        pct = r8["dirty"] / r8["evictions"]
        lines = VGroup(
            label(r"heap and stack pages have no file: \ once dirty, \ they can only go to swap", font_size=21,
                  color=WHITE),
            label(rf"the Job's trace under LRU with 8 frames: \ {fmt_n(r8['dirty'])} of {fmt_n(r8['evictions'])} "
                  rf"evictions dirty \ ({pct * 100:.0f}\%), \ each an extra disk write",
                  font_size=21, color=NO),
            label(r"so a daemon \ (Linux's \texttt{kswapd}) \ cleans pages ahead of time, \ in batches, \ and keeps "
                  r"free frames ready", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "When memory is full, a fault must first free a frame, and the page in it has to go somewhere. <bookmark "
            "mark='a'/> The dirty bit from chapter three decides where. <bookmark mark='b'/> A clean page, unchanged "
            "since it was read from a file, can simply be dropped: if it is needed again, it is read again. <bookmark "
            "mark='c'/> A dirty page must be written out first, and a page of heap or stack has no file at all, so it "
            "goes to swap space, a partition or file set aside for exactly this. <bookmark mark='d'/> That doubles the "
            "cost of the fault. On the Job's trace, with eight frames under LRU, forty-four percent of evictions are "
            "dirty. <bookmark mark='e'/> So kernels do not wait for the fault. A page-out daemon, kswapd in Linux, "
            "writes dirty pages back in the background, in batches, and keeps a pool of free frames ready, so that a "
            "fault only has to read."
        ) as vo:
            self.play(FadeIn(head), FadeIn(fl), LaggedStart(*[FadeIn(f[:2]) for f in frames], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(*[FadeIn(f[2]) for f in frames if len(f) > 2])
            vo.wait_until("b")
            self.play(FadeIn(fil), GrowArrow(a_clean), FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(disk), GrowArrow(a_dirty), FadeIn(dl), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def costs(self):
        st = load("staircase")
        e = load("eat")
        head = label(r"What a fault costs", font_size=36).to_edge(UP, buff=0.3)
        meas = VGroup(
            label(rf"on this machine: \ touching a mapped page {st['touch_ns']:.0f} ns; \ the first touch of a new page "
                  rf"{st['fault_ns'] / 1000:.1f} $\mu$s \ (a fault, \ zeroing 4 KiB)", font_size=21, color=WHITE),
            label(r"a fault that must read the disk: \ about 100 $\mu$s on flash, \ 8 ms on a spinning disk",
                  font_size=21, color=NO),
        ).arrange(DOWN, buff=0.15).next_to(head, DOWN, buff=0.4)
        f = MathTex(r"\text{effective access time} = (1 - p)\cdot 100\,\text{ns} + p \cdot t_{\text{fault}}",
                    font_size=34, color=HEAD).next_to(meas, DOWN, buff=0.35)
        rows = []
        for pv in (1e-3, 1e-4, 1e-5, 1e-6, 1e-7):
            ssd = next(r for r in e["rows"] if r["p"] == pv and r["dev"] == "ssd")
            hdd = next(r for r in e["rows"] if r["p"] == pv and r["dev"] == "hdd")
            rows.append([rf"$10^{{{int(round(math.log10(pv)))}}}$", f"{ssd['eat_ns']:,.0f} ns".replace(
                ",", "{,}"), f"{hdd['eat_ns']:,.0f} ns".replace(",", "{,}")])
        tab = grid_table([r"faults per access $p$", r"flash \ (100 $\mu$s)", r"disk \ (8 ms)"], rows,
                         widths=[3.6, 3.0, 3.0], row_h=0.44, font_size=20, mono_cols=())
        tab.next_to(f, DOWN, buff=0.35)
        line = label(r"to stay within 10\% of memory speed with a disk, \ fewer than one fault in a million accesses",
                     font_size=21, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How much does a fault cost? <bookmark mark='a'/> On this machine, touching a page that is already mapped "
            "takes twenty-five nanoseconds. The first touch of a brand-new page, a fault plus zeroing four kibibytes, "
            "takes almost two microseconds. <bookmark mark='b'/> A fault that must read from storage is far worse: "
            "around a hundred microseconds from flash, and eight milliseconds from a spinning disk. <bookmark "
            "mark='c'/> So the average cost of a memory access depends on how often it faults. <bookmark mark='d'/> "
            "With a disk, one fault in a thousand accesses makes memory eighty times slower. Even one in a million "
            "adds eight percent. <bookmark mark='e'/> A system that pages to disk is usable only while faults are rarer "
            "than one in a million, which is why running out of memory feels like falling off a cliff."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(meas[0]))
            vo.wait_until("b")
            self.play(FadeIn(meas[1]))
            vo.wait_until("c")
            self.play(FadeIn(f))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
            vo.wait_until("e")
            self.play(FadeIn(line))
        self.wait(0.3)
        self.clear_scene()
