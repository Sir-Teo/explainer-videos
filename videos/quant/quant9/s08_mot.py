from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, ARB, CALL, FWD, PART, PUT, Q_C, load, real_data
from videos.quant.quant9.s07_ross import heat


class MOT(VoiceoverScene):
    def construct(self):
        m = load("mot")
        self.card()
        self.problem()
        self.bounds(m)

    def card(self):
        c = chapter_card(7, r"Bounds without a model", r"What do vanilla prices alone imply for exotic ones?",
                         part=PART)
        with self.voiceover("Chapter seven. Bounds without a model."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def problem(self):
        rows = [cmath(r"\sup_{\pi}\ / \inf_{\pi}", r"\ ", r"\sum_{i,j} \pi_{ij}\, c(x_i, y_j)", font_size=36,
                      colors={r"\sup_{\pi}\ / \inf_{\pi}": ALT}),
                cmath(r"\sum_j \pi_{ij} = \mu_i,\ \ \sum_i \pi_{ij} = \nu_j", r",", r"\sum_j \pi_{ij}\,(y_j - x_i) = 0",
                      font_size=34, colors={r"\sum_j \pi_{ij}\,(y_j - x_i) = 0": Q_C})]
        whys = [why(r"a claim on the price at two dates, $c(S_1, S_2)$: its price depends on how the two are joined, "
                    r"which vanilla options do not reveal"),
                why(r"but any joining must match both expiries' densities, and be a martingale (no arbitrage): the "
                    r"range is a linear program (Hobson 1998; Beiglb\"ock, Henry-Labord\`ere and Penkner 2013)")]
        step = ladder(self, rows, whys, keep=2, top=2.6, x=-0.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "The density gives each expiry on its own. A claim that depends on the price at two dates, like a "
            "forward-starting option, depends on how the two dates are joined, and vanilla prices are silent about "
            "that. <bookmark mark='a'/> But not completely silent. Any joint distribution must match both densities, "
            "and, because there is no arbitrage, the later price must be a fair game given the earlier one. Over all "
            "such joinings, the claim's price has a highest and a lowest value, and finding them is a linear "
            "program: martingale optimal transport, from David Hobson in 1998 and Mathias Beiglböck, Pierre "
            "Henry-Labordère and Friedrich Penkner in 2013."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def bounds(self, m):
        lo, up, model = m["lower"], m["upper"], m["model"]
        g = axes([0.10, 0.24], [0, 1], x_length=6.4, y_length=1.2, xlabel=r"price of the forward-start straddle, as a "
                 r"fraction of the price at the first expiry", xticks=[0.10, 0.14, 0.18, 0.22], yticks=[], font_size=16)
        g.to_edge(UP, buff=0.8).to_edge(LEFT, buff=0.8)
        ax = g.ax
        band = Rectangle(width=ax.c2p(up, 0)[0] - ax.c2p(lo, 0)[0], height=0.5, stroke_width=0, fill_color=ALT,
                         fill_opacity=0.5).move_to((ax.c2p(lo, 0.5) + ax.c2p(up, 0.5)) / 2)
        bl = MathTex(f"{lo:.3f}", font_size=26, color=ALT).next_to(ax.c2p(lo, 0.5), UP, buff=0.35)
        bu = MathTex(f"{up:.3f}", font_size=26, color=ALT).next_to(ax.c2p(up, 0.5), UP, buff=0.35)
        md = Line(ax.c2p(model, 0.15), ax.c2p(model, 0.85), color=CALL, stroke_width=5)
        ml = MathTex(rf"\text{{log-normal: }} {model:.3f}", font_size=24, color=CALL).next_to(md, DOWN, buff=0.45)
        pl, pu = np.asarray(m["pi_lower"]), np.asarray(m["pi_upper"])
        hi = max(pl.max(), pu.max()) ** 0.5
        h1 = heat(np.sqrt(pl), size=0.07, lo=0, hi=hi)
        h2 = heat(np.sqrt(pu), size=0.07, lo=0, hi=hi)
        b1 = VGroup(label(r"the cheapest joining", font_size=19, color=GREY_A), h1).arrange(DOWN, buff=0.12)
        b2 = VGroup(label(r"the dearest joining", font_size=19, color=GREY_A), h2).arrange(DOWN, buff=0.12)
        hb = VGroup(b1, b2).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.6).to_edge(LEFT, buff=0.8)
        axes_note = label(r"rows: price at the first expiry; columns: at the second", font_size=17, color=GREY_B).next_to(
            hb, DOWN, buff=0.1).align_to(hb, LEFT)
        side = VGroup(
            label(r"$|S_2 / S_1 - 1|$ between the Surface's two expiries", font_size=21, color=GREY_A),
            wrapped_label(rf"no arbitrage and today's vanilla prices pin it between {lo:.3f} and {up:.3f}; a model "
                          rf"with independent log-normal returns (forward volatility {100 * m['fwd_vol']:.0f}\%) says "
                          rf"{model:.3f}", 4.2, 20, GREY_A),
            wrapped_label(r"the cheapest joining moves little: it keeps the second price close to the first where it "
                          r"can; the dearest spreads it as far as the densities allow", 4.2, 20, Q_C),
            wrapped_label(r"a dealer quoting outside the band is arbitrageable with vanilla options alone; inside it, "
                          r"the price is a choice of model (Parts 12 to 14)", 4.2, 20, CALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"densities from the Surface (chapter 5), 25 and 81 atoms; the House's \texttt{mot\_bounds} (HiGHS)")
        with self.voiceover(
            "Here it is on the Surface. The claim pays the absolute return of Bitcoin between the two expiries of "
            "chapter five: a forward-starting straddle. <bookmark mark='a'/> Joining the two densities in every way "
            f"that respects no arbitrage, its price must lie between {lo:.3f} and {up:.3f}, as a fraction of the "
            "price at the first expiry. A model with independent log-normal returns, at the forward volatility the "
            f"Surface implies, says {model:.3f}: inside the band, as it must be. <bookmark mark='b'/> The two "
            "extreme joinings show why. The cheapest keeps the second price as close to the first as it can; the "
            "dearest spreads it as far as both densities allow. <bookmark mark='c'/> A dealer quoting outside this "
            "band can be arbitraged with vanilla options alone. Inside it, the price is a choice of model, and "
            "Parts twelve to fourteen are about making that choice well."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(band), FadeIn(bl), FadeIn(bu), FadeIn(side[1]))
            self.play(Create(md), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(hb), FadeIn(axes_note), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
