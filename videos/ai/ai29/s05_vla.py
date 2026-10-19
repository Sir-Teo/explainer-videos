from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403


class VLA(VoiceoverScene):
    def construct(self):
        self.card()
        self.pipeline()
        self.chunks()
        self.exact()

    def card(self):
        card = chapter_card(4, r"Acting in the physical world", r"How does a language model move a robot arm?", part=29)
        with self.voiceover("Chapter four. Acting in the physical world."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pipeline(self):
        cam = VGroup(*[Square(0.3, stroke_color=C.BITS, stroke_width=1.2, fill_color=C.BITS, fill_opacity=0.25) for _ in range(9)])
        cam.arrange_in_grid(rows=3, cols=3, buff=0.04).move_to([-5.2, 1.0, 0])
        cl = label(r"camera images", font_size=20, color=C.BITS).next_to(cam, DOWN, buff=0.12)
        txt = VGroup(*[Square(0.3, stroke_color=C.TRUE_P, stroke_width=1.2, fill_color=C.TRUE_P, fill_opacity=0.25) for _ in range(5)])
        txt.arrange(RIGHT, buff=0.04).move_to([-5.0, -1.0, 0])
        tl = label(r"``fold the towel''", font_size=20, color=C.TRUE_P).next_to(txt, DOWN, buff=0.12)
        vlm = RoundedRectangle(width=3.0, height=2.4, corner_radius=0.2, stroke_color=WHITE, stroke_width=2.5).move_to([-0.8, 0, 0])
        vl = label(r"a vision-language model \\ (pretrained on the web)", font_size=22, color=WHITE).move_to(vlm)
        act = RoundedRectangle(width=2.4, height=1.4, corner_radius=0.2, stroke_color=C.INTERVAL, stroke_width=2.5).move_to([3.0, 0, 0])
        al = label(r"an action expert: \\ flow matching \\ (Part 21)", font_size=22, color=C.INTERVAL).move_to(act)
        arm = VGroup(Line([5.0, -1.2, 0], [5.4, 0.2, 0], color=GREY_A, stroke_width=6), Line([5.4, 0.2, 0], [6.2, 0.6, 0], color=GREY_A,
                                                                                                  stroke_width=6),
                     Dot([5.4, 0.2, 0], radius=0.08, color=GREY_B), Dot([6.2, 0.6, 0], radius=0.1, color=C.INTERVAL))
        arrows = VGroup(Arrow(cam.get_right(), vlm.get_left() + UP * 0.5, buff=0.1, color=GREY_B),
                        Arrow(txt.get_right(), vlm.get_left() + DOWN * 0.5, buff=0.1, color=GREY_B),
                        Arrow(vlm.get_right(), act.get_left(), buff=0.1, color=GREY_B),
                        Arrow(act.get_right(), arm[0].get_start() + UP * 0.6 + LEFT * 0.2, buff=0.1, color=GREY_B))
        # RT-2's way: actions written as tokens, like words
        toks = VGroup(*[VGroup(RoundedRectangle(width=0.62, height=0.42, corner_radius=0.06, stroke_color=GREY_B, stroke_width=1.5),
                               Text(v, font="DejaVu Sans Mono", font_size=16, color=GREY_A)) for v in ("132", "87", "201", "64")])
        for t_ in toks:
            t_[1].move_to(t_[0])
        toks.arrange(RIGHT, buff=0.08).move_to([3.0, 0, 0])
        tkl = label(r"actions as tokens, \ like words \ (RT-2)", font_size=20, color=GREY_B).next_to(toks, DOWN, buff=0.2)
        ta = Arrow(vlm.get_right(), toks.get_left(), buff=0.1, color=GREY_B)
        # pi-zero's way: flow matching turns noise into a smooth stretch of motion
        xs = np.linspace(1.9, 4.1, 24)
        g = np.random.default_rng(18)
        y0 = -1.85 + 0.45 * g.standard_normal(len(xs))
        y1 = -1.85 + 0.35 * np.sin((xs - 1.9) * 2.6)
        noisy = VGroup(*[Dot([x, y, 0], radius=0.045, color=C.INTERVAL) for x, y in zip(xs, y0)])
        smooth = VGroup(*[Dot([x, y, 0], radius=0.045, color=C.INTERVAL) for x, y in zip(xs, y1)])
        path = VMobject(color=C.INTERVAL, stroke_width=3).set_points_smoothly([[x, y, 0] for x, y in zip(xs, y1)])
        fml = label(r"noise $\to$ a smooth motion", font_size=20, color=C.INTERVAL).next_to(smooth, DOWN, buff=0.35)
        cite_ = cite(r"A.~Brohan et al., \textit{RT-2} (2023); \ K.~Black et al., \textit{$\pi_0$} (2024)", corner=DR)
        tag = note(r"schematic").to_corner(DL, buff=0.3)
        ae = gloss(r"action expert", r"a small extra network on the vision-language model, \\ whose only job is smooth arm motion \\ "
                   r"(not Part 16's mixture-of-experts experts)", corner=UR, width=5.6, color=C.INTERVAL)
        with self.voiceover(
            "Robots are where agents meet physics. A vision-language-action model starts from a model that already "
            "reads images and text, trained on the web. <bookmark mark='a'/> Give it camera images and an "
            "instruction, and add a way to output motion. <bookmark mark='r'/> RT-2, in 2023, wrote actions as "
            "tokens, like words. <bookmark mark='b'/> Pi-zero, in 2024, added an action expert: a small extra network "
            "attached to the vision-language model, whose only job is to output smooth arm motions. It's not one of "
            "part sixteen's mixture-of-experts experts. It generates those motions by flow matching, part twenty-one's "
            "machinery, now drawing trajectories instead of pictures."
        ) as vo:
            self.play(Create(vlm), FadeIn(vl), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(cam, shift=RIGHT * 0.2), FadeIn(cl), FadeIn(txt, shift=RIGHT * 0.2), FadeIn(tl))
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), Indicate(vlm, color=WHITE, scale_factor=1.03))
            vo.wait_until("r")
            self.play(GrowArrow(ta), LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.15) for t_ in toks], lag_ratio=0.2), FadeIn(tkl))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(toks, tkl, ta)), GrowArrow(arrows[2]), Create(act), FadeIn(al))
            self.play(FadeIn(ae))
            self.play(FadeIn(noisy, lag_ratio=0.05), FadeIn(fml))
            self.play(Transform(noisy, smooth), run_time=1.5)
            self.play(Create(path), GrowArrow(arrows[3]), FadeIn(arm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chunks(self):
        ax = Axes(x_range=[0, 50, 10], y_range=[-1.2, 1.2, 1], x_length=10.0, y_length=2.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(DOWN * 2.0)

        def f(t):
            return 0.8 * np.sin(t / 7) * np.cos(t / 13)

        segs = VGroup(*[VMobject(color=C.INTERVAL, stroke_width=4).set_points_smoothly(
            [ax.c2p(t, f(t)) for t in np.linspace(10 * i, 10 * (i + 1), 60)]) for i in range(5)])
        bands = VGroup(*[Rectangle(width=10.0 / 5 * 0.98, height=2.2, stroke_color=GREY_D, stroke_width=1, fill_color=C.INTERVAL,
                                   fill_opacity=0.05).move_to(ax.c2p(5 + 10 * i, 0)) for i in range(5)])
        bl = VGroup(*[label(rf"chunk {i + 1}", font_size=20, color=GREY_B).next_to(b, UP, buff=0.08) for i, b in enumerate(bands)])
        head = label(r"action chunks: \ the model plans a short stretch of motion at once, \\ then looks again", font_size=26)
        head.to_edge(UP, buff=0.3)
        xn = label(r"time $\to$ \ (the elbow's angle)", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        tag = note(r"illustrative trajectory").to_corner(DR, buff=0.3)
        # a two-link arm whose elbow follows the planned trajectory
        tt = ValueTracker(0.0)
        base = np.array([-0.8, -0.2, 0])

        def arm():
            t = tt.get_value()
            a1 = 1.15 + 0.35 * f(t)
            a2 = a1 - 1.1 + 1.1 * f(t)
            p1 = base + 1.5 * np.array([np.cos(a1), np.sin(a1), 0])
            p2 = p1 + 1.3 * np.array([np.cos(a2), np.sin(a2), 0])
            return VGroup(Line(base, p1, color=GREY_A, stroke_width=8), Line(p1, p2, color=GREY_A, stroke_width=7),
                          Dot(base, radius=0.1, color=GREY_B), Dot(p1, radius=0.08, color=C.INTERVAL), Dot(p2, radius=0.11, color=WHITE))

        plinth = Rectangle(width=1.2, height=0.2, stroke_width=0, fill_color=GREY_D, fill_opacity=1).next_to(base, DOWN, buff=0.08)
        live = always_redraw(arm)
        cursor = always_redraw(lambda: Line(ax.c2p(tt.get_value(), -1.2), ax.c2p(tt.get_value(), 1.2), color=WHITE, stroke_width=2))
        dot = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), f(tt.get_value())), radius=0.07, color=WHITE))
        look = label(r"look", font_size=24, color=C.BITS).move_to([3.2, 0.6, 0])
        plan = label(r"plan a chunk", font_size=24, color=C.INTERVAL).move_to([3.2, 0.6, 0])
        act = label(r"act", font_size=24, color=WHITE).move_to([3.2, 0.6, 0])

        def chunk(i):
            self.play(FadeIn(look, scale=1.2), bands[i].animate.set_fill(opacity=0.18), run_time=0.3)
            self.play(FadeOut(look), FadeIn(plan), Create(segs[i]), run_time=0.5)
            self.play(FadeOut(plan), FadeIn(act), tt.animate.set_value(10 * (i + 1)), run_time=1.0, rate_func=linear)
            self.play(FadeOut(act), bands[i].animate.set_fill(opacity=0.05), run_time=0.2)

        with self.voiceover(
            "And it doesn't act one tiny step at a time. It plans a chunk of motion, a second or so, then looks at "
            "the world again and plans the next: <bookmark mark='a'/> the belief and the world model of the earlier "
            "chapters, folded into one network that sees, thinks and moves."
        ) as vo:
            still = arm()  # fade in a still copy; the live arm (rebuilt every frame) can't be faded in
            self.play(FadeIn(head), Create(ax), FadeIn(xn), FadeIn(tag), FadeIn(bands), FadeIn(bl), FadeIn(plinth), FadeIn(still))
            self.remove(still)
            self.add(live, cursor, dot)
            for i in range(3):
                chunk(i)
            vo.wait_until("a")
            for i in range(3, 5):
                chunk(i)
        live.clear_updaters()
        cursor.clear_updaters()
        dot.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exact(self):
        """The two ways to write actions, exactly: pi-zero's flow-matched chunks, and FAST's compressed tokens."""
        from scipy.fft import dct, idct

        H = 50
        t = np.linspace(0, 1, H)
        a = 0.6 * np.sin(2.2 * t + 0.3) + 0.25 * t ** 2 + 0.08 * np.sin(9 * t)  # an illustrative joint angle over one chunk
        c = dct(a, norm="ortho")
        gam = 10.0
        q = np.round(gam * c)
        rec = idct(q / gam, norm="ortho")
        nz = int((q != 0).sum())
        err = float(np.abs(rec - a).max())
        colors = {r"A": C.INTERVAL, r"\varepsilon": C.TRUE_P, r"v_\theta": C.BITS}
        f1 = cmath(r"A", r"= (a_t, \ldots, a_{t+H-1}), \quad", r"A", r"^{\tau} = (1 - \tau)\,", r"\varepsilon", r"+ \tau\,", r"A",
                   colors=colors, font_size=30)
        f2 = cmath(r"\mathcal{L} = \big\|", r"v_\theta", r"(", r"A", r"^{\tau}, o_t) - (", r"A", r"-", r"\varepsilon", r")\big\|^2",
                   colors=colors, font_size=30)
        top = VGroup(f1, f2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_corner(UL, buff=0.5)
        tl = label(r"$\pi_0$: \ a chunk of $H = 50$ actions \ ($1$ s at $50$ Hz), \ flow-matched given the observation $o_t$; "
                   r"\ $10$ steps to draw", font_size=18, color=C.INTERVAL).next_to(top, DOWN, buff=0.12).align_to(top, LEFT)
        keep_in_frame(tl)
        # the flow-matching path on this chunk: noise at tau = 0, the chunk at tau = 1
        eps = np.clip(np.random.default_rng(3).normal(0, 0.45, H), -1, 1)
        px = CornerAxes(x_range=[0, H, 10], y_range=[-1, 1, 0.5], x_length=3.6, y_length=1.7, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.2, 2.0, 0])
        tau = ValueTracker(0.0)

        def mix():
            v = (1 - tau.get_value()) * eps + tau.get_value() * a
            return VGroup(VMobject(color=C.INTERVAL, stroke_width=2, stroke_opacity=0.5).set_points_as_corners(
                [px.c2p(i, x) for i, x in enumerate(v)]), *[Dot(px.c2p(i, x), radius=0.025, color=C.INTERVAL) for i, x in enumerate(v)])

        path = always_redraw(mix)
        pl = always_redraw(lambda: MathTex(rf"A^{{\tau}}, \ \tau = {tau.get_value():.2f}", font_size=24, color=C.INTERVAL)
                           .next_to(px, UP, buff=0.08))
        # FAST on one chunk, computed here
        ax = CornerAxes(x_range=[0, H, 10], y_range=[-1, 1, 0.5], x_length=4.4, y_length=2.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-4.2, -1.3, 0])
        sig = VMobject(color=C.INTERVAL, stroke_width=3).set_points_smoothly([ax.c2p(i, v) for i, v in enumerate(a)])
        rs = VMobject(color=C.BITS, stroke_width=2).set_points_smoothly([ax.c2p(i, v) for i, v in enumerate(rec)])
        al = label(r"one joint over one chunk \ (illustrative)", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
        bx = CornerAxes(x_range=[0, H, 10], y_range=[0, float(np.abs(c).max()) * 1.1, 1], x_length=4.4, y_length=2.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([0.7, -1.3, 0])
        bars = VGroup(*[Line(bx.c2p(i + 0.5, 0), bx.c2p(i + 0.5, abs(float(v))), stroke_width=4,
                             color=C.BITS if q[i] != 0 else GREY_D) for i, v in enumerate(c)])
        bl = label(r"its cosine transform: \ smooth motion \\ lives in the first few numbers", font_size=18, color=GREY_A).next_to(bx, UP, buff=0.1)
        toks = MathTex(r"\text{tokens} = \operatorname{BPE}\big(\operatorname{round}(\gamma \cdot \operatorname{DCT}(a))\big)",
                       font_size=28, color=C.BITS).move_to([4.6, -0.6, 0])
        tk = label(rf"$\gamma = {gam:.0f}$: \ ${nz}$ of ${H}$ numbers \\ survive the rounding; \ rebuilt to ${err:.3f}$; \\ "
                   r"byte-pair encoding packs \\ the zeros and repeats", font_size=18, color=GREY_A).next_to(toks, DOWN, buff=0.2)
        keep_in_frame(VGroup(toks, tk))
        # any smooth motion is a sum of cosine waves, slow ones first: the first 1, 2, 3, 7 of them, added up
        def partial(k):
            ck = c.copy()
            ck[k:] = 0
            return VMobject(color=WHITE, stroke_width=2.5).set_points_smoothly([ax.c2p(i, v) for i, v in enumerate(idct(ck, norm="ortho"))])

        ks_ = (1, 2, 3, 7)
        kl_ = [label(t_, font_size=18, color=WHITE).next_to(ax, DOWN, buff=0.15) for t_ in (
            r"the slowest cosine wave", r"the first $2$ cosine waves, \ added up", r"the first $3$ cosine waves, \ added up",
            r"the first $7$ cosine waves, \ added up")]
        cite_ = cite(r"K.~Black et al., \textit{$\pi_0$} (2024); \ K.~Pertsch et al., \textit{FAST} (2025)", corner=DR)
        with self.voiceover(
            "Here are the two answers, exactly. <bookmark mark='a'/> Physical Intelligence's pi zero predicts a whole "
            "chunk of fifty actions, one second of motion, by part twenty-one's flow matching: mix the true chunk with "
            "noise, and train the action expert to predict the straight-line velocity between them, given what the "
            "robot sees. Ten steps draw a chunk. <bookmark mark='b'/> The other answer turns actions into tokens a "
            "language model can write. Taking every time step as a token works badly: neighbouring steps are nearly "
            "the same, so each token says almost nothing. <bookmark mark='c'/> FAST compresses first, with a cosine "
            "transform. <bookmark mark='k'/> Any smooth motion is a sum of cosine waves, slow ones first; the "
            "transform lists how much of each wave you need, and a smooth motion needs only the first few. "
            "<bookmark mark='d'/> Round those amounts, and on "
            f"this chunk only {nz} of {H} survive, yet they rebuild the motion to within {err:.3f}; byte-pair encoding, "
            "from part twenty-three, then packs what's left into a handful of tokens."
        ) as vo:
            self.play(FadeIn(cite_), Write(f1), Create(px), run_time=1.5)
            self.add(path, pl)  # the chunk's noise, at tau = 0, from the first words
            vo.wait_until("a")
            self.play(Write(f2), FadeIn(tl), run_time=1.5)
            self.play(tau.animate.set_value(1.0), run_time=4.0, rate_func=smooth)
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(al), Create(sig))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bl), LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.02), run_time=1.5)
            vo.wait_until("k")
            ps_ = partial(ks_[0])
            self.play(sig.animate.set_stroke(opacity=0.35), Create(ps_), FadeIn(kl_[0]), bars[0].animate.set_color(WHITE))
            for j in range(1, len(ks_)):
                self.play(Transform(ps_, partial(ks_[j])), FadeTransform(kl_[j - 1], kl_[j]),
                          *[b_.animate.set_color(WHITE) for b_ in bars[ks_[j - 1]:ks_[j]]], run_time=1.0)
            vo.wait_until("d")
            self.play(FadeOut(ps_), FadeOut(kl_[-1]), sig.animate.set_stroke(opacity=1),
                      *[b_.animate.set_color(C.BITS if q[i] != 0 else GREY_D) for i, b_ in enumerate(bars[:ks_[-1]])], run_time=0.5)
            self.play(Write(toks), FadeIn(tk), Create(rs))
        self.wait(0.3)
        self.clear_scene()
