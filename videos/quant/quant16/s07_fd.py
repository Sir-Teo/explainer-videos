from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, illustration, load, loglog


class FD(VoiceoverScene):
    def construct(self):
        f = load("fd")
        self.card()
        self.schemes(f)
        self.convergence(f)
        self.ringing(f)

    def card(self):
        c = chapter_card(6, r"Finite differences", r"How do you solve the pricing equation on a grid?", part=PART)
        with self.voiceover("Chapter six. Finite differences."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def schemes(self, f):
        rows = [cmath(r"\frac{V^{n+1} - V^n}{\Delta t}", r"=", r"\theta\,\mathcal{L}V^{n+1} + (1 - \theta)\,\mathcal{L}V^n",
                      font_size=36, colors={r"\frac{V^{n+1} - V^n}{\Delta t}": OPT}),
                cmath(r"\Delta t", r"<", r"\frac{\Delta S^2}{\sigma^2 S_{\max}^2}\quad (\theta = 0)", font_size=34,
                      colors={r"\Delta t": BAD})]
        whys = [why(r"Part 10's PDE on a grid, stepped back from expiry: explicit ($\theta = 0$), fully implicit ($\theta = 1$), "
                    r"or Crank and Nicolson (1947, $\theta = \tfrac12$), second-order accurate in time"),
                why(rf"the explicit scheme is stable only for tiny steps: here at least {f['explicit_nt_min']:,.0f} steps "
                    rf"for a 100-point grid; with 400 it explodes to {f['explicit']['400']:.1e}, with 2{{,}}000 it gives "
                    rf"{f['explicit']['2000']:.3f}".replace(",", "{,}"))]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.8, buff=1.0, edge=6.9)
        with self.voiceover(
            "The other family of methods solves Part ten's pricing equation directly, on a grid in price and time, "
            "stepping back from expiry. The theta scheme mixes today's and tomorrow's operator: theta zero is explicit, "
            "one is fully implicit, and one half is Crank and Nicolson's scheme from 1947, second-order accurate in "
            "time. <bookmark mark='a'/> The explicit scheme is the simplest and the most fragile: stable only if the "
            "time step is below the square of the price step over the variance. With too few time steps it does not "
            f"just lose accuracy, it explodes, here to about {f['explicit']['400']:.0e}."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def convergence(self, f):
        grids = np.log10(np.asarray(f["grids"], float))
        g = loglog(1.2, 2.8, -6, -1, r"grid points in price and in time", r"error in the call price", xt=[2], yt=[-5, -4, -3, -2, -1])
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        cols = {"implicit": BAD, "cn": OPT, "cn+rannacher": GOOD}
        lines = VGroup()
        for k in ("implicit", "cn", "cn+rannacher"):
            y = np.log10(np.maximum(np.asarray(f["errors"][k]), 1e-7))
            pts = [ax.c2p(a, np.clip(b, -6, -1)) for a, b in zip(grids, y)]
            lines.add(VGroup(VMobject(stroke_color=cols[k], stroke_width=3).set_points_as_corners(pts),
                             *[Dot(p_, radius=0.05, color=cols[k]) for p_ in pts]))
        leg = legend([(BAD, r"fully implicit: first order"), (OPT, r"Crank--Nicolson"),
                      (GOOD, r"Crank--Nicolson after two implicit half-steps (Rannacher)")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = wrapped_label(r"the implicit scheme's error halves when the grid doubles; Crank--Nicolson's falls about four "
                             r"times: second order. For a smooth call the two second-order lines coincide", 4.4, 19,
                             GREY_A).to_edge(RIGHT, buff=0.4)
        src = illustration(r"one-year at-the-money call; uniform grid to four times the strike")
        with self.voiceover(
            "Here is each stable scheme's error as the grid is refined, in price and time together. The fully "
            "implicit scheme is first order: double the grid, halve the error. <bookmark mark='a'/> Crank–Nicolson "
            "is second order: double the grid, and the error falls about four times."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(leg[1]), Create(lines[2]), FadeIn(leg[2]), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def ringing(self, f):
        S = np.asarray(f["gamma_S"])
        ge = np.asarray(f["gamma_exact"])
        lo, hi = np.percentile(ge, 1) * 1.6, np.percentile(ge, 99) * 1.6
        g = axes([85, 115], [lo, hi], x_length=7.4, y_length=4.2, xlabel=r"spot", ylabel=r"gamma of a digital, a week before expiry",
                 xticks=[90, 100, 110], yticks=[], font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        cn = curve(ax, np.asarray(f["gamma"]["cn"]["S"]), np.clip(np.asarray(f["gamma"]["cn"]["gamma"]), lo, hi), BAD,
                   stroke_width=2.5)
        rn = curve(ax, np.asarray(f["gamma"]["cn+rannacher"]["S"]),
                   np.clip(np.asarray(f["gamma"]["cn+rannacher"]["gamma"]), lo, hi), GOOD, stroke_width=3)
        ex = DashedVMobject(curve(ax, S, ge, WHITE, stroke_width=2), num_dashes=50)
        leg = legend([(WHITE, r"exact"), (BAD, r"Crank--Nicolson"), (GOOD, r"with Rannacher's start")], font_size=17)
        leg.next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = wrapped_label(r"Crank--Nicolson does not damp the sharp corner of a payoff: the price looks fine, but its "
                             r"gamma rings around the strike. Two fully implicit half-steps at the start smooth the corner "
                             r"away and keep second order (Rannacher 1984). Gamma is what the desk hedges with", 4.2, 18,
                             GREY_A).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "But Crank–Nicolson has a flaw that the price hides. Near expiry, with a payoff that jumps, like a "
            "digital, it does not damp the jump. <bookmark mark='a'/> The price looks right, but its gamma rings "
            "around the strike, and gamma is what the desk hedges with. <bookmark mark='b'/> The fix, from Rolf "
            "Rannacher in 1984, is to start with two fully implicit half-steps, which smooth the corner, and then "
            "switch to Crank–Nicolson. The ringing disappears, and the scheme stays second order."
        ) as vo:
            self.play(FadeIn(g), Create(ex), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(cn), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(Create(rn), FadeIn(leg[2]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
