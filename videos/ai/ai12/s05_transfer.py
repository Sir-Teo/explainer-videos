from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import HIST, MUP, PART, SP, WIDTH_COLORS, band, load


class Transfer(VoiceoverScene):
    def construct(self):
        self.card()
        self.sweeps()
        self.copy()

    def card(self):
        card = chapter_card(4, r"One learning rate for every width",
                            r"Can a learning rate tuned on a small model be used on a large one?", lit=(2022,), part=PART)
        with self.voiceover("Chapter four. One learning rate for every width."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sweeps(self):
        m = load("mup")
        lrs = np.log10(np.asarray(m["lrs"]))
        widths = [int(w) for w in m["widths"]]
        allv = np.concatenate([np.asarray(m[f"{k}{w}"]).ravel() for k in ("sp", "mup") for w in widths])
        allv = allv[np.isfinite(allv)]
        lo = float(np.floor(allv.min() * 10) / 10)
        hi = float(min(np.ceil(np.percentile(allv, 80) * 10) / 10, lo + 1.4))
        panels = VGroup()
        for k, (mode, title, col) in enumerate((("sp", r"the usual way (SP)", SP), ("mup", r"$\mu$P", MUP))):
            ax = CornerAxes(x_range=[lrs[0], lrs[-1], 0.5], y_range=[lo, hi, 0.2], x_length=5.6, y_length=3.8, tips=False,
                            axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
            ax.move_to([-3.4 + 6.8 * k, -0.75, 0])
            lines, bests, bands = VGroup(), VGroup(), VGroup()
            for w, wc in zip(widths, WIDTH_COLORS):
                v = np.asarray(m[f"{mode}{w}"])  # seeds x rates
                v = np.where(np.isfinite(v), np.minimum(v, hi), hi)
                mean = v.mean(0)
                bands.add(band(ax, lrs, v.min(0), v.max(0), wc, 0.18))
                lines.add(curve(ax, lrs, mean, wc, 3))
                i = int(np.argmin(mean))
                bests.add(Dot(ax.c2p(lrs[i], mean[i]), radius=0.09, color=wc))
            xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.08)
                          for v in range(math.ceil(lrs[0]), math.floor(lrs[-1]) + 1)])
            xl = label(r"learning rate", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
            t = label(title, font_size=30, color=col).next_to(ax, UP, buff=0.2)
            yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(lrs[0], v), LEFT, buff=0.08)
                          for v in np.arange(lo, hi + 1e-9, 0.2)])
            panels.add(VGroup(ax, xt, xl, t, yt, bands, lines, bests))
        key = VGroup(*[label(rf"width ${w:,}$".replace(",", "{,}"), font_size=24, color=c) for w, c in zip(widths, WIDTH_COLORS)])
        key.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.3)
        yn = label(rf"held-out bits after ${int(m['steps'])}$ steps \ (lower is better; \ two seeds, \ bands: \ both)",
                   font_size=22, color=GREY_A).next_to(key, DOWN, buff=0.15)
        drift, bl = m["drift"], m["best_loss"]
        bsp = [10 ** v for v in m["bests"]["sp"]]
        transfer = drift["sp"] >= drift["mup"] + 0.4
        wider = bl["mup"][-1] < bl["mup"][0]
        said1 = (
            f"The best learning rate drifts as the model grows: from {bsp[0]:.1e} at the smallest to "
            f"{bsp[-1]:.1e} at the largest, {drift['sp']:.1f} powers of ten. Tune the small model, copy its rate, "
            "and the big one is mistuned. " if transfer else
            f"Over this range the best rate moves by {drift['sp']:.1f} powers of ten. "
        )
        said2 = (
            f"the valleys line up: the best rate moves by {drift['mup']:.1f} at most. "
            if drift["mup"] <= 0.25 else f"the best rate moves by {drift['mup']:.1f}. "
        )
        said3 = (
            f"And wider is better at every rate: {bl['mup'][0]:.2f} bits at the smallest width, "
            f"{bl['mup'][-1]:.2f} at the largest." if wider else ""
        )
        with self.voiceover(
            "Now the test that matters: sweep the learning rate at three widths, sixty-four to a thousand and "
            "twenty-four, two seeds each, the usual way first. <bookmark mark='a'/> "
            + said1
            + "<bookmark mark='b'/> In mu-P "
            + said2
            + said3
        ) as vo:
            self.play(FadeIn(key), FadeIn(yn))
            p = panels[0]
            self.play(Create(p[0]), FadeIn(p[1]), FadeIn(p[2]), FadeIn(p[3]), FadeIn(p[4]))
            self.play(FadeIn(p[5]), LaggedStart(*[Create(l_) for l_ in p[6]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(p[7]))
            vo.wait_until("b")
            p = panels[1]
            self.play(Create(p[0]), FadeIn(p[1]), FadeIn(p[2]), FadeIn(p[3]), FadeIn(p[4]))
            self.play(FadeIn(p[5]), LaggedStart(*[Create(l_) for l_ in p[6]], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(p[7]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def copy(self):
        m = load("mup")
        widths = [int(w) for w in m["widths"]]
        bl, cp = m["best_loss"], m["copy_loss"]
        vals = [("sp", SP, r"SP"), ("mup", MUP, r"$\mu$P")]
        lo = min(min(bl[k][-1], cp[k]) for k, _, _ in vals) - 0.05
        hi = max(cp[k] for k, _, _ in vals) + 0.05
        hi = max(hi, lo + 0.3)
        ax = CornerAxes(x_range=[0, 4, 1], y_range=[lo, hi, (hi - lo) / 4], x_length=5.0, y_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, -0.6, 0])
        bars = VGroup()
        for k, (key, col, name) in enumerate(vals):
            for j, (v, op, txt) in enumerate(((bl[key][-1], 0.9, r"its own best rate"), (cp[key], 0.45, r"the small model's"))):
                x = 0.6 + 2.0 * k + 0.8 * j
                h = ax.c2p(0, v)[1] - ax.c2p(0, lo)[1]
                r_ = Rectangle(width=0.62, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=op)
                r_.move_to(ax.c2p(x, lo), aligned_edge=DOWN)
                bars.add(VGroup(r_, MathTex(f"{v:.2f}", font_size=22, color=col).next_to(r_, UP, buff=0.06)))
            bars.add(label(name, font_size=26, color=col).next_to(ax.c2p(1.0 + 2.0 * k, lo), DOWN, buff=0.15))
        bk = VGroup(label(r"solid: \ its own best rate", font_size=20, color=GREY_A),
                    label(r"faint: \ the width-$64$ model's best rate, copied", font_size=20, color=GREY_A))
        bk.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=0.25).align_to(ax, LEFT)
        yn = label(rf"width ${widths[-1]:,}$, \ held-out bits".replace(",", "{,}"), font_size=22, color=GREY_A)
        yn.next_to(bk, UP, buff=0.12).align_to(ax, LEFT)
        cards = VGroup(
            history_card(2022, r"Yang, Hu et al., \ \textit{Tensor Programs V}",
                         r"tuned a $40$-million-parameter model, \ copied its settings to a $6.7$-billion GPT-3, \ and "
                         r"beat the published one; \ tuning cost $7\%$ of one training run", width=6.0, color=HIST),
            history_card(2024, r"Everett et al.\ (Google DeepMind)",
                         r"every parametrization can transfer, \ with the right per-layer rates; \ $26.8$ billion "
                         r"parameters tested", width=6.0, color=HIST),
            history_card(2025, r"Meta, \ Llama 4: \ ``MetaP''", r"per-layer learning rates and starting scales that "
                         r"transfer across width, depth, batch size and training length", width=6.0, color=HIST),
        ).arrange(DOWN, buff=0.18).move_to([3.4, -0.35, 0])
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        pen_sp, pen_mu = cp["sp"] - bl["sp"][-1], cp["mup"] - bl["mup"][-1]
        said4 = (
            f"The usual way, that costs {pen_sp:.2f} bits against the large model's own best; in mu-P, "
            f"{pen_mu:.2f}." if pen_sp > pen_mu + 0.01 else
            f"Here the copied rate costs {pen_sp:.2f} bits the usual way and {pen_mu:.2f} in mu-P."
        )
        with self.voiceover(
            "Here is what that means in practice. Tune the smallest model, and train the largest with its learning "
            "rate. <bookmark mark='a'/> "
            + said4
            + " <bookmark mark='b'/> At scale, this is what mu-P was built for. In 2022, Yang and colleagues tuned "
            "a forty-million-parameter model, copied its settings to a GPT-3 of six point seven billion, and beat "
            "the published one, for seven percent of the cost of one training run. <bookmark mark='c'/> In 2024, "
            "Everett and colleagues at Google DeepMind showed that the usual parametrization transfers too, with "
            "the right learning rate for each layer, and in 2025 Meta set Llama 4's per-layer rates and starting "
            "scales this way, transferring them across width, depth, batch size and training length."
        ) as vo:
            self.play(Create(ax), FadeIn(bk), FadeIn(yn))
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cards[0], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=LEFT * 0.1))
            self.play(FadeIn(cards[2], shift=LEFT * 0.1))
        self.wait(0.3)
        self.clear_scene()
