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
            desk_question(r"the test", r"take every sharp run-up in history and ask what came next: a crash more often than "
                          r"chance, or not?", width=12.0, font_size=21),
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
        rows = [cmath(r"\text{run-up}", r"\iff", r"R_{t-24,t} > 100\%\ \ \text{and}\ \ R_{t-24,t} - R^m_{t-24,t} > 100\%",
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
            "Robin Greenwood, Andrei Shleifer and Yang You took up Fama's challenge. Find every American industry whose "
            "price doubled in two years, both outright and relative to the market. <bookmark mark='a'/> Then ask what "
            "happened next. <bookmark mark='b'/> On Kenneth French's forty-nine industries since 1926 there are "
            f"{b['n']} such run-ups. {100 * b['p_crash']:.0f} percent of them crashed, falling forty percent from a peak "
            f"within two years. And yet the average return over those two years was {100 * b['mean_next']:+.0f} percent. "
            "Both sides were right: crashes are far more likely after run-ups, but the run-ups that kept running paid "
            "enough to make the average positive."
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
        g = axes([1925, 2026], [0.8, 3.8], x_length=8.4, y_length=4.4, xlabel=r"year of the run-up",
                 ylabel=r"two-year return, multiple", xticks=[1930, 1950, 1970, 1990, 2010], yticks=[1, 2, 3], font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup()
        for e in ev:
            y = e["ym"] // 100 + (e["ym"] % 100 - 0.5) / 12
            dots.add(Dot(ax.c2p(y, min(1 + e["raw"], 3.7)), color=BAD if e["crash"] else TAN, radius=0.07))
        side = VGroup(
            legend([(BAD, r"crashed within two years"), (TAN, r"did not")], font_size=17),
            wrapped_label(r"every 49-industry run-up, by when it happened and how far prices had risen (capped on the "
                          r"chart at $\times$3.7). They cluster in the 1930s recovery, the late 1960s, 1980, the late "
                          r"1990s and the 2020s. Greenwood, Shleifer and You find that volatility, issuance and a younger "
                          r"set of firms help tell the crashes apart in advance", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Every run-up, by when it happened and how far prices had climbed. <bookmark mark='a'/> Red ones crashed, "
            "the others did not. They cluster: the recovery of the 1930s, the go-go years of the late 1960s, the "
            "commodity boom of 1980, the late 1990s, and the 2020s. <bookmark mark='b'/> Greenwood, Shleifer and You "
            "found the crashes can be told apart, partly, in advance: run-ups with rising volatility, heavy share "
            "issuance and many young firms crashed more often. Predictable, then, in probability; never in timing."
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
        whys = [why(r"any price above the fundamental value $P^*$ that is expected to grow at the required return $r$ "
                    r"satisfies the pricing equation: a rational bubble"),
                why(r"Blanchard and Watson (1982): it may burst each period; to be held it must grow faster while it lasts, "
                    r"to pay for the risk of bursting"),
                why(r"with $r$ = 5\% and a 10\% chance a year of bursting: rising about 17\% a year, expected to last "
                    r"ten years")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.6, buff=0.7, edge=6.9)
        tail = wrapped_label(r"why rational bubbles are rare in theory: a bubble cannot be negative (shares can be thrown "
                             r"away), so if it is ever zero it is zero for ever, and it must have been there since the "
                             r"asset was first traded (Diba and Grossman, 1988); it cannot exist on a bond with a maturity "
                             r"(backward induction from the last payment); and it cannot grow faster than the economy for "
                             r"ever if $r$ exceeds growth", 12.4, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Can a bubble be rational? Write the price as the fundamental value plus a bubble term. If the bubble is "
            "expected to grow at exactly the required return, the pricing equation is still satisfied: nobody is "
            "making a mistake by holding it. <bookmark mark='a'/> Olivier Blanchard and Mark Watson let it burst. "
            "Each year it survives with some probability, and to be held it must grow faster while it lasts, to pay "
            "for the risk of bursting. <bookmark mark='b'/> With a required return of five percent and a one-in-ten "
            "chance a year of bursting, it rises about seventeen percent a year, and is expected to last ten. "
            "<bookmark mark='c'/> But theory hems it in. A bubble cannot be negative, so once it bursts it can never "
            "restart, and it must have existed since the asset first traded. It cannot exist on anything with a final "
            "payment, like a bond. And it cannot outgrow the economy for ever. Rational bubbles are possible; they "
            "are not a good description of the Nasdaq."
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
            desk_question(r"rational bubbles", r"a price above value can persist if it is expected to grow at the required "
                          r"return forever (Blanchard and Watson, 1982); impossible for assets with finite lives or a fixed "
                          r"supply against growing wealth", width=12.0, font_size=20),
            desk_question(r"riding the bubble", r"Brunnermeier and Nagel (2004): hedge funds held technology stocks in "
                          r"1998--2000 and sold before the peak; arbitrageurs may ride a bubble rather than fight it "
                          r"(Abreu and Brunnermeier, 2003)", width=12.0, font_size=20),
            desk_question(r"for a risk manager", r"a run-up raises the probability of a crash, not the certainty: size "
                          r"for the crash, as Rule 22 sized carry", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Theory has two strands. <bookmark mark='a'/> Rational bubbles, prices above value that grow at exactly the "
            "required return, can survive only in special conditions. <bookmark mark='b'/> More useful is the evidence "
            "that sophisticated investors ride bubbles instead of fighting them: Markus Brunnermeier and Stefan Nagel "
            "found hedge funds heavily in technology stocks in 1999, getting out before the peak. If the smart money "
            "times the bubble rather than shorting it, the bubble grows. <bookmark mark='c'/> For a risk manager the "
            "lesson is the one carry taught: a run-up changes the probability of a crash, not the date, so size the "
            "position for the crash."
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
