from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from explainer.quant.house import deep as D
from explainer.quant.house import quoting
from videos.quant.quant17.common import (BAD, DELTA, GOOD, NET, OPT, PART, REF, ask, grid_fn, house_lab, illustration,
                                         load, flat_camera)


class Band3D(VoiceoverScene, ThreeDScene):
    def construct(self):
        h = load("hedge")
        hs = load("hedge_seeds")
        self.card()
        self.sheets(h, load("hedge_live"), hs)
        self.theory()
        self.seeds(h, hs)
        self.prior(load("band_prior"))
        self.lab(h, hs)

    def card(self):
        c = chapter_card(14, r"The band as a surface", r"What does the learned hedge look like over time and price?",
                         part=PART)
        with self.voiceover("Chapter fourteen. Where not to trade, part two: the band as a surface."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheets(self, h, L, hs):
        sf = dict(h["band"]["surface"])
        other = hs["surface"]
        assert np.allclose(sf["S"], other["S"]) and np.allclose(sf["tau"], other["tau"])
        sf.update(lo=other["lo"], hi=other["hi"])
        S = np.asarray(sf["S"])
        days = np.asarray(sf["tau"]) * 30
        lo, hi, wl, wh = (np.asarray(sf[k]) for k in ("lo", "hi", "ww_lo", "ww_hi"))
        Sx, hb = np.asarray(L["S"]), np.asarray(L["band"])
        zr = data_range(lo, hi, wl, wh, hb, [0, 1])
        xr = data_range(S, Sx)
        ax = ThreeDAxes(x_range=[*xr, 10], y_range=[0, 30, 10], z_range=[*zr, 0.5], x_length=7.0, y_length=5.0,
                        z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2}).shift(DOWN * 0.9 + RIGHT * 1.3)  # clear of the key

        def sheet(Z, col, op, stroke=0.3, sw=None):
            f = grid_fn(S, days, Z)
            return Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(S[0], S[-1]), v_range=(days[0], days[-1]),
                           resolution=(24, 12), fill_color=col, fill_opacity=op, stroke_width=sw if sw is not None else stroke,
                           stroke_color=col, checkerboard_colors=False)
        mid = (np.asarray(sf["ww_lo"]) + np.asarray(sf["ww_hi"])) / 2
        dl = sheet(mid, WHITE, 0.0, sw=0.8)
        s_lo, s_hi = sheet(lo, NET, 0.45), sheet(hi, NET, 0.45)
        w_lo, w_hi = sheet(wl, DELTA, 0.0, sw=1.0), sheet(wh, DELTA, 0.0, sw=1.0)
        pts = []
        for k in range(len(hb)):
            if k:
                pts.append(ax.c2p(Sx[k], 30-k, hb[k-1]))
            pts.append(ax.c2p(Sx[k], 30-k, hb[k]))
        trail = VMobject(stroke_color=GOOD, stroke_width=4).set_points_as_corners(pts)
        bead = Dot3D(pts[0], radius=0.08, color=GOOD)
        k0 = int(np.argmin(np.abs(S - 100)))
        wn = hi[:, k0] - lo[:, k0]
        ww_w = wh[:, k0] - wl[:, k0]
        i30, i5 = len(days) - 1, int(np.argmin(np.abs(days - 5)))
        hint = VGroup(label(r"price (across), days to expiry (back), shares held (up)", font_size=19, color=GREY_A),
                      legend([(WHITE, r"Black--Scholes delta"), (NET, r"the learned band's two edges"),
                              (DELTA, r"Whalley--Wilmott's edges (mesh)"), (GOOD, r"one path's holding")], font_size=16),
                      label(rf"width at the money: {wn[i30]:.2f} at 30 days, {wn[i5]:.2f} at 5 (theirs: {ww_w[i30]:.2f}, "
                            rf"{ww_w[i5]:.2f})", font_size=18, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.3)
        hint[2].to_corner(DL, buff=0.4)  # clear of the surface
        self.set_camera_orientation(phi=64 * DEGREES, theta=-62 * DEGREES, zoom=0.8)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "The learned sheets and the path now use the same saved policy, seed three. White is the supplied Black–Scholes delta; all edge values are retained. <bookmark mark='a'/> The architecture learns two positive offsets around that delta. After a daily decision it clamps the holding inside its band; between decisions a moving band can leave the old holding outside. <bookmark mark='b'/> Yellow meshes are the continuous small-cost asymptotic edges, not a guarantee for this daily model. <bookmark mark='c'/> The path joins saved daily states, with vertical segments for changes in holding. The mesh covers one and a half to thirty days remaining, while the last daily decision is at one day, outside that mesh. This animation illustrates recorded decisions rather than continuous optimal control."
        ) as vo:
            self.play(Create(ax), FadeIn(hint[0]), Create(dl), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(s_lo), FadeIn(s_hi), FadeIn(hint[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(w_lo), Create(w_hi), FadeIn(hint[2]), run_time=2)
            self.move_camera(theta=-25 * DEGREES, phi=70 * DEGREES, run_time=3)
            vo.wait_until("c")
            self.add(bead)
            self.play(MoveAlongPath(bead, trail), Create(trail), run_time=max(vo.remaining(0.3), 4), rate_func=linear)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, dl, s_lo, s_hi, w_lo, w_hi, trail, bead)),
                                                                  FadeOut(hint)], run_time=1.2)
        flat_camera(self)
        self.clear_scene()

    def theory(self):
        rows = [cmath(r"[\ell, u]", r"=", r"\big[\Delta - \mathrm{softplus}(a_\theta),\ \Delta + \mathrm{softplus}(b_\theta)\big]",
                      font_size=38, colors={r"[\ell, u]": NET}),
                cmath(r"\delta_k", r"=", r"\min\big(\max(\delta_{k-1}, \ell_k), u_k\big)", font_size=40, colors={r"\delta_k": NET}),
                cmath(r"\text{architecture}", r":", r"\text{delta-centred band restriction, to validate}", font_size=40,
                      colors={r"\text{architecture}": GOOD})]
        whys = [why(r"Imaki, Imajo, Ito, Minami and Nakagawa (2021): the network outputs only how far below and above "
                    r"the Black--Scholes delta the band reaches, from the log price and the time left"),
                why(r"the hedge moves only to the nearest edge, and only when it is outside: the architecture cannot "
                    r"trade inside the band, so it never pays for small corrections"),
                why(r"No-trade-region theorems have model and admissibility assumptions. They do not certify this delta-centred finite network or its daily empirical objective.")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "This architecture supplies Black–Scholes delta and learns positive lower and upper offsets. <bookmark mark='a'/> Clamping gives an exact no-trade rule inside that fitted band at each decision date. It is a useful structural restriction, not something learned from scratch. <bookmark mark='b'/> Continuous-time transaction-cost control can yield no-trade regions under specific utility, admissibility and market assumptions. That does not prove this finite network, delta-centred parameterization or daily grid sacrifices no optimality. Nor does it prove the learned band must be narrower than the asymptotic one. Both the structural prior and the fitted policy need validation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def seeds(self, h, hs):
        costs = [0.001, 0.005, 0.01]
        cache = {r["cost"]: r["deep"]["price"] for r in h["band"]["rows"]}
        yr = data_range(list(cache.values()), *[[hs["runs"][f"{c}_{s}"]["eval"]["price"] for s in (3,4)] for c in costs])
        g = axes([-0.5, 2.5], yr, x_length=6.2, y_length=4.2, xlabel=r"trading cost, per cent",
                 ylabel=r"band policy's empirical objective", xticks=[0, 1, 2], xfmt=lambda v: f"{100 * costs[int(round(v))]:g}",
                 yticks=[2.5, 3.0, 3.5], font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        dots = VGroup()
        spreads = []
        for i, c in enumerate(costs):
            vals = [cache[c]] + [hs["runs"][f"{c}_{s}"]["eval"]["price"] for s in (3, 4)]
            spreads.append(max(vals) - min(vals))
            for j, v in enumerate(vals):
                dots.add(Dot(g.ax.c2p(i - 0.12 + 0.12 * j, v), radius=0.07, color=[NET, GOOD, OPT][j]))
        leg = legend([(NET, r"seed 2 (the cached run)"), (GOOD, r"seed 3"), (OPT, r"seed 4")], font_size=17).next_to(
            g, UP, buff=0.1).align_to(g, LEFT)
        w5 = [hs["runs"][f"0.005_{s}"]["band_atm"] for s in (3, 4)]
        w10 = [hs["runs"][f"0.01_{s}"]["band_atm"] for s in (3, 4)]
        ratio = float(np.mean([(b[1] - b[0]) / (a[1] - a[0]) for a, b in zip(w5, w10)]))
        wwr = hs["ww_half_atm"]["0.01"] / hs["ww_half_atm"]["0.005"]
        side = VGroup(label(r"double the cost, from 0.5\% to 1\%:", font_size=21),
                      MathTex(rf"\text{{learned width ratio}}\ \times {ratio:.2f}", font_size=30, color=NET),
                      MathTex(rf"\text{{Whalley--Wilmott}}\ \times {wwr:.2f} = 2^{{1/3}}", font_size=30, color=DELTA),
                      wrapped_label(rf"three recorded empirical objectives span at most {max(spreads):.3f} at each displayed cost", 4.2,
                                    19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            f"Three fixed training seeds use the same saved setup at each cost. Their empirical evaluation objectives span at most {max(spreads):.3f}. <bookmark mark='a'/> This finite range is not a confidence interval, proof of stable training in general, or control of exponential-tail error. <bookmark mark='b'/> At the money and fifteen days remaining, the ratio of learned full widths after doubling cost is averaged over only seeds three and four: {ratio:.2f}. The analytic small-cost half-width ratio is {wwr:.2f}. These two summaries are not a statistical test of a scaling law across products, times and market states."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def prior(self, bp):
        runs_d = np.array([bp["runs"][f"default_{s}"]["curve"] for s in (0, 1)])
        runs_w = np.array([bp["runs"][f"ww_{s}"]["curve"] for s in (0, 1)])
        steps = np.arange(runs_d.shape[1], dtype=float)
        top = data_range(runs_d, runs_w)[1]
        lo = float(min(runs_d.min(), runs_w.min())) - 0.05
        g = axes([0, steps[-1]], [lo, top], x_length=7.2, y_length=4.2, xlabel=r"training step",
                 ylabel=r"empirical exponential objective, 0.5\% costs", xticks=[0, 200, 400, 600], yticks=[round(lo + 0.1, 1), round(top, 1)],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        bd = seed_band(g.ax, steps, runs_d, NET)
        bw = seed_band(g.ax, steps, runs_w, GOOD)
        leg = legend([(NET, r"default start: a narrow band"), (GOOD, r"clamped Whalley--Wilmott structural prior")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        e_d = [bp["runs"][f"default_{s}"]["eval"]["price"] for s in (0, 1)]
        e_w = [bp["runs"][f"ww_{s}"]["eval"]["price"] for s in (0, 1)]
        early = int(len(steps) * 0.15)
        a_d, a_w = float(runs_d[:, :early].mean()), float(runs_w[:, :early].mean())
        if a_w < a_d:
            verdict = "the Whalley-Wilmott start is ahead early, as Arzel and Lehdili report"
        else:
            verdict = "in our small run the Whalley-Wilmott start is not ahead early, unlike Arzel and Lehdili's report"
        side = wrapped_label(rf"after 600 steps of 4{{,}}096 paths, two seeds each: empirical objectives {min(e_d):.3f}--{max(e_d):.3f} "
                             rf"from the default start, {min(e_w):.3f}--{max(e_w):.3f} from Whalley--Wilmott's", 4.2, 19,
                             GREY_A).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            f"The 2026 Arzel–Lehdili preprint studies a Whalley–Wilmott structural prior and a differentiable soft clamp. Our saved illustration uses a different hard-clamp implementation. Its prior half-width is floored at 0.001 shares and capped at one, and remains in the parameterization throughout training; this changes more than initialization. <bookmark mark='a'/> There are two seeds per setup. The displayed early average uses {early} updates, and the six-hundred-update empirical evaluations range from {min(e_w):.3f} to {max(e_w):.3f} with the prior, and {min(e_d):.3f} to {max(e_d):.3f} without it. These runs illustrate a design choice; they neither reproduce the paper's experiment nor isolate a universal initialization advantage."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.play(Create(bd), Create(bw), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, h, hs):
        card = house_lab(r"the band, learned and derived", D.Hedger.band, "t = torch.clamp", 5,
                         extra=[(quoting.ww_band, "g = bs.greeks", 2)], width=8.6)
        card.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.6)
        m = h["mlp_cost"]["ww_slices"]["100"]
        b = hs["runs"]["0.005_3"]["band_atm"]
        outs = [f"at the money, 15 days left, 0.5% costs:",
                f"learned band   [{b[0]:.3f}, {b[1]:.3f}]",
                f"Whalley-Wilmott [{m[0]:.3f}, {m[1]:.3f}]   delta {m[2]:.3f}"]
        with self.voiceover(
            "The two bands in the House's code: the network's, delta plus two softplus offsets; Whalley and "
            "Wilmott's, the cube-root half-width. <bookmark mark='a'/> At the money, fifteen days left:"
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        q = ask(r"near expiry and far out of the money, where are the band's two edges?")
        with self.voiceover(
            'For the asymptotic formula, away from the strike as maturity tends to zero, delta and gamma vanish, so its two edges tend to zero. Learned softplus widths are not guaranteed to share that limit. Nor does a zero target imply no trade: a positive previous holding may have to be sold at the next decision. Whether a band binds depends on both its current edges and the previous position. Next: what vanilla prices leave undecided.'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
