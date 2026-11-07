from __future__ import annotations

import numpy as np

from videos.stats.stats53.common import *  # noqa: F403


class Doob(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.proof()
        self.chart()
        self.finite()
        self.catch()

    def card(self):
        card = chapter_card(1, r"Doob's theorem", r"Consistency, \ almost surely \ under the prior", lit=(1949,), part=PART)
        with self.voiceover("Chapter one. Doob's theorem: consistency, almost surely under the prior."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\theta \sim \Pi, \ \ X_1, X_2, \dots \mid \theta \overset{iid}{\sim} P_\theta", r":", r"\text{identifiable, measurable; suitable standard-Borel spaces}", font_size=30),
            cmath(r"\text{Doob (1949)}", r":", r"\Pi(\cdot \mid X_{1:n}) \Rightarrow \delta_\theta \ \text{ for } \Pi\text{-almost every } \theta", font_size=32),
            cmath(r"\text{no conditions}", r":", r"\text{on smoothness, \ dimension, \ or the prior's shape}", font_size=32),
            cmath(r"\text{the catch}", r":", r"\text{``almost every'' is measured by the prior itself}", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"identifiable"), why(r"Doob's martingale theorem"), why(r"remarkably general"), why(r"a self-fulfilling guarantee")]
        heading = label('Posterior convergence requires both local and global model conditions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Joseph Doob's theorem of 1949 requires identifiable i.i.d. sampling, measurable parametrization and suitable standard-Borel parameter and sample spaces: a parameter drawn from the prior, observations independent given it, and an identifiable model. <bookmark mark='b'/> Then, for almost every value of the parameter, the posterior converges to a point mass at that value. <bookmark mark='c'/> Within those measurability and identifiability conditions, no extra smoothness or finite-dimensional restriction is needed. <bookmark mark='d'/> The catch is in the words almost every. They are measured by the prior itself. The theorem says the Bayesian expects to be consistent, which is not the same as being consistent for the truth that actually generated the data."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"M_n", r"=", r"E[g(\theta) \mid X_{1:n}]: \ \text{a martingale, \ bounded}", font_size=34),
            cmath(r"M_n \to M_\infty", r"=", r"E[g(\theta) \mid X_{1:\infty}] \ \text{ a.s. (Part 44)}", font_size=34),
            cmath(r"\theta \text{ is a function of } X_{1:\infty}", r":", r"\text{the infinite sample identifies } \theta \ \text{(the LLN)}", font_size=30),
            cmath(r"\text{so}", r":", r"E[g(\theta) \mid X_{1:\infty}] = g(\theta): \ \text{for each fixed bounded measurable }g", font_size=30),
        ]
        rows[3][-1].set_color(GOODC)
        whys = [why(r"a Doob martingale"), why(r"martingale convergence"), why(r"identifiability"), why(r"weak convergence")]
        heading = label('An identifiable infinite sample and martingale convergence imply consistency', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The proof is pure Part forty-four. For any bounded function of the parameter, its posterior mean is a bounded martingale in n. <bookmark mark='b'/> By the martingale convergence theorem it converges almost surely, to the conditional expectation given the whole infinite sample. <bookmark mark='c'/> But the infinite sample identifies the parameter: the empirical distribution converges to P theta, which determines theta. <bookmark mark='d'/> So that conditional expectation is just the function evaluated at the parameter, for each fixed bounded measurable function its posterior expectation converges almost surely under the joint law. A countable determining class supplies a common event for weak posterior consistency. All of this holds under the joint law of the parameter and the data, which is why the exceptional set is null under the prior."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("doob")
        ln = np.log10(d["ns"])
        A = axes([0, 3.6], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"posterior mean of $p$",
                 xticks=[0, 1, 2, 3], xfmt=lambda v: f"10^{{{int(v)}}}", yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        paths = VGroup(*[polyline(ax, ln, p, POSTC, 1.8, opacity=0.7) for p in d["paths"]])
        ends = VGroup(*[Dot(ax.c2p(3.55, t), radius=0.05, color=TRUTHC) for t in d["truths"]])
        err = float(np.mean([abs(p[-1] - t) for p, t in zip(d["paths"], d["truths"])]))
        side = fit_rows(VGroup(
            label(r"$p \sim$ Uniform$(0, 1)$, \ then coin flips", font_size=22),
            label(r"24 truths drawn from the prior", font_size=22),
            label(r"blue: \ posterior means, \ Beta(1, 1) prior", font_size=22, color=POSTC),
            label(rf"white: \ the truths; \ mean error at $n = 3{{,}}000$: \ {err:.3f}", font_size=22, color=TRUTHC),
            label(r"prior-almost-sure consistency; \ a finite simulation is illustrative", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Doob's theorem in a picture. Draw a coin's probability from a uniform prior, then flip it. <bookmark mark='b'/> Twenty-four such truths. <bookmark mark='c'/> The posterior means, under the same uniform prior, wander at first and then settle. <bookmark mark='d'/> Each one settles on its own truth, the white dots on the right: the average error after three thousand flips is {say(err, 3)}. <bookmark mark='e'/> When the truth is drawn from the prior, Bayes is consistent. In one dimension, with a prior that puts mass everywhere, that illustrates regular interior Bernoulli truths; Doob alone still gives only a prior-almost-everywhere assertion; in infinite dimensions it need not."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.05), FadeIn(side[2]), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(ends), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def finite(self):
        import math

        r = np.random.default_rng(531)
        thetas = [0.3, 0.4, 0.5]
        x = r.random(800) < 0.4
        ns = np.arange(0, 801, 10)
        post = []
        for n in ns:
            k = int(x[:n].sum())
            lp = np.array([k * math.log(t) + (n - k) * math.log(1 - t) for t in thetas])
            w = np.exp(lp - lp.max())
            post.append(w / w.sum())
        post = np.asarray(post)
        A = axes([0, 820], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$n$", ylabel=r"posterior probability",
                 xticks=[0, 200, 400, 600, 800], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = [GREY_B, GOODC, BADC]
        cs = VGroup(*[polyline(ax, ns, post[:, j], c, 4) for j, c in enumerate(cols)])
        kl = 0.4 * math.log(0.4 / 0.3) + 0.6 * math.log(0.6 / 0.7)
        side = fit_rows(VGroup(
            label(r"a prior on three values: \ $p \in \{0.3, \ 0.4, \ 0.5\}$, \ equal weights", font_size=22),
            label(r"the truth is $0.4$: \ green", font_size=22, color=GOODC),
            label(rf"each wrong value dies like $e^{{-n\,\mathrm{{KL}}}}$: \ KL$(0.4, 0.3) = {kl:.4f}$", font_size=22, color=BADC),
            label(rf"posterior on the truth at $n = 800$: \ {post[-1, 1]:.4f}", font_size=22, color=GOODC),
            label(r"problem 1: \ the law of large numbers does it", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The finite case shows the mechanism. A prior on three coin probabilities, point three, "
            f"point four and point five, with the truth at point four. <bookmark mark='b'/> The posterior probability of the "
            f"truth, in green, climbs towards one. <bookmark mark='c'/> Each wrong value's posterior falls like e to the minus "
            f"n times its Kullback–Leibler divergence from the truth, {say(kl, 4)} for point three, because the log "
            f"likelihood ratio is an average that the law of large numbers controls. <bookmark mark='d'/> After eight hundred "
            f"flips the truth has posterior probability {say(post[-1, 1], 4)}. <bookmark mark='e'/> With finitely many "
            f"candidates, consistency is just the law of large numbers; the trouble starts with infinitely many."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"one simulated sequence")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs[0]), Create(cs[2]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def catch(self):
        rows = fit_rows(VGroup(
            label(r"so why is Doob not enough?", font_size=28, color=GREY_A),
            label(r"a null set under the prior can be most of the space, \ in another sense", font_size=26, color=BADC),
            label(r"Freedman (1963): \ for priors on distributions on the integers, \ inconsistency is generic", font_size=26, color=BADC),
            label(r"and the statistician's truth is fixed, \ not drawn from their prior", font_size=26, color=BALLC),
            label(r"we need conditions that say which truths: \ Schwartz", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So why is Doob's theorem not the end of the story? <bookmark mark='b'/> Because a set of prior probability zero can be most of the parameter space in other senses. <bookmark mark='c'/> David Freedman showed in 1963 that for priors on distributions over the integers, genericity results can make consistency topologically small in specified spaces of priors and truths. They do not say every prior is inconsistent for most truths under every topology. <bookmark mark='d'/> And the frequentist's truth is fixed by nature, not drawn from anyone's prior. <bookmark mark='e'/> What is needed is a theorem that says which truths a given prior can learn. That is Lorraine Schwartz's."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
