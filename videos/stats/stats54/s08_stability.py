from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class Stability(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.ridge()
        self.chart()
        self.privacy()
        self.sgd()
        self.sgd_chart()

    def card(self):
        card = chapter_card(7, r"Stability", r"Generalization from the algorithm, \ not the class", lit=(2002,), part=PART)
        with self.voiceover("Chapter seven. Stability: generalization from the algorithm, not the class."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        rows = [
            cmath(r"A: S \mapsto h_S", r":", r"\text{a learning algorithm}", font_size=36),
            cmath(r"\beta\text{-uniform stability}", r":", r"\sup_{S, i, z} |\ell(h_S, z) - \ell(h_{S^{(i)}}, z)| \le \beta", font_size=32),
            cmath(r"E[R(h_S) - R_n(h_S)]", r"\le", r"\beta: \ \text{the generalization gap}", font_size=36),
            cmath(r"\text{w.h.p.}", r":", r"R(h_S) \le R_n(h_S) + \beta + (2n\beta + M)\sqrt{\log(1/\delta)/(2n)}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"no class needed"), why(r"replace one point"), why(r"Bousquet \& Elisseeff (2002)"), why(r"McDiarmid")]
        heading = label('Uniform loss stability bounds the expected generalization gap', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A different route to generalization looks at the algorithm instead of the class. <bookmark "
            "mark='b'/> An algorithm is beta-uniformly stable if replacing any one training point changes the loss of its "
            "output on any example by at most beta. <bookmark mark='c'/> Olivier Bousquet and André Elisseeff showed in 2002 "
            "that the expected gap between true and empirical risk is then at most beta: <bookmark mark='d'/> and with "
            "McDiarmid's inequality, a high-probability bound, useful when beta is of order one over n. An algorithm that "
            "does not depend much on any single example cannot overfit any single example."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ridge(self):
        rows = [
            cmath(r"\hat w", r"=", r"\arg\min \tfrac1n\textstyle\sum(y_i - \langle w, x_i\rangle)^2 + \lambda\|w\|^2", font_size=34),
            cmath(r"\lambda\text{-strong convexity}", r"\Rightarrow", r"\|\hat w_S - \hat w_{S^{(i)}}\| \lesssim \frac{L R}{\lambda n}", font_size=34),
            cmath(r"\beta", r"\lesssim", r"\frac{L^2R^2}{\lambda n}: \ \text{stable, \ at rate } 1/n", font_size=36),
            cmath(r"\text{the trade-off}", r":", r"\text{larger } \lambda: \ \text{more stable, \ more biased}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Tikhonov regularization"), why(r"one point moves the minimizer little"), why(r"$R$: \ data radius"), why(r"as ever")]
        heading = label('Ridge loss stability needs bounded data and a controlled loss slope', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Ridge regression is the model case. <bookmark mark='b'/> Its objective is lambda-strongly "
            "convex, so replacing one of n points moves the minimizer by at most a constant over lambda n. <bookmark "
            "mark='c'/> Its stability is therefore of order L squared R squared over lambda n, with R the data's radius: "
            "stable at the rate one over n. <bookmark mark='d'/> Larger lambda buys more stability at the price of more bias, "
            "the same trade-off in a new language."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("stability")
        ll = np.log10([r["lam"] for r in d["rows"]])
        vals = np.arcsinh(np.array([[r["stability"], r["gap"]] for r in d["rows"]])/.001)
        low, high = np.floor(vals.min())-.3, np.ceil(vals.max())+.3
        A = axes([-3.2, 0.7], [low, high], x_length=7.4, y_length=4.4, xlabel=rf"ridge penalty $\lambda$ \ (log scale), \ $n = {d['n']}$, \ $p = {d['p']}$", ylabel=r"$\mathrm{asinh}(\mathrm{loss}/0.001)$",
                 xticks=[-3, -2, -1, 0], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=list(np.arange(np.ceil(low), high, 1)), center=[-2.5, 0.2, 0])
        ax = A.ax
        st = np.arcsinh(np.array([r["stability"] for r in d["rows"]]) / .001)
        gp = [r["gap"] for r in d["rows"]]
        cs = VGroup(polyline(ax, ll, st, BOUNDC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=BOUNDC) for a, b in zip(ll, st)])
        cg = VGroup(*[Dot(ax.c2p(a, np.arcsinh(g/.001)), radius=0.1, color=TESTC) for a, g in zip(ll, gp)])
        r = d["rows"]
        side = fit_rows(VGroup(
            label(r"bounded ridge; \ sampled replacement loss diagnostic", font_size=22),
            label(rf"purple: \ sampled loss change, \ {r[0]['stability']:.2f} at $\lambda = 10^{{-3}}$, \ {r[-1]['stability']:.4f} at 3", font_size=22, color=BOUNDC),
            label(rf"blue: \ the test--train gap, \ {r[0]['gap']:.3f} to {r[3]['gap']:.3f}", font_size=22, color=TESTC),
            label(r"sampled changes do not certify uniform stability", font_size=22, color=GOODC),
            label(r"signed scale retains negative gaps; \ 10 datasets", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here the design and responses are bounded. For each dataset we refit twenty sampled neighbouring datasets, and measure the largest squared-loss change on two thousand validation points. <bookmark mark='b'/> Purple averages that sampled diagnostic over ten datasets. It is not the supremum defining uniform stability. <bookmark mark='c'/> Blue shows the average test-minus-training loss, with negative values retained on this signed axis. <bookmark mark='d'/> Both tend to shrink as regularization increases, but the theorem does not force the observed gap to track this diagnostic. <bookmark mark='e'/> Monte Carlo standard errors and a conservative theoretical uniform bound are retained with the numerical inputs."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cg), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def privacy(self):
        rows = [
            cmath(r"\varepsilon\text{-differential privacy}", r":", r"\text{changing one record changes the output's law by } e^{\varepsilon}", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\text{stability: \ } |E R - E R_n| \lesssim e^\varepsilon - 1", font_size=34),
            cmath(r"\text{adaptive data analysis}", r":", r"\text{private mechanism, accuracy and query budget required}", font_size=34),
            cmath(r"\text{the reusable holdout}", r":", r"\text{Dwork et al. (2015)}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        whys = [why(r"Part 63"), why(r"privacy implies generalization"), why(r"the garden of forking paths"), why(r"\emph{Science}")]
        heading = label('Privacy generalization and holdout reuse require explicit assumptions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Pure differential privacy bounds output probabilities under replacement of one record by a factor e to epsilon. <bookmark mark='b'/> For independent data and losses in zero to one, it yields an expected generalization-gap bound of order e to epsilon minus one, useful for small epsilon. It is distributional stability, not a claim that coupled outputs are always close. <bookmark mark='c'/> Private mechanisms can also help control adaptive reuse of a holdout. <bookmark mark='d'/> Dwork and colleagues' reusable holdout needs a specified mechanism, accuracy and query budget, and privacy accounting. Repeated arbitrary access is not made safe by the name alone."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sgd(self):
        rows = fit_rows(VGroup(
            label(r"stability reaches where uniform convergence cannot:", font_size=28, color=GREY_A),
            label(r"SGD: convex, smooth, Lipschitz; \ suitable steps; \ expected \ $\beta \lesssim T\eta/n$ \ (Hardt, \ Recht \& Singer 2016)", font_size=26, color=GOODC),
            label(r"early stopping is regularization: \ fewer steps, \ more stable", font_size=26, color=CLASSC),
            label(r"some neighbour and bagged rules: \ distributional stability assumptions", font_size=26, color=TESTC),
            label(r"the leave-one-out error estimates the risk of stable algorithms (Part 28)", font_size=26, color=BOUNDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Stability can exploit the training algorithm. <bookmark mark='b'/> For convex Lipschitz smooth losses, suitable step sizes and independent uniform index sampling, the expected stability of coupled SGD is controlled by the summed step sizes over n. This is an expectation over algorithmic randomness. <bookmark mark='c'/> Early stopping limits that upper bound; it does not prove that every later iterate generalizes worse. <bookmark mark='d'/> Some nearest-neighbour or bagged procedures admit other forms of stability under distributional assumptions. Ordinary one-nearest-neighbour is not uniformly stable in general. <bookmark mark='e'/> Appropriate stability assumptions also support leave-one-out risk estimation."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sgd_chart(self):
        d = load("sgd")
        t = np.asarray(d["t"])
        A = axes([0, d["steps"]], [-2.5, 1.5], x_length=7.4, y_length=4.4, xlabel=rf"SGD steps \ ($n = {d['n']}$: \ 200 steps per epoch)",
                 ylabel=r"$\log_{10}\|w_t - w_t'\|$", xticks=[0, 500, 1000, 1500, 2000], yticks=[-2, -1, 0, 1], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.5, 0.2, 0])
        ax = A.ax
        a, b = d["0.2"], d["1.0"]
        da = polyline(ax, t, np.log10(np.where(np.array(a["div"])>0, a["div"], np.nan)), TESTC, 4)
        ba = DashedVMobject(polyline(ax, t, np.log10(a["bound"]), TESTC, 3), num_dashes=40)
        db = polyline(ax, t, np.log10(np.where(np.array(b["div"])>0, b["div"], np.nan)), CLASSC, 4)
        bb = DashedVMobject(polyline(ax, t, np.log10(b["bound"]), CLASSC, 3), num_dashes=40)
        side = fit_rows(VGroup(
            label(rf"logistic SGD on two samples differing in one point", font_size=22),
            label(rf"blue: \ step size 0.2: \ divergence {a['div'][-1]:.2f} \ (bound {a['bound'][-1]:.0f})", font_size=22, color=TESTC),
            label(rf"gold: \ step size 1: \ divergence {b['div'][-1]:.2f} \ (bound {b['bound'][-1]:.0f})", font_size=22, color=CLASSC),
            label(r"dashed: \ $2\eta t/n$, \ bound on the expectation", font_size=22, color=GREY_A),
            label(r"40 coupled runs; \ stored pointwise Monte Carlo errors", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is the theorem at work. Run stochastic gradient descent for logistic regression on two samples of two hundred that differ in a single point, with the same independent uniform index stream, averaged over forty coupled runs, and measure how far apart the two parameter vectors drift. <bookmark mark='b'/> With step size a fifth, the divergence after ten epochs is {say(a['div'][-1], 2)}. <bookmark mark='c'/> With step size one, it is {say(b['div'][-1], 2)}. <bookmark mark='d'/> The dashed lines bound the expected divergence over algorithmic randomness. They are not pathwise bounds, two times the step size times the number of steps over n: under the bounded logistic smoothness conditions, and loose in this example. <bookmark mark='e'/> The bound grows with every step; the real divergence levels off after an epoch or two, because the data's curvature keeps pulling the two runs together, which a worst-case argument cannot see. What the bound does get right is the larger step's larger price, and that without strong convexity, it is the number of steps that must be limited: early stopping."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ 40 replications")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(da), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(db), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ba), Create(bb), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
