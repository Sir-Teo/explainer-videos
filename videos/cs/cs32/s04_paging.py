from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, DATA, HEAD, KERN, L2C, LAM, NO, OFFC, PART, YES, addr_bits, grid_table,
                                   hx, load, mono)


def table_box(title, rows, color, hl):
    """A page-table excerpt: (index, entry) rows; row `hl` highlighted."""
    g = VGroup()
    for k, (i, e) in enumerate(rows):
        r = Rectangle(width=3.4, height=0.46, stroke_color=color, stroke_width=1.2,
                      fill_color=color if k == hl else BG, fill_opacity=0.35 if k == hl else 1)
        t = mono(f"{i:>4}  {e}", 19, WHITE).move_to(r)
        g.add(VGroup(r, t))
    g.arrange(DOWN, buff=0)
    t = label(title, font_size=19, color=color).next_to(g, UP, buff=0.08)
    return VGroup(t, g)


class Paging(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.bits()
        self.walk()

    def card(self):
        card = chapter_card(3, r"Paging", r"How do you translate an address in pieces?", lit=(1962,),
                            extra=((1962, r"Atlas"),), part=PART)
        with self.voiceover("Chapter three. Paging."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def split(self):
        d = load("sameva")
        va = d["va"]
        head = label(r"A virtual address, \ in three parts", font_size=36).to_edge(UP, buff=0.3)
        bits = addr_bits(va, cell=0.33, font=16).move_to([0, 1.3, 0])
        vl = mono(f"{hx(va)} = 0b" + format(va, "032b"), 20, WHITE).next_to(bits, UP, buff=0.4)
        lines = VGroup(
            label(r"pages of 4 KiB: \ the low 12 bits are the \textbf{offset} inside the page, \ never translated",
                  font_size=22, color=OFFC),
            label(r"the high 20 bits are the \textbf{virtual page number}: \ that is what the table maps", font_size=22,
                  color=WHITE),
            label(r"split again, \ 10 and 10: \ an index into a first-level table, \ then a second", font_size=22,
                  color=L2C),
            label(r"any free frame holds any page: \ no fragmentation between pages, \ at most a part page wasted "
                  r"inside", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(bits, DOWN, buff=0.6)
        with self.voiceover(
            "Paging cuts memory into pieces of one size, four kibibytes in our machine, and translates each piece "
            "separately. <bookmark mark='a'/> Here is the address from the start of this part, in binary. <bookmark "
            "mark='b'/> The low twelve bits are the offset within the page, and pass through untouched. <bookmark "
            "mark='c'/> The high twenty bits are the virtual page number, and that is what gets translated. <bookmark "
            "mark='d'/> Our hardware splits the page number again, into two ten-bit indexes, for the two levels of "
            "table you will see in a moment. <bookmark mark='e'/> And because every frame of physical memory is the "
            "same size, any free frame can hold any page. Fragmentation between pieces is gone; at most part of the "
            "last page of each region is wasted."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(vl), FadeIn(bits.fields))
            vo.wait_until("b")
            self.play(Indicate(bits.fields[2], color=OFFC), FadeIn(bits.tags[2]), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(bits.fields[0], bits.fields[1]), color=WHITE), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(bits.tags[0]), FadeIn(bits.tags[1]), FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def bits(self):
        head = label(r"A page-table entry", font_size=36).to_edge(UP, buff=0.3)
        cells = VGroup()
        for name, w, c in (("physical frame number: 20 bits", 6.0, YES), ("..", 0.8, GREY_D), ("D", 0.5, NO),
                           ("A", 0.5, LAM), ("..", 0.5, GREY_D), ("U", 0.5, HEAD), ("X", 0.5, DATA), ("W", 0.5, DATA),
                           ("R", 0.5, DATA), ("V", 0.5, YES)):
            r = Rectangle(width=w, height=0.7, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.15)
            cells.add(VGroup(r, label(name, font_size=18, color=WHITE).move_to(r)))
        cells.arrange(RIGHT, buff=0).next_to(head, DOWN, buff=0.6)
        tab = grid_table([r"bit", r"meaning", r"who sets it"], [
            [r"V", r"valid: \ the page is mapped", r"the kernel"],
            [r"R, \ W, \ X", r"read, \ write, \ execute allowed", r"the kernel"],
            [r"U", r"user mode may touch it", r"the kernel"],
            [r"A", r"accessed since the bit was cleared", r"the hardware, \ on every access"],
            [r"D", r"dirty: \ written since loaded", r"the hardware, \ on every write"],
        ], widths=[1.6, 5.2, 4.2], row_h=0.48, font_size=20, mono_cols=())
        tab.next_to(cells, DOWN, buff=0.45)
        line = label(r"A tells the kernel which pages are in use \ (chapter 7); \ D which must be written back before "
                     r"reuse", font_size=21, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Each entry in a page table is one word. <bookmark mark='a'/> The top twenty bits name the physical frame. "
            "The low bits are flags. <bookmark mark='b'/> Valid means the page is mapped at all. Read, write and execute "
            "say what may be done with it, so code can be execute-only and data never executed. User says whether a "
            "user-mode program may touch it. <bookmark mark='c'/> And two bits are set by the hardware itself: "
            "accessed, on every use, and dirty, on every write. <bookmark mark='d'/> The kernel reads them back. "
            "Accessed tells it which pages are in use, which chapter seven needs; dirty tells it which pages must be "
            "written to disk before their frame is reused."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[1], *tab.cells[2],
                                                                                     *tab.cells[3])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[4], *tab.cells[5])))
            vo.wait_until("d")
            self.play(FadeIn(line))
        self.wait(0.3)
        self.clear_scene()

    def walk(self):
        d = load("sameva")
        sp = d["split"]
        head = label(rf"Walking {hx(d['va'])} \ in each process", font_size=34).to_edge(UP, buff=0.3)
        cols = VGroup()
        for w, color in zip(d["walks"], (DATA, HEAD)):
            root = mono(f"ptbr = {hx(w['root'])}", 20, color)
            l1 = table_box(r"L1 table", [(0, "superpage"), (sp["l1"], hx(w["e1"]))], color, 1)
            l2 = table_box(r"L2 table", [(sp["l2"] - 1, "..."), (sp["l2"], hx(w["e2"])), (sp["l2"] + 1, "...")],
                           color, 1)
            pa = mono(f"frame {hx(w['pa'] & ~0xFFF)} + {sp['off']}", 20, YES)
            val = label(rf"holds {w['value']}", font_size=21, color=YES)
            col = VGroup(label(w["name"].replace("P", r"process \ "), font_size=24, color=color), root, l1, l2, pa,
                         val).arrange(DOWN, buff=0.3)
            cols.add(col)
        cols.arrange(RIGHT, buff=3.0).next_to(head, DOWN, buff=0.3)
        arrows = VGroup()
        for col, color in zip(cols, (DATA, HEAD)):
            for a, b in ((col[1], col[2]), (col[2], col[3]), (col[3], col[4])):
                arrows.add(Arrow(a.get_bottom(), b.get_top(), buff=0.05, color=color, stroke_width=2,
                                 max_tip_length_to_length_ratio=0.25))
        note = VGroup(
            label(rf"L1 index {sp['l1']}, \ L2 index {sp['l2']}, \ offset {sp['off']}: \ the same in both", font_size=20,
                  color=WHITE),
            label(r"different tables, \ different frames: \ the kernel chose them; \ the program never sees them",
                  font_size=20, color=YES),
            label(r"entry 0 of every L1 table maps the kernel \ (chapter 10)", font_size=20, color=KERN),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the walk itself, done in hardware on every access that misses the cache of chapter five. <bookmark "
            "mark='a'/> The control register p-t-b-r holds the physical address of the current process's first-level "
            "table. The first ten bits of the address pick an entry there, which points to a second-level table. "
            "<bookmark mark='b'/> The next ten bits pick an entry in that, which names the frame. Add the offset, and "
            "that is the physical address. <bookmark mark='c'/> The two processes use the same indexes, but their "
            "tables, built by the kernel, point to different frames, so the same address holds one in one process and "
            "two in the other. <bookmark mark='d'/> Entry zero of every first-level table is the same: it maps the "
            "kernel, as chapter ten explains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(cols[0][:2], cols[1][:2])))
            vo.wait_until("a")
            self.play(FadeIn(cols[0][2]), FadeIn(cols[1][2]), FadeIn(arrows[0]), FadeIn(arrows[3]))
            vo.wait_until("b")
            self.play(FadeIn(cols[0][3]), FadeIn(cols[1][3]), FadeIn(arrows[1]), FadeIn(arrows[4]), FadeIn(arrows[2]),
                      FadeIn(arrows[5]), FadeIn(cols[0][4:]), FadeIn(cols[1][4:]))
            vo.wait_until("c")
            self.play(FadeIn(note[0]), FadeIn(note[1]))
            vo.wait_until("d")
            self.play(FadeIn(note[2]))
        self.wait(0.3)
        self.clear_scene()
