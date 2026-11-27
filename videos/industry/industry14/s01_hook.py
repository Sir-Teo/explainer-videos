from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.stink()
        self.eighteen()
        self.falls()
        self.title()

    def stink(self):
        river = VGroup()
        for k in range(4):
            wv = FunctionGraph(lambda x, k=k: -1.9 - 0.32 * k + 0.06 * np.sin(2.2 * x + k), x_range=[-7.2, 7.2],
                               color=interpolate_color(ManimColor("#6B7A4A"), ManimColor("#4E5A3A"), k / 3), stroke_width=10)
            river.add(wv)
        water = Rectangle(width=14.4, height=1.7, stroke_width=0, fill_color="#46523A", fill_opacity=1).move_to([0, -2.75, 0])
        bank = Rectangle(width=14.4, height=0.12, stroke_width=0, fill_color="#5B4A36", fill_opacity=1).move_to([0, -1.62, 0])
        houses = VGroup(*[draw.house(0.55, "#B9B2A3").move_to([x, -1.25, 0]) for x in (-6.2, -5.4, -4.6, 2.3, 3.1, 3.9, 4.7)])
        parl = draw.castle(2.6, "#C9BFA6").move_to([-1.5, -0.95, 0])
        parl_l = tx("the Houses of Parliament", 15, GREY_A).next_to(parl, UP, buff=0.12)
        outfalls = VGroup(*[Line([h.get_center()[0] + 0.2, -1.5, 0], [h.get_center()[0] + 0.2, -1.95, 0], stroke_color=SEWAGE,
                                 stroke_width=5) for h in houses])
        blobs = VGroup(*[Dot([h.get_center()[0] + 0.2 + 0.3 * j, -2.05 - 0.15 * j, 0], radius=0.06, color=SEWAGE)
                         for h in houses for j in range(3)])
        fumes = VGroup(*[Circle(radius=0.22 + 0.06 * (k % 3), stroke_width=0, fill_color="#8C9A5A", fill_opacity=0.35).move_to(
            [-6.5 + 0.95 * k, -1.8 + 0.1 * (k % 2), 0]) for k in range(14)])
        base = [f.get_center().copy() for f in fumes]
        clock = {"t": 0.0}

        def drift(m, dt):
            clock["t"] += dt
            for k, c in enumerate(m):
                ph = (clock["t"] * 0.18 + (k * 0.37) % 1.0) % 1.0
                c.move_to(base[k] + UP * 2.4 * ph + RIGHT * 0.2 * np.sin(5 * ph + k))
                c.set_fill(opacity=0.4 * np.sin(PI * ph))
        when = VGroup(tx("London, July 1858", 26, WHITE, bold=True),
                      tx("the summer the river began to stink", 17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_corner(UL, buff=0.45)
        quote = VGroup(tx("'That noble river ... has really become a Stygian pool,", 17, WHITE),
                       tx("reeking with ineffable and intolerable horrors.'", 17, WHITE),
                       tx("Benjamin Disraeli, House of Commons, 15 July 1858", 14, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        quote.to_corner(UR, buff=0.45)
        src = source("Hansard, HC Deb 15 July 1858 vol 151 cc1508-40", size=13)
        with self.voiceover(
            "London, July 1858. <bookmark mark='a'/> A few years earlier, Parliament had decided, in the words of the "
            "man who now led the House of Commons, that 'the sewage of the metropolis should be diverted to the waters "
            "of the Thames'. <bookmark mark='b'/> Now it was summer, and the river ran past Parliament's own windows. "
            "<bookmark mark='c'/> On the fifteenth of July, Benjamin Disraeli rose and told the House that the Thames had "
            "'really become a Stygian pool, reeking with ineffable and intolerable horrors'. Almost every living thing in "
            "it, he said, had disappeared, and there was 'a pervading apprehension of pestilence in this great city'."
        ) as vo:
            self.play(FadeIn(water), FadeIn(river), FadeIn(bank), FadeIn(when), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(h, shift=UP * 0.1) for h in houses], lag_ratio=0.08), FadeIn(parl), FadeIn(parl_l))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(o) for o in outfalls], lag_ratio=0.08), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in blobs], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("b")
            self.add(fumes)
            fumes.add_updater(drift)
            self.play(river.animate.set_color("#556035"), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(quote, shift=DOWN * 0.1))
            self.wait(3)
        fumes.clear_updaters()
        self.clear_scene()

    def eighteen(self):
        H = R["hook"]
        start = VGroup(tx("15 July 1858", 30, WHITE, bold=True), tx("Disraeli asks leave to bring in a bill", 16, GREY_A)).arrange(
            DOWN, buff=0.08).move_to([-4.0, 1.6, 0])
        end = VGroup(tx("2 August 1858", 30, GOOD, bold=True), tx("royal assent: 'the Act ... for the Purification", 16, GREY_A),
                     tx("of that noble River'", 16, GREY_A)).arrange(DOWN, buff=0.06).move_to([4.0, 1.6, 0])
        line = Line([-4.0, 0.6, 0], [4.0, 0.6, 0], stroke_color=GREY_B, stroke_width=3)
        ticks = VGroup(*[Line([-4.0 + 8.0 * d / 18, 0.5, 0], [-4.0 + 8.0 * d / 18, 0.7, 0], stroke_color=GREY_B, stroke_width=2)
                         for d in range(19)])
        t = ValueTracker(0)
        dot = always_redraw(lambda: Dot([-4.0 + 8.0 * t.get_value() / 18, 0.6, 0], radius=0.1, color=PRICE))
        days_n = draw.number(lambda: t.get_value(), 0, size=40, color=PRICE)
        days_n.add_updater(lambda m: m.move_to([-0.45, -0.2, 0], aligned_edge=RIGHT))
        days = VGroup(days_n, tx("days", 32, PRICE, bold=True).move_to([-0.3, -0.2, 0], aligned_edge=LEFT))
        cost = VGroup(tx(f"£{H['cost']:.0f},000,000", 44, WHITE, bold=True), tx("Disraeli's estimate of the cost of the main drainage", 16, GREY_A)).arrange(
            DOWN, buff=0.08).move_to([-3.4, -2.0, 0])
        pay = VGroup(tx(f"{H['rate']:.0f}d in the pound, for {H['years']:.0f} years", 30, WHITE, bold=True),
                     tx("a rate on the property of London", 16, GREY_A)).arrange(DOWN, buff=0.08).move_to([3.4, -2.0, 0])
        src = source("Hansard, HC Deb 15 July 1858 vol 151 cc1508-40; HL Deb 2 August 1858 (the Lords Commissioners' speech)", size=13)
        with self.voiceover(
            "What happened next was fast. <bookmark mark='a'/> "
            "Disraeli asked for leave to bring in a bill on the fifteenth of July. <bookmark mark='b'/> On the second of "
            "August, the Queen's commissioners told both Houses she had 'readily sanctioned the Act ... for the "
            f"Purification of that noble River'. Eighteen days. <bookmark mark='c'/> The cost, Disraeli said, 'cannot, "
            f"indeed, be computed at much less than three million pounds'. <bookmark mark='d'/> It would be paid by a "
            f"rate of no more than threepence in the pound on London's property, for forty years: a bill, spread over "
            "two generations, for pipes meant to last far longer."
        ) as vo:
            self.play(FadeIn(src), Create(line), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(start, shift=DOWN * 0.1))
            self.add(dot, days)
            vo.wait_until("b")
            self.play(t.animate.set_value(18), run_time=3.0, rate_func=linear)
            self.play(FadeIn(end, shift=DOWN * 0.1), Indicate(days, color=PRICE))
            vo.wait_until("c")
            self.play(FadeIn(cost, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(pay, shift=UP * 0.1))
        days_n.clear_updaters()
        self.clear_scene()

    def falls(self):
        H = R["hook"]["falls"]
        order = ["SEHG01", "SEHG02", "SEHA", "SA0", "SEHF01", "SEHF02"]
        y0, y1 = 1954, 2025
        n = y1 - y0 + 1
        cw = 8.0 / n
        rows = VGroup()
        for i, k in enumerate(order):
            f = H[k]
            y = 2.0 - 0.78 * i
            cells = VGroup()
            for j, yr in enumerate(range(y0, y1 + 1)):
                if yr <= f["start"]:
                    col, op = "#2A3140", 0.6
                elif yr in f["years"]:
                    col, op = BAD, 1.0
                else:
                    col, op = SERIES_COL[k], 0.75
                cells.add(Rectangle(width=cw * 0.82, height=0.42, stroke_width=0, fill_color=col, fill_opacity=op).move_to(
                    [-3.4 + cw * (j + 0.5), y, 0]))
            name = tx(f["name"], 17, SERIES_COL[k], bold=True).next_to([-3.5, y, 0], LEFT, buff=0.1)
            cnt = tx(f"fell in {f['n']} years" if f["n"] else "never fell", 17, BAD if f["n"] else WHITE, bold=True).move_to(
                [4.85, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(name, cells, cnt))
        axis = VGroup(*[tx(str(yr), 13, GREY_B).move_to([-3.4 + cw * (yr - y0 + 0.5), 2.45, 0]) for yr in (1954, 1970, 1990, 2010, 2025)])
        head = tx("Each year since 1953: did the US price index fall?", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=BAD, fill_opacity=1), tx("a year the price fell", 14, GREY_A)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.2, stroke_width=0, fill_color="#2A3140", fill_opacity=1), tx("no index yet", 14, GREY_A)).arrange(RIGHT, buff=0.08)).arrange(
            RIGHT, buff=0.5).to_edge(DOWN, buff=0.75)
        src = source("BLS, consumer price indexes, US city average, annual averages (rubbish collection from 1984)", size=13)
        w, g = H["SEHG01"], H["SEHG02"]
        with self.voiceover(
            "Hold that thought: pipes paid for over decades. Now jump to America today, and ask a simple question of each "
            "household bill: in how many years since 1953 did its price fall? <bookmark mark='a'/> Water and sewerage: "
            f"not once in seventy-two years. <bookmark mark='b'/> Rubbish collection, measured since 1984: not once. "
            "<bookmark mark='c'/> Rent shares that record. <bookmark mark='d'/> Prices in general fell in "
            f"{H['SA0']['n']} years. <bookmark mark='e'/> Electricity fell in {H['SEHF01']['n']}, and piped gas in "
            f"{H['SEHF02']['n']}. The bills nobody thinks about are the ones that have only ever gone one way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(key), FadeIn(src), *[FadeIn(r_[0]) for r_ in rows])
            for m_, i in zip("abcde", (0, 1, 2, 3, 4)):
                vo.wait_until(m_)
                idx = (i,) if m_ != "e" else (4, 5)
                for ii in idx:
                    self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in rows[ii][1]], lag_ratio=0.01), run_time=1.3)
                    self.play(FadeIn(rows[ii][2], shift=LEFT * 0.1), run_time=0.5)
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover(
            "Water comes in through pipes built to last for generations, and leaves through sewers built the same way. Rubbish leaves "
            "in a truck and ends in a hole in the ground that nobody wants next door. Industry, Built. Part fourteen: "
            "water and waste. Why are the businesses nobody thinks about among the steadiest there are?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
