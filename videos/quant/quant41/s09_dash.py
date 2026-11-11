from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant41.common import ladder
from videos.quant.quant41.common import (BAD, FUND_C, GOOD, HURDLE, LEV_C, PART, PRICE_C, SAFE_C, SPIRAL_C, load)


def _t(d):
    from datetime import date
    base=date(2020, 2, 1)
    dates=[str(x).replace('-', '')[:8] for x in d]
    return np.asarray([(date(int(s[:4]), int(s[4:6]), int(s[6:8]))-base).days for s in dates], float)


class Dash(VoiceoverScene):
    def construct(self):
        x = load("dash")
        self.card(x)
        self.yields(x)
        self.sellers()
        self.basis()
        self.funding(x)
        self.fed()
        self.compare()
        self.question()

    def card(self, x):
        y = x["y10"]
        c = chapter_card(8, r"March 2020: the dash for cash", r"Why would anyone sell the safest asset in a panic?",
                         part=PART)
        with self.voiceover(
            f"""Chapter eight. The ten-year Treasury yield rises from {y['m9']:.2f} percent on March ninth to {y['m18']:.2f} on March eighteenth, twenty twenty, while stocks fall. Treasuries often attract safe-haven demand, but urgent cash needs can also induce sales of liquid government securities. Official reviews describe several selling sectors and constrained intermediation. This price co-movement motivates those mechanisms; by itself it does not identify every seller or prove one cause."""
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def yields(self, x):
        y = x["y10"]
        m = x["mkt"]
        drop = 100 * (1 - m["low"])
        t1, v1 = _t(y["d"]), np.asarray(y["v"], float)
        t2, v2 = _t(m["d"]), np.asarray(m["v"], float)
        g1 = axes([0, 90], [0.4, 1.8], x_length=5.6, y_length=3.6, xlabel=r"Feb--Apr 2020",
                  ylabel=r"10-year yield, \%", xticks=[0, 29, 60, 90], yticks=[0.5, 1.0, 1.5],
                  xfmt=lambda u: {0: r"\text{1 Feb}", 29: r"\text{1 Mar}", 60: r"\text{1 Apr}", 90: r"\text{1 May}"}[int(u)], font_size=14)
        g2 = axes([0, 90], [0.6, 1.1], x_length=5.6, y_length=3.6, xlabel=r"Feb--Apr 2020",
                  ylabel='US stocks, before first Feb observation = 1', xticks=[0, 29, 60, 90], yticks=[0.6, 0.8, 1.0],
                  xfmt=lambda u: {0: r"\text{1 Feb}", 29: r"\text{1 Mar}", 60: r"\text{1 Apr}", 90: r"\text{1 May}"}[int(u)], font_size=14)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.2)
        l1 = curve(g1.ax, t1, v1, FUND_C, stroke_width=2.5)
        l2 = curve(g2.ax, t2, v2, PRICE_C, stroke_width=2.5)
        spans = VGroup(*[Rectangle(width=abs(g.ax.c2p(46, 0)[0] - g.ax.c2p(37, 0)[0]), height=g.ax.height,
                                   stroke_width=0, fill_color=SPIRAL_C, fill_opacity=0.18)
                         .move_to([(g.ax.c2p(46, 0)[0] + g.ax.c2p(37, 0)[0]) / 2, g.ax.get_center()[1], 0])
                         for g in (g1, g2)])
        tag = label(r"9--18 March", font_size=17, color=SPIRAL_C).next_to(spans[0], UP, buff=0.1)
        with self.voiceover(
            "Two charts from public data. <bookmark mark='a'/> On the right, American stocks: down about "
            f"{drop:.0f} percent from the start of February at the low. <bookmark mark='b'/> On the left, "
            "the ten-year Treasury yield. Through February it falls, as it should: a flight to safety. "
            "<bookmark mark='c'/> Then, in the week of the ninth to the eighteenth of March, it rises as stocks keep "
            "falling. The safe asset was being sold."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), Create(l2))
            vo.wait_until("a")
            self.play(Indicate(l2, color=HURDLE), run_time=2)
            vo.wait_until("b")
            self.play(Create(l1), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(spans), FadeIn(tag))
        self.wait(0.4)
        self.clear_scene()

    def sellers(self):
        cards = VGroup(
            desk_question(r"foreign official holders", r"central banks sold Treasuries for dollars to defend their "
                          r"currencies, as the Fed's and BIS's later accounts report", width=12.4, font_size=19),
            desk_question(r"open-end funds", r"bond funds facing redemptions sold what they could sell fastest, which "
                          r"was Treasuries, not their corporate bonds", width=12.4, font_size=19),
            desk_question(r"leveraged relative-value funds", r"the cash--futures basis trade, financed in repo, unwound as "
                          r"margins rose, as reported (next card)", width=12.4, font_size=19),
            desk_question(r"and dealers could not absorb it", 'intermediation capacity faced balance-sheet, risk-management and regulatory constraints; the leverage ratio was one factor', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.2)
        with self.voiceover(
            "Official reviews describe several sellers. <bookmark mark='a'/> Foreign official holders sold Treasuries while seeking dollar liquidity. <bookmark mark='b'/> Open-end funds sold liquid holdings to meet redemptions. <bookmark mark='c'/> Some leveraged relative-value funds unwound cash-futures positions. <bookmark mark='d'/> Dealer intermediation capacity faced risk-management, balance-sheet and regulatory constraints. The supplementary leverage ratio was one constraint, not a complete causal explanation, and funding terms did not tighten identically for every trader."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
                else:
                    self.play(Indicate(cards[0], color=HURDLE, scale_factor=1.0))
        self.wait(0.4)
        self.clear_scene()

    def basis(self):
        rows = [cmath(r"\text{long}", r":", r"\text{cash Treasury, financed in repo at } 50\text{--}100\times", font_size=36,
                      colors={r"\text{long}": LEV_C}),
                cmath(r"\text{short}", r":", r"\text{the futures contract on it}", font_size=36, colors={r"\text{short}": LEV_C}),
                cmath(r"\text{earn}", r":", r"F - P - \text{carry}\ \approx\ \text{a few basis points}", font_size=38),
                cmath(r"\text{risk}", r":", '\\text{basis, margin and funding}', font_size=32,
                      colors={r"\text{risk}": SPIRAL_C})]
        whys = [why(r"the cash bond is bought with borrowed money; the leverage figure is as reported for the trade"),
                why('demand for futures exposure can contribute to richness; actual basis also depends on delivery, financing and relative demand'),
                why('stylized net-carry basis; actual Treasury futures require conversion factors, cheapest-to-deliver and delivery-option adjustments'),
                why('basis moves, residual duration, variation margin and repo rollover can create cash needs; haircut changes and forced sales depend on financing terms')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A Treasury cash-futures basis trade. <bookmark mark='a'/> Buy a cash bond using repo financing, often at high leverage. <bookmark mark='b'/> Short Treasury futures with approximately offsetting duration. <bookmark mark='c'/> Futures minus cash minus carry is shorthand: actual pricing needs the conversion factor, cheapest-to-deliver bond, delivery options and repo specials. The residual basis is not a riskless few basis points. <bookmark mark='d'/> Variation margin, basis movements, residual duration and financing rollover can all force cash needs. Some traders faced tighter funding; a universal increase in every repo haircut is not established here."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def funding(self, x):
        cp = x["cp"]
        baa = x["baa"]
        bars = [(r"3-month commercial paper", cp["pre"], cp["max"], FUND_C),
                (r"Baa over 10-year", baa["pre"], baa["max"], SPIRAL_C)]
        rows = VGroup()
        for name, a, b, col in bars:
            r0 = Rectangle(width=a * 1.6, height=0.42, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9)
            r1 = Rectangle(width=b * 1.6, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
            VGroup(r0, r1).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            t0 = label(rf"mid-February {a:.2f}", font_size=16, color=GREY_B).next_to(r0, RIGHT, buff=0.15)
            t1 = label(rf"peak {b:.2f}", font_size=16, color=col).next_to(r1, RIGHT, buff=0.15)
            nm = label(name, font_size=19).next_to(VGroup(r0, r1), UP, aligned_edge=LEFT, buff=0.15)
            rows.add(VGroup(nm, r0, r1, t0, t1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(LEFT * 1.5)
        note_ = wrapped_label(r"percent, FRED: DCPF3M and BAA10Y", 4.2, 16, GREY_B).next_to(rows, DOWN, buff=0.4)
        with self.voiceover(
            "Funding stress, again. <bookmark mark='a'/> Three-month commercial paper went from "
            f"{cp['pre']:.2f} percent in mid-February to {cp['max']:.2f}, even as the Fed cut rates to zero: a market that "
            f"had stopped working. <bookmark mark='b'/> And the Baa credit spread roughly doubled, to {baa['max']:.2f} "
            "points. Prime money funds again lost billions in days, as in twenty oh eight."
        ) as vo:
            # Keep numerical content visible through the introductory phrase.
            self.play(FadeIn(rows[0]), FadeIn(note_))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
        self.wait(0.4)
        self.clear_scene()

    def fed(self):
        events = [(r"15 Mar", r"rates to zero; \$700bn of purchases; cheaper dollar swap lines", FUND_C),
                  (r"17--18 Mar", r"commercial paper, primary dealer and money fund facilities", FUND_C),
                  (r"23 Mar", r"purchases ``in the amounts needed''; corporate bond facilities", SAFE_C),
                  (r"31 Mar", r"a repo facility for foreign central banks' Treasuries", SAFE_C),
                  (r"1 Apr", 'temporary Treasury/reserve exclusion from the supplementary leverage ratio at eligible holding companies', SAFE_C)]
        rows = VGroup(*[VGroup(label(d_, font_size=20, color=c_), label(w_, font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.4)
                        for d_, w_, c_ in events]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(ORIGIN)
        with self.voiceover(
            "The response came in days, not months. <bookmark mark='a'/> On the fifteenth: rates to zero, seven hundred "
            "billion dollars of purchases, cheaper dollar swap lines. <bookmark mark='b'/> Then the twenty oh eight "
            "facilities, revived in two days. <bookmark mark='c'/> On the twenty-third, purchases in whatever amounts were "
            "needed, and for the first time corporate bonds. <bookmark mark='d'/> A repo facility so foreign central "
            "banks could borrow against Treasuries rather than sell them. <bookmark mark='e'/> And relief from the "
            "leverage ratio, so dealers could hold them. The yield fell back, and stocks bottomed on the twenty-third."
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

    def compare(self):
        heads = [r"", r"2008", r"2020"]
        body = [[r"where the run was", r"repo, money funds, interbank", r"Treasuries, money funds, CP"],
                [r"who held the losses", r"banks and their vehicles", r"market losses plus funding stress"],
                [r"the constraint", r"bank capital", r"dealer balance sheets"],
                [r"episode compared", r"broad financial crisis", r"acute March market dysfunction"]]
        tab = VGroup()
        for r_, row in enumerate([heads] + body):
            cells = VGroup(*[label(c, font_size=19 if r_ else 21, color=(GREY_A if r_ else QC.IDEA) if j else QC.IDEA)
                             for j, c in enumerate(row)])
            tab.add(cells)
        widths = [3.6, 4.0, 4.4]
        for row in tab:
            for j, c in enumerate(row):
                c.move_to([-6.0 + sum(widths[:j]) + c.width / 2, 0, 0])
        tab.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(ORIGIN)
        with self.voiceover(
            "Compare carefully chosen episodes. <bookmark mark='a'/> The acute March twenty twenty disruption included Treasury, money-fund and commercial-paper markets; two thousand eight involved a broader credit and banking crisis. <bookmark mark='b'/> Twenty twenty was not a world without losses: pandemic news changed expected cash flows and asset values while urgent cash needs disrupted trading. <bookmark mark='c'/> Dealer capacity and financing mattered alongside capital, risk management and market structure. <bookmark mark='d'/> Acute Treasury dysfunction eased after extensive interventions, but comparing two weeks with an eighteen-month financial crisis mixes definitions. These charts cannot isolate the interventions' causal effect or certify the status of later market reforms."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k == 0:
                    self.play(Indicate(tab[1], color=HURDLE))
                else:
                    self.play(FadeIn(tab[k + 1], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"from mid-2014 China's Shanghai Composite more than doubled in a year, much of it bought with "
                       r"borrowed money. How far did it fall, and how fast?")
        with self.voiceover(
            "Pause and predict. From the middle of twenty fourteen, China's Shanghai Composite index more than doubled in "
            "a year, much of the buying done with borrowed money. How far did it fall, and how fast?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
