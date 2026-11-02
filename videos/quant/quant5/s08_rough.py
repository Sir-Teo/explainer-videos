from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, real_data


class Rough(VoiceoverScene):
    def construct(self):
        fm = load("fbm_morph")
        r = load("rough")
        cd = load("cont_das")
        self.card()
        self.dial(fm)
        self.theory(fm)
        self.lab()
        self.bitcoin(r)
        self.caveat(cd, r)

    def card(self):
        c = chapter_card(15, r"Fractional Brownian motion: memory and roughness", r"How rough is volatility?", lit=(1963,),
                         part=PART)
        with self.voiceover("Chapter fifteen. Fractional Brownian motion: memory, roughness, and a caveat."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def dial(self, fm):
        Hs = [f"{h:.2f}" for h in fm["Hs"]]
        P = {k: np.asarray(v) for k, v in fm["paths"].items()}
        t = np.linspace(0, 1, len(P[Hs[0]]))
        order = [k for k in reversed(Hs)]

        def norm_(y):
            return (y - y.mean()) / (y.std() + 1e-12)
        g = axes([0, 1], [-3.2, 3.2], x_length=10.0, y_length=4.0, xlabel=r"time", xticks=[0, 1], yticks=[],
                 font_size=16).shift(DOWN * 0.6)
        ax = g.ax
        lines = {k: curve(ax, t, np.clip(norm_(P[k]), -3.2, 3.2), interpolate_color(ManimColor(JUMP), ManimColor(DRIFT),
                                                                                    float(k)), stroke_width=2)
                 for k in Hs}
        lines["0.50"].set_color(BM)
        lab = {k: VGroup(MathTex(rf"H = {k}", font_size=36), MathTex(rf"\rho(1) = 2^{{2H - 1}} - 1 = "
                                                                     rf"{fm['rho1'][k]:+.2f}", font_size=30,
                                                                     color=GREY_A)).arrange(RIGHT, buff=0.6)
               .to_edge(UP, buff=0.5) for k in Hs}
        cap = label(r"one fixed vector of Gaussian numbers, turned into fBM by Davies--Harte at each $H$", font_size=20,
                    color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Brownian increments are independent. In 1968 Benoit Mandelbrot and John Van Ness generalised them: "
            "fractional Brownian motion, whose increments over a lag have variance equal to the lag to the power two "
            "H. <bookmark mark='a'/> Here is one path, built from the same random numbers at every H, as a dial turns "
            "H down from point nine five. <bookmark mark='b'/> At high H the increments are positively correlated and "
            "the path trends. At a half, highlighted, it is Brownian motion. Below a half, neighbouring increments "
            "are negatively correlated, and the path becomes a jagged scrawl."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cap), Create(lines[order[0]]), FadeIn(lab[order[0]]))
            vo.wait_until("a")
            cur, cl = lines[order[0]], lab[order[0]]
            for k in order[1:]:
                self.play(Transform(cur, lines[k]), Transform(cl, lab[k]), run_time=0.45 if k != "0.50" else 0.8)
                if k == "0.50":
                    vo.wait_until("b")
                    self.play(Indicate(cur, color=BM), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def theory(self, fm):
        rows = [cmath(r"\mathbb{E}\big[B^H_t B^H_s\big]", r"=", r"\tfrac12\big(t^{2H} + s^{2H} - |t - s|^{2H}\big)", font_size=32),
                cmath(r"B^H_t", r"=", r"\frac{1}{\Gamma(H + \frac12)}\int_{\mathbb{R}} \Big[(t - s)_+^{H - \frac12} - (-s)_+^{H - "
                      r"\frac12}\Big]\,dW_s", font_size=30, colors={r"(t - s)_+^{H - \frac12}": ITO}),
                cmath(r"\mathbb{E}\sum_{k < n} \big|B^H_{(k+1)/n} - B^H_{k/n}\big|^2", r"=", r"n \cdot n^{-2H} = n^{1 - 2H}",
                      font_size=30, colors={r"n^{1 - 2H}": JUMP}),
                cmath(r"H \ne \tfrac12", r"\Rightarrow", r"B^H \text{ is not a semimartingale}", font_size=32)]
        whys = [why(r"the definition: Gaussian, stationary increments, self-similar with index $H$", 20),
                why(r"Mandelbrot and Van Ness (1968): Brownian motion with a power-law memory kernel", 20),
                why(r"self-similarity: $\to \infty$ for $H < \frac12$, $\to 0$ for $H > \frac12$", 20),
                why(r"a semimartingale's QV is finite; QV zero means finite variation, which fails for $H > \frac12$ by "
                    r"the $1/H$-variation (Rogers 1997: a price driven by it admits arbitrage)", 20)]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=-2.0, buff=0.45, edge=6.9)
        ns = np.log2(fm["ns"])
        g = axes([ns[0] - 0.3, ns[-1] + 0.3], [-1.6, 1.6], x_length=4.4, y_length=2.4, xlabel=r"grid $n$",
                 ylabel=r"$\log_{10}\mathbb{E}\sum|\Delta B^H|^2$", xticks=[4, 8, 12], xfmt=lambda u: rf"2^{{{int(u)}}}",
                 yticks=[-1, 0, 1], font_size=14).to_corner(DR, buff=0.3)
        cols = {"0.3": JUMP, "0.5": BM, "0.7": DRIFT}
        lines = VGroup(*[curve(g.ax, ns, np.log10(fm["pvar"][k]), cols[k], stroke_width=3) for k in ("0.3", "0.5", "0.7")])
        leg = legend([(JUMP, r"$H = 0.3$"), (BM, r"$H = 0.5$"), (DRIFT, r"$H = 0.7$")], font_size=16).next_to(g, LEFT,
                                                                                                        buff=0.2)
        pc, ans = pause(r"$H = 0.1$. Is a rise more likely to be followed by a fall?",
                        rf"Yes: $\rho(1) = 2^{{-0.8}} - 1 = {fm['rho1']['0.10']:.2f}$.", width=4.6, font_size=19)
        VGroup(pc, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DL, buff=0.3)
        with self.voiceover(
            "Mandelbrot and Van Ness wrote it as a Brownian integral with a power-law memory kernel: every past shock "
            "still matters. <bookmark mark='a'/> The sum of squared increments on a grid of n steps is n to the power "
            "one minus two H. <bookmark mark='b'/> On two hundred paths it blows up for H point three and vanishes "
            "for point seven; only Brownian motion lands on one. So for H not a half it is not a semimartingale, and, "
            "as Chris Rogers showed in 1997, a price driven by it would admit arbitrage. Nothing forbids volatility "
            "from being rough. <bookmark mark='c'/> A pause: at H point one, is a rise more likely to be followed by "
            f"a fall? Yes: the neighbouring correlation is {fm['rho1']['0.10']:.2f}."
        ) as vo:
            step(0)
            step(1)
            vo.wait_until("a")
            step(2)
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(leg), Create(lines), run_time=2)
            step(3)
            vo.wait_until("c")
            self.play(FadeIn(pc), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = lab_card(r"fBM by circulant embedding", [
            "def fbm(H, n, T=1.0, n_paths=1, seed=0):           # Davies-Harte",
            "    rng = np.random.default_rng(seed); k = np.arange(n + 1)",
            "    gamma = 0.5*(abs(k-1)**(2*H) - 2*abs(k)**(2*H) + abs(k+1)**(2*H))",
            "    row = np.concatenate([gamma, gamma[-2:0:-1]])   # a circulant row",
            "    lam = np.clip(np.fft.fft(row).real, 0, None)     # its eigenvalues",
            "    m = len(row); out = np.empty((n_paths, n + 1))",
            "    for p in range(n_paths):",
            "        z = rng.standard_normal(m) + 1j*rng.standard_normal(m)",
            "        y = np.fft.fft(np.sqrt(lam/m) * z)[:n].real  # exact increments",
            "        out[p] = np.concatenate([[0.0], np.cumsum(y)]) * (T/n)**H",
            "    return out",
        ], source="explainer/quant/house/sim.py", width=9.2, font_size=16).to_edge(UP, buff=0.4)
        outs = ["fbm(H, 4096); hurst_from_increments(path)    # Part 5's test",
                "recovers H = 0.1, 0.5, 0.8 to within 0.06; Var B_1 = 1 over 4,000 paths"]
        with self.voiceover(
            "How do you simulate it exactly? Increments of fractional Brownian motion are a stationary Gaussian "
            "sequence with a known covariance. Davies and Harte embedded that covariance in a circulant matrix, whose "
            "eigenvalues are a Fourier transform of its first row. <bookmark mark='a'/> Multiply complex Gaussian "
            "noise by the square roots of the eigenvalues, transform back, and the increments come out with exactly "
            "the right covariance, in n log n operations instead of the n cubed of a Cholesky factor. "
            "<bookmark mark='b'/> The House's test checks that the Hurst estimator recovers H from paths made this "
            "way."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(Indicate(card.code[3:5], color=ITO, scale_factor=1.02), Indicate(card.code[8], color=ITO,
                                                                                       scale_factor=1.02))
            vo.wait_until("b")
            lab_run(self, card, outs, font_size=17)
        self.wait(0.4)
        self.clear_scene()

    def bitcoin(self, r):
        d = np.asarray(r["days"], float)
        lv = np.asarray(r["log_vol"])
        t = np.array([datetime.fromtimestamp(x, tz=timezone.utc).year + (datetime.fromtimestamp(x, tz=timezone.utc)
                                                                            .timetuple().tm_yday - 1) / 366 for x in d])
        g = axes([2019, 2021], [lv.min() - 0.2, lv.max() + 0.2], x_length=6.6, y_length=1.9,
                 ylabel=r"log daily volatility (5-minute returns)", xticks=[2019, 2020, 2021], xfmt=lambda u: f"{int(u)}",
                 yticks=[], font_size=16).to_corner(UL, buff=0.5)
        ax = g.ax
        line = curve(ax, t, lv, BM, stroke_width=1.8)
        h = r["hurst"]
        qs, zeta = np.asarray(h["qs"]), np.asarray(h["zeta"])
        g2 = axes([0, 3.2], [0, 0.5], x_length=5.0, y_length=2.7, xlabel=r"$q$", ylabel=r"$\zeta_q$: scaling of "
                  r"$\mathbb{E}|\Delta \log\sigma|^q$", xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5], font_size=16)
        g2.to_corner(DL, buff=0.55)
        a2 = g2.ax
        dots = VGroup(*[Dot(a2.c2p(q, z), radius=0.07, color=JUMP) for q, z in zip(qs, zeta)])
        fit = curve(a2, np.array([0, 3.2]), h["H"] * np.array([0, 3.2]), JUMP, stroke_width=2.5)
        bm = DashedVMobject(curve(a2, np.array([0, 1.0]), 0.5 * np.array([0, 1.0]), GREY_B, stroke_width=2), num_dashes=12)
        side = VGroup(
            MathTex(rf"H \approx {h['H']:.2f}", font_size=44, color=JUMP),
            label(rf"each $q$ alone: {min(h['H_each']):.2f} to {max(h['H_each']):.2f}", font_size=21, color=GREY_A),
            label(rf"the same estimator on simulated fBM: {r['fbm_check']['0.1']:.2f} for $H = 0.1$, "
                  rf"{r['fbm_check']['0.5']:.2f} for $0.5$", font_size=19, color=GREY_B),
            wrapped_label(r"Gatheral, Jaisson and Rosenbaum (2018), ``Volatility is rough'': $H \approx 0.1$ for equity "
                          r"indices", 5.2, 20, ITO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        src = real_data(r"Binance BTCUSDT one-minute candles, 2019--2020; the House's \texttt{hurst\_from\_increments}")
        with self.voiceover(
            "How rough is volatility? Measure Bitcoin's volatility each day from five-minute returns, for "
            f"{r['n_days']} days, and take logs. <bookmark mark='a'/> For fractional Brownian motion, the average q-th "
            "power of the changes grows with the lag at exponent q times H: a line through the origin. "
            f"<bookmark mark='b'/> Bitcoin's points lie on such a line with slope about {h['H']:.2f}, far below a "
            "half. In 2018 Gatheral, Jaisson and Rosenbaum found H near a tenth for stock indices: \"Volatility is "
            "rough\"."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(line), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(bm))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd, scale=1.5) for dd in dots], lag_ratio=0.2), Create(fit))
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def caveat(self, cd, r):
        li, lr = np.asarray(cd["log_iv"]), np.asarray(cd["log_rv"])
        n = len(li)
        g = axes([0, n], [min(li.min(), lr.min()) - 0.1, max(li.max(), lr.max()) + 0.1], x_length=7.0, y_length=3.0,
                 xlabel=r"day", ylabel=r"simulated log volatility", xticks=[0, n], yticks=[], font_size=15)
        g.to_corner(UL, buff=0.45)
        l1 = curve(g.ax, np.arange(n), lr, JUMP, stroke_width=1.5)
        l2 = curve(g.ax, np.arange(n), li, ITO, stroke_width=1.5)
        leg = legend([(ITO, r"true integrated variance (smooth OU, $H = \tfrac12$)"),
                      (JUMP, r"measured: 5-minute RV with 5 bp noise")], font_size=18).next_to(g, DOWN, buff=0.2)
        leg.align_to(g, LEFT)
        rows = VGroup(
            MathTex(rf"\hat H\ \text{{from measured RV}} = {cd['H_rv']:.2f}", font_size=30, color=JUMP),
            MathTex(rf"\hat H\ \text{{without noise}} = {cd['H_rv_clean']:.2f}", font_size=30, color=GREY_A),
            MathTex(rf"\hat H\ \text{{from the true variance}} = {cd['H_iv']:.2f}", font_size=30, color=ITO),
            MathTex(rf"\text{{Bitcoin}}: {r['hurst']['H']:.2f}", font_size=30, color=BM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        low = cd["H_iv"] < 0.4
        verdict = (f"The estimator says {cd['H_iv']:.2f} even from the true integrated variance, and "
                   f"{cd['H_rv']:.2f} from the noisy measurement: a smooth volatility that mean-reverts within a week "
                   "looks rough at daily resolution." if low else
                   f"Here the estimator returns {cd['H_iv']:.2f} from the true variance and {cd['H_rv']:.2f} from the "
                   "measured one: the artefact needs other settings to appear.")
        note_ = wrapped_label(r"Cont and Das (2024), ``Rough volatility: fact or artefact?'' (\textit{Sankhy\=a B}); against "
                              r"them, the evidence collected in \textit{Rough Volatility} (SIAM, 2023). The debate is "
                              r"open; Part 14 returns to it with option prices, which see roughness more directly.", 6.0,
                              19, GREY_A).to_corner(DR, buff=0.35)
        with self.voiceover(
            "Now the caveat, computed. Rama Cont and Purba Das argued in 2024 that measured volatility can look rough "
            "when the true volatility is not. Simulate five hundred days with an ordinary Ornstein-Uhlenbeck log "
            "volatility, H exactly a half, mean-reverting in a week, a price every second and five basis points of "
            f"noise, and measure it as we did Bitcoin. <bookmark mark='a'/> {verdict} <bookmark mark='b'/> So a low H "
            "in data fits roughness, and also fast mean reversion seen through a coarse lens; Part fourteen takes up "
            "the debate with option prices."
            " Fractional Brownian motion is not a semimartingale, so Itô's calculus fails on it. Next: a calculus that works on any path."
        ) as vo:
            self.play(FadeIn(g), Create(l2), Create(l1), FadeIn(leg), run_time=2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
