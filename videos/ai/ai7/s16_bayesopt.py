from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import HIDDEN, PART, card_in, load

GPC = HIDDEN
EI = C.BITS
OBS = C.MODEL_Q
TRUTH = GREY_C


class BayesOpt(VoiceoverScene):
    def construct(self):
        card_in(self, 15, r"Bayesian optimization", r"Where should we look next?",
                "Chapter fifteen. Bayesian optimization.")
        self.idea()
        self.replay()

    # ------------------------------------------------------------------
    def idea(self):
        b = load("bayesopt")
        colors = {r"\mu(x)": GPC, r"\sigma(x)": GPC, r"\mathrm{EI}(x)": EI}
        rows = [
            cmath(r"\mathrm{EI}(x)", r"=", r"\mathbb{E}\big[\max(f_{\mathrm{best}} - f(x),\; 0)\big]", colors=colors,
                  font_size=38),
            cmath(r"\mathrm{EI}(x)", r"=", r"(f_{\mathrm{best}} - \mu(x))\, \Phi(z)", r"+", r"\sigma(x)\, \varphi(z)",
                  colors=colors, font_size=38),
        ]
        whys = [why(r"how much better than the best so far, \\ on average, under the GP"),
                why(r"$z = (f_{\mathrm{best}} - \mu(x)) / \sigma(x)$: \\ exploit a low mean, \ explore a wide band")]
        step = ladder(self, rows, whys, keep=2, top=0.6, x=-2.6, buff=0.75, edge=6.8)
        prob = VGroup(label(r"the knob: \ Kneser--Ney's discount $D$, \ one for every order", font_size=26),
                      label(rf"the score: \ bits per character on ${b['valid_chars']:,}$ held-out characters".replace(",", "{,}"),
                            font_size=26),
                      label(r"each try: \ build and score a model \ (seconds here; \ days for a large network)",
                            font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        prob.scale(1.25).move_to(UP * 0.5)
        hist = VGroup(history_card(1975, r"Jonas Mockus", r"the Bayesian approach to global optimization", width=4.2),
                      history_card(1998, r"D.~Jones, M.~Schonlau \& W.~Welch", r"expected improvement", width=4.2),
                      history_card(2012, r"J.~Snoek, H.~Larochelle \& R.~Adams", r"tuning machine learning", width=4.2))
        hist.arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Every model in this series has knobs. Here's one: Kneser–Ney's discount, D, a single value for every "
            "order. Each try means building a model and scoring it on held-out text: seconds here, but days for a "
            "large network. So we want the best D in as few tries as possible. <bookmark mark='a'/> Bayesian "
            "optimization puts a Gaussian process on the unknown score, and asks, at every candidate, how much "
            "better than the best so far we can expect it to be. <bookmark mark='b'/> For a Gaussian the answer has a "
            "formula, the expected improvement. One term rewards a low predicted score: exploit. The other rewards a "
            "wide band: explore. <bookmark mark='c'/> Jonas Mockus proposed the approach in the 1970s; Donald Jones "
            "and colleagues made expected improvement standard in 1998; and in 2012 Jasper Snoek and colleagues "
            "showed it tuning neural networks better than experts."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p_) for p_ in prob], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("a")
            self.play(prob.animate.scale(0.8).to_edge(UP, buff=0.4))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.2) for h in hist], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        b = load("bayesopt")
        cand, grid, truth = np.asarray(b["cand"]), np.asarray(b["grid"]), np.asarray(b["truth"])
        means, sds, eis = np.asarray(b["steps_mean"]), np.asarray(b["steps_sd"]), np.asarray(b["steps_ei"])
        sx, sy, nxt = b["steps_x"], b["steps_y"], b["steps_next"]
        ylo = float(truth.min()) - 0.01
        yhi = float(np.percentile(truth, 90)) + 0.01
        g = axes([0, 1, 0.2], [ylo, yhi, 0.02], x_length=8.0, y_length=3.6, ylabel=r"bits per character (held out)",
                 yticks=[round(v, 2) for v in np.linspace(ylo + 0.005, yhi - 0.005, 3)], center=[-1.9, 1.0, 0])
        ax = g.ax
        ge = axes([0, 1, 0.2], [0, 1, 0.5], x_length=8.0, y_length=1.3, xlabel=r"the discount $D$",
                  ylabel=r"relative EI (peak $1$)", xticks=[0, 0.25, 0.5, 0.75, 1.0], center=[-1.9, -2.3, 0])
        ae = ge.ax
        tr = DashedVMobject(curve(ax, grid, np.clip(truth, ylo, yhi), TRUTH, 2), num_dashes=60)
        trl = label(r"the true curve: \\ $31$ evaluations, \\ never shown to the optimizer", font_size=18, color=TRUTH)
        trl.move_to([4.9, 2.1, 0])
        k = ValueTracker(0)

        def state():
            i = min(int(round(k.get_value())), len(means) - 1)
            m, s_ = means[i], sds[i]
            lo, hi = np.clip(m - 2 * s_, ylo, yhi), np.clip(m + 2 * s_, ylo, yhi)
            bandp = band(ax, cand, lo, hi, GPC, 0.3)
            mc = curve(ax, cand, np.clip(m, ylo, yhi), WHITE, 3)
            pts = VGroup(*[Dot(ax.c2p(x_, min(y_, yhi)), radius=0.08, color=OBS) for x_, y_ in zip(sx[i], sy[i])])
            e = eis[i] / max(eis[i].max(), 1e-12)
            ec = VGroup(band(ae, cand, np.zeros_like(e), e, EI, 0.35), curve(ae, cand, e, EI, 3))
            nl = DashedLine(ae.c2p(nxt[i], 0), ax.c2p(nxt[i], yhi), color=EI, stroke_width=2)
            return VGroup(bandp, mc, pts, ec, nl)

        st = always_redraw(state)
        nv = Integer(len(sx[0]), font_size=30)
        nl_ = VGroup(label(r"evaluations:", font_size=24, color=GREY_A), nv).arrange(RIGHT, buff=0.15).move_to([4.9, 0.6, 0])
        found = VGroup(label(rf"best found: \ $D = {b['best_D']:.2f}$, \ ${b['best_bits']:.4f}$ bits", font_size=22,
                             color=OBS),
                       label(rf"grid of ${b['grid_evals']}$: \ $D = {b['grid_best_D']:.2f}$, \ ${b['grid_best_bits']:.4f}$",
                             font_size=22, color=TRUTH),
                       label(rf"the counts-of-counts discounts: \ ${b['gt_bits']:.4f}$", font_size=22, color=C.COUNTING))
        found.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.7, -0.6, 0])
        if found.get_right()[0] > 6.9:
            found.shift(LEFT * (found.get_right()[0] - 6.9))
        close = abs(b["best_bits"] - b["grid_best_bits"]) < 0.001
        tuned = b["best_bits"] < b["gt_bits"]
        verdict = (f"After {b['evals']} evaluations it has found D = {b['best_D']:.2f}, scoring {b['best_bits']:.4f} "
                   f"bits, as good as a grid of {b['grid_evals']} evaluations. "
                   if close else
                   f"After {b['evals']} evaluations its best is D = {b['best_D']:.2f}, at {b['best_bits']:.4f} bits, "
                   f"against {b['grid_best_bits']:.4f} for a grid of {b['grid_evals']}. ")
        verdict2 = ("One tuned discount even beats the discounts estimated from counts of counts, "
                    f"{b['gt_bits']:.4f}: the formula is a good guess, not the optimum." if tuned else
                    f"The discounts estimated from counts of counts do as well, {b['gt_bits']:.4f}.")
        with self.voiceover(
            "Here it runs. Two random tries to start. The grey band is the Gaussian process's belief about the "
            "score; the yellow curve below is expected improvement, rescaled to a peak of one at each step. "
            "Its peak is where to look next. "
            "<bookmark mark='a'/> Each new score lands, the band pinches there, and the next look moves. Mostly it "
            "heads for low scores, and now and then it checks a place where the band is still wide. "
            "<bookmark mark='b'/> " + verdict + " <bookmark mark='b2'/> " + verdict2 + " <bookmark mark='c'/> "
            "Exploring and exploiting is part twenty-six's bandit problem in another form. DeepMind tuned AlphaGo's "
            "settings this way before its 2016 match."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ge), FadeIn(st), FadeIn(nl_), Create(tr), FadeIn(trl))
            vo.wait_until("a")
            for i in range(1, len(means)):
                self.play(k.animate.set_value(i), ChangeDecimalToValue(nv, len(sx[i])), run_time=1.4)
                self.wait(0.6)
            vo.wait_until("b")
            self.play(FadeIn(found[0]), FadeIn(found[1]))
            self.play(FadeIn(found[2]))
            vo.wait_until("c")
            self.play(Indicate(found[0], color=OBS))
        st.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
