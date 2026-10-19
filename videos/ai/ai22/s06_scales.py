from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.compute import load as load1
from videos.ai.ai22.common import MONO, PATCH, codebook_picture, gray_image, heat_image, load

ADD, SUB = C.BITS, C.TRUE_P  # what a scale adds (brighter) or takes away (darker)


def signed_image(D, size, top=None) -> ImageMobject:
    """A signed picture: dark where zero, gold where positive, blue where negative."""
    D = np.asarray(D, float)
    top = top or max(float(np.abs(D).max()), 1e-9)
    v = np.clip(D / top, -1, 1)
    bg = np.array(ManimColor("#121722").to_rgb())
    pos, neg = np.array(ManimColor(ADD).to_rgb()), np.array(ManimColor(SUB).to_rgb())
    a = np.abs(v)[..., None]
    rgb = bg * (1 - a) + np.where(v[..., None] > 0, pos, neg) * a
    img = ImageMobject((np.concatenate([rgb, np.ones(D.shape + (1,))], -1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.stretch_to_fit_width(size).stretch_to_fit_height(size)


class Scales(VoiceoverScene):
    def construct(self):
        self.card()
        self.raster()
        self.residual()
        self.mask()

    def card(self):
        card = chapter_card(5, r"Coarse to fine", r"Can a picture be written token by token?", lit=(2024,), part=22)
        with self.voiceover("Chapter five. Coarse to fine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def raster(self):
        v = load("var")
        x = np.asarray(v["image"])
        n = x.shape[0]
        S = 4.0
        img = gray_image(x, S).move_to([-2.6, -0.2, 0])
        px = S / n
        ul = img.get_corner(UL)
        cover = VGroup(*[Square(px * 1.04, stroke_width=0, fill_color="#121722", fill_opacity=1)
                         .move_to(ul + RIGHT * px * (c + 0.5) + DOWN * px * (r + 0.5)) for r in range(n) for c in range(n)])
        upto = n * 8 + 6
        cur = Square(px, stroke_color=C.BITS, stroke_width=3).move_to(cover[upto])
        cnt = label(rf"token ${upto + 1}$ of ${n * n}$, \ one at a time", font_size=24, color=GREY_A).next_to(img, DOWN, buff=0.25)
        note_ = label(r"the top rows are written \\ before anything below exists", font_size=24, color=GREY_A).move_to([3.6, 0.6, 0])
        # a language model's way: a real line of text, cut the way GPT-2 cuts it, written one token at a time
        toks = load1("lms")["surprise"]["GPT-2 small"]["tokens"][22:31]
        tiles = VGroup()
        for k, tk in enumerate(toks):
            t_ = data_text(tk.replace(" ", "\u2423"), font=MONO, font_size=24, color=WHITE)
            r_ = RoundedRectangle(width=t_.width + 0.22, height=0.46, corner_radius=0.06, stroke_width=0,
                                  fill_color=[C.EMBED, C.MLP, C.KEY][k % 3], fill_opacity=0.5).move_to(t_)
            tiles.add(VGroup(r_, t_))
        tiles.arrange(RIGHT, buff=0.08).move_to([0, 2.95, 0])
        tcap = label(r"text: \ one token at a time \ (a real line, \ cut into GPT-2's tokens)", font_size=20,
                     color=GREY_A).next_to(tiles, DOWN, buff=0.12)
        canvas = SurroundingRectangle(img, buff=0, color=GREY_C, stroke_width=1.5)
        pcap = label(r"a picture: \ the same, \ pixel by pixel?", font_size=24, color=GREY_A).move_to([3.6, 0.6, 0])
        with self.voiceover(
            "Diffusion isn't the only way to make pictures. <bookmark mark='t'/> Language models write one token at a time, so why not "
            "pictures? <bookmark mark='a'/> Read the pixels, or patches, left to right and top to bottom, and "
            f"predict each from the ones before: here, {n * n} steps. <bookmark mark='b'/> It works, and models like "
            "Parti did it at scale. But it's slow, and it's an odd order for a picture: the top rows are fixed "
            "before anything below them exists."
        ) as vo:
            self.add(img, cover)
            self.play(Create(canvas))
            vo.wait_until("t")
            self.play(FadeIn(tcap))
            for t_ in tiles:
                self.play(FadeIn(t_, shift=RIGHT * 0.15), run_time=0.25)
            self.play(FadeIn(pcap))
            vo.wait_until("a")
            self.play(FadeOut(pcap), LaggedStart(*[FadeOut(c_) for c_ in cover[:upto]], lag_ratio=0.02), Create(cur), run_time=3.0)
            self.play(FadeIn(cnt))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def residual(self):
        v = load("var")
        sizes = [int(s) for s in v["sizes"]]
        ex = np.asarray(v["example"])
        errs = np.asarray(v["errs"], float)
        toks = [int(t) for t in v["tokens"]]
        K = len(sizes)
        S = 1.25
        prev = np.zeros_like(ex[0])
        so_far, adds = Group(), Group()
        top = max(float(np.abs(ex[0]).max()), float(np.abs(np.diff(ex, axis=0)).max()))
        for k in range(K):
            so_far.add(gray_image(ex[k], S))
            adds.add(signed_image(ex[k] - prev, S, top))
            prev = ex[k]
        so_far.arrange(RIGHT, buff=0.5).move_to([0, 1.55, 0])
        for a_, s_ in zip(adds, so_far):
            a_.next_to(s_, DOWN, buff=0.55)
        sl = VGroup(*[MathTex(rf"{s}\times{s}", font_size=22, color=PATCH).next_to(im, UP, buff=0.1) for s, im in zip(sizes, so_far)])
        al = VGroup(*[MathTex(rf"{t}", font_size=22, color=GREY_B).next_to(im, DOWN, buff=0.08) for t, im in zip(toks, adds)])
        rowl = VGroup(label(r"the picture \\ so far", font_size=18, color=GREY_A).next_to(so_far, LEFT, buff=0.25),
                      label(r"what this \\ scale adds", font_size=18, color=GREY_A).next_to(adds, LEFT, buff=0.25))
        tl = label(r"tokens", font_size=18, color=GREY_B).next_to(al, LEFT, buff=0.25).align_to(rowl, RIGHT)
        colors = {r"r_k": PATCH, r"\hat x": GREY_A}
        eqs = VGroup(
            cmath(r"r_k", r"= Q\big(\operatorname{down}_{s_k}(x -", r"\hat x", r"_{k-1})\big), \quad", r"\hat x", r"_k =",
                  r"\hat x", r"_{k-1} + \operatorname{up}(", r"r_k", r")", colors=colors, font_size=30),
            MathTex(r"p(r_1, \ldots, r_K) = \prod_{k} p\big(r_k \mid r_1, \ldots, r_{k-1}\big)", font_size=30),
        )
        eqs.arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.75)
        ql = label(r"$Q$: \ each number rounded to one of $16$ levels \ (a $16$-word codebook)", font_size=20,
                   color=GREY_A).next_to(eqs, DOWN, buff=0.12)
        cite_ = cite(r"K.~Tian et al., \textit{Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale "
                     r"Prediction} (2024)", corner=UR)
        cb = gloss(r"codebook", r"a fixed list of allowed values: \ each number is replaced \\ by its nearest entry, "
                   r"and that entry's index is the token", codebook_picture(), width=6.4, color=PATCH)
        cb.to_edge(DOWN, buff=0.2).set_x(0)
        with self.voiceover(
            "VAR, the NeurIPS best paper of 2024, writes in a better order: coarse to fine. <bookmark mark='a'/> "
            "First one token for the whole picture: its average brightness. <bookmark mark='b'/> Then two by two, "
            "four by four, and so on: at each scale, take what the picture still lacks, shrink it to that size, and "
            "round each number to one of sixteen levels; those are the tokens. <bookmark mark='q'/> The sixteen "
            "levels are a codebook: a fixed list of allowed values. Each number snaps to its nearest entry, and "
            "that entry's place in the list is the token. <bookmark mark='c'/> Add them, "
            "enlarged, to the picture so far. <bookmark mark='d'/> And the model's job is to predict each scale's "
            f"tokens given all the coarser ones: {K} steps, {sum(toks)} tokens in all."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(rowl))
            vo.wait_until("a")
            self.play(FadeIn(so_far[0]), FadeIn(adds[0]), FadeIn(sl[0]), FadeIn(al[0]), FadeIn(tl))
            vo.wait_until("b")
            for k in range(1, K):
                self.play(FadeIn(adds[k]), FadeIn(al[k]), FadeIn(sl[k]), TransformFromCopy(so_far[k - 1], so_far[k]), run_time=0.8)
            vo.wait_until("q")
            self.play(FadeIn(cb, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(cb))
            self.play(Write(eqs[0]), FadeIn(ql))
            vo.wait_until("d")
            self.play(Write(eqs[1]))
        self.wait(0.3)
        self.clear_scene()
        # how fast the error falls, scale by scale
        cum = np.cumsum(toks)
        ax = CornerAxes(x_range=[0, math.log10(cum[-1]) + 0.1, 1], y_range=[0, float(errs.max()) * 1.15, 0.1], x_length=6.4,
                        y_length=3.6, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-1.6, -0.3, 0])
        pts = [ax.c2p(math.log10(c), e) for c, e in zip(cum, errs)]
        ln = VMobject(color=PATCH, stroke_width=3.5).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=PATCH) for p in pts])
        dl = VGroup(*[MathTex(rf"{s}\times{s}", font_size=20, color=PATCH).next_to(p, UR, buff=0.06) for s, p in zip(sizes, pts)])
        xt = VGroup(*[MathTex(f"{int(c)}", font_size=20, color=GREY_B).next_to(ax.c2p(math.log10(c), 0), DOWN, buff=0.08)
                      for c in (cum[0], cum[2], cum[4], cum[-1])])
        xn = label(r"tokens so far \ (log scale)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.08)
        yn = label(r"error of the picture so far \ (held-out fonts)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        flat = errs[1] > 0.95 * errs[0]
        with self.voiceover(
            f"Measured on fonts the codebook never saw, the error falls from {errs[0]:.2f} with one token to "
            f"{errs[-1]:.3f} with all {cum[-1]}. "
            + ("The two-by-two scale adds almost nothing on letters, which are mostly about their middle; the big "
               "drops come from the finer scales, where the strokes are." if flat else
               "Each finer scale takes a bite out of what's left.")
        ):
            self.play(Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn))
            self.play(Create(ln), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.2), FadeIn(dl), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mask(self):
        v = load("var")
        toks = [int(t) for t in v["tokens"]]
        sizes = [int(s) for s in v["sizes"]]
        scale_of = np.repeat(np.arange(len(toks)), toks)
        M = (scale_of[None, :] <= scale_of[:, None]).astype(float)
        img = heat_image(M, 4.6, color=PATCH, gamma=1.0).move_to([-3.2, -0.4, 0])
        frame = SurroundingRectangle(img, buff=0, color=GREY_C, stroke_width=1)
        cum = np.concatenate([[0], np.cumsum(toks)])
        tot = cum[-1]
        ul = img.get_corner(UL)
        cuts = VGroup()
        for c in cum[1:-1]:
            f = c / tot * 4.6
            cuts.add(Line(ul + RIGHT * f, ul + RIGHT * f + DOWN * 4.6, stroke_width=1, color=GREY_D),
                     Line(ul + DOWN * f, ul + DOWN * f + RIGHT * 4.6, stroke_width=1, color=GREY_D))
        ml = label(rf"which of the ${tot}$ tokens each one sees", font_size=20, color=GREY_A).next_to(img, UP, buff=0.15)
        # the first four scales are tiny next to the last: enlarge them
        k4 = int(cum[4])
        zoom = heat_image(M[:k4, :k4], 2.0, color=PATCH, gamma=1.0).move_to([1.1, 0.6, 0])
        zf = SurroundingRectangle(zoom, buff=0, color=GREY_B, stroke_width=1.5)
        zc = VGroup()
        for c in cum[1:4]:
            f = c / k4 * 2.0
            zc.add(Line(zoom.get_corner(UL) + RIGHT * f, zoom.get_corner(UL) + RIGHT * f + DOWN * 2.0, stroke_width=1, color=GREY_D),
                   Line(zoom.get_corner(UL) + DOWN * f, zoom.get_corner(UL) + DOWN * f + RIGHT * 2.0, stroke_width=1, color=GREY_D))
        src = Square(k4 / tot * 4.6, stroke_color=GREY_B, stroke_width=1.5).move_to(ul, aligned_edge=UL)
        link = VGroup(DashedLine(src.get_corner(UR), zf.get_corner(UL), dash_length=0.05, stroke_width=1, color=GREY_B),
                      DashedLine(src.get_corner(DR), zf.get_corner(DL), dash_length=0.05, stroke_width=1, color=GREY_B))
        zl = label(rf"the first ${k4}$, \ enlarged", font_size=18, color=GREY_A).next_to(zf, DOWN, buff=0.1)
        big = label(r"the $20 \times 20$ scale: \\ $400$ tokens at once", font_size=20, color=PATCH).next_to(img, RIGHT, buff=0.2)
        big.align_to(img, DOWN)
        cmp_ = VGroup(
            VGroup(label(r"one token at a time", font_size=24, color=GREY_A), MathTex(rf"{sizes[-1] ** 2}", font_size=36, color=GREY_A),
                   label(r"steps", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.2),
            VGroup(label(r"coarse to fine", font_size=24, color=PATCH), MathTex(rf"{len(toks)}", font_size=36, color=PATCH),
                   label(r"steps", font_size=24, color=PATCH)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.35).move_to([4.5, 1.4, 0])
        fl = label(r"real models: \ a learned codebook of $4{,}096$ words, \\ $10$ scales up to $16 \times 16$ \ (as published)",
                   font_size=20, color=GREY_A).move_to([4.4, -1.5, 0])
        with self.voiceover(
            "Inside the transformer, that's a block-shaped mask: each token sees every token of its own scale and "
            "all the coarser ones. <bookmark mark='a'/> The finest scale, four hundred tokens here, is predicted in a "
            f"single pass. <bookmark mark='b'/> So the picture takes {len(toks)} steps instead of {sizes[-1] ** 2}, "
            "and every step sees the whole picture, roughly. In the real model the tokens come from a learned "
            "codebook rather than our sixteen levels, and the paper showed it scaling like a language model."
        ) as vo:
            self.play(FadeIn(img), Create(frame), FadeIn(ml), Create(cuts))
            self.play(Create(src), Create(link), FadeIn(zoom), Create(zf), Create(zc), FadeIn(zl))
            vo.wait_until("a")
            self.play(FadeIn(big))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.2) for r_ in cmp_], lag_ratio=0.4), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()
