from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Leibniz(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Sufficient reason", r"Must everything have a reason why it is so and not otherwise?",
                            lit=(1714,), part=PART)
        with self.voiceover("Chapter four. Sufficient reason."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.psr()
        self.analysis()
        self.optics()
        self.monads()
        self.clarke()

    def psr(self):
        hc = history_card(1714, r"Gottfried Wilhelm Leibniz", r"\textit{Monadology}", width=5.0, color=HIST).to_corner(
            UL, buff=0.35)
        two = VGroup(
            VGroup(label(r"the principle of contradiction", font_size=28, color=REASON),
                   label(r"what implies a contradiction is false", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(label(r"the principle of sufficient reason", font_size=28, color=GOAL),
                   label(r"nothing is so without a reason why it is so and not otherwise", font_size=22,
                         color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(DOWN, buff=0.6).move_to([0, 0.4, 0])
        tail = label(r"Monadology \S\S 31--32: \ our reasoning rests on these two great principles", font_size=22,
                     color=GREY_B).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Gottfried Wilhelm Leibniz, mathematician, diplomat and the inventor of the calculation dream of Part 1, "
            "rested all reasoning on two principles. <bookmark mark='a'/>The principle of contradiction: whatever "
            "implies a contradiction is false. <bookmark mark='b'/>And the principle of sufficient reason: nothing is "
            "so without a reason why it is so and not otherwise. <bookmark mark='c'/>The second is the bolder. It "
            "says the world contains no brute facts. Every truth, even the truth that this world exists rather than "
            "another, has a reason."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(two[0]))
            vo.wait_until("b")
            self.play(FadeIn(two[1]))
            vo.wait_until("c")
            self.play(FadeIn(tail))
        self.clear_scene()

    def analysis(self):
        d = load("analysis")
        head = label(r"Truths of reason, \ truths of fact", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        left = VGroup(label(r"a truth of reason", font_size=26, color=REASON),
                      label(r"analysis ends in an identity, \ in finitely many steps", font_size=21, color=GREY_A),
                      label(r"like a ratio of whole numbers:", font_size=21, color=GREY_A),
                      MathTex(r"\tfrac{355}{113} = 3 + \cfrac{1}{7 + \cfrac{1}{16}}", font_size=34, color=REASON),
                      label(r"Euclid's algorithm stops", font_size=21, color=OK)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"a truth of fact", font_size=26, color=SENSE),
                       label(r"analysis goes on forever; \ only God sees it to the end", font_size=21, color=GREY_A),
                       label(r"like an incommensurable ratio:", font_size=21, color=GREY_A),
                       MathTex(r"\sqrt{2} = 1 + \cfrac{1}{2 + \cfrac{1}{2 + \cfrac{1}{2 + \cdots}}}", font_size=34,
                               color=SENSE),
                       label(r"the Reasoner: \ $1;\ 2, 2, 2, \dots$ \ never stops", font_size=21, color=BAD)).arrange(
            DOWN, buff=0.2)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to([0, 0.2, 0])
        conv = label(r"convergents: \ " + r", \ ".join(rf"${c}$".replace("/", r"/") for c in d["convergents"][1:7])
                     + r", \ \dots \ \ closer and closer, \ never equal", font_size=21, color=GREY_B).to_edge(
            DOWN, buff=0.45)
        assert d["pi_approx"] == [3, 7, 16] and set(d["sqrt2"][1:]) == {2}
        with self.voiceover(
            "From the two principles come two kinds of truth. <bookmark mark='a'/>A truth of reason, Leibniz said, "
            "can be analysed into identities in finitely many steps: its denial is a contradiction. He compared it "
            "to a ratio of whole numbers. The Reasoner analyses three hundred and fifty-five over a hundred and "
            "thirteen by Euclid's algorithm: three, then seven, then sixteen, and it stops. <bookmark mark='b'/>A "
            "truth of fact, such as that Caesar crossed the Rubicon, has a reason too, but its analysis never ends; "
            "only God sees it through. Leibniz compared it to an incommensurable ratio, like the square root of two. "
            "The same algorithm gives one, then two, then two, then two, forever. <bookmark mark='c'/>The fractions it "
            "produces come closer and closer to the root of two, and never reach it. So contingent truths are not "
            "arbitrary; they are infinitely complex."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(conv))
        self.clear_scene()

    def optics(self):
        d = load("leasttime")
        head = label(r"Nature takes the easiest path", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        u = 1.7
        o = np.array([-4.6, 0.1, 0])

        def p(x, y):
            return o + u * np.array([x, y, 0])
        water = Rectangle(width=u * 2.8, height=u * 1.25, stroke_width=0, fill_color="#1E3A5F",
                          fill_opacity=0.5).move_to(p(1.0, -0.62))
        surf = Line(p(-0.4, 0), p(2.4, 0), color=GREY_B, stroke_width=2)
        A, B = Dot(p(0, 1), color=GOAL), Dot(p(2, -1), color=GOAL)
        la, lb = MathTex("A", font_size=28).next_to(A, LEFT), MathTex("B", font_size=28).next_to(B, RIGHT)
        x = ValueTracker(1.0)

        def path():
            xx = x.get_value()
            return VMobject(color=OK, stroke_width=3).set_points_as_corners([p(0, 1), p(xx, 0), p(2, -1)])
        ray = always_redraw(path)
        vals = d["samples"]
        ax = Axes(x_range=[0, 2, 0.5], y_range=[3.2, 4.0, 0.2], x_length=4.2, y_length=2.6, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2}).move_to([3.6, 0.4, 0])
        curve = ax.plot_line_graph([v[0] for v in vals], [v[1] for v in vals], line_color=SENSE,
                                   add_vertex_dots=False, stroke_width=3)
        best = Dot(ax.c2p(d["x"], d["time"]), color=OK)
        cap = VGroup(label(r"travel time against the crossing point", font_size=20, color=GREY_A).next_to(ax, UP,
                                                                                                       buff=0.15),
                     label(r"slower in water: \ the fastest path bends", font_size=22, color=SENSE).next_to(ax, DOWN,
                                                                                                       buff=0.2))
        snell = VGroup(MathTex(r"\frac{\sin i}{v_1} = " + f"{d['sin_i_over_v1']:.4f}" + r"\;=\;\frac{\sin r}{v_2}",
                               font_size=30, color=OK),
                       label(r"the least-time point obeys Snell's law: \ Fermat (1662), \ Leibniz (1682)", font_size=21,
                             color=GREY_A)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Leibniz thought the principle of sufficient reason showed up in physics. <bookmark mark='a'/>Light "
            "travels from A, in air, to B, under water, where it is slower. Which path does it take? "
            "<bookmark mark='b'/>The Reasoner tries every crossing point on the surface and times each path. The "
            "straight line is not fastest: it spends too long in the slow water. <bookmark mark='c'/>The fastest "
            "path bends at the surface, and at that point the ratio of sines equals the ratio of speeds, which is "
            "Snell's law of refraction. Fermat derived it from least time in 1662, and Leibniz in 1682 saw in it "
            "a reason in nature: of all the paths, the one actually taken is the best. <bookmark mark='d'/>Applied to "
            "everything, the same thought gives his most famous claim: God, choosing among all possible worlds, chose "
            "the best, the one richest in phenomena and simplest in laws. Part 23 returns to it, and to Voltaire's "
            "mockery of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(water), Create(surf), FadeIn(A), FadeIn(B), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(Create(ray))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(cap[0]))
            self.play(Create(curve), x.animate.set_value(1.7), run_time=2)
            self.play(x.animate.set_value(0.2), run_time=2)
            vo.wait_until("c")
            self.play(x.animate.set_value(d["x"]), FadeIn(best), FadeIn(cap[1]), run_time=2)
            self.play(FadeIn(snell))
            vo.wait_until("d")
            self.play(Indicate(ray, color=GOAL))
        self.clear_scene()

    def monads(self):
        head = label(r"The monads", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the world is made of simple, \ unextended substances: \ monads", font_size=26, color=REASON),
            label(r"each mirrors the whole universe \ from its own point of view", font_size=24),
            label(r"monads have no windows: \ nothing passes between them", font_size=24, color=GOAL),
            label(r"their agreement is pre-established, \ like clocks set together by the same clockmaker",
                  font_size=24, color=GREY_A),
            label(r"and every truth about a monad \ is contained in its complete concept", font_size=24,
                  color=SENSE)).arrange(DOWN, buff=0.35).move_to([0, -0.3, 0])
        with self.voiceover(
            "Sufficient reason also shaped Leibniz's metaphysics. <bookmark mark='a'/>In the Monadology of 1714 the "
            "world consists of simple substances without extension, which he called monads. <bookmark mark='b'/>"
            "Each mirrors the whole universe from its own point of view. <bookmark mark='c'/>But the monads have no "
            "windows: nothing passes from one to another. <bookmark mark='d'/>They agree because God set them in "
            "harmony at the start, like clocks set together by the same clockmaker. <bookmark mark='e'/>And every "
            "truth about a monad, everything it will ever do, is already contained in its complete concept: the "
            "infinite analysis of a truth of fact."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def clarke(self):
        hc = history_card(1715, r"Leibniz and Samuel Clarke", r"the correspondence, \ with Clarke speaking for Newton",
                          width=6.0, color=HIST).to_corner(UL, buff=0.35)
        world = VGroup(*[Dot([x, y, 0], radius=0.08, color=c) for x, y, c in
                         ((-1.0, 0.3, SENSE), (-0.3, -0.4, REASON), (0.5, 0.5, OK), (0.9, -0.2, GOAL))])
        w1 = world.copy().move_to([-5.2, 0.4, 0])
        w2 = world.copy().move_to([-2.4, 0.4, 0])
        arr = Arrow(w1.get_right(), w2.get_left(), buff=0.3, color=GREY_B)
        tag = label(r"the whole universe, \ ten feet to the east", font_size=20, color=GREY_A).next_to(arr, DOWN,
                                                                                                   buff=0.6)
        rows = VGroup(
            label(r"Newton: \ space is absolute, \ so the shift is a real difference", font_size=22, color=SENSE),
            label(r"Leibniz: \ then God had no reason to put the world here rather than there", font_size=22,
                  color=GOAL),
            label(r"so the two are one: \ the identity of indiscernibles", font_size=22, color=REASON),
            label(r"space is only the order of coexisting things \ (Newton's bucket, \ Part 25)", font_size=22,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -0.6, 0])
        for r in rows:
            if r.width > 6.0:
                r.width = 6.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0.6, -0.6, 0], aligned_edge=LEFT)
        with self.voiceover(
            "In his last years Leibniz turned the principle against Newton. <bookmark mark='a'/>In letters of 1715 "
            "and 1716 with Samuel Clarke, who spoke for Newton, he imagined the whole universe moved ten feet to the "
            "east, everything keeping its relations to everything else. <bookmark mark='b'/>For Newton, space is "
            "absolute, so the shifted universe would be really different. <bookmark mark='c'/>But then, Leibniz "
            "replied, God would have had no reason to put the world here rather than there, which violates sufficient "
            "reason. <bookmark mark='d'/>So the two situations are one and the same: indiscernible things are "
            "identical. <bookmark mark='e'/>And space is nothing but the order of things that exist together. Part "
            "25 returns to this argument, and to Newton's reply with a spinning bucket of water."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(w1))
            self.play(TransformFromCopy(w1, w2), GrowArrow(arr), FadeIn(tag))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
