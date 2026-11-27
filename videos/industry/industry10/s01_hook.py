from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.wheat()
        self.yields()
        self.dollar()
        self.title()

    def wheat(self):
        H = R["hook"]
        sky = Rectangle(width=14.4, height=5.0, stroke_width=0, fill_color="#1C3557", fill_opacity=1).move_to([0, 1.6, 0])
        soil = Rectangle(width=14.4, height=3.0, stroke_width=0, fill_color=SOIL, fill_opacity=1).move_to([0, -2.6, 0])
        sun = draw.sun(0.45).move_to([5.8, 3.1, 0])
        where = VGroup(tx("Mexico, the 1940s and 1950s", 22, WHITE, bold=True),
                       tx("Norman Borlaug, plant scientist", 18, GREY_A)).arrange(DOWN, buff=0.06, aligned_edge=LEFT
                                                                                 ).to_corner(UL, buff=0.4)
        tall = VGroup(*[draw.wheat(2.2) for _ in range(9)]).arrange(RIGHT, buff=0.22).move_to([-3.4, -1.1, 0],
                                                                                              aligned_edge=DOWN)
        dwarf = VGroup(*[draw.wheat(2.2, dwarf=True) for _ in range(9)]).arrange(RIGHT, buff=0.22).move_to(
            [3.4, -1.1, 0], aligned_edge=DOWN)
        for g in (tall, dwarf):
            g.align_to([0, -1.1, 0], DOWN)
        lt = VGroup(tx("the old tall wheat", 20, WHITE, bold=True), tx("fertilize it, and it falls over", 16, GREY_A)
                    ).arrange(DOWN, buff=0.04).next_to(tall, DOWN, buff=0.35)
        ld = VGroup(tx("Borlaug's dwarf wheat", 20, WHEATC, bold=True), tx("short, stiff, heavy with grain", 16, GREY_A)
                    ).arrange(DOWN, buff=0.04).next_to(dwarf, DOWN, buff=0.35)
        bag = draw.sack(0.8, label_="N").move_to([0, 0.8, 0])
        stamp = VGroup(tx(f"Mexico grows all its own wheat by {H['mexico']:.0f}", 19, WHEATC, bold=True),
                       tx("India and Pakistan from the mid-1960s", 17, WHITE),
                       tx(f"Nobel Peace Prize, {H['prize']:.0f}", 17, PRICE)).arrange(DOWN, buff=0.06).move_to([-3.2, 1.9, 0])
        src = source("The Nobel Foundation, 'Norman Borlaug - Facts', NobelPrize.org", size=13)
        with self.voiceover(
            "In the 1940s, an American plant scientist named Norman Borlaug went to Mexico to help its farmers grow more "
            "wheat. <bookmark mark='a'/> The wheat they grew was tall and thin. <bookmark mark='b'/> Feed it fertilizer, "
            "and its heads grew heavy, and the stalks bent and fell over before harvest, flattening the crop into the "
            "mud. <bookmark mark='c'/> So Borlaug and his team bred a short wheat, a dwarf, with a thick stem that could "
            "carry a big head of grain without falling. They crossed thousands of plants, two crops a year, in two "
            "corners of the country. <bookmark mark='d'/> By 1956, Mexico grew all the wheat it needed. In the mid-1960s "
            "the dwarf wheat went to India and Pakistan, where famine was feared, and production rose enormously. In "
            "1970 Borlaug won the Nobel Peace Prize, for having given, in the committee's words, a well-founded hope: "
            "the green revolution."
        ) as vo:
            self.play(FadeIn(sky), FadeIn(soil), FadeIn(sun), FadeIn(where), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(w, DOWN) for w in tall], lag_ratio=0.15), FadeIn(lt), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bag, shift=DOWN * 0.3))
            self.play(bag.animate.move_to(tall.get_center() + UP * 1.4).scale(0.6), run_time=0.8)
            self.play(FadeOut(bag), *[w.head.animate.scale(1.3, about_point=w.head.get_bottom()) for w in tall], run_time=0.8)
            self.play(*[Rotate(w, angle=-1.2 + 0.08 * k, about_point=w.get_bottom()) for k, w in enumerate(tall)],
                      run_time=1.6, rate_func=rush_into)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(w, DOWN) for w in dwarf], lag_ratio=0.15), FadeIn(ld), run_time=2.0)
            self.play(*[w.head.animate.scale(1.2, about_point=w.head.get_bottom()) for w in dwarf], run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(stamp, shift=DOWN * 0.1))
        self.clear_scene()

    def yields(self):
        H = R["hook"]
        W = H["wheat"]
        cols = {"Mexico": WHEATC, "India": FARM, "Pakistan": TRADE, "World": WHITE}
        pa = viz.plot_axes([1961, 2024], [0, 7], x_length=10.4, y_length=4.8, xticks=[1961, 1970, 1980, 1990, 2000, 2010, 2024],
                           yticks=[1, 2, 3, 4, 5, 6], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g} t",
                           ylabel="wheat harvested per hectare, tonnes", size=15).move_to([-0.4, -0.4, 0])
        t = ValueTracker(1961)

        def line(e):
            pts = sorted(W[e].items())

            def f():
                q = [pa.ax.c2p(y, v) for y, v in pts if y <= t.get_value()]
                return VMobject(stroke_color=cols[e], stroke_width=3.5 if e != "World" else 2.5).set_points_as_corners(
                    q) if len(q) > 1 else VMobject()
            return always_redraw(f)
        lines = VGroup(*[line(e) for e in cols])
        labs = VGroup(*[tx(f"{e} x{H[e + '_x']:.1f}", 17, cols[e], bold=True).next_to(
            pa.ax.c2p(2024, W[e][2024]), RIGHT, buff=0.12) for e in cols])
        labs[3].shift(UP * 0.16)
        labs[1].shift(DOWN * 0.02)
        labs[2].shift(DOWN * 0.2)
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=34, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        yr.update()
        mark = DashedLine(pa.ax.c2p(1966, 0), pa.ax.c2p(1966, 6.6), stroke_color=GREY_B, stroke_width=1.2)
        ml = tx("dwarf wheat reaches India and Pakistan", 14, GREY_A).next_to(pa.ax.c2p(1966, 6.6), RIGHT, buff=0.1)
        head = tx("Wheat yields since 1961", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("FAO (FAOSTAT) via Our World in Data, wheat yields", size=13)
        with self.voiceover(
            "Here is what followed, in the data the United Nations' Food and Agriculture Organization has kept since "
            "1961: tonnes of wheat harvested from each hectare. <bookmark mark='a'/> In the 1960s, India and Pakistan "
            "harvested less than a tonne a hectare. <bookmark mark='b'/> Watch them climb as the new wheat, fertilizer "
            f"and irrigation spread. Since 1961 India's yield has multiplied {H['India_x']:.1f} times, Pakistan's "
            f"{H['Pakistan_x']:.1f}, Mexico's {H['Mexico_x']:.1f}, and the world's {H['World_x']:.1f}. "
            "<bookmark mark='c'/> The famines that many experts predicted for the 1970s did not come on anything like "
            "the scale they feared. It is one of the greatest things any industry has ever done."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src))
            self.add(lines, yr)
            vo.wait_until("a")
            self.play(t.animate.set_value(1966), run_time=2.0, rate_func=linear)
            self.play(Create(mark), FadeIn(ml))
            vo.wait_until("b")
            self.play(t.animate.set_value(2024), run_time=7.0, rate_func=linear)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in labs], lag_ratio=0.2))
        for m in (*lines, yr):
            m.clear_updaters()
        self.clear_scene()

    def dollar(self):
        D = R["dollar"]
        coin = Circle(2.0, stroke_color=PRICE, stroke_width=5, fill_color="#3A2F10", fill_opacity=1).move_to([-3.2, -0.2, 0])
        cl = tx("$1", 60, PRICE, bold=True).move_to(coin)
        farm_sector = AnnularSector(inner_radius=0.0, outer_radius=2.0, angle=-TAU * D["farm"] / 100, start_angle=PI / 2,
                                    fill_color=FARM, fill_opacity=0.95, stroke_width=0).move_to(coin.get_center(),
                                                                                              aligned_edge=ORIGIN)
        farm_sector.shift(coin.get_center() - ORIGIN)
        rest = AnnularSector(inner_radius=0.0, outer_radius=2.0, angle=-TAU * (1 - D["farm"] / 100),
                             start_angle=PI / 2 - TAU * D["farm"] / 100, fill_color="#3A4558", fill_opacity=0.95,
                             stroke_width=0)
        rest.shift(coin.get_center() - ORIGIN)
        for s_ in (farm_sector, rest):
            s_.move_arc_center_to(coin.get_center())
        right = VGroup(tx(f"Of every dollar Americans spent on food in {D['year']}:", 22, WHITE),
                       tx(f"{D['farm']:.1f} cents went to farms", 34, FARM, bold=True),
                       tx(f"{100 - D['farm']:.1f} cents to everything after the farm gate", 22, GREY_A),
                       tx(f"(at a grocery store: {D['home']:.1f} cents; at a restaurant: {D['away']:.1f})", 18, GREY_B)
                       ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([2.9, 0.0, 0])
        src = source(f"USDA Economic Research Service, Food Dollar Series (November 2026), {D['year']}", size=13)
        with self.voiceover(
            "And yet. <bookmark mark='a'/> Take a dollar that an American spent on food in "
            f"{D['year']}, at a supermarket or a restaurant. <bookmark mark='b'/> According to the Department of "
            f"Agriculture's economists, about {D['farm']:.1f} cents of it went to farms. "
            f"<bookmark mark='c'/> The other {100 - D['farm']:.0f}-odd cents went to everything that happens after the "
            "farm gate: processing, packing, shipping, selling, cooking and serving. Farmers have multiplied what an "
            "acre can grow, again and again, and kept a small and shrinking slice of what we pay for food. This part is "
            "about why."
        ) as vo:
            self.play(FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromCenter(coin), Write(cl))
            vo.wait_until("b")
            self.play(FadeOut(cl), FadeOut(coin), FadeIn(rest), FadeIn(farm_sector))
            self.play(farm_sector.animate.shift((RIGHT * 0.35 + UP * 0.25)), FadeIn(right[0]), FadeIn(right[1]))
            vo.wait_until("c")
            self.play(FadeIn(right[2:], shift=UP * 0.1))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part ten: farming and food. Why do farmers grow ever more, and keep so little of what we "
            "pay?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
