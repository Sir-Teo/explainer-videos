from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai30.common import FEAT, MONO, RESID, heat_image, load, show, signed_image, vec_bars


class Hook(VoiceoverScene):
    def construct(self):
        self.opaque()
        self.plan()

    # ------------------------------------------------------------------
    def opaque(self):
        s = load("sae")
        text = str(s["demo_text"])[:48]
        R = np.asarray(s["demo_resid"])[:48]  # (positions, 128)
        Fz = np.asarray(s["demo_feats"])[:48]  # (positions, 512)
        n = len(text)
        W = 12.0
        step = W / n
        chars = VGroup(*[Text(show(c), font=MONO, font_size=22, color=GREY_A).move_to([-W / 2 + step * (i + 0.5), 3.1, 0])
                         for i, c in enumerate(text)])
        dense = signed_image(R.T, W, 2.4, pos=RESID, neg=C.SURPRISE).move_to([0, 1.35, 0])
        dl = label(r"inside Part 13's transformer, \ after block $2$: \ $128$ numbers per character", font_size=22,
                   color=RESID).next_to(dense, DOWN, buff=0.12)
        used = Fz[:, (Fz > 0).any(0)]
        order = np.argsort(np.argmax(used > 0, 0))  # features in order of first firing, for a readable picture
        sparse = heat_image(used[:, order].T, W, 2.4, color=FEAT, gamma=0.6).move_to([0, -1.6, 0])
        sl = label(rf"the same, rewritten as features: \ ${used.shape[1]}$ of $512$ ever fire here, \ "
                   rf"${float(s['l0']):.0f}$ at a time on average", font_size=22, color=FEAT).next_to(sparse, DOWN, buff=0.12)
        # one character, as numbers and as features
        k = int(np.argmax([c.isalpha() for c in text[20:]])) + 20
        col = SurroundingRectangle(Group(chars[k], dense), buff=0.02, color=WHITE, stroke_width=2)
        col.stretch_to_fit_width(step * 1.1).move_to([chars[k].get_x(), (chars[k].get_top()[1] + dense.get_bottom()[1]) / 2, 0])
        q = label(r"What is it thinking?", font_size=40).move_to(DOWN * 1.6)
        with self.voiceover(
            "Over twenty parts, we've built every piece of these models ourselves. We know every number in them. And "
            "yet we can't say what they're thinking. <bookmark mark='a'/> Here's our transformer reading a line of the "
            "passage: for each character, the hundred and twenty-eight numbers it carries after its second block. "
            "Every one of them busy, all the time; not one of them means anything by itself. <bookmark mark='b'/> "
            "This part is about reading them. <bookmark mark='c'/> Rewritten in the right basis, the picture "
            "changes: only a handful of features, ideas the model tracks, are on at each character, and each one "
            "turns out to mean something."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c) for c in chars], lag_ratio=0.02), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(dense), FadeIn(dl), run_time=1.5)
            self.play(Create(col))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(q), FadeOut(col))
            self.play(FadeIn(sparse), FadeIn(sl), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

        # the continuity: one character's 128 numbers turn into its few features
        x, f = R[k], Fz[k]
        b1 = vec_bars(x, 9.0, 2.4, RESID).move_to([1.3, 1.3, 0])
        b2 = vec_bars(f, 9.0, 2.2, FEAT, signed=False)
        b2.shift([1.3 - b2.get_x(), -2.9 - b2.get_bottom()[1], 0])
        ch = Text(f"“{show(text[k])}”", font=MONO, font_size=36, color=WHITE).to_edge(UP, buff=0.3)
        l1 = label(r"$128$ numbers, \\ all busy", font_size=24, color=RESID).move_to([-4.9, 1.3, 0])
        l2 = label(rf"$512$ features, \\ ${int((f > 0).sum())}$ on", font_size=24, color=FEAT).move_to([-4.9, -1.8, 0])
        # what a feature is: a direction; how far the vector points along it is how strongly the feature is on
        O = np.array([-3.0, -1.6, 0])
        u = np.array([np.cos(0.35), np.sin(0.35), 0])
        fa = Arrow(O, O + 6.6 * u, buff=0, color=FEAT, stroke_width=5, max_tip_length_to_length_ratio=0.05)
        fl = label(r"a feature: \\ ``inside a quotation''", font_size=24, color=FEAT).next_to(fa.get_end(), RIGHT, buff=0.2)
        ang = ValueTracker(1.45)

        def xv():
            return 3.4 * np.array([np.cos(ang.get_value()), np.sin(ang.get_value()), 0])

        def shadow():
            v = xv()
            p_ = O + max(float(v @ u), 0) * u
            return VGroup(Arrow(O, O + v, buff=0, color=WHITE, stroke_width=5, max_tip_length_to_length_ratio=0.1),
                          DashedLine(O + v, p_, dash_length=0.08, stroke_width=1.5, color=GREY_B),
                          Line(O, p_, color=C.TRUE_P, stroke_width=10),
                          MathTex("x", font_size=34, color=WHITE).next_to(O + v, UP, buff=0.1))

        sh = always_redraw(shadow)
        hl = label(r"its shadow on the feature: \\ how strongly the feature is on", font_size=22, color=C.TRUE_P).move_to([3.0, 2.3, 0])
        fh = label(r"a feature is a direction", font_size=30, color=FEAT).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Take one character. <bookmark mark='a'/> Its hundred and twenty-eight numbers, tangled together, "
            f"become {int((f > 0).sum())} features out of five hundred and twelve. <bookmark mark='f'/> A feature is "
            "one idea the model tracks, like 'inside a quotation', stored as a direction among those numbers. How far "
            "the vector points that way, its shadow on that direction, is how strongly the feature is on."
        ) as vo:
            self.play(FadeIn(ch), FadeIn(b1), FadeIn(l1))
            vo.wait_until("a")
            self.play(ReplacementTransform(b1.copy(), b2), FadeIn(l2), run_time=2.0)
            vo.wait_until("f")
            self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
            self.play(FadeIn(fh), GrowArrow(fa), FadeIn(fl))
            self.add(sh)
            self.play(FadeIn(hl))
            self.play(ang.animate.set_value(0.75), run_time=2.0)
            self.play(ang.animate.set_value(1.2), run_time=1.2)
        sh.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 30: \ Inside the Model", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"superposition, \ sparse features, \ circuits, \ steering", font_size=30, color=C.BITS)
        sub.next_to(title, DOWN, buff=0.25)
        smap = series_map(current=30, done=29).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "In this last part: why the numbers are tangled, how to untangle them, how to trace a thought from input "
            "to output, <bookmark mark='a'/> and how to reach in and change it."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
