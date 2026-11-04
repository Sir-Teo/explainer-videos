from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import deep as D
from explainer.quant.house import quoting
from videos.quant.quant17.common import (BAD, DELTA, GOOD, NET, OPT, PART, REF, ask, grid_fn, house_lab, illustration,
                                         load)


class Band3D(VoiceoverScene, ThreeDScene):
    def construct(self):
        h = load("hedge")
        hs = load("hedge_seeds")
        self.card()
        self.sheets(h, load("hedge_live"))
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

    def sheets(self, h, L):
        sf = h["band"]["surface"]
        S = np.asarray(sf["S"])
        days = np.asarray(sf["tau"]) * 30
        lo, hi, wl, wh = (np.clip(np.asarray(sf[k]), 0, 1) for k in ("lo", "hi", "ww_lo", "ww_hi"))
        ax = ThreeDAxes(x_range=[S[0], S[-1], 10], y_range=[0, 30, 10], z_range=[0, 1, 0.5], x_length=7.0, y_length=5.0,
                        z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2}).shift(DOWN * 0.9 + RIGHT * 1.3)  # clear of the key

        def sheet(Z, col, op, stroke=0.3, sw=None):
            f = grid_fn(S, days, Z)
            return Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(S[0], S[-1]), v_range=(days[0], days[-1]),
                           resolution=(24, 12), fill_color=col, fill_opacity=op, stroke_width=sw if sw is not None else stroke,
                           stroke_color=col, checkerboard_colors=False)
        mid = (np.asarray(sf["ww_lo"]) + np.asarray(sf["ww_hi"])) / 2
        dl = sheet(np.clip(mid, 0, 1), WHITE, 0.0, sw=0.8)
        s_lo, s_hi = sheet(lo, NET, 0.45), sheet(hi, NET, 0.45)
        w_lo, w_hi = sheet(wl, DELTA, 0.0, sw=1.0), sheet(wh, DELTA, 0.0, sw=1.0)
        Sx, hb = np.asarray(L["S"]), np.asarray(L["band"])
        k_ = np.arange(len(hb))
        pts = [ax.c2p(np.clip(Sx[k], S[0], S[-1]), 30 - k, hb[k]) for k in k_]
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
        self.set_camera_orientation(phi=64 * DEGREES, theta=-62 * DEGREES, zoom=0.8)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "The learned hedge as a surface, over time and price: the Black–Scholes delta as a white mesh, "
            "sharpening toward expiry. <bookmark mark='a'/> Above and below it, the two edges of the band the network learned, at half "
            "a percent costs: two translucent sheets, the hedge never leaving the space between them. "
            "<bookmark mark='b'/> And in yellow, Whalley and Wilmott's edges. Walk along the strike toward expiry: their "
            "band bulges where gamma is largest, at the money in the last days; the learned band stays nearly flat "
            f"across prices, {wn[i30]:.2f} shares wide at the money with a month left and {wn[i5]:.2f} with five days. "
            "<bookmark mark='c'/> Now one simulated month runs on the surface. The bead is the network's holding: it "
            "sits still while the sheets move around it, and is pushed only when an edge reaches it."
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
        self.clear_scene()

    def theory(self):
        rows = [cmath(r"[\ell, u]", r"=", r"\big[\Delta - \mathrm{softplus}(a_\theta),\ \Delta + \mathrm{softplus}(b_\theta)\big]",
                      font_size=38, colors={r"[\ell, u]": NET}),
                cmath(r"\delta_k", r"=", r"\min\big(\max(\delta_{k-1}, \ell_k), u_k\big)", font_size=40, colors={r"\delta_k": NET}),
                cmath(r"\text{optimal policy}", r"=", r"\text{a no-trade region}", font_size=40,
                      colors={r"\text{optimal policy}": GOOD})]
        whys = [why(r"Imaki, Imajo, Ito, Minami and Nakagawa (2021): the network outputs only how far below and above "
                    r"the Black--Scholes delta the band reaches, from the log price and the time left"),
                why(r"the hedge moves only to the nearest edge, and only when it is outside: the architecture cannot "
                    r"trade inside the band, so it never pays for small corrections"),
                why(r"Davis, Panas and Zariphopoulou (1993): under exponential utility and proportional costs the optimal "
                    r"hedge of an option is a no-trade region, so the architecture gives up nothing. Whalley and "
                    r"Wilmott's band is its small-cost, continuous-trading limit; at daily rebalancing the hedge already "
                    r"lags between dates, which is one reason the learned band is narrower")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Why build the band into the network? The band network outputs only two numbers: how far below and above "
            "the delta its band reaches. <bookmark mark='a'/> The hedge is then clipped into the band: it moves only "
            "to the nearest edge, and only when it is outside. <bookmark mark='b'/> And theory says nothing is lost. "
            "Mark Davis, Vassilios Panas and Thaleia Zariphopoulou proved in 1993 that with exponential utility and "
            "proportional costs the optimal hedge is a no-trade region. Whalley and Wilmott's band is its limit for "
            "small costs and continuous trading. With trading only once a day, the hedge already drifts between dates, "
            "so it needs less band."
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
        g = axes([-0.5, 2.5], [2.3, 3.9], x_length=6.2, y_length=4.2, xlabel=r"trading cost, per cent",
                 ylabel=r"band network's price", xticks=[0, 1, 2], xfmt=lambda v: f"{100 * costs[int(round(v))]:g}",
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
                      MathTex(rf"\text{{learned band widens}}\ \times {ratio:.2f}", font_size=30, color=NET),
                      MathTex(rf"\text{{Whalley--Wilmott}}\ \times {wwr:.2f} = 2^{{1/3}}", font_size=30, color=DELTA),
                      wrapped_label(rf"three seeds agree on the price to within {max(spreads):.3f} at every cost", 4.2,
                                    19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Is this one lucky network? Three seeds at three cost levels. <bookmark mark='a'/> The prices agree to "
            f"within {max(spreads):.3f} at every cost: the band network is a very stable thing to train. "
            "<bookmark mark='b'/> And the hook's question, measured. Double the cost from half a percent to one: "
            f"Whalley and Wilmott's band widens by the cube root of two, {wwr:.2f}; the learned band at the money "
            f"widens by {ratio:.2f}. Not double, in either case."
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
        top = float(np.percentile(np.r_[runs_d.ravel(), runs_w.ravel()], 98))
        lo = float(min(runs_d.min(), runs_w.min())) - 0.05
        g = axes([0, steps[-1]], [lo, top], x_length=7.2, y_length=4.2, xlabel=r"training step",
                 ylabel=r"entropic risk, 0.5\% costs", xticks=[0, 200, 400, 600], yticks=[round(lo + 0.1, 1), round(top, 1)],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        bd = seed_band(g.ax, steps, np.clip(runs_d, lo, top), NET)
        bw = seed_band(g.ax, steps, np.clip(runs_w, lo, top), GOOD)
        leg = legend([(NET, r"default start: a narrow band"), (GOOD, r"started at Whalley--Wilmott's band")],
                     font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        e_d = [bp["runs"][f"default_{s}"]["eval"]["price"] for s in (0, 1)]
        e_w = [bp["runs"][f"ww_{s}"]["eval"]["price"] for s in (0, 1)]
        early = int(len(steps) * 0.15)
        a_d, a_w = float(runs_d[:, :early].mean()), float(runs_w[:, :early].mean())
        if a_w < a_d:
            verdict = "the Whalley-Wilmott start is ahead early, as Arzel and Lehdili report"
        else:
            verdict = "in our small run the Whalley-Wilmott start is not ahead early, unlike Arzel and Lehdili's report"
        side = wrapped_label(rf"after 600 steps of 4{{,}}096 paths, two seeds each: prices {min(e_d):.3f}--{max(e_d):.3f} "
                             rf"from the default start, {min(e_w):.3f}--{max(e_w):.3f} from Whalley--Wilmott's", 4.2, 19,
                             GREY_A).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Theory can also help the training. Jules Arzel and Noureddine Lehdili proposed in 2026 to start the band "
            "network at Whalley and Wilmott's band instead of a narrow one: the formula as a prior, the network as "
            "the correction. We built that start into the House and trained both, two seeds each. "
            f"<bookmark mark='a'/> Over the first hundred steps, {verdict}. After six hundred steps, the prices are "
            f"{min(e_w):.3f} to {max(e_w):.3f} from the formula's start and {min(e_d):.3f} to {max(e_d):.3f} from "
            "the default."
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
            "A question: near expiry, far out of the money, where are the two edges? Think about what the delta is "
            "there, and whether the band can bind."
            " Both edges close in on zero. The delta is zero there and so is gamma, so the band is narrow, but the holding is already zero and nothing trades: the band cannot bind. Next: what the vanillas leave undecided."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
