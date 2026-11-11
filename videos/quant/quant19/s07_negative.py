from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, LOGN, NORMAL, PART, ask, fit_right, illustration, load
from videos.quant.quant19.common import ZERO as ZERO_C

MONTHS = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
          'November', 'December']


class Negative(VoiceoverScene):
    def construct(self):
        n = load("negative")
        self.card()
        self.ecb(n)
        self.bund(n["bund"])
        self.models(n)
        self.floors()
        self.oil()

    def card(self):
        c = chapter_card(6, r"Negative rates and Bachelier", r"What does a lognormal model do below zero?", lit=(2020,),
                         part=PART)
        with self.voiceover("Chapter six. Negative rates, and the return of Bachelier."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ecb(self, n):
        t, v = np.asarray(n["t"]), np.asarray(n["dfr"])
        g = axes([1999, 2026], [-1, 4.5], x_length=8.6, y_length=4.4, xlabel=r"year",
                 ylabel=r"ECB deposit facility rate, \%", xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[-1, 0, 2, 4],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(1999, 0), ax.c2p(2026, 0), color=WHITE, stroke_width=1.5)
        line = curve(ax, t, v, NORMAL, stroke_width=3)
        neg = v < 0
        shade = Polygon(*[ax.c2p(a, min(b, 0)) for a, b in zip(t[neg], v[neg])], ax.c2p(t[neg][-1], 0),
                        ax.c2p(t[neg][0], 0), stroke_width=0, fill_color=BAD, fill_opacity=0.35)

        def ymd(x):
            return f"{x % 100:d} {['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][x // 100 % 100]} {x // 10000:d}"
        side = VGroup(
            wrapped_label(rf"below zero from {ymd(n['first_neg'])} to {ymd(n['last_neg'])}", 3.6, 19, BAD),
            MathTex(rf"\min = {n['min']:.2f}\%", font_size=30, color=BAD),
            wrapped_label(r"banks paid to keep money at the central bank; for years, much of the euro area's government "
                          r"curve, and many swap rates, sat below zero", 3.6, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "For most of the history of finance, interest rates below zero were treated as impossible: why lend if you "
            "could hold cash? In June 2014 the European Central Bank cut its deposit rate below zero. "
            f"<bookmark mark='a'/> It stayed negative for eight years, as low as {n['min']:.1f} percent, until July "
            "2022. Banks paid to keep money at the central bank, and much of the euro area's government curve and many "
            "swap rates sat below zero with it. Denmark, Switzerland, Sweden and Japan went there too."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(line), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(shade), LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.4))
        self.add(illustration(r"FRED: ECBDFR"))
        self.wait(0.4)
        self.clear_scene()

    def bund(self, b):
        t, v = np.asarray(b["t"]), np.asarray(b["v"])
        g = axes([1999, 2026], [-1, 6], x_length=8.6, y_length=4.4, xlabel=r"year",
                 ylabel=r"German 10-year government yield, \%", xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                 yticks=[-1, 0, 2, 4, 6], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        zero = Line(ax.c2p(1999, 0), ax.c2p(2026, 0), color=WHITE, stroke_width=1.5)
        line = curve(ax, t, v, ZERO_C, stroke_width=3)
        neg = VGroup(*[Rectangle(width=ax.c2p(1 / 12, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 0)[1] - ax.c2p(0, y_)[1],
                                 stroke_width=0, fill_color=BAD, fill_opacity=0.5).move_to(
            [ax.c2p(x_, 0)[0], (ax.c2p(0, 0)[1] + ax.c2p(0, y_)[1]) / 2, 0]) for x_, y_ in zip(t, v) if y_ < 0])
        md = b["min_date"]
        side = VGroup(
            MathTex(rf"\min = {b['min']:.2f}\%", font_size=30, color=BAD),
            label(rf"{MONTHS[md // 100 % 100]} {md // 10000:d}", font_size=19, color=GREY_A),
            MathTex(rf"{b['months']}\ \text{{months below zero}}", font_size=26),
            wrapped_label(r"a buyer of a ten-year Bund in mid-2019 locked in a loss in nominal terms, held to maturity. "
                          r"Swiss, Dutch, French and Japanese yields went below zero too: at the peak in 2020, about "
                          r"\$18 trillion of bonds worldwide had negative yields", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        first = f"{MONTHS[b['first'] // 100 % 100]} {b['first'] // 10000:d}"
        low = f"{MONTHS[md // 100 % 100]} {md // 10000:d}"
        with self.voiceover(
            "And not only the overnight rate. The ten-year yield on German government bonds first averaged a month "
            f"below zero in {first}, and reached {b['min']:.2f} percent in {low}. <bookmark mark='a'/> An investor who "
            "bought then and held for ten years was guaranteed to get back less than they paid. Bonds of other "
            "countries followed, until in 2020 about eighteen trillion dollars of debt worldwide paid negative "
            "yields. Every model that assumed rates stay positive had to be retired or patched."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(line), run_time=2)
            self.play(FadeIn(neg), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.add(illustration(r"FRED: IRLTLT01DEM156N (OECD, monthly averages); the \$18 trillion is Bloomberg's "
                              r"index of negative-yielding debt, December 2020"))
        self.wait(0.4)
        self.clear_scene()

    def models(self, n):
        F, b, bl = np.asarray(n["F"]) * 100, np.asarray(n["bach"]) * 1e4, np.asarray(n["black"], float) * 1e4
        g = axes([-1, 2], [0, 220], x_length=7.4, y_length=4.4, xlabel=r"forward rate, \%",
                 ylabel=r"a 1-year call struck at 0\%, bp", xticks=[-1, 0, 1, 2], yticks=[0, 100, 200], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lb = curve(ax, F, np.clip(b, 0, 220), NORMAL, stroke_width=3.5)
        ok = np.isfinite(bl)
        ll = curve(ax, F[ok], np.clip(bl[ok], 0, 220), LOGN, stroke_width=3.5)
        wall = DashedLine(ax.c2p(0, 0), ax.c2p(0, 220), color=BAD, stroke_width=2)
        rows = [cmath(r"\ln(F/K)", r"\ ", r"\text{undefined for } F \le 0 \text{ or } K \le 0", font_size=32,
                      colors={r"\ln(F/K)": LOGN}),
                cmath(r"F + \text{shift}", r"\sim", r"\text{lognormal}", font_size=32, colors={r"F + \text{shift}": LOGN}),
                cmath(r"F", r"\sim", r"\mathcal{N}\big(F_0,\ \sigma_N^2 T\big)", font_size=32, colors={r"F": NORMAL})]
        side = VGroup(rows[0], why(r"Black's formula has no answer below zero: a lognormal rate can never get there"),
                      rows[1], why(r"the first patch: shifted Black, a lognormal model for the rate plus a constant"),
                      rows[2], why(r"the lasting one: Bachelier, quoted in basis points of normal volatility")).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3)
        if side.width > 5.4:
            side.scale_to_fit_width(5.4)
        leg = legend([(NORMAL, r"Bachelier, 60 bp"), (LOGN, r"Black, 60\% (ends at zero)")], font_size=17).next_to(
            g, UP, buff=0.05)
        with self.voiceover(
            "What does that do to the formulas? A one-year call on the rate, struck at zero, as the forward slides "
            "from two percent down to minus one. <bookmark mark='a'/> Bachelier's normal model prices it smoothly "
            "across zero. <bookmark mark='b'/> Black's lognormal model stops at the wall: the logarithm of a negative "
            "rate does not exist, and a lognormal rate can never get there. <bookmark mark='c'/> Desks first patched "
            "Black by shifting the rate by a constant; the lasting answer was to quote in Bachelier's normal "
            "volatility, basis points a year, as much of the interest rate option market now does."
        ) as vo:
            self.play(FadeIn(g), Create(wall), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lb), FadeIn(side[4]), FadeIn(side[5]), run_time=2)
            vo.wait_until("b")
            self.play(Create(ll), FadeIn(side[0]), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def floors(self):
        from explainer.quant.house import termstructure as TS
        F = np.linspace(-0.01, 0.02, 61)
        T = np.arange(0.25, 5.0001, 0.25)
        vals = np.array([sum(0.25 * TS.bachelier(f, 0.0, t, 0.006, cp=-1) for t in T) for f in F]) * 1e4
        g = axes([-1, 2], [0, 600], x_length=7.0, y_length=4.2, xlabel=r"forward rate, every quarter, \%",
                 ylabel=r"value of a 0\% floor, bp of notional", xticks=[-1, 0, 1, 2], yticks=[0, 200, 400, 600],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, F * 100, vals, NORMAL, stroke_width=3.5, smooth=True)
        k = int(np.argmin(np.abs(F - 0.005)))
        dot = Dot(ax.c2p(0.5, vals[k]), color=WHITE)
        side = VGroup(
            label(r"a 5-year floor at 0\%, quarterly; Bachelier, 60 bp", font_size=18, color=GREY_A),
            MathTex(rf"\text{{forward at }} 0.5\%:\ {vals[k]:.0f}\ \text{{bp}}", font_size=28),
            MathTex(r"\text{Black: } 0 \text{ for any } F > 0", font_size=26, color=LOGN),
            wrapped_label(r"from 2009 many leveraged loans and some deposits promised a floor: the floating rate never "
                          r"below 0\% (or 1\%). The lender owns that floor. A lognormal model says a positive rate can "
                          r"never reach zero, so it values the floor at nothing; a normal model gives it a real price, "
                          r"and it was paid out for years", 3.8, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            "Here is where the choice of model had a price. After 2009 many floating-rate loans promised that the rate "
            "used would never go below zero, or below one percent: the lender owned a floor. <bookmark mark='a'/> "
            "Value a five-year floor at zero percent. Under Bachelier, with rates at half a percent, it is worth "
            f"about {vals[k]:.0f} basis points of notional, more as rates fall. <bookmark mark='b'/> Under Black it "
            "is worth exactly nothing, because a lognormal rate cannot reach zero. Rates did reach zero, and "
            "below, and those floors paid for years."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dot), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def oil(self):
        cc = crisis_card(r"20--22 April 2020", r"A negative price, and a model switch",
                         r"the May contract of West Texas Intermediate crude oil settled at minus 37.63 dollars a barrel on "
                         r"20 April 2020: holders paid to be rid of oil they could not store. Black--Scholes cannot "
                         r"value an option on a negative price; CME Group moved its options on certain energy futures "
                         r"to the Bachelier model for its pricing and margins that week",
                         stats=[(r"-\$37.63", r"WTI May future, 20 April 2020"),
                                (r"\text{Bachelier}", r"CME's model for those options, from 22 April")],
                         width=8.4, font_size=21).move_to(UP * 0.4)
        foot = wrapped_label(r"Bachelier's 1900 thesis priced options on French government bonds; 120 years later it "
                             r"was the model left standing at and below zero", 11.0, 20, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Rates were not the only market to break through zero. On the twentieth of April 2020, with storage full, "
            "the expiring futures contract on West Texas crude oil settled at minus thirty-seven dollars and sixty-three "
            "cents a barrel. Options on it could not be valued in Black and Scholes, and that week CME Group switched "
            "those options to the Bachelier model. <bookmark mark='a'/> Louis Bachelier's 1900 thesis had priced "
            "options on French government bonds. A hundred and twenty years later, his was the model that still worked "
            "at and below zero."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(foot))
        q = ask(r"in a Bachelier world a rate can go to minus 5\%. What economic force stops that from happening, "
                r"and why is it weak?")
        with self.voiceover("In a Bachelier world a rate can reach minus five percent. What stops that in practice, and "
                            "why is the stop weak?"):
            self.play(FadeOut(foot), FadeIn(q))
        self.add(illustration(r"CME Group and Risk.net reports, April 2020; NYMEX WTI settlement, 20 April 2020"))
        self.wait(0.5)
        self.clear_scene()
