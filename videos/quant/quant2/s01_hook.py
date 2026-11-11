from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import ro, CASH, CCP, LOSS, PART, TRADE, arrow, node

# NSCC, 27 January 2021 (SEC staff report, October 2021, section 3.5): intraday calls of $6.9 bn on 36 members,
# $2.1 bn mark-to-market and $4.8 bn special charge, bringing the total required across members to $25.5 bn
NSCC = {"before": 25.5 - 6.9, "mtm": 2.1, "special": 4.8, "total": 25.5}

HISTORY = [(1602, r"Amsterdam: the VOC's shares trade"), (1730, r"Osaka: Dojima rice futures recognized"),
           (1792, r"New York: the Buttonwood Agreement"), (1848, r"Chicago Board of Trade"),
           (1925, r"the first independent US futures clearing house"), (1973, r"the DTC; the CBOE opens"),
           (1986, r"London's Big Bang"), (2001, r"US stocks quoted in cents"), (2005, r"Reg NMS"),
           (2024, r"US settlement at T+1")]


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.life()
        self.robinhood()
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"What happens when you press buy?")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part two. The machinery of markets. Press buy: you see a trade in seconds. Why do the shares and cash "
            "arrive later?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def life(self):
        names = [(r"you", GREY_B), (r"your broker", TRADE), (r"an exchange or\\a wholesaler", TRADE),
                 (r"the clearing\\house (CCP)", CCP), (r"the depository\\(settlement)", CCP), (r"your account", GREY_B)]
        nodes = VGroup()
        for t, c in names:
            nd = node(t, c, width=1.95, height=1.05, font_size=20)
            nd[1].become(Tex(r"\begin{tabular}{c}" + t + r"\end{tabular}", font_size=20).move_to(nd[0]))
            nodes.add(nd)
        nodes.arrange(RIGHT, buff=0.32).shift(UP * 1.6)
        arrows = VGroup(*[arrow(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)])
        token = Dot(nodes[0].get_center(), radius=0.13, color=QC.IDEA)
        # two lanes: the trade happens in seconds; settlement a business day later
        lane_y = [-0.3, -1.3]
        lanes = VGroup()
        for y, txt, col in ((lane_y[0], r"seconds: order, match, trade", TRADE),
                            (lane_y[1], r"T+1: shares and cash change hands", CCP)):
            ln = Line([-6.2, y, 0], [6.2, y, 0], color=col, stroke_width=2, stroke_opacity=0.6)
            lanes.add(VGroup(ln, label(txt, font_size=20, color=col).next_to(ln, UP, buff=0.08).align_to(ln, LEFT)))
        clock = ValueTracker(0.0)
        hand = always_redraw(lambda: Dot([-6.2 + 12.4 * clock.get_value(), lane_y[1], 0], radius=0.09, color=CCP))
        # collateral coins drop into the CCP box while the trade waits to settle
        box = Rectangle(width=1.8, height=1.3, stroke_color=CCP, stroke_width=2).move_to([4.7, -2.75, 0])
        box_l = label(r"collateral at the CCP", font_size=18, color=CCP).next_to(box, LEFT, buff=0.15)
        coins = VGroup(*[Circle(radius=0.09, stroke_width=0, fill_color=CASH, fill_opacity=0.9)
                         .move_to(box.get_bottom() + UP * (0.15 + 0.2 * (k // 6)) + RIGHT * (-0.62 + 0.25 * (k % 6)))
                         for k in range(24)])
        with self.voiceover(
            "Here is what happens when you press buy on a share. Your broker routes the order to an exchange or a "
            "wholesaler. <bookmark mark='a'/> It meets a seller: you see a trade, but settlement has not happened. "
            "<bookmark mark='b'/> The clearing house steps between its members, becoming buyer to every seller and "
            "seller to every buyer. <bookmark mark='c'/> For US stocks, shares and cash normally move one business "
            "day later. Until then, a member could fail to pay. The clearing house collects collateral against that "
            "risk: watch it build while the trade waits. That waiting has a cost."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(n) for n in nodes], lag_ratio=0.15), FadeIn(token), FadeIn(lanes[0]))
            for i in range(2):
                self.play(GrowArrow(arrows[i]), token.animate.move_to(nodes[i + 1]), run_time=0.8)
            vo.wait_until("a")
            self.play(Indicate(nodes[2], color=TRADE))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[2]), token.animate.move_to(nodes[3]), FadeIn(lanes[1]), FadeIn(box),
                      FadeIn(box_l))
            self.add(hand)
            vo.wait_until("c")
            self.play(clock.animate.set_value(1.0),
                      LaggedStart(*[FadeIn(c, shift=DOWN * 0.6) for c in coins], lag_ratio=0.12),
                      run_time=4, rate_func=linear)
            self.play(GrowArrow(arrows[3]), token.animate.move_to(nodes[4]))
            self.play(GrowArrow(arrows[4]), token.animate.move_to(nodes[5]),
                      LaggedStart(*[FadeOut(c, shift=UP * 0.3) for c in coins], lag_ratio=0.03))
        self.wait(0.4)
        hand.clear_updaters()
        self.clear_scene()

    def robinhood(self):
        g = axes([-0.6, 1.6], [0, 28], x_length=4.2, y_length=4.4, ylabel=r"required at NSCC, all members, \$ bn",
                 yticks=[0, 10, 20], font_size=18).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        ax = g.ax
        h = ValueTracker(0.0)

        def stack():
            v = h.get_value()
            parts = [(NSCC["before"], GREY_B), (NSCC["mtm"], TRADE), (NSCC["special"], LOSS)]
            out, base = VGroup(), 0.0
            for amt, col in parts:
                top = min(base + amt, v)
                if top > base:
                    out.add(Rectangle(width=1.3, height=ax.c2p(0, top)[1] - ax.c2p(0, base)[1], stroke_width=0,
                                      fill_color=col, fill_opacity=0.85).move_to(ax.c2p(0.5, (base + top) / 2)))
                base += amt
            return out
        bars = always_redraw(stack)
        tot = ro(r"\$", lambda: h.get_value(), digits=1, font_size=32, unit=r"\,\text{bn}")
        tot.add_updater(lambda m: m.next_to(ax.c2p(0.5, max(h.get_value(), 0.5)), UP, buff=0.1))
        leg = legend([(GREY_B, r"required before the session"), (TRADE, r"intraday mark-to-market calls"),
                      (LOSS, r"special charge (volatility)")], font_size=18).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        c = crisis_card(r"27--28 January 2021", r"The day a trading app stopped buying",
                        r"On the 28th NSCC waived the excess capital premium charge for all members. ``Absent this "
                        r"waiver, one retail broker-dealer would have had an additional ECP charge of more than double "
                        r"its margin requirement of \$1.4 billion.'' Robinhood restricted buying in GameStop that "
                        r"morning, citing its clearing deposit.",
                        stats=[(r"\$6.9\,\text{bn}", r"intraday calls on 36 members, 27 Jan"),
                               (r">2\times\$1.4\,\text{bn}", r"the waived charge, one broker"),
                               (r"122.97\%", r"GameStop short interest, of float")],
                        width=6.4, font_size=20).to_corner(DR, buff=0.55)
        src = note(r"SEC staff, \textit{Equity and Options Market Structure Conditions in Early 2021} (October 2021), "
                   r"section 3.5; the report does not name the broker", font_size=16).to_edge(DOWN, buff=0.15)
        lesson = label(r"The plumbing, not the price, decided who could trade.", font_size=28, color=QC.IDEA)
        lesson.to_edge(UP, buff=0.35)
        with self.voiceover(
            "That collateral once decided who could trade. On 27 January 2021, NSCC called six point nine billion "
            "dollars from thirty-six members: two point one billion mark-to-market, four point eight billion special "
            "charge. Total required deposits reached twenty-five point five billion. <bookmark mark='a'/> Next "
            "morning, NSCC waived an excess capital premium. Without it, the SEC says, one unnamed retail broker "
            "would owe an additional charge exceeding twice its one point four billion dollar margin requirement. "
            "Robinhood restricted GameStop buying, citing its clearing deposit. Short interest had reached a hundred "
            "and twenty-three percent of float. <bookmark mark='b'/> Collateral constrained who could buy."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(src))
            self.add(bars, tot)
            self.play(h.animate.set_value(NSCC["before"]), run_time=1.5)
            self.play(h.animate.set_value(NSCC["total"]), run_time=3, rate_func=rate_functions.ease_in_quad)
            vo.wait_until("a")
            self.play(FadeIn(c, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(lesson))
        bars.clear_updaters()
        tot.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        x0, x1 = 1590, 2035
        W = 12.6

        def X(y):
            return -W / 2 + W * (y - x0) / (x1 - x0)
        line = Line([X(x0), 0, 0], [X(x1), 0, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(y), -0.06, 0], [X(y), 0.06, 0], color=GREY_C),
                                MathTex(str(y), font_size=18, color=GREY_C).next_to([X(y), 0, 0], DOWN, buff=0.12))
                         for y in (1600, 1700, 1800, 1900, 2000)])
        marks = VGroup()
        for k, (yr, what) in enumerate(HISTORY):
            up = 1 if k % 2 == 0 else -1
            d = Dot([X(yr), 0, 0], radius=0.07, color=QC.IDEA if yr < 1990 else CCP)
            row = 1 + (k // 2) % 3
            t = VGroup(MathTex(str(yr), font_size=22, color=d.get_color()),
                       wrapped_label(what, 2.5, 18, GREY_A)).arrange(DOWN, buff=0.05)
            t.move_to([X(yr), up * (0.55 + 0.75 * row), 0])
            keep_in_frame(t, 0.2)
            lead = Line(d.get_center(), t.get_bottom() if up > 0 else t.get_top(), color=GREY_D, stroke_width=1)
            marks.add(VGroup(d, lead, t))
        with self.voiceover(
            "How we got here. Shares in Amsterdam, futures in Osaka and Chicago, and exchanges in New York. <bookmark"
            " mark='a'/> Independent clearing and electronic depositories replaced chains of bilateral promises and "
            "paper certificates. <bookmark mark='b'/> Decimal quotes, market-system rules and shorter settlement "
            "changed the machine again. The timeline marks the milestones."
        ) as vo:
            self.play(Create(line), FadeIn(ticks))
            self.play(LaggedStart(*[FadeIn(m) for m in marks[:4]], lag_ratio=0.5, run_time=4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[4:6]], lag_ratio=0.5, run_time=2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks[6:]], lag_ratio=0.5, run_time=3))
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"The instruments and how each is quoted; futures, carry and the hedge",
            r"The order book, auctions, dealers and wholesalers",
            r"Clearing, netting, the default waterfall, settlement and its deposit",
            r"Margin: liquidation on a real crash, margin models and procyclicality",
            r"Short selling, repo, specials, prime brokers: the market's funding",
            r"Who earns what; indices; markets around the world; the industry and the frontier",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: follow a trade, measure collateral and funding, then compare the firms and rules behind the machine."
        ):
            self.play(FadeIn(card.head), FadeIn(card.rows[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows[1:]],
                                                     lag_ratio=0.5, run_time=9))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("treasury",))
        with self.voiceover(
            "The House gets its second desk. <bookmark mark='a'/> Treasury and funding: the cash and collateral a "
            "position needs. Every backtest pays."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(Indicate(chart.desk["treasury"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
