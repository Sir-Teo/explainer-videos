from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Bundles(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Bundles, \ subscriptions and free", r"Why sell a thousand songs for one monthly fee?",
             "Chapter eight. Bundles, subscriptions and free.", lit={1999: r"Bakos and Brynjolfsson"},
             scale=("person", "firm"), horizon=("a year",))
        self.law()
        self.free()

    def law(self):
        B = load("bundle")
        rows = B["rows"]
        n = np.array([r["n"] for r in rows], float)
        rev = np.array([r["revenue_per_good"] for r in rows])
        buy = np.array([r["buyers"] for r in rows])
        dwl = np.array([r["deadweight"] for r in rows])
        ax = plane([0, 2.0], [0, 0.55], center=LEFT * 2.7 + DOWN * 0.4, x_length=6.4, y_length=4.6,
                   xticks=[0, 0.3, 0.7, 1.0, 1.3, 1.7, 2.0], yticks=[0, 0.125, 0.25, 0.375, 0.5],
                   xlabel=r"goods in the bundle \ (log scale)", ylabel=r"per good, \ per buyer",
                   xfmt=lambda v: {0: "1", 0.3: "2", 0.7: "5", 1.0: "10", 1.3: "20", 1.7: "50", 2.0: "100"}.get(
                       round(v, 1), ""), yfmt=lambda v: f"{v:.3g}", font_size=14)
        lx = np.log10(n)
        mean = DashedLine(ax.ax.c2p(0, 0.5), ax.ax.c2p(2.0, 0.5), color=GREY_B, stroke_width=1.4)
        ml = label(r"the average value of a good: \ 0.5", font_size=15, color=GREY_B).next_to(ax.ax.c2p(1.0, 0.5), UP,
                                                                                            buff=0.05)
        sep = DashedLine(ax.ax.c2p(0, 0.25), ax.ax.c2p(2.0, 0.25), color=COST, stroke_width=1.4)
        sl = label(r"sold separately: \ 0.25", font_size=15, color=COST).next_to(ax.ax.c2p(1.6, 0.25), DOWN,
                                                                                 buff=0.05)
        rc = path(ax, lx, rev, OPT, 3.0, smooth=False)
        dc = path(ax, lx, dwl, GREY_A, 2.0, smooth=False)
        side = VGroup(
            label(r"each good's value to each buyer: \ uniform on 0 to 1, \ independent; \ no marginal cost",
                  font_size=18, color=GREY_A),
            label(r"sold alone: \ price \$0.50, \ half buy, \ revenue 0.25 per buyer", font_size=19, color=COST),
            label(rf"in a bundle of 100: \ revenue {rev[-1]:.3f} per good, \ {100 * buy[-1]:.0f}\% buy", font_size=19,
                  color=OPT),
            label(r"the sum of many independent values is predictable: \\ the law of large numbers prices the "
                  r"bundle", font_size=19, color=WHITE),
            label(r"grey: \ value lost because some buyers are priced out", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ agora.revenue.big\_bundle, \ 20,000 buyers".replace(",", "{,}"), corner=DL,
                        font_size=12)
        with self.voiceover(
            "Part ten showed bundling two goods. With many goods something stronger happens. <bookmark mark='a'/> "
            "Suppose each buyer values each of a hundred songs at a random amount between nothing and a dollar, "
            "independently, and a song costs nothing to copy. <bookmark mark='b'/> Sold one at a time, the best "
            "price is fifty cents, half the buyers take each song, and the seller earns a quarter per song per "
            "buyer. <bookmark mark='c'/> Sold as a bundle, the revenue per song rises with the bundle's size; with "
            f"a hundred songs it is {rev[-1]:.3f}, and {100 * buy[-1]:.0f} percent of buyers subscribe. <bookmark "
            "mark='d'/> The reason is the law of large numbers. One buyer's value for one song is anyone's guess, "
            "but the sum of a hundred independent values is close to fifty for everyone, so one price captures "
            "nearly all of it. Yannis Bakos and Erik Brynjolfsson made the point in 1999, before music "
            "subscriptions existed. <bookmark mark='e'/> And the value lost to buyers who are priced out, in grey, "
            "shrinks too. The seller gains most, but almost everyone gets everything."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(mean), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(sep), FadeIn(sl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(rc), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(dc), FadeIn(side[4]))
        self.clear_scene()

    def free(self):
        cards = point_cards([
            (r"subscriptions", r"a bundle over time as well as across goods: \ a monthly fee for everything, \ and "
             r"a buyer who forgets to cancel", AIR),
            (r"free to one side", r"Part 44's platforms: \ the side whose presence attracts the other is "
             r"subsidized, \ sometimes to zero", LEIS),
            (r"freemium", r"a damaged free version, \ chapter seven's menu with a price of nothing at the bottom",
             BUS),
            (r"zero is special", r"buyers treat a price of nothing differently from a small price; \ Part 45's "
             r"behaviour, \ priced", COST),
        ], width=12.6, cols=2, font_size=20).move_to(DOWN * 0.2)
        head = label(r"subscriptions and the economics of free", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Bundles explain much of modern pricing. <bookmark mark='a'/> A subscription bundles across time as "
            "well as across goods: one monthly fee for everything, and some buyers who forget to cancel. <bookmark "
            "mark='b'/> Free is often one side of a platform, as Part forty-four showed: the side whose presence "
            "attracts the other is subsidized, sometimes all the way to nothing. <bookmark mark='c'/> Freemium is "
            "chapter seven's menu with a damaged version at the bottom priced at zero. <bookmark mark='d'/> And "
            "zero is a special price: buyers treat nothing differently from a few cents, which Part forty-five's "
            "behavioural economics explains and pricing teams exploit."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
