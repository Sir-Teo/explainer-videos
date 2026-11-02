from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, load, pause, real_data


class Debate(VoiceoverScene, ThreeDScene):
    def construct(self):
        a = load("artefact")
        r = load("roughness")
        b = load("bias_map")
        self.card()
        self.weekends(a)
        self.estimates(a, r)
        self.bias(b)
        self.derive()
        self.theory(b)

    def card(self):
        c = chapter_card(11, r"The debate I: is the time series fooling us?", r"Is volatility really rough?", part=PART)
        with self.voiceover("Chapter eleven. The debate, part one: is the time series fooling us?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def weekends(self, a):
        dv = np.sqrt(np.asarray(a["dow_mean_rv"]))
        names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        g = axes([-0.6, 6.6], [0, 0.6], x_length=6.0, y_length=3.6, xticks=list(range(7)), xfmt=lambda u: names[int(round(u))],
                 ylabel=r"typical realized volatility", yticks=[0, 0.2, 0.4, 0.6], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=16).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        bars = VGroup(*[Rectangle(width=0.55, height=abs(g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1]), stroke_width=0,
                                  fill_color=BAD if i >= 5 else RV, fill_opacity=0.85).move_to(g.ax.c2p(i, v / 2))
                        for i, v in enumerate(dv)])
        side = VGroup(
            wrapped_label(r"the first trap is in the data: bitcoin's weekends are calm, a weekly rhythm that the estimator "
                          r"reads as extra roughness", 4.6, 20, WHITE),
            MathTex(rf"H:\ {a['btc']:.2f} \to {a['btc_deseasonalized']:.2f}", font_size=34, color=ROUGH),
            label(r"after removing each weekday's average", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        src = real_data(r"geometric mean of daily realized variance by weekday (UTC), 2024--2025")
        with self.voiceover(
            "Not everyone accepts that volatility is rough. Start with a trap in our own data: Bitcoin's weekends "
            "are calm, a Saturday's realized volatility about half a weekday's. "
            "<bookmark mark='a'/> That weekly rhythm jumps up and down from day to day, and the estimator reads it "
            f"as roughness. Remove it, and H rises from {a['btc']:.2f} to {a['btc_deseasonalized']:.2f}. Still rough, "
            "but the number moved because of a calendar, not a law of nature."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                      FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def estimates(self, a, r):
        items = [(r"bitcoin", a["btc"], RV), (r"bitcoin, weekdays evened out", a["btc_deseasonalized"], RV)]
        cols = [VAR, IV, BAD]
        for m, c in zip(a["models"], cols):
            items.append((rf"smooth: {m['name']}", m["H_rv"], c))
        g = axes([0, 0.5], [-0.5, len(items) - 0.5], x_length=6.0, y_length=4.0, xlabel=r"estimated $H$",
                 xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[], font_size=15).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, (t, v, c) in enumerate(items):
            y = len(items) - 1 - i
            bars.add(Rectangle(width=max(abs(ax.c2p(max(v, 0), 0)[0] - ax.c2p(0, 0)[0]), 1e-3), height=0.42, stroke_width=0,
                               fill_color=c, fill_opacity=0.85).move_to(ax.c2p(max(v, 0) / 2, y)))
            labs.add(VGroup(label(t, font_size=18, color=c), MathTex(f"{v:.2f}", font_size=22))
                     .arrange(RIGHT, buff=0.2).next_to(ax.c2p(0, y), LEFT, buff=0.2))
        half = DashedLine(ax.c2p(0.5, -0.5), ax.c2p(0.5, len(items) - 0.5), stroke_color=GREY_C, stroke_width=1.5)
        side = wrapped_label(r"three smooth volatilities ($H = \tfrac12$), as variable as bitcoin's and measured the same "
                             r"way, through 5-minute realized variance: slow ones read 0.4; one that mean-reverts within "
                             r"hours reads almost 0. At a daily resolution, fast mean reversion and roughness look alike "
                             r"(Cont and Das 2024; Guyon and El Amrani 2023)", 5.6, 19, GREY_A).to_corner(UL, buff=0.5)
        verdict = wrapped_label(r"the case for roughness rests on several measurements agreeing: time series, the skew's "
                                r"term structure, and a microstructure story. Each alone has a smooth explanation", 12.0, 20,
                                ROUGH).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The deeper objection, made by Rama Cont and Purba Das, is that the estimator can be fooled. Simulate "
            "three perfectly smooth volatilities, as variable as Bitcoin's, and measure them the same way. "
            "<bookmark mark='a'/> The slow ones read about four-tenths. <bookmark mark='b'/> The one that "
            "mean-reverts within hours reads almost zero: at a daily resolution, fast and rough look alike. "
            "<bookmark mark='c'/> To see how far the estimator can be fooled, map it."
        ) as vo:
            self.play(FadeIn(g), Create(half), FadeIn(bars[:2]), FadeIn(labs[:2]), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(bars[2:4]), FadeIn(labs[2:4]))
            vo.wait_until("b")
            self.play(FadeIn(bars[4]), FadeIn(labs[4]))
            vo.wait_until("c")
            self.play(FadeIn(verdict))
        self.wait(0.4)
        self.clear_scene()

    def bias(self, b):
        from scipy.interpolate import RegularGridInterpolator
        Hs = np.asarray(b["Hs"])
        M = np.asarray(b["mean"])               # (H, half-life)
        ny = M.shape[1]
        ys = np.arange(ny, dtype=float)
        hl_names = ["none" if h == 0 else (f"{h:g}d" if h >= 1 else f"{24 * h:g}h") for h in b["half_lives"]]
        ax = ThreeDAxes(x_range=[0, 0.5, 0.1], y_range=[0, ny - 1, 1], z_range=[-0.05, 0.55, 0.1], x_length=6.0,
                        y_length=5.4, z_length=3.4, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        ax.shift(DOWN * 0.4)
        f = RegularGridInterpolator((Hs, ys), M)
        surf = Surface(lambda u, v: ax.c2p(u, v, float(f((u, v)))), u_range=[Hs[0], Hs[-1]], v_range=[0, ny - 1],
                       resolution=(16, 14), fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D)
        surf.set_fill_by_value(axes=ax, colorscale=[(BAD, 0.0), (IV, 0.2), (VAR, 0.45)], axis=2)
        lvl = float(b["btc_H"])
        plane = Surface(lambda u, v: ax.c2p(u, v, lvl), u_range=[Hs[0], Hs[-1]], v_range=[0, ny - 1], resolution=(2, 2),
                        fill_opacity=0.25, stroke_width=0)
        plane.set_fill(YELLOW, opacity=0.25)
        segs = contour_segments(Hs, ys, M.T, lvl)
        gold = VGroup(*[Line(ax.c2p(p0[0], p0[1], lvl), ax.c2p(p1[0], p1[1], lvl), stroke_color=GOLD, stroke_width=5)
                        for p0, p1 in segs])
        ylabs = VGroup(*[Text(n_, font_size=14, color=GREY_B).move_to(ax.c2p(0.56, j, -0.05)) for j, n_ in enumerate(hl_names)])
        hint = VGroup(label(r"left to right: the true $H$ of a fractional OU log-volatility, 0.05 to 0.5", font_size=19,
                            color=GREY_A),
                      label(r"front to back: its mean-reversion half-life, none down to 5 hours", font_size=19, color=GREY_A),
                      label(r"height: what the estimator reads from 5-minute realized variance, 700 days", font_size=19,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.3)
        i05 = int(np.argmin(np.abs(Hs - 0.5)))
        j1 = int(np.argmin(np.abs(np.asarray(b["half_lives"], float) - 1.0)))
        i005 = 0
        note_ = VGroup(MathTex(rf"\text{{bitcoin: }}\hat H = {lvl:.2f}", font_size=28, color=GOLD),
                       MathTex(rf"H = 0.5,\ \text{{half-life 1 day}}:\ \hat H = {M[i05, j1]:.2f}", font_size=26),
                       MathTex(rf"H = 0.05,\ \text{{no mean reversion}}:\ \hat H = {M[i005, 0]:.2f}", font_size=26)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DR, buff=0.35)
        q = pause(r"A perfectly smooth volatility with a one-day half-life: what $H$ does the estimator report?",
                  width=5.4, font_size=20).to_corner(UR, buff=0.3)
        src = real_data(r"simulated: 64 cells, 4 seeds each; the House's \texttt{fou\_paths}", corner=DL)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-125 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, src, q, note_)
        self.remove(hint, src, q, note_)
        with self.voiceover(
            "Here is the estimator's bias map, the centrepiece of the debate. On the floor, two dials of a simulated "
            "log-volatility: its true H, from very rough to Brownian, and how fast it mean-reverts, from not at all "
            "to a half-life of five hours, each simulated for seven hundred days and measured exactly as Bitcoin "
            "was. The height is the H the estimator reports. "
            "<bookmark mark='a'/> Pause and predict: a perfectly smooth volatility, H one half, with a one-day "
            "half-life. What does the estimator report? <bookmark mark='b'/> About a tenth: "
            f"{M[i05, j1]:.2f}. Bitcoin's number. <bookmark mark='c'/> Now slice the map at Bitcoin's reading, "
            f"{lvl:.2f}. The gold curve is every pair of true roughness and mean reversion that reads exactly like "
            "Bitcoin: from very rough with slow mean reversion, to perfectly smooth with a half-life of about a "
            "day. One number cannot choose between them. <bookmark mark='d'/> Notice too that at the back left, "
            f"with no mean reversion, a true H of 0.05 reads {M[i005, 0]:.2f}: averaging over a day smooths the "
            "path and pushes the estimate up, while mean reversion and noise pull it down."
        ) as vo:
            self.play(FadeIn(hint), FadeIn(src), Create(ax), FadeIn(surf), FadeIn(ylabs), run_time=2)
            self.move_camera(theta=-70 * DEGREES, run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeOut(q), FadeIn(note_[1]))
            vo.wait_until("c")
            self.play(FadeIn(plane), FadeIn(note_[0]))
            self.play(LaggedStart(*[Create(l_) for l_ in gold], lag_ratio=0.05, run_time=2))
            self.move_camera(phi=40 * DEGREES, theta=-95 * DEGREES, run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(note_[2]))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, surf, plane, gold, ylabs)), FadeOut(hint), FadeOut(src),
                                      FadeOut(note_)], run_time=1.2)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\widehat{RV}_t", r"=", r"\int_t^{t + 1}\sigma^2_s\,ds + \varepsilon_t", font_size=38,
                      colors={r"\widehat{RV}_t": RV}),
                cmath(r"\mathbb{E}\big|\Delta_\ell\log\widehat{RV}\big|^q", r"\approx", r"c\,\ell^{qH} + \text{floor}",
                      font_size=38, colors={r"\mathbb{E}\big|\Delta_\ell\log\widehat{RV}\big|^q": IV}),
                cmath(r"\mathrm{Var}(X_{t + \Delta} - X_t)", r"\approx", r"\begin{cases}\nu^2\Delta^{2H} & \Delta \ll 1/\kappa\\ "
                      r"2\,\mathrm{Var}\,X & \Delta \gg 1/\kappa\end{cases}", font_size=36,
                      colors={r"\mathrm{Var}(X_{t + \Delta} - X_t)": VAR}),
                cmath(r"\inf_{\hat H}\sup\,\mathbb{E}|\hat H - H|", r"\asymp", r"n^{-1/(4H + 2)}", font_size=38,
                      colors={r"\inf_{\hat H}\sup\,\mathbb{E}|\hat H - H|": ROUGH})]
        whys = [why(r"we observe a day's integrated variance, plus measurement error"),
                why(r"an i.i.d. error adds the same amount at every lag: a flat term lowers the fitted slope, and so $\hat H$"),
                why(r"a fractional OU with rate $\kappa$: rough at lags below $1/\kappa$, flat (stationary) above; if $1/\kappa$ "
                    r"is under a day, every daily lag sits on the flat part and $\hat H \approx 0$"),
                why(r"the best possible rate from $n$ observations (Chong, Hoffmann, Liu, Rosenbaum and Szymanski 2024): "
                    r"slow, slower the rougher")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Why does the map look like this? Three effects. First, what we observe is the variance integrated over "
            "a day, plus measurement error. <bookmark mark='a'/> An independent error adds the same amount at every "
            "lag: a floor under the scaling law that flattens its slope and lowers the estimate. "
            "<bookmark mark='b'/> Second, a mean-reverting process is rough only at lags shorter than its "
            "mean-reversion time; beyond that its increments stop growing. If that time is under a day, every daily "
            "lag sits on the flat part, and the estimator reads roughness that is really stationarity. "
            "<bookmark mark='c'/> Third, even with perfect data, H is hard to estimate: Carsten Chong and "
            "co-authors proved in 2024 that the best possible error shrinks only like n to the minus one over four "
            "H plus two."
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

    def theory(self, b):
        cards = VGroup(
            history_card(2022, r"Fukasawa, Takabatake and Westphal (Mathematical Finance 32(4))",
                         r"A consistent estimator for fractional stochastic volatility under high-frequency asymptotics, "
                         r"with the measurement error modelled; their empirical study still finds volatility rough.",
                         color=QC.IDEA, width=6.2, font_size=19),
            history_card(2023, r"Bolko, Christensen, Pakkanen and Veliyev (J. Econometrics 235(2))",
                         r"A GMM estimator that corrects for the error in realized variance: $H$ still about 0.05.",
                         color=QC.IDEA, width=6.2, font_size=19),
            history_card(2024, r"Cont and Das: ``Rough volatility: fact or artefact?'' (Sankhya B)",
                         r"Rough volatility via the lens of the estimator: smooth models measured through realized "
                         r"variance can look rough. The artefact we simulated.", color=BAD, width=6.2, font_size=19),
            history_card(2024, r"Chong, Hoffmann, Liu, Rosenbaum and Szymanski (Annals of Statistics 52(4))",
                         r"Minimax theory for $H$; a companion paper gives central limit theorems (Annals of Applied "
                         r"Probability 34(3)).", color=QC.IDEA, width=6.2, font_size=19))
        grid = VGroup(VGroup(cards[0], cards[1]).arrange(RIGHT, buff=0.3, aligned_edge=UP),
                      VGroup(cards[2], cards[3]).arrange(RIGHT, buff=0.3, aligned_edge=UP)).arrange(DOWN, buff=0.25)
        if grid.height > 6.0:
            grid.scale_to_fit_height(6.0)
        grid.to_edge(UP, buff=0.3)
        what = wrapped_label(rf"what can choose: the curvature of the scaling line (bitcoin's residual "
                             rf"{b['btc_straight']:.2f}, inside the simulated range), sub-daily lags, and the options "
                             r"(next chapter)", 12.0, 20, GOLD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The statistics literature took this seriously. Masaaki Fukasawa, Tetsuya Takabatake and Rebecca "
            "Westphal modelled the measurement error and still found volatility rough. <bookmark mark='a'/> Anine "
            "Bolko and co-authors corrected it by the generalized method of moments: H still about 0.05. "
            "<bookmark mark='b'/> Rama Cont and Purba Das showed the artefact we just simulated. "
            "<bookmark mark='c'/> And the minimax theory says how little one number can settle. What can choose? "
            "Lags shorter than a day, and the options. That is the next chapter."
            " Next: what the options say."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2), FadeIn(what))
        self.wait(0.4)
        self.clear_scene()
