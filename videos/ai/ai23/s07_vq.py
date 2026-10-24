from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import (IMG_C, PART, TOKEN_COLORS, VQ_COLORS, VQ_NAMES, band, curve, gray_image, load,
                                   spread_rows)


class VQ(VoiceoverScene):
    def construct(self):
        self.card()
        self.codebook()
        self.learned()
        self.collapse()
        self.cures()

    def card(self):
        card = chapter_card(6, r"Learning a codebook", r"How do you turn a picture into words?", part=PART)
        with self.voiceover("Chapter six. Learning a codebook."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def codebook(self):
        v = load("codebooks")
        book = np.asarray(v["codebook16"])
        img = np.asarray(v["image"])
        cb = Group(*[gray_image(c, 0.5) for c in book]).arrange_in_grid(rows=2, cols=8, buff=0.08).move_to([3.0, 2.3, 0])
        ids = VGroup(*[MathTex(str(i), font_size=18, color=TOKEN_COLORS[i % 8]).next_to(c, DOWN, buff=0.04)
                       for i, c in enumerate(cb)])
        cbl = label(r"a codebook: \ $16$ typical $4\times4$ patches \ (k-means on the letters)", font_size=22, color=IMG_C)
        cbl.next_to(cb, UP, buff=0.15)
        n, P = 5, 0.62
        c0 = np.array([-4.0, 0.1, 0])
        pos = [c0 + np.array([(c - 2) * P, (2 - r) * P, 0]) for r in range(n) for c in range(n)]
        pats = [img[4 * r:4 * r + 4, 4 * c:4 * c + 4] for r in range(n) for c in range(n)]
        code = [int(x) for x in v["code16"]]
        tiles = Group(*[gray_image(p_, P).move_to(x) for p_, x in zip(pats, pos)])
        ol = label(r"a letter, \ cut into $4\times4$ patches", font_size=22, color=GREY_A)
        ol.move_to([c0[0], c0[1] + 2 * P * 1.3 + P / 2 + 0.3, 0])
        spread = [c0 + (x - c0) * 1.3 for x in pos]
        coded = Group(*[gray_image(book[k], P).move_to(x) for k, x in zip(code, spread)])
        nums = VGroup(*[MathTex(str(k), font_size=26, color=TOKEN_COLORS[k % 8]).move_to(x) for k, x in zip(code, spread)])
        seq = VGroup(*[MathTex(str(k), font_size=26, color=TOKEN_COLORS[k % 8]) for k in code]).arrange(RIGHT, buff=0.16)
        if seq.width > 6.2:
            seq.scale_to_fit_width(6.2)
        seq.move_to([2.3, -0.9, 0])
        sql = label(r"the picture, \ as $25$ tokens", font_size=22, color=IMG_C).next_to(seq, UP, buff=0.2)
        sizes = [int(k) for k in v["sizes"]]
        recs = Group(*[gray_image(np.asarray(v[f"img_vq{k}"]), 1.3) for k in sizes]).arrange(RIGHT, buff=0.35)
        recs.move_to([2.3, -2.45, 0])
        rl = VGroup(*[label(rf"${k:,}$: \ ${float(v[f'err_vq{k}']):.3f}$".replace(",", "{,}"), font_size=18, color=IMG_C)
                      .next_to(r, DOWN, buff=0.08) for k, r in zip(sizes, recs)])
        km_g = np.random.default_rng(6)
        km_pts = np.concatenate([m + km_g.normal(0, 0.32, (8, 2)) for m in ([-1.3, 0.6], [1.2, 0.9], [0.1, -0.9])])
        km_dots = VGroup(*[Dot([x, y, 0], radius=0.07, color=GREY_B) for x, y in km_pts])
        km_cols = [TOKEN_COLORS[0], TOKEN_COLORS[1], TOKEN_COLORS[2]]
        km_cent = VGroup(*[Star(5, outer_radius=0.17, color=c_, fill_opacity=1, stroke_width=1.5, stroke_color=WHITE).move_to([x, y, 0])
                           for c_, (x, y) in zip(km_cols, [[-0.4, 1.2], [0.0, 1.0], [0.4, 0.6]])])
        km = gloss(r"k-means \ (schematic)", r"start with guesses; \ give each patch to its nearest; \\ move each guess to the "
                   r"average of its patches; \ repeat", picture=VGroup(km_dots, km_cent), corner=DR, width=5.0, color=IMG_C)
        km_d, km_c = km[1][2][0], km[1][2][1]
        with self.voiceover(
            "Text comes in pieces; pictures and sound are continuous. To make tokens of them we need a vocabulary of "
            "shapes: a codebook. <bookmark mark='a'/> Cut every letter picture into four by four patches and find "
            "sixteen typical ones by k-means: <bookmark mark='k'/> start with sixteen guesses, give each patch to its "
            "nearest guess, move each guess to the average of its patches, and repeat. <bookmark mark='b'/> Now a "
            "picture is a sequence of numbers from zero to fifteen: each patch is replaced by its nearest code. "
            "<bookmark mark='c'/> With more codes the copy comes closer; the numbers are the error per pixel, on "
            f"held-out patches, for {', '.join(f'{k:,}' for k in sizes[:-1])} and {sizes[-1]:,} codes."
        ) as vo:
            self.play(FadeIn(tiles), FadeIn(ol))
            self.play(*[t_.animate.move_to(x) for t_, x in zip(tiles, spread)], run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(cbl), LaggedStart(*[FadeIn(c, scale=0.6) for c in cb], lag_ratio=0.06), FadeIn(ids), run_time=2.0)
            vo.wait_until("k")
            self.play(FadeIn(km))
            for _ in range(3):
                near = [int(np.argmin([np.linalg.norm(d_.get_center() - s_.get_center()) for s_ in km_c])) for d_ in km_d]
                self.play(*[d_.animate.set_color(km_cols[j]) for d_, j in zip(km_d, near)], run_time=0.6)
                means = [np.mean([d_.get_center() for d_, j in zip(km_d, near) if j == i] or [s_.get_center()], axis=0)
                         for i, s_ in enumerate(km_c)]
                self.play(*[s_.animate.move_to(m_) for s_, m_ in zip(km_c, means)], run_time=0.8)
            vo.wait_until("b")
            self.play(FadeOut(km), run_time=0.5)
            self.play(LaggedStart(*[FadeTransform(t_, c_) for t_, c_ in zip(tiles, coded)], lag_ratio=0.04), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(m_) for m_ in nums], lag_ratio=0.03), *[c_.animate.set_opacity(0.35) for c_ in coded])
            self.play(LaggedStart(*[TransformFromCopy(m_, q_) for m_, q_ in zip(nums, seq)], lag_ratio=0.04), FadeIn(sql), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in recs], lag_ratio=0.4), FadeIn(rl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        """Training a codebook inside a network: the nearest code, the straight-through gradient, the two extra losses."""
        g = np.random.default_rng(16)
        codes = g.uniform(-1.6, 1.6, (7, 2))
        O, u = np.array([-4.3, -0.6, 0]), 1.05

        def P(x):
            return O + u * np.array([x[0], x[1], 0])

        grid = VGroup()
        for a in np.linspace(-2, 2, 29):
            for b in np.linspace(-2, 2, 29):
                k = int(np.argmin(((codes - [a, b]) ** 2).sum(1)))
                grid.add(Dot(P([a, b]), radius=0.022, color=TOKEN_COLORS[k % len(TOKEN_COLORS)], fill_opacity=0.35))
        cdots = VGroup(*[Dot(P(c), radius=0.08, color=TOKEN_COLORS[k % len(TOKEN_COLORS)]) for k, c in enumerate(codes)])
        z = np.array([0.35, 0.2])
        k = int(np.argmin(((codes - z) ** 2).sum(1)))
        zd = Dot(P(z), radius=0.08, color=WHITE)
        zl = MathTex(r"z", font_size=30).next_to(zd, UL, buff=0.05)
        el = MathTex(r"e_k", font_size=30, color=TOKEN_COLORS[k % len(TOKEN_COLORS)]).next_to(cdots[k], DL, buff=0.05)
        fwd = Arrow(P(z), P(codes[k]), buff=0.1, color=GREY_A, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        gvec = np.array([0.55, -0.45])
        gq = Arrow(P(codes[k]), P(codes[k] + gvec), buff=0, color=C.SURPRISE, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        gz = Arrow(P(z), P(z + gvec), buff=0, color=C.SURPRISE, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        gl = label(r"the gradient at $e_k$, \\ copied to $z$", font_size=20, color=C.SURPRISE).next_to(gz.get_end(), DR, buff=0.05)
        colors = {r"\operatorname{sg}": C.SURPRISE, r"\beta": C.BITS}
        eqs = VGroup(
            MathTex(r"z_q = e_k, \quad k = \arg\min_j \|z - e_j\|", font_size=30),
            cmath(r"z_q = z +", r"\operatorname{sg}", r"(e_k - z)", colors=colors, font_size=30),
            cmath(r"\mathcal{L} = \|x - D(z_q)\|^2 + \|", r"\operatorname{sg}", r"(z) - e_k\|^2 +", r"\beta", r"\,\|z -",
                  r"\operatorname{sg}", r"(e_k)\|^2", colors=colors, font_size=30),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.0, 0.6, 0])
        notes = VGroup(label(r"the nearest code: \ no gradient through $\arg\min$", font_size=18, color=GREY_A),
                       label(r"sg: \ stop the gradient. \ Forward: \ $e_k$; \ backward: \ as if $z$", font_size=18, color=GREY_A),
                       label(r"rebuild; \ \ pull the code to $z$; \ \ keep $z$ near its code ($\beta = 0.25$)", font_size=18,
                             color=GREY_A))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.08).align_to(e_, LEFT)
        keep_in_frame(VGroup(eqs, notes))
        tag = note(r"schematic: \ $7$ codes in $2$ dimensions").to_corner(DL, buff=0.3)
        cite_ = cite(r"A.~van den Oord, O.~Vinyals \& K.~Kavukcuoglu, \textit{VQ-VAE} (2017)", corner=UR)
        with self.voiceover(
            "In a real model the codebook is learned with the encoder and decoder, as in Part 20's VQ-VAE, and that "
            "hits a snag. <bookmark mark='a'/> Each encoder output z is replaced by its nearest code. Picking the "
            "nearest is a jump, with no gradient. <bookmark mark='b'/> The fix is the straight-through trick: forward, "
            "use the code; backward, pretend nothing happened, and hand the code's gradient straight to z. "
            "<bookmark mark='c'/> Two more terms keep things together: one pulls each chosen code toward the outputs "
            "that chose it; the other, the commitment loss, weighted by beta, keeps each output near the code it was "
            "snapped to. <bookmark mark='d'/> And here is the weakness: a code that nobody picks gets no gradient at "
            "all. It never moves, and it is never picked."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(grid), FadeIn(cdots), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(zd), FadeIn(zl), GrowArrow(fwd), FadeIn(el), Write(eqs[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(notes[1]), GrowArrow(gq))
            self.play(TransformFromCopy(gq, gz), FadeIn(gl))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(notes[2]))
            vo.wait_until("d")
            far = [int(i) for i in np.argsort(-np.linalg.norm(codes, axis=1))[:3] if int(i) != k]
            owner = [int(np.argmin(((codes - [a, b]) ** 2).sum(1))) for a in np.linspace(-2, 2, 29) for b in np.linspace(-2, 2, 29)]
            dead_l = label(r"codes nobody picks: \\ no gradient reaches them", font_size=20, color=GREY_B).move_to([O[0], 2.7, 0])
            self.play(*[cdots[i].animate.set_color(GREY_D).scale(0.7) for i in far],
                      *[d_.animate.set_fill(GREY_D, opacity=0.15) for d_, o_ in zip(grid, owner) if o_ in far],
                      FadeIn(dead_l), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def collapse(self):
        d = load("vqtrain")
        K = int(d["K"])
        checks = [int(c) for c in d["checks"]]
        ax = axes([0, checks[-1], 500], [0, K, 64], x_length=6.2, y_length=4.0, xlabel=r"training steps",
                  ylabel=rf"codes in use on held-out letters \ (of ${K}$)", xticks=[0, checks[-1] // 2, checks[-1]],
                  yticks=[0, 128, 256], center=[-2.9, -0.4, 0])
        curves = VGroup()
        legend_ = []
        for m in ("vq", "ema", "restart"):
            U = np.asarray(d[f"used_t_{m}"], float)
            curves.add(band(ax.ax, checks, U.min(0), U.max(0), VQ_COLORS[m], 0.2))
            curves.add(curve(ax.ax, checks, U.mean(0), VQ_COLORS[m], 3.5))
            legend_.append((VQ_COLORS[m], VQ_NAMES[m]))
        leg = legend(legend_, font_size=20).next_to(ax, RIGHT, buff=0.3).align_to(ax, UP)
        # the final usage of every code, sorted, for plain VQ and for EMA + restarts
        hist = VGroup()
        for i, m in enumerate(("vq", "restart")):
            cnt = np.sort(np.asarray(d[f"counts_{m}"], float))[::-1]
            w = 4.2 / K
            hmax = cnt.max()
            bars = VGroup(*[Rectangle(width=w, height=max(1.4 * c_ / hmax, 0.005), stroke_width=0, fill_color=VQ_COLORS[m],
                                      fill_opacity=0.85).move_to([w * (j + 0.5), 0.7 * c_ / hmax, 0]) for j, c_ in enumerate(cnt)])
            hl = label(VQ_NAMES[m] + rf": \ ${int((cnt > 0).sum())}$ codes used", font_size=20, color=VQ_COLORS[m])
            hist.add(VGroup(bars, hl.next_to(bars, UP, buff=0.1).align_to(bars, LEFT)))
        hist.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([4.3, -1.6, 0])
        hh = label(r"how often each code is used, \ most to least", font_size=18, color=GREY_B).next_to(hist, UP, buff=0.15)
        u = {m: np.asarray(d[f"used_{m}"], float) for m in ("vq", "ema", "restart")}
        steps = int(d["steps"])
        verdict_ema = ("EMA alone does not fix it" if u["ema"].mean() <= u["vq"].mean() * 1.2 else
                       "EMA helps")
        state = (f"the codebook collapses: at the end only {u['vq'].mean():.0f} of the {K} codes are in use"
                 if u["vq"].mean() < 0.5 * K else f"most of the codebook survives: {u['vq'].mean():.0f} of the {K} "
                 "codes are in use")
        works = ("What works is to start the codes on real encoder outputs" if u["restart"].mean() > max(u["vq"].mean(),
                 u["ema"].mean()) else "Another repair is to start the codes on real encoder outputs")
        with self.voiceover(
            "We trained a small VQ autoencoder on the letters: each letter becomes a five by five grid of codes "
            f"from a book of {K}, the same budget of {steps:,} steps and three seeds for every variant. "
            f"<bookmark mark='a'/> With the textbook recipe, {state} on held-out letters, on average over the seeds. "
            "<bookmark mark='b'/> A popular repair updates each code as a running average of the outputs that chose "
            f"it, an exponential moving average, which is k-means done online. Here {verdict_ema}: "
            f"{u['ema'].mean():.0f} codes in use. <bookmark mark='c'/> {works} and restart any code unused for fifty "
            "steps at a random output of the batch: "
            f"{u['restart'].mean():.0f} codes in use."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(FadeIn(curves[0]), Create(curves[1]), FadeIn(leg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(curves[2]), Create(curves[3]), FadeIn(leg[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(curves[4]), Create(curves[5]), FadeIn(leg[2]), run_time=1.5)
            self.play(FadeIn(hh), FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cures(self):
        d = load("vqtrain")
        meth = ("vq", "ema", "restart")
        ppl = spread_rows([(VQ_NAMES[m], VQ_COLORS[m], d[f"ppl_{m}"]) for m in meth],
                          x_max=max(float(np.max(d[f"ppl_{m}"])) for m in meth) * 1.1, width=3.2, font_size=20, label_w=2.2,
                          fmt="{:.0f}")
        err = spread_rows([(VQ_NAMES[m], VQ_COLORS[m], 1000 * np.asarray(d[f"mse_{m}"])) for m in meth],
                          x_max=max(1000 * float(np.max(d[f"mse_{m}"])) for m in meth) * 1.1, width=3.2, font_size=20,
                          label_w=2.2, fmt="{:.1f}")
        ppl.move_to([-2.4, 1.3, 0])
        err.move_to([-2.4, -1.4, 0])
        pl = label(r"perplexity of the codes \ (the number of equally used codes \\ with the same entropy; \ "
                   r"bar: mean, \ dots: seeds)", font_size=20, color=GREY_A).next_to(ppl, UP, buff=0.2)
        el = label(r"error per pixel on held-out letters, \ $\times 10^{-3}$", font_size=20, color=GREY_A).next_to(err, UP, buff=0.2)
        test = np.asarray(d["test"])
        cols = Group()
        for j, m in enumerate(("orig",) + meth):
            ims = test if m == "orig" else np.asarray(d[f"recon_{m}"])[-1]
            col = Group(*[gray_image(ims[i], 0.62) for i in range(4)]).arrange(DOWN, buff=0.06)
            cl = label(r"original" if m == "orig" else VQ_NAMES[m], font_size=16, color=WHITE if m == "orig" else VQ_COLORS[m])
            cols.add(Group(cl, col).arrange(DOWN, buff=0.12))
        cols.arrange(RIGHT, buff=0.22).move_to([4.6, -0.2, 0])
        p = {m: float(np.mean(d[f"ppl_{m}"])) for m in meth}
        e = {m: float(np.mean(d[f"mse_{m}"])) for m in meth}
        best = min(meth, key=lambda m: e[m])
        names = {"vq": "plain VQ", "ema": "EMA", "restart": "EMA with restarts"}
        with self.voiceover(
            "A fairer measure than counting codes is perplexity: the number of equally used codes that would carry "
            f"the same information. <bookmark mark='a'/> Plain VQ reaches {p['vq']:.0f}, EMA {p['ema']:.0f}, and EMA "
            f"with restarts {p['restart']:.0f}. <bookmark mark='b'/> The reconstructions: {names[best]} rebuilds the "
            f"held-out letters best, at {1000 * e[best]:.1f} thousandths per pixel. <bookmark mark='c'/> Restarts are "
            "standard in audio codecs; the other cure is to get rid of the learned codebook altogether, the subject of "
            "the next chapter."
        ) as vo:
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(r_) for r_ in ppl.rows], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("a")
            self.play(*[Indicate(r_.value) for r_ in ppl.rows])
            vo.wait_until("b")
            self.play(FadeIn(el), LaggedStart(*[FadeIn(r_) for r_ in err.rows], lag_ratio=0.3), FadeIn(cols), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(cols[-1], color=VQ_COLORS["restart"], scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()
