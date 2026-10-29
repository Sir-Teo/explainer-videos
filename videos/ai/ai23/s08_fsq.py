from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import IMG_C, PART, VQ_COLORS, VQ_NAMES, curve, gray_image, load, spread_rows


class FSQ(VoiceoverScene):
    def construct(self):
        self.card()
        self.fsq()
        self.lfq()
        self.results()
        self.residual()

    def card(self):
        card = chapter_card(7, r"Codes without a codebook", r"Can quantization be made to never collapse?", part=PART)
        with self.voiceover("Chapter seven. Codes without a codebook."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def fsq(self):
        g = np.random.default_rng(16)
        O, u = np.array([-3.9, -0.5, 0]), 1.0

        def P(x):
            return O + u * np.array([x[0], x[1], 0])

        lv = np.arange(-2, 3)
        fgrid = VGroup(*[Dot(P([a, b]), radius=0.07, color=VQ_COLORS["fsq"]) for a in lv for b in lv])
        fbox = Square(4 * u, stroke_color=VQ_COLORS["fsq"], stroke_width=1.5).move_to(P([0, 0]))
        fz = g.normal(0, 1.6, (14, 2))
        fpts = VGroup(*[Dot(P(np.clip(x, -2.6, 2.6)), radius=0.07, color=WHITE) for x in fz])
        fl_ = label(r"the codebook is the grid \ ($5 \times 5$, \ schematic)", font_size=22, color=VQ_COLORS["fsq"])
        fl_.next_to(fbox, UP, buff=0.2)
        rows = [MathTex(r"\hat z_i = \operatorname{round}\big(\lfloor L_i / 2 \rfloor \tanh z_i\big)", font_size=34),
                MathTex(r"\#\text{codes} = \prod_i L_i = 4 \cdot 4 \cdot 4 \cdot 4 = 256", font_size=34),
                MathTex(r"\text{bits} = \sum_i \log_2 L_i = 8", font_size=34)]
        whys = [why(r"squash into a box, \ round each number; \\ the gradient goes straight through", font_size=20),
                why(r"every corner of the grid is a code \\ (our letters: $4$ numbers, $4$ levels)", font_size=20),
                why(r"the same $256$ codes as chapter six", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=2.6, align_index=None, buff=0.75, edge=6.9)
        cite_ = cite(r"F.~Mentzer, D.~Minnen, E.~Agustsson \& M.~Tschannen, \textit{FSQ} (2023)", corner=DR)
        with self.voiceover(
            "In 2023 Fabian Mentzer and colleagues at Google asked whether the codebook needs learning at all. "
            "<bookmark mark='a'/> Finite scalar quantization: map the encoder's output to a few numbers, squash each "
            "into a fixed range, and round it to one of a few levels. <bookmark mark='b'/> The codebook is just the "
            "grid of all the combinations: with four numbers of four levels each, 256 codes, eight bits, the same as "
            "our VQ. <bookmark mark='c'/> Rounding has no gradient either, so the straight-through trick again. But "
            "there is nothing to collapse: no code can be stranded, because no code is learned."
        ) as vo:
            self.play(FadeIn(fbox), FadeIn(fgrid), FadeIn(fpts), FadeIn(fl_), FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            self.play(*[d_.animate.move_to(P(2 * np.tanh(x))) for d_, x in zip(fpts, fz)], run_time=1.0)
            self.play(*[d_.animate.move_to(P(np.round(2 * np.tanh(x)))) for d_, x in zip(fpts, fz)], run_time=0.8)
            vo.wait_until("b")
            step(1, transform=False)
            step(2, transform=False)
            vo.wait_until("c")
            self.play(Indicate(fgrid, color=WHITE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lfq(self):
        col = VQ_COLORS["lfq"]
        # a cube: the 8 sign patterns of 3 numbers, drawn in oblique projection (schematic)
        def proj(v):
            return np.array([-3.6 + 1.3 * v[0] + 0.55 * v[2], -0.5 + 1.3 * v[1] + 0.4 * v[2], 0])

        corners = [np.array([a, b, c]) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
        edges = VGroup(*[Line(proj(p), proj(q), color=col, stroke_width=1.5, stroke_opacity=0.6)
                         for i, p in enumerate(corners) for q in corners[i + 1:] if np.abs(p - q).sum() == 2])
        dots = VGroup(*[Dot(proj(p), radius=0.08, color=col) for p in corners])
        labs = VGroup(*[MathTex("".join("+" if x > 0 else "-" for x in p), font_size=20, color=WHITE)
                        .next_to(proj(p), UR if p[0] > 0 else UL, buff=0.05) for p in corners])
        cl = label(r"$3$ signs: \ $2^3 = 8$ codes \ (schematic)", font_size=22, color=col).move_to([-3.4, 2.2, 0])
        rows = [MathTex(r"\hat z_i = \operatorname{sign}(z_i), \qquad \#\text{codes} = 2^d", font_size=34),
                MathTex(r"\mathcal{L}_{\text{ent}} = \mathbb{E}\big[H(q(z))\big] - H\big(\mathbb{E}[q(z)]\big)", font_size=34)]
        whys = [why(r"each number keeps only its sign; \\ our letters: $d = 8$, \ $256$ codes", font_size=20),
                why(r"each output confident, \ the codes used evenly \\ ($q$: a softmax over the codes, by distance)",
                    font_size=20)]
        step = ladder(self, rows, whys, keep=2, top=2.0, x=2.6, align_index=None, buff=0.9, edge=6.9)
        cite_ = cite(r"L.~Yu et al., \textit{MAGVIT-v2} (2023)", corner=DR)
        with self.voiceover(
            "Months later, Lijun Yu and colleagues pushed it to the limit for their video tokenizer, MAGVIT-v2: "
            "lookup-free quantization. <bookmark mark='a'/> Keep only each number's sign. With d numbers there are two "
            "to the d codes, the corners of a cube, and a vocabulary of a quarter of a million costs no table at "
            "all. <bookmark mark='b'/> To make the codes earn their keep they add an entropy term: each output should "
            "be confidently near one corner, while across the batch all the corners are used."
        ) as vo:
            self.play(Create(edges), FadeIn(dots), FadeIn(labs), FadeIn(cl), FadeIn(cite_))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1, transform=False)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        d = load("vqtrain")
        meth = [str(m) for m in d["methods"]]
        ppl = spread_rows([(VQ_NAMES[m], VQ_COLORS[m], d[f"ppl_{m}"]) for m in meth],
                          x_max=max(float(np.max(d[f"ppl_{m}"])) for m in meth) * 1.1, width=3.0, font_size=20,
                          label_w=2.2, row_h=0.5, fmt="{:.0f}")
        err = spread_rows([(VQ_NAMES[m], VQ_COLORS[m], 1000 * np.asarray(d[f"mse_{m}"])) for m in meth],
                          x_max=max(1000 * float(np.max(d[f"mse_{m}"])) for m in meth) * 1.1, width=3.0, font_size=20,
                          label_w=2.2, row_h=0.5, fmt="{:.1f}")
        ppl.move_to([-3.0, 0.9, 0])
        err.move_to([3.6, 0.9, 0])
        pl = label(r"perplexity of the codes \ (of $256$)", font_size=22, color=GREY_A).next_to(ppl, UP, buff=0.3)
        el = label(r"error per pixel, \ $\times 10^{-3}$", font_size=22, color=GREY_A).next_to(err, UP, buff=0.3)
        test = np.asarray(d["test"])
        strip = Group()
        for m in ["orig"] + meth:
            ims = test if m == "orig" else np.asarray(d[f"recon_{m}"])[-1]
            row = Group(*[gray_image(ims[i], 0.72) for i in range(3)]).arrange(RIGHT, buff=0.05)
            strip.add(row)
        strip.arrange(RIGHT, buff=0.3)
        if strip.width > 13:
            strip.width = 13
        strip.to_edge(DOWN, buff=0.75)
        sl = VGroup(*[label(r"original" if m == "orig" else VQ_NAMES[m], font_size=16,
                            color=WHITE if m == "orig" else VQ_COLORS[m]).next_to(r_, DOWN, buff=0.08)
                      for m, r_ in zip(["orig"] + meth, strip)])
        e = {m: float(np.mean(d[f"mse_{m}"])) for m in meth}
        p = {m: float(np.mean(d[f"ppl_{m}"])) for m in meth}
        order = sorted(meth, key=lambda m: e[m])
        well = ("use their codes well" if min(p["fsq"], p["lfq"]) > p["vq"] else "do not use their codes better than VQ")
        say = {"vq": "plain VQ", "ema": "VQ with EMA", "restart": "EMA with restarts", "fsq": "FSQ", "lfq": "LFQ"}
        with self.voiceover(
            "All five, at 256 codes, the same network, the same steps and three seeds. <bookmark mark='a'/> The two "
            f"methods without a learned codebook {well}: perplexity {p['fsq']:.0f} for FSQ and "
            f"{p['lfq']:.0f} for LFQ, against {p['vq']:.0f} for plain VQ. <bookmark mark='b'/> On error, "
            f"{say[order[0]]} comes first at {1000 * e[order[0]]:.1f} thousandths, then {say[order[1]]} at "
            f"{1000 * e[order[1]]:.1f}, and {say[order[-1]]} last at {1000 * e[order[-1]]:.1f}. The Google team's "
            "point was not that FSQ wins outright, but that it matches VQ without any of VQ's repairs."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(el), LaggedStart(*[FadeIn(r_) for r_ in ppl.rows], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("a")
            self.play(*[Indicate(ppl.rows[meth.index(m)], scale_factor=1.04) for m in ("fsq", "lfq")])
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in err.rows], lag_ratio=0.15), FadeIn(strip), FadeIn(sl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def residual(self):
        v = load("codebooks")
        sizes = [int(k) for k in v["sizes"]]
        rv = [float(x) for x in v["rvq_errs"]]
        bits1 = [math.log2(k) for k in sizes]
        e1 = [float(v[f"err_vq{k}"]) for k in sizes]
        bits2 = [4 * (i + 1) for i in range(len(rv))]
        ymax = max(e1 + rv) * 1.1
        ax = axes([0, 17, 4], [0, ymax, 0.05], x_length=5.6, y_length=3.6, xlabel=r"bits per $4 \times 4$ patch",
                  ylabel=r"error per pixel, \ held-out patches", xticks=[4, 8, 12, 16],
                  yticks=[round(y, 2) for y in np.arange(0, ymax, 0.05)][:5], center=[-3.4, -0.6, 0])
        c1 = curve(ax.ax, bits1, e1, IMG_C, 3.5)
        d1 = VGroup(*[Dot(ax.ax.c2p(b_, e_), radius=0.07, color=IMG_C) for b_, e_ in zip(bits1, e1)])
        c2 = curve(ax.ax, bits2, rv, C.INTERVAL, 3.5)
        d2 = VGroup(*[Dot(ax.ax.c2p(b_, e_), radius=0.07, color=C.INTERVAL) for b_, e_ in zip(bits2, rv)])
        leg = legend([(IMG_C, r"one codebook \ ($16$ to $1{,}024$ codes)"),
                      (C.INTERVAL, r"stages of $16$ codes, \ residual")], font_size=20).move_to([3.4, -1.3, 0])
        f = cmath(r"\hat x", "=", r"c^{(1)}_{i_1} + c^{(2)}_{i_2} + c^{(3)}_{i_3} + c^{(4)}_{i_4}", colors={r"\hat x": C.INTERVAL},
                  font_size=34).move_to([3.4, 2.4, 0])
        fl = label(r"each stage codes what the earlier ones missed", font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.12)
        stages = Group(*[gray_image(np.asarray(v[f"img_rvq{k}"]), 1.15) for k in range(1, 5)]).arrange(RIGHT, buff=0.25)
        stages.move_to([3.4, 0.6, 0])
        stl = VGroup(*[label(rf"${4 * k}$ bits", font_size=18, color=C.INTERVAL).next_to(s_, DOWN, buff=0.08)
                       for k, s_ in zip(range(1, 5), stages)])
        k8 = sizes.index(256) if 256 in sizes else -1
        at8 = (f"At eight bits one codebook of 256 codes, error {e1[k8]:.3f}, "
               + ("beats" if e1[k8] < rv[1] else "loses to") + f" two stages of 16, {rv[1]:.3f}.")
        with self.voiceover(
            "One more trick, the one sound codecs rely on: quantize in stages. <bookmark mark='a'/> The first stage "
            "codes the patch roughly; the second codes what the first missed; then a third, and a fourth. The patch is "
            "rebuilt as the sum. <bookmark mark='b'/> Is it better than one big codebook? Not at equal bits. "
            f"{at8} <bookmark mark='c'/> But residual stages keep going where one codebook can't: sixteen bits would "
            f"need a table of 65,536 entries, and four stages of 16 reach {rv[-1]:.3f} with 64. That is residual "
            "vector quantization, inside nearly every neural audio codec."
        ) as vo:
            self.play(FadeIn(ax), Write(f), FadeIn(fl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.1) for s_ in stages], lag_ratio=0.4), FadeIn(stl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(leg), Create(c1), FadeIn(d1), run_time=1.5)
            self.play(Create(c2), FadeIn(d2), run_time=1.5)
            vo.wait_until("c")
            self.play(Indicate(d2[-1], scale_factor=1.8))
        self.wait(0.3)
        self.clear_scene()
