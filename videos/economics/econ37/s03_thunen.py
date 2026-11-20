from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403

SHORT = {"vegetables and milk": r"vegetables \\ and milk", "firewood": r"firewood", "grain": r"grain",
         "cattle": r"cattle"}


def rings_map(rings, names, centre, scale=0.29, max_km=None):
    """Concentric rings, radius proportional to the square root of distance (so the inner rings show)."""
    g = VGroup()
    for name, a, b in reversed(rings):
        if max_km:
            b = min(b, max_km)
        k = names.index(name)
        g.add(Circle(radius=scale * np.sqrt(b), stroke_color=GREY_D, stroke_width=1, fill_color=RING_COLORS[k],
                     fill_opacity=0.75).move_to(centre))
    g.add(Dot(centre, radius=0.07, color=WHITE))
    return g


class Thunen(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Von Th\"unen's rings", r"What grows where, around a market town?",
             "Chapter two. Von Thünen's rings.", lit={1826: r"von Th\"unen, \ \emph{The Isolated State}"},
             scale=("firm", "city"), horizon=("a decade",))
        self.bids()
        self.railway()

    def bids(self):
        T = load("thunen")
        names = T["names"]
        ax = plane([0, 60], [0, 1000], center=LEFT * 4.0 + DOWN * 0.45, x_length=5.4, y_length=4.4,
                   xticks=[0, 20, 40, 60], yticks=[0, 250, 500, 750, 1000],
                   xlabel=r"kilometres from the market", ylabel=r"rent a farmer can pay, \ \$ a hectare a year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        x = np.array(T["x"])
        lines = VGroup(*[path(ax, x, b, RING_COLORS[k], 3.0, xr=(0, 60), yr=(0, 1000), smooth=False)
                         for k, b in enumerate(T["bids"])])
        env = path(ax, x, np.max(np.array(T["bids"]), axis=0), WHITE, 5.0, xr=(0, 60), yr=(0, 1000), smooth=False)
        eq = MathTex(r"\text{rent}(x) = \text{yield}\times(\text{price} - \text{cost} - \text{freight}\times x)",
                     font_size=28).to_edge(UP, buff=0.3)
        centre = RIGHT * 1.7 + DOWN * 0.4
        mp = rings_map(T["rings"], names, centre, scale=0.25)
        legend = VGroup()
        for n, a, b in T["rings"]:
            k = names.index(n)
            legend.add(VGroup(Square(side_length=0.28, stroke_width=0, fill_color=RING_COLORS[k], fill_opacity=0.85),
                              label(rf"{SHORT[n]} \\ {a:.0f}--{b:.0f} km", font_size=16,
                                    color=RING_COLORS[k])).arrange(RIGHT, buff=0.15, aligned_edge=UP))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.3)
        note = label(r"radius $\propto \sqrt{\text{distance}}$", font_size=13, color=GREY_B).next_to(mp, DOWN,
                                                                                                    buff=0.15)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In 1826 Johann Heinrich von Thünen, who farmed an estate in Mecklenburg, published The Isolated State. "
            "Imagine one market town in the middle of a flat, uniform plain. What will be grown where? "
            "<bookmark mark='a'/> A farmer's rent for a hectare is what the crop sells for, less the cost of "
            "growing it and the cost of carting it to town, which rises with distance. <bookmark mark='b'/> So each "
            "crop has a bid-rent line falling with distance. Bulky or perishable crops, vegetables and milk, fall "
            "steeply; cattle, which walk to market, fall slowly. <bookmark mark='c'/> Land goes to whoever bids "
            "most: the upper edge, in white. <bookmark mark='d'/> On the map, the plain sorts itself into rings. "
            "Von Thünen's surprise was the second ring: forest, because firewood is heavy and every town needed "
            "it. Nobody plans the rings; competition for land draws them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(legend), LaggedStart(*[Create(ln) for ln in lines],
                                                                           lag_ratio=0.3), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(Indicate(lines[0], color=WHITE, scale_factor=1.0), Indicate(lines[3], color=WHITE,
                                                                                    scale_factor=1.0))
            vo.wait_until("c")
            self.play(Create(env), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(mp), FadeIn(note), run_time=1.5)
        self.clear_scene()

    def railway(self):
        T = load("thunen")
        names = T["names"]
        left, right = LEFT * 3.4 + DOWN * 0.5, RIGHT * 3.0 + DOWN * 0.5
        s = 0.18
        before = rings_map(T["rings"], names, left, scale=s)
        after = rings_map(T["rings_rail"], names, right, scale=s)
        hb = label(r"before", font_size=24, color=GREY_A).next_to(before, UP, buff=0.25)
        ha = label(r"a railway halves the freight \\ on grain and cattle", font_size=22, color=ROAD).next_to(
            after, UP, buff=0.25)
        foot = VGroup(*[label(rf"{SHORT[n].replace(chr(92) * 2, '')}: \ to {b:.0f} km", font_size=17,
                              color=RING_COLORS[names.index(n)]) for n, _, b in T["rings_rail"][2:]])
        foot.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now cut the cost of carrying grain and cattle in half, as the railways did in the nineteenth century. "
            "<bookmark mark='a'/> The grain ring stretches from thirty-five kilometres to seventy, and cattle "
            "graze two hundred kilometres out. The town's market reaches twice as far, and land that was worthless "
            "acquires a rent. <bookmark mark='b'/> Swap crops for commuters and the market town for a business "
            "district, and the same logic draws a city."
        ) as vo:
            self.play(FadeIn(before), FadeIn(hb), FadeIn(tag))
            vo.wait_until("a")
            self.play(TransformFromCopy(before, after), FadeIn(ha), run_time=2.0)
            self.play(FadeIn(foot))
            vo.wait_until("b")
            self.play(Indicate(after[-1], color=WHITE, scale_factor=2.0))
        self.clear_scene()
