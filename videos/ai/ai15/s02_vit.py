from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, heat_image, load, patch_grid


class ViT(VoiceoverScene):
    def construct(self):
        self.card()
        self.tokens()
        self.looking()
        self.positions()

    def card(self):
        card = chapter_card(1, r"An image is a sequence", r"How does a transformer read a picture?", part=15)
        with self.voiceover("Chapter one. An image is a sequence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tokens(self):
        v = load("vit")
        im = np.asarray(v["ex_imgs"])[0]
        n = im.shape[0]
        k = 4
        big = gray_image(im, 3.2).move_to([-4.2, 0.2, 0])
        grid = patch_grid(big, n // k)
        cells = Group()
        for r in range(n // k):
            for c in range(n // k):
                cells.add(gray_image(im[r * k:(r + 1) * k, c * k:(c + 1) * k], 0.42))
        cells.arrange(RIGHT, buff=0.06).move_to([1.6, 0.2, 0])
        if cells.width > 7.6:
            cells.width = 7.6
        cl = label(rf"${(n // k) ** 2}$ patches of ${k}\times{k}$ pixels \ $\to$ \ ${(n // k) ** 2}$ tokens", font_size=26,
                   color=PATCH).next_to(cells, DOWN, buff=0.4)
        lin = label(r"each patch: \ ${16}$ numbers, \ times a matrix, \ plus a learned position vector", font_size=24,
                    color=GREY_A).next_to(cl, DOWN, buff=0.25)
        cite_ = cite(r"A.~Dosovitskiy et al., \textit{An Image Is Worth 16x16 Words} (2020)", corner=DR)
        with self.voiceover(
            "A transformer reads sequences of tokens. So cut the picture into squares, patches, and line them up: "
            "<bookmark mark='a'/> each patch becomes a token, its pixels times a matrix, plus a vector saying where "
            "it was. Then it's part eleven's machinery, unchanged. The 2020 paper's title said it: an image is worth "
            "sixteen by sixteen words."
        ) as vo:
            self.play(FadeIn(big), FadeIn(cite_))
            self.play(Create(grid))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.2) for c_ in cells], lag_ratio=0.04), FadeIn(cl), run_time=2.0)
            self.play(FadeIn(lin))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def looking(self):
        v = load("vit")
        ims, labs, att = np.asarray(v["ex_imgs"]), [int(x) for x in v["ex_labels"]], np.asarray(v["cls_att"])
        acc = float(v["acc"])
        S = 2.0
        pairs = Group()
        for im, lb, a in zip(ims, labs, att):
            pic = gray_image(im, S)
            heat = heat_image(a, S, gamma=0.8).set_opacity(0.75).move_to(pic)
            t = label(rf"``{LETTERS[lb]}''", font_size=26, color=WHITE).next_to(pic, UP, buff=0.12)
            pairs.add(Group(pic, heat, t))
        pairs.arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        head = label(rf"our small vision transformer: \ ${int(v['n_params']):,}$ numbers, \ ${int(v['n_fonts'])}$ fonts".replace(",", "{,}"),
                     font_size=26).to_edge(UP, buff=0.4)
        res = label(rf"${100 * acc:.0f}\%$ right on ${int(v['n_test_fonts'])}$ fonts it never saw", font_size=30, color=PATCH)
        res.to_edge(DOWN, buff=0.9)
        hl = label(r"orange: \ where its summary token looks, \ last layer", font_size=22, color=C.ATTN).next_to(pairs, DOWN, buff=0.3)
        with self.voiceover(
            "We trained a small one to name the letter in each picture, reading twenty-five patches and one extra "
            f"summary token. <bookmark mark='a'/> On fonts it never saw, it's right {100 * acc:.0f} percent of the time. "
            "<bookmark mark='b'/> And here's where its summary token looks, in the last layer: at the strokes that "
            "tell letters apart."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(Group(p[0], p[2])) for p in pairs], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(res))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p[1]) for p in pairs], lag_ratio=0.25), FadeIn(hl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def positions(self):
        v = load("vit")
        sim = np.asarray(v["pos_sim"])
        n = int(round(np.sqrt(sim.shape[0])))
        S = 0.92
        tiles = Group()
        for i in range(n * n):
            row = np.clip(sim[i].reshape(n, n), 0, None)
            row[i // n, i % n] = 0  # leave out each patch's similarity to itself, which is always 1
            tiles.add(heat_image(row, S, color=C.TRUE_P, gamma=0.7))
        tiles.arrange_in_grid(rows=n, cols=n, buff=0.07).move_to([-2.6, -0.3, 0])
        frame = SurroundingRectangle(tiles[n + 1], color=PATCH, buff=0.02, stroke_width=2.5)
        expl = label(r"tile $(r, c)$: \ how alike the position vector \\ of patch $(r, c)$ is to every other \\ (itself left out)", font_size=24,
                     color=GREY_A).move_to([3.8, 1.2, 0])
        nf = label(rf"neighbours: \ ${float(v['near']):.2f}$; \ far apart: \ ${float(v['far']):.2f}$", font_size=26,
                   color=C.TRUE_P).next_to(expl, DOWN, buff=0.5)
        grid = float(v["near"]) > float(v["far"]) + 0.1
        msg = label(r"nobody told it the patches \\ form a grid: \ it learned that" if grid else
                    r"too few pictures to learn the grid: \\ big models trained on millions do", font_size=28,
                    color=PATCH).next_to(nf, DOWN, buff=0.5)
        with self.voiceover(
            "One more look inside. Each patch position has a learned vector, which starts at zero. "
            "<bookmark mark='a'/> Here, for each position, is how similar its vector is to every other position's. "
            + ("<bookmark mark='b'/> Each tile lights up around its own place: neighbours in the picture have similar "
               "vectors. Nobody told the model the patches form a five by five grid. It learned the geometry of the "
               "picture from the pictures."
               if grid else
               "<bookmark mark='b'/> In our little model, there's no clear pattern: neighbours are hardly more alike "
               "than patches far apart. A few thousand letters weren't enough to need it. In the original vision "
               "transformer, trained on millions of photos, each tile lights up around its own place: it learned the "
               "picture's geometry from the pictures alone.")
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tiles], lag_ratio=0.03), FadeIn(expl), run_time=2.0)
            self.play(Create(frame))
            vo.wait_until("b")
            self.play(FadeIn(nf), FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()
