from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


def hand(points, center, scale=0.42, color=MATTER):
    pts = [np.array([center[0] + scale * x, center[1] + scale * y, 0]) for x, y in points]
    return Polygon(*pts[:-1], color=color, fill_color=color, fill_opacity=0.35, stroke_width=3)


class Hands(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Incongruent counterparts", r"What makes a left hand left?", lit=(1768,),
                            part=PART)
        with self.voiceover("Chapter three. Incongruent counterparts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.kant()
        self.computed()
        self.mobius()
        self.verdict()

    def kant(self):
        d = load("hands")
        hc = history_card(1768, r"Immanuel Kant", r"`On the First Ground of the Distinction of Regions in Space'",
                          width=6.8, color=HIST).to_corner(UL, buff=0.3)
        L_ = hand(d["left"], (-3.2, -1.2), color=MATTER)
        R_ = hand(d["right"], (3.2, -1.2), color=CURVE)
        ll = label(r"left", font_size=22, color=MATTER).next_to(L_, DOWN, buff=0.25)
        rl = label(r"right", font_size=22, color=CURVE).next_to(R_, DOWN, buff=0.25)
        mirror = DashedLine([0, 1.0, 0], [0, -2.8, 0], color=GREY_B)
        rows = stack([(r"every internal relation is the same: \ lengths, \ angles, \ distances", WHITE),
                      (r"yet no motion in the plane lays one exactly on the other", BAD),
                      (r"Kant \ (1768): \ the difference is a relation to space itself", SPACE)], font_size=21,
                     aligned_edge=LEFT, width=6.6, buff=0.25).move_to([0, 1.6, 0])
        with self.voiceover(
            "In 1768 Immanuel Kant found a new argument for Newton. <bookmark mark='a'/>Take a left hand and a right "
            "hand, exact mirror images. <bookmark mark='b'/>Every relation among the parts of one is the same as "
            "among the parts of the other: the same lengths, the same angles, the same distances between every pair "
            "of points. <bookmark mark='c'/>Yet you cannot lay one exactly on top of the other; a right glove will "
            "not fit a left hand. They are incongruent counterparts. <bookmark mark='d'/>So, Kant argued, the "
            "difference between them cannot lie in the relations of their parts. It must be a relation to space "
            "itself, which is therefore real and absolute."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(L_), FadeIn(ll), Create(mirror))
            self.play(TransformFromCopy(L_, R_), FadeIn(rl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            moved = L_.copy()
            self.play(moved.animate.move_to(R_.get_center()), run_time=1.5)
            self.play(Rotate(moved, angle=PI / 2), run_time=1.0)
            self.play(Rotate(moved, angle=PI / 2), run_time=1.0)
            self.play(FadeOut(moved), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def computed(self):
        d = load("hands")
        head = label(r"Orientation, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"A = \tfrac12 \sum_i (x_i y_{i+1} - x_{i+1} y_i)", font_size=36, color=ABS).move_to(
            [0, 1.9, 0])
        rows = stack([(rf"the signed area of the left hand: \ ${d['left_area']:+.2f}$", MATTER),
                      (rf"of the right hand: \ ${d['right_area']:+.2f}$", CURVE),
                      (r"a rotation or translation of the plane has determinant $+1$: \ it keeps the sign", SPACE),
                      (rf"the Reasoner tries {d['rigid_motions_tried']} random rigid motions: \ "
                       rf"{d['rigid_sign_changes']} change the sign", OK),
                      (r"but turn the hand over through a third dimension, \ and the sign flips", GOAL)],
                     font_size=22, aligned_edge=LEFT, width=11.6, buff=0.3).move_to([0, -0.6, 0])
        assert d["rigid_sign_changes"] == 0
        with self.voiceover(
            "Kant's observation can be computed. <bookmark mark='a'/>Walk around the outline of a hand and add up "
            "this sum: it gives the area, with a sign that records which way round the outline goes. "
            "<bookmark mark='b'/>For the left hand the signed area is positive; <bookmark mark='c'/>for the right "
            "hand, the same size, negative. <bookmark mark='d'/>Any rotation or translation of the plane has "
            "determinant plus one, and keeps the sign. <bookmark mark='e'/>The Reasoner tries two hundred random "
            "rigid motions: not one changes the sign. <bookmark mark='f'/>But lift the hand out of the plane and "
            "turn it over through the third dimension, and the sign flips. In the plane the two are incongruent; "
            "in space, a flat hand and its mirror image are congruent."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            for mk, r in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def mobius(self):
        d = load("hands")
        head = label(r"A strip with a twist", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        strip = Rectangle(width=9.0, height=2.4, color=SPACE, fill_color=SPACE, fill_opacity=0.08,
                          stroke_width=2).move_to([0, 0.4, 0])
        a1 = Arrow([-4.5, -0.6, 0], [-4.5, 1.4, 0], buff=0, color=LIGHT, stroke_width=5)
        a2 = Arrow([4.5, 1.4, 0], [4.5, -0.6, 0], buff=0, color=LIGHT, stroke_width=5)
        glue = label(r"glue the ends so the arrows match: \ a Möbius strip", font_size=20,
                     color=LIGHT).next_to(strip, UP, buff=0.25)
        small = [(x * 0.55, y * 0.55) for x, y in d["left"]]
        h0 = hand(small, (-3.4, -0.1), scale=0.3, color=MATTER)
        rows = stack([(r"slide the hand to the right end: \ it re-enters at the left end, \ upside down", MATTER),
                      (r"once round the strip, \ a left hand comes back a right hand", CURVE),
                      (rf"the Reasoner carries a frame once round: \ the width direction comes back reversed, \ "
                       rf"{tuple(int(v) for v in d['mobius_width_start'])} $\to$ "
                       rf"{tuple(int(v) for v in d['mobius_width_end'])}", ABS),
                      (r"on a non-orientable space, \ `left' and `right' are not global facts", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=11.4, buff=0.25).to_edge(DOWN, buff=0.35)
        assert d["mobius_orientation_flips"]
        with self.voiceover(
            "There is a better reply to Kant, and it uses a strip of paper. <bookmark mark='a'/>Glue the ends of a "
            "strip together with a half twist, so that the arrows match: a Möbius strip. Draw a left hand on it. "
            "<bookmark mark='b'/>Slide the hand along the strip. When it passes the glued edge it comes back in at "
            "the other end, upside down: <bookmark mark='c'/>once round the strip, the left hand has become a right "
            "hand, without ever leaving the surface. <bookmark mark='d'/>The Reasoner carries a frame round the "
            "strip's centre line and finds its width direction reversed at the end. <bookmark mark='e'/>So whether "
            "two hands are incongruent depends on the global shape, the topology, of the space they live in. On a "
            "non-orientable space there is no fact about which hand is left."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(strip), GrowArrow(a1), GrowArrow(a2), FadeIn(glue), FadeIn(h0))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            self.play(h0.animate.move_to([4.2, -0.1, 0]), run_time=2.0, rate_func=linear)
            h0.flip(RIGHT).move_to([-4.2, 0.9, 0])
            self.play(h0.animate.move_to([-1.0, 0.9, 0]), run_time=1.6, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), Indicate(h0, color=CURVE))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def verdict(self):
        head = label(r"What the hands show", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Kant \ (1768)", r"handedness is a relation to absolute space", SPACE),
            (r"Kant \ (1783)", r"later: \ it shows that space is a form of our intuition, \ not a thing in itself", HIST),
            (r"the relationalist", r"handedness is a relation to the other hands, \ or to the orientation of the "
                                   r"whole space", MATTER),
            (r"a lone hand", r"in a universe containing only one hand, \ is it left or right? \ perhaps neither", BAD),
            (r"physics \ (1957)", r"the weak interaction is not mirror-symmetric: \ nature itself can tell left from "
                                  r"right", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "What do the hands show? <bookmark mark='a'/>In 1768 Kant took them to prove absolute space. "
            "<bookmark mark='b'/>By 1783 he used them for a different conclusion: that space is a form of our "
            "intuition, not a feature of things in themselves. <bookmark mark='c'/>A relationalist answers that "
            "handedness is a relation, to other hands, or to the orientation of the space as a whole, which the "
            "Möbius strip shows is a global, structural fact. <bookmark mark='d'/>Kant's own test case was a "
            "universe containing a single hand. Is it left or right? Perhaps neither, until there is something to "
            "compare it with. <bookmark mark='e'/>And physics added a twist of its own in 1957: the weak "
            "interaction is not mirror-symmetric. In the decay of cobalt-60, nature itself prefers one hand."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
