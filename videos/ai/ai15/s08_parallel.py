from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import DECAY, DELTA, K, PART, Q, SSM_C, STATE, V, load, sci


class Parallel(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.scan()
        self.parallel()

    def card(self):
        card = chapter_card(7, r"Training a recurrence in parallel", r"How can a loop over tokens run all at once?",
                            part=PART)
        with self.voiceover("Chapter seven. Training a recurrence in parallel."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        colors = {r"h_t": STATE, r"h_{t-1}": STATE, r"a_t": DECAY, r"b_t": K, r"a_1": DECAY, r"a_2": DECAY,
                  r"b_1": K, r"b_2": K, r"a_3": DECAY, r"b_3": K}
        f0 = cmath(r"h_t", "=", r"a_t", r"\,", r"h_{t-1}", "+", r"b_t", colors=colors, font_size=40).to_edge(UP, buff=0.4)
        fl = label(r"a linear recurrence: \ the decaying memory, \ an SSM, \ one channel of Mamba", font_size=22,
                   color=GREY_A).next_to(f0, DOWN, buff=0.15)
        rows = [
            cmath(r"(a_1, b_1)", r"\bullet", r"(a_2, b_2)", "=", r"(a_1 a_2,\; a_2 b_1 + b_2)", font_size=34),
            cmath(r"h_2", "=", r"a_2 (a_1 h_0 + b_1) + b_2", "=", r"(a_1 a_2)\, h_0 + (a_2 b_1 + b_2)", font_size=34),
            cmath(r"\big((a_1,b_1) \bullet (a_2,b_2)\big) \bullet (a_3,b_3)", "=", r"(a_1 a_2 a_3,\; a_3 a_2 b_1 + a_3 b_2 + b_3)",
                  font_size=32),
            cmath(r"(a_1,b_1) \bullet \big((a_2,b_2) \bullet (a_3,b_3)\big)", "=", r"(a_1 a_2 a_3,\; a_3 a_2 b_1 + a_3 b_2 + b_3)",
                  font_size=32),
        ]
        whys = [why(r"a step as a pair: \ multiply by $a$, \ add $b$"), why(r"two steps are again one step"),
                why(r"group the first two first"), why(r"or the last two: \ the same \ (associative)")]
        tag = label(r"associative $\Rightarrow$ any grouping, \ so all prefixes in $\log_2 T$ rounds", font_size=26,
                    color=C.BITS).to_edge(DOWN, buff=0.5)
        cite_ = cite(r"G.~E.~Blelloch, \textit{Prefix Sums and Their Applications} (1990); \ E.~Martin \& C.~Cundy (2018)",
                     corner=DR)
        with self.voiceover(
            "Every memory so far is written one token at a time, and each step waits for the one before: thousands "
            "of steps in a row, while a graphics card wants a few big operations. Training on a whole text at once "
            "needs another way. <bookmark mark='a'/> Take the simplest case, one number: multiply the memory by a_t, "
            "add b_t. That's the decaying memory, a state-space model, one channel of Mamba. "
            "<bookmark mark='b'/> Write each step as a pair, a and b. <bookmark mark='c'/> Two steps in a row are "
            "again one step: multiply by a_1 a_2, and add a_2 b_1 plus b_2. <bookmark mark='d'/> And it doesn't "
            "matter how you group three of them: <bookmark mark='e'/> first two first, or last two first, the "
            "result is the same. <bookmark mark='f'/> The combination is associative, and that is all a parallel "
            "prefix scan needs, a trick from the 1980s for adding up running totals in parallel. Eric Martin and "
            "Chris Cundy brought it to recurrent networks in 2018, Part 10 used it for minGRU, and Mamba runs on it."
        ) as vo:
            self.play(Write(f0), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(fl))
            step = ladder(self, rows, whys, keep=4, top=1.6, x=-0.6, buff=0.42, edge=6.8, align_index=None)
            for k, m in enumerate("bcde"):
                vo.wait_until(m)
                step(k)
            vo.wait_until("f")
            self.play(FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scan(self):
        s = load("scan")
        T = 8
        xs = np.linspace(-4.6, 2.4, T)
        ys = [1.9, 0.75, -0.4, -1.55]
        bw = 0.78

        def box(i, lv):
            lo = max(0, i - 2 ** lv + 1)
            full = lo == 0
            col = C.BITS if full else STATE
            r = RoundedRectangle(width=bw, height=0.5, corner_radius=0.08, stroke_color=col, stroke_width=2,
                                 fill_color=col, fill_opacity=0.25 if full else 0.1)
            t = MathTex(rf"{lo + 1}" if lo == i else rf"{lo + 1}\text{{--}}{i + 1}", font_size=22, color=WHITE)
            return VGroup(r, t.move_to(r)).move_to([xs[i], ys[lv], 0])

        levels = [VGroup(*[box(i, lv) for i in range(T)]) for lv in range(4)]
        links = []
        for lv, kk in enumerate((1, 2, 4), start=1):
            ln = VGroup()
            for i in range(T):
                ln.add(Line(levels[lv - 1][i].get_bottom(), levels[lv][i].get_top(), color=GREY_C, stroke_width=1.5))
                if i >= kk:
                    ln.add(Line(levels[lv - 1][i - kk].get_bottom(), levels[lv][i].get_top(), color=C.BITS, stroke_width=2.5))
            links.append(ln)
        lab = VGroup(*[label(t, font_size=18, color=GREY_B).next_to(levels[lv], LEFT, buff=0.25) for lv, t in
                       enumerate([r"steps", r"round 1", r"round 2", r"round 3"])])
        key = label(r"each box: \ the combined steps it covers; \ gold: \ a finished $h_t$", font_size=20, color=GREY_A)
        key.to_edge(DOWN, buff=0.3).shift(LEFT * 1.3)
        res = VGroup(
            label(rf"$T = {s['T']:,}$: \ ${int(s['rounds_hs'])}$ rounds \ instead of ${s['T']:,}$ steps".replace(",", "{,}"),
                  font_size=22, color=WHITE),
            label(rf"Blelloch's version: \ ${int(s['work_bl']):,}$ combines, \ about $2T$".replace(",", "{,}"), font_size=20,
                  color=GREY_A),
            label(rf"against the loop: \ largest relative difference ${sci(max(float(s['diff_hs']), float(s['diff_bl'])))}$",
                  font_size=20, color=C.INTERVAL),
            label(rf"with $4 \times 4$ matrices for $a_t$: \ ${sci(float(s['diff_mat']))}$", font_size=20, color=C.INTERVAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([5.0, 0.2, 0])
        with self.voiceover(
            "Here's the scan on eight steps. <bookmark mark='a'/> In the first round, every step combines with the "
            "one just before it. <bookmark mark='b'/> In the second, with the one two before, <bookmark mark='c'/> "
            "and in the third, four before. After three rounds every position holds the combination of all the "
            "steps up to it: every h_t at once. <bookmark mark='d'/> For "
            f"{int(s['T']):,} steps that's {int(s['rounds_hs'])} rounds. This simple version does more work in all, T "
            "times the number of rounds; Guy Blelloch's up-and-down sweep does about two T. "
            "<bookmark mark='e'/> We checked both against the plain loop, and with four-by-four matrices in place of "
            "the numbers: the same answers, to rounding error."
        ) as vo:
            self.play(FadeIn(levels[0]), FadeIn(lab[0]), FadeIn(key))
            for lv, m in enumerate("abc", start=1):
                vo.wait_until(m)
                self.play(Create(links[lv - 1]), FadeIn(lab[lv]), run_time=0.8)
                self.play(LaggedStart(*[FadeIn(b_, shift=DOWN * 0.1) for b_ in levels[lv]], lag_ratio=0.08), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("e")
            self.play(FadeIn(res[2]), FadeIn(res[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def parallel(self):
        d = load("delta")
        T, Cn = int(d["T"]), int(d["chunk"])
        nC = T // Cn
        W = 12.0
        cw = W / nC
        chunks = VGroup(*[Rectangle(width=cw * 0.92, height=0.5, stroke_color=GREY_C, stroke_width=1, fill_color=STATE,
                                    fill_opacity=0.08).move_to([-W / 2 + cw * (i + 0.5), 2.0, 0]) for i in range(nC)])
        tl = label(rf"${T:,}$ tokens \ in ${nC}$ chunks of ${Cn}$".replace(",", "{,}"), font_size=22, color=GREY_A)
        tl.next_to(chunks, UP, buff=0.15)
        cursor = Rectangle(width=W / T * 8, height=0.62, stroke_width=0, fill_color=WHITE, fill_opacity=0.9).move_to(chunks[0].get_left())
        colors = {r"k_i": K, r"k_i^{\top}": K, r"\beta_i": DELTA, r"w_i": C.BITS, r"W": C.BITS, r"K": K, r"\beta": DELTA}
        f1 = cmath(r"\prod_{i=1}^{C}", r"\big(I - ", r"\beta_i", r"k_i", r"k_i^{\top}", r"\big)", "=", r"I - \sum_{i=1}^{C}", r"w_i",
                   r"k_i^{\top}", colors=colors, font_size=34)
        f2 = cmath(r"\big(I + \mathrm{tril}(\mathrm{diag}(", r"\beta", r")\,", r"K", r"K", r"^{\top}", r", -1)\big)\,", r"W", "=",
                   r"\mathrm{diag}(", r"\beta", r")\,", r"K", colors=colors, font_size=34)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.5).move_to([-1.6, -0.3, 0])
        l1 = label(r"the WY form: \ a product of $C$ such matrices \\ is the identity minus one low-rank matrix",
                   font_size=20, color=GREY_A).next_to(f1, RIGHT, buff=0.4)
        l2 = label(r"one triangular solve gives every $w_i$: \\ the UT transform", font_size=20, color=GREY_A).next_to(f2, RIGHT, buff=0.4)
        for l_ in (l1, l2):
            keep_in_frame(l_)
        # sixty-four corrections in a row, collapsing into one matrix
        chain = VGroup(*[Square(0.32, stroke_color=DELTA, stroke_width=1.5, fill_color=DELTA, fill_opacity=0.15)
                         for _ in range(8)], MathTex(r"\cdots", font_size=30, color=GREY_B),
                       *[Square(0.32, stroke_color=DELTA, stroke_width=1.5, fill_color=DELTA, fill_opacity=0.15)
                         for _ in range(3)]).arrange(RIGHT, buff=0.1).move_to([-3.2, 1.2, 0])
        chain_l = label(r"$64$ corrections, \\ one after another", font_size=20, color=DELTA).next_to(chain, RIGHT, buff=0.3)
        one = VGroup(Rectangle(width=1.6, height=0.5, stroke_color=C.BITS, stroke_width=2, fill_color=C.BITS, fill_opacity=0.15),
                     MathTex(r"I - \sum w_i k_i^{\top}", font_size=24, color=C.BITS)).move_to([-3.2, 1.2, 0])
        one[1].move_to(one[0])
        one_l = label(r"one matrix, \\ the same result", font_size=20, color=C.BITS).next_to(one, RIGHT, buff=0.3)
        dp, dg = float(d["diff_plain"]), float(d["diff_gated"])
        tr_, tc_ = float(d["t_rec_gated"]), float(d["t_chunk_gated"])
        speed = (f"Even on this processor the chunks were quicker, {tc_:.2f} seconds against {tr_:.2f} for the loop; "
                 "on a graphics card, built for big matrix products, the gap is far larger." if tc_ < tr_ else
                 f"On this processor the plain loop was still quicker, {tr_:.2f} seconds against {tc_:.2f}; on a "
                 "graphics card, built for big matrix products, the chunks win by far.")

        res = VGroup(label(rf"step by step \ vs \ by chunks, \ on ${T:,}$ random tokens: \ largest difference "
                           rf"${sci(max(dp, dg))}$".replace(",", "{,}"), font_size=24, color=C.INTERVAL),
                     label(rf"sequential steps: \ ${T:,}$ \ vs \ ${nC}$ \ (each chunk is matrix products)".replace(",", "{,}"),
                           font_size=24, color=WHITE)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.55)
        cite_ = cite(r"S.~Yang, B.~Wang, Y.~Zhang, Y.~Shen \& Y.~Kim, \textit{Parallelizing Linear Transformers with the Delta "
                     r"Rule over Sequence Length} (2024)", corner=UR)
        with self.voiceover(
            "For the delta rule, the coefficient is a matrix, I minus beta k k transpose, and combining two of them "
            "costs a full matrix product: scanning with them would be slow. <bookmark mark='a'/> The way out is to "
            "cut the text into chunks of sixty-four and handle each chunk at once. <bookmark mark='b'/> "
            "Within a chunk, the memory gets multiplied by sixty-four of those I minus beta k k transpose matrices: "
            "sixty-four small corrections, one after another. <bookmark mark='w'/> Multiplied out, they collapse "
            "into one: the identity minus a sum of sixty-four rank-one terms, w times k transpose. Numerical "
            "analysts call it the WY form; they found it decades ago for products of Householder reflections, "
            "matrices just like these. <bookmark mark='c'/> And all the w's come from one triangular solve, the UT "
            "transform: each w depends only on the ones before it, and the hardware works them all out with a few "
            "big matrix products instead of sixty-four waits in a row. With them, a chunk's outputs and its final memory are just matrix products, and the "
            "decay of the gated version folds into the same form. <bookmark mark='d'/> We checked it on our "
            f"computer: for {T} random tokens, step by step and chunk by chunk agree to rounding error, with "
            f"{nC} sequential steps instead of {T}. " + speed + " That's how Qwen3-Next and Kimi Linear were trained."
        ) as vo:
            self.play(FadeIn(chunks), FadeIn(tl), FadeIn(cite_))
            self.add(cursor)
            self.play(cursor.animate.move_to(chunks[3].get_center()), run_time=2.0, rate_func=linear)
            self.remove(cursor)
            vo.wait_until("a")
            self.play(LaggedStart(*[c_.animate.set_fill(STATE, 0.55) for c_ in chunks], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_, shift=RIGHT * 0.1) for m_ in chain], lag_ratio=0.08), FadeIn(chain_l))
            vo.wait_until("w")
            self.play(ReplacementTransform(chain, one), FadeTransform(chain_l, one_l))
            self.play(Write(f1), FadeIn(l1))
            vo.wait_until("c")
            self.play(Write(f2), FadeIn(l2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in res], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

