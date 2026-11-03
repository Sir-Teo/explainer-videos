from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, illustration, load, pause


class Hawkes(VoiceoverScene):
    def construct(self):
        h = load("hawkes")
        hs = load("hawkes_sweep")
        self.card()
        self.flows(h)
        self.tree(hs)
        self.theory()
        self.zoomout(hs)
        self.sweep(hs)

    def card(self):
        c = chapter_card(9, r"Where roughness comes from", r"Why would volatility be rough?", lit=(2016,), part=PART)
        with self.voiceover("Chapter nine. Where roughness comes from: nearly unstable order flow."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def flows(self, h):
        grid = np.asarray(h["grid"])
        mid = 0.5 * (grid[1:] + grid[:-1])
        keys = ("0.5", "0.9", "0.99")
        cols = (VAR, IV, ROUGH)
        panels, lines = VGroup(), VGroup()
        tr = ValueTracker(0)
        for k, c in zip(keys, cols):
            y = np.asarray(h[k]["counts"], float)
            y = y / y.mean()
            g = axes([0, grid[-1]], [0, 12], x_length=10.4, y_length=1.5, xticks=[], yticks=[0, 6, 12], font_size=13)
            t = label(rf"branching ratio {k}: each trade triggers {float(k):g} more on average"
                      + (r" (nearly unstable)" if k == "0.99" else ""), font_size=19, color=c).next_to(g, UP, buff=0.05).align_to(g, LEFT)
            panels.add(VGroup(g, t))
            lines.add(tracing(g.ax, mid, np.minimum(y, 12), tr, c, stroke_width=1.6))
        panels.arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        foot = label(r"trading activity in equal time bins, relative to its average; every process has the same mean rate",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.7)
        src = illustration(r"Hawkes processes with exponential kernels (Part 5's simulator)")
        with self.voiceover(
            "Why would volatility be rough? Look at where it comes from: orders. Part five modelled order arrivals as "
            "a Hawkes process, in which every trade raises the chance of another. Here are three with the same "
            "average rate. When each trade triggers half a trade on "
            "average, activity is steady. <bookmark mark='a'/> At nine-tenths, it starts to cluster. "
            "<bookmark mark='b'/> At ninety-nine hundredths, the edge of instability, almost all activity is "
            "triggered by other activity: clusters inside clusters. Fitted to order flow, the branching ratio comes "
            "out close to one: most orders react to other orders."
        ) as vo:
            self.play(FadeIn(panels), FadeIn(src), FadeIn(foot), FadeIn(lines))
            self.play(tr.animate.set_value(len(mid) - 1), run_time=max(vo.remaining(0.0) - 1, 5), rate_func=linear)
        lines.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def tree(self, hs):
        t = np.asarray(hs["tree"]["t"])
        par = np.asarray(hs["tree"]["parent"], int)
        gen = np.asarray(hs["tree"]["gen"], int)
        G = int(min(gen.max(), 7))
        g = axes([0, 400], [-G - 0.5, 0.5], x_length=12.0, y_length=4.4, xlabel=r"time", xticks=[], yticks=[],
                 font_size=14).move_to(DOWN * 0.1)
        ax = g.ax
        keep = gen <= G
        pos = {i: ax.c2p(t[i], -gen[i]) for i in np.flatnonzero(keep)}
        cols = [interpolate_color(ManimColor(OPT), ManimColor(ROUGH), min(k / max(G, 1), 1)) for k in range(G + 1)]
        layers = []
        for k in range(G + 1):
            grp = VGroup()
            for i in np.flatnonzero(keep & (gen == k)):
                if par[i] >= 0 and par[i] in pos:
                    grp.add(Line(pos[par[i]], pos[i], stroke_color=GREY_C, stroke_width=1, stroke_opacity=0.6))
                grp.add(Dot(pos[i], radius=0.05, color=cols[k]))
            layers.append(grp)
        lab = VGroup(label(r"immigrants: orders from outside", font_size=18, color=OPT).next_to(ax.c2p(0, 0), RIGHT, buff=0.15),
                     label(r"each lower row: the children of the row above, at power-law delays", font_size=18,
                           color=GREY_A).next_to(g, DOWN, buff=0.15))  # under the axis label, above the source
        q = pause(r"Branching ratio 0.99: what share of trades are reactions to earlier trades?", width=5.6,
                  font_size=21).to_corner(UR, buff=0.3)
        src = illustration(rf"branching simulation, ratio 0.9, Lomax delays with tail $t^{{-1.6}}$; {int(keep.sum())} events")
        with self.voiceover(
            "Here is the same process as a family tree. Immigrants, the top row, are orders that arrive from outside. "
            "Each has children, reactions to it, after delays drawn from a heavy-tailed, power-law distribution; "
            "the children have children of their own. <bookmark mark='a'/> With a branching ratio of nine-tenths, "
            "a family averages ten members, spread over time scales from seconds to far later. "
            "<bookmark mark='b'/> Pause and predict: with a branching ratio of 0.99, what share of all trades are "
            "reactions to earlier trades? <bookmark mark='c'/> Ninety-nine percent. Each immigrant's family has a "
            "hundred members on average, and the families overlap at every scale."
        ) as vo:
            self.play(FadeIn(g), FadeIn(layers[0]), FadeIn(lab[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(L) for L in layers[1:]], lag_ratio=0.6, run_time=5), FadeIn(lab[1]))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(Indicate(q, color=YELLOW))
        self.wait(0.4)
        self.clear_scene()

    def theory(self):
        rows = [cmath(r"\lambda_t", r"=", r"\mu + \int_0^t \phi(t - s)\,dN_s", font_size=38, colors={r"\lambda_t": IV}),
                cmath(r"\mathbb{E}\lambda_t", r"=", r"\mu + \int_0^t \phi(t - s)\,\mathbb{E}\lambda_s\,ds", font_size=38,
                      colors={r"\mathbb{E}\lambda_t": IV}),
                cmath(r"\mathbb{E}\lambda_t", r"=", r"\mu\Big(1 + \int_0^t \psi\Big),\qquad \psi = \sum_{k \ge 1}\phi^{*k}",
                      font_size=38, colors={r"\mathbb{E}\lambda_t": IV}),
                cmath(r"\|\phi\|_1 \to 1,\ \phi(t) \sim t^{-(1 + \alpha)}", r"\Rightarrow",
                      r"\psi \to t^{\alpha - 1}E_{\alpha, \alpha}(-c\,t^\alpha)\ \sim\ t^{\alpha - 1}", font_size=34,
                      colors={r"\|\phi\|_1 \to 1,\ \phi(t) \sim t^{-(1 + \alpha)}": ROUGH}),
                cmath(r"\text{scaling limit}", r"=", r"\text{rough Heston},\quad H = \alpha - \tfrac12", font_size=38,
                      colors={r"\text{scaling limit}": ROUGH})]
        whys = [why(r"each event raises the intensity by the kernel $\phi$; $\|\phi\|_1$ is the branching ratio"),
                why(r"take expectations: $dN_s - \lambda_s ds$ is a martingale"),
                why(r"solve the renewal equation by its resolvent: $\phi^{*k}$ is generation $k$ of the family tree"),
                why(r"Laplace transforms: a heavy tail gives $1 - \hat\phi(z) \approx c z^\alpha$; rescaled, the resolvent "
                    r"is a Mittag-Leffler density, whose small-time behaviour is the fractional kernel"),
                why(r"Jaisson and Rosenbaum (2016): the rescaled intensity solves rough Heston's Volterra equation")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "Thibault Jaisson and Mathieu Rosenbaum made this precise in 2016. The intensity is a baseline mu plus "
            "the kernel phi applied to every past event. <bookmark mark='a'/> Take expectations: the expected "
            "intensity satisfies a renewal equation. <bookmark mark='b'/> Its solution is the baseline times one "
            "plus the integral of the resolvent psi, the sum of phi convolved with itself k times: generation k of "
            "the family tree. <bookmark mark='c'/> Now push the branching ratio to one, with a heavy power-law "
            "tail. In Laplace space the tail gives one minus phi hat of z close to a constant times z to the alpha. "
            "Rescale time, and the resolvent converges to a Mittag-Leffler density, which near zero behaves like t "
            "to the alpha minus one: the fractional kernel of rough Heston. <bookmark mark='d'/> The limit theorem: "
            "zoomed out, the intensity becomes a rough Heston variance with H equal to alpha minus a half."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()

    def zoomout(self, hs):
        c = np.asarray(hs["counts_9999"], float)
        n = len(c)
        y = np.log(np.maximum(c, 1))
        s = ValueTracker(0.0)
        frame = Rectangle(width=11.6, height=3.6, stroke_color=GREY_D, stroke_width=1.5).move_to(DOWN * 0.2)

        def make():
            span = max(int(200 * (n / 200) ** s.get_value()), 50)
            seg = y[:span]
            idx = np.linspace(0, span - 1, min(span, 800)).astype(int)
            z = seg[idx]
            z = (z - z.min()) / max(z.max() - z.min(), 1e-9)
            pts = [frame.get_corner(DL) + RIGHT * (0.1 + 11.4 * a) + UP * (0.1 + 3.4 * b)
                   for a, b in zip(np.linspace(0, 1, len(z)), z)]
            return VMobject(stroke_color=ROUGH, stroke_width=1.5).set_points_as_corners(pts)

        line = always_redraw(make)
        cap = label(r"log activity of a nearly unstable Hawkes process (ratio 0.9999), from 200 bins to 20{,}000",
                    font_size=20, color=GREY_A).next_to(frame, UP, buff=0.2)
        src = illustration(r"power-law kernel, simulated by branching: 4 million time units, bins of 200")
        with self.voiceover(
            "Watch the limit happen. This is the log of trading activity in a Hawkes process with a branching "
            "ratio of 0.9999, first over two hundred bins. Zoom out to twenty thousand bins, rescaling as we go. "
            "The curve does not smooth into a line: it stays jagged at every scale, like the rough path of the "
            "hook."
        ):
            self.play(FadeIn(frame), FadeIn(cap), FadeIn(line), FadeIn(src))
            self.play(s.animate.set_value(1.0), run_time=7, rate_func=linear)
        line.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def sweep(self, hs):
        sw = hs["sweep"]
        ns = [r["n"] for r in sw]
        g = axes([-0.5, len(ns) - 0.5], [-0.02, 0.45], x_length=6.0, y_length=4.0, xlabel=r"branching ratio",
                 ylabel=r"estimated $H$ of log activity", xticks=list(range(len(ns))),
                 xfmt=lambda u: f"{ns[int(round(u))]:g}", yticks=[0, 0.1, 0.2, 0.3, 0.4], font_size=15).to_edge(LEFT, buff=0.7)
        ax = g.ax
        pts = VGroup()
        for i, r in enumerate(sw):
            for h in r["H"]:
                pts.add(Dot(ax.c2p(i, h), radius=0.06, color=ROUGH))
        mean = curve(ax, np.arange(len(ns)), [np.mean(r["H"]) for r in sw], ROUGH, stroke_width=2.5)
        tl = hs["tails"]
        tab = VGroup(VGroup(label(r"tail $\alpha$", font_size=18, color=GREY_A), label(r"theory $\alpha - \tfrac12$", font_size=18,
                                                                                     color=GREY_A),
                            label(r"estimated (3 seeds)", font_size=18, color=GREY_A)))
        for r in tl:
            tab.add(VGroup(MathTex(f"{r['alpha']:g}", font_size=24), MathTex(f"{r['theory']:.2f}", font_size=24),
                           MathTex(f"{min(r['H']):.2f}\\text{{--}}{max(r['H']):.2f}", font_size=24, color=ROUGH)))
        grid = VGroup(*[c for row in tab for c in row]).arrange_in_grid(rows=len(tab), cols=3, buff=(0.4, 0.2))
        grid.to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
        cards = VGroup(
            wrapped_label(r"El Euch, Fukasawa and Rosenbaum (2018): add no-arbitrage at high frequency and buy/sell "
                          r"asymmetry, and the limit carries a leverage effect, $\rho < 0$", 5.2, 18, GREY_A),
            wrapped_label(r"Jusselin and Rosenbaum (\textit{Rough Volatility}, ch. 3): no-arbitrage implies power-law "
                          r"market impact and rough volatility (impact: Part 37)", 5.2, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(grid, DOWN, buff=0.4).to_edge(RIGHT, buff=0.35)
        lo = np.mean(sw[0]["H"])
        hi = max(np.mean(r["H"]) for r in sw)
        src = illustration(r"the House's \texttt{hawkes\_branching\_powerlaw}; the roughness estimator on log activity in "
                           r"bins of 200", corner=DL)
        with self.voiceover(
            "Can we measure it? Simulate order flow by branching and run chapter three's estimator on log activity, "
            "three seeds per ratio. <bookmark mark='a'/> At a ratio of "
            f"one half, activity is not rough at all: H of {lo:.2f}, essentially noise. As the ratio approaches one, "
            f"roughness emerges: close to one the estimate reaches about {hi:.2f}. <bookmark mark='b'/> But the theory says "
            "more: H should equal the tail exponent minus a half. Change the tail, and the finite simulation does "
            "not follow; every tail reads about a tenth. The limit theorem needs the branching ratio to reach one "
            "and the horizon to grow together, and a finite sample shows the emergence of roughness, not its "
            "exact value. <bookmark mark='c'/> Omar El Euch, Masaaki Fukasawa and Rosenbaum showed no-arbitrage also "
            "forces the leverage effect, and Paul Jusselin and Rosenbaum tied rough volatility to power-law market "
            "impact. Roughness, on this account, is reactive order flow seen from a distance."
            " Many time scales at once can also be built directly. Next: Markovian lifts."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.1), Create(mean))
            vo.wait_until("b")
            self.play(FadeIn(grid))
            vo.wait_until("c")
            self.play(FadeIn(cards))
        self.wait(0.4)
        self.clear_scene()
