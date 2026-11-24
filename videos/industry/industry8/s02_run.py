from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403

PCOL = [GAS, BRENT, SHALE]


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: drill, wait or buy back", "You have a budget and three prospects. Which do you drill?",
             "Chapter one. Run it: drill, wait, or buy back.", lit=("make", "change"))
        self.offer()
        self.paths()

    def _cards(self):
        P = R["cost"]["prospects"]
        icons = [draw.pumpjack(1.6), draw.platform(1.9), draw.derrick(1.5)]
        cards = VGroup()
        for p, ic, col in zip(P, icons, PCOL):
            ic.scale_to_fit_height(1.3)
            box = RoundedRectangle(corner_radius=0.12, width=3.6, height=4.3, stroke_color=col, stroke_width=2,
                                   fill_color="#141A24", fill_opacity=1)
            cost = p["capex"] / 1000
            lines = VGroup(tx(p["name"], 21, col, bold=True),
                           tx(f"costs ${cost:.1f}bn" if cost >= 1 else f"costs ${p['capex']:.0f}m", 18, WHITE),
                           tx(f"first oil in {p['build']} year{'s' if p['build'] > 1 else ''}", 18, WHITE),
                           tx(f"{p['barrels']:.0f} million barrels in all" if p["barrels"] >= 10 else
                              f"{p['barrels']:.0f} million barrels in all", 18, WHITE),
                           tx(f"output falls {100 * p['decline']:.0f}% in year one", 18, WHITE),
                           tx(f"needs ${p['breakeven']:.0f} a barrel", 20, PRICE, bold=True)).arrange(
                DOWN, buff=0.12)
            inner = VGroup(ic, lines).arrange(DOWN, buff=0.25).move_to(box)
            cards.add(VGroup(box, inner))
        cards.arrange(RIGHT, buff=0.35).move_to([-1.0, -0.35, 0])
        buy = VGroup(RoundedRectangle(corner_radius=0.12, width=1.9, height=4.3, stroke_color=GREY_B, stroke_width=2,
                                      fill_color="#141A24", fill_opacity=1),
                     VGroup(draw.coin_stack(5, r=0.22), tx("or give the", 17, WHITE), tx("money back:", 17, WHITE),
                            tx("buy back", 19, GREY_A, bold=True), tx("shares", 19, GREY_A, bold=True)).arrange(
                         DOWN, buff=0.12)).next_to(cards, RIGHT, buff=0.35)
        buy[1].move_to(buy[0])
        return cards, buy

    def offer(self):
        cards, buy = self._cards()
        price = VGroup(tx("Oil today: $90 a barrel", 26, PRICE, bold=True)).to_edge(UP, buff=0.4)
        tag = estimate_tag("three model developments from the Works (oil.py), not any company's", corner=DR, size=14)
        P = R["cost"]["prospects"]
        with self.voiceover(
            "Play it yourself. You run an oil company, oil sells for ninety dollars a barrel, and you have three "
            "projects on the table. <bookmark mark='a'/> A conventional field on land: "
            f"{P[0]['capex']:.0f} million dollars, first oil in two years, and its wells fade slowly, by about a tenth "
            f"in their first year. It pays its way at about {P[0]['breakeven']:.0f} dollars a barrel. "
            "<bookmark mark='b'/> A deepwater platform: six billion dollars, five years before the first barrel, and "
            f"half a billion barrels after that. It needs about {P[1]['breakeven']:.0f}. <bookmark mark='c'/> A pad "
            "of ten shale wells: a hundred and twenty million dollars, oil within the year, but each well's output "
            f"falls by {100 * P[2]['decline']:.0f} percent in its first year. It needs about {P[2]['breakeven']:.0f}. "
            "<bookmark mark='d'/> Or you can drill nothing, and hand the money back to your shareholders. "
            "Pause, and choose. Remember that you are betting on the price of oil for as long as the project lasts."
        ) as vo:
            self.play(FadeIn(price), FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k], shift=UP * 0.2), run_time=1.0)
                if k == 0:
                    self.add(draw.nod(cards[0][1][0]))
            vo.wait_until("d")
            self.play(FadeIn(buy, shift=UP * 0.2))
        cards[0][1][0].clear_updaters()
        self.clear_scene()

    def paths(self):
        RR = R["run"]
        paths = np.array(RR["paths"])
        years = paths.shape[1]
        pa = viz.plot_axes([0, years - 1], [0, 220], x_length=6.0, y_length=4.0, xticks=[0, 5, 10, 15],
                           yticks=[50, 100, 150, 200], xfmt=lambda v: f"year {int(v)}", yfmt=lambda v: f"${v:g}",
                           size=13)
        pa.move_to([-3.4, -0.2, 0])
        lines = VGroup(*[VMobject(stroke_color=PRICE, stroke_width=1.4, stroke_opacity=0.45).set_points_as_corners(
            [pa.ax.c2p(t, min(v, 220)) for t, v in enumerate(p)]) for p in paths])
        head = tx("Forty of four hundred possible futures for the price", 18, GREY_A).next_to(pa, UP, buff=0.15)
        res = RR["results"]
        rows = VGroup()
        for k, (r_, col) in enumerate(zip(res, PCOL)):
            name = tx(r_["name"], 19, col, bold=True)
            loss = tx(f"loses money in {100 * r_['loss_share']:.0f}% of futures", 16, WHITE)
            per = tx(f"adds ${r_['per_dollar']:.2f} of value per dollar spent", 16, WHITE)
            pay = tx(f"pays back in {r_['payback_at_90']} years at $90", 16, GREY_B)
            rows.add(VGroup(name, loss, per, pay).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        rows.add(VGroup(tx("Buy back shares", 19, GREY_A, bold=True), tx("returns exactly the dollar", 16, WHITE)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.1, 0])
        tag = estimate_tag("the Works' model: 400 price paths drifting towards $70, discounted at 10% a year", corner=DR,
                           size=14)
        with self.voiceover(
            "Now let the price wander, as it does. <bookmark mark='a'/> Here are forty of four hundred futures for the "
            "price, each starting at ninety and drifting, with shocks every year, towards seventy. "
            "<bookmark mark='b'/> Run each project through all four hundred. The conventional field almost never "
            f"loses: on average, each dollar spent on it adds about {res[0]['per_dollar']:.1f} dollars of value, in "
            "today's money. <bookmark mark='c'/> The deepwater platform makes the most money in total, but you wait five "
            f"years for it, and in {100 * res[1]['loss_share']:.0f} percent of the futures it loses. "
            f"<bookmark mark='d'/> The shale pad loses in {100 * res[2]['loss_share']:.0f} percent, but you know within "
            "two years whether you were right, and you can stop. <bookmark mark='e'/> So the cheap, slow field is the "
            "prize, if you can get one, and the rest of this part shows who has them. The giant project is a bet on the "
            "price a decade away. The short project is the one you can stop. Every oil company is a mix of these "
            "three bets, and the price it assumes matters more than anything else it decides."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.04), run_time=4.0)
            for k, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=LEFT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(rows[3], shift=LEFT * 0.2))
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
        self.clear_scene()
