from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403

LOW_E, HIGH_E = "#2E5D9F", "#A6E6F2"  # no substitute ... a good substitute


def e_color(e: float) -> str:
    return interpolate_color(ManimColor(LOW_E), ManimColor(HIGH_E), min(max((e - 0.1) / 2.4, 0), 1))


class Prices(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Prices as messages", r"How does a whole economy learn that something has become scarce?",
             "Chapter five. Prices as messages.", lit={1945: r"Hayek on knowledge"}, scale=("market", "world"),
             horizon=("a year",))
        self.hayek()
        self.users()
        self.shock()
        self.who_cuts()
        self.planner()
        self.dials()

    # ------------------------------------------------------------------
    def hayek(self):
        h = tables.HAYEK_1945.data
        hc = history_card(1945, r"Friedrich Hayek, \ ``The Use of Knowledge in Society''",
                          r"\emph{American Economic Review}", color=TIN, width=7.0, font_size=26).to_edge(UP, buff=0.4)
        q = quote_card(h["tin"], r"Hayek (1945)", width=12.4, font_size=28, color=TIN).next_to(hc, DOWN, buff=0.4)
        q2 = quote_card(h["economize"], r"Hayek (1945)", width=12.4, font_size=28, color=TIN).move_to(q)
        src = published_tag(tables.HAYEK_1945.tag, corner=DR, font_size=18)
        with self.voiceover(
            "How did the pencil's thousands of makers know how much cedar to cut, or Paris's eighty departments how "
            "much wheat to send? <bookmark mark='a'/> In 1945 Friedrich Hayek answered with a thought experiment. "
            "<bookmark mark='b'/> Suppose that somewhere in the world a new use for tin has arisen, or one of the "
            "mines that supply it has closed. It does not matter which, he wrote, and it is very significant that "
            "it does not matter. <bookmark mark='c'/> All that the users of tin need to know is that some of the "
            "tin they used to consume is now more valuable somewhere else, and that, in consequence, they must "
            "economize tin."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeTransform(q, q2))
        self.clear_scene()

    def _cloud(self, d):
        rng = np.random.default_rng(5)
        n = d["n"]
        cols = 12
        dots = VGroup()
        for i in range(n):
            x, y = i % cols, i // cols
            r = 0.045 * np.sqrt(d["a"][i]) + 0.03
            dot = Circle(radius=r, stroke_width=0, fill_color=e_color(d["e"][i]), fill_opacity=0.95)
            dot.move_to([-5.6 + 0.66 * x + rng.uniform(-0.12, 0.12), 1.7 - 0.72 * y + rng.uniform(-0.12, 0.12), 0])
            dots.add(dot)
        return dots

    def users(self):
        d = load("tin")
        dots = self._cloud(d)
        bar = VGroup(*[Rectangle(width=0.32, height=0.22, stroke_width=0, fill_color=e_color(0.1 + 2.4 * k / 11),
                                 fill_opacity=1) for k in range(12)]).arrange(RIGHT, buff=0)
        bar.move_to([-1.9, -2.55, 0])
        bl = label(r"no substitute", font_size=20, color=GREY_A).next_to(bar, LEFT, buff=0.15)
        br = label(r"a good substitute", font_size=20, color=GREY_A).next_to(bar, RIGHT, buff=0.15)
        size = label(r"size: \ how much tin each uses", font_size=20, color=GREY_A).next_to(bar, DOWN, buff=0.25)
        model = VGroup(
            MathTex(r"q_i(p) = a_i\, p^{-\varepsilon_i}", font_size=40),
            label(r"user $i$'s demand at the price $p$", font_size=22, color=GREY_A),
            label(r"$\varepsilon_i$: \ how easily $i$ can switch", font_size=22, color=GREY_A),
            label(r"to copper, aluminium, glass, plastic", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 1.0, 0])
        tag = agora_tag(rf"computed: Agora, {d['n']} tin users (agora.signals)", font_size=17)
        with self.voiceover(
            f"Let's build Hayek's market. Here are {d['n']} users of tin, each one a dot: a cannery, a maker of "
            "solder, an organ builder, a toy factory. The size of the dot is how much tin they use. "
            "<bookmark mark='a'/> The colour is how easily they could do without it. Some have a good substitute: "
            "aluminium cans, glass jars. Some have none at all. <bookmark mark='b'/> Write each user's demand as "
            "a quantity that falls as the price rises, at a rate that depends on how easily they can switch. "
            "Economists call that rate the price elasticity. <bookmark mark='c'/> Each user knows its own business "
            "and nobody else's. And nobody, anywhere, knows all sixty."
        ) as vo:
            self.play(LaggedStart(*[GrowFromCenter(x) for x in dots], lag_ratio=0.02), FadeIn(tag), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(bar), FadeIn(bl), FadeIn(br), FadeIn(size))
            vo.wait_until("b")
            self.play(FadeIn(model, shift=LEFT * 0.2))
        self.dots, self.legend, self.model, self.tag = dots, VGroup(bar, bl, br, size), model, tag

    def shock(self):
        d = load("tin")
        path = d["path"]
        exc = d["excess"]
        mine = VGroup(Polygon([-0.5, 0, 0], [0.5, 0, 0], [0.32, 0.45, 0], [-0.32, 0.45, 0], stroke_width=0,
                              fill_color="#6B5A45", fill_opacity=1),
                      label(r"mine", font_size=20, color=WHITE)).move_to([4.6, -1.0, 0])
        mine[1].move_to(mine[0])
        cross = Cross(mine, stroke_color=E.MISS, stroke_width=6, scale_factor=0.8)
        cut = label(rf"supply falls by {100 * d['cut']:.0f}\%", font_size=26, color=E.MISS).next_to(mine, DOWN,
                                                                                                buff=0.2)
        p = ValueTracker(1.0)
        price = always_redraw(lambda: VGroup(label(r"price of tin", font_size=24, color=TIN),
                                             DecimalNumber(p.get_value(), num_decimal_places=3, font_size=40,
                                                           color=WHITE)).arrange(DOWN, buff=0.1).move_to([4.6, 2.4, 0]))
        self.play(FadeOut(self.model))
        with self.voiceover(
            "Now a mine closes, and the supply of tin falls by "
            f"{100 * d['cut']:.0f} percent. <bookmark mark='a'/> At the old price, users want more tin than there "
            "is. Sellers notice that they can ask more, and buyers that they must offer more, and the price starts "
            "to climb. <bookmark mark='b'/> It keeps climbing while demand exceeds supply, by less and less, until "
            f"the two meet: {100 * (d['price'] - 1):.0f} percent above where it began. <bookmark mark='c'/> That "
            "single number is the whole message. It reaches every user, whether or not they've heard of the mine."
        ) as vo:
            self.play(FadeIn(mine), FadeIn(price))
            self.play(Create(cross), FadeIn(cut))
            vo.wait_until("a")
            for k in range(1, 9):
                self.play(p.animate.set_value(path[k]), run_time=0.55 if k < 4 else 0.35)
            vo.wait_until("c")
            self.play(Indicate(price, color=E.ACCENT))
        self.price_box = price
        self.mine = VGroup(mine, cross, cut)

    def who_cuts(self):
        d = load("tin")
        cut_share = d["cut_share"]
        anims = [x.animate.scale(np.sqrt(max(1 - c, 0.05))) for x, c in zip(self.dots, cut_share)]
        ax = axes([0, 2.6], [0, 0.36], x_length=5.2, y_length=3.6, xticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5],
                  yticks=[0, 0.1, 0.2, 0.3], yfmt=lambda v: rf"{100 * v:.0f}\%",
                  xlabel=r"how easily they can switch \ ($\varepsilon$)", font_size=18, center=[3.6, -0.4, 0])
        yl = label(r"how much tin each gives up", font_size=20, color=GREY_A).next_to(ax.ax, UP, buff=0.12).align_to(
            ax.ax, LEFT)
        pts = VGroup(*[Dot(ax.ax.c2p(e, c), radius=0.05, color=e_color(e)) for e, c in zip(d["e"], cut_share)])
        with self.voiceover(
            "And each user responds to the price in the way its own circumstances dictate. <bookmark mark='a'/> "
            "Watch the dots. <bookmark mark='b'/> The users with a good substitute switch, and give up a lot of "
            f"tin: as much as {100 * d['cut_hi']:.0f} percent. The users with no substitute keep almost all of it, "
            f"giving up as little as {100 * d['cut_lo']:.0f} percent. <bookmark mark='c'/> Nobody ordered any of "
            "this. In Hayek's words, tens of thousands of people whose identity could not be ascertained by months "
            "of investigation are made to use the material or its products more sparingly. They move in the right "
            "direction, and "
            "the cuts add up exactly to the tin that's missing."
        ) as vo:
            self.play(FadeOut(self.legend), FadeOut(self.mine))
            vo.wait_until("a")
            self.play(*anims, run_time=2.5)
            vo.wait_until("b")
            self.play(self.dots.animate.scale(0.72).to_edge(LEFT, buff=0.35), FadeIn(ax), FadeIn(yl))
            self.play(LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(self.dots, pts)], lag_ratio=0.02),
                      run_time=2.5)
        self.clear_scene()

    def planner(self):
        d = load("tin")
        order = np.argsort(d["e"])
        mv = d["mv_ration"][order]
        n = len(mv)
        ax = axes([0, n], [0, 3.0], x_length=7.2, y_length=3.8, yticks=[0, 1, 2, 3],
                  xlabel=r"the users, from no substitute to a good one", font_size=18, center=[-2.6, -0.5, 0])
        yl = label(r"what the last unit of tin is worth to each", font_size=20, color=GREY_A).next_to(ax.ax, UP,
                                                                                                  buff=0.12)
        yl.align_to(ax.ax, LEFT)
        bars = VGroup(*[Rectangle(width=0.09, height=ax.ax.c2p(0, v)[1] - ax.ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=e_color(d["e"][i]), fill_opacity=0.9).move_to(ax.ax.c2p(k + 0.5, v / 2))
                        for k, (i, v) in enumerate(zip(order, mv))])
        line = DashedLine(ax.ax.c2p(0, d["price"]), ax.ax.c2p(n, d["price"]), color=E.ACCENT, stroke_width=3)
        ll = VGroup(label(r"with the price:", font_size=20, color=E.ACCENT),
                    label(rf"every last unit is worth {d['price']:.2f}", font_size=20, color=E.ACCENT))
        ll.arrange(DOWN, aligned_edge=RIGHT, buff=0.06).next_to(ax.ax.c2p(n, d["price"]), UP, buff=0.12)
        ll.align_to(ax.ax.c2p(n, 0), RIGHT)
        right = VGroup(
            label(rf"a planner who cuts everyone by {100 * d['cut']:.0f}\%", font_size=24, color=WHITE),
            label(rf"leaves last units worth {d['mv_lo']:.2f} to {d['mv_hi']:.2f}", font_size=24, color=GREY_A),
            label(rf"and gives up {100 * d['extra_share']:.1f}\% more value", font_size=24, color=E.MISS),
            label(r"to match the price, \ the planner needs", font_size=24, color=WHITE),
            label(rf"{d['numbers_planner']} numbers, \ which keep changing", font_size=30, color=E.MISS),
            label(r"the market used one", font_size=30, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.2, 0.0, 0])
        with self.voiceover(
            "Could a wise planner do as well? Suppose a ministry of tin, which hears about the mine and orders "
            f"everyone to cut their use by {100 * d['cut']:.0f} percent. Fair shares. <bookmark mark='a'/> Here is "
            "what the last unit of tin is then worth to each user. The users with substitutes have more than they "
            "need; the users without are desperate for more. A unit moved from one to the other would be worth "
            f"{d['mv_hi'] / d['mv_lo']:.1f} times as much. <bookmark mark='b'/> With the price, every user stops "
            "where the last unit is worth exactly the price, so there are no such gains left lying around. "
            "<bookmark mark='c'/> In this example rationing gives up "
            f"{100 * d['extra_share']:.1f} percent more of tin's value than the price does. <bookmark mark='d'/> "
            "The deeper point is the knowledge. To match the price, the planner would need every user's demand: "
            f"{d['numbers_planner']} numbers here, and far more in any real economy, and they change whenever a "
            "factory opens or a recipe does. The market did it with one number, which nobody had to collect."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(yl), FadeIn(right[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(right[1]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(ll))
            vo.wait_until("c")
            self.play(FadeIn(right[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in right[3:]], lag_ratio=0.5), run_time=2.5)
        self.clear_scene()

    def dials(self):
        h = tables.HAYEK_1945.data
        q = quote_card(h["dials"], r"Hayek (1945)", width=12.0, font_size=30, color=TIN).to_edge(UP, buff=0.6)
        faces = VGroup(*[dial_face(nm, p, radius=0.62, font_size=18) for nm, p in
                         ((r"the price of tin", 1), (r"a wage", 38), (r"an interest rate", 31),
                          (r"an exchange rate", 34))]).arrange(RIGHT, buff=0.9).next_to(q, DOWN, buff=0.6)
        for f_ in faces:
            f_.sub.become(label(r"a price", font_size=16, color=GREY_B).move_to(f_.sub))
        caveat = VGroup(
            label(r"Hayek's own caveat: \ the system works ``less perfectly as prices grow more rigid''",
                  font_size=24, color=GREY_A),
            label(r"and a price allocates by willingness to pay, \ which depends on income \ (Parts 18 and 40)",
                  font_size=24, color=E.OUGHT),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Hayek's image for this was a control room. The price system, he wrote, lets each producer watch merely "
            "the movement of a few pointers, as an engineer might watch the hands of a few dials. "
            "<bookmark mark='a'/> The price of tin, a wage, an interest rate, an exchange rate: each one is a dial, "
            "summing up what millions of people know and want. <bookmark mark='b'/> Two warnings, so that we don't "
            "oversell it. Hayek himself said the system works less perfectly as prices grow more rigid, and a great "
            "deal of this series is about prices that stick, or lie, or are missing altogether. And a price gives "
            "the tin to those willing to pay the most, which depends on how much money they have. Whether that is "
            "fair is a different question, and we'll keep it apart from how the system works."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f_, shift=UP * 0.1) for f_ in faces], lag_ratio=0.3), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(caveat[0]))
            self.play(FadeIn(caveat[1]))
        self.clear_scene()
