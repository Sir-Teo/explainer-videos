from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import FEATURE_COLORS, PART, arrow2d, load

COLS = FEATURE_COLORS[:5]


class Superposition(VoiceoverScene):
    def construct(self):
        self.card()
        self.toy()
        self.learning()
        self.interference()

    def card(self):
        card = chapter_card(6, r"More ideas than dimensions", r"Why is every number busy?", part=PART)
        with self.voiceover("Chapter six. More ideas than dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def plane(self, c0, R):
        circ = Circle(radius=R, stroke_color=GREY_D, stroke_width=1.5).move_to(c0)
        axes = VGroup(Line(c0 + LEFT * (R + 0.3), c0 + RIGHT * (R + 0.3), color=GREY_D, stroke_width=1),
                      Line(c0 + DOWN * (R + 0.3), c0 + UP * (R + 0.3), color=GREY_D, stroke_width=1))
        return VGroup(axes, circ)

    def toy(self):
        s = load("superposition")
        Ss = [float(v) for v in s["sparsities"]]
        imp = np.asarray(s["importance"])
        c0, R = np.array([3.4, -0.5, 0]), 2.0
        sc = R / max(np.linalg.norm(np.asarray(s[f"W{Ss[-1]:g}"]), axis=0).max(), 1e-9)

        def arrows(S):
            W = np.asarray(s[f"W{S:g}"])
            return VGroup(*[arrow2d(c0, W[:, i], COLS[i], sc) if np.linalg.norm(W[:, i]) > 0.05 else
                            Dot(c0, radius=0.06, color=COLS[i]) for i in range(5)])

        pl = self.plane(c0, R)
        hl = label(r"the $2$ hidden numbers: \ where each feature points", font_size=22, color=GREY_A).next_to(pl, UP, buff=0.15)
        # the network: 5 features in, 2 numbers in the middle, 5 out
        xin = VGroup(*[Circle(radius=0.16, stroke_color=c_, stroke_width=2.5, fill_color=c_, fill_opacity=0.2 + 0.6 * imp[i])
                       for i, c_ in enumerate(COLS)]).arrange(DOWN, buff=0.22).move_to([-5.6, -0.6, 0])
        hid = VGroup(*[Circle(radius=0.16, stroke_color=WHITE, stroke_width=2.5) for _ in range(2)]).arrange(DOWN, buff=0.5)
        hid.move_to([-3.9, -0.6, 0])
        xout = xin.copy().move_to([-2.2, -0.6, 0])
        e1 = VGroup(*[Line(a.get_right(), b.get_left(), stroke_width=1.2, color=GREY_C) for a in xin for b in hid])
        e2 = VGroup(*[Line(a.get_right(), b.get_left(), stroke_width=1.2, color=GREY_C) for a in hid for b in xout])
        nl = VGroup(label(r"$5$ features", font_size=20, color=GREY_A).next_to(xin, DOWN, buff=0.2),
                    label(r"$2$ numbers", font_size=20, color=GREY_A).next_to(hid, DOWN, buff=1.0),
                    label(r"$5$ back", font_size=20, color=GREY_A).next_to(xout, DOWN, buff=0.2))
        colors = {r"W": C.BITS, r"x": C.TRUE_P}
        f = cmath(r"\hat{", r"x", r"} = \operatorname{ReLU}(", r"W", r"^{\!\top}", r"W", r"\,", r"x", r" + b)", colors=colors,
                  font_size=36).move_to([-3.9, 2.4, 0])
        imp_l = label(r"brighter: \ more important to get right", font_size=20, color=GREY_B).next_to(nl, DOWN, buff=0.3)
        imp_l.set_x(-3.9)
        fw = label(r"$W$: \ squeeze $5$ numbers into $2$; \\ $W^{\top}$: \ spread them back out to $5$; \\ "
                   r"ReLU: \ cut off negatives", font_size=18, color=GREY_A).next_to(f, DOWN, buff=0.15)
        keep_in_frame(fw)
        tracker = ValueTracker(Ss[0])

        def freq_label():
            on = 100 * (1 - tracker.get_value())
            return label(rf"each feature on \ ${on:.0f}\%$ \ of the time", font_size=26, color=C.BITS).move_to([3.4, -3.15, 0])

        fl = freq_label()
        cur = arrows(Ss[0])
        cite_ = cite(r"N.~Elhage et al., \textit{Toy Models of Superposition} (2022)", corner=UR)
        n_kept = [int((np.asarray(s[f"norms{S:g}"]) > 0.5).sum()) for S in Ss]
        with self.voiceover(
            "Here's the smallest model that shows why. Five features go in, squeezed through just two numbers, and "
            "the network must give all five back: x hat equals ReLU of W transpose W x, plus b. <bookmark mark='w'/> "
            "In words: W squeezes the five numbers into two, the same W run backwards spreads them out to five again, "
            "and the ReLU cuts off anything negative. The features matter unequally, the brighter ones more. "
            "<bookmark mark='a'/> Each column of W says where a feature points in "
            "the two-dimensional middle. <bookmark mark='b'/> When every feature is on all the time, the trained "
            f"network keeps just the {n_kept[0]} most important, at right angles, and drops the rest. "
            f"<bookmark mark='c'/> Make the features rarer, and it starts to cheat: {n_kept[1]} features, in opposite "
            f"pairs. <bookmark mark='d'/> Rarer still, and all {n_kept[-1]} fit, as a pentagon. Five ideas in two "
            "dimensions. That's superposition."
        ) as vo:
            self.play(FadeIn(xin), FadeIn(hid), FadeIn(xout), Create(e1), Create(e2), FadeIn(nl), FadeIn(cite_), run_time=1.5)
            self.play(Write(f), FadeIn(imp_l))
            vo.wait_until("w")
            self.play(FadeIn(fw, shift=DOWN * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(pl), FadeIn(hl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a_) if isinstance(a_, Arrow) else FadeIn(a_) for a_ in cur], lag_ratio=0.15), FadeIn(fl))
            for mark_, S in zip("cd", Ss[1:3]):
                vo.wait_until(mark_)
                self.play(Transform(cur, arrows(S)), tracker.animate.set_value(S), run_time=2.0)
                self.play(Transform(fl, freq_label()), run_time=0.3)
            self.play(Transform(cur, arrows(Ss[-1])), tracker.animate.set_value(Ss[-1]), run_time=1.2)
            self.play(Transform(fl, freq_label()), run_time=0.3)
            poly = Polygon(*[c0 + sc * np.array([*np.asarray(s[f"W{Ss[-1]:g}"])[:, i], 0]) for i in
                             np.argsort(np.arctan2(*np.asarray(s[f"W{Ss[-1]:g}"])[::-1]))], color=C.BITS, stroke_width=2)
            self.play(Create(poly))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def interference(self):
        s = load("superposition")
        S = float(s["sparsities"][-1])
        W, b = np.asarray(s[f"W{S:g}"]), np.asarray(s[f"b{S:g}"])
        ro, ar = np.asarray(s["readout"]), np.asarray(s["after_relu"])
        c0, R = np.array([-3.6, -0.3, 0]), 2.0
        sc = R / np.linalg.norm(W, axis=0).max()
        pl = self.plane(c0, R)
        arr = VGroup(*[arrow2d(c0, W[:, i], COLS[i], sc) for i in range(5)])
        on = arr[0].copy().set_stroke(width=9)
        u = W[:, 0] / np.linalg.norm(W[:, 0])
        projs = VGroup(*[DashedLine(c0 + sc * np.array([*W[:, i], 0]), c0 + sc * np.dot(W[:, i], u) * np.array([*u, 0]),
                                    color=COLS[i], stroke_width=1.5) for i in range(1, 5)])
        # the five outputs, as bars: W^T W x, then + b, then ReLU
        x0, y0, bw, k = 1.2, -0.6, 0.6, 1.2

        def bars(v):
            return VGroup(*[Rectangle(width=bw, height=max(abs(x) * k, 0.01), stroke_width=0, fill_color=COLS[i], fill_opacity=0.9)
                            .move_to([x0 + i * 1.0, y0 + x * k / 2, 0]) for i, x in enumerate(v)])

        base = Line([x0 - 0.6, y0, 0], [x0 + 4.6, y0, 0], color=GREY_C, stroke_width=1.5)
        b_ro, b_b, b_ar = bars(ro), bars(ro + b), bars(ar)
        names = VGroup(*[MathTex(rf"\hat x_{i + 1}", font_size=26, color=COLS[i]).move_to([x0 + i * 1.0, y0 - 1.75, 0]) for i in range(5)])
        steps = [cmath(r"W^{\!\top} W x", font_size=32), cmath(r"W^{\!\top} W x + b", font_size=32),
                 cmath(r"\operatorname{ReLU}(W^{\!\top} W x + b)", font_size=32)]
        for t in steps:
            t.move_to([x0 + 2.0, 2.5, 0])
        lab = label(r"feature $1$ on, \ the rest off", font_size=24, color=COLS[0]).next_to(pl, UP, buff=0.15)
        res = label(rf"what leaks through: \ ${ar[1:].max():.2f}$ at most, \ against ${ar[0]:.2f}$", font_size=22,
                    color=GREY_A).move_to([x0 + 2.0, -3.1, 0])
        ang = np.degrees(np.arccos(np.clip([W[:, 0] @ W[:, i] / np.linalg.norm(W[:, 0]) / np.linalg.norm(W[:, i])
                                            for i in range(1, 5)], -1, 1)))
        near, far = np.sort(ang)[:2].mean(), np.sort(ang)[2:].mean()
        with self.voiceover(
            "But packing has a price. Turn on feature one alone. <bookmark mark='a'/> Reading it back out, every "
            f"other feature sees its shadow along their direction. <bookmark mark='b'/> The neighbours, at about "
            f"{near:.0f} degrees, get a little; the far ones, at about {far:.0f}, get a negative amount. "
            "<bookmark mark='c'/> The bias pushes everything down a little, <bookmark mark='d'/> and the ReLU throws "
            "away whatever is negative. What's left over is small: a little noise, the cost of sharing space. It's "
            "worth paying only because the features are rarely on together."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(arr), FadeIn(lab))
            self.play(FadeIn(on), *[a_.animate.set_opacity(0.35) for a_ in arr[1:]])
            vo.wait_until("a")
            self.play(Create(projs), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(base), FadeIn(names), FadeIn(steps[0]), LaggedStart(*[GrowFromEdge(r_, DOWN if v > 0 else UP)
                                                                                   for r_, v in zip(b_ro, ro)], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(Transform(b_ro, b_b), TransformMatchingTex(steps[0], steps[1]), run_time=1.2)
            vo.wait_until("d")
            self.play(Transform(b_ro, b_ar), TransformMatchingTex(steps[1], steps[2]), run_time=1.2)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        """How the pentagon forms: the sparse model's five feature arrows, from random to the pentagon, as it trains."""
        s = load("superposition")
        Ss = [float(v) for v in s["sparsities"]]
        S = Ss[-1]
        Wt = np.asarray(s[f"Wtrain{S:g}"])
        checks = [int(c) for c in s["checks"]]
        L = np.asarray(s[f"losses{S:g}"])
        c0, R = np.array([-3.0, -0.4, 0]), 2.2
        sc = R / max(np.linalg.norm(Wt[-1], axis=0).max(), 1e-9)

        def arrows(k):
            W = Wt[k]
            return VGroup(*[arrow2d(c0, W[:, i], COLS[i], sc) if np.linalg.norm(W[:, i]) * sc > 0.08 else
                            Dot(c0, radius=0.06, color=COLS[i]) for i in range(W.shape[1])])

        pl = self.plane(c0, R)
        cur = arrows(0)
        ax = CornerAxes(x_range=[0, checks[-1], 2000], y_range=[0, float(L[:, 1].max()) * 1.05, float(L[:, 1].max()) / 2],
                        x_length=4.6, y_length=2.6, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}
                        ).move_to([3.6, -0.4, 0])
        yn = label(r"the weighted rebuild error", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        xn = label(r"training steps", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        t = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28, color=C.BITS)
                            .next_to(pl, UP, buff=0.2))
        on = 100 * (1 - S)
        ang = [np.sort(np.mod(np.degrees(np.arctan2(W_[1], W_[0])), 360)) for W_ in Wt]
        gaps = [np.diff(np.concatenate([a_, [a_[0] + 360]])) for a_ in ang]
        settled = next((c for c, g_ in zip(checks, gaps) if g_.std() < 3), checks[-1])  # the first even spacing
        hl = label(rf"each feature on ${on:.0f}\%$ of the time", font_size=20, color=GREY_A).next_to(pl, DOWN, buff=0.2)
        with self.voiceover(
            "How does the network find that pentagon? Here is the sparse model learning, from its random start. "
            "<bookmark mark='a'/> At first the five arrows point anywhere, some short, some long. "
            "<bookmark mark='b'/> Within a few hundred steps they all grow, and they push each other apart: two "
            "features pointing the same way would be read as each other. "
            + f"<bookmark mark='c'/> By step {settled:,} the spacing is even, and the rest of training barely moves "
            "them. Nobody planned the pentagon; gradient descent found it, fast."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(hl), Create(ax), FadeIn(yn), FadeIn(xn))
            self.add(cnt)
            self.play(FadeIn(cur))
            vo.wait_until("a")
            marks = {2: "b", 4: "c"}
            for k in range(1, len(checks)):
                if k in marks:
                    vo.wait_until(marks[k])
                seg = [ax.c2p(a, b) for a, b in L if checks[k - 1] <= a <= checks[k]]
                anims = [Transform(cur, arrows(k)), t.animate.set_value(checks[k])]
                if len(seg) > 1:
                    anims.append(Create(VMobject(color=C.BITS, stroke_width=2.5).set_points_as_corners(seg)))
                self.play(*anims, run_time=1.2)
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()
