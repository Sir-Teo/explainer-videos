from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, HEAD, KERN, L1C, L2C, LAM, NO, OFFC, PART, YES, grid_table, load)


def human(b):
    for unit, n in (("TiB", 1 << 40), ("GiB", 1 << 30), ("MiB", 1 << 20), ("KiB", 1 << 10)):
        if b >= n:
            return f"{b / n:.0f} {unit}"
    return f"{b} B"


def slots(n, used, color, w=0.11, h=0.34):
    g = VGroup(*[Rectangle(width=w, height=h, stroke_width=0.3, stroke_color=GREY_D,
                           fill_color=color if i in used else BG, fill_opacity=0.9 if i in used else 1)
                 for i in range(n)]).arrange(RIGHT, buff=0)
    return g


class Tables(VoiceoverScene):
    def construct(self):
        self.card()
        self.tree()
        self.sizes()

    def card(self):
        card = chapter_card(4, r"Multi-level page tables", r"How big must a page table be?", lit=(2019,),
                            extra=((2019, r"five-level paging"),), part=PART)
        with self.voiceover("Chapter four. Multi-level page tables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tree(self):
        d = load("sameva")
        maps = d["walks"][0]["maps"]
        head = label(r"A page table is a radix tree", font_size=36).to_edge(UP, buff=0.3)
        root = slots(64, {0, 1}, L1C).move_to([0, 1.9, 0])
        rl = label(r"L1: \ 1{,}024 entries \ (64 drawn); \ 2 used", font_size=19, color=L1C).next_to(root, UP,
                                                                                                  buff=0.1)
        used = sorted({((va >> 12) & 0x3FF) for va, _, _ in maps})
        l2 = slots(64, {u for u in used if u < 64} | {63}, L2C).move_to([1.6, 0.2, 0])
        l2l = label(rf"process 1's L2: \ {len(used)} of 1{{,}}024 entries used", font_size=19, color=L2C).next_to(
            l2, DOWN, buff=0.1)
        kern = RoundedRectangle(width=3.0, height=0.8, corner_radius=0.1, stroke_color=KERN, fill_color=BG,
                                fill_opacity=1).move_to([-4.0, 0.2, 0])
        kl = label(r"entry 0: \ a 4 MiB superpage, \\ the kernel", font_size=18, color=KERN).move_to(kern)
        a1 = Arrow(root[0].get_bottom(), kern.get_top(), buff=0.05, color=KERN, stroke_width=2)
        a2 = Arrow(root[1].get_bottom(), l2.get_top() + LEFT * 2.5, buff=0.05, color=L2C, stroke_width=2)
        lines = VGroup(
            label(r"each level resolves 10 bits of the page number: \ like a trie on the address \ (Part 21)",
                  font_size=21, color=WHITE),
            label(r"empty subtrees cost nothing: \ a null entry at L1 covers 4 MiB with no L2 table at all",
                  font_size=21, color=YES),
            label(r"our process: \ 8 KiB of tables \ (one L1, \ one L2) \ instead of a 4 MiB flat array", font_size=21,
                  color=HEAD),
            label(r"the price: \ a translation now takes one memory read per level", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why two levels? A flat table, one entry for each of the million pages in a thirty-two-bit address space, "
            "would need four mebibytes per process, almost all of it saying not mapped. <bookmark mark='a'/> Instead "
            "the table is a tree. The first level has a thousand and twenty-four entries, each covering four "
            "mebibytes. <bookmark mark='b'/> In our processes only two are used: entry zero maps the kernel with one "
            "large page, and entry one points to the process's second-level table. <bookmark mark='c'/> That table "
            "has entries for the pages actually mapped. <bookmark mark='d'/> Each level resolves ten bits of the page "
            "number, like the tries of Part 21. <bookmark mark='e'/> An empty first-level entry covers four mebibytes "
            "with no second-level table at all. <bookmark mark='f'/> So our process needs eight kibibytes of table "
            "instead of four mebibytes. <bookmark mark='g'/> The price is a memory read per level on every "
            "translation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(root), FadeIn(rl))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(kern), FadeIn(kl))
            vo.wait_until("c")
            self.play(GrowArrow(a2), FadeIn(l2), FadeIn(l2l))
            for mk, ln in zip("defg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def sizes(self):
        d = load("tables")
        head = label(r"Wider addresses, \ deeper trees", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"machine", r"virtual bits", r"levels", r"a flat table would be"],
                         [[r["name"], str(r["bits"]), str(r["levels"]), human(r["flat_bytes"])] for r in d["rows"]],
                         widths=[5.4, 2.2, 1.6, 3.6], row_h=0.55, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        bits = VGroup(*[VGroup(Rectangle(width=w, height=0.5, stroke_color=c, fill_color=c, fill_opacity=0.18),
                               label(t, font_size=16, color=WHITE)) for t, w, c in (
            (r"9", 0.9, L1C), (r"9", 0.9, L2C), (r"9", 0.9, LAM), (r"9", 0.9, HEAD), (r"offset 12", 1.6, OFFC))])
        for b in bits:
            b[1].move_to(b[0])
        bits.arrange(RIGHT, buff=0.04).next_to(tab, DOWN, buff=0.45)
        bl = label(r"x86-64: \ 48 bits, \ 9 + 9 + 9 + 9 + 12, \ 512 eight-byte entries per 4 KiB table", font_size=19,
                   color=GREY_A).next_to(bits, DOWN, buff=0.1)
        lines = VGroup(
            label(r"five levels since 2019 \ (57 bits, \ 128 PiB): \ a TLB miss can cost five memory reads",
                  font_size=21, color=NO),
            label(r"\textbf{inverted} tables \ (PowerPC, \ IA-64): \ one entry per physical frame, \ found by hashing "
                  r"the virtual page", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Real machines go deeper. <bookmark mark='a'/> For our thirty-two-bit addresses, a flat table would be four "
            "mebibytes. For x86-64's forty-eight bits, five hundred and twelve gibibytes, per process. <bookmark "
            "mark='b'/> So x86-64 uses four levels of nine bits each, with five hundred and twelve eight-byte entries "
            "in each four-kibibyte table. <bookmark mark='c'/> Since 2019, servers can use five levels, for "
            "fifty-seven-bit addresses, so a miss in the translation cache can cost five memory reads before the real "
            "one. <bookmark mark='d'/> Some designs invert the table instead, with one entry per physical frame, found "
            "by hashing the virtual page number; PowerPC and Itanium did this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(bits), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()
