from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


def _t(d):
    from videos.quant.quant41.common import calendar_year
    return calendar_year(d)


class GFC(VoiceoverScene):
    def construct(self):
        g = load("gfc")
        self.card(g)
        self.shadow()
        self.ted(g)
        self.timeline()
        self.lehman_aig()
        self.mmf()
        self.response()
        self.question()

    def card(self, g):
        t = g["ted"]
        c = chapter_card(7, r"2007--08: the run on the shadow banks", r"How did a mortgage problem become a run on the "
                         r"financial system?", part=PART)
        with self.voiceover(
            f"""Chapter seven. The TED spread reaches {t['max']:.2f} percentage points on {t['max_day']}, compared with a roughly {t['pre']:.2f} median over the first two hundred fifty observations. It is three-month dollar LIBOR minus the Treasury-bill yield. Bank credit risk, term funding liquidity and demand for Treasury safety all affect it. Calling it pure trust or a default probability would discard those components."""
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def shadow(self):
        rows = [cmath(r"\text{mortgages}", r"\to", r"\text{securities} \to \text{tranches}", font_size=40, colors={r"\text{mortgages}": PRICE_C}),
                cmath(r"\text{held by}", r":", r"\text{dealers, conduits, SIVs, money funds}", font_size=36),
                cmath(r"\text{funded by}", r":", r"\text{repo and commercial paper, overnight to weeks}", font_size=36,
                      colors={r"\text{funded by}": FUND_C}),
                cmath(r"\text{insured by}", r":", r"\text{credit default swaps, AIG among the sellers}", font_size=34,
                      colors={r"\text{insured by}": SPIRAL_C})]
        whys = [why(r"loans pooled and sliced, Part 20's tranches priced with Part 40's Gaussian copula"),
                why(r"much of it outside deposit-taking banks: the shadow banking system"),
                why('short wholesale funding without ordinary insured-deposit protection; bank backstops and emergency-facility access differed across entities'),
                why('AIG financial-products collateral depended on contract terms, including valuation changes and rating triggers')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A stylized funding chain. <bookmark mark='a'/> Mortgages were pooled and sliced into different-risk securities and tranches. <bookmark mark='b'/> Dealers, conduits, investment vehicles and funds held different instruments; money funds often supplied short funding rather than holding the same mortgage assets directly. <bookmark mark='c'/> Repo and commercial paper financed longer assets. Ordinary deposit insurance did not cover these wholesale claims, although bank backstops and eventual emergency support varied. <bookmark mark='d'/> Credit derivatives transferred some credit risk. AIG's collateral calls could follow market-value changes as well as rating downgrades, under the contracts' terms."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def ted(self, g):
        t = _t(g["ted"]["d"])
        v = np.asarray(g["ted"]["v"], float)
        t2 = _t(g["baa"]["d"])
        v2 = np.asarray(g["baa"]["v"], float)
        gr = axes([2006, 2011], [0, 6.5], x_length=7.6, y_length=4.2, xlabel=r"2006--2010",
                  ylabel=r"percentage points", xticks=[2006, 2007, 2008, 2009, 2010, 2011], yticks=[0, 2, 4, 6],
                  font_size=15).move_to(LEFT * 0.8 + DOWN * 0.2)
        ax = gr.ax
        l1 = curve(ax, t, v, FUND_C, stroke_width=2.5)
        l2 = curve(ax, t2, v2, SPIRAL_C, stroke_width=2.5)
        leg = legend([(FUND_C, r"TED spread"), (SPIRAL_C, r"Baa over 10-year Treasury")], font_size=17).to_corner(UR, buff=0.5)
        with self.voiceover(
            f"""Two FRED yield differences. <bookmark mark='a'/> TED rose during several funding-stress episodes, including August two thousand seven and the period after Lehman's failure. Its components include bank credit and liquidity risk and Treasury-bill safe-haven demand. <bookmark mark='b'/> Baa yields minus the ten-year Treasury move from a roughly {g['baa']['pre']:.1f}-point early median to a {g['baa']['max']:.1f}-point peak. That difference also contains liquidity and maturity effects; it is not a matched-maturity credit-default-swap spread. Two plotted series do not identify a causal sequence from funding to credit losses."""
        ) as vo:
            self.play(FadeIn(gr), FadeIn(leg[0]), Create(l1))
            vo.wait_until("a")
            self.play(Indicate(l1, color=HURDLE), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), Create(l2), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def timeline(self):
        events = [(r"Aug 2007", r"BNP Paribas freezes three funds; interbank rates jump", FUND_C),
                  (r"Mar 2008", r"Bear Stearns, unable to roll its repo, is sold to JPMorgan with Fed support", SPIRAL_C),
                  (r"Sep 2008", r"Fannie Mae and Freddie Mac taken over; Lehman files on the 15th", BAD),
                  (r"16 Sep", r"AIG's collateral calls: an \$85bn Fed loan; a money fund breaks the buck", BAD),
                  (r"Oct 2008", r"TARP; capital injections; guarantees of bank debt", SAFE_C)]
        rows = VGroup(*[VGroup(label(d_, font_size=20, color=c_), label(w_, font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.4)
                        for d_, w_, c_ in events]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(ORIGIN)
        with self.voiceover(
            "The sequence, from the public record. <bookmark mark='a'/> August twenty oh seven: BNP Paribas freezes three "
            "funds, and interbank rates jump. <bookmark mark='b'/> March twenty oh eight: Bear Stearns cannot roll its "
            "repo and is sold to JPMorgan with Federal Reserve support. <bookmark mark='c'/> September: the government "
            "takes over Fannie Mae and Freddie Mac, and Lehman files for bankruptcy on the fifteenth. "
            "<bookmark mark='d'/> The next day, AIG's collateral calls bring an eighty-five billion dollar Fed loan, and a "
            "money market fund breaks the buck. <bookmark mark='e'/> In October, public capital and guarantees."
        ) as vo:
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            for k, m_ in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
                else:
                    self.play(Indicate(rows[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def lehman_aig(self):
        cards = VGroup(
            desk_question(r"Lehman: a run on repo", r"at about 31 times, with much of its funding overnight, Lehman lost "
                          r"its lenders over a weekend; its failure froze its prime-brokerage clients' assets in London, as "
                          r"reported", width=12.4, font_size=19),
            desk_question(r"AIG: a margin spiral", r"it had sold protection on hundreds of billions of senior tranches; "
                          r"downgrades and falling prices triggered collateral calls it could not meet, as McDonald and "
                          r"Paulson describe", width=12.4, font_size=19),
            desk_question(r"both were Chapter 1's arithmetic", r"a small fall in asset values against thin equity, and "
                          r"lenders who demanded more collateral exactly when it was scarcest", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Two failures, two mechanisms. <bookmark mark='a'/> Lehman, at about thirty-one times, with much of its "
            "funding overnight, lost its lenders over a weekend, and its failure froze its prime-brokerage clients' "
            "assets in London, as reported. <bookmark mark='b'/> AIG had sold protection on hundreds of billions of senior "
            "tranches; downgrades and falling prices triggered collateral calls it could not meet. "
            "<bookmark mark='c'/> Both were Chapter one's arithmetic: thin equity, and lenders demanding more exactly when "
            "it was scarcest."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def mmf(self):
        rows = [cmath(r"\text{money fund}", r":", r"\$1\ \text{a share, redeemable daily}", font_size=38, colors={r"\text{money fund}": FUND_C}),
                cmath(r"\text{Reserve Primary}", r":", '\\text{losses on Lehman exposure} \\Rightarrow \\$0.97', font_size=36,
                      colors={r"\text{Reserve Primary}": BAD}),
                cmath(r"\text{run}", r":", r"\text{prime funds lose hundreds of billions in a week}", font_size=36)]
        whys = [why('a stable-NAV target under the applicable accounting rules, not an FDIC-insured deposit or an unconditional one-dollar guarantee'),
                why(r"the oldest US money fund held Lehman commercial paper; on 16 September it broke the buck"),
                why(r"investors pulled out of prime funds, which stopped buying commercial paper, which starved firms of "
                    r"funding; the Treasury guaranteed money funds within days")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Runs can also reach cash-management funds. <bookmark mark='a'/> Many money market funds sought a stable one-dollar net asset value with daily redemption; that target was not an insured bank-deposit promise. <bookmark mark='b'/> The Reserve Primary Fund's Lehman exposure contributed to its breaking the buck in September two thousand eight. <bookmark mark='c'/> Large redemptions from prime funds impaired commercial-paper funding. The Treasury's temporary guarantee and Federal Reserve liquidity programs were separate emergency interventions, rather than proof that fund shares had always been insured."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def response(self):
        cards = VGroup(
            desk_question(r"lender, then buyer of last resort", r"the Fed's facilities lent to dealers, money funds and "
                          r"commercial-paper issuers, then bought mortgage securities outright", width=12.4, font_size=19),
            desk_question(r"capital", r"public capital in the banks, and from 2009 stress tests that told markets how "
                          r"much each needed (Part 40)", width=12.4, font_size=19),
            desk_question(r"the rules that followed", r"Basel III's capital and liquidity ratios, central clearing of swaps "
                          r"(Part 21), resolution plans, and G-SIB surcharges (Chapter 5)", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The response. <bookmark mark='a'/> The Fed lent to dealers, money funds and commercial-paper issuers, then "
            "bought mortgage securities outright: lender, then buyer, of last resort. <bookmark mark='b'/> Governments put "
            "capital into the banks, and from twenty oh nine stress tests told markets how much each needed. "
            "<bookmark mark='c'/> And the rules that followed: Basel three's capital and liquidity ratios, central clearing, "
            "resolution plans and surcharges for the systemic banks."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"between 9 and 18 March 2020 US stocks fell sharply. What happened to the yield of the ten-year "
                       r"Treasury, the world's safest asset, and why?")
        with self.voiceover(
            "Pause and predict. Between the ninth and the eighteenth of March twenty twenty, American stocks fell sharply. "
            "What happened to the yield of the ten-year Treasury, the world's safest asset, and why?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
