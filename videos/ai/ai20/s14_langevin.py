from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (DATA, EBM, HIST, NOISE, PART, SCORE_C, Plane, arrows, curve, load, take_away)


def particle_play(scene, plane, P, run_time, color=WHITE, radius=0.025, n=None):
    """Points moving through the frames of P (frames x points x 2), interpolated."""
    P = np.asarray(P)
    n = n or P.shape[1]
    dots = VGroup(*[Dot(q, radius=radius, color=color, fill_opacity=0.9) for q in plane.pts(np.clip(P[0][:n],
                                                                                                    -plane.box * 0.98,
                                                                                                    plane.box * 0.98))])
    t = ValueTracker(0.0)

    def upd(g):
        v = t.get_value() * (len(P) - 1)
        k = min(int(v), len(P) - 2)
        a = v - k
        Q = (1 - a) * P[k][:n] + a * P[k + 1][:n]
        for d_, q in zip(g, plane.pts(np.clip(Q, -plane.box * 0.98, plane.box * 0.98))):
            d_.move_to(q)

    scene.add(dots)
    dots.add_updater(upd)
    scene.play(t.animate.set_value(1.0), run_time=run_time, rate_func=linear)
    dots.clear_updaters()
    return dots


class Langevin(VoiceoverScene):
    def construct(self):
        self.card()
        self.ebm()
        self.dynamics()
        self.replay()
        self.from_noise()
        self.mixing()

    def card(self):
        card = chapter_card(13, r"Langevin dynamics and the score", r"How do you sample from an energy without "
                            r"its normalizer?", lit=(1953, 2015), part=PART)
        with self.voiceover("Chapter thirteen. Langevin dynamics and the score."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ebm(self):
        rows = [
            cmath(r"p_\theta(x)", r"=", r"\frac{e^{-E_\theta(x)}}{Z_\theta}, \qquad Z_\theta = \int e^{-E_\theta(x)}"
                  r"\, dx", font_size=36),
            cmath(r"\nabla_\theta \log p_\theta(x)", r"=", r"-\nabla_\theta E_\theta(x)", r"+",
                  r"\mathbb E_{x' \sim p_\theta}\big[\nabla_\theta E_\theta(x')\big]", font_size=34),
        ]
        rows[1][2].set_color(DATA)
        rows[1][4].set_color(EBM)
        whys = [why(r"any network $E_\theta$ is an energy"), why(r"push data down, \ push the model's samples up")]
        step = ladder(self, rows, whys, keep=2, top=2.9, x=-1.6, buff=0.6, edge=6.9)
        e = load("ebm2d")
        t = load("toys")
        h = float(t["ring_entropy"])
        nll = float(np.asarray(e["ring_curve"])[-1, 1])
        pl = Plane(2.8, center=[-4.2, -1.9, 0])
        img = pl.image(np.asarray(e["ring_frames"])[-1], EBM)
        box = VGroup(label(r"in two dimensions, $Z$ can be summed on a grid:", font_size=22, color=GREY_A),
                     label(rf"our ring model's held-out NLL: \ ${nll:.2f}$ nats \ (floor ${h:.2f}$)", font_size=22,
                           color=EBM),
                     label(r"in $196$ dimensions, \ a grid of $10$ points per axis has $10^{196}$ cells", font_size=22,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([1.6, -1.9, 0])
        cite_ = cite(r"LeCun, Chopra, Hadsell, Ranzato \& Huang, \textit{A Tutorial on Energy-Based Learning} (2006)",
                     corner=UR)
        with self.voiceover(
            "Restricted Boltzmann machines are one case of a general idea. Any network that outputs a single "
            "number can be an energy, and e to the minus energy, divided by its integral Z, is a density. Nothing "
            "about the network has to be special: no masks, no invertibility, no code. <bookmark mark='a'/> The "
            "gradient of the log-likelihood has the same two phases as before: lower the energy of the data, and "
            "raise it wherever the model puts its own samples. <bookmark mark='b'/> In the plane we can even sum Z "
            f"on a grid, so our ring model's likelihood is exact: {nll:.2f} nats on held-out points, against a "
            f"floor of {h:.2f}. In 196 dimensions no grid will do, so both Z and the samples have to come from "
            "somewhere else."
        ) as vo:
            self.play(FadeIn(cite_))
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(pl), FadeIn(img), FadeIn(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dynamics(self):
        e = load("ebm2d")
        rows = [
            cmath(r"x_{k+1}", r"=", r"x_k", r"+", r"\tfrac{\eta}{2}\, \nabla_x \log p(x_k)", r"+",
                  r"\sqrt{\eta}\; \varepsilon_k", font_size=36),
            cmath(r"\nabla_x \log p_\theta(x)", r"=", r"-\nabla_x E_\theta(x)", r"-", r"\nabla_x \log Z_\theta",
                  font_size=36),
            cmath(r"\nabla_x \log p_\theta(x)", r"=", r"-\nabla_x E_\theta(x)", font_size=36),
        ]
        rows[0][4].set_color(SCORE_C)
        rows[0][6].set_color(NOISE)
        rows[2][2].set_color(SCORE_C)
        whys = [why(r"Langevin dynamics: \ uphill, \ plus noise (Part 5)"), why(r"take the log of $e^{-E}/Z$"),
                why(r"$Z$ doesn't depend on $x$: \ it vanishes")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-1.2, buff=0.5, edge=6.9)
        pl = Plane(3.2, center=[-4.3, -2.0, 0])
        pl.frame.set_opacity(0)
        img = pl.image(np.asarray(e["ring_frames"])[-1], EBM)
        img.set_opacity(0.7)
        ar = arrows(pl, e["ring_score_pts"], e["ring_score"], color=SCORE_C, max_len=0.22, stroke_width=1.8)
        d = definition_card(r"the score", r"$\nabla_x \log p(x)$: \ the direction in which the density rises "
                            r"fastest. \ For an energy model, $-\nabla_x E$, \ with no $Z$ in sight.", width=6.4,
                            font_size=22).move_to([2.6, -2.1, 0])
        with self.voiceover(
            "Sampling comes from physics. Paul Langevin's equation of 1908 describes a particle that drifts "
            "downhill in a potential while being kicked by random collisions. As an algorithm: step uphill on the "
            "log-density, add a little Gaussian noise, repeat. Part 5's Fokker-Planck equation says where such a "
            "walk's distribution settles: exactly into p. <bookmark mark='a'/> The step needs the gradient of log p with respect to "
            "x. Take the log of e to the minus E over Z: <bookmark mark='b'/> Z is a constant, the same for every "
            "x, so its gradient is zero. The normalizer that made training hard has vanished from sampling. "
            "<bookmark mark='c'/> That gradient has a name, the score: the direction in which the density "
            "rises fastest. Here it is for our ring model, arrows pointing into each of the eight valleys of the "
            "energy."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(img), LaggedStart(*[GrowArrow(a_) for a_ in ar], lag_ratio=0.01), FadeIn(d), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        e, t = load("ebm2d"), load("toys")
        pl = Plane(4.4, center=[-3.4, -0.1, 0])
        frames = np.asarray(e["ring_frames"])
        chains = np.asarray(e["ring_frame_chains"])
        steps = list(e["ring_frame_steps"])
        imgs = [pl.image(f, EBM) for f in frames]
        dots = [pl.dots(np.clip(c[:250], -2.95, 2.95), WHITE, radius=0.02, opacity=0.8) for c in chains]
        cap = [label(rf"step ${s:,}$".replace(",", "{,}"), font_size=22, color=EBM).next_to(pl, UP, buff=0.12)
               for s in steps]
        cv = np.asarray(e["ring_curve"])
        h = float(t["ring_entropy"])
        top = float(math.ceil(cv[:, 1].max()))
        g = axes([0, cv[-1, 0]], [0, top], x_length=4.6, y_length=3.0, xlabel=r"training step",
                 ylabel=r"held-out NLL (nats)", xticks=[0, cv[-1, 0]], yticks=[0, round(h, 2), top],
                 center=[3.4, 0.3, 0])
        fl = DashedLine(g.ax.c2p(0, h), g.ax.c2p(cv[-1, 0], h), color=DATA, stroke_width=1.5)
        pts = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.05, color=EBM) for a, b in cv])
        key = VGroup(label(r"glow: \ $e^{-E}/Z$", font_size=18, color=EBM),
                     label(r"dots: \ the Langevin chains it trains against", font_size=18)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(pl, DOWN, buff=0.12)
        k_, eta = int(e["k_steps"]), float(e["eta"])
        gap = float(cv[-1, 1]) - h
        cite_ = cite(r"Du \& Mordatch (2019); \ Nijkamp et al.\ (2019)", corner=DR)
        with self.voiceover(
            "So an energy model can be trained with its own Langevin chains. Keep a pool of chains; at each step "
            f"move a batch of them {k_} Langevin steps downhill, lower the energy of real points, raise it where "
            "the chains ended, and put them back in the pool. Yilun Du and Igor Mordatch made this work for images "
            "in 2019. <bookmark mark='a'/> Here it is on the ring. At first the energy is flat and the chains "
            "wander everywhere. Then valleys open where the data is, the chains fall into them, and the energy "
            "rises wherever the chains crowd but the data doesn't. <bookmark mark='b'/> On held-out points it ends "
            f"{gap:.2f} nats above the floor."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(imgs[0]), FadeIn(dots[0]), FadeIn(cap[0]), FadeIn(key), FadeIn(g),
                      Create(fl), FadeIn(pts[0]), FadeIn(cite_))
            vo.wait_until("a")
            ci, cd, cc = imgs[0], dots[0], cap[0]
            per = max(0.5, vo.until("b") / max(1, len(imgs) - 1))
            for k in range(1, len(imgs)):
                self.play(FadeTransform(ci, imgs[k]), Transform(cd, dots[k]), ReplacementTransform(cc, cap[k]),
                          FadeIn(pts[k]), run_time=0.7 * per)
                ci, cc = imgs[k], cap[k]
                self.wait(0.3 * per)
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def from_noise(self):
        e, ev = load("ebm2d"), load("eval2d")
        panels = []
        for k, n_ in enumerate(("moons", "ring", "checker")):
            pl = Plane(3.6, center=[-4.4 + 4.4 * k, 0.1, 0])
            img = pl.image(np.asarray(e[f"{n_}_frames"])[-1], EBM)
            img.set_opacity(0.6)
            panels.append((pl, img, n_))
        names = {"moons": r"two moons", "ring": r"ring of eight", "checker": r"checkerboard"}
        heads = VGroup(*[label(names[n_], font_size=22, color=EBM).next_to(pl, UP, buff=0.12) for pl, _, n_ in panels])
        rows = ev["rows"]["ebm"]
        modes = [r["modes"] for r in rows]
        steps = 3 * (len(np.asarray(e["ring_langevin"])) - 1)
        with self.voiceover(
            "And sampling. Three hundred points of uniform noise on each density, then Langevin steps on the "
            f"learned energies, {steps} of them. <bookmark mark='a'/> The points slide into the valleys and "
            "jitter there, a sample of the model. <bookmark mark='b'/> On the ring, long chains from noise land "
            f"on {modes[0]}, {modes[1]} and {modes[2]} of the eight modes, in the three seeds. Notice what the "
            "sampler never needed: Z, or any way to invert anything. Only the score."
        ) as vo:
            self.play(*[FadeIn(pl) for pl, _, _ in panels], *[FadeIn(i) for _, i, _ in panels], FadeIn(heads))
            vo.wait_until("a")
            P = [np.asarray(e[f"{n_}_langevin"]) for _, _, n_ in panels]
            dots = [VGroup(*[Dot(q, radius=0.022, color=WHITE) for q in pl.pts(np.clip(p_[0][:200], -2.95, 2.95))])
                    for (pl, _, _), p_ in zip(panels, P)]
            tt = ValueTracker(0.0)

            def mk(dg, pl, p_):
                def upd(g):
                    v = tt.get_value() * (len(p_) - 1)
                    k = min(int(v), len(p_) - 2)
                    a = v - k
                    Q = (1 - a) * p_[k][:200] + a * p_[k + 1][:200]
                    for d_, q in zip(g, pl.pts(np.clip(Q, -2.95, 2.95))):
                        d_.move_to(q)
                return upd

            for dg, (pl, _, _), p_ in zip(dots, panels, P):
                dg.add_updater(mk(dg, pl, p_))
                self.add(dg)
            self.play(tt.animate.set_value(1.0), run_time=max(4.0, vo.until("b") - 0.3), rate_func=linear)
            for dg in dots:
                dg.clear_updaters()
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mixing(self):
        L = load("langevin")
        mus, w = np.asarray(L["mus"]), np.asarray(L["weights"])
        box = 3.0
        pa, pb = Plane(3.6, center=[-3.3, 0.3, 0], box=box), Plane(3.6, center=[1.3, 0.3, 0], box=box)
        def rings(pl):
            return VGroup(*[Circle(radius=0.35 * 2 * pl.side / (2 * box), stroke_color=DATA, stroke_width=1.5)
                            .move_to(pl.p(*m)) for m in mus])
        ra, rb = rings(pa), rings(pb)
        wl = VGroup(MathTex(rf"{w[0]:.1f}", font_size=26, color=DATA).next_to(pa.p(*mus[0]), DL, buff=0.25),
                    MathTex(rf"{w[1]:.1f}", font_size=26, color=DATA).next_to(pa.p(*mus[1]), UR, buff=0.25))
        ta = label(r"Langevin, \ one noise level", font_size=22, color=EBM).next_to(pa, UP, buff=0.12)
        tb = label(r"annealed: \ ten noise levels, \ large to small", font_size=22, color=SCORE_C).next_to(pb, UP,
                                                                                                         buff=0.12)
        ph, ah, sh = float(L["plain_heavy"]), float(L["annealed_heavy"]), float(L["start_heavy"])
        res = VGroup(label(rf"heavy mode: \ ${100 * ph:.0f}\%$ of samples", font_size=22, color=EBM).next_to(pa, DOWN,
                                                                                                         buff=0.15),
                     label(rf"heavy mode: \ ${100 * ah:.0f}\%$", font_size=22, color=SCORE_C).next_to(pb, DOWN,
                                                                                                    buff=0.15))
        truth = label(rf"the truth: \ ${100 * w[1]:.0f}\%$", font_size=22, color=DATA).move_to([5.3, 1.6, 0])
        hist = VGroup(label(r"Hyv\"arinen (2005): \ score matching", font_size=18, color=GREY_A),
                      label(r"Vincent (2011): \ denoising score matching", font_size=18, color=GREY_A),
                      label(r"Song \& Ermon (2019): \ many noise levels", font_size=18, color=GREY_A),
                      label(r"$\to$ \ diffusion, \ Part 21", font_size=20, color=SCORE_C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.2, -0.6, 0])
        eqm = label(r"2025: \ Equilibrium Matching (Wang \& Du): \ an implicit energy, \ FID $1.90$ on ImageNet "
                    r"$256^2$", font_size=20, color=EBM).to_edge(DOWN, buff=0.3)
        close = abs(ah - w[1]) < abs(ph - w[1])
        verdict = (f"Annealing fixes it: {100 * ah:.0f} percent, close to the truth." if close and abs(ah - w[1]) < 0.06
                   else f"Annealing moves it to {100 * ah:.0f} percent.")
        with self.voiceover(
            "There is a catch, and it is the bridge to the next part. Here are two Gaussians, one holding twenty "
            "percent of the probability and one eighty, with their score known exactly. <bookmark mark='a'/> Start "
            "points uniformly and run Langevin. <bookmark mark='b'/> Each point falls into the nearer valley and "
            "stays: crossing the gap between them is so unlikely that it never happens. So the share of samples in "
            f"the heavy mode is {100 * ph:.0f} percent, set by where they started, {100 * sh:.0f} percent, not by "
            "the eighty percent the density says. The score is blind to the weights of separated modes. <bookmark "
            "mark='c'/> Yang Song and Stefano Ermon's fix, in 2019: blur the density with a lot of noise, where the "
            "valleys merge and points can move freely, then follow the score as the noise is turned down, level by "
            f"level. {verdict} <bookmark mark='d'/> To do this on images you need the score of the data at every "
            "noise level, learned by denoising, as Aapo Hyvarinen and Pascal Vincent showed. That is diffusion, "
            "Part 21. And energies themselves are back: in 2025 Equilibrium Matching learned an implicit energy "
            "landscape and generated ImageNet images by descending it."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(ra), FadeIn(wl), FadeIn(ta), FadeIn(truth))
            vo.wait_until("a")
            particle_play(self, pa, L["plain_path"], max(3.0, vo.until("b") + 2.0), color=EBM, n=250)
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(pb), FadeIn(rb), FadeIn(tb))
            particle_play(self, pb, L["annealed_path"], max(3.0, vo.until("d") - 1.0), color=SCORE_C, n=250)
            self.play(FadeIn(res[1]))
            vo.wait_until("d")
            self.play(FadeIn(hist), FadeIn(eqm))
        self.wait(0.3)
        self.clear_scene()
