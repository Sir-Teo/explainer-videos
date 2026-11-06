from __future__ import annotations

import numpy as np

from videos.stats.stats27.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.disks()
        self.rule()
        self.ergodic()
        self.banana()
        self.problem()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1953,)).to_edge(UP, buff=0.35)
        hc = history_card(1953, r"Metropolis, \ A. \& M. Rosenbluth, \ A. \& E. Teller, \ \emph{J. Chem. Phys.}",
                          r"at Los Alamos, \ on the MANIAC computer, \ a team computed the equation of state of hard disks "
                          r"in a box. \ The integral over every arrangement of the disks was hopeless; \ instead they let the "
                          r"disks wander at random, \ rejecting any move that made two of them overlap",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"224 disks: \ an integral in 448 dimensions", font_size=24),
            label(r"no grid, \ no formula: \ a random walk that spends its time where the probability is", font_size=24, color=SAMPLER),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1953, at Los Alamos, Nicholas Metropolis, Arianna and Marshall Rosenbluth, and Augusta "
            "and Edward Teller wanted the equation of state of a fluid, modelled as hard disks in a box. It needed an "
            "average over every possible arrangement of the disks. <bookmark mark='b'/> With two hundred and twenty-four "
            "disks that is an integral in four hundred and forty-eight dimensions: no grid could touch it. "
            "<bookmark mark='c'/> Their idea, run on the MANIAC computer, was a random walk through arrangements that spends "
            "its time in proportion to their probability."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def disks(self):
        d = load("disks")
        box = Square(side_length=4.6, stroke_color=GREY_B, stroke_width=2).move_to([-2.6, 0.2, 0])
        c0 = box.get_center() - np.array([2.3, 2.3, 0])
        r = d["d"] / 2 * 4.6

        def disk_group(xy):
            return VGroup(*[Circle(radius=r, stroke_color=SAMPLER, stroke_width=2, fill_color=SAMPLER, fill_opacity=0.35)
                            .move_to(c0 + np.array([x * 4.6, y * 4.6, 0])) for x, y in xy])

        g0 = disk_group(d["start"])
        snaps = [disk_group(s) for s in d["snaps"]]
        rows = fit_rows(VGroup(
            label(rf"{d['N']} hard disks; \ start on a lattice", font_size=22),
            label(r"pick a disk; \ propose a small random shift", font_size=22, color=SAMPLER),
            label(r"overlap? \ reject, \ and stay put", font_size=22, color=RES),
            label(r"no overlap? \ accept", font_size=22, color=HIT),
            label(rf"{100 * d['accept']:.0f}\% of moves accepted; \ 400 sweeps", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.3, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is their algorithm on forty disks. Start them on a lattice. <bookmark mark='b'/> "
            "Pick a disk and propose moving it a small random distance. <bookmark mark='c'/> If it would overlap another, "
            "reject the move: the disk stays where it is, and that position is counted again. <bookmark mark='d'/> "
            "Otherwise accept it. <bookmark mark='e'/> Sweep after sweep, the lattice melts into a typical arrangement, and "
            "averages over the walk become averages over all arrangements, each weighted by its probability."
        ) as vo:
            self.add(seeded_tag())
            self.play(Create(box), FadeIn(g0))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            cur = g0
            for s_ in snaps:
                self.play(Transform(cur, s_), run_time=1.2)
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def rule(self):
        rows = [
            cmath(r"\text{propose}", r":", r"x' = x + \text{a symmetric random step}", font_size=30),
            cmath(r"\text{accept with}", r":", r"\min\Bigl\{1, \ \dfrac{\pi(x')}{\pi(x)}\Bigr\}", font_size=32),
            cmath(r"\text{hard disks}", r":", r"\pi = \text{constant, \ or } 0 \text{ if overlapping}", font_size=30),
            cmath(r"\text{only ratios}", r":", r"\pi \text{ need not be normalized}", font_size=30),
        ]
        rows[1][2].set_color(SAMPLER)
        whys = [why(r"a random walk"), why(r"uphill always, \ downhill sometimes"), why(r"accept unless overlapping"),
                why(r"so $\pi(\theta) \propto p(y \mid \theta)\,p(\theta)$ is enough")]
        with self.voiceover(
            "<bookmark mark='a'/> In general: from the current point, propose a random step. <bookmark mark='b'/> Accept it "
            "with probability the ratio of the target densities, capped at one: always move uphill, sometimes downhill. "
            "<bookmark mark='c'/> For hard disks every legal arrangement is equally likely, so the rule is simply 'accept "
            "unless they overlap'. <bookmark mark='d'/> And because only ratios appear, the normalizing constant is never "
            "needed, which is exactly what Bayesians lack: the posterior up to a constant, likelihood times prior."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def banana(self):
        d = load("banana")
        A = axes(d["x_range"], d["y_range"], x_length=6.4, y_length=4.8, xlabel=r"$\theta_1$", ylabel=r"$\theta_2$",
                 xticks=[-5, 0, 5], yticks=[0, 4, 8], center=[-2.4, 0.2, 0])
        ax = A.ax
        Z = np.asarray(d["Z"])
        L = Landscape(ax, Z, d["x_range"], d["y_range"], levels=[0.6, 0.3, 0.1, 0.02], color=EXACTC, stroke_width=1.8)
        path = np.asarray(d["path"])
        line = polyline(ax, path[:, 0], path[:, 1], SAMPLER, 1.5, 0.8)
        cloud = scatter_pts(ax, np.asarray(d["draws"])[400::3, 0], np.asarray(d["draws"])[400::3, 1], SAMPLER, 0.022, 0.5)
        start = Dot(ax.c2p(*path[0]), radius=0.08, color=RES)
        rows = fit_rows(VGroup(
            label(r"gold: \ a curved posterior's contours", font_size=22, color=EXACTC),
            label(r"red: \ start far out", font_size=22, color=RES),
            label(r"blue: \ the walk's first 400 steps", font_size=22, color=SAMPLER),
            label(rf"accepted {100 * d['accept']:.0f}\% of proposals", font_size=22, color=GREY_A),
            label(r"the cloud of positions is the posterior", font_size=22, color=HIT),
        ), 4.4, 0.42, [4.5, 0.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The same walk on a curved two-parameter posterior, its contours in gold. "
            "<bookmark mark='b'/> Start somewhere unlikely. <bookmark mark='c'/> The walk drifts in, then wanders along the "
            "curved ridge. <bookmark mark='d'/> About half the proposals are accepted. <bookmark mark='e'/> Thousands of "
            "steps later, the cloud of visited positions is a sample from the posterior, and any average over it is an "
            "estimate of a posterior expectation."
        ) as vo:
            self.play(FadeIn(A), FadeIn(L.levels))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(start, scale=2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(rows[2]), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(line.animate.set_stroke(opacity=0.15), LaggedStart(*[FadeIn(p) for p in cloud], lag_ratio=0.002), FadeIn(rows[4]), run_time=2.5)
        self.clear_scene()

    def problem(self):
        rows = fit_rows(VGroup(
            label(r"Part 26 integrated on a grid: \ fine in one dimension", font_size=26),
            label(r"100 parameters, \ 10 grid points each: \ $10^{100}$ evaluations", font_size=26, color=RES),
            label(r"a sampler's cost grows with the dimension, \ not exponentially in it", font_size=26, color=SAMPLER),
            label(r"but which sampler, \ how to know it worked, \ and what to do when it fails?", font_size=26, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 26 integrated over tau on a grid, which works in one dimension. "
            "<bookmark mark='b'/> With a hundred parameters and only ten grid points each, a grid needs ten to the hundred "
            "evaluations. <bookmark mark='c'/> A good sampler's cost grows with the dimension, not exponentially in it. "
            "<bookmark mark='d'/> The questions of this part are which sampler, how to know it worked, and what to do when it "
            "doesn't."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 27", font_size=34, color=GREY_B), label(r"Bayesian Computation", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"importance sampling and PSIS; \ Metropolis--Hastings; \ Gibbs",
            r"diagnostics: \ $\hat R$ and effective sample size",
            r"Hamiltonian Monte Carlo, \ NUTS, \ and Neal's funnel",
            r"a probabilistic programming language, \ built and checked",
            r"SMC, \ variational inference, \ Laplace, \ ABC, \ exact sampling",
        ], color=SAMPLER, font_size=26)
        prereq = note(r"prerequisites: \ Parts 7 and 26").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.ppl}; \ the puck on the surface").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-seven: Bayesian computation. <bookmark mark='b'/> We'll weight samples by "
            "importance and learn when the weights lie; build Metropolis–Hastings and Gibbs samplers; diagnose chains; slide "
            "a puck over the posterior with Hamiltonian Monte Carlo and its self-tuning descendant NUTS, and watch it fail "
            "in Neal's funnel and be fixed; build a small probabilistic programming language and check it against exact "
            "answers; and meet the alternatives: particle methods, variational inference, Laplace approximations, "
            "likelihood-free inference, and sampling that is exactly right."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

    def ergodic(self):
        rows = [
            cmath(r"\tfrac1S \textstyle\sum_s f(x_s)", r"\to", r"E_\pi f", font_size=32),
            cmath(r"\sqrt S\,(\bar f - E_\pi f)", r"\to", r"N(0, \sigma_f^2 \tau_f)", font_size=30),
            cmath(r"\tau_f", r"=", r"1 + 2\textstyle\sum_{t \ge 1} \rho_t", font_size=30),
            cmath(r"\text{the price}", r":", r"\text{correlated draws: \ } S/\tau_f \text{ effective}", font_size=30),
        ]
        rows[3][-1].set_color(RES)
        whys = [why(r"the ergodic theorem: \ Part 6 for chains"), why(r"a Markov-chain CLT, \ under conditions"), why(r"the integrated autocorrelation time"), why(r"chapter four's ESS")]
        with self.voiceover(
            "<bookmark mark='a'/> Why averages over a walk work: the ergodic theorem, Part 6's law of large numbers for Markov "
            "chains, says they converge to expectations under the target. <bookmark mark='b'/> Under further conditions "
            "there is a central limit theorem too, <bookmark mark='c'/> but with the variance inflated by the integrated "
            "autocorrelation time, because each draw resembles the last. <bookmark mark='d'/> The price of a random walk is "
            "that S draws are worth only S over tau independent ones; chapter four turns this into the effective sample size."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
