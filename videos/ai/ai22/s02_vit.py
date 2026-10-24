from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import (LETTERS, PART, PATCH, VIT_C, fmt_int, glyph_sheet, gray_image, heat_image, load,
                                   patch_grid)


def summary_picture(answer: str) -> VGroup:
    """The summary token: an extra token at the front of the patch sequence; attention gathers from every patch into
    it, and its final vector alone names the letter."""
    u = 0.36
    cls = Square(u, stroke_color=C.BITS, stroke_width=2.5, fill_color=C.BITS, fill_opacity=0.5)
    pts = VGroup(*[Square(u, stroke_color=PATCH, stroke_width=1.5, fill_color=PATCH, fill_opacity=0.15) for _ in range(7)])
    dots_ = MathTex(r"\cdots", font_size=26, color=PATCH)
    toks = VGroup(cls, pts, dots_)
    pts.arrange(RIGHT, buff=0.08)
    toks.arrange(RIGHT, buff=0.22)
    gather = VGroup(*[CurvedArrow(p_.get_top() + UP * 0.03, cls.get_top() + UP * 0.03 + RIGHT * 0.04 * k, angle=PI / 3,
                                  color=C.ATTN, stroke_width=1.6, tip_length=0.1) for k, p_ in enumerate(pts)])
    ans = data_text(f"“{answer}”", font="DejaVu Sans Mono", font_size=24, color=WHITE).next_to(cls, LEFT, buff=0.6)
    out = Arrow(cls.get_left(), ans.get_right(), buff=0.06, color=C.BITS, stroke_width=2.5, max_tip_length_to_length_ratio=0.25)
    names = VGroup(label(r"summary", font_size=16, color=C.BITS).next_to(cls, DOWN, buff=0.1),
                   label(r"the $25$ patch tokens", font_size=16, color=PATCH).next_to(pts, DOWN, buff=0.1))
    names[1].match_y(names[0])
    g = VGroup(toks, gather, out, ans, names)
    g.toks, g.gather, g.out, g.answer, g.names = toks, gather, out, ans, names
    return g


