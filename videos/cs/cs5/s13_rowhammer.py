from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, load


class Rowhammer(VoiceoverScene):
    def construct(self):
        self.card()
        self.hammer()
        self.why()
        self.exploit()

    def card(self):
        card = chapter_card(12, r"When memory leaks", r"Can reading memory change it?", lit=(2014, 2015), part=PART)
        with self.voiceover("Chapter twelve. When memory leaks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def hammer(self):
        head = label(r"Rowhammer \ (Kim et al., 2014)", font_size=38).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(7)
        nrows, ncols = 7, 16
        cells = []
        g = VGroup()
        for r in range(nrows):
            row = []
            for c in range(ncols):
                sq = Square(0.3, stroke_color=GREY_D, stroke_width=1, fill_color=YES, fill_opacity=0.65)
                sq.move_to([-6.3 + 0.34 * c, 1.9 - 0.42 * r, 0])
                row.append(sq)
                g.add(sq)
            cells.append(row)
        aggr = (2, 4)
        victim = 3
        tags = VGroup(label(r"aggressor", font_size=22, color=NO).next_to(cells[2][-1], RIGHT, buff=0.25),
                      label(r"victim", font_size=22, color=HEAD).next_to(cells[3][-1], RIGHT, buff=0.25),
                      label(r"aggressor", font_size=22, color=NO).next_to(cells[4][-1], RIGHT, buff=0.25))
        counter = ValueTracker(0)
        cnt = always_redraw(lambda: label(rf"activations in one refresh period: \ {int(counter.get_value()):,}".replace(
            ",", "{,}"), font_size=26, color=HEAD).next_to(g, DOWN, buff=0.45).align_to(g, LEFT))
        weak = rng.choice(ncols, 3, replace=False)
        side = VGroup(
            label(r"open row A, \ open row B, \\ again and again", font_size=24, color=GREY_A),
            label(r"each activation disturbs the neighbouring row \\ and drains a little of its charge", font_size=24,
                  color=GREY_A),
            label(r"110 of 129 DDR3 modules tested \\ flipped bits; \ as few as \\ 139{,}000 activations sufficed",
                  font_size=24, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        side.next_to(tags, RIGHT, buff=0.45).align_to(g, UP)
        with self.voiceover(
            "As DRAM cells shrank, their neighbours came uncomfortably close. In 2014 Yoongu Kim, Onur Mutlu and their "
            "colleagues at Carnegie Mellon and Intel published a disturbing measurement. <bookmark mark='a'/> Pick two "
            "rows of memory, and access them alternately, as fast as possible: open one, open the other, again and "
            "again. Each time a row is opened, the electrical activity disturbs the rows next to it, and a little "
            "charge leaks out of their cells. <bookmark mark='b'/> Do it enough times between two refreshes, and the "
            "weakest cells in the row in between, the victim, which the program never touches, lose enough charge to "
            "flip. <bookmark mark='c'/> Of a hundred and twenty-nine DDR3 memory modules they tested, a hundred and ten "
            "flipped bits, some after only a hundred and thirty-nine thousand activations, well within one "
            "sixty-four-millisecond refresh period."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g, lag_ratio=0.003), FadeIn(tags))
            vo.wait_until("a")
            self.add(cnt)
            self.play(FadeIn(side[0]))
            for k in range(6):
                rr = aggr[k % 2]
                self.play(*[cells[rr][c].animate.set_fill(NO, 0.9) for c in range(ncols)], counter.animate.set_value(
                    (k + 1) * 4000), run_time=0.25)
                self.play(*[cells[rr][c].animate.set_fill(YES, 0.65) for c in range(ncols)], run_time=0.15)
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(counter.animate.set_value(139000), *[cells[victim][c].animate.set_fill(YES, 0.3) for c in range(ncols)],
                      run_time=3.0)
            self.play(*[cells[victim][c].animate.set_fill(NO, 1.0) for c in weak])
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        head = label(r"Why it appeared when it did", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 64, 16], y_range=[0, 1.05, 0.5], x_length=5.6, y_length=3.4, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 3.4 + DOWN * 0.2)
        xl = note(r"ms since the last refresh", font_size=20).next_to(ax, DOWN, buff=0.3)
        yl = note(r"victim cell's charge \ (schematic)", font_size=20).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        thr = DashedLine(ax.c2p(0, 0.5), ax.c2p(64, 0.5), color=NO, stroke_width=2)
        tl = label(r"read as 0", font_size=20, color=NO).next_to(ax.c2p(64, 0.5), RIGHT, buff=0.08)
        ts = np.linspace(0, 64, 129)
        calm = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(t, np.exp(-t / 400)) for t in ts])
        def hammered(t):
            return np.exp(-t / 400) - 0.62 * (1 - np.exp(-t / 22))

        ham = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(t, hammered(t)) for t in ts])
        t_flip = float(ts[np.argmax(hammered(ts) < 0.5)])
        cl = label(r"ordinary leakage", font_size=20, color=YES).next_to(ax.c2p(40, np.exp(-0.1)), UP, buff=0.08)
        hl = label(r"neighbour hammered", font_size=20, color=NO).next_to(ax.c2p(44, 0.25), DOWN, buff=0.08)
        flip = Dot(ax.c2p(t_flip, 0.5), radius=0.09, color=NO)
        fl = label(r"flips \ before refresh", font_size=20, color=NO).next_to(flip, UP + RIGHT, buff=0.05)
        pts = VGroup(*[label(t, font_size=24, color=c) for t, c in (
            (r"each generation shrinks the cells \\ and packs the rows closer together", GREY_A),
            (r"a cell's charge is now only \\ tens of thousands of electrons, \ or fewer", GREY_A),
            (r"opening a row swings its word line \\ from 0 to full voltage, \ coupling into the \\ neighbours "
             r"and speeding their leakage", HEAD),
            (r"the 64 ms refresh interval \ was set for leakage alone, \\ not for a neighbour opened \\ "
             r"hundreds of thousands of times", NO),
            (r"a reliability margin \\ quietly became a security boundary", YES),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 3.75 + DOWN * 0.1)
        with self.voiceover(
            "Why did this appear only around 2010? <bookmark mark='a'/> Scaling often shrinks cells and packs "
            "rows closer, though vulnerability varies by device and mitigation, and a cell now holds only tens of "
            "thousands of electrons, or fewer. <bookmark mark='b'/> Opening a row swings its word line from zero "
            "to full voltage, and the electrical coupling into the neighbouring rows, together with charge "
            "trapped in the silicon between them, speeds up their leakage a little every time. <bookmark "
            "mark='c'/> The sixty-four millisecond refresh interval was chosen for ordinary leakage, with a "
            "safety margin, which does not by itself guarantee safety against repeated neighboring-row activity. "
            "A reliability margin had quietly become a security boundary, and nobody had been guarding it."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(thr), FadeIn(tl), Create(calm), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]), Indicate(calm, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]), Create(ham), FadeIn(hl), run_time=2.5)
            self.play(FadeIn(flip, scale=2), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(pts[3]), Indicate(ax.x_axis.numbers[-1], color=NO))
            self.play(FadeIn(pts[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exploit(self):
        head = label(r"From a reliability bug \ to an attack", font_size=38).to_edge(UP, buff=0.4)
        events = (
            ("2014", r"Kim et al.: \ hammering flips bits \ in 110 of 129 modules", NO),
            ("2015", r"Google Project Zero flips a bit in a page table \\ and takes over the operating system", NO),
            ("2016", r"from JavaScript in a web page; \ from an Android app", NO),
            ("", r"defences: \ refresh more often, \\ count activations and refresh neighbours (TRR), \ ECC", YES),
            ("2020", r"new hammering patterns \ still beat the defences of DDR4", NO),
        )
        rows = VGroup()
        for yr, t, c in events:
            dot = Dot(radius=0.09, color=c)
            yl = label(yr, font_size=26, color=HEAD) if yr else label(r"--", font_size=26, color=GREY_D)
            tx = label(t, font_size=24, color=c)
            rows.add(VGroup(yl, dot, tx))
        y = 2.3
        for r in rows:
            r[1].move_to([-4.6, y, 0])
            r[0].next_to(r[1], LEFT, buff=0.3)
            r[2].next_to(r[1], RIGHT, buff=0.35)
            r[2].align_to(r[1], UP).shift(UP * 0.12)
            y -= max(r[2].height, 0.4) + 0.32
        spine = Line([-4.6, 2.5, 0], [-4.6, y + 0.3, 0], color=GREY_D, stroke_width=2)
        lesson = label(r"the lesson: \ an abstraction (``memory holds what you wrote'') \ leaked \ (Parts 32 and 42)",
                       font_size=26, color=HEAD).to_edge(DOWN, buff=0.35)
        lines = VGroup(*rows[1:], lesson)
        with self.voiceover(
            "At first it looked like a reliability problem. It is a security problem. <bookmark mark='a'/> In "
            "2015 Mark Seaborn and Thomas Dullien at Google's Project Zero hammered rows until a bit flipped "
            "inside a page table, the structure Part 32 uses to keep programs out of each other's memory, and "
            "took over the machine. <bookmark mark='b'/> Others did it from JavaScript running in a web page, and "
            "from an ordinary Android app. <bookmark mark='c'/> The defences are refreshing more often, counting "
            "activations and refreshing a hammered row's neighbours early, and error-correcting codes. <bookmark "
            "mark='d'/> These measures need precise scope. TRRespass in 2020 defeated several deployed DDR4 "
            "tracking schemes; that does not show that every refresh policy, counter design or error-correcting "
            "code fails. <bookmark mark='e'/> The deeper lesson runs through the whole series. Every layer "
            "promises something simple; memory promises to hold what you wrote. Rowhammer is what happens when "
            "the physics underneath an abstraction leaks through it, and Part 42 meets its relatives."
        ) as vo:
            self.play(FadeIn(head), Create(spine), FadeIn(rows[0]))
            for mk, l in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
