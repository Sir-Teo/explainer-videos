from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403

SDS = [("0.1", BAD), ("1.5", GOOD), ("20.0", S.POST)]


class Metropolis(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.algorithm()
        self.proof()
        self.traces()
        self.histogram()
        self.gibbs()
        self.lessons()

    def card(self):
        c = chapter_card(11, r"The Metropolis algorithm", r"A walk whose long-run law is the one you want", lit=(1953,), part=PART)
        with self.voiceover("Chapter eleven. The Metropolis algorithm, first look."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def history(self):
        hc = history_card(1953, r"N. Metropolis, A. Rosenbluth, M. Rosenbluth, A. Teller \& E. Teller",
                          r"``Equation of state calculations by fast computing machines'': \ sampling the arrangements of "
                          r"molecules on the MANIAC computer at Los Alamos", color=S.MUSEUM, width=8.6, font_size=24).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"Arianna Rosenbluth wrote the program", font_size=24, color=GREY_A),
            label(r"W. K. Hastings (1970) generalized it to any proposal", font_size=24, color=GREY_A),
            label(r"the problem it solves: \ sample from $f \propto e^{-\text{energy}}$ \ without knowing the normalizing constant",
                  font_size=24, color=S.ACCENT),
        ), 12.6, 0.28, [0, -1.4, 0])
        intro = label('Sampling without a normalizing constant', font_size=36)
        with self.voiceover(
            "Chapter three ended with a problem: in high dimensions, independent darts almost all miss. The fix was "
            "found at Los Alamos. <bookmark mark='a'/> In 1953 Nicholas Metropolis, Arianna and Marshall Rosenbluth, "
            "and Augusta and Edward Teller published a method for sampling arrangements of molecules on the MANIAC "
            "computer. Arianna Rosenbluth wrote the program. <bookmark mark='b'/> Seventeen years later Keith "
            "Hastings generalized it. <bookmark mark='c'/> It samples from a density known only up to a constant, "
            "which is exactly the situation of Bayesian statistics, where the posterior's normalizing constant is an "
            "an integral that may be difficult to compute."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def algorithm(self):
        code = code_block([
            "x = start                         # f(start) > 0; 0 < integral f < infinity",
            "repeat:",
            "    y = x + s * normal()            # propose a step",
            "    if log(uniform()) < logf(y) - logf(x):",
            "        x = y                        # accept",
            "    record x                         # (a rejected step repeats x)",
        ], font_size=24)
        code.width = min(code.width, 12.4)
        code.move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"only the \emph{ratio} $f(y)/f(x)$: \ the unknown constant cancels", font_size=26, color=S.ACCENT),
            label(r"uphill moves are always taken; \ downhill ones with chance $f(y)/f(x)$", font_size=26),
            label(r"with ergodicity, time averages converge to target expectations", font_size=26, color=CHAIN),
        ), 12.6, 0.3, [0, -1.9, 0])
        intro = label('A symmetric proposal and an acceptance ratio', font_size=36)
        with self.voiceover(
            "The algorithm fits in six lines. <bookmark mark='a'/> From the current point x, propose a random step to "
            "y. If y has higher density, move there. If lower, move there anyway with chance equal to the ratio of "
            "the densities; otherwise stay put, and record x again. <bookmark mark='b'/> Only the ratio f of y over f "
            "of x is used, so any constant multiplying f cancels. <bookmark mark='c'/> Uphill moves are always "
            "taken; downhill moves sometimes; and the result is a walk that spends time in each region in proportion "
            "to its probability."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(code, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[1:], shift=RIGHT * 0.2))
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"T(x \to y)", r"=", r"q(y \mid x)\,\min\!\Big(1, \frac{f(y)}{f(x)}\Big)", r"\quad (y \ne x)", font_size=32),
            cmath(r"f(x)\,T(x \to y)", r"=", r"q(y \mid x)\,\min\big(f(x),\ f(y)\big)", font_size=32),
            cmath(r"f(x)\,T(x \to y)", r"=", r"f(y)\,T(y \to x)", font_size=34),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"propose with $q$, \ symmetric: \ $q(y \mid x) = q(x \mid y)$"), why(r"symmetric in $x$ and $y$"),
                why(r"detailed balance (chapter 9): \ $f$ is stationary")]
        intro = label('Detailed balance establishes stationarity', font_size=36)
        with self.voiceover(
            "Why does it work? Chapter nine's detailed balance. <bookmark mark='a'/> The off-diagonal transition density from x to y "
            "is the proposal density at y, times the acceptance probability. <bookmark mark='b'/> Multiply by f of x: "
            "you get the proposal density times the smaller of f of x and f of y, which is symmetric in x and y, "
            "because the proposal is. <bookmark mark='c'/> So the flow from x to y equals the flow from y to x: "
            "detailed balance, and f is the chain's stationary distribution. Run it long enough and its states are "
            "dependent draws with a distribution approaching normalized f, under irreducibility and appropriate recurrence and aperiodicity conditions. Detailed balance alone establishes stationarity."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.0, buff=1.0, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def traces(self):
        d = load("metropolis")
        panels = VGroup()
        for k, (sd, c) in enumerate(SDS):
            tr = np.asarray(d[sd]["trace"])
            A = axes([0, 600], [-5, 5.5], x_length=9.4, y_length=1.6, yticks=[-2, 2], center=[1.6, 2.0 - 2.15 * k, 0], font_size=16)
            A.ax.x_axis.set_opacity(0.3)
            ln = polyline(A.ax, np.arange(len(tr)), tr, c, 1.6)
            t = label(rf"step $s = {float(sd):g}$: \ accepts {100 * d[sd]['rate']:.0f}\%", font_size=22, color=c)
            t.next_to(A, LEFT, buff=0.2).shift(UP * 0.4)
            if t.width > 2.4:
                t.width = 2.4
            t.to_edge(LEFT, buff=0.2)
            panels.add(VGroup(A, ln, t))
        cap = label(r"target: \ a two-humped density, \ modes at $-2$ and $+2$; \ first 600 steps shown; acceptance from all 6,000", font_size=22,
                    color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The one thing you must choose is the step size. Here's a target with two humps, at minus two and plus "
            "two, and the first six hundred steps of three longer chains; acceptance rates use all six thousand steps. <bookmark mark='a'/> With tiny steps, nearly every "
            "proposal is accepted, but the chain crawls, and it never leaves the hump where it started. "
            "<bookmark mark='b'/> With steps of one and a half, about half the proposals are accepted and the chain "
            "moves freely between the humps. <bookmark mark='c'/> With huge steps, most proposals land in empty "
            "regions and are rejected: the chain sits still for long stretches, then jumps. A high acceptance rate "
            "is not a good sign by itself; neither is a low one."
        ) as vo:
            self.play(FadeIn(cap))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(panels[k][0]), FadeIn(panels[k][2]), Create(panels[k][1]), run_time=2.0)
        self.clear_scene()

    def histogram(self):
        d = load("metropolis")
        ed = np.asarray(d["edges"])
        g, tgt = np.asarray(d["grid"]), np.asarray(d["target"])
        A = axes([-5, 6], [0, 0.5], x_length=7.4, y_length=4.2, xlabel=r"$x$", xticks=[-4, -2, 0, 2, 4, 6], yticks=[0, 0.2, 0.4],
                 center=[-2.0, -0.4, 0])
        h = hist_bars(A.ax, ed, np.asarray(d["1.5"]["hist"]), color=GOOD, opacity=0.7)
        cv = curve(A.ax, g, tgt, EXACT, 3)
        rows = fit_rows(VGroup(
            MathTex(r"f(x) \propto 0.3\,\phi\big(\tfrac{x + 2}{0.6}\big)/0.6 + 0.7\,\phi\big(\tfrac{x - 2}{0.9}\big)/0.9", font_size=24,
                    color=EXACT),
            label(r"6,000 steps, \ $s = 1.5$", font_size=24, color=GOOD),
            MathTex(r"\text{means: } " + rf"s = 0.1:\ {d['0.1']['mean']:.2f},\ \ s = 1.5:\ {d['1.5']['mean']:.2f},\ \ s = 20:\ {d['20.0']['mean']:.2f}",
                    font_size=24),
            MathTex(rf"\text{{truth: }} {d['true_mean']:.2f}", font_size=24, color=EXACT),
            label(r"the tiny-step chain gives a misleading mean: \ it never found the other hump", font_size=22, color=BAD),
        ), 5.2, 0.28, [4.2, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Six thousand steps of the well-tuned chain: the histogram of its states matches the "
            "target, both humps in the right proportions. <bookmark mark='b'/> Compare the three chains' estimates of "
            "the mean. The truth is point eight. The well-tuned chain and the big-step chain get close. The tiny-step "
            "chain reports two point oh five, and its histogram and acceptance rate alone can mislead: it simply never found the "
            "other hump. That's the danger of Markov chain Monte Carlo, and Part 27 builds the diagnostics against it."
        ) as vo:
            self.play(FadeIn(A), Create(cv), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(h), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2:]))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"draws are dependent: \ effective sample size is often smaller; \ negative autocorrelation can reverse this", font_size=26),
            label(r"the start matters until the chain has mixed: \ discarding early steps cannot repair missing modes", font_size=26),
            label(r"several chains from scattered starts: \ do they agree? \ (Gelman \& Rubin's $\hat R$, Part 27)", font_size=26),
            label(r"in high dimensions, \ random-walk steps often shrink in common high-dimensional models: \ Hamiltonian Monte Carlo (Part 27)", font_size=26),
            label(r"the same machine samples Part 15's posteriors, \ when conjugacy runs out", font_size=26, color=S.ACCENT),
        ), 12.6, 0.38, [0, 0.2, 0])
        intro = label('Checking whether a Markov chain has explored its target', font_size=36)
        with self.voiceover(
            "This was a first look; Part 27 does it in full. <bookmark mark='a'/> The draws are dependent, so a chain "
            "of six thousand steps usually carries less information for a given estimand than six thousand independent draws; negative autocorrelation can improve efficiency. <bookmark mark='b'/> "
            "The start matters until the chain has mixed, so early steps are often discarded, but burn-in cannot fix a chain that never explores missing modes. <bookmark mark='c'/> "
            "Running several chains from scattered starts, and checking that they agree, can reveal the tiny-step "
            "failure we just saw. <bookmark mark='d'/> In high dimensions, random-walk proposals often need to shrink in common models, and "
            "better proposals use the gradient of the density: Hamiltonian Monte Carlo. <bookmark mark='e'/> And this "
            "is the machine that samples posterior distributions in Bayesian statistics, once the conjugate formulas "
            "of Part 15 run out."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def gibbs(self):
        rho = 0.85
        g = np.random.Generator(np.random.PCG64(1984))
        x, y = -2.5, 2.5
        pts = [(x, y)]
        for _ in range(40):
            x = rho * y + np.sqrt(1 - rho ** 2) * g.standard_normal()
            pts.append((x, y))
            y = rho * x + np.sqrt(1 - rho ** 2) * g.standard_normal()
            pts.append((x, y))
        A = axes([-3.2, 3.2], [-3.2, 3.2], x_length=4.8, y_length=4.8, xlabel=r"$x$", ylabel=r"$y$", xticks=[-2, 0, 2],
                 yticks=[-2, 0, 2], center=[-3.4, -0.4, 0])
        ax = A.ax
        th = np.linspace(0, TAU, 120)
        ev, V = np.linalg.eigh(np.array([[1, rho], [rho, 1]]))
        ells = VGroup(*[VMobject(stroke_color=GREY_C, stroke_width=1.5).set_points_smoothly(
            [ax.c2p(*(c * (np.sqrt(ev[0]) * np.cos(t) * V[:, 0] + np.sqrt(ev[1]) * np.sin(t) * V[:, 1]))) for t in th]) for c in (1, 2)])
        path = VMobject(stroke_color=CHAIN, stroke_width=2)
        path.set_points_as_corners([ax.c2p(a, b) for a, b in pts])
        rows = fit_rows(VGroup(
            label(r"Gibbs sampling: \ update one coordinate at a time, \ from its conditional", font_size=24),
            MathTex(r"x \mid y \sim N\big(\rho y,\ 1 - \rho^2\big),\quad y \mid x \sim N\big(\rho x,\ 1 - \rho^2\big)", font_size=26,
                    color=CHAIN),
            label(r"Part 5's Gaussian conditionals; \ every step is accepted", font_size=22, color=GREY_A),
            label(r"strong correlation: \ short steps, \ slow mixing ($\rho = 0.85$ here)", font_size=22, color=BAD),
            label(r"Geman \& Geman (1984); \ Gelfand \& Smith (1990): \ Part 27", font_size=22, color=GREY_A),
        ), 6.0, 0.3, [3.4, 0.2, 0])
        with self.voiceover(
            "One special case deserves a first look. <bookmark mark='a'/> When the conditional distribution of each "
            "coordinate, given all the others, is easy to sample, update one coordinate at a time from its conditional. "
            "<bookmark mark='b'/> For a correlated normal pair, those conditionals are Part 5's: normal, centred at rho "
            "times the other coordinate. The chain moves in horizontal and vertical steps, and every step is accepted. "
            "<bookmark mark='c'/> It's called Gibbs sampling, after the physicist, and Alan Gelfand and Adrian Smith's "
            "1990 paper put it at the centre of Bayesian statistics. Notice the staircase: when the coordinates are "
            "strongly correlated, the steps are short and the chain mixes slowly, a problem Part 27 takes on."
        ) as vo:
            self.play(FadeIn(A), Create(ells))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1:3]), Create(path), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()
