from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from explainer.quant.house import deep as D
from videos.quant.quant16.compute import load as load16
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, ask, house_lab, illustration, load, flat_camera


def _lsm():
    """Part 16's Longstaff-Schwartz on the same five-asset max-call, read from its cache (never recomputed here)."""
    return load16("maxcall")


class Stopping(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("stopping")
        r = load("stopping_region")
        self.card()
        self.method()
        self.tunnel(r)
        self.replay(r)
        self.table(s)
        self.lab(s)

    def card(self):
        c = chapter_card(10, r"Deep optimal stopping", r"Can a network learn when to exercise?", lit=(2019,), part=PART)
        with self.voiceover("Chapter ten. Deep optimal stopping."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def method(self):
        rows = [cmath(r"V_n", r"=", r"\max\big(g_n,\ \mathbb{E}[V_{n+1} \mid X_n]\big),\quad V_N = g_N", font_size=38,
                      colors={r"V_n": OPT}),
                cmath(r"\tau_n", r"=", r"n\,F_n + \tau_{n+1}\,(1 - F_n),\qquad F_n = f_n(X_n) \in \{0, 1\}", font_size=38,
                      colors={r"\tau_n": NET}),
                cmath(r"\mathbb{E}\big[g_n F + G_{n+1}(1 - F) \mid X_n\big]", r"=",
                      r"\mathbb{E}[G_{n+1} \mid X_n] + F\,\big(g_n - \mathbb{E}[G_{n+1} \mid X_n]\big)", font_size=34,
                      colors={r"=": WHITE}),
                cmath(r"\mathbb{E}\, g_{\tau_\theta}", r"\le", r"V_0", font_size=40, colors={r"\mathbb{E}\, g_{\tau_\theta}": GOOD})]
        whys = [why(r"the Snell envelope (Parts 8 and 16): at each exercise date, the better of stopping now and the "
                    r"value of waiting"),
                why(r"Becker, Cheridito and Jentzen (2019): any stopping time is built backwards from yes-or-no decisions, "
                    r"one adapted decision per date. In this Markov model, the state is sufficient for an optimal Markov rule; arbitrary history-dependent stopping rules need not be state-only"),
                why(r"given today's state the objective is linear in $F$, so it is maximized at $F = 1$ when the payoff beats "
                    r"the value of waiting and $F = 0$ otherwise: bang-bang. Train a sigmoid $F_\theta$ for gradients, "
                    r"then use the hard rule $F_\theta > 1/2$"),
                why(r"an admissible fixed policy's expected discounted payoff is a lower bound. Its noisy fresh-path mean need not be; "
                    r"Part 16's dual gives the upper bound")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "This is a Bermudan max-call with nine potential exercise dates over three years. Payoffs in the recursion are already discounted. The Snell envelope compares stopping with optimal continuation. <bookmark mark='a'/> In this Markov model an optimal rule can use the current state; arbitrary history-dependent stopping times require adapted decisions, not necessarily state-only functions. <bookmark mark='b'/> With later policies fixed, the conditional objective is linear in today's decision. Its ideal unrestricted maximizer is hard; the finite neural optimizer trains a sigmoid relaxation and then thresholds the logit at zero. That need not recover the ideal rule. <bookmark mark='c'/> A fixed admissible policy's expected discounted payoff is a lower bound on the optimal value. A finite Monte Carlo mean is noisy and need not be a lower bound realization by realization."
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

    def tunnel(self, r):
        gr = np.asarray(r["grid"])
        regs = {int(k): np.asarray(v) for k, v in r["regions"].items()}
        dates = sorted(regs)
        edge = 1.5 * (gr[1] - gr[0])
        ax = ThreeDAxes(x_range=[gr[0]-edge, gr[-1]+edge, 40], y_range=[gr[0]-edge, gr[-1]+edge, 40], z_range=[0, 9, 1], x_length=5.4,
                        y_length=5.4, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(RIGHT * 1.2 + DOWN * 0.9)  # the stack stays in frame and clear of the key
        st = 3
        dx = (gr[1] - gr[0]) * st
        layers = VGroup()
        for n in dates:
            R = regs[n]
            cells = VGroup()
            for i in range(0, len(gr), st):
                for j in range(0, len(gr), st):
                    if R[i, j]:
                        x, y = gr[j], gr[i]
                        cells.add(Polygon(ax.c2p(x - dx / 2, y - dx / 2, n), ax.c2p(x + dx / 2, y - dx / 2, n),
                                          ax.c2p(x + dx / 2, y + dx / 2, n), ax.c2p(x - dx / 2, y + dx / 2, n),
                                          stroke_width=0, fill_color=interpolate_color(ManimColor(GOOD), ManimColor(OPT),
                                                                                       (n - 1) / 7), fill_opacity=0.55))
            layers.add(cells)
        diag = Line(ax.c2p(gr[0], gr[0], 0), ax.c2p(gr[-1], gr[-1], 0), stroke_color=GREY_B, stroke_width=2)
        shares = [float(regs[n].mean()) for n in dates]
        hint = VGroup(label(r"two assets; early dates 1--8; every third grid site drawn as a coarse cell", font_size=19, color=GREY_A),
                      legend([(GOOD, r"exercise now, early dates"), (OPT, r"exercise now, late dates")], font_size=17),
                      label(rf"share of the square where it stops: {100 * shares[0]:.0f}\% at date 1, "
                            rf"{100 * shares[-1]:.0f}\% at date 8", font_size=18, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-50 * DEGREES, zoom=0.75)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "What does it learn? A call on the better of two assets. Every date's decision at once: the floor is the "
            "two prices, each layer a later date, coloured where it exercises. <bookmark mark='a'/> Each layer has two lobes: "
            "exercise when one asset is far above the strike and well ahead of the other. Between them runs a valley "
            "along the diagonal, where either asset could still end up the winner and the right to pick the better "
            "one later is worth more than the dividends given up. <bookmark mark='b'/> Fly up the tunnel toward "
            "expiry: the lobes widen and the valley narrows, as waiting is worth less and less. This is the shape "
            "Broadie and Detemple found by theory in 1997, rebuilt from simulations alone."
        ) as vo:
            self.play(Create(ax), Create(diag), FadeIn(hint[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(L_) for L_ in layers], lag_ratio=0.4, run_time=4), FadeIn(hint[1]))
            vo.wait_until("b")
            self.play(FadeIn(hint[2]))
            self.move_camera(phi=40 * DEGREES, theta=-20 * DEGREES, zoom=0.8, run_time=max(vo.remaining(0.3), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, diag, layers)),
                                                                            FadeOut(hint)], run_time=1.2)
        flat_camera(self)
        self.clear_scene()

    def replay(self, r):
        cv = r["curves"]
        dates = sorted((int(k) for k in cv), reverse=True)
        steps, vals, ends = [], [], []
        per = r["steps"]
        for i, n in enumerate(dates):
            ys = cv[str(n)]
            for j, y in enumerate(ys):
                steps.append(i * per + j * 50)
                vals.append(y)
            ends.append(i * per + (len(ys) - 1) * 50)
        gr = np.asarray(r["grid"])
        regs = {int(k): np.asarray(v) for k, v in r["regions"].items()}

        def frame(i):
            n = dates[max(i - 1, 0)] if i else dates[0]
            g = axes([gr[0], gr[-1]], [gr[0], gr[-1]], x_length=3.8, y_length=3.8, xlabel=r"asset 1", ylabel=r"asset 2",
                     xticks=[80, 120, 160], yticks=[80, 120, 160], font_size=12)
            R = regs[n] if i else np.zeros_like(regs[n])
            st = 2
            d = (gr[1] - gr[0]) * st
            cells = VGroup()
            for a in range(0, len(gr), st):
                for b_ in range(0, len(gr), st):
                    if R[a, b_]:
                        p0, p1 = g.ax.c2p(gr[b_] - d / 2, gr[a] - d / 2), g.ax.c2p(gr[b_] + d / 2, gr[a] + d / 2)
                        cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GOOD,
                                            fill_opacity=0.6).move_to((p0 + p1) / 2))
            return VGroup(g, cells, label(rf"date {n}: trained" if i else rf"date {n}: final region revealed after its stage", font_size=18,
                                          color=GOOD).next_to(g, DOWN, buff=0.1))
        rp = TrainingReplay(np.array(steps, float), np.array(vals), frame, checkpoints=[0] + ends,
                            ylabel=r"objective (expected payoff)", xlabel=r"training, date 8 back to date 1")
        with self.voiceover(
            f"The saved training trace runs backward from date eight to date one, using {per} optimizer updates per date while keeping later policies fixed. The right panel is a noisy sampled soft objective, not a certified expected payoff. The left reveals each date's saved final hard region when that stage ends; it does not reconstruct intermediate boundaries. <bookmark mark='a'/> Stochastic updates and thresholding need not produce monotone improvement. Different dates use different continuation policies, so jumps between stages are not one common loss curve converging to a known optimum."
        ) as vo:
            self.play(FadeIn(rp))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 6))
        self.wait(0.4)
        self.clear_scene()

    def table(self, s):
        d2, d5 = s["2"], s["5"]
        lsm = _lsm()["lsm"]["200000"]
        bcj = d5["reference"]
        rows_ = [(r"deep stopping (ours)", d5["lower"], d5["se"], NET, r"500 updates/date; 1 million evaluation paths"),
                 (r"Longstaff--Schwartz (Part 16)", lsm["lower"], lsm["se"], QC.DELTA,
                  rf"{lsm['n_basis']} basis functions, 200{{,}}000 fitting paths")]
        lo, hi = data_range([d5["lower"]-2*d5["se"], d5["lower"]+2*d5["se"],
                             lsm["lower"]-2*lsm["se"], lsm["lower"]+2*lsm["se"],
                             bcj["lower"], bcj["upper"], *bcj["ci"]])
        g = axes([lo, hi], [-0.5, 2.5], x_length=9.6, y_length=3.0, xlabel=r"price of the five-asset Bermudan max-call",
                 xticks=[round(v, 2) for v in np.linspace(lo + 0.02, hi - 0.02, 4)], xfmt=lambda v: f"{v:.2f}",
                 yticks=[], font_size=15).move_to(UP * 0.3)
        ax = g.ax
        marks = VGroup()
        for i, (nm, v, se, col, note_) in enumerate(rows_):
            y = 2 - i
            marks.add(VGroup(Line(ax.c2p(v - 2 * se, y), ax.c2p(v + 2 * se, y), stroke_color=col, stroke_width=6),
                             Dot(ax.c2p(v, y), radius=0.08, color=col),
                             label(rf"{nm}: {v:.3f} $\pm$ {2 * se:.3f}", font_size=19, color=col).next_to(
                                 ax.c2p(lo, y), RIGHT, buff=0.1).shift(UP * 0.28)))
        ci = Line(ax.c2p(bcj["ci"][0], 0), ax.c2p(bcj["ci"][1], 0), stroke_color=REF, stroke_width=2)
        bc = VGroup(ci, Rectangle(width=ax.c2p(bcj["upper"], 0)[0] - ax.c2p(bcj["lower"], 0)[0], height=0.3, stroke_width=0,
                              fill_color=REF, fill_opacity=0.7).move_to(ax.c2p((bcj["lower"] + bcj["upper"]) / 2, 0)),
                    label(rf"published lower/upper estimates: {bcj['lower']:.3f}, {bcj['upper']:.3f}", font_size=19,
                          color=REF).next_to(ax.c2p(lo, 0), RIGHT, buff=0.1).shift(UP * 0.3))
        gap = abs(d5["lower"] - lsm["lower"])
        foot = wrapped_label(rf"bars: approximate conditional MC $\pm2$ SE, not training uncertainty. Two assets: policy mean "
                             rf"{d2['lower']:.3f}, a binomial tree {d2['reference']['binomial']:.3f}. Their bounds used "
                             r"3{,}000 + $d$ steps of 8{,}192 paths a date on a GPU (their Table 1); ours, 500 steps on a "
                             r"shared CPU; unequal training/evaluation budgets. Published outer interval: [26.138, 26.174]. Policy expectations, not noisy estimates, are lower bounds", 12.2, 19, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"Compare fixed-policy evaluations, with their limitations. The two-asset policy mean is {d2['lower']:.3f}; its cited tree reference is {d2['reference']['binomial']:.3f}, a numerical benchmark. With five assets, our network gives {d5['lower']:.3f}, and the saved Part sixteen regression policy gives {lsm['lower']:.3f}. <bookmark mark='a'/> Their point estimates differ by {gap:.3f}. The bars show about two conditional Monte Carlo standard errors; they omit training uncertainty, and the evaluation budgets differ. This is not an equal-cost test or a certified statistical tie. <bookmark mark='b'/> The paper reports lower and upper estimates {bcj['lower']:.3f} and {bcj['upper']:.3f}, with a wider statistical interval shown by the thin line. These are not deterministic price bounds. More training need not improve every finite run. The paper's high-dimensional results demonstrate a useful approach, rather than proving that regression methods cannot work there."
        ) as vo:
            self.play(FadeIn(g), FadeIn(marks[0]))
            self.play(FadeIn(marks[1]))
            vo.wait_until("a")
            self.wait(0.3)
            vo.wait_until("b")
            self.play(FadeIn(bc), FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def lab(self, s):
        card = house_lab(r"one exercise date", D.deep_stopping, "for it in range(steps):", 9)
        card.to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.6)
        d2, d5 = s["2"], s["5"]
        outs = [f"d=2: policy mean {d2['lower']:.3f} +/- {2 * d2['se']:.3f}   binomial {d2['reference']['binomial']:.3f}",
                f"d=5: policy mean {d5['lower']:.3f} +/- {2 * d5['se']:.3f}"]
        with self.voiceover(
            "This excerpt trains one date's soft stopping objective using the already-trained later rules. <bookmark mark='a'/> The final hard policy is evaluated on a million fresh paths. Its reported standard error is conditional on the trained policy and the simulation model; it does not measure variation across training runs or establish that the policy is optimal."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        import math
        p = D.MAX_CALL
        dt = p["T"] / p["N"]
        cont_lb = 130 * math.exp(-p["div"] * dt) * (1 + math.erf(p["sigma"] * math.sqrt(dt) / 2)) - p["K"] * math.exp(-p["r"] * dt)
        q = ask(r"both assets at 130, one date before expiry. Stop or wait?")
        with self.voiceover(
            'Pause and predict in this specified two-independent-asset model. Both prices are a hundred and thirty, with one exercise date left before maturity. Is the learned valley alone a proof that waiting is better? Compare the conditional continuation payoff with immediate exercise.'
        ):
            self.play(FadeIn(q))
        self.wait(2.5)
        answer = MathTex(rf"\mathbb E[e^{{-r\Delta t}}(\max S_T-K)^+\mid S_1=S_2=130]"
                         rf"\ge {cont_lb:.2f}>30", font_size=25, color=GOOD).next_to(q, UP, buff=0.3)
        with self.voiceover(f'Waiting is better here. The positive-part terminal payoff is at least the maximum asset price minus the strike. With these independent lognormal assets and one-third year remaining, the discounted expectation of that simpler payoff is {cont_lb:.2f}, already above the immediate thirty. This analytic comparison proves the decision within the specified model. A qualitative valley or a learned rule alone would not. Dividends, dependence and the time interval matter. Next: the deep hedger.'):
            self.play(FadeIn(answer))
        self.wait(3)
        self.clear_scene()
