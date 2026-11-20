from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


class Fisher(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Money, interest and prices", r"Does more money change anything real?",
             "Chapter eleven. Money, interest and prices.", lit={1896: r"Fisher", 1967: r"Sidrauski"},
             scale=("nation",), horizon=("years", "decades"))
        self.equation()
        self.data_()
        self.neutral()

    def equation(self):
        rows = VGroup(
            MathTex(r"i \;\approx\; r \;+\; \pi^e", font_size=60, color=RATE),
            label(r"the nominal rate is the real rate plus the inflation lenders expect", font_size=24, color=GREY_A),
            label(r"Irving Fisher, \ \emph{Appreciation and Interest}, \ 1896", font_size=21, color=GREY_B),
            label(r"so in the long run, \ faster money growth means higher interest rates, \ not lower", font_size=24,
                  color=E.ACCENT),
            label(r"the opposite of the short run, \ when a central bank lowers rates by supplying reserves \ "
                  r"(Part 31)", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Fisher, \emph{Appreciation and Interest} (1896); \ \emph{The Theory of Interest} (1930)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Money also shows up in interest rates. <bookmark mark='a'/> A lender who expects prices to rise five "
            "percent a year will want five points more interest, just to stay even. So the nominal interest rate is "
            "roughly the real rate plus expected inflation. <bookmark mark='b'/> Irving Fisher wrote this down in "
            "1896. <bookmark mark='c'/> It means that in the long run, faster money growth brings higher interest "
            "rates, not lower ones. <bookmark mark='d'/> That is the opposite of the short run, when a central bank "
            "pushes rates down by supplying reserves, as Part thirty-one will show. The two are reconciled by time: "
            "the first effect is immediate, the second comes as expectations catch up."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def data_(self):
        f = load("fisher")
        ax = plane([1960, 2027], [-4, 16], center=LEFT * 2.6 + DOWN * 0.3, x_length=6.6, y_length=4.8,
                   xticks=[1960, 1980, 2000, 2020], yticks=[-4, 0, 4, 8, 12, 16], ylabel=r"\% a year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        zero = seg(ax, 1960, 0, 2027, 0, color=GREY_D, width=2)
        rate = path(ax, f["t"], f["rate"], color=RATE, width=3, smooth=False)
        infl = path(ax, f["t"], f["inflation"], color=PRICE, width=3, smooth=False, yr=(-4, 16))
        rows = VGroup(VGroup(label(r"decade", font_size=18, color=GREY_B), label(r"bill rate", font_size=18,
                                                                                 color=RATE),
                             label(r"inflation", font_size=18, color=PRICE), label(r"real", font_size=18,
                                                                                    color=WHITE)))
        for d in f["decades"]:
            rows.add(VGroup(label(d["decade"], font_size=18, color=GREY_A), label(f"{d['rate']:.1f}", font_size=18,
                                                                                    color=RATE),
                            label(f"{d['inflation']:.1f}", font_size=18, color=PRICE),
                            label(f"{d['real']:+.1f}", font_size=18, color=WHITE)))
        for k, row in enumerate(rows):
            for c, cell in enumerate(row):
                cell.move_to([2.6 + 1.15 * c, 2.3 - 0.5 * k, 0])
        tag = data_tag(r"three-month Treasury bill rate; \ CPI inflation over twelve months; \ via FRED", corner=DR,
                       font_size=12)
        r70 = next(d for d in f["decades"] if d["decade"] == "1970s")
        r80 = next(d for d in f["decades"] if d["decade"] == "1980s")
        with self.voiceover(
            "In American data the two travel together. <bookmark mark='a'/> The three-month Treasury bill rate, and "
            "inflation over the previous twelve months, since 1960. <bookmark mark='b'/> Decade by decade, as "
            "inflation rose into the 1970s, so did interest rates, though in the 1970s not by enough: the real "
            f"rate averaged {r70['real']:+.1f} points, as lenders kept being surprised. <bookmark mark='c'/> In the "
            f"1980s, with inflation coming down, it averaged {r80['real']:+.1f}. The real rate moves, but much less "
            "than the nominal rate and inflation do. That is Fisher's point."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), Create(rate), Create(infl), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(Indicate(rows[3], color=WHITE))
        self.clear_scene()

    def neutral(self):
        rows = VGroup(
            label(r"neutrality: \ a one-time doubling of all money doubles all prices, \ and changes nothing real",
                  font_size=23, color=MONEY),
            label(r"superneutrality: \ a faster \emph{rate} of money growth changes nothing real either", font_size=23,
                  color=MONEY),
            label(r"Sidrauski, \ 1967: \ in the long run, \ with money in the utility function, \ capital is "
                  r"superneutral", font_size=21, color=GREY_A),
            label(r"but inflation is a tax on holding money, \ and people spend effort avoiding it: \ not quite "
                  r"neutral", font_size=22, color=PRICE),
            label(r"and in the short run, \ with sticky prices, \ money moves output \ (Parts 27 and 30)", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Sidrauski, AER 57(2) (1967): \ 534--544", corner=DR, font_size=12)
        with self.voiceover(
            "Two words for what money does not do. <bookmark mark='a'/> Neutrality: a once-and-for-all doubling of "
            "every amount of money, every price and every debt changes nothing real. It is a change of units, like "
            "Venezuela's lopped zeros. <bookmark mark='b'/> Superneutrality: a permanently faster rate of money "
            "growth changes nothing real either. <bookmark mark='c'/> Miguel Sidrauski showed in 1967 that in a "
            "growth model with money, the long-run capital stock does not depend on money growth. "
            "<bookmark mark='d'/> But inflation is a tax on holding money, and people spend time and effort avoiding "
            "it, so money growth is not quite neutral, as the next chapter measures. <bookmark mark='e'/> And in the "
            "short run, when prices are sticky, money moves output and jobs. That is the subject of Parts "
            "twenty-seven and thirty."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
