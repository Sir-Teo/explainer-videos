from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Plot, calc, label, load, note, pow10_label, source, train_curve
from videos.frontier.compute import STAB_LRS

FAIL = 7.0  # a run whose final loss is above this (or diverged) counts as failed


def final_or_fail(r):
    return FAIL if r["diverged"] or not np.isfinite(r["final_val"]) else min(FAIL, r["final_val"])


class Stability(VoiceoverScene):
    def construct(self):
        self.res = load("stability")
        self.spikes()
        self.sweep()
        self.logits()
        self.qk_math()
        self.fixes()

    # ------------------------------------------------------------------
    def spikes(self):
        rng = np.random.default_rng(5)
        t = np.arange(0, 1001)
        base = 2.3 + 2.6 * np.exp(-t / 170) + rng.normal(0, 0.035, len(t))
        t_spike, t_ckpt, t_end = 620, 520, 700
        bad = base[t_spike:t_end + 1].copy()
        bad += np.clip((np.arange(len(bad)) - 2) * 0.35, 0, 2.9) + rng.normal(0, 0.25, len(bad)) * (np.arange(len(bad)) > 3)
        plot = Plot(x_range=(0, 1000), y_range=(2.0, 6.2), width=8.6, height=3.0, x_label=r"training step",
                    y_label=r"loss", font_size=22)
        plot.move_to(UP * 0.75)
        ok = plot.line(t[:t_spike + 1], base[:t_spike + 1], color=C.LR, stroke_width=3)
        blow = plot.line(t[t_spike:t_end + 1], np.minimum(bad, 6.1), color=C.PENALTY, stroke_width=3)
        ck = plot.vline(t_ckpt, color=C.KEPT, dash_length=0.08)
        ckl = label(r"checkpoint", font_size=20, color=C.KEPT).next_to(plot.c2p(t_ckpt, 6.2), UP, buff=0.05)
        back = CurvedArrow(plot.c2p(t_end, 6.0), plot.c2p(t_ckpt + 10, 5.6), angle=PI / 3, color=WHITE, stroke_width=3)
        redo = plot.line(t[t_ckpt:], base[t_ckpt:] - 0.02, color=C.KEPT, stroke_width=3)
        fix = label(r"PaLM's fix: restart $\sim$100 steps earlier, skip 200--500 batches of data", font_size=24,
                    color=C.KEPT).next_to(plot, DOWN, buff=0.15)
        tag = note(r"illustrative curve").to_corner(UR, buff=0.3)
        head = label(r"Loss spikes: a big run can suddenly go wrong", font_size=34).to_edge(UP, buff=0.35)

        def card(title, body):
            g = VGroup(label(title, font_size=24), label(body, font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            box = SurroundingRectangle(g, buff=0.18, corner_radius=0.1, color=GREY_D, stroke_width=1.5)
            return VGroup(box, g)
        cards = VGroup(card(r"\textbf{PaLM} 540B (2022)", r"about 20 spikes, despite gradient clipping"),
                       card(r"\textbf{OPT-175B} (2022)", r"35+ manual restarts in two months"),
                       card(r"\textbf{Nemotron 3 Ultra} (2026)", r"2 divergences; one from gradients summed in BF16")
                       ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.55)
        if cards.width > 13.4:
            cards.scale_to_fit_width(13.4)
        src = source(r"Chowdhery et al.\ 2022 (PaLM); Zhang et al.\ 2022 (OPT); NVIDIA, arXiv 2606.15007")
        with self.voiceover(
            "Big runs are fragile. <bookmark mark='s'/> The loss can suddenly spike, and sometimes it never "
            "recovers. <bookmark mark='p'/> Google's PaLM saw about twenty spikes during training, even with gradient "
            "clipping; <bookmark mark='f'/> the fix was to restart from a checkpoint about a hundred steps earlier "
            "and skip a few hundred batches of data. <bookmark mark='o'/> Meta's OPT needed more than thirty-five "
            "manual restarts. <bookmark mark='n'/> And labs still hit this in 2026: NVIDIA's Nemotron 3 Ultra report "
            "describes two divergences, one traced to gradients being summed in sixteen-bit instead of thirty-two-bit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(tag), FadeIn(src))
            self.play(Create(ok), run_time=2.0, rate_func=linear)
            vo.wait_until("s")
            self.play(Create(blow), run_time=1.2, rate_func=linear)
            vo.wait_until("p")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("f")
            self.play(Create(ck), FadeIn(ckl), Create(back))
            self.play(blow.animate.set_stroke(opacity=0.25), FadeOut(back))
            self.play(Create(redo), FadeIn(fix), run_time=2.0, rate_func=linear)
            vo.wait_until("o")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("n")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        res = self.res
        base = np.array([final_or_fail(res[f"stab_base_{lr:.0e}"]) for lr in STAB_LRS])
        qk = np.array([final_or_fail(res[f"stab_qk_{lr:.0e}"]) for lr in STAB_LRS])
        self.base, self.qk = base, qk
        i3, i30 = STAB_LRS.index(3e-3), STAB_LRS.index(3e-2)
        assert base[i30] - base[i3] > 0.15 and abs(qk[i30] - qk[i3]) < 0.03 and base[i3] < qk[i3]
        assert not any(res[k]["diverged"] for k in res)
        lo, hi = min(base.min(), qk.min()), max(base.max(), qk.max())
        plot = Plot(x_range=(2e-4, 1.5e-1), y_range=(lo - 0.1, hi + 0.1), width=8.6, height=4.4, log_x=True,
                    x_ticks=[1e-3, 1e-2, 1e-1], y_ticks=list(np.round(np.arange(np.ceil((lo - 0.1) * 5) / 5, hi + 0.1, 0.2), 1)),
                    x_fmt=lambda v: pow10_label(int(round(np.log10(v)))), x_label=r"peak learning rate",
                    y_label=r"final validation loss")
        plot.move_to(DOWN * 0.4 + LEFT * 0.8)
        lb = plot.line(STAB_LRS, base, color=C.PENALTY, stroke_width=4)
        lq = plot.line(STAB_LRS, qk, color=C.KEPT, stroke_width=4)
        db = plot.dots(STAB_LRS, base, C.PENALTY, radius=0.07)
        dq = plot.dots(STAB_LRS, qk, C.KEPT, radius=0.07)
        tb = label(r"standard attention", font_size=26, color=C.PENALTY)
        tq = label(r"with QK-norm", font_size=26, color=C.KEPT)
        VGroup(tb, tq).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(plot, RIGHT, buff=0.3).shift(UP * 1.0)
        band = Polygon(plot.c2p(3e-3, lo - 0.1), plot.c2p(3e-2, lo - 0.1), plot.c2p(3e-2, hi + 0.1), plot.c2p(3e-3, hi + 0.1),
                       stroke_width=0, fill_color=C.KEPT, fill_opacity=0.08)
        bt = VGroup(label(r"from 0.003 to 0.03:", font_size=22, color=GREY_A),
                    label(rf"QK-norm {qk[i3]:.2f} $\rightarrow$ {qk[i30]:.2f}", font_size=22, color=C.KEPT),
                    label(rf"standard {base[i3]:.2f} $\rightarrow$ {base[i30]:.2f}", font_size=22, color=C.PENALTY)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(tq, DOWN, buff=0.5).align_to(tq, LEFT)
        head = label(r"Real sweep: 12 pocket models, 6 learning rates, with and without QK-norm", font_size=30).to_edge(UP, buff=0.35)
        src = source(r"after Wortsman et al., \emph{Small-scale proxies for large-scale Transformer training instabilities} (2023)")
        with self.voiceover(
            "Many instabilities can be reproduced in miniature. Researchers at Google showed in 2023 that small "
            "models trained at high learning rates fail in the same ways big ones do. So we trained twelve pocket "
            "models: six learning rates, each with standard attention <bookmark mark='q'/> and with a fix called "
            "QK-norm. <bookmark mark='r'/> These runs are short, so nothing blows up outright. But look at the shape. "
            "<bookmark mark='f'/> From 0.003 to 0.03, the QK-norm model's loss barely moves, while the standard "
            "model's climbs. QK-norm makes training far less sensitive to the learning rate, for a small cost at the "
            "best setting."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(src))
            self.play(Create(lb), FadeIn(db), FadeIn(tb), run_time=1.5)
            vo.wait_until("q")
            self.play(Create(lq), FadeIn(dq), FadeIn(tq), run_time=1.5)
            vo.wait_until("f")
            self.play(FadeIn(band), FadeIn(bt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def logits(self):
        res = self.res
        pb = np.array([np.array(res[f"stab_base_{lr:.0e}"]["probes"], float)[:, 1].max() for lr in STAB_LRS])
        pq = np.array([np.array(res[f"stab_qk_{lr:.0e}"]["probes"], float)[:, 1].max() for lr in STAB_LRS])
        assert round(pb[0]) == 9 and pb[STAB_LRS.index(1e-2)] > 100 and 9_000 < pb[-1] < 12_000 and pq.max() < 25
        plot = Plot(x_range=(2e-4, 1.5e-1), y_range=(2, 3e4), width=8.6, height=4.4, log_x=True, log_y=True,
                    x_ticks=[1e-3, 1e-2, 1e-1], y_ticks=[10, 100, 1000, 10000],
                    x_fmt=lambda v: pow10_label(int(round(np.log10(v)))), y_fmt=lambda v: pow10_label(int(round(np.log10(v)))),
                    x_label=r"peak learning rate", y_label=r"largest attention score $q\cdot k/\sqrt{d}$ during training")
        plot.move_to(DOWN * 0.4 + LEFT * 1.2)
        lb = plot.line(STAB_LRS, pb, color=C.PENALTY, stroke_width=4)
        lq = plot.line(STAB_LRS, pq, color=C.KEPT, stroke_width=4)
        db = plot.dots(STAB_LRS, pb, C.PENALTY, radius=0.07)
        dq = plot.dots(STAB_LRS, pq, C.KEPT, radius=0.07)
        nb = VGroup(*[label(rf"{v:,.0f}".replace(",", "{,}"), font_size=22, color=C.PENALTY).next_to(d, UL, buff=0.05)
                      for v, d in zip(pb, db) if v > 50])
        tb = label(r"standard", font_size=26, color=C.PENALTY).next_to(plot, RIGHT, buff=0.3).shift(UP * 1.4)
        tq = label(r"QK-norm:\\always below 25", font_size=26, color=C.KEPT).next_to(plot.c2p(1.5e-1, pq[-1]), RIGHT, buff=0.25)
        tb.next_to(plot.c2p(1.5e-1, pb[-1]), RIGHT, buff=0.25)
        head = label(r"What's inside: attention scores blow up", font_size=32).to_edge(UP, buff=0.35)
        side = label(r"huge scores $\Rightarrow$ softmax becomes one-hot\\$\Rightarrow$ gradients vanish or explode", font_size=24,
                     color=GREY_A).move_to(plot.c2p(3.5e-4, 6000), aligned_edge=UL)
        self.pb, self.pq = pb, pq
        with self.voiceover(
            "What's going on inside? <bookmark mark='b'/> Here is the largest attention score each model produced, "
            "the dot product of a query and a key, against the learning rate. In the standard model it explodes: "
            f"about nine at the gentlest rate, over a hundred at 0.01, and roughly {pb[-1]:,.0f} at 0.1. <bookmark mark='s'/> A "
            "softmax over scores that large is one-hot, and in longer runs, this is what Wortsman and colleagues saw "
            "right before the loss diverged. <bookmark mark='q'/> QK-norm normalizes every query and key vector before "
            "the dot product, and the largest score stays below twenty-five at every learning rate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(db), FadeIn(tb), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(n) for n in nb], lag_ratio=0.3))
            vo.wait_until("s")
            self.play(FadeIn(side))
            vo.wait_until("q")
            self.play(Create(lq), FadeIn(dq), FadeIn(tq), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def qk_math(self):
        res = self.res
        hd = 128 // 4  # head dimension of the L4 d128 stability models
        bound = np.sqrt(hd)
        pq, pb = self.pq, self.pb
        assert round(bound, 2) == 5.66 and pq[0] < bound and pq.max() < 25
        assert pb[-1] > 9_000 and res[f"stab_qk_{STAB_LRS[0]:.0e}"]["run"]["model"]["qk_norm"]
        der = calc(r"|q\cdot k| &\le \|q\|\,\|k\| \qquad \text{(Cauchy--Schwarz)}",
                   r"\\ \hat q &= g \odot \frac{q}{\operatorname{rms}(q)},\quad \operatorname{rms}(q) = "
                   r"\sqrt{\tfrac1d\textstyle\sum_i q_i^2} \;\Rightarrow\; \|\hat q\| = \sqrt d \ \ (g=1)",
                   rf"\\ \frac{{|\hat q\cdot \hat k|}}{{\sqrt d}} &\le \frac{{\sqrt d\,\sqrt d}}{{\sqrt d}} = \sqrt{{{hd}}} \approx {bound:.2f}",
                   font_size=32)
        der.to_edge(UP, buff=0.5).set_x(-0.6)
        der[2].set_color(C.KEPT)
        meas = VGroup(
            label(rf"measured, QK-norm: {pq[0]:.1f} at learning rate 0.0003 (below the bound)", font_size=26, color=C.KEPT),
            label(rf"at 0.1 the learned gains $g$ have grown: {pq.max():.1f}", font_size=26, color=C.KEPT),
            label(rf"without QK-norm, nothing limits $\|q\|$ and $\|k\|$: {pb[-1]:,.0f}".replace(",", "{,}"), font_size=26,
                  color=C.PENALTY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(der, DOWN, buff=0.45).align_to(der, LEFT)
        gap = 45
        ratio = np.exp(-gap)
        assert 2.5e-20 < ratio < 3.2e-20
        sm = calc(r"\operatorname{softmax}(10045,\ 10000) &= \left(\frac{1}{1+e^{-45}},\ \frac{e^{-45}}{1+e^{-45}}\right)",
                  r"\\ &= (1,\ 2.9\times10^{-20}), \qquad \frac{\partial p_i}{\partial s_i} = p_i(1-p_i) \approx 0",
                  font_size=30)
        sm.next_to(meas, DOWN, buff=0.5).align_to(der, LEFT)
        ill = note(r"two scores 45 apart (illustrative)").next_to(sm, DOWN, buff=0.12).align_to(sm, LEFT)
        with self.voiceover(
            "Why does normalizing cap the scores? A dot product can never exceed the product of the two lengths: "
            "that's the Cauchy-Schwarz inequality. <bookmark mark='r'/> RMS normalization divides each "
            "32-dimensional query and key by its root-mean-square, which sets its length to root 32. "
            "<bookmark mark='b'/> So the score, q dot k over root d, can be at most root 32, about 5.66, unless the "
            f"learned gains grow. <bookmark mark='m'/> Our gentlest run peaked at {pq[0]:.1f}, under the bound. Even at the "
            f"highest learning rate, with grown gains, it reached only {pq.max():.1f}, while without normalization the score hit "
            f"roughly {pb[-1]:,.0f}. <bookmark mark='s'/> And a softmax over scores like that is brutal. Two scores 45 apart get "
            "weights in the ratio e to the minus 45, about three in ten to the twenty: the output is one-hot, and its "
            "gradient, p times one minus p, is zero."
        ) as vo:
            self.play(Write(der[0]))
            vo.wait_until("r")
            self.play(Write(der[1]))
            vo.wait_until("b")
            self.play(Write(der[2]))
            vo.wait_until("m")
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in meas], lag_ratio=0.5), run_time=2.5)
            vo.wait_until("s")
            self.play(Write(sm[0]), FadeIn(ill))
            self.play(Write(sm[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixes(self):
        items = VGroup(
            label(r"\textbf{QK-norm} (Qwen3, OLMo 3, GLM-4.5): normalize queries and keys", font_size=28),
            label(r"\textbf{z-loss} (PaLM): a small penalty that keeps output logits from drifting", font_size=28),
            label(r"\textbf{Gradient clipping} at norm 1.0; \textbf{warmup}; careful initialization", font_size=28),
            label(r"\textbf{MuonClip} (Kimi K2): rescale $W_q, W_k$ whenever a score exceeds 100", font_size=28),
            label(r"$\Rightarrow$ ``zero loss spikes'' over 15.5 trillion tokens", font_size=26, color=C.KEPT),
            label(r"\textbf{2026}: DeepSeek-V4 clamps SwiGLU activations and re-routes experts after a spike", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.27).move_to(DOWN * 0.15)
        items[4].shift(RIGHT * 0.5)
        head = label(r"The toolbox", font_size=36).to_edge(UP, buff=0.45)
        src = source(r"Qwen3, OLMo 3, PaLM, Kimi K2 (arXiv 2507.20534), DeepSeek-V4 (arXiv 2606.19348) reports")
        with self.voiceover(
            "QK-norm is now standard in many open models. Alongside it: a small z-loss that keeps the output logits "
            "from drifting, gradient clipping, warmup and careful initialization. <bookmark mark='m'/> Moonshot's "
            "MuonClip rescales the query and key weights whenever an attention score passes a hundred, and Kimi K2 "
            "trained on fifteen and a half trillion tokens with zero loss spikes. <bookmark mark='d'/> And new failure "
            "modes keep appearing: in 2026, DeepSeek-V4 traced spikes to outliers in its mixture of experts, and added "
            "activation clamping and an emergency re-routing mode that switches on after a spike."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items[:3]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("m")
            self.play(FadeIn(items[3]), FadeIn(items[4]))
            vo.wait_until("d")
            self.play(FadeIn(items[5]))
        self.wait(0.4)
        self.clear_scene()
