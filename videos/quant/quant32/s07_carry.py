from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, CARRY_C, GOOD, HURDLE, PART, SPY_C, fit_right, load

CCY = {"FXA": r"Australian dollar", "FXE": r"euro", "FXB": r"pound", "FXY": r"yen", "FXF": r"Swiss franc",
       "FXC": r"Canadian dollar"}


class Carry(VoiceoverScene):
    def construct(self):
        c = load("carry")
        self.card()
        self.split()
        self.oil(c)
        self.contango()
        self.bonds()
        self.crisis(c)
        self.fx(c)
        self.book(c)
        self.lessons()
        self.question()

    def card(self):
        c = chapter_card(6, r"Carry, made visible", r"How much of a fund's return is the price, and how much is carry?",
                         part=PART)
        with self.voiceover("Chapter six. Carry is the part of a return you can see in advance. In the House's own panel "
                            "it can be measured directly, by setting each fund against the spot price it tracks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def split(self):
        rows = [cmath(r"r^{\text{fund}}", r"=", r"r^{\text{spot}} + \underbrace{\text{carry}}_{\text{roll, interest}} - "
                      r"\text{fees}", font_size=36, colors={r"\text{carry}": CARRY_C}),
                cmath(r"\text{oil fund}", r":", r"\text{carry} = \text{roll yield} = (S - F)/F\ \text{each month}",
                      font_size=32),
                cmath(r"\text{currency fund}", r":", r"\text{carry} = i^{*} - i\ \ \text{(the deposit rate it earns)}",
                      font_size=32)]
        whys = [why(r"a fund that holds futures or deposits earns the spot price's change plus what the position earns if "
                    r"the price stands still"),
                why(r"an oil fund holds the next month's future and sells it before expiry: when the future is above spot "
                    r"(contango), each roll loses the gap"),
                why(r"a currency fund holds a foreign deposit: it earns the foreign interest rate, and over T-bills, the "
                    r"differential")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The decomposition. <bookmark mark='a'/> A fund that holds futures or deposits earns the change in the spot "
            "price, plus carry, less fees. <bookmark mark='b'/> An oil fund holds next month's future and sells it "
            "before expiry; when futures sit above spot, every roll loses the gap. <bookmark mark='c'/> A currency fund "
            "holds a foreign deposit, and earns the foreign interest rate. So the fund's return minus the spot price's "
            "return is carry, measured."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def oil(self, c):
        u = c["cmd"]["USO"]
        md = np.asarray(u["months"], float)
        x = md // 100 + ((md % 100) - 0.5) / 12
        yf, ys = 100 * np.asarray(u["cum_fund"], float), 100 * np.asarray(u["cum_spot"], float)
        g = axes([x[0], x[-1]], [-100, 60], x_length=7.4, y_length=4.4, xlabel=r"mid-2007 to 2020",
                 ylabel=r"cumulative return, \%", xticks=[2008, 2012, 2016, 2020], yticks=[-100, -50, 0, 50],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, x, np.clip(ys, -100, 60), HURDLE, stroke_width=3)
        l2 = curve(ax, x, np.clip(yf, -100, 60), BAD, stroke_width=3)
        leg = legend([(HURDLE, r"WTI crude, spot (FRED)"), (BAD, r"USO, the oil fund")], font_size=16)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        g_ = c["cmd"]["UNG"]
        st = VGroup(label(rf"oil: spot {100 * u['spot']:+.1f}\%, fund {100 * u['fund']:+.1f}\% a year", font_size=16,
                          color=GREY_A),
                    label(rf"natural gas: spot {100 * g_['spot']:+.1f}\%, fund {100 * g_['fund']:+.1f}\% a year",
                          font_size=16, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        st.next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        fit_right(st)
        gap = u["spot"] - u["fund"]
        with self.voiceover(
            "Oil. <bookmark mark='a'/> The spot price of crude went up and down and ended the period somewhat lower: "
            f"{100 * u['spot']:+.1f} percent a year in log terms. <bookmark mark='b'/> The oil fund lost "
            f"{abs(100 * u['fund']):.0f} percent a year: about {100 * gap:.0f} points a year of negative carry, the cost of "
            f"rolling futures in a market that was mostly in contango. Natural gas was worse: a fund return of "
            f"{100 * g_['fund']:.0f} percent a year against a spot of {100 * g_['spot']:.0f}. An investor who bought "
            "these funds to own the commodity owned the roll instead."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(l1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(st), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def contango(self):
        mats = np.arange(1, 13)
        cont = 50 + 1.2 * mats
        back = 50 - 1.0 * mats
        g = axes([0.5, 12.5], [35, 70], x_length=6.8, y_length=4.0, xlabel=r"months to delivery",
                 ylabel=r"futures price", xticks=[1, 6, 12], yticks=[40, 50, 60], font_size=15).move_to(LEFT * 1.8)
        ax = g.ax
        c1 = curve(ax, mats, cont, BAD, stroke_width=3)
        c2 = curve(ax, mats, back, GOOD, stroke_width=3)
        spot = Dot(ax.c2p(0.5, 50), radius=0.09, color=WHITE)
        sl = label(r"spot", font_size=16).next_to(spot, LEFT, buff=0.1)
        leg = legend([(BAD, r"contango: the holder pays to roll"), (GOOD, r"backwardation: the holder is paid")],
                     font_size=16).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        fit_right(leg)
        txt = wrapped_label(r"carry for a commodity: storage costs and interest push futures above spot; a shortage, or "
                            r"producers hedging, pulls them below. Keynes and Hicks called the second normal backwardation, "
                            r"a premium paid by hedgers", 4.0, 16, GREY_A).next_to(leg, DOWN, buff=0.4)
        fit_right(txt)
        ill = note(r"illustration", font_size=18, color=GREY_B).to_corner(DL, buff=0.25)
        with self.voiceover(
            "Why it happens. <bookmark mark='a'/> When storage is plentiful, futures sit above spot to pay for storage "
            "and interest: contango, and a long holder loses as each future converges down to spot. "
            "<bookmark mark='b'/> When supply is tight, or producers hedge heavily, futures sit below spot: "
            "backwardation, and the holder is paid. John Maynard Keynes and John Hicks argued that the second is the "
            "normal state, a premium paid by hedgers to speculators. Carry strategies in commodities buy the "
            "backwardated markets and sell the contangoed ones."
        ) as vo:
            self.play(FadeIn(g), FadeIn(spot), FadeIn(sl), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(leg[1]), FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def crisis(self, c):
        u = c["uso_2020"]
        card = crisis_card(r"20 April 2020", r"Negative oil",
                           r"with storage at Cushing nearly full, the expiring May WTI futures contract settled at "
                           r"$-\$37.63$ a barrel: holders had to pay to give it away. USO, which held front-month "
                           r"futures, moved to longer maturities, as reported, and lost most of its value in two months",
                           stats=((r"-\$37.63", r"May 2020 WTI settlement, 20 April"),
                                  (rf"{100 * min(u['cum']):.0f}\%", r"USO's worst cumulative excess return from 1 March "
                                                                     r"2020, computed here")),
                           width=11.0, font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "The crisis file. In April 2020, with demand collapsed and storage at Cushing, Oklahoma, nearly full, the "
            "expiring May crude contract settled at minus thirty-seven dollars and sixty-three cents a barrel: holders "
            "paid to have it taken away. The oil fund, which held front-month futures, moved into longer maturities, "
            f"as reported. From the first of March its excess return fell as far as {100 * min(u['cum']):.0f} percent. "
            "Contango, at its extreme, is a market telling the holder that there is nowhere to put the oil."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def fx(self, c):
        fx = c["fx"]
        keys = sorted(fx, key=lambda k: fx[k]["carry"], reverse=True)
        mx = max(abs(fx[k]["carry"]) for k in keys)
        bars = VGroup()
        for j, k in enumerate(keys):
            v = fx[k]["carry"]
            r = Rectangle(width=max(abs(v) * 4.5 / mx, 0.03), height=0.5, fill_color=CARRY_C if v > 0 else BAD,
                          fill_opacity=0.85, stroke_width=0).move_to([0.6, 1.9 - 0.75 * j, 0],
                                                                     aligned_edge=LEFT if v > 0 else RIGHT)
            bars.add(VGroup(label(CCY[k], font_size=21, color=GREY_A).move_to([-4.0, 1.9 - 0.75 * j, 0]), r,
                            MathTex(rf"{100 * v:+.1f}\%", font_size=24).next_to(r, RIGHT if v > 0 else LEFT, buff=0.15)))
        axis = Line([0.6, 2.4, 0], [0.6, -2.4, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"Currency funds: carry over T-bills, a year, mid-2007 to 2020", font_size=26).to_edge(UP, buff=0.35)
        foot = wrapped_label(r"each CurrencyShares fund's monthly excess return minus the change in FRED's spot rate for its "
                             r"currency: the foreign deposit rate over the US bill rate, net of the fund's fee", 11.6, 16,
                             GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Currencies. <bookmark mark='a'/> Subtract the spot rate's change from each currency fund's return over "
            "bills, and what remains is the interest differential, net of fees. <bookmark mark='b'/> Over these years "
            "only the Australian dollar paid a positive carry, about one and a half percent a year. The yen, the Swiss "
            "franc and the euro paid less than American bills, and their funds charged fees on top: negative carry. "
            "After 2008 interest rates everywhere sat near zero, and the classic carry trade had little to harvest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b[0]) for b in bars], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(b[1], b[2])) for b in bars], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def book(self, c):
        b = c["book"]
        md = np.asarray(b["months"], float)
        x = md // 100 + ((md % 100) - 0.5) / 12
        y = 100 * np.asarray(b["cum"], float)
        lo, hi = float(np.floor(y.min() / 10) * 10), float(np.ceil(y.max() / 10) * 10)
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.4, y_length=4.2, xlabel=r"2008--2020",
                 ylabel=r"cumulative return, \%", xticks=[2010, 2015, 2020], yticks=[lo, 0, hi],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, x, y, CARRY_C, stroke_width=3)
        st = VGroup(label(rf"Sharpe ratio {b['sharpe']:.2f}", font_size=17, color=CARRY_C),
                    label(rf"October--December 2008: {100 * b['q4_2008']:+.0f}\%", font_size=17, color=BAD),
                    label(rf"monthly skewness {b['skew']:.2f}", font_size=17, color=BAD)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.14)
        st.to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        fit_right(st)
        foot = wrapped_label(r"each month, long the two currency funds with the highest trailing-year carry and short the two "
                             r"lowest, equal weights; research only, not registered", 11.0, 16, GREY_A).to_edge(DOWN,
                                                                                                     buff=0.3)
        with self.voiceover(
            "A carry book from the six funds: each month, long the two with the highest carry over the past year, short "
            "the two lowest. <bookmark mark='a'/> It begins with a crash: in the last quarter of 2008 it lost "
            f"{abs(100 * b['q4_2008']):.0f} percent, as investors fled high-yielding currencies for the yen and the "
            f"franc. <bookmark mark='b'/> Over the whole period, a Sharpe ratio of {b['sharpe']:.2f} and a skewness of "
            f"{b['skew']:.2f}. Carry is paid for crash risk, and in these years, with little carry left to earn, the "
            "crash was most of the story."
        ) as vo:
            self.play(FadeIn(g), FadeIn(foot))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"carry is visible", r"unlike most premia it can be measured in advance: the curve, the rate, the "
                          r"basis; the risk is in the price change it does not control", width=12.4, font_size=19),
            desk_question(r"carry is pro-cyclical", r"high-carry assets fall in a crisis as leveraged holders sell: the "
                          r"same skew as selling insurance (next chapter)", width=12.4, font_size=19),
            desk_question(r"carry is a product's hidden cost", r"a fund that rolls futures in contango or holds a "
                          r"low-yielding deposit can lose steadily while its underlying goes nowhere", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Carry, unlike most premia, can be seen in advance: in the curve, the "
            "rate, the basis. The risk is in the price change it does not control. <bookmark mark='b'/> Carry is "
            "pro-cyclical: high-carry assets fall together in a crisis, as leveraged holders sell; the same skew as "
            "selling insurance, which is the next chapter. <bookmark mark='c'/> And carry is the hidden cost of many "
            "products: a fund can lose steadily while the thing it tracks goes nowhere."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def bonds(self):
        rows = [cmath(r"\text{carry}_{\text{bond}}", r"\approx", r"(y_n - r_f) + \underbrace{(y_n - y_{n-\Delta})\,D}_{"
                      r"\text{roll-down}}", font_size=34, colors={r"\text{carry}_{\text{bond}}": CARRY_C}),
                cmath(r"\text{steep curve}", r":", r"\text{high carry; flat or inverted: little or negative}", font_size=32),
                cmath(r"\text{carry across countries}", r":", r"\text{long the steep curves, short the flat}", font_size=30)]
        whys = [why(r"a bond earns its yield over the short rate, plus the price gain as it ages into a lower yield on an "
                    r"upward-sloping curve (Part 18's roll-down), times its duration"),
                why(r"so carry is the slope of the curve, and the slope is what an investor is paid for holding duration"),
                why(r"the bond carry of AQR's series, a Sharpe ratio of about 0.65 over a century, is this trade in "
                    r"government bond futures")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Bonds have carry too. <bookmark mark='a'/> A bond earns its yield over the short rate, plus the gain as it "
            "rolls down an upward-sloping curve into a lower yield, which Part eighteen called roll-down. "
            "<bookmark mark='b'/> So a bond's carry is the slope of the curve: high when it is steep, negative when it "
            "inverts. <bookmark mark='c'/> Across countries, the carry trade buys the steep curves and sells the flat "
            "ones; in AQR's series it was the most rewarding carry of all, with a Sharpe ratio of about two thirds over a "
            "century."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card(r"oil's one-month future is \$2 above spot at \$50, and spot does not move for a year. Roughly what "
                       r"does a fund that rolls monthly lose?")
        with self.voiceover(
            "Pause and predict. Oil's one-month future is two dollars above a spot price of fifty, and spot does not "
            "move for a year. Roughly what does a fund that rolls every month lose?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
