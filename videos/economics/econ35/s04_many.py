from __future__ import annotations

from videos.economics.econ35.common import *  # noqa: F403


class Many(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Many goods: \ the chain and the continuum", r"With thousands of goods, where is the line?",
             "Chapter three. Many goods: the chain and the continuum.",
             lit={1977: r"Dornbusch, \ Fischer and Samuelson"}, scale=("nation", "world"),
             horizon=("a year", "a decade"))
        self.chain()
        self.continuum()
        self.shocks()

    def chain(self):
        M = load("many")
        A = M["chain_A"]
        om = M["free"]["omega"]
        ax = plane([0.4, 10.6], [0, 2.0], center=LEFT * 1.6 + DOWN * 0.4, x_length=9.0, y_length=4.4, xticks=[],
                   yticks=[0, 0.5, 1.0, 1.5, 2.0], ylabel=r"the Island's productivity advantage, \ $a^*_i / a_i$",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        bars = VGroup()
        for k, (v, home) in enumerate(zip(A, M["chain_home"])):
            p0, p1 = ax.ax.c2p(k + 0.65, 0), ax.ax.c2p(k + 1.35, v)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=ISLAND if home else ARCH,
                               fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
        line = seg(ax, 0.4, om, 10.6, om, WHITE, 2.5, dashed=True)
        lab = label(rf"the relative wage, \ {om:.2f}", font_size=17, color=WHITE).next_to(ax.ax.c2p(10.6, om), UP,
                                                                                         buff=0.08).shift(LEFT * 1.2)
        side = VGroup(
            label(r"goods ranked by \\ the Island's edge", font_size=18, color=GREY_A),
            label(r"teal: \ the Island makes them \\ (its edge beats its wage)", font_size=18, color=ISLAND),
            label(r"gold: \ the Archipelago", font_size=18, color=ARCH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "With two goods the answer is a comparison. With many it is a chain. <bookmark mark='a'/> Rank the "
            "goods by how much more productive the Island is than the Archipelago at each, its relative edge. "
            "<bookmark mark='b'/> Now draw the Island's wage relative to the Archipelago's. The Island makes every "
            "good whose edge is larger than its relative wage, <bookmark mark='c'/> and buys the rest. Where the "
            "line falls depends on wages, and wages depend on demand: if the line were too high, the Island would "
            "sell too little and its wage would fall."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(lab), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def _dfs_axes(self):
        return plane([0, 1], [0, 2.0], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.6,
                     xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.5, 1.0, 1.5, 2.0],
                     xlabel=r"goods, \ $z$, \ ranked by the Island's edge", ylabel=r"the relative wage, \ $\omega$",
                     xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.1f}", font_size=14)

    def continuum(self):
        M = load("many")
        ax = self._dfs_axes()
        A = path(ax, M["z"], M["A"], ISLAND, 3.5, yr=(0, 2.0))
        B = path(ax, M["z"], M["B"], ARCH, 3.5, yr=(0, 2.0))
        om, zb = M["free"]["omega"], M["free"]["zbar"]
        eq = dot(ax, zb, om, WHITE, 0.09)
        guides = VGroup(vline(ax, zb, 0, om, GREY_B, 1.5), seg(ax, 0, om, zb, om, GREY_B, 1.5, dashed=True))
        side = VGroup(
            label(r"teal \ $A(z)$: \ the edge, \\ falling along the chain", font_size=18, color=ISLAND),
            label(r"gold \ $B(z)$: \ the wage at which \\ trade balances if the Island \\ makes the goods up to $z$",
                  font_size=18, color=ARCH),
            label(rf"they cross at $\omega$ = {om:.2f}: \\ the Island makes {100 * zb:.0f}\% \\ of the goods",
                  font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Dornbusch, \ Fischer and Samuelson, \ \emph{AER} 67(5) (1977); \ the Island",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 1977 Rudiger Dornbusch, Stanley Fischer and Paul Samuelson took the chain to its limit: a continuum "
            "of goods, lined up from the Island's strongest to its weakest. <bookmark mark='a'/> The teal curve is "
            "the Island's edge along the line, falling. <bookmark mark='b'/> The gold curve is demand: if the Island "
            "makes every good up to some point, the relative wage at which its exports pay for its imports. The "
            "more goods it makes, the more the world spends on them, and the higher that wage. "
            f"<bookmark mark='c'/> They cross at a relative wage of {om:.2f}, with the Island making "
            f"{100 * zb:.0f} percent of the goods. Two curves, and the whole pattern of trade and wages follows."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(A), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(B), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(eq, scale=1.4), FadeIn(guides), FadeIn(side[2]))
        self.clear_scene()

    def shocks(self):
        M = load("many")
        ax = self._dfs_axes()
        A = path(ax, M["z"], M["A"], ISLAND, 3.0, yr=(0, 2.0))
        B = path(ax, M["z"], M["B"], ARCH, 2.0, yr=(0, 2.0))
        B2 = path(ax, M["z"], M["B_grow"], ARCH, 3.5, yr=(0, 2.0))
        g = M["g"]
        zs = np.array(M["z"])
        Aarr = np.array(M["A"])
        lo = path(ax, zs, g * Aarr, ISLAND, 1.8, yr=(0, 2.0))
        hi = path(ax, zs, Aarr / g, ISLAND, 1.8, yr=(0, 2.0))
        Sh = M["ship"]
        nt = Rectangle(width=ax.ax.c2p(Sh["zF"], 0)[0] - ax.ax.c2p(Sh["zH"], 0)[0], height=ax.ax.height,
                       fill_color=GREY_B, fill_opacity=0.2, stroke_width=0).move_to(
            ax.ax.c2p((Sh["zH"] + Sh["zF"]) / 2, 1.0))
        e1 = dot(ax, M["free"]["zbar"], M["free"]["omega"], WHITE, 0.08)
        e2 = dot(ax, M["grow"]["zbar"], M["grow"]["omega"], GAIN, 0.09)
        side = VGroup(
            label(rf"the Archipelago grows by half: \\ the Island's wage {M['free']['omega']:.2f} $\to$ "
                  rf"{M['grow']['omega']:.2f}; \\ its share of goods {100 * M['free']['zbar']:.0f}\% $\to$ "
                  rf"{100 * M['grow']['zbar']:.0f}\%", font_size=17, color=GAIN),
            label(rf"shipping loses {100 * (1 - g):.0f}\%: \\ {100 * Sh['nontraded']:.0f}\% of goods \\ are not "
                  r"traded at all", font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Dornbusch, \ Fischer and Samuelson (1977); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "The model earns its keep in experiments. <bookmark mark='a'/> Let the Archipelago's workforce grow by "
            "half. Its demand for the Island's goods rises, and the gold curve shifts up. "
            f"<bookmark mark='b'/> The Island's relative wage rises, from {M['free']['omega']:.2f} to "
            f"{M['grow']['omega']:.2f}, and it gives up its marginal industries to the Archipelago: it makes "
            f"{100 * M['grow']['zbar']:.0f} percent of goods instead of {100 * M['free']['zbar']:.0f}. Losing "
            "industries and gaining income at the same time is what the theory predicts. "
            f"<bookmark mark='c'/> Now add the cost of shipping: suppose {100 * (1 - g):.0f} percent of a cargo is "
            "lost on the way. A good is exported only if the edge beats the wage by enough to pay for the trip, so "
            f"the edge curve splits in two, and between them lies a band of goods, {100 * Sh['nontraded']:.0f} "
            "percent here, that each country makes for itself: haircuts, houses, most services."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(A), FadeIn(B), FadeIn(e1), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(B2), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(e2, scale=1.4), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeOut(B2), FadeOut(e2), Create(lo), Create(hi), FadeIn(nt), FadeIn(side[1]), run_time=1.5)
        self.clear_scene()
