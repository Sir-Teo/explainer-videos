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
            cmath(r"\text{w.h.p.}", r":", r"R(h_S) \le R_n(h_S) + \beta + (n\beta + M)\sqrt{\log(1/\delta)/(2n)}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"no class needed"), why(r"replace one point"), why(r"Bousquet \& Elisseeff (2002)"), why(r"McDiarmid")]
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
        A = axes([-3.2, 0.7], [-3.0, 0.0], x_length=7.4, y_length=4.4, xlabel=rf"ridge penalty $\lambda$ \ (log scale), \ $n = {d['n']}$, \ $p = {d['p']}$", ylabel=r"$\log_{10}$",
                 xticks=[-3, -2, -1, 0], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[-3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        st = np.log10([r["stability"] for r in d["rows"]])
        gp = [r["gap"] for r in d["rows"]]
        cs = VGroup(polyline(ax, ll, st, BOUNDC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=BOUNDC) for a, b in zip(ll, st)])
        pos = [(a, g) for a, g in zip(ll, gp) if g > 0]
        cg = VGroup(*[Dot(ax.c2p(a, np.log10(g)), radius=0.1, color=TESTC) for a, g in pos])
        r = d["rows"]
        side = fit_rows(VGroup(
            label(r"ridge regression, \ replace-one stability by refitting", font_size=22),
            label(rf"purple: \ stability, \ {r[0]['stability']:.2f} at $\lambda = 10^{{-3}}$, \ {r[-1]['stability']:.4f} at 3", font_size=22, color=BOUNDC),
            label(rf"blue: \ the test--train gap, \ {r[0]['gap']:.3f} to {r[3]['gap']:.3f}", font_size=22, color=TESTC),
            label(r"the gap tracks the stability", font_size=22, color=GOODC),
            label(r"(gaps below zero at large $\lambda$ not shown)", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Ridge regression with two hundred points and fifty features, stability measured by "
            f"refitting with one point replaced. <bookmark mark='b'/> As lambda grows from a thousandth to three, the "
            f"stability falls from {say(r[0]['stability'], 2)} to {say(r[-1]['stability'], 4)}. <bookmark mark='c'/> The gap "
            f"between test and training error, in blue, falls from {say(r[0]['gap'], 3)} to {say(r[3]['gap'], 3)} at a "
            f"tenth. <bookmark mark='d'/> The gap tracks the stability, as the theorem says it must. <bookmark mark='e'/> At "
            f"the largest penalties the gap is lost in noise."
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
            cmath(r"\text{adaptive data analysis}", r":", r"\text{reuse a holdout many times, \ safely}", font_size=34),
            cmath(r"\text{the reusable holdout}", r":", r"\text{Dwork et al. (2015)}", font_size=34),
        ]
        rows[1][-1].set_color(GOODC)
        whys = [why(r"Part 63"), why(r"privacy implies generalization"), why(r"the garden of forking paths"), why(r"\emph{Science}")]
        with self.voiceover(
            "<bookmark mark='a'/> A surprising source of stability is privacy. An algorithm is epsilon differentially private if changing one record changes the distribution of its output by at most a factor e to the epsilon, Part sixty-three's subject. <bookmark mark='b'/> That is a strong form of stability, so private algorithms generalize. <bookmark mark='c'/> It solves a practical problem, adaptive data analysis, where an analyst queries the same holdout set repeatedly and would otherwise overfit it, as in Part thirty-three's garden of forking paths. <bookmark mark='d'/> Cynthia Dwork and colleagues' reusable holdout of 2015 answers each query through a private mechanism, so the holdout stays honest."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sgd(self):
        rows = fit_rows(VGroup(
            label(r"stability reaches where uniform convergence cannot:", font_size=28, color=GREY_A),
            label(r"SGD on convex, \ smooth losses: \ stable, \ $\beta \lesssim T\eta/n$ \ (Hardt, \ Recht \& Singer 2016)", font_size=26, color=GOODC),
            label(r"early stopping is regularization: \ fewer steps, \ more stable", font_size=26, color=CLASSC),
            label(r"nearest-neighbour and bagged rules: \ stability without a finite VC class", font_size=26, color=TESTC),
            label(r"the leave-one-out error estimates the risk of stable algorithms (Part 28)", font_size=26, color=BOUNDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Stability reaches places uniform convergence cannot. <bookmark mark='b'/> Moritz Hardt, "
            "Benjamin Recht and Yoram Singer showed in 2016 that stochastic gradient descent on convex smooth losses is stable, "
            "with beta of order the number of steps times the step size over n. <bookmark mark='c'/> So stopping early is a "
            "form of regularization: fewer steps, more stability. <bookmark mark='d'/> Nearest-neighbour rules and bagged "
            "predictors are stable without belonging to any small class. <bookmark mark='e'/> And for stable algorithms, the "
            "leave-one-out error of Part twenty-eight is a reliable estimate of the risk."
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
        da = polyline(ax, t, np.log10(a["div"]), TESTC, 4)
        ba = DashedVMobject(polyline(ax, t, np.log10(a["bound"]), TESTC, 3), num_dashes=40)
        db = polyline(ax, t, np.log10(b["div"]), CLASSC, 4)
        bb = DashedVMobject(polyline(ax, t, np.log10(b["bound"]), CLASSC, 3), num_dashes=40)
        side = fit_rows(VGroup(
            label(rf"logistic SGD on two samples differing in one point", font_size=22),
            label(rf"blue: \ step size 0.2: \ divergence {a['div'][-1]:.2f} \ (bound {a['bound'][-1]:.0f})", font_size=22, color=TESTC),
            label(rf"gold: \ step size 1: \ divergence {b['div'][-1]:.2f} \ (bound {b['bound'][-1]:.0f})", font_size=22, color=CLASSC),
            label(r"dashed: \ $2\eta t/n$, \ linear in the steps", font_size=22, color=GREY_A),
            label(r"bigger steps: \ less stable; \ the truth levels off", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is the theorem at work. Run stochastic gradient descent for logistic regression on "
            f"two samples of two hundred that differ in a single point, with the same random order, and measure how far apart "
            f"the two parameter vectors drift. <bookmark mark='b'/> With step size a fifth, the divergence after ten epochs is "
            f"{say(a['div'][-1], 2)}. <bookmark mark='c'/> With step size one, it is {say(b['div'][-1], 2)}. <bookmark "
            f"mark='d'/> The dashed lines are Hardt, Recht and Singer's bounds, two times the step size times the number of "
            f"steps over n: valid, and loose. <bookmark mark='e'/> The bound grows with every step; the real divergence "
            f"levels off after an epoch or two, because the data's curvature keeps pulling the two runs together, which a "
            f"worst-case argument cannot see. What the bound does get right is the larger step's larger price, and that "
            f"without strong convexity, it is the number of steps that must be limited: early stopping."
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
