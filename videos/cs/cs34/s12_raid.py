from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (BITS, FILEC, HEAD, KERN, LAM, NO, PART, YES, blk, grid_table, load)

CELLC = {"D": FILEC, "M": LAM, "P": BITS, "Q": KERN}


def layout_grid(lay, w=0.78, h=0.42, font=14):
    g = VGroup()
    for row in lay:
        r = VGroup(*[blk(t, CELLC[t[0]], w=w, h=h, font=font, fill=0.3) for t in row]).arrange(RIGHT, buff=0.06)
        g.add(r)
    g.arrange(DOWN, buff=0.06)
    heads = VGroup(*[label(rf"disk {k}", font_size=13, color=GREY_B).next_to(c, UP, buff=0.08)
                     for k, c in enumerate(g[0])])
    return VGroup(heads, g)


class Raid(VoiceoverScene):
    def construct(self):
        self.card()
        self.levels()
        self.parity()
        self.rebuild()

    def card(self):
        card = chapter_card(11, r"RAID", r"Can many cheap disks be faster and safer than one?", lit=(1988,),
                            extra=((1988, r"Patterson, Gibson and Katz: \ RAID"),), part=PART)
        with self.voiceover("Chapter eleven. RAID."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def levels(self):
        d = load("raid")
        L = d["layouts"]
        head = label(r"Redundant arrays of inexpensive disks", font_size=36).to_edge(UP, buff=0.3)
        g0 = VGroup(label(r"RAID 0: \ striping", font_size=20, color=FILEC), layout_grid(L["0"][:4]))
        g1 = VGroup(label(r"RAID 1: \ mirroring", font_size=20, color=LAM), layout_grid(L["1"][:4]))
        g5 = VGroup(label(r"RAID 5: \ rotating parity", font_size=20, color=BITS), layout_grid(L["5"][:4]))
        for g in (g0, g1, g5):
            g.arrange(DOWN, buff=0.2)
        VGroup(g0, g1, g5).arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.45)
        rows = [[r"0", r"$N$", r"$N$", r"$N$", r"none"],
                [r"1", r"$N/2$", r"$N$", r"$N/2$", r"one per pair"],
                [r"5", r"$N-1$", r"$N$", r"$N/4$", r"any one"],
                [r"6", r"$N-2$", r"$N$", r"$N/6$", r"any two"]]
        tab = grid_table([r"RAID", r"capacity", r"random reads", r"random writes", r"disks that may fail"], rows,
                         widths=[1.2, 1.9, 2.3, 2.4, 2.8], row_h=0.42, font_size=19, mono_cols=())
        tab.to_edge(DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "In 1988 Patterson, Gibson and Katz argued that an array of small, cheap disks could beat one big "
            "expensive one, if it were organised well. <bookmark mark='a'/> Striping, RAID 0, spreads consecutive "
            "blocks across the disks, so they all work at once; but one disk failing loses everything. <bookmark "
            "mark='b'/> Mirroring, RAID 1, keeps every block on two disks: half the capacity, and either copy will "
            "do. <bookmark mark='c'/> RAID 5 adds one parity block to each stripe, rotating which disk holds it so no "
            "disk becomes a bottleneck. It survives the loss of any one disk, at the cost of one disk's capacity. "
            "<bookmark mark='d'/> Here is the trade in one table, for N disks. Random writes are the weak spot of "
            "parity, for a reason we will see next."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g0))
            vo.wait_until("b")
            self.play(FadeIn(g1))
            vo.wait_until("c")
            self.play(FadeIn(g5))
            vo.wait_until("d")
            self.play(FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    def parity(self):
        d = load("raid")
        head = label(r"Parity: \ Part 28's simplest code", font_size=36).to_edge(UP, buff=0.3)
        bits = [[1, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 1, 1]]
        par = [a ^ b ^ c ^ e for a, b, c, e in zip(*bits)]
        cols = VGroup()
        for k, bs in enumerate(bits + [par]):
            c = FILEC if k < 4 else BITS
            col = VGroup(*[blk(str(b), c, w=0.5, h=0.42, font=18, fill=0.25) for b in bs]).arrange(DOWN, buff=0.04)
            nm = label(rf"$D_{k}$" if k < 4 else r"$P$", font_size=22, color=c).next_to(col, UP, buff=0.1)
            cols.add(VGroup(nm, col))
        cols.arrange(RIGHT, buff=0.35).move_to([-3.6, 0.9, 0])
        eq = MathTex(r"P = D_0 \oplus D_1 \oplus D_2 \oplus D_3", font_size=30, color=BITS).next_to(cols, DOWN, buff=0.3)
        lost = MathTex(r"D_2 = D_0 \oplus D_1 \oplus D_3 \oplus P", font_size=30, color=YES).next_to(eq, DOWN, buff=0.2)
        sm = d["small"]["5"]
        right = VGroup(
            label(r"\textbf{the small-write problem}", font_size=22, color=NO),
            label(r"to change one block $D$ to $D'$:", font_size=19, color=WHITE),
            label(r"read $D$ and $P$; \ write $D'$ and $P' = P \oplus D \oplus D'$", font_size=19, color=WHITE),
            label(rf"{sm['reads']} reads and {sm['writes']} writes for one block: \ a quarter of the disks' speed",
                  font_size=19, color=NO),
            label(r"\textbf{RAID 6}: \ a second check block $Q = \sum_i 2^i D_i$ over GF(256)", font_size=19,
                  color=KERN),
            label(r"the field of Part 28's Reed--Solomon codes, \ and of Linux's RAID 6", font_size=17, color=GREY_A),
            label(rf"checked: \ all {d['pairs']} pairs of lost disks, \ out of six, \ rebuilt exactly", font_size=19,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.4, 0.4, 0])
        with self.voiceover(
            "The parity block is the exclusive or of the data blocks in its stripe, bit by bit, Part 28's simplest "
            "error-correcting code. <bookmark mark='a'/> If any one disk dies, we know which one, so each of its "
            "blocks is just the exclusive or of the survivors, parity included. <bookmark mark='b'/> But updating one "
            "block is expensive. The new parity depends on the old: read the old data and the old parity, then write "
            "the new data and the new parity. Four disk operations for one block. That is the small-write problem, "
            "and why databases often prefer mirrors. <bookmark mark='c'/> RAID 6 adds a second check block, Q, a "
            "weighted sum over the field with 256 elements, the field of Part 28's Reed-Solomon codes. Two equations, "
            "two unknowns: any two failed disks can be rebuilt. Our implementation rebuilds every one of the fifteen "
            "pairs of lost disks from six, exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols), FadeIn(eq))
            vo.wait_until("a")
            self.play(cols[2][1].animate.set_opacity(0.2), FadeIn(lost))
            vo.wait_until("b")
            self.play(FadeIn(right[:4]))
            vo.wait_until("c")
            self.play(FadeIn(right[4:]))
        self.wait(0.3)
        self.clear_scene()

    def rebuild(self):
        d = load("raid")
        head = label(r"Eight 16 TB disks, \ one fails: \ the rebuild", font_size=34).to_edge(UP, buff=0.3)
        rk = {(r["label"], r["ure"]): r for r in d["risk"]}
        hrs = d["rebuild_hours"]
        rows = [[r"another disk fails", rf"{rk[('datasheet', 1e-15)]['p_second_failure'] * 100:.2f}\%",
                 rf"{rk[('field', 1e-15)]['p_second_failure'] * 100:.2f}\%"],
                [r"an unreadable sector, \ at $10^{-15}$ per bit", rf"{rk[('datasheet', 1e-15)]['p_ure'] * 100:.0f}\%",
                 rf"{rk[('field', 1e-15)]['p_ure'] * 100:.0f}\%"],
                [r"an unreadable sector, \ at $10^{-14}$ per bit", rf"{rk[('datasheet', 1e-14)]['p_ure'] * 100:.2f}\%",
                 rf"{rk[('field', 1e-14)]['p_ure'] * 100:.2f}\%"]]
        tab = grid_table([rf"during the {hrs:.0f}-hour rebuild", r"datasheet: \ 0.87\% a year",
                          r"field: \ 3\% a year"], rows, widths=[5.4, 3.0, 2.6], row_h=0.48, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        for r in (2, 3):
            for c in (1, 2):
                tab.cells[r][c].set_color(NO)
        mt = d["mttdl"]
        ck = d["check"]
        mant, expo = f"{rk[('datasheet', 1e-15)]['bits_read']:.1e}".split("e")
        expo = int(expo)
        years = f"{mt[0]['raid5_years']:,.0f}".replace(",", "{,}")
        lines = VGroup(
            label(rf"reading the seven survivors end to end: \ ${mant} \times 10^{{{expo}}}$ bits", font_size=20,
                  color=WHITE),
            label(r"the second failure is rare; \ the \textbf{bad sector} during the rebuild is the real danger", font_size=20,
                  color=NO),
            label(rf"mean time to data loss, \ RAID 5: \ {years} years by the formula \ (independent failures; \ "
                  r"chapter 12 doubts that)", font_size=19, color=HEAD),
            label(rf"the formula against simulation \ ($\text{{MTTF}}/\text{{MTTR}} = {ck['ratio']}$): \ "
                  rf"{ck['raid5']['formula']:.0f}, \ exact {ck['raid5']['exact']:.0f}, \ simulated "
                  rf"{ck['raid5']['simulated']:.0f}", font_size=18, color=GREY_A),
            label(r"hence RAID 6, \ checksums, \ and scrubbing that finds bad sectors before a rebuild needs them",
                  font_size=20, color=YES),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the arithmetic of a real failure. Eight disks of sixteen terabytes in RAID 5; one dies. Rebuilding "
            "its contents means reading all seven survivors from end to end, at perhaps a hundred megabytes a second: "
            "about 44 hours. <bookmark mark='a'/> What can go wrong in that time? Another disk can fail. At the "
            "failure rate on the datasheet, the chance is three in ten thousand; at the three percent a year seen in "
            "the field, about one in a thousand. <bookmark mark='b'/> But the rebuild reads nine times ten to the "
            "fourteen bits, and drives are specified to fail to read about one sector per ten to the fifteen bits, "
            "or, for cheaper drives, per ten to the fourteen. At those rates the chance of hitting an unreadable "
            "sector is 59 percent, or near certainty. Those are worst-case bounds, and real drives usually do "
            "better, but the lesson stands: the danger is not the second disk, it is the bad sector. <bookmark "
            "mark='c'/> The classic formula for the mean time to data loss, which assumes failures are independent, "
            "gives RAID 5 tens of thousands of years, and our simulation agrees with the formula's model. <bookmark "
            "mark='d'/> Hence RAID 6, checksums, and scrubbing, which reads everything regularly so that bad sectors "
            "are found and repaired while the redundancy is still there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]),
                      FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(m) for m in tab.cells[1]])
            vo.wait_until("b")
            self.play(FadeIn(lines[0]), *[FadeIn(m) for m in tab.cells[2] + tab.cells[3]], FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]), FadeIn(lines[3]))
            vo.wait_until("d")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()
