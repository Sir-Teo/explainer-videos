from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import IMG_C, TEXT_C, gray_image, heat, load


class Clip(VoiceoverScene):
    def construct(self):
        self.card()
        self.pairs()
        self.learning()
        self.losses()

    def card(self):
        card = chapter_card(4, r"Matching senses", r"How do pictures and words meet?", part=23)
        with self.voiceover("Chapter four. Matching senses."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pairs(self):
        c = load("clip")
        imgs, caps = np.asarray(c["batch_imgs"]), [str(x) for x in c["batch_caps"]]
        sim = np.asarray(c["sim_clip"])
        n = len(caps)
        S = 4.6
        grid = heat(sim, S, S, signed=True).move_to([1.6, -0.5, 0])
        frame = SurroundingRectangle(grid, buff=0, color=GREY_D, stroke_width=1.5)
        cell = S / n
        pics = Group(*[gray_image(im, cell * 0.92).move_to([grid.get_left()[0] - 0.35, grid.get_top()[1] - cell * (i + 0.5), 0])
                       for i, im in enumerate(imgs)])
        words = VGroup(*[Text(cp, font="DejaVu Sans Mono", font_size=14, color=TEXT_C).rotate(PI / 3)
                         .move_to([grid.get_left()[0] + cell * (i + 0.5), grid.get_top()[1] + 0.55, 0]) for i, cp in enumerate(caps)])
        diag = VGroup(*[Square(cell, stroke_color=WHITE, stroke_width=1.5).move_to(
            [grid.get_left()[0] + cell * (i + 0.5), grid.get_top()[1] - cell * (i + 0.5), 0]) for i in range(n)])
        # two encoders, one vector each, and their dot product
        g = np.random.default_rng(16)
        u = g.uniform(0.15, 1, 6)
        w = np.clip(u + g.normal(0, 0.12, 6), 0.1, 1)

        def vec(vals, col):
            return VGroup(*[Square(0.2, stroke_width=1, stroke_color=col, fill_color=col, fill_opacity=float(x)) for x in vals]).arrange(
                RIGHT, buff=0.03)

        def box(text, col):
            b_ = RoundedRectangle(width=1.5, height=0.55, corner_radius=0.1, stroke_color=col, stroke_width=2)
            return VGroup(b_, label(text, font_size=18, color=col).move_to(b_))

        p_in = gray_image(imgs[0], 0.8).move_to([-6.1, 2.3, 0])
        c_in = Text(caps[0], font="DejaVu Sans Mono", font_size=16, color=TEXT_C).move_to([-6.0, 0.9, 0])
        e1, e2 = box(r"picture encoder", IMG_C).move_to([-4.3, 2.3, 0]), box(r"caption encoder", TEXT_C).move_to([-4.3, 0.9, 0])
        v1, v2 = vec(u, IMG_C).move_to([-2.3, 2.3, 0]), vec(w, TEXT_C).move_to([-2.3, 0.9, 0])
        arr = VGroup(*[Arrow(a_.get_right(), b_.get_left(), buff=0.1, stroke_width=2.5, color=GREY_B, max_tip_length_to_length_ratio=0.25)
                       for a_, b_ in ((p_in, e1), (c_in, e2), (e1, v1), (e2, v2))])
        dot_ = MathTex(r"\cdot", font_size=48, color=WHITE).move_to([-2.3, 1.6, 0])
        sc = label(rf"score $= u \cdot v = {float(u @ w):.2f}$", font_size=22, color=GREY_A).move_to([-3.6, 0.1, 0])
        enc = Group(p_in, c_in, e1, e2, v1, v2, arr, dot_, sc)
        tag = label(r"blue: \ high score; \ red: \ low", font_size=20, color=GREY_B).next_to(grid, DOWN, buff=0.2)
        cite_ = cite(r"A.~Radford et al., \textit{CLIP} (2021)", corner=DR)
        with self.voiceover(
            "How does a model know a picture of an A and the word A mean the same thing? Train two encoders, one for "
            "pictures and one for captions, so that matching pairs get similar vectors. <bookmark mark='a'/> We "
            "trained a small pair on our letters, with captions like 'bold serif A'. Here's a batch: every picture "
            "scored against every caption. <bookmark mark='b'/> The bright diagonal is the right pairs. Trained on "
            "four hundred million pictures from the web, this is CLIP, and its picture encoder is how most models "
            "see."
        ) as vo:
            self.play(FadeIn(p_in), FadeIn(c_in), FadeIn(cite_))
            self.play(GrowArrow(arr[0]), GrowArrow(arr[1]), FadeIn(e1), FadeIn(e2))
            self.play(GrowArrow(arr[2]), GrowArrow(arr[3]), FadeIn(v1, shift=RIGHT * 0.2), FadeIn(v2, shift=RIGHT * 0.2))
            self.play(FadeIn(dot_), FadeIn(sc))
            vo.wait_until("a")
            self.play(enc.animate.scale(0.75).to_corner(UL, buff=0.3).shift(DOWN * 0.3), run_time=0.8)
            self.play(FadeIn(pics), FadeIn(words), FadeIn(grid), Create(frame), FadeIn(tag), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(d) for d in diag], lag_ratio=0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def losses(self):
        c = load("clip")
        colors = {r"s_{ij}": GREY_A}
        f1 = cmath(r"\text{CLIP:}\quad -\log \frac{e^{s_{ii}}}{\sum_j e^{s_{ij}}}", font_size=34, color=TEXT_C)
        f2 = cmath(r"\text{SigLIP:}\quad -\sum_{j} \log \sigma\big(\pm(s_{ij} + b)\big)", font_size=34, color=IMG_C)
        fs = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-2.6, 2.05, 0])
        l1 = label(r"each picture picks its caption \\ out of the whole batch", font_size=22, color=GREY_A).next_to(f1, RIGHT, buff=0.5)
        l2 = label(r"every pair on its own: \\ match, \ or not?", font_size=22, color=GREY_A).next_to(f2, RIGHT, buff=0.5)
        res = VGroup(label(rf"CLIP's loss: \ right caption ${100 * float(c['acc_clip']):.0f}\%$, \ right letter "
                           rf"${100 * float(c['letter_clip']):.0f}\%$", font_size=24, color=TEXT_C),
                     label(rf"SigLIP's loss: \ right caption ${100 * float(c['acc_siglip']):.0f}\%$, \ right letter "
                           rf"${100 * float(c['letter_siglip']):.0f}\%$", font_size=24, color=IMG_C))
        # the two runs, side by side: the same twelve pairs scored at the same checkpoints
        checks = [int(x) for x in c["checks_clip"]]
        assert checks == [int(x) for x in c["checks_siglip"]]
        S2 = 2.3
        snaps = {m: np.asarray(c[f"snaps_{m}"]) for m in ("clip", "siglip")}
        gx = {"clip": -3.0, "siglip": 3.0}

        def tbl(m, k):
            return heat(snaps[m][k], S2, S2, signed=True).move_to([gx[m], -0.75, 0])

        cur = {m: tbl(m, 0) for m in snaps}
        frames = VGroup(*[SurroundingRectangle(cur[m], buff=0, color=GREY_D, stroke_width=1.5) for m in snaps])
        names = VGroup(label(r"trained with CLIP's loss", font_size=22, color=TEXT_C).next_to(cur["clip"], UP, buff=0.12),
                       label(r"trained with SigLIP's loss", font_size=22, color=IMG_C).next_to(cur["siglip"], UP, buff=0.12))
        for r_, m in zip(res, snaps):
            r_.scale(0.85).next_to(cur[m], DOWN, buff=0.15)
        t = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28,
                                            color=C.BITS).move_to([0, -0.75, 0]))
        rl = label(rf"choosing among all ${int(c['n_captions'])}$ captions, \ for all ${int(c['n_images']):,}$ pictures".replace(",", "{,}"),
                   font_size=20, color=GREY_B).to_edge(DOWN, buff=0.25)
        key_ = label(r"blue: \ high score; \ red: \ low", font_size=20, color=GREY_B).move_to([0, -2.55, 0])
        cite_ = cite(r"X.~Zhai et al., \textit{Sigmoid Loss for Language Image Pre-Training} (2023)", corner=UR)
        with self.voiceover(
            "There are two ways to train this. CLIP's: each picture must pick its own caption out of the whole batch, "
            "a softmax, which ties every pair's loss to every other. <bookmark mark='a'/> SigLIP's: treat every "
            "picture-caption pair as its own yes-or-no question, with a sigmoid. No batch-wide sum, so it scales "
            "to huge batches across many chips. <bookmark mark='b'/> On our letters the two end up close; at scale, "
            "SigLIP's encoders are what many of today's open models see with."
        ) as vo:
            self.play(Write(f1), FadeIn(l1), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(f2), FadeIn(l2))
            vo.wait_until("b")
            self.play(*[FadeIn(cur[m]) for m in cur], Create(frames), FadeIn(names), FadeIn(key_))
            self.add(cnt)
            for k in range(1, len(checks)):
                nxt = {m: tbl(m, k) for m in cur}
                self.play(*[FadeTransform(cur[m], nxt[m]) for m in cur], t.animate.set_value(checks[k]), run_time=0.7)
                cur = nxt
                self.bring_to_front(frames)
            self.play(FadeIn(res), FadeIn(rl))
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        """How contrastive training finds the diagonal: the same twelve pairs, scored at checkpoints."""
        c = load("clip")
        snaps = np.asarray(c["snaps_clip"])
        checks = [int(x) for x in c["checks_clip"]]
        L = np.asarray(c["losses_clip"])
        n = snaps.shape[1]
        S = 4.2

        def grid(k):
            return heat(snaps[k], S, S, signed=True).move_to([-2.6, -0.3, 0])

        cur = grid(0)
        frame = SurroundingRectangle(cur, buff=0, color=GREY_D, stroke_width=1.5)
        cell = S / n
        diag = VGroup(*[Square(cell, stroke_color=WHITE, stroke_width=1.2).move_to(
            [cur.get_left()[0] + cell * (i + 0.5), cur.get_top()[1] - cell * (i + 0.5), 0]) for i in range(n)])
        gl = label(r"rows: \ $12$ pictures; \ columns: \ their $12$ captions", font_size=20, color=GREY_A).next_to(cur, UP, buff=0.15)
        ax = CornerAxes(x_range=[0, checks[-1], 1000], y_range=[0, float(L[:, 1].max()) * 1.05, 1], x_length=4.6, y_length=2.8,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.6, 0.25, 0])
        yn = label(r"CLIP's loss on each batch of $128$", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        xn = label(r"training steps", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        t = ValueTracker(0)
        cnt = always_redraw(lambda: MathTex(rf"\text{{step }}{int(t.get_value()):,}".replace(",", "{,}"), font_size=28, color=C.BITS)
                            .next_to(gl, UP, buff=0.15))
        dg = np.array([np.mean(np.diag(s_)) - np.mean(s_[~np.eye(n, dtype=bool)]) for s_ in snaps])
        # contrastive training, schematic: three pictures (squares) and their captions (dots), scattered; then each pair
        # pulled together and the pairs pushed apart
        pair_c = [TEXT_C, IMG_C, C.SURPRISE]
        before = [((-1.3, 0.25), (0.9, -0.3)), ((0.2, 0.35), (-0.6, -0.35)), ((1.4, 0.2), (-1.6, -0.3))]
        after = [((-1.75, 0.0), (-1.4, 0.0)), ((-0.18, 0.0), (0.18, 0.0)), ((1.4, 0.0), (1.75, 0.0))]

        def pairs_pic(pos):
            fr = Rectangle(width=4.0, height=0.9, stroke_width=0, fill_opacity=0)  # a fixed frame: both states line up
            g_ = VGroup(fr)
            for col, (pi, ci) in zip(pair_c, pos):
                g_.add(Square(0.22, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to([*pi, 0]),
                       Dot([*ci, 0], radius=0.11, color=col))
            return g_

        con = gloss(r"contrastive training", r"pull the matching pairs together, \ push the rest apart \\ "
                    r"(squares: \ pictures; \ dots: \ captions)", picture=pairs_pic(before), corner=DR, width=4.6, color=TEXT_C)
        pic = con[1][2]
        tgt = pairs_pic(after)
        tgt.scale(pic[0].width / tgt[0].width).shift(pic[0].get_center() - tgt[0].get_center())
        with self.voiceover(
            "How does training find that diagonal? Here is the same table of twelve pictures and their captions, "
            "scored at checkpoints while the two encoders learn. <bookmark mark='a'/> At the start, every score is "
            "noise. <bookmark mark='b'/> This is contrastive training: each batch pulls the matching pairs' vectors "
            "together and pushes every other pair apart, and the diagonal lights up: "
            f"matching pairs end up {dg[-1]:.2f} more similar, on average, than mismatched ones. Pairs that share a "
            "letter or a style stay partly lit: they really are alike."
        ) as vo:
            self.play(FadeIn(cur), Create(frame), FadeIn(gl), Create(ax), FadeIn(yn), FadeIn(xn))
            self.add(cnt)
            vo.wait_until("a")
            self.play(Create(diag))
            vo.wait_until("b")
            self.play(FadeIn(con), run_time=0.5)
            self.play(*[m_.animate.move_to(t_) for m_, t_ in zip(pic[1:], tgt[1:])], run_time=1.2)
            for k in range(1, len(checks)):
                nxt = grid(k)
                seg = [ax.c2p(a, b) for a, b in L if checks[k - 1] <= a <= checks[k]]
                anims = [FadeTransform(cur, nxt), t.animate.set_value(checks[k])]
                if len(seg) > 1:
                    anims.append(Create(VMobject(color=TEXT_C, stroke_width=2.5).set_points_as_corners(seg)))
                self.play(*anims, run_time=1.1)
                cur = nxt
                self.bring_to_front(diag)
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()
