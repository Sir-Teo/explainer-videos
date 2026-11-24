from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403

X0, X1 = -6.6, 6.6


def arch(x, amp=0.9, w=2.4):
    """The shape of the fold: a dome centred at x = 0."""
    return amp * np.exp(-(x / w) ** 2)


def layer(y_bot, y_top, color, amp_bot=0.9, amp_top=0.9, n=80, opacity=1.0):
    xs = np.linspace(X0, X1, n)
    top = [[x, y_top + arch(x, amp_top), 0] for x in xs]
    bot = [[x, y_bot + arch(x, amp_bot), 0] for x in xs[::-1]]
    return Polygon(*top, *bot, stroke_width=0, fill_color=color, fill_opacity=opacity)


class Rock(VoiceoverScene):
    def construct(self):
        card(self, 2, "Under the ground", "Where is oil, and why is some of it so much harder to reach?",
             "Chapter two. Under the ground.", lit=("unit", "make"))
        self.formation()
        self.kinds()

    def formation(self):
        source_ = layer(-3.2, -2.4, "#2A2520")
        reservoir = layer(-2.4, -1.2, "#B79A6A")
        cap = layer(-1.2, -0.6, "#5A6170")
        over = layer(-0.6, 1.0, "#4B4030", amp_top=0.0)
        sky = Rectangle(width=13.4, height=2.6, stroke_width=0, fill_color="#0E1117", fill_opacity=1).move_to([0, 2.4, 0])
        ground = Line([X0, 1.0, 0], [X1, 1.0, 0], stroke_color="#7A6A50", stroke_width=3)
        # grains in the reservoir: little circles, the pore space between them
        rng = np.random.default_rng(3)
        grains = VGroup(*[Circle(radius=0.05, stroke_width=0, fill_color="#D7BE8E", fill_opacity=0.8).move_to(
            [x, y + arch(x), 0]) for x, y in zip(rng.uniform(X0 + 0.2, X1 - 0.2, 160), rng.uniform(-2.3, -1.3, 160))])
        plankton = VGroup(*[Dot([x, y + arch(x), 0], radius=0.03, color="#7BD88F") for x, y in
                            zip(rng.uniform(X0 + 0.2, X1 - 0.2, 70), rng.uniform(-3.1, -2.5, 70))])
        labels = VGroup(tx("source rock: shale, rich in old plankton", 19, WHITE).move_to([4.2, -2.85, 0]),
                        tx("reservoir: sandstone, full of tiny pores", 19, WHITE).move_to([4.2, -1.85, 0]),
                        tx("cap rock: tight, nothing passes", 19, WHITE).move_to([4.2, -0.9, 0]))
        for l_ in labels:
            l_.add_to_back(BackgroundRectangle(l_, fill_color="#0E1117", fill_opacity=0.7, buff=0.08))
        # oil droplets: start in the source rock, rise to the top of the reservoir under the dome
        n = 46
        starts = [[x, y + arch(x), 0] for x, y in zip(rng.uniform(-5.5, 5.5, n), rng.uniform(-3.0, -2.6, n))]
        ends = []
        for k in range(n):
            x = rng.normal(0, 0.9)
            y = -1.25 + arch(x) - abs(rng.normal(0, 0.18))
            ends.append([x, y, 0])
        drops = VGroup(*[Dot(p, radius=0.075, color="#F2A65A") for p in starts])
        trap = tx("trap: the oil collects under the dome", 20, CRUDE, bold=True).move_to([3.6, 1.6, 0])
        arrow = Arrow([3.6, 1.35, 0], [1.0, -0.6, 0], buff=0.1, stroke_width=3, color=CRUDE,
                      max_tip_length_to_length_ratio=0.1)
        tag = estimate_tag("illustrative cross-section, not to scale", corner=DR, size=14)
        with self.voiceover(
            "Oil begins as life. <bookmark mark='a'/> For millions of years, the remains of tiny sea plants and animals "
            "settled on the floors of ancient seas, and were buried in mud. The mud became a dark rock, shale, and "
            "the buried remains were slowly cooked, a few kilometres down, into oil and gas. Geologists call it the "
            "source rock. <bookmark mark='b'/> Oil is lighter than water, so it creeps upward, through any rock with "
            "spaces in it, like this sandstone, whose grains leave tiny pores between them. <bookmark mark='c'/> Much "
            "of it seeps all the way to the surface and is lost. But where a layer of tight rock lies on top, and the "
            "layers are folded into a dome, the oil is caught. <bookmark mark='d'/> That is a trap, and for a century "
            "and a half, finding oil meant finding traps: a source, a reservoir, and a lid."
        ) as vo:
            self.play(FadeIn(sky), FadeIn(over), FadeIn(cap), FadeIn(reservoir), FadeIn(source_), Create(ground),
                      FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=2) for d_ in plankton], lag_ratio=0.02), FadeIn(labels[0]),
                      run_time=2.0)
            self.play(plankton.animate.set_color(CRUDE).set_opacity(0.5), run_time=1.2)
            self.add(drops)
            self.remove(plankton)
            vo.wait_until("b")
            self.play(FadeIn(grains), FadeIn(labels[1]))
            self.play(*[d_.animate.move_to([s[0], -2.0 + arch(s[0]), 0]) for d_, s in zip(drops, starts)], run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(labels[2]))
            self.play(*[d_.animate.move_to(e) for d_, e in zip(drops, ends)], run_time=3.0, rate_func=smooth)
            vo.wait_until("d")
            self.play(FadeIn(trap), GrowArrow(arrow))
        self.clear_scene()

    def kinds(self):
        def panel(title, sub, pic, col):
            box = RoundedRectangle(corner_radius=0.12, width=3.1, height=4.6, stroke_color=col, stroke_width=2,
                                   fill_color="#141A24", fill_opacity=1)
            body = VGroup(tx(title, 21, col, bold=True), pic, *[tx(s, 15, GREY_A) for s in sub]).arrange(DOWN, buff=0.16)
            body.move_to(box)
            return VGroup(box, body)

        def conv_pic():
            g = VGroup(Rectangle(width=2.4, height=1.4, stroke_width=0, fill_color="#4B4030", fill_opacity=1),
                       Arc(radius=1.0, start_angle=0.25, angle=PI - 0.5, stroke_color="#5A6170", stroke_width=6).shift(
                           DOWN * 0.95),
                       Ellipse(width=1.0, height=0.25, stroke_width=0, fill_color=CRUDE, fill_opacity=1).shift(DOWN * 0.05),
                       Line([0, 0.7, 0], [0, -0.05, 0], stroke_color=GREY_A, stroke_width=3))
            return VGroup(draw.pumpjack(1.0).next_to(g, UP, buff=0), g)

        def shale_pic():
            g = VGroup(Rectangle(width=2.4, height=1.4, stroke_width=0, fill_color="#4B4030", fill_opacity=1),
                       Rectangle(width=2.4, height=0.35, stroke_width=0, fill_color="#2A2520", fill_opacity=1).shift(
                           DOWN * 0.45),
                       VMobject(stroke_color=GREY_A, stroke_width=3).set_points_as_corners(
                           [[-0.8, 0.7, 0], [-0.8, -0.3, 0], [-0.6, -0.45, 0], [1.1, -0.45, 0]]),
                       *[Line([x, -0.25, 0], [x, -0.65, 0], stroke_color=CRUDE, stroke_width=2) for x in
                         np.linspace(-0.4, 1.0, 6)])
            return VGroup(draw.derrick(0.7).shift(LEFT * 0.8).next_to(g, UP, buff=0).shift(LEFT * 0.8), g)

        def deep_pic():
            return draw.platform(2.2)

        def sands_pic():
            g = VGroup(Rectangle(width=2.4, height=1.0, stroke_width=0, fill_color="#3A2F22", fill_opacity=1),
                       Polygon([-0.9, 0.5, 0], [0.9, 0.5, 0], [0.5, 0.0, 0], [-0.5, 0.0, 0], stroke_width=0,
                               fill_color="#1E1A16", fill_opacity=1))
            return VGroup(draw.truck(0.9, color="#F2C14E").next_to(g, UP, buff=0).shift(RIGHT * 0.5), g)

        panels = VGroup(
            panel("Conventional", ["drill into a trap;", "the oil flows to the well", "Saudi Arabia's great fields"],
                  conv_pic(), GAS),
            panel("Shale", ["drill sideways inside", "the source rock and crack it", "Texas, North Dakota"], shale_pic(),
                  SHALE),
            panel("Deep water", ["traps under the sea floor,", "from platforms or ships", "the Gulf of Mexico, Brazil"],
                  deep_pic(), BRENT),
            panel("Oil sands", ["tar near the surface,", "dug up or steamed out", "Alberta, Canada"], sands_pic(), CRUDE))
        for p in panels:
            pic = p[1][1]
            pic.scale_to_fit_height(min(pic.height, 1.8))
            if pic.width > 2.7:
                pic.scale_to_fit_width(2.7)
            p[1].arrange(DOWN, buff=0.16).move_to(p[0])
        panels.arrange(RIGHT, buff=0.25).move_to([0, -0.2, 0])
        head = tx("Four ways oil is produced", 26, WHITE, bold=True).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Today oil comes out of the ground in four main ways. <bookmark mark='a'/> Conventional fields: drill into "
            "a trap, and the pressure pushes the oil up the well. The great fields of Saudi Arabia are like this, and "
            "so was most of the world's oil for a century. <bookmark mark='b'/> Shale: drill down into the source rock "
            "itself, turn and drill sideways for a mile or more, then crack the rock open with water and sand pumped in "
            "at high pressure. The oil that never escaped can now flow. <bookmark mark='c'/> Deep water: traps "
            "beneath the sea floor, under hundreds or thousands of metres of water, reached from platforms and ships that cost "
            "billions. <bookmark mark='d'/> And oil sands: tar, too thick to flow, near the surface in Alberta, dug up "
            "with trucks or melted out with steam. Each way costs something different per barrel, and fades at a "
            "different speed, which is what the next three chapters are about."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(panels[k], shift=UP * 0.2), run_time=1.0)
                if k == 0:
                    self.add(draw.nod(panels[0][1][1][0]))
        panels[0][1][1][0].clear_updaters()
        self.clear_scene()
