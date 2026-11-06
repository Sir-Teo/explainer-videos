from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (FILEC, HEAD, LAM, NO, PART, YES, curve, load, num)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.design_space()
        self.verified()
        self.zoned()
        self.open_problems()

    def card(self):
        card = chapter_card(16, r"Frontier: \ storage that can be trusted", r"What is still unsolved?",
                            lit=(2015, 2017, 2020), extra=((2015, r"FSCQ: \ a verified file system"),
                                                           (2017, r"Monkey"), (2020, r"zoned namespaces")), part=PART)
        with self.voiceover("Chapter sixteen. Frontier: storage that can be trusted."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def design_space(self):
        d = load("frontier")
        head = label(r"The LSM design space", font_size=36).to_edge(UP, buff=0.3)
        rows = d["monkey"]
        ax = Axes(x_range=[0, 10, 2], y_range=[-2, 1, 1], x_length=6.4, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-2.2, -0.3, 0])
        xt = VGroup(*[label(str(x), font_size=16, color=GREY_B).next_to(ax.c2p(x, -2), DOWN, buff=0.1)
                      for x in (2, 4, 6, 8, 10)])
        yt = VGroup(*[MathTex(rf"10^{{{y}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                      for y in (-2, -1, 0, 1)])
        xl = label(r"Bloom filter memory, \ bits per key", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yl = label(r"wasted reads per lookup of an absent key", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        xs = [r["bits"] for r in rows]
        cu = curve(ax, xs, [math.log10(r["uniform"]) for r in rows], NO)
        cm = curve(ax, xs, [math.log10(r["monkey"]) for r in rows], YES)
        r10 = rows[-1]
        notes = VGroup(
            label(r"the same bits per key at every level", font_size=19, color=NO),
            label(r"Monkey \ (Dayan, Athanassoulis and Idreos, 2017): \\ more bits for the small levels, \ "
                  r"false-positive \\ rates proportional to level size", font_size=19, color=YES),
            label(rf"at 10 bits a key: \ {r10['uniform']:.3f} against {r10['monkey']:.3f}, \\ "
                  rf"${r10['uniform'] / r10['monkey']:.1f}\times$ fewer, \ for no extra memory", font_size=19,
                  color=WHITE),
            label(r"Dostoevsky \ (2018), \ lazy leveling, \ and tuning \\ for a changing workload: \ open", font_size=19,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 0.0, 0])
        foot = label(rf"a leveled tree of {d['levels']} levels, \ ratio {d['ratio']}: \ the analytic model of the paper",
                     font_size=16, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Chapter 14 found that no LSM design wins on every cost. Research now treats the whole space as one "
            "continuum to be navigated. <bookmark mark='a'/> A small example. The usual tree gives every run the same "
            "number of Bloom filter bits per key, so every level has the same false-positive rate, and a lookup for "
            "an absent key wastes that much at each level. <bookmark mark='b'/> Dayan, Athanassoulis and Idreos "
            "observed in 2017 that the levels differ enormously in size. Bits spent on a small level are cheap, so "
            "give the small levels more and the big one fewer, until each level's false-positive rate is proportional "
            "to its size. <bookmark mark='c'/> With the same total memory, the wasted reads fall three and a half "
            "times. <bookmark mark='d'/> Their next design, Dostoevsky, mixed leveling and tiering within one tree; "
            "how to choose and change such a design as a workload drifts is still open."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(foot))
            vo.wait_until("a")
            self.play(Create(cu), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(cm), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def verified(self):
        d = load("frontier")
        head = label(r"Verified crash consistency", font_size=36).to_edge(UP, buff=0.3)
        g = d["grow"]
        W = 5.0
        mx = math.log10(max(r["states"] for r in g))
        bars = VGroup()
        for k, r in enumerate(g):
            w = max(0.1, W * math.log10(r["states"]) / mx)
            rect = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=NO, fill_opacity=0.8)
            bars.add(VGroup(label(rf"{r['writes']} writes", font_size=18, color=GREY_A), rect,
                            label(rf"{num(r['states'])} crash states", font_size=18, color=WHITE)))
        for k, b in enumerate(bars):
            b[0].move_to([-5.3, 1.6 - 0.6 * k, 0], aligned_edge=LEFT)
            b[1].move_to([-3.7, 1.6 - 0.6 * k, 0], aligned_edge=LEFT)
            b[2].next_to(b[1], RIGHT, buff=0.15)
        bl = label(r"our checker, \ no ordering: \ $2^k$ for $k$ writes between flushes \ (log scale)", font_size=17,
                   color=GREY_B).next_to(bars, UP, buff=0.2).align_to(bars, LEFT)
        items = VGroup(*[VGroup(label(a, font_size=20, color=c), label(b, font_size=17, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05) for a, b, c in (
            (r"FSCQ \ (Chen et al., 2015)", r"a file system proved correct in Coq: \ after any crash, \ recovery "
                                            r"restores a state the specification allows", YES),
            (r"Yggdrasil \ (Sigurbjarnarson et al., 2016)", r"file systems verified push-button, \ by an SMT solver",
             LAM),
            (r"CrashMonkey \ (Mohan et al., 2018)", r"bounded, systematic crash testing of Linux file systems: \ new "
                                                    r"bugs in widely used ones", HEAD),
            (r"still open", r"verified file systems as fast as ext4, \ with concurrency and delayed allocation; \ "
                            r"a precise model of what real drives promise", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        with self.voiceover(
            "Our checker tried every crash, and that does not scale. <bookmark mark='a'/> With k writes between "
            "flushes the disk can be left in two to the k states: nine for three writes, over a thousand for ten. "
            "Exhaustive checking works for small operations, not for whole programs. <bookmark mark='b'/> So "
            "researchers prove instead. FSCQ, in 2015, was a file system proved correct in the Coq proof assistant, "
            "with a logic for crashes: whatever point it crashes at, recovery leads to a state its specification "
            "allows. <bookmark mark='c'/> Yggdrasil made such proofs push-button, by handing them to an SMT solver. "
            "<bookmark mark='d'/> CrashMonkey went the other way, testing Linux file systems systematically over "
            "short sequences of operations, and found new bugs in widely used ones. <bookmark mark='e'/> What is "
            "missing is a verified file system as fast as ext4, with concurrency and delayed allocation, and a precise "
            "model of what real drives actually promise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.25))
            for mk, it in zip("bcde", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def zoned(self):
        d = load("frontier")
        head = label(r"Zoned storage: \ the host does the cleaning", font_size=36).to_edge(UP, buff=0.3)
        zones = VGroup()
        for k, fill in enumerate((1.0, 1.0, 0.55, 0.0, 0.0)):
            z = Rectangle(width=2.0, height=0.7, stroke_color=GREY_B, stroke_width=1.5)
            f = Rectangle(width=max(0.01, 2.0 * fill), height=0.7, stroke_width=0, fill_color=FILEC,
                          fill_opacity=0.5).align_to(z, LEFT)
            wp = Line(UP * 0.4, DOWN * 0.4, color=HEAD, stroke_width=3).move_to(z.get_left() + RIGHT * 2.0 * fill) \
                if 0 < fill < 1 else VectorizedPoint()
            zones.add(VGroup(z, f, wp, label(rf"zone {k}", font_size=15, color=GREY_B).next_to(z, DOWN, buff=0.08)))
        zones.arrange(RIGHT, buff=0.15).next_to(head, DOWN, buff=0.6)
        wpl = label(r"write pointer: \ append only; \ reset a whole zone at once", font_size=18, color=HEAD).next_to(
            zones, DOWN, buff=0.35)
        z = d["zns"]
        lines = VGroup(
            label(r"shingled disks \ (tracks overlap like roof tiles) \ and NVMe zoned SSDs \ (2020) \ expose "
                  r"zones", font_size=20, color=WHITE),
            label(rf"no hidden garbage collector: \ the host writes sequentially: \ amplification {z['sequential']:.1f}, "
                  rf"\ against {z['random']:.1f} for random writes on 7\% spare \ (chapter 3's simulator)",
                  font_size=20, color=YES),
            label(r"log-structured designs fit at once: \ LFS, \ LSM trees \ (RocksDB on zones), \ F2FS", font_size=20,
                  color=LAM),
            label(r"open: \ general file systems and databases on zones, \ without the device's help", font_size=20,
                  color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Chapter 3's translation layer hides flash behind the old interface of rewritable blocks, and pays for it "
            "in write amplification and spare capacity. Zoned storage stops pretending. <bookmark mark='a'/> Shingled "
            "disks, whose tracks overlap like roof tiles, and the zoned SSDs standardized for NVMe in 2020, divide "
            "themselves into zones. Each zone is written strictly in order, at a write pointer, and reset as a "
            "whole. <bookmark mark='b'/> The device no longer cleans; the host does, and it can write sequentially by "
            "design. In our simulator, rewriting pages in order gives an amplification of exactly one, against seven "
            "and a half for random writes on the same spare space. <bookmark mark='c'/> Log-structured software fits "
            "zones naturally: LFS, LSM trees, flash file systems. <bookmark mark='d'/> Bringing everything else along "
            "is open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(zones), FadeIn(wpl))
            for mk, ln in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def open_problems(self):
        head = label(r"Open problems", font_size=36).to_edge(UP, buff=0.3)
        probs = VGroup(*[label(t, font_size=21, color=WHITE) for t in (
            r"1. \ A precise, \ portable model of what file systems promise after a crash, \ that programs can rely on",
            r"2. \ Verified file systems with the performance of the best unverified ones",
            r"3. \ Choosing and re-tuning an LSM design automatically as the workload changes",
            r"4. \ Placing data by its lifetime, \ unknown in advance, \ to minimise flash write amplification",
            r"5. \ General-purpose file systems and databases on zoned devices, \ at full speed",
            r"6. \ Durability models that match the field: \ correlated failures across disks, \ racks and sites",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        star = label(r"$\bigstar$ \ the part's research problem takes the fewest flushes that make an operation safe",
                     font_size=19, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Six problems at the frontier. <bookmark mark='a'/> A precise, portable model of what a file system "
            "promises after a crash, one that programs could rely on everywhere. <bookmark mark='b'/> Verified file "
            "systems that are as fast as the best unverified ones. <bookmark mark='c'/> Choosing, and re-choosing, an "
            "LSM tree's design automatically as its workload changes. <bookmark mark='d'/> Placing data on flash by "
            "how long it will live, which nobody knows in advance, so that whole blocks die together. <bookmark "
            "mark='e'/> File systems and databases that run on zoned devices at full speed. <bookmark mark='f'/> And "
            "models of durability that match the field, where failures are correlated across disks, racks and sites. "
            "The research problem at the end of this part asks a small, sharp question of its own: the fewest "
            "flushes that make an operation safe."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", probs):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
