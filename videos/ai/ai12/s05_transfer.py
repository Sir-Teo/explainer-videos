from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import HIST, MUP, PANEL_FILL, PART, SP, WIDTH_COLORS, band, load, predict_card, takeaway_card


class Transfer(VoiceoverScene):
    def construct(self):
        self.card()
        self.predict()
        self.sweeps()
        self.copy()
        self.takeaway()

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
        allv = np.concatenate([np.asarray(m[k + str(w)]).ravel() for k in ("sp", "mup") for w in widths])
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
                v = np.asarray(m[mode + str(w)])  # seeds x rates
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
            # where the best rate sits at the smallest and the largest width
            xb = [lrs[int(np.argmin(np.asarray(m[mode + str(w)]).mean(0)))] for w in (widths[0], widths[-1])]
            ym = hi - 0.12
            mk = VGroup(*[DashedLine(ax.c2p(x, lo + 0.02), ax.c2p(x, ym), color=c, stroke_width=1.6, dash_length=0.06)
                          for x, c in zip(xb, (WIDTH_COLORS[0], WIDTH_COLORS[len(widths) - 1]))])
            if abs(xb[1] - xb[0]) > 0.05:
                mk.add(Arrow(ax.c2p(xb[0], ym), ax.c2p(xb[1], ym), buff=0, stroke_width=3, color=col,
                             max_tip_length_to_length_ratio=0.25))
            mk.add(label(rf"best rate moves ${abs(xb[1] - xb[0]):.1f}$ decades", font_size=22, color=col)
                   .next_to(ax.c2p((xb[0] + xb[1]) / 2, ym), UP, buff=0.1))
            panels.add(VGroup(ax, xt, xl, t, yt, bands, lines, bests, mk))
        key = VGroup(*[label(rf"width ${w:,}$".replace(",", "{,}"), font_size=24, color=c) for w, c in zip(widths, WIDTH_COLORS)])
        key.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.3)
        yn = label(rf"held-out bits after ${int(m['steps'])}$ steps \ (lower is better; \ two seeds, \ bands: \ both)",
                   font_size=22, color=GREY_A).next_to(key, DOWN, buff=0.15)
        drift, bl = m["drift"], m["best_loss"]
        bsp = [10 ** v for v in m["bests"]["sp"]]
        # a learning rate, for speech: mantissa times ten to the minus exponent
        e0, e1 = [int(math.ceil(-math.log10(v) - 1e-9)) for v in (bsp[0], bsp[-1])]
        m0, m1 = bsp[0] * 10 ** e0, bsp[-1] * 10 ** e1
        transfer = drift["sp"] >= drift["mup"] + 0.4
        wider = bl["mup"][-1] < bl["mup"][0]
        said1 = (
            f"The best learning rate drifts as the model grows: from about {m0:.0f} times ten to the minus {e0} at the "
            f"smallest to {m1:.0f} times ten to the minus {e1} at the largest, {drift['sp']:.1f} powers of ten. Tune "
            "the small model, copy its rate, "
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
            + "<bookmark mark='c'/> "
            + said3
        ) as vo:
            self.play(FadeIn(key), FadeIn(yn))
            self.play(*[Create(q[0]) for q in panels], *[FadeIn(q[i]) for q in panels for i in (1, 2, 3, 4)])
            p = panels[0]
            self.play(FadeIn(p[5]), LaggedStart(*[Create(l_) for l_ in p[6]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(p[7]))
            self.play(FadeIn(p[8]), run_time=1.2)
            vo.wait_until("b")
            p = panels[1]
            self.play(FadeIn(p[5]), LaggedStart(*[Create(l_) for l_ in p[6]], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(p[7]))
            self.play(FadeIn(p[8]), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def copy(self):
        m = load("mup")
        widths = [int(w) for w in m["widths"]]
        bl, cp = m["best_loss"], m["copy_loss"]
        vals = [("sp", SP, r"SP"), ("mup", MUP, r"$\mu$P")]
        # what copying the small model's best rate costs the big one: its loss there minus its loss at its own best
        pen = {k: max(cp[k] - bl[k][-1], 0.0) for k, _, _ in vals}
        top = max(0.05, max(pen.values()) * 1.25)
        ax = CornerAxes(x_range=[0, 3, 1], y_range=[0, top, top / 4], x_length=4.2, y_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, -0.7, 0])
        bars = VGroup()
        for k, (key, col, name) in enumerate(vals):
            h = ax.c2p(0, pen[key])[1] - ax.c2p(0, 0)[1]
            r_ = Rectangle(width=0.9, height=max(h, 0.02), stroke_width=0, fill_color=col, fill_opacity=0.9)
            r_.move_to(ax.c2p(0.9 + 1.2 * k, 0), aligned_edge=DOWN)
            bars.add(VGroup(r_, MathTex(rf"+{pen[key]:.3f}", font_size=26, color=col).next_to(r_, UP, buff=0.08),
                            label(name, font_size=26, color=col).next_to(ax.c2p(0.9 + 1.2 * k, 0), DOWN, buff=0.15)))
        bk = label(rf"bits lost at width ${widths[-1]:,}$ \\ by copying width ${widths[0]}$'s best rate".replace(",", "{,}"),
                   font_size=22, color=GREY_A).next_to(ax, UP, buff=0.25).align_to(ax, LEFT)
        yn = VGroup()
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
        # the recipe, drawn: tune the small model, copy its rate, train the large one
        def box(txt, col):
            t_ = label(txt, font_size=22, color=WHITE)
            return VGroup(RoundedRectangle(width=t_.width + 0.5, height=t_.height + 0.4, corner_radius=0.12, stroke_color=col,
                                           stroke_width=2, fill_color=PANEL_FILL, fill_opacity=1), t_)
        b1 = box(rf"tune: \ width ${widths[0]}$, \\ a sweep of rates", WIDTH_COLORS[0])
        b2 = box(rf"train once: \ width ${widths[-1]:,}$".replace(",", "{,}"), WIDTH_COLORS[-1])
        recipe = VGroup(b1, b2).arrange(DOWN, buff=1.0).move_to([3.4, -0.4, 0])
        arr = Arrow(b1.get_bottom(), b2.get_top(), buff=0.1, color=GREY_B, stroke_width=3)
        al_ = label(r"copy the best rate", font_size=20, color=GREY_A).next_to(arr, RIGHT, buff=0.15)
        recipe.add(arr, al_)
        pen_sp, pen_mu = cp["sp"] - bl["sp"][-1], cp["mup"] - bl["mup"][-1]
        said4 = (
            f"The usual way, that costs {pen_sp:.3f} bits against the large model's own best; in mu-P, "
            f"{pen_mu:.3f}." if pen_sp > pen_mu + 0.01 else
            f"Here the copied rate costs {pen_sp:.3f} bits the usual way and {pen_mu:.3f} in mu-P."
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
            self.play(Create(ax), FadeIn(bk), FadeIn(yn), FadeIn(recipe[0]))
            self.play(GrowArrow(recipe[2]), FadeIn(recipe[3]), FadeIn(recipe[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(recipe))
            self.play(FadeIn(cards[0], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=LEFT * 0.1))
            self.play(FadeIn(cards[2], shift=LEFT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"As a model gets wider, \ the usual way, \ will its best learning rate go up, \ go down, "
                          r"\ or stay put?")
        with self.voiceover(
            "Pause and predict. As a model gets wider, the usual way, will its best learning rate go up, go down, or "
            "stay put?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Tune small, \ train large",
                           r"In $\mu$P the best learning rate stays put as the width grows, \ so it can be tuned on "
                           r"a small model and copied to a large one \ (Yang et al., 2022).",
                           r"next: \ the same question for depth")
        with self.voiceover(
            "The takeaway: in mu-P, a learning rate tuned on a small model carries over to a wide one, which is how "
            "large models are tuned without tuning them at full size. Next, the same question for depth."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
