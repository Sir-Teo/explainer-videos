from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403

NAMES = {"price": ("Run full", "sell what is ordered, push the rest out 15% cheaper", GOOD),
         "output": ("Cut output", "make only what is ordered (never below 75%)", PRICE),
         "bank": ("Bank the furnace", "stop it when orders fall below 75%", SCRAP)}


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a mill in a glut", "Prices are falling and orders are drying up. What do you do with a "
             "blast furnace?", "Chapter one. Run it: a mill in a glut.", lit=("make", "change"))
        self.setup_()
        self.choices()
        self.play_out()
        self.everyone()
        self.real()

    def setup_(self):
        G = R["run"]
        m = G["mill"]
        bf = draw.blast_furnace(3.6).move_to([-4.0, -0.2, 0])
        tag = estimate_tag("the Works (mill.py): a model mill, its costs set near what US steelmakers disclose",
                           corner=DR, size=13)
        lines = VGroup(
            tx("Your mill: a blast furnace and a steel shop", 22, WHITE, bold=True),
            tx(f"{m['capacity']:.0f} million tonnes a year at full output", 18, GREY_A),
            tx(f"${m['variable']:.0f} a tonne for ore, coke, power and the rest", 18, ORE),
            tx(f"${m['fixed']:.0f} million a year whatever it makes", 18, COST),
            tx(f"(${m['fixed'] / m['capacity']:.0f} a tonne at full output: labour, upkeep, pensions)", 15, GREY_B),
            tx(f"break-even at full output: ${G['breakeven']:.0f} a tonne", 20, PRICE, bold=True),
            tx(f"it cannot run below {100 * m['min_rate']:.0f}% of capacity; to stop it,", 17, WHITE),
            tx(f"you bank it: half the fixed costs go on, and a restart costs ${m['restart']:.0f} million", 17, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([2.2, 0.3, 0])
        with self.voiceover(
            "Play it yourself. You run an integrated steel mill: a blast furnace that turns iron ore into molten iron, "
            f"and a steel shop beside it. It can make about {m['capacity']:.0f} million tonnes of steel a year. "
            f"<bookmark mark='a'/> Each tonne costs about {m['variable']:.0f} dollars in ore, coke, power and everything "
            f"else that goes into it. <bookmark mark='b'/> And {m['fixed']:.0f} million dollars a year must be paid "
            "whether you make anything or not: wages, maintenance, the pensions of past workers, the interest on what "
            f"the plant cost. <bookmark mark='c'/> So at full output you break even at about {G['breakeven']:.0f} "
            "dollars a tonne. <bookmark mark='d'/> One more fact about a blast furnace: it is not a tap. Below about "
            "three quarters of its capacity it does not run well, and to stop it you bank it, keep it warm and idle, "
            "which still costs about half the fixed costs, and bringing it back costs millions."
        ) as vo:
            self.play(FadeIn(bf, shift=UP * 0.2), FadeIn(tag), FadeIn(lines[:2]))
            self.play(Flash(bf.tap[0], color=HOT, flash_radius=0.4), run_time=0.8)
            vo.wait_until("a")
            self.play(FadeIn(lines[2]))
            vo.wait_until("b")
            self.play(FadeIn(lines[3:5]))
            vo.wait_until("c")
            self.play(FadeIn(lines[5], scale=1.1))
            vo.wait_until("d")
            self.play(FadeIn(lines[6:]))
        self.clear_scene()

    def chart(self, prices, pos=(0, 0.6, 0), w=7.6, h=3.0):
        G = R["run"]
        pa = viz.plot_axes([0.4, 8.6], [400, 950], x_length=w, y_length=h, xticks=list(range(1, 9)),
                           yticks=[500, 700, 900], xfmt=lambda v: f"Q{int(v)}", yfmt=lambda v: f"${v:.0f}",
                           size=13).move_to(pos)
        bars = VGroup()
        for i, o in enumerate(G["orders"]):
            x = i + 1
            b0 = pa.ax.c2p(x, 400)
            b1 = pa.ax.c2p(x, 400 + 500 * o)
            bars.add(Rectangle(width=0.42, height=b1[1] - b0[1], stroke_width=0, fill_color=SCRAP, fill_opacity=0.25).move_to(
                b0, aligned_edge=DOWN))
        ln = VMobject(stroke_color=PRICE, stroke_width=3.5).set_points_as_corners(
            [pa.ax.c2p(i + 1, p) for i, p in enumerate(prices)])
        dots = VGroup(*[Dot(pa.ax.c2p(i + 1, p), radius=0.05, color=PRICE) for i, p in enumerate(prices)])
        be = DashedLine(pa.ax.c2p(0.4, G["breakeven"]), pa.ax.c2p(8.6, G["breakeven"]), stroke_color=GREY_B,
                        stroke_width=1.5, dash_length=0.08)
        bel = tx("break-even at full output", 12, GREY_B).next_to(be, UP, buff=0.04).align_to(be, RIGHT)
        return pa, bars, ln, dots, be, bel

    def choices(self):
        G = R["run"]
        pa, bars, ln, dots, be, bel = self.chart(G["prices"], (-2.2, 1.0, 0))
        keys = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=PRICE, stroke_width=4), tx("market price, $ a tonne", 14, PRICE)
                             ).arrange(RIGHT, buff=0.1),
                      VGroup(Square(0.2, stroke_width=0, fill_color=SCRAP, fill_opacity=0.4), tx("orders, share of your capacity",
                                                                                               14, SCRAP)).arrange(RIGHT, buff=0.1)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(pa, RIGHT, buff=0.3).align_to(pa, UP)
        opts = VGroup()
        for k, key in enumerate(("price", "output", "bank")):
            n, d, col = NAMES[key]
            opts.add(VGroup(tx(f"{'ABC'[k]}.", 24, col, bold=True), VGroup(tx(n, 20, col, bold=True), tx(d, 15, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.03)).arrange(RIGHT, buff=0.2, aligned_edge=UP))
        opts.arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, -2.4, 0])
        if opts.width > 13:
            opts.scale_to_fit_width(13)
        head = tx("The glut: eight quarters", 22, WHITE, bold=True).next_to(pa, UP, buff=0.2)
        with self.voiceover(
            "Now a glut arrives. Over the next two years, quarter by quarter, <bookmark mark='a'/> the market price "
            f"falls from {G['prices'][0]} dollars a tonne to {min(G['prices'])}, below your break-even, before it "
            f"recovers. <bookmark mark='b'/> And your customers' orders shrink, to {100 * min(G['orders']):.0f} per cent "
            "of what you can make. <bookmark mark='c'/> You have three choices. A: run full anyway, sell what is ordered "
            "and push the rest out at fifteen per cent below the market. <bookmark mark='d'/> B: cut your output to "
            "what is ordered, though never below the furnace's three quarters. <bookmark mark='e'/> C: bank the furnace "
            "in the quarters when orders fall below three quarters, and restart it when they come back. Pause, and "
            "choose."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(keys), Create(be), FadeIn(bel))
            vo.wait_until("a")
            self.play(Create(ln), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), run_time=1.6)
            for m_, o in zip("cde", opts):
                vo.wait_until(m_)
                self.play(FadeIn(o, shift=UP * 0.15))
        self.clear_scene()

    def lanes(self, games, title, prices):
        G = R["run"]
        head = tx(title, 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        lanes = VGroup()
        totals = []
        for k, key in enumerate(("price", "output", "bank")):
            n, _, col = NAMES[key]
            y = 1.7 - 1.75 * k
            lab = VGroup(tx(f"{'ABC'[k]}. {n}", 18, col, bold=True)).move_to([-5.4, y, 0])
            base = Line([-4.2, y, 0], [3.9, y, 0], stroke_color=GREY_D, stroke_width=1)
            bars = VGroup()
            for q, p in enumerate(games[key]["profit"]):
                x = -3.8 + q * 1.0
                hgt = abs(p) / 150 * 0.7
                b = Rectangle(width=0.6, height=max(hgt, 0.02), stroke_width=0, fill_color=GOOD if p >= 0 else BAD,
                              fill_opacity=0.85)
                b.move_to([x, y, 0], aligned_edge=DOWN if p >= 0 else UP)
                lbl = tx(f"{p:+.0f}", 11, GREY_A).next_to(b, UP if p >= 0 else DOWN, buff=0.03)
                if games[key]["banked"][q]:
                    lbl = VGroup(lbl, tx("banked", 10, SCRAP).next_to(b, UP, buff=0.03))
                bars.add(VGroup(b, lbl))
            tot = games[key]["total"]
            totals.append(tot)
            tl = VGroup(tx("total", 13, GREY_A), tx(mm(tot), 22, col, bold=True)).arrange(DOWN, buff=0.03).move_to(
                [5.3, y, 0])
            lanes.add(VGroup(lab, base, bars, tl))
        qs = VGroup(*[tx(f"Q{q + 1}", 12, GREY_B).move_to([-3.8 + q, -3.2, 0]) for q in range(8)])
        pr = VGroup(*[tx(f"${p:.0f}", 11, PRICE).move_to([-3.8 + q, -3.45, 0]) for q, p in enumerate(prices)])
        unit = tx("profit each quarter, $ million", 13, GREY_B).move_to([-5.4, -3.3, 0])
        return head, lanes, qs, pr, unit

    def play_out(self):
        G = R["run"]
        g = G["games"]
        head, lanes, qs, pr, unit = self.lanes(g, "Your mill, quarter by quarter", G["prices"])
        best = max(("price", "output", "bank"), key=lambda k: g[k]["total"])
        tag = estimate_tag("the Works (mill.py)", corner=DR, size=13)
        with self.voiceover(
            "Here is how each choice plays out, quarter by quarter, in millions of dollars. <bookmark mark='a'/> In the "
            "good quarters, all three make money. <bookmark mark='b'/> Then the glut. Running full loses money, but "
            "every tonne still sells for more than its ore and coke, so each extra tonne cuts the loss a little. "
            "Cutting output saves on ore and coke, but the fixed costs do not shrink. Banking the furnace stops the "
            "bleeding from steel, but half the fixed costs go on, and the restart costs more. <bookmark mark='c'/> The "
            f"totals: running full, about {abs(g['price']['total']):.0f} million dollars lost; cutting output, "
            f"{abs(g['output']['total']):.0f} million; banking, {abs(g['bank']['total']):.0f} million. <bookmark mark='d'/> For one mill, on its own, the least bad choice is to keep "
            "the furnace running and sell at whatever price it takes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(qs), FadeIn(pr), FadeIn(unit), FadeIn(tag),
                      *[FadeIn(VGroup(l_[0], l_[1])) for l_ in lanes])
            vo.wait_until("a")
            for q in range(2):
                self.play(*[FadeIn(l_[2][q], shift=UP * 0.1) for l_ in lanes], run_time=0.6)
            vo.wait_until("b")
            for q in range(2, 8):
                self.play(*[FadeIn(l_[2][q], shift=UP * 0.1) for l_ in lanes], run_time=0.7)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l_[3], scale=1.2) for l_ in lanes], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("d")
            k = ("price", "output", "bank").index(best)
            self.play(Indicate(lanes[k][3], color=GOOD, scale_factor=1.3), run_time=1.2)
        self.clear_scene()

    def everyone(self):
        G = R["run"]
        pa, bars, ln, dots, be, bel = self.chart(G["prices"], (-2.4, 0.9, 0), w=7.0, h=3.0)
        ln2 = VMobject(stroke_color=BAD, stroke_width=3.5).set_points_as_corners(
            [pa.ax.c2p(i + 1, p) for i, p in enumerate(G["all_prices"])])
        l2 = tx(f"if every mill runs full: the price falls to ${min(G['all_prices']):.0f}", 15, BAD).next_to(pa, DOWN, buff=0.2)
        ga = G["games_all"]
        tab = VGroup(tx("Your losses, if every mill runs full", 18, WHITE, bold=True))
        for k, key in enumerate(("price", "output", "bank")):
            n, _, col = NAMES[key]
            tab.add(VGroup(tx(f"{'ABC'[k]}. {n}", 17, col, bold=True),
                           tx(mm(G['games'][key]['total']), 17, GREY_B),
                           tx(mm(ga[key]['total']), 19, col, bold=True)).arrange(RIGHT, buff=0.35))
        tab.add(VGroup(tx("before", 13, GREY_B), tx("now", 13, WHITE)).arrange(RIGHT, buff=0.5))
        tab.arrange(DOWN, buff=0.18, aligned_edge=RIGHT).move_to([4.2, 0.6, 0])
        lesson = VGroup(tx("What is best for each mill makes the glut deeper for all of them.", 20, PRICE, bold=True),
                        tx("That is why gluts in heavy industry last: furnaces keep running at a loss.", 17, GREY_A)
                        ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.45)
        tag = estimate_tag("the Works (mill.py): every mill's extra tonnes push the price down", corner=UR, size=13)
        with self.voiceover(
            "But you are not the only mill. Every mill in the glut does the same sum, and reaches the same answer. "
            "<bookmark mark='a'/> If all of them run full and push their extra tonnes onto the market, the price falls "
            f"much further: in this model, to about {min(G['all_prices']):.0f} dollars a tonne. <bookmark mark='b'/> Now "
            f"running full loses about {abs(ga['price']['total']):,.0f} million dollars, twice as much, and banking the "
            "furnace becomes the least bad choice. And the longer the glut lasts, the better banking looks. "
            "<bookmark mark='c'/> What is best for each mill alone makes the glut deeper for all of them. That is why "
            "gluts in heavy industry last: furnaces keep running at a loss, each hoping the others will stop first."
        ) as vo:
            self.play(FadeIn(pa), Create(ln), FadeIn(dots), Create(be), FadeIn(bel), FadeIn(tag))
            vo.wait_until("a")
            self.play(TransformFromCopy(ln, ln2), FadeIn(l2), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tab], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()

    def real(self):
        G = R["run"]
        steps = [(draw.blast_furnace(1.3), "Cleveland-Cliffs, 2025", f"decided to idle or close {G['clf_idled']:.0f} "
                  "operations: banked the blast furnace at Dearborn, Michigan;", "closed Steelton, Conshohocken and "
                  "Riverdale; restarted a blast furnace in Ohio"),
                 (draw.factory(1.2), "US Steel, 2025 (bought by Nippon Steel in June)", "halted a 2.7-million-tonne mill in "
                  "Illinois,", "but kept it ready to restart"),
                 (draw.coin_stack(3, r=0.15), "and their results", f"Cliffs lost ${abs(R['tonne']['clf_net']):.1f} billion in "
                  "2025;", f"Nucor, whose mills are all electric, earned ${R['tonne']['nue_net']:.1f} billion")]
        rows = VGroup()
        for ic, h, a, b in steps:
            ic.scale_to_fit_height(1.0)
            rows.add(VGroup(ic, VGroup(tx(h, 24, WHITE, bold=True), tx(a, 19, GREY_A), tx(b, 19, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.04)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        head = tx("What American mills actually did", 26, GOLD, bold=True).to_edge(UP, buff=0.5)
        src = source("Cleveland-Cliffs, Form 10-K 2025; USGS, Mineral Commodity Summaries 2026 (Iron and Steel); SEC "
                     "company facts", size=13)
        with self.voiceover(
            "And what did real mills do? <bookmark mark='a'/> In 2025, a hard year for American integrated steel, "
            f"Cleveland-Cliffs decided to idle or close {G['clf_idled']:.0f} of its operations: it banked the blast "
            "furnace at Dearborn in Michigan, closed three older plants for good, and restarted a furnace in Ohio. "
            "<bookmark mark='b'/> US Steel, bought that June by Nippon Steel, halted a mill in Illinois but kept it "
            "ready to restart. <bookmark mark='c'/> Cliffs lost about "
            f"{abs(R['tonne']['clf_net']):.1f} billion dollars that year. Nucor, whose mills melt scrap in electric "
            f"furnaces, earned {R['tonne']['nue_net']:.1f} billion. Why such different fortunes? It starts with the two "
            "ways of making steel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for m_, r_ in zip("abc", rows):
                vo.wait_until(m_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
