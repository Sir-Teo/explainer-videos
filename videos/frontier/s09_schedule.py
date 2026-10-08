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
        lu = plot.line(t[:51], cos[:51], color=C.LR, stroke_width=4)
        lc = plot.line(t[50:], cos[50:], color=C.LR, stroke_width=4)
        lw = plot.line(t, wsd, color=C.KEPT, stroke_width=4)
        half = plot.vline(500, color=GREY_B, dash_length=0.08)
        hd = Dot(plot.c2p(500, cos[500]), radius=0.08, color=C.LR)
        hl = label(rf"stop at 50\%: still at {100 * cos[500]:.0f}\% of peak", font_size=22, color=C.LR).next_to(hd, DL, buff=0.1)
        tc = label(r"warmup, then cosine decay", font_size=26, color=C.LR).next_to(plot.c2p(520, 0.55), RIGHT, buff=0.1)
        tw = label(r"warmup--stable--decay (WSD)", font_size=26, color=C.KEPT).next_to(plot.c2p(400, 1.0), UP, buff=0.1)
        wl = label(r"warmup", font_size=22, color=C.LR).next_to(plot.c2p(50, 0.2), RIGHT, buff=0.12)
        head = label(r"The learning rate over a run", font_size=36).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The learning rate sets how big each step is, and how it changes over the run matters a lot. "
            "<bookmark mark='u'/> Runs begin with a short warmup, ramping up from near zero, because big steps on a "
            "freshly initialized network can blow it up. <bookmark mark='c'/> Then the rate decays. The classic "
            "choice is a cosine curve, down to a tenth of the peak. <bookmark mark='h'/> Cosine has a catch: you "
            "must choose the length of the run in advance. Stop halfway, and the rate was never brought down. "
            "<bookmark mark='w'/> The alternative is warmup, stable, decay: hold the peak for most of the run, and "
            "decay only in the last fifth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("u")
            self.play(Create(lu), FadeIn(wl), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(lc), FadeIn(tc), run_time=1.5)
            vo.wait_until("h")
            self.play(Create(half), FadeIn(hd), FadeIn(hl))
            vo.wait_until("w")
            self.play(FadeOut(half), FadeOut(hd), FadeOut(hl), Create(lw), FadeIn(tw), run_time=1.5)
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
            m = v <= hi
            return plot.line(x[m], v[m], color=color, stroke_width=w)
        lc, lw = line("cos100", C.LR), line("wsd100", C.KEPT)
        b5, b7 = line("wsd050", C.KEPT, 3), line("wsd075", C.KEPT, 3)
        c5 = line("cos050", C.LR, 2.5)
        fc, fw = curves["cos100"][1][-1], curves["wsd100"][1][-1]
        f5, fc5 = curves["wsd050"][1][-1], curves["cos050"][1][-1]
        self.final = (fc, fw, f5, fc5)
        xs, vc_ = curves["cos100"]
        stable = (xs >= 1.5) & (xs <= 4.0)
        lag = curves["wsd100"][1][stable] - np.interp(xs[stable], *curves["cos100"])
        assert 0 < lag.mean() < 0.05 and (round(fw, 2), round(fc, 2)) == (4.18, 4.30) and f5 < fc5 - 0.2
        del vc_
        k5 = label(rf"{f5:.2f}", font_size=22, color=C.KEPT).next_to(plot.c2p(curves["wsd050"][0][-1], f5), DOWN, buff=0.12)
        kc5 = label(rf"{fc5:.2f}", font_size=22, color=C.LR).next_to(plot.c2p(curves["cos050"][0][-1], fc5), UP, buff=0.12)
        kc = label(rf"cosine {fc:.3f}", font_size=24, color=C.LR).next_to(plot.c2p(T, fc), RIGHT, buff=0.1).shift(UP * 0.15)
        kw = label(rf"WSD {fw:.3f}", font_size=24, color=C.KEPT).next_to(plot.c2p(T, fw), RIGHT, buff=0.1).shift(DOWN * 0.15)
        head = label(r"Real runs: one pocket model, same data, two schedules", font_size=32).to_edge(UP, buff=0.35)
        br = label(r"WSD cooldown branches,\\started at 40\% and 60\%", font_size=24, color=C.KEPT)
        br.next_to(plot.c2p(0.15, lo + 0.05), UR, buff=0.0)
        with self.voiceover(
            "Here are both schedules on one of our pocket models, with the same data. <bookmark mark='a'/> During the "
            "stable phase, WSD's loss lags slightly behind. <bookmark mark='d'/> Then its decay begins, and the loss "
            "drops off a cliff, finishing below cosine. Larger published comparisons usually find the two about "
            "level. <bookmark mark='b'/> And the stable phase can be reused: branch off and decay early, here at forty "
            "and sixty percent of the way, and each branch is a finished model for that budget. <bookmark mark='h'/> "
            "Our half-length branch even beat a separate half-length cosine run. One long run gives you a model at "
            "every budget."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("a")
            self.play(Create(lc), Create(lw), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(kc), FadeIn(kw))
            vo.wait_until("b")
            self.play(Create(b5), Create(b7), FadeIn(br), run_time=1.5)
            vo.wait_until("h")
            self.play(Create(c5), run_time=1.0)
            self.play(FadeIn(k5), FadeIn(kc5))
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
        lp.move_to(DOWN * 2.05)
        l1 = lp.line(np.arange(t_decay), np.minimum(losses[:t_decay], lp.y_range[1]), color=C.LR, stroke_width=2.5)
        l2 = lp.line(np.arange(t_decay - 1, len(losses)), np.minimum(losses[t_decay - 1:], lp.y_range[1]), color=C.KEPT, stroke_width=2.5)
        tag = note(r"computed toy: noisy gradient descent on $f = 12\,(y - \tfrac12\sin x)^2 + 0.4\,(5 - x)$").to_corner(UL, buff=0.2)
        ac = label(r"decay: settles onto the floor", font_size=24, color=C.KEPT).next_to(ax, UP, buff=0.0).align_to(ax, RIGHT)
        ah = label(r"high learning rate: bouncing between the walls", font_size=24, color=C.LR).next_to(ac, UP, buff=0.08).align_to(ax, LEFT)
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
        head = label(r"In practice: schedules from the labs' reports", font_size=34).to_edge(UP, buff=0.35)
        src = source(r"DeepSeek-V3 report, Sec.\ 4.2; Llama 3 paper, Sec.\ 3.4; Kimi K3 report (arXiv 2607.24653)")
        centers = [(-3.45, 1.0), (3.55, 1.0), (-3.45, -2.1), (3.55, -2.1)]

        def panel(i, title, x_range, y_range, x_ticks, y_ticks, x_label, y_fmt=None):
            pl = Plot(x_range=x_range, y_range=y_range, width=5.0, height=1.65, x_ticks=x_ticks, y_ticks=y_ticks,
                      x_label=x_label, font_size=20, y_fmt=y_fmt)
            pl.move_to([*centers[i], 0])
            t = label(title, font_size=24).next_to(pl, UP, buff=0.25).align_to(pl, LEFT)
            return pl, t
        pct = lambda v: f"{int(round(100 * v))}\\%"  # noqa: E731
        # DeepSeek-V3: peak to 10T tokens, cosine decay to 10% over 4.3T, then 10% for 333B and ~3.3% for 167B
        p1, t1 = panel(0, r"\textbf{DeepSeek-V3}: hold the peak for 10T tokens, then decay", (0, 14.8), (0, 1.1),
                       [0, 5, 10, 14.8], [0, 1], r"tokens (trillions)", pct)
        x = np.linspace(0, 14.8, 600)
        y = np.where(x < 10, 1.0, np.where(x < 14.3, 0.1 + 0.45 * (1 + np.cos(np.pi * (x - 10) / 4.3)),
                                           np.where(x < 14.633, 0.1, 7.3 / 220)))
        l1 = p1.line(np.r_[0, x], np.r_[0, y], color=C.LR)
        # Llama 3 405B: cosine; the last 40M tokens annealed linearly to zero, then checkpoint averaging
        p2, t2 = panel(1, r"\textbf{Llama 3 405B}: cosine, annealed to 0 at the end", (0, 15.6), (0, 1.1),
                       [0, 5, 10, 15.6], [0, 1], r"tokens (trillions)", pct)
        x2 = np.linspace(0, 15.6, 400)
        l2 = p2.line(np.r_[0, x2, 15.6], np.r_[0, 0.01 + 0.495 * (1 + np.cos(np.pi * x2 / 15.6)), 0], color=C.LR)
        n2 = label(r"last 40M tokens: to zero; checkpoints averaged", font_size=18, color=GREY_A).next_to(p2.c2p(15.6, 0.9), LEFT, buff=0.0)
        # Kimi K3: fitted scaling laws for both, chose cosine
        p3, t3 = panel(2, r"\textbf{Kimi K3}: fitted scaling laws for both, chose cosine", (0, 1), (0, 1.1),
                       [0, 1], [0, 1], r"fraction of training", pct)
        x3 = np.linspace(0, 1, 300)
        l3c = p3.line(x3, 0.05 + 0.475 * (1 + np.cos(np.pi * x3)), color=C.LR, stroke_width=4)
        l3w = DashedVMobject(p3.line(x3, np.where(x3 < 0.8, 1.0, 1 - 0.95 * (x3 - 0.8) / 0.2), color=C.KEPT, stroke_width=2.5), num_dashes=40)
        k3 = VGroup(label(r"cosine (chosen)", font_size=18, color=C.LR), label(r"WSD", font_size=18, color=C.KEPT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(p3.c2p(0.04, 0.08), aligned_edge=DL)
        # Llama 3 405B batch size: 4M tokens, 8M after 252M tokens, 16M after 2.87T tokens
        p4, t4 = panel(3, r"\textbf{Batch size grows}: Llama 3 405B, tokens per step", (0, 15.6), (0, 18),
                       [0, 5, 10, 15.6], [4, 8, 16], r"tokens (trillions)", lambda v: f"{v:g}\\text{{M}}")
        l4 = p4.line([0, 0.252, 0.252, 2.87, 2.87, 15.6], [4, 4, 8, 8, 16, 16], color=C.DATA)
        sch = note(r"shapes as described in each report").to_corner(DL, buff=0.15)
        with self.voiceover(
            "Frontier runs use variations of both. <bookmark mark='a'/> DeepSeek-V3 held its peak learning rate for "
            "ten trillion tokens, then decayed over the next four. <bookmark mark='b'/> Llama 3 used cosine, "
            "annealed to zero over its last forty million tokens, and averaged checkpoints. <bookmark mark='c'/> "
            "Kimi K3 fitted scaling laws for both schedules and chose cosine. <bookmark mark='d'/> And the batch "
            "size usually grows as training goes, from a few million tokens per step to tens of millions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(sch))
            for m, (pl, t, lines, texts) in zip("abcd", [(p1, t1, [l1], []), (p2, t2, [l2], [n2]), (p3, t3, [l3c, l3w], [k3]),
                                                       (p4, t4, [l4], [])]):
                vo.wait_until(m)
                self.play(FadeIn(pl), FadeIn(t), run_time=0.6)
                self.play(*[Create(x_) for x_ in lines], *[FadeIn(x_) for x_ in texts], run_time=1.2)
        self.wait(0.4)
        self.clear_scene()