class ViT(VoiceoverScene):
    def construct(self):
        self.card()
        self.tokens()
        self.replay()
        self.looking()
        self.positions()

    def card(self):
        card = chapter_card(1, r"An image is a sequence", r"How does a transformer read a picture?", part=PART)
        with self.voiceover("Chapter one. An image is a sequence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tokens(self):
        v = load("vit")
        im = np.asarray(v["ex_imgs"])[0]
        n = im.shape[0]
        k = 4
        big = gray_image(im, 3.2).move_to([-4.4, 0.3, 0])
        grid = patch_grid(big, n // k)
        cells = Group(*[gray_image(im[r * k:(r + 1) * k, c * k:(c + 1) * k], 0.42) for r in range(n // k)
                        for c in range(n // k)]).arrange(RIGHT, buff=0.06).move_to([1.6, 0.9, 0])
        if cells.width > 7.6:
            cells.width = 7.6
        cl = label(rf"${(n // k) ** 2}$ patches of ${k}\times{k}$ pixels \ $\to$ \ ${(n // k) ** 2}$ tokens", font_size=26,
                   color=PATCH).next_to(cells, DOWN, buff=0.35)
        f = MathTex(r"z_0 = [\,x_{\text{cls}};\ x_1 E;\ x_2 E;\ \dots;\ x_{25} E\,] + E_{\text{pos}}", font_size=32)
        f.next_to(cl, DOWN, buff=0.45)
        fl = label(r"each patch's $16$ pixels times a learned matrix $E$, \ plus a learned position vector", font_size=22,
                   color=GREY_A).next_to(f, DOWN, buff=0.2)
        cite_ = cite(r"A.~Dosovitskiy et al., \textit{An Image Is Worth 16x16 Words} (2020)", corner=DR)
        tf = label(r"then Part 13's transformer: \ attention and MLPs, \ layer after layer", font_size=24, color=WHITE)
        tf = VGroup(SurroundingRectangle(tf, buff=0.18, corner_radius=0.1, color=C.ATTN, stroke_width=2), tf)
        tf.next_to(fl, DOWN, buff=0.4)
        with self.voiceover(
            "A transformer reads sequences of tokens. So cut the picture into squares, called patches, and line them "
            "up. <bookmark mark='a'/> Each patch becomes a token: its pixels times a learned matrix, plus a learned "
            "vector that says where it was. <bookmark mark='b'/> From there it's Part 13's machinery, unchanged: "
            "attention and MLPs, layer after layer. The 2020 paper that did this, by Alexey Dosovitskiy and colleagues "
            "at Google, said it in its title: an image is worth sixteen by sixteen words."
        ) as vo:
            self.play(FadeIn(big), FadeIn(cite_))
            self.play(Create(grid))
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.2) for c_ in cells], lag_ratio=0.04), FadeIn(cl), run_time=2.0)
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(tf, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self):
        """The vision transformer learning: eight held-out letters and what it calls them, the held-out accuracy, and
        how alike the centre patch's position vector is to every other, at each checkpoint."""
        v = load("vit")
        checks = [int(c) for c in v["checks"]]
        W = np.asarray(v["watch_imgs"])
        wl = [int(x) for x in v["watch_labels"]]
        pred, conf = np.asarray(v["replay_pred"]), np.asarray(v["replay_conf"])
        accs = [float(a) for a in v["replay_acc"]]
        sims = np.asarray(v["replay_sim"])
        cv = np.asarray(v["curve"])
        n = int(round(np.sqrt(sims.shape[-1])))
        pics = Group(*[gray_image(im, 0.85) for im in W]).arrange_in_grid(rows=2, cols=4, buff=(0.25, 0.75)).move_to([-3.8, 0.6, 0])

        def names(k):
            g = VGroup()
            for i, p_ in enumerate(pics):
                right = int(pred[k, i]) == wl[i]
                g.add(data_text(LETTERS[int(pred[k, i])], font=MONO_FONT, font_size=24,
                                color=C.INTERVAL if right else C.SURPRISE).next_to(p_, DOWN, buff=0.1))
            return g

        nm = names(0)
        hl = label(r"held-out fonts: \ what it calls each letter", font_size=20, color=GREY_A).next_to(pics, UP, buff=0.2)
        ax = axes([0, checks[-1]], [0, 1], x_length=4.2, y_length=2.2, xlabel=r"training step", ylabel=r"held-out accuracy",
                  xticks=[0, checks[-1]], yticks=[0, 0.5, 1], center=[3.6, 1.6, 0], font_size=18,
                  xfmt=lambda x: fmt_int(x))
        cc = 2  # the centre patch
        centre = n * cc + cc

        def tile(k):
            row = np.clip(sims[k][centre].reshape(n, n), 0, None)
            row[cc, cc] = 0
            return heat_image(row, 1.5, color=C.TRUE_P, gamma=0.8).move_to([3.6, -1.75, 0])

        tl = label(r"the centre patch's position vector: \\ how alike it is to each other patch's", font_size=18,
                   color=C.TRUE_P).next_to(tile(0), UP, buff=0.12)
        ring = Square(1.5 / n, stroke_color=PATCH, stroke_width=2.5).move_to(tile(0).get_center())
        t = ValueTracker(0)
        cnt = always_redraw(lambda: label(rf"step ${fmt_int(t.get_value())}$", font_size=24, color=VIT_C)
                            .next_to(pics, DOWN, buff=0.75))
        cur = tile(0)
        k_half = next((k for k, a in enumerate(accs) if a > 0.5), len(accs) - 1)
        same0 = len(set(int(p_) for p_ in pred[0])) <= 2
        rn, rf = [float(x) for x in v["replay_near"]], [float(x) for x in v["replay_far"]]
        grew = rn[-1] - rf[-1] > rn[0] - rf[0] + 0.05
        start = ("At first it calls almost everything the same letter. " if same0 else
                 "At first its guesses are scattered at random. ")
        pos_line = ("it comes to resemble its neighbours' vectors more than distant ones." if grew else
                    "it hardly changes shape: the neighbours aren't singled out.")
        with self.voiceover(
            f"We trained a small one, with {int(v['n_params']) // 1000} thousand weights, to name the letter in each "
            f"picture, on {int(v['n_fonts']) - int(v['n_test_fonts'])} fonts, and tested it on "
            f"{int(v['n_test_fonts'])} it never saw. Here it is learning. <bookmark mark='a'/> " + start
            + f"<bookmark mark='b'/> By step {checks[k_half]:,} it's right on {100 * accs[k_half]:.0f} percent of the "
            f"unseen fonts, and at the end on {100 * accs[-1]:.0f} percent. <bookmark mark='c'/> Meanwhile, watch "
            "the position vector of the centre patch, which starts at zero: " + pos_line
        ) as vo:
            self.play(FadeIn(pics), FadeIn(hl), FadeIn(nm), Create(ax), FadeIn(cur), FadeIn(tl), Create(ring))
            self.add(cnt)
            vo.wait_until("a")
            for k in range(1, len(checks)):
                if k == k_half:
                    vo.wait_until("b")
                if k == len(checks) - 2:
                    vo.wait_until("c")
                seg = [ax.ax.c2p(a, b) for a, b in cv if checks[k - 1] <= a <= checks[k]]
                anims = [t.animate.set_value(checks[k]), Transform(nm, names(k)), FadeOut(cur)]
                nxt = tile(k)
                anims.append(FadeIn(nxt))
                if len(seg) > 1:
                    anims.append(Create(VMobject(color=VIT_C, stroke_width=3).set_points_as_corners(seg)))
                self.play(*anims, run_time=1.2)
                cur = nxt
                self.bring_to_front(ring)
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def looking(self):
        v = load("vit")
        ims, labs, att = np.asarray(v["ex_imgs"]), [int(x) for x in v["ex_labels"]], np.asarray(v["cls_att"])
        S = 1.55
        pairs = Group()
        for im, lb, a in zip(ims, labs, att):
            pic = gray_image(im, S)
            heat = heat_image(a, S, gamma=0.8).set_opacity(0.75).move_to(pic)
            t = label(rf"``{LETTERS[lb]}''", font_size=24, color=WHITE).next_to(pic, UP, buff=0.1)
            pairs.add(Group(pic, heat, t))
        pairs.arrange(RIGHT, buff=0.45).move_to([0, 1.75, 0])
        hl = label(r"orange: \ where its summary token looks, \ last layer", font_size=20, color=C.ATTN).next_to(pairs, DOWN, buff=0.2)
        st = gloss(r"summary token", r"one extra token with no picture in it: \\ it gathers from every patch, \ and "
                   r"its final vector names the letter", summary_picture(LETTERS[labs[0]]), width=5.6, color=C.BITS)
        st.move_to([0, -1.9, 0])
        # how far each head looks, layer by layer
        D_ = np.asarray(v["att_dist"])  # (layers, heads), pixels
        L_, H_ = D_.shape
        top = float(np.ceil(D_.max() / 2) * 2 + 2)
        ax = axes([0.5, L_ + 0.5], [0, top], x_length=3.4, y_length=2.2, xlabel=r"layer",
                  ylabel=r"how far each head looks, \ on average (pixels)", xticks=list(range(1, L_ + 1)),
                  yticks=[0, int(top // 2), int(top)], center=[3.6, -1.75, 0], font_size=17)
        dots = VGroup(*[Dot(ax.ax.c2p(l_ + 1 + (h - (H_ - 1) / 2) * 0.12, D_[l_, h]), radius=0.06, color=C.ATTN)
                        for l_ in range(L_) for h in range(H_)])
        lo, hi = float(D_[0].min()), float(D_[0].max())
        mean_first, mean_last = float(D_[0].mean()), float(D_[-1].mean())
        # how much of the summary token's attention falls on patches with ink, against their share of the picture
        ink = np.array([im.reshape(5, 4, 5, 4).mean((1, 3)) > 0.08 for im in ims])
        on_ink = float(np.mean([(a * k).sum() / a.sum() for a, k in zip(att, ink)]))
        ink_share = float(ink.mean())
        rr, cc_ = np.divmod(np.arange(25), 5)
        uniform = float((4 * np.sqrt((rr[:, None] - rr[None]) ** 2 + (cc_[:, None] - cc_[None]) ** 2)).mean())
        if mean_first > 0.8 * uniform:
            reach = (f"Our heads in the first layer already look between {lo:.1f} and {hi:.1f} pixels away, about as far "
                     f"as two patches picked at random, {uniform:.1f}: from the first layer, they look everywhere. A "
                     "convolution's first layer sees only a few pixels.")
        else:
            reach = (f"Our heads in the first layer look between {lo:.1f} and {hi:.1f} pixels away, where two patches "
                     f"picked at random are {uniform:.1f} apart: some heads stay local, like a convolution.")
        with self.voiceover(
            "How does it decide? The transformer adds one extra token, the summary token, which has no picture in "
            "it. <bookmark mark='s'/> Layer by layer it gathers from every patch, and its final vector alone names "
            "the letter. <bookmark mark='a'/> Here is where the summary token looks in the last layer, for four "
            f"letters from an unseen font: {100 * on_ink:.0f} percent of its attention falls on patches with ink in "
            f"them, which are {100 * ink_share:.0f} percent of the picture. <bookmark mark='b'/> And here is how "
            "far each attention head looks, on average. " + reach
        ) as vo:
            self.play(LaggedStart(*[FadeIn(Group(p[0], p[2])) for p in pairs], lag_ratio=0.2), run_time=1.2)
            self.play(FadeIn(st[0]), FadeIn(st[1][:2]))
            vo.wait_until("s")
            sp = st[1][2]
            self.play(FadeIn(sp.toks), FadeIn(sp.names))
            self.play(LaggedStart(*[Create(a_) for a_ in sp.gather], lag_ratio=0.12), run_time=1.5)
            self.play(GrowArrow(sp.out), FadeIn(sp.answer))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p[1]) for p in pairs], lag_ratio=0.25), FadeIn(hl), run_time=2.0)
            vo.wait_until("b")
            self.play(st.animate.move_to([-3.4, -1.9, 0]), FadeIn(ax), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.05), run_time=2.0)
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
        tiles.arrange_in_grid(rows=n, cols=n, buff=0.07).move_to([-2.6, -0.2, 0])
        frame = SurroundingRectangle(tiles[n + 1], color=PATCH, buff=0.02, stroke_width=2.5)
        expl = label(r"tile $(r, c)$: \ how alike the position vector \\ of patch $(r, c)$ is to every other \\ (itself left out)",
                     font_size=22, color=GREY_A).move_to([3.8, 1.6, 0])
        near, far = float(v["near"]), float(v["far"])
        nf = label(rf"neighbours: \ ${near:.2f}$; \ far apart: \ ${far:.2f}$", font_size=26,
                   color=C.TRUE_P).next_to(expl, DOWN, buff=0.45)
        grid = near > far + 0.1
        msg = label(r"nobody told it the patches \\ form a grid: \ it learned that" if grid else
                    r"too few pictures to learn the grid: \\ big models trained on millions do", font_size=26,
                    color=PATCH).next_to(nf, DOWN, buff=0.45)
        pattern = ("Each tile lights up around its own place. Nobody told the model that the patches form a five by "
                   "five grid; it learned the geometry of the picture from the pictures." if grid else
                   "There's little pattern: a few thousand letters weren't enough to need it. In the original vision "
                   "transformer, trained on millions of photos, each tile lights up around its own place.")
        with self.voiceover(
            "All twenty-five position vectors at the end of training: each tile shows how similar one patch's vector "
            f"is to every other's. <bookmark mark='a'/> Neighbours average {near:.2f}, patches far apart {far:.2f}. "
            + pattern
        ) as vo:
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tiles], lag_ratio=0.03), FadeIn(expl), run_time=2.0)
            self.play(Create(frame))
            vo.wait_until("a")
            self.play(FadeIn(nf), FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()


MONO_FONT = "DejaVu Sans Mono"
