from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Pareto(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Pareto tails and random growth", r"Why do incomes have such long tails?",
             "Chapter four. Pareto tails and random growth.", lit={1896: r"Pareto", 1953: r"Champernowne",
                                                                   2009: r"Gabaix"},
             scale=("person", "nation"), horizon=("a decade", "a century"))
        self.law()
        self.exponent()
        self.careers()
        self.derive()
        self.fact()

    def law(self):
        P = load("pareto")
        ax = plane([-4.2, -0.8], [-2.8, -0.2], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.4, y_length=5.0,
                   xticks=[-4, -3, -2, -1], yticks=[-2.5, -2, -1.5, -1, -0.5],
                   xlabel=r"the richest fraction $p$ \ (log scale)", ylabel=r"their share of income \ (log scale)",
                   xfmt=lambda v: {-4: "0.01\\%", -3: "0.1\\%", -2: "1\\%", -1: "10\\%"}.get(round(v), ""),
                   yfmt=lambda v: f"{100 * 10 ** v:.1f}\\%" if v < -1.5 else f"{100 * 10 ** v:.0f}\\%",
                   font_size=14)
        groups = VGroup()
        for y, col in (("1970", BOTTOM), ("2022", TOP)):
            t = P["tails"][y]
            lp, ls = np.log10(t["p"]), np.log10(np.array(t["share"]) / 100)
            pts = VGroup(*[dot(ax, a, b, col, 0.08) for a, b in zip(lp, ls)])
            fit = seg(ax, -4.1, ls[-1] + t["slope"] * (-4.1 - lp[-1]), -0.9, ls[-1] + t["slope"] * (-0.9 - lp[-1]),
                      col, 2.4)
            groups.add(VGroup(pts, fit))
        eq = MathTex(r"P(\text{income} > x) \propto x^{-\alpha} \ \Rightarrow \ "
                     r"\text{share of the top } p \propto p^{\,1 - 1/\alpha}", font_size=30).to_edge(UP, buff=0.35)
        side = VGroup(
            label(r"each dot: \ the top 10\%, 5\%, 1\%, \\ 0.5\%, 0.1\% and 0.01\%", font_size=17, color=GREY_A),
            label(rf"1970: \ slope {P['tails']['1970']['slope']:.2f}, \\ $\alpha$ = {P['tails']['1970']['alpha']:.2f}",
                  font_size=19, color=BOTTOM),
            label(rf"2022: \ slope {P['tails']['2022']['slope']:.2f}, \\ $\alpha$ = {P['tails']['2022']['alpha']:.2f}",
                  font_size=19, color=TOP),
            label(r"a straight line: \\ the same shape at \\ every level of the top", font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = data_tag(tables.PIKETTY_SAEZ_2003.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 1896 Vilfredo Pareto, working through tax records from several countries, noticed that the number of "
            "people with incomes above x fell like x to a fixed power, minus alpha. If that holds, the share of "
            "income held by the richest fraction p is proportional to p to the power one minus one over alpha: on "
            "logarithmic scales, a straight line. <bookmark mark='a'/> Here are America's top shares in 1970, from "
            "the top ten percent to the top one in ten thousand. <bookmark mark='b'/> A straight line, with slope "
            f"{P['tails']['1970']['slope']:.2f}: alpha about {P['tails']['1970']['alpha']:.1f}. "
            "<bookmark mark='c'/> In 2022, another straight line, flatter, with alpha about "
            f"{P['tails']['2022']['alpha']:.1f}. <bookmark mark='d'/> The smaller alpha, the fatter the tail: within "
            "the top one percent, the top tenth then holds a larger share, and the same again within that tenth. The "
            "tail looks the same at every scale."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(groups[0][0], lag_ratio=0.2),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(groups[0][0], color=WHITE))
            vo.wait_until("b")
            self.play(Create(groups[0][1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(groups[1][0], lag_ratio=0.2), Create(groups[1][1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def exponent(self):
        P = load("pareto")
        ys, a = np.array(P["years"]), np.array(P["alpha"])
        ax = plane([1910, 2025], [1.2, 2.8], center=LEFT * 1.4 + DOWN * 0.4, x_length=9.2, y_length=4.8,
                   xticks=[1920, 1940, 1960, 1980, 2000, 2020], yticks=[1.2, 1.6, 2.0, 2.4, 2.8],
                   ylabel=r"Pareto exponent $\alpha$, \ from the top 1\% and top 0.1\% shares",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        ln = path(ax, ys, a, TOP, 3.2, smooth=False)
        side = VGroup(
            label(rf"1928: \ {P['a1928']:.2f}", font_size=19, color=WHITE),
            label(rf"{P['amax_year']}: \ {P['amax']:.2f}, \ the thinnest", font_size=19, color=BOTTOM),
            label(rf"2022: \ {P['a2022']:.2f}", font_size=19, color=TOP),
            label(r"lower $\alpha$: \ a fatter tail", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"computed from Piketty and Saez's shares", corner=DR, font_size=12)
        with self.voiceover(
            "From the ratio of two top shares, each year's alpha follows. <bookmark mark='a'/> In 1928 it was "
            f"{P['a1928']:.2f}, a fat tail. <bookmark mark='b'/> The tail thinned through the war and after, to "
            f"{P['amax']:.2f} in {P['amax_year']}. <bookmark mark='c'/> Since then it has fattened again, to "
            f"{P['a2022']:.2f} in 2022. Pareto's law has held for a century; what moves is its exponent. Why should "
            "incomes have such a tail at all?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            for mk, r_ in zip("abc", side[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def careers(self):
        G = load("growth")
        ax = plane([0, 60], [-1.2, 2.5], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.8,
                   xticks=[0, 10, 20, 30, 40, 50, 60], yticks=[np.log(v) for v in (0.5, 1, 2, 4, 8)],
                   xlabel=r"years into a career", ylabel=r"income \ (the starting income = 1, \ log scale)",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{np.exp(v):.3g}", font_size=14)
        cols = (BOTTOM, MIDDLE, TOP, CHILD, WEALTH)
        lines = VGroup(*[path(ax, list(range(61)), np.log(p), c, 2.6, smooth=False) for p, c in
                         zip(G["paths"], cols)])
        floor = seg(ax, 0, -1.0, 60, -1.0, GREY_D, 1.5, dashed=True)
        at40 = [p[40] for p in G["paths"]]
        down = sum(v < 1 for v in at40)
        best = max(at40)
        eq = MathTex(r"\ln x_{t+1} = \ln x_t + \nu + \sigma \varepsilon_{t+1}", font_size=32).to_edge(UP, buff=0.35)
        side = VGroup(
            label(rf"each year: \ a random \\ percentage change, \\ $\sigma$ = {100 * G['sigma1']:.1f}\%", font_size=18,
                  color=WHITE),
            label(r"a floor: \ a third of \\ the starting income", font_size=18, color=GREY_A),
            label(rf"careers end at rate \\ $\delta$ = {G['delta']:.3f} \ (40 years \\ on average); \ newcomers \\ "
                  r"start at 1", font_size=18, color=GREY_A),
            label(r"luck compounds", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The answer most economists now give goes back to David Champernowne in 1953: random growth. On the "
            "Island, each year every income changes by a random percentage, a promotion, a bad year, a lucky "
            f"client, with a spread of {100 * G['sigma1']:.0f} percent, and no one falls below a floor of a third of "
            "the starting income. <bookmark mark='a'/> Here are five careers that start at the same income. "
            f"Percentage changes compound: <bookmark mark='b'/> after forty years, {down} of the five earn less than "
            f"when they started, and one earns {best:.0f} times as much. <bookmark mark='c'/> Careers end, on average "
            "after forty years, and newcomers start again at the bottom. Without that, incomes would spread out for "
            "ever; with it, the distribution settles down."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(floor), FadeIn(side[1]),
                      run_time=1.5)
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), run_time=5.0)
            vo.wait_until("a")
            self.play(Indicate(lines, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def derive(self):
        G = load("growth")
        ax = plane([0, 3.0], [-4.6, 0], center=LEFT * 2.4 + DOWN * 0.6, x_length=6.4, y_length=4.4,
                   xticks=[0, 1, 2, 3], yticks=[-4, -3, -2, -1, 0], xlabel=r"income, \ relative to the start "
                   r"\ (log scale)", ylabel=r"share of people above it \ (log scale)",
                   xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{10 ** v:g}", font_size=13)
        gx, gs = np.log10(G["grid"]), np.array(G["surv"])
        m = gs > 0
        sim = VGroup(*[dot(ax, a, np.log10(b), TOP, 0.045) for a, b in zip(gx[m][::2], gs[m][::2])
                       if a <= 3.0 and np.log10(b) >= -4.6])
        kx, ks = np.log10(G["kfe_x"]), np.array(G["kfe_surv"])
        k = (kx >= 0) & (kx <= 3.0) & (ks > 10 ** -4.6)
        kfe = path(ax, kx[k], np.log10(ks[k]), THEORY, 3.0, smooth=False)
        steps = VGroup(
            MathTex(r"\partial_t f = -\nu\, \partial_y f + \tfrac{\sigma^2}{2}\, \partial_{yy} f - \delta f "
                    r"+ \delta\, \mathbb{1}_{y = 0}", font_size=28),
            MathTex(r"\text{stationary, above the entry point: } f(y) \propto e^{-\zeta y}", font_size=26),
            MathTex(r"\tfrac{\sigma^2}{2}\zeta^2 + \nu \zeta - \delta = 0 \ \Rightarrow \ "
                    r"\zeta = \frac{-\nu + \sqrt{\nu^2 + 2\sigma^2\delta}}{\sigma^2}", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.3).to_edge(RIGHT, buff=0.3)
        side = VGroup(
            label(rf"theory: \ $\zeta$ = {G['zeta']:.2f}", font_size=20, color=THEORY),
            label(rf"{G['n']:,} simulated careers: \\ Hill's estimate {G['hill']:.2f}", font_size=19, color=TOP),
            label(rf"top 1\% share: \ {100 * G['top1_kfe']:.0f}\% \\ (simulated: {100 * G['top1_sim']:.0f}\%)",
                  font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Simulate {G['n']:,} careers for three centuries, until the distribution stops changing. "
            "<bookmark mark='a'/> On logarithmic scales, the share of people above each income falls on a straight "
            "line: a Pareto tail, from nothing but compounding luck and turnover. <bookmark mark='b'/> Why a straight "
            "line? Write y for log income and f for its density. f changes because incomes drift, because they "
            "spread, because careers end, and because newcomers enter: the Kolmogorov forward equation. "
            "<bookmark mark='c'/> In the stationary state, above the entry point, the solution is an exponential in "
            "y, which is a power law in income. <bookmark mark='d'/> Substituting gives a quadratic for the exponent "
            f"zeta. With the Island's numbers, zeta is {G['zeta']:.2f}; <bookmark mark='e'/> the simulation agrees, "
            f"and the top one percent take about {100 * G['top1_kfe']:.0f} percent of income. The formula says what "
            "fattens the tail: more volatile incomes, faster average growth at the top, or longer careers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(sim, lag_ratio=0.01), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Write(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), Create(kfe), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def fact(self):
        G = load("growth")
        P = load("pareto")
        f = facts.BY_KEY["pareto"]
        data_m = label(rf"America's top incomes: \\ $\alpha$ = {P['a1970']:.1f} in 1970, \\ {P['a2022']:.1f} in 2022",
                       font_size=18, color=WHITE)
        theory_m = label(r"random proportional \\ growth with turnover \\ (Champernowne; \ Gabaix)", font_size=18,
                         color=THEORY)
        agora_m = label(rf"the Kolmogorov equation's \\ tail, \ $\zeta$ = {G['zeta']:.2f}, \\ matches the "
                        rf"simulation", font_size=18, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, THEORY, None)).move_to(UP * 0.3)
        tag = published_tag(tables.PARETO_1896.tag, corner=DR, font_size=11)
        with self.voiceover(
            "That makes Pareto tails one of the series' facts. <bookmark mark='a'/> In the data, top incomes follow "
            "Pareto's law, with an exponent that moves. <bookmark mark='b'/> The theory: proportional random growth "
            "with turnover. <bookmark mark='c'/> And Agora's Kolmogorov equation gives the tail its simulated careers "
            "produce."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(fc.cols[k][2:]))
        self.clear_scene()
