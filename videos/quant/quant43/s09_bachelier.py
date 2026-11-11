from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import ladder
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C,
                                         era_strip, load)


class Bachelier(VoiceoverScene):
    def construct(self):
        self.card()
        self.april()
        self.normal_vols()
        self.formulas()
        self.prices(load("bachelier"))
        self.fair_game()
        self.thesis()
        self.timeline()
        self.question()

    def card(self):
        c=chapter_card(8,r"Back to Bachelier",r"Price support, strikes and the pricing measure",part=PART)
        with self.voiceover(
            "Chapter eight. A dated example of model support. The May WTI futures contract settled at minus "
            "thirty-seven dollars and sixty-three cents on April twentieth, twenty twenty. CME Clearing then used "
            "Bachelier valuation for specified energy products from the April twenty-second end-of-day margin cycle. "
            "This was a clearing valuation change with a stated product scope, not a claim about every transaction's "
            "pricing. A later notice returned products to Whaley or Black seventy-six from August thirty-first."
        ):self.play(FadeIn(c[0],shift=UP*.2),FadeIn(c[1]))
        self.play(FadeOut(c))

    def april(self):
        cards=VGroup(
            desk_question(r"20 April 2020",r"May WTI futures settled at $-\$37.63$; the CFTC described coinciding demand, supply, storage and market-structure factors",width=12.4,font_size=19),
            desk_question(r"CME Clearing 20-171",r"specified products: Bachelier pricing/valuation from the end-of-day margin cycle on 22 April 2020",width=12.4,font_size=19),
            desk_question(r"CME Clearing 20-320",r"products transitioned back to Whaley or Black 76 from trade date 31 August 2020, depending on product",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "The public record has a precise scope. <bookmark mark='a'/> The CFTC confirms the May contract's "
            "negative settlement and discusses coinciding fundamental and market-structure factors, without claiming "
            "a complete root-cause decomposition. <bookmark mark='b'/> CME Clearing notice twenty dash one seventy-one "
            "specifies the April valuation change for listed products and its margin-cycle timing. "
            "<bookmark mark='c'/> Notice twenty dash three twenty later specifies the August transition back, depending "
            "on product. These are historical notices, not a statement of today's complete valuation policy."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def normal_vols(self):
        cards=VGroup(
            desk_question(r"rates",r"normal and shifted-lognormal conventions can accommodate rate domains where an unshifted lognormal model is unsuitable",width=12.4,font_size=19),
            desk_question(r"spreads",r"a normal model allows either sign, but suitability also depends on tails, dynamics and the payoff",width=12.4,font_size=19),
            desk_question(r"units",r"normal volatility has price units per square-root year; lognormal volatility is relative per square-root year",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "The support question extends beyond oil. <bookmark mark='a'/> Normal and shifted-lognormal rate "
            "conventions are alternatives when unshifted positive support is inappropriate. "
            "<bookmark mark='b'/> A normal model also permits negative spreads, but matching the support alone does "
            "not validate its tails or dynamics. <bookmark mark='c'/> Its volatility has absolute price units, whereas "
            "lognormal volatility is relative. Setting normal volatility equal to the current forward times relative "
            "volatility matches a local diffusion coefficient; it does not exactly equate option prices."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def formulas(self):
        rows=[cmath(r"dF_t",r"=",r"\sigma_NdW_t^Q\quad\text{(zero-rate normal forward model)}",font_size=34),
              cmath(r"C",r"=",r"(F-K)\Phi(d)+s_N\varphi(d),\quad d=(F-K)/s_N",font_size=36),
              cmath(r"dF_t",r"=",r"\sigma F_tdW_t^Q,\quad F_0>0\Rightarrow F_t>0",font_size=36)]
        whys=[why(r"risk-neutral forward formulation; normal terminal support includes negative prices"),
              why(r"$s_N=\sigma_N\sqrt T>0$; at nonzero deterministic rates multiply by the discount factor"),
              why(r"unshifted Black-76 forward dynamics; stock BSM additionally specifies carry and spot drift")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=0,buff=.6)
        with self.voiceover(
            "Compare two zero-rate risk-neutral forward models. <bookmark mark='a'/> Normal forward increments can "
            "cross zero. <bookmark mark='b'/> Integrating the normal payoff gives the displayed call price, with s N "
            "equal to normal volatility times square-root maturity. A deterministic discount factor is needed at "
            "nonzero rates. <bookmark mark='c'/> Unshifted Black forward dynamics preserve a strictly positive initial "
            "forward. A negative underlying forward therefore falls outside that model; this is different from asking "
            "about a nonpositive strike on a positive forward."
        ) as vo:
            step(0)
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:step(k)
        self.clear_scene()

    def prices(self,b):
        tab=VGroup(VGroup(*[label(v,font_size=20,color=QC.IDEA)for v in(r"strike",r"normal model",r"positive Black model")]))
        for x in b['rows']:
            black=x['bs']if np.isfinite(x['bs'])else b['S']-x['K']
            tab.add(VGroup(label(rf"{x['K']:+.0f}",font_size=21),label(rf"{x['bachelier']:.2f}",font_size=21,color=MKT_C),label(rf"{black:.2f}",font_size=21,color=ACT_C)))
        for j,row in enumerate(tab):
            for cell,x in zip(row,(-3.3,0,3.5)):cell.move_to([x,2.5-.65*j,0])
        note=wrapped_label(r"$F=10$, $T=1/12$, $\sigma_N=F\sigma$. Coefficients matched locally, not exact ATM prices. "
                           r"For $K\le0$ the Black call is analytically $F-K$; original skipped entries are extended here.",12.4,19,GREY_B).to_edge(DOWN,buff=.4)
        with self.voiceover(
            "The ordinary numerical example has a positive ten-dollar forward and one-month maturity. "
            "<bookmark mark='a'/> Volatility coefficients are matched locally; the at-the-money call values are "
            "close, but not exactly equal. <bookmark mark='b'/> Away from the money, support and tails change the "
            "payoff expectation. <bookmark mark='c'/> The original computation skips Black values at zero and negative "
            "strikes. They are not undefined economically: a strictly positive lognormal terminal forward makes the "
            "call payoff always F T minus K, so its zero-rate price is F minus K. The table supplies that analytical "
            "extension. Negative underlying forwards are the separate domain problem motivating the normal model."
        ) as vo:
            self.play(FadeIn(tab[0]),FadeIn(tab[4]),FadeIn(note))
            vo.wait_until('a');vo.wait_until('b');self.play(FadeIn(tab[3]),FadeIn(tab[5]))
            vo.wait_until('c');self.play(FadeIn(tab[1]),FadeIn(tab[2]))
        self.clear_scene()

    def fair_game(self):
        rows=[cmath(r"\mathbb E_Q[F_{t+1}\mid\mathcal F_t]",r"=",r"F_t",font_size=42),
              cmath(r"G_T=\int_0^T H_t\,dF_t",r"\Rightarrow",r"\mathbb E_QG_T=0\quad\text{under integrability conditions}",font_size=32),
              cmath(r"Q\text{-pricing}",r"\ne",r"\text{a claim of zero physical expected excess return}",font_size=32)]
        whys=[why(r"the pricing measure and the traded or forward gain process must be specified"),
              why(r"for example, bounded predictable H and a square-integrable martingale on a finite horizon"),
              why(r"Sharpe's accounting identity is separate from a probabilistic martingale assumption")]
        step=ladder(self,rows,whys,keep=3,top=2.6,x=0,buff=.6)
        with self.voiceover(
            "Return to the fair game with its measure stated. <bookmark mark='a'/> Under the pricing measure, a "
            "suitable forward gain process is a martingale. <bookmark mark='b'/> Predictable trading against it has "
            "zero expected gain when the stochastic integral is a true integrable martingale, for example with "
            "bounded holdings and square-integrable increments over a finite horizon. Predictability alone is not "
            "enough. <bookmark mark='c'/> A pricing-measure statement does not imply zero physical expected alpha, "
            "and Sharpe's holdings identity is a separate accounting argument. Neither licenses a universal claim "
            "that every actual trading strategy has zero expected profit."
        ) as vo:
            step(0)
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:step(k)
        self.clear_scene()

    def thesis(self):
        cards = VGroup(
            desk_question(r"Paris, 29 March 1900", r"Louis Bachelier defended ``Théorie de la spéculation'', with Henri "
                          r"Poincaré on the committee; it received a respectable but not the highest mention, as "
                          r"historians report", width=12.4, font_size=19),
            desk_question(r"what was in it", r"the random walk, the diffusion equation five years before Einstein's "
                          r"paper, and option prices tested on Paris rentes", width=12.4, font_size=19),
            desk_question(r"forgotten, then found", r"rediscovered in the 1950s by Savage and Samuelson; this series "
                          r"began with it in Part 1", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the man. <bookmark mark='a'/> On the twenty-ninth of March nineteen hundred, Louis Bachelier defended "
            "his thesis on the theory of speculation in Paris, with Henri Poincaré on the committee. "
            "<bookmark mark='b'/> It contained the random walk, the diffusion equation five years before Einstein's "
            "paper on Brownian motion, and option prices tested on French government bonds. <bookmark mark='c'/> It was "
            "forgotten for half a century, until Leonard Savage and Paul Samuelson found it. This series began there."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def timeline(self):
        I = QC.IDEA
        R = BAD
        entries = [(1900, r"Bachelier", I), (1952, r"Markowitz", I), (1965, r"Samuelson, Fama", I),
                   (1973, r"Black--Scholes--Merton", I), (1979, r"Harrison--Kreps", I), (1987, r"the crash", R),
                   (1992, r"Fama--French", I), (1998, r"LTCM", R), (2008, r"the crisis", R), (2014, r"rough volatility", I),
                   (2020, r"negative oil; the dash for cash", R), (2025, r"public pricing examples", REC_C)]
        strip = era_strip(entries, y0=1895, y1=2030, font_size=12, step=20).move_to(DOWN * 0.3)
        head = label(r"A hundred and twenty-five years", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 12)]
        with self.voiceover(
            "The whole arc. Bachelier's thesis; Markowitz's portfolios; Samuelson and Fama on efficient prices; Black, "
            "Scholes and Merton. <bookmark mark='a'/> Harrison and Kreps's measures; the crash of nineteen eighty-seven; "
            "the factors of Fama and French; LTCM. <bookmark mark='b'/> The crisis; rough volatility; negative oil and "
            "the dash for cash; and the dated public pricing examples from twenty twenty-five."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk_ in zip(groups, [None, "a", "b"]):
                if mk_:
                    vo.wait_until(mk_)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the House began as an empty building and a sealed envelope. Name one thing each of the seven acts "
                       r"added to it.")
        with self.voiceover(
            "Pause and predict. The House began as an empty building and a sealed envelope. Name one thing each of the "
            "series' seven acts added to it."
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
