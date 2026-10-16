from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai2.common import MONO, arrow, barcode, load, plane


class Dot(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.turning()
        self.words()
        self.logits()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Angles: the dot product", r"How alike are two vectors?", part=2)
        with self.voiceover("Chapter two. How alike are two vectors?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definition(self):
        pl = plane(faded=True)
        a, b = np.array([3.0, 1.0, 0]), np.array([1.0, 2.0, 0])
        A, B = C.TRUE_P, C.MODEL_Q
        aa, ab = arrow(a, color=A), arrow(b, color=B)
        la = MathTex(r"\mathbf{a}", font_size=42, color=A).next_to(a, RIGHT, buff=0.12)
        lb = MathTex(r"\mathbf{b}", font_size=42, color=B).next_to(b, UP, buff=0.12)
        ang = Angle(Line(ORIGIN, a), Line(ORIGIN, b), radius=0.8, color=WHITE)
        th = MathTex(r"\theta", font_size=36).move_to(Angle(Line(ORIGIN, a), Line(ORIGIN, b), radius=1.15).point_from_proportion(0.5))
        colors = {r"\mathbf{a}": A, r"\mathbf{b}": B, r"a_1": A, r"a_2": A, r"b_1": B, r"b_2": B, r"|\mathbf{a}|": A,
                  r"|\mathbf{b}|": B}
        e1 = cmath(r"\mathbf{a}", r"\cdot", r"\mathbf{b}", "=", r"a_1", r"b_1", "+", r"a_2", r"b_2", colors=colors,
                   font_size=50).to_corner(UL, buff=0.5)
        e2 = cmath(r"\mathbf{a}", r"\cdot", r"\mathbf{b}", "=", r"|\mathbf{a}|", r"|\mathbf{b}|", r"\cos\theta",
                   colors=colors, font_size=50).next_to(e1, DOWN, buff=0.35, aligned_edge=LEFT)
        num = MathTex(r"3 \cdot 1 + 1 \cdot 2 = 5", font_size=40).next_to(e1, RIGHT, buff=0.6)
        for m in (e1, e2, num):
            m.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.1)
        with self.voiceover(
            "How alike are two vectors? <bookmark mark='a'/> Multiply them coordinate by coordinate, and add it all "
            "up. That's the dot product. <bookmark mark='b'/> It has a second meaning: the length of one, times the "
            "length of the other, times the cosine of the angle between them."
        ) as vo:
            self.play(FadeIn(pl), GrowArrow(aa), GrowArrow(ab), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(Write(e1))
            self.play(FadeIn(num))
            vo.wait_until("b")
            self.play(Create(ang), FadeIn(th), Write(e2))
        self.wait(0.3)
        self.play(FadeOut(VGroup(ab, lb, ang, th, num, e1)), e2.animate.to_corner(UL, buff=0.5))
        self.pl, self.a, self.aa, self.la, self.e2 = pl, a, aa, la, e2

    # ------------------------------------------------------------------
    def turning(self):
        a = self.a
        ua = a / np.linalg.norm(a)
        t = ValueTracker(math.atan2(2, 1))
        R = 2.4

        def bvec():
            return R * np.array([math.cos(t.get_value()), math.sin(t.get_value()), 0])

        def shadow():
            b = bvec()
            p = (b @ ua) * ua
            col = C.REWARD if b @ ua > 0.05 else (C.PENALTY if b @ ua < -0.05 else GREY_B)
            return VGroup(DashedLine(b, p, color=GREY_B, stroke_width=2),
                          Line(ORIGIN, p, color=col, stroke_width=10, stroke_opacity=0.85))

        line = Line(-4.5 * ua, 4.5 * ua, color=GREY_D, stroke_width=2)
        ab = always_redraw(lambda: arrow(bvec(), color=C.MODEL_Q))
        sh = always_redraw(shadow)
        cosv = DecimalNumber(0, num_decimal_places=2, font_size=44, include_sign=True)
        cl = MathTex(r"\cos\theta =", font_size=44)
        read = VGroup(cl, cosv).arrange(RIGHT, buff=0.2).to_corner(UR, buff=0.6)
        cosv.add_updater(lambda m: m.set_value(float(bvec() @ ua) / R))
        bg = BackgroundRectangle(read, color=BACKGROUND, fill_opacity=0.85, buff=0.15)
        with self.voiceover(
            "Watch it as one vector turns. <bookmark mark='a'/> Pointing the same way, the dot product is as big as "
            "it can get. <bookmark mark='b'/> At a right angle, it's zero. <bookmark mark='c'/> Pointing apart, it's "
            "negative. Against a vector of length one, the dot product is the length of the shadow that one vector "
            "casts on the other."
        ) as vo:
            self.add(line, sh, ab, bg, read)
            self.bring_to_front(self.aa, self.la)
            vo.wait_until("a")
            self.play(t.animate.set_value(math.atan2(1, 3)), run_time=1.5)
            vo.wait_until("b")
            self.play(t.animate.set_value(math.atan2(1, 3) + PI / 2), run_time=1.5)
            vo.wait_until("c")
            self.play(t.animate.set_value(math.atan2(1, 3) + PI), run_time=1.5)
            self.play(t.animate.set_value(math.atan2(1, 3) + 2 * PI + 0.6), run_time=3.0)
        for m in (ab, sh, cosv):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def words(self):
        g = load("gpt2")
        V = np.asarray(g["barcodes"])
        cos = np.asarray(g["barcode_cos"])
        names = list(g["barcode_words"])
        assert names == ["dog", "puppy", "tobacco", "cat"]
        assert abs(cos[0, 1] - 0.62) < 0.005 and abs(cos[0, 3] - 0.55) < 0.005 and abs(cos[0, 2] - 0.23) < 0.005
        head = label(r"cosine similarity $= \dfrac{\mathbf{a} \cdot \mathbf{b}}{|\mathbf{a}|\,|\mathbf{b}|}$", font_size=38)
        head.to_edge(UP, buff=0.4)
        pairs = [(1, C.TRUE_P), (3, C.TRUE_P), (2, GREY_B)]
        rows = VGroup()
        for j, col in pairs:
            name = Text(f"dog · {names[j]}", font=MONO, font_size=28, color=WHITE)
            w = 6.5 * cos[0, j]
            bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.9)
            val = MathTex(f"{cos[0, j]:.2f}", font_size=34, color=col)
            rows.add(VGroup(name, bar, val))
        for k, r in enumerate(rows):
            r[0].move_to([-4.3, 1.6 - 0.75 * k, 0], aligned_edge=RIGHT).shift(RIGHT * 1.4)
            r[1].move_to([-2.6, 1.6 - 0.75 * k, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.2)
        # in 768 dimensions: multiply number by number, and add
        vmax = float(np.abs(V[:2]).max())
        prod = V[0] * V[1]
        b1 = barcode(V[0], width=9.0, height=0.7, vmax=vmax).move_to([0.2, -1.0, 0])
        b2 = barcode(V[1], width=9.0, height=0.7, vmax=vmax).move_to([0.2, -1.9, 0])
        b3 = barcode(prod, width=9.0, height=0.7, pos=C.REWARD, neg=C.PENALTY).move_to([0.2, -2.95, 0])
        n1 = Text("dog", font=MONO, font_size=24).next_to(b1, LEFT, buff=0.25)
        n2 = Text("puppy", font=MONO, font_size=24).next_to(b2, LEFT, buff=0.25)
        n3 = MathTex(r"\times", font_size=34).next_to(b3, LEFT, buff=0.35)
        tot = MathTex(rf"\textstyle\sum = {float(prod.sum()):.1f}", font_size=34, color=C.REWARD).next_to(b3, RIGHT, buff=0.2)
        with self.voiceover(
            "Divide by the two lengths and you get the cosine similarity, which runs from minus one to one. "
            "<bookmark mark='a'/> For GPT-2's words: dog and puppy, 0.62. Dog and cat, 0.55. Dog and tobacco, "
            "0.23. <bookmark mark='b'/> In 768 dimensions you can't draw the angle, but you can compute it: "
            "multiply the two lists number by number, and add."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for r in rows:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(n1), FadeIn(b1), FadeIn(n2), FadeIn(b2))
            # bar by bar (the same structure): a group-to-group transform would pad 2 barcodes into 768 copies
            self.play(TransformFromCopy(b1, b3), Indicate(b2, color=WHITE, scale_factor=1.02), FadeIn(n3), run_time=1.5)
            self.play(FadeIn(tot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def logits(self):
        g = load("gpt2")
        toks = [t.strip() for t in g["top_tokens"]]
        logit = np.asarray(g["top_logits"])
        prob = np.asarray(g["top_probs"])
        assert toks[:3] == ["Paris", "London", "Amsterdam"] and abs(prob[0] - 0.064) < 0.0005
        prompt = Text(g["prompt"] + " …", font=MONO, font_size=28).to_edge(UP, buff=0.5)
        n = len(toks)
        xs = np.linspace(-4.6, 4.6, n)
        # the scores, relative to the best one: only differences matter to the softmax
        rel = logit - logit[0]
        bars_s, bars_p, labs = VGroup(), VGroup(), VGroup()
        for k in range(n):
            hs = 1.6 * (rel[k] + 1.5) / 1.5  # draw the score as a height above a floor 1.5 below the best
            bars_s.add(Rectangle(width=0.9, height=max(hs, 0.02), stroke_width=0, fill_color=C.MODEL_Q,
                                 fill_opacity=0.9).move_to([xs[k], -1.6 + hs / 2, 0]))
            hp = 30 * prob[k]
            bars_p.add(Rectangle(width=0.9, height=hp, stroke_width=0, fill_color=C.PROB, fill_opacity=0.9)
                       .move_to([xs[k], -1.6 + hp / 2, 0]))
            labs.add(Text(toks[k], font=MONO, font_size=24, color=C.TOKEN).move_to([xs[k], -2.0, 0]))
        sv = VGroup(*[MathTex(f"{v:.2f}", font_size=24, color=C.MODEL_Q).next_to(b, UP, buff=0.08)
                      for v, b in zip(logit, bars_s)])
        pv = VGroup(*[MathTex(f"{v:.3f}", font_size=24, color=C.PROB).next_to(b, UP, buff=0.08)
                      for v, b in zip(prob, bars_p)])
        f = cmath(r"z_k", "=", r"\mathbf{h}", r"\cdot", r"\mathbf{e}_k", colors={r"z_k": C.MODEL_Q, r"\mathbf{h}": C.BITS,
                                                                           r"\mathbf{e}_k": C.TRUE_P}, font_size=46)
        f.next_to(prompt, DOWN, buff=0.45)
        soft_f = cmath(r"q_k", "=", r"\frac{e^{z_k}}{\sum_j e^{z_j}}", colors={r"q_k": C.PROB}, font_size=46).move_to(f)
        recall = label(r"Part 1: \ scores $z_k$, \ then the softmax", font_size=26, color=GREY_A).next_to(soft_f, DOWN, buff=0.25)
        fh = label(r"$\mathbf{h}$: the model's final state; \ $\mathbf{e}_k$: token $k$'s own vector", font_size=26,
                   color=GREY_A).next_to(f, DOWN, buff=0.2)
        tie = label(r"the same $50{,}257$ vectors the tokens start as", font_size=26, color=C.TRUE_P).next_to(fh, DOWN, buff=0.12)
        soft = label(r"softmax: \ the probabilities", font_size=26, color=C.PROB).next_to(fh, DOWN, buff=0.12)
        floor = Line([-5.4, -1.6, 0], [5.4, -1.6, 0], color=GREY_D, stroke_width=1.5)
        with self.voiceover(
            "Here is why this matters. In part one, a network ended with a score for every possible next token, and "
            "the softmax turned the scores into probabilities. <bookmark mark='a'/> In GPT-2, every one of those "
            "scores is a dot product: the model's final state, dotted with each token's vector, the very same "
            "vectors the tokens started out as. <bookmark mark='b'/> After the Eiffel Tower is located in the city "
            "of, the biggest dot product belongs to Paris, then London, then Amsterdam. <bookmark mark='c'/> Only the "
            "differences matter: the softmax gives Paris 6.4 percent, the number we met in part one."
        ) as vo:
            self.play(FadeIn(prompt))
            self.play(Write(soft_f), FadeIn(recall))
            vo.wait_until("a")
            self.play(ReplacementTransform(soft_f, f), FadeOut(recall), FadeIn(fh))
            self.play(FadeIn(tie))
            vo.wait_until("b")
            self.play(Create(floor), FadeIn(labs), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_s], lag_ratio=0.15),
                      FadeIn(sv), run_time=1.6)
            vo.wait_until("c")
            self.play(ReplacementTransform(bars_s, bars_p), ReplacementTransform(sv, pv), ReplacementTransform(tie, soft),
                      run_time=1.6)
            self.play(Indicate(pv[0], color=WHITE, scale_factor=1.4))
        self.wait(0.5)
        self.clear_scene()
