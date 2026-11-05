from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


def _t(d):
    d = np.array([int(str(x).replace("-", "")[:8]) for x in d])
    return (d // 10000) + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365


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
            f"Chapter seven, and the answer to the pause: {t['max']:.2f} percentage points, on the tenth of October twenty "
            f"oh eight, against a median of {t['pre']:.2f} in twenty oh six. The TED spread measures what banks charge each "
            "other over a riskless rate: how far they trust one another. That autumn they nearly stopped."
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
                why(r"long assets on short wholesale funding, without deposit insurance or a lender of last resort: "
                    r"Diamond and Dybvig, at scale"),
                why(r"and protection sold on the senior tranches by firms that posted collateral only if downgraded")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The structure. <bookmark mark='a'/> Mortgages pooled into securities and sliced into tranches, Part twenty's "
            "credit models. <bookmark mark='b'/> Held by dealers, off-balance-sheet conduits and investment vehicles, and "
            "money funds: a banking system outside the banks. <bookmark mark='c'/> Funded short, by repo and commercial "
            "paper, with no deposit insurance and no lender of last resort. <bookmark mark='d'/> And insured with credit "
            "default swaps, sold by firms such as AIG that would post collateral only if downgraded."
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
            "Two spreads from FRED. <bookmark mark='a'/> The TED spread: a first jump in August twenty oh seven, when BNP "
            "Paribas froze three funds holding mortgage securities, a second around Bear Stearns, and the spike after "
            "Lehman. <bookmark mark='b'/> And the Baa corporate spread, from about "
            f"{g['baa']['pre']:.1f} to {g['baa']['max']:.1f} points: funding stress first, then credit."
        ) as vo:
            self.play(FadeIn(gr), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(l1), run_time=2.5)
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
            for k, m_ in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
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
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def mmf(self):
        rows = [cmath(r"\text{money fund}", r":", r"\$1\ \text{a share, redeemable daily}", font_size=38, colors={r"\text{money fund}": FUND_C}),
                cmath(r"\text{Reserve Primary}", r":", r"\text{Lehman paper written to zero} \Rightarrow \$0.97", font_size=36,
                      colors={r"\text{Reserve Primary}": BAD}),
                cmath(r"\text{run}", r":", r"\text{prime funds lose hundreds of billions in a week}", font_size=36)]
        whys = [why(r"a fund that promises a stable dollar: Part 39's stablecoin, in 2008"),
                why(r"the oldest US money fund held Lehman commercial paper; on 16 September it broke the buck"),
                why(r"investors pulled out of prime funds, which stopped buying commercial paper, which starved firms of "
                    r"funding; the Treasury guaranteed money funds within days")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And the run spread to cash itself. <bookmark mark='a'/> A money market fund promises a stable dollar a share, "
            "redeemable daily: Part thirty-nine's stablecoin, in twenty oh eight. <bookmark mark='b'/> The Reserve Primary "
            "Fund held Lehman commercial paper, wrote it to zero, and broke the buck. <bookmark mark='c'/> Investors pulled "
            "hundreds of billions from prime funds within a week, the funds stopped buying commercial paper, and companies "
            "lost their funding, until the Treasury guaranteed money funds."
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
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
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
        self.wait(0.5)
        self.clear_scene()
