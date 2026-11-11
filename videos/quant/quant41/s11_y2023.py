from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


def _t(d):
    from videos.quant.quant41.common import calendar_year
    return calendar_year(d)


class Y2023(VoiceoverScene):
    def construct(self):
        x = load("y2023")
        q = load("dd")
        self.card()
        self.gilts()
        self.svb(q)
        self.dd(q)
        self.games(q)
        self.deposits(x)
        self.cs()
        self.policy()
        self.question()

    def card(self):
        c = chapter_card(10, r"2022--23: rates, runs and a rescue", r"Can a bank holding only Treasuries fail?",
                         part=PART)
        with self.voiceover(
            'Chapter ten. In the chosen example, book equity is one hundred minus ninety, or ten. Marked equity is eighty-five minus ninety, or minus five. Holding a bond to maturity can avoid a forced sale, but does not erase its current economic value loss, opportunity cost or funding obligations. Meeting withdrawals requires cash, collateral capacity, operational access and viable funding. This toy calculation illustrates a mechanism; it is not a complete valuation or solvency determination for Silicon Valley Bank.'
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def gilts(self):
        rows = [cmath(r"\text{LDI funds}", r":", r"\text{long gilts and swaps, levered with repo}", font_size=38,
                      colors={r"\text{LDI funds}": LEV_C}),
                cmath(r"\text{23 Sep 2022}", r":", r"\text{the mini-budget; long gilt yields jump}", font_size=38,
                      colors={r"\text{23 Sep 2022}": BAD}),
                cmath(r"\text{collateral calls}", r"\Rightarrow", r"\text{sell gilts} \Rightarrow \text{yields up}", font_size=38,
                      colors={r"\text{collateral calls}": SPIRAL_C}),
                cmath(r"\text{28 Sep}", r":", r"\text{temporary gilt purchases, 28 Sep--14 Oct 2022}", font_size=36,
                      colors={r"\text{28 Sep}": SAFE_C})]
        whys = [why(r"liability-driven investment: UK pension schemes hedging long liabilities with leverage"),
                why(r"an unfunded fiscal plan; thirty-year yields rose by more than a percentage point in days, as reported"),
                why(r"Chapter 2's margin spiral, in a government bond market"),
                why('temporary market-functioning purchases over 13 business days; initial purchase limits and eligible instruments were later expanded')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "London, September twenty twenty-two. <bookmark mark='a'/> Some liability-driven investment funds used gilt and derivatives exposures with leverage to hedge pension liabilities. <bookmark mark='b'/> Gilt yields rose sharply around the September mini-budget announcement. <bookmark mark='c'/> Collateral calls and gilt sales amplified market dysfunction. <bookmark mark='d'/> The Bank of England's temporary purchases ran from September twenty-eighth through October fourteenth: thirteen business days, not thirteen calendar days. The initial daily limits and eligible instruments were expanded during the intervention; this is a historical market-functioning episode."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def svb(self, q):
        s = q["svb"]
        rows = [cmath(r"\text{deposits}", r":", rf"\${s['deposits']:.0f}\text{{bn, mostly above the insured limit}}",
                      font_size=36, colors={r"\text{deposits}": FUND_C}),
                cmath(r"\text{held-to-maturity bonds}", r":", rf"\${s['htm_book']:.1f}\text{{bn at cost}},\ "
                      rf"\${s['htm_fair']:.1f}\text{{bn at fair value}}", font_size=32,
                      colors={r"\text{held-to-maturity bonds}": PRICE_C}),
                cmath(r"\text{pretax book-equity bridge}", r":", rf"\${s['equity']:.1f}\text{{bn}} - \${s['loss']:.1f}\text{{bn}} = "
                      rf"\${s['equity_fair']:.1f}\text{{bn}}", font_size=36, colors={r"\text{pretax book-equity bridge}": LEV_C}),
                cmath(r"\text{9 March 2023}", r":", rf"\${s['out_9mar']:.0f}\text{{bn withdrawn in a day}}", font_size=36,
                      colors={r"\text{9 March 2023}": BAD})]
        whys = [why(r"end of 2022, from its annual report; a concentrated base of technology firms and their investors"),
                why(r"bonds bought in 2020--21 at low yields, carried at cost under the accounting rules"),
                why('illustrative pretax HTM fair/book gap subtracted from group book equity; taxes, other assets, AFS marks and entity differences omitted'),
                why('the Fed review reports over \\$40bn out on March 9 and management expecting over \\$100bn more March 10; the bank closed March 10')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            f"""SVB Financial Group's reported end-two-thousand-twenty-two balance sheet provides context. <bookmark mark='a'/> Deposits are {s['deposits']:.0f} billion dollars, mostly uninsured and concentrated among technology firms and investors. <bookmark mark='b'/> The unchanged illustration records {s['htm_book']:.1f} billion of held-to-maturity securities at cost and {s['htm_fair']:.1f} at fair value. <bookmark mark='c'/> Their {s['loss']:.1f}-billion pretax gap is close to {s['equity']:.1f} billion of group book equity. Simply subtracting it omits taxes, other valuations and bank-versus-group differences; it is not a regulatory or economic solvency proof. <bookmark mark='d'/> The Fed review reports over forty billion leaving March ninth, management expecting over one hundred billion more the next day, and closure on March tenth. The actual outflow and expected further outflow are different quantities."""
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def dd(self, q):
        f = np.asarray(q["f"], float)
        e = np.asarray(q["early"], float)
        w = np.asarray(q["wait"], float)
        th, r = q["theta"], q["r"]
        g = axes([0, 1], [0, 1.4], x_length=7.6, y_length=4.2, xlabel=r"share of depositors who withdraw early, $f$",
                 ylabel=r"payoff per unit deposited", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 1.0],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        ce = curve(ax, f, e, FUND_C, stroke_width=3)
        cw = curve(ax, f, w, SAFE_C, stroke_width=3)
        cut = DashedLine(ax.c2p(r, 0), ax.c2p(r, 1.4), color=GREY_C, stroke_width=1.5)
        leg = legend([(FUND_C, r"withdraw early"), (SAFE_C, r"wait")], font_size=17)
        eqs = VGroup(cmath(r"\text{early}", r"=", r"\min(1, r/f)", font_size=30),
                     cmath(r"\text{wait}", r"=", r"\begin{cases}\theta\frac{1-f/r}{1-f},&f<r\\0,&f\ge r\end{cases}", font_size=25),
                     label(rf"$\theta = {th:.1f}$, $r = {r:.2f}$", font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        side = VGroup(leg, eqs).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        d1 = Dot(ax.c2p(0, th), color=SAFE_C, radius=0.08)
        d2 = Dot(ax.c2p(1, e[-1]), color=FUND_C, radius=0.08)
        with self.voiceover(
            "A chosen run-game illustration inspired by Diamond and Dybvig, rather than their complete liquidity-type contract model. Depositors form a continuum, are risk neutral, and each may request one now. Assets pay theta later or r under early liquidation. <bookmark mark='a'/> Early withdrawal pays one while f is at most r, then r divided by f; at f zero use payoff one by convention. <bookmark mark='b'/> Waiting pays theta times one minus f over r, divided by one minus f, for f below r, and zero once f reaches r. The green line includes that zero branch. <bookmark mark='c'/> With theta above one, no-run is an equilibrium. <bookmark mark='d'/> Everyone running is also an equilibrium: an individual who waits receives zero. This illustrates coordination failure under stated payoffs, not every feature of real deposits."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side), Create(ce))
            vo.wait_until("a")
            self.play(Indicate(ce, color=HURDLE), FadeIn(cut), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cw), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(d1, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(d2, scale=1.5))
        self.wait(0.4)
        self.clear_scene()

    def games(self, q):
        rs = np.asarray(q["rs"], float)
        g = axes([0.5, 1.0], [0.8, 3.0], x_length=7.4, y_length=4.2, xlabel=r"fire-sale value of the assets, $r$",
                 ylabel=r"run threshold $\theta^*$", xticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yticks=[1, 2, 3],
                 font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        cols = {"0.0": BAD, "0.5": HURDLE, "0.9": SAFE_C}
        names = {"0.0": r"no deposits insured", "0.5": r"half insured", "0.9": r"90\% insured"}
        lines = {k: curve(ax, rs, np.asarray(v, float), cols[k], stroke_width=3) for k, v in q["thr"].items()}
        one = DashedLine(ax.c2p(0.5, 1), ax.c2p(1.0, 1), color=GREY_C, stroke_width=1.5)
        one_l = label(r"solvent: $\theta \ge 1$", font_size=16, color=GREY_B).next_to(ax.c2p(0.52, 1), DOWN, buff=0.1, aligned_edge=LEFT)
        leg = legend([(cols[k], names[k]) for k in ("0.0", "0.5", "0.9")], font_size=17)
        eq = cmath(r"\int_0^1 \big(\text{wait} - \text{early}\big)(f)\, df", r"=", r"0", font_size=28)
        side = VGroup(leg, eq).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        n = q["noisy"]
        conv = label(rf"noisy signals: $\sigma = 0.3, 0.1, 0.03, 0.01 \Rightarrow x^* = {n[0]:.2f}, {n[1]:.2f}, {n[2]:.2f}, "
                     rf"{n[3]:.2f}$", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            f"""A selected global-games limiting calculation. The payoff structure, a locally flat prior and a vanishing private-noise argument give a uniform rank belief about other depositors' withdrawals. <bookmark mark='a'/> Conditional on those assumptions, the marginal depositor's expected wait-minus-run gap is zero at the threshold. This integral alone is not a general uniqueness proof for all banking games. <bookmark mark='b'/> We choose r equal to {q['r']:.2f}, giving {q['thr85']:.2f}. This is not a calibration of SVB's securities or funding structure. <bookmark mark='c'/> If half the depositors are assumed insured and never run, the threshold becomes {q['thr85_half']:.2f}. <bookmark mark='d'/> The unchanged finite quadrature and bisection give noisy-signal thresholds from {n[0]:.2f} to {n[3]:.2f} across the chosen decreasing noise levels. Their approach to the limiting number supports this numerical illustration, not a universal equilibrium theorem."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(one), FadeIn(one_l), FadeIn(eq), Create(lines['0.0']))
            vo.wait_until("a")
            self.play(FadeIn(leg[0]), Indicate(lines['0.0'], color=HURDLE), run_time=1.5)
            vo.wait_until("b")
            self.play(Indicate(lines["0.0"], color=BAD))
            vo.wait_until("c")
            self.play(FadeIn(leg[1]), Create(lines["0.5"]), FadeIn(leg[2]), Create(lines["0.9"]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(conv))
        self.wait(0.4)
        self.clear_scene()

    def deposits(self, x):
        dp = x["dep"]
        t = _t(dp["d"])
        v = np.asarray(dp["v"], float) / 1000
        t2 = _t(x["y2"]["d"])
        v2 = np.asarray(x["y2"]["v"], float)
        g1 = axes([2022.4, 2024], [17.0, 18.3], x_length=5.6, y_length=3.6, xlabel=r"June 2022 to 2023",
                  ylabel=r"US commercial bank deposits, \$tn", xticks=[2023, 2024], yticks=[17.0, 17.5, 18.0], font_size=14)
        g2 = axes([2022, 2024], [0, 5.5], x_length=5.6, y_length=3.6, xlabel=r"2022--2023",
                  ylabel=r"two-year Treasury yield, \%", xticks=[2022, 2023, 2024], yticks=[0, 2, 4], font_size=14)
        VGroup(g2, g1).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)
        l1 = curve(g1.ax, t, v, FUND_C, stroke_width=2.5)
        l2 = curve(g2.ax, t2, v2, PRICE_C, stroke_width=2.5)
        drop = (dp["mar1"] - dp["mar22"])
        with self.voiceover(
            f"""Two descriptive FRED series. <bookmark mark='a'/> The two-year Treasury yield moves from {x['y2']['start']:.2f} to a {x['y2']['max']:.2f}-percent maximum over the selected twenty-twenty-two and twenty-twenty-three window. This two-year extract does not establish a forty-year speed record, and individual bonds differ in duration and hedging. <bookmark mark='b'/> Seasonally adjusted aggregate commercial-bank deposits fall by {drop:.0f} billion dollars between the selected weekly observations around March first and twenty-second. This is a net aggregate change. Transfers between banks alone do not lower aggregate bank deposits, and this series does not identify a decomposition into money-fund flows, within-bank shifts or other causes."""
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(l2))
            vo.wait_until("a")
            self.play(Indicate(l2, color=HURDLE), run_time=2)
            vo.wait_until("b")
            self.play(Create(l1), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def cs(self):
        cards = VGroup(
            desk_question(r"Signature and First Republic", r"Signature Bank was closed on 12 March; First Republic, after "
                          r"losing over \$100bn of deposits, was sold to JPMorgan on 1 May", width=12.4, font_size=19),
            desk_question(r"Credit Suisse, 19 March", r"years of losses and scandals, then outflows; the Swiss authorities "
                          r"arranged its sale to UBS for CHF 3bn", width=12.4, font_size=19),
            desk_question(r"and the AT1 write-off", "historical March 2023 write-down of about CHF 16bn AT1; FINMA cited the instruments' terms and emergency ordinance. No current litigation status is asserted", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Historical outcomes in March and May twenty twenty-three. <bookmark mark='a'/> Signature Bank was closed on March twelfth; First Republic was sold to JPMorgan in May after large deposit outflows. <bookmark mark='b'/> Swiss authorities arranged Credit Suisse's acquisition by UBS following sustained losses and severe liquidity pressure. <bookmark mark='c'/> FINMA's March twenty-third statement explained its AT1 write-down decision by reference to the instruments' viability-event clauses and the emergency ordinance. Shareholders receiving consideration did not make every jurisdiction's creditor hierarchy identical. This lesson does not assert a present-day litigation outcome or legal conclusion."
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

    def policy(self):
        cards = VGroup(
            desk_question(r"insure the run away", 'the historical systemic-risk exception protected all depositors at the two failed banks; it was not universal prior insurance at every bank', width=12.4,
                          font_size=19),
            desk_question(r"lend at par", 'historical BTFP: eligible par-valued collateral supported recourse loans up to one year; loan interest, eligibility and repayment obligations remained', width=12.4, font_size=19),
            desk_question(r"and outside the banks", 'LDI, money funds, the basis trade: the non-bank lenders and borrowers the FSB now calls NBFI, whose funding and liquidity links deserve separate measurement; no location forecast follows from these examples', width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Policy changed funding incentives through concrete institutions. <bookmark mark='a'/> The historical systemic-risk exception protected all depositors of SVB and Signature in resolution, not every deposit at every bank in advance. <bookmark mark='b'/> The BTFP offered eligible institutions recourse advances against eligible securities valued at par, for up to one year, at a stated interest rate. Eligibility, March-twelfth ownership and repayment still mattered. A par collateral loan creates liquidity; it does not erase economic losses or literally set every bank's liquidation payoff to one. <bookmark mark='c'/> Nonbank funds and dealers also require attention. These episodes motivate measuring their financing links, rather than forecasting where the next run must begin."
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
        q = pause_card('a proposed teaching book holds the market at two times leverage through a hypothetical prime broker. If the broker doubles its margins on the worst day of 2008, what must the House sell, and can it?')
        with self.voiceover(
            "Pause and predict. A proposed teaching book holds the market at two times leverage with a twenty-five-percent haircut. Replay the worst market day within two thousand eight and double the haircut. What fraction must be sold? If positions equal half a day's normal volume, what volume-equivalent time follows from a ten-percent participation assumption, and why is that not an execution guarantee?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
