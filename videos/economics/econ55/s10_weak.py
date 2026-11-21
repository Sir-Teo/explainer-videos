from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403
from videos.economics.econ55.s09_dsge import histograms


class Weak(VoiceoverScene):
    def construct(self):
        card(self, 8, r"What the data cannot tell apart", r"When does a posterior just repeat the prior?",
             "Chapter eight. What the data cannot tell apart.", lit={2009: r"Canova and Sala"}, scale=("nation",),
             horizon=("a decade",))
        self.drop()
        self.profile()

    def drop(self):
        D = load("dsge_weak")
        g = histograms(D, D["names"], post_color=MODEL).move_to(UP * 0.5)
        if g.width > 13.4:
            g.width = 13.4
        key = VGroup(label(r"grey line: \ the prior", font_size=18, color=GREY_B),
                     label(r"purple: \ the posterior, \ without the rate", font_size=18, color=MODEL),
                     label(r"white: \ the truth", font_size=18, color=TRUTHC)).arrange(RIGHT, buff=0.8).next_to(
            g, DOWN, buff=0.6)
        weak = [n for n in D["names"] if D["params"][n]["ratio"] > 0.5]
        foot = label(rf"{len(weak)} of {len(D['names'])} posteriors are more than half as wide as their priors",
                     font_size=21, color=E.ACCENT).next_to(key, DOWN, buff=0.4)
        tag = published_tag(r"Canova and Sala, \ Journal of Monetary Economics 56(4) (2009)", corner=DR, font_size=12)
        kp = D["params"]["kappa"]
        with self.voiceover(
            "Now estimate the same model from the same history, but suppose the policy rate is not observed: only "
            "the output gap and inflation. <bookmark mark='a'/> The Phillips curve's slope is still learned, its "
            f"posterior {100 * kp['ratio']:.0f} percent as wide as the prior. <bookmark mark='b'/> But look at the "
            f"other four. Their posteriors are {100 * min(D['params'][n]['ratio'] for n in weak):.0f} to "
            f"{100 * max(D['params'][n]['ratio'] for n in weak):.0f} percent as wide as their priors, and centred "
            "near them. The answer looks like an estimate, with a mean and a band, but it is mostly the prior "
            "coming back out. <bookmark mark='c'/> Fabio Canova and Luca Sala showed that this happens in "
            "published models: some parameters barely move the likelihood, and a Bayesian posterior hides that "
            "unless it is compared with its prior."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(key), LaggedStart(*[FadeIn(p_) for p_ in g], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(g[0], color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(*[Indicate(g[D["names"].index(n)], color=MODEL, scale_factor=1.02) for n in weak])
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def profile(self):
        P = load("profile")
        g = np.array(P["grid"])
        ax = plane([0.5, 3.1], [-40, 3], center=LEFT * 1.8 + DOWN * 0.35, x_length=7.6, y_length=4.8,
                   xticks=[0.6, 1.0, 1.5, 2.0, 2.5, 3.0], yticks=[-40, -30, -20, -10, 0],
                   xlabel=r"$\sigma$, \ fixed", ylabel=r"log likelihood, \ below its best", xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        full = path(ax, g, P["full"], EST, 3.0, yr=(-40, 3))
        two = path(ax, g, P["two"], MODEL, 3.0)
        tv = vline(ax, P["truth"], -40, 3, TRUTHC, 1.6)
        side = VGroup(
            label(r"for each $\sigma$, \ the other \\ four re-estimated", font_size=18, color=WHITE),
            label(rf"gold: \ the rate observed: \\ a peak, \ {abs(P['full'][-1]):.0f} log points \\ deep by "
                  r"$\sigma = 3$", font_size=18, color=EST),
            label(rf"purple: \ without it: \\ {abs(min(P['two'])):.1f} log points \\ across the whole range",
                  font_size=18, color=MODEL),
            label(r"a flat likelihood: \\ the prior decides", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"simulated: \ the Island's model", corner=DR, font_size=13)
        with self.voiceover(
            "Here is why. Fix sigma, re-estimate the other four, and record how well the model can then fit. "
            f"<bookmark mark='a'/> With the rate observed, the fit falls off sharply on either side of the best "
            f"value, by {abs(P['full'][-1]):.0f} log points by a sigma of three: sigma is pinned. <bookmark "
            f"mark='b'/> Without the rate, the fit changes by only {abs(min(P['two'])):.1f} log points across the "
            "whole range: almost any sigma can be made to fit by adjusting the others. <bookmark mark='c'/> When "
            "the likelihood is flat, the prior decides. The cure is not a cleverer sampler; it is data that move "
            "the parameter, here the rate itself."
        ) as vo:
            self.play(FadeIn(ax), Create(tv), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(full), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(two), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
