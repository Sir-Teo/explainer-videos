from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load, real_data


class Correlation(VoiceoverScene, ThreeDScene):
    def construct(self):
        w = load("worstof")
        self.card()
        self.cloud(w)
        self.derive()
        self.worst(w)
        self.regimes(load("corr_regimes"))
        self.snowball(load("worstof_ac"))
        self.family()

    def card(self):
        c = chapter_card(11, r"Worst-of, correlation and the correlation skew", r"Why does a two-index note pay more "
                         r"than either alone?", part=PART)
        with self.voiceover("Chapter eleven. Worst-of payoffs, correlation, and the correlation skew."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cloud(self, w):
        s1, s2 = w["sig1"], w["sig2"]
        rh = np.asarray(w["rhos"])
        pr = np.asarray(w["prices"])
        ax = ThreeDAxes(x_range=[0.4, 1.6, 0.2], y_range=[0.4, 1.6, 0.2], z_range=[0, 0.6, 0.2], x_length=5.6,
                        y_length=5.6, z_length=2.6, tips=False, axis_config={"stroke_color": GREY_C,
                                                                              "include_ticks": False, "stroke_width": 2})
        ax.shift(LEFT * 1.6 + DOWN * 0.5)
        surf = Surface(lambda u, v: ax.c2p(u, v, max(1.0 - min(u, v), 0.0)), u_range=[0.4, 1.6], v_range=[0.4, 1.6],
                       resolution=(24, 24), fill_opacity=0.55, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(SPOT, 0), (OPT, 0.3), ("#F7A8D8", 0.6)], axis=2)
        crease = Line(ax.c2p(0.4, 0.4, 0.6), ax.c2p(1.0, 1.0, 0), stroke_color=WHITE, stroke_width=3)
        g = np.random.default_rng(3)
        z1, z3 = g.standard_normal(300), g.standard_normal(300)
        rho = ValueTracker(-0.2)

        def pts():
            r = rho.get_value()
            z2 = r * z1 + np.sqrt(max(1 - r * r, 0)) * z3
            x = np.exp(-0.5 * s1 ** 2 + s1 * z1)
            y = np.exp(-0.5 * s2 ** 2 + s2 * z2)
            return VGroup(*[Dot(ax.c2p(float(np.clip(a, 0.4, 1.6)), float(np.clip(b, 0.4, 1.6)), 0), radius=0.03,
                                color=IV if min(a, b) < 1 else GREY_B) for a, b in zip(x, y)])
        cloud = always_redraw(pts)
        ro = readout(r"\rho =", lambda: rho.get_value(), digits=2, font_size=32, color=IV)
        rp = readout(r"\text{worst-of put} =", lambda: float(np.interp(rho.get_value(), rh, pr)), digits=3,
                     font_size=32, color=OPT)
        hint = VGroup(label(r"$(K - \min(S_1, S_2))^+$ over the two indices' final levels", font_size=21, color=OPT),
                      ro, rp, label(r"orange dots: the worse of the two ends below 1", font_size=18, color=IV)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.4)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-130 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "Structurers raise the coupon by linking a note to the worst of two or three indices. Here is the put "
            "the buyer sells, over the final levels of two indices: a folded surface, creased along the diagonal. "
            "<bookmark mark='a'/> On the floor, three hundred joint outcomes. With correlation near zero "
            "the cloud is round, and many points have one index or the other below the strike. "
            "<bookmark mark='b'/> Now raise the correlation toward one. The cloud collapses onto the diagonal, the "
            "two indices move as one, and the put shrinks to a put on a single index. The price readout follows: "
            f"from {pr[0]:.3f} at minus 0.2 to {pr[-1]:.3f} at one."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), Create(surf), run_time=3)
            self.play(Create(crease))
            vo.wait_until("a")
            self.add(cloud)
            self.move_camera(theta=-100 * DEGREES, phi=50 * DEGREES, run_time=2)
            vo.wait_until("b")
            self.play(rho.animate.set_value(1.0), run_time=max(vo.remaining(0.5), 3.0), rate_func=smooth)
        cloud.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, crease, cloud)), FadeOut(hint)],
                         run_time=1.2)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\mathbb E^{\mathbb Q}\big[e^{-rT}(S_1 - S_2)^+\big]", r"=", r"S_2(0)\,\mathbb E^{\mathbb Q^{(2)}}"
                  r"\Big[\Big(\frac{S_1}{S_2} - 1\Big)^+\Big]", font_size=32,
                  colors={r"\mathbb E^{\mathbb Q}\big[e^{-rT}(S_1 - S_2)^+\big]": OPT}),
            cmath(r"\sigma^2", r"=", r"\sigma_1^2 + \sigma_2^2 - 2\rho\,\sigma_1\sigma_2", font_size=36,
                  colors={r"\sigma^2": IV}),
            cmath(r"\min(S_1, S_2)", r"=", r"S_1 - (S_1 - S_2)^+", font_size=36, colors={r"\min(S_1, S_2)": SPOT}),
            cmath(r"\frac{\partial V}{\partial\rho}", r"=", r"\mathbb E\Big[\int_0^T \sigma_1\sigma_2 S_1 S_2\,"
                  r"\partial_{12}V\,dt\Big]", font_size=34, colors={r"\frac{\partial V}{\partial\rho}": BAD}),
        ]
        whys = [why(r"Margrabe (1978): change the numeraire to $S_2$ (Part 9); the exchange option becomes a call on the "
                    r"ratio, struck at 1"),
                why(r"It\^o for a ratio (Part 5): $S_1/S_2$ is a $\mathbb Q^{(2)}$-martingale with this volatility; so the "
                    r"price is Black--Scholes with $\sigma$, $K = 1$"),
                why(r"algebra: the worse asset is the first minus an exchange option, priced by Margrabe; the worst-of "
                    r"put needs the bivariate normal (Stulz 1982; Johnson 1987 for many assets)"),
                why(r"cross-gamma is what correlation buys, as gamma is what volatility buys: the worst-of put has "
                    r"negative cross-gamma, so its holder is short correlation")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.9, buff=0.8, edge=6.9)
        with self.voiceover(
            "How are two-asset payoffs priced? William Margrabe's 1978 trick: price the option to exchange one asset "
            "for another in units of the second asset, the change of numeraire of Part nine. "
            "<bookmark mark='a'/> In those units the ratio of the two is a martingale, and Itô's formula gives its "
            "volatility: sigma one squared plus sigma two squared minus twice rho sigma one sigma two. So the "
            "exchange option is a plain Black–Scholes call on the ratio, struck at one. <bookmark mark='b'/> And the "
            "worse of two assets is the first minus an exchange option, so it is priced too. The worst-of put needs "
            "one more step, the bivariate normal distribution, which René Stulz worked out in 1982. "
            "<bookmark mark='c'/> Finally, what does correlation buy? Differentiate the price in rho: it is the "
            "expected cross-gamma, the way vega is the expected gamma. A worst-of put gains when the assets "
            "diverge, so whoever owns it is short correlation."
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

    def worst(self, w):
        rh = np.asarray(w["rhos"])
        pr = np.asarray(w["prices"])
        g = axes([-0.2, 1.0], [0.1, 0.18], x_length=6.4, y_length=4.2, xlabel=r"correlation between the two indices",
                 ylabel=r"worst-of put, at the money, one year", xticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yticks=[0.10, 0.12, 0.14, 0.16, 0.18], font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, rh, pr, OPT, stroke_width=3)
        s1, s2 = w["single"]
        h1 = DashedLine(ax.c2p(-0.2, s2), ax.c2p(1.0, s2), stroke_color=GREY_B, stroke_width=1.5)
        h1l = label(r"a put on the HSCEI alone", font_size=16, color=GREY_B).next_to(ax.c2p(-0.2, s2), UR, buff=0.05)
        mk = DashedLine(ax.c2p(w["rho_measured"], 0.1), ax.c2p(w["rho_measured"], 0.18), stroke_color=IV, stroke_width=2)
        mkl = label(rf"measured, 2021--2023: {w['rho_measured']:.2f}", font_size=17, color=IV).next_to(
            ax.c2p(w["rho_measured"], 0.18), DOWN, buff=0.1)
        pm = float(np.interp(w["rho_measured"], rh, pr))
        side = VGroup(
            wrapped_label(r"a worst-of note pays on whichever of several underlyings does worst: the investor is short "
                          r"a put on the worst performer, so the coupon is higher", 4.4, 19, GREY_A),
            wrapped_label(rf"at the measured correlation the put is worth {pm:.3f}, against {s2:.3f} for the riskier "
                          r"index alone: the buyer is paid for the chance that one of the two falls", 4.4, 19, WHITE),
            wrapped_label(r"the dealer owns the put: it is short correlation, an input no market quotes directly", 4.4,
                          19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        src = real_data(rf"vols from 2021--2023: CSI 500 ETF {100 * w['sig1']:.0f}\%, HSCEI {100 * w['sig2']:.0f}\%; "
                        r"200{,}000 paths")
        pp = pause_card(r"Correlation jumps toward one in a crash. Does the dealer, long the worst-of put, gain or lose "
                        r"on the correlation?", width=4.6).to_corner(UR, buff=0.3)
        with self.voiceover(
            "The price against correlation, for the CSI 500 and the HSCEI at their 2021 to 2023 volatilities. The "
            "lower the correlation, the dearer the put. Between these two indices the measured correlation was "
            f"{w['rho_measured']:.2f}, where the put is worth {pm:.3f}, against {s2:.3f} for the riskier index alone. "
            "<bookmark mark='a'/> Pause and predict: in a crash, correlations jump toward one. Does the dealer, who "
            "owns the worst-of put, gain or lose on that? <bookmark mark='b'/> It loses: the put is worth less when "
            "the indices move together. The dealer is short correlation, a number no market quotes."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), Create(line), Create(h1), FadeIn(h1l), Create(mk),
                      FadeIn(mkl), run_time=2.5)
            self.play(FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(pp))
            vo.wait_until("b")
            self.play(FadeOut(pp), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def regimes(self, cr):
        head = VGroup(*[label(h, font_size=20, color=GREY_A) for h in (r"window", r"CSI 500 vs CSI 1000",
                                                                       r"CSI 500 vs HSCEI")])
        tab = VGroup(head)
        A, B = cr["CSI 1000"]["rows"], cr["HSCEI"]["rows"]
        for a, b in zip(A, B):
            tab.add(VGroup(label(a["window"], font_size=22), MathTex(f"{a['rho']:.2f}", font_size=30, color=IV),
                           MathTex(f"{b['rho']:.2f}", font_size=30, color=IV)))
        xs = [-3.8, 0.4, 3.8]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.9 - 0.55 * i, 0])
        dn, up, gd = cr["HSCEI"]["down"], cr["HSCEI"]["up"], cr["gaussian_down"]
        beyond = dn > gd + 0.1 and dn > up + 0.1
        cav = wrapped_label(
            rf"a caution: correlation measured on big moves is biased even when the true correlation is constant "
            rf"(Boyer, Gibson and Loretan 1999; Forbes and Rigobon 2002). For a Gaussian with $\rho = "
            rf"{cr['gaussian_rho']:.2f}$, days when the first falls by more than one s.d. show {gd:.2f}. Measured "
            rf"CSI 500 vs HSCEI: {dn:.2f} on such down days, {up:.2f} on the matching up days", 12.0, 20, GREY_A)
        cav.to_edge(DOWN, buff=0.5)
        src = real_data(r"Yahoo Finance: 510500.SS, 512100.SS (from 2017; its 2016 rebasing excluded), \^{}HSCE; daily "
                        r"log returns", corner=UR)
        verdict = ("So the asymmetry is real: the bias cannot make down days more correlated than up days."
                   if beyond else
                   "So the measured gap is within what conditioning alone can produce.")
        with self.voiceover(
            "Does correlation jump when it matters? The CSI 500 against the CSI 1000: "
            f"{A[0]['rho']:.2f} over 2021 to 2023, {A[1]['rho']:.2f} in January and February 2024, {A[2]['rho']:.2f} in "
            f"the Covid crash. Against the HSCEI: {B[0]['rho']:.2f}, {B[1]['rho']:.2f} and {B[2]['rho']:.2f}. "
            "<bookmark mark='a'/> But correlation measured on turbulent windows is biased even when the true correlation "
            "never changes, as Boyer, Gibson and Loretan, and Forbes and Rigobon, showed. So compare like with like. On "
            f"days when the CSI 500 falls by more than one standard deviation, its correlation with the HSCEI is {dn:.2f}; "
            f"on the matching up days, {up:.2f}; a constant-correlation Gaussian gives {gd:.2f} on both. {verdict}"
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(src), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.4,
                                                                run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(cav))
        self.wait(0.4)
        self.clear_scene()

    def snowball(self, wa):
        rows = wa["rows"]
        rh = np.array([r["rho"] for r in rows])
        cp = np.array([r["coupon"] for r in rows])
        g = axes([0.25, 1.05], [0.10, 0.26], x_length=6.4, y_length=4.2, xlabel=r"correlation, CSI 500 and CSI 1000",
                 ylabel=r"fair coupon, worst-of snowball", xticks=[0.3, 0.5, 0.7, 0.9, 1.0],
                 yticks=[0.10, 0.15, 0.20, 0.25], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, rh, cp, OPT, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=OPT) for a, b in zip(rh, cp)])
        sg = DashedLine(ax.c2p(0.25, wa["single"][0]), ax.c2p(1.05, wa["single"][0]), stroke_color=GREY_B, stroke_width=1.5)
        sgl = label(r"the CSI 500 snowball alone", font_size=16, color=GREY_B).next_to(ax.c2p(0.3, wa["single"][0]), DR,
                                                                                    buff=0.05)
        cm = float(np.interp(wa["rho_measured"], rh, cp))
        mk = DashedLine(ax.c2p(wa["rho_measured"], 0.10), ax.c2p(wa["rho_measured"], 0.26), stroke_color=IV, stroke_width=2)
        side = VGroup(
            wrapped_label(r"the same snowball terms, reading the worse of the two indices each day: a linear solve for "
                          r"the fair coupon at each correlation, 20{,}000 paths", 4.4, 19, GREY_A),
            wrapped_label(rf"single index: {100 * wa['single'][0]:.1f}\%. Worst-of at the measured "
                          rf"{wa['rho_measured']:.2f}: {100 * cm:.1f}\%; at 0.3: {100 * cp[0]:.1f}\%", 4.4, 19, WHITE),
            wrapped_label(r"the higher headline coupon is the price of selling correlation, and the correlation sold "
                          r"is the one that rises in a fall", 4.4, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Put the two ideas together: a worst-of snowball on the CSI 500 and the CSI 1000, with the usual terms, "
            "reading whichever index is lower. At perfect correlation it is the single-index note, "
            f"{100 * wa['single'][0]:.1f} percent. <bookmark mark='a'/> At the correlation measured over 2021 to "
            f"2023, {wa['rho_measured']:.2f}, the fair coupon is {100 * cm:.1f} percent, and at 0.3 it would be "
            f"{100 * cp[0]:.1f}. The higher headline is the price of selling correlation, and it is a correlation "
            "that rises exactly when the indices fall."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), Create(sg), FadeIn(sgl), Create(line), FadeIn(dots), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(mk), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def family(self):
        cards = VGroup(
            definition_card(r"Correlation skew", r"implied correlation is higher for downside strikes than for upside "
                            r"ones, as implied volatility is. Desks mark it from index options against single-stock "
                            r"options (Part 11's dispersion), and model it with local correlation, the multi-asset "
                            r"cousin of local volatility, calibrated by the particle method (Guyon and "
                            r"Henry-Labord\`ere)", color=IV, width=6.2, font_size=20),
            definition_card(r"Mountain range", r"options on baskets with rules about which asset counts when "
                            r"(Bouzoubaa and Osseiran, ch.\ 15): the Himalaya removes the best performer at each date "
                            r"and locks in its return; the Everest pays on the worst of many; the Altiplano pays a "
                            r"coupon only if no asset falls below a barrier", color=OPT, width=6.2, font_size=20),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.2)
        foot = wrapped_label(r"best-of and rainbow options (Rubinstein's ``Somewhere over the rainbow'', 1991) are the "
                             r"long-correlation mirror: dispersion trading and implied correlation are Part 11; quantos, "
                             r"which add a currency correlation, are Part 22", 11.6, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two more names. The correlation skew: implied correlation is higher for downside strikes, as implied "
            "volatility is, and desks model it with local correlation, calibrated by Guyon and Henry-Labordère's "
            "particle method. <bookmark mark='a'/> And the mountain range: the Himalaya, the Everest, the Altiplano, "
            "all bets on correlation, sold as coupons."
            " Next: a product whose risk vega cannot see, the cliquet."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
