from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt, load,
                                  mono, sci)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.stack()
        self.model()
        self.corpus()

    def card(self):
        card = chapter_card(14, r"The Job out of order", r"Where do the Job's cycles go now?", part=PART)
        with self.voiceover("Chapter fourteen. The Job out of order."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stack(self):
        sp = load("speculate")["rows"]
        h = load("hook")
        head = label(r"The first chapter's cycles, \ accounted for", font_size=34).to_edge(UP, buff=0.3)
        n = sp["tournament"]["committed"]
        cpi_pipe = h["pipeline"]["cpi"]
        cpi_perf = 1 / sp["perfect"]["ipc"]
        cpi_real = 1 / sp["tournament"]["ipc"]
        ideal = 0.25
        parts = [(r"4 a cycle: \ the width", ideal, GREY_B), (r"dependences, \ fetch, \ ports", cpi_perf - ideal, FUNC),
                 (r"wrong guesses", cpi_real - cpi_perf, NO)]
        S = 9.0
        bar = VGroup()
        x = 0
        for nm, v, c in parts:
            w = S * v
            r = Rectangle(width=w, height=0.9, stroke_color=BG, stroke_width=2, fill_color=c, fill_opacity=0.8)
            r.move_to([x + w / 2, 0, 0])
            t = label(rf"{nm} \\ {v:.3f}", font_size=19, color=WHITE).move_to(r)
            if t.width > w - 0.1:
                t = label(rf"{nm} \\ {v:.3f}", font_size=17, color=c).next_to(r, DOWN, buff=0.15)
            bar.add(VGroup(r, t))
            x += w
        bar.move_to(UP * 0.9).to_edge(LEFT, buff=1.5)
        tot = label(rf"CPI {cpi_real:.3f} \ (IPC {1 / cpi_real:.2f})", font_size=26, color=HEAD).next_to(bar, UP,
                                                                                                    buff=0.3)
        pipe = Rectangle(width=S * cpi_pipe, height=0.5, stroke_width=0, fill_color=GREY_D, fill_opacity=0.6)
        pipe.next_to(bar, DOWN, buff=1.1).align_to(bar, LEFT)
        pl = label(rf"Part 7's pipeline: \ CPI {cpi_pipe:.3f}", font_size=22, color=GREY_A).move_to(pipe)
        share = label(rf"{100 * ((cpi_real - cpi_perf) / cpi_real):.0f}\% of the core's time: \ recovering from the scan loop's "
                      r"length test", font_size=24, color=NO).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Where do the cycles go now? Measure cycles per instruction on the first chapter, and split it. "
            "<bookmark mark='a'/> A four-wide core could at best spend a quarter of a cycle on each instruction. "
            "<bookmark mark='b'/> With perfect prediction it spends about a third: the rest of that is true "
            "dependences, the one-taken-branch fetch limit, and the memory ports. <bookmark mark='c'/> With the real "
            "predictor, another fifth of a cycle per instruction goes to wrong guesses. <bookmark mark='d'/> Part "
            "7's pipeline, for comparison, spent one point two. <bookmark mark='e'/> So forty percent of the core's "
            "time goes to recovering from mispredictions, nearly all of them in one branch: the scan loop's test of "
            "whether an entry has the word's length. That branch depends on the text, and no history predicts it "
            "well. The fix is not in the hardware; it is in the program, and Part 17 makes it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bar[k], LEFT))
            self.play(FadeIn(tot))
            vo.wait_until("d")
            self.play(GrowFromEdge(pipe, LEFT), FadeIn(pl))
            vo.wait_until("e")
            self.play(FadeIn(share))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        j = load("job")
        ck = j["check"]
        head = label(r"From passages to the corpus", font_size=36).to_edge(UP, buff=0.35)
        s = j["samples"]
        x = np.array([r["instructions"] for r in s], float) / 1e6
        y = np.array([r["cycles"] for r in s], float) / 1e6
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 3.5, 1], x_length=7.0, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 2.4 + DOWN * 0.4)
        ax.x_axis.add_numbers(list(range(0, 8)), font_size=16, num_decimal_places=0)
        ax.y_axis.add_numbers([0, 1, 2, 3], font_size=16, num_decimal_places=0)
        xl = note(r"millions of instructions", font_size=18).next_to(ax, DOWN, buff=0.15)
        yl = note(r"millions of cycles", font_size=18).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=DATA) for a, b in zip(x, y)])
        chk = Dot(ax.c2p(ck["instructions"] / 1e6, ck["cycles"] / 1e6), radius=0.1, color=YES)
        guide = DashedLine(ax.c2p(0, 0), ax.c2p(7, 3.5), color=GREY_D, stroke_width=2)
        gl = label(r"IPC 2", font_size=18, color=GREY_B).next_to(ax.c2p(4.4, 2.2), UP + LEFT, buff=0.05)
        cl = label(r"the check passage", font_size=18, color=YES).next_to(chk, LEFT, buff=0.15)
        side = VGroup(
            label(r"24 passages of 400 to 4000 bytes, \\ run on the core", font_size=22, color=DATA),
            label(r"cycles fitted as a linear function \\ of the text's events \ (words, \ entries scanned, \ \dots)",
                  font_size=22, color=GREY_A),
            label(rf"checked on 16 KB of \textit{{Moby-Dick}}: \\ {ck['cycles']:,} cycles measured, \\ "
                  rf"{ck['predicted']:,.0f} predicted \ ({100 * ck['error']:+.2f}\%)", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Simulating thirty novels on this core, cycle by cycle, would take about a month: it runs about thirty-five thousand "
            "instructions a second. So, as in Part 7, we count. <bookmark mark='a'/> Twenty-four passages of four "
            "hundred to four thousand bytes, from random books, are run on the core. <bookmark mark='b'/> Their "
            "cycle counts are fitted as a linear function of the events in each text that the Job's work depends on: "
            "the words, the entries scanned, the entries of the same length, and so on. <bookmark mark='c'/> Then "
            "the model is checked on a passage four times longer than any it was fitted on, sixteen thousand bytes "
            "of Moby-Dick: six and a half million instructions, three point three million cycles, predicted to within "
            "a tenth of a percent."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(guide), FadeIn(gl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.05), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(chk, scale=2), FadeIn(cl), FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def corpus(self):
        j = load("job")
        co = j["corpus"]
        head = label(r"Thirty novels, \ out of order: \ ledger row 2", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(rf"the corpus: \ ${sci(co['instructions'], 4)}$ instructions, \ ${sci(co['cycles'], 4)}$ cycles: \ "
                  rf"IPC {co['ipc']:.2f}", font_size=24, color=HEAD),
            label(rf"at Part 7's clock, \ {j['clock_mhz']:.0f} MHz \ (an assumption: \ a real out-of-order core "
                  r"needs more stages to keep it)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).move_to(UP * 1.9)
        rows = j["ledger"] + [{"part": p_, "label": t} for p_, t in ((9, r"caches"), (10, r"four cores"),
                                                                     (13, r"an optimizing compiler"),
                                                                     (16, r"sort, then count"), (17, r"a hash table"))]
        led = ledger_table(rows, shown=3, highlight=(2,), font_size=21, row_h=0.38, label_width=4.8).move_to(DOWN * 1.1)
        res = label(rf"{human_time(j['ledger'][1]['seconds'])} $\to$ {human_time(co['seconds'])}: \ "
                    rf"{j['speedup']:.2f} times faster, \ for the same program", font_size=26,
                    color=COST).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Applied to the whole corpus, the model gives a hundred seven billion instructions in fifty-one billion "
            "cycles: two point one instructions per cycle. <bookmark mark='a'/> We keep Part 7's clock of eight "
            "hundred eighty-five megahertz. That is generous: renaming, wakeup and the reorder buffer add logic, and "
            "a real out-of-order core needs more pipeline stages to hold the same clock. Part 10 returns to clocks. "
            "<bookmark mark='b'/> The thirty novels now take fifty-seven seconds, against two minutes twenty-five "
            "on the pipeline and four minutes forty on the single-cycle Pebble. <bookmark mark='c'/> That is the "
            "third row of the ledger: two and a half times faster again, for exactly the same program. The rows "
            "still to come are caches, more cores, a compiler, and then, at last, better algorithms."
        ) as vo:
            self.play(FadeIn(head), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(led.axis), LaggedStart(*[FadeIn(r) for r in led.rows], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()
