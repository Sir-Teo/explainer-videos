from __future__ import annotations

from videos.economics.econ60.common import *  # noqa: F403


class Algorithms(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Algorithms and personalized prices", r"When software sets the price for each buyer, \ who "
             r"gains, \ and is anyone colluding?", "Chapter twelve. Algorithms and personalized prices.",
             lit={2020: r"Calvano et al.", 2024: r"United States v. RealPage"}, scale=("person", "market"),
             horizon=("a day",))
        self.personal()
        self.collusion()

    def personal(self):
        M = load("menu")["mfn"]
        ax = plane([-0.6, 1.6], [0, 70], center=LEFT * 2.8 + DOWN * 0.4, x_length=5.6, y_length=4.4, xticks=[],
                   yticks=[0, 20, 40, 60], ylabel=r"price, \ \$", yfmt=lambda v: f"{v:.0f}", font_size=14)
        one = [M["p_one"], M["p_one"]]
        own = M["p_sep"]
        b1 = bars(ax, [-0.17, 0.83], one, [GREY_B, GREY_B], width=0.3)
        b2 = bars(ax, [0.17, 1.17], own, [BUS, LEIS], width=0.3)
        labs = VGroup(label(r"buyers who \\ care less about price", font_size=14, color=BUS).next_to(ax.ax.c2p(0, 0),
                                                                                                     DOWN, buff=0.12),
                      label(r"buyers who \\ care more", font_size=14, color=LEIS).next_to(ax.ax.c2p(1, 0), DOWN,
                                                                                         buff=0.12))
        vals = VGroup(*[label(f"{v:.0f}", font_size=15, color=c).next_to(x, UP, buff=0.05)
                        for v, c, x in zip(one + own, [GREY_B, GREY_B, BUS, LEIS], list(b1) + list(b2))])
        side = VGroup(
            label(r"grey: \ one price for all; \ colour: \ a price for each group", font_size=18, color=GREY_A),
            label(rf"profit: \ {M['profit_one']:,.0f} \ $\to$ \ {M['profit_sep']:,.0f}".replace(",", "{,}"),
                  font_size=20, color=OPT),
            label(rf"price-sensitive buyers pay less and buy more: \ {M['q_one'][1]:.0f} $\to$ {M['q_sep'][1]:.0f}",
                  font_size=19, color=LEIS),
            label(r"the others pay more", font_size=19, color=BUS),
            label(r"an algorithm trained on browsing and purchase data \\ can tell the groups apart: \ Part 10's "
                  r"experiment, \ at scale", font_size=18, color=GREY_A),
            label(r"limits: \ no prices by protected traits, \ and buyers who feel cheated", font_size=18,
                  color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        if side.width > 6.6:
            side.width = 6.6
            side.to_edge(RIGHT, buff=0.35)
        tag = agora_tag(r"computed: \ two groups with linear demand; \ agora.revenue.mfn", corner=DL, font_size=12)
        with self.voiceover(
            "Algorithms can do what chains choose not to: price each buyer separately. <bookmark mark='a'/> Take "
            "two groups of buyers, one that cares less about price and one that cares more. With one price for "
            f"all, both pay {M['p_one']:.0f}. <bookmark mark='b'/> Priced separately, the first pays {own[0]:.0f} "
            f"and the second {own[1]:.0f}, and profit rises from {M['profit_one']:,.0f} to {M['profit_sep']:,.0f}. "
            "<bookmark mark='c'/> The price-sensitive buyers gain: they pay less and buy twice as much. The others "
            "lose. Whether personalization helps buyers on balance depends on who the groups are, which is Part "
            "ten's third-degree discrimination. <bookmark mark='d'/> What is new is that software trained on "
            "browsing and purchase data can tell the groups apart, as Part ten's price experiment showed. <bookmark "
            "mark='e'/> The limits are legal, no prices by protected traits, and practical: buyers who discover "
            "they paid more than their neighbour feel cheated, and some stop buying."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(b1[0], DOWN), GrowFromEdge(b1[1], DOWN), FadeIn(vals[0]), FadeIn(vals[1]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b2[0], DOWN), GrowFromEdge(b2[1], DOWN), FadeIn(vals[2]), FadeIn(vals[3]),
                      FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def collusion(self):
        cards = VGroup(
            history_card(2020, r"Calvano, \ Calzolari, \ Denicol\`o and Pastorello", r"Part 44: \ two Q-learning "
                         r"algorithms, \ left to learn, \ settled on prices above competition and punished "
                         r"deviations, \ with no instruction to collude", color=AIR, width=11.4, font_size=20),
            history_card(2024, r"United States v. RealPage", r"the Justice Department sues the maker of rent-pricing "
                         r"software used by many landlords, \ alleging that sharing their data through it raised "
                         r"rents", color=COST, width=11.4, font_size=20),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        q = label(r"the legal question: \ is a shared algorithm an agreement?", font_size=22, color=E.ACCENT).next_to(
            cards, DOWN, buff=0.5)
        tag = published_tag(r"Calvano et al., \ American Economic Review (2020); \ U.S. Department of Justice "
                            r"(August 2024)", corner=DL, font_size=12)
        with self.voiceover(
            "And there is the collusion question of Part forty-four. <bookmark mark='a'/> In simulations by Emilio "
            "Calvano and coauthors, pricing algorithms that learned by trial and error settled on prices above the "
            "competitive level and punished undercutting, though nobody told them to collude. <bookmark mark='b'/> "
            "In August 2024 the Justice Department sued RealPage, whose software recommends rents to many landlords, "
            "alleging that pooling the landlords' private data through it raised rents. <bookmark mark='c'/> The "
            "legal question is old: what counts as an agreement. Prices set by the same software from the same pooled "
            "data are a new way of asking it."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.clear_scene()
