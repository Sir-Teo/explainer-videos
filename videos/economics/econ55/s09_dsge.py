from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403

PNAME = {"kappa": r"$\kappa$, \ Phillips slope", "sigma": r"$\sigma$, \ inverse EIS",
         "phi_pi": r"$\phi_\pi$, \ rule on inflation", "phi_x": r"$\phi_x$, \ rule on the gap",
         "rho_v": r"$\rho_v$, \ policy persistence"}


def histograms(D, names, width=2.45, height=1.9, post_color=EST):
    """One small panel per parameter: the prior (grey outline), the posterior (filled) and the truth (white)."""
    g = VGroup()
    for n in names:
        p = D["params"][n]
        e = np.array(p["edges"])
        top = max(max(p["prior"]), max(p["post"])) * 1.1
        ax = plane([e[0], e[-1]], [0, top], x_length=width, y_length=height, xticks=[], yticks=[], xlabel=r"",
                   ylabel=r"", font_size=10)
        bars = VGroup()
        for k, hgt in enumerate(p["post"]):
            if hgt <= 0:
                continue
            p0, p1 = ax.ax.c2p(e[k], 0), ax.ax.c2p(e[k + 1], hgt)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=post_color, fill_opacity=0.75,
                               stroke_width=0).move_to((p0 + p1) / 2))
        mids = (e[:-1] + e[1:]) / 2
        prior = path(ax, mids, p["prior"], GREY_B, 1.8)
        tv = D["truth"][D["names"].index(n)]
        truth = DashedLine(ax.ax.c2p(tv, 0), ax.ax.c2p(tv, top), color=TRUTHC, stroke_width=1.8)
        lab = label(PNAME[n], font_size=14, color=WHITE).next_to(ax, UP, buff=0.08)
        ratio = label(rf"width: \ {100 * p['ratio']:.0f}\% of the prior's", font_size=12, color=post_color).next_to(
            ax, DOWN, buff=0.08)
        g.add(VGroup(ax, bars, prior, truth, lab, ratio))
    return g.arrange(RIGHT, buff=0.25)


