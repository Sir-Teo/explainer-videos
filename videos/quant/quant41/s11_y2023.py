from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


def _t(d):
    d = np.array([int(str(x).replace("-", "")[:8]) for x in d])
    return (d // 10000) + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365


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
            "Chapter ten, and the answer to the pause. At fair value the bank has eighty-five against ninety: minus five "
            "of equity, though its books say plus ten. While depositors stay, it can hold the bonds to maturity and the "
            "loss never appears. If they leave, it must sell at eighty-five, and the loss becomes real. That is Silicon "
            "Valley Bank, and the reason the safest assets can sink a bank."
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
                cmath(r"\text{28 Sep}", r":", r"\text{the Bank of England buys long gilts, for 13 days}", font_size=36,
                      colors={r"\text{28 Sep}": SAFE_C})]
        whys = [why(r"liability-driven investment: UK pension schemes hedging long liabilities with leverage"),
                why(r"an unfunded fiscal plan; thirty-year yields rose by more than a percentage point in days, as reported"),
                why(r"Chapter 2's margin spiral, in a government bond market"),
                why(r"a temporary facility of up to \pounds 5bn a day to restore market functioning, as the Bank described it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "First, London, September twenty twenty-two. <bookmark mark='a'/> British pension schemes hedged their long "
            "liabilities with liability-driven funds: long gilts and swaps, levered with repo. <bookmark mark='b'/> A "
            "mini-budget with unfunded tax cuts sent thirty-year yields up by more than a point in days. "
            "<bookmark mark='c'/> The funds faced collateral calls, sold gilts to meet them, and pushed yields higher: the "
            "margin spiral, in government bonds. <bookmark mark='d'/> On the twenty-eighth the Bank of England bought long "
            "gilts, for thirteen days, to stop it."
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
                cmath(r"\text{equity}", r":", rf"\${s['equity']:.1f}\text{{bn}} - \${s['loss']:.1f}\text{{bn}} = "
                      rf"\${s['equity_fair']:.1f}\text{{bn}}", font_size=36, colors={r"\text{equity}": LEV_C}),
                cmath(r"\text{9 March 2023}", r":", rf"\${s['out_9mar']:.0f}\text{{bn withdrawn in a day}}", font_size=36,
                      colors={r"\text{9 March 2023}": BAD})]
        whys = [why(r"end of 2022, from its annual report; a concentrated base of technology firms and their investors"),
                why(r"bonds bought in 2020--21 at low yields, carried at cost under the accounting rules"),
                why(r"the unrealised loss, disclosed in a footnote, nearly equal to its capital"),
                why(r"and about \$100bn more requested for the next morning, as the Fed's review reported; closed on the 10th")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Silicon Valley Bank, from its annual report and the Federal Reserve's review. <bookmark mark='a'/> "
            f"{s['deposits']:.0f} billion dollars of deposits, mostly above the insured limit, from technology firms and "
            f"their investors. <bookmark mark='b'/> {s['htm_book']:.1f} billion of bonds held to maturity, carried at cost, "
            f"worth {s['htm_fair']:.1f} billion at the end of twenty twenty-two. <bookmark mark='c'/> A loss of "
            f"{s['loss']:.1f} billion, nearly all of its {s['equity']:.1f} billion of equity. <bookmark mark='d'/> When it "
            f"announced a loss on bond sales and a share issue, {s['out_9mar']:.0f} billion left in a day, more was "
            "requested for the next morning, and it was closed on the tenth."
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
        cw = curve(ax, f[w > 0], w[w > 0], SAFE_C, stroke_width=3)
        cut = DashedLine(ax.c2p(r, 0), ax.c2p(r, 1.4), color=GREY_C, stroke_width=1.5)
        leg = legend([(FUND_C, r"withdraw early"), (SAFE_C, r"wait")], font_size=17)
        eqs = VGroup(cmath(r"\text{early}", r"=", r"\min(1, r/f)", font_size=30),
                     cmath(r"\text{wait}", r"=", r"\theta\,\frac{1 - f/r}{1 - f}", font_size=30),
                     label(rf"$\theta = {th:.1f}$, $r = {r:.2f}$", font_size=18, color=GREY_B))
        side = VGroup(leg, eqs).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        d1 = Dot(ax.c2p(0, th), color=SAFE_C, radius=0.08)
        d2 = Dot(ax.c2p(1, e[-1]), color=FUND_C, radius=0.08)
        with self.voiceover(
            "Diamond and Dybvig, nineteen eighty-three, with a fire sale. The bank's assets are worth theta per unit if "
            "held, but only r if sold early. Every depositor may withdraw one now. <bookmark mark='a'/> If a share f "
            "withdraws, those who go early get one, until the bank runs out at f equal to r. <bookmark mark='b'/> Those "
            "who wait share what is left: theta times one minus f over r, over one minus f. Falling in f, and zero once "
            f"f reaches r. <bookmark mark='c'/> Two equilibria. If no one runs, waiting pays {th:.1f}, and no one should "
            "run. <bookmark mark='d'/> If everyone runs, waiting pays nothing, and everyone should. Same bank, same "
            "assets: the outcome depends only on what depositors expect of each other."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(ce), FadeIn(cut), run_time=1.5)
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
            "Which equilibrium? Carlsson and van Damme's global games answer it, as Morris and Shin, and Goldstein and "
            "Pauzner, did for runs. Give each depositor a slightly noisy signal of theta. <bookmark mark='a'/> Then there "
            "is one equilibrium: run below a threshold theta star, stay above it. At the threshold, the marginal "
            "depositor is uncertain about how many others run, uniformly so, which makes theta star the root of this "
            "integral. <bookmark mark='b'/> With r of "
            f"{q['r']:.2f}, roughly SVB's bonds, theta star is {q['thr85']:.2f}: a solvent bank with assets worth up to "
            f"{q['thr85']:.2f} still suffers a run. <bookmark mark='c'/> Insure half the deposits and it falls to "
            f"{q['thr85_half']:.2f}. <bookmark mark='d'/> And the House checked the limit: solving the game with noise "
            f"of nought point three down to nought point nought one gives thresholds of {n[0]:.2f} rising to "
            f"{n[3]:.2f}, converging to the formula."
        ) as vo:
            self.play(FadeIn(g), FadeIn(one), FadeIn(one_l), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(leg[0]), Create(lines["0.0"]), run_time=1.5)
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
            "The system's view, from FRED. <bookmark mark='a'/> The two-year Treasury yield, from "
            f"{x['y2']['start']:.2f} percent at the start of twenty twenty-two to {x['y2']['max']:.2f}: the fastest rise in "
            "forty years, and every bond bought before it marked down. <bookmark mark='b'/> And deposits at American "
            f"commercial banks, which had been falling all year, lost {drop:.0f} billion dollars in the three weeks to "
            "the twenty-second of March twenty twenty-three, as money moved to the largest banks and to money funds "
            "paying the new rates."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(l2), run_time=2)
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
            desk_question(r"and the AT1 write-off", r"about CHF 16bn of contingent bonds written to zero while shareholders "
                          r"received something, under an emergency ordinance; contested in the courts since", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The run spread, as reported. <bookmark mark='a'/> Signature Bank was closed on the twelfth of March; First "
            "Republic lost more than a hundred billion dollars of deposits and was sold to JPMorgan on the first of May. "
            "<bookmark mark='b'/> In Zurich, Credit Suisse, after years of losses and scandals, faced its own outflows, "
            "and on the nineteenth the Swiss authorities arranged its sale to UBS for three billion francs. "
            "<bookmark mark='c'/> About sixteen billion francs of its additional tier one bonds, contingent capital meant to "
            "absorb losses, were written to zero while shareholders received something, under an emergency ordinance, "
            "and contested in the courts since."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def policy(self):
        cards = VGroup(
            desk_question(r"insure the run away", r"all of SVB's and Signature's deposits were guaranteed under the "
                          r"systemic-risk exception: this chapter's insured share, set to one after the fact", width=12.4,
                          font_size=19),
            desk_question(r"lend at par", r"the Fed's Bank Term Funding Program lent against Treasuries at face value, "
                          r"not market value: r set to one, so no bank had to sell at a loss", width=12.4, font_size=19),
            desk_question(r"and outside the banks", r"LDI, money funds, the basis trade: the non-bank lenders and "
                          r"borrowers the FSB now calls NBFI, where the next run is likeliest to start", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the policy answer was the model's. <bookmark mark='a'/> Every deposit at the two failed banks was "
            "guaranteed: the insured share, set to one after the fact. <bookmark mark='b'/> The Fed's new term funding "
            "programme lent against Treasuries at face value, not market value: the fire-sale value r, set to one. "
            "<bookmark mark='c'/> And the open problem is outside the banks: the pension funds, money funds and basis "
            "traders that regulators call non-bank financial intermediation, where much of this part's stress "
            "began."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"the House runs its strategies at about two times leverage through a prime broker. If the broker "
                       r"doubles its margins on the worst day of 2008, what must the House sell, and can it?")
        with self.voiceover(
            "Pause and predict. The House runs its strategies at about two times leverage, financed by a prime broker. "
            "If the broker doubles its margins on the worst day of twenty oh eight, what must the House sell, and can it "
            "sell that much in a day?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
