from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import (CLIP_C, IMG_C, PART, SIGLIP_C, TEXT_C, curve, gray_image, heat, load, spread_rows)


class Clip(VoiceoverScene):
    def construct(self):
        self.card()
        self.pairs()
        self.bound()
        self.learning()
        self.siglip()

    def card(self):
        card = chapter_card(14, r"Matching pictures and words", r"How do pictures and words meet?", part=PART)
        with self.voiceover("Chapter fourteen. Matching pictures and words."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pairs(self):
        c = load("clip")
        imgs, caps = np.asarray(c["batch_imgs"]), [str(x) for x in c["batch_caps"]]
        sim = np.asarray(c["sim_clip"])
        n = len(caps)
        S = 4.4
        grid = heat(sim, S, S, signed=True).move_to([1.8, -0.6, 0])
        frame = SurroundingRectangle(grid, buff=0, color=GREY_D, stroke_width=1.5)
        cell = S / n
        pics = Group(*[gray_image(im, cell * 0.92).move_to([grid.get_left()[0] - 0.35, grid.get_top()[1] - cell * (i + 0.5), 0])
                       for i, im in enumerate(imgs)])
        words = VGroup(*[data_text(cp, font="DejaVu Sans Mono", font_size=13, color=TEXT_C).rotate(PI / 3)
                         .move_to([grid.get_left()[0] + cell * (i + 0.5), grid.get_top()[1] + 0.55, 0]) for i, cp in enumerate(caps)])
        diag = VGroup(*[Square(cell, stroke_color=WHITE, stroke_width=1.5).move_to(
            [grid.get_left()[0] + cell * (i + 0.5), grid.get_top()[1] - cell * (i + 0.5), 0]) for i in range(n)])
        def vec(vals, col):
            return VGroup(*[Square(0.24, stroke_width=1, stroke_color=col, fill_color=col, fill_opacity=float(x)) for x in vals]).arrange(
                RIGHT, buff=0.03)

        def box(text, col):
            b_ = RoundedRectangle(width=2.0, height=0.7, corner_radius=0.1, stroke_color=col, stroke_width=2)
            return VGroup(b_, label(text, font_size=22, color=col).move_to(b_))

        gq = np.random.default_rng(16)
        u = gq.uniform(0.15, 1, 6)
        w = np.clip(u + gq.normal(0, 0.12, 6), 0.1, 1)
        p_in = gray_image(imgs[0], 1.0).move_to([-4.6, 0.9, 0])
        c_in = data_text(caps[0], font="DejaVu Sans Mono", font_size=22, color=TEXT_C).move_to([-4.6, -0.9, 0])
        e1, e2 = box(r"picture encoder", IMG_C).move_to([-1.6, 0.9, 0]), box(r"caption encoder", TEXT_C).move_to([-1.6, -0.9, 0])
        v1, v2 = vec(u, IMG_C).move_to([1.6, 0.9, 0]), vec(w, TEXT_C).move_to([1.6, -0.9, 0])
        arr = VGroup(*[Arrow(a_.get_right(), b_.get_left(), buff=0.12, stroke_width=3, color=GREY_B) for a_, b_ in
                       ((p_in, e1), (c_in, e2), (e1, v1), (e2, v2))])
        sc = label(rf"score $= u \cdot v = {float(u @ w):.2f}$ \\ matching pairs: \ high \\ the rest: \ low", font_size=24,
                   color=GREY_A).move_to([4.9, 0.0, 0])
        enc = Group(p_in, c_in, e1, e2, v1, v2, arr, sc)
        etag = note(r"schematic", font_size=18).next_to(enc, DOWN, buff=0.3)
        hist = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (r"2014--15: \ a network captions a photo, \ word by word", GREY_A),
            (r"2021: \ CLIP (OpenAI): \ $400$ million pictures and captions; \\ zero-shot ImageNet $76.2\%$, \ with none of "
             r"its $1.28$ million labels", IMG_C))]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_corner(UL, buff=0.4)
        tag = label(r"blue: \ high score; \ red: \ low", font_size=20, color=GREY_B).next_to(grid, DOWN, buff=0.2)
        ours = label(rf"ours: \ ${int(c['n_images']):,}$ letter pictures, \ ${int(c['n_captions'])}$ captions"
                     .replace(",", "{,}"), font_size=20, color=GREY_A).next_to(tag, DOWN, buff=0.12)
        cite_ = cite(r"A.~Radford et al., \textit{CLIP} (2021)", corner=DR)
        with self.voiceover(
            "Pictures met words in two ways. <bookmark mark='a'/> Around 2014 networks learned to caption photos, a "
            "vision network feeding a language model that wrote a sentence. <bookmark mark='b'/> In 2021 OpenAI's "
            "CLIP did something simpler. Two encoders, one for pictures and one for text, trained on four hundred "
            "million pictures with their captions from the web, so that matching pairs get similar vectors. It could "
            "then classify pictures it was never trained to classify: write each class as a caption, and pick the "
            "closest. On ImageNet that scored 76 percent, without a single one of its labels. <bookmark mark='c'/> "
            "We trained a small pair on our letters, with captions like bold serif A. Here's a batch: every picture "
            "scored against every caption, <bookmark mark='d'/> and the bright diagonal is the right pairs."
        ) as vo:
            self.play(FadeIn(hist[0]), FadeIn(p_in), FadeIn(c_in), FadeIn(etag))
            vo.wait_until("b")
            self.play(FadeIn(hist[1]), FadeIn(cite_))
            self.play(GrowArrow(arr[0]), GrowArrow(arr[1]), FadeIn(e1), FadeIn(e2))
            self.play(GrowArrow(arr[2]), GrowArrow(arr[3]), FadeIn(v1), FadeIn(v2), FadeIn(sc))
            vo.wait_until("c")
            self.play(FadeOut(enc), FadeOut(etag))
            self.play(FadeIn(pics), FadeIn(words), FadeIn(grid), Create(frame), FadeIn(tag), FadeIn(ours), run_time=2.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(d_) for d_ in diag], lag_ratio=0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bound(self):
        c = load("clip")
        rows = [MathTex(r"\mathcal L = -\,\mathbb E \log \frac{e^{f(x, y_1)}}{\sum_{j=1}^{N} e^{f(x, y_j)}}", font_size=32),
                MathTex(r"f^*(x, y) = \log \frac{p(y \mid x)}{p(y)} + c(x)", font_size=32),
                MathTex(r"\mathcal L^* = \mathbb E \log\Big(1 + \frac{p(y_1)}{p(y_1 \mid x)} \sum_{j \ge 2} \frac{p(y_j \mid x)}{p(y_j)}\Big)",
                        font_size=30),
                MathTex(r"\approx \mathbb E \log\Big(1 + (N-1)\, \frac{p(y_1)}{p(y_1 \mid x)}\Big) \ \ge \ \log N - I(x; y)",
                        font_size=30, color=CLIP_C)]
        whys = [why(r"picture $x$ picks its caption $y_1$ among $N$", font_size=19),
                why(r"the best critic: \ a density ratio (Part 24)", font_size=19),
                why(r"put it in; \ divide by the true pair's term", font_size=19),
                why(r"each ratio averages $1$ over random captions; \\ then $1 + (N{-}1)r \ge Nr$ for $r \le 1$", font_size=19)]
        step = ladder(self, rows, whys, keep=4, top=3.3, x=-1.6, align_index=None, buff=0.25, edge=6.9)
        Bs = [int(b) for b in c["batches"]]
        k = {B: i for i, B in enumerate(Bs)}
        est = [np.asarray(c[f"mi_clip_{B}"], float)[:, k[B]] for B in Bs]
        H = float(c["H_caption"])
        x0, w = 2.6, 0.9
        sy = 0.3
        base_y = -3.45
        bars = VGroup()
        for i, (B, e) in enumerate(zip(Bs, est)):
            x = x0 + i * 1.5
            ceil_ = Rectangle(width=w, height=math.log(B) * sy, stroke_color=WHITE, stroke_width=1.5).move_to(
                [x, base_y + math.log(B) * sy / 2, 0])
            fill = Rectangle(width=w, height=max(e.mean(), 0.01) * sy, stroke_width=0, fill_color=CLIP_C, fill_opacity=0.7).move_to(
                [x, base_y + e.mean() * sy / 2, 0])
            dots = VGroup(*[Dot([x + 0.3 * (j - 1), base_y + v * sy, 0], radius=0.04, color=WHITE) for j, v in enumerate(e)])
            bars.add(VGroup(ceil_, fill, dots, label(rf"$N = {B}$", font_size=18, color=GREY_A).next_to(ceil_, DOWN, buff=0.08),
                            MathTex(f"{e.mean():.2f}", font_size=20, color=CLIP_C).next_to(fill, UP, buff=0.05)
                            if e.mean() < math.log(B) - 0.4 else MathTex(f"{e.mean():.2f}", font_size=20, color=CLIP_C).move_to(fill)))
        hl = DashedLine([x0 - 0.6, base_y + H * sy, 0], [x0 + 2 * 1.5 + 0.6, base_y + H * sy, 0], color=TEXT_C)
        hll = label(rf"$H(\text{{caption}}) = \log {int(round(math.exp(H)))} = {H:.2f}$", font_size=18, color=TEXT_C).next_to(hl, LEFT, buff=0.1)
        bl = label(r"our CLIP: \ $\log N - \mathcal L$ in nats \ (outline: $\log N$)", font_size=18, color=GREY_A)
        bl.next_to(VGroup(bars, hl), UP, buff=0.12).align_to(bars, LEFT)
        bars_g = VGroup(bars, hl, hll, bl)
        keep_in_frame(bars_g, margin=0.2)
        e16, e256 = est[0].mean(), est[-1].mean()
        bh = VGroup(label(r"what the loss measures", font_size=44),
                    label(r"Part 24: \ $\log N - \mathcal L$ is a lower bound on the mutual information \\ "
                          r"here: \ the same bound, \ from the best possible critic", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "Part 24 showed that this kind of loss measures information. Here is the same fact seen from the critic's "
            "side. <bookmark mark='a'/> The loss asks each picture to pick its caption out of N. <bookmark mark='b'/> "
            "The best possible score is the log of how much more likely the caption is given the picture than on its "
            "own. <bookmark mark='c'/> Put that in, and divide through by the true pair's term. <bookmark mark='d'/> "
            "With many random captions each ratio averages one, and what is left is at least log N minus the mutual "
            "information between pictures and words. So log N minus the loss estimates that information from below, "
            "and can never exceed log N. <bookmark mark='e'/> Our models, trained at three batch sizes, three seeds "
            f"each: the estimate grows from {e16:.2f} nats at a batch of {Bs[0]} to {e256:.2f} at {Bs[-1]}, pinned under "
            f"log N, while the captions themselves hold {H:.2f}. Bigger batches can measure more of what the pictures "
            "and words share."
        ) as vo:
            self.play(FadeIn(bh))
            vo.wait_until("a")
            self.play(FadeOut(bh))
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            step(3, transform=False)
            vo.wait_until("e")
            self.play(FadeIn(bl), Create(hl), FadeIn(hll),
                      LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        c = load("clip")
        snaps = np.asarray(c["snaps_clip"])
        checks = [int(x) for x in c["checks_clip"]]
        Bmax = int(c["batches"][-1])
        L = np.asarray(c[f"losses_clip_{Bmax}"])
        n = snaps.shape[1]
        S = 3.8

        def grid(k):
            return heat(snaps[k], S, S, signed=True).move_to([-3.2, -0.5, 0])

        cur = grid(0)
        frame = SurroundingRectangle(cur, buff=0, color=GREY_D, stroke_width=1.5)
        cell = S / n
        diag = VGroup(*[Square(cell, stroke_color=WHITE, stroke_width=1.2).move_to(
            [cur.get_left()[0] + cell * (i + 0.5), cur.get_top()[1] - cell * (i + 0.5), 0]) for i in range(n)])
        gl = label(r"$12$ pictures against their captions", font_size=20, color=GREY_A).next_to(cur, UP, buff=0.15)
        t = ValueTracker(0)
        cnt = always_redraw(lambda: label(rf"${int(t.get_value()) / 1000:.0f}$ thousand pairs seen", font_size=22,
                                          color=C.BITS).next_to(gl, UP, buff=0.12))
        un = {B: np.asarray(c[f"unseen_clip_{B}"], float) for B in [int(b) for b in c["batches"]]}
        lu = {B: np.asarray(c[f"letter_unseen_clip_{B}"], float) for B in un}
        nh, nc = int(c["n_held"]), int(c["n_captions"])
        zs = VGroup(label(rf"zero-shot: \ ${nh}$ of the ${nc}$ captions never shown in training", font_size=22, color=TEXT_C),
                    label(rf"their pictures find the exact caption: \ ${100 * un[Bmax].mean():.0f}\%$ \ (chance: \ "
                          rf"$1$ in ${nc}$)", font_size=22, color=CLIP_C),
                    label(rf"the right letter: \ ${100 * lu[Bmax].mean():.0f}\%$", font_size=22, color=CLIP_C))
        zs.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.3, -1.7, 0])
        lax = axes([0, float(L[-1, 0]), 1], [0, float(np.percentile(L[:, 1], 98)) * 1.05, 1], x_length=4.6, y_length=2.2,
                   xlabel=r"pairs seen", ylabel=rf"CLIP's loss, \ batches of ${Bmax}$", center=[3.4, 1.4, 0])
        zl = label(rf"CLIP's loss, \ batch ${Bmax}$, \ three seeds", font_size=18, color=GREY_B).next_to(zs, DOWN, buff=0.25)
        because = ("because the caption encoder learned bold, mono and Q separately, and can put them together"
                   if un[Bmax].mean() > 0.2 else "far above chance, but putting known words together is harder than "
                   "it looks")
        with self.voiceover(
            "Here is that table while the two encoders learn. <bookmark mark='a'/> At the start every score is noise. "
            "Each batch pulls the matching pairs' vectors together and pushes the others apart, and the diagonal "
            "lights up; pairs that share a letter or a style stay partly lit, because they really are alike. "
            f"<bookmark mark='b'/> Now the test CLIP was famous for. We hid {nh} of the {nc} captions, every picture "
            "of bold mono Q and the like, from training altogether. <bookmark mark='c'/> Asked to choose among all "
            f"{nc} captions, those pictures find their exact caption {100 * un[Bmax].mean():.0f} percent of the time, "
            f"{because}."
        ) as vo:
            self.play(FadeIn(cur), Create(frame), FadeIn(gl), FadeIn(lax))
            self.add(cnt)
            vo.wait_until("a")
            self.play(Create(diag))
            for k_ in range(1, len(checks)):
                nxt = grid(k_)
                segp = [(a_, b_) for a_, b_ in L if checks[k_ - 1] <= a_ <= checks[k_]]
                extra = [Create(curve(lax.ax, [p_[0] for p_ in segp], [min(p_[1], lax.ax.y_range[1]) for p_ in segp], CLIP_C, 2.5))] \
                    if len(segp) > 1 else []
                self.play(FadeTransform(cur, nxt), t.animate.set_value(checks[k_]), *extra, run_time=1.0)
                cur = nxt
                self.bring_to_front(diag)
            vo.wait_until("b")
            self.play(FadeIn(zs[0]))
            vo.wait_until("c")
            self.play(FadeIn(zs[1:]), FadeIn(zl))
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def siglip(self):
        c = load("clip")
        Bs = [int(b) for b in c["batches"]]
        f1 = MathTex(r"\text{CLIP:} \quad -\log \frac{e^{t\, s_{ii}}}{\sum_j e^{t\, s_{ij}}}", font_size=32, color=CLIP_C)
        f2 = MathTex(r"\text{SigLIP:} \quad -\sum_{j} \log \sigma\big(z_{ij}\,(t\, s_{ij} + b)\big), \quad z_{ij} = \pm 1",
                     font_size=32, color=SIGLIP_C)
        fs = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.4).shift(LEFT * 2.2)
        l1 = label(r"each picture picks its caption \\ out of the whole batch", font_size=20, color=GREY_A).next_to(f1, RIGHT, buff=0.4)
        l2 = label(r"every pair on its own: \\ match, \ or not?", font_size=20, color=GREY_A).next_to(f2, RIGHT, buff=0.4)
        rows = []
        for B in Bs:
            rows.append((rf"CLIP, \ $N = {B}$", CLIP_C, 100 * np.asarray(c[f"unseen_clip_{B}"], float)))
            rows.append((rf"SigLIP, \ $N = {B}$", SIGLIP_C, 100 * np.asarray(c[f"unseen_siglip_{B}"], float)))
        mx = max(r[2].max() for r in rows)
        bars = spread_rows(rows, x_max=max(10.0, mx * 1.15), width=4.4, row_h=0.42, font_size=18, label_w=2.4, fmt="{:.0f}")
        bars.move_to([-0.6, -1.3, 0])
        bl = label(rf"unseen captions found, \ $\%$ \ (same ${int(c['pairs']) // 1000}$ thousand pairs for every run; "
                   r"three seeds)", font_size=18, color=GREY_A).next_to(bars, UP, buff=0.15)
        tabs = Group()
        for nm, key, col in ((r"CLIP's loss", "sim_clip", CLIP_C), (r"SigLIP's loss", "sim_siglip", SIGLIP_C)):
            im = heat(np.asarray(c[key]), 2.6, 2.6, signed=True)
            tabs.add(Group(im, label(nm + r", \ trained", font_size=20, color=col).next_to(im, UP, buff=0.1)))
        tabs.arrange(RIGHT, buff=0.8).move_to([0, -1.4, 0])
        use = label(r"SigLIP 2 (2025): \ the eyes of many open \\ vision-language models, \ Qwen3-VL's among them",
                    font_size=19, color=SIGLIP_C).to_corner(DR, buff=0.35)
        cite_ = cite(r"X.~Zhai et al., \textit{Sigmoid Loss for Language Image Pre-Training} (2023)", corner=DL)
        m = {(L, B): float(np.mean(c[f"unseen_{L}_{B}"])) for L in ("clip", "siglip") for B in Bs}
        small = ("SigLIP is ahead at the smallest batch" if m[("siglip", Bs[0])] > m[("clip", Bs[0])] + 2e-2 else
                 "CLIP is ahead at the smallest batch" if m[("clip", Bs[0])] > m[("siglip", Bs[0])] + 2e-2 else
                 "the two are level at the smallest batch")
        big = ("SigLIP is ahead at the largest" if m[("siglip", Bs[-1])] > m[("clip", Bs[-1])] + 2e-2 else
               "CLIP is ahead at the largest" if m[("clip", Bs[-1])] > m[("siglip", Bs[-1])] + 2e-2 else
               "level at the largest")
        with self.voiceover(
            "In 2023 Xiaohua Zhai and colleagues at Google changed one thing. CLIP's loss is a softmax over the "
            "batch: each picture's score depends on every other caption in it, so the whole batch must be gathered "
            "on every chip. <bookmark mark='a'/> SigLIP asks each picture-caption pair a yes-or-no question instead, "
            "with a sigmoid and a learned bias. No batch-wide sum, so it scales to enormous batches, and they found "
            "it better at small ones. <bookmark mark='b'/> We ran both at three batch sizes, on the same budget of "
            f"pairs, three seeds each. On the unseen captions, {small}, and {big}: "
            f"{100 * m[('clip', Bs[0])]:.0f} against {100 * m[('siglip', Bs[0])]:.0f} percent at {Bs[0]}, "
            f"{100 * m[('clip', Bs[-1])]:.0f} against {100 * m[('siglip', Bs[-1])]:.0f} at {Bs[-1]}, CLIP first. "
            "<bookmark mark='c'/> At scale, SigLIP's encoders became the eyes of many open vision-language models."
        ) as vo:
            self.play(FadeIn(f1), FadeIn(l1), FadeIn(cite_), FadeIn(tabs[0]))
            vo.wait_until("a")
            self.play(FadeIn(f2), FadeIn(l2), FadeIn(tabs[1]))
            vo.wait_until("b")
            self.play(FadeOut(tabs))
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(r_) for r_ in bars.rows], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(use))
        self.wait(0.3)
        self.clear_scene()
