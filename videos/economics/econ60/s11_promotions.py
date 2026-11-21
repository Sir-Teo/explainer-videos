from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Promotions(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Promotions, \ reference prices and hidden fees", r"Why would a store raise its regular "
             r"price \ just to cut it again?", "Chapter nine. Promotions, reference prices and hidden fees.",
             lit={2012: r"fair and square", 2021: r"StubHub's fees", 2025: r"the FTC's fee rule"},
             scale=("person", "firm"), horizon=("a week", "a year"))
        self.hilo()
        self.fees()

    def hilo(self):
        H = load("hilo")
        etas, diff = np.array(H["etas"]), np.array(H["diff"]) / 1e3
        weeks = np.arange(12)
        ax = plane([0, 12], [0, 60], center=LEFT * 3.0 + UP * 1.2, x_length=5.6, y_length=2.4,
                   xticks=[0, 4, 8, 12], yticks=[0, 20, 40, 60], xlabel=r"week", ylabel=r"price, \ \$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        hl = [50.0 if w % 2 == 0 else 35.0 for w in weeks]
        xs, ys = [], []
        for w, p in zip(weeks, hl):
            xs += [w, w + 1]
            ys += [p, p]
        hil = path(ax, xs, ys, BUS, 2.8, smooth=False)
        ed = path(ax, [0, 12], [40, 40], LEIS, 2.8, smooth=False)
        key = VGroup(label(r"gold: \ high-low, \ \$50 with a sale at \$35 every other week", font_size=14,
                           color=BUS),
                     label(r"green: \ everyday low price, \ \$40", font_size=14, color=LEIS)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).next_to(ax, DOWN, buff=0.45).align_to(ax, LEFT)
        bx = plane([0, 1.5], [-150, 200], center=LEFT * 3.0 + DOWN * 2.5, x_length=5.6, y_length=2.0,
                   xticks=[0, 0.5, 1.0, 1.5], yticks=[-100, 0, 100, 200],
                   xlabel=r"how much shoppers value a deal, \ $\eta$", ylabel=r"high-low minus EDLP, \ \$000",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   font_size=12)
        z = DashedLine(bx.ax.c2p(0, 0), bx.ax.c2p(1.5, 0), color=GREY_C, stroke_width=1.2)
        dc = path(bx, etas, diff, OPT, 2.6, smooth=False)
        side = VGroup(
            MathTex(r"u = v - p + \eta\,\max(r - p, 0)", font_size=30, color=WHITE),
            label(r"$r$: \ the reference price, \ here the posted regular price", font_size=18, color=GREY_A),
            label(rf"with $\eta = {H['eta']}$: \ high-low earns \${H['revenue_hilo'] / 1e3:,.0f} thousand a year, \\ "
                  rf"everyday low prices \${H['revenue_edlp'] / 1e3:,.0f} thousand".replace(",", "{,}"),
                  font_size=19, color=OPT),
            label(r"a sale that is felt as a deal sells more than \\ the same price every day", font_size=19,
                  color=BUS),
            label(r"2012: \ J.C. Penney replaced its sales and coupons \\ with `fair and square' everyday prices "
                  r"\ (chapter fifteen)", font_size=18, color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.4:
            side.width = 6.4
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ a store's shoppers; \ agora.revenue.hilo", corner=DL, font_size=12)
        with self.voiceover(
            "Supermarkets and department stores have long run high-low pricing: a high regular price, frequently "
            "cut. <bookmark mark='a'/> Here is the Island's store: fifty dollars, with a sale at thirty-five every "
            "other week, against an everyday price of forty. On a plain model of demand, everyday low prices should "
            "win. <bookmark mark='b'/> But suppose shoppers also enjoy a deal: they compare the price with a "
            "reference price, here the posted regular price, and value the gap. <bookmark mark='c'/> With a weight "
            f"of {H['eta']} on that gain, high-low earns {H['revenue_hilo'] / 1e3:,.0f} thousand dollars a year and "
            f"everyday low prices {H['revenue_edlp'] / 1e3:,.0f} thousand. <bookmark mark='d'/> The more shoppers "
            "value the deal, the more high-low wins; with no taste for deals, everyday low prices win. The regular "
            "price is not only a price, it is the reference that makes the sale feel like one. <bookmark mark='e'/> "
            "In 2012 J.C. Penney bet the other way, as chapter fifteen will tell."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(hil), Create(ed), FadeIn(key), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(bx), Create(z), Create(dc), FadeIn(side[3]), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def fees(self):
        cards = VGroup(
            history_card(r"\$3.99", r"prices ending in nines", r"Part 45: \ buyers read the left digit first; \ "
                         r"a price of \$3.99 feels nearer 3 than 4", color=GREY_A, width=11.4, font_size=20),
            history_card(2021, r"Blake, \ Moshary, \ Sweeney and Tadelis, \ StubHub", r"half of buyers saw ticket "
                         r"fees only at checkout: \ they spent about a fifth more, \ and bought pricier seats",
                         color=COST, width=11.4, font_size=20),
            history_card(2025, r"the Federal Trade Commission's fee rule", r"in force from May: \ live-event tickets "
                         r"and short-term lodging must show the total price, \ fees included, \ up front",
                         color=AIR, width=11.4, font_size=20),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        tag = published_tag(r"Blake, \ Moshary, \ Sweeney and Tadelis, \ Marketing Science 40(4) (2021); \ FTC, \ "
                            r"Rule on Unfair or Deceptive Fees (2024)", corner=DL, font_size=12)
        with self.voiceover(
            "How a price is shown matters as much as its level. <bookmark mark='a'/> Prices ending in nines exploit "
            "the way buyers read the left digit first, as Part forty-five measured. <bookmark mark='b'/> Drip "
            "pricing hides part of the price until the end. In an experiment on StubHub, half of buyers saw the "
            "ticket fees only at checkout; they spent about a fifth more than those shown the full price from the "
            "start, partly by choosing more expensive seats. <bookmark mark='c'/> In December 2024 the Federal Trade "
            "Commission adopted a rule, in force from May 2025, requiring sellers of live-event tickets and "
            "short-term lodging to show the total price, fees included, up front. The economics of attention has "
            "reached the law."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
        self.clear_scene()
