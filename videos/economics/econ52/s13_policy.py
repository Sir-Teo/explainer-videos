from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Policy(VoiceoverScene):
    def construct(self):
        card(self, 11, r"What changes for policy", r"Which answers move when the households differ?",
             "Chapter eleven. What changes for policy.",
             lit={2006: r"Doepke and Schneider", 2016: r"McKay, Nakamura, Steinsson"}, scale=("household", "nation"),
             horizon=("a decade",))
        self.multipliers()
        self.guidance()
        self.inflation()

    def multipliers(self):
        Hk = load("hank")
        rows = Hk["rows"]
        x = np.log2([r["liquid"] for r in rows])
        ax = plane([0, 4], [0.8, 2.0], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 1, 2, 3, 4], yticks=[0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
                   xlabel=r"liquid wealth, \ quarters of output", ylabel=r"spending multiplier",
                   xfmt=lambda v: f"{2 ** v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        bal = path(ax, x, [r["mult_balanced"] for r in rows], WHITE, 3.0, smooth=False)
        dfc = path(ax, x, [r["mult_deficit"] for r in rows], INDIRECT, 3.0, smooth=False)
        dd = VGroup(*[dot(ax, xx, r["mult_deficit"], INDIRECT, 0.08) for xx, r in zip(x, rows)])
        side = VGroup(
            label(r"the government buys 1\% of output \\ for a while; \ the real rate is fixed", font_size=18,
                  color=WHITE),
            label(r"white: \ paid by taxes at once: \\ exactly 1, \ whatever the households", font_size=18,
                  color=WHITE),
            label(r"gold: \ paid by borrowing, \\ taxes later", font_size=18, color=INDIRECT),
            label(r"one representative household: \\ 1 either way \ (Ricardo)", font_size=18, color=REP),
            label(rf"with 1 quarter of liquid wealth: \\ {rows[0]['mult_deficit']:.2f}", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Auclert, \ Rognlie and Straub, \ \emph{The Intertemporal Keynesian Cross}", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Fiscal policy first. The government buys an extra one percent of output for a while, with the real "
            "interest rate held fixed. <bookmark mark='a'/> If it pays with taxes at once, output rises by exactly "
            "what the government buys: a multiplier of one, whatever the households are like. Higher taxes and "
            "higher incomes cancel for every household. <bookmark mark='b'/> If it borrows and taxes later, the "
            "answer depends on who the households are. <bookmark mark='c'/> A representative household sees the "
            "future taxes coming and saves for them: the multiplier is still one, as David Ricardo argued. "
            "<bookmark mark='d'/> Households with little liquid wealth spend the extra income now and worry about "
            f"the taxes later. With one quarter of liquid wealth, the multiplier is {rows[0]['mult_deficit']:.2f}. "
            "Adrien Auclert, Matthew Rognlie and Ludwig Straub call this the intertemporal Keynesian cross."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(bal), FadeIn(side[1]), run_time=1.4)
            vo.wait_until("b")
            self.play(Create(dfc), FadeIn(dd), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Indicate(dd[0], color=WHITE), FadeIn(side[4]))
        self.clear_scene()

    def guidance(self):
        Hk = load("hank")
        rows = {r["liquid"]: r for r in Hk["rows"]}
        h = np.arange(1, 21)
        ra = 100 * Hk["fg_ra"]
        ax = plane([1, 20], [0.21, 0.30], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[1, 4, 8, 12, 16, 20], yticks=[0.21, 0.24, 0.27, 0.30],
                   xlabel=r"how many quarters ahead the cut comes", ylabel=r"spending today, \ \% of output",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        rline = seg(ax, 1, ra, 20, ra, REP, 2.6)
        c1 = path(ax, h, 100 * np.array(rows[1.0]["fg"]), POOR, 2.8, smooth=False)
        c16 = path(ax, h, 100 * np.array(rows[16.0]["fg"]), RICH, 2.8, smooth=False)
        f1, l1 = 100 * rows[1.0]["fg"][0], 100 * rows[1.0]["fg"][-1]
        f16, l16 = 100 * rows[16.0]["fg"][0], 100 * rows[16.0]["fg"][-1]
        side = VGroup(
            label(r"a quarter-point cut, \ for one quarter, \\ promised for later", font_size=18, color=WHITE),
            label(r"white: \ one household: \\ the same, \ however far off", font_size=18, color=REP),
            label(r"orange: \ 1 quarter of liquid wealth", font_size=18, color=POOR),
            label(r"blue: \ 16 quarters", font_size=18, color=RICH),
            label(rf"many households: \ five years out \\ does {100 * (1 - l1 / f1):.0f}\% less than "
                  r"next quarter", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"McKay, \ Nakamura and Steinsson, \ AER 106(10) (2016)", corner=DR, font_size=12)
        with self.voiceover(
            "Next, promises. The central bank announces a quarter-point cut, for one quarter only, some quarters "
            "from now. How much does spending rise today? <bookmark mark='a'/> For a representative household the "
            "answer does not depend on how far off the cut is. Its spending today depends on the sum of all future "
            "interest rates, and a cut five years away lowers that sum as much as a cut next quarter. "
            "Promises about the distant future are as powerful as action now: the forward guidance puzzle. "
            "<bookmark mark='b'/> With many households, some of whom may hit their borrowing limits before the "
            "cut arrives, distant promises count for less. With one quarter of liquid wealth, a cut five years "
            f"away does {100 * (1 - l1 / f1):.0f} percent less today than one next quarter; with sixteen quarters, "
            f"{100 * (1 - l16 / f16):.0f} percent less. <bookmark mark='c'/> Here the discount is mild. Alisdair "
            "McKay, Emi Nakamura and Jón Steinsson showed it can be much stronger when the households most likely "
            "to hit their limits face more risk; the puzzle is softened, not solved."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(rline), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(c1), FadeIn(side[2]), Create(c16), FadeIn(side[3]), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def inflation(self):
        N = load("nominal")
        rows = N["rows"]
        cards = VGroup()
        for r in rows:
            pos = r["position"]
            ch = r["change"]
            col = GAIN if ch > 0 else LOSS
            c = VGroup(
                label(r["who"], font_size=22, color=WHITE),
                label((r"owes " if pos < 0 else r"owns ") + dollars(abs(pos), 0) + (r" in a mortgage" if pos < 0 else
                                                                                   r" in bonds"),
                      font_size=19, color=GREY_A),
                label((r"gains " if ch > 0 else r"loses ") + dollars(abs(ch), 0), font_size=24, color=col),
            ).arrange(DOWN, buff=0.18)
            box = RoundedRectangle(width=3.8, height=2.0, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.08)
            cards.add(VGroup(box, c.move_to(box)))
        cards.arrange(RIGHT, buff=0.4).move_to(UP * 0.4)
        head = label(rf"prices rise {100 * N['surprise']:.0f}\% more than anyone expected", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        ds = wrapped_label(r"Doepke and Schneider (2006): \ the main losers from inflation are rich, \ old "
                           r"households, \ the big bondholders; \ the winners are young, \ middle-class households "
                           r"with fixed-rate mortgages, \ and the government", 12.0, 21, WHITE).to_edge(
            DOWN, buff=0.7)
        tag = island_tag(r"three Island households \ (illustrative)", corner=DL, font_size=12)
        with self.voiceover(
            "Finally, who gains from inflation? A representative household owes its debts to itself, so a surprise "
            "rise in prices moves nothing. Real households hold their debts and their bonds in dollars. <bookmark "
            f"mark='a'/> Suppose prices rise {100 * N['surprise']:.0f} percent more than anyone expected. <bookmark "
            f"mark='b'/> A young family with a fixed-rate mortgage of {abs(rows[0]['position']):,.0f} dollars gains "
            f"{rows[0]['change']:,.0f} dollars in real terms: the debt is now smaller. A middle-aged couple with a "
            f"smaller mortgage gains less; a retired teacher with {rows[2]['position']:,.0f} dollars in bonds loses "
            f"{abs(rows[2]['change']):,.0f}. <bookmark mark='c'/> Matthias Doepke and Martin Schneider measured "
            "these positions for the whole United States. The main losers from a moderate inflation are rich, old "
            "households, the big bondholders; the winners are young, middle-class households with fixed-rate "
            "mortgages, and the government. A representative household cannot even ask the question."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(head))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(ds, shift=UP * 0.1))
        self.clear_scene()
