from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403

STAGES = [("High returns", BOOM), ("Everyone orders", ORDER), ("The wait", GREY_A), ("Capacity arrives", CAP),
          ("Prices fall: losses", BUST), ("Orders stop, old plants close", GREY_B)]


def _pic(k):
    if k == 0:
        return VGroup(*[draw.coin(0.11) for _ in range(6)]).arrange_in_grid(rows=2, cols=3, buff=0.03)
    if k == 1:
        return VGroup(draw.crane(0.9), *[RoundedRectangle(corner_radius=0.03, width=0.32, height=0.42, stroke_width=0,
                                                          fill_color="#E8E4DA", fill_opacity=1).shift(RIGHT * (0.7 + 0.12 * j) + UP * 0.2 * j)
                                         for j in range(3)])
    if k == 2:
        glass = VGroup(Polygon([-0.25, 0.4, 0], [0.25, 0.4, 0], [0, 0, 0], stroke_color=GREY_A, stroke_width=2,
                               fill_opacity=0),
                       Polygon([-0.25, -0.4, 0], [0.25, -0.4, 0], [0, 0, 0], stroke_color=GREY_A, stroke_width=2,
                               fill_color=ORDER, fill_opacity=0.7))
        return VGroup(glass, tx("3 years", 15, GREY_A).next_to(glass, RIGHT, buff=0.1))
    if k == 3:
        return VGroup(*[draw.ship(0.6) for _ in range(4)]).arrange_in_grid(rows=2, cols=2, buff=0.08)
    if k == 4:
        return VGroup(Arrow(UP * 0.4, DOWN * 0.4, color=BUST, buff=0, stroke_width=6),
                      VGroup(*[draw.coin(0.1, color="#8C929B") for _ in range(2)]).arrange(RIGHT, buff=0.03))
    return VGroup(draw.factory(0.9, color="#5B6372"), Cross(stroke_color=BUST, stroke_width=4).scale(0.3))


class Loop(VoiceoverScene):
    def construct(self):
        card(self, 4, "The capital cycle", "Is the hog cycle just about hogs?",
             "Chapter four. The capital cycle.", lit=("change", "moat"))
        r = 2.75
        centre = np.array([-1.7, -0.25, 0])
        angles = [PI / 2 - k * TAU / 6 for k in range(6)]
        nodes = VGroup()
        for k, ((name, col), a) in enumerate(zip(STAGES, angles)):
            pos = centre + r * np.array([np.cos(a), np.sin(a), 0])
            pic = _pic(k)
            pic.scale_to_fit_height(min(pic.height, 0.85)).move_to(pos)
            lab = tx(name, 20, col, bold=True)
            out = np.array([np.cos(a), np.sin(a), 0])
            lab.next_to(pic, out if abs(out[1]) > 0.5 else (RIGHT if out[0] > 0 else LEFT), buff=0.15)
            nodes.add(VGroup(pic, lab))
        arcs = VGroup(*[Arc(radius=r, start_angle=angles[k] - 0.3, angle=-(TAU / 6 - 0.6), arc_center=centre,
                            stroke_color=GREY_C, stroke_width=3).add_tip(tip_length=0.15)
                        for k in range(6)])
        dot = glow_dot(centre + r * np.array([np.cos(angles[0]), np.sin(angles[0]), 0]), color=GOLD, radius=0.1)
        trackr = ValueTracker(0.0)
        dot.add_updater(lambda d: d.move_to(centre + r * np.array([np.cos(PI / 2 - trackr.get_value()),
                                                                  np.sin(PI / 2 - trackr.get_value()), 0])))
        where = VGroup(tx("ships", 20, CAP), tx("memory chips", 20, "#B58CFF"), tx("mines", 20, "#C9A26B"),
                       tx("houses", 20, HOG), tx("office towers", 20, STONE), tx("oil wells", 20, PRICE))
        where.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.9, -0.2, 0])
        where_t = tx("the same loop in", 18, GREY_B).next_to(where, UP, buff=0.25).align_to(where, LEFT)
        with self.voiceover(
            "The hog cycle is the simplest case of something that runs through every industry that builds things "
            "which take time to build. Investors call it the capital cycle. <bookmark mark='a'/> It starts with high "
            "returns: too little capacity, high prices, fat profits. <bookmark mark='b'/> Everyone can see them, so "
            "everyone orders: ships, fabs, mines, houses. <bookmark mark='c'/> Then comes the wait, while the new "
            "capacity is built, and the prices stay high, and more orders come in. <bookmark mark='d'/> Then the "
            "capacity arrives, all at once. <bookmark mark='e'/> Prices fall, often below the cost of running the "
            "new plant, and the industry loses money. <bookmark mark='f'/> Orders stop. The oldest, costliest "
            "plants close, ships are sent to be broken up, and companies merge or fail. With no new capacity coming "
            "and demand still growing, there is too little again, <bookmark mark='g'/> and the loop starts over. "
            "<bookmark mark='h'/> The same loop turns in ships, memory chips, mines, houses, office towers and oil "
            "wells. The next chapters measure it in four of them."
        ) as vo:
            ghost = VGroup(nodes.copy(), arcs.copy()).set_opacity(0.15)
            self.play(FadeIn(ghost), run_time=1.2)
            self.add(dot)
            self.play(FadeIn(nodes[0]), FadeIn(dot))
            self.play(trackr.animate.set_value(TAU), run_time=4.0, rate_func=linear)
            trackr.set_value(0)
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                if k > 0:
                    self.play(Create(arcs[k - 1]), trackr.animate.set_value(k * TAU / 6), FadeIn(nodes[k], scale=0.8),
                              run_time=1.2)
                else:
                    self.play(Indicate(nodes[0], color=BOOM))
            vo.wait_until("g")
            self.play(Create(arcs[5]), trackr.animate.set_value(TAU), run_time=1.2)
            self.remove(ghost)
            self.play(trackr.animate.set_value(2 * TAU), run_time=3.0, rate_func=linear)
            vo.wait_until("h")
            self.play(FadeIn(where_t), LaggedStart(*[FadeIn(w_, shift=LEFT * 0.2) for w_ in where], lag_ratio=0.25),
                      trackr.animate.set_value(3 * TAU), run_time=3.0)
        dot.clear_updaters()
        self.clear_scene()
