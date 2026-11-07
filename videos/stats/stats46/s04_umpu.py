from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class UMPU(VoiceoverScene):
    def construct(self):
        self.card()
        self.unbiased()
        self.power()
        self.lp()
        self.structure()
        self.slices()
        self.sizes()
        self.isis()
        self.ttest()

    def card(self):
        card = chapter_card(3, r"Unbiased tests and Neyman structure", r"Optimality when nuisance parameters intrude", lit=(1933,), part=PART)
        with self.voiceover("Chapter three. Unbiased tests and Neyman structure: optimality when nuisance parameters intrude."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def unbiased(self):
        rows = [
            cmath(r"\phi \text{ unbiased}", r":", r"\beta(\theta) \le \alpha \text{ on } H_0, \ \ \beta(\theta) \ge \alpha \text{ on } H_1", font_size=32),
            cmath(r"\theta = \theta_0 \text{ vs } \theta \ne \theta_0", r"\Rightarrow", r"\beta(\theta_0) = \alpha, \ \ \beta'(\theta_0) = 0", font_size=32),
            cmath(r"\text{exponential family}", r":", r"E_{\theta_0}\phi = \alpha, \ \ E_{\theta_0}[T\phi] = \alpha\, E_{\theta_0} T", font_size=32),
            cmath(r"\phi^*", r"=", r"1 \text{ outside } [c_1, c_2], \ \gamma_i \text{ at } c_i: \ \text{UMPU}", font_size=34),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"never less likely to reject under $H_1$"), why(r"a minimum at $\theta_0$"), why(r"$\partial_\eta\beta = \mathrm{Cov}(T, \phi)$"), why(r"two tails, \ chosen jointly")]
        with self.voiceover(
            "<bookmark mark='a'/> A test is unbiased if it is never less likely to reject under an alternative than "
            "under the null: its power function is at most alpha on the null and at least alpha on the alternative. "
            "<bookmark mark='b'/> For a point null against a two-sided alternative, a smooth power function must then"
            " have a minimum at theta nought: value alpha, slope zero. <bookmark mark='c'/> In an exponential family "
            "differentiation with respect to the natural parameter makes the slope the covariance of T with the test."
            " The conditions are size alpha and expected T times phi equal to alpha times expected T. A different "
            "smooth parameterization adds the derivative of the natural parameter. <bookmark mark='d'/> The "
            "generalized Neyman–Pearson lemma, with these two side conditions, gives the uniformly most powerful "
            "unbiased test: reject outside an interval, with its two endpoints and their randomizations solved for "
            "jointly."
        ) as vo:
            heading=label('Two-sided unbiasedness constrains size and first moment',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def power(self):
        d = load("umpu")
        ps = np.asarray(d["ps"])
        u = d["umpu"]
        A = axes([0.1, 0.55], [0, 0.6], x_length=7.4, y_length=4.4, xlabel=r"$p$", ylabel=r"power, \ $n = 20$",
                 xticks=[0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.05, 0.2, 0.4, 0.6], center=[-2.5, 0.2, 0])
        ax = A.ax
        k = (ps >= 0.1) & (ps <= 0.55)
        cu = polyline(ax, ps[k], np.asarray(d["pw_umpu"])[k], UMPC, 4)
        ce = polyline(ax, ps[k], np.asarray(d["pw_et"])[k], REJC, 3)
        a = DashedLine(ax.c2p(0.1, 0.05), ax.c2p(0.55, 0.05), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"$p = 0.3$ \ vs \ $p \ne 0.3$, \ 5\%", font_size=22),
            label(rf"green: \ UMPU: \ reject $x < {u['c1']}$ or $> {u['c2']}$; \ $\gamma = {u['g1']:.2f}, \ {u['g2']:.2f}$", font_size=22, color=UMPC),
            label(r"red: \ equal tails, \ 2.5\% each", font_size=22, color=REJC),
            label(rf"its minimum: \ {100 * d['et_min']:.2f}\% at $p = {d['et_argmin']:.3f}$: \ slightly biased", font_size=22, color=REJC),
            label(r"the UMPU curve bottoms out at $p_0$, \ exactly", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The binomial again: p equal to point three against p different, at five percent. "
            f"<bookmark mark='b'/> The UMPU test rejects below {u['c1']} or above {u['c2']} successes, randomizing at the "
            f"two endpoints with probabilities {say(u['g1'], 2)} and {say(u['g2'], 2)}: the tails are not equal. <bookmark "
            f"mark='c'/> The familiar equal-tailed test puts two and a half percent in each tail. <bookmark mark='d'/> Its "
            f"power dips just below five percent, to {100 * d['et_min']:.2f} percent, slightly to the left of point three: "
            f"it is biased, by a hair. <bookmark mark='e'/> The UMPU curve has its minimum exactly at the null value. With "
            f"skewed distributions the difference can be large."
        ) as vo:
            self.play(FadeIn(A), Create(a), FadeIn(exact_tag(r"exact power functions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cu), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ce), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lp(self):
        d = load("umpu")
        lp = d["lp"]
        rows = [
            cmath(r"\max_\phi \textstyle\sum \phi f_{p_1}", r"\ \text{s.t.}\ ", r"\textstyle\sum \phi f_{0.3} = 0.05, \ \sum x \phi f_{0.3} = 0.05 \cdot 20 \cdot 0.3", font_size=30),
            cmath(r"p_1 = 0.15", r":", rf"\text{{LP power}} \ {lp['0.15']['power']:.4f} \ = \ \text{{UMPU}} \ {lp['0.15']['umpu']:.4f}", font_size=32),
            cmath(r"p_1 = 0.5", r":", rf"\text{{LP power}} \ {lp['0.5']['power']:.4f} \ = \ \text{{UMPU}} \ {lp['0.5']['umpu']:.4f}", font_size=32),
            cmath(r"\text{the same test, \ from either side}", r":", r"\text{uniformly most powerful among unbiased tests}", font_size=30),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"chapter 1's generalized lemma"), why(r"an alternative below"), why(r"an alternative above"), why(r"UMPU")]
        with self.voiceover(
            f"<bookmark mark='a'/> Check it with chapter one's linear programme. Maximize the power against one "
            f"alternative, subject to the two unbiasedness conditions. <bookmark mark='b'/> Against p equal to point one "
            f"five, the programme's best power is {say(lp['0.15']['power'], 3)}, exactly the UMPU test's. <bookmark "
            f"mark='c'/> Against point five, {say(lp['0.5']['power'], 3)}, again exactly. <bookmark mark='d'/> The same "
            f"test solves the programme for every alternative on either side: that is what uniformly most powerful unbiased "
            f"means."
        ) as vo:
            heading=label('One binomial test solves both constrained power programs',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def structure(self):
        rows = [
            cmath(r"\text{nuisance } \lambda", r":", r"T \text{ sufficient for } \lambda \text{ on the boundary of } H_0", font_size=32),
            cmath(r"\phi \text{ similar}", r":", r"E_{\lambda}\phi = \alpha \ \text{for every } \lambda", font_size=34),
            cmath(r"\text{Neyman structure}", r":", r"E[\phi \mid T] = \alpha \ \text{a.s.}", font_size=34),
            cmath(r"T \text{ complete}", r"\Rightarrow", r"\text{similar} \iff \text{Neyman structure}: \ \text{test within each slice}", font_size=30),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"a statistic for the nuisance"), why(r"exact size, \ whatever $\lambda$"), why(r"exact size given $T$"), why(r"Part 45's completeness")]
        with self.voiceover(
            "<bookmark mark='a'/> Now add a nuisance parameter, and suppose that on the boundary of the null a "
            "statistic T is sufficient for it. <bookmark mark='b'/> A test is similar if its size is exactly alpha "
            "whatever the nuisance parameter is: the exact-size property that fails for the familiar Behrens–Fisher "
            "approximations. <bookmark mark='c'/> It has Neyman structure if its conditional size given T is alpha, "
            "slice by slice. Neyman structure implies similarity, by averaging over T. <bookmark mark='d'/> If T is "
            "also complete, the converse holds: the conditional size minus alpha is a function of T with mean zero "
            "for every lambda, hence zero. So similar tests are exactly the tests with conditional rejection "
            "probability equal to alpha within almost every slice, and the best of them is the best test in each "
            "slice."
        ) as vo:
            heading=label('Completeness turns similarity into conditional equality',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def slices(self):
        d = load("neyman")
        sl = [(rf"total $t = {t}$", v["x"], v["pmf"], v["phi"]) for t, v in d["slices"].items()]
        ns = NeymanSlices(sl, width=12.0, height=2.8, color=H0C, reject_color=REJC).move_to([0, 0.3, 0])
        side = fit_rows(VGroup(
            label(rf"$X \sim$ Bin$({d['m']}, p_1)$, \ $Y \sim$ Bin$({d['n']}, p_2)$: \ is $p_1 > p_2$?", font_size=24),
            label(r"given $T = X + Y = t$, \ $X$ is hypergeometric on $p_1=p_2$, \ whatever the common $p$", font_size=24, color=GREY_A),
            label(r"red: \ the rejected part of each slice, \ exactly 5\% of it", font_size=24, color=REJC),
        ), 12.4, 0.22, [0, -2.6, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is Neyman structure as a picture, the part's instrument. Two binomial samples, of {d['m']} and {d['n']} trials: is the first success probability larger? On the boundary of the one-sided null the probabilities are equal, to an unknown common value, the nuisance parameter, and the total number of successes is sufficient for it. <bookmark mark='b'/> Given the total, the first count is hypergeometric, whatever the common p. Here are its distributions for totals of four, nine and thirteen. <bookmark mark='c'/> In each slice, the test rejects the top five percent, randomizing at the edge: the red portions. Every slice spends exactly five percent, so the whole test has size five percent at every value of the nuisance parameter."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(side[0]), *[FadeIn(VGroup(p[0], p[1], p.title)) for p in ns.panels])
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(p.rej) for p in ns.panels], FadeIn(side[2]))
        self.wait(1.0)
        self.clear_scene()

    def sizes(self):
        d = load("neyman")
        ps = np.asarray(d["ps"])
        A = axes([0, 1], [0, 0.07], x_length=7.4, y_length=4.4, xlabel=r"the common $p$ \ (nuisance)", ylabel=r"size",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.025, 0.05], center=[-2.5, 0.2, 0])
        ax = A.ax
        cr = polyline(ax, ps, d["size_rand"], UMPC, 5)
        cf = polyline(ax, ps, d["size_fisher"], REJC, 4)
        side = fit_rows(VGroup(
            label(r"green: \ randomized: \ 5\% at every $p$", font_size=22, color=UMPC),
            label(r"red: \ nonrandomized one-sided conditional test", font_size=22, color=REJC),
            label(r"the green test is UMPU \ (one-sided)", font_size=22, color=S.ACCENT),
            label(r"Fisher's: \ conservative, \ the price of not flipping coins", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The unconditional size of that test, as a function of the common p: a flat line at five "
            "percent. It is similar, as promised. <bookmark mark='b'/> Fisher's exact test is the same test without the "
            "randomization at the slice edges. With samples this small, its size never exceeds about two percent, and "
            "it varies with p. "
            "<bookmark mark='c'/> The randomized version is the uniformly most powerful unbiased test for comparing two "
            "binomials; <bookmark mark='d'/> Fisher's is its conservative, practical cousin."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ binomial and hypergeometric sums")))
            vo.wait_until("a")
            self.play(Create(cr), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cf), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def isis(self):
        d = load("neyman")
        i, t = d["isis"], d["tea"]
        rows = [
            cmath(r"\text{ISIS-2, \ vascular deaths}", r":", rf"\text{{aspirin}} \ {i['deaths'][0]}/{i['n'][0]:,}, \ \text{{placebo}} \ {i['deaths'][1]}/{i['n'][1]:,}", font_size=30),
            cmath(r"\text{given the total } " + f"{i['total']:,}", r":", rf"\text{{expected}} \ {i['expected']:.1f} \ \text{{aspirin deaths}}; \ \text{{observed}} \ {i['deaths'][0]}", font_size=30),
            cmath(r"\text{hypergeometric}", r":", rf"z = {i['z']:.2f}, \ \ P \approx 10^{{-7}}", font_size=34),
            cmath(r"\text{the lady tasting tea}", r":", rf"\text{{all 4 cups right: }} 1/70 = {t['p_all']:.4f}", font_size=32),
        ]
        rows[2][-1].set_color(UMPC)
        whys = [why(r"17,187 patients (1988)"), why(r"condition on the margin"), why(r"the conditional test"), why(r"Fisher (1935), \ the same test")]
        with self.voiceover(
            f"<bookmark mark='a'/> Two real tables. ISIS-2, the trial of aspirin after heart attacks: {i['deaths'][0]} "
            f"vascular deaths among {i['n'][0]:,} patients on aspirin, {i['deaths'][1]:,} among {i['n'][1]:,} on placebo. "
            f"<bookmark mark='b'/> Given the {i['total']:,} deaths in total, the null predicts about {i['expected']:.0f} in "
            f"the aspirin arm. <bookmark mark='c'/> The conditional, hypergeometric test gives a z of {say(i['z'], 1)}: a "
            f"p-value of about one in ten million. <bookmark mark='d'/> And Fisher's lady tasting tea, eight cups with four "
            f"of each kind: the same conditional test, in which identifying all four correctly has probability one in "
            f"seventy."
        ) as vo:
            self.play(FadeIn(museum_tag(r"ISIS-2 \ (\emph{Lancet} 1988); \ Fisher (1935)")))
            heading=label('Conditional hypergeometric probabilities compare fixed margins',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ttest(self):
        rows = [
            cmath(r"N(\mu, \sigma^2)", r":", r"H_0: \mu = 0; \ \ \text{nuisance } \sigma; \ \ T = \textstyle\sum x_i^2 \text{ sufficient on } H_0", font_size=30),
            cmath(r"\text{given } T", r":", r"x / \sqrt T \text{ is uniform on the sphere}; \ \ \text{test } \textstyle\sum x_i \text{ within it}", font_size=30),
            cmath(r"\textstyle\sum x_i / \sqrt{\sum x_i^2}", r"\leftrightarrow", r"t = \sqrt n\, \bar x / s: \ \text{monotone}", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\text{the two-sided } t \text{ test is UMPU}", font_size=36),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"the boundary of $H_0$"), why(r"Neyman structure"), why(r"a function of $t$ alone"), why(r"Lehmann (1959)")]
        with self.voiceover(
            "<bookmark mark='a'/> For independent normal observations and at least two observations, Neyman structure"
            " also proves the t test optimal. Test a normal mean equal to zero with sigma unknown. On the null, the "
            "sum of squares is complete and sufficient for sigma. <bookmark mark='b'/> Given it, the data vector "
            "divided by its length is uniform on a sphere, whatever sigma is, so the conditional nuisance-free family"
            " can be tested within each sphere. Two-sided unbiasedness adds a zero first-moment constraint; the "
            "generalized lemma selects symmetric tails of the sum. <bookmark mark='c'/> And the sum over the root of "
            "the sum of squares is a monotone function of Student's t. <bookmark mark='d'/> So the two-sided t test "
            "is uniformly most powerful among unbiased tests: Part ten's workhorse, now with a theorem behind it, as "
            "Lehmann's Testing Statistical Hypotheses set out in 1959."
        ) as vo:
            heading=label('Conditional symmetric tails yield the two-sided normal t test',font_size=36).move_to([0,3.3,0])
            if heading.width>12.5: heading.width=12.5
            self.play(FadeIn(heading))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
