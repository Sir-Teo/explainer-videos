from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import (BAD, GOOD, HURDLE, LEV_C, NET_C, PART, PRICE_C, SPIRAL_C, load)


class FireSales(VoiceoverScene):
    def construct(self):
        f = load("firesale")
        self.card(f)
        self.shleifer()
        self.glt_model()
        self.banks(f)
        self.rounds(f)
        self.vulnerable(f)
        self.coval()
        self.overlap()
        self.question()

    def card(self, f):
        E = sum(f["E"])
        first, second = -sum(f["first"]), -sum(f["second"])
        c = chapter_card(3, r"Fire sales", r"How does one bank's selling become another bank's loss?", part=PART)
        with self.voiceover(
            f"Chapter three, and the answer to the pause: comparable. The first loss costs the five banks "
            f"{100 * first / E:.0f} percent of their equity; the fire sales it forces cost another {100 * second / E:.0f} "
            "percent. And for the banks that held few mortgage securities, the fire-sale loss is larger than the one the "
            "news itself caused them. The loss travelled through prices, not through any contract between them."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def shleifer(self):
        cards = VGroup(
            desk_question(r"the natural buyers are in trouble too", r"Shleifer and Vishny (1992): when an industry's "
                          r"assets must be sold, the buyers who value them most are its own firms, hit by the same shock",
                          width=12.4, font_size=19),
            desk_question(r"so the price falls below value", r"outsiders buy only at a discount: a fire-sale price, "
                          r"below what the asset would fetch in normal times", width=12.4, font_size=19),
            desk_question(r"and the discount is contagious", r"every holder marks the asset at the fire-sale price, so the "
                          r"sale of one hurts all; 2011's ``Fire sales in finance and macroeconomics'' made it general",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Andrei Shleifer and Robert Vishny's insight. <bookmark mark='a'/> When an industry's assets must be sold, the "
            "buyers who value them most are the industry's own firms, hit by the same shock. <bookmark mark='b'/> So "
            "outsiders buy only at a discount: a fire-sale price, below the asset's value in normal times. "
            "<bookmark mark='c'/> And because every holder marks the asset at that price, one firm's sale is every firm's "
            "loss."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def glt_model(self):
        rows = [cmath(r"\text{first round}", r":", r"x_i = \textstyle\sum_k M_{ik} F_k", font_size=38, colors={r"\text{first round}": SPIRAL_C}),
                cmath(r"\text{sales}", r":", r"s_i = -\lambda_i\,x_i", font_size=40, colors={r"\text{sales}": LEV_C}),
                cmath(r"\text{price impact}", r":", r"\Delta P_k = -L_k \textstyle\sum_i s_i\,M_{ik}/A_i", font_size=36,
                      colors={r"\text{price impact}": PRICE_C}),
                cmath(r"\text{second round}", r":", r"y_i = \textstyle\sum_k M_{ik}(1 + F_k)\,\Delta P_k", font_size=36,
                      colors={r"\text{second round}": BAD})]
        whys = [why(r"Greenwood, Landier and Thesmar (2015): bank $i$ holds $M_{ik}$ dollars of asset $k$; a shock $F$ "
                    r"costs it $x_i$"),
                why(r"banks target their leverage $\lambda_i$, so a loss of $x$ forces sales of $\lambda x$, spread over "
                    r"their holdings"),
                why(r"the sales move each asset's price in proportion to the dollars sold, with illiquid assets moving most"),
                why(r"and every bank holding those assets loses again, whether or not it sold anything")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Robin Greenwood, Augustin Landier and David Thesmar made it a model. <bookmark mark='a'/> A shock to asset "
            "returns costs each bank in proportion to its holdings. <bookmark mark='b'/> Banks that target their leverage "
            "must sell leverage times that loss. <bookmark mark='c'/> The sales move prices, the illiquid assets most. "
            "<bookmark mark='d'/> And every bank holding those assets loses again, whether or not it sold."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def banks(self, f):
        hx = [-4.4, -2.2, -0.2, 1.8, 3.8, 5.6]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"bank", r"mortgage sec.", r"loans",
                                                                         r"gov.\ bonds", r"leverage", r"equity, \$bn")])
        tab = VGroup(head)
        for i, nm in enumerate(f["names"]):
            m = f["M"][i]
            tab.add(VGroup(label(nm, font_size=20), *[MathTex(f"{x:.0f}", font_size=24) for x in m],
                           MathTex(rf"{f['lev'][i]:.0f}\times", font_size=24, color=LEV_C),
                           MathTex(f"{f['E'][i]:.1f}", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.72 * j, 0])
        foot = wrapped_label(r"five stylised banks, holdings in \$bn; the price impact of selling \$1bn is 0.5 bp for "
                             r"mortgage securities, 0.25 bp for loans and 0.05 bp for government bonds", 11.4, 16,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Five stylised banks. <bookmark mark='a'/> Each holds mortgage securities, loans and government bonds in "
            "different proportions, at leverage from fifteen to thirty. <bookmark mark='b'/> Bank D is the most levered "
            "and the most exposed to mortgages; bank C holds mostly government bonds. Mortgage securities are the "
            "illiquid asset: selling them moves their price ten times more than selling bonds."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Indicate(tab[4], color=BAD), Indicate(tab[3], color=GOOD))
        self.wait(0.4)
        self.clear_scene()

    def rounds(self, f):
        hx = [-3.8, -1.4, 1.0, 3.4, 5.4]
        head = VGroup(*[label(t, font_size=15, color=GREY_B) for t in (r"bank", r"first loss", r"sales", r"fire-sale loss",
                                                                         r"of equity")])
        tab = VGroup(head)
        for i, nm in enumerate(f["names"]):
            tab.add(VGroup(label(nm, font_size=20), MathTex(f"{-f['first'][i]:.1f}", font_size=24, color=SPIRAL_C),
                           MathTex(f"{f['sales'][i]:.0f}", font_size=24, color=LEV_C),
                           MathTex(f"{-f['second'][i]:.1f}", font_size=24, color=BAD),
                           MathTex(rf"{100 * f['IV'][i]:.0f}\%", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.2 - 0.72 * j, 0])
        e_i = f["names"].index("E")
        total = sum(f["sales"])
        with self.voiceover(
            "A five percent fall in mortgage securities. <bookmark mark='a'/> The first losses, in billions, follow the "
            "mortgage holdings. <bookmark mark='b'/> To restore leverage the banks sell fifteen to thirty times those "
            f"losses: {total:,.0f} billion in all. <bookmark mark='c'/> The sales push prices down further, and "
            f"every bank loses again. Bank E lost {-f['first'][e_i]:.1f} billion to the news and "
            f"{-f['second'][e_i]:.1f} to the others' selling."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_[2]) for r_ in tab[1:]], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[3], r_[4])) for r_ in tab[1:]], lag_ratio=0.15))
        self.wait(0.4)
        self.clear_scene()

    def vulnerable(self, f):
        rows = [cmath(r"\text{AV}", r"=", r"\frac{-\sum_i y_i}{\sum_i E_i}", font_size=44, colors={r"\text{AV}": BAD}),
                cmath(r"\text{this system}", r":", rf"{100 * f['AV']:.0f}\%\ \text{{of equity}}", font_size=40),
                cmath(r"\text{impact doubled}", r":", rf"{100 * f['AV_double']:.0f}\%", font_size=40, colors={r"\text{impact doubled}": SPIRAL_C})]
        whys = [why(r"aggregate vulnerability: the fire-sale loss as a share of the system's equity"),
                why(r"here larger than a quarter of all equity, from a 5\% move in one asset"),
                why(r"with the illiquid asset twice as hard to sell, half the system's equity; Greenwood, Landier and "
                    r"Thesmar applied it to the EBA's 2011 bank holdings of sovereign debt")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "One number for the system. <bookmark mark='a'/> Aggregate vulnerability: the fire-sale loss as a share of "
            f"all the banks' equity. <bookmark mark='b'/> Here {100 * f['AV']:.0f} percent, from a five percent move in one "
            f"asset. <bookmark mark='c'/> If that asset were twice as hard to sell, {100 * f['AV_double']:.0f} percent. "
            "Greenwood, Landier and Thesmar applied it to European banks' sovereign holdings in twenty eleven."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def coval(self):
        cards = VGroup(
            desk_question(r"funds sell what they own", r"Coval and Stafford (2007): mutual funds facing outflows sell "
                          r"their existing holdings, and those stocks fall, then recover over months: a measurable fire-sale "
                          r"discount", width=12.4, font_size=19),
            desk_question(r"the recovery is the evidence", r"a price that comes back was not information: it was "
                          r"liquidity, paid for by the forced seller and earned by whoever bought", width=12.4, font_size=19),
            desk_question(r"and it repeats", r"Part 38's bond ETFs in March 2020, Part 21's Archegos block sales: forced "
                          r"sellers at a discount, patient buyers at a premium", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In the data. <bookmark mark='a'/> Joshua Coval and Erik Stafford found that mutual funds facing outflows sell "
            "the stocks they already own, and those stocks fall, then recover over the following months. "
            "<bookmark mark='b'/> The recovery is the evidence: a price that comes back was not information but "
            "liquidity, paid for by the forced seller. <bookmark mark='c'/> And it repeats: Part thirty-eight's bond funds "
            "in March twenty twenty, Part twenty-one's Archegos block sales."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def overlap(self):
        cards = VGroup(
            desk_question(r"common holdings are a network", r"two banks that never lend to each other are linked if they "
                          r"own the same assets: Cont and Schaanning's price-mediated contagion", width=12.4, font_size=19),
            desk_question(r"diversification can concentrate", r"if every bank diversifies into the same assets, each is "
                          r"safer alone and the system is more exposed to one fire sale", width=12.4, font_size=19),
            desk_question(r"stress tests must include it", r"a bank's own stress test misses the others' sales; system "
                          r"stress tests add the second round", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The broader lesson. <bookmark mark='a'/> Common holdings are a network: two banks that never lend to each "
            "other are linked if they own the same assets, which Rama Cont and Eric Schaanning call price-mediated "
            "contagion. <bookmark mark='b'/> So diversification can concentrate: if every bank diversifies into the same "
            "assets, each is safer alone and all are exposed to one fire sale. <bookmark mark='c'/> A bank's own stress "
            "test misses the others' sales; a system's must include them."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"ten banks each owe the others \$6 in total and have a buffer of \$0.5. Bank 1 loses money. Is the "
                       r"system safer if each bank owes all nine others a little, or only its neighbour?")
        with self.voiceover(
            "Pause and predict. Ten banks each owe the others six dollars in total and have a buffer of half a dollar. "
            "Bank one suffers a loss. Is the system safer if each bank owes all nine others a little, or owes only its "
            "neighbour?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
