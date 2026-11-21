from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403


class Chains(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Supply chains, \ measured", r"How far does a disaster travel along the links, \ and what "
             r"stops it?", "Chapter six. Supply chains, measured.",
             lit={2016: r"Barrot and Sauvagnat", 2021: r"Carvalho et al."}, scale=("firm", "nation"),
             horizon=("a year",))
        self.island()
        self.specific()
        self.evidence()

    def island(self):
        Q = load("quake")
        dn, up = Q["rows"]["downstream"], Q["rows"]["upstream"]
        xs = [0, 1, 2, 4, 5, 6, 8]
        vals = [100 * r["loss"] for r in dn] + [100 * r["loss"] for r in up] + [100 * Q["far_loss"]]
        cols = [SEED] * 3 + [BANK] * 3 + [GREY_B]
        ax = plane([-0.7, 8.7], [0, 20], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15, 20], ylabel=r"sales lost in the year, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        b = bars(ax, xs, vals, cols, width=0.6)
        vl = VGroup(*[label(f"{v:.1f}", font_size=14, color=c).next_to(x, UP, buff=0.06)
                      for v, c, x in zip(vals, cols, b)])
        names = [r"1 step", r"2", r"3"] * 2 + [r"further"]
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.12)
                        for x, n, c in zip(xs, names, cols)])
        grp = VGroup(label(r"customers of hit firms \ (downstream)", font_size=16, color=SEED).next_to(
            ax.ax.c2p(1, 0), DOWN, buff=0.55),
            label(r"suppliers of hit firms \ (upstream)", font_size=16, color=BANK).next_to(ax.ax.c2p(5, 0), DOWN,
                                                                                            buff=0.55))
        side = VGroup(
            label(rf"{100 * Q['hit_share']:.0f}\% of firms hit, \\ each losing {100 * (1 - Q['capacity']):.0f}\% "
                  r"of output", font_size=19, color=SHOCK),
            label(rf"losses from the hit firms alone: \\ {100 * Q['direct_only']:.1f}\% of all sales", font_size=19,
                  color=GREY_A),
            label(rf"with the links: \ {100 * Q['total_loss']:.1f}\%", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ 3,000 firms in five tiers; \ agora.network.quake".replace(",", "{,}"),
                         corner=DL, font_size=12)
        with self.voiceover(
            "Back to the Island's three thousand firms, in five tiers, now with a disaster. <bookmark mark='a'/> "
            f"{100 * Q['hit_share']:.0f} percent of them, on the coast, lose {100 * (1 - Q['capacity']):.0f} "
            "percent of their output for a year. <bookmark mark='b'/> Their direct customers lose sales because a "
            f"part is missing: {vals[0]:.1f} percent on average. Their customers' customers lose {vals[1]:.1f}, "
            "and the loss fades within a few steps. <bookmark mark='c'/> Upstream, the hit firms' suppliers lose "
            f"a buyer: {vals[3]:.1f} percent at one step, {vals[4]:.1f} at two. <bookmark mark='d'/> Counting "
            f"only the hit firms, the Island loses {100 * Q['direct_only']:.1f} percent of its sales. With the "
            f"links, it loses {100 * Q['total_loss']:.1f}: most of the damage is done to firms the disaster never "
            "touched."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(grp), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b[k], DOWN) for k in range(3)], FadeIn(vl[:3]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b[k], DOWN) for k in range(3, 7)], FadeIn(vl[3:]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.clear_scene()

    def specific(self):
        Q = load("quake")
        G = Q["all_replaceable"]
        cd = Q["cobb_douglas"]
        vals = [100 * Q["direct_specific"], 100 * Q["direct_generic"], 100 * G["direct_specific"]]
        cols = [SHOCK, LINK, GAIN]
        ax = plane([-0.6, 2.6], [0, 20], center=LEFT * 2.8 + DOWN * 0.3, x_length=5.8, y_length=4.6, xticks=[],
                   yticks=[0, 5, 10, 15, 20], ylabel=r"direct customers' sales lost, \ \%",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        b = bars(ax, range(3), vals, cols, width=0.55)
        names = [r"a specific input \\ from the hit firm", r"only generic inputs \\ from it",
                 r"if every input \\ could be replaced"]
        labs = VGroup(*[label(n, font_size=14, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.12)
                        for k, (n, c) in enumerate(zip(names, cols))])
        vl = VGroup(*[label(f"{v:.1f}", font_size=15, color=c).next_to(x, UP, buff=0.06)
                      for v, c, x in zip(vals, cols, b)])
        side = VGroup(
            label(r"specific: \ made to the buyer's design, \\ no other supplier for months", font_size=19,
                  color=SHOCK),
            label(r"generic: \ bought elsewhere within weeks", font_size=19, color=LINK),
            label(rf"the Island's total loss: \ {100 * Q['total_loss']:.1f}\% as it is, \\ "
                  rf"{100 * G['total_loss']:.1f}\% if every input could be replaced", font_size=19, color=E.ACCENT),
            label(rf"easier substitution between inputs \\ (Cobb-Douglas): \ {100 * cd['total_loss']:.1f}\%",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ 40\% of links specific \ (planted); \ agora.network.quake", corner=DL,
                         font_size=12)
        with self.voiceover(
            "What makes a link carry a shock? <bookmark mark='a'/> Some inputs are specific: made to the buyer's "
            "design, a moulded part, a custom chip. If its maker is hit, there is no other supplier for months. "
            f"Direct customers who bought something specific from a hit firm lose {vals[0]:.1f} percent of their "
            f"sales. <bookmark mark='b'/> Customers who bought only generic inputs from it, steel, packaging, lose "
            f"{vals[1]:.1f}, and most of that through their other links. <bookmark mark='c'/> Make every input "
            f"replaceable and the direct customers' loss falls to {vals[2]:.1f} percent, <bookmark mark='d'/> and "
            f"the Island's total loss from {100 * Q['total_loss']:.1f} percent to {100 * G['total_loss']:.1f}. What "
            "the links carry depends on what flows along them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(vl[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(vl[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(vl[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def evidence(self):
        head = label(r"what the disasters showed", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        cards = point_cards([
            (r"Japan, \ 2011", r"losses travelled upstream and downstream, \ several links deep; \ about half a point "
             r"of GDP growth in the year after (Carvalho et al.)", SHOCK),
            (r"American disasters", r"when a supplier is hit, \ its customers' sales growth falls by about "
             r"2 points, \ but only if its input is specific (Barrot and Sauvagnat)", SEED),
            (r"Japanese plants in America", r"after the earthquake, \ output fell about one for one with imported "
             r"parts: \ inputs nearly impossible to substitute (Boehm, \ Flaaen and Pandalai-Nayar)", LINK),
            (r"and since", r"floods in Thailand (2011), \ the pandemic's chip shortage (2021): \ the same mechanism, \ "
             r"each time a surprise", GDP),
        ], cols=2, width=12.8, font_size=19).next_to(head, DOWN, buff=0.45)
        tag = published_tag(r"Carvalho, \ Nirei, \ Saito and Tahbaz-Salehi, \ QJE 136(2) (2021); \ Barrot and "
                            r"Sauvagnat, \ QJE 131(3) (2016); \ Boehm et al., \ REStat 101(1) (2019)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "The real economy has run this experiment several times. <bookmark mark='a'/> In Japan in 2011, "
            "firms linked to the disaster area lost sales whether the link ran upstream or downstream, and the "
            "loss reached firms several links away: about half a point of GDP growth in all. <bookmark mark='b'/> "
            "Jean-Noël Barrot and Julien Sauvagnat followed American firms hit by hurricanes, floods and "
            "earthquakes over several decades. Their customers' sales growth fell by about two percentage "
            "points, but only when the hit supplier made something specific. <bookmark mark='c'/> Christoph Boehm, "
            "Aaron Flaaen and Nitya Pandalai-Nayar looked at Japanese-owned plants in America after the earthquake: "
            "their output fell almost one for one with the parts they could no longer import, as if inputs could "
            "not be substituted at all. <bookmark mark='d'/> Floods in Thailand later in 2011, the shortage of "
            "chips in the pandemic: the same mechanism each time, and each time a surprise to those who had not "
            "mapped their suppliers' suppliers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
