from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import A, K, MONO, OURS, Q, V, curve, heat_image, load


def board_rows():
    """The scoreboard so far (Parts 1, 6 and 8), plus our transformer."""
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai6 import compute as c6
    from videos.ai.ai8 import compute as c8

    t, k, n = load("tf"), c6.load("kn"), c8.load("lm")
    rows = [dict(r) for r in c1.load("scoreboard")["rows"]]
    i = next(j for j, r in enumerate(rows) if r["key"] == "best") + 1
    rows.insert(i, dict(key="kn", label=rf"Kneser--Ney, \ ${k['best']}$ characters", bits=k["best_bits"], part=6, kind="count"))
    rows.insert(i + 1, dict(key="nlm", label=rf"a neural model, \ ${n['n_ctx']}$ characters", bits=n["passage_bits"], part=8,
                            kind="lm"))
    rows.insert(i + 2, dict(key="mix", label=r"the neural model $+$ Kneser--Ney", bits=n["mix_bits"], part=8, kind="lm"))
    rows.insert(i + 3, dict(key="tf", label=rf"our transformer, \ ${t['ctx']}$ characters", bits=t["passage_bits"], part=11,
                            kind="lm"))
    return rows, i + 3, n, k


class Transformer(VoiceoverScene):
    def construct(self):
        self.card()
        self.block()
        self.heads()
        self.train()
        self.board()

    def card(self):
        card = chapter_card(2, r"Our own transformer", r"What does a whole transformer look like?", part=11, lit=(2017,))
        with self.voiceover("Chapter two. Our own transformer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def block(self):
        t = load("tf")
        word = "Spade"
        n = len(word)
        xs = np.linspace(-4.6, -0.6, n)
        cells = 8
        g = np.random.default_rng(1)

        def column(x, seed_shift=0.0):
            vals = g.normal(size=cells)
            return VGroup(*[Square(0.26, stroke_width=0.8, stroke_color=GREY_D, fill_color=C.EMBED,
                                   fill_opacity=float(0.2 + 0.6 * min(abs(v) / 2, 1))) for v in vals]).arrange(DOWN, buff=0)
        cols = VGroup(*[column(x).move_to([x, 0.2, 0]) for x in xs])
        chars = VGroup(*[Text(ch, font=MONO, font_size=30, color=GREY_A).next_to(c_, DOWN, buff=0.25) for ch, c_ in zip(word, cols)])
        stream = label(r"each character: \ a vector of $" + str(t["d"]) + r"$ numbers \ (the residual stream)",
                       font_size=24, color=C.EMBED).to_edge(UP, buff=0.4)
        # attention: arrows between columns (later reads earlier)
        att = VGroup(*[CurvedArrow(cols[j].get_top() + UP * 0.1, cols[i].get_top() + UP * 0.1, angle=-PI / 3, color=A,
                                   stroke_width=2.5, tip_length=0.14)
                       for i in range(1, n) for j in range(i) if (i - j) <= 2])
        at_l = label(r"attention: \ moves information \\ between positions", font_size=26, color=A).move_to([3.6, 1.6, 0])
        mlp = VGroup(*[RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08, stroke_color=C.BITS, stroke_width=2.5)
                       .move_to(c_.get_center()) for c_ in cols])
        ml_l = label(r"MLP \ (multilayer perceptron): \\ Part 8's small network, \\ on each position on its own", font_size=26,
                     color=C.BITS).move_to([3.6, -0.1, 0])
        colors = {r"\mathrm{Attn}": A, r"\mathrm{MLP}": C.BITS}
        eqs = VGroup(cmath(r"x \leftarrow x +", r"\mathrm{Attn}", r"(\mathrm{LN}(x))", colors=colors, font_size=34),
                     cmath(r"x \leftarrow x +", r"\mathrm{MLP}", r"(\mathrm{LN}(x))", colors=colors, font_size=34))
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.6, -1.9, 0])
        rep = label(rf"one block; \ ours stacks ${t['layers']}$", font_size=24, color=GREY_A).next_to(eqs, DOWN, buff=0.2)
        cite_ = cite(r"A.~Vaswani et al., \textit{Attention Is All You Need} (2017)", corner=DL)
        with self.voiceover(
            f"Now build one. Each character enters as a vector, part two's idea, {t['d']} numbers here. "
            "The column of vectors is the residual stream from part eight: every layer reads from it and adds back "
            "to it. <bookmark mark='a'/> A transformer block has two halves. Attention moves information between "
            "positions: each character gathers from the ones before it. <bookmark mark='b'/> Then an MLP, a "
            "multilayer perceptron: part eight's small network of weighted sums and bends, applied to each position "
            "on its own, like thinking over what was gathered. "
            "<bookmark mark='c'/> Each half normalizes its input, and adds its output back to the stream. Stack four "
            "blocks, read off a guess for the next character, and that's the whole machine."
        ) as vo:
            self.play(FadeIn(stream), LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cols], lag_ratio=0.15),
                      FadeIn(chars), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a_) for a_ in att], lag_ratio=0.1), FadeIn(at_l), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(att), LaggedStart(*[Create(m) for m in mlp], lag_ratio=0.1), FadeIn(ml_l))
            self.play(*[Indicate(c_, color=C.BITS, scale_factor=1.05) for c_ in cols])
            vo.wait_until("c")
            self.play(FadeOut(mlp), Write(eqs), FadeIn(rep))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heads(self):
        t = load("tf")
        H, L, dh = int(t["heads"]), int(t["layers"]), int(t["d"]) // int(t["heads"])
        maps = np.asarray(t["maps"])  # layer, head, query, key
        S = min(1.55 * 6 / H, 2.4)
        imgs = Group(*[heat_image(maps[0, h], S, S, color=A, mask_upper=True) for h in range(H)])
        imgs.arrange(RIGHT, buff=0.22).move_to(DOWN * 0.2)
        frames = VGroup(*[SurroundingRectangle(m, buff=0, color=GREY_D, stroke_width=1) for m in imgs])
        hl = VGroup(*[label(rf"head {h + 1}", font_size=20, color=GREY_B).next_to(m, UP, buff=0.1) for h, m in enumerate(imgs)])
        head = label(rf"${H}$ heads, \ each with its own $W_Q$, $W_K$, $W_V$, \ in ${dh}$ dimensions", font_size=28)
        head.to_edge(UP, buff=0.4)
        under = label(r"layer 1 of our trained model, \ on a sentence of the passage: \ row $=$ a character, "
                      r"\ bright $=$ where it looks", font_size=22, color=GREY_A).next_to(imgs, DOWN, buff=0.3)
        mask = label(r"dark triangle: \ the future, \ which no character may see", font_size=24, color=GREY_B)
        mask.next_to(under, DOWN, buff=0.3)
        cat = cmath(r"\mathrm{Attn}(x) = W_O\,\big[\,\mathrm{head}_1;\ \dots;\ \mathrm{head}_" + str(H) + r"\,\big]",
                    font_size=32, colors={r"\mathrm{Attn}(x)": A}).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"Attention runs as {H} separate heads, each with its own query, key and value matrices in "
            f"{dh} dimensions, so each can look for something different. <bookmark mark='a'/> Here are the {H} "
            "heads of our trained model's first layer, reading a sentence of the passage: each row is a character, "
            "and the bright squares are where it looks. Some look one step back, some a few, some spread out. "
            "<bookmark mark='b'/> The upper triangle is dark: a character may only look at the past, since it's "
            "the future the model is trying to guess. <bookmark mark='c'/> The heads' outputs are stacked and mixed "
            "by one more matrix."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in imgs], lag_ratio=0.15), FadeIn(frames), FadeIn(hl), FadeIn(under),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(mask))
            vo.wait_until("c")
            self.play(Write(cat))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def train(self):
        t = load("tf")
        rows, i, n, k = board_rows()
        cv = np.asarray(t["curve"])
        lo = float(np.floor(min(cv[:, 1:].min(), k["best_bits"], n["mix_bits"]) * 4) / 4 - 0.25)
        hi = 4.0
        ax = Axes(x_range=[0, float(t["steps"]), float(t["steps"]) / 4], y_range=[lo, hi, 0.5], x_length=7.6, y_length=4.4,
                  tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05})
        ax.move_to([-2.2, -0.5, 0])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(np.ceil(lo * 2) / 2, hi + 0.01, 0.5)])
        xt = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=22, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.1)
                      for v in np.linspace(0, float(t["steps"]), 5)])
        xn = label(r"training steps", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"bits per character", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        steps = cv[:, 0]
        cvv = curve(ax, steps, np.minimum(cv[:, 1], hi), GREY_B, 3)
        cps = curve(ax, steps, np.minimum(cv[:, 2], hi), OURS, 4)
        refs = VGroup()
        for val, txt, col in ((k["best_bits"], r"Kneser--Ney (Part 6)", C.TRUE_P), (n["mix_bits"], r"Part 8's best", C.NEURAL)):
            refs.add(VGroup(DashedLine(ax.c2p(0, val), ax.c2p(float(t["steps"]), val), color=col, stroke_width=1.5),
                            label(txt, font_size=20, color=col).next_to(ax.c2p(float(t["steps"]), val), RIGHT, buff=0.1)))
        if abs(refs[0][1].get_y() - refs[1][1].get_y()) < 0.28:  # close values: keep the two names apart
            hi_, lo_ = sorted(refs, key=lambda r_: -r_[1].get_y())
            hi_[1].shift(UP * 0.14)
            lo_[1].shift(DOWN * 0.14)
        key = VGroup(label(r"held-out novels", font_size=24, color=GREY_B), label(r"the passage", font_size=24, color=OURS))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 2.2, 0])
        facts = VGroup(label(rf"${t['n_params'] / 1e6:.1f}$ million numbers", font_size=26, color=WHITE),
                       label(rf"${t['tokens'] / 1e6:.0f}$ million characters of training", font_size=26, color=WHITE),
                       label(rf"${t['ctx']}$ characters of context", font_size=26, color=WHITE),
                       label(r"on this video's $4$-core CPU", font_size=24, color=GREY_B))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        keep_in_frame(facts)  # clear of the reference lines' names, which sit at the end of the curves
        pb = float(t["passage_bits"])
        beat_kn, beat_mix = pb < k["best_bits"], pb < n["mix_bits"]
        verdict = (f"It reaches {pb:.2f} bits a character on the passage"
                   + (", better than every model before it on our board." if beat_kn and beat_mix else
                      ", better than part eight's neural model, " + ("and than counting. " if beat_kn else
                                                                       "though not yet better than counting. ")))
        with self.voiceover(
            f"Ours has {t['layers']} blocks, {t['heads']} heads and {t['n_params'] / 1e6:.1f} million numbers, and "
            f"reads {t['ctx']} characters at a time. We trained it on the thirty novels, about "
            f"{t['tokens'] / 1e6:.0f} million characters, on the four-core processor that rendered this video. "
            f"<bookmark mark='a'/> {verdict}"
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(xn), FadeIn(yn), FadeIn(facts))
            self.play(FadeIn(refs), FadeIn(key))
            self.play(Create(cvv), Create(cps), run_time=4.0)
            vo.wait_until("a")
            end = glow_dot(cps.get_end(), color=OURS, radius=0.09)
            self.play(FadeIn(end, scale=0.5), Indicate(key[1], color=OURS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def board(self):
        t = load("tf")
        rows, i, n, k = board_rows()
        board = scoreboard(rows, highlight=(i,), max_bits=8.0)
        board.scale_to_fit_height(min(board.height, 6.6)).move_to(DOWN * 0.1)
        glow = SurroundingRectangle(board.rows[i], color=OURS, buff=0.08, corner_radius=0.08)
        samples = t["samples"]
        txt = VGroup(Text(samples[0][0], font="DejaVu Serif", font_size=20, color=GREY_B),
                     Text(" ".join(samples[0][1].split())[:96] + " …", font="DejaVu Serif", font_size=20, color=WHITE))
        txt.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(ORIGIN)
        if txt.width > 12.8:
            txt.scale_to_fit_width(12.8)
        gpt = next(r for r in rows if "GPT-2 small" in r["label"])
        with self.voiceover(
            "On the scoreboard, a new row. <bookmark mark='a'/> GPT-2 small, at "
            f"{gpt['bits']:.2f}, is the same kind of machine: a stack of these blocks, about "
            f"{round(124e6 / t['n_params'], -1):.0f} times bigger, trained on far more text with far more computing. "
            "What separates them is mostly scale, which was part ten's story."
        ) as vo:
            self.play(FadeIn(board))
            self.play(Create(glow))
            vo.wait_until("a")
            self.play(Indicate(board.rows[next(j for j, r in enumerate(rows) if r is gpt)], color=C.NEURAL))
        self.play(FadeOut(board), FadeOut(glow))
        with self.voiceover(
            "And here's what it writes, from part four's prompt: <bookmark mark='a'/> still not sense, but sentences, "
            "names and dialogue, held together over longer stretches than before."
        ) as vo:
            self.play(FadeIn(txt[0]))
            vo.wait_until("a")
            self.play(AddTextLetterByLetter(txt[1]), run_time=3.0)
        self.wait(0.6)
        self.clear_scene()
