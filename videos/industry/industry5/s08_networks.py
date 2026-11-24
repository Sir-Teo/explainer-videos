from __future__ import annotations

from videos.industry.industry5.common import *  # noqa: F403


class Networks(VoiceoverScene):
    def construct(self):
        card(self, 10, "Walls of networks and law", "When does each new customer make the castle stronger?",
             "Chapter ten. Walls of networks and law.", lit=("moat",))
        self.network()
        self.two()
        self.law()

    def two(self):
        M = R["margins"]["V"]["points"]
        MA = R["mastercard"]["points"]
        pa = viz.plot_axes([2008.5, 2026.5], [0, 0.75], x_length=8.0, y_length=3.4, xticks=[2010, 2014, 2018, 2022, 2026],
                           yticks=[0.25, 0.5, 0.75], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}%",
                           size=15)
        pa.move_to([1.6, -1.0, 0])
        lv = VMobject(stroke_color=GOLD, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, v) for y, v in M])
        lm = VMobject(stroke_color=ENTRANT, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, v) for y, v in MA])
        tv = tx("Visa", 20, GOLD, bold=True).next_to(pa.ax.c2p(*M[-1]), RIGHT, buff=0.12)
        tm = tx("Mastercard", 20, ENTRANT, bold=True).next_to(pa.ax.c2p(*MA[-1]), RIGHT, buff=0.12)
        head = tx("operating profit per dollar of sales, each year", 17, GREY_A).next_to(pa, UP, buff=0.12).align_to(
            pa, LEFT)
        keeps = VGroup(draw.castle(1.3, moat=0.45, color="#F6C453"), draw.castle(1.3, moat=0.45, color=ENTRANT)).arrange(
            RIGHT, buff=0.6).move_to([-4.6, 1.6, 0])
        names = VGroup(tx("Visa", 18, GOLD), tx("Mastercard", 18, ENTRANT))
        for n_, k_ in zip(names, keeps):
            n_.next_to(k_, DOWN, buff=0.12)
        cards = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.5, height=0.32, stroke_width=0,
                                          fill_color=c, fill_opacity=0.95) for c in ("#2B4C9B", "#C0392B") * 4])
        cards.arrange_in_grid(rows=2, cols=4, buff=0.08).move_to([-4.6, -1.4, 0])
        ct = tx("the same shops, the same shoppers", 15, GREY_B).next_to(cards, DOWN, buff=0.15)
        src = source("Forms 10-K of Visa and Mastercard, fiscal 2009-2026 (SEC company facts)", size=13)
        last = R["mastercard"]["last"]
        with self.voiceover(
            "A network can hold more than one castle. <bookmark mark='a'/> Visa has a rival with the same kind of "
            "network: Mastercard. The two compete for the same shops and the same shoppers. You might expect them to "
            "fight each other down to thin margins. <bookmark mark='b'/> They have not. Here is the share of each "
            "dollar of sales that Visa keeps as operating profit, every year since 2009, <bookmark mark='c'/> and "
            f"here is Mastercard's: {100 * last[1]:.0f} cents in {last[0]}. Two firms, side by side, both earning "
            "more than half of what they take in. <bookmark mark='d'/> Remember the two conditions from chapter "
            "seven: something keeps newcomers out, and the few do not fight. Here the network keeps newcomers out, "
            "since a new card is useless until shops take it, and shops will not take it until shoppers carry it. "
            "And the fees land mostly on shops, which cannot easily refuse the cards their customers carry, so the "
            "two have little reason to fight over them."
        ) as vo:
            self.play(FadeIn(src), FadeIn(keeps[0], shift=UP * 0.2), FadeIn(names[0]))
            vo.wait_until("a")
            self.play(FadeIn(keeps[1], shift=UP * 0.2), FadeIn(names[1]),
                      LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in cards], lag_ratio=0.1), FadeIn(ct))
            vo.wait_until("b")
            self.play(FadeIn(pa), FadeIn(head), Create(lv), run_time=2.0)
            self.play(FadeIn(tv))
            vo.wait_until("c")
            self.play(Create(lm), run_time=2.0)
            self.play(FadeIn(tm))
            vo.wait_until("d")
            self.play(Indicate(keeps, color=WHITE, scale_factor=1.04))
        self.clear_scene()

    def network(self):
        V = R["visa"]
        n_max = 12
        rng = np.random.default_rng(5)
        pos = [np.array([2.2 * np.cos(a) - 3.3, 2.2 * np.sin(a) - 0.2, 0]) for a in
               np.linspace(PI / 2, PI / 2 + TAU, n_max, endpoint=False)]
        nodes = VGroup(*[Dot(p, radius=0.11, color=GOLD) for p in pos])
        n = ValueTracker(2)

        def links():
            k = int(round(n.get_value()))
            g = VGroup()
            for i in range(k):
                for j in range(i + 1, k):
                    g.add(Line(pos[i], pos[j], stroke_color="#7EC8F5", stroke_width=1.6, stroke_opacity=0.7))
            return g
        web = always_redraw(links)
        shown = always_redraw(lambda: VGroup(*[nodes[i] for i in range(int(round(n.get_value())))]))
        cnt = draw.number(lambda: round(n.get_value()), 0, size=38, color=GOLD)
        cnt.add_updater(lambda m: m.move_to([1.4, 1.6, 0]), call_updater=True)
        cnt_t = tx("users", 18, GREY_B).move_to([1.4, 1.05, 0])
        lk = draw.number(lambda: (lambda k: k * (k - 1) // 2)(round(n.get_value())), 0, size=38, color="#7EC8F5")
        lk.add_updater(lambda m: m.move_to([1.4, 0.1, 0]), call_updater=True)
        lk_t = tx("possible connections", 18, GREY_B).move_to([1.4, -0.45, 0])
        law = MathTex(r"\frac{n(n-1)}{2}", font_size=44).move_to([1.4, -1.4, 0])
        visa = VGroup(tx("Visa, fiscal 2026", 24, WHITE, bold=True),
                      tx(f"revenue ${V['rev']:.1f}bn", 20, GREY_A),
                      tx(f"operating profit ${V['oi']:.1f}bn", 20, RET),
                      tx(f"{100 * V['margin']:.0f} cents of each dollar", 30, RET, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.9, 0.6, 0])
        two = tx("two sides: more cardholders bring more shops; more shops, more cardholders", 18, GREY_A).to_edge(
            DOWN, buff=0.45)
        src = source("Visa Form 10-K, fiscal year to September 2026", corner=DR)
        del rng
        with self.voiceover(
            "The third kind of wall gets higher the more customers come. <bookmark mark='a'/> A network of two "
            "users has one connection. <bookmark mark='b'/> Add users one at a time, and the possible connections "
            "grow much faster than the users: twelve users, sixty-six connections. Each newcomer is worth more to "
            "join the big network than the small one, so the big one gets bigger. <bookmark mark='c'/> A payment "
            "card works this way twice over. Shoppers want the card that every shop takes; shops take the card that "
            "every shopper carries. <bookmark mark='d'/> Visa does not lend money or issue the cards: it runs the "
            f"network between banks, shops and shoppers. In fiscal 2026 it turned {V['rev']:.0f} billion dollars "
            f"of revenue into {V['oi']:.0f} billion of operating profit: {100 * V['margin']:.0f} cents of every "
            "dollar. A rival with a better card would still have to sign up millions of shops and shoppers, each of "
            "whom wants the other to come first. Markets like this tend to tip: once one network is ahead, the gap "
            "feeds itself, and the second network shrinks rather than catches up. That is why so many of them end "
            "with one or two winners, and why their owners will spend heavily to be first."
        ) as vo:
            self.add(web, shown)
            self.play(FadeIn(cnt), FadeIn(cnt_t), FadeIn(lk), FadeIn(lk_t), FadeIn(src))
            vo.wait_until("a")
            self.play(Write(law))
            vo.wait_until("b")
            self.play(n.animate.set_value(n_max), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(two, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(visa, shift=LEFT * 0.2))
        for m in (cnt, lk):
            m.clear_updaters()
        self.clear_scene()

    def law(self):
        term = 20
        keep = draw.castle(1.9, moat=0.5).move_to([-3.2, 0.6, 0])
        clock = ValueTracker(0)
        bar_bg = RoundedRectangle(corner_radius=0.08, width=6.0, height=0.34, stroke_color=GREY_D, stroke_width=1.5,
                                  fill_opacity=0).move_to([0.3, -2.2, 0])
        bar = always_redraw(lambda: Rectangle(width=max(6.0 * (1 - clock.get_value() / term), 0.001), height=0.34,
                                              stroke_width=0, fill_color=MOAT, fill_opacity=0.9).move_to(
            bar_bg.get_left(), aligned_edge=LEFT))
        yrs = draw.number(lambda: term - clock.get_value(), 0, suffix=" years left", size=30, color=WHITE)
        yrs.add_updater(lambda m: m.next_to(bar_bg, UP, buff=0.15), call_updater=True)
        title = tx("A patent: 20 years from filing", 22, MOAT, bold=True).next_to(bar_bg, DOWN, buff=0.2)
        copies = VGroup(*[draw.castle(0.7, color=ENTRANT) for _ in range(5)]).arrange(RIGHT, buff=0.15).move_to(
            [3.6, 0.4, 0])
        price = ValueTracker(1.0)
        tag = always_redraw(lambda: VGroup(RoundedRectangle(corner_radius=0.08, width=1.3, height=0.5, stroke_width=0,
                                                            fill_color=GOLD, fill_opacity=1),
                                           tx("price", 18, "#0E1117", bold=True)).scale(price.get_value()).move_to(
            [-3.2, 2.7, 0]))
        others = VGroup(tx("licences: a TV channel, a bank charter, a taxi medallion", 17, GREY_B),
                        tx("rights to scarce things: airport slots, radio spectrum", 17, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR, buff=0.4)
        src = source("35 U.S.C. 154 (patent term); the picture is illustrative", corner=DL)
        with self.voiceover(
            "The fourth kind of wall is built by law. <bookmark mark='a'/> A patent gives an inventor the sole right "
            "to an invention for twenty years from the day the application is filed. Inside that wall the price can "
            "sit far above the cost of one more, which is how a new medicine can sell for many times what a pill "
            "costs to make. <bookmark mark='b'/> But this wall has a date on it. <bookmark mark='c'/> When the "
            "patent runs out, copies arrive, and the price falls towards the cost of making them. "
            "<bookmark mark='d'/> Licences and rights to scarce things work the same way without the expiry date: a "
            "broadcast licence, a bank charter, a slot to land at a crowded airport, a slice of the radio spectrum. "
            "Whoever holds one holds a piece of a market that others are not allowed to enter."
        ) as vo:
            self.play(FadeIn(keep, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bar_bg), FadeIn(bar), FadeIn(yrs), FadeIn(title), FadeIn(tag))
            vo.wait_until("b")
            self.play(clock.animate.set_value(term), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(keep.moat.animate.set_opacity(0.1),
                      LaggedStart(*[FadeIn(c_, shift=LEFT * 0.4) for c_ in copies], lag_ratio=0.2),
                      price.animate.set_value(0.45), run_time=2.4)
            vo.wait_until("d")
            self.play(FadeIn(others, shift=LEFT * 0.2))
        yrs.clear_updaters()
        self.clear_scene()
