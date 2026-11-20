from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class Trap(VoiceoverScene):
    def construct(self):
        card(self, 7, r"The liquidity trap", r"What if the interest rate is already zero?", "Chapter seven. The "
             "liquidity trap.", lit={1936: r"Keynes", 1998: r"Krugman"}, scale=("nation",), horizon=("years",))
        self.flat()
        self.japan()
        self.promise()

    def flat(self):
        L = load("islm")
        ax = plane([1000, 1800], [0, 8], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                   xticks=[1000, 1200, 1400, 1600, 1800], yticks=[0, 2, 4, 6, 8], xlabel=r"income $Y$",
                   ylabel=r"interest rate $i$, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=15)
        isl = path(ax, L["is_slump"], L["i"], color=PRICE, width=4, xr=(1000, 1800), smooth=False)
        isf = path(ax, L["is_slump_fiscal"], L["i"], color=GOV, width=4, xr=(1000, 1800), smooth=False)
        lm0 = path(ax, L["Y"], L["lm0"], color=RATE, width=3, yr=(0, 8), smooth=False)
        lm2 = path(ax, L["Y"], L["lm2"], color=COUPON, width=4, yr=(0, 8), smooth=False)
        s, sm, sf = L["slump"], L["slump_money"], L["slump_fiscal"]
        d0 = dot(ax, s["Y"], s["i"], color=PRICE, r=0.09)
        dm = dot(ax, sm["Y"], sm["i"], color=COUPON, r=0.09)
        df = dot(ax, sf["Y"], sf["i"], color=GOV, r=0.09)
        side = VGroup(
            label(rf"investment collapses by {L['slump_size']:.0f}: \\ $Y = {s['Y']:.0f}$, \ "
                  rf"$i = {s['i']:.2f}\%$",
                  font_size=20, color=PRICE),
            label(r"the interest rate cannot fall below zero: \\ LM is flat along the floor", font_size=20,
                  color=RATE),
            label(rf"double the extra money: \\ $Y = {sm['Y']:.0f}$, \ almost nothing", font_size=20, color=COUPON),
            label(rf"spend {L['dG']:.0f} more: \ $Y = {sf['Y']:.0f}$, \\ the full multiplier of "
                  rf"{L['trap_fiscal_mult']:.1f}", font_size=20, color=GOV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now a slump. <bookmark mark='a'/> Firms lose confidence and investment collapses by "
            f"{L['slump_size']:.0f} at every interest rate. The I S curve moves far to the left, and the economy "
            "settles "
            f"at an income of {s['Y']:,.0f}, with the interest rate barely above zero. <bookmark mark='b'/> And "
            "the interest rate cannot go much below zero, because nobody lends at a negative rate when they could "
            "hold cash instead. Along that floor, the L M curve is flat. <bookmark mark='c'/> So the central bank "
            f"prints. It adds {2 * L['dM']:.0f} of money. The L M curve moves right, along the floor, and income "
            f"rises to {sm['Y']:,.0f}: almost nothing. People simply hold the extra money. That is Keynes's "
            "liquidity trap. <bookmark mark='d'/> Fiscal policy is another story. Spend "
            f"{L['dG']:.0f} more, and income rises to {sf['Y']:,.0f}: the full multiplier of "
            f"{L['trap_fiscal_mult']:.1f}, because the interest rate does not rise to crowd anything out."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(lm0), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(isl), GrowFromCenter(d0), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(lm0, color=WHITE))
            vo.wait_until("c")
            self.play(Create(lm2), GrowFromCenter(dm), FadeIn(side[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(Create(isf), GrowFromCenter(df), FadeIn(side[3]), run_time=1.2)
        self.clear_scene()

    def japan(self):
        T = load("trap")
        ax = plane([1985, 2027], [-0.5, 9], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.4, y_length=4.8,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 2, 4, 6, 8], ylabel=r"percent a year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        zero = seg(ax, 1985, 0, 2027, 0, color=GREY_D, width=2)
        jp = path(ax, T["jp_t"], T["jp"], color=PRICE, width=3, smooth=False)
        us = path(ax, T["us_t"], T["us"], color=GOV, width=3, smooth=False)
        side = VGroup(
            label(rf"Japan's overnight rate: \\ about {T['jp_1990']:.0f}\% in 1990", font_size=20, color=PRICE),
            label(rf"below half a percent \\ from {T['jp_below_half']:.0f}, \ and near zero \\ for most of 25 years",
                  font_size=20, color=PRICE),
            label(rf"the federal funds rate: \\ near zero for {T['us_zero_months']} months \\ after 2008 and in "
                  r"2020", font_size=20, color=GOV),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"OECD Main Economic Indicators: \ Japan's call rate; \ Federal Reserve: \ the federal funds "
                       r"rate; \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "For decades the trap looked like a curiosity of the 1930s. Then it came back. <bookmark mark='a'/> "
            f"Japan's overnight interest rate was about {T['jp_1990']:.0f} percent in 1990, as its bubble in land "
            f"and shares burst. <bookmark mark='b'/> By {T['jp_below_half']:.0f} it was below half a percent, and "
            "it stayed near zero for most of the next twenty-five years, while prices drifted down and growth "
            "stalled. <bookmark mark='c'/> America followed: after 2008, and again in 2020, the federal funds rate "
            f"sat near zero, for {T['us_zero_months']} months in all."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), Create(jp), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(us), FadeIn(side[2]), run_time=1.5)
        self.clear_scene()

    def promise(self):
        L = load("islm")
        sm, d, p = L["slump_money"], L["deflation"], L["promise"]
        rows = VGroup(
            label(r"Krugman, \ 1998: \ ``It's baaack''", font_size=27, color=E.ACCENT),
            label(r"what matters for investment is the real rate: \ $r = i - \pi^e$", font_size=24, color=RATE),
            label(rf"at $i = 0$ with prices expected to fall 2\%: \ $r = 2\%$, \ income {d['Y']:.0f}", font_size=24,
                  color=PRICE),
            label(rf"at $i = 0$ with prices expected to rise 2\%: \ $r = -2\%$, \ income {p['Y']:.0f}",
                  font_size=24, color=OUTPUT),
            label(r"so a central bank at zero should promise to keep money easy after the slump, \ "
                  r"credibly to be irresponsible", font_size=22, color=COUPON),
            label(r"later: \ forward guidance, \ bond purchases, \ inflation targets (Part 31)", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Krugman, \ ``It's baaack: \ Japan's slump and the return of the liquidity trap'', \ "
                            r"BPEA 1998(2): \ 137--205", corner=DR, font_size=12)
        with self.voiceover(
            "In 1998, Paul Krugman wrote a paper about Japan called It's baaack, and asked what a central bank "
            "could do at zero. <bookmark mark='a'/> His answer starts from the real interest rate. Investment "
            "depends on the interest rate minus the inflation people expect. <bookmark mark='b'/> At a zero rate "
            "with prices expected to fall two percent a year, the real rate is two percent, and on the Island "
            f"income falls further, to {d['Y']:,.0f}, compared with {sm['Y']:,.0f} with stable prices. "
            "<bookmark mark='c'/> If people instead expect prices to rise two percent, the real rate is minus two, "
            f"and income rises to {p['Y']:,.0f}. <bookmark mark='d'/> So the central bank should promise to keep "
            "money easy even after the slump ends, and make people believe it. In Krugman's phrase, it must "
            "credibly promise to be irresponsible. <bookmark mark='e'/> The tools central banks used after 2008, "
            "forward guidance and large purchases of bonds, grew from that idea. Part thirty-one takes them up."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
