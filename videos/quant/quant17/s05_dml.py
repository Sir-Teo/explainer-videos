from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import deep as D
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, ask, house_lab, illustration, load


class DML(VoiceoverScene):
    def construct(self):
        d = load("dml")
        self.card()
        self.idea(d)
        self.arrows(load("dml_replay"))
        self.replay(load("dml_replay"), load("dml_seeds"))
        self.errors(d, load("dml_seeds"))
        self.lab(d, load("dml_seeds"))

    def card(self):
        c = chapter_card(6, r"Differential machine learning", r"What if every training label came with its derivatives?",
                         part=PART)
        with self.voiceover("Chapter six. Differential machine learning."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def idea(self, d):
        rows = [cmath(r"Y", r"=", r"(w\cdot X_T - K)^+,\qquad X_T = X + \sqrt{T}\,L Z", font_size=38, colors={r"Y": OPT}),
                cmath(r"\partial_X Y", r"=", r"\mathbf{1}\{w\cdot X_T > K\}\, w", font_size=38, colors={r"\partial_X Y": GOOD}),
                cmath(r"\mathbb{E}[\partial_X Y \mid X]", r"=", r"\partial_X \mathbb{E}[Y \mid X] = \nabla V(X)", font_size=38,
                      colors={r"\mathbb{E}[\partial_X Y \mid X]": GOOD}),
                cmath(r"\mathcal{L}", r"=", r"\tfrac{1}{1+\lambda}\Big[(f(x) - y)^2 + \lambda \textstyle\sum_j \omega_j"
                      r"\big(\partial_j f(x) - \partial_j y\big)^2\Big]", font_size=36, colors={r"\mathcal{L}": NET})]
        whys = [why(rf"a desk's training example: from a state $X$ of {d['d']} correlated assets, simulate one payoff $Y$. "
                    r"Noisy, but its expectation given $X$ is the price $V(X)$"),
                why(r"the pathwise derivative, by the chain rule along the simulated path; adjoint differentiation (Part 16) "
                    r"returns all $d$ of them for a small constant multiple of one pricing"),
                why(r"and it is unbiased: $Y$ is Lipschitz in $X$, so by dominated convergence derivative and expectation "
                    r"commute. Each sample carries $1 + d$ honest labels, not one"),
                why(r"Huge and Savine (2020): fit the network to both, by differentiating the network itself (the "
                    r"'twin network': its backward pass is part of the model); $\omega_j$ puts each input on one scale")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.5, buff=0.62, edge=6.9)
        with self.voiceover(
            "Chapter one's network learned from exact prices. A real desk has simulations: a starting state and one "
            "simulated payoff, noisy but right on average. <bookmark mark='a'/> Brian Huge and Antoine Savine at Danske "
            "Bank noticed what else the desk has: the payoff's derivative with respect to every input, along the path, "
            "which adjoint differentiation from Part sixteen computes almost for free. <bookmark mark='b'/> And these derivatives are honest labels. The payoff is Lipschitz "
            "in the starting state, so the derivative and the expectation can be swapped: the average pathwise "
            "derivative is exactly the delta. <bookmark mark='c'/> So fit the network to the payoffs and to their "
            "derivatives together, by differentiating the network itself. The test: a basket option on "
            f"{d['d']} assets with normal dynamics, where the right answer is known exactly."
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

    def arrows(self, r):
        u = np.asarray(r["u"])
        g = axes([-30, 30], [0, 32], x_length=7.4, y_length=4.4, xlabel=r"basket level relative to the strike",
                 ylabel=r"basket call price", xticks=[-20, 0, 20], yticks=[0, 10, 20, 30],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        B, Y, dB = (np.asarray(r[k]) for k in ("scatter_B", "scatter_Y", "scatter_dY"))
        keep = (B > -30) & (B < 30) & (Y < 32)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.03, color=GREY_C) for x, y in zip(B[keep], Y[keep])])
        arr = VGroup()
        for x, y, sl in zip(B[keep], Y[keep], dB[keep]):
            h = 2.2
            y0, y1 = y - sl * h, y + sl * h
            if 0 <= y0 <= 32 and 0 <= y1 <= 32:
                arr.add(Line(ax.c2p(x - h, y0), ax.c2p(x + h, y1), stroke_color=GOOD, stroke_width=1.6,
                             stroke_opacity=0.7))
        ex = DashedVMobject(curve(ax, u, np.asarray(r["exact"]), REF, stroke_width=2.5), num_dashes=40)
        leg = legend([(GREY_C, r"one simulated payoff per state"), (GOOD, r"its pathwise slope"),
                      (REF, r"the exact price")], font_size=17).next_to(g, RIGHT, buff=0.4).align_to(g, UP)
        side = wrapped_label(r"along equal moves of all seven assets the pathwise slope is 1 if the basket finishes in the "
                             r"money and 0 if not; averaged, it is the price's slope", 4.0, 19, GREY_A).next_to(
            leg, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "See the two kinds of label. A slice through the seven-dimensional price, along equal moves in every "
            "asset. The grey dots are payoffs: each one a single simulation, scattered far from the price. "
            "<bookmark mark='a'/> Now give each dot its pathwise slope. Along this slice the slope is one if the basket "
            "finished in the money and zero if not: crude, but its average is the slope of the price. The slopes carry "
            "the shape far more clearly than the dots carry the level."
        ) as vo:
            self.play(FadeIn(g), Create(ex), FadeIn(leg[2]), FadeIn(dots, lag_ratio=0.01), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a_) for a_ in arr], lag_ratio=0.005, run_time=3), FadeIn(leg[1]),
                      FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, r, sd):
        u = np.asarray(r["u"])
        ex = np.asarray(r["exact"])
        ck = [str(c) for c in r["checkpoints"]]
        ep = np.array([c[0] for c in r["diff"]["curve"]])
        runs = [np.array([c[1] for c in r["diff"]["curve"]])]
        for row in sd["rows"]:
            if row["n"] == 1024 and row["differential"]:
                runs.append(np.array([c[1] for c in row["curve"]]))

        def frame(i):
            g = axes([-30, 30], [0, 32], x_length=5.0, y_length=3.6, xlabel=r"basket level $-$ strike",
                     ylabel=r"price", xticks=[-20, 0, 20], yticks=[0, 15, 30], font_size=13)
            return VGroup(g, DashedVMobject(curve(g.ax, u, ex, REF, stroke_width=2.2), num_dashes=36),
                          curve(g.ax, u, np.clip(np.asarray(r["plain"]["snaps"][ck[i]]), 0, 32), BAD, stroke_width=3),
                          curve(g.ax, u, np.clip(np.asarray(r["diff"]["snaps"][ck[i]]), 0, 32), GOOD, stroke_width=3.5))
            # the replay prints the step above the loss curve; one counter is enough
        rp = TrainingReplay(ep, np.array(runs), frame, checkpoints=[1] + [int(c) for c in ck[1:]],
                            ylabel=r"value loss (normalized)", xlabel=r"epoch", log_y=True, color=GOOD)
        leg = legend([(REF, r"exact"), (BAD, r"payoffs only"), (GOOD, r"payoffs and slopes"),
                      (GOOD, r"right: differential fit, three seeds")], font_size=16).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now train both networks on the same thousand and twenty-four samples and watch them, checkpoint by "
            "checkpoint. Red is fitted to payoffs only, green to payoffs and slopes. <bookmark mark='a'/> Both start "
            "flat. The green one finds the shape almost at once, because every sample tells it which way the price is "
            "sloping. The red one has only the noisy levels, and wanders before it settles, never quite on the price "
            "where the payoffs are largest and noisiest."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 4))
        self.wait(0.4)
        self.clear_scene()

    def errors(self, d, sd):
        allrows = d["rows"] + sd["rows"]
        ns = [256, 1024, 4096]

        def vals(n, use, key):
            return [r[key] for r in allrows if r["n"] == n and r["differential"] == use]
        g1 = axes([np.log10(ns[0]) - 0.2, np.log10(16384) + 0.2], [-1.4, 1.0], x_length=5.2, y_length=3.6,
                  xlabel=r"training samples", ylabel=r"price error (RMSE)", xticks=list(np.log10(ns + [16384])),
                  xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yticks=[-1, 0, 1],
                  yfmt=lambda v: f"10^{{{int(round(v))}}}", font_size=14)
        g2 = axes([np.log10(ns[0]) - 0.2, np.log10(16384) + 0.2], [-3, 0], x_length=5.2, y_length=3.6,
                  xlabel=r"training samples", ylabel=r"delta error (RMSE)", xticks=list(np.log10(ns + [16384])),
                  xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yticks=[-3, -2, -1, 0],
                  yfmt=lambda v: f"10^{{{int(round(v))}}}", font_size=14)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).shift(DOWN * 0.3)
        lines = VGroup()
        for g, key, lo, hi in ((g1, "price_rmse", -1.4, 1.0), (g2, "delta_rmse", -3, 0)):
            for use, col in ((False, BAD), (True, GOOD)):
                xs = np.log10(ns)
                runs = np.array([np.clip(np.log10(sorted(vals(n, use, key))), lo, hi) for n in ns]).T
                band_ = seed_band(g.ax, xs, runs, col, stroke_width=3)
                big = vals(16384, use, key)[0]
                lines.add(VGroup(band_,
                                 Dot(g.ax.c2p(np.log10(16384), np.clip(np.log10(big), lo, hi)), radius=0.07, color=col)))
        leg = legend([(BAD, r"payoffs only"), (GOOD, r"payoffs and slopes"),
                      (GREY_B, r"band: three seeds (fresh data and weights); dot: one seed")], font_size=17).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        p256, d256 = vals(256, False, "price_rmse"), vals(256, True, "price_rmse")
        q256, e256 = vals(256, False, "delta_rmse"), vals(256, True, "delta_rmse")
        gain = float(np.mean(q256) / np.mean(e256))
        cached = d["rows"][0]["price_rmse"]
        others = [v for v in p256 if v != cached]
        if cached > 2 * max(others):
            verdict = "the first seed's large error was one bad fit; the other seeds did far better without slopes, " \
                      "but still worse than with them"
        else:
            verdict = "every seed tells the same story"
        foot = wrapped_label(rf"256 samples: price error {min(p256):.2f} to {max(p256):.2f} without slopes, {min(d256):.2f} to "
                             rf"{max(d256):.2f} with them; deltas {gain:.0f} times more accurate on average", 11.8, 20,
                             GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And the error as the training set grows, for the price on the left and the deltas on the right, now with "
            "three seeds at each size: different samples, different starting weights. <bookmark mark='a'/> With two "
            f"hundred and fifty-six samples the plain network's price error ranges from {min(p256):.2f} to "
            f"{max(p256):.2f} across seeds; with slopes, {min(d256):.2f} to {max(d256):.2f}. So {verdict}. The deltas are "
            f"{gain:.0f} times more accurate on average. For a risk system the derivatives are not decoration; they are "
            "the point."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(leg))
            vo.wait_until("a")
            self.play(*[FadeIn(l_) for l_ in lines], FadeIn(foot), run_time=2.5)
        self.wait(0.5)
        self.clear_scene()

    def lab(self, d, sd):
        card = house_lab(r"the twin loss", D.train_differential, "xb = Xn[j].requires_grad_(use_d)", 9, width=8.6)
        card.to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.6)
        rows = [r for r in d["rows"] + sd["rows"] if r["n"] == 1024]
        outs = []
        for use, nm in ((False, "plain       "), (True, "differential")):
            pr = [r["price_rmse"] for r in rows if r["differential"] == use]
            de = [r["delta_rmse"] for r in rows if r["differential"] == use]
            outs.append(f"n=1024 {nm}: price rmse {np.mean(pr):.3f}   delta rmse {np.mean(de):.4f}   (3 seeds)")
        with self.voiceover(
            "The House's twin loss: the value error, then the network's own input gradient, kept in the graph so "
            "training can differentiate through it, scored against the pathwise slopes. <bookmark mark='a'/> At a "
            "thousand and twenty-four samples, over three seeds:"
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        q = ask(r"price a digital option this way. What is the pathwise derivative of a digital's payoff?")
        with self.voiceover(
            "A question to take into the next chapter: what would the slopes say if the payoff were a digital, which "
            "pays one or nothing?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
