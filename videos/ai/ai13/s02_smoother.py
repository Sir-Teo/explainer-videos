from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, HIST, K, PART, Q, V, curve, load, softmax_picture, softmax_stage


class Smoother(VoiceoverScene):
    def construct(self):
        self.card()
        self.smoother()
        self.formula()
        self.definition()
        self.geometry()

    def card(self):
        card = chapter_card(1, r"A weighted average", r"How do you guess a value from its neighbours?", part=PART,
                            lit=(1964, 2017))
        with self.voiceover("Chapter one. Attention is a weighted average."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def smoother(self):
        s = load("smoother")
        x, y, xs = np.asarray(s["x"]), np.asarray(s["y"]), np.asarray(s["xs"])
        hs = [float(h) for h in s["hs"]]
        h0 = hs[1]
        yhi = float(np.ceil(y.max() / 10) * 10)
        ax = Axes(x_range=[0, len(x), 25], y_range=[0, yhi, 10], x_length=10.6, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([0, 0.75, 0])
        xl = label(r"page of \textit{Great Expectations}", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        yl = label(r"``her'' per $1{,}000$ words \ (Part 7)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.1)
        yl.align_to(ax, LEFT)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=V) for a, b in zip(x, y)])
        # the weights, on a strip of their own under the plot
        wax = Axes(x_range=[0, len(x), 25], y_range=[0, 1, 1], x_length=10.6, y_length=1.3, tips=False,
                   axis_config={"stroke_color": GREY_D, "include_ticks": False}).move_to([0, -2.55, 0])
        wl = label(r"weights", font_size=22, color=A).next_to(wax, LEFT, buff=0.15)
        qv, hv = ValueTracker(float(s["q"])), ValueTracker(h0)

        def weights():
            sc = -0.5 * (qv.get_value() - x) ** 2 / hv.get_value() ** 2
            w = np.exp(sc - sc.max())
            return w / w.sum()

        def wbars():
            w = weights()
            top = max(w.max(), 1e-9)
            return VGroup(*[Line(wax.c2p(a, 0), wax.c2p(a, 0.95 * b / top), color=A, stroke_width=3)
                            for a, b in zip(x, w) if b > 1e-3 * top])

        def qline():
            return DashedLine(wax.c2p(qv.get_value(), 0), ax.c2p(qv.get_value(), yhi), color=Q, stroke_width=2,
                              dash_length=0.08)

        def est():
            return glow_dot(ax.c2p(qv.get_value(), float(weights() @ y)), color=Q, radius=0.09)

        def lit_dots():
            w = weights()
            top = max(w.max(), 1e-9)
            return VGroup(*[Dot(ax.c2p(a, b), radius=0.045 + 0.05 * c / top, color=V).set_opacity(0.25 + 0.75 * c / top)
                            for a, b, c in zip(x, y, w) if c > 0.02 * top])

        bars, ql, ed, lit = always_redraw(wbars), always_redraw(qline), always_redraw(est), always_redraw(lit_dots)
        fit = curve(ax, xs, np.asarray(s[f"fit{h0:g}"]), Q, 3.5, smooth=True)
        ql_lab = MathTex(r"q", font_size=30, color=Q)
        ql_lab.add_updater(lambda m: m.next_to(ax.c2p(qv.get_value(), yhi), UP, buff=0.05))
        cite_ = cite(r"E.~A.~Nadaraya (1964); \ G.~S.~Watson (1964)", corner=DR)
        with self.voiceover(
            "Here is Part 7's data again: how often each page of Great Expectations says 'her'. Suppose you want a "
            "smooth guess for page one hundred and twenty. <bookmark mark='a'/> Take a weighted average of every "
            "page, weighting each by how close it is: a bump of weights, centered on the page you're asking about. "
            "<bookmark mark='b'/> Pages near the query count a lot, far ones not at all. The weights are positive "
            "and add up to one. <bookmark mark='c'/> Slide the query along, and the average traces a smooth curve. "
            "This is Nadaraya and Watson's kernel smoother, from 1964."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.005),
                      run_time=2.0)
            vo.wait_until("a")
            sb, sq = wbars(), qline()  # still pictures first; the live versions take over once they're on screen
            self.play(Create(wax), FadeIn(wl), FadeIn(sq), FadeIn(ql_lab), FadeIn(sb))
            self.remove(sb, sq)
            self.add(bars, ql)
            vo.wait_until("b")
            sl, se = lit_dots(), est()
            self.play(FadeIn(sl), dots.animate.set_opacity(0.25), FadeIn(se))
            self.remove(sl, se)
            self.add(lit, ed)
            vo.wait_until("c")
            self.play(FadeIn(cite_))
            self.play(qv.animate.set_value(3.0), run_time=1.5)
            trace = TracedPath(lambda: ax.c2p(qv.get_value(), float(weights() @ y)), stroke_color=Q, stroke_width=3.5)
            self.add(trace)
            self.play(qv.animate.set_value(len(x) - 3.0), run_time=6.0, rate_func=linear)
            self.remove(trace)
            self.add(fit)
        # the one knob: the width of the bump
        hl = label(rf"bump width: \ ${h0:g}$ pages", font_size=26, color=A).to_corner(UR, buff=0.35)
        fits = {h: curve(ax, xs, np.asarray(s[f"fit{h:g}"]), Q, 3.5, smooth=True) for h in hs}
        with self.voiceover(
            "The only knob is the width of the bump. <bookmark mark='a'/> Too narrow, and the curve chases every "
            "page's noise. <bookmark mark='b'/> Too wide, and it flattens the whole story into one number."
        ) as vo:
            self.play(qv.animate.set_value(float(s["q"])), FadeIn(hl), run_time=1.5)
            vo.wait_until("a")
            hl2 = label(rf"bump width: \ ${hs[0]:g}$ pages", font_size=26, color=A).move_to(hl)
            self.play(hv.animate.set_value(hs[0]), Transform(fit, fits[hs[0]]), Transform(hl, hl2), run_time=1.5)
            vo.wait_until("b")
            hl3 = label(rf"bump width: \ ${hs[2]:g}$ pages", font_size=26, color=A).move_to(hl)
            self.play(hv.animate.set_value(hs[2]), Transform(fit, fits[hs[2]]), Transform(hl, hl3), run_time=1.5)
        self.wait(0.3)
        for m in (bars, ql, ed, lit):
            m.clear_updaters()
        ql_lab.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def formula(self):
        colors = {r"q": Q, r"x_i": K, r"y_i": V, r"\mathrm{softmax}_i": A, r"k_i": K, r"v_i": V}
        f1 = cmath(r"\hat y(", r"q", r")", "=", r"\sum_i", r"\mathrm{softmax}_i", r"\Big(", r"-\tfrac{(", r"q",
                   r"-", r"x_i", r")^2}{2h^2}", r"\Big)", r"\,", r"y_i", colors=colors, font_size=48).move_to(UP * 1.9)
        f2 = cmath(r"\mathrm{out}(", r"q", r")", "=", r"\sum_i", r"\mathrm{softmax}_i", r"\Big(", r"\tfrac{", r"q",
                   r"\cdot", r"k_i", r"}{\sqrt{d}}", r"\Big)", r"\,", r"v_i", colors=colors, font_size=48).move_to(UP * 1.9)
        sm = cmath(r"\mathrm{softmax}_i(s)", "=", r"\frac{e^{s_i}}{\sum_j e^{s_j}}", font_size=36,
                   colors={r"\mathrm{softmax}_i(s)": A}).next_to(f1, DOWN, buff=0.45)
        sml = label(r"positive weights that add up to one", font_size=24, color=GREY_A).next_to(sm, DOWN, buff=0.15)
        roles = VGroup(
            VGroup(MathTex(r"q", font_size=40, color=Q), label(r"the query: \ what am I looking for?", font_size=26, color=Q)),
            VGroup(MathTex(r"k_i", font_size=40, color=K), label(r"the keys: \ what does each one offer?", font_size=26, color=K)),
            VGroup(MathTex(r"v_i", font_size=40, color=V), label(r"the values: \ what each one passes on", font_size=26, color=V)),
        )
        for r_ in roles:
            r_.arrange(RIGHT, buff=0.3)
        roles.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 1.2)
        proj = cmath(r"q = W_Q\, x, \quad k = W_K\, x, \quad v = W_V\, x", font_size=36).to_edge(DOWN, buff=0.5)
        pl = label(r"three learned matrices, applied to every character's vector", font_size=24, color=GREY_A)
        pl.next_to(proj, UP, buff=0.15)
        cite_ = cite(r"A.~Vaswani et al., \textit{Attention Is All You Need} (2017)", corner=UR)
        smc = gloss(r"softmax", r"make every score positive with $e^{\,s}$, \\ then divide by their total",
                    softmax_picture(), width=5.0, color=A).move_to([0, -2.0, 0])
        smp = smc[1][-1]
        with self.voiceover(
            "Write it down. The guess at the query is a sum over the pages: each page's value, times a weight. The "
            "weight is a softmax of a score: the exponential of the score, divided by the total, so the weights are "
            "positive and add up to one. Here the score is minus the squared distance. <bookmark mark='a'/> Now "
            "change one thing. Instead of a distance between page numbers, score each item by a dot product between "
            "two vectors: a query and a key. <bookmark mark='b'/> That's attention, the heart of the transformer. "
            "The query asks what am I looking for; each key says what it offers; each value is what it passes on. "
            "<bookmark mark='c'/> And all three are computed from the characters by matrices the network learns. "
            "Attention is a kernel smoother whose kernel is learned."
        ) as vo:
            self.play(Write(f1), run_time=2.0)
            self.play(FadeIn(sm), FadeIn(sml), FadeIn(smc, shift=UP * 0.2))
            self.wait(1.5)  # until the narration reaches the softmax
            for k_ in (1, 2):  # the scores, then their exponentials, then those over their total
                b_, c_ = softmax_stage(smp, k_)
                self.play(Transform(smp[1], b_), Transform(smp[2], c_), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeOut(sm), FadeOut(sml), FadeOut(smc))
            morph(self, f1, f2, run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cite_), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in roles], lag_ratio=0.5),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(Write(proj), FadeIn(pl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def definition(self):
        colors = {r"q": Q, r"k_i": K, r"k_j": K, r"v_i": V}
        f = cmath(r"\mathrm{Attn}(", r"q", r")", r"=", r"\sum_i", r"\frac{e^{\,", r"q", r"\cdot", r"k_i",
                  r"/\sqrt{d}}}{\sum_j e^{\,", r"q", r"\cdot", r"k_j", r"/\sqrt{d}}}", r"\,", r"v_i",
                  colors=colors, font_size=40)
        words = label(r"score the keys against the query, \\ \ softmax the scores, \ average the values",
                      font_size=26, color=GREY_A)
        card = definition_card(r"Attention", VGroup(f, words).arrange(DOWN, buff=0.35, aligned_edge=LEFT),
                               color=A, width=8.6, font_size=28).move_to([0, 0.4, 0])
        # the same weights, drawn: a query, five keys, their weights, the average
        wv = np.array([0.08, 0.46, 0.21, 0.05, 0.20])
        demo = VGroup(*[VGroup(Rectangle(width=0.42, height=max(1.5 * v, 0.02), stroke_width=0, fill_color=A,
                                         fill_opacity=0.9), MathTex(rf"v_{i + 1}", font_size=24, color=V))
                        for i, v in enumerate(wv)])
        for b_ in demo:
            b_[1].next_to(b_[0], DOWN, buff=0.1)
        demo.arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        demo_l = label(r"weights \ (illustrative)", font_size=20, color=GREY_B).next_to(demo, LEFT, buff=0.3)
        demo_g = VGroup(demo, demo_l).move_to([0, -2.6, 0])
        hist = history_card(2014, r"D.~Bahdanau, K.~Cho \& Y.~Bengio",
                            r"a translation network looks back at the source sentence (Part 10); \ "
                            r"in 2017 attention becomes the whole network", color=HIST, width=5.0)
        hist.move_to([4.3, 0.9, 0])
        quiz = pause_card(r"If every key is the same, \ what does attention return?", width=6.4)
        quiz.move_to([-3.0, -2.45, 0])
        ans = label(r"every weight is $1/n$: \ the plain average of the values", font_size=26, color=V)
        ans.move_to([3.6, -2.45, 0])
        with self.voiceover(
            "Here is the definition for the rest of this part. <bookmark mark='a'/> Attention scores each key against "
            "the query with a dot product divided by the square root of d, turns the scores into weights with a "
            "softmax, and returns the weighted average of the values. <bookmark mark='b'/> It entered neural "
            "networks in 2014, when Dzmitry Bahdanau, Kyunghyun Cho and Yoshua Bengio let a translation network "
            "look back at its source sentence, as in Part 10; in 2017 it became the whole network. "
            "<bookmark mark='c'/> A question: if every key is the same, what does attention return? "
            "<bookmark mark='d'/> Every weight is one over n: the plain average of the values. Attention can only "
            "weigh and blend what it is given."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_[0], DOWN) for b_ in demo], lag_ratio=0.15), FadeIn(demo_l),
                      FadeIn(VGroup(*[b_[1] for b_ in demo])))
            self.play(Indicate(f, color=A, scale_factor=1.04))
            vo.wait_until("b")
            self.play(FadeOut(demo_g), card.animate.scale(0.82).move_to([-2.6, 0.9, 0]))
            self.play(FadeIn(hist, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(quiz, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(ans, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def geometry(self):
        plane = NumberPlane(x_range=[-3.2, 3.2, 1], y_range=[-3.2, 3.2, 1], x_length=6.2, y_length=6.2,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.5},
                            axis_config={"stroke_color": GREY_C}).move_to([-3.2, -0.35, 0])
        keys = np.array([[2.4, 0.5], [1.2, 1.9], [-0.6, 2.2], [-2.1, 0.4], [-1.0, -1.9], [1.6, -1.6]])
        names = ["a", "b", "c", "d", "e", "f"]
        karrows = VGroup(*[Arrow(plane.c2p(0, 0), plane.c2p(*k), buff=0, color=K, stroke_width=4,
                                 max_tip_length_to_length_ratio=0.12) for k in keys])
        klabs = VGroup(*[MathTex(rf"k_{n}", font_size=30, color=K).next_to(plane.c2p(*k), normalize([*k, 0]), buff=0.1)
                         for n, k in zip(names, keys)])
        ang = ValueTracker(0.3)
        qlen = 1.6

        def qvec():
            return np.array([math.cos(ang.get_value()), math.sin(ang.get_value())]) * qlen

        qarrow = always_redraw(lambda: Arrow(plane.c2p(0, 0), plane.c2p(*qvec()), buff=0, color=Q, stroke_width=6,
                                             max_tip_length_to_length_ratio=0.15))
        qlab = always_redraw(lambda: MathTex(r"q", font_size=34, color=Q).next_to(plane.c2p(*qvec()),
                                                                                    normalize([*qvec(), 0]), buff=0.1))
        # live softmax weights
        bx, by, bw, bh = 2.2, -2.3, 0.62, 3.6

        def wts():
            s = keys @ qvec()
            e = np.exp(s - s.max())
            return e / e.sum()

        def bars():
            w = wts()
            g = VGroup()
            for i, (n, v) in enumerate(zip(names, w)):
                r = Rectangle(width=bw * 0.8, height=max(bh * v, 0.01), stroke_width=0, fill_color=A, fill_opacity=0.9)
                r.move_to([bx + i * bw, by + bh * v / 2, 0])
                g.add(r)
            return g

        wb = always_redraw(bars)
        wlabs = VGroup(*[MathTex(n, font_size=28, color=K).move_to([bx + i * bw, by - 0.25, 0]) for i, n in enumerate(names)])
        base = Line([bx - bw / 2, by, 0], [bx + 5.5 * bw, by, 0], color=GREY_C, stroke_width=2)
        wt = label(r"softmax of $q \cdot k_i$", font_size=26, color=A).next_to(base, UP, buff=bh + 0.25)
        wt.set_x(bx + 2.5 * bw)
        dotf = cmath(r"q \cdot k", "=", r"|q|\,|k|\cos\theta", font_size=34).to_corner(UR, buff=0.35)
        dl = label(r"long keys pointing the query's way win", font_size=24, color=GREY_A).next_to(dotf, DOWN, buff=0.15)
        dl.align_to(dotf, RIGHT)
        tag = note(r"illustrative vectors, \ in 2 of a head's 32 dimensions").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Here's the geometry. Every key is an arrow; so is the query. <bookmark mark='a'/> The score of a key is "
            "its dot product with the query: how long both are, times how much they point the same way. The softmax "
            "turns the scores into weights. <bookmark mark='b'/> Turn the query, and the weights flow from key to "
            "key. A query is a direction to look in. Next, the same formula read another way: as a memory that "
            "recalls what it stored."
        ) as vo:
            self.play(Create(plane), FadeIn(tag))
            self.play(LaggedStart(*[GrowArrow(a) for a in karrows], lag_ratio=0.15), FadeIn(klabs), run_time=1.5)
            self.play(GrowArrow(qarrow), FadeIn(qlab))
            self.add(qarrow, qlab)
            vo.wait_until("a")
            self.play(Write(dotf), FadeIn(dl), Create(base), FadeIn(wlabs), FadeIn(wt), FadeIn(wb))
            vo.wait_until("b")
            self.play(ang.animate.set_value(0.3 + 2 * PI), run_time=7.0, rate_func=smooth)
        self.wait(0.3)
        for m in (qarrow, qlab, wb):
            m.clear_updaters()
        self.clear_scene()
