from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from explainer.lm.pocket import lr_factor
from videos.frontier.common import Plot, eval_curve, label, load, note, source


def river_path(steps=320, seed=4):
    """Noisy gradient descent on a 'river valley' f = 12 (y - 0.5 sin x)^2 + 0.4 (5 - x): steep walls, a slowly
    descending floor.  Constant learning rate, then a linear decay over the last 30% (computed, not drawn)."""
    rng = np.random.default_rng(seed)

    def f(p):
        return 12 * (p[1] - 0.5 * np.sin(p[0])) ** 2 + 0.4 * (5 - p[0])

    def grad(p):
        r = p[1] - 0.5 * np.sin(p[0])
        return np.array([-12 * r * np.cos(p[0]) - 0.4, 24 * r])
    p = np.array([-2.6, 0.5 * np.sin(-2.6) + 0.15])
    path, losses, lrs = [p.copy()], [f(p)], []
    for t in range(steps):
        lr = 0.065 if t < int(0.7 * steps) else 0.065 * (1 - 0.95 * (t - 0.7 * steps) / (0.3 * steps))
        g = grad(p) + rng.normal(0, 1.2, 2) * np.array([0.3, 1.0])
        p = p - lr * g
        path.append(p.copy())
        losses.append(f(p))
        lrs.append(lr)
    return np.array(path), np.array(losses), int(0.7 * steps)


