from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


def countdown(radius: float = 0.42) -> VGroup:
    t = ValueTracker(1.0)
    back = Circle(radius=radius, stroke_color=GREY_D, stroke_width=5)
    arc = always_redraw(lambda: Arc(radius=radius, start_angle=PI / 2, angle=-TAU * max(t.get_value(), 1e-3),
                                    stroke_color=E.ACCENT, stroke_width=5).move_arc_center_to(back.get_center()))
    g = VGroup(back, arc)
    g.t = t
    return g


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Play it: guess the price", r"Was Smith's market an accident of symmetry?",
             "Chapter four. Play it: guess the price.", lit={1962: r"Smith's double auction"},
             scale=("person", "market"), horizon=("a day",))
        self.worry()
        self.cards()
        self.reveal()
        self.trade()

    # ------------------------------------------------------------------
    def worry(self):
        q = quote_card(r"I thought perhaps that it was an accident of symmetry in the buyer and seller surpluses. I "
                       r"shot that idea down with an experiment later using a design in which the seller surplus was "
                       r"much greater than that of the buyers.", r"Vernon Smith, on his first market (2002)",
                       width=11.8, font_size=30, color=E.DEMAND).move_to(UP * 0.6)
        sym = label(r"Part 1's pit: \ the two staircases are mirror images", font_size=26, color=GREY_A)
        sym.next_to(q, DOWN, buff=0.6)
        src = published_tag(r"V. L. Smith, autobiography, Nobel Prize 2002", corner=DR, font_size=17)
        with self.voiceover(
            "Smith didn't trust his first result. <bookmark mark='a'/> I thought perhaps, he wrote, that it was an "
            "accident of symmetry in the buyer and seller surpluses. <bookmark mark='b'/> In Part one's pit, the "
            "buyers' staircase and the sellers' were close to mirror images, and the price landed in the middle. "
            "Maybe that's all convergence was: a market that happened to be balanced. <bookmark mark='c'/> So he "
            "ran a lopsided one, where the sellers stood to gain far more than the buyers. Let's run one too. This "
            "time you're the economist: you get to see everyone's card."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(sym))
            vo.wait_until("c")
            self.play(Indicate(q, color=E.DEMAND, scale_factor=1.02))
        self.clear_scene()

    def cards(self):
        d = load("playit")
        stage = game_stage(13.0, 6.8, center=DOWN * 0.1)
        bs = VGroup(*[trader_card("buy", x, width=0.92, font_size=19, show_rule=False) for x in d["values"]])
        ss = VGroup(*[trader_card("sell", x, width=0.92, font_size=19, show_rule=False) for x in d["costs"]])
        bs.arrange(RIGHT, buff=0.16)
        ss.arrange(RIGHT, buff=0.16)
        lb = label(r"10 buyers", font_size=24, color=E.DEMAND)
        ls = label(r"10 sellers", font_size=24, color=E.SUPPLY)
        rb = VGroup(lb, bs).arrange(RIGHT, buff=0.35)
        rs = VGroup(ls, ss).arrange(RIGHT, buff=0.35)
        rows = VGroup(rb, rs).arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to(stage.box.get_center() + UP * 1.15)
        q = VGroup(label(r"Same rules as the pit. \ Where will the price settle?", font_size=32, color=E.ACCENT),
                   label(r"\$0.50 \quad \dots \quad \$3.00", font_size=28, color=GREY_B)).arrange(DOWN, buff=0.2)
        q.move_to(stage.box.get_center() + DOWN * 1.65 + LEFT * 0.8)
        ring = countdown().next_to(q, RIGHT, buff=0.7)
        tag = illustrative_tag(r"a lopsided design in the spirit of Smith's: \ these cards are the series' own",
                               corner=UR, font_size=16)
        with self.voiceover(
            "Here are the cards. <bookmark mark='a'/> The ten buyers are all much alike: the keenest will pay up "
            "to two sixty, the least keen two fifteen. <bookmark mark='b'/> The sellers are spread out: the "
            "cheapest can sell for sixty cents, the dearest needs two eighty-five. <bookmark mark='c'/> The rules "
            "are the pit's rules: anyone may call out a bid or an offer, each trader trades once, and the market "
            "opens six times. Before it opens, make your guess. Where will the price settle? Pause if you like."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lb), LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in bs], lag_ratio=0.08), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(ls), LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in ss], lag_ratio=0.08), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.1), FadeIn(ring))
        self.play(ring.t.animate.set_value(0.0), run_time=4.0, rate_func=linear)
        guesses = VGroup(
            label(rf"the middle of all the cards: \ {dollars(d['guess_middle'])}", font_size=26, color=GREY_A),
            label(rf"the average card: \ {dollars(d['guess_mean'])}", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(q).align_to(q, LEFT)
        with self.voiceover(
            "Two guesses are tempting. <bookmark mark='a'/> The middle of the range of cards, which is "
            f"{money_words(d['guess_middle'])}. <bookmark mark='b'/> Or the average of all twenty cards, "
            f"{money_words(d['guess_mean'])}. Both feel fair. Neither is where this market goes."
        ) as vo:
            self.play(FadeOut(q), FadeOut(ring))
            vo.wait_until("a")
            self.play(FadeIn(guesses[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(guesses[1], shift=UP * 0.1))
        self.clear_scene()

    def reveal(self):
        d = load("playit")
        m = Market(tuple(d["values"]), tuple(d["costs"]))
        ax = price_axes(10, (0.5, 3.0), x_length=7.4, y_length=4.8, qticks=list(range(0, 11, 2)),
                        pticks=[0.5, 1, 1.5, 2, 2.5, 3], qlabel=r"units", plabel=r"price",
                        center=LEFT * 2.4 + DOWN * 0.35)
        a = ax.ax
        st = market_steps(a, m.steps())
        lo, hi, p, q = d["lo"], d["hi"], d["p"], d["q"]
        band = Rectangle(width=a.c2p(10, 0)[0] - a.c2p(0, 0)[0], height=max(a.c2p(0, hi)[1] - a.c2p(0, lo)[1], 0.04),
                         stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.3).move_to((a.c2p(0, lo) + a.c2p(10, hi)) / 2)
        v, c = m.v, m.c
        cs = VGroup(*[Rectangle(width=a.c2p(1, 0)[0] - a.c2p(0, 0)[0], height=max(a.c2p(0, x)[1] - a.c2p(0, p)[1], 0.01),
                                stroke_width=0, fill_color=E.CS, fill_opacity=0.45).move_to((a.c2p(k, p) + a.c2p(k + 1, x)) / 2)
                      for k, x in enumerate(v[:q])])
        ps = VGroup(*[Rectangle(width=a.c2p(1, 0)[0] - a.c2p(0, 0)[0], height=a.c2p(0, p)[1] - a.c2p(0, x)[1],
                                stroke_width=0, fill_color=E.PS, fill_opacity=0.35).move_to((a.c2p(k, x) + a.c2p(k + 1, p)) / 2)
                      for k, x in enumerate(c[:q])])
        right = VGroup(
            label(rf"{q} units trade", font_size=30, color=WHITE),
            label(rf"at {dollars(lo)} to {dollars(hi)}", font_size=28, color=E.ACCENT),
            label(rf"buyers keep \ {dollars(d['cs'])}", font_size=26, color=E.CS),
            label(rf"sellers keep \ {dollars(d['ps'])}", font_size=26, color=E.PS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5).shift(UP * 0.8)
        why = VGroup(label(r"ten buyers who are much alike", font_size=23, color=GREY_A),
                     label(r"compete the price up to them", font_size=23, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.1)
        why.next_to(right, DOWN, buff=0.45).align_to(right, LEFT)
        with self.voiceover(
            "Turn the cards into staircases. <bookmark mark='a'/> The buyers' staircase is nearly flat, because "
            "the buyers are so alike. The sellers' climbs steeply. <bookmark mark='b'/> They cross at "
            f"{q} units, and the band of prices that clears the market runs from {money_words(lo)} to "
            f"{money_words(hi)}: right up against the buyers' cards. <bookmark mark='c'/> At that price the buyers "
            f"keep only {money_words(d['cs'])} between them, and the sellers keep {money_words(d['ps'])}. "
            "<bookmark mark='d'/> Why so lopsided? Because there are more buyers willing to pay about two twenty-five "
            "than there are sellers who can sell at that price, and a buyer who holds out for less is simply "
            "replaced by one who won't. The competition is on the buyers' side, so the gains go to the sellers."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(st.demand), run_time=1.5)
            self.play(Create(st.supply), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(right[0:2], shift=LEFT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cs), FadeIn(right[2]))
            self.play(FadeIn(ps), FadeIn(right[3]))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.clear_scene()

    def trade(self):
        d = load("playit")
        shown = d["shown"]
        lo, hi = d["lo"], d["hi"]
        n = sum(len(p) for p in shown) + 2 * len(shown)
        ax = price_axes(n, (1.4, 2.8), x_length=11.0, y_length=4.2, qticks=None, pticks=[1.5, 2.0, 2.25, 2.5, 2.75],
                        qlabel="", plabel=r"price of each deal, \ every deal in order", center=DOWN * 0.3)
        a = ax.ax
        band = Rectangle(width=a.c2p(n, 0)[0] - a.c2p(0, 0)[0], height=a.c2p(0, hi)[1] - a.c2p(0, lo)[1],
                         stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.25).move_to((a.c2p(0, lo) + a.c2p(n, hi)) / 2)
        groups, seps, labels_ = [], VGroup(), VGroup()
        x = 1.0
        for k, prices in enumerate(shown):
            g = VGroup()
            for pr in prices:
                g.add(Dot(a.c2p(x, pr), radius=0.065, color=WHITE))
                x += 1
            groups.append(g)
            labels_.add(label(rf"period {k + 1}", font_size=18, color=GREY_B).next_to(a.c2p(x - len(prices) / 2 - 0.5, 1.4),
                                                                                     DOWN, buff=0.15))
            x += 1.0
            if k < len(shown) - 1:
                seps.add(DashedLine(a.c2p(x - 0.5, 1.4), a.c2p(x - 0.5, 2.8), color=GREY_D, stroke_width=1.5))
            x += 1.0
        alpha = VGroup(*[label(rf"{al:.1f}\%", font_size=19, color=E.AGORA).next_to(lab, DOWN, buff=0.1)
                         for al, lab in zip(d["shown_alpha"], labels_)])
        alpha_name = label(r"Smith's alpha:", font_size=19, color=E.AGORA).next_to(alpha[0], LEFT, buff=0.25)
        tag = agora_tag(rf"computed: Agora, learning traders; the median of {41} runs by final alpha", corner=DR,
                        font_size=16)
        zi = d["zi"]["price"]
        line_zi = DashedLine(a.c2p(0, zi), a.c2p(n, zi), color=GREY_B, stroke_width=2)
        zi_lab = label(rf"zero-intelligence traders settle near {dollars(zi)}", font_size=20, color=GREY_B)
        zi_lab.next_to(a.c2p(n, zi), DOWN, buff=0.1).align_to(a.c2p(n, zi), RIGHT)
        with self.voiceover(
            "Now let the traders loose. These are Agora's learning traders from Part one, who know only their own "
            f"cards. <bookmark mark='a'/> In the first period most deals are struck at about "
            f"{money_words(float(np.median(shown[0])))}, well below the band: the buyers' bids start low, and the "
            "cheap sellers take them. <bookmark mark='b'/> By the third period the deals are in or near the band, "
            f"and they stay there. Smith's coefficient of convergence falls from {d['shown_alpha'][0]:.0f} percent "
            f"to under {max(d['shown_alpha'][2:]) + 0.5:.0f}. <bookmark mark='c'/> So the lopsided market finds "
            "its price too, near the top of the buyers' cards, where the theory put it. That's what Smith found "
            "with his students. <bookmark mark='d'/> But notice the grey line. Traders with no intelligence, who "
            f"found the price in Part one's balanced pit, settle here around {money_words(zi)}, well below the "
            "band. In a lopsided market, zero intelligence isn't enough. The next chapter is about why."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(band), FadeIn(seps), FadeIn(labels_), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in groups[0]], lag_ratio=0.2), FadeIn(alpha_name),
                      FadeIn(alpha[0]), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in groups[1]], lag_ratio=0.2), FadeIn(alpha[1]),
                      run_time=1.2)
            vo.wait_until("b")
            for g, al in zip(groups[2:], alpha[2:]):
                self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in g], lag_ratio=0.15), FadeIn(al), run_time=0.9)
            vo.wait_until("c")
            self.play(Indicate(band, color=E.ACCENT, scale_factor=1.01))
            vo.wait_until("d")
            self.play(Create(line_zi), FadeIn(zi_lab))
        self.clear_scene()
