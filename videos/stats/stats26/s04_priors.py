from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403

PCOL = {"uniform": S.EST, "halfcauchy": S.KEPT, "ig1": S.POST, "ig001": S.RESID}
PNAME = {"uniform": r"uniform on $\tau$", "halfcauchy": r"half-Cauchy(25)", "ig1": r"inv-gamma(1, 1) on $\tau^2$",
         "ig001": r"inv-gamma(.001, .001)"}


class Priors(VoiceoverScene):
    def construct(self):
        self.card()
        self.invariance()
        self.jeffreys_picture()
        self.reference()
        self.weak()
        self.sensitivity("eight")
        self.sensitivity("three")
        self.improper()

    def card(self):
        card = chapter_card(3, r"Priors", r"Invariance, \ reference, \ and weak information", lit=(1946, 2006), part=PART)
        with self.voiceover("Chapter three. Priors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def invariance(self):
        rows = [
            cmath(r"\text{flat on } p", r"\ne", r"\text{flat on } \log\tfrac{p}{1 - p}", font_size=30),
            cmath(r"p(\theta)", r"\propto", r"\sqrt{\det I(\theta)}", font_size=32),
            cmath(r"\eta = g(\theta)", r":", r"\sqrt{I(\eta)} = \sqrt{I(\theta)}\,|d\theta/d\eta|: \ \text{the same prior}", font_size=28),
            cmath(r"\text{binomial}", r":", r"I(p) = \tfrac{n}{p(1 - p)} \ \Rightarrow \ \text{Beta}(\tfrac12, \tfrac12)", font_size=30),
        ]
        rows[1][2].set_color(PRIOR)
        whys = [why(r"`ignorance' depends on the scale"), why(r"Jeffreys (1946)"),
                why(r"the rule gives the same answer on any scale"), why(r"Part 22's Fisher information")]
        intro = label('A change of variables changes a density through its Jacobian', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Part 15 met the problem: a flat prior on a probability isn't flat on its log odds, so "
            "'knowing nothing' depends on the scale you happen to write the parameter in. <bookmark mark='b'/> Harold "
            "Jeffreys's 1946 answer: take the prior proportional to the square root of the Fisher information. "
            "<bookmark mark='c'/> Under any change of variables, the information transforms with exactly the Jacobian that "
            "a density needs, so the rule gives the same prior whichever scale you start from. <bookmark mark='d'/> For a "
            "binomial proportion it's the beta of a half and a half."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def jeffreys_picture(self):
        d = load("jeffreys")
        A = axes([0, 1], [0, 4], x_length=5.2, y_length=3.6, xlabel=r"$p$", ylabel=r"prior density", xticks=[0, 0.5, 1],
                 yticks=[0, 2, 4], center=[-3.4, 0.4, 0])
        B_ = axes([-6, 6], [0, 0.3], x_length=5.2, y_length=3.6, xlabel=r"log odds $\eta$", ylabel=r"", xticks=[-6, 0, 6],
                  yticks=[0, 0.15, 0.3], center=[3.2, 0.4, 0])
        p, eta = np.asarray(d["p"]), np.asarray(d["eta"])
        uni_p = Line(A.ax.c2p(0, 1), A.ax.c2p(1, 1), color=RAW, stroke_width=3)
        jef_p = curve(A.ax, p, d["jef_p"], PRIOR, 3)
        uni_e = curve(B_.ax, eta, d["unif_eta"], RAW, 3)
        jef_e = curve(B_.ax, eta, d["jef_eta"], PRIOR, 3)
        rows = fit_rows(VGroup(
            label(r"blue: \ flat on $p$, \ seen on both scales", font_size=22, color=RAW),
            label(r"purple: \ Jeffreys's Beta($\tfrac12, \tfrac12$), \ on both scales", font_size=22, color=PRIOR),
            label(r"a flat prior on $p$ is a confident hump on $\eta$", font_size=22, color=RES),
        ), 12.0, 0.2, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the left, priors for a proportion; on the right, the same priors seen on the log-odds "
            "scale. The flat prior on p, in blue, becomes a hump on the log odds, quite confident that the odds are "
            "moderate. <bookmark mark='b'/> Jeffreys's prior, in purple, piles up at zero and one on the p scale and is "
            "broader on the log-odds scale; it is the same rule applied to either, and the two pictures are the same "
            "distribution. <bookmark mark='c'/> No prior is uninformative on every scale; Jeffreys's is at least "
            "consistent."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B_))
            vo.wait_until("a")
            self.play(Create(uni_p), Create(uni_e), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(jef_p), Create(jef_e), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def reference(self):
        rows = [
            cmath(r"\text{reference prior}", r":", r"\text{asymptotic expected posterior-to-prior KL}", font_size=28),
            cmath(r"\text{one parameter}", r":", r"\text{Jeffreys's prior}", font_size=30),
            cmath(r"\text{nuisance parameters}", r":", r"\text{order them; \ avoids Jeffreys's multi-parameter failures}", font_size=28),
            cmath(r"N(\mu, \sigma^2)", r":", r"\text{Jeffreys } \sigma^{-2}; \ \text{reference } \sigma^{-1}, \ \text{matching } t", font_size=28),
        ]
        rows[0][2].set_color(PRIOR)
        whys = [why(r"Bernardo (1979): \ let the data say the most"), why(r"under regularity"),
                why(r"Berger \& Bernardo (1992)"), why(r"the reference posterior gives Student's interval")]
        intro = label('Reference priors use an ordered, asymptotic information criterion', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> José Bernardo's reference priors of 1979 ask for the prior from which the data are "
            "expected to teach the most, measured by expected posterior-to-prior Kullback–Leibler information in a "
            "regular repeated-sampling limit. <bookmark mark='b'/> For one regular parameter, that is Jeffreys's "
            "prior again. <bookmark mark='c'/> With nuisance parameters, Bernardo and James Berger handle them in "
            "order of interest, avoiding the cases where Jeffreys's rule misbehaves in many dimensions. <bookmark "
            "mark='d'/> For a normal mean and variance, Jeffreys's joint rule gives one over sigma squared; the "
            "reference prior gives one over sigma, and its posterior interval for the mean is exactly Student's t "
            "interval, so the frequentist and Bayesian answers coincide."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def weak(self):
        rows = [
            cmath(r"\text{weakly informative}", r":", r"\text{rule out the absurd, \ not the plausible}", font_size=30),
            cmath(r"\tau", r"\sim", r"\text{half-Cauchy}(0, 25): \ \text{most mass below 50 SAT points}", font_size=28),
            cmath(r"\tau^2", r"\sim", r"\text{inv-gamma}(\epsilon, \epsilon): \ \text{looks vague, \ is not}", font_size=28),
            cmath(r"\text{test}", r":", r"\text{does the answer change when the prior does?}", font_size=30),
        ]
        rows[1][2].set_color(SHRUNK)
        whys = [why(r"Gelman (2006)"), why(r"a scale chosen from the problem"), why(r"a near-zero density mode and an extreme tail"),
                why(r"sensitivity analysis")]
        intro = label('A density mode near zero does not describe the entire prior mass', font_size=36).move_to([0, 3.3, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> Andrew Gelman's 2006 paper argued for weakly informative priors: priors that rule "
            "out the absurd without ruling out the plausible. <bookmark mark='b'/> For tau, a half-Cauchy with scale "
            "twenty-five points: most of its mass is below fifty, since a coaching course that moves SAT scores by a "
            "hundred points between schools is absurd, but it has a long tail. <bookmark mark='c'/> The popular "
            "inverse-gamma with tiny parameters on tau squared looks vague and isn't: its density can peak near a "
            "tiny positive variance while retaining an extremely heavy tail. That is not a neutral prior; in this "
            "example it pushes the posterior towards zero. <bookmark mark='d'/> The test of any prior is whether the "
            "answer changes when the prior does."
        ) as vo:
            self.add(intro)
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sensitivity(self, subset):
        d = load("priors")
        tau = np.asarray(d["tau"])
        sub = d[subset]
        eta = np.log10(tau)
        densities = {k: tau*np.log(10)*np.asarray(sub[k]["dens"]) for k in PCOL}
        ymax = 1.1*max(a.max() for a in densities.values())
        A = axes([-3, 3], [0, ymax], x_length=7.4, y_length=4.4, xlabel=r"$\tau$ (log scale)", ylabel=r"density per log unit",
                 xticks=[-3,-2,-1,0,1,2,3], xfmt=lambda v: rf"10^{{{int(v)}}}", yticks=[0, ymax / 2, ymax], center=[-2.1, 0.3, 0], yfmt=lambda v: f"{v:.2f}")
        ax = A.ax
        cs = VGroup(*[curve(ax, eta, densities[k], PCOL[k], 3) for k in PCOL])
        rows = fit_rows(VGroup(
            *[label(rf"{PNAME[k]}: \ median {sub[k]['median']:.1f}, \ 95\% below {sub[k]['q95']:.0f}", font_size=20, color=PCOL[k]) for k in PCOL],
        ), 4.4, 0.42, [4.5, 0.3, 0])
        n = "all eight schools" if subset == "eight" else "only schools A, B and C"
        head = label(rf"$p(\log_{10}\tau \mid y)$ under four priors: \ {n}", font_size=24).to_edge(UP, buff=0.35)
        if subset == "eight":
            text = ("<bookmark mark='a'/> Here are the posteriors per log-tau unit for all eight schools. Quantiles retain the tails beyond the viewport. "
                    "<bookmark mark='b'/> The uniform and the half-Cauchy agree closely: medians of five point two and four "
                    "point eight. <bookmark mark='c'/> The inverse-gammas disagree with both: with parameters one and one, "
                    "the median is one point two; with point oh oh one, the posterior piles against zero, with a median of "
                    "point six. <bookmark mark='d'/> These are supposed to be the vague ones, and they are the ones driving "
                    "the answer.")
        else:
            text = ("<bookmark mark='a'/> With only three schools the data say even less. <bookmark mark='b'/> The uniform "
                    "prior leaves a heavy right tail: median twenty-three and five percent beyond two hundred and eighty-five. "
                    "About a third of its probability lies beyond the old plotting limit of forty. The half-Cauchy reduces that tail. "
                    "<bookmark mark='c'/> The inverse-gammas again force tau towards zero. <bookmark mark='d'/> Gelman's "
                    "advice: a uniform prior on tau is fine with many groups; with few, use a half-Cauchy or half-normal "
                    "with a problem-informed scale. Do not assume an inverse-gamma with tiny parameters is vague.")
        with self.voiceover(text) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(cs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cs[2]), Create(cs[3]), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(*[Indicate(r, scale_factor=1.05) for r in rows[2:]])
        self.clear_scene()

    def improper(self):
        d = load("priors")["improper"]
        lt = np.asarray(d["logtau"])
        A = axes([-12, 4], [0, 1.2], x_length=7.4, y_length=4.0, xlabel=r"$\log\tau$", ylabel=r"posterior density of $\log\tau$, \ unnormalized",
                 xticks=[-12, -8, -4, 0, 4], yticks=[0, 0.5, 1], center=[-2.1, 0.3, 0])
        ax = A.ax
        c = curve(ax, lt, d["dens_logtau"], RES, 3.5)
        arrow = Arrow(ax.c2p(-6, 1.1), ax.c2p(-11.8, 1.1), color=RES, buff=0, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"prior: \ flat on $\log\tau$, \ i.e.\ $p(\tau) \propto 1/\tau$", font_size=22),
            label(r"as $\tau \to 0$ the likelihood tends to a constant", font_size=22, color=GREY_A),
            label(r"so the posterior stays flat forever to the left", font_size=22, color=RES),
            label(r"infinite area: \ an improper posterior", font_size=22, color=RES),
            label(r"an MCMC sampler would not complain", font_size=22, color=PATH),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> An improper prior is acceptable only if the posterior comes out proper. Take the "
            "'scale-invariant' prior that is flat on log tau. <bookmark mark='b'/> As tau goes to zero, the "
            "likelihood doesn't vanish; it tends to the likelihood of complete pooling. <bookmark mark='c'/> So the "
            "posterior of log tau stays flat all the way to minus infinity, <bookmark mark='d'/> and has infinite "
            "area: there is no posterior at all. <bookmark mark='e'/> A sampler can produce plausible-looking output "
            "while drifting towards zero; it need not diagnose an improper target. Check propriety, or use a proper "
            "prior."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
