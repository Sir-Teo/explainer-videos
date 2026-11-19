from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


def card_back(width: float = 1.0) -> VGroup:
    h = width * 1.4
    box = RoundedRectangle(width=width, height=h, corner_radius=0.08, stroke_color=GREY_C, stroke_width=1.5,
                           fill_color="#1A2130", fill_opacity=1)
    q = label(r"?", font_size=width * 30, color=GREY_C).move_to(box)
    return VGroup(box, q)


def countdown(seconds_label: str = "", radius: float = 0.42) -> VGroup:
    t = ValueTracker(1.0)
    back = Circle(radius=radius, stroke_color=GREY_D, stroke_width=5)
    arc = always_redraw(lambda: Arc(radius=radius, start_angle=PI / 2, angle=-TAU * max(t.get_value(), 1e-3),
                                    stroke_color=E.ACCENT, stroke_width=5).move_arc_center_to(back.get_center()))
    g = VGroup(back, arc)
    g.t = t
    return g


class Pit(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: the pit", r"Where does a price come from, when nobody knows more than their own "
             r"card?", "Chapter one. Play it: the pit.", lit={1948: r"Chamberlin's classroom market",
                                                              1962: r"Smith's double auction"},
             scale=("person", "market"), horizon=("a day",))
        self.rules()
        self.predict()
        self.trade()
        self.reveal()
        self.what_did_it()
        self.fact()

    # ------------------------------------------------------------------
    def rules(self):
        d = load("pit")
        stage = game_stage(12.8, 6.6, center=DOWN * 0.15)
        backs_b = VGroup(*[card_back(0.82) for _ in range(10)]).arrange(RIGHT, buff=0.22)
        backs_s = VGroup(*[card_back(0.82) for _ in range(10)]).arrange(RIGHT, buff=0.22)
        lb = label(r"10 buyers", font_size=26, color=E.DEMAND)
        ls = label(r"10 sellers", font_size=26, color=E.SUPPLY)
        rowb = VGroup(lb, backs_b).arrange(RIGHT, buff=0.4)
        rows_ = VGroup(ls, backs_s).arrange(RIGHT, buff=0.4)
        table_ = VGroup(rowb, rows_).arrange(DOWN, buff=0.45, aligned_edge=RIGHT).move_to(stage.box.get_center() +
                                                                                           UP * 1.25)
        you = trader_card("buy", d["viewer_value"], you=True, width=1.55, font_size=32)
        you.move_to(stage.box.get_center() + DOWN * 1.75 + LEFT * 4.6)
        slot = backs_b[d["viewer"]]
        rules = VGroup(*[label(r, font_size=25, color=GREY_A) for r in (
            r"anyone may call out a bid or an offer, at any time",
            r"accept a standing bid or offer, \ and that is a deal",
            r"never pay more than your card, \ never sell for less than yours",
            r"each of you trades at most one unit; \ the market opens six times",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rules.next_to(you, RIGHT, buff=0.7).align_to(you, UP).shift(DOWN * 0.1)
        earn = label(rf"you earn \ \ {dollars(d['viewer_value'])} \ $-$ \ the price you pay", font_size=28,
                     color=E.ACCENT).next_to(rules, DOWN, buff=0.3).align_to(rules, LEFT)
        src = published_tag(r"the design of Vernon Smith (1962) and Edward Chamberlin (1948)", corner=DR,
                            font_size=18)
        with self.voiceover(
            "Let's begin with a game, and you're in it. <bookmark mark='a'/> There are twenty people in a room: ten "
            "buyers and ten sellers. Each of them has been handed a card, face down. <bookmark mark='b'/> Here's "
            f"yours. You're a buyer, and your card says {money_words(d['viewer_value'])}: that's the most this "
            "thing is worth to you. Nobody else can see it, and you can't see theirs. <bookmark mark='c'/> A "
            "seller's card says the least they'll take. <bookmark mark='d'/> The rules: anyone may call out a bid "
            "or an offer, at any time. If someone accepts a standing bid or offer, that's a deal. You may never pay "
            "more than your card, and a seller may never sell for less than theirs. Each person trades at most one "
            "unit, and when trading dies down the market closes and opens again, six times, with the same cards. "
            "<bookmark mark='e'/> If you buy, you keep the difference between your card and the price. "
            "<bookmark mark='f'/> This is the design of an experiment that Vernon Smith first ran with his "
            "students at Purdue in January 1956, after Edward Chamberlin had run a looser version at Harvard."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(table_, lag_ratio=0.05), run_time=1.6)
            vo.wait_until("b")
            self.play(slot.animate.set_stroke(E.ACCENT, 3))
            self.play(TransformFromCopy(slot, you), run_time=1.0)
            vo.wait_until("c")
            seller = trader_card("sell", d["costs"][0], width=0.82, font_size=17, show_rule=False)
            seller.move_to(backs_s[0])
            self.play(FadeTransform(backs_s[0], seller))
            self.play(Indicate(seller, color=E.SUPPLY))
            self.play(FadeTransform(seller, backs_s[0].copy()))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rules], lag_ratio=0.6), run_time=4)
            vo.wait_until("e")
            self.play(FadeIn(earn, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(src))
        self.stage, self.you = stage, you
        self.clear_scene()

    def predict(self):
        d = load("pit")
        stage = game_stage(10.0, 5.6)
        you = trader_card("buy", d["viewer_value"], you=True, width=1.55, font_size=32)
        you.move_to(stage.box.get_center() + LEFT * 3.2)
        q = VGroup(label(r"Before the market opens:", font_size=32, color=GREY_A),
                   label(r"what price will it settle at?", font_size=40, color=E.ACCENT),
                   label(r"\$1.00 \quad \dots \quad \$3.50", font_size=30, color=GREY_B))
        q.arrange(DOWN, buff=0.3).move_to(stage.box.get_center() + RIGHT * 1.4 + UP * 0.4)
        ring = countdown().next_to(q, DOWN, buff=0.45)
        with self.voiceover(
            "Before the market opens, make a prediction. Nobody here knows anyone else's card. What price do you "
            "think this market will settle at? Pick a number between one dollar and three fifty."
        ):
            self.play(FadeIn(stage), FadeIn(you), FadeIn(q[0]))
            self.play(FadeIn(q[1:], shift=UP * 0.1))
        self.add(ring)
        self.play(ring.t.animate.set_value(0.0), run_time=6.0, rate_func=linear)
        self.remove(ring)
        self.clear_scene()

    def trade(self):
        d = load("pit")
        periods = d["periods"]
        gap = 1.6
        xs, ys, viewer_pts, seps = [], [], [], []
        x = 0.6
        for k, p in enumerate(periods):
            seps.append(x - 0.8)
            for pr, v, c in p["trades"]:
                xs.append(x)
                ys.append(pr)
                if p["viewer_price"] is not None and abs(pr - p["viewer_price"]) < 1e-12:
                    viewer_pts.append(len(xs) - 1)
                x += 1.0
            x += gap
        x_max = x - gap + 0.4
        ax = axes([0, x_max], [1.0, 3.5], x_length=11.4, y_length=4.4, yticks=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5],
                  yfmt=lambda v: rf"\${v:.2f}", font_size=20, center=[0.35, 0.35, 0])
        ylab = label(r"price of each deal", font_size=22, color=GREY_A).next_to(ax.ax, UP, buff=0.15).align_to(
            ax.ax, LEFT)
        plabels = VGroup()
        sepl = VGroup()
        bounds = seps + [x_max + 0.4]
        for k in range(len(periods)):
            mid = (bounds[k] + bounds[k + 1]) / 2 + 0.2
            plabels.add(label(rf"period {k + 1}", font_size=19, color=GREY_B).move_to(ax.ax.c2p(mid, 1.0) +
                                                                                     DOWN * 0.3))
            if k:
                sepl.add(DashedLine(ax.ax.c2p(bounds[k], 1.0), ax.ax.c2p(bounds[k], 3.5), color=GREY_D,
                                    stroke_width=1.5))
        dots = VGroup(*[Dot(ax.ax.c2p(a, b), radius=0.06, color=WHITE) for a, b in zip(xs, ys)])
        rings = VGroup(*[Circle(radius=0.12, stroke_color=E.ACCENT, stroke_width=3).move_to(dots[i])
                         for i in viewer_pts])
        tag = agora_tag(r"computed: Agora, traders who adjust their margins (Cliff 1997); the median of 41 runs",
                        font_size=17)
        # Smith's coefficient of convergence per period
        alphas = [p["alpha"] for p in periods]
        bars = VGroup()
        for k, a in enumerate(alphas):
            mid = (bounds[k] + bounds[k + 1]) / 2 + 0.2
            h = 0.06 * a
            bars.add(Rectangle(width=0.7, height=max(h, 0.02), stroke_width=0, fill_color=E.AGORA, fill_opacity=0.85)
                     .move_to(ax.ax.c2p(mid, 1.0) + DOWN * (0.75 + h / 2)).align_to(ax.ax.c2p(mid, 1.0) + DOWN * 0.62,
                                                                                    UP))
        bar_vals = VGroup(*[label(rf"{a:.1f}", font_size=18, color=E.AGORA).next_to(b, RIGHT, buff=0.08)
                            for a, b in zip(alphas, bars)])
        alpha_lab = label(r"Smith's $\alpha$: \ how far prices stray from one another, in \% of the price",
                          font_size=18, color=E.AGORA).next_to(bars, DOWN, buff=0.12).align_to(ax.ax, LEFT)
        p1 = periods[0]["prices"]
        p3 = periods[2]["prices"]
        mine = [p["viewer_price"] for p in periods]
        with self.voiceover(
            "Now the market opens. Each dot is one deal, at the price it was struck. <bookmark mark='a'/> In the "
            f"first period, prices are all over the place: from {money_words(min(p1))} to "
            f"{money_words(max(p1))}. People are feeling their way. Your own deal is ringed: you paid "
            f"{money_words(mine[0])}. <bookmark mark='b'/> Then the market opens again with the same cards, and "
            "the deals start to bunch. <bookmark mark='c'/> By the third period, every price is within a few cents "
            f"of {money_words(np.mean(p3))}, and it stays there. <bookmark mark='d'/> Vernon Smith measured this "
            "with a single number, which he called alpha: how far the prices in a period stray, as a percentage of "
            f"the price they're converging to. Here it falls from {alphas[0]:.0f} percent in the first period to "
            f"about {np.median(alphas[2:]):.0f} percent. <bookmark mark='e'/> These traders are Agora's, the "
            "economy this series builds. Each one adjusts the margin it asks for after every call it hears: a "
            "simple model of what people do. This run is the median of forty-one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ylab), FadeIn(plabels), FadeIn(sepl), FadeIn(tag))
            n1 = len(periods[0]["trades"])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots[:n1]], lag_ratio=0.35), run_time=3)
            self.play(Create(rings[0]))
            vo.wait_until("b")
            n2 = n1 + len(periods[1]["trades"])
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots[n1:n2]], lag_ratio=0.3), run_time=2.2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in dots[n2:]], lag_ratio=0.1),
                      LaggedStart(*[Create(r) for r in rings[1:]], lag_ratio=0.2), run_time=3)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b in bars], lag_ratio=0.2), FadeIn(bar_vals),
                      FadeIn(alpha_lab), run_time=2.5)
        self.clear_scene()

    def reveal(self):
        d = load("pit")
        vals = sorted(d["values"], reverse=True)
        costs = sorted(d["costs"])
        ax = axes([0, 10], [1.0, 3.5], x_length=7.6, y_length=4.6, xticks=list(range(0, 11, 2)),
                  yticks=[1.0, 1.5, 2.0, 2.5, 3.0, 3.5], yfmt=lambda v: rf"\${v:.2f}",
                  xlabel=r"how many units", font_size=20, center=[-2.4, -0.25, 0])
        st = market_steps(ax.ax, d["steps"])
        b_cards = VGroup(*[trader_card("buy", v, width=0.62, font_size=14, show_rule=False,
                                       you=abs(v - d["viewer_value"]) < 1e-9) for v in vals])
        s_cards = VGroup(*[trader_card("sell", c, width=0.62, font_size=14, show_rule=False) for c in costs])
        b_cards.arrange(RIGHT, buff=0.12).to_edge(UP, buff=0.35)
        s_cards.arrange(RIGHT, buff=0.12).next_to(b_cards, DOWN, buff=0.18)
        lo, hi, q = d["p_lo"], d["p_hi"], d["q"]
        band = Rectangle(width=ax.ax.c2p(q, 0)[0] - ax.ax.c2p(0, 0)[0],
                         height=ax.ax.c2p(0, hi)[1] - ax.ax.c2p(0, lo)[1], stroke_width=0, fill_color=E.ACCENT,
                         fill_opacity=0.25)
        band.move_to((ax.ax.c2p(0, lo) + ax.ax.c2p(q, hi)) / 2)
        qline = DashedLine(ax.ax.c2p(q, 1.0), ax.ax.c2p(q, hi), color=GREY_B, stroke_width=2)
        p = d["p"]
        cs = VGroup(*[Rectangle(width=ax.ax.c2p(1, 0)[0] - ax.ax.c2p(0, 0)[0],
                                height=ax.ax.c2p(0, v)[1] - ax.ax.c2p(0, p)[1], stroke_width=0, fill_color=E.CS,
                                fill_opacity=0.3).move_to((ax.ax.c2p(k, p) + ax.ax.c2p(k + 1, v)) / 2)
                      for k, v in enumerate(vals[:q])])
        ps = VGroup(*[Rectangle(width=ax.ax.c2p(1, 0)[0] - ax.ax.c2p(0, 0)[0],
                                height=ax.ax.c2p(0, p)[1] - ax.ax.c2p(0, c)[1], stroke_width=0, fill_color=E.PS,
                                fill_opacity=0.3).move_to((ax.ax.c2p(k, c) + ax.ax.c2p(k + 1, p)) / 2)
                      for k, c in enumerate(costs[:q])])
        right = VGroup(
            label(rf"{q} units trade", font_size=30, color=WHITE),
            label(rf"at a price between {dollars(lo)} and {dollars(hi)}", font_size=26, color=E.ACCENT),
            label(rf"buyers' gain at {dollars(p)}: \ {dollars(d['cs'])}", font_size=24, color=E.CS),
            label(rf"sellers' gain: \ {dollars(d['ps'])}", font_size=24, color=E.PS),
            label(rf"the most any allocation can make: \ {dollars(d['surplus'])}", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ax, RIGHT, buff=0.5).shift(UP * 0.2)
        dl = label(r"demand: \ the buyers' cards, highest first", font_size=20, color=E.DEMAND)
        sl = label(r"supply: \ the sellers' cards, lowest first", font_size=20, color=E.SUPPLY)
        legend_ = VGroup(dl, sl).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(right, DOWN, buff=0.35)
        legend_.align_to(right, LEFT)
        mine = d["periods"][-1]["viewer_price"]
        with self.voiceover(
            "Now turn every card over. <bookmark mark='a'/> Line the buyers' cards up from the highest to the "
            "lowest, and the sellers' from the lowest to the highest. <bookmark mark='b'/> Then draw them as "
            "steps. The buyers' steps fall: at any price, they tell you how many buyers would want to buy. That's "
            "a demand curve. The sellers' steps rise, and they're a supply curve. <bookmark mark='c'/> They cross "
            f"at {q} units. The sixth buyer's card is {money_words(vals[q - 1])} and the sixth seller's is "
            f"{money_words(costs[q - 1])}; the seventh buyer won't pay more than {money_words(vals[q])}, and the "
            f"seventh seller won't take less than {money_words(costs[q])}. So any price between "
            f"{money_words(lo)} and {money_words(hi)} has exactly six buyers and six sellers willing. "
            "<bookmark mark='d'/> That's where the deals went: into the band, found by twenty people who never saw "
            f"each other's cards. <bookmark mark='e'/> And the gains: the buyers keep the blue area, the sellers "
            f"the amber, {money_words(d['surplus'])} in all, which is the most any arrangement of these twenty "
            f"people could make. In the last period you paid {money_words(mine)}, and kept "
            f"{money_words(d['viewer_value'] - mine)}."
        ) as vo:
            self.play(FadeIn(b_cards, lag_ratio=0.08), FadeIn(s_cards, lag_ratio=0.08), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(ax))
            self.play(Create(st.demand), b_cards.animate.set_opacity(0.35), run_time=2)
            self.play(Create(st.supply), s_cards.animate.set_opacity(0.35), run_time=2)
            self.play(FadeIn(legend_))
            vo.wait_until("c")
            self.play(FadeIn(band), Create(qline), FadeIn(right[0:2], shift=LEFT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(cs), FadeIn(ps), FadeIn(right[2:], shift=LEFT * 0.1), run_time=1.5)
        self.clear_scene()

    def what_did_it(self):
        d = load("pit")
        ch = study_card(r"Chamberlin's market (1948)", r"Harvard students, cards as here",
                        [(r"rules", r"bargain in pairs, wandering the room; one round"),
                         (r"found", r"more units traded than the competitive six, at scattered prices")],
                        design="lab", width=6.2, font_size=22).to_corner(UL, buff=0.4)
        sm = study_card(r"Smith's market (1962)", r"Purdue students, from 1956",
                        [(r"rules", r"every bid and offer called out to everyone; the market reopens"),
                         (r"found", r"prices converge on the crossing within a few periods")],
                        design="lab", width=6.2, font_size=22).to_corner(UR, buff=0.4)
        ax = axes([0.5, 6.5], [0, 20], x_length=5.4, y_length=2.7, xticks=[1, 2, 3, 4, 5, 6], yticks=[0, 10, 20],
                  xlabel=r"period", font_size=18, center=[-3.4, -2.0, 0])
        ax2 = axes([0.5, 6.5], [0.85, 1.0], x_length=5.4, y_length=2.7, xticks=[1, 2, 3, 4, 5, 6],
                   yticks=[0.85, 0.9, 0.95, 1.0], yfmt=lambda v: rf"{100 * v:.0f}\%", xlabel=r"period",
                   font_size=18, center=[3.6, -2.0, 0])
        per = np.arange(1, 7)
        za, ia = d["zip_alpha_median"], d["zi_alpha_median"]
        ze, ie = d["zip_eff_mean"], d["zi_eff_mean"]
        l_zip = curve(ax.ax, per, za, E.AGORA, 4)
        l_zi = curve(ax.ax, per, ia, GREY_B, 4)
        e_zip = curve(ax2.ax, per, ze, E.AGORA, 4)
        e_zi = curve(ax2.ax, per, ie, GREY_B, 4)
        t1 = label(r"$\alpha$: \ how scattered the prices are", font_size=20, color=GREY_A).next_to(ax.ax, UP,
                                                                                                 buff=0.12)
        t2 = label(r"efficiency: \ the share of the possible gains", font_size=20, color=GREY_A).next_to(ax2.ax, UP,
                                                                                                     buff=0.12)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=E.AGORA, stroke_width=5),
                            label(r"traders who learn", font_size=19, color=E.AGORA)).arrange(RIGHT, buff=0.12),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, color=GREY_B, stroke_width=5),
                            label(r"zero intelligence: \ random bids inside their cards", font_size=19,
                                  color=GREY_B)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.6)
        leg.move_to([0, 0.95, 0])
        tag = note(rf"computed: Agora; means and medians of {d['n_runs']} runs each", font_size=17,
                   color=E.AGORA).next_to(leg, DOWN, buff=0.18)
        with self.voiceover(
            "So what did the work? <bookmark mark='a'/> In 1948 Edward Chamberlin ran this game at Harvard, with "
            "one difference: his students wandered around the room and bargained in pairs, with nothing called out "
            "to everyone. His markets traded more units than the competitive quantity, at scattered prices, and he "
            "concluded that the textbook theory of competition didn't describe real markets. "
            "<bookmark mark='b'/> Vernon Smith played Chamberlin's game as a graduate student at Harvard in 1952. "
            "At Purdue he changed two things: every bid and offer was called out to the whole room, and the market "
            "opened again and again. His prices converged, and the line of work it started won him a Nobel prize in "
            "2002. <bookmark mark='c'/> Here is one way to see what the rules "
            "contribute. In 1993 Dhananjay Gode and Shyam Sunder replaced the people with traders who have no "
            "intelligence at all: each one calls out a random price, anywhere that wouldn't lose it money. "
            "<bookmark mark='d'/> "
            "Their prices never settle. Alpha stays around "
            f"{np.median(ia):.0f} percent, period after period. <bookmark mark='e'/> And yet they capture about "
            f"{100 * d['zi_eff_all']:.0f} percent of the gains, because the rules alone stop anyone trading at a "
            "loss and let the high-value buyers and low-cost sellers find each other first. "
            "<bookmark mark='f'/> Traders who learn do the rest. Their prices settle, and by the last period they "
            f"capture {100 * d['zip_eff_last']:.1f} percent. The institution gives you most of the efficiency; the "
            "learning gives you the price."
        ) as vo:
            self.play(FadeIn(ch, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(sm, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(ch.animate.scale(0.75).to_corner(UL, buff=0.3), sm.animate.scale(0.75).to_corner(UR, buff=0.3))
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(t1), FadeIn(t2), FadeIn(leg), FadeIn(tag))
            vo.wait_until("d")
            self.play(Create(l_zi), Create(e_zi), run_time=1.5)
            vo.wait_until("f")
            self.play(Create(l_zip), Create(e_zip), run_time=1.5)
        self.clear_scene()

    def fact(self):
        f = facts.BY_KEY["auctions_converge"]
        guess = label(r"(yours)", font_size=26, color=E.ACCENT)
        data_col = VGroup(label(r"Smith (1962):", font_size=22, color=WHITE),
                          label(r"prices converge on the", font_size=22, color=GREY_A),
                          label(r"crossing in a few periods", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.06)
        ag = VGroup(label(r"learning traders: \ yes, by", font_size=22, color=E.AGORA),
                    label(r"period 3; \ random traders:", font_size=22, color=E.AGORA),
                    label(r"most of the gains, no price", font_size=22, color=E.AGORA)).arrange(DOWN, buff=0.06)
        fc = fact_card(f.statement, columns=((r"your guess", guess), (r"the data", data_col), (r"Agora", ag)),
                       width=12.4).move_to(UP * 1.2)
        pay = payoff_card([(r"supply and demand, built from the cards", [2]),
                           (r"an economy-wide price system", [9]),
                           (r"auctions and the rules of a market", [16, 17])], font_size=22).scale(0.85)
        pay.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That's the first of the series' Facts: regularities that any account of an economy has to reproduce. "
            "Each one has three columns: your guess, the data, and what Agora does. <bookmark mark='a'/> The two "
            "staircases you just drew are the whole of next part's subject, where we build supply and demand from "
            "these cards. The same question, scaled up to a whole economy of prices, comes in Part nine, and the "
            "rules of a market, designed on purpose, in Parts sixteen and seventeen."
        ) as vo:
            self.play(FadeIn(fc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(pay, shift=UP * 0.2))
        self.clear_scene()
