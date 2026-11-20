from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class IGE(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Like parent, \ like child? \ The elasticity and the Gatsby curve",
             r"How much of a parent's income advantage passes to the child?",
             "Chapter eight. Like parent, like child? The elasticity and the Gatsby curve.",
             lit={1992: r"Solon", 2005: r"Mazumder", 2013: r"Corak"}, scale=("household", "nation"),
             horizon=("a century",))
        self.define()
        self.attenuation()
        self.model()
        self.america()
        self.fact()

    def define(self):
        I = load("ige")
        ax = plane([-2.6, 2.6], [-2.4, 2.4], center=LEFT * 2.3 + DOWN * 0.4, x_length=6.0, y_length=5.2,
                   xticks=[-2, -1, 0, 1, 2], yticks=[-2, -1, 0, 1, 2],
                   xlabel=r"parent's log income, \ one year", ylabel=r"child's log income, \ long run",
                   xfmt=lambda v: f"{v:+.0f}", yfmt=lambda v: f"{v:+.0f}", font_size=14)
        pts = VGroup(*[dot(ax, a, b, PARENT, 0.03) for a, b in zip(I["scatter_p"], I["scatter_c"])
                       if abs(a) < 2.6 and abs(b) < 2.4])
        b1 = I["rows"][0]["ige"]
        truth = seg(ax, -2.4, -2.4 * I["beta"], 2.4, 2.4 * I["beta"], GAIN, 3.0)
        est = seg(ax, -2.4, -2.4 * b1, 2.4, 2.4 * b1, LOSS, 3.0)
        eq = MathTex(r"\ln y_{\mathrm{child}} = a + \beta\, \ln y_{\mathrm{parent}} + e", font_size=32).to_edge(
            UP, buff=0.35)
        side = VGroup(
            label(r"$\beta$: \ the intergenerational \\ elasticity; \ $1 - \beta$: \\ how fast families \\ regress "
                  r"to the mean", font_size=18, color=WHITE),
            label(rf"planted on the Island: \\ $\beta$ = {I['beta']:.2f}", font_size=19, color=GAIN),
            label(rf"estimated from one year \\ of parents' income: \\ {b1:.2f} \ (s.e. {I['rows'][0]['se']:.3f})",
                  font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the second half of the question: do children escape where they started? The classic measure is the "
            "intergenerational elasticity, beta: regress children's log income on their parents'. A beta of "
            "zero-point-four means a parent earning twice as much as another has children earning about a third "
            "more. <bookmark mark='a'/> Here are six hundred of the Island's families, where the truth is "
            f"planted: <bookmark mark='b'/> beta is {I['beta']:.2f}. <bookmark mark='c'/> But estimate it with one "
            f"year of the parents' income, as early studies did, and you get {b1:.2f}: families look more mobile "
            "than they are. One year of income is permanent income plus a good or bad year, and the noise "
            "flattens the slope."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(pts, lag_ratio=0.002), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(pts, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(est), FadeIn(side[2]))
        self.clear_scene()

    def attenuation(self):
        I = load("ige")
        rows = I["rows"]
        ax = plane([0, 16], [0, 0.7], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.8,
                   xticks=[1, 3, 5, 10, 15], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                   xlabel=r"years of parents' income averaged", ylabel=r"estimated elasticity",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        th = path(ax, I["curve_x"], I["curve_y"], THEORY, 2.6)
        truth = seg(ax, 0, I["beta"], 16, I["beta"], GAIN, 2.0, dashed=True)
        pts = VGroup(*[VGroup(dot(ax, r["years"], r["ige"], LOSS, 0.09),
                              Line(ax.ax.c2p(r["years"], r["ige"] - 1.96 * r["se"]),
                                   ax.ax.c2p(r["years"], r["ige"] + 1.96 * r["se"]), color=LOSS, stroke_width=2))
                       for r in rows])
        eq = MathTex(r"\operatorname{plim} \hat\beta_T = \beta \cdot \frac{\sigma_{\mathrm{perm}}^2}"
                     r"{\sigma_{\mathrm{perm}}^2 + \sigma_{\mathrm{trans}}^2 / T}", font_size=30).to_edge(UP, buff=0.3)
        S = I["studies"]
        side = VGroup(
            label(r"red: \ estimates; \ teal: \\ the attenuation formula", font_size=17, color=WHITE),
            label(rf"Solon (1992), \ several \\ years: \ {S['solon']:.1f} or higher", font_size=18, color=TOP),
            label(rf"Mazumder (2005), \ long \\ Social Security spells: \\ about {S['mazumder']:.1f}", font_size=18,
                  color=TOP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The fix is to average. With T years of parents' income, the transitory part shrinks by T, and the "
            "estimate climbs towards the truth by exactly the factor in this formula. <bookmark mark='a'/> On the "
            f"Island: {rows[0]['ige']:.2f} with one year, {rows[2]['ige']:.2f} with five, {rows[-1]['ige']:.2f} with "
            "fifteen. <bookmark mark='b'/> This is the history of the American estimates. Early studies with a "
            "single year found about 0.2, and concluded that America was very mobile. In 1992 Gary Solon averaged "
            "several years and found 0.4 or higher. <bookmark mark='c'/> In 2005 Bhashkar Mazumder used long spells "
            "of fathers' Social Security earnings, and found about 0.6. Measurement error had made America look "
            "more mobile than it was."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), Create(truth), Create(th), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def model(self):
        G = load("gatsby")
        ax = plane([0.25, 0.65], [0, 0.5], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.4, y_length=4.8,
                   xticks=[0.3, 0.4, 0.5, 0.6], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5],
                   xlabel=r"inequality: \ Gini", ylabel=r"immobility: \ intergenerational elasticity",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        pts = VGroup(*[dot(ax, g, b, TOP, 0.09) for g, b in zip(G["gini"], G["ige"])])
        ln = path(ax, G["gini"], G["ige_theory"], THEORY, 2.6)
        side = VGroup(
            label(r"each dot: \ an economy \\ that differs only in \\ the return to skill", font_size=18,
                  color=WHITE),
            label(rf"skill is inherited \\ (half of it, $\lambda$ = {G['lam']:.1f}); \\ luck is not", font_size=18,
                  color=GREY_A),
            label(r"a higher return \\ widens the distribution \\ and tightens the link", font_size=18,
                  color=TOP),
            label(r"Corak's 22 countries: \\ from below 0.2 \\ (the Nordic countries) \\ to almost 0.7 (Peru)",
                  font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        hc = history_card(2013, r"Miles Corak", r"across 22 countries, \ the elasticity runs from below 0.2 in "
                          r"Denmark, \ Norway and Finland to almost 0.7 in Peru, \ and is higher where inequality is "
                          r"higher: \ Alan Krueger's `Great Gatsby curve'", color=E.ACCENT, width=10.4, font_size=24)
        with self.voiceover(
            "Across countries, the elasticity runs from below 0.2 in Denmark, Norway and Finland to almost 0.7 in "
            "Peru, and Miles Corak showed in 2013 that it is higher where inequality is higher. Alan Krueger named "
            "the pattern the Great Gatsby curve. Why might they go together? <bookmark mark='a'/> On the Island, "
            "build economies that differ in one thing only: how much the labour market pays for skill. "
            "<bookmark mark='b'/> Skill is partly inherited, and luck is not. <bookmark mark='c'/> Where skill pays "
            "more, incomes spread out, and because skill runs in families, parents' incomes predict their "
            "children's more closely: <bookmark mark='d'/> the economies line up on a Gatsby curve. The curve need "
            "not mean that inequality causes immobility; one cause can produce both."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(hc), run_time=0.6)
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[3]), FadeIn(side[0]),
                      LaggedStart(*[FadeIn(p_, scale=1.4) for p_ in pts], lag_ratio=0.25), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(pts, color=WHITE, scale_factor=1.1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ln))
        self.clear_scene()

    def america(self):
        G = load("gatsby")
        ax = plane([0.05, 0.45], [25, 65], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.8,
                   xticks=[0.1, 0.2, 0.3, 0.4], yticks=[30, 40, 50, 60],
                   xlabel=r"Gini of the bottom 99\%, \ by commuting zone",
                   ylabel=r"upward mobility: \ the expected rank \\ of a child from the 25th percentile",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        pop = np.array(G["cz_pop"])
        rr = 0.02 + 0.06 * np.sqrt(pop / pop.max())
        pts = VGroup(*[Dot(ax.ax.c2p(g, a), radius=float(r), color=CHILD, fill_opacity=0.55)
                       for g, a, r in zip(G["cz_gini"], G["cz_am"], rr) if 25 <= a <= 65])
        b = G["fit"]
        fit = seg(ax, 0.06, b[1] + b[0] * 0.06, 0.44, b[1] + b[0] * 0.44, WHITE, 3)
        side = VGroup(
            label(rf"{G['cz_n']} commuting zones; \\ larger dots: \ more people", font_size=17, color=GREY_A),
            label(rf"correlation, \ weighted \\ by population: \ {G['corr_am']:.2f}", font_size=19, color=WHITE),
            label(r"more unequal places: \\ less upward mobility", font_size=18, color=CHILD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Chetty, \ Hendren, \ Kline and Saez (2014), \ Online Data Tables V and VIII", corner=DR,
                       font_size=11)
        with self.voiceover(
            "The curve appears within America too. <bookmark mark='a'/> Here are the country's commuting zones, "
            "local labour markets, sized by population. Across, the inequality of incomes among the bottom ninety-"
            "nine percent; up, how high a child from a family at the twenty-fifth percentile is expected to rise. "
            f"<bookmark mark='b'/> The correlation is {say_num(G['corr_am'], 2)}: <bookmark mark='c'/> in more "
            "unequal places, children from poorer families rise less. Where those numbers come from is the subject "
            "of the next two chapters."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(pts, lag_ratio=0.002), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def fact(self):
        G = load("gatsby")
        f = facts.BY_KEY["gatsby"]
        data_m = label(rf"22 countries: \ below 0.2 \\ to almost 0.7; \\ America's places: \\ correlation "
                       rf"{G['corr_am']:.2f}", font_size=18, color=WHITE)
        theory_m = label(r"one cause, \ two effects: \\ a high return to \\ inherited skill", font_size=18,
                         color=THEORY)
        agora_m = label(rf"economies differing \\ in the return to skill: \\ Gini {G['gini'][0]:.2f} to "
                        rf"{G['gini'][-1]:.2f}, \\ elasticity {G['ige'][0]:.2f} to {G['ige'][-1]:.2f}",
                        font_size=18, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, THEORY, None)).move_to(UP * 0.3)
        tag = published_tag(tables.IGE_STUDIES.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The Gatsby curve is one of the series' facts. <bookmark mark='a'/> In the data, more unequal countries, "
            "and more unequal American places, have less mobility. <bookmark mark='b'/> One theory: a high return "
            "to skills that families pass on. <bookmark mark='c'/> And in Agora, raising only that return moves an "
            f"economy up the curve, from a Gini of {G['gini'][0]:.2f} and an elasticity of {G['ige'][0]:.2f} to "
            f"{G['gini'][-1]:.2f} and {G['ige'][-1]:.2f}."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(fc.cols[k][2:]))
        self.clear_scene()
