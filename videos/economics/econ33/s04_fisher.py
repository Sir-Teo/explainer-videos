from __future__ import annotations

from videos.economics.econ33.common import *  # noqa: F403


class Fisher(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Debt deflation, \ and banks as information", r"How did falling prices and failing banks "
             r"deepen the Depression?", "Chapter three. Debt deflation, and banks as information.",
             lit={1933: r"Fisher", 1983: r"Bernanke"}, scale=("household", "nation"), horizon=("a year", "a decade"))
        self.paradox()
        self.depression()
        self.banks()

    def paradox(self):
        F = load("fisher")
        b = F["illus"]
        ax = plane([-0.5, 4.5], [0, 1.6], center=LEFT * 2.6 + DOWN * 0.6, x_length=6.4, y_length=4.0,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 0.5, 1.0, 1.5], xlabel=r"years", ylabel=r"debt over income",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=15)
        bars = VGroup()
        for k, v in enumerate(b):
            p0, p1 = ax.ax.c2p(k - 0.3, 0), ax.ax.c2p(k + 0.3, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=CREDIT, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
        vals = VGroup(*[label(rf"{v:.2f}", font_size=17, color=CREDIT).next_to(bars[k], UP, buff=0.06)
                        for k, v in enumerate(b)])
        qc = quote_card(r"the more the debtors pay, \ the more they owe", r"Irving Fisher, \ \emph{Econometrica} "
                        r"(1933)", width=5.6, font_size=26).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        side = VGroup(
            label(r"each year: \ debtors repay 5\% of what they owe", font_size=19, color=CALM),
            label(r"prices fall 10\%; \ real income falls 5\%", font_size=19, color=CRISIS),
            label(rf"debt over income: \ 1.00 \ $\to$ \ {b[-1]:.2f}", font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(qc, DOWN, buff=0.5)
        tag = published_tag(r"Fisher, \ ``The Debt-Deflation Theory of Great Depressions'', \ \emph{Econometrica} "
                            r"1(4) (1933)", corner=DR, font_size=12)
        with self.voiceover(
            "In 1933, having lost a fortune in the crash, Irving Fisher wrote down the mechanism that had ruined him. "
            "<bookmark mark='a'/> Over-indebted borrowers sell assets and cut spending to repay their debts. Prices "
            "fall. But debts are fixed in money, so falling prices make each dollar owed heavier. "
            "<bookmark mark='b'/> Take a household that repays five percent of its debt every year, <bookmark "
            "mark='c'/> while prices fall ten percent a year and real income falls five. <bookmark mark='d'/> Its "
            f"debt relative to its income rises from one to {b[-1]:.2f} in four years, despite every payment. "
            "Fisher's sentence: the more the debtors pay, the more they owe."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]))
            vo.wait_until("a")
            self.play(FadeIn(qc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], DOWN), FadeIn(vals[k]))
                                    for k in range(1, len(b))], lag_ratio=0.4), FadeIn(side[2]), run_time=2.4)
        self.clear_scene()

    def depression(self):
        F = load("fisher")
        yrs = np.array(F["years"])
        i29 = list(yrs).index(1929)
        idx = {k: 100 * np.array(F[k]) / F[k][i29] for k in ("loans", "gdp", "cpi")}
        ax = plane([1926, 1936], [40, 110], center=LEFT * 3.4 + DOWN * 0.5, x_length=5.6, y_length=4.2,
                   xticks=[1926, 1929, 1932, 1935], yticks=[40, 60, 80, 100], ylabel=r"1929 = 100",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ax2 = plane([1926, 1936], [25, 65], center=RIGHT * 3.0 + DOWN * 0.5, x_length=5.6, y_length=4.2,
                    xticks=[1926, 1929, 1932, 1935], yticks=[30, 40, 50, 60], ylabel=r"bank loans, \ \% of GDP",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ln = {k: path(ax, yrs, idx[k], c, 3.2, smooth=False) for k, c in (("loans", CREDIT), ("gdp", OUTPUT),
                                                                          ("cpi", CRISIS))}
        ratio = path(ax2, yrs, F["ratio"], CREDIT, 3.5, smooth=False)
        key = VGroup(label(rf"bank loans: \ $-{F['loans_fall']:.0f}\%$", font_size=17, color=CREDIT),
                     label(rf"nominal GDP: \ $-{F['gdp_fall']:.0f}\%$", font_size=17, color=OUTPUT),
                     label(rf"prices: \ $-{F['cpi_fall']:.0f}\%$", font_size=17, color=CRISIS)).arrange(
            RIGHT, buff=0.35).next_to(ax, UP, buff=0.15)
        k2 = label(rf"{F['ratio29']:.0f}\% in 1929, \ {F['ratio32']:.0f}\% in 1932", font_size=19,
                   color=CREDIT).next_to(ax2, UP, buff=0.15)
        head = label(r"the United States, \ 1929--1933", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.3)
        tag = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6", corner=DR, font_size=12)
        with self.voiceover(
            "That is what happened in America. <bookmark mark='a'/> Between 1929 and 1933 banks' loans "
            f"outstanding fell {F['loans_fall']:.0f} percent, as borrowers repaid and defaulted and banks called "
            f"in what they could. <bookmark mark='b'/> But nominal GDP fell {F['gdp_fall']:.0f} percent, and prices "
            f"{F['cpi_fall']:.0f}. <bookmark mark='c'/> So the weight of the debt that remained did not fall at all: "
            f"bank loans were {F['ratio29']:.0f} percent of GDP in 1929 and {F['ratio32']:.0f} percent in 1932. "
            "Four years of painful repayment had left the economy as indebted as before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ax2), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln["loans"]), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ln["gdp"]), Create(ln["cpi"]), FadeIn(key[1:]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ratio), FadeIn(k2), run_time=1.8)
        self.clear_scene()

    def banks(self):
        F = load("fisher")
        t = np.array(F["susp_t"])
        v = np.array(F["susp"])
        ax = plane([1921, 1933.3], [0, 550], center=LEFT * 1.8 + DOWN * 0.5, x_length=8.4, y_length=4.2,
                   xticks=[1921, 1924, 1927, 1930, 1933], yticks=[0, 100, 200, 300, 400, 500],
                   ylabel=r"banks suspended, \ each month", xfmt=lambda x: f"{x:.0f}", yfmt=lambda x: f"{x:.0f}",
                   font_size=14)
        w = (ax.ax.c2p(1 / 12, 0) - ax.ax.c2p(0, 0))[0] * 0.8
        bars = VGroup(*[Rectangle(width=w, height=max(ax.ax.c2p(0, y)[1] - ax.ax.c2p(0, 0)[1], 1e-3),
                                  fill_color=CRISIS if tt >= 1930 else GREY_B, fill_opacity=0.85,
                                  stroke_width=0).move_to(ax.ax.c2p(tt, y / 2)) for tt, y in zip(t, v)])
        side = VGroup(
            label(rf"commercial banks suspended, \\ 1930--33: \ {F['susp_30_33']:,.0f}".replace(",", "{,}"),
                  font_size=20, color=CRISIS),
            label(r"Bernanke (1983): \ each failure \\ destroyed what the bank \\ knew about its borrowers",
                  font_size=19, color=BANK),
            label(r"credit dearer and scarcer \\ for those without \\ a record elsewhere", font_size=19,
                  color=GREY_A),
            label(r"a nonmonetary channel, \\ beside the fall in money \\ (Part 25)", font_size=19, color=HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"NBER Macrohistory and Board of Governors, \ via FRED; \ Bernanke, \ \emph{AER} 73(3) "
                       r"(1983)", corner=DR, font_size=12)
        with self.voiceover(
            "There was a second mechanism. American banks had always failed in small numbers. "
            "<bookmark mark='a'/> From 1930 they failed in waves: "
            f"{F['susp_30_33']:,.0f} commercial banks suspended in four years. <bookmark mark='b'/> In 1983 Ben "
            "Bernanke argued that this mattered not only because deposits, and so money, vanished. A bank's real "
            "asset is what it knows about its borrowers: which farmer pays, which shop is sound. When the bank "
            "fails, that knowledge goes with it. <bookmark mark='c'/> Small firms and farmers without a record "
            "elsewhere found credit dearer, or found none. <bookmark mark='d'/> He showed that measures of bank "
            "failures helped explain the fall in output beyond what the fall in money did. Twenty-five years later, "
            "as chairman of the Federal Reserve, he would be in charge of preventing a repeat."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[:108]],
                                                            lag_ratio=0.01), run_time=1.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[108:]], lag_ratio=0.05),
                      FadeIn(side[0]), run_time=2.0)
            for mk, r_ in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
