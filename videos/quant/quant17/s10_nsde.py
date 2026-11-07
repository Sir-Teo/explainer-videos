from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from videos.quant.quant17.common import BAD, GOOD, IV, NET, OPT, PART, REF, ask, grid_fn, illustration, load, flat_camera


class NSDE(VoiceoverScene, ThreeDScene):
    def construct(self):
        n = load("nsde")
        t = load("nsde_trace")
        n = dict(n, calibrated=t["calibrated"], low=t["low"], high=t["high"])
        self.card()
        self.model()
        self.derive()
        self.calib_replay(t)
        self.push(t)
        self.bounds(n)
        self.surfaces(t)

    def card(self):
        c = chapter_card(15, r"Neural SDEs and model sensitivity", r"How wrong can an exotic price be, if the vanillas are right?",
                         part=PART)
        with self.voiceover('Chapter fifteen. Neural SDEs and model sensitivity.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"dX_t", r"=", r"-\tfrac12\sigma_\theta^2\,dt + \sigma_\theta(t, X_t, V_t)\,dW^1_t", font_size=36,
                      colors={r"dX_t": NET}),
                cmath(r"dV_t", r"=", r"b_\theta(t, V_t)\,dt + \eta_\theta(t, V_t)\,dW^2_t,\quad d\langle W^1, W^2\rangle = "
                      r"\rho\,dt", font_size=34, colors={r"dV_t": NET}),
                cmath(r"\min_\theta\ /\ \max_\theta", r"\ ", r"\text{exotic}(\theta)\quad \text{ideal: every vanilla "
                      r"repriced}", font_size=34, colors={r"\min_\theta\ /\ \max_\theta": GOOD})]
        whys = [why(r"Gierjatowicz, Sabate-Vidales, \v{S}i\v{s}ka, Szpruch and \v{Z}uri\v{c} (2022): a stochastic volatility "
                    r"model whose coefficients are networks, simulated by Euler steps and differentiated end to end"),
                why(r"a hidden factor $V$ drives the volatility; drift, volatility of volatility and correlation are all "
                    r"learned, so the implemented class has a volatility floor/cap, a clipped latent state and bounded constant correlation; it is not guaranteed to contain every Heston law"),
                why(r"the ideal exact-constraint problem asks for extrema over laws repricing the vanillas. The saved code "
                    r"instead performs local penalized searches with aggregate calibration error; its candidate sensitivities "
                    r"are not certified robust bounds")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Neural SDEs parameterize coefficients rather than directly mapping inputs to a price. This illustration follows the model-sensitivity literature, including Gierjatowicz and coauthors. <bookmark mark='a'/> Its implemented volatility is floored at 0.02 and capped at three, its latent state is clipped between minus six and six, and its learned constant correlation stays within 0.95 in magnitude. Fifty log-price time steps approximate the dynamics. <bookmark mark='b'/> After calibration, two local penalized searches push a barrier payoff in opposite directions. Their outputs are candidate sensitivities within this restricted numerical construction, not certified robust bounds or a complete measure of model risk."
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
        for v, txt, col, side in ((lo["doc"], r"down-push candidate", GOOD, DOWN), (hi["doc"], r"up-push candidate", GOOD, DOWN),
                                  (hes, r"Heston, the model behind the vanillas", REF, UP),
                                  (cal["doc"], r"the first calibration", NET, UP)):
            d = Dot(ax.c2p(v, 0), radius=0.08, color=col)
            lab = VGroup(label(txt, font_size=17, color=col), MathTex(f"{v:.4f}", font_size=24, color=col)).arrange(DOWN, buff=0.06)
            lab.next_to(d, side, buff=0.25 if side is DOWN else 0.35)
            marks.add(VGroup(d, lab))
        if abs(hes - cal["doc"]) < (b - a) * 0.12:
            marks[3][1].shift(UP * 0.75)
        head = label(rf"a down-and-out call: strike 1, barrier {su['barrier']:g}, one year, {su['steps']} intervals; initial and terminal monitoring included",
                     font_size=24).to_edge(UP, buff=0.6)
        foot = wrapped_label(rf"Traced-run candidates: vanilla IV RMSE up to {max(lo['iv_rmse'], hi['iv_rmse'], cal['iv_rmse']):.2f} vol points. These approximate fits do not certify exact feasibility. A finite set of 36 calls does not determine complete marginals or their temporal coupling. The barrier is discretely monitored.", 11.8, 20, GREY_A).to_edge(DOWN, buff=0.45)
        src = illustration(r"neural SDE with 3 small networks; 16{,}384 paths a step; neural estimates: 200{,}000 paths in antithetic pairs; Heston QE: 400{,}000 paths",
                           corner=UR)
        with self.voiceover(
            f"Use the traced run's endpoint models consistently with its replay. The separately simulated Heston reference uses the same fifty-interval monitoring grid, not a continuously monitored barrier. <bookmark mark='a'/> The initial candidate gives {cal['doc']:.4f}, against Heston's numerical estimate {hes:.4f}. <bookmark mark='b'/> The two search directions give {lo['doc']:.4f} and {hi['doc']:.4f}. These are noisy candidate prices with approximate vanilla fits and unquantified discretization effects, not rigorous lower and upper bounds. A continuum of call strikes can determine a maturity's marginal law; these thirty-six calls cannot. Even fully specified marginals at selected dates do not determine a barrier's temporal coupling."
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
                cmath(r"\text{certified inner range}", r"\Rightarrow", r"\text{feasible laws and controlled numerical error}", font_size=36, colors={r"\subseteq": WHITE})]
        whys = [why(r"calibrate: Monte Carlo prices of the 36 vanillas, differentiated through every Euler step back to "
                    r"the networks' weights"),
                why(r"push: a local penalized objective; select an extreme saved training state under an aggregate "
                    r"mean-squared calibration-error ceiling, without enforcing every vanilla exactly"),
                why(r"batchwise division by a sample mean makes the marginal sample average equal its forward; "
                    r"a nonlinear ratio estimator; it enforces only this sample mean, can introduce finite-sample bias, and is not an arbitrage certificate"),
                why(r"only demonstrably feasible candidate laws with controlled pricing errors yield an inner range; a finite penalty search alone does not imply inclusion in "
                    r"the model-free martingale optimal transport bounds of Part 9")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-0.4, buff=0.42, edge=6.9)
        with self.voiceover(
            "The ideal exact-constraint problem differs from the code's finite penalty objective. Its calibration loss is an aggregate mean squared price error in spot-price points, not an exact constraint on every implied volatility. <bookmark mark='a'/> Candidates are selected using a noisy training ceiling and then repriced; that selection alone does not certify out-of-sample feasibility or a global extremum. <bookmark mark='b'/> Vanilla estimates divide each simulated marginal by its own sample mean. This nonlinear ratio correction has finite-sample bias; it neither imposes full process-level martingale constraints nor proves absence of arbitrage. The barrier estimator uses raw paths. Its survival indicator is differentiated as constant, so pathwise autograd misses the crossing-boundary contribution to the derivative of expected payoff. <bookmark mark='c'/> To certify an inner robust-price range, the candidate laws, constraints, monitoring and numerical errors must all be justified. The saved experiment does not provide those certificates."
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
        yr = data_range(ivs[idx], tiv)

        def frame(i):
            panels = VGroup()
            for m_ in range(4):
                g = axes([0.8, 1.2], yr, x_length=1.6, y_length=2.6, xlabel=rf"{mats[m_]:g}y",
                         ylabel=r"implied vol" if m_ == 0 else "", xticks=[], yticks=[0.15, 0.3] if m_ == 0 else [],
                         yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=12)
                y = ivs[idx[i]][m_]
                segments = VGroup(*[Line(g.ax.c2p(K[j], y[j]), g.ax.c2p(K[j+1], y[j+1]), color=NET, stroke_width=3)
                                    for j in range(len(K)-1) if np.all(np.isfinite(y[j:j+2]))])
                panels.add(VGroup(g, VGroup(*[Dot(g.ax.c2p(k, v), radius=0.035, color=IV)
                                             for k, v in zip(K, tiv[m_]) if np.isfinite(v)]),
                                  VGroup(segments, *[Dot(g.ax.c2p(k,v),radius=0.025,color=NET) for k,v in zip(K,y) if np.isfinite(v)])))
            panels.arrange(RIGHT, buff=0.12)
            return VGroup(panels, label(rf"calibration step {int(steps[idx[i]])}", font_size=17,
                                        color=NET).next_to(panels, DOWN, buff=0.12))
        rp = TrainingReplay(steps, np.log10(loss), frame, checkpoints=[steps[i] for i in idx],
                            ylabel=r"$\log_{10}$ aggregate price-MSE loss")
        leg = legend([(IV, r"Heston's 36 vanilla prices, as implied vols"), (NET, r"the neural SDE")],
                     font_size=16).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Four expiries and nine strikes define the synthetic calibration targets. The displayed implied volatilities are transformations of finite Monte Carlo price estimates. <bookmark mark='a'/> Missing or non-finite implied volatilities are omitted; lines connect only adjacent finite nodes, and no missing value is replaced by a fabricated level. The loss panel retains the full positive logarithmic loss range. The neural paths use antithetic pairs, so the path count is not a count of independent observations. Visual convergence and a small aggregate loss alone do not verify exact call-by-call calibration."
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
        xmax = data_range(allc, [ceil], zero=True)[1]
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
                    g_.add(Dot(ax.c2p(c_[i], d_[i]), radius=0.03, color=col if ok[i] else GREY_D))
                return g_
            return f
        a = always_redraw(trail(lo_t, GOOD))
        b = always_redraw(trail(hi_t, OPT))
        leg = legend([(GOOD, r"pushed down"), (OPT, r"pushed up"), (GREY_D, r"outside sampled aggregate-loss ceiling"),
                      (BAD, r"the ceiling on the vanilla error")], font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = wrapped_label(rf"every 10th step of 600, both pushes start from the calibrated model; kept: the down-push candidate and "
                             rf"up-push candidate prices under the ceiling, {t['low']['doc']:.4f} and {t['high']['doc']:.4f} on "
                             r"200{,}000 fresh paths", 4.2, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Two local searches start from the calibrated model. Every retained trace point is plotted at its actual aggregate vanilla loss and barrier estimate, without moving outliers to an axis edge. <bookmark mark='a'/> Grey identifies a sampled training loss above the chosen ceiling. It does not identify arbitrage, and an accepted point does not certify every vanilla quote or fresh-sample feasibility. The selected candidates are reevaluated with new simulation draws, but their calibration and barrier errors still need uncertainty and bias analysis."
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
        zr = data_range(tiv, lo, hi)
        ax = ThreeDAxes(x_range=[0.8, 1.2, 0.1], y_range=[0.25, 1.0, 0.25], z_range=[*zr, 0.05], x_length=6.4,
                        y_length=4.6, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2}).shift(DOWN * 0.8 + RIGHT * 1.4)  # clear of the key

        def sheet(Z, col, op, sw):
            Z = np.asarray(Z)
            cells = VGroup()
            for i in range(len(mats)-1):
                for j in range(len(K)-1):
                    if np.all(np.isfinite(Z[i:i+2, j:j+2])):
                        cells.add(Polygon(ax.c2p(K[j],mats[i],Z[i,j]), ax.c2p(K[j+1],mats[i],Z[i,j+1]),
                                          ax.c2p(K[j+1],mats[i+1],Z[i+1,j+1]), ax.c2p(K[j],mats[i+1],Z[i+1,j]),
                                          fill_color=col,fill_opacity=op,stroke_color=col,stroke_width=sw))
            cells.add(*[Dot3D(ax.c2p(K[j],mats[i],Z[i,j]),radius=0.025,color=col,resolution=(4,4))
                        for i in range(len(mats)) for j in range(len(K)) if np.isfinite(Z[i,j])])
            return cells
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
            f"The sheets join finite implied-volatility grid cells for the two traced candidates and the Heston targets. A cell with a missing corner is omitted, rather than filled with an invented volatility. <bookmark mark='a'/> The largest finite-node difference between the candidate grids is {gap:.2f} vol points. Agreement at these sparse, noisy nodes does not specify a full marginal distribution, certify an arbitrage-free interpolated surface or fix barrier dynamics. The displayed exotic sensitivity is illustrative rather than a robust bound."
        ) as vo:
            self.play(Create(ax), Create(sh), FadeIn(hint[0]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(sl), FadeIn(sH), FadeIn(hint[1]), FadeIn(hint[2]))
            self.move_camera(theta=-25 * DEGREES, run_time=max(vo.remaining(0.3), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, sh, sl, sH)), FadeOut(hint)],
                         run_time=1.2)
        flat_camera(self)
        self.clear_scene()
        rel = wrapped_label(r"the same idea elsewhere: Cuchiero, Khosrawi and Teichmann (2020) calibrate a local "
                            r"stochastic volatility model whose leverage function is a network, trained like a GAN's "
                            r"generator; Guyon and Mustapha's neural model fits the S\&P 500 and VIX smiles and VIX "
                            r"futures jointly, within bid-ask spreads (SSRN 4309576; \textit{Risk})", 11.6, 22,
                            GREY_A).shift(UP * 0.8)
        q = ask(r"add a consistent maturity-paid one-touch with the same monitoring grid. Must the exact range shrink strictly?")
        with self.voiceover(
            "Related neural-SDE work explores richer calibration settings; the saved toy is not a reproduction of all those methods. <bookmark mark='a'/> Adding an exactly consistent, maturity-paid one-touch constraint with the same monitoring grid weakly reduces the exact feasible set. Its price range may remain unchanged; strict shrinkage is not guaranteed. A hitting probability alone also does not fix its joint dependence with the terminal call payoff. Finite penalty searches can move differently because optimization and numerical error remain. Next: market generators."
        ) as vo:
            self.play(FadeIn(rel))
            vo.wait_until("a")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
