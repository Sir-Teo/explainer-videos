from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, BARRIER, DELTA, GOOD, IV, OPT, PART, SPOT, VEGA, load

DESK = [
    (r"Price a digital with a call spread. What width, and what happens to the hedge near expiry?",
     r"buy the $K - \varepsilon$ call and sell the $K$ call, scaled by $1/\varepsilon$: it pays at least the digital, costs "
     r"about $\varepsilon$ times the density more, and caps the delta at $1/\varepsilon$; near expiry the hedge still "
     r"swings, but within a band the desk can trade"),
    (r"Why is a snowball's issuer long volatility above the knock-in, and what changes below it?",
     r"above the barrier the issuer owns the down-and-in put the buyer sold: more volatility makes a knock-in likelier, "
     r"so the issuer is long vega; once knocked in, the put has become a forward-like position and the vega collapses"),
    (r"A client wants a worst-of note on three indices. What is your biggest risk?",
     r"correlation: you own the put on the worst performer, so you are short correlation, an input no market quotes; in "
     r"a crash correlations jump toward one, and your marks move on a number you cannot hedge"),
]

PROBLEMS = [
    r"With $r = q = 0$, use the reflection principle to show that a down-and-out call ($H \le K$) is worth "
    r"$C(S, K) - \frac{S}{H} C\big(\frac{H^2}{S}, K\big)$.",
    r"Explain why a barrier watched every $\Delta t$ behaves like a continuous one moved by $e^{\pm\beta\sigma\sqrt{\Delta t}}$, "
    r"and check it against a simulation.",
    r"Show that the geometric average of $n$ log-normal fixings is log-normal, and find its mean and variance.",
    r"Show that $\frac{C(K - \varepsilon) - C(K)}{\varepsilon}$ dominates the digital at every expiry price and converges to "
    r"it as $\varepsilon \to 0$.",
    r"Write a snowball as a bond, a strip of knock-out-contingent coupons and a short down-and-in put, and explain the "
    r"sign of the buyer's vega.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("barrier"), load("asian"), load("snowball"), load("book2024"), load("korea"), load("surrogate"),
                   load("worstof"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, b, a, s, bk, k, sg, w):
        lost = [r for r in k["rows"] if r["knocked_in"]]
        dl = np.asarray(bk["dealer_delta"])
        px = np.asarray(bk["close"])
        items = [
            (r"a structured note is a bond plus options; the issuer keeps the gap to fair value", OPT),
            (rf"a monthly-watched barrier is worth {b['rows'][0]['mc']:.2f}, not {b['continuous']:.2f}: shift it by BGK", BARRIER),
            (r"a digital is a smooth price on an impossible hedge: book it as a call spread", BAD),
            (rf"a snowball's fair coupon was {100 * s['coupon']:.1f}\%: the price of selling a crash", IV),
            (rf"January 2024: dealers' hedges grew to {dl.max():.0f} and were cut to {dl[np.argmin(px)]:.0f} at the low", DELTA),
            (rf"Korea: {len(lost)} of 12 notes from 2021 lost {100 * min(-r['return'] for r in lost):.0f}--"
             rf"{100 * max(-r['return'] for r in lost):.0f}\%", BAD),
            (rf"a worst-of is short correlation; uncertain volatility puts a price on the model", GOOD),
            (rf"a network reprices a snowball in {1e6 * sg['t_net']:.1f} microseconds", VEGA),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 15 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part fifteen in eight lines. A structured note is a bond plus options, and the issuer keeps the gap to "
            "fair value. Barriers depend on how often they are watched. A digital is a smooth price on an impossible "
            "hedge. A snowball's coupon is the price of selling a crash. In January 2024 the dealers who had bought "
            "all the way down were forced to sell at the bottom. Korea's savers learned the same lesson from Hong "
            "Kong. Worst-of notes are bets on correlation, and model uncertainty has a price. And a small network can "
            "reprice a whole book in microseconds."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. A digital is hedged as a call spread, whose width trades price against a hedge "
            "the desk can run. <bookmark mark='a'/> A snowball's issuer is long volatility above the barrier, because "
            "it owns the put the buyer sold, and that exposure collapses once the barrier breaks. "
            "<bookmark mark='b'/> And a worst-of on three indices leaves the dealer short correlation, an input no "
            "market quotes. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "And five problems: the barrier formula by reflection, the discrete-monitoring shift, the geometric "
            "average, the call spread's bound, and the snowball taken apart. Solutions, in English and Chinese, are in "
            "the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"Monte Carlo, PDEs and Greeks for path-dependent payoffs", [16]),
            (r"neural pricers and hedgers at scale", [17]),
            (r"the issuer's credit, funding and XVA on every note", [21]),
            (r"crowded hedges, leverage and crises", [41]),
        ])
        with self.voiceover(
            "Where this comes back. Part sixteen builds the Monte Carlo and finite-difference engines these prices "
            "need, with Greeks. Part seventeen trains pricers and hedgers at scale. Every note is also the issuer's "
            "debt, which Part twenty-one prices. And crowded hedges return in Part forty-one, on crises."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Hull, \textit{Options, Futures, and Other Derivatives}, ch.\ 26; Bouzoubaa and Osseiran, \textit{Exotic "
             r"Options and Hybrids}", r"Guyon and Henry-Labord\`ere, \textit{Nonlinear Option Pricing}; Wilmott, "
             r"\textit{Paul Wilmott on Quantitative Finance}"],
            [r"Merton (1973); Goldman, Sosin and Gatto (1979); Kemna and Vorst (1990); Reiner and Rubinstein (1991)",
             r"Avellaneda, Levy and Par\'as (1995); Lyons (1995); Broadie, Glasserman and Kou (1997); Cont (2006)",
             r"Henderson and Pearson (2011); C\'el\'erier and Vall\'ee (2017); Bloomberg, Risk.net, Korean press (2024)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers and reports it draws on. The data are the CSI 500 "
            "through its largest fund and the HSCEI, from Yahoo Finance."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 16, Computing Prices", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The volatility desk can now price, hedge and reserve for the products it sells. "
            "<bookmark mark='a'/> Next, Part sixteen: computing prices. Monte Carlo and its variance reduction, "
            "finite differences, Fourier methods and adjoint Greeks, and how fast each one really is."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
