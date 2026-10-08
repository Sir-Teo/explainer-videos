from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Plot, label, load, note, pow10_label, source, train_curve
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
        lo = min(base.min(), qk.min())
        plot = Plot(x_range=(2e-4, 1.5e-1), y_range=(lo - 0.2, FAIL + 0.2), width=8.6, height=4.4, log_x=True,
                    x_ticks=[1e-3, 1e-2, 1e-1], y_ticks=list(np.arange(np.ceil(lo), FAIL + 0.01, 1.0)),
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
        head = label(r"Real sweep: 12 pocket models, 6 learning rates, with and without QK-norm", font_size=30).to_edge(UP, buff=0.35)
        src = source(r"after Wortsman et al., \emph{Small-scale proxies for large-scale Transformer training instabilities} (2023)")
        with self.voiceover(
            "Many instabilities can be reproduced in miniature. Researchers at Google showed in 2023 that small "
            "models trained at high learning rates fail in the same ways big ones do. So we trained twelve pocket "
            "models: six learning rates, each with standard attention <bookmark mark='q'/> and with a fix called "
            "QK-norm. <bookmark mark='r'/> At gentle learning rates, both behave the same. Push the rate up, and the "
            "standard model falls apart, while the one with QK-norm keeps training."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(src))
            self.play(Create(lb), FadeIn(db), FadeIn(tb), run_time=1.5)
            vo.wait_until("q")
            self.play(Create(lq), FadeIn(dq), FadeIn(tq), run_time=1.5)
            vo.wait_until("r")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def logits(self):
        res = self.res
        lr = STAB_LRS[-2]
        rb, rq = res[f"stab_base_{lr:.0e}"], res[f"stab_qk_{lr:.0e}"]
        pb = np.array(rb["probes"], float)
        pq = np.array(rq["probes"], float)
        ymax = max(pb[:, 1].max(), pq[:, 1].max()) * 1.1
        S = max(pb[-1, 0], pq[-1, 0])
        plot = Plot(x_range=(0, S), y_range=(0, ymax), width=8.6, height=4.2, x_ticks=list(np.linspace(0, S, 5).round(-1)),
                    y_ticks=list(np.linspace(0, ymax, 5).round(-1))[:-1], x_label=r"training step",
                    y_label=r"largest attention score $q\cdot k/\sqrt{d}$")
        plot.move_to(DOWN * 0.4 + LEFT * 0.8)
        lb = plot.line(pb[:, 0], pb[:, 1], color=C.PENALTY, stroke_width=3.5)
        lq = plot.line(pq[:, 0], pq[:, 1], color=C.KEPT, stroke_width=3.5)
        tb = label(r"standard", font_size=26, color=C.PENALTY).next_to(plot.c2p(pb[-1, 0], pb[-1, 1]), RIGHT, buff=0.1)
        tq = label(r"QK-norm", font_size=26, color=C.KEPT).next_to(plot.c2p(pq[-1, 0], pq[-1, 1]), RIGHT, buff=0.1)
        head = label(rf"What goes wrong: attention scores blow up (learning rate {lr:g})", font_size=32).to_edge(UP, buff=0.35)
        side = label(r"huge scores $\Rightarrow$ softmax becomes one-hot\\$\Rightarrow$ gradients vanish or explode", font_size=24,
                     color=GREY_A).to_corner(DR, buff=0.5).shift(UP * 0.4)
        self.pb, self.pq = pb, pq
        with self.voiceover(
            "What goes wrong? Look inside attention. <bookmark mark='b'/> In the standard model, the largest "
            "attention score, the dot product of a query and a key, keeps growing as training goes on. Once scores are "
            "huge, the softmax turns one-hot, and the gradients through it either vanish or explode. "
            "<bookmark mark='q'/> QK-norm normalizes every query and key vector before the dot product, which keeps "
            "the scores from running away."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(tb), FadeIn(side), run_time=2.0)
            vo.wait_until("q")
            self.play(Create(lq), FadeIn(tq), run_time=1.5)
        self.wait(0.3)
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
