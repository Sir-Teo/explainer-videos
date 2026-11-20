from __future__ import annotations

from videos.economics.econ27.common import *  # noqa: F403


class ISLM(VoiceoverScene):
    def construct(self):
        card(self, 6, r"IS--LM", r"How do the goods market and the money market settle together?",
             "Chapter six. I S, L M.", lit={1937: r"Hicks", 1936: r"Keynes"}, scale=("nation",),
             horizon=("a year",))
        self.derive()
        self.diagram()
        self.policy()

    def derive(self):
        rows = VGroup(
            label(r"Hicks, \ 1937: \ ``Mr.\ Keynes and the `Classics'\,''", font_size=26, color=E.ACCENT),
            label(r"IS: \ the goods market, \ where spending equals output", font_size=23, color=SPEND),
            MathTex(r"Y = \frac{a - bT + I_0 + G - d\,r}{1-b}", font_size=38, color=SPEND),
            label(r"a higher interest rate cuts investment, \ so less output: \ IS slopes down", font_size=22,
                  color=GREY_A),
            label(r"LM: \ the money market, \ where the money people want equals the money there is", font_size=23,
                  color=RATE),
            MathTex(r"\frac{M}{P} = k\,Y - h\,i", font_size=38, color=RATE),
            label(r"more income means more money wanted, \ so a higher rate clears it: \ LM slopes up",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.22).move_to(UP * 0.1)
        tag = published_tag(r"Hicks, \ Econometrica 5(2) (1937): \ 147--159", corner=DR, font_size=12)
        with self.voiceover(
            "Keynes's book was long and hard. In 1937 John Hicks turned it into two curves, in a paper called "
            "Mister Keynes and the Classics. <bookmark mark='a'/> The first is the I S curve: every pair of income "
            "and interest rate at which spending equals output. <bookmark mark='b'/> It is the Keynesian cross, with "
            "one change: investment now falls when the interest rate rises. <bookmark mark='c'/> A higher rate means "
            "less investment, so less output: the curve slopes down. <bookmark mark='d'/> The second is the L M "
            "curve: every pair at which the money people want to hold equals the money there is. "
            "<bookmark mark='e'/> People want more money when their income is higher, for transactions, and less "
            "when the interest rate is higher, because holding money then costs more. <bookmark mark='f'/> So more "
            "income needs a higher interest rate to keep money demand equal to the fixed supply: the curve slopes "
            "up."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
            vo.wait_until("f")
            self.play(FadeIn(rows[6]))
        self.clear_scene()

    def _axes(self):
        return plane([1000, 1800], [0, 8], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.0, y_length=4.8,
                     xticks=[1000, 1200, 1400, 1600, 1800], yticks=[0, 2, 4, 6, 8], xlabel=r"income $Y$",
                     ylabel=r"interest rate $i$, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                     font_size=15)

    def diagram(self):
        L = load("islm")
        ax = self._axes()
        is0 = path(ax, L["is0"], L["i"], color=SPEND, width=4, xr=(1000, 1800), smooth=False)
        lm0 = path(ax, L["Y"], L["lm0"], color=RATE, width=4, yr=(0, 8), smooth=False)
        b = L["base"]
        d0 = dot(ax, b["Y"], b["i"], color=OUTPUT, r=0.09)
        side = VGroup(
            label(r"IS", font_size=26, color=SPEND),
            label(r"LM", font_size=26, color=RATE),
            label(rf"they cross at \\ $Y = {b['Y']:.0f}$, \ $i = {b['i']:.1f}\%$", font_size=22, color=OUTPUT),
            label(r"the one point where goods \\ and money both clear", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Draw them together, on the Island's numbers. <bookmark mark='a'/> The I S curve, sloping down. "
            "<bookmark mark='b'/> The L M curve, sloping up. <bookmark mark='c'/> They cross at an income of "
            f"{b['Y']:,.0f} and an interest rate of {b['i']:.1f} percent. <bookmark mark='d'/> That is the one "
            "combination at which the goods market and the money market both clear. Nothing in it says that "
            "everyone who wants a job has one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(is0), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lm0), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(d0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def policy(self):
        L = load("islm")
        ax = self._axes()
        is0 = path(ax, L["is0"], L["i"], color=SPEND, width=3, xr=(1000, 1800), smooth=False)
        is1 = path(ax, L["is1"], L["i"], color=GOV, width=4, xr=(1000, 1800), smooth=False)
        lm0 = path(ax, L["Y"], L["lm0"], color=RATE, width=3, yr=(0, 8), smooth=False)
        lm1 = path(ax, L["Y"], L["lm1"], color=COUPON, width=4, yr=(0, 8), smooth=False)
        b, f, m = L["base"], L["fiscal"], L["money"]
        d0 = dot(ax, b["Y"], b["i"], color=OUTPUT, r=0.08)
        df = dot(ax, f["Y"], f["i"], color=GOV, r=0.09)
        dm = dot(ax, m["Y"], m["i"], color=COUPON, r=0.09)
        side = VGroup(
            label(rf"fiscal: \ $G$ up {L['dG']:.0f}: \\ $Y = {f['Y']:.0f}$, \ $i = {f['i']:.1f}\%$", font_size=21,
                  color=GOV),
            label(rf"a multiplier of {L['fiscal_mult']:.2f}, \\ not {L['cross_mult']:.1f}: \ the higher rate "
                  r"\\ crowds out investment", font_size=20, color=GREY_A),
            label(rf"monetary: \ $M$ up {L['dM']:.0f}: \\ $Y = {m['Y']:.0f}$, \ $i = {m['i']:.1f}\%$",
                  font_size=21, color=COUPON),
            label(r"the same income, \\ a lower interest rate", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now use it. <bookmark mark='a'/> Fiscal policy first: the government buys "
            f"{L['dG']:.0f} more. The I S curve shifts right, and income rises to {f['Y']:,.0f}. "
            f"<bookmark mark='b'/> But the multiplier is now only {L['fiscal_mult']:.2f}, not "
            f"{L['cross_mult']:.1f}. Higher income raises the demand for money, the interest rate rises to "
            f"{f['i']:.1f} percent, and the higher rate crowds out some private investment. "
            f"<bookmark mark='c'/> Monetary policy instead: the central bank adds {L['dM']:.0f} of money. The L M "
            f"curve shifts right, the interest rate falls to {m['i']:.1f} percent, and investment rises. "
            f"<bookmark mark='d'/> Here it gives the same income, {m['Y']:,.0f}, by a different route. For thirty "
            "years this diagram was how economists, central banks and treasuries thought about a slump."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(is0), Create(lm0), GrowFromCenter(d0), run_time=1.2)
            vo.wait_until("a")
            self.play(Create(is1), GrowFromCenter(df), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lm1), GrowFromCenter(dm), FadeIn(side[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
