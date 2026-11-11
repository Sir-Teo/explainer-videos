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
        head = label("Chapter 1 CPI: counterfactual accounting, not unique causes", font_size=34).to_edge(UP, buff=0.3)
        n = sp["tournament"]["committed"]
        cpi_pipe = h["pipeline"]["cpi"]
        cpi_perf = 1 / sp["perfect"]["ipc"]
        cpi_real = 1 / sp["tournament"]["ipc"]
        ideal = 0.25
        parts = [(r"4-wide retirement \\ floor", ideal, GREY_B), (r"oracle-assisted \\ gap above floor", cpi_perf - ideal, FUNC),
                 (r"configuration \\ gap", cpi_real - cpi_perf, NO)]
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
        share = label(rf"oracle-assisted run: {100 * ((cpi_real - cpi_perf) / cpi_real):.0f}\% fewer cycles \\ "
                      r"configuration comparison; not unique time spent on branches", font_size=24, color=NO).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This stack is an accounting comparison, not a unique causal decomposition. <bookmark mark='a'/> "
            "Four-wide architectural retirement gives an ideal lower floor of one quarter cycle per retired "
            "instruction. It is not the total execution-start limit. <bookmark mark='b'/> The oracle-assisted run "
            "uses about zero point three one seven cycles per instruction; its gap above that floor includes the "
            "model's dependency, front-end and resource constraints. <bookmark mark='c'/> The tournament run uses "
            "about zero point five two nine. Their difference is a configuration gap, not a separately measured "
            "amount of time spent only on branches. <bookmark mark='d'/> Part 7's pipeline is another "
            "configuration, with about one point two cycles per instruction. <bookmark mark='e'/> The "
            "oracle-assisted core uses about forty percent fewer cycles than the tournament core on this chapter, "
            "with interactions among prediction, queues and memory recovery. The length test is important in the "
            "measured trace, but these comparisons do not prove its outcomes are unlearnable or assign every saved "
            "cycle to it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, k in zip("abc", range(3)):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(GrowFromEdge(bar[k], LEFT))
                if mk == "a":
                    vo.wait_until(mk)
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
            label("24 slices of 400 to 4000 characters; \\\\ features count encoded bytes", font_size=22, color=DATA),
            label(r"cycles fitted as a linear function \\ of the text's events \ (words, \ entries scanned, \ \dots)",
                  font_size=22, color=GREY_A),
            label(rf"heldout: 16000 chars / 16019 bytes \\ measured: {ck['cycles']:,} cycles \\ "
                  rf"predicted: {ck['predicted']:,.0f} ({100 * ck['error']:+.2f}\%)", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A full cycle-by-cycle simulation of the corpus is expensive, so use a fitted projection and expose its "
            "limits. <bookmark mark='a'/> The training set contains twenty-four randomly selected text slices, four "
            "hundred to four thousand characters long. The actual inputs and byte-count features are UTF-8 encoded; "
            "the slice length metadata is not always the encoded byte length. <bookmark mark='b'/> Fit model cycles "
            "as a linear function of text features, including word counts, scanned entries and letter comparisons. "
            "<bookmark mark='c'/> One separate Moby-Dick slice has sixteen thousand characters and sixteen thousand "
            "nineteen encoded bytes. It takes about three point two nine million simulated cycles, and this fit "
            "predicts it within about zero point zero nine percent. That is one heldout check, not a full-corpus "
            "error bound or evidence that all unseen texts behave equally well. Host simulation speed also depends "
            "on machine and configuration."
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
        head = label("Projected corpus runtime: \\ ledger row 2", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(rf"projected corpus: \ ${sci(co['instructions'], 4)}$ instructions, \ ${sci(co['cycles'], 4)}$ cycles: \ "
                  rf"IPC {co['ipc']:.2f}", font_size=24, color=HEAD),
            label(rf"assumed teaching clock: {j['clock_mhz']:.0f} MHz; \ no out-of-order gate timing result", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).move_to(UP * 1.9)
        rows = j["ledger"] + [{"part": p_, "label": t} for p_, t in ((9, r"caches"), (10, r"four cores"),
                                                                     (13, r"an optimizing compiler"),
                                                                     (16, r"sort, then count"), (17, r"a hash table"))]
        led = ledger_table(rows, shown=3, highlight=(2,), font_size=21, row_h=0.38, label_width=4.8).move_to(DOWN * 1.1)
        res = label(rf"{human_time(j['ledger'][1]['seconds'])} $\to$ {human_time(co['seconds'])}: \ "
                    rf"{j['speedup']:.2f} times: fitted projections at the shared assumed clock", font_size=26,
                    color=COST).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Apply the fitted cycle model to the corpus's counted text features. <bookmark mark='a'/> It projects "
            "about fifty point seven billion cycles for about a hundred six point nine billion architectural "
            "instructions, an average IPC near two point one. Those corpus cycles were not obtained by running "
            "every instruction through this core. <bookmark mark='b'/> Converting them to time additionally assumes "
            "Part 7's teaching clock budget, about eight hundred eighty-five megahertz. This out-of-order design "
            "has no gate-level timing result establishing that frequency. The projected runtime is about "
            "fifty-seven seconds. <bookmark mark='c'/> At the shared assumed clock, the previous fitted pipeline "
            "row is about two and a half times slower. Both the cycle extrapolation and frequency assumptions "
            "travel with that ratio. The ledger is a transparent model comparison, not a measured complete-corpus "
            "hardware benchmark."
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
