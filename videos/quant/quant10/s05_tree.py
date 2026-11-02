from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import CASH, DEL, GAM, OPT, PART, QQ, SPOT, THE, computed, load


class Tree(VoiceoverScene, ThreeDScene):
    def construct(self):
        d = load("tree")
        self.card()
        self.one_step()
        self.lattice(load("tree3d"))
        self.derive()
        self.limit(d, load("tree3d"))

    def card(self):
        c = chapter_card(5, r"The tree and its limit", r"Can a coin flip price an option?", lit=(1979,), part=PART)
        with self.voiceover("Chapter five. The tree and its limit."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def one_step(self):
        # one period: the stock goes from 100 to 120 or 90; a call with strike 100; no interest
        S0, Su, Sd, K = 100, 120, 90, 100
        Cu, Cd = Su - K, 0
        delta = (Cu - Cd) / (Su - Sd)
        bond = Cu - delta * Su
        c0 = delta * S0 + bond
        root = np.array([-5.6, 0.2, 0])
        up, dn = root + np.array([3.2, 1.7, 0]), root + np.array([3.2, -1.7, 0])

        def node(p, tex, col):
            return VGroup(Circle(radius=0.48, color=col, stroke_width=2.5, fill_color=BACKGROUND, fill_opacity=1)
                          .move_to(p), MathTex(tex, font_size=34, color=col).move_to(p))

        n0, nu, nd = node(root, "100", SPOT), node(up, "120", SPOT), node(dn, "90", SPOT)
        e1 = Line(n0.get_center(), nu.get_center(), buff=0.5, color=GREY_C)
        e2 = Line(n0.get_center(), nd.get_center(), buff=0.5, color=GREY_C)
        cu = MathTex(r"C_u = 20", font_size=32, color=OPT).next_to(nu, RIGHT, buff=0.3)
        cd = MathTex(r"C_d = 0", font_size=32, color=OPT).next_to(nd, RIGHT, buff=0.3)
        tree = VGroup(e1, e2, n0, nu, nd, cu, cd)
        rows = VGroup(
            MathTex(r"\Delta = \frac{C_u - C_d}{S_u - S_d} = \frac{20}{30} = \tfrac23", font_size=34, color=DEL),
            MathTex(rf"\text{{bond}} = C_u - \Delta S_u = 20 - 80 = {bond:.0f}", font_size=34, color=CASH),
            MathTex(rf"C_0 = \Delta S_0 + \text{{bond}} = 66.67 - 60 = {c0:.2f}", font_size=36, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.5).shift(UP * 1.4)
        prob = VGroup(
            MathTex(r"C_0 = q\,C_u + (1 - q)\,C_d", font_size=34, color=OPT),
            MathTex(r"q = \frac{S_0 - S_d}{S_u - S_d} = \tfrac13", font_size=34, color=QQ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows, DOWN, buff=0.6).align_to(rows, LEFT)
        pnote = label(r"whatever the real chance of going up", font_size=24, color=GREY_A)
        pnote.next_to(prob, DOWN, buff=0.25).align_to(prob, LEFT)
        ill = note(r"illustrative: zero interest, one period", font_size=18).to_corner(DL, buff=0.3)
        with self.voiceover(
            "The third road is the one that is easiest to see. Cox, Ross and Rubinstein, 1979: one step, two "
            "outcomes. From one hundred the stock goes to one hundred and twenty or to ninety, and a call struck at "
            "one hundred is worth twenty or nothing. <bookmark mark='a'/> Hold two thirds of a share, "
            "<bookmark mark='b'/> borrow sixty, and the copy matches the call in both states, so it costs the same: "
            f"{c0:.2f}. <bookmark mark='c'/> Written as an average of the payoffs, the weight on the up state is "
            "one third, whatever the real chance of going up. Part nine built this; here we take it to its "
            "limit."
        ) as vo:
            self.play(FadeIn(n0), FadeIn(ill))
            self.play(Create(e1), Create(e2), FadeIn(nu), FadeIn(nd))
            self.play(FadeIn(cu), FadeIn(cd))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            self.play(Write(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(prob, shift=UP * 0.2))
            self.play(FadeIn(pnote))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lattice(self, t3):
        K, T, sig, r = t3["K"], t3["T"], t3["sigma"], t3["r"]
        ax = ThreeDAxes(x_range=[0, 1, 0.25], y_range=[50, 200, 50], z_range=[0, 100, 25], x_length=7.0,
                        y_length=6.0, z_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.4)
        surf = price_surface(ax, lambda t, S: float(bs.price(S, K, max(T - t, 1e-4), sig, r)), (0.0, 0.999),
                             (50, 200), resolution=(24, 24), z_lo=0, z_hi=100, opacity=0.35)

        def nodes(N, cap=1500):
            t, S, V = (np.asarray(t3[f"{c}_{N}"], float) for c in ("t", "s", "v"))
            m = (S >= 50) & (S <= 200)
            idx = np.flatnonzero(m)
            if len(idx) > cap:
                idx = idx[np.linspace(0, len(idx) - 1, cap).astype(int)]
            rad = {4: 0.09, 16: 0.06, 64: 0.04, 256: 0.03}[N]
            return VGroup(*[Dot3D(ax.c2p(t[i], S[i], min(V[i], 100)), radius=rad, color=YELLOW, resolution=(4, 4))
                            for i in idx])

        groups = {N: nodes(N) for N in t3["N"]}
        hint = VGroup(label(r"time $t$", font_size=24, color=THE), label(r"stock price $S$", font_size=24, color=SPOT),
                      label(r"call value $V$", font_size=24, color=OPT)).arrange(DOWN, aligned_edge=LEFT,
                                                                                 buff=0.1).to_corner(UL, buff=0.35)
        readout_ = VGroup()

        def tag_(N):
            j = list(t3["N"]).index(N)
            return VGroup(MathTex(rf"N = {N}", font_size=36, color=YELLOW),
                          MathTex(rf"\text{{price}}\ {t3[f'price_{N}']:.4f}", font_size=30, color=OPT),
                          MathTex(rf"\text{{worst node gap}}\ {t3['max_gap'][j]:.3f}", font_size=26, color=GREY_A)
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)

        self.set_camera_orientation(phi=68 * DEGREES, theta=-60 * DEGREES, zoom=0.88)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "Chop the year into steps and the tree's nodes become points in space: time across, stock price "
            "along, and the call's value as height. Here is a four-step tree, every node at the value backward "
            "induction gives it, and behind it, translucent, the Black-Scholes surface. "
            "<bookmark mark='a'/> Sixteen steps. <bookmark mark='b'/> Sixty-four. <bookmark mark='c'/> Two hundred "
            "and fifty-six. The nodes multiply and settle onto the surface: the worst gap between a node and the "
            f"surface falls from {t3['max_gap'][0]:.2f} to {t3['max_gap'][-1]:.2f}, roughly halving every time the "
            "steps are multiplied by four, and the largest gaps sit where the payoff has its kink. The tree is not "
            "an approximation to the price at one point. It is a whole discretized copy of the surface."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            self.play(FadeIn(surf), run_time=1.0)
            cur = groups[4]
            tg = tag_(4)
            self.add_fixed_in_frame_mobjects(tg)
            self.play(LaggedStart(*[FadeIn(x, scale=0.5) for x in cur], lag_ratio=0.05, run_time=1.5), FadeIn(tg))
            for N, mark in ((16, "a"), (64, "b"), (256, "c")):
                vo.wait_until(mark)
                nt = tag_(N)
                self.add_fixed_in_frame_mobjects(nt)
                self.remove(nt)
                self.play(FadeOut(cur), FadeIn(groups[N]), FadeOut(tg), FadeIn(nt), run_time=1.2)
                cur, tg = groups[N], nt
            self.move_camera(theta=-20 * DEGREES, phi=62 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, cur)), FadeOut(hint),
                                                                  FadeOut(tg)], run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        C = {r"q": QQ, r"u": SPOT, r"\Delta t": THE, r"V": OPT, r"r": CASH, r"\sigma": GAM}
        rows = [
            cmath(r"V(t, S)", r"=", r"e^{-r\Delta t}\big[", r"q", r"\,V(t + \Delta t, uS) + (1 - ", r"q",
                  r")\,V(t + \Delta t, S/u)\big]", font_size=32, colors=C),
            cmath(r"u = e^{\sigma\sqrt{\Delta t}},\quad", r"q", r"= \tfrac12 + \frac{r - \sigma^2/2}{2\sigma}\sqrt{\Delta t}"
                  r" + O(\Delta t)", font_size=32, colors=C),
            cmath(r"V(t + \Delta t, u^{\pm 1}S) = V \pm \sigma\sqrt{\Delta t}\,S V_S + \Delta t\,(V_t + "
                  r"\tfrac12\sigma^2 S V_S + \tfrac12\sigma^2 S^2 V_{SS}) + \dots", font_size=30, colors=C),
            cmath(r"0", r"=", r"V_t + r S V_S + \tfrac12\sigma^2 S^2 V_{SS} - r V", r"\;+\;O(\Delta t)", font_size=36,
                  colors=C),
        ]
        whys = [why(r"backward induction: the discounted risk-neutral average"),
                why(r"expand $q = (e^{r\Delta t} - 1/u)/(u - 1/u)$ in $\sqrt{\Delta t}$"),
                why(r"Taylor in $\ln S$ to order $\Delta t$"),
                why(r"collect powers of $\sqrt{\Delta t}$, divide by $\Delta t$: the Black--Scholes PDE")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-1.0, buff=0.75, edge=6.9)
        with self.voiceover(
            "Why it must converge is a short calculation. Each node is the discounted risk-neutral average of its "
            "two successors. <bookmark mark='a'/> With an up move of e to the sigma root delta t, the risk-neutral "
            "probability is one half plus a correction of order root delta t. <bookmark mark='b'/> Expand the two "
            "successors' values in a Taylor series: the root delta t terms carry the slope, the delta t terms "
            "the curvature. <bookmark mark='c'/> Substitute, collect powers, divide by delta t, and the recursion "
            "is the Black-Scholes equation plus an error of order delta t. The tree is the equation, discretized."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limit(self, d, t3d):
        N = np.asarray(d["N"], float)
        px = np.asarray(d["price"], float)
        exact = d["exact"]
        g = axes([0, np.log10(400)], [9.4, 12.4], x_length=7.4, y_length=4.4, xlabel=r"number of steps $N$",
                 ylabel=r"the tree's price", xticks=[0, 1, 2], yticks=[9.5, 10.5, 11.5],
                 xfmt=lambda v: f"10^{{{int(v)}}}", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        lx = np.log10(N)
        line = DashedLine(ax.c2p(0, exact), ax.c2p(np.log10(400), exact), color=OPT, stroke_width=2)
        line_lab = MathTex(rf"\text{{formula}}\ {exact:.4f}", font_size=26, color=OPT)
        line_lab.next_to(ax.c2p(np.log10(400), exact), UP, buff=0.12).shift(LEFT * 0.9)
        odd = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=SPOT) for a, b, n in zip(lx, px, N) if int(n) % 2])
        even = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=QQ) for a, b, n in zip(lx, px, N) if not int(n) % 2])
        leg = VGroup(VGroup(Dot(color=SPOT, radius=0.06), label(r"odd $N$", font_size=22, color=SPOT))
                     .arrange(RIGHT, buff=0.12),
                     VGroup(Dot(color=QQ, radius=0.06), label(r"even $N$", font_size=22, color=QQ))
                     .arrange(RIGHT, buff=0.12)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        leg.move_to(ax.c2p(1.9, 12.0))
        right = VGroup(
            label(r"$N = 400$ steps:", font_size=28, color=GREY_A),
            MathTex(rf"{d['big_N_price']:.4f}", font_size=42, color=OPT),
            label(r"the formula:", font_size=28, color=GREY_A),
            MathTex(rf"{exact:.4f}", font_size=42, color=OPT),
            label(r"error $\propto 1/N$, alternating in sign", font_size=24, color=GREY_A),
            label(r"central limit theorem: the coin flips", font_size=24, color=GREY_A),
            label(r"become a lognormal", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.55)
        even_err = float(np.mean((px - exact)[(N % 2 == 0) & (N >= 20)]))
        side = "below" if even_err < 0 else "above"
        with self.voiceover(
            "Add steps and the tree's price converges to the formula. Here it is for every number of steps from "
            "one to four hundred, drawn as it computes. It zigzags. Pause and predict: an even number of steps "
            "puts a node exactly at the strike. Are those trees above the formula, or below? "
            f"<bookmark mark='a'/> Here, {side}: the two families err on opposite sides and close in like one over "
            "N, with a wobble set by where the strike falls between nodes, which Francine and Marc Diener worked "
            "out exactly in 2004, and which Part sixteen's smoother trees remove. "
            f"<bookmark mark='b'/> With four hundred steps the tree gives {d['big_N_price']:.4f}; the formula, "
            f"{exact:.4f}."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(line_lab), FadeIn(leg))
            self.play(LaggedStart(*[FadeIn(x) for x in sorted([*odd, *even], key=lambda m: m.get_x())],
                                  lag_ratio=0.01, run_time=max(vo.until("a") - 2.5, 3.0)))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()
        t3 = t3d
        card = lab_card(r"backward induction", [
            "for n in range(N - 1, -1, -1):",
            "    spots_n = S * u ** (2 * np.arange(n + 1) - n)",
            "    cont = disc * (p * values[1:] + (1 - p) * values[:-1])",
            "    if american:",
            "        ex = np.maximum(cp * (spots_n - K), 0.0)",
            "        values = np.where(ex > cont, ex, cont)",
            "    else:",
            "        values = cont",
            "return values[0]",
        ], source="explainer/quant/house/trees.py (crr, abridged)", width=7.6).to_edge(UP, buff=0.5)
        lab = t3["lab"]
        with self.voiceover(
            "The House's tree is one loop backwards from expiry, plus one line for chapter fourteen's American "
            f"option. <bookmark mark='a'/> Four steps: {lab['4']:.4f}. Sixty-four: {lab['64']:.4f}. Four hundred: "
            f"{lab['400']:.4f}; the formula, {t3['exact']:.4f}. Three roads, one formula."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"crr(100, 100, 1, 0.2, 0.05, N={n})  ->  {lab[str(n)]:.6f}" for n in (4, 64, 400)]
                    + [f"price(100, 100, 1, 0.2, 0.05)      ->  {t3['exact']:.6f}"])
            self.play(FadeIn(computed()))
        self.wait(0.4)
        self.clear_scene()
