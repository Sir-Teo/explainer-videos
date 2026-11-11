from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt, load,
                                  mono)


class Ilp(VoiceoverScene):
    def construct(self):
        self.card()
        self.wall()
        self.curves()
        self.core()
        self.verdict()

    def card(self):
        card = chapter_card(6, r"Wider, \ and the ILP wall", r"How much parallelism is in a real program?",
                            lit=(1972, 1991), extra=((1972, r"Riseman and Foster"), (1991, r"Wall's limits of ILP")),
                            part=PART)
        with self.voiceover("Chapter six. Wider, and the wall."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def wall(self):
        d = load("limits")
        head = label("Oracle sensitivity: \\ one baseline assumption changed per bar", font_size=32).to_edge(UP, buff=0.3)
        names = [r"the oracle", r"no renaming", r"memory: \\ wait for \\ every store", "branches: \\\\ predictor \\\\ barriers", r"branches: \\ no \\ speculation"]
        vals = [e["ipc"] for e in d["each"]]
        cols = [YES, CTRL, INF, NO, NO]
        lo, hi = -0.5, 3.5
        H = 4.2
        bars = VGroup()
        for k, (v, nm, c) in enumerate(zip(vals, names, cols)):
            h = H * (np.log10(v) - lo) / (hi - lo)
            b = Rectangle(width=1.3, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([k * 2.3, h / 2, 0], aligned_edge=ORIGIN)
            b.move_to([k * 2.3, h / 2, 0])
            t = label(f"{v:,.0f}" if v >= 10 else f"{v:.2f}", font_size=24, color=c).next_to(b, UP, buff=0.08)
            n = label(nm, font_size=18, color=GREY_A).next_to([k * 2.3, 0, 0], DOWN, buff=0.15)
            bars.add(VGroup(b, t, n))
        axis = VGroup()
        for e in (0, 1, 2, 3):
            y = H * (e - lo) / (hi - lo)
            axis.add(DashedLine([-1.0, y, 0], [4 * 2.3 + 0.8, y, 0], color=GREY_D, stroke_width=1, dash_length=0.08))
            axis.add(label(f"{10 ** e:,}", font_size=16, color=GREY_B).move_to([-1.4, y, 0]))
        fig = VGroup(axis, bars).move_to(DOWN * 0.35)
        yl = note(r"instructions per cycle \ (log scale), \ the Job's first chapter", font_size=20).next_to(
            fig, UP, buff=0.15).align_to(fig, LEFT)
        with self.voiceover(
            "Limit studies inspired by David Wall's 1991 work schedule a recorded execution under progressively "
            "changed assumptions. Our bars change one assumption at a time from the same baseline; they are not "
            "cumulative stages. <bookmark mark='a'/> Unlimited start width and lookahead, fixed latencies, perfect "
            "path and word-address knowledge, register renaming and omitted realistic I/O ordering produce about "
            "twenty-four hundred instructions per modeled cycle on this trace. <bookmark mark='b'/> Adding "
            "register-name constraints alone gives about three point seven. <bookmark mark='c'/> Making loads wait "
            "for earlier store addresses instead gives about sixty-two. <bookmark mark='d'/> Keeping the other "
            "oracle powers but adding tournament-predicted control barriers gives about three point four. <bookmark "
            "mark='e'/> Barriers at every branch and jump give under one half. These are sensitivities of a "
            "particular trace scheduler, not attainable processor specifications or universal program limits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(yl))
            for mk, b in zip("abcde", bars):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]))
                if mk == "a":
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("limits")
        head = label("Trace scheduler: \\ start width and start-distance parameter", font_size=34).to_edge(UP, buff=0.3)
        ws = d["widths"]
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 32, 8], x_length=8.0, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 1.3 + DOWN * 0.3)
        ax.y_axis.add_numbers([0, 8, 16, 24, 32], font_size=18, num_decimal_places=0)
        xt = VGroup(*[label(str(w), font_size=18, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k, w in enumerate(ws)])
        xl = note(r"width: \ instructions started per cycle", font_size=20).next_to(xt, DOWN, buff=0.1)
        yl = note(r"instructions per cycle", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)

        def curve(vals, color, width=4):
            return VMobject(color=color, stroke_width=width).set_points_as_corners(
                [ax.c2p(k, v) for k, v in enumerate(vals)])

        real = VGroup(*[curve(d["curves"][k], NO, 3) for k in ("32", "128", "512", "2048", "inf")])
        pb128 = curve(d["perfect_branches"]["128"], DATA)
        pb2048 = curve(d["perfect_branches"]["2048"], YES)
        lr = label(r"modeled control barriers: \ start distance 32 to $\infty$", font_size=20, color=NO).next_to(
            ax.c2p(6, d["curves"]["inf"][-1]), UP, buff=0.15).shift(LEFT * 1.2)
        l128 = label(r"known path, \ start distance 128", font_size=20, color=DATA).next_to(
            ax.c2p(6, d["perfect_branches"]["128"][-1]), UP, buff=0.1).shift(LEFT * 1.0)
        l2048 = label(r"known path, \ start distance 2048", font_size=20, color=YES).next_to(
            ax.c2p(6, d["perfect_branches"]["2048"][-1]), LEFT, buff=0.15).shift(DOWN * 0.3)
        side = VGroup(
            label(r"start distance: index-separated starts; \\ not an active ROB capacity", font_size=22, color=GREY_A),
            label(r"with modeled control barriers \\ these curves nearly coincide", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        with self.voiceover(
            "Now vary start width and the scheduler's window parameter. This parameter constrains an instruction's "
            "start relative to the start of an earlier trace position. It does not wait for the oldest unfinished "
            "operation to retire, so it is not a physical reorder-buffer capacity. <bookmark mark='a'/> With the "
            "modeled predictor barriers, curves for the tested window parameters almost overlap and flatten near "
            "three point four. That shows little benefit from this parameter on this trace under these assumptions. "
            "<bookmark mark='b'/> With perfect control, a parameter of one hundred twenty-eight permits "
            "considerably more overlap. <bookmark mark='c'/> Two thousand forty-eight permits still more. Control "
            "assumptions interact strongly with start-width and lookahead assumptions here. The result does not "
            "prove that larger buffers are useless on other programs, or that the oracle's distant future inputs "
            "can be supplied by hardware."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in real], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(lr), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(pb128), FadeIn(l128), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(pb2048), FadeIn(l2048), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def core(self):
        d = load("sweep")
        head = label("Functional core: \\ front-end width and queue capacities", font_size=34).to_edge(UP, buff=0.3)
        runs = d["runs"]
        robs = [16, 32, 64, 128, 256, 512]
        widths = [1, 2, 4, 8]
        cw, chh = 1.3, 0.62
        grid = VGroup()
        for r, w in enumerate(widths):
            for c, rb in enumerate(robs):
                v = [x["ipc"] for x in runs if x["width"] == w and x["rob"] == rb][0]
                cell = Rectangle(width=cw * 0.95, height=chh * 0.9, stroke_width=0, fill_color=FUNC,
                                 fill_opacity=0.15 + 0.4 * v / 2.0)
                cell.move_to([c * cw, -r * chh, 0])
                grid.add(VGroup(cell, label(f"{v:.2f}", font_size=20, color=WHITE).move_to(cell)))
        rl = VGroup(*[label(rf"{w} wide", font_size=20, color=GREY_A).move_to([-1.1, -r * chh, 0])
                      for r, w in enumerate(widths)])
        cl = VGroup(*[label(str(rb), font_size=20, color=GREY_A).move_to([c * cw, 0.6, 0]) for c, rb in enumerate(robs)])
        ct = note(r"reorder-buffer entries", font_size=20).move_to([2.5 * cw, 1.05, 0])
        tab = VGroup(grid, rl, cl, ct).move_to(UP * 0.4)
        pp = d["perfect_512"]
        perf = label(rf"oracle-assisted \ (512 ROB entries): \ {pp[0]:.2f}, \ {pp[1]:.2f}, \ {pp[2]:.2f}, \ "
                     rf"{pp[3]:.2f}", font_size=24, color=YES).next_to(tab, DOWN, buff=0.5)
        why = label("constraints include one taken fetch branch/cycle and two memory ports", font_size=22,
                    color=GREY_B).next_to(perf, DOWN, buff=0.2)
        with self.voiceover(
            "Compare that oracle with the functional core's actual model runs. <bookmark mark='a'/> Each heatmap "
            "cell reports retired IPC while varying the front-end and retirement width, reorder-buffer capacity and "
            "proportional queue sizes. The four-width configuration is about one point eight nine; eight increases "
            "it only slightly on this chapter. Execution starts have their own unit and port limits. <bookmark "
            "mark='b'/> Increasing these capacities beyond the smaller tested settings brings little benefit here. "
            "That is a workload-specific observation, consistent with low whole-run occupancy. <bookmark mark='c'/> "
            "Oracle-assisted correct-path prediction improves IPC substantially, but the implementation can still "
            "redirect after speculative memory-order mistakes. Front-end taken-branch bandwidth, memory ports and "
            "other resources remain constraints; this sweep alone does not uniquely assign the remaining gap to one "
            "of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(cl), FadeIn(ct))
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(*[Indicate(grid[2 * 6 + c], color=HEAD, scale_factor=1.05) for c in range(6)])
            vo.wait_until("c")
            self.play(FadeIn(perf))
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self):
        head = label(r"The ILP wall", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(
            label("large oracle overlap relies on supplied future knowledge", font_size=26, color=YES),
            label("prediction, dependencies, resources and ordering interact", font_size=26, color=NO),
            label("selection and broadcast: \\\\ costs depend on organization and implementation",
                  font_size=26, color=COST),
            label("width, caches, energy and multiple cores: \\ workload-dependent trade-offs", font_size=26,
                  color=HEAD),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "This illustrates an instruction-level parallelism trade-off. <bookmark mark='a'/> An offline oracle "
            "exposes large overlap by supplying knowledge and resources that a real core lacks. Its "
            "twenty-four-hundred figure is not independently available hardware parallelism. <bookmark mark='b'/> "
            "Finite lookahead, prediction, memory ordering and front-end bandwidth restrict useful overlap in the "
            "functional model. Larger windows can still help other workloads, especially when they expose "
            "independent misses or long-latency work. <bookmark mark='c'/> Increasing width also adds bypass, "
            "selection, port, wiring and energy costs. Those costs depend on the implementation; not every design "
            "uses one fully connected broadcast structure. <bookmark mark='d'/> Designers balance wider cores, "
            "caches, multiple cores and other techniques. Fetch, decode, issue and retirement widths are different "
            "metrics, and there is no universal four-to-eight-wide stopping point."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
