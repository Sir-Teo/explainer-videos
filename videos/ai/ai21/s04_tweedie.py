from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, NOISE, PART, SCORE, Panel, load, take_away


class Tweedie(VoiceoverScene):
    def construct(self):
        self.card()
        self.best_guess()
        self.theorem()
        self.check()
        self.blur()

    def card(self):
        card = chapter_card(3, r"Tweedie's formula", r"What is the best possible guess of the noise?", part=PART)
        with self.voiceover("Chapter three. Tweedie's formula."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def best_guess(self):
        tw = load("tweedie")
        x0 = np.asarray(tw["x0grid"])
        p0 = np.asarray(tw["p0"])
        t = 0.35
        a = math.cos(math.pi * t / 2)
        keep = (x0 > -3.6) & (x0 < 3.6)
        posts = {xq: np.asarray(tw[f"t{t:g}_post{xq:g}"]) for xq in (-1.2, 0.2, 1.4)}
        top = max(float(p0.max()), max(float(p.max()) for p in posts.values())) * 1.1
        g = axes([-3.6, 3.6], [0, top], x_length=9.0, y_length=3.4, xlabel=r"the clean value $x_0$", ylabel=r"density",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], center=[0, -0.4, 0])
        prior = curve(g.ax, x0[keep], p0[keep], DATA, 3.5)
        pl = label(r"$p(x_0)$: \ the data, \ two bumps", font_size=22, color=DATA)

        def post_curve(xq):
            p = posts[xq]
            return curve(g.ax, x0[keep], p[keep], SCORE, 3)

        def mean_of(xq):
            p = posts[xq]
            return float((p * x0).sum() / p.sum())

        def marker(xq):
            m = mean_of(xq)
            obs = VGroup(Triangle(color=NOISE, fill_opacity=1).scale(0.09).rotate(PI).move_to(g.ax.c2p(xq / a, top * 1.02)),
                         label(r"noisy $x_t$", font_size=20, color=NOISE).next_to(g.ax.c2p(xq / a, top * 1.02), UP, buff=0.12))
            mean = VGroup(DashedLine(g.ax.c2p(m, 0), g.ax.c2p(m, 0.75 * top), color=WHITE, stroke_width=2),
                          Dot(g.ax.c2p(m, 0), radius=0.08, color=WHITE),
                          label(r"$\mathbb E[x_0 \mid x_t]$", font_size=22, color=WHITE).next_to(g.ax.c2p(m, 0.75 * top), UP,
                                                                                                buff=0.08))
            return obs, mean

        cur = post_curve(0.2)
        obs, mean = marker(0.2)
        cl = label(r"$p(x_0 \mid x_t)$: \ what could have been", font_size=22, color=SCORE)
        VGroup(pl, cl).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-4.0, 2.75, 0])
        rule = label(r"the guess with the smallest squared error \ $=$ \ the average of what could have been",
                     font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A noisy point could have come from many clean ones. Here is a one-dimensional data distribution, two "
            "bumps. <bookmark mark='a'/> We see a noisy value, x t, at a moderate noise level. <bookmark mark='b'/> "
            "Bayes gives the distribution of the clean value it came from: wide, because the noise is wide, and "
            "pulled towards the bumps. <bookmark mark='c'/> The guess with the smallest expected squared error is "
            "the average of this distribution, the posterior mean. That is what a network trained by squared error "
            "learns to output, if it can. <bookmark mark='d'/> Move the noisy value, and the posterior mean slides "
            "between the bumps, never quite reaching either."
        ) as vo:
            self.play(FadeIn(g), Create(prior), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(obs))
            vo.wait_until("b")
            self.play(Create(cur), FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(mean), FadeIn(rule))
            vo.wait_until("d")
            for xq in (-1.2, 1.4):
                o2, m2 = marker(xq)
                self.play(Transform(cur, post_curve(xq)), Transform(obs, o2), Transform(mean, m2), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        card = theorem_card(r"Tweedie's formula", MathTex(r"\mathbb E[x_0 \mid x_t] = \frac{x_t + \sigma_t^2\, \nabla \log "
                                                          r"p_t(x_t)}{\alpha_t}", font_size=34),
                            who=r"Robbins (1956), \ crediting Maurice Tweedie; \ Efron (2011)", width=6.4)
        card.to_corner(UL, buff=0.35)
        rows = [
            cmath(r"p_t(x)", r"=", r"\int \mathcal N(x;\ \alpha_t x_0,\ \sigma_t^2)\; p(x_0)\, dx_0", font_size=32),
            cmath(r"\nabla p_t(x)", r"=", r"\int \frac{\alpha_t x_0 - x}{\sigma_t^2}\; \mathcal N(x;\ \alpha_t x_0,\ "
                  r"\sigma_t^2)\; p(x_0)\, dx_0", font_size=32),
            cmath(r"\nabla \log p_t(x)", r"=", r"\frac{\alpha_t\, \mathbb E[x_0 \mid x] - x}{\sigma_t^2}", font_size=32),
            cmath(r"\hat\varepsilon^{*}(x)", r"=", r"\frac{x - \alpha_t \mathbb E[x_0 \mid x]}{\sigma_t}", r"=",
                  r"-\sigma_t\, \nabla \log p_t(x)", colors={r"-\sigma_t\, \nabla \log p_t(x)": SCORE}, font_size=32),
        ]
        whys = [why(r"the noised data: \ a blur of the clean"), why(r"differentiate the Gaussian"),
                why(r"divide by $p_t$: \ Bayes turns it into the posterior"), why(r"the best noise guess")]
        step = ladder(self, rows, whys, keep=4, top=1.35, x=-1.6, buff=0.3, edge=6.85)
        with self.voiceover(
            "That average has a formula. Herbert Robbins published it in 1956, crediting Maurice Tweedie: the "
            "posterior mean is the noisy point plus sigma squared times the score, divided by alpha. "
            "<bookmark mark='a'/> The proof is three lines. The noised density is a blur of the clean one. "
            "<bookmark mark='b'/> Differentiate under the integral: only the Gaussian depends on x. "
            "<bookmark mark='c'/> Divide by the density, and Bayes turns the integral into the posterior mean. "
            "<bookmark mark='d'/> Now the noise. The best guess of the noise is the noisy point minus alpha times "
            "the best clean point, over sigma: minus sigma times the score. A network trained to guess the noise is "
            "learning the score. That is why diffusion works."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        tw, dn = load("tweedie"), load("denoiser")
        t = 0.35
        xs = np.asarray(tw[f"t{t:g}_xs"])
        m, twd = np.asarray(tw[f"t{t:g}_mean"]), np.asarray(tw[f"t{t:g}_tweedie"])
        g = axes([-3.5, 3.5], [-2.5, 2.5], x_length=4.4, y_length=2.5, xlabel=r"noisy value $x_t$",
                 ylabel=r"$\mathbb E[x_0 \mid x_t]$, \ 1D", xticks=[-3, 0, 3], yticks=[-2, 0, 2], center=[-4.3, 1.05, 0])
        cm = curve(g.ax, xs, np.clip(m, -2.5, 2.5), WHITE, 3)
        cd = VGroup(*[Dot(g.ax.c2p(x, y), radius=0.04, color=SCORE) for x, y in zip(xs[::6], np.clip(twd[::6], -2.5, 2.5))])
        mx = max(float(tw["t0.35_maxdiff"]), float(tw["t0.65_maxdiff"]))
        l1 = VGroup(label(r"line: \ the posterior mean, \ by brute force", font_size=18, color=WHITE),
                    label(r"dots: \ Tweedie, \ from the exact score", font_size=18, color=SCORE),
                    label(rf"largest gap: \ ${sci(mx, 1)}$", font_size=18, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(g, DOWN, buff=0.12)
        decimals = max(1, int(math.floor(-math.log10(max(mx, 1e-300)))))
        pn = Panel(4.6, center=[1.9, 0.95, 0])
        tq = 0.5
        q, mc, tw2 = (np.asarray(tw[f"{k}{tq:g}"]) for k in ("q", "mc", "tw"))
        qd = pn.dots(q, NOISE, radius=0.03)
        lines = VGroup(*[Line(a_, b_, stroke_width=1, color=GREY_B, stroke_opacity=0.6) for a_, b_ in zip(pn.pts(q), pn.pts(mc))])
        md = pn.dots(mc, WHITE, radius=0.035)
        td = VGroup(*[Cross(scale_factor=0.06, stroke_width=2.5, stroke_color=SCORE).move_to(p_) for p_ in pn.pts(tw2)])
        pl = label(rf"2D, \ $t = {tq:g}$: \ noisy points, \ their posterior means", font_size=20, color=GREY_A).next_to(pn, UP, buff=0.1)
        rows = tw["mc_rows"]
        nets = dn["tw_rows"]
        tab_rows = [[r"noise level $t$", r"Monte Carlo vs Tweedie", r"our network vs Tweedie", r"spread of the means"]]
        for r, n_ in zip(rows, nets):
            tab_rows.append([rf"${r['t']:g}$", rf"${r['mean_err']:.3f}$", rf"${n_['err']:.3f}$", rf"${r['spread']:.2f}$"])
        tab = VGroup(*[VGroup(*[label(c, font_size=19, color=(GREY_A if i == 0 else [WHITE, WHITE, SCORE, GREY_B][j]))
                                for j, c in enumerate(row)]) for i, row in enumerate(tab_rows)])
        xcol = [-4.6, -1.9, 1.0, 3.9]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xcol[j] + 1.0, -2.25 - 0.36 * i, 0])
        tab.shift(LEFT * 0.4)
        worst_mc = max(r["mean_err"] for r in rows)
        worst_net = max(n_["err"] for n_ in nets)
        spread = min(r["spread"] for r in rows)
        net_says = (f"Our trained network's guesses sit within {worst_net:.3f} of the formula's, small beside the "
                    f"spread of {spread:.2f}: it has learned the score." if worst_net < 0.25 * spread else
                    f"Our trained network's guesses are within {worst_net:.3f} of the formula's, against a spread of "
                    f"{spread:.2f}: close, not exact.")
        with self.voiceover(
            "Check it. In one dimension, compute the posterior mean by brute force, integrating over a fine grid, "
            f"and compare it with Tweedie's formula, using the exact score. <bookmark mark='a'/> They agree to "
            f"{decimals} decimal places: the formula is exact. <bookmark mark='b'/> In two dimensions, on our letters, "
            "estimate each posterior mean by Monte Carlo, weighting fifty thousand clean points by how likely each "
            f"is to have produced the noisy one. <bookmark mark='c'/> The estimates land within {worst_mc:.3f} of the "
            f"formula, on average. <bookmark mark='d'/> {net_says}"
        ) as vo:
            self.play(FadeIn(g), Create(cm), FadeIn(l1[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in cd], lag_ratio=0.02), FadeIn(l1[1:]))
            vo.wait_until("b")
            self.play(FadeIn(pn), FadeIn(pl), FadeIn(qd))
            self.play(Create(lines), FadeIn(md), run_time=1.2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in td], lag_ratio=0.01), FadeIn(tab[0]), FadeIn(VGroup(*[r_[:2] for r_ in tab[1:]])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*[r_[2:] for r_ in tab[1:]])))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blur(self):
        tw = load("tweedie")
        ts = [float(v) for v in tw["den_ts"]]
        panels = VGroup()
        for i, t in enumerate(ts):
            pn = Panel(3.25, center=[-5.02 + 3.35 * i, 0.5, 0])
            panels.add(VGroup(pn, pn.dots(np.asarray(tw[f"den_x0{t:g}"])[:500], WHITE, radius=0.02),
                              label(rf"$t = {t:g}$", font_size=24, color=SCORE).next_to(pn, UP, buff=0.12),
                              label(rf"error ${float(tw[f'den_mse{t:g}']):.2f}$", font_size=19, color=GREY_A).next_to(pn, DOWN, buff=0.1)))
        head = label(r"the best possible one-jump guess of the clean points", font_size=28).to_edge(UP, buff=0.5)
        ta = take_away(r"One jump lands on the average of what could have been: \ a blur. \ So samplers walk back in "
                       r"many small steps, \ re-guessing as the noise falls.")
        e0, e1 = float(tw[f"den_mse{ts[0]:g}"]), float(tw[f"den_mse{ts[-1]:g}"])
        with self.voiceover(
            "What does the best denoiser do with very noisy points? Here are its guesses for five hundred noisy "
            "points, at four noise levels. <bookmark mark='a'/> At high noise every guess is near the middle of the "
            f"letters: the average letter, with a squared error of {e0:.2f}. <bookmark mark='b'/> As the noise falls, "
            f"the guesses spread onto the strokes, and the error drops to {e1:.3f}. <bookmark mark='c'/> So you cannot "
            "jump from pure noise to a sample in one step: the best jump lands on a blur. Samplers take many small "
            "steps instead, re-guessing as the noise falls: chapters five and six."
        ) as vo:
            self.play(FadeIn(head))
            for i, pnl in enumerate(panels):
                if i == 0:
                    self.play(FadeIn(pnl))
                    vo.wait_until("a")
                elif i == 1:
                    vo.wait_until("b")
                    self.play(FadeIn(pnl))
                else:
                    self.play(FadeIn(pnl))
            vo.wait_until("c")
            self.play(FadeIn(ta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
