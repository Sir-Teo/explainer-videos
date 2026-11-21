from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Hank(VoiceoverScene):
    def construct(self):
        card(self, 9, r"HANK: \ monetary policy with many households", r"How does a rate cut reach spending?",
             "Chapter nine. HANK: monetary policy with many households.",
             lit={2015: r"Werning", 2018: r"Kaplan, Moll and Violante"}, scale=("household", "nation"),
             horizon=("a year",))
        self.setup_()
        self.paths()
        self.compare()
        self.liquidity()

    def setup_(self):
        steps = flow_chain([(r"households: \ Aiyagari's, \ quarterly", MANY),
                            (r"firms: \ output is whatever is bought", FIRM),
                            (r"the central bank sets the real rate", DIRECT),
                            (r"the government keeps its debt fixed", GREY_B)], box_w=2.9, box_h=1.25, font_size=19,
                           buff=0.45).move_to(UP * 1.0)
        eqs = VGroup(
            MathTex(r"dC = \underbrace{\mathbf{M}_r\, dr}_{\text{direct}} + "
                    r"\underbrace{\mathbf{M}_Z\, dZ}_{\text{indirect}}", font_size=40),
            label(r"$dZ$: \ the change in after-tax incomes that comes from everyone else's spending", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(steps, DOWN, buff=0.8)
        eqs[0][0].set_color(WHITE)
        tag = published_tag(r"Kaplan, \ Moll and Violante, \ AER 108(3) (2018); \ Werning (2015)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "HANK stands for Heterogeneous Agent New Keynesian: the households of this part, in an economy where "
            "spending sets output, as in Parts twenty-seven and thirty. <bookmark mark='a'/> Here, the households "
            "are Aiyagari's, with quarterly periods. <bookmark mark='b'/> Prices are sticky, so firms produce "
            "whatever is bought. <bookmark mark='c'/> The central bank sets the real interest rate. <bookmark "
            "mark='d'/> The government keeps its debt fixed, so when interest payments fall, taxes fall with them. "
            "<bookmark mark='e'/> Any change in spending can be split in two: the direct effect of the interest "
            "rate, holding every household's income fixed, and the indirect effect of the change in incomes that "
            "comes from everyone else's spending."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                an = [FadeIn(steps.boxes[k], shift=UP * 0.1)]
                if k > 0:
                    an.append(Create(steps.arrows[k - 1]))
                self.play(*an)
            vo.wait_until("e")
            self.play(Write(eqs[0]), FadeIn(eqs[1]), run_time=2.0)
        self.clear_scene()

    def paths(self):
        Hk = load("hank")
        row = next(r for r in Hk["rows"] if r["liquid"] == Hk["island"])
        q = np.arange(16)
        tot = 100 * np.array(row["dC"][:16])
        dr_ = 100 * np.array(row["direct"][:16])
        ind = 100 * np.array(row["indirect"][:16])
        ax = plane([0, 15], [-0.2, 1.0], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.2, y_length=4.8,
                   xticks=[0, 4, 8, 12], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"quarters after the announcement",
                   ylabel=r"spending, \ \% of output", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                   font_size=14)
        zero = seg(ax, 0, 0, 15, 0, GREY_B, 1.2, dashed=True)
        c_tot = path(ax, q, tot, WHITE, 3.2, smooth=False)
        c_dir = path(ax, q, dr_, DIRECT, 2.8, smooth=False)
        c_ind = path(ax, q, ind, INDIRECT, 2.8, smooth=False)
        side = VGroup(
            label(r"white: \ the total", font_size=19, color=WHITE),
            label(r"blue: \ direct, \ the rate itself", font_size=19, color=DIRECT),
            label(r"gold: \ indirect, \ through incomes", font_size=19, color=INDIRECT),
            label(rf"first quarter: \ {100 * row['share_impact']:.0f}\% direct \\ first year: \ "
                  rf"{100 * row['share_year']:.0f}\% direct", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(rf"the Island's HANK: \ liquid wealth {Hk['island']:.0f} quarters of output \ (computed)",
                         corner=DL, font_size=12)
        with self.voiceover(
            "Here is the rate cut of the Play it, in the Island's economy, quarter by quarter. <bookmark mark='a'/> "
            f"Spending jumps by {tot[0]:.2f} percent of output at once and fades with the cut. <bookmark mark='b'/> "
            "The direct effect, the response to the rate with incomes held fixed, is the blue line. <bookmark "
            "mark='c'/> The indirect effect through incomes is the gold one. <bookmark mark='d'/> In the first "
            f"quarter the direct effect is {100 * row['share_impact']:.0f} percent of the total; over the first "
            f"year, {100 * row['share_year']:.0f} percent. Within a year, most of the extra spending is people "
            "spending incomes that other people's spending created."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c_tot), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(c_dir), FadeIn(side[1]), run_time=1.4)
            vo.wait_until("c")
            self.play(Create(c_ind), FadeIn(side[2]), run_time=1.4)
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def compare(self):
        Hk = load("hank")
        rows = {r["liquid"]: r for r in Hk["rows"]}
        items = [(r"one household", Hk["ra"]["dC"][0], Hk["ra"]["share_impact"], REP),
                 (r"16 quarters", rows[16.0]["dC"][0], rows[16.0]["share_impact"], RICH),
                 (r"4 quarters", rows[4.0]["dC"][0], rows[4.0]["share_impact"], MANY),
                 (r"1 quarter", rows[1.0]["dC"][0], rows[1.0]["share_impact"], POOR)]
        ax = plane([-0.5, 3.5], [0, 1.0], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.0, y_length=4.6, xticks=[],
                   yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"first-quarter rise in spending, \ \% of output",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        bars = VGroup()
        for i, (nm, tot, sh, col) in enumerate(items):
            tot = 100 * tot
            d = tot * sh
            p0, p1 = ax.ax.c2p(i - 0.3, 0), ax.ax.c2p(i + 0.3, d)
            q0, q1 = ax.ax.c2p(i - 0.3, d), ax.ax.c2p(i + 0.3, tot)
            b1 = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=DIRECT,
                           fill_opacity=0.85).move_to((p0 + p1) / 2)
            b2 = Rectangle(width=q1[0] - q0[0], height=max(q1[1] - q0[1], 0.01), stroke_width=0, fill_color=INDIRECT,
                           fill_opacity=0.85).move_to((q0 + q1) / 2)
            pc = label(rf"{100 * sh:.0f}\%", font_size=16, color=WHITE).move_to(b1)
            nmo = label(nm, font_size=16, color=col).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.2)
            bars.add(VGroup(b1, b2, pc, nmo))
        sub = label(r"liquid wealth:", font_size=15, color=GREY_A).next_to(bars[1][3], DOWN, buff=0.12).align_to(
            bars[1][3], LEFT)
        side = VGroup(
            label(r"blue: \ direct, \ with its share", font_size=18, color=DIRECT),
            label(r"gold: \ indirect", font_size=18, color=INDIRECT),
            label(r"the totals barely change; \\ what changes is why", font_size=20, color=E.ACCENT),
            label(r"the less liquid wealth, \\ the more of it comes \\ through incomes", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Now compare economies. <bookmark mark='a'/> A representative household, with the same rate cut: "
            f"spending rises by {100 * Hk['ra']['dC'][0]:.2f} percent, and {100 * Hk['ra']['share_impact']:.0f} "
            "percent of it is direct. That is the textbook. <bookmark mark='b'/> Households with sixteen quarters of "
            "income in liquid savings, then four, then just one. <bookmark mark='c'/> Look first at the heights: "
            "the totals barely change. Iván Werning showed that, under some conditions, the total response with "
            "many households matches the representative household's exactly; here it nearly does. <bookmark "
            "mark='d'/> What changes is why. The less liquid wealth households hold, the larger the share that "
            f"comes through incomes: with one quarter of liquid wealth, only {100 * rows[1.0]['share_impact']:.0f} "
            "percent is direct. Kaplan, Moll and Violante's economy, with most wealth in illiquid houses and "
            "pensions, puts the direct share lower still."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[:2]))
            vo.wait_until("a")
            self.play(FadeIn(bars[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars[1:]], lag_ratio=0.5), FadeIn(sub),
                      run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def liquidity(self):
        Hk = load("hank")
        rows = Hk["rows"]
        x = np.log2([r["liquid"] for r in rows])
        ax = plane([0, 4], [0, 0.6], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 0.2, 0.4, 0.6],
                   xlabel=r"liquid wealth, \ quarters of output", ylabel=r"share of a windfall spent in the quarter",
                   xfmt=lambda v: f"{2 ** v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        mpc = path(ax, x, [r["mpc"] for r in rows], POOR, 3.0, smooth=False)
        dots = VGroup(*[dot(ax, xx, r["mpc"], POOR, 0.08) for xx, r in zip(x, rows)])
        band_ = Rectangle(width=ax.ax.c2p(4, 0)[0] - ax.ax.c2p(0, 0)[0],
                          height=ax.ax.c2p(0, 0.4)[1] - ax.ax.c2p(0, 0.1)[1], stroke_width=0, fill_color=DATA,
                          fill_opacity=0.15).move_to((ax.ax.c2p(0, 0.1) + ax.ax.c2p(4, 0.4)) / 2)
        blab = label(r"the evidence: \ 10 to 40\% \ (nondurables)", font_size=16, color=DATA).next_to(
            ax.ax.c2p(4, 0.4), DL, buff=0.08)
        side = VGroup(
            label(r"US households hold a few years \\ of income in wealth, \\ but most of it in houses \\ and "
                  r"pensions", font_size=18, color=WHITE),
            label(rf"with all of it liquid \ (16 quarters): \\ they spend {100 * rows[-1]['mpc']:.0f}\% of a "
                  r"windfall", font_size=18, color=RICH),
            label(rf"with only the liquid part \ (1): \\ {100 * rows[0]['mpc']:.0f}\%", font_size=18, color=POOR),
            label(r"one asset cannot match both: \\ two assets, \ one liquid and one \\ not: \ the wealthy "
                  r"hand-to-mouth", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Kaplan and Violante, \ Econometrica (2014); \ the mpc\_windfall dial", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Which economy is right? It turns on how much of a windfall households spend. <bookmark mark='a'/> "
            "American households hold several years of income in wealth, but most of it in houses and retirement "
            "accounts they cannot easily spend. <bookmark mark='b'/> If all of that wealth were liquid, households "
            f"here would spend {100 * rows[-1]['mpc']:.0f} percent of a windfall within the quarter, below the "
            "evidence of Part twenty-two, ten to forty percent. <bookmark mark='c'/> If only the liquid part "
            f"existed, they would spend {100 * rows[0]['mpc']:.0f} percent, above it. <bookmark mark='d'/> A "
            "one-asset model "
            "cannot match both the wealth and the spending. Kaplan and Violante's answer was two assets: many "
            "households are wealthy on paper and live hand to mouth, because their wealth is locked in a house or a "
            "pension."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(band_), FadeIn(blab), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mpc), FadeIn(dots), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Indicate(dots[0], color=WHITE), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()
