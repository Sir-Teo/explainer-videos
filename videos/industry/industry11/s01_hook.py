from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.cheltenham()
        self.blow()
        self.tonnes()
        self.per_kg()
        self.title()

    def cheltenham(self):
        H = R["hook"]
        where = VGroup(tx("Cheltenham, England", 24, WHITE, bold=True),
                       tx("Wednesday 13 August 1856, the British Association's meeting", 17, GREY_A)).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT).to_corner(UL, buff=0.45)
        table = Rectangle(width=5.0, height=0.12, stroke_width=0, fill_color="#8A6E52", fill_opacity=1).move_to([-1.0, -1.3, 0])
        legs = VGroup(*[Rectangle(width=0.1, height=1.0, stroke_width=0, fill_color="#6B5640", fill_opacity=1).move_to(
            [x, -1.85, 0]) for x in (-3.2, 1.2)])
        cups = VGroup(*[VGroup(Rectangle(width=0.28, height=0.24, stroke_width=0, fill_color="#E8EAED", fill_opacity=1),
                               Arc(radius=0.08, start_angle=-PI / 2, angle=PI, stroke_color="#E8EAED", stroke_width=3
                                   ).shift(RIGHT * 0.17)).move_to([x, -1.1, 0]) for x in (-2.6, 0.6)])
        men = VGroup(draw.person(1.3, "#9AA3B2"), draw.person(1.3, "#7EC8F5"), draw.person(1.3, "#F6C453")).arrange(
            RIGHT, buff=1.2).move_to([-1.0, -0.35, 0])
        quote = VGroup(tx("\"Do you know, that there is actually a fellow come down from London", 20, WHITE),
                       tx("to read a paper on the manufacture of malleable iron without fuel?", 20, WHITE),
                       tx("Ha, ha, ha!\"", 24, PRICE, bold=True)).arrange(DOWN, buff=0.1).move_to([0.3, 2.0, 0])
        who = tx("a Welsh ironmaster at breakfast, as Bessemer recalled it", 15, GREY_A).next_to(quote, DOWN, buff=0.15)
        me = VGroup(tx("The fellow:", 17, GREY_A), tx("Henry Bessemer", 26, HOT, bold=True)).arrange(DOWN, buff=0.06).move_to(
            [4.6, -0.6, 0])
        arr = Arrow(me.get_left(), men[2].get_right() + RIGHT * 0.1, buff=0.1, color=HOT, stroke_width=3, tip_length=0.15)
        src = source("Sir Henry Bessemer, F.R.S.: An Autobiography (1905), 'The Cheltenham Meeting'", size=13)
        with self.voiceover(
            "Cheltenham, in England, on the morning of the thirteenth of August, 1856. The British Association for the "
            "Advancement of Science is meeting in the town. <bookmark mark='a'/> At breakfast in a hotel, a Welsh "
            "ironmaster sits down opposite a friend and says, as the inventor himself later told it: do you know, "
            "there is actually a fellow come down from London to read a paper on the manufacture of malleable iron "
            "without fuel? Ha, ha, ha! <bookmark mark='b'/> The man sitting next to his friend was the fellow: Henry "
            "Bessemer. And that morning he read the paper."
        ) as vo:
            self.play(FadeIn(where), FadeIn(src), FadeIn(table), FadeIn(legs), FadeIn(cups))
            self.play(LaggedStart(*[FadeIn(m_, shift=UP * 0.2) for m_ in men], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(quote[:2], shift=DOWN * 0.1), run_time=1.5)
            self.play(FadeIn(quote[2], scale=1.3), FadeIn(who))
            self.play(Wiggle(men[0]), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeIn(me, shift=LEFT * 0.2), GrowArrow(arr))
            self.play(men[2].animate.set_color(HOT), run_time=0.8)
        self.clear_scene()

    def blow(self):
        H = R["hook"]
        conv = draw.converter(2.6).move_to([-3.0, -0.6, 0])
        conv.sparks.set_opacity(0)
        conv.glow.set_opacity(0)
        air = VGroup(*[Arrow([-3.0 + dx, -2.9, 0], [-3.0 + dx * 0.6, -1.7, 0], buff=0, color="#C9D3E0", stroke_width=3,
                             tip_length=0.15) for dx in (-0.4, -0.2, 0, 0.2, 0.4)])
        air_l = tx("air blown in from below", 16, "#C9D3E0").next_to(air, DOWN, buff=0.05)
        iron = VGroup(tx("Pig iron from the blast furnace", 20, WHITE, bold=True),
                      tx(f"about {H['carbon']:.0f}% carbon: hard, brittle, cheap", 17, GREY_A)).arrange(
            DOWN, buff=0.05, aligned_edge=LEFT).move_to([2.6, 2.4, 0])
        burn = VGroup(tx("The carbon burns in the blast", 20, HOT, bold=True),
                      tx("and the heat it gives off keeps the iron molten", 17, GREY_A),
                      tx("without a fire: iron without fuel", 17, GREY_A)).arrange(DOWN, buff=0.05, aligned_edge=LEFT
                                                                                    ).move_to([2.6, 0.9, 0])
        out = VGroup(tx("What is left: steel", 20, STEELC, bold=True),
                     tx("strong and tough, now in bulk", 17, GREY_A),
                     tx(f"{H['cwt']:.0f} hundredweight (about {H['kg_charge']:.0f} kg) in {H['minutes']:.0f} minutes, in his "
                        "first vessel", 15, GREY_B)).arrange(DOWN, buff=0.05, aligned_edge=LEFT).move_to([2.6, -0.7, 0])
        c_pct = ValueTracker(H["carbon"])
        cread = always_redraw(lambda: tx(f"carbon in the iron: {c_pct.get_value():.1f}%", 20, ORE, bold=True).move_to(
            [3.6, -2.4, 0]))
        src = source("Bessemer (1905), 'The Cheltenham Paper, 1856'", size=13)
        with self.voiceover(
            "Iron from a blast furnace, pig iron, carries about five per cent carbon. That makes it hard and brittle: "
            "you can cast it, but you cannot roll it into rails or plates. To make it tough, the carbon had to come out, "
            "and that took hours of stirring in a furnace, by hand, a few hundredweight at a time. "
            "<bookmark mark='a'/> Bessemer's idea was to blow cold air through the molten iron. <bookmark mark='b'/> "
            "The oxygen burns the carbon, and the burning gives off so much heat that the iron gets hotter, not colder. "
            "No fuel, no furnace: the impurity is the fuel. <bookmark mark='c'/> What is left is steel. His first vessel "
            f"converted about {H['cwt']:.0f} hundredweight of pig iron, some {H['kg_charge']:.0f} kilograms, in "
            f"{H['minutes']:.0f} minutes. Within a generation, steel went from a craftsman's metal to the stuff of rails, "
            "ships and bridges."
        ) as vo:
            self.play(FadeIn(conv), FadeIn(iron), FadeIn(src), FadeIn(cread))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in air], lag_ratio=0.1), FadeIn(air_l), run_time=1.2)
            vo.wait_until("b")
            self.play(conv.sparks.animate.set_opacity(1), conv.glow.animate.set_opacity(0.4), FadeIn(burn),
                      c_pct.animate.set_value(2.0), run_time=2.5)
            for k in range(3):
                self.play(conv.sparks.animate.scale(1.15, about_point=conv.sparks.get_bottom()).set_opacity(0.6),
                          run_time=0.5)
                self.play(conv.sparks.animate.scale(1 / 1.15, about_point=conv.sparks.get_bottom()).set_opacity(1),
                          c_pct.animate.set_value(max(0.1, 2.0 - 0.7 * (k + 1))), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeOut(conv.sparks), FadeOut(air), FadeOut(air_l),
                      Rotate(conv.vessel, angle=-1.6, about_point=conv[2].get_center()),
                      run_time=1.6)
            ingot = draw.slab(1.6).next_to(conv, RIGHT, buff=0.2).shift(DOWN * 1.2)
            self.play(FadeIn(ingot, shift=DOWN * 0.2), FadeIn(out))
        cread.clear_updaters()
        self.clear_scene()

    def tonnes(self):
        H = R["hook"]
        vals = [("cement", H["cement"], CEMENT, draw.silo(1.0)), ("steel", H["steel"], STEELC, draw.coil(0.4)),
                ("aluminium", H["aluminium"], ALU, draw.can(0.8))]
        side = lambda v: 0.06 * np.sqrt(v)  # noqa: E731
        blocks = VGroup()
        x = -4.8
        for name, v, col, ic in vals:
            s = side(v)
            sq = Square(s, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.35).move_to([x + s / 2, -1.9 + s / 2, 0])
            ic.scale_to_fit_height(0.7).next_to(sq, UP, buff=0.12)
            lab = VGroup(tx(name, 22, col, bold=True), tx(f"{v:,.0f} million tonnes", 18, WHITE)).arrange(
                DOWN, buff=0.04).next_to(sq, DOWN, buff=0.12)
            blocks.add(VGroup(sq, ic, lab))
            x += s + 1.0
        head = tx("Made in one year, 2025", 26, WHITE, bold=True).to_edge(UP, buff=0.5)
        pc = VGroup(tx(f"{H['steel_pc']:.0f} kg", 40, STEELC, bold=True),
                    tx("of finished steel used per person on Earth", 17, GREY_A)).arrange(DOWN, buff=0.06).move_to(
            [4.6, 1.6, 0])
        src = source("USGS, Mineral Commodity Summaries 2026 (cement, aluminium); World Steel Association, World Steel in "
                     "Figures 2026 (steel)", size=13)
        with self.voiceover(
            "Today the world makes steel by the billion tonnes. <bookmark mark='a'/> In 2025, about "
            f"{H['steel']:,.0f} million tonnes of it. <bookmark mark='b'/> Even more cement: some "
            f"{H['cement'] / 1000:.1f} billion tonnes, about twice the weight of the steel. <bookmark mark='c'/> And "
            f"{H['aluminium']:.0f} million tonnes of new aluminium. <bookmark mark='d'/> Spread over everyone, about "
            f"{H['steel_pc']:.0f} kilograms of finished steel a year for every person on Earth: in buildings, cars, "
            "pipes, cans and machines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for m, k in zip("abc", (1, 0, 2)):
                vo.wait_until(m)
                b = blocks[k]
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1], shift=DOWN * 0.2), FadeIn(b[2]), run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(pc, shift=LEFT * 0.2))
        self.clear_scene()

    def per_kg(self):
        H = R["hook"]
        pk = H["per_kg"]
        order = [("crushed stone", STONE, draw.pile(0.8, "#9AA0A6", 50, 4, "jagged")), ("cement", CEMENT, draw.silo(0.8)),
                 ("steel", STEELC, draw.coil(0.35)), ("bananas", "#F2D04E", draw.banana(0.5)),
                 ("aluminium", ALU, draw.can(0.7))]
        pa = viz.plot_axes([0, 6], [np.log10(0.01), np.log10(5)], x_length=10.2, y_length=4.4,
                           xticks=[], yticks=[np.log10(v) for v in (0.01, 0.1, 1, 5)],
                           yfmt=lambda v: cents(10 ** v), ylabel="price a kilogram (log scale)", size=14).move_to([0.2, -0.5, 0])
        bars = VGroup()
        for i, (name, col, ic) in enumerate(order):
            v = pk[name]
            x = 0.6 + 1.2 * i
            base = pa.ax.c2p(x, np.log10(0.01))
            top = pa.ax.c2p(x, np.log10(v))
            b = Rectangle(width=0.7, height=top[1] - base[1], stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                base, aligned_edge=DOWN)
            ic.scale_to_fit_height(0.5)
            if ic.width > 0.8:
                ic.scale_to_fit_width(0.8)
            ic.next_to(b, UP, buff=0.32)
            val = tx(cents(v), 18, WHITE, bold=True).next_to(b, UP, buff=0.04)
            nm = tx(name, 16, col, bold=True).next_to(base, DOWN, buff=0.1)
            bars.add(VGroup(b, val, ic, nm))
        head = tx("What a kilogram costs", 26, WHITE, bold=True).to_edge(UP, buff=0.4)
        note = tx("steel: hot-rolled sheet, US index, 2025; aluminium: London price, " + mlabel(H["alu_month"]) +
                  "; bananas: US shops, " + mlabel(H["banana_month"]), 13, GREY_B).next_to(pa, DOWN, buff=0.45)
        src = source("USGS MCS 2026 (stone, cement); Cleveland-Cliffs 10-K 2025 (hot-rolled coil); IMF and BLS prices "
                     "via FRED", size=13)
        with self.voiceover(
            "And they are astonishingly cheap. Here is what a kilogram costs, on a scale where each step is ten times "
            "the last. <bookmark mark='a'/> Crushed stone, the gravel in every road and every slab of concrete: about "
            f"{100 * pk['crushed stone']:.0f} cents a kilogram at the quarry. <bookmark mark='b'/> Cement: about "
            f"{100 * pk['cement']:.0f} cents. <bookmark mark='c'/> Steel sheet, rolled and coiled: about "
            f"{100 * pk['steel']:.0f} cents. <bookmark mark='d'/> For comparison, a kilogram of bananas in an American "
            f"shop: {say_money(pk['bananas'])}. Steel, cheaper than fruit. <bookmark mark='e'/> Aluminium, the dear one "
            f"of the family, about {say_money(pk['aluminium'])}."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), FadeIn(note))
            for m, b in zip("abcde", bars):
                vo.wait_until(m)
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[3]), run_time=0.9)
                self.play(FadeIn(b[1]), FadeIn(b[2], shift=DOWN * 0.15), run_time=0.5)
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        stuff = VGroup(draw.ibeam(0.8), draw.coil(0.42), draw.rebar(1.3, 4), draw.silo(1.0), draw.mixer_truck(1.6),
                       draw.can(0.8), draw.carton(0.7), draw.pile(1.0, "#9AA0A6", 60, 5, "jagged")).arrange(RIGHT, buff=0.45)
        stuff.scale_to_fit_width(12.5).move_to([0, 0.2, 0])
        with self.voiceover(
            "These are the materials everything else is made of, <bookmark mark='a'/> made in plants that cost billions "
            "and last half a century, and yet the companies that make them mostly earn thin and unreliable profits. "
            "<bookmark mark='b'/> Industry, Built. Part eleven: heavy materials. Why do the things everything is made of "
            "earn so little?"
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m_, shift=UP * 0.2) for m_ in stuff], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("a")
            self.play(stuff.animate.scale(0.6).to_edge(DOWN, buff=0.4).set_opacity(0.5), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeOut(stuff), FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
