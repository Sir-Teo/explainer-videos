from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403


def donut(parts, r=1.3, w=0.45):
    g = VGroup()
    a0 = PI / 2
    for share, col in parts:
        ang = -TAU * share
        g.add(AnnularSector(inner_radius=r - w, outer_radius=r, angle=ang, start_angle=a0, fill_color=col,
                            fill_opacity=0.9, stroke_color=BACKGROUND, stroke_width=2))
        a0 += ang
    return g


class State(VoiceoverScene):
    def construct(self):
        card(self, 10, "The state takes its share", "Who owns the copper under a country's mountains?",
             "Chapter ten. The state takes its share.", lit=("dollar", "moat"))
        self.split()
        self.grasberg()
        self.levers()

    def split(self):
        T = R["take"]
        parts = [("running the mine", T["cost"], COST), ("building and closing", T["capex"] + T["closure"], "#6F8FB8"),
                 ("royalty", T["royalty"], STATE), ("income tax", T["tax"], "#F28B82"), ("the owners", T["owners"],
                                                                                       PRICE)]
        W = 12.0
        x = -W / 2
        blocks = VGroup()
        labs = VGroup()
        for k, (n, v, c) in enumerate(parts):
            w = W * v / T["revenue"]
            b = Rectangle(width=w, height=1.0, stroke_width=1, stroke_color=BACKGROUND, fill_color=c,
                          fill_opacity=0.9).move_to([x + w / 2, 0.4, 0])
            blocks.add(b)
            labs.add(VGroup(tx(n, 16, c, bold=True), tx(f"${v / 1000:.1f}bn", 16, WHITE)).arrange(DOWN, buff=0.03
                                                                                               ).next_to(
                b, DOWN if k % 2 == 0 else UP, buff=0.15))
            x += w
        whole = Rectangle(width=W, height=1.0, stroke_color=WHITE, stroke_width=2, fill_color=COPPER,
                          fill_opacity=0.25).move_to([0, 0.4, 0])
        wl = tx(f"everything the model mine sells over its life at ${T['price']:.2f} a pound: "
                f"${T['revenue'] / 1000:.1f}bn", 19, WHITE, bold=True).next_to(whole, UP, buff=0.9)
        state = Brace(VGroup(blocks[2], blocks[3]), DOWN, buff=0.9, color=STATE)
        sl = VGroup(tx("the state", 20, STATE, bold=True),
                    tx(f"{100 * T['state_share']:.0f}% of the profit, before anyone else is paid", 16, WHITE)).arrange(
            DOWN, buff=0.04).next_to(state, DOWN, buff=0.08)
        ground = Rectangle(width=14.4, height=3.0, stroke_width=0, fill_color="#4E4034", fill_opacity=1).move_to(
            [0, -2.5, 0])
        grass = Rectangle(width=14.4, height=0.25, stroke_width=0, fill_color="#5E7A3A", fill_opacity=1).move_to(
            [0, -0.9, 0])
        farm = VGroup(draw.house(1.0), draw.house(0.7).shift(RIGHT * 0.9 + DOWN * 0.08)).move_to([-2.5, -0.35, 0])
        ore_ = Ellipse(width=4.0, height=1.0, stroke_width=0, fill_color=COPPER, fill_opacity=0.85).move_to([0.6, -2.7, 0])
        l_land = VGroup(tx("the land:", 20, GREY_A), tx("whoever owns it", 20, WHITE, bold=True)).arrange(
            DOWN, buff=0.05).move_to([-2.4, 1.2, 0])
        l_min = VGroup(tx("the minerals beneath:", 20, GREY_A), tx("in most countries, the state", 20, STATE, bold=True)
                       ).arrange(DOWN, buff=0.05).move_to([4.7, -1.75, 0])
        l_min = VGroup(BackgroundRectangle(l_min, color=BACKGROUND, fill_opacity=0.85, buff=0.12), l_min)
        intro = VGroup(ground, grass, farm, ore_, l_land, l_min)
        tag = estimate_tag(f"the Works' model mine (mine.py): {100 * T['royalty_rate']:.0f}% royalty, "
                           f"{100 * T['tax_rate']:.0f}% income tax; undiscounted", corner=DR, size=14)
        with self.voiceover(
            "In almost every country outside the United States, the minerals under the ground belong to the state, not "
            "to whoever owns the land on top. A mining company is a tenant. It digs, and pays rent. "
            f"<bookmark mark='a'/> Take everything our model mine sells over its life at four fifty a pound: about "
            f"{T['revenue'] / 1000:.0f} billion dollars. <bookmark mark='b'/> Running the mine takes about half. "
            "Building it and closing it takes more. <bookmark mark='c'/> The state takes a royalty, a share of every "
            "dollar sold, and an income tax on the profit. <bookmark mark='d'/> What is left belongs to the owners. "
            f"With a four percent royalty and a twenty-seven percent tax, the state takes about "
            f"{100 * T['state_share']:.0f} percent of the mine's profit, and it takes the royalty even in years when the "
            "mine makes none. Many countries take far more: through bigger royalties, special mining taxes, or by "
            "owning part of the mine itself."
        ) as vo:
            self.play(FadeIn(ground), FadeIn(grass), FadeIn(farm, shift=DOWN * 0.2), FadeIn(l_land))
            self.play(FadeIn(ore_, scale=0.7), FadeIn(l_min))
            vo.wait_until("a")
            self.play(FadeOut(intro), FadeIn(tag))
            self.play(FadeIn(whole), FadeIn(wl))
            vo.wait_until("b")
            self.play(FadeOut(whole), FadeIn(blocks[0]), FadeIn(labs[0]))
            self.play(FadeIn(blocks[1]), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(FadeIn(blocks[2]), FadeIn(labs[2]))
            self.play(FadeIn(blocks[3]), FadeIn(labs[3]))
            vo.wait_until("d")
            self.play(FadeIn(blocks[4]), FadeIn(labs[4]))
            self.play(GrowFromCenter(state), FadeIn(sl))
        self.clear_scene()

    def grasberg(self):
        st = get("fcx.ptfi.state") / 100
        ring = donut([(0.2624, STATE), (0.25, "#F28B82"), (1 - st, COPPER)]).move_to([-4.2, 0.6, 0])
        mid = VGroup(tx("PT Freeport", 16, WHITE, bold=True), tx("Indonesia", 16, WHITE, bold=True)).arrange(
            DOWN, buff=0.03).move_to(ring)
        key = VGroup(tx("MIND ID, the state's mining company: 26.24%", 15, STATE),
                     tx("PT Indonesia Papua Metal dan Mineral: 25.00%", 15, "#F28B82"),
                     tx(f"Freeport-McMoRan: {100 * (1 - st):.2f}%", 15, COPPER)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.08).next_to(ring, DOWN,
                                                                                                          buff=0.35)
        pa = viz.plot_axes([0, 2], [0, 2000], x_length=3.6, y_length=3.0, xticks=[], yticks=[500, 1000, 1500, 2000],
                           yfmt=lambda v: f"{v:,.0f}", size=13).move_to([3.4, 0.4, 0])
        v24, v25 = get("fcx.ptfi.prod.2024"), get("fcx.ptfi.prod")
        b24 = Rectangle(width=0.9, height=pa.ax.c2p(0, v24)[1] - pa.ax.c2p(0, 0)[1], stroke_width=0, fill_color=COPPER,
                        fill_opacity=0.9).move_to(pa.ax.c2p(0.55, 0), aligned_edge=DOWN)
        b25 = Rectangle(width=0.9, height=pa.ax.c2p(0, v25)[1] - pa.ax.c2p(0, 0)[1], stroke_width=0, fill_color=STATE,
                        fill_opacity=0.9).move_to(pa.ax.c2p(1.45, 0), aligned_edge=DOWN)
        bl = VGroup(tx("2024", 15, GREY_A).next_to(b24, DOWN, buff=0.08), tx("2025", 15, GREY_A).next_to(b25, DOWN, buff=0.08),
                    tx(f"{v24:,.0f}", 15, WHITE, bold=True).next_to(b24, UP, buff=0.06),
                    tx(f"{v25:,.0f}", 15, WHITE, bold=True).next_to(b25, UP, buff=0.06))
        ttl = tx("Grasberg's copper, million pounds", 16, GREY_A).next_to(pa, UP, buff=0.15)
        rush = VGroup(tx("8 September 2025: a mud rush in the", 16, WHITE),
                      tx(f"Grasberg Block Cave mine kills {get('fcx.mudrush'):.0f} workers", 16, STATE, bold=True)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.04).next_to(pa, DOWN, buff=0.6)
        src = source("Freeport-McMoRan, Form 10-K for 2025", size=13)
        with self.voiceover(
            "Sometimes the state takes the mine itself. <bookmark mark='a'/> Grasberg, in the highlands of Indonesian "
            "Papua, was run for half a century by the American company Freeport-McMoRan. Since December 2018, "
            f"Indonesian state-owned and regional interests have held {100 * st:.2f} percent of it, and Freeport the "
            "rest, though Freeport still runs it. Indonesia got control of one of the world's richest mines; Freeport "
            "got the right to keep operating it for decades more. <bookmark mark='b'/> And the rock itself pushes "
            "back. Much of Grasberg is now mined underground, by block caving: the miners undercut a huge column of "
            "ore and let it collapse under its own weight into tunnels below. On the eighth of September 2025, a rush "
            f"of wet mud flooded the workings and killed {get('fcx.mudrush'):.0f} workers. <bookmark mark='c'/> "
            f"Grasberg's copper output fell from about {v24:,.0f} million pounds in 2024 to {v25:,.0f} million in 2025, "
            "and a phased restart is planned from 2026. A mine is not only a bet on the price; it is a bet on the rock, "
            "and the people inside it bear that risk first."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(s_, scale=0.9) for s_ in ring], lag_ratio=0.3), FadeIn(mid),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k_) for k_ in key], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(pa), FadeIn(ttl), GrowFromEdge(b24, DOWN), FadeIn(bl[0]), FadeIn(bl[2]))
            self.play(FadeIn(rush, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(GrowFromEdge(b25, DOWN), FadeIn(bl[1]), FadeIn(bl[3]))
        self.clear_scene()

    def levers(self):
        wm = draw.world_map(12.4).move_to([0, 0.35, 0])
        congo = wm.p(24, -4)
        indo = wm.p(122, -2)
        aus = wm.p(122, -28)
        cq, cm = get("usgs.co.quota"), get("usgs.co.congo.mine")
        cards = VGroup()

        def panel(title, lines, col, at):
            body = VGroup(tx(title, 17, col, bold=True), *[tx(l_, 14, WHITE) for l_ in lines]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05)
            box = RoundedRectangle(corner_radius=0.1, width=body.width + 0.3, height=body.height + 0.25,
                                   stroke_color=col, stroke_width=1.5, fill_color="#141A24", fill_opacity=0.95)
            return VGroup(box, body.move_to(box)).move_to(at)
        c1 = panel("Congo: cobalt", [f"{get('usgs.co.congo'):.0f}% of the world's cobalt mining", "Feb 2025: exports banned",
                                     f"from Oct: a quota of {cq:,.0f} t a year,", f"against {cm:,.0f} t mined in 2025",
                                     f"price: ${get('usgs.co.price.2024'):.2f} a pound (2024)",
                                     f"to about ${get('usgs.co.price.2025'):.0f} (2025)"], STATE, [-2.2, -2.0, 0])
        c2 = panel("Indonesia: nickel", [f"{get('usgs.ni.indonesia.2024') / 1000:.2f} to "
                                         f"{get('usgs.ni.indonesia') / 1000:.1f} million tonnes, 2024 to 2025",
                                         "two-thirds of the world's mined nickel"], "#7EC8F5", [4.4, 2.3, 0])
        c3 = panel("Australia: nickel", [f"98 to {get('usgs.ni.australia'):.0f} thousand tonnes",
                                         "mines shut by low prices"], GREY_A, [4.6, -2.3, 0])
        cards.add(c1, c2, c3)
        lines = VGroup(Line(congo, c1.get_top(), stroke_color=STATE, stroke_width=1.5),
                       Line(indo, c2.get_bottom(), stroke_color="#7EC8F5", stroke_width=1.5),
                       Line(aus, c3.get_top(), stroke_color=GREY_A, stroke_width=1.5))
        dots = VGroup(Dot(congo, color=STATE, radius=0.09), Dot(indo, color="#7EC8F5", radius=0.09),
                      Dot(aus, color=GREY_A, radius=0.09))
        head = tx("Governments that move the market", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'cobalt' and 'nickel'", size=13)
        with self.voiceover(
            "And sometimes a state does more than collect rent: it moves the whole market. <bookmark mark='a'/> Congo "
            "produces about three-quarters of the world's cobalt, a metal used in batteries, mostly as a by-product of "
            "its copper mines. In February 2025, with prices low, it banned cobalt exports outright. In October it "
            f"replaced the ban with quotas: {cq:,.0f} tonnes a year for 2026 and 2027, less than half of the "
            f"{cm:,.0f} tonnes its mines produced in 2025. The price of cobalt on the London Metal Exchange rose from "
            f"about {get('usgs.co.price.2024'):.0f} dollars a pound in 2024 to about {get('usgs.co.price.2025'):.0f}. "
            "That is a cartel of one. <bookmark mark='b'/> Indonesia took the opposite route. Since 2020 it has banned "
            "the export of raw nickel ore, so anyone who wanted its nickel had to build smelters in Indonesia, and "
            f"Chinese companies did. Its mines produced {get('usgs.ni.indonesia') / 1000:.1f} million tonnes of nickel "
            "in 2025, two-thirds of the world's. <bookmark mark='c'/> The flood of Indonesian nickel pushed prices "
            "down, and Australia's nickel mines, among the oldest in the business, could not compete. Its output fell "
            f"by more than half in a single year, to {get('usgs.ni.australia'):.0f} thousand tonnes, as one company "
            "after another put its mines on care and maintenance."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(dots[0], scale=2), Create(lines[0]), FadeIn(c1, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(dots[1], scale=2), Create(lines[1]), FadeIn(c2, shift=DOWN * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(dots[2], scale=2), Create(lines[2]), FadeIn(c3, shift=UP * 0.1))
        self.clear_scene()
