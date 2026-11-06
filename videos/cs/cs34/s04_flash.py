from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs34.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono)


def page(color=GREY_D, fill=0.0, w=0.62, h=0.4, text=""):
    r = Rectangle(width=w, height=h, stroke_color=GREY_B, stroke_width=1.2, fill_color=color, fill_opacity=fill)
    g = VGroup(r)
    if text:
        g.add(label(text, font_size=14, color=WHITE).move_to(r))
    return g


class Flash(VoiceoverScene):
    def construct(self):
        self.card()
        self.cells()
        self.ftl()
        self.amplification()
        self.wear()

    def card(self):
        card = chapter_card(3, r"Flash", r"How do you rewrite a disk that can only be erased in bulk?",
                            lit=(1984, 1987), extra=((1984, r"Masuoka: \ flash"), (1987, r"NAND flash")), part=PART)
        with self.voiceover("Chapter three. Flash."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cells(self):
        head = label(r"Pages, \ erase blocks, \ and wear", font_size=36).to_edge(UP, buff=0.3)
        blocks = VGroup()
        for b in range(4):
            col = VGroup(*[page() for _ in range(8)]).arrange(DOWN, buff=0.04)
            blocks.add(VGroup(col, label(rf"block {b}", font_size=16, color=GREY_B).next_to(col, DOWN, buff=0.1)))
        blocks.arrange(RIGHT, buff=0.35).move_to([-3.6, -0.1, 0])
        ops = VGroup(
            VGroup(label(r"\textbf{read} a page", font_size=22, color=DATA),
                   label(r"tens of microseconds", font_size=19, color=GREY_A)),
            VGroup(label(r"\textbf{program} a page: \ only an \textit{erased} one", font_size=22, color=HEAD),
                   label(r"hundreds of microseconds; \ bits can only go from 1 to 0", font_size=19, color=GREY_A)),
            VGroup(label(r"\textbf{erase}: \ a whole block at once", font_size=22, color=NO),
                   label(r"milliseconds; \ a block holds hundreds of pages", font_size=19, color=GREY_A)),
            VGroup(label(r"\textbf{wear}: \ each erase damages the insulator", font_size=22, color=KERN),
                   label(r"a few thousand erases per block for today's dense cells", font_size=19, color=GREY_A)),
        )
        for o in ops:
            o.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        ops.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.0, 0.2, 0])
        foot = label(r"so a page cannot be overwritten in place: \ to change 4 KiB, \ erase a block of a megabyte or "
                     r"more?", font_size=21, color=NO).to_edge(DOWN, buff=0.45)
        p0 = blocks[0][0]
        with self.voiceover(
            "Flash stores a bit as charge trapped on a floating gate, behind an insulator. Its shape dictates "
            "everything a flash drive does. <bookmark mark='a'/> The chip is read a page at a time, a few kilobytes, "
            "in tens of microseconds. <bookmark mark='b'/> It is written a page at a time too, but only into a page "
            "that has been erased: programming can only push bits one way. <bookmark mark='c'/> And erasing works "
            "only on a whole block of hundreds of pages, and takes milliseconds. <bookmark mark='d'/> Worse, every "
            "erase wears the insulator a little; today's dense chips survive a few thousand per block. <bookmark "
            "mark='e'/> So you cannot simply overwrite a page. Rewriting four kilobytes in place would mean erasing "
            "and rewriting a whole block, and wearing it out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blocks))
            vo.wait_until("a")
            self.play(FadeIn(ops[0]), p0[0][0].animate.set_fill(DATA, opacity=0.6))
            vo.wait_until("b")
            self.play(FadeIn(ops[1]), *[p0[k][0].animate.set_fill(HEAD, opacity=0.6) for k in range(1, 4)])
            vo.wait_until("c")
            self.play(FadeIn(ops[2]))
            self.play(*[p[0].animate.set_fill(NO, opacity=0.5) for p in blocks[1][0]], run_time=0.5)
            self.play(*[p[0].animate.set_fill(BG, opacity=0.0) for p in blocks[1][0]], run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(ops[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def ftl(self):
        head = label(r"The flash translation layer: \ a log, \ and a garbage collector", font_size=32).to_edge(
            UP, buff=0.3)
        NB, NP = 4, 4
        grid = VGroup()
        for b in range(NB):
            col = VGroup(*[page(w=0.9, h=0.45) for _ in range(NP)]).arrange(DOWN, buff=0.05)
            grid.add(VGroup(col, label(rf"block {b}", font_size=16, color=GREY_B).next_to(col, DOWN, buff=0.1)))
        grid.arrange(RIGHT, buff=0.3).move_to([-2.4, 0.3, 0])
        mapl = label(r"map: \ logical page $\rightarrow$ where it is now", font_size=19, color=GREY_A)
        mapl.move_to([4.0, 2.2, 0])
        host = mono("host writes:  A B C D  B' A'", 20, WHITE).move_to([-2.4, 2.5, 0])
        lines = VGroup(
            label(r"never overwrite: \ write the new copy to the next free page, \ mark the old one dead, \ update "
                  r"the map", font_size=20, color=WHITE),
            label(r"when free blocks run low: \ pick a \textbf{victim}, \ copy its live pages forward, \ erase it",
                  font_size=20, color=HEAD),
            label(r"those copies are writes the host never asked for: \ \textbf{write amplification}", font_size=20,
                  color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        seq = [("A", 0, 0), ("B", 0, 1), ("C", 0, 2), ("D", 0, 3), ("B'", 1, 0), ("A'", 1, 1)]
        cells = {}
        with self.voiceover(
            "The answer is a piece of software inside every drive, the flash translation layer, and it is a log. "
            "<bookmark mark='a'/> The host writes logical pages A, B, C, D, and they go to the next free pages, in "
            "order. <bookmark mark='b'/> Now the host rewrites B. The drive does not touch the old page: it writes "
            "the new B to the next free page, marks the old one dead, and updates its map from logical to physical "
            "pages. The same for A. <bookmark mark='c'/> Free pages run out, so a garbage collector picks a victim "
            "block, copies the pages still alive in it to a fresh block, and erases it. <bookmark mark='d'/> Those "
            "copies are writes the host never asked for. The ratio of what the flash writes to what the host writes "
            "is the write amplification, and it costs both speed and lifetime."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(host), FadeIn(mapl))
            vo.wait_until("a")
            for nm, b, k in seq[:4]:
                cell = grid[b][0][k]
                t = label(nm, font_size=18, color=WHITE).move_to(cell)
                cells[nm] = (cell, t)
                self.play(cell[0].animate.set_fill(DATA, opacity=0.5), FadeIn(t), run_time=0.35)
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            for nm, b, k in seq[4:]:
                cell = grid[b][0][k]
                t = label(nm, font_size=18, color=WHITE).move_to(cell)
                old = cells[nm[0]]
                cross = Cross(old[0], stroke_color=NO, stroke_width=3)
                self.play(cell[0].animate.set_fill(DATA, opacity=0.5), FadeIn(t), Create(cross),
                          old[0][0].animate.set_fill(NO, opacity=0.25), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            live = [grid[0][0][2], grid[0][0][3]]
            dests = [grid[1][0][2], grid[1][0][3]]
            moves = []
            for src, dst, nm in zip(live, dests, ("C", "D")):
                t = label(nm, font_size=18, color=WHITE).move_to(src)
                moves.append(t)
                self.play(t.animate.move_to(dst), dst[0].animate.set_fill(HEAD, opacity=0.5), run_time=0.7)
            victim = grid[0][0]
            self.play(*[p[0].animate.set_fill(NO, opacity=0.6) for p in victim], run_time=0.4)
            erase = [m for m in self.mobjects if isinstance(m, (Cross,))]
            self.play(*[p[0].animate.set_fill(BG, opacity=0.0) for p in victim], *[FadeOut(m) for m in erase],
                      *[FadeOut(cells[n][1]) for n in ("A", "B", "C", "D")], run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def amplification(self):
        d = load("flash")
        head = label(r"Write amplification against spare capacity, \ simulated", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1.0, 0.2], y_range=[1, 8, 1], x_length=7.0, y_length=4.0,
                  axis_config={"color": GREY_D, "include_numbers": False}).move_to([-1.2, -0.2, 0])
        xt = VGroup(*[label(rf"{int(x * 100)}\%", font_size=16, color=GREY_B).next_to(ax.c2p(x, 1), DOWN, buff=0.1)
                      for x in (0.2, 0.4, 0.6, 0.8, 1.0)])
        yt = VGroup(*[label(str(y), font_size=16, color=GREY_B).next_to(ax.c2p(0, y), LEFT, buff=0.1)
                      for y in range(1, 9)])
        xl = label(r"over-provisioning: \ spare flash, \ as a share of what the host can use", font_size=17,
                   color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"flash writes per host write", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        g = d["greedy"]
        est = VMobject(color=GREY_B, stroke_width=2).set_points_smoothly(
            [ax.c2p(x, (1 + x) / (2 * x)) for x in [0.0625 + i * 0.0125 for i in range(76)]])
        sim = VGroup(*[Dot(ax.c2p(r["op"], r["wa"]), radius=0.06, color=HEAD) for r in g])
        fifo = VGroup(*[Dot(ax.c2p(r["op"], r["wa"]), radius=0.05, color=LAM) for r in d["fifo"]])
        keys = VGroup(
            VGroup(Dot(radius=0.06, color=HEAD), label(r"simulated: \ greedy collection, \ random writes",
                                                       font_size=17, color=HEAD)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(radius=0.05, color=LAM), label(r"collect the oldest block instead", font_size=17,
                                                      color=LAM)).arrange(RIGHT, buff=0.12),
            VGroup(Line(LEFT * 0.15, RIGHT * 0.15, color=GREY_B), label(r"the estimate $(1 + p) / 2p$", font_size=17,
                                                                         color=GREY_B)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.4, 1.6, 0])
        c7 = next(r for r in g if abs(r["op"] - 0.07) < 1e-9)
        c28 = next(r for r in g if abs(r["op"] - 0.28) < 1e-9)
        notes = VGroup(
            label(rf"7\% spare \ (a consumer drive): \ {c7['wa']:.1f}", font_size=19, color=NO),
            label(rf"28\% \ (an enterprise drive): \ {c28['wa']:.1f}", font_size=19, color=YES),
            label(r"the collector's victim still holds live pages; \\ more spare, \ emptier victims", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(keys, DOWN, buff=0.45).align_to(keys, LEFT)
        foot = label(r"256 blocks of 64 pages; \ the drive filled, \ then six times its capacity in random writes",
                     font_size=17, color=GREY_B).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "How bad is it? We simulate a drive of 256 blocks, fill it, then write six times its capacity at random "
            "places. <bookmark mark='a'/> The one parameter that matters is the spare flash the drive keeps hidden "
            "from the host, the over-provisioning. <bookmark mark='b'/> With seven percent spare, typical of a "
            "consumer drive, the flash writes seven and a half pages for every page the host writes. With 28 "
            "percent, an enterprise figure, about two and a half. <bookmark mark='c'/> The dots follow a simple "
            "estimate closely: one plus p, over two p. With little spare, the collector's victim is still mostly "
            "alive, and copying it is most of the work. <bookmark mark='d'/> Collecting the oldest block instead of "
            "the emptiest is a little worse everywhere."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in sim], lag_ratio=0.15), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(est), FadeIn(keys[2]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(fifo), FadeIn(keys[1]))
        self.wait(0.3)
        self.clear_scene()

    def wear(self):
        d = load("flash")
        head = label(r"Skew, \ wear, \ TRIM, \ and many queues", font_size=36).to_edge(UP, buff=0.3)
        hot, uni = d["hot"], d["uniform"]
        W, H = 5.4, 1.6

        def hist(er, color):
            mx = max(max(hot["erases"]), max(uni["erases"]))
            bars = VGroup()
            w = W / len(er)
            for k, e in enumerate(sorted(er)):
                hh = max(0.01, H * e / mx)
                bars.add(Rectangle(width=w, height=hh, stroke_width=0, fill_color=color,
                                   fill_opacity=0.85).move_to([k * w, hh / 2, 0]))
            return bars
        hu = hist(uni["erases"], YES)
        hh = hist(hot["erases"], NO)
        gu = VGroup(hu, label(rf"uniform writes: \ erases per block from {min(uni['erases'])} to {uni['max']}",
                              font_size=18, color=YES).next_to(hu, UP, buff=0.12))
        gh = VGroup(hh, label(rf"90\% of writes to 10\% of the data: \ from {min(hot['erases'])} to {hot['max']}",
                              font_size=18, color=NO).next_to(hh, UP, buff=0.12))
        VGroup(gu, gh).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-3.4, 0.0, 0])
        tr = d["trim"]
        tl = VGroup(*[label(rf"{int(r['trim'] * 100)}\% trimmed: \ {r['wa']:.1f}", font_size=19,
                            color=YES if r["trim"] else NO) for r in tr]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tg = VGroup(label(r"\textbf{TRIM}: \ the file system says which pages are free; \\ 7\% spare, \ write "
                          r"amplification:", font_size=19, color=WHITE), tl).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.15)
        tg.move_to([3.6, 0.9, 0])
        nv = label(r"\textbf{NVMe}: \ up to 65{,}535 queues of 65{,}536 commands, \\ one per core, \ no lock; \ "
                   r"dozens of chips work at once", font_size=19, color=DATA).next_to(tg, DOWN, buff=0.5).align_to(
            tg, LEFT)
        foot = label(r"skew barely changes the amplification, \ but its busiest blocks wear almost three times faster "
                     r"than average: \\ \textbf{wear leveling} moves cold data onto worn blocks", font_size=19,
                     color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Three more things every drive must handle. <bookmark mark='a'/> Real traffic is skewed. With writes "
            "spread evenly, the blocks wear evenly. Send ninety percent of the writes to a tenth of the data, and the "
            "amplification hardly changes, but the busiest blocks are erased almost three times as often as the "
            "average, and would die first. So drives practise wear leveling, moving cold data onto worn blocks to rest "
            "them. <bookmark mark='b'/> Second, the drive cannot know which pages hold files you have deleted, and "
            "faithfully copies them forward. TRIM is the command by which the file system tells it. With a fifth of "
            "the drive trimmed, amplification falls from seven and a half to about two. <bookmark mark='c'/> And "
            "third, a drive is dozens of chips that can all work at once. NVMe gives it tens of thousands of queues, "
            "one per core, so no lock stands between the cores and the chips."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(gu), FadeIn(gh))
            self.play(FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tg))
            vo.wait_until("c")
            self.play(FadeIn(nv))
        self.wait(0.3)
        self.clear_scene()
