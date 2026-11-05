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
        with self.voiceover(
            "Memory is a row of bytes, but most values are bigger than a byte. <bookmark mark='a'/> A 32-bit word "
            "takes four of them, and someone has to decide their order. <bookmark mark='b'/> Big-endian machines "
            "store the most significant byte first, the way we write numbers; network protocols do the same. "
            "<bookmark mark='c'/> Little-endian machines store the least significant byte first. x86, Arm in its "
            "usual mode, RISC-V and Pebble are all little-endian, and this computer confirms it: the four bytes of "
            "zero A zero B zero C zero D sit in memory as zero D, zero C, zero B, zero A. <bookmark mark='d'/> The "
            "names come from a 1980 memo by Danny Cohen, after the war in Gulliver's Travels over which end of an "
            "egg to break. Neither order is better; mixing them up is a classic bug whenever bytes cross a network "
            "or a file."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(val))
            vo.wait_until("b")
            self.play(FadeIn(g1))
            vo.wait_until("c")
            self.play(FadeIn(g2), FadeIn(meas))
            vo.wait_until("d")
            self.play(FadeIn(cohen))
        self.wait(0.3)
        self.clear_scene()

    def padding(self):
        lay = load("layout")
        a, b, n = lay["a"], lay["b"], lay["node"]
        head = label(r"Alignment and padding", font_size=34).to_edge(UP, buff=0.3)
        rule = label(r"a value of $k$ bytes sits at an address divisible by $k$: \ one cache line, \ one bus "
                     r"transfer", font_size=21, color=GREY_A).next_to(head, DOWN, buff=0.25)

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
        with self.voiceover(
            "Values also have to sit at sensible addresses. <bookmark mark='a'/> A four-byte integer normally "
            "lives at an address divisible by four, so that it never straddles two cache lines and can be fetched "
            "in one transfer; Pebble's own loads demand it. <bookmark mark='b'/> So a compiler pads structures. A "
            "character, an integer and a character take six bytes of data, but laid out in that order they take "
            f"{a[0]}: three bytes of padding after the first character so the integer is aligned, and three at the "
            "end so that an array of these stays aligned too. <bookmark mark='c'/> Put the largest field first and "
            f"the same data fits in {b[0]}. <bookmark mark='d'/> The Job's list node, two pointers and two integers, "
            f"is {n[0]} bytes on this 64-bit machine and sixteen on Pebble, where a pointer is four bytes. These "
            "sizes were measured here, by compiling the structures and asking."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(sa))
            vo.wait_until("c")
            self.play(FadeIn(sb))
            vo.wait_until("d")
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
        eq = MathTex(r"\&a[i][j] = a + 4\,(4i + j)", font_size=36, color=HEAD).next_to(flat, DOWN, buff=0.45)
        pts = VGroup(
            label(r"a pointer is an address; \ \texttt{p + 1} adds the size of what it points to", font_size=21,
                  color=GREY_A),
            label(r"\texttt{a[i]} is \texttt{*(a + i)}: \ indexing is pointer arithmetic", font_size=21, color=DATA),
            label(r"nothing checks that \texttt{i} is inside the array: \ chapter 14", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Arrays are the simplest structure of all. <bookmark mark='a'/> A two-dimensional array of three rows "
            "and four columns <bookmark mark='b'/> is stored as one row after another, row-major order, in C and in "
            "most languages; Fortran stores columns instead. <bookmark mark='c'/> So the address of element i, j is "
            "the start of the array plus four bytes times four i plus j. <bookmark mark='d'/> A pointer is just an "
            "address, and adding one to a pointer adds the size of the thing it points to. Indexing an array is "
            "pointer arithmetic: a of i means the contents of a plus i. And nothing in the hardware checks that i "
            "is inside the array. Chapter fourteen shows what that costs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(gl))
            vo.wait_until("b")
            self.play(TransformFromCopy(grid, flat), FadeIn(fl))
            vo.wait_until("c")
            self.play(Write(eq))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.5), run_time=3)
        self.wait(0.3)
        self.clear_scene()
