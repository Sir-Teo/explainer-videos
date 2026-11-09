from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, region)


def byte_row(vals, colors, w=0.75, h=0.55, font_size=20, labels=None):
    g = VGroup()
    for k, (v, c) in enumerate(zip(vals, colors)):
        r = Rectangle(width=w, height=h, stroke_color=GREY_C, stroke_width=1.5, fill_color=c, fill_opacity=0.35)
        t = Text(v, font="DejaVu Sans Mono", font_size=font_size, color=WHITE).move_to(r)
        g.add(VGroup(r, t))
    g.arrange(RIGHT, buff=0)
    if labels:
        for cell, lab in zip(g, labels):
            cell.add(Text(lab, font="DejaVu Sans Mono", font_size=13, color=GREY_B).next_to(cell[0], DOWN, buff=0.06))
    return g


class Data(VoiceoverScene):
    def construct(self):
        self.card()
        self.endian()
        self.padding()
        self.arrays()

    def card(self):
        card = chapter_card(2, r"Data in memory", r"How does a program's data become bytes?", lit=(1980,),
                            extra=((1980, r"Cohen: \ ``On holy wars''"),), part=PART)
        with self.voiceover("Chapter two. Data in memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def endian(self):
        lay = load("layout")
        head = label(r"A word is four bytes: \ in which order?", font_size=34).to_edge(UP, buff=0.35)
        val = Text("0x0A0B0C0D", font="DejaVu Sans Mono", font_size=30, color=CODE).shift(UP * 1.7)
        cols = [DATA, CTRL, YES, FUNC]
        big = byte_row(["0a", "0b", "0c", "0d"], cols, labels=["+0", "+1", "+2", "+3"])
        little = byte_row(lay["bytes"], [cols[3], cols[2], cols[1], cols[0]], labels=["+0", "+1", "+2", "+3"])
        bl = label(r"big-endian: \ the most significant byte first \ (networks, \ IBM mainframes)", font_size=20,
                   color=GREY_A)
        ll = label(r"little-endian: \ the least significant first \ (x86, \ Arm, \ RISC-V, \ Pebble)", font_size=20,
                   color=GREY_A)
        g1 = VGroup(big, bl).arrange(DOWN, buff=0.2)
        g2 = VGroup(little, ll).arrange(DOWN, buff=0.2)
        VGroup(g1, g2).arrange(DOWN, buff=0.55).next_to(val, DOWN, buff=0.45)
        meas = note(r"measured here: \ \texttt{" + " ".join(lay["bytes"]) + r"} \ in memory order", font_size=18
                    ).next_to(g2, DOWN, buff=0.25)
        cohen = label(r"the names: \ Danny Cohen \ (1980), \ after the egg-breaking wars of \textit{Gulliver's "
                      r"Travels}", font_size=20, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover("Memory has byte addresses, while many values span several bytes. <bookmark mark='a'/> A 32-bit word occupies four bytes; endianness specifies their order. <bookmark mark='b'/> Big-endian puts the most significant byte at the lowest address. Many network protocols use this network byte order; each protocol defines its own encoding. <bookmark mark='c'/> Little-endian puts the least significant byte first. x86, the usual Arm configuration and our Pebble use it. The compiled host probe displays zero D, zero C, zero B, zero A for hexadecimal zero A zero B zero C zero D. <bookmark mark='d'/> Danny Cohen's 1980 essay borrowed the names from Gulliver's Travels. Neither order changes the value when decoded consistently; a format mismatch changes what the same bytes mean.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(val), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(g1))
            vo.wait_until('c')
            self.play(FadeIn(g2), FadeIn(meas))
            vo.wait_until('d')
            self.play(FadeIn(cohen))
        self.wait(0.3)
        self.clear_scene()

    def padding(self):
        lay = load("layout")
        a, b, n = lay["a"], lay["b"], lay["node"]
        head = label(r"Alignment and padding", font_size=34).to_edge(UP, buff=0.3)
        rule = label("alignment follows the ABI; \\\\ access cost also depends on boundaries and hardware", font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.25)

        def strip(size, fields, title, src):
            cells = []
            owner = ["pad"] * size
            for name, off, ln, c in fields:
                for k in range(off, off + ln):
                    owner[k] = (name, c)
            g = VGroup()
            for k in range(size):
                o = owner[k]
                c = o[1] if o != "pad" else GREY_E
                r = Rectangle(width=0.42, height=0.45, stroke_color=GREY_C, stroke_width=1,
                              fill_color=c, fill_opacity=0.5 if o != "pad" else 0.25)
                g.add(r)
            g.arrange(RIGHT, buff=0)
            for name, off, ln, c in fields:
                span = VGroup(*g[off:off + ln])
                g.add(Text(name, font="DejaVu Sans Mono", font_size=14, color=WHITE).move_to(span).set_z_index(1))
            t = VGroup(Text(src, font="DejaVu Sans Mono", font_size=17, color=CODE),
                       label(title, font_size=18, color=GREY_B)).arrange(RIGHT, buff=0.4)
            return VGroup(t, g).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        sa = strip(a[0], [("c", a[1], 1, DATA), ("i", a[2], 4, CTRL), ("d", a[3], 1, YES)],
                   rf"{a[0]} bytes: \ 6 of them padding", "struct { char c; int i; char d; }")
        sb = strip(b[0], [("i", b[1], 4, CTRL), ("c", b[2], 1, DATA), ("d", b[3], 1, YES)],
                   rf"{b[0]} bytes: \ largest field first", "struct { int i; char c; char d; }")
        sn = strip(n[0], [("next", n[1], 8, FUNC), ("letters", n[2], 8, DATA), ("len", n[3], 4, CTRL),
                          ("count", n[4], 4, YES)], rf"the Job's list node: \ {n[0]} bytes here, \ 16 on Pebble",
                   "struct node { node *next; char *letters; int length, count; }")
        VGroup(sa, sb, sn).arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(rule, DOWN, buff=0.4)
        cap = note(r"sizes and offsets compiled and measured on this machine \ (x86-64: \ 8-byte pointers)",
                   font_size=17).to_edge(DOWN, buff=0.3)
        with self.voiceover(f"Alignment is part of a machine and language implementation's layout rules. <bookmark mark='a'/> Here a four-byte integer has four-byte alignment. This often makes access simpler and can avoid crossing a normally aligned cache line, but it does not guarantee a particular number of transfers. Pebble requires aligned word accesses; x86 also supports many unaligned accesses. <bookmark mark='b'/> In this compiled structure, char, int, char occupy {a[0]} bytes: padding aligns the integer, then trailing padding aligns consecutive array elements. <bookmark mark='c'/> Reordering the integer first reduces the size to {b[0]}. This is a layout change, so an external binary format must agree. <bookmark mark='d'/> The two-pointer, two-integer node occupies {n[0]} bytes under this host ABI and sixteen on Pebble. Pointer width, alignment and ABI determine these sizes; they are not universal C constants.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(rule), FadeIn(sa), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(sa[1], color=HEAD), run_time=0.6)
            vo.wait_until('c')
            self.play(FadeIn(sb))
            vo.wait_until('d')
            self.play(FadeIn(sn), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def arrays(self):
        head = label(r"Arrays and pointers", font_size=34).to_edge(UP, buff=0.3)
        grid = VGroup()
        for r in range(3):
            for c in range(4):
                sq = Square(side_length=0.55, stroke_color=GREY_C, stroke_width=1.2).move_to([c * 0.58, -r * 0.58, 0])
                grid.add(VGroup(sq, Text(f"{r},{c}", font="DejaVu Sans Mono", font_size=14, color=WHITE).move_to(sq)))
        grid.move_to(LEFT * 4 + UP * 0.8)
        gl = label(r"\texttt{int a[3][4]}", font_size=20, color=CODE).next_to(grid, UP, buff=0.15)
        flat = VGroup(*[VGroup(Rectangle(width=0.5, height=0.45, stroke_color=GREY_C, stroke_width=1,
                                         fill_color=[DATA, CTRL, YES][k // 4], fill_opacity=0.3),
                               Text(f"{k // 4},{k % 4}", font="DejaVu Sans Mono", font_size=12, color=WHITE))
                        for k in range(12)])
        for cell in flat:
            cell[1].move_to(cell[0])
        flat.arrange(RIGHT, buff=0).next_to(grid, RIGHT, buff=0.8)
        fl = label(r"in memory: \ row after row \ (row-major)", font_size=20, color=GREY_A).next_to(flat, UP,
                                                                                                  buff=0.15)
        eq = MathTex("\\operatorname{byteaddr}(a[i][j]) = \\mathrm{base} + 4\\,(4i + j)", font_size=36, color=HEAD).next_to(flat, DOWN, buff=0.45)
        pts = VGroup(
            label("typed pointer arithmetic scales by element size; \\\\ object bounds and lifetime still apply", font_size=21,
                  color=GREY_A),
            label(r"\texttt{a[i]} is \texttt{*(a + i)}: \ indexing is pointer arithmetic", font_size=21, color=DATA),
            label("basic Pebble does not check logical array bounds: chapter 14", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover("An array gives indexing a regular address calculation. <bookmark mark='a'/> Take a C array with three rows and four columns of four-byte integers. <bookmark mark='b'/> Its rows are consecutive: row-major order. Fortran normally uses column-major order; other languages may instead store references to separate row objects. <bookmark mark='c'/> Within this C array, element i, j starts at base plus four times the quantity four i plus j. <bookmark mark='d'/> In C, adding one to a typed pointer advances by the size of its element, and a of i is defined through pointer addition and dereference. These operations have object-bound and lifetime rules: a pointer is more than an unrestricted permission to access any numeric address. Our basic Pebble hardware does not check an array's logical bounds; the Frontier adds a toy capability check.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(grid), FadeIn(gl), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(TransformFromCopy(grid, flat), FadeIn(fl))
            vo.wait_until('c')
            self.play(Write(eq))
            vo.wait_until('d')
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.5), run_time=3)
        self.wait(0.3)
        self.clear_scene()