class DSGE(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Estimating a DSGE model", r"How is a whole model of the economy fitted to data?",
             "Chapter seven. Estimating a DSGE model.",
             lit={2007: r"An and Schorfheide; \ Smets and Wouters"}, scale=("nation",), horizon=("a decade",))
        self.state_space()
        self.data()
        self.posteriors()

    def state_space(self):
        eqs = VGroup(
            MathTex(r"\text{the model, solved:}\quad s_t = R\, s_{t-1} + w_t, \qquad y_t = \Gamma(\theta)\, s_t + e_t",
                    font_size=34, color=MODEL),
            MathTex(r"\text{the Kalman filter:}\quad \log p(y_1, \dots, y_T \mid \theta) = \sum_t \log "
                    r"\mathcal{N}\big(y_t;\ \hat y_{t \mid t-1},\ F_t\big)", font_size=34, color=DATA),
            MathTex(r"\text{Bayes:}\quad p(\theta \mid y) \propto p(y \mid \theta)\, p(\theta)", font_size=34,
                    color=EST),
            MathTex(r"\text{Metropolis--Hastings:}\quad \theta' = \theta + \text{step}; \ \text{accept with "
                    r"probability } \min\!\Big(1, \tfrac{p(\theta' \mid y)}{p(\theta \mid y)}\Big)", font_size=32,
                    color=THEORY),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.4)
        foot = label(r"Part 30's three equations: \ a demand curve, \ a Phillips curve, \ a Taylor rule; \ three "
                     r"shocks", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"An and Schorfheide, \ Econometric Reviews 26 (2007); \ Smets and Wouters, \ AER 97(3) "
                            r"(2007)", corner=DR, font_size=12)
        nk = VGroup(
            MathTex(r"x_t = \mathbb{E}_t x_{t+1} - \tfrac{1}{\sigma}\big(i_t - \mathbb{E}_t \pi_{t+1}\big) + d_t",
                    font_size=36, color=OUT),
            MathTex(r"\pi_t = \beta\, \mathbb{E}_t \pi_{t+1} + \kappa\, x_t + u_t", font_size=36, color=INFL),
            MathTex(r"i_t = \phi_\pi \pi_t + \phi_x x_t + v_t", font_size=36, color=RATE),
        ).arrange(DOWN, buff=0.5)
        nk_lab = VGroup(*[label(t_, font_size=20, color=c_) for t_, c_ in
                          ((r"demand", OUT), (r"Phillips curve", INFL), (r"Taylor rule", RATE))])
        for l_, e_ in zip(nk_lab, nk):
            l_.next_to(e_, LEFT, buff=0.6)
        nk_all = VGroup(nk, nk_lab).move_to(UP * 0.5)
        with self.voiceover(
            "Autoregressions ask what the data say about one shock at a time. A dynamic stochastic general "
            "equilibrium model, a DSGE model, claims to account for everything at once, and can be estimated "
            "whole. <bookmark mark='a'/> Solve the model, here Part thirty's three equations with a demand shock, a "
            "cost shock and a monetary shock, and it becomes a state-space system: hidden states that evolve, and "
            "observed series that are combinations of them. <bookmark mark='b'/> The Kalman filter, from Part "
            "thirty-one, turns that into a likelihood: for any parameters, how probable the observed history is. "
            "<bookmark mark='c'/> Multiply by a prior, what we believed before, and Bayes's rule gives the "
            "posterior. <bookmark mark='d'/> To explore it, the Metropolis-Hastings algorithm takes a random step, "
            "keeps it if the posterior is higher and sometimes even if it is lower, and repeats thousands of "
            "times. The places it visits are draws from the posterior. Sungbae An and Frank Schorfheide set out the "
            "recipe; Frank Smets and Rafael Wouters used it to estimate a model with seven observed series that "
            "central banks still build on."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot))
            self.play(LaggedStart(*[FadeIn(VGroup(e_, l_), shift=UP * 0.1) for e_, l_ in zip(nk, nk_lab)],
                                  lag_ratio=0.5), run_time=2.5)
            for mk, e_ in zip("abcd", eqs):
                vo.wait_until(mk)
                if mk == "a":
                    self.play(FadeOut(nk_all, shift=UP * 0.2), run_time=0.7)
                self.play(FadeIn(e_, shift=UP * 0.1), run_time=1.0)
        self.clear_scene()

    def data(self):
        D = load("dsge")
        Y = np.array(D["Y"])
        t = np.arange(len(Y))
        ax = plane([0, len(Y)], [-6, 6], center=LEFT * 0.6 + DOWN * 0.3, x_length=10.4, y_length=4.6,
                   xticks=[0, 40, 80, 120], yticks=[-4, 0, 4], xlabel=r"quarters", ylabel=r"",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   font_size=14)
        cols = (OUT, INFL, RATE)
        lines = VGroup(*[path(ax, t, Y[:, k], c, 2.0, smooth=False) for k, c in enumerate(cols)])
        key = VGroup(label(r"output gap", font_size=18, color=OUT), label(r"inflation", font_size=18, color=INFL),
                     label(r"the rate", font_size=18, color=RATE)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.5)
        tag = island_tag(rf"simulated: \ {D['T']} quarters of the Island's model", corner=DR, font_size=13)
        with self.voiceover(
            f"The Island's version: {D['T']} quarters of the output gap, inflation and the policy rate, generated "
            "by the model itself with parameters we chose. <bookmark mark='a'/> Here are the first thirty years. "
            "We estimate five parameters: the slope of the Phillips curve, the inverse of the elasticity of "
            "intertemporal substitution, the rule's response to inflation and to the output gap, and the "
            "persistence of policy shocks."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.3), FadeIn(key), run_time=3.0)
        self.clear_scene()

    def posteriors(self):
        D = load("dsge")
        g = histograms(D, D["names"]).move_to(UP * 0.5)
        if g.width > 13.4:
            g.width = 13.4
        key = VGroup(label(r"grey line: \ the prior", font_size=18, color=GREY_B),
                     label(r"gold: \ the posterior", font_size=18, color=EST),
                     label(r"white: \ the truth", font_size=18, color=TRUTHC)).arrange(RIGHT, buff=0.8).next_to(
            g, DOWN, buff=0.6)
        k = D["params"]["kappa"]
        foot = label(rf"{len(D['names'])} parameters, \ 6,000 draws \ (acceptance {100 * D['accept']:.0f}\%): \ "
                     r"every posterior far narrower than its prior", font_size=20, color=WHITE).next_to(
            key, DOWN, buff=0.4)
        tag = island_tag(r"simulated: \ the Island's model", corner=DR, font_size=13)
        with self.voiceover(
            "The results. <bookmark mark='a'/> For each parameter, the grey line is the prior, the gold bars the "
            "posterior, and the white line the truth. <bookmark mark='b'/> With all three series observed, every "
            "posterior is far narrower than its prior and sits near the truth: the Phillips curve's slope, for "
            f"instance, is {k['post_mean']:.3f}, with ninety percent of the posterior between {k['q05']:.3f} and "
            f"{k['q95']:.3f}, against a truth of {D['truth'][0]:.1f}. The data have taught us something about every "
            "parameter. <bookmark mark='c'/> That is not always so, as the next chapter shows."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in g], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(Indicate(foot, color=E.ACCENT, scale_factor=1.0))
        self.clear_scene()
