from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import (
    BAD,
    GOOD,
    HURDLE,
    PART,
    STABLE_C,
    fit_right,
    load,
)


class Stable(VoiceoverScene):
    def construct(self):
        s = load("stable")
        self.card(s)
        self.kinds()
        self.dd()
        self.dd_table(s)
        self.usdc(s)
        self.usdc_read(s)
        self.peg_arb()
        self.terra_mech()
        self.terra_chart(s)
        self.terra_lessons()
        self.rules()
        self.question()

    def card(self, s):
        c = chapter_card(8, r"Stablecoins and runs", r"What is a token that promises a dollar, and when does the promise "
                         r"break?", part=PART)
        with self.voiceover(
            "Chapter eight, and the answer to the pause: yes, a run, on an issuer whose reserves were briefly in doubt. "
            "And a holder who waited three days received a dollar again, because American authorities guaranteed the "
            "failed bank's deposits. A stablecoin is a bank, and it can be run on like one."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def kinds(self):
        cards = VGroup(
            desk_question(r"backed by dollars", r"tether, USD Coin: the issuer holds bank deposits, Treasury bills and repo, "
                          r"and redeems tokens for dollars, for approved customers", width=12.4, font_size=19),
            desk_question(r"backed by crypto", r"DAI: loans against more than their value in other tokens, liquidated "
                          r"automatically when collateral falls", width=12.4, font_size=19),
            desk_question(r"backed by its own twin", r"Terra's UST: redeemable for a dollar's worth of a second token, LUNA, "
                          r"that the protocol itself printed", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three kinds. <bookmark mark='a'/> Backed by dollars, like tether and USD coin: the issuer holds deposits, "
            "bills and repo, and redeems tokens for approved customers. <bookmark mark='b'/> Backed by crypto, like DAI: "
            "loans against more than their value in other tokens, liquidated automatically when collateral falls. "
            "<bookmark mark='c'/> And backed by a twin: Terra's UST, redeemable for a dollar's worth of a second token "
            "that the protocol itself printed."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def dd(self):
        rows = [cmath(r"\text{liabilities}", r":", r"\text{redeemable at } \$1 \text{ on demand}", font_size=36),
                cmath(r"\text{assets}", r":", r"\text{a share } \ell \text{ liquid, the rest sold at a discount } d",
                      font_size=34),
                cmath(r"\text{all redeem}", r"\Rightarrow", r"\ell + (1 - \ell)(1 - d) < 1", font_size=38,
                      colors={r"\ell + (1 - \ell)(1 - d) < 1": BAD}),
                cmath(r"\text{first come, first served}", r"\Rightarrow", r"\text{a run is an equilibrium}", font_size=34)]
        whys = [why(r"Diamond and Dybvig (1983): a bank promises liquidity it does not hold"),
                why(r"reserves in bills and deposits are liquid in normal times and can be sold only at a loss in a hurry"),
                why(r"if everyone redeems at once, the assets fall short of the promises"),
                why(r"so if others redeem, it pays to redeem first; a run can happen even when the issuer is solvent at "
                    r"leisure")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Douglas Diamond and Philip Dybvig's bank, on chain. <bookmark mark='a'/> Liabilities redeemable at a dollar "
            "on demand. <bookmark mark='b'/> Assets of which a share is liquid, and the rest can be sold in a hurry only "
            "at a discount. <bookmark mark='c'/> If everyone redeems at once, the assets fall short. "
            "<bookmark mark='d'/> And with first-come, first-served redemption, if others run it pays to run first, so "
            "a run is an equilibrium even for an issuer that is solvent at leisure."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def dd_table(self, s):
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"liquid share $\ell$", r"fire-sale discount $d$",
                                                                         r"assets per \$1, if all redeem")])
        tab = VGroup(head)
        for r in s["dd"]:
            v = r["full_run"]
            tab.add(VGroup(MathTex(f"{r['liquid']:.0%}".replace("%", r"\%"), font_size=26),
                           MathTex(f"{r['disc']:.0%}".replace("%", r"\%"), font_size=26),
                           MathTex(f"{v:.2f}", font_size=26, color=GOOD if v >= 0.999 else BAD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.8 - 0.6 * j, 0])
        with self.voiceover(
            "In numbers. <bookmark mark='a'/> With all reserves liquid, there is nothing to run for: a dollar for a "
            "dollar. <bookmark mark='b'/> With a fifth illiquid and a twenty percent fire-sale discount, a full run "
            "leaves ninety-six cents per dollar, enough to make running the safe choice. Any illiquidity at all makes a "
            "run possible; how much it costs depends on the discount."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[3:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def usdc(self, s):
        u = s["usdc"]
        t = (np.asarray(u["t"], float) - u["t0"]) / 3600
        p = np.asarray(u["p"], float)
        keep = t <= 168
        t, p = t[keep], p[keep]
        g = axes([0, 168], [0.86, 1.01], x_length=7.6, y_length=4.0, xlabel=r"hours from 14:00 UTC, 11 March 2023",
                 ylabel=r"USDC in tether, Binance", xticks=[0, 24, 48, 72, 96, 120, 144, 168],
                 yticks=[0.88, 0.92, 0.96, 1.0], font_size=15).move_to(LEFT * 1.0 + DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, p, STABLE_C, stroke_width=2.5)
        par = DashedLine(ax.c2p(0, 1.0), ax.c2p(168, 1.0), color=GREY_C)
        notes = VGroup(label(r"10 Mar: Silicon Valley Bank fails", font_size=17, color=GREY_A),
                       label(r"Circle: \$3.3bn of reserves there, as it disclosed", font_size=17, color=BAD),
                       label(r"12 Mar, evening: deposits guaranteed", font_size=17, color=GOOD))
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.2)
        fit_right(notes)
        with self.voiceover(
            "USD coin in March twenty twenty-three, minute by minute. <bookmark mark='a'/> Silicon Valley Bank failed on "
            "Friday the tenth; Circle, the issuer, disclosed that three point three billion dollars of its reserves were "
            "there. Binance's series of the coin against tether opens on Saturday afternoon at "
            f"{u['low']:.3f}. <bookmark mark='b'/> It spent {u['min_below98'] / 60:.0f} hours below ninety-eight cents. "
            "<bookmark mark='c'/> On Sunday evening, American authorities guaranteed all of the bank's deposits, and by "
            f"{u['hours_to_995']:.0f} hours after the low the coin was back above ninety-nine and a half cents."
        ) as vo:
            self.play(FadeIn(g), Create(par))
            vo.wait_until("a")
            self.play(FadeIn(notes[:2]))
            self.play(Create(line), run_time=3)
            vo.wait_until("b")
            self.wait(0.1)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def usdc_read(self, s):
        u = s["usdc"]
        rows = [cmath(r"\frac{3.3}{\approx 40}", r"\approx", r"8\%\ \text{of reserves at the bank}", font_size=38),
                cmath(r"\text{zero recovery}", r"\Rightarrow", r"\approx 0.92", font_size=38),
                cmath(r"\text{traded at}", r":", rf"{u['low']:.2f}", font_size=40, colors={rf"{u['low']:.2f}": BAD})]
        whys = [why(r"about \$40bn of USDC outstanding, as reported at the time"),
                why(r"even if nothing at the bank were recovered, the remaining reserves covered about 92 cents"),
                why(r"the market priced more than the exposure: redemptions needed banks that were shut for the weekend, so "
                    r"a holder who needed dollars now had only the market")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Read the price. <bookmark mark='a'/> About eight percent of the reserves were at the failed bank. "
            "<bookmark mark='b'/> Even with nothing recovered, the rest covered about ninety-two cents. "
            f"<bookmark mark='c'/> Yet it traded at {u['low']:.2f}: below even the worst case, because redemptions ran "
            "through banks that were shut for the weekend, and a holder who needed dollars at once had only the market. "
            "Liquidity, not solvency, set the price."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def peg_arb(self):
        rows = [cmath(r"P < 1", r":", r"\text{buy tokens, redeem for } \$1", font_size=38, colors={r"P < 1": BAD}),
                cmath(r"P > 1", r":", r"\text{deposit } \$1,\ \text{mint, sell}", font_size=38, colors={r"P > 1": GOOD}),
                cmath(r"\text{who can}", r":", r"\text{approved customers, in banking hours}", font_size=36,
                      colors={r"\text{who can}": HURDLE})]
        whys = [why(r"the peg is held by arbitrage against the issuer's own redemption window, like an ETF's creation and "
                    r"redemption in Part 38"),
                why(r"and above par by creation"),
                why(r"Lyons and Viswanath-Natraj: the arbitrage works only as well as access to it; when the window shuts, "
                    r"the band widens")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "What normally holds the peg is Part thirty-eight's ETF arbitrage. <bookmark mark='a'/> Below a dollar, buy "
            "tokens and redeem them with the issuer. <bookmark mark='b'/> Above, deposit dollars, mint and sell. "
            "<bookmark mark='c'/> But only approved customers can, and only when banks are open; as Richard Lyons and "
            "Ganesh Viswanath-Natraj showed, the peg is only as tight as access to that window."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def terra_mech(self):
        rows = [cmath(r"1\ \text{UST}", r"\leftrightarrow", r"\$1\ \text{of newly minted LUNA}", font_size=38,
                      colors={r"1\ \text{UST}": STABLE_C}),
                cmath(r"\text{UST} < \$1", r"\Rightarrow", r"\text{burn UST, mint LUNA, sell LUNA}", font_size=34),
                cmath(r"\text{more LUNA}", r"\Rightarrow", r"\text{lower LUNA price}", font_size=36),
                cmath(r"\text{lower LUNA}", r"\Rightarrow", r"\text{more LUNA per UST redeemed}", font_size=34,
                      colors={r"\text{more LUNA per UST redeemed}": BAD})]
        whys = [why(r"the protocol always swaps one UST for a dollar's worth of LUNA, at an oracle price"),
                why(r"so arbitrageurs defend the peg by redeeming UST and selling the LUNA they receive"),
                why(r"which floods the market with LUNA"),
                why(r"and each further redemption mints more LUNA: the defence feeds on itself. Demand was supported by "
                    r"Anchor, a lending protocol paying close to 20\% on UST deposits, as reported")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Terra, in May twenty twenty-two. <bookmark mark='a'/> The protocol swapped one UST for a dollar's worth of "
            "newly minted LUNA, its twin. <bookmark mark='b'/> Below a dollar, arbitrageurs burn UST, receive LUNA, and "
            "sell it. <bookmark mark='c'/> That floods the market with LUNA and pushes its price down, "
            "<bookmark mark='d'/> so each further redemption mints even more LUNA. The defence feeds on itself. Demand for "
            "UST rested largely on a lending protocol, Anchor, that paid close to twenty percent on deposits, as reported."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def terra_chart(self, s):
        ut, lu = s["USTUSDT"], s["LUNAUSDT"]
        t0 = float(ut["t"][0])
        tu = (np.asarray(ut["t"], float) - t0) / 86400
        tl = (np.asarray(lu["t"], float) - t0) / 86400
        g = axes([0, 13], [-5, 2.2], x_length=7.6, y_length=4.2, xlabel=r"May 2022, days",
                 ylabel=r"price, dollars (log scale)", xticks=[0, 4, 8, 12], yticks=[-4, -2, 0, 2],
                 xfmt=lambda v: f"{int(v) + 1}", yfmt=lambda v: f"10^{{{int(v)}}}", font_size=15)
        g.move_to(LEFT * 1.2 + DOWN * 0.2)
        ax = g.ax
        cu = curve(ax, tu, np.log10(np.asarray(ut["p"], float)), STABLE_C, stroke_width=2.5)
        cl = curve(ax, tl, np.log10(np.maximum(np.asarray(lu["p"], float), 1e-5)), BAD, stroke_width=2.5)
        leg = legend([(STABLE_C, rf"UST: {ut['first']:.2f} to {ut['low']:.2f}"),
                      (BAD, rf"LUNA: \${lu['first']:.0f} to \${lu['low']:.5f}")], font_size=18)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 2.0)
        fit_right(leg)
        with self.voiceover(
            "On Binance, hour by hour. <bookmark mark='a'/> UST began the month at a dollar and lost the peg on the "
            f"ninth; by the time trading stopped it was near {ut['last']:.2f}. <bookmark mark='b'/> LUNA, at about "
            f"{lu['first']:.0f} dollars on the first, fell by more than six orders of magnitude in a week, as the "
            "redemptions printed it by the trillion. Tens of billions of dollars of market value were gone, as reported."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg[0]), Create(cu), run_time=2)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(FadeIn(leg[1]), Create(cl), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def terra_lessons(self):
        cards = VGroup(
            desk_question(r"no outside asset", r"a coin backed by a token its own system prints is backed by confidence in "
                          r"that system; when confidence goes, both go", width=12.4, font_size=19),
            desk_question(r"contagion", r"lenders exposed to Terra and to each other failed through June and July 2022, as "
                          r"reported, and FTX followed in November: Part 41's spiral", width=12.4, font_size=19),
            desk_question(r"the law", r"Terraform Labs and its founder were found liable for fraud by an American jury in "
                          r"2024, and the founder later pleaded guilty in a criminal case, as reported", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> A coin backed by a token its own system prints is backed by confidence, "
            "and when confidence goes, both go together. <bookmark mark='b'/> Contagion: lenders exposed to Terra and to "
            "each other failed through the summer, as reported, and FTX followed in November, Part forty-one's spiral in "
            "miniature. <bookmark mark='c'/> And the law: Terraform Labs and its founder were found liable for fraud by "
            "an American jury in twenty twenty-four, and the founder later pleaded guilty in a criminal case, as "
            "reported."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        cards = VGroup(
            desk_question(r"Europe", r"the MiCA regulation's stablecoin rules applied from mid-2024: authorised issuers, "
                          r"reserves held with banks, redemption at par", width=12.4, font_size=19),
            desk_question(r"the United States", r"the GENIUS Act of July 2025 set federal rules for payment "
                          r"stablecoins: one-to-one reserves in cash and short Treasury bills, and regular disclosure",
                          width=12.4, font_size=19),
            desk_question(r"what rules cannot do", r"a reserve of bills is safe but not instantly cash; a run on a "
                          r"weekend still meets closed banks", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the rules that followed. <bookmark mark='a'/> In Europe, the MiCA regulation's stablecoin rules applied "
            "from mid twenty twenty-four. <bookmark mark='b'/> In the United States, the GENIUS Act of July twenty "
            "twenty-five required one-to-one reserves in cash and short Treasury bills, with regular disclosure. "
            "<bookmark mark='c'/> But a reserve of bills is safe, not instantly cash, and a run on a weekend still meets "
            "closed banks."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"in early 2018 Bitcoin cost tens of percent more in South Korea than in the United States, for "
                       r"weeks. Why did arbitrageurs not close the gap?")
        with self.voiceover(
            "Pause and predict. In early twenty eighteen, Bitcoin cost tens of percent more in South Korea than in the "
            "United States, for weeks. Why did arbitrageurs not close the gap?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
