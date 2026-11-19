from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403
from videos.economics.econ9.s03_box import ana_curve, bo_curve, u_cd


class SecondTheorem(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The second welfare theorem", r"Can any efficient outcome be reached by a market, and at what "
             r"cost?", "Chapter six. The second welfare theorem.")
        self.target()
        self.hyperplane()
        self.rare()

    def target(self):
        b = load("box")
        w = load("welfare")
        X = np.array(b["X"])
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        om = Dot(box.c2p(*b["eA"]), radius=0.09, color=WHITE)
        oml = label(r"$\omega$", font_size=22).next_to(om, DR, buff=0.05)
        cc = box.curve(b["cc_x"], b["cc_y"], color=CC, width=3)
        E_ = Dot(box.c2p(*b["xA"]), radius=0.08, color=GREY_B)
        T = Dot(box.c2p(*w["target"]), radius=0.1, color=E.ACCENT)
        Tl = label(r"$T$", font_size=24, color=E.ACCENT).next_to(T, UL, buff=0.05)
        line = price_line(box, w["target"], w["price"])
        new_om = np.array([b["eA"][0], b["eA"][1] + w["transfer"]])
        om2 = Dot(box.c2p(*new_om), radius=0.09, color=E.ACCENT)
        arrow = Arrow(box.c2p(*b["eA"]), box.c2p(*new_om), buff=0.05, color=E.ACCENT, stroke_width=4,
                      max_tip_length_to_length_ratio=0.2)
        side = VGroup(
            label(rf"a target: \ the efficient point $T$, \\ {w['target'][0]:.0f} fish and {w['target'][1]:.2f} "
                  r"baskets for Ana", font_size=22, color=E.ACCENT),
            label(rf"the price that supports it: \\ the common slope there, \ {w['price']:.3f} baskets a fish",
                  font_size=22),
            label(rf"move {w['transfer']:.2f} baskets from Bo to Ana, \\ once, \ before trade", font_size=22,
                  color=E.ACCENT),
            label(r"then let them trade at that price: \\ each chooses exactly $T$", font_size=22, color=CC),
            label(r"any efficient point, \ by a transfer and a market", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The first theorem goes from markets to efficiency. The second goes back. <bookmark mark='a'/> Suppose "
            "the islanders decide that the market's outcome is too hard on Ana, and pick a different efficient "
            "point, T, where she ends up with five fish and nearly seven baskets. <bookmark mark='b'/> At T the two "
            "indifference curves touch, and their common slope is a price: nought point nine two three baskets a "
            "fish. <bookmark mark='c'/> Now move two point six five baskets from Bo to Ana, once, before any "
            "trade. That puts the starting point on the price line through T. <bookmark mark='d'/> Open the market "
            "at that price, and each of them chooses to trade exactly to T. <bookmark mark='e'/> That's the second "
            "welfare theorem: with convex preferences, any efficient allocation can be reached by a market, after "
            "the right transfer of wealth."
        ) as vo:
            self.play(FadeIn(box), FadeIn(om), FadeIn(oml), FadeIn(cc), FadeIn(E_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(T, scale=0.5), FadeIn(Tl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrow), FadeIn(om2), FadeIn(side[2]))
            vo.wait_until("d")
            mover = om2.copy()
            self.play(mover.animate.move_to(T.get_center()), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        del X
        self.clear_scene()

    def hyperplane(self):
        b = load("box")
        w = load("welfare")
        X = np.array(b["X"])
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        t = np.array(w["target"])
        ua, ub = u_cd(b["aA"], t), u_cd(b["aB"], X - t)
        xs = np.linspace(0.3, X[0], 200)
        ya = np.minimum(ge.cd_indifference(b["aA"], ua, xs), X[1])
        upper = Polygon(*[box.c2p(x, y) for x, y in zip(xs, ya)], box.c2p(X[0], X[1]), box.c2p(xs[0], X[1]),
                        stroke_width=0, fill_color=ANA, fill_opacity=0.25)
        xs2 = np.linspace(0.0, X[0] - 0.3, 200)
        yb = np.maximum(X[1] - ge.cd_indifference(b["aB"], ub, X[0] - xs2), 0)
        lower = Polygon(*[box.c2p(x, y) for x, y in zip(xs2, yb)], box.c2p(xs2[-1], 0), box.c2p(0, 0),
                        stroke_width=0, fill_color=BO, fill_opacity=0.25)
        ia, ib = ana_curve(box, b, ua, width=3), bo_curve(box, b, ub, width=3)
        line = price_line(box, t, w["price"], color=WHITE, width=3.5)
        T = Dot(box.c2p(*t), radius=0.1, color=E.ACCENT)
        side = VGroup(
            label(r"what Ana prefers to $T$: \ a convex set", font_size=22, color=ANA),
            label(r"what Bo prefers to $T$: \ another", font_size=22, color=BO),
            label(r"they touch only at $T$, \ so a straight line \\ separates them: \ a \emph{separating "
                  r"hyperplane}", font_size=22),
            label(r"its slope is the price; \ with many goods, \\ the same theorem of geometry, \ in many "
                  r"dimensions", font_size=21, color=GREY_A),
            label(r"needs convexity: \ curves that bow the right way", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Why must such a price exist? <bookmark mark='a'/> Shade everything Ana likes better than T. Because "
            "her curves bow toward her corner, it's a convex set: no dents. <bookmark mark='b'/> Shade everything "
            "Bo likes better than T. That's convex too. <bookmark mark='c'/> T is efficient, so the two sets don't "
            "overlap: they touch only at T. And two convex sets that don't overlap can always be separated by a "
            "straight line. <bookmark mark='d'/> The slope of that line is the supporting price. With many goods "
            "the line becomes a plane in many dimensions, a separating hyperplane, and the theorem of geometry "
            "that guarantees it is the heart of the proof. <bookmark mark='e'/> Which is also its limit: without "
            "convex preferences, the sets can't always be separated, and some efficient points can't be reached "
            "by any prices."
        ) as vo:
            self.play(FadeIn(box), FadeIn(T))
            vo.wait_until("a")
            self.play(FadeIn(upper), Create(ia), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(lower), Create(ib), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def rare(self):
        head = label(r"so why not redistribute this way?", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the transfer must be \emph{lump-sum}: \ nothing anyone does can change it", font_size=26),
            label(r"real taxes fall on income, \ spending, \ wealth: \ things people choose", font_size=26),
            label(r"so they change what people do, \ and the change wastes something", font_size=26, color=HOLD),
            label(r"to tax ability itself, \ you would have to observe it", font_size=26, color=HOLD),
            label(r"the theorem separates efficiency from fairness in principle; \\ in practice they trade off: "
                  r"\ Part 41", font_size=25, color=GREY_A),
        ).arrange(DOWN, buff=0.38).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "So the second theorem seems to say that fairness and efficiency can be had separately: redistribute "
            "once, then let the market work. <bookmark mark='a'/> The catch is in the word transfer. It has to be "
            "lump-sum: a sum that nothing anyone does can change. <bookmark mark='b'/> Real taxes fall on income, "
            "spending and wealth, which people choose. <bookmark mark='c'/> So they change what people do, and "
            "the change wastes something. <bookmark mark='d'/> To tax the thing that really differs between "
            "people, their ability to earn, a government would have to see it, and it can't. <bookmark mark='e'/> "
            "So in principle the theorem separates efficiency from fairness; in practice they trade off, and how "
            "steeply is the subject of Part forty-one."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