class Schedule(VoiceoverScene):
    def construct(self):
        self.res = load("schedule")
        self.shapes()
        self.real_runs()
        self.river()
        self.practice()

    # ------------------------------------------------------------------
    def shapes(self):
        T = 1000
        t = np.arange(T)
        cos = np.array([lr_factor(s, T, "cosine", 50, final=0.1) for s in t])
        wsd = np.array([lr_factor(s, T, "wsd", 50, decay_frac=0.2, final=0.1) for s in t])
        plot = Plot(x_range=(0, T), y_range=(0, 1.1), width=8.5, height=3.8, x_ticks=[0, 250, 500, 750, 1000],
                    y_ticks=[0, 0.5, 1], x_fmt=lambda v: MathTex(rf"{int(v / 10)}\%", font_size=24, color=GREY_A),
                    x_label=r"progress through training", y_label=r"learning rate (fraction of peak)")
        plot.move_to(DOWN * 0.5)
        lc = plot.line(t, cos, color=C.LR, stroke_width=4)
        lw = plot.line(t, wsd, color=C.KEPT, stroke_width=4)
        tc = label(r"warmup, then cosine decay", font_size=26, color=C.LR).next_to(plot.c2p(520, 0.55), RIGHT, buff=0.1)
        tw = label(r"warmup--stable--decay (WSD)", font_size=26, color=C.KEPT).next_to(plot.c2p(400, 1.0), UP, buff=0.1)
        wu = Brace(Line(plot.c2p(0, 0), plot.c2p(50, 0)), DOWN, color=GREY_B)
        wl = label(r"warmup", font_size=22, color=GREY_B).next_to(wu, DOWN, buff=0.05)
        head = label(r"The learning rate over a run", font_size=36).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The learning rate sets how big each step is, and how it changes over the run matters a lot. Runs begin "
            "with a short warmup, ramping up from near zero, because big steps on a freshly initialized network can "
            "blow it up. <bookmark mark='c'/> Then the rate decays. The classic choice is a cosine curve, down to a "
            "tenth of the peak. <bookmark mark='w'/> Cosine has a catch: you must choose the length of the run in "
            "advance. Stop halfway, and the rate was never brought down. The alternative is warmup, stable, decay: "
            "hold the peak for most of the run, and decay only in the last fifth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), GrowFromCenter(wu), FadeIn(wl))
            vo.wait_until("c")
            self.play(Create(lc), FadeIn(tc), run_time=1.5)
            vo.wait_until("w")
            self.play(Create(lw), FadeIn(tw), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_runs(self):
        r = self.res
        cos100, wsd100 = r["sched_cos_100"], r["sched_wsd_100"]
        wsd050, wsd075, cos050 = r["sched_wsd_050"], r["sched_wsd_075"], r["sched_cos_050"]
        curves = {}
        for k, run in [("cos100", cos100), ("wsd100", wsd100), ("wsd050", wsd050), ("wsd075", wsd075), ("cos050", cos050)]:
            _, tok, val = eval_curve(run)
            curves[k] = (tok / 1e6, val)
        T = curves["cos100"][0][-1]
        lo = min(min(v) for _, v in curves.values())
        hi = 5.2
        plot = Plot(x_range=(0, T), y_range=(lo - 0.05, hi), width=9.2, height=4.6, x_ticks=[0, 1, 2, 3, 4, 5],
                    y_ticks=list(np.round(np.arange(np.ceil((lo - 0.05) * 10) / 10, hi + 0.01, 0.2), 1)),
                    x_label=r"training tokens (millions)", y_label=r"validation loss")
        plot.move_to(DOWN * 0.4 + LEFT * 0.4)

        def line(k, color, w=4):
            x, v = curves[k]
            return plot.line(x, np.minimum(v, hi), color=color, stroke_width=w)
        lc, lw = line("cos100", C.LR), line("wsd100", C.KEPT)
        b5, b7 = line("wsd050", C.KEPT, 3), line("wsd075", C.KEPT, 3)
        c5 = line("cos050", C.LR, 2.5)
        fc, fw = curves["cos100"][1][-1], curves["wsd100"][1][-1]
        f5, fc5 = curves["wsd050"][1][-1], curves["cos050"][1][-1]
        self.final = (fc, fw, f5, fc5)
        kc = label(rf"cosine {fc:.3f}", font_size=24, color=C.LR).next_to(plot.c2p(T, fc), RIGHT, buff=0.1).shift(UP * 0.15)
        kw = label(rf"WSD {fw:.3f}", font_size=24, color=C.KEPT).next_to(plot.c2p(T, fw), RIGHT, buff=0.1).shift(DOWN * 0.15)
        head = label(r"Real runs: one pocket model, same data, two schedules", font_size=32).to_edge(UP, buff=0.35)
        br = label(r"WSD cooldown branches, started at 40\% and 60\%", font_size=24, color=C.KEPT).next_to(plot.c2p(T * 0.35, lo + 0.25), UP, buff=0.0)
        with self.voiceover(
            "Here are both schedules on one of our pocket models, with the same data. <bookmark mark='a'/> During the "
            "stable phase, WSD's loss lags behind. <bookmark mark='d'/> Then its decay begins, and the loss drops off a "
            "cliff, finishing level with cosine. <bookmark mark='b'/> And the stable phase can be reused: branch off and "
            "decay early, here at forty and sixty percent of the way, and each branch lands where a separate cosine "
            "run of that length would. One long run gives you a model at every budget."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("a")
            self.play(Create(lc), Create(lw), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(kc), FadeIn(kw))
            vo.wait_until("b")
            self.play(Create(b5), Create(b7), FadeIn(br), run_time=1.5)
            self.play(Create(c5), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def river(self):
        path, losses, t_decay = river_path()
        ax = Axes(x_range=[-3, 5.2, 1], y_range=[-1.3, 1.5, 1], x_length=8.0, y_length=3.6,
                  axis_config={"include_ticks": False, "stroke_color": GREY_D}).move_to(UP * 1.2)
        xs = np.linspace(-3, 5.2, 200)
        walls = VGroup(*[ax.plot(lambda x, o=o: 0.5 * np.sin(x) + o, x_range=[-3, 5.2], color=GREY_C, stroke_width=1.2)
                         for o in (-0.55, -0.3, -0.12, 0.12, 0.3, 0.55)])
        floor = ax.plot(lambda x: 0.5 * np.sin(x), x_range=[-3, 5.2], color=BLUE_D, stroke_width=3)
        del xs
        hot = VMobject(stroke_color=C.LR, stroke_width=2).set_points_as_corners([ax.c2p(*q) for q in path[:t_decay]])
        cool = VMobject(stroke_color=C.KEPT, stroke_width=2.5).set_points_as_corners([ax.c2p(*q) for q in path[t_decay - 1:]])
        lp = Plot(x_range=(0, len(losses)), y_range=(0, max(1.2, float(np.percentile(losses, 98)))), width=8.0, height=2.0,
                  x_ticks=[], y_ticks=[], x_label=r"steps", y_label=r"loss")
        lp.move_to(DOWN * 2.3)
        l1 = lp.line(np.arange(t_decay), np.minimum(losses[:t_decay], lp.y_range[1]), color=C.LR, stroke_width=2.5)
        l2 = lp.line(np.arange(t_decay - 1, len(losses)), np.minimum(losses[t_decay - 1:], lp.y_range[1]), color=C.KEPT, stroke_width=2.5)
        tag = note(r"computed toy: noisy gradient descent on $f = 12\,(y - \tfrac12\sin x)^2 + 0.4\,(5 - x)$").to_corner(DL, buff=0.2)
        ah = label(r"high learning rate: bouncing between the walls", font_size=24, color=C.LR).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        ac = label(r"decay: settles onto the floor", font_size=24, color=C.KEPT).next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        src = source(r"after Wen et al., \emph{Understanding Warmup-Stable-Decay Learning Rates: A River Valley Loss Landscape} (2024)")
        with self.voiceover(
            "Why does the loss fall so suddenly? One picture: late in training, the loss landscape looks like a river "
            "valley, with steep walls and a slowly descending floor. <bookmark mark='h'/> At a high learning rate, the "
            "optimizer bounces between the walls while drifting downstream. <bookmark mark='c'/> Lower the rate, and "
            "it settles onto the valley floor, revealing progress it had already made."
        ) as vo:
            self.play(FadeIn(walls), Create(floor), FadeIn(lp), FadeIn(tag), FadeIn(src))
            vo.wait_until("h")
            self.play(Create(hot), Create(l1), FadeIn(ah), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(Create(cool), Create(l2), FadeIn(ac), run_time=2.0, rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        items = VGroup(
            label(r"\textbf{DeepSeek-V3}: peak learning rate for 10T tokens, then decay over 4.3T", font_size=28),
            label(r"\textbf{Llama 3 405B}: cosine; annealed to zero over the last 40M tokens; checkpoint averaging", font_size=28),
            label(r"\textbf{Kimi K3} (2026): fitted scaling laws for both schedules, chose cosine", font_size=28),
            label(r"batch size grows too: from a few million to tens of millions of tokens per step", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.1)
        head = label(r"In practice", font_size=36).to_edge(UP, buff=0.5)
        src = source(r"DeepSeek-V3 report; Llama 3 paper; Kimi K3 report (arXiv 2607.24653)")
        with self.voiceover(
            "Frontier runs use variations of both. DeepSeek-V3 held its peak learning rate for ten trillion tokens, "
            "then decayed over the next four. Llama 3 used cosine, annealed to zero over its last forty million "
            "tokens, and averaged checkpoints. Kimi K3 fitted scaling laws for both schedules and chose cosine. And "
            "the batch size usually grows as training goes, from a few million tokens per step to tens of millions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.6), run_time=vo.remaining() * 0.75)
        self.wait(0.4)
        self.clear_scene()
