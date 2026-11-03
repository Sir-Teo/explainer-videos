from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import quoting as Q
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load, pause


class Hedging(VoiceoverScene):
    def construct(self):
        gh = load("greekhedge")
        self.card()
        self.greek_space(gh)
        self.derive(gh)
        self.heston(gh)
        self.buckets(load("buckets"))
        self.band()
        self.frontier(load("hedging"), load("hedging_replay"))

    def card(self):
        c = chapter_card(10, r"Hedging the book", r"What does the underlying not hedge?", part=PART)
        with self.voiceover("Chapter ten. Hedging the book: gamma and vega with other options, and hedging under costs."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def greek_space(self, gh):
        b, a7, a60, sol = gh["book"], gh["i7"], gh["i60"], gh["sol"]
        sx, sy = 100.0, 10.0                     # display units: gamma x 100, vega per vol point x 10
        P = lambda d: np.array([d["gamma"] * sx, d["vega"] / 100 * sy, 0.0])  # noqa: E731
        g = axes([-7, 7], [-3, 3], x_length=8.0, y_length=4.6, xlabel=r"gamma ($\times 100$)",
                 ylabel=r"vega per vol point ($\times 10$)", xticks=[-6, 0, 6], yticks=[-2, 0, 2], font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        o = ax.c2p(0, 0)
        u = lambda v: ax.c2p(v[0], v[1]) - o  # noqa: E731
        book = Arrow(o, o + u(P(b)), buff=0, color=QC.LOSS, stroke_width=6)
        e7 = Arrow(o, o + u(P(a7)), buff=0, color=GAMMA, stroke_width=4)
        e60 = Arrow(o, o + u(P(a60)), buff=0, color=VEGA, stroke_width=4)
        tip = o + u(P(b))
        h7 = Arrow(tip, tip + u(P(a7)) * sol["n1"], buff=0, color=GAMMA, stroke_width=6)
        h60 = Arrow(h7.get_end(), h7.get_end() + u(P(a60)) * sol["n2"], buff=0, color=VEGA, stroke_width=6)
        labs = VGroup(label(r"the book: short a 30-day straddle", font_size=18, color=QC.LOSS).next_to(book.get_end(), UP, buff=0.3),  # the hedges start below it
                      label(r"a 7-day option: mostly gamma", font_size=18, color=GAMMA).next_to(e7.get_end(), DOWN, buff=0.2).align_to(e7.get_end(), RIGHT),
                      label(r"a 60-day option: mostly vega", font_size=18, color=VEGA).next_to(e60.get_end(), UP, buff=0.08))
        side = VGroup(
            MathTex(rf"n_7 = {sol['n1']:+.2f},\quad n_{{60}} = {sol['n2']:+.2f}", font_size=30),
            MathTex(rf"\text{{then shares: }} {sol['shares']:+.2f}", font_size=30, color=QC.DELTA),
            wrapped_label(r"two options span the plane: their arrows, scaled and laid tip to tail, carry the book back "
                          r"to the origin; the stock, which has no gamma and no vega, takes care of delta last", 4.2, 19,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"spot 100, 50\% vol; options at the money; per unit of each")
        with self.voiceover(
            "The underlying hedges delta and nothing else. To hedge gamma and vega, a desk trades other options. "
            "Picture the book as an arrow in Greek space, gamma across and vega up: a short straddle points down and "
            "left. <bookmark mark='a'/> Each option the desk could "
            "trade is another arrow: a seven-day option is nearly all gamma, a sixty-day one mostly vega. <bookmark mark='b'/> So "
            f"scale them, {sol['n1']:.2f} of the short one and {sol['n2']:.2f} of the long one, and lay them tip to "
            "tail: they carry the book's arrow exactly back to the origin. <bookmark mark='c'/> Only then trade the "
            "underlying, for the delta that is left."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), GrowArrow(book), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(GrowArrow(e7), GrowArrow(e60), FadeIn(labs[1]), FadeIn(labs[2]))
            vo.wait_until("b")
            self.play(GrowArrow(h7), run_time=1.2)
            self.play(GrowArrow(h60), FadeIn(side[0]), run_time=1.2)
            self.play(Flash(o, color=YELLOW))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self, gh):
        rows = [
            cmath(r"\begin{pmatrix}\Gamma_1 & \Gamma_2\\ \mathcal{V}_1 & \mathcal{V}_2\end{pmatrix}"
                  r"\begin{pmatrix}n_1\\ n_2\end{pmatrix}", r"=", r"-\begin{pmatrix}\Gamma_B\\ \mathcal{V}_B\end{pmatrix}",
                  font_size=36),
            cmath(r"n_0", r"=", r"-\left(\Delta_B + n_1\Delta_1 + n_2\Delta_2\right)", font_size=36,
                  colors={r"n_0": QC.DELTA}),
            cmath(r"\frac{\mathcal{V}}{\Gamma}", r"=", r"\sigma\,\tau\,S^2", font_size=40),
        ]
        whys = [why(r"zero the book's gamma and vega with two options: a two-by-two linear system, solvable when the "
                    r"two options have different vega-to-gamma ratios"),
                why(r"then the shares: the stock has delta one and no other Greek, so it goes last"),
                why(r"chapter 1's identity: an option's vega-to-gamma ratio grows with its time to expiry, so short and "
                    r"long expiries are independent hedges")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-0.4, buff=0.55, edge=6.9)  # ends higher: the card fits below
        pc = pause(r"You must kill your gamma but keep your vega. Trade short-dated options or long-dated ones?",
                   width=5.4, font_size=21)
        with self.voiceover(
            "In symbols, a two by two system: amounts of two options whose gammas and vegas cancel the book's. "
            "<bookmark mark='a'/> Then the shares, last, because the stock has a delta of one and no other Greek. "
            "<bookmark mark='b'/> It is solvable when the two options have different ratios of vega to gamma, and "
            "chapter one's identity says that ratio grows with the expiry. "
            "<bookmark mark='c'/> Pause and predict: you must kill your gamma but keep your vega. Short-dated or "
            "long-dated options? Short-dated: they carry gamma cheaply, with little vega attached."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heston(self, gh):
        sims = gh["sims"]
        rules = [("delta", r"delta only", GREY_B), ("delta-gamma", r"+ gamma (7-day)", GAMMA),
                 ("delta-gamma-vega", r"+ vega (60-day)", VEGA)]
        top = max(v["sd"] for d in sims.values() for v in d.values()) * 1.2
        g = axes([0, 7], [0, top], x_length=7.4, y_length=4.2, ylabel=r"s.d.\ of the hedged book's P\&L, per 100",
                 yticks=[0, 1, 2], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for k, (model, x0) in enumerate((("GBM", 0.4), ("Heston", 3.9))):
            for j, (r_, txt, c) in enumerate(rules):
                v = sims[model][r_]["sd"]
                a, b = ax.c2p(x0 + j + 0.4, 0), ax.c2p(x0 + j + 0.4, v)
                bars.add(Rectangle(width=0.7, height=max(b[1] - a[1], 0.01), stroke_width=0, fill_color=c,
                                   fill_opacity=0.85).move_to((a + b) / 2))
                labs.add(MathTex(f"{v:.2f}", font_size=22, color=c).next_to(bars[-1], UP, buff=0.06))
            labs.add(label(r"constant volatility" if model == "GBM" else r"stochastic volatility (Heston)",
                           font_size=18, color=GREY_A).next_to(ax.c2p(x0 + 1.5, 0), DOWN, buff=0.15))
        leg = legend([(c, t) for _, t, c in rules], font_size=18).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
        G, H = sims["GBM"], sims["Heston"]
        cut_g = 1 - G["delta-gamma"]["sd"] / G["delta"]["sd"]
        cut_h = 1 - H["delta-gamma-vega"]["sd"] / H["delta-gamma"]["sd"]
        side = VGroup(
            wrapped_label(rf"constant vol: the gamma hedge removes {100 * cut_g:.0f}\% of the risk, and a vega hedge "
                          r"has nothing left to do", 4.0, 20, GAMMA),
            wrapped_label(rf"stochastic vol: after the gamma hedge, the vega hedge removes {100 * cut_h:.0f}\% of what "
                          r"is left", 4.0, 20, VEGA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"simulated: 10{,}000 paths, a short 30-day straddle, rehedged 4 times a day; every option "
                           r"marked at Black--Scholes with the current volatility")
        hsay = (f"Once volatility moves, the vega hedge earns its place: it removes {100 * cut_h:.0f} percent of what the "
                "gamma hedge left." if cut_h > 0.3 else
                f"Even with volatility moving, the vega hedge removes only {100 * cut_h:.0f} percent more.")
        with self.voiceover(
            "Does it work? Simulate a short straddle on ten thousand paths, hedged three ways: delta only; adding "
            "gamma with a seven-day option; adding vega with a sixty-day option. <bookmark mark='a'/> When volatility is constant, the delta hedge alone leaves a "
            f"standard deviation of {G['delta']['sd']:.2f}, the discrete-hedging error of Part ten. The gamma hedge "
            f"removes {100 * cut_g:.0f} percent of it, and vega has nothing to add. <bookmark mark='b'/> Now let "
            "volatility itself wander, as in Heston's model. Delta alone leaves "
            f"{H['delta']['sd']:.2f}, the gamma hedge {H['delta-gamma']['sd']:.2f}. {hsay}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            for j in range(3):
                self.play(GrowFromEdge(bars[j], DOWN), FadeIn(labs[j]), run_time=0.7)
            self.play(FadeIn(labs[3]), FadeIn(side[0]))
            vo.wait_until("b")
            for j in range(3):
                self.play(GrowFromEdge(bars[3 + j], DOWN), FadeIn(labs[4 + j]), run_time=0.7)
            self.play(FadeIn(labs[7]), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def buckets(self, bk):
        exps = np.asarray(bk["buckets"])
        vb, va, mv = np.asarray(bk["vega_by"]), np.asarray(bk["vega_after"]), np.asarray(bk["move"])
        lim = max(np.abs(vb).max(), np.abs(va).max()) * 1.2
        g = axes([0, 5], [-lim, lim], x_length=6.4, y_length=3.8, ylabel=r"vega per vol point, by expiry",
                 yticks=[-0.4, 0, 0.4], font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        z = Line(ax.c2p(0, 0), ax.c2p(5, 0), color=GREY_C)

        def bars(v, c, op):
            gr = VGroup()
            for j, x in enumerate(v):
                a, b = ax.c2p(j + 0.5, 0), ax.c2p(j + 0.5, x)
                gr.add(Rectangle(width=0.6, height=max(abs(b[1] - a[1]), 0.01), stroke_width=0, fill_color=c,
                                 fill_opacity=op).move_to((a + b) / 2))
            return gr
        b0 = bars(vb, VEGA, 0.85)
        b1 = bars(va, VEGA, 0.85)
        names = VGroup(*[label(f"{int(e)}d", font_size=17, color=GREY_A).next_to(ax.c2p(j + 0.5, -lim), DOWN, buff=0.08)
                         for j, e in enumerate(exps)])
        mvl = VGroup(*[MathTex(f"{m:+.1f}", font_size=20, color=ALT).next_to(ax.c2p(j + 0.5, -lim), UP, buff=0.05)
                       for j, m in enumerate(mv)])
        side = VGroup(
            label(rf"total vega: {vb.sum():+.2f} $\to$ {va.sum():+.2f}", font_size=22, color=VEGA),
            label(r"a steepening: the short end up, the long end down (gold, vol points)", font_size=19, color=ALT),
            label(rf"P\&L: {bk['before']:+.2f} unhedged, {bk['after']:+.2f} after the parallel hedge", font_size=21,
                  color=QC.LOSS),
            wrapped_label(r"Taleb's point in \textit{Dynamic Hedging}: a book flat in total vega is not flat; hedge "
                          r"vega bucket by bucket", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        src = illustration(r"a book of options at five expiries; vega per option on 100, 50\% vol")
        with self.voiceover(
            "One vega number hides the term structure. Here is a book's vega by expiry bucket. <bookmark mark='a'/> A desk can zero the total with a single "
            "ninety-day option: the parallel hedge. <bookmark mark='b'/> Now let the term structure steepen, the short "
            "end up four points and the long end down one and a half. The book flat in total vega loses "
            f"{-bk['after']:.2f}, barely less than the {-bk['before']:.2f} it lost unhedged. Nassim Taleb's lesson in "
            "Dynamic Hedging: hedge vega by bucket."
        ) as vo:
            self.play(FadeIn(g), Create(z), FadeIn(names), FadeIn(src), LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in b0],
                                                                                       lag_ratio=0.2, run_time=2))
            vo.wait_until("a")
            self.play(Transform(b0, b1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(mvl), FadeIn(side[1]))
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def band(self):
        S = np.linspace(70, 130, 121)
        b = Q.ww_band(S, 100.0, 15 / 365, 0.6, 0.001, gamma_risk=1.0)
        g = axes([70, 130], [-0.05, 1.05], x_length=6.0, y_length=3.6, xlabel=r"underlying", ylabel=r"hedge, units held "
                 r"(short call)", xticks=[70, 85, 100, 115, 130], yticks=[0, 0.5, 1], font_size=16)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.6)
        ax = g.ax
        band = Polygon(*[ax.c2p(x, y) for x, y in zip(S, np.clip(b["hi"], -0.05, 1.05))],
                       *[ax.c2p(x, y) for x, y in zip(S[::-1], np.clip(b["lo"][::-1], -0.05, 1.05))], stroke_width=0,
                       fill_color=VEGA, fill_opacity=0.3)
        mid = curve(ax, S, b["delta"], OPT, stroke_width=3)
        card = lab_card(r"the no-trade band", [
            "def ww_band(S, K, T, sigma, cost, gamma_risk=1.0, r=0.0, cp=1):",
            "    g = bs.greeks(S, K, T, sigma, r, 0.0, cp)",
            "    h = (1.5 * cost * S * g[\"gamma\"] ** 2 * np.exp(-r * T)",
            "         / gamma_risk) ** (1 / 3)",
            "    return {\"delta\": g[\"delta\"], \"lo\": g[\"delta\"] - h,",
            "            \"hi\": g[\"delta\"] + h, \"half_width\": h}",
        ], source="explainer/quant/house/quoting.py", width=6.4, font_size=17).to_edge(RIGHT, buff=0.3).to_edge(UP, buff=0.35)
        hw = {x: float(Q.ww_band(x, 100.0, 15 / 365, 0.6, 0.001)["half_width"]) for x in (90.0, 100.0, 110.0)}
        eq = MathTex(r"\Delta \pm \left(\frac{3\,\lambda\, S\,\Gamma^2}{2\,\gamma}\right)^{1/3}", font_size=34,
                     color=VEGA).to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.8)
        src = illustration(r"a 15-day call, 60\% vol, 10 bp cost, $\gamma = 1$")
        with self.voiceover(
            "Hedging costs money. Vlad Whalley and Paul Wilmott found the answer in 1997: a band around delta. Inside it, do nothing; when "
            "the hedge drifts out, trade only back to the band's edge. <bookmark mark='a'/> Its half-width is the cube "
            "root of the cost times gamma squared over the risk aversion, the House's ww band. Run it fifteen days "
            f"from expiry: {hw[90.0]:.3f} at ninety, {hw[100.0]:.3f} at the strike, {hw[110.0]:.3f} at a hundred and ten. "
            "<bookmark mark='b'/> Widest at the strike, where delta moves fastest and chasing it would cost the most. "
            ""
        ) as vo:
            self.play(FadeIn(g), Create(mid), FadeIn(src), FadeIn(eq), FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, ["ww_band(S, 100, 15/365, 0.6, 0.001)",
                                 "   ".join(f"S={int(x)}: {v:.3f}" for x, v in hw.items())], font_size=17)
            vo.wait_until("b")
            self.play(FadeIn(band))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self, h, hr):
        runs = hr["runs"]
        steps = np.asarray(hr["steps"], float)
        L = np.array([runs[f"1-{s}"]["loss"] for s in range(3)])
        gaps = np.asarray(hr["gaps"])

        def frame(i):
            c = str(hr["checkpoints"][i])
            a = axes([-0.3, 0.3], [0, 1], x_length=4.0, y_length=2.6, xlabel=r"hedge minus delta",
                     ylabel=r"share of the gap closed", xticks=[-0.3, 0, 0.3], yticks=[0, 1], font_size=14)
            return VGroup(a, curve(a.ax, gaps, np.asarray(runs["1-0"]["snaps"][c]), GAMMA, stroke_width=3))
        rp = TrainingReplay(steps, L, frame, hr["checkpoints"], ylabel=r"variance $+\ \kappa\cdot$cost ($\kappa = 1$)",
                            xlabel=r"training step", color=GAMMA, left=LEFT * 3.6 + DOWN * 0.2,
                            right=RIGHT * 3.0 + DOWN * 0.2, x_length=5.2, y_length=3.2)
        with self.voiceover(
            "Can a network learn the band without being told it exists? Deep hedging, from Hans Bühler and his "
            "coauthors, trains a small network to choose, at each step, how far to move the hedge toward delta, "
            "through the simulator, minimizing the variance of the profit plus a price kappa on costs. "
            "<bookmark mark='a'/> Watch it learn, three seeds as a band. On the left, the policy it has learned at the "
            "middle of the option's life: the share of the gap to delta it closes, against the size of the gap. It "
            "starts flat, and learns to leave small gaps alone and close large ones: a soft band."
        ) as vo:
            self.play(FadeIn(rp))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(1.0) - 0.5, 4.0))
        self.wait(0.4)
        self.clear_scene()
        self.cost_risk(h, hr)

    def cost_risk(self, h, hr):
        rows = h["rows"]
        g = axes([0.15, 0.5], [0.5, 1.5], x_length=6.6, y_length=4.4, xlabel=r"average trading cost (per 100)",
                 ylabel=r"spread of hedged P\&L (s.d.)", xticks=[0.2, 0.3, 0.4, 0.5], yticks=[0.5, 0.75, 1.0, 1.25, 1.5],
                 font_size=17).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        groups = {"every step": GREY_B, "fixed band": ALT, "Whalley-Wilmott": VEGA}
        dots, lines = VGroup(), VGroup()
        for name, col in groups.items():
            pts = sorted([(r_["cost"], r_["sd"]) for r_ in rows if r_["rule"] == name and np.isfinite(r_["sd"])])
            if name == "fixed band":
                pts = sorted(pts + [(r_["cost"], r_["sd"]) for r_ in rows if r_["rule"] == "every step"])
            pts = [p for p in pts if 0.15 <= p[0] <= 0.5 and p[1] <= 1.5]
            dots.add(VGroup(*[Dot(ax.c2p(*p), radius=0.07, color=col) for p in pts]))
            lines.add(VMobject(stroke_color=col, stroke_width=2.5).set_points_as_corners([ax.c2p(*p) for p in pts])
                      if len(pts) > 1 else VGroup())
        deep = VGroup()
        pts = [(r_["cost"], r_["sd"]) for r_ in rows if r_["rule"] == "deep hedge"]
        pts += [(r_["cost"], r_["sd"]) for r_ in hr["runs"].values()]
        for c_, s_ in pts:
            if 0.15 <= c_ <= 0.5 and s_ <= 1.5:
                deep.add(Dot(ax.c2p(c_, s_), radius=0.06, color=GAMMA))
        leg = legend([(GREY_B, r"rehedge every 6 hours"), (ALT, r"fixed bands"), (VEGA, r"Whalley--Wilmott bands"),
                      (GAMMA, r"deep hedger: 3 cost weights, and 3 seeds at $\kappa = 1$")], font_size=17)
        leg.move_to(ax.c2p(0.32, 1.32)).align_to(ax.c2p(0.24, 0), LEFT)
        side = VGroup(
            wrapped_label(r"each point: a short 30-day option on 20{,}000 simulated paths (5{,}000 held out for the "
                          r"learner), costs of 10 bp; lower and to the left is better", 4.2, 19, GREY_A),
            wrapped_label(r"the simple Whalley--Wilmott band is hard to beat; the learner lands close to its curve "
                          r"without being told the shape of the answer. Part 17 takes it further", 4.2, 19, GAMMA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = illustration(r"geometric Brownian motion at 60\%; 120 rebalancing points")
        with self.voiceover(
            "The scoreboard: risk against cost on the same paths, lower left is better. Rehedging every six hours "
            "is safest and dearest; the Whalley-Wilmott bands trace the better curve. <bookmark mark='a'/> The deep hedger, at three cost weights, "
            "with three seeds at the first, lands close to that curve, without being told what a band is. The classical answer was "
            "already very good; the learner's value is that it scales to books with no formula, Part seventeen."
            " Every option eventually expires. Next: what happens on that day."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[:3]), FadeIn(side[0]), FadeIn(src), FadeIn(dots), Create(lines[1]),
                      Create(lines[2]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(leg[3]), FadeIn(deep), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()
