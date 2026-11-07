from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load


def lamp(col, on=True, s=0.42):
    return Square(side_length=s, stroke_color=col, stroke_width=1.6, fill_color=col, fill_opacity=0.75 if on else 0.08)


class Method(VoiceoverScene):
    def construct(self):
        self.card()
        self.use_red()
        self.roofline()
        self.capacity()
        self.regressions()

    def card(self):
        card = chapter_card(11, r"Performance method and capacity", r"Where do you look first, \ and how much do you "
                            r"need?", lit=(1917, 2009), extra=((1917, r"Erlang: \ waiting at telephone exchanges"),
                                                               (2009, r"Williams, \ Waterman and Patterson: \ the "
                                                                      r"roofline")), part=PART)
        with self.voiceover("Chapter eleven. Performance as a method: where to look first, how much capacity to "
                            "buy, and how to notice when things get slower."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def use_red(self):
        head = label(r"Checklists: \ USE and RED", font_size=36).to_edge(UP, buff=0.3)
        res = (r"CPU", r"memory", r"disk", r"network")
        # an illustrative machine: the disk is saturated (a queue), though not fully utilised
        state = {(2, 1): NO, (2, 0): HEAD, (0, 0): YES}
        use = VGroup()
        cols = VGroup(*[label(t, font_size=20, color=c) for t, c in ((r"U", DATA), (r"S", DATA), (r"E", DATA))])
        for j, c in enumerate(cols):
            c.move_to([-3.0 + j * 0.7, 1.55, 0])
        rows = VGroup()
        for i, r in enumerate(res):
            y = 0.95 - i * 0.65
            nm = label(r, font_size=20, color=GREY_A).move_to([-4.0, y, 0], aligned_edge=RIGHT)
            lamps = VGroup(*[lamp(GREY_C, on=False).move_to([-3.0 + j * 0.7, y, 0]) for j in range(3)])
            rows.add(VGroup(nm, lamps))
        use.add(cols, rows)
        use_t = label(r"\textbf{USE}: \ for every resource", font_size=21, color=DATA).next_to(cols, UP, buff=0.3)
        use_t.align_to(rows, LEFT)
        use_k = wrapped_label(r"\textbf{U}tilisation: \ the share of time busy; \ \textbf{S}aturation: \ work queued "
                              r"that it cannot take yet; \ \textbf{E}rrors", 5.6, font_size=19, color=GREY_A)
        use_k.next_to(rows, DOWN, buff=0.35).align_to(rows, LEFT)
        svcs = (r"frontend", r"catalog", r"database")
        red = VGroup()
        rcols = VGroup(*[label(t, font_size=20, color=LAM) for t in (r"R", r"E", r"D")])
        for j, c in enumerate(rcols):
            c.move_to([3.6 + j * 0.7, 1.55, 0])
        rrows = VGroup()
        for i, s in enumerate(svcs):
            y = 0.95 - i * 0.65
            nm = label(s, font_size=20, color=GREY_A).move_to([2.6, y, 0], aligned_edge=RIGHT)
            lamps = VGroup(*[lamp(GREY_C, on=False).move_to([3.6 + j * 0.7, y, 0]) for j in range(3)])
            rrows.add(VGroup(nm, lamps))
        red.add(rcols, rrows)
        red_t = label(r"\textbf{RED}: \ for every service", font_size=21, color=LAM).next_to(rcols, UP, buff=0.3)
        red_t.align_to(rrows, LEFT)
        red_k = wrapped_label(r"\textbf{R}ate of requests, \ \textbf{E}rrors, \ \textbf{D}uration \ (as a "
                              r"distribution, \ chapter 7)", 4.6, font_size=19, color=GREY_A)
        red_k.next_to(rrows, DOWN, buff=0.35).align_to(rrows, LEFT)
        found = wrapped_label(r"the disk is only 60\% busy, \ yet requests queue for it: \ saturation, \ not "
                              r"utilisation, \ was the clue", 5.6, font_size=19, color=NO)
        found.next_to(use_k, DOWN, buff=0.3).align_to(use_k, LEFT)
        ill = note(r"illustrative", font_size=16).to_corner(DR, buff=0.35)
        gold = wrapped_label(r"Google's \textbf{four golden signals}: \ latency, \ traffic, \ errors, \ saturation",
                             4.6, font_size=19, color=WHITE).next_to(red_k, DOWN, buff=0.3).align_to(red_k, LEFT)
        with self.voiceover(
            "Faced with a slow system, the worst method is to look wherever you happen to know the tools. <bookmark "
            "mark='a'/> Brendan Gregg's USE method is a checklist instead. For every resource, the processors, "
            "memory, disks and network, check utilisation, the share of time it was busy; saturation, the work "
            "queued that it cannot take yet; and errors. <bookmark mark='b'/> Going down the list finds what the "
            "eye misses. Here the disk is only sixty percent busy, yet requests queue for it in bursts. Saturation, "
            "not utilisation, was the clue. <bookmark mark='c'/> For services, Tom Wilkie's RED method asks for the "
            "rate of requests, the errors, and the duration, as a distribution, as chapter seven insisted. "
            "<bookmark mark='d'/> Google's site reliability book calls its version the four golden signals: "
            "latency, traffic, errors and saturation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(use_t), FadeIn(cols), *[FadeIn(r) for r in rows], FadeIn(use_k))
            vo.wait_until("b")
            for i in range(4):
                anims = []
                for j in range(3):
                    col = state.get((i, j), YES)
                    anims.append(rows[i][1][j].animate.set_fill(col, 0.75).set_stroke(col))
                self.play(*anims, run_time=0.5)
            self.play(Indicate(rows[2][1][1], color=NO, scale_factor=1.3), FadeIn(found))
            vo.wait_until("c")
            self.play(FadeIn(red_t), FadeIn(rcols), *[FadeIn(r) for r in rrows], FadeIn(red_k))
            self.play(LaggedStart(*[l_.animate.set_fill(YES, 0.75).set_stroke(YES) for r in rrows for l_ in r[1]],
                                  lag_ratio=0.08), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(gold))
        self.wait(0.4)
        self.clear_scene()

    def roofline(self):
        head = label(r"The roofline, \ again", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 4, 1], [0, 3, 1], x_length=6.6, y_length=4.4,
                 x_label=r"arithmetic intensity: \ operations per byte from memory",
                 y_label=r"attainable operations per second", xticks=(0, 1, 2, 3, 4), yticks=(),
                 fx=lambda v: (r"1/10", r"1", r"10", r"100", r"1000")[int(v)])
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        ax = g.ax
        ridge = 2.0                     # in log10 units (+1): where the slanted roof meets the flat one
        mem = Line(ax.c2p(0, 0.6), ax.c2p(ridge, 2.6), color=DATA, stroke_width=4)
        cpu = Line(ax.c2p(ridge, 2.6), ax.c2p(4, 2.6), color=KERN, stroke_width=4)
        d = ax.c2p(ridge, 2.6) - ax.c2p(0, 0.6)
        mem_l = label(r"memory bandwidth", font_size=18, color=DATA).rotate(math.atan2(d[1], d[0]))
        mem_l.next_to(mem.get_center(), UL, buff=0.02)
        cpu_l = label(r"peak arithmetic", font_size=18, color=KERN).next_to(cpu, UP, buff=0.1)
        rd = Dot(ax.c2p(ridge, 2.6), radius=0.07, color=WHITE)
        rd_l = label(r"ridge", font_size=17, color=WHITE).next_to(rd, DOWN, buff=0.15)
        a = Dot(ax.c2p(0.9, 1.0), radius=0.09, color=NO)
        a_l = label(r"a table scan", font_size=18, color=NO).next_to(a, DOWN, buff=0.15)
        b = Dot(ax.c2p(3.2, 2.25), radius=0.09, color=YES)
        b_l = label(r"a tiled matrix multiply", font_size=18, color=YES).next_to(b, DOWN, buff=0.15)
        ill = note(r"schematic", font_size=16).next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        notes = VGroup(
            wrapped_label(r"Williams, \ Waterman and Patterson, \ 2009: \ performance is capped by the lower of two "
                          r"roofs", 4.8, font_size=19, color=WHITE),
            wrapped_label(r"left of the ridge, \ faster arithmetic buys nothing: \ move fewer bytes \ (Part 9's "
                          r"caches and tiles)", 4.8, font_size=19, color=DATA),
            wrapped_label(r"right of it, \ the processor is the limit: \ vectorise, \ or buy a bigger one \ "
                          r"(\emph{AI, \ Built} 17's accelerators)", 4.8, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(g, RIGHT, buff=0.5).align_to(g, UP)
        with self.voiceover(
            "For code that computes, the first question is which resource is the limit, and Part 9's roofline "
            "answers it on one chart. <bookmark mark='a'/> Samuel Williams, Andrew Waterman and David Patterson "
            "drew it in 2009. Across, the arithmetic a kernel does per byte it fetches from memory; up, the "
            "operations per second it can reach. Two roofs cap it: the slope of memory bandwidth, and the flat line "
            "of peak arithmetic. <bookmark mark='b'/> A table scan does little arithmetic per byte and sits under "
            "the slope. A faster processor buys it nothing; moving fewer bytes, with Part 9's caches and tiles, buys "
            "everything. <bookmark mark='c'/> A tiled matrix multiply sits under the flat roof, where only more "
            "arithmetic helps, the territory of AI, Built's Part 17 accelerators. Measure first where a program "
            "sits, then decide what to change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(mem), FadeIn(mem_l), FadeIn(notes[0]))
            self.play(Create(cpu), FadeIn(cpu_l), FadeIn(rd), FadeIn(rd_l))
            vo.wait_until("b")
            self.play(FadeIn(a, scale=1.5), FadeIn(a_l), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(b, scale=1.5), FadeIn(b_l), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def capacity(self):
        rows = load("capacity")["rows"]
        head = label(r"Capacity planning for the Job service", font_size=36).to_edge(UP, buff=0.3)
        sub = label(r"80 ms of work per book; \ target: \ mean wait under 20 ms, \ and at most 20\% of requests "
                    r"wait at all", font_size=20, color=GREY_A).next_to(head, DOWN, buff=0.25)
        data = []
        for r in rows:
            spare = r["servers"] - r["erlangs"]
            data.append([rf"{r['per_s']:,}", rf"{r['erlangs']:.2f}", rf"{r['servers']}",
                         rf"{100 * r['util']:.0f}\%", rf"{100 * r['p_wait']:.0f}\%", rf"{spare:.1f}",
                         rf"{math.sqrt(r['erlangs']):.1f}"])
        tab = grid_table([r"books a second", r"busy servers", r"servers", r"utilisation", r"wait at all",
                          r"spare", r"$\sqrt{\text{busy}}$"], data, widths=[2.1, 1.8, 1.4, 1.7, 1.7, 1.4, 1.5],
                         row_h=0.55, font_size=20, mono_cols=())
        tab.next_to(sub, DOWN, buff=0.45)
        for r in range(1, len(rows) + 1):
            tab.cells[r][2].set_color(HEAD)
            tab.cells[r][3].set_color(YES)
            tab.cells[r][5].set_color(LAM)
            tab.cells[r][6].set_color(LAM)
        hl = SurroundingRectangle(VGroup(*[tab.cells[r][3] for r in range(1, len(rows) + 1)]), color=YES, buff=0.08,
                                  stroke_width=2)
        notes = VGroup(
            wrapped_label(r"Erlang C, \ as in Part 45: \ bigger pools run hotter for the same wait, \ because the "
                          r"spare capacity needed grows only like the square root of the load", 6.0, font_size=19,
                          color=WHITE),
            wrapped_label(r"then add chapter 6's $N + k$ for failures, \ and check the plan with an open-loop load "
                          r"test \ (chapter 9)", 6.0, font_size=19, color=HEAD),
        ).arrange(RIGHT, buff=0.5, aligned_edge=UP).next_to(tab, DOWN, buff=0.7)
        with self.voiceover(
            "Capacity planning asks how many servers next year's load will need, and queueing theory answers. "
            "<bookmark mark='a'/> Each book takes the Job's service eighty milliseconds, and we want the mean wait "
            "under twenty milliseconds, with at most one request in five waiting at all. <bookmark mark='b'/> At "
            "twelve books a second, about one server's worth of work, Erlang's formula from Part 45 asks for three "
            "servers, only thirty-two percent busy. At a thousand a second it asks for ninety, eighty-nine percent "
            "busy. <bookmark mark='c'/> Bigger pools run hotter for the same wait, because the spare capacity they "
            "need grows only like the square root of the load: two spare servers at the top of the table, ten at "
            "the bottom. <bookmark mark='d'/> Then add chapter six's spares for failures, and check the plan with "
            "an open-loop load test, or chapter nine's illusion will flatter it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25), run_time=2.5)
            self.play(Create(hl))
            vo.wait_until("c")
            self.play(FadeOut(hl), FadeIn(notes[0]),
                      *[Indicate(VGroup(tab.cells[r][5], tab.cells[r][6]), color=LAM) for r in
                        range(1, len(rows) + 1)])
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def regressions(self):
        c = load("changepoint")
        xs = c["series"]
        n = len(xs)
        head = label(r"Catching a regression in CI", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, n, 10], [0.94, 1.09, 0.03], x_length=11.0, y_length=4.2, x_label=r"commit",
                 y_label=r"benchmark time, \ relative", xticks=range(0, n + 1, 10),
                 yticks=(0.94, 0.97, 1.0, 1.03, 1.06, 1.09), fy=lambda v: rf"{v:.2f}")
        g.next_to(head, DOWN, buff=0.35)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(i, v), radius=0.045, color=DATA) for i, v in enumerate(xs)])
        rings = VGroup(*[Circle(radius=0.13, color=NO, stroke_width=2.5).move_to(ax.c2p(i, xs[i]))
                         for i in c["naive_alerts"]])
        k = c["found"]
        split = DashedLine(ax.c2p(k - 0.5, 0.94), ax.c2p(k - 0.5, 1.09), color=YES, stroke_width=2)
        m1 = Line(ax.c2p(0, c["before"]), ax.c2p(k - 0.5, c["before"]), color=YES, stroke_width=4)
        m2 = Line(ax.c2p(k - 0.5, c["after"]), ax.c2p(n, c["after"]), color=YES, stroke_width=4)
        m_l = label(rf"mean {c['before']:.3f} \ $\to$ \ {c['after']:.3f}", font_size=19, color=YES).move_to(
            ax.c2p(68, 0.955))
        naive_l = wrapped_label(rf"naive rule, \ alert when a run is 5\% slower than the one before: \ "
                                rf"{len(c['naive_alerts'])} alerts, \ at commits "
                                rf"{', '.join(str(i) for i in c['naive_alerts'])}", 6.0, font_size=19, color=NO)
        cp_l = wrapped_label(rf"change point: \ the split that best separates two means, \ at commit {k}; \ none of "
                             rf"{round(1 / c['p']) - 1:,} shuffles of the data splits as well", 6.0, font_size=19,
                             color=YES)
        VGroup(naive_l, cp_l).arrange(RIGHT, buff=0.5, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Last, regressions. A team wants to know the day its code got slower, not the month. <bookmark "
            "mark='a'/> Here are eighty commits, each benchmarked once. Runs vary by about two percent, and from "
            "commit fifty-two on, the code is three percent slower. <bookmark mark='b'/> A naive rule alerts "
            "whenever a run is five percent slower than the one before. It fires five times. Four are noise, and "
            "the real one looks no different from them. <bookmark mark='c'/> Change-point detection asks where one "
            "split would best separate the series into two different means. It answers commit fifty-two: from one "
            "point zero zero zero to one point zero three two. <bookmark mark='d'/> Is that luck? Shuffle the "
            "measurements and search again. In two thousand shuffles, none split as well. MongoDB's engineers "
            "described running tests of this kind on their benchmarks in continuous integration in 2020."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.25), FadeIn(naive_l), run_time=1.8)
            vo.wait_until("c")
            self.play(Create(split), Create(m1), Create(m2), FadeIn(m_l))
            vo.wait_until("d")
            self.play(FadeIn(cp_l))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
