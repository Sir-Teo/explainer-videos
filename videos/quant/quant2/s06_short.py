from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import ro, CASH, GAIN, LOSS, PART, TRADE, load

C_ = {r"r_b": CASH, r"f": LOSS, r"\Pi_T": QC.IDEA, r"\kappa": QC.HOUSE}


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class Short(VoiceoverScene):
    def construct(self):
        q = load("squeeze")
        self.card()
        self.mechanics()
        self.pnl(q)
        self.relend()
        self.squeeze(q)
        self.vw(q)

    def card(self):
        c = chapter_card(10, r"Short selling and the squeeze", r"How do you sell what you don't own, and what can "
                         r"go wrong?", lit=(2008, 2021), part=PART)
        with self.voiceover("Chapter ten. Short selling, and the squeeze."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def mechanics(self):
        steps = VGroup(
            label(r"1. locate: find a lender (a pension fund, an index fund) through your broker", font_size=24),
            label(r"2. borrow the shares, post cash collateral (about 102\% of their value), and sell them", font_size=24),
            label(r"3. the lender keeps a fee: it pays you a rebate on your cash below the market rate", font_size=24),
            label(r"4. the lender can recall the shares at any time; you must buy them back and return them", font_size=24),
            label(r"5. the lender keeps its dividends: the short seller pays them", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.3)
        if steps.width > 13.0:
            steps.scale_to_fit_width(13.0)
        with self.voiceover(
            "To bet that a price will fall, you sell something you don't own. First your broker locates a lender: "
            "often a pension fund or an index fund, which lends its shares for a fee. <bookmark mark='a'/> You borrow "
            "the shares, post cash collateral worth a little more than they are, and sell them. <bookmark mark='b'/> "
            "The lender pays you interest on that cash, a rebate, less its fee. <bookmark mark='c'/> It can recall "
            "its shares at any moment, and then you must buy them back, at whatever the price is. "
            "<bookmark mark='d'/> And any dividend paid while you are short is yours to pay."
        ) as vo:
            self.play(FadeIn(steps[0]))
            for i, mk in enumerate("abcd", start=1):
                vo.wait_until(mk)
                self.play(FadeIn(steps[i], shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def pnl(self, q):
        rows = [
            row(r"C \approx 1.02\,S_0,\qquad", r"r_b", r"=", r"r - f"),
            row(r"\Pi_T", r"=", r"(S_0 - S_T) + C\,", r"r_b", r"\,T - \textstyle\sum \text{div}"),
            row(r"f > r", r"\Rightarrow", r"r_b", r"< 0"),
        ]
        whys = [why(r"the collateral earns the rebate: the market rate less the lender's fee", font_size=21),
                why(r"price, plus rebate, less the dividends paid to the lender", font_size=21),
                why(r"a ``special'': the short seller pays interest on its own collateral", font_size=21)]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.0, buff=0.45, edge=6.9)
        ex = VGroup(
            MathTex(rf"S: 100 \to 90,\ r = 5\%,\ \text{{one year}}", font_size=30),
            MathTex(rf"\text{{general collateral, }} f = 0.25\%:\ \Pi = +{q['short_pnl_gc']:.2f}", font_size=30,
                    color=GAIN),
            MathTex(rf"\text{{special, }} f = 20\%:\ \Pi = {q['short_pnl_special']:.2f}", font_size=30, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(LEFT, buff=0.8).shift(DOWN * 1.6)
        dav = VGroup(
            label(r"D'Avolio (2002), a large lender, April 2000 -- September 2001:", font_size=21, color=QC.IDEA),
            label(r"91\% of stocks on loan cost under 1\% a year (17 bp, value-weighted)", font_size=20),
            label(r"9\% were specials, averaging 4.3\% a year", font_size=20),
            label(r"under 1\% had negative rebates; fees up to 50\%", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.35).shift(DOWN * 1.6)
        with self.voiceover(
            "The arithmetic of a short. The collateral, about a hundred and two percent of the price, earns the "
            "rebate rate: the market rate less the lender's fee. <bookmark mark='a'/> So the profit is the fall in "
            "the price, plus the rebate on the collateral, less the dividends handed to the lender. "
            "<bookmark mark='b'/> When shares are scarce the fee can exceed the interest rate, and the rebate turns "
            "negative: the short seller pays to borrow its own cash back. Take a stock that falls from a hundred to "
            f"ninety in a year, with rates at five percent. Borrowed cheaply, the short makes {q['short_pnl_gc']:.2f}. "
            f"At a twenty percent fee it loses {abs(q['short_pnl_special']):.2f}, though it was right about the "
            "price. <bookmark mark='c'/> How common is that? D'Avolio's data from a large lender: ninety-one percent "
            "of stocks on loan were general collateral, costing seventeen basis points; nine percent were special, "
            "at four point three percent on average; and under one percent cost more than the interest rate."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(ex))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d) for d in dav], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def relend(self):
        people = VGroup(*[VGroup(Circle(radius=0.5, color=c, fill_opacity=0.12), label(n, font_size=22))
                          for n, c in ((r"lender A", CASH), (r"short seller", LOSS), (r"buyer B", TRADE),
                                       (r"short seller 2", LOSS), (r"buyer C", TRADE))])
        people.arrange(RIGHT, buff=0.9).shift(UP * 1.0)
        for p in people:
            p[1].move_to(p[0])
        share = Square(0.35, color=QC.IDEA, fill_opacity=0.9).move_to(people[0].get_center() + UP * 0.9)
        si = ValueTracker(0)
        cnt = VGroup(ro(r"\text{short interest (shares)}:", lambda: si.get_value(), digits=0, font_size=32,
                             color=LOSS),
                     MathTex(r"\text{shares that exist: } 1", font_size=32, color=QC.IDEA)).arrange(DOWN, aligned_edge=LEFT)
        cnt.shift(DOWN * 1.3)
        foot = wrapped_label(r"SEC staff report, footnote 75: one share sold short twice gives short interest of 2\% on "
                             r"100 shares; GameStop's short interest reached 122.97\% of its float in January 2021",
                             11.4, 21, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How can short interest exceed a hundred percent of the shares available? Follow one share. The lender "
            "lends it to a short seller, who sells it to buyer B. <bookmark mark='a'/> B now owns a share like any "
            "other, and can lend it too: to a second short seller, who sells it to C. <bookmark mark='b'/> One share "
            "exists, two are sold short, and short interest counts two. Repeat it enough and short interest passes "
            "a hundred percent of the float: GameStop's reached a hundred and twenty-three. Every short is a future "
            "buyer."
        ) as vo:
            self.play(FadeIn(people), FadeIn(share), FadeIn(cnt))
            self.play(share.animate.move_to(people[1].get_center() + UP * 0.9), si.animate.set_value(1))
            self.play(share.animate.move_to(people[2].get_center() + UP * 0.9))
            vo.wait_until("a")
            self.play(share.animate.move_to(people[3].get_center() + UP * 0.9), si.animate.set_value(2))
            self.play(share.animate.move_to(people[4].get_center() + UP * 0.9))
            vo.wait_until("b")
            self.play(FadeIn(foot), Indicate(cnt[0], color=LOSS))
        cnt[0].clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def squeeze(self, q):
        rel = np.asarray(q["rel"], float)
        peak = np.asarray(q["peak"]["0.2"], float)
        trans = float(rel[int(np.argmax(peak.mean(0) > 5))])
        mv = np.asarray(q["movie_hi"], float)
        cov = np.asarray(q["cov_hi"], float)
        # the float as a tank: locked-up holders below, the free float above; covering buyers drain it
        tank = Rectangle(width=1.6, height=4.4, stroke_color=GREY_B, stroke_width=2).move_to(LEFT * 5.2 + DOWN * 0.2)
        rk = ValueTracker(0)
        free = always_redraw(lambda: Rectangle(width=1.6, height=max(4.4 * (1 - min(at_index(cov, rk) / 1000 * 1.2,
                                                                                      1.0)), 0.02),
                                               stroke_width=0, fill_color=TRADE, fill_opacity=0.6)
                             .align_to(tank, DOWN).set_x(tank.get_x()))
        tl = label(r"free float left to buy", font_size=18, color=TRADE).next_to(tank, DOWN, buff=0.15)
        therm = always_redraw(lambda: Rectangle(width=0.4, height=max(4.4 * np.log(at_index(mv, rk)) / np.log(50), 0.02),
                                                stroke_width=0, fill_color=LOSS, fill_opacity=0.85)
                              .move_to(LEFT * 3.4 + DOWN * 2.4, aligned_edge=DOWN))
        thf = Rectangle(width=0.4, height=4.4, stroke_color=GREY_B).move_to(LEFT * 3.4 + DOWN * 0.2)
        pr = ro(r"P/P_0 =", lambda: at_index(mv, rk), digits=2, font_size=28, color=LOSS).next_to(thf, UP, buff=0.15)
        cv = ro(r"\text{shorts covered:}", lambda: at_index(cov, rk), digits=0, font_size=24).next_to(pr, UP, buff=0.12)
        g = axes([0.2, 1.4], [0, 3.2], x_length=5.6, y_length=3.6, xlabel=r"short interest / free float",
                 ylabel=r"peak price multiple (log scale)", xticks=[0.2, 0.6, 1.0, 1.4], yticks=[0, 1, 2, 3],
                 yfmt=lambda v: f"10^{{{int(v)}}}", font_size=16).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        sb = seed_band(g.ax, rel, np.log10(np.clip(peak, 1, 1000)), LOSS)
        tv = DashedLine(g.ax.c2p(trans, 0), g.ax.c2p(trans, 3.2), color=QC.IDEA)
        rows = VGroup(
            MathTex(r"\frac{P}{P_0} = \Big(1 - \frac{B}{f}\Big)^{-\kappa}", font_size=34, color=QC.HOUSE),
            label(r"buys $B$ drain the free float $f$; each short covers past its own pain threshold", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, UP, buff=0.3).align_to(g, LEFT)
        src = note(r"simulated: 1,000 shorts with lognormal thresholds (median +50\%), $\kappa = 0.5$ (1\% of the float "
                   r"moves the price 0.5\%), 8 seeds", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Why do squeezes explode? Picture the float as a tank. Big holders who never sell sit at the bottom; "
            "above them, the free float, the only shares anyone can buy. Every short seller must one day buy a "
            "share out of that layer. <bookmark mark='a'/> Model it: buying drains the free layer, and the price "
            "rises as it empties; each short has a pain threshold and covers once the price passes it. Start a "
            "thousand shorts holding one point two times the free float, and nudge the price. A few cover; their "
            "buying lifts the price past the next thresholds; the queue outruns the layer, and the price explodes. "
            "<bookmark mark='b'/> Run it across short interest, eight seeds each. Below about "
            f"{trans:.1f} times the free float, a nudge stays a nudge. Above it, the same nudge runs away. The size "
            "of the float doesn't matter in this model; the ratio does."
        ) as vo:
            self.play(FadeIn(tank), FadeIn(tl), FadeIn(thf), FadeIn(pr), FadeIn(cv), FadeIn(rows), FadeIn(src))
            self.add(free, therm)
            vo.wait_until("a")
            self.play(rk.animate.set_value(len(mv) - 1), run_time=7, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("b")
            self.play(FadeIn(g), FadeIn(sb[0]), Create(sb[1]), Create(tv))
        for m in (free, therm, pr, cv):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def vw(self, q):
        parts = [(r"Porsche: shares", 0.426, QC.FIRM), (r"Porsche: cash-settled options", 0.315, QC.IDEA),
                 (r"Lower Saxony (about 20\%)", 0.20, CASH), (r"free float", q["vw_free"], TRADE)]
        bar = VGroup()
        y = -2.4
        for name, v, c in parts:
            h = 4.6 * v
            r_ = Rectangle(width=1.6, height=h, stroke_width=1, stroke_color=GREY_D, fill_color=c, fill_opacity=0.75)
            r_.move_to([-4.8, y + h / 2, 0])
            bar.add(VGroup(r_, label(name, font_size=19, color=c).next_to(r_, RIGHT, buff=0.2)))
            y += h
        top = MathTex(rf"\approx {100 * q['vw_free']:.0f}\%\ \text{{left}}", font_size=30, color=TRADE)
        top.next_to(bar[-1], RIGHT, buff=0.2).shift(RIGHT * 1.7)
        c = crisis_card(r"26--29 October 2008", r"Volkswagen: the squeeze",
                        r"On Sunday 26 October Porsche disclosed 42.6\% of VW's ordinary shares plus cash-settled "
                        r"options on 31.5\%: 74.1\%. With Lower Saxony's stake, about 6\% was left to buy. Short "
                        r"sellers rushed to cover; for a few hours VW was the world's most valuable company. Porsche "
                        r"then said it would release up to 5\%, and the price fell back. Hedge funds later sued, "
                        r"alleging that Porsche had misled the market; Porsche denied it.",
                        stats=[(r"\sim\text{\texteuro}211 \to >\text{\texteuro}1{,}000", r"Friday's close to Tuesday's "
                                                                                       r"intraday high"),
                               (r"74.1\%", r"held or controlled by Porsche")], width=6.6, font_size=19)
        c.to_edge(RIGHT, buff=0.3)
        q_ = desk_question(r"Short interest is 120\% of float. How is that possible, and who is short what?",
                           width=6.6, font_size=20).to_corner(DR, buff=0.25)
        src = note(r"reported prices and stakes (Reuters, Risk.net); free float computed from the stakes", font_size=16)
        src.to_edge(DOWN, buff=0.1).to_edge(LEFT, buff=0.3)
        with self.voiceover(
            "The crisis file is the most famous squeeze of all. On Sunday the 26th of October 2008, Porsche "
            "disclosed that it held forty-two point six percent of Volkswagen's ordinary shares, and cash-settled "
            "options on thirty-one point five more: seventy-four point one percent. The state of Lower Saxony held "
            f"about a fifth. Fill the tank: about {100 * q['vw_free']:.0f} percent was left to buy, and short "
            "interest was larger than that. <bookmark mark='a'/> On Monday and Tuesday the price went from about two "
            "hundred and eleven euros to above a thousand, and for a few hours Volkswagen was the most valuable "
            "company in the world. Then Porsche said it would release up to five percent, and the price fell back. "
            "Hedge funds later sued, alleging Porsche had misled the market; Porsche denied it. Prices in a squeeze "
            "are set not by value but by who must buy, and how much is left. Pause and predict: short interest at a "
            "hundred and twenty percent of float. How, and who is short what?"
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b) for b in bar], lag_ratio=0.5, run_time=4), FadeIn(src))
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(c, shift=LEFT * 0.2))
            self.wait(2)
            self.play(FadeOut(c), FadeIn(q_))
        self.wait(1.0)
        self.clear_scene()
