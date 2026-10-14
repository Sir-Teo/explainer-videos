from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import load


class Vitali(VoiceoverScene):
    def construct(self):
        self.card()
        self.wishes()
        self.orbit()
        self.construction()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"A set with no length", r"Can every set be given a length?", lit=(), part=5)
        with self.voiceover("Chapter two: why some sets must be left without a length."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def wishes(self):
        head = label(r"What we would like: \ a length $m(E)$ for \emph{every} set $E$ on the circle", font_size=34)
        head.to_edge(UP, buff=0.3)
        wishes = VGroup(
            label(r"1. \ countably additive: \ $m\big(\bigcup E_k\big) = \sum m(E_k)$ for disjoint $E_k$", font_size=26),
            label(r"2. \ rotation invariant: \ turning a set does not change its length", font_size=26),
            label(r"3. \ the whole circle has length $2\pi$", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        for w_ in wishes:
            if w_.width > 8.3:
                w_.width = 8.3
        wishes.next_to([-1.6, 0.7, 0], RIGHT, buff=0)
        verdict = label(r"impossible \ (Vitali, 1905): \ some set must be left out", font_size=30,
                        color=C.PATHOLOGY).next_to(wishes, DOWN, buff=0.7, aligned_edge=LEFT)
        # the picture: three disjoint arcs of the unit circle, measured by angle
        o, R = np.array([-4.3, -0.5, 0]), 1.85
        base = Circle(radius=R, color=GREY_D, stroke_width=2).move_to(o)
        starts, lens, cols = [0.3, 1.6, 3.6], [0.6, 0.9, 0.4], [C.FUNC, C.APPROX, C.MEASURE]
        arcs = VGroup(*[Arc(radius=R, start_angle=a0, angle=ln, color=c, stroke_width=10).move_arc_center_to(o)
                        for a0, ln, c in zip(starts, lens, cols)])
        assert all(starts[k] + lens[k] < starts[k + 1] for k in range(2))  # disjoint
        # each arc named just inside the circle, following its arc when the set is turned
        alabs = VGroup()
        for k, (a_, c_) in enumerate(zip(arcs, cols)):
            t_ = MathTex(rf"E_{k + 1}", font_size=26, color=c_)
            t_.add_updater(lambda m, a_=a_: m.move_to(o + (a_.point_from_proportion(0.5) - o) * (R - 0.42) / R),
                           call_updater=True)
            alabs.add(t_)
        tot = sum(lens)
        r1 = MathTex(rf"m(E_1 \cup E_2 \cup E_3) = {lens[0]} + {lens[1]} + {lens[2]} = {tot:.1f}", font_size=24).next_to(
            base, DOWN, buff=0.3)
        r2 = MathTex(rf"\text{{turned by }} 1.2: \ \text{{still }} {tot:.1f}", font_size=24).next_to(r1, DOWN, buff=0.15)
        whole = Circle(radius=R, color=C.EPS, stroke_width=3, stroke_opacity=0.8).move_to(o)
        r3 = MathTex(rf"m(\text{{circle}}) = 2\pi = {2 * math.pi:.4f}", font_size=24, color=C.EPS).next_to(base, UP,
                                                                                                         buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> Outer measure is defined for every set, but it isn't additive on every set. Could "
            "some cleverer definition be? We'd want three things on the circle: <bookmark mark='b'/> the length of a "
            "disjoint countable union is the sum of the lengths; <bookmark mark='c'/> turning a set doesn't change its "
            "length; <bookmark mark='d'/> and the whole circle has length two pi. <bookmark mark='e'/> In 1905 Vitali "
            "showed that no length function on all subsets can do all three."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(base), LaggedStart(*[Create(a_) for a_ in arcs], lag_ratio=0.4),
                      FadeIn(alabs))
            vo.wait_until("b")
            self.play(FadeIn(wishes[0], shift=RIGHT * 0.15), FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(wishes[1], shift=RIGHT * 0.15))
            self.play(Rotate(arcs, angle=1.2, about_point=o), FadeIn(r2), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(wishes[2], shift=RIGHT * 0.15), Create(whole), FadeIn(r3))
            self.bring_to_front(arcs)
            vo.wait_until("e")
            self.play(FadeIn(verdict))
        alabs.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def orbit(self):
        d = load("vitali")
        ang, maxgap, Ns = d["ang"], d["maxgap"], d["Ns"]
        o = np.array([-3.0, -0.5, 0])
        R = 2.6
        circ = Circle(radius=R, color=GREY_C, stroke_width=2).move_to(o)

        def pt(a):
            return o + R * np.array([math.cos(a), math.sin(a), 0])

        dots = VGroup(*[Dot(pt(a), radius=0.06 if k < 50 else 0.03, color=C.SEQ) for k, a in enumerate(ang)])
        nums = VGroup(*[MathTex(str(k), font_size=20, color=C.SEQ).move_to(o + (R + 0.3) * np.array(
            [math.cos(ang[k]), math.sin(ang[k]), 0])) for k in range(7)])
        head = VGroup(label(r"Rotate by $1$ radian, again and again", font_size=34),
                      label(r"$1$ is not a rational multiple of $2\pi$: \ the orbit never repeats", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.3)
        tab = VGroup(MathTex(r"N", r"\quad \text{largest gap}", font_size=28, color=GREY_A))
        for n, g in zip(Ns, maxgap):
            tab.add(MathTex(rf"{int(n)}", rf"\quad {g:.4f}", font_size=28))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.6, 0.0, 0])
        regrid(tab)
        out = label(r"the orbit is dense: \ it comes within $0.0044$ of every point", font_size=26, color=C.EPS).next_to(
            tab, DOWN, buff=0.35)
        assert maxgap[-1] < 0.0088 + 1e-4
        with self.voiceover(
            "<bookmark mark='a'/> The construction uses rotation of the circle by one radian. Since one radian is not "
            "a rational multiple of a full turn, the orbit of a point never comes back to it. <bookmark mark='b'/> "
            "It fills the circle densely: after two thousand steps, the largest gap is less than a hundredth of a "
            "radian."
        ) as vo:
            self.play(FadeIn(head[0]), Create(circ))
            vo.wait_until("a")
            self.play(FadeIn(head[1]), LaggedStart(*[AnimationGroup(FadeIn(dots[k], scale=1.5), FadeIn(nums[k]))
                                                     for k in range(7)], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            prev = 7
            for i, n in enumerate(Ns[1:], start=2):
                self.play(LaggedStart(*[FadeIn(dd) for dd in dots[prev:int(n)]], lag_ratio=0.002), FadeIn(tab[i]),
                          run_time=1.2)
                prev = int(n)
            self.play(FadeIn(out))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def construction(self):
        o = np.array([-3.4, -0.55, 0])
        R = 2.35
        circ = Circle(radius=R, color=GREY_C, stroke_width=2).move_to(o)

        def pt(a):
            return o + R * np.array([math.cos(a), math.sin(a), 0])

        starts = [0.15, 0.55, 1.05, 1.6, 2.3]
        cols = [C.SEQ, C.APPROX, C.CLOSED_SET, C.CONNECTED_SET, C.FREQ]
        orbits = VGroup()
        for s0, c in zip(starts, cols):
            orbits.add(VGroup(*[Dot(pt(s0 + k), radius=0.045, color=c).set_opacity(0.8) for k in range(-12, 13)]))
        reps = VGroup(*[Dot(pt(s0), radius=0.11, color=c) for s0, c in zip(starts, cols)])
        tag = schematic_tag().scale(0.9).next_to(circ, UP, buff=0.15).align_to(circ, LEFT)

        def shifted(k):
            return VGroup(*[Dot(pt(s0 + k), radius=0.11, color=c) for s0, c in zip(starts, cols)])

        rows = VGroup(
            label(r"call $x \sim y$ if they differ by a whole number of radians", font_size=24),
            label(r"each class is one orbit: \ countable, dense", font_size=24, color=GREY_A),
            label(r"$V$: \ one point from every class \ (the axiom of choice)", font_size=24, color=C.EPS),
            label(r"the copies $V + k$, \ $k \in \mathbb Z$: \ disjoint, and they fill the circle", font_size=24),
            MathTex(r"2\pi = \sum_{k \in \mathbb Z} m(V + k) = \sum_{k \in \mathbb Z} m(V) \in \{0, \infty\}",
                    font_size=30, color=C.PATHOLOGY),
            label(r"so $V$ can have no length \ (Rudin, \textit{RCA} 2.22)", font_size=24, color=C.PATHOLOGY),
            label(r"in 3D the sequel is Banach--Tarski: \ a ball cut and reassembled into two", font_size=22,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, -0.55, 0])
        for r_ in rows:
            if r_.width > 6.6:
                r_.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, -0.55, 0])
        head = label(r"Vitali's set", font_size=34).to_edge(UP, buff=0.3)
        # the sum over k of m(V + k), laid end to end around the circle as arcs of a common length c (a spiral, so
        # that the wraps stay visible): c = 0 gives nothing, any c > 0 wraps around more than once, forever
        cv = ValueTracker(1e-3)
        K = 16
        # lengths are MEASURE (the orbit colors above name classes, not copies): alternate the opacity so the copies
        # V + k laid end to end stay distinct

        def arcs_():
            c = cv.get_value()
            return VGroup(*[Arc(radius=R + 0.15 + 0.035 * k, start_angle=k * c, angle=c, arc_center=o,
                                color=C.MEASURE, stroke_width=5, stroke_opacity=1.0 if k % 2 == 0 else 0.55)
                            for k in range(K)])

        arcs = always_redraw(arcs_)
        zl = MathTex(r"m(V) = 0: \ 0 + 0 + 0 + \cdots = 0", font_size=26).move_to(o + 0.35 * UP)
        il = MathTex(r"m(V) = c > 0: \ c + c + c + \cdots = \infty", font_size=26, color=C.PATHOLOGY
                     ).move_to(o + 0.35 * DOWN)
        assert K * 0.9 > 2 * 2 * math.pi  # at c = 0.9 the 16 shown arcs already wrap around twice
        assert (R + 0.15 + 0.035 * (K - 1)) + abs(o[0]) < 6.7 and o[1] - (R + 0.15 + 0.035 * (K - 1)) > -3.6
        assert max(zl.width, il.width) < 2 * R - 0.6
        with self.voiceover(
            "<bookmark mark='a'/> Call two points equivalent if they differ by a whole number of radians. Each "
            "class is one orbit, countable and dense; here are five of them, though there are uncountably many. "
            "<bookmark mark='b'/> Using the axiom of choice, pick one point from every class, and call the resulting "
            "set V. This step can only be drawn as a schematic. <bookmark mark='c'/> Now rotate V by one radian, by "
            "two, by minus one, and so on. These copies are disjoint, and since every point is in some class, they "
            "fill the whole circle. <bookmark mark='d'/> If V had a length, countable additivity and rotation "
            "invariance would make two pi a sum of infinitely many copies of the same number: <bookmark mark='z'/> "
            "zero if the number is zero, <bookmark mark='i'/> infinite otherwise, because copies of any positive "
            "length, laid end to end, go around the circle again and again. <bookmark mark='n'/> Neither is two pi. "
            "So V has no length, and a theory of length must restrict itself to a smaller class of sets: the "
            "measurable ones. <bookmark mark='t'/> In three dimensions the same idea gives the Banach–Tarski paradox."
        ) as vo:
            self.play(FadeIn(head), Create(circ))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(o_) for o_ in orbits], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(tag), orbits.animate.set_opacity(0.35), FadeIn(reps, scale=1.6), FadeIn(rows[2]))
            vo.wait_until("c")
            cur = reps
            for k in (1, 2, 3, -1, -2):
                nxt = shifted(k)
                self.play(TransformFromCopy(cur, nxt), run_time=0.7)
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("z")
            self.add(arcs)
            self.play(FadeIn(zl))
            vo.wait_until("i")
            self.play(cv.animate.set_value(0.9), FadeIn(il), run_time=3.5, rate_func=smooth)
            arcs.clear_updaters()
            vo.wait_until("n")
            self.play(FadeIn(rows[5]), Indicate(rows[4][0][0:2], color=C.PATHOLOGY))
            vo.wait_until("t")
            self.play(FadeIn(rows[6]))
        self.wait(0.4)
        self.clear_scene()
