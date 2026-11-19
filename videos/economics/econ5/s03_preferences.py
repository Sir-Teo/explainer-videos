from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403

GOOD_COLOR = {"fish": FISHC, "coconut": COCO, "cloth": "#C9A0FF"}


class Preferences(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Preferences as a ranking", r"What has to be true of someone's tastes for choice to make sense?",
             "Chapter two. Preferences as a ranking.")
        self.axioms()
        self.regions()
        self.pump()

    def axioms(self):
        bundles = VGroup()
        for name, f, c in ((r"A", 4, 2), (r"B", 2, 5), (r"C", 3, 3)):
            box = RoundedRectangle(width=2.3, height=1.3, corner_radius=0.12, stroke_color=GREY_B, stroke_width=2,
                                   fill_color=GREY_E, fill_opacity=0.3)
            t = VGroup(label(name, font_size=30, color=E.ACCENT),
                       label(rf"{f} fish, \ {c} coconuts", font_size=20)).arrange(DOWN, buff=0.1).move_to(box)
            bundles.add(VGroup(box, t))
        bundles.arrange(RIGHT, buff=1.4).to_edge(UP, buff=0.9)
        rules = VGroup(
            label(r"\textbf{complete}: \ for any two bundles, \ A $\succsim$ B, \ or B $\succsim$ A, \ or both",
                  font_size=26),
            label(r"\textbf{transitive}: \ A $\succsim$ B \ and \ B $\succsim$ C \ $\Rightarrow$ \ A $\succsim$ C",
                  font_size=26),
            label(r"\textbf{continuous}: \ a bundle slightly changed is ranked only slightly differently",
                  font_size=26),
            label(r"nothing about \emph{why}: \ taste, habit, kindness, religion, all allowed", font_size=26,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(bundles, DOWN, buff=0.75)
        a1 = CurvedArrow(bundles[0].get_bottom() + DOWN * 0.05, bundles[1].get_bottom() + DOWN * 0.05, angle=PI / 3,
                         color=GREY_B, stroke_width=2.5)
        with self.voiceover(
            "Start with what a taste is, as economics uses the word. It's a ranking. <bookmark mark='a'/> Give "
            "someone any two bundles, say four fish and two coconuts against two fish and five coconuts, and they "
            "can say which they'd rather have, or that they don't mind. That's completeness. "
            "<bookmark mark='b'/> If they'd rather have A than B, and B than C, they'd rather have A than C. That's "
            "transitivity. <bookmark mark='c'/> And a tiny change in a bundle makes only a tiny change in where it "
            "ranks. That's continuity. <bookmark mark='d'/> Notice what's missing. Nothing says why. The ranking can "
            "come from hunger, habit, generosity or faith. Economics takes it as given, and asks only that it hang "
            "together."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in bundles], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Create(a1), FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]))
            vo.wait_until("d")
            self.play(FadeIn(rules[3]))
        self.clear_scene()

    def regions(self):
        ax = goods_axes(center=LEFT * 2.8 + DOWN * 0.2, top=10, ticks=(0, 2, 4, 6, 8, 10))
        a = ax.ax
        x0, y0 = 4.0, 4.0
        pt = Dot(a.c2p(x0, y0), radius=0.1, color=WHITE)
        pl = label(r"A", font_size=26, color=WHITE).next_to(pt, DL, buff=0.08)
        better = Polygon(a.c2p(x0, y0), a.c2p(10, y0), a.c2p(10, 10), a.c2p(x0, 10), stroke_width=0,
                         fill_color=PASS, fill_opacity=0.25)
        worse = Polygon(a.c2p(0, 0), a.c2p(x0, 0), a.c2p(x0, y0), a.c2p(0, y0), stroke_width=0, fill_color=VIOL,
                        fill_opacity=0.25)

        cd = cs.Preference("cobb-douglas", a=0.5)
        xs = np.linspace(1.6, 10, 200)
        ic = curve(ax, xs, cd.indifference(float(cd.u(x0, y0)), xs), color=IC, top=10)
        rows = VGroup(
            label(r"more of both is better: \ the green corner", font_size=24, color=PASS),
            label(r"less of both is worse: \ the red corner", font_size=24, color=VIOL),
            label(r"in between, \ more fish for fewer coconuts: \\ the person must say", font_size=24),
            label(r"the bundles exactly as good as A: \\ an indifference curve", font_size=24, color=IC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Put the ranking in the plane of fish and coconuts. <bookmark mark='a'/> Take bundle A, four of each. "
            "If more is better, everything up and to the right of it is better. <bookmark mark='b'/> Everything down "
            "and to the left is worse. <bookmark mark='c'/> The other two corners trade fish for coconuts, and only "
            "the person can say how they rank. <bookmark mark='d'/> Somewhere through those corners runs the line "
            "of bundles exactly as good as A: an indifference curve. A complete, transitive, continuous ranking "
            "fills the plane with them, and they never cross."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(pt, scale=1.5), FadeIn(pl), FadeIn(better), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(worse), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(ic), FadeIn(rows[3]))
        self.clear_scene()

    def pump(self):
        pu = load("pump")
        goods = ["fish", "cloth", "coconut"]
        r = 1.8
        centre = LEFT * 3.0 + DOWN * 0.2
        pos = {g: centre + r * np.array([np.cos(PI / 2 + 2 * PI * k / 3), np.sin(PI / 2 + 2 * PI * k / 3), 0])
               for k, g in enumerate(goods)}
        nodes = VGroup()
        for g in goods:
            c = Circle(radius=0.6, stroke_color=GOOD_COLOR[g], stroke_width=3, fill_color=GOOD_COLOR[g],
                       fill_opacity=0.15).move_to(pos[g])
            nodes.add(VGroup(c, label(g, font_size=22, color=GOOD_COLOR[g]).move_to(c)))
        arrows = VGroup()
        for g in goods:
            h = pu["better"][g]
            arrows.add(Arrow(pos[g], pos[h], buff=0.68, color=GREY_B, stroke_width=3,
                             max_tip_length_to_length_ratio=0.12))
        prefers = label(r"the arrow points to what he would rather have", font_size=20, color=GREY_A).next_to(
            VGroup(*nodes), DOWN, buff=0.35)
        token = Dot(pos["fish"], radius=0.16, color=E.ACCENT)
        coins = Integer(pu["start_coins"], font_size=48, color=E.ACCENT)
        clab = label(r"coins left", font_size=22, color=GREY_A)
        meter = VGroup(coins, clab).arrange(DOWN, buff=0.1).move_to(RIGHT * 3.6 + UP * 1.4)
        rows = VGroup(
            label(r"each swap up the circle: \ one coin", font_size=24),
            label(r"after a lap: \ the same fish, \ three coins poorer", font_size=24, color=VIOL),
            label(r"the money pump: \ Davidson, McKinsey and Suppes, 1955", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(meter, DOWN, buff=0.6)
        with self.voiceover(
            "Why insist on transitivity? Because without it, you can be robbed politely. "
            "<bookmark mark='a'/> Here's a trader whose tastes go round in a circle: he'd rather have cloth than "
            "fish, coconuts than cloth, and fish than coconuts. <bookmark mark='b'/> He holds a fish. Offer him the "
            "cloth for his fish and one coin, and he takes it. Offer the coconut for the cloth and a coin. Then the "
            "fish for the coconut and a coin. <bookmark mark='c'/> He's back where he started, holding the same "
            "fish, three coins poorer, and happy to go round again. Philosophers call this the money pump; Donald "
            "Davidson, John McKinsey and Patrick Suppes set it out in 1955. Real people do sometimes have cycles. "
            "Markets, which keep offering the next trade, are hard on them."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(n_) for n_ in nodes], lag_ratio=0.2), FadeIn(meter))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(x) for x in arrows], lag_ratio=0.3), FadeIn(prefers))
            vo.wait_until("b")
            self.play(FadeIn(token, scale=1.5), FadeIn(rows[0]))
            for st in pu["steps"][:3]:
                self.play(token.animate.move_to(pos[st["to"]]), coins.animate.set_value(st["coins"]), run_time=0.9)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            for st in pu["steps"][3:]:
                self.play(token.animate.move_to(pos[st["to"]]), coins.animate.set_value(st["coins"]), run_time=0.35)
            self.play(FadeIn(rows[2]))
        self.clear_scene()
