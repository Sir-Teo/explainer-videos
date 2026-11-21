from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Innovation(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Learning curves and directed technical change", r"Can policy change what gets invented?",
             "Chapter eleven. Learning curves and directed technical change.",
             lit={1936: r"Wright", 2012: r"Acemoglu, Aghion, Bursztyn and Hemous"}, scale=("firm", "world"),
             horizon=("a decade", "a century"))
        self.prices()
        self.wright()
        self.directed()

    def prices(self):
        So = load("solar")
        py, pr = np.array(So["price_year"]), np.array(So["price"])
        ax = plane([1974, 2026], [-1.1, 2.3], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.4, y_length=4.6,
                   xticks=[1975, 1985, 1995, 2005, 2015, 2025], yticks=[np.log10(x) for x in (0.1, 1, 10, 100)],
                   ylabel=r"solar module price, \ 2025 \$ per watt \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:g}", font_size=14)
        ln = path(ax, py, np.log10(pr), SOLAR, 3.2, smooth=False)
        pins = VGroup(
            VGroup(dot(ax, py[0], np.log10(pr[0]), WHITE, 0.07), label(rf"{py[0]}: \ \${pr[0]:.0f}", font_size=17,
                                                                         color=WHITE).next_to(
                ax.ax.c2p(py[0], np.log10(pr[0])), RIGHT, buff=0.15)),
            VGroup(dot(ax, py[-1], np.log10(pr[-1]), WHITE, 0.07), label(rf"{py[-1]}: \ \${pr[-1]:.2f}",
                                                                           font_size=17, color=WHITE).next_to(
                ax.ax.c2p(py[-1], np.log10(pr[-1])), UL, buff=0.12)),
        )
        side = VGroup(
            label(rf"a fall of \\ {100 * So['fall_total']:.1f}\%", font_size=22, color=SOLAR),
            label(r"each step down \\ the log scale is \\ a tenfold fall", font_size=18, color=GREY_A),
            label(r"the costs of wind \\ and batteries fell \\ steeply too", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"IRENA and other sources, \ via Our World in Data", corner=DL, font_size=12)
        with self.voiceover(
            "The DICE model assumes the cost of clean energy falls at a slow, steady pace whatever anyone does. "
            "Here is what happened to one clean technology. <bookmark mark='a'/> The price of solar photovoltaic "
            f"modules, after inflation: about {pr[0]:.0f} dollars a watt in {py[0]}, <bookmark mark='b'/> "
            f"{pr[-1]:.2f} in {py[-1]}. <bookmark mark='c'/> A fall of {100 * So['fall_total']:.1f} percent, more "
            "than three tenfold steps on this scale. <bookmark mark='d'/> Few forecasters expected it, and the "
            "question for climate policy is whether it was luck or something policy can cause."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            self.play(Create(ln), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(pins[0]))
            vo.wait_until("b")
            self.play(FadeIn(pins[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def wright(self):
        So = load("solar")
        cy, cap = np.array(So["cap_year"]), np.array(So["capacity"])
        fy = np.array(So["fit_year"])
        pr = np.array(So["price"])[np.isin(So["price_year"], fy)]
        capf = cap[np.isin(cy, fy)]
        ax = plane([0, 3.6], [-1.1, 1.0], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.0, y_length=4.6,
                   xticks=[np.log10(x) for x in (1, 10, 100, 1000)], yticks=[np.log10(x) for x in (0.1, 0.3, 1, 3, 10)],
                   xlabel=r"solar capacity installed worldwide, \ gigawatts \ (log scale)",
                   ylabel=r"module price, \ \$ per watt \ (log)", xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"),
                   yfmt=lambda v: f"{10 ** v:g}", font_size=14)
        pts = VGroup(*[dot(ax, np.log10(c), np.log10(p), SOLAR, 0.06) for c, p in zip(capf, pr)])
        fit = path(ax, np.log10(capf), np.log10(So["fit"]), WHITE, 2.6, smooth=False)
        eq = MathTex(r"\log p = a + b \log Q, \qquad 1 - 2^{\,b} = \text{the learning rate}", font_size=28,
                     color=THEORY).to_edge(UP, buff=0.45)
        side = VGroup(
            label(rf"{fy[0]}--{fy[-1]}: \ capacity \\ doubled {So['doublings']:.0f} times", font_size=18,
                  color=WHITE),
            label(rf"each doubling: \\ price down \\ {100 * So['learning_rate']:.0f}\%", font_size=22, color=SOLAR),
            label(r"learning by doing: \\ the more is built, \\ the cheaper it gets, \\ and the first buyers \\ pay "
                  r"for everyone's \\ learning", font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"IRENA, \ via Our World in Data; \ fitted here", corner=DL, font_size=12)
        with self.voiceover(
            "In 1936 the aeronautical engineer Theodore Wright noticed that each doubling of the number of aircraft "
            "built cut the labour needed for one by a steady fraction. <bookmark mark='a'/> Plot the price of solar "
            f"modules against the capacity installed worldwide, from {fy[0]} to {fy[-1]}, both on log scales. "
            f"<bookmark mark='b'/> Capacity doubled about {So['doublings']:.0f} times, and the points fall on a "
            f"line: <bookmark mark='c'/> each doubling cut the price by about {100 * So['learning_rate']:.0f} "
            "percent. <bookmark mark='d'/> If cost falls because things are built, then building more now makes "
            "the technology cheaper for everyone later, a spillover the first buyers do not capture. That is an "
            "argument for subsidizing early deployment, on top of pricing carbon, that many economists accept, "
            "though how much of the fall came from learning, and how much from research and scale, is still argued."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(eq), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("a")
            self.play(Indicate(pts, color=WHITE, scale_factor=1.2))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def directed(self):
        Dt = load("dtc")
        cases = Dt["cases"]
        t = np.array(Dt["t"])
        ax = plane([0, 150], [0, 1.0], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.4, y_length=4.6,
                   xticks=[0, 40, 80, 120], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"years",
                   ylabel=r"clean inputs' share of production", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        cols = {"laissez-faire": DIRTY, "a tax alone": LOSS, "a tax and a research subsidy": CLEAN,
                "a heavy tax alone": POLICY}
        lines = VGroup(*[path(ax, t, cases[k]["share"], cols[k], 3.0, smooth=False) for k in cols])
        policy = shade(ax, [(0, 40)], 0, 1.0, color=RECESS, opacity=0.5)
        side = VGroup(
            label(r"grey: \ laissez-faire: \\ research follows \\ the bigger, dirty \\ market", font_size=17,
                  color=DIRTY),
            label(r"red: \ a 20\% tax \\ for 40 years: \ not \\ enough to turn it", font_size=17, color=LOSS),
            label(r"green: \ the same tax \\ with a research \\ subsidy: \ research \\ switches, \ and stays",
                  font_size=17, color=CLEAN),
            label(r"purple: \ a 40\% tax \\ alone does it too, \\ at a higher cost", font_size=17, color=POLICY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Daron Acemoglu, Philippe Aghion, Leonardo Bursztyn and David Hemous asked a deeper question in 2012: "
            "what decides whether inventors work on clean or dirty technology? Here is a toy of their model on the "
            "Island, with clean and dirty inputs that substitute well. <bookmark mark='a'/> Left alone, inventors "
            "go where the market is biggest, and the dirty technology is ahead, so it keeps getting better and "
            "clean falls behind: path dependence. <bookmark mark='b'/> A modest carbon tax for forty years, the "
            "grey band, is not enough to turn it. <bookmark mark='c'/> The same tax with a subsidy for clean "
            "research makes clean research more profitable; once clean technology has caught up, inventors stay "
            "with it after the policy ends. <bookmark mark='d'/> A tax twice as heavy does it alone, at a higher "
            "cost to consumers. Their conclusion: with good substitutes, temporary policy can change the direction "
            "of technology for good, and acting early is cheaper than acting late."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(policy), run_time=1.0)
            self.play(Create(lines[0]), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(lines[0], color=WHITE))
            for mk, ln, s_ in zip("bcd", lines[1:], side[1:]):
                vo.wait_until(mk)
                self.play(Create(ln), FadeIn(s_), run_time=2.0)
        self.clear_scene()
