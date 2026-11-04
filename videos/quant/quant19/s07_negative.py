from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, LOGN, NORMAL, PART, ask, fit_right, illustration, load


class Negative(VoiceoverScene):
    def construct(self):
        n = load("negative")
        self.card()
        self.ecb(n)
        self.models(n)
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
            return f"{x % 100} {['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][x // 100 % 100]} {x // 10000}"
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
            self.play(FadeIn(q))
        self.add(illustration(r"CME Group and Risk.net reports, April 2020; NYMEX WTI settlement, 20 April 2020"))
        self.wait(0.5)
        self.clear_scene()
