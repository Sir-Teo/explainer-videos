from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant23.common import BAD, CONS, GOOD, MKT, PART, SDF, TAN, ask, fit_right, illustration, load


class Bubbles(VoiceoverScene):
    def construct(self):
        b = load("bubbles")
        self.card()
        self.define()
        self.nasdaq(b)
        self.gsy(b)
        self.events(b)
        self.rational()
        self.theory()

    def card(self):
        c = chapter_card(12, r"Bubbles", r"Can you see one before it bursts?", lit=(2000,), part=PART)
        with self.voiceover("Chapter twelve. Bubbles, and whether anyone can see one coming."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def define(self):
        cards = VGroup(
            desk_question(r"Fama's view", r"a bubble is a predictable crash. If prices that have risen a lot do not "
                          r"predictably fall, the word has no content", width=12.0, font_size=21),
            desk_question(r"Shiller's view", r"a bubble is a social epidemic of optimism: rising prices draw in investors "
                          r"whose buying raises prices further", width=12.0, font_size=21),
            desk_question('the descriptive check', 'take every sharp run-up in history and ask what came next: what crash frequency and mean followed? A matched baseline would be needed to establish an increase', width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "What is a bubble? <bookmark mark='a'/> Eugene Fama's challenge: if prices that have risen a lot do not then "
            "predictably fall, the word means nothing; it is hindsight. <bookmark mark='b'/> Robert Shiller's answer: a "
            "bubble is an epidemic of optimism, rising prices drawing in buyers whose buying raises prices further. "
            "<bookmark mark='c'/> The disagreement can be tested: find every sharp run-up in history, and see what came "
            "after."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def nasdaq(self, b):
        n = b["nasdaq"]
        t, v = np.asarray(n["t"]), np.asarray(n["v"])
        g = axes([1995, 2004], [0, 5500], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"Nasdaq Composite",
                 xticks=[1995, 1997, 1999, 2001, 2003], yticks=[0, 1000, 2000, 3000, 4000, 5000], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, v, MKT, stroke_width=2.6)
        pk, tr = n["peak"], n["trough"]
        side = VGroup(
            MathTex(rf"10\ \text{{March 2000}}:\ {pk['v']:,.0f}".replace(",", "{,}"), font_size=26, color=MKT),
            MathTex(rf"9\ \text{{October 2002}}:\ {tr['v']:,.0f}".replace(",", "{,}"), font_size=26, color=BAD),
            MathTex(rf"{100 * (tr['v'] / pk['v'] - 1):.0f}\%", font_size=34, color=BAD),
            wrapped_label(r"the technology-heavy index rose almost sevenfold from 1995 to its peak, then lost almost four fifths; it "
                          r"did not regain the peak until 2015", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The bubble everyone remembers. <bookmark mark='a'/> The Nasdaq Composite, heavy with technology and "
            "internet companies, rose almost sevenfold between the start of 1995 and March 2000. <bookmark mark='b'/> It peaked on the "
            f"tenth of March 2000 at about {pk['v']:,.0f}, and by October 2002 had lost "
            f"{abs(100 * (tr['v'] / pk['v'] - 1)):.0f} percent. It took fifteen years to see the peak again. It looked "
            "like a bubble afterwards. Did it look like one before, in a way that could be measured?"
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in side], lag_ratio=0.3))
        self.add(illustration(r"FRED: NASDAQCOM"))
        self.wait(0.4)
        self.clear_scene()

    def gsy(self, b):
        rows = [cmath(r"\text{run-up}", r"\iff", r"R_{t-24,t} > 100\%\ \ \text{and}\ \ \frac{1+R_{t-24,t}}{1+R^m_{t-24,t}}-1 > 100\%",
                      font_size=34, colors={r"\text{run-up}": MKT}),
                cmath(r"\text{crash}", r"\iff", r"\text{a fall of } 40\% \text{ from a peak within the next 24 months}",
                      font_size=34, colors={r"\text{crash}": BAD})]
        whys = [why(r"Greenwood, Shleifer and You (2019), 'Bubbles for Fama': every US industry whose price doubled in two "
                    r"years, in absolute terms and against the market"),
                why(r"then: how often did it crash, and what did it return on average?")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        res = VGroup(
            MathTex(rf"{b['n']}\ \text{{run-ups in 49 industries, 1926--2025}}", font_size=30),
            MathTex(rf"\text{{crashed}}:\ {100 * b['p_crash']:.0f}\%", font_size=34, color=BAD),
            MathTex(rf"\text{{average return over the next two years}}:\ {100 * b['mean_next']:+.0f}\%", font_size=30,
                    color=MKT),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"Robin Greenwood, Andrei Shleifer and Yang You took up Fama's challenge. Find every American industry whose price doubled in two years, both outright and relative to the market. <bookmark mark='a'/> Then ask what happened next. <bookmark mark='b'/> On Kenneth French's forty-nine industries since 1926 there are {b['n']} such run-ups. {100 * b['p_crash']:.0f} percent of them crashed, falling forty percent from a peak within two years. And yet the average return over those two years was {100 * b['mean_next']:+.0f} percent. This original descriptive implementation uses a relative wealth ratio, fills missing industry returns with zero, and keeps the first trigger with at least twenty-five months between triggers per industry. Its sixty saved events all have complete twenty-four-month follow-up, although the algorithm allows censoring. Events can overlap across industries. No matched unconditional crash baseline is computed, so these results alone cannot establish an increased crash probability or a profitable short strategy."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def events(self, b):
        ev = b["events"]
        g = axes([1925, 2026], [0.8, 6.5], x_length=8.4, y_length=4.4, xlabel=r"year of the run-up",
                 ylabel=r"two-year return, multiple", xticks=[1930, 1950, 1970, 1990, 2010], yticks=[1, 2, 3, 4, 5, 6], font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup()
        for e in ev:
            y = e["ym"] // 100 + (e["ym"] % 100 - 0.5) / 12
            dots.add(Dot(ax.c2p(y, 1 + e["raw"]), color=BAD if e["crash"] else TAN, radius=0.07))
        side = VGroup(
            legend([(BAD, r"crashed within two years"), (TAN, r"did not")], font_size=17),
            wrapped_label('every 49-industry run-up, by when it happened and how far prices had risen, full multiples retained; colours use subsequent outcomes, known only in hindsight. They cluster in the 1930s recovery, the late 1960s, 1980, the late 1990s and the 2020s. Greenwood, Shleifer and You find that volatility, issuance and a younger set of firms help tell the crashes apart in advance', 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Every run-up, by when it happened and how far prices had climbed. <bookmark mark='a'/> Red ones subsequently crashed, the others did not; those colours use hindsight, and the full return multiples are retained without clipping. They cluster: the recovery of the 1930s, the go-go years of the late 1960s, the commodity boom of 1980, the late 1990s, and the 2020s. <bookmark mark='b'/> Greenwood, Shleifer and You found the crashes can be told apart, partly, in advance: run-ups with rising volatility, heavy share issuance and many young firms crashed more often. Those are findings of the cited paper; our simplified event table does not recompute their predictors or establish a matched-baseline probability improvement."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.04), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
        self.add(illustration(r"Kenneth French's 49 industries; the rules of Greenwood, Shleifer and You (2019)"))
        self.wait(0.4)
        self.clear_scene()

    def rational(self):
        rows = [cmath(r"P_t", r"=", r"P^*_t + B_t,\qquad \mathbb{E}_t[B_{t+1}] = (1 + r)\,B_t", font_size=40,
                      colors={r"P_t": MKT}),
                cmath(r"B_{t+1}", r"=", r"\begin{cases} \frac{1 + r}{\pi}\,B_t & \text{with probability } \pi \\ 0 & "
                      r"\text{otherwise} \end{cases}", font_size=36, colors={r"B_{t+1}": BAD}),
                cmath(r"\frac{1 + r}{\pi} - 1", r"=", r"\frac{1.05}{0.9} - 1 \approx 16.7\%\ \text{a year}", font_size=38)]
        whys = [why('risk-neutral, constant-required-return illustration. General pricing needs $B_t=E_t[m_{t+1}B_{t+1}]$; no-bubble transversality excludes it: a rational bubble'),
                why(r"Blanchard and Watson (1982): it may burst each period; to be held it must grow faster while it lasts, "
                    r"to pay for the risk of bursting"),
                why(r"with $r$ = 5\% and a 10\% chance a year of bursting: rising about 17\% a year, expected to last "
                    r"ten years")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        tail = wrapped_label('conditional restrictions: under a nonnegative bubble and positive pricing kernel, zero is absorbing. A known finite terminal payoff permits backward induction. Wealth-growth restrictions need additional assumptions; fixed supply alone does not rule bubbles out', 12.4, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A bubble term must satisfy the same pricing equation as other payoffs: B today equals the expectation of next B times the stochastic discount factor. The physical-expectation formula on screen is a risk-neutral constant-required-return illustration, not the general risk-adjusted condition. <bookmark mark='a'/> Blanchard and Watson allow the bubble to burst; conditional on survival it must grow faster. <bookmark mark='b'/> With a five-percent required return and a ten-percent annual burst probability, the fixed illustration gives sixteen point seven percent conditional growth and ten years expected waiting time. <bookmark mark='c'/> No-bubble transversality excludes such a term. Under additional nonnegativity and positive-kernel assumptions, zero is absorbing. A known finite final payoff supports backward induction, while limits from wealth growth require further assumptions. Fixed supply alone does not rule out bubbles, and none of this identifies the Nasdaq as a rational bubble."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(tail))
        self.wait(0.4)
        self.clear_scene()

    def theory(self):
        cards = VGroup(
            desk_question(r"rational bubbles", 'a price above value can persist if it is expected to grow at the required return forever (Blanchard and Watson, 1982); impossible for assets with finite lives under an imposed no-bubble transversality condition; fixed supply alone is insufficient', width=12.0, font_size=20),
            desk_question(r"riding the bubble", 'Brunnermeier and Nagel (2004): hedge funds held technology stocks in 1998--2000 with portfolio-level timing evidence, not universal perfect pre-peak exit; arbitrageurs may ride a bubble rather than fight it (Abreu and Brunnermeier, 2003)', width=12.0, font_size=20),
            desk_question(r"for a risk manager", 'the saved run-up sample has substantial subsequent crash frequency; no unconditional baseline or timing guarantee: size for the crash, as Rule 22 sized carry', width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Theory has two strands. <bookmark mark='a'/> Rational bubbles, prices above value that grow at exactly the required return, can survive only in special conditions. <bookmark mark='b'/> More useful is the evidence that sophisticated investors ride bubbles instead of fighting them: Markus Brunnermeier and Stefan Nagel found hedge funds heavily in technology stocks in 1999, with evidence of portfolio-level timing, not proof that all funds exited perfectly before the peak. Their study does not establish a universal timing ability or certify the strategy's riskless profitability. <bookmark mark='c'/> For a risk manager the lesson is the one carry taught: the saved conditional sample contains large crash risk, but it has no matched unconditional comparison or reliable crash date. Position sizing must also account for liquidity, borrow and model uncertainty."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"an industry has doubled in two years against the market. The data say a crash follows about half the "
                r"time, yet the average return after is positive. Would you short it?")
        with self.voiceover("An industry has doubled in two years against the market. A crash follows about half the time, "
                            "yet the average return after is positive. Would you short it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
