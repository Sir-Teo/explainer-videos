from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import IMG_C, TOKEN_COLORS, gray_image, load


class VQ(VoiceoverScene):
    def construct(self):
        self.card()
        self.codebook()
        self.residual()
        self.learned()

    def card(self):
        card = chapter_card(2, r"Codebooks", r"How do you turn a picture into words?", part=16)
        with self.voiceover("Chapter two. Codebooks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def codebook(self):
        v = load("vq")
        book = np.asarray(v["codebook16"])
        img = np.asarray(v["image"])
        cb = Group(*[gray_image(c, 0.5) for c in book]).arrange_in_grid(rows=2, cols=8, buff=0.08).move_to([3.0, 2.3, 0])
        ids = VGroup(*[MathTex(str(i), font_size=18, color=TOKEN_COLORS[i % 8]).next_to(c, DOWN, buff=0.04)
                       for i, c in enumerate(cb)])
        cbl = label(r"a codebook: \ $16$ typical $4\times4$ patches \ (k-means on the letters)", font_size=22, color=IMG_C)
        cbl.next_to(cb, UP, buff=0.15)
        # the letter, as 25 patches; each patch's nearest code (the token), and the copy built from the codes
        n, P = 5, 0.62
        c0 = np.array([-4.0, 0.1, 0])
        pos = [c0 + np.array([(c - 2) * P, (2 - r) * P, 0]) for r in range(n) for c in range(n)]
        pats = [img[4 * r:4 * r + 4, 4 * c:4 * c + 4] for r in range(n) for c in range(n)]
        code = [int(np.argmin(((book - p_[None]) ** 2).sum((1, 2)))) for p_ in pats]
        tiles = Group(*[gray_image(p_, P).move_to(x) for p_, x in zip(pats, pos)])
        ol = label(r"a letter, \ cut into $4\times4$ patches", font_size=22, color=GREY_A)
        ol.move_to([c0[0], c0[1] + 2 * P * 1.3 + P / 2 + 0.3, 0])  # above the patches once they are spread apart
        spread = [c0 + (x - c0) * 1.3 for x in pos]
        coded = Group(*[gray_image(book[k], P).move_to(x) for k, x in zip(code, spread)])
        nums = VGroup(*[MathTex(str(k), font_size=26, color=TOKEN_COLORS[k % 8]).move_to(x) for k, x in zip(code, spread)])
        seq = VGroup(*[MathTex(str(k), font_size=26, color=TOKEN_COLORS[k % 8]) for k in code]).arrange(RIGHT, buff=0.16)
        if seq.width > 6.2:
            seq.scale_to_fit_width(6.2)
        seq.move_to([2.3, -0.9, 0])
        sql = label(r"the picture, \ as $25$ tokens", font_size=22, color=IMG_C).next_to(seq, UP, buff=0.2)
        recs = Group(*[gray_image(np.asarray(v[f"img_vq{k}"]), 1.6) for k in v["sizes"]]).arrange(RIGHT, buff=0.5)
        recs.move_to([2.3, -2.5, 0])
        rl = VGroup(*[label(rf"${int(k)}$ codes: \ ${float(v[f'err_vq{k}']):.3f}$", font_size=20, color=IMG_C)
                      .next_to(r, DOWN, buff=0.1) for k, r in zip(v["sizes"], recs)])
        cite_ = cite(r"A.~van den Oord, O.~Vinyals \& K.~Kavukcuoglu, \textit{VQ-VAE} (2017)", corner=UR)
        # k-means, schematic: three guesses find three clusters in three rounds
        km_g = np.random.default_rng(6)
        km_pts = np.concatenate([m + km_g.normal(0, 0.32, (8, 2)) for m in ([-1.3, 0.6], [1.2, 0.9], [0.1, -0.9])])
        km_dots = VGroup(*[Dot([x, y, 0], radius=0.07, color=GREY_B) for x, y in km_pts])
        km_cols = [TOKEN_COLORS[0], TOKEN_COLORS[1], TOKEN_COLORS[2]]
        km_cent = VGroup(*[Star(5, outer_radius=0.17, color=c_, fill_opacity=1, stroke_width=1.5, stroke_color=WHITE).move_to([x, y, 0])
                           for c_, (x, y) in zip(km_cols, [[-0.4, 1.2], [0.0, 1.0], [0.4, 0.6]])])
        km = gloss(r"k-means", r"start with guesses; \ give each patch to its nearest; \\ move each guess to the average of its patches; \ repeat",
                   picture=VGroup(km_dots, km_cent), corner=DR, width=5.0, color=IMG_C)
        km_d, km_c = km[1][2][0], km[1][2][1]
        with self.voiceover(
            "Text comes in pieces. Pictures and sound are continuous, so to make tokens of them, we need a "
            "vocabulary of shapes: a codebook. <bookmark mark='a'/> Cut every letter picture into four by four "
            "patches and find sixteen typical ones by k-means clustering: <bookmark mark='k'/> start with sixteen "
            "guesses, give each patch to its nearest guess, move each guess to the average of its patches, and "
            "repeat. Part six's mixtures generalize it. <bookmark mark='b'/> Now any picture becomes a sequence of "
            "numbers from zero to fifteen: replace each patch by its nearest code. <bookmark mark='c'/> With more "
            "codes, the copy gets closer: sixteen, sixty-four, two hundred and fifty-six."
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
    def residual(self):
        v = load("vq")
        errs = [float(e) for e in v["rvq_errs"]]
        stages = Group(*[gray_image(np.asarray(v[f"img_rvq{k}"]), 1.6) for k in range(1, 5)]).arrange(RIGHT, buff=0.6)
        stages.move_to(UP * 0.7)
        plus = VGroup(*[MathTex(r"\to", font_size=34, color=GREY_B).move_to((a.get_right() + b.get_left()) / 2)
                        for a, b in zip(stages, stages[1:])])
        sl = VGroup(*[label(rf"${k}$ stage{'s' if k > 1 else ''}: \ ${e:.3f}$", font_size=22, color=IMG_C)
                      .next_to(st, DOWN, buff=0.15) for k, (st, e) in enumerate(zip(stages, errs), start=1)])
        colors = {r"\hat x": IMG_C}
        f = cmath(r"\hat x", "=", r"c^{(1)}_{i_1} + c^{(2)}_{i_2} + c^{(3)}_{i_3} + c^{(4)}_{i_4}", colors=colors,
                  font_size=38).to_edge(UP, buff=0.4)
        fl = label(r"each stage codes what the earlier ones missed", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.12)
        comp = label(rf"$4$ stages of $16$: \ ${errs[-1]:.3f}$, \ like one codebook of $256$ (${float(v['err_vq256']):.3f}$) \\ "
                     rf"finite scalar quantization, \ rounding $4$ numbers to $5$ levels each: \ ${float(v['err_fsq']):.3f}$",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        used = label(r"sound codecs: \ SoundStream, \ EnCodec, \ Mimi", font_size=22, color=C.INTERVAL).next_to(comp, UP, buff=0.25)
        # to quantize: a value slides along a menu of 16 points, snaps to the nearest, and sends its number
        ql = NumberLine(x_range=[0, 15, 1], length=9.0, include_numbers=False, color=GREY_C, tick_size=0.12).move_to(UP * 0.4)
        qn = VGroup(*[MathTex(str(i), font_size=22, color=GREY_B).next_to(ql.n2p(i), DOWN, buff=0.15) for i in range(16)])
        qm = VGroup(*[Dot(ql.n2p(i), radius=0.06, color=TOKEN_COLORS[i % 8]) for i in range(16)])
        qt = label(r"quantize: \ snap a value to the nearest point on a fixed menu, \ and send that point's number",
                   font_size=24, color=IMG_C).next_to(ql, UP, buff=0.9)
        qv = ValueTracker(2.3)
        qd = always_redraw(lambda: Dot(ql.n2p(qv.get_value()), radius=0.11, color=WHITE).shift(UP * 0.35))
        with self.voiceover(
            "One codebook can only be so fine. <bookmark mark='q'/> What we just did has a name: to quantize is to "
            "snap a value to the nearest item on a fixed menu, so it can be sent as a small whole number. The trick "
            "sound models use is to quantize in stages. "
            "<bookmark mark='a'/> The first stage codes the patch roughly; the second codes what the first missed; "
            "then the third, and the fourth. <bookmark mark='b'/> Four stages of sixteen codes do as well here as one "
            "codebook of two hundred and fifty-six, and each token stays a small number. That's residual vector "
            "quantization, inside every neural audio codec, the coder and decoder pair that turns sound into codes "
            "and back. A simpler cousin, finite scalar quantization, just rounds a few numbers to a few levels, with "
            "no codebook at all."
        ) as vo:
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("q")
            self.play(Create(ql), FadeIn(qm), FadeIn(qn), FadeIn(qt))
            self.add(qd)
            self.play(qv.animate.set_value(9.37), run_time=1.6, rate_func=smooth)
            self.play(qv.animate.set_value(9), run_time=0.4)
            sent = MathTex("9", font_size=40, color=TOKEN_COLORS[9 % 8]).move_to(qd.get_center())
            sl_ = label(r"sent:", font_size=24, color=GREY_A).move_to(ql.n2p(9) + DOWN * 1.1 + LEFT * 0.4)
            self.play(Indicate(qm[9], scale_factor=1.6), sent.animate.next_to(sl_, RIGHT, buff=0.15), FadeIn(sl_))
            vo.wait_until("a")
            self.remove(qd)
            self.play(FadeOut(VGroup(ql, qm, qn, qt, sent, sl_)), run_time=0.5)
            for i, st in enumerate(stages):
                self.play(FadeIn(st, shift=RIGHT * 0.2), FadeIn(sl[i]), *([FadeIn(plus[i - 1])] if i else []), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(comp), FadeIn(used))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        """Training a codebook inside a network: the straight-through gradient, the two extra losses, and FSQ."""
        g = np.random.default_rng(16)
        codes = g.uniform(-1.6, 1.6, (7, 2))
        O, u = np.array([-4.3, -0.4, 0]), 1.1

        def P(x):
            return O + u * np.array([x[0], x[1], 0])

        # the cells of the codebook (nearest code), drawn as a coarse map of dots
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
            MathTex(r"\hat z_i = \operatorname{round}\big(\lfloor L/2 \rfloor \tanh z_i\big)", font_size=30, color=C.INTERVAL),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([3.0, 0.2, 0])
        notes = VGroup(label(r"the nearest code: \ no gradient through $\arg\min$", font_size=18, color=GREY_A),
                       label(r"sg: \ stop the gradient. \ Forward: \ $e_k$; \ backward: \ as if $z$", font_size=18, color=GREY_A),
                       label(r"rebuild, \ \ pull codes to the outputs, \ \ keep outputs near their codes", font_size=18, color=GREY_A),
                       label(r"FSQ: \ round each number to $L$ levels: \\ a fixed grid of $L^d$ codes, \ nothing to collapse",
                             font_size=18, color=C.INTERVAL))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.08).align_to(e_, LEFT)
        keep_in_frame(VGroup(eqs, notes))
        tag = note(r"schematic: \ $7$ codes in $2$ dimensions").to_corner(DL, buff=0.3)
        cite_ = cite(r"A.~van den Oord et al., \textit{VQ-VAE} (2017); \ F.~Mentzer et al., \textit{FSQ} (2023)", corner=UR)

        # the two extra terms as two springs between z and its code: a strong one moves the code, a weak one (beta) z
        def spring(a, b, width, color, n=9, amp=0.12):
            d = (b - a) / np.linalg.norm(b - a)
            nrm = np.array([-d[1], d[0], 0])
            pts = [a + (b - a) * (i / (2 * n)) + (nrm * amp * (1 if i % 2 else -1) if 0 < i < 2 * n else 0) for i in range(2 * n + 1)]
            return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)

        sa, sb = np.array([-1.6, 0, 0]), np.array([1.6, 0, 0])
        kc = TOKEN_COLORS[k % len(TOKEN_COLORS)]
        springs = VGroup(spring(sa + UP * 0.35, sb + UP * 0.35, 5, kc), spring(sa + DOWN * 0.35, sb + DOWN * 0.35, 1.8, C.BITS),
                         Dot(sa, radius=0.12, color=WHITE), Dot(sb, radius=0.12, color=kc))
        springs.add(MathTex("z", font_size=32).next_to(springs[2], LEFT, buff=0.12),
                    MathTex("e_k", font_size=32, color=kc).next_to(springs[3], RIGHT, buff=0.12),
                    label(r"strong: \ moves the code to $z$", font_size=20, color=kc).next_to(springs[0], UP, buff=0.08),
                    label(r"weak, \ $\beta$: \ keeps $z$ near its code", font_size=20, color=C.BITS).next_to(springs[1], DOWN, buff=0.08))
        commit = gloss(r"commitment loss", r"a small penalty that stops the encoder's output \\ drifting far from the code it was snapped to",
                       picture=springs, corner=DR, width=5.4, color=C.BITS)
        # FSQ: squash each number into a box, round to the nearest of L = 5 levels: the codebook is the grid
        lv = np.arange(-2, 3)
        fgrid = VGroup(*[Dot(P([a, b]), radius=0.06, color=C.INTERVAL) for a in lv for b in lv])
        fbox = Square(4 * u, stroke_color=C.INTERVAL, stroke_width=1.5).move_to(P([0, 0]))
        fz = g.normal(0, 1.6, (12, 2))
        fpts = VGroup(*[Dot(P(np.clip(x, -2.5, 2.5)), radius=0.07, color=WHITE) for x in fz])
        fl_ = label(r"the codebook is just this grid", font_size=22, color=C.INTERVAL).next_to(fbox, UP, buff=0.15)
        with self.voiceover(
            "In a real model, the codebook is learned along with the encoder and decoder, and that hits a snag. "
            "<bookmark mark='a'/> Each encoder output z is replaced by its nearest code. Picking the nearest is a "
            "jump, with no gradient. <bookmark mark='b'/> The fix is the straight-through trick: forward, use the "
            "code; backward, pretend nothing happened, and hand the code's gradient straight to z. "
            "<bookmark mark='c'/> Two more terms keep things together: one pulls each code toward the outputs that "
            "chose it; the other, the commitment loss, is a small penalty, weighted by beta, that stops each output "
            "drifting far from the code it was snapped to. "
            "<bookmark mark='d'/> Even so, codes that nobody picks stop learning, and many go unused. "
            "<bookmark mark='e'/> Finite scalar quantization, FSQ, sidesteps all of it: squash each number, round it "
            "to a few levels, and the codebook is just the grid. It's what several recent image and video tokenizers use."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(grid), FadeIn(cdots), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(zd), FadeIn(zl), GrowArrow(fwd), FadeIn(el), Write(eqs[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(notes[1]), GrowArrow(gq))
            self.play(TransformFromCopy(gq, gz), FadeIn(gl))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(notes[2]))
            self.play(FadeIn(commit))
            vo.wait_until("d")
            self.play(FadeOut(commit), run_time=0.5)
            vo.wait_until("e")
            self.play(FadeOut(VGroup(grid, cdots, zd, zl, el, fwd, gq, gz, gl, tag)), Write(eqs[3]), FadeIn(notes[3]))
            self.play(FadeIn(fbox), FadeIn(fgrid), FadeIn(fpts), FadeIn(fl_))
            self.play(*[d_.animate.move_to(P(2 * np.tanh(x))) for d_, x in zip(fpts, fz)], run_time=1.0)
            self.play(*[d_.animate.move_to(P(np.round(2 * np.tanh(x)))) for d_, x in zip(fpts, fz)], run_time=0.8)
        self.wait(0.3)
        self.clear_scene()
