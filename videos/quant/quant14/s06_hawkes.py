from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import axes, data_range, skew_range
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
            g = axes([0, grid[-1]], [0, max(12, float(y.max()) * 1.05)], x_length=10.4, y_length=1.5, xticks=[], yticks=[0, 6, 12], font_size=13)
            t = label(rf"branching ratio {k}: each trade triggers {float(k):g} more on average"
                      + (r" (nearly unstable)" if k == "0.99" else ""), font_size=19, color=c).next_to(g, UP, buff=0.05).align_to(g, LEFT)
            panels.add(VGroup(g, t))
            lines.add(tracing(g.ax, mid, y, tr, c, stroke_width=1.6))
        panels.arrange(DOWN, buff=0.35).move_to(UP * 0.2)
        foot = label(r"trading activity in equal time bins, relative to its average; every process has the same mean rate",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.7)
        src = illustration(r"Hawkes processes with exponential kernels (Part 5's simulator)")
        with self.voiceover(
            """Hawkes models illustrate reactive order arrivals. Each event temporarily raises the conditional arrival intensity. The three exponential-kernel examples set baselines for the same stationary mean rate, then normalize each finite sample by its own mean. <bookmark mark='a'/> A branching ratio of nine tenths produces stronger clustering than one half in these examples. <bookmark mark='b'/> Near one, families can become large. This is a synthetic activity illustration, not a fitted empirical branching estimate or proof of rough volatility. Heavy-tailed kernels and a carefully coordinated nearly critical limit enter next."""
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
            """Now a branching representation with a heavy-tailed Lomax delay kernel, rather than the preceding exponential kernel. Immigrants trigger children, which trigger further generations. <bookmark mark='a'/> At branching ratio nine tenths, a stationary immigrant family has ten members on average before finite-horizon truncation. <bookmark mark='b'/> At ratio point nine nine, what share of stationary events are descendants rather than immigrants? <bookmark mark='c'/> Ninety-nine percent, with one hundred members per family on average. The displayed finite tree retains only the shown generations and horizon; these stationary expectations are not exact counts in its picture."""
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
                cmath(r"\text{joint scaling},\quad 1/2<\alpha<1", r"\Rightarrow",
                      r"\psi_{\rm scaled}(t) \to c_1t^{\alpha-1}E_{\alpha,\alpha}(-c_2t^\alpha)", font_size=34,
                      colors={r"\text{joint scaling},\quad 1/2<\alpha<1": ROUGH}),
                cmath(r"\text{scaling limit}", r"=", '\\text{integrated fractional CIR},\\quad H=\\alpha-\\tfrac12', font_size=38,
                      colors={r"\text{scaling limit}": ROUGH})]
        whys = [why(r"each event raises the intensity by the kernel $\phi$; $\|\phi\|_1$ is the branching ratio"),
                why(r"take expectations: $dN_s - \lambda_s ds$ is a martingale"),
                why(r"solve the renewal equation by its resolvent: $\phi^{*k}$ is generation $k$ of the family tree"),
                why('Under the coordinated scaling: a Mittag--Leffler resolvent density; as $t\\downarrow0$ it is proportional to $t^{\\alpha-1}$. Constants depend on the scaling.'),
                why('Jaisson--Rosenbaum: a coordinated nearly critical heavy-tail scaling gives an integrated fractional-CIR limit, $1/2<\\alpha<1$')]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            """Start with Hawkes intensity: a baseline plus past events weighted by a kernel. <bookmark mark='a'/> Taking expectations gives a renewal equation. <bookmark mark='b'/> Its resolvent is the sum of convolution powers, one for each generation. <bookmark mark='c'/> Jaisson and Rosenbaum take a heavy-tail parameter alpha between one half and one, with a nearly critical branching sequence and coordinated time, baseline and amplitude scaling. The rescaled resolvent approaches a Mittag--Leffler density, proportional to t to alpha minus one near zero. <bookmark mark='d'/> Their 2016 theorem yields an integrated fractional-CIR limit with H equal to alpha minus one half. A price process and leverage require further modeling assumptions. The preceding finite simulations do not implement this entire limiting sequence."""
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
            """A finite-scale illustration, not a limit theorem in motion. We show log binned counts from one Hawkes simulation with branching ratio point nine nine nine nine. Zero counts are floored at one before taking logs. As the displayed horizon grows from two hundred to twenty thousand bins, each segment is independently range-normalized and downsampled. The remaining irregularity is a visual feature of this one realization. The theorem requires a jointly rescaled sequence of processes, baselines and horizons; this animation does not implement that sequence."""
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
            f"""Apply the same finite-lag estimator to log binned activity, with three fixed seeds per branching ratio. <bookmark mark='a'/> At ratio one half the estimate averages {lo:.2f}, close to lag-independent count noise. The largest mean in this sweep is {hi:.2f}. A higher H here means a steeper finite-lag moment slope, not greater local roughness. <bookmark mark='b'/> The tail sweep does not track the limiting formula: all three tails read near one tenth. Jaisson and Rosenbaum's theorem requires tail parameter alpha between one half and one, a nearly critical branching sequence, and coordinated time, baseline and amplitude scaling. It yields an integrated fractional-CIR limit with H equal to alpha minus one half. These fixed finite simulations do not test all those hypotheses. <bookmark mark='c'/> Multivariate extensions connect suitable buy-sell asymmetry and no-arbitrage assumptions to leverage; further market-impact models link reactive flow to rough limits. These are model-based mechanisms, not a universal inference from observed clustering. Next: Markovian lifts."""
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
