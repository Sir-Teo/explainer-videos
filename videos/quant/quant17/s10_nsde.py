from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, IV, NET, OPT, PART, REF, ask, grid_fn, illustration, load


class NSDE(VoiceoverScene, ThreeDScene):
    def construct(self):
        n = load("nsde")
        t = load("nsde_trace")
        self.card()
        self.model()
        self.derive()
        self.calib_replay(t)
        self.push(t)
        self.bounds(n)
        self.surfaces(t)

    def card(self):
        c = chapter_card(15, r"Neural SDEs and robust bounds", r"How wrong can an exotic price be, if the vanillas are right?",
                         part=PART)
        with self.voiceover("Chapter fifteen. Neural SDEs and robust bounds."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"dX_t", r"=", r"-\tfrac12\sigma_\theta^2\,dt + \sigma_\theta(t, X_t, V_t)\,dW^1_t", font_size=36,
                      colors={r"dX_t": NET}),
                cmath(r"dV_t", r"=", r"b_\theta(t, V_t)\,dt + \eta_\theta(t, V_t)\,dW^2_t,\quad d\langle W^1, W^2\rangle = "
                      r"\rho\,dt", font_size=34, colors={r"dV_t": NET}),
                cmath(r"\min_\theta\ /\ \max_\theta", r"\ ", r"\text{exotic}(\theta)\quad \text{subject to every vanilla "
                      r"repriced}", font_size=34, colors={r"\min_\theta\ /\ \max_\theta": GOOD})]
        whys = [why(r"Gierjatowicz, Sabate-Vidales, \v{S}i\v{s}ka, Szpruch and \v{Z}uri\v{c} (2022): a stochastic volatility "
                    r"model whose coefficients are networks, simulated by Euler steps and differentiated end to end"),
                why(r"a hidden factor $V$ drives the volatility; drift, volatility of volatility and correlation are all "
                    r"learned, so the model can produce any smile Heston can, and many it cannot"),
                why(r"calibrate to vanilla prices, then push the price of an exotic as low and as high as it will go while "
                    r"the vanillas stay repriced: a range, not a point. Part 9's robust bounds and Part 15's model reserve, "
                    r"computed with a model rich enough to matter")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Part fifteen asked what to charge for not knowing the model. Here is a modern answer. Write a stochastic "
            "volatility model whose coefficients are all neural networks, simulate it with Euler steps, and "
            "differentiate through the simulation. <bookmark mark='a'/> A hidden factor drives the volatility, and its "
            "drift, its volatility and its correlation with the price are all learned. <bookmark mark='b'/> Calibrate "
            "it to the vanilla options. Then push the price of an exotic as low as it will go, and as high, while every "
            "vanilla stays repriced. The answer is a range, and its width is the model risk."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def bounds(self, n):
        su = n["setup"]
        lo, hi, cal, hes = n["low"], n["high"], n["calibrated"], n["heston_doc"]
        vals = [lo["doc"], cal["doc"], hes, hi["doc"]]
        span = max(vals) - min(vals)
        a, b = min(vals) - 0.6 * span, max(vals) + 0.6 * span
        g = axes([a, b], [-1, 1], x_length=10.0, y_length=1.6, xlabel=r"price of the down-and-out call (per unit of spot)",
                 xticks=list(np.linspace(a, b, 5)), xfmt=lambda v: f"{v:.4f}", yticks=[], font_size=15)
        g.move_to(UP * 0.2)
        ax = g.ax
        band = Line(ax.c2p(lo["doc"], 0), ax.c2p(hi["doc"], 0), stroke_color=GOOD, stroke_width=14, stroke_opacity=0.6)
        marks = VGroup()
        for v, txt, col, side in ((lo["doc"], r"lowest", GOOD, DOWN), (hi["doc"], r"highest", GOOD, DOWN),
                                  (hes, r"Heston, the model behind the vanillas", REF, UP),
                                  (cal["doc"], r"the first calibration", NET, UP)):
            d = Dot(ax.c2p(v, 0), radius=0.08, color=col)
            lab = VGroup(label(txt, font_size=17, color=col), MathTex(f"{v:.4f}", font_size=24, color=col)).arrange(DOWN, buff=0.06)
            lab.next_to(d, side, buff=0.25 if side is DOWN else 0.35)
            marks.add(VGroup(d, lab))
        if abs(hes - cal["doc"]) < (b - a) * 0.12:
            marks[3][1].shift(UP * 0.75)
        head = label(rf"a down-and-out call: strike 1, barrier {su['barrier']:g}, one year, watched on {su['steps']} dates",
                     font_size=24).to_edge(UP, buff=0.6)
        foot = wrapped_label(rf"all three neural models reprice the same 36 vanilla calls (4 expiries, 9 strikes) to within "
                             rf"{max(lo['iv_rmse'], hi['iv_rmse'], cal['iv_rmse']):.2f} vol points of Heston's; yet the exotic "
                             rf"ranges from {lo['doc']:.4f} to {hi['doc']:.4f}, {100 * (hi['doc'] - lo['doc']) / hes:.0f}\% of "
                             r"Heston's price. Vanillas fix the marginal distributions; a barrier depends on how they are "
                             r"joined through time, which they do not fix. Small networks, trained for minutes: the true "
                             r"range is at least this wide", 11.8, 20, GREY_A).to_edge(DOWN, buff=0.45)
        src = illustration(r"neural SDE with 3 small networks; 16{,}384 paths a step; prices checked on 200{,}000 fresh paths",
                           corner=UR)
        with self.voiceover(
            "Here is the result for a down-and-out call, with the vanilla prices generated by Heston's model. "
            f"<bookmark mark='a'/> The first calibration prices the barrier option at {cal['doc']:.4f}; Heston's own "
            f"price is {hes:.4f}. <bookmark mark='b'/> Pushed down and up while still repricing every vanilla, the "
            f"neural model reaches {lo['doc']:.4f} and {hi['doc']:.4f}: a range of {100 * (hi['doc'] - lo['doc']) / hes:.0f} "
            "percent of the price, from models that all agree on every quoted option. And it is only a lower estimate "
            "of the true range."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(src))
            self.play(FadeIn(marks[2]))
            vo.wait_until("a")
            self.play(FadeIn(marks[3]))
            vo.wait_until("b")
            self.play(Create(band), FadeIn(marks[0]), FadeIn(marks[1]), FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\min_\theta", r"\ ", r"\textstyle\sum_{ij}\big(P^\theta_{ij} - P^{\text{mkt}}_{ij}\big)^2,\quad "
                      r"P^\theta_{ij} = \mathbb{E}^\theta (S_{T_i} - K_j)^+", font_size=36, colors={r"\min_\theta": GOOD}),
                cmath(r"\min_\theta", r"\ ", r"\pm\,\mathbb{E}^\theta[\Phi] + \lambda \textstyle\sum_{ij}\big(P^\theta_{ij} - "
                      r"P^{\text{mkt}}_{ij}\big)^2", font_size=36, colors={r"\min_\theta": BAD}),
                cmath(r"S_T", r"\leftarrow", r"S_T / \overline{S_T}\ \Rightarrow\ \widehat{\mathbb{E}}\, S_T = 1", font_size=38,
                      colors={r"S_T": NET}),
                cmath(r"[\,p_{\min},\ p_{\max}\,]_{\text{found}}", r"\subseteq", r"[\,p_{\min},\ p_{\max}\,]_{\text{model}}"
                      r"\subseteq \text{MOT bounds}", font_size=36, colors={r"\subseteq": WHITE})]
        whys = [why(r"calibrate: Monte Carlo prices of the 36 vanillas, differentiated through every Euler step back to "
                    r"the networks' weights"),
                why(r"push: make the exotic $\Phi$ as cheap (or as dear) as possible, with a penalty that keeps every "
                    r"vanilla repriced; keep the most extreme state whose vanilla error stays under a ceiling"),
                why(r"a control variate on every batch: rescale the simulated prices so their mean is exactly the forward, "
                    r"so the model cannot buy a fit with an arbitrage"),
                why(r"a local search inside one model class finds a range inside the true one, which in turn lies inside "
                    r"the model-free martingale optimal transport bounds of Part 9")]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.4, buff=0.42, edge=6.9)
        with self.voiceover(
            "In equations. Calibrate: minimize the squared errors of the thirty-six vanilla prices, each a Monte "
            "Carlo average, differentiated through every Euler step back to the networks' weights. "
            "<bookmark mark='a'/> Then push: minimize the exotic's price, or its negative, with a heavy penalty for "
            "any vanilla that drifts away, and keep the most extreme state whose vanilla error stays under a "
            "ceiling. <bookmark mark='b'/> One safeguard on every batch: rescale the simulated prices so their mean is "
            "exactly the forward, so the model cannot buy its fit with an arbitrage. <bookmark mark='c'/> What comes "
            "out is a range found by a local search in one class of models: inside the true range of all calibrated "
            "models, which in turn sits inside the model-free bounds of Part nine."
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

    def calib_replay(self, t):
        c = t["calib"]
        steps = np.asarray(c["step"], float)
        loss = np.asarray(c["loss"])
        ivs = np.asarray(c["iv"])
        tiv = np.asarray(t["target_iv"])
        K = np.asarray(t["setup"]["strikes"])
        mats = t["setup"]["mats"]
        idx = [0, 1, 3, 5, 10, 20, len(steps) - 1]

        def frame(i):
            panels = VGroup()
            for m_ in range(4):
                g = axes([0.8, 1.2], [0.1, 0.35], x_length=1.6, y_length=2.6, xlabel=rf"{mats[m_]:g}y",
                         ylabel=r"implied vol" if m_ == 0 else "", xticks=[], yticks=[0.15, 0.3] if m_ == 0 else [],
                         yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=12)
                y = np.clip(np.nan_to_num(ivs[idx[i]][m_], nan=0.1), 0.1, 0.35)
                panels.add(VGroup(g, VGroup(*[Dot(g.ax.c2p(k, v), radius=0.035, color=IV) for k, v in zip(K, tiv[m_])]),
                                  curve(g.ax, K, y, NET, stroke_width=3)))
            panels.arrange(RIGHT, buff=0.12)
            return VGroup(panels, label(rf"calibration step {int(steps[idx[i]])}", font_size=17,
                                        color=NET).next_to(panels, DOWN, buff=0.12))
        rp = TrainingReplay(steps, np.log10(np.maximum(loss, 1e-6)), frame, checkpoints=[steps[i] for i in idx],
                            ylabel=r"$\log_{10}$ vanilla error")
        leg = legend([(IV, r"Heston's 36 vanilla prices, as implied vols"), (NET, r"the neural SDE")],
                     font_size=16).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Act one, calibration, replayed. Four expiries, nine strikes: the targets are Heston's prices, shown as "
            "implied volatilities, and the purple lines are what the neural model prices. <bookmark mark='a'/> It "
            "starts flat, a model with almost no smile. Step by step the skew appears at every expiry and the lines "
            "settle onto the dots, while the error on the right falls by orders of magnitude."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 5))
        self.wait(0.4)
        self.clear_scene()

    def push(self, t):
        lo_t, hi_t = t["low"]["trace"], t["high"]["trace"]
        ceil = t["ceiling"]
        allc = np.r_[lo_t["cl"], hi_t["cl"]]
        alld = np.r_[lo_t["doc"], hi_t["doc"]]
        xmax = float(min(np.percentile(allc, 97), ceil * 6))
        ylo, yhi = float(alld.min()) - 0.001, float(alld.max()) + 0.001
        g = axes([0, xmax], [ylo, yhi], x_length=7.2, y_length=4.4, xlabel=r"vanilla error (calibration loss)",
                 ylabel=r"barrier option's price", xticks=[0, round(ceil, 4)], xfmt=lambda v: f"{v:.4f}",
                 yticks=[round(v, 3) for v in np.linspace(ylo + 0.001, yhi - 0.001, 3)], font_size=14
                 ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        cl = DashedLine(ax.c2p(ceil, ylo), ax.c2p(ceil, yhi), stroke_color=BAD, stroke_width=2.5)
        tr = ValueTracker(0)

        def trail(T_, col):
            c_, d_, ok = np.asarray(T_["cl"]), np.asarray(T_["doc"]), np.asarray(T_["ok"])

            def f():
                k = max(int(tr.get_value() * (len(c_) - 1)), 1)
                g_ = VGroup()
                for i in range(k):
                    g_.add(Dot(ax.c2p(min(c_[i], xmax), d_[i]), radius=0.03, color=col if ok[i] else GREY_D))
                return g_
            return f
        a = always_redraw(trail(lo_t, GOOD))
        b = always_redraw(trail(hi_t, OPT))
        leg = legend([(GOOD, r"pushed down"), (OPT, r"pushed up"), (GREY_D, r"vanillas broken: rejected"),
                      (BAD, r"the ceiling on the vanilla error")], font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = wrapped_label(rf"every 10th step of 600, both pushes start from the calibrated model; kept: the lowest and "
                             rf"highest prices under the ceiling, {t['low']['doc']:.4f} and {t['high']['doc']:.4f} on "
                             r"200{,}000 fresh paths", 4.2, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Act two, the push. Two copies of the calibrated model; one is pushed to make the barrier option cheap, "
            "the other dear. Each dot is a state of the model: its vanilla error across, the barrier price up. "
            "<bookmark mark='a'/> Watch them separate. Every state to the right of the red line breaks the vanillas "
            "and is greyed out and rejected; the search keeps the most extreme states that still reprice every "
            "vanilla."
        ) as vo:
            self.play(FadeIn(g), Create(cl), FadeIn(leg))
            self.add(a, b)
            vo.wait_until("a")
            self.play(tr.animate.set_value(1), run_time=max(vo.remaining(0.5), 5), rate_func=linear)
            a.clear_updaters()
            b.clear_updaters()
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def surfaces(self, t):
        K = np.asarray(t["setup"]["strikes"])
        mats = np.asarray(t["setup"]["mats"])
        tiv = np.asarray(t["target_iv"])
        lo, hi = np.asarray(t["low"]["iv"]), np.asarray(t["high"]["iv"])
        ax = ThreeDAxes(x_range=[0.8, 1.2, 0.1], y_range=[0.25, 1.0, 0.25], z_range=[0.15, 0.32, 0.05], x_length=6.4,
                        y_length=4.6, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2}).shift(DOWN * 0.8 + RIGHT * 1.4)  # clear of the key

        def sheet(Z, col, op, sw):
            f = grid_fn(K, mats, np.clip(np.nan_to_num(Z, nan=0.2), 0.15, 0.32))
            return Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(0.8, 1.2), v_range=(0.25, 1.0), resolution=(16, 6),
                           fill_color=col, fill_opacity=op, stroke_width=sw, stroke_color=col, checkerboard_colors=False)
        sh, sl, sH = sheet(tiv, WHITE, 0.0, 1.2), sheet(lo, GOOD, 0.4, 0.3), sheet(hi, OPT, 0.4, 0.3)
        gap = float(np.nanmax(np.abs(hi - lo))) * 100
        hint = VGroup(label(r"strike (across), expiry (back), implied vol (up)", font_size=19, color=GREY_A),
                      legend([(WHITE, r"Heston (mesh)"), (GOOD, r"the low model"), (OPT, r"the high model")], font_size=17),
                      label(rf"largest gap between the low and high smiles: {gap:.2f} vol points", font_size=19,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.3)
        hint[2].to_corner(DL, buff=0.4)  # clear of the z axis
        self.set_camera_orientation(phi=66 * DEGREES, theta=-58 * DEGREES, zoom=0.82)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "Here are the implied-volatility surfaces of the two extreme models, over strike and expiry, laid on "
            "Heston's mesh. <bookmark mark='a'/> They are, to the eye, the same surface: the largest gap anywhere is "
            f"{gap:.2f} vol points. Yet they disagree on the barrier option: the vanillas fix where the price is likely "
            "to be at each expiry, not the path it takes to the barrier."
        ) as vo:
            self.play(Create(ax), Create(sh), FadeIn(hint[0]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(sl), FadeIn(sH), FadeIn(hint[1]), FadeIn(hint[2]))
            self.move_camera(theta=-25 * DEGREES, run_time=max(vo.remaining(0.3), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, sh, sl, sH)), FadeOut(hint)],
                         run_time=1.2)
        self.clear_scene()
        rel = wrapped_label(r"the same idea elsewhere: Cuchiero, Khosrawi and Teichmann (2020) calibrate a local "
                            r"stochastic volatility model whose leverage function is a network, trained like a GAN's "
                            r"generator; Guyon and Mustapha's neural model fits the S\&P 500 and VIX smiles and VIX "
                            r"futures jointly, within bid-ask spreads (SSRN 4309576; \textit{Risk})", 11.6, 22,
                            GREY_A).shift(UP * 0.8)
        q = ask(r"add a one-touch at the barrier, 0.8, to the calibration set. What happens to the range?")
        with self.voiceover(
            "The same idea runs through recent work, from generative calibration of local stochastic volatility to "
            "joint calibration of the S&P 500 and VIX smiles. <bookmark mark='a'/> And a question: add a one-touch "
            "struck at the barrier to the calibration set. What happens to the range?"
            " It shrinks. A one-touch at the barrier prices the chance of hitting it, exactly what the barrier option depends on, so fewer models fit everything. Next: where a hedger's training paths come from."
        ) as vo:
            self.play(FadeIn(rel))
            vo.wait_until("a")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
