from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


def skyline(m, width=12.0, hmax=3.2, far_max=3.0, x_max=36.0, color=CITY):
    """The city seen from the side: one bar per half kilometre, its height the floor-area ratio there."""
    x = np.array(m["x"])
    far = np.nan_to_num(np.array(m["far"]), nan=0.0)
    xs = np.arange(-x_max + 0.25, x_max, 0.5)
    g = VGroup()
    for xc in xs:
        f = float(np.interp(abs(xc), x, far, right=0.0))
        h = max(hmax * f / far_max, 0.0)
        w = width / (2 * x_max) * 0.5
        bar = Rectangle(width=w * 0.92, height=max(h, 0.001), stroke_width=0, fill_color=color,
                        fill_opacity=0.85 if h > 0.002 else 0.0)
        bar.move_to(np.array([xc / (2 * x_max) * width, h / 2, 0]))
        g.add(bar)
    return g


class Mono(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The monocentric city", r"Why does rent fall with distance from the centre?",
             "Chapter three. The monocentric city.", lit={1964: r"Alonso", 1967: r"Mills", 1969: r"Muth"},
             scale=("household", "city"), horizon=("a decade",))
        self.gradient()
        self.skyline_scene()

    def gradient(self):
        M = load("mono")
        b, c = M["base"], M["car"]
        P = M["params"]
        ax = plane([0, 32], [0, 1.0], center=LEFT * 1.8 + DOWN * 0.45, x_length=8.6, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"kilometres from the centre", ylabel=r"floor rent, \ relative to the centre",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        p0 = b["p0"]
        ln = path(ax, b["x"], np.array(b["p"]) / p0, RENT, 3.4, xr=(0, b["edge"]))
        edge = vline(ax, b["edge"], 0, 1.0, GREY_B)
        eq = MathTex(r"p'(x)\,h(x) = -t", font_size=40).to_edge(UP, buff=0.35).shift(RIGHT * 3.0)
        side = VGroup(
            label(r"move one kilometre out: \\ commuting costs $t$ more, \\ so the rent on your $h$ \\ square metres "
                  r"must fall \\ by as much", font_size=18, color=WHITE),
            label(rf"near the centre \\ rent falls \ {M['grad']:.1f}\% a km", font_size=19, color=RENT),
            label(rf"the edge, \ {b['edge']:.0f} km: \\ where farming \\ outbids housing", font_size=18, color=FARM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In the 1960s William Alonso, Edwin Mills and Richard Muth turned von Thünen's farmers into commuters. "
            f"A town of a million households, each earning sixty thousand dollars, all working in one centre. "
            "Commuting costs about a thousand dollars a year for each kilometre from the centre. "
            "<bookmark mark='a'/> In equilibrium nobody can gain by moving, so every location must be equally good. "
            "Move one kilometre out and your commute costs more; the rent on your floor space must fall by exactly "
            "as much. <bookmark mark='b'/> That condition is a differential equation for the rent gradient, and "
            f"here is its solution: rent falls about {M['grad']:.1f} percent a kilometre near the centre. "
            f"<bookmark mark='c'/> The town ends at {b['edge']:.0f} kilometres, where housing can no longer outbid "
            "farming for land."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(eq))
            vo.wait_until("b")
            self.play(Indicate(ln, color=WHITE, scale_factor=1.0), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(edge), FadeIn(side[2]))
        _ = (c, P)
        self.clear_scene()

    def skyline_scene(self):
        M = load("mono")
        b, c, li = M["base"], M["car"], M["lift"]
        ground = Line(LEFT * 6.4, RIGHT * 6.4, color=GREY_B, stroke_width=2).shift(DOWN * 1.6)
        sb = skyline(b).shift(DOWN * 1.6)
        sc = skyline(c).shift(DOWN * 1.6)
        sl = skyline(li).shift(DOWN * 1.6)
        centre = Triangle(color=E.ACCENT, fill_opacity=1, stroke_width=0).scale(0.1).rotate(PI).next_to(
            ground, DOWN, buff=0.05)
        clab = label(r"the centre", font_size=15, color=E.ACCENT).next_to(centre, DOWN, buff=0.05)
        ticks = VGroup(*[label(f"{abs(k)}", font_size=13, color=GREY_B).move_to(
            np.array([k / 72 * 12.0, -1.95, 0])) for k in (-30, -20, -10, 10, 20, 30)])
        km = label(r"km", font_size=13, color=GREY_B).move_to(np.array([6.0, -1.95, 0]))
        head = label(r"the town from the side: \ height = floor space per square metre of land", font_size=22,
                     color=GREY_A).to_edge(UP, buff=0.35)

        def stats(m, col, title):
            return VGroup(
                label(title, font_size=22, color=col),
                label(rf"edge \ {m['edge']:.0f} km; \ centre: \ {m['centre_density']:,.0f} households a km$^2$; \ "
                      rf"{100 * m['within8']:.0f}\% within 8 km; \ {m['h0']:.0f} m$^2$ each", font_size=18,
                      color=WHITE),
            ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)

        s0 = stats(b, CITY, r"the town")
        s1 = stats(c, ROAD, r"the car: \ commuting costs halve")
        s2 = stats(li, AMENITY, r"the lift: \ building up costs 40\% less")
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Developers build up where land is dear. Here is the town from the side, each bar the floor space built "
            "on a square metre of land: towers at the centre, houses at the edge. <bookmark mark='a'/> Now give "
            "everyone a car, halving the cost of commuting. The rent gradient flattens, and the town spreads out: "
            f"its edge moves from {b['edge']:.0f} kilometres to {c['edge']:.0f}, the density at the centre falls "
            f"by {100 * (1 - c['centre_density'] / b['centre_density']):.0f} percent, and the share of households "
            f"within eight kilometres from {100 * b['within8']:.0f} percent to {100 * c['within8']:.0f}. "
            "<bookmark mark='b'/> Instead, give everyone the lift and steel frames, making height forty percent "
            "cheaper to build. The town grows up, not out: the same edge and the same densities, but taller "
            f"buildings, and {li['h0']:.0f} square metres for each household at the centre instead of "
            f"{b['h0']:.0f}. <bookmark mark='c'/> The car helped make the American suburb, and the lift helped "
            "make Manhattan; both come out of this one equation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ground), FadeIn(centre), FadeIn(clab), FadeIn(ticks), FadeIn(km),
                      FadeIn(tag), LaggedStart(*[GrowFromEdge(r, DOWN) for r in sb], lag_ratio=0.004),
                      FadeIn(s0), run_time=2.5)
            vo.wait_until("a")
            self.play(Transform(sb, sc), ReplacementTransform(s0, s1), run_time=2.0)
            vo.wait_until("b")
            self.play(Transform(sb, sl), ReplacementTransform(s1, s2), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(sb, color=WHITE, scale_factor=1.02))
        self.clear_scene()
