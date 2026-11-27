from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a gas plant in a cold snap", "Would you promise next week's power at today's price?",
             "Chapter one. Run it: a gas plant in a cold snap.", lit=("make", "change"))
        self.setup_()
        self.week()
        self.outcomes()
        self.real()

    def setup_(self):
        G = R["run"]
        plant = draw.gas_plant(2.0).move_to([-4.4, -0.6, 0])
        lab = tx(f"your plant: {G['mw']:.0f} MW of gas turbines", 18, GAS, bold=True).next_to(plant, DOWN, buff=0.2)
        cost = tx(f"its fuel and running cost: about ${G['cost']:.0f} a MWh", 15, GREY_A).next_to(lab, DOWN, buff=0.08)
        opts = VGroup(
            VGroup(tx("A.  Sell at the spot price, hour by hour", 22, WHITE, bold=True),
                   tx("run when the price covers your cost; take whatever the market pays", 16, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05),
            VGroup(tx(f"B.  Sell the whole week forward at ${G['forward']:.0f} a MWh", 22, WHITE, bold=True),
                   tx("a buyer pays you a fixed price for every hour; if you cannot run,", 16, GREY_A),
                   tx("you must buy the power somewhere else and deliver it anyway", 16, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.4, 1.0, 0])
        cold = VGroup(tx("the weather forecast: a cold front, midweek", 17, WIND, bold=True),
                      tx("and in a cold snap, gas wells and pipelines can freeze", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([2.4, -1.8, 0])
        tag = estimate_tag("the Works (power.py): an illustrative plant, prices and week", corner=DR, size=12)
        with self.voiceover(
            f"Play it yourself. You own a {G['mw']:.0f}-megawatt gas plant in a market like Texas's in 2021, where power "
            "was bought and sold hour by hour and the price could rise as high as nine thousand dollars a megawatt-hour "
            f"when supply ran short. Your fuel and running costs come to about {G['cost']:.0f} dollars a megawatt-hour. "
            "<bookmark mark='a'/> You can sell at the spot price, hour by hour. <bookmark mark='b'/> Or a buyer will "
            f"take your whole week's output now, at a fixed {G['forward']:.0f} dollars. Safe money; but if your plant "
            "cannot run, you still owe the power, and must buy it somewhere else. <bookmark mark='c'/> The forecast "
            "says a cold front is coming, midweek. Pause, and choose."
        ) as vo:
            opts.set_opacity(0.25)
            self.play(FadeIn(plant), FadeIn(lab), FadeIn(cost), FadeIn(tag), FadeIn(opts))
            vo.wait_until("a")
            self.play(opts[0].animate.set_opacity(1))
            vo.wait_until("b")
            self.play(opts[1].animate.set_opacity(1))
            vo.wait_until("c")
            self.play(FadeIn(cold, shift=UP * 0.1))
        self.clear_scene()

    def week(self):
        G = R["run"]
        p = G["prices"]
        hrs = list(range(len(p)))
        pa = viz.plot_axes([0, 168], [1, 4.1], x_length=10.4, y_length=4.4, xticks=[12 + 24 * k for k in range(7)],
                           yticks=[1, 2, 3, 4], xfmt=lambda v: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][int(v) // 24],
                           yfmt=lambda v: f"${10 ** v:,.0f}", ylabel="spot price, $ a MWh (log scale)", size=14).move_to(
            [0, -0.5, 0])
        ln = poly(pa, [(h, np.log10(max(v, 1))) for h, v in zip(hrs, p)], PRICE, 3)
        cost = DashedLine(pa.ax.c2p(0, np.log10(G["cost"])), pa.ax.c2p(168, np.log10(G["cost"])), stroke_color=GAS,
                          stroke_width=2, dash_length=0.08)
        cl = tx(f"your cost, ${G['cost']:.0f}", 14, GAS).next_to(cost, UP, buff=0.04).align_to(cost, LEFT)
        fw = DashedLine(pa.ax.c2p(0, np.log10(G["forward"])), pa.ax.c2p(168, np.log10(G["forward"])), stroke_color=WHITE,
                        stroke_width=1.5, dash_length=0.05)
        snap = Rectangle(width=pa.ax.c2p(120, 0)[0] - pa.ax.c2p(72, 0)[0], height=4.4, stroke_width=0, fill_color=WIND,
                         fill_opacity=0.10).move_to([(pa.ax.c2p(120, 0)[0] + pa.ax.c2p(72, 0)[0]) / 2, pa.ax.c2p(0, 2.55)[1], 0])
        sl = tx("the cold snap: the price at the cap, $9,000", 15, WIND, bold=True).next_to(snap, UP, buff=0.05)
        fz = VGroup(tx("and gas for your plant costs", 14, GREY_A), tx(f"about ${G['snap_cost']:.0f} a MWh, if it", 14, GREY_A),
                    tx("arrives at all", 14, GREY_A)).arrange(DOWN, buff=0.02).move_to(pa.ax.c2p(146, 2.6))
        head = tx("Your week, hour by hour", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        tag = estimate_tag("the Works (power.py): an illustrative week", corner=DR, size=12)
        with self.voiceover(
            "Here is the week. <bookmark mark='a'/> Monday to Wednesday, the price moves between about twenty and fifty "
            f"dollars, around your cost. <bookmark mark='b'/> Then the cold arrives. Everyone turns up the heat; plants "
            "freeze; there is not enough power, and the price goes to the cap, nine thousand dollars a megawatt-hour, "
            "for two whole days. <bookmark mark='c'/> And the gas for your plant, if it arrives at all, now costs ten "
            "times as much."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(tag), Create(cost), FadeIn(cl), Create(fw))
            vo.wait_until("a")
            part1 = poly(pa, [(h, np.log10(max(v, 1))) for h, v in zip(hrs[:66], p[:66])], PRICE, 3)
            self.play(Create(part1), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(snap), Create(ln), run_time=3.0, rate_func=linear)
            self.play(FadeIn(sl))
            vo.wait_until("c")
            self.play(FadeIn(fz))
        self.clear_scene()

    def outcomes(self):
        G = R["run"]["games"]
        keys = [("spot, runs", "A. spot, and it runs", GOOD), ("hedged, runs", "B. sold forward, and it runs", PRICE),
                ("spot, freezes", "A. spot, and it freezes", WIND), ("hedged, freezes", "B. sold forward, and it freezes", BAD)]
        lo = min(min(G[k]["cum"]) for k, _, _ in keys)
        hi = max(max(G[k]["cum"]) for k, _, _ in keys)
        pa = viz.plot_axes([0, 168], [lo * 1.15, hi * 1.15], x_length=8.4, y_length=4.6, xticks=[12 + 24 * k for k in range(7)],
                           yticks=[-200, -100, 0, 100, 200], xfmt=lambda v: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][int(v) // 24],
                           yfmt=lambda v: f"${v:,.0f}m", ylabel="your cash so far this week", size=13).move_to([-1.8, -0.4, 0])
        zero = Line(pa.ax.c2p(0, 0), pa.ax.c2p(168, 0), stroke_color=GREY_B, stroke_width=1.2)
        lines, labs = VGroup(), VGroup()
        for i, (k, name, col) in enumerate(keys):
            c = G[k]["cum"]
            lines.add(poly(pa, list(zip(range(len(c)), c)), col, 3.5))
            v = G[k]["total"]
            labs.add(VGroup(tx(name, 15, col, bold=True), tx(("+" if v >= 0 else "−") + f"${abs(v):,.0f}m", 20, col, bold=True)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.03))
        labs.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.9, -0.3, 0])
        tag = estimate_tag("the Works (power.py)", corner=DR, size=12)
        with self.voiceover(
            "Here is your week, four ways. <bookmark mark='a'/> If you sold at the spot price and your plant kept running, "
            f"you made about {G['spot, runs']['total']:.0f} million dollars, almost all of it in two days. "
            "<bookmark mark='b'/> If you sold forward and kept running, you made nothing at all: you were paid forty "
            "dollars for power that cost you three hundred to make. <bookmark mark='c'/> If you sold at spot and your "
            "plant froze, you simply earned nothing during the storm. <bookmark mark='d'/> But if you sold forward and "
            f"your plant froze, you had to buy {R['run']['mw']:.0f} megawatts every hour at nine thousand dollars, to "
            f"deliver power you had sold for forty: a loss of about {abs(G['hedged, freezes']['total']):.0f} million "
            "dollars in two days. The hedge that looked safe was the most dangerous choice of all."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(tag))
            for m_, ln, lb in zip("abcd", lines, labs):
                vo.wait_until(m_)
                self.play(Create(ln), FadeIn(lb, shift=LEFT * 0.1), run_time=2.0)
        self.clear_scene()

    def real(self):
        G = R["run"]
        quote = VGroup(tx(f"Vistra, a Texas power company: Winter Storm Uri cost ${G['vst']:.1f} billion", 22, WHITE, bold=True),
                       tx("of pre-tax earnings in 2021, driven by", 18, GREY_A),
                       tx("'the need to procure power in ERCOT at market prices at or near the price cap", 18, PRICE),
                       tx("due to lower output from our natural gas-fueled power plants", 18, PRICE),
                       tx("driven by natural gas deliverability issues'", 18, PRICE)).arrange(DOWN, buff=0.1)
        quote.move_to([0, 0.4, 0])
        plant = draw.gas_plant(1.2).next_to(quote, DOWN, buff=0.5)
        ice = VGroup(*[Line(UP * 0.18, DOWN * 0.18, stroke_color=WIND, stroke_width=3).rotate(a).move_to(plant.get_top() + RIGHT * (0.4 * k - 0.6))
                       for k in range(4) for a in (0, PI / 3, -PI / 3)])
        src = source("Vistra Corp., Form 10-K 2021", size=13)
        with self.voiceover(
            "That is not a thought experiment. In February 2021 a storm called Uri froze Texas. <bookmark mark='a'/> "
            f"Vistra, a Texas company that owns power plants and sells electricity to homes, lost about {G['vst']:.1f} billion dollars of pre-tax "
            "earnings on it. Its own words: it had to buy power at or near the price cap, because its gas plants could "
            "not get enough gas. <bookmark mark='b'/> Electricity punishes promises. A power company sells something "
            "it has to deliver at the very second it is used, and on the worst day of the year it may not be able to."
        ) as vo:
            self.play(FadeIn(src), FadeIn(plant), FadeIn(quote[0]))
            vo.wait_until("a")
            self.play(FadeIn(quote[1]), Indicate(quote[0], color=PRICE), run_time=1.0)
            self.play(FadeIn(quote[2:]), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(i_) for i_ in ice], lag_ratio=0.05), run_time=1.5)
        self.clear_scene()
