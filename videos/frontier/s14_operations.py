from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import LLAMA3, Plot, bar_rows, label, note, pow10_label, source

MTTF = [  # (GPUs per job, mean time to failure in hours, measured?) -- Kokolis et al. (Meta) 2024
    (8, 47.7 * 24, True),
    (1024, 7.9, True),
    (16_384, 1.8, False),
    (131_072, 0.23, False),
]

LLAMA3_CAUSES = [  # share of the 419 unexpected interruptions (Llama 3 paper, Table 5)
    (r"faulty GPU", 30.1),
    (r"GPU memory (HBM3)", 17.2),
    (r"software bug", 12.9),
    (r"network switch or cable", 8.4),
    (r"unplanned host maintenance", 7.6),
    (r"GPU SRAM", 4.5),
    (r"GPU system processor", 4.1),
]


class Operations(VoiceoverScene):
    def construct(self):
        self.failure_law()
        self.llama_snapshot()
        self.checkpoints()
        self.silent()

    # ------------------------------------------------------------------
    def failure_law(self):
        plot = Plot(x_range=(4, 3e5), y_range=(0.1, 3000), width=8.5, height=4.6, log_x=True, log_y=True,
                    x_ticks=[10, 100, 1000, 1e4, 1e5], y_ticks=[0.1, 1, 10, 100, 1000],
                    x_fmt=lambda v: pow10_label(int(round(np.log10(v)))),
                    y_fmt=lambda v: MathTex(f"{v:g}", font_size=24, color=GREY_A),
                    x_label=r"GPUs in one job", y_label=r"mean time between failures (hours)")
        plot.move_to(LEFT * 1.4 + DOWN * 0.3)
        xs = np.array([6, 2e5])
        k = MTTF[0][0] * MTTF[0][1]
        line = plot.line(xs, k / xs, color=GREY_C, stroke_width=2.5)
        line = DashedVMobject(line, num_dashes=40)
        pts = VGroup()
        labs = VGroup()
        texts = [r"8 GPUs: 48 days", r"1{,}024: 7.9 hours", r"16{,}384: 1.8 hours (projected)", r"131{,}072: 14 minutes (projected)"]
        for (n, h, measured), t in zip(MTTF, texts):
            d = Dot(plot.c2p(n, h), radius=0.09, color=C.REMOVED if measured else GREY_A)
            if not measured:
                d.set_fill(opacity=0).set_stroke(GREY_A, width=3)
            pts.add(d)
            labs.add(label(t, font_size=24, color=C.REMOVED if measured else GREY_A).next_to(d, RIGHT, buff=0.2))
        head = label(r"More GPUs, more failures", font_size=38).to_edge(UP, buff=0.4)
        src = source(r"Kokolis et al.\ (Meta), \emph{Revisiting Reliability in Large-Scale ML Research Clusters}, 2024")
        with self.voiceover(
            "A run like this lasts weeks or months, and keeping it alive is a job in itself, because the more GPUs you "
            "use, the more often something breaks. <bookmark mark='a'/> Meta measured this across its research "
            "clusters: an eight-GPU job ran, on average, forty-eight days between failures. <bookmark mark='b'/> A "
            "thousand-GPU job: about eight hours. <bookmark mark='c'/> Failures scale with the number of parts, so at "
            "sixteen thousand GPUs you'd expect one every couple of hours, <bookmark mark='d'/> and at a hundred "
            "thousand, about every quarter of an hour."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(src))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                anims = [FadeIn(pts[i], scale=2), FadeIn(labs[i])]
                if i == 2:
                    anims.append(Create(line))
                self.play(*anims, run_time=0.9)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def llama_snapshot(self):
        days, n = LLAMA3["days"], LLAMA3["interruptions"]
        hours_each = days * 24 / n
        assert abs(hours_each - 2.78) < 0.05
        rng = np.random.default_rng(5)
        t = np.sort(rng.uniform(0, days, n))
        strip = Rectangle(width=12.0, height=0.6, stroke_color=GREY_B, stroke_width=1.5).move_to(UP * 2.0)
        ticks = VGroup(*[Line(strip.get_left() + RIGHT * 12.0 * x / days + UP * 0.3,
                              strip.get_left() + RIGHT * 12.0 * x / days + DOWN * 0.3, color=C.REMOVED, stroke_width=1.2)
                         for x in t])
        dl = VGroup(*[MathTex(str(dd), font_size=22, color=GREY_A).next_to(strip.get_left() + RIGHT * 12.0 * dd / days, DOWN, buff=0.38)
                      for dd in range(0, days + 1, 9)])
        cap = label(rf"Llama 3: {n} interruptions in {days} days on 16{{,}}384 GPUs: one every {hours_each:.1f} hours",
                    font_size=30).next_to(strip, UP, buff=0.3)
        illus = note(r"(tick positions illustrative; count from the paper)").next_to(dl, DOWN, buff=0.1)
        bars = bar_rows([(name, pct, C.REMOVED, rf"{pct:.1f}\%") for name, pct in LLAMA3_CAUSES], 6.0 / 30.1,
                        font_size=24, bar_h=0.3, buff=0.12, opacity=0.8)
        bars.move_to(DOWN * 1.35)
        bh = label(r"causes of the 419 unexpected interruptions", font_size=24, color=GREY_B).next_to(bars, UP, buff=0.15)
        src = source(r"Llama Team, Meta, \emph{The Llama 3 Herd of Models} (2024), Section 3.3.4 and Table 5")
        with self.voiceover(
            "And that's what Llama 3 saw. In one fifty-four-day stretch of training on 16,384 GPUs, the job was "
            "interrupted 466 times: once every two point eight hours. <bookmark mark='c'/> About four fifths of the "
            "unexpected stops traced to hardware, mostly the GPUs themselves and their memory."
        ) as vo:
            self.play(FadeIn(cap), Create(strip), FadeIn(dl))
            self.play(LaggedStart(*[Create(k) for k in ticks], lag_ratio=0.004), FadeIn(illus), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in bars], lag_ratio=0.08), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checkpoints(self):
        L = 12.0
        x0 = -6.0
        base = Line([x0, 0.4, 0], [x0 + L, 0.4, 0], color=GREY_C, stroke_width=3)
        flags = VGroup()
        for k in range(1, 6):
            x = x0 + L * k / 6
            pole = Line([x, 0.4, 0], [x, 1.1, 0], color=C.KEPT, stroke_width=3)
            flag = Polygon([x, 1.1, 0], [x + 0.35, 0.95, 0], [x, 0.8, 0], stroke_width=0, fill_color=C.KEPT, fill_opacity=0.9)
            flags.add(VGroup(pole, flag))
        prog = Line([x0, 0.4, 0], [x0 + L * 0.58, 0.4, 0], color=C.PARAMS, stroke_width=8)
        boom = VGroup(Line(UL, DR), Line(UR, DL)).scale(0.22).set_stroke(C.REMOVED, 6).move_to([x0 + L * 0.58, 0.4, 0])
        back = CurvedArrow([x0 + L * 0.58, -0.05, 0], [x0 + L * 3 / 6, -0.05, 0], angle=-1.2, color=C.REMOVED, stroke_width=4)
        lost = label(r"work lost: since the last checkpoint", font_size=24, color=C.REMOVED).next_to(back, DOWN, buff=0.15)
        fl = label(r"checkpoints: save the full training state", font_size=26, color=C.KEPT).next_to(flags, UP, buff=0.2)
        head = label(r"Checkpoint, fail, restart", font_size=38).to_edge(UP, buff=0.5)
        facts = VGroup(
            label(r"Llama 3: over 90\% of time spent training", font_size=28),
            label(r"Gemini: redundant in-memory copies of the state raised useful time from 85\% to 97\%", font_size=28),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "So the training state is checkpointed regularly. <bookmark mark='f'/> When a GPU dies, the job restarts "
            "from the last checkpoint on healthy machines, and only the work since then is lost. "
            "<bookmark mark='g'/> Doing this well is the difference between a run that spends nine tenths of its time "
            "training and one that doesn't. Llama 3 stayed above ninety percent. Google kept redundant copies of "
            "Gemini's state in memory, so recovery took seconds, and raised the share of useful time from eighty-five "
            "to ninety-seven percent."
        ) as vo:
            self.play(FadeIn(head), Create(base), LaggedStart(*[FadeIn(f) for f in flags], lag_ratio=0.15), FadeIn(fl))
            self.play(Create(prog), run_time=2.0, rate_func=linear)
            vo.wait_until("f")
            self.play(FadeIn(boom, scale=1.5))
            self.play(Create(back), FadeIn(lost))
            vo.wait_until("g")
            self.play(FadeIn(facts[0]))
            self.play(FadeIn(facts[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def silent(self):
        items = VGroup(
            label(r"\textbf{Silent data corruption}: a chip that keeps running,\\but computes slightly wrong numbers",
                  font_size=32),
            label(r"Gemini: expected every week or two; caught by replaying steps", font_size=26, color=GREY_A),
            label(r"\textbf{The power grid notices}: when 16{,}000 GPUs pause together,\\the draw swings by tens of megawatts",
                  font_size=32),
            label(r"Llama 3 paper", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.35)
        items[2].shift(DOWN * 0.3)
        items[3].shift(DOWN * 0.3)
        src = source(r"Gemini Team, \emph{Gemini: A Family of Highly Capable Multimodal Models} (2023); Llama 3 paper")
        with self.voiceover(
            "Some failures are silent: a chip that keeps running but computes slightly wrong numbers. At Gemini's "
            "scale, Google expected such silent data corruption every week or two, and caught it by replaying "
            "steps. <bookmark mark='p'/> Even the power grid notices: when sixteen thousand GPUs pause at the same "
            "moment, Meta saw the power draw swing by tens of megawatts."
        ) as vo:
            self.play(FadeIn(items[0]), FadeIn(items[1]), FadeIn(src))
            vo.wait_until("p")
            self.play(FadeIn(items[2]), FadeIn(items[3]))
        self.wait(0.5)
        self.clear_scene()
