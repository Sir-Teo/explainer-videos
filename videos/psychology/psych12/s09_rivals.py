from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403
from videos.psychology.psych12.s04_roc import roc_axes


class Rivals(VoiceoverScene):
    def construct(self):
        self.card()
        self.threshold()
        self.dual()

    def card(self):
        card = chapter_card(8, r"Threshold or signal detection?", r"Is there a line below which nothing gets through?",
                            lit={1961: r"Swets, Tanner and Birdsall", 1994: r"Yonelinas"}, part=PART, scale=("mind",),
                            marr=("how",))
        with self.voiceover(
            "Chapter eight. Threshold or signal detection?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def threshold(self):
        d = load("rivals")
        head = heading(r"The old idea: \ a real threshold, \ and guessing below it")
        R = roc_axes([-3.2, -0.2, 0], size=4.8)
        rx = R.ax
        diag = DashedLine(rx.c2p(0, 0), rx.c2p(1, 1), color=GREY_C, stroke_width=2)
        pts = VGroup(*[Dot(rx.c2p(float(f), float(h)), radius=0.08, color=YOU) for h, f in zip(d["hit"], d["fa"])])
        ht = curve(rx, d["fa_grid"], d["ht_curve"], MISS, stroke_width=4)
        sd = curve(rx, d["fa_grid"], d["sdt_curve"], MODEL, stroke_width=4)
        p0 = Dot(rx.c2p(0, d["ht_p"]), radius=0.07, color=MISS)
        rows = rows_of([
            (r"high-threshold model: \ a signal is detected with probability $p$, \ or not at all", MISS),
            (r"undetected, \ the observer guesses yes at some rate $g$: \ $H = p + (1 - p)\,g$, \ $F = g$", MISS),
            (r"so its ROC is a straight line from $(0, p)$ to $(1, 1)$", MISS),
            (rf"on the rating data: \ the line misses badly \ (squared error {d['sse_ht']:.3f}); \ the curve fits \ "
             rf"({d['sse_sdt']:.3f})", MODEL),
            (r"curved ROCs in detection were early evidence that there is no line below which nothing gets through",
             THRESH),
        ], 5.4, 26, 0.26).move_to([3.6, -0.1, 0])
        keep_in_frame(rows)
        tag = simulated_tag(r"simulated: \ chapter 6's rating study")
        with self.voiceover(
            "Signal detection had a rival, and it was the older idea. <bookmark mark='a'/> In the high-threshold "
            "model a signal either crosses a real threshold and is detected, with some probability p, or it "
            "doesn't get through at all. <bookmark mark='b'/> When nothing gets through, the observer guesses, "
            "saying yes at some rate that payoffs can push up or down. <bookmark mark='c'/> Work out the ROC: as "
            "the guessing rate moves, the point moves along a straight line from p on the left edge to the top "
            "right corner. <bookmark mark='d'/> Now put chapter six's ratings on the plot. They curve, and the "
            "straight line can't follow them; the signal-detection curve can. <bookmark mark='e'/> Curved ROCs like "
            "these, in vision and hearing, were among the first evidence that a sensory threshold, in the old sense "
            "of a line below which nothing gets through, doesn't exist. The threshold of Part 11 is a point on a "
            "curve, not a gate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(R), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(p0), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ht), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.2), Create(sd), FadeIn(rows[3]),
                      run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def dual(self):
        d = load("rivals")
        src = archive.YONELINAS_1994
        head = heading(r"A mixture: \ all-or-none recollection plus graded familiarity")
        R = roc_axes([-3.2, -0.2, 0], size=4.8)
        rx = R.ax
        diag = DashedLine(rx.c2p(0, 0), rx.c2p(1, 1), color=GREY_C, stroke_width=2)
        pts = VGroup(*[Dot(rx.c2p(float(f), float(h)), radius=0.08, color=YOU) for h, f in zip(d["hit"], d["fa"])])
        sd = curve(rx, d["fa_grid"], d["sdt_curve"], MODEL, stroke_width=4)
        dp = curve(rx, d["fa_grid"], d["dp_curve"], RIVAL, stroke_width=4)
        lg = legend([(MODEL, r"unequal-variance detection"), (RIVAL, r"recollection + familiarity")], font_size=22
                    ).move_to(rx.c2p(0.62, 0.18))
        rows = rows_of([
            (r"Yonelinas (1994): \ sometimes a studied word is simply recollected, \ yes for sure", RIVAL),
            (r"otherwise, \ familiarity, \ judged like any signal", RIVAL),
            (rf"fitted here: \ recollection on {pct(d['dp_r'])} of studied words", RIVAL),
            (rf"both curves fit the five points \ (squared errors {d['sse_sdt']:.3f} and {d['sse_dp']:.3f})", WHITE),
            (r"they part only at the edges, \ where data are thin: \ the dispute is still open (Part 21)", THRESH),
        ], 5.4, 26, 0.26).move_to([3.6, -0.1, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(src.cite), simulated_tag(r"simulated: \ data from the unequal-variance observer"))
        with self.voiceover(
            "In memory the rival is subtler. <bookmark mark='a'/> Andrew Yonelinas proposed in 1994 that sometimes a "
            "studied word is simply recollected: you remember seeing it, and you say old with full confidence. "
            "<bookmark mark='b'/> When it isn't, you fall back on familiarity, which behaves like any graded signal. "
            "<bookmark mark='c'/> Fit that mixture to the same five points, generated, remember, by an "
            f"unequal-variance observer. It says {100 * d['dp_r']:.0f} percent of studied words were recollected. "
            "<bookmark mark='d'/> And it fits essentially as well as the model that made the data. "
            "<bookmark mark='e'/> The two curves part only at the very edges of the square, where the strictest and "
            "laxest criteria are and where data are scarce. That's why the debate about what recognition's ROC "
            "means has run for thirty years. The shape of a curve can rule out a model, as it ruled out the gate. "
            "It can't always pick between the survivors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), FadeIn(R), Create(diag), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(dp), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(sd), FadeIn(lg), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
