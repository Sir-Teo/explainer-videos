from __future__ import annotations

import numpy as np

from videos.stats.stats15.common import *  # noqa: F403


def trace(ax, ys, color, n=None):
    ys = np.asarray(ys)[:n]
    return VMobject(stroke_color=color, stroke_width=1.6).set_points_as_corners([ax.c2p(i, y) for i, y in enumerate(ys)])


class Metropolis(VoiceoverScene):
    def construct(self):
        self.card()
        self.algorithm()
        self.why_works()
        self.steps()
        self.reparam()
        self.burnin()
        self.answer()
        self.functions()

    def card(self):
        card = chapter_card(8, r"When grids fail", r"A Metropolis walk through the posterior", lit=(1953,), part=PART)
        with self.voiceover("Chapter eight. When grids fail."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def algorithm(self):
        rows = [
            cmath(r"\text{propose}", r":", r"\theta' = \theta + \text{step} \times Z,\quad Z \sim N(0, I)", font_size=32),
            cmath(r"r", r"=", r"\frac{\pi(\theta' \mid y)}{\pi(\theta \mid y)} = \frac{p(y \mid \theta')\pi(\theta')}{p(y \mid \theta)\pi(\theta)}", font_size=32),
            cmath(r"\text{accept}", r":", r"\theta \leftarrow \theta'\ \text{with probability } \min(1, r)", font_size=32),
            cmath(r"\text{record}", r":", r"\theta\ \text{(the new value, \ or the old one again)}", font_size=32),
        ]
        rows[1][2].set_color(POST)
        whys = [why(r"a random step from where we are"), why(r"the normalizing constant cancels!"),
                why(r"uphill always; \ downhill sometimes"), why(r"Metropolis et al.\ (1953), \ Part 7")]
        with self.voiceover(
            "Part 7 built a Markov chain whose long-run distribution is any target we like. Here's the target: the posterior. "
            "<bookmark mark='a'/> From the current point, propose a random step. <bookmark mark='b'/> Compute the ratio of the "
            "posterior at the proposal to the posterior here. The unknown normalizing constant, the integral we couldn't do, "
            "cancels: only likelihood times prior is needed. <bookmark mark='c'/> If the proposal is more probable, move there; "
            "if it's less probable, move there only with probability equal to the ratio. <bookmark mark='d'/> Record where you "
            "are, even if you stayed. That's the Metropolis algorithm of 1953, invented to simulate molecules at Los Alamos."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.8, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def why_works(self):
        rows = [
            cmath(r"\pi(\theta)\,q(\theta'\mid\theta)\,\alpha(\theta \to \theta')", r"=", r"\min\big(\pi(\theta),\ \pi(\theta')\big)\,q", font_size=30),
            cmath(r"\ ", r"=", r"\pi(\theta')\,q(\theta\mid\theta')\,\alpha(\theta' \to \theta)", font_size=30),
            cmath(r"\text{so}", r":", r"\pi \text{ is stationary (detailed balance, \ Part 7)}", font_size=30),
            cmath(r"\text{ergodic averages}", r"\to", r"\mathbb E[f(\theta) \mid y]", font_size=32),
        ]
        rows[2][2].set_color(POST)
        whys = [why(r"flow from $\theta$ to $\theta'$, \ symmetric $q$"), why(r"equals the flow back"),
                why(r"the posterior is the chain's long-run distribution"), why(r"Part 7's ergodic theorem")]
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> With a symmetric proposal, the probability flow from theta to theta prime, "
            "in equilibrium, is the smaller of the two posterior values times the proposal density. <bookmark mark='b'/> That's "
            "symmetric, so it equals the flow back. <bookmark mark='c'/> Detailed balance, from Part 7: the posterior is the "
            "chain's stationary distribution. <bookmark mark='d'/> So averages along the chain converge to posterior "
            "expectations, though successive draws are correlated, which is the price."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def steps(self):
        d = load("mcmc")["chains"]
        names = [("tiny", r"tiny steps", S.CTRL), ("good", r"good steps", S.LIK), ("huge", r"huge steps", RES)]
        g = VGroup()
        for k, (key, nm, c) in enumerate(names):
            A = axes([0, 1500], [-0.75, 0.15], x_length=7.6, y_length=1.5, xlabel=r"", ylabel=r"", xticks=[], yticks=[-0.6, -0.2],
                     center=[-1.4, 2.0 - 2.0 * k, 0])
            tr = trace(A.ax, d[key]["b1"], c)
            lab = VGroup(label(nm, font_size=24, color=c),
                         label(rf"acceptance {100 * d[key]['acc']:.0f}\%", font_size=20, color=GREY_A),
                         label(rf"ESS {d[key]['ess']:.0f} of 5,000", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            lab.next_to(A, RIGHT, buff=0.4)
            g.add(VGroup(A, tr, lab))
        head = label(r"traces of $\beta_1$: \ Challenger posterior, \ temperature centred at 70$^\circ$F", font_size=22, color=GREY_B).to_edge(UP, buff=0.2)
        with self.voiceover(
            "The step size matters, and trace plots show why. These are three chains on the Challenger posterior, each "
            "fifteen hundred steps of the slope. <bookmark mark='a'/> With tiny steps, nearly every proposal is accepted, but "
            "the chain creeps, wandering slowly: its five thousand draws are worth only about twelve independent ones, its "
            "effective sample size. <bookmark mark='b'/> With good steps, about forty-five percent are accepted and the trace "
            "looks like noise, the fuzzy caterpillar you want: an effective sample size of over two hundred. "
            "<bookmark mark='c'/> With huge steps, nearly every proposal lands somewhere improbable and is rejected; the chain "
            "sits still for long stretches. The theory of Roberts, Gelman and Gilks suggests aiming for acceptance of a quarter "
            "to a half."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(g[k][0]), Create(g[k][1]), FadeIn(g[k][2]), run_time=2.0)
        self.clear_scene()

    def reparam(self):
        d = load("mcmc")
        A1 = axes([0, 1500], [-0.75, 0.15], x_length=7.6, y_length=1.7, xlabel=r"", ylabel=r"", xticks=[], yticks=[-0.6, -0.2], center=[-1.4, 1.4, 0])
        A2 = axes([0, 1500], [-0.75, 0.15], x_length=7.6, y_length=1.7, xlabel=r"", ylabel=r"", xticks=[], yticks=[-0.6, -0.2], center=[-1.4, -1.0, 0])
        t1 = trace(A1.ax, d["raw"]["b1"], RES)
        t2 = trace(A2.ax, d["chains"]["good"]["b1"], S.LIK)
        l1 = VGroup(label(r"raw: \ $\beta_0 + \beta_1 T$", font_size=22, color=RES),
                    label(rf"ESS {d['raw']['ess']:.0f}", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(A1, RIGHT, buff=0.4)
        l2 = VGroup(label(r"centred: \ $\alpha + \beta_1(T - 70)$", font_size=22, color=S.LIK),
                    label(rf"ESS {d['chains']['good']['ess']:.0f}", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(A2, RIGHT, buff=0.4)
        foot = label(r"the same posterior, \ rotated: \ the long diagonal ridge becomes a round hill", font_size=24, color=OBS).move_to([0, -2.8, 0])
        with self.voiceover(
            "The Challenger posterior hides a second trap. <bookmark mark='a'/> In the original coordinates, intercept and "
            "slope, it's the long diagonal ridge of Part 14. A random walk with independent steps in each coordinate can't follow "
            "a ridge: steps along it are rare, and steps across it are rejected. The best this chain manages is an effective "
            "sample size of twelve. <bookmark mark='b'/> Centre the temperature at seventy degrees, so the intercept becomes the "
            "log-odds at seventy, and the ridge becomes a round hill. The same algorithm, the same step budget, the same "
            "posterior: an effective sample size of over two hundred. <bookmark mark='c'/> Choosing coordinates in which the "
            "posterior is roughly round is the single most useful trick in practical MCMC, and Part 27 goes much further, with "
            "Hamiltonian Monte Carlo."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A1), Create(t1), FadeIn(l1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(A2), Create(t2), FadeIn(l2), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def burnin(self):
        d = load("mcmc")
        A = axes([0, 600], [-0.75, 0.15], x_length=9.0, y_length=3.6, xlabel=r"iteration", ylabel=r"$\beta_1$", xticks=[0, 200, 400, 600],
                 yticks=[-0.6, -0.4, -0.2, 0], center=[-0.6, 0.4, 0])
        tr = trace(A.ax, d["start0_trace"], S.LIK)
        z = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(600, 0), color=GREY_C, stroke_width=1.5)
        rows = fit_rows(VGroup(
            label(r"start from a bad guess, \ $\beta_1 = 0$: \ the chain must first find the posterior", font_size=24),
            label(r"discard the early draws: \ the burn-in, \ or warm-up", font_size=24, color=OBS),
            label(r"run several chains from scattered starts, \ and check that they agree \ ($\hat R$, \ Part 27)", font_size=22, color=GREY_A),
        ), 12.4, 0.26, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A chain must also find the posterior before it can explore it. This one starts at a slope of "
            "zero, no temperature effect at all, and takes a few dozen steps to drift into the region of high probability. "
            "<bookmark mark='b'/> Those early draws reflect the starting point, not the posterior, so they're thrown away: the "
            "burn-in, or warm-up. <bookmark mark='c'/> In practice you run several chains from scattered starting points and "
            "check that they end up agreeing, with diagnostics like the R-hat statistic of Part 27. A single chain that looks "
            "fine can still be stuck."
        ) as vo:
            self.play(FadeIn(A), Create(z))
            vo.wait_until("a")
            self.play(Create(tr), FadeIn(rows[0]), run_time=2.5)
            for k, m_ in enumerate("bc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def answer(self):
        d = load("mcmc")
        g = load("grid")
        A = axes([-3.5, 1.0], [-0.75, 0.0], x_length=5.4, y_length=4.0, xlabel=r"$\alpha = $ log-odds at 70$^\circ$F", ylabel=r"$\beta_1$",
                 xticks=[-3, -2, -1, 0, 1], yticks=[-0.6, -0.4, -0.2, 0], center=[-3.4, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=POST, fill_opacity=0.6) for a, b in zip(d["a_draws"], d["b1_draws"])
                       if -3.5 < a < 1.0 and -0.75 < b < 0])
        tab = table_rows([
            [r"", r"grid", r"Metropolis"],
            [r"$\mathbb E[\beta_1 \mid y]$", rf"{g['b1_mean']:.3f}", rf"{d['full_mean']:.3f}"],
            [r"median $p(31)$", rf"{g['p31_median']:.4f}", rf"{d['p31_median']:.4f}"],
            [r"$P(p(31) > 0.9)$", rf"{g['p_gt_09']:.3f}", rf"{d['p_gt_09']:.3f}"],
        ], font_size=26, col_buff=0.6, row_buff=0.3, colors=[GREY_B, None, None, None]).move_to([3.4, 0.9, 0])
        foot = fit_rows(VGroup(
            label(rf"18,000 draws, \ acceptance {100 * d['acc']:.0f}\%, \ ESS {d['ess']:.0f}", font_size=22, color=GREY_A),
            label(r"the walk reproduces the grid; \ and unlike the grid, \ it scales to many parameters", font_size=24, color=OBS),
        ), 6.4, 0.24, [3.4, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Run a longer chain: twenty thousand steps, the first two thousand discarded. Here are its draws "
            "of the two coefficients, a round cloud in the centred coordinates. <bookmark mark='b'/> Compare with the grid. The "
            "posterior mean of the slope: minus point two eight seven both ways. The median probability of distress at "
            "thirty-one degrees: point nine nine nine nine both ways. The probability it exceeds ninety percent: point nine "
            "seven, both ways. <bookmark mark='c'/> The chain's eighteen thousand correlated draws are worth about five hundred "
            "independent ones, enough for these summaries. <bookmark mark='d'/> The walk reproduces the grid, and unlike the grid "
            "it scales: in Part 27 the same idea handles models with thousands of parameters."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.002), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tab, lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def functions(self):
        d = load("mcmc")
        b = np.asarray(d["b1_draws"])
        o = np.exp(-10 * b)
        lo, hi = np.quantile(o, [0.025, 0.975])
        rows = [
            cmath(r"\text{draws}", r":", r"(\alpha_\ell, \beta_\ell),\ \ \ell = 1, \ldots, L", font_size=32),
            cmath(r"\text{any } g(\theta)", r":", r"g(\theta_\ell) \text{ are draws from its posterior}", font_size=32),
            cmath(r"\text{OR per } 10^\circ\text{F colder}", r"=", rf"e^{{-10\beta_1}}:\ \text{{median}}\ {np.median(o):.1f},\ 95\%\ [{lo:.1f},\ {hi:.0f}]", font_size=28),
            cmath(r"P(\text{OR} > 5 \mid y)", r"=", rf"{np.mean(o > 5):.2f}", font_size=32),
        ]
        rows[2][2].set_color(POST)
        whys = [why(r"the chain's output"), why(r"no delta method, \ no new algebra"),
                why(r"Part 14's profile interval: \ [1.8, 173]"), why(r"a direct probability for a practical question")]
        with self.voiceover(
            "One more reason to like posterior draws. <bookmark mark='a'/> The chain gives a list of parameter values. "
            "<bookmark mark='b'/> Apply any function to each draw, and you have draws from that function's posterior: no delta "
            "method, no new derivation. <bookmark mark='c'/> The odds ratio for ten degrees colder is e to the minus ten beta "
            "one: its posterior median is about fourteen, with a ninety-five percent interval from about two to about three "
            "hundred and fifty, wider at the top than Part 14's profile interval, because a flat prior leaves the steep slopes "
            "plausible. <bookmark mark='d'/> And practical questions get direct "
            "answers: the posterior probability that ten degrees of cold multiplies the odds of distress by more than five."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
