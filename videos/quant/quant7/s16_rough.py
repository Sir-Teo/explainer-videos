from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, predict


class Rough(VoiceoverScene):
    def construct(self):
        ro = load("rough")
        self.card()
        self.zoom(ro)
        self.lab(ro)
        self.meaning(ro)

    def card(self):
        c = chapter_card(11, r"Is volatility rough?", r"How jagged is the hidden river?", lit=(2018,), part=PART)
        with self.voiceover("Chapter eleven. Is volatility rough?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def zoom(self, ro):
        p1, p5 = np.asarray(ro["path01"]), np.asarray(ro["path05"])

        def panel(p, n, col, title):
            seg = p[:n]
            seg = (seg - seg.min()) / max(seg.max() - seg.min(), 1e-9)
            g = axes([0, n], [0, 1], x_length=3.6, y_length=1.6, xticks=[], yticks=[], font_size=13, ylabel=title)
            return VGroup(g, curve(g.ax, np.arange(n), seg, col, stroke_width=1.6))

        rows = VGroup()
        for p, col, h in ((p1, BAD, r"$H = 0.1$"), (p5, VOL, r"$H = 0.5$")):
            rows.add(VGroup(*[panel(p, n, col, rf"{h}: {n:,} steps".replace(",", "{,}")) for n in (2048, 512, 128)]).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, buff=0.6).to_edge(UP, buff=0.6)
        rows[1].align_to(rows[0], LEFT)
        cap = label(r"fractional Brownian motion, simulated; each panel zooms 4$\times$ into the start of the one before, "
                    r"rescaled to fill it", font_size=18, color=GREY_B).to_edge(DOWN, buff=1.6)
        rows_eq = [
            cmath(r"m(q,\Delta) = \big\langle|\log\sigma_{t+\Delta} - \log\sigma_t|^q\big\rangle", r"\propto", r"\Delta^{\zeta_q}", font_size=32),
            cmath(r"\mathbb{E}|B^H_{t+\Delta} - B^H_t|^q = c_q\Delta^{qH}", r"\Rightarrow", r"\zeta_q = qH", font_size=32),
        ]
        eqs = VGroup(*rows_eq).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            """How rough is the river? Two simulated paths, with H one half below. <bookmark mark='a'/> These min-max-rescaled panels compare shapes, not estimate H. <bookmark mark='b'/> H point one is more jagged; self-similarity means equality in law. <bookmark mark='c'/> Gatheral, Jaisson and Rosenbaum found H near point one on realized-volatility proxies. Noise, smoothing and finite scales remain alternative explanations for latent volatility."""
        ) as vo:
            self.play(FadeIn(rows[1][0]), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(rows[1][1]), run_time=0.8)
            self.play(FadeIn(rows[1][2]), run_time=0.8)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in rows[0]], lag_ratio=0.5, run_time=2.5))
            vo.wait_until("c")
            self.play(FadeOut(cap), FadeIn(eqs))
        self.wait(0.3)
        self.clear_scene()

    def lab(self, ro):
        card = lab_card(r"measuring roughness", [
            "def log_rv_scaling(log_v, lags, qs):",
            "    zeta = []",
            "    for q in qs:",
            "        m = [np.mean(np.abs(log_v[L:] - log_v[:-L])**q)",
            "             for L in lags]",
            "        zeta.append(np.polyfit(np.log(lags), np.log(m), 1)[0])",
            "    H = np.polyfit(qs, zeta, 1)[0]",
            "    return zeta, H",
        ], source="explainer/quant/house/rough.py", width=6.4).to_corner(UL, buff=0.3)
        b = ro["btc"]
        s1, s5 = np.asarray(ro["sims"]["0.1"]), np.asarray(ro["sims"]["0.5"])
        lags, qs, zeta = np.asarray(b["lags"], float), np.asarray(b["qs"]), np.asarray(b["zeta"])
        ms = [np.asarray(b[f"m_{q}"]) for q in qs]
        g = axes([0, 4.1], [-3.5, 1.5], x_length=4.6, y_length=3.0, xticks=[0, 2, 4], yticks=[-3, -1, 1],
                 xlabel=r"$\log\Delta$ (days)", ylabel=r"$\log m(q,\Delta)$, Bitcoin", font_size=14).to_corner(DL, buff=0.45)
        cols = [GREY_B, RET, VOL, GOOD, BAD]
        lines = VGroup(*[VGroup(*[Dot(g.ax.c2p(np.log(L), np.log(v)), radius=0.04, color=c_) for L, v in zip(lags, m)],
                                curve(g.ax, np.log(lags), np.log(m), c_, stroke_width=2)) for m, c_ in zip(ms, cols)])
        g2 = axes([0, 3.2], [0, 0.5], x_length=3.6, y_length=3.0, xticks=[0, 1, 2, 3], yticks=[0, 0.2, 0.4],
                  xlabel=r"$q$", ylabel=r"$\zeta_q$", font_size=14).next_to(g, RIGHT, buff=0.7)
        zd = VGroup(*[Dot(g2.ax.c2p(q, z), radius=0.07, color=c_) for q, z, c_ in zip(qs, zeta, cols)])
        zl = curve(g2.ax, np.array([0, 3.2]), b["H"] * np.array([0, 3.2]), BAD, stroke_width=3)
        hl = MathTex(rf"H = {b['H']:.2f}", font_size=34, color=BAD).next_to(g2, UP, buff=0.1)
        kern = VGroup(
            label(r"forecasting with roughness (Gatheral, Jaisson and Rosenbaum 2018):", font_size=19, color=GREY_A),
            MathTex(r"\mathbb{E}[\log\sigma^2_{t+\Delta}\mid\mathcal{F}_t] \propto \Delta^{H+\frac12}\!\int_{-\infty}^{t}"
                    r"\frac{\log\sigma^2_s\,ds}{(t-s+\Delta)(t-s)^{H+\frac12}}", font_size=28, color=VOL),
            label(r"a power-law kernel over the whole past; HAR's three steps are a cheap approximation. Part 14 builds "
                  r"the models.", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(UP, buff=0.35)  # above both charts, clear of H
        pc = predict(r"If $H = 0.5$, what slope would the $q = 2$ line have?", width=4.4, font_size=20).to_corner(UR, buff=0.3)
        rough = b["H"] < 0.25
        verdict = ("Rough, as Gatheral, Jaisson and Rosenbaum found on equity indices."
                   if rough else "Smoother than the equity-index result.")
        with self.voiceover(
            f"""Lab. The House's estimator fits moment slopes across lags and powers q. <bookmark mark='a'/> Simulated H point one and one half return about {s1.mean():.2f} and {s5.mean():.2f}. <bookmark mark='b'/> On {len(ro['lv']):,} Bitcoin log-realized-volatility observations, H is {b['H']:.2f}. {verdict} This proxy estimate does not establish latent roughness. <bookmark mark='c'/> At H one half and q two, the slope is one. <bookmark mark='d'/> An idealized Gaussian rough model gives a power-law predictor; HAR approximates it over finite horizons."""
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"H = 0.1, 5 paths: " + ", ".join(f"{v:.2f}" for v in s1),
                                 f"H = 0.5, 5 paths: " + ", ".join(f"{v:.2f}" for v in s5)], run_time=1.5)
            vo.wait_until("b")
            self.play(FadeOut(card), FadeOut(card.out))
            self.play(FadeIn(g), LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.3, run_time=2))
            self.play(FadeIn(g2), LaggedStart(*[GrowFromCenter(d) for d in zd], lag_ratio=0.2), Create(zl), FadeIn(hl))
            vo.wait_until("c")
            self.play(FadeIn(pc))
            vo.wait_until("d")
            self.play(FadeOut(pc))
            self.play(FadeIn(kern))
        self.wait(0.3)
        self.clear_scene()

    def meaning(self, ro):
        H = float(ro["btc"]["H"])
        rho = 2 ** (2 * H - 1) - 1
        rows = [
            cmath(r"\mathbb{E}[B^H_tB^H_s]", r"=", r"\tfrac12\big(t^{2H} + s^{2H} - |t-s|^{2H}\big)", font_size=34),
            cmath(r"\operatorname{corr}(\Delta_1, \Delta_2)", r"=", r"2^{2H-1} - 1", font_size=34),
            cmath(r"\operatorname{Var}(B^H_{t+\Delta} - B^H_t)", r"=", r"\Delta^{2H}", font_size=34),
            cmath(r"\text{ATM skew}", r"\propto", r"T^{H - \frac12}", font_size=34),
        ]
        whys = [why(r"fractional Brownian motion: the covariance that makes it self-similar with exponent $H$"),
                why(r"two successive increments: negatively correlated when $H < \tfrac12$, the path keeps turning back"),
                why(r"the variance of a change grows like $\Delta^{2H}$: fast at short lags when $H$ is small"),
                why('short-maturity skew law under suitable rough-model, leverage and regularity assumptions (Part 14)')]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-1.8, buff=0.5, edge=6.9)
        res = MathTex(rf"H = {H:.2f}:\ \operatorname{{corr}}(\Delta_1, \Delta_2) = {rho:+.2f}", font_size=32, color=BAD)
        res.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"""What does H measure? Fractional Brownian scaling holds in distribution, not as identical segments. <bookmark mark='a'/> Its adjacent-increment correlation is two to the power two H minus one, minus one. <bookmark mark='b'/> That is negative for H below one half. <bookmark mark='c'/> At estimated H {H:.2f}, this model implies {rho:.2f}; it is not a directly measured Bitcoin increment correlation. <bookmark mark='d'/> Suitable rough-volatility, leverage and regularity assumptions yield the short-maturity skew law. Next: scoring."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            step(3)
        self.wait(0.3)
        self.clear_scene()
