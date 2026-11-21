from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Incomplete(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Incomplete markets", r"What does risk that cannot be insured do to saving?",
             "Chapter two. Incomplete markets.", lit={1977: r"Bewley", 1993: r"Huggett"},
             scale=("household", "market"), horizon=("a lifetime",))
        self.setup_()
        self.buffer()
        self.market()
        self.distribution()

    def setup_(self):
        steps = flow_chain([(r"income jumps between low and high", POOR),
                            (r"no insurance can be bought", ERR),
                            (r"one asset: \ a bond", MANY),
                            (r"a limit on borrowing", ERR)], box_w=2.8, box_h=1.2, font_size=20, buff=0.45)
        steps.move_to(UP * 0.8)
        cols = VGroup(
            label(r"complete markets: \ insure every risk, \ consumption flat, \ one household is exact",
                  font_size=21, color=GREY_A),
            label(r"incomplete markets: \ self-insure by saving, \ each household's history matters",
                  font_size=21, color=MANY),
        ).arrange(DOWN, buff=0.35).next_to(steps, DOWN, buff=0.9)
        tag = published_tag(r"Bewley (1977, 1986); \ Huggett, \ JEDC (1993)", corner=DR, font_size=12)
        with self.voiceover(
            "The models of this part start from one change to the textbook. <bookmark mark='a'/> Each household's "
            "income jumps between bad years and good ones, <bookmark mark='b'/> and there is no insurance to buy "
            "against it: no contract pays out when your own income falls. <bookmark mark='c'/> The only way to "
            "smooth is to save in a single asset, a bond, <bookmark mark='d'/> and there is a limit on how much "
            "can be borrowed. <bookmark mark='e'/> With complete insurance, consumption would be flat and one "
            "household would stand for all. Without it, each household self-insures by saving, and its own history "
            "of luck decides how much it holds. Truman Bewley studied such households in the late 1970s; Mark "
            "Huggett put them into a market in 1993."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, b in zip("abcd", steps.boxes):
                vo.wait_until(mk)
                k = list(steps.boxes).index(b)
                anims = [FadeIn(b, shift=UP * 0.1)]
                if k > 0:
                    anims.append(Create(steps.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("e")
            self.play(FadeIn(cols[0], shift=UP * 0.1))
            self.play(FadeIn(cols[1], shift=UP * 0.1))
        self.clear_scene()

    def buffer(self):
        eq = MathTex(r"u'(c_t) \;\ge\; \beta (1 + r)\, \mathbb{E}_t\, u'(c_{t+1}),", r"\quad",
                     r"\text{with equality unless } a_{t+1} = \underline{a}", font_size=38, color=THEORY).move_to(
            UP * 2.2)
        rows = VGroup(
            label(r"if $\beta(1 + r) = 1$, \ as for a representative household:", font_size=23, color=WHITE),
            label(r"$\mathbb{E}\, u'(c_{t+1}) \le u'(c_t)$: \ marginal utility is a supermartingale", font_size=23,
                  color=WHITE),
            label(r"risk keeps pushing consumption around; \ the only way to stop is to be rich enough",
                  font_size=23, color=WHITE),
            label(r"so wealth drifts up without bound: \ households want to save at that rate", font_size=23,
                  color=ERR),
            label(r"in equilibrium the interest rate must fall below the rate of time preference", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(eq, DOWN, buff=0.6)
        tag = published_tag(r"Chamberlain and Wilson (2000); \ Huggett (1993); \ Aiyagari (1994)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Why does this matter for interest rates? Start from the household's Euler equation. Today's marginal "
            "utility is at least the discounted, interest-weighted marginal utility expected tomorrow, with "
            "equality unless the household is pinned at its borrowing limit. <bookmark mark='a'/> Give it the "
            "interest rate a representative household would face, where patience exactly offsets interest. "
            "<bookmark mark='b'/> Then expected marginal utility can only fall over time. <bookmark mark='c'/> "
            "But income risk keeps knocking consumption around, so marginal utility can only stop falling once the "
            "household is so rich that the risk no longer matters. <bookmark mark='d'/> Wealth drifts up without "
            "bound: at that interest rate, everyone wants to save, and nobody wants to borrow. <bookmark "
            "mark='e'/> So the market can only clear at a lower rate. Uninsurable risk pushes the interest rate "
            "below the rate of time preference."
        ) as vo:
            self.play(Write(eq), FadeIn(tag), run_time=2.0)
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def market(self):
        Hg = load("huggett")
        rs = np.array(Hg["rs"]) * 100
        B = np.array(Hg["B"])
        ax = plane([-0.1, 0.5], [0, 5.5], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=5.0,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 1, 2, 3, 4, 5],
                   xlabel=r"bonds households want to hold, \ in total", ylabel=r"interest rate, \ \%",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        curve = path(ax, B, rs, MANY, 3.2, xr=(-0.1, 0.5), smooth=True)
        zero = vline(ax, 0.0, 0, 5.5, WHITE, 2.0)
        rho = DashedLine(ax.ax.c2p(-0.1, 100 * Hg["rho"]), ax.ax.c2p(0.5, 100 * Hg["rho"]), color=ERR,
                         stroke_width=2.2)
        rlab = label(r"rate of time preference, \ 5\%", font_size=17, color=ERR).next_to(
            ax.ax.c2p(0.5, 100 * Hg["rho"]), UL, buff=0.08)
        eq_dot = dot(ax, 0.0, 100 * Hg["r"], E.ACCENT, 0.12)
        side = VGroup(
            label(r"bonds are lent among households: \\ in total they must sum to zero", font_size=19,
                  color=WHITE),
            label(rf"the market clears at \\ {100 * Hg['r']:.2f}\%, \ not 5\%", font_size=21, color=E.ACCENT),
            label(r"as the rate nears 5\%, \\ the demand for bonds explodes", font_size=19, color=MANY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"Huggett's economy in continuous time \ (computed)", corner=DR, font_size=12)
        with self.voiceover(
            "Huggett's economy makes this concrete. Households lend to and borrow from one another, so their bond "
            "holdings must add up to zero. <bookmark mark='a'/> The curve shows the total they want to hold at each "
            "interest rate. At low rates, borrowers outweigh savers. <bookmark mark='b'/> As the rate rises toward "
            "the rate of time preference, five percent, the precautionary demand for bonds explodes, exactly as "
            "the Euler equation said. <bookmark mark='c'/> The market clears where the curve crosses zero, at "
            f"{say_pct(Hg['r'], 2)}. Huggett used this to ask whether uninsured risk could explain why safe "
            "interest rates are so low; with a tight enough limit on borrowing, it pushes them a long way down."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(curve), run_time=2.2)
            vo.wait_until("b")
            self.play(Create(rho), FadeIn(rlab), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(eq_dot, scale=1.5), FadeIn(side[1]))
        self.clear_scene()

    def distribution(self):
        Hg = load("huggett")
        a = np.array(Hg["a"])
        g = np.array(Hg["g"])
        top = float(np.percentile(g[1:-1], 99.5)) * 1.1
        ax = plane([a[0], 2.0], [0, top], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.8,
                   xticks=[-0.15, 0.5, 1.0, 1.5, 2.0], yticks=[],
                   xlabel=r"bonds held \ (negative: \ borrowing)", ylabel=r"share of households",
                   xfmt=lambda v: f"{v:.2f}".replace("-", "{-}") if abs(v) < 0.2 and v else f"{v:.1f}", font_size=14)
        lo = path(ax, a, np.minimum(g[:, 0], top), POOR, 3.0, xr=(a[0], 2.0))
        hi = path(ax, a, np.minimum(g[:, 1], top), RICH, 3.0, xr=(a[0], 2.0))
        spike = Line(ax.ax.c2p(a[0], 0), ax.ax.c2p(a[0], top), color=ERR, stroke_width=7)
        side = VGroup(
            label(r"orange: \ low income", font_size=19, color=POOR),
            label(r"blue: \ high income", font_size=19, color=RICH),
            label(r"red: \ a crowd at the limit, \\ low income, \ nothing left \\ to borrow", font_size=19,
                  color=ERR),
            label(r"the distribution is \\ part of the answer", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "In equilibrium, the households spread out. <bookmark mark='a'/> Those with low incomes run down their "
            "bonds and borrow; <bookmark mark='b'/> those with high incomes build them up. <bookmark mark='c'/> "
            "And a crowd of low-income households sits exactly at the borrowing limit, with nothing left to "
            "borrow: they would spend any extra dollar. <bookmark mark='d'/> The interest rate, the amount saved, "
            "and the response to any shock all depend on this whole picture, not on an average household."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(lo), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(hi), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(spike), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()
