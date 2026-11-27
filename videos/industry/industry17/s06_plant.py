from __future__ import annotations

from videos.industry.industry17.common import *  # noqa: F403


class Plant(VoiceoverScene):
    def construct(self):
        card(self, 5, "The plant's break-even", "How full must a car plant be to make money?",
             "Chapter five. The plant's break-even. How full must a car plant be to make money?", lit=("make",))
        self.curve()
        self.history()
        self.newcomers()
        self.worlds()

    def curve(self):
        P = R["plant"]
        cv = P["curve"]
        pa = viz.plot_axes([0.3, 1.0], [-1000, 900], x_length=8.6, y_length=4.4, xticks=[0.3, 0.5, 0.7, 0.9, 1.0],
                           yticks=[-900, -600, -300, 0, 300, 600, 900], xfmt=lambda v: f"{100 * v:.0f}%",
                           yfmt=lambda v: ("-" if v < 0 else "") + f"${abs(v):.0f}m",
                           ylabel="the plant's profit for the year", size=13).move_to([-1.4, -0.5, 0])
        pa.add(xlab(pa, "how full the plant is (cars sold over what two shifts can build)"))
        line = poly(pa, sorted(cv.items()), YOU, 4)
        zero = DashedLine(pa.ax.c2p(0.3, 0), pa.ax.c2p(1.0, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        be = Dot(pa.ax.c2p(P["be_share"], 0), radius=0.11, color=PRICE)
        bel = tx(f"break-even: {100 * P['be_share']:.0f}% full", 16, PRICE, bold=True).next_to(be, UL, buff=0.1)
        loss = Polygon(*[pa.ax.c2p(u, v) for u, v in sorted(cv.items()) if u <= P["be_share"] + 1e-9],
                       pa.ax.c2p(P["be_share"], 0), pa.ax.c2p(0.3, 0), stroke_width=0, fill_color=BAD, fill_opacity=0.25)
        quote = VGroup(tx("Toyota, Form 20-F, fiscal 2026:", 14, GREY_B),
                       tx("'we have recently seen a significant rise in our", 15, WHITE),
                       tx("break-even volume due to a combination of increases", 15, WHITE),
                       tx("in investments in human resources and future-oriented", 15, WHITE),
                       tx("investments and the impact of U.S. tariffs.'", 15, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).to_corner(UR, buff=0.35).shift(DOWN * 0.2)
        tag = estimate_tag("the Works' model plant from chapter one: illustrative numbers", size=12)
        with self.voiceover(
            "Go back to the plant from the Run it game and ask a plainer question: how full must it be? "
            "<bookmark mark='a'/> Here is its profit at every level of output. Below about "
            f"{100 * P['be_share']:.0f} per cent of what its two shifts can build, it loses money, because the crews, the "
            "tooling and the engineering cost the same at any level. <bookmark mark='b'/> Above it, every extra car adds "
            "its full margin, and profit climbs steeply. A car plant is a machine for turning volume into profit, and its "
            "owner lives on the steep part of this line. <bookmark mark='c'/> Carmakers say so themselves. Toyota told its "
            "investors in 2026 that its break-even volume had risen significantly, because of new investment and America's "
            "tariffs."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(tag), FadeIn(ghost(line, opacity=0.3)))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.0)
            self.play(FadeIn(loss), GrowFromCenter(be), FadeIn(bel))
            vo.wait_until("b")
            self.play(Indicate(line, color=GOOD))
            vo.wait_until("c")
            self.play(FadeIn(quote, shift=LEFT * 0.2))
        self.clear_scene()

    def history(self):
        P = R["plant"]
        u = {y: v for y, v in P["util"].items() if y <= 2025}
        pa = viz.plot_axes([1948, 2026], [30, 100], x_length=10.4, y_length=4.4, xticks=[1950, 1970, 1990, 2010, 2025],
                           yticks=[40, 60, 80, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                           ylabel="US motor vehicle and parts plants: output over capacity, yearly average", size=13).move_to([-0.2, -0.5, 0])
        line = poly(pa, sorted(u.items()), MAKER, 3)
        avg = DashedLine(pa.ax.c2p(1948, P["avg"]), pa.ax.c2p(2026, P["avg"]), stroke_color=GOOD, stroke_width=1.5, dash_length=0.08)
        al = tx(f"average since 1948: {P['avg']:.0f}%", 14, GOOD).next_to(pa.ax.c2p(1950, P["avg"]), UR, buff=0.06)
        lows = VGroup()
        for y, txt in ((1982, "1982"), (2009, "2009")):
            d = Dot(pa.ax.c2p(y, u[y]), radius=0.08, color=BAD)
            lows.add(VGroup(d, tx(f"{txt}: {u[y]:.0f}%", 14, BAD, bold=True).next_to(d, DOWN, buff=0.08)))
        covid = tx(f"April 2020, one month: {P['low']:.0f}%", 14, BAD, bold=True).next_to(pa.ax.c2p(2020, 35), LEFT, buff=0.1)
        last = Dot(pa.ax.c2p(2025, u[2025]), radius=0.08, color=PRICE)
        ll = tx(f"2025: {u[2025]:.0f}%", 14, PRICE, bold=True).next_to(last, UP, buff=0.12)
        src = source("Federal Reserve, G.17 Industrial Production and Capacity Utilization, motor vehicles and parts (via FRED, "
                     "CAPUTLG3361T3S)", size=12)
        with self.voiceover(
            "How full are real plants? <bookmark mark='a'/> The Federal Reserve has measured America's motor vehicle and "
            "parts plants against their capacity every month since 1948. <bookmark mark='b'/> On average they have run at "
            f"about {P['avg']:.0f} per cent. <bookmark mark='c'/> In bad years the line falls off a cliff: "
            f"{u[1982]:.0f} per cent in 1982, {u[2009]:.0f} per cent in 2009, the year Chrysler's business was sold in a "
            f"government-sponsored restructuring, and in April 2020, with the plants shut for the pandemic, {P['low']:.0f} "
            "per cent. "
            f"<bookmark mark='d'/> In 2025 the plants ran at about {u[2025]:.0f} per cent: about the break-even "
            "of the model plant."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(ghost(line, opacity=0.3)))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(avg), FadeIn(al))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lows], lag_ratio=0.5), FadeIn(covid))
            vo.wait_until("d")
            self.play(GrowFromCenter(last), FadeIn(ll))
        self.clear_scene()

    def newcomers(self):
        P = R["plant"]
        rows = [("Rivian, Normal, Illinois", P["rivian"], EV), ("Lucid, Casa Grande, Arizona", P["lucid"], EV)]
        g = VGroup()
        for i, (name, (made, cap), col) in enumerate(rows):
            y = 1.3 - 2.0 * i
            full = Rectangle(width=8.0, height=0.6, stroke_color=GREY_B, stroke_width=2, fill_opacity=0).move_to([0.6, y, 0])
            used = Rectangle(width=8.0 * made / cap, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(full.get_left(), aligned_edge=LEFT)
            nm = tx(name, 18, WHITE, bold=True).next_to(full, UP, buff=0.1).align_to(full, LEFT)
            cl = tx(f"capacity {cap:,.0f} a year", 15, GREY_A).next_to(full, UP, buff=0.1).align_to(full, RIGHT)
            ml = tx(f"built in 2025: {made:,.0f} ({100 * made / cap:.0f}%)", 16, col, bold=True).next_to(used, DOWN, buff=0.1).align_to(full, LEFT)
            g.add(VGroup(full, nm, cl, used, ml))
        fac = VGroup(draw.factory(1.6, "#5C6472"), draw.factory(1.6, "#5C6472")).arrange(DOWN, buff=0.9).move_to([-5.2, 0.3, 0])
        quote = VGroup(tx("Rivian, Form 10-K 2025: 'This lower utilization of plant capacity results in the cost of revenues", 14, WHITE),
                       tx("to operate the plant being much higher per unit of production than would be the case", 14, WHITE),
                       tx("if we were manufacturing at capacity.'", 14, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([0, -2.35, 0])
        src = source("Rivian, Form 10-K 2025; Lucid, Form 10-K 2025 and production release of 5 January 2026", size=12)
        with self.voiceover(
            "Now look at the newcomers. <bookmark mark='a'/> Rivian's plant in Normal, Illinois, can build "
            f"{P['rivian'][1]:,.0f} vehicles a year. In 2025 it built {P['rivian'][0]:,.0f}: about a fifth. "
            f"<bookmark mark='b'/> Lucid's plant in Arizona has room for {P['lucid'][1]:,.0f}; it built "
            f"{P['lucid'][0]:,.0f}. <bookmark mark='c'/> Rivian's annual report puts the consequence plainly: running "
            "below capacity makes the cost of each vehicle much higher than it would be if the plant were full. That is "
            "where the losses per car of the last chapter come from."
        ) as vo:
            self.play(FadeIn(src), FadeIn(fac), FadeIn(ghost(g, opacity=0.3)))
            for mk, row in zip("ab", g):
                vo.wait_until(mk)
                self.play(FadeIn(row[:3]))
                self.play(GrowFromEdge(row[3], LEFT), FadeIn(row[4]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(quote))
        self.clear_scene()

    def worlds(self):
        P = R["plant"]
        L = P["launch"]
        names = ["weak", "as planned", "strong"]
        cols = [BAD, GOOD, GOOD]
        bars_ = VGroup()
        for i, (n, c) in enumerate(zip(names, cols)):
            v = L[n]["locked"]
            x = -3.0 + 3.0 * i
            h = v / 300
            b = Rectangle(width=1.4, height=abs(h), stroke_width=0, fill_color=c, fill_opacity=0.9).move_to([x, h / 2 - 0.6, 0])
            lab = tx(("+" if v > 0 else "-") + f"${abs(v):.0f}m", 20, c, bold=True).next_to(b, UP if v > 0 else DOWN, buff=0.1)
            nm = VGroup(tx(f"orders {n}", 17, WHITE, bold=True), tx(f"demand {L[n]['demand']:,.0f}", 14, GREY_A)).arrange(DOWN, buff=0.04).move_to([x, -2.8, 0])
            bars_.add(VGroup(b, lab, nm))
        base = Line([-4.5, -0.6, 0], [4.5, -0.6, 0], stroke_color=GREY_B, stroke_width=2)
        cap = DashedLine([3.8, -0.6 + L["strong"]["locked"] / 300, 0], [6.4, -0.6 + L["strong"]["locked"] / 300, 0], stroke_color=PRICE, stroke_width=2)
        capl = VGroup(tx("the line is full:", 14, PRICE), tx("extra orders are lost", 14, PRICE)).arrange(DOWN, buff=0.04).next_to(cap, DOWN, buff=0.1)
        head = tx("One launch, three possible worlds", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        tag = estimate_tag("the Works' model: a launch planned at 220,000 cars a year, two shifts", size=12)
        up_, down_ = L["strong"]["locked"] - L["as planned"]["locked"], L["as planned"]["locked"] - L["weak"]["locked"]
        with self.voiceover(
            "The same arithmetic makes every launch lopsided. <bookmark mark='a'/> Plan the model plant for two hundred "
            f"and twenty thousand cars a year. If the orders come in as planned, it makes about {L['as planned']['locked']:.0f} "
            f"million dollars. <bookmark mark='b'/> If they come in thirty per cent short, it loses {-L['weak']['locked']:.0f} "
            f"million: {down_:.0f} million worse than plan. <bookmark mark='c'/> If they come in thirty per cent above "
            f"plan, it makes only {up_:.0f} million more, because two shifts cannot build more than two hundred and fifty "
            "thousand cars, and a third crew would cost more than the extra cars earn. The bad surprises cost more than the "
            "good ones pay. That is the second answer to the film's question."
        ) as vo:
            self.play(FadeIn(base), FadeIn(head), FadeIn(tag), FadeIn(ghost(bars_, opacity=0.25)))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars_[1][0], DOWN), FadeIn(bars_[1][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars_[0][0], UP), FadeIn(bars_[0][1:]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars_[2][0], DOWN), FadeIn(bars_[2][1:]))
            self.play(Create(cap), FadeIn(capl))
        self.clear_scene()
