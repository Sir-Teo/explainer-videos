from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import heat_image
from videos.ai.ai12.common import DECAY, DELTA, K, Q, STATE, V, load

GATE = C.SURPRISE  # the gate alpha


def sci(x: float) -> str:
    """3.1e-15 as TeX: 3 \\times 10^{-15}."""
    m, e = f"{x:.0e}".split("e")
    return rf"{m} \times 10^{{{int(e)}}}"


class GatedDelta(VoiceoverScene):
    def construct(self):
        self.card()
        self.geometry()
        self.family()
        self.parallel()
        self.duality()

    def card(self):
        card = chapter_card(5, r"The gated delta rule", r"How do Qwen3-Next and Kimi Linear write to memory?", part=12)
        with self.voiceover("Chapter five. The gated delta rule."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def geometry(self):
        d = load("delta")
        S0, k, v = np.asarray(d["geo_S0"]), np.asarray(d["geo_k"]), np.asarray(d["geo_v"])
        Ss = {b: np.asarray(d[f"geo_S{b:g}"]) for b in (0.5, 1.0, 2.0)}
        O, u = np.array([-3.4, -0.3]), 1.1

        def P(x):
            return np.array([O[0] + u * x[0], O[1] + u * x[1], 0.0])

        def grid(M, r=1.0, n=5):
            g = VGroup()
            for s in np.linspace(-r, r, n):
                g.add(Line(P(M @ [s, -r]), P(M @ [s, r]), stroke_width=1.2, color=STATE).set_stroke(opacity=0.45))
                g.add(Line(P(M @ [-r, s]), P(M @ [r, s]), stroke_width=1.2, color=STATE).set_stroke(opacity=0.45))
            return g

        def arrow(x, color, sw=5):
            return Arrow(P([0, 0]), P(x), buff=0, color=color, stroke_width=sw, max_tip_length_to_length_ratio=0.15)

        perp = np.array([-k[1], k[0]])
        base = VGroup(*[Line(P([s, -2.5]), P([s, 2.5]), stroke_width=1, color=GREY_D) for s in np.linspace(-2.5, 2.5, 11)],
                      *[Line(P([-3.0, s]), P([3.0, s]), stroke_width=1, color=GREY_D) for s in np.linspace(-2.5, 2.5, 11)])
        gS = grid(S0)
        ak = arrow(k, K, 4)
        kl = MathTex(r"k", font_size=34, color=K).next_to(P(k), UR, buff=0.05)
        ans = arrow(S0 @ k, STATE)
        al = MathTex(r"S k", font_size=34, color=STATE).next_to(P(S0 @ k), RIGHT, buff=0.1)
        tgt = DashedLine(P([0, 0]), P(v), color=V, stroke_width=4, dash_length=0.1)
        tip = Dot(P(v), radius=0.07, color=V)
        vl = MathTex(r"v", font_size=34, color=V).next_to(P(v), UL, buff=0.05)
        ap = arrow(S0 @ perp, GREY_B, 3)
        pl = VGroup(Line(ORIGIN, RIGHT * 0.5, color=GREY_B, stroke_width=3),
                    label(r"the answer for the direction at right angles to $k$: \\ it never moves", font_size=20, color=GREY_B))
        pl.arrange(RIGHT, buff=0.15).move_to([3.4, -2.75, 0])
        colors = {r"S_{t-1}": STATE, r"S_t": STATE, r"k_t": K, r"k_t^{\top}": K, r"v_t": V, r"\beta_t": DELTA}
        f = cmath(r"S_t", "=", r"S_{t-1}", r"\big(I - ", r"\beta_t", r"\,", r"k_t", r"k_t^{\top}", r"\big)", "+", r"\beta_t",
                  r"\,", r"v_t", r"k_t^{\top}", colors=colors, font_size=36).move_to([3.4, 2.6, 0])
        e1 = label(r"$I - \beta\, k k^{\top}$: \ stretches the direction $k$ by $1 - \beta$, \\ leaves every direction "
                   r"at right angles to $k$ alone", font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.25)
        steps = VGroup(label(r"$\beta = \tfrac12$: \ halfway to $v$", font_size=24, color=DELTA),
                       label(r"$\beta = 1$: \ the old answer erased, \ exactly $v$ \\ (a projection)", font_size=24, color=DELTA),
                       label(r"$\beta = 2$: \ past $v$, \ a reflection \\ (eigenvalue $-1$)", font_size=24, color=DELTA))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.5, 0])
        neg = label(r"with $\beta$ up to $2$, \ the memory can flip signs: \\ enough to track parity, \ as in Part 17",
                    font_size=20, color=GREY_A).next_to(steps, DOWN, buff=0.3).align_to(steps, LEFT)
        cite_ = cite(r"S.~Yang et al., \textit{Gated Delta Networks} (2025); \ R.~Grazzi et al., \textit{Unlocking State-Tracking "
                     r"in Linear RNNs Through Negative Eigenvalues} (2025)", corner=DR)
        with self.voiceover(
            "Let's look at the delta rule as geometry. The memory S is a linear map: give it a key, and it gives back "
            "an answer. <bookmark mark='p'/> Here it is acting on the plane. <bookmark mark='a'/> Feed it the key k, and it answers S k, "
            "but the value we want stored is v. <bookmark mark='b'/> The update multiplies S by I minus beta k k "
            "transpose, then adds beta v k transpose. That first matrix only touches the direction k: it shrinks it "
            "by one minus beta, and leaves every direction at right angles alone. <bookmark mark='c'/> With beta a "
            "half, the answer for k moves halfway to v, and the answer for the perpendicular direction doesn't move "
            "at all. <bookmark mark='d'/> With beta one, the old answer is erased exactly and replaced by v: a "
            "projection. <bookmark mark='e'/> And with beta up to two, it overshoots into a reflection, a matrix with "
            "eigenvalue minus one. That sounds like a bug, but it's a feature: Grazzi and colleagues showed it lets "
            "these memories track parity, the very problem part seventeen's transformer could not solve in one go."
        ) as vo:
            gI = grid(np.eye(2))
            self.play(FadeIn(base), Create(gI), FadeIn(cite_), run_time=1.5)
            vo.wait_until("p")
            self.play(ReplacementTransform(gI, gS), run_time=2.0)
            vo.wait_until("a")
            self.play(GrowArrow(ak), FadeIn(kl), GrowArrow(ans), FadeIn(al))
            self.play(Create(tgt), FadeIn(tip), FadeIn(vl), GrowArrow(ap), FadeIn(pl))
            vo.wait_until("b")
            self.play(Write(f), FadeIn(e1))
            vo.wait_until("c")
            cur = S0
            for i, b in enumerate((0.5, 1.0, 2.0)):
                if i:
                    vo.wait_until("d" if b == 1.0 else "e")
                M = Ss[b]
                self.play(Transform(gS, grid(M)), Transform(ans, arrow(M @ k, STATE)),
                          al.animate.next_to(P(M @ k), LEFT if b == 2.0 else RIGHT, buff=0.1), Transform(ap, arrow(M @ perp, GREY_B, 3)),
                          FadeIn(steps[i]), run_time=1.8)
                cur = M
            self.play(FadeIn(neg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        colors = {r"S_{t-1}": STATE, r"S_t": STATE, r"k_t^{\top}": K, r"k_t": K, r"v_t": V, r"\beta_t": DELTA,
                  r"\alpha_t": GATE, r"\mathrm{Diag}(\alpha_t)": GATE}
        rows_ = [
            (r"linear attention", (r"S_t", "=", r"S_{t-1}", "+", r"v_t", r"k_t^{\top}"), r"Part 12, chapter 2", C.SURPRISE),
            (r"decay \ (Mamba-2, \ GLA)", (r"S_t", "=", r"\alpha_t", r"S_{t-1}", "+", r"v_t", r"k_t^{\top}"), r"forgets everything a little",
             DECAY),
            (r"delta rule \ (DeltaNet)", (r"S_t", "=", r"S_{t-1}", r"(I - ", r"\beta_t", r"k_t", r"k_t^{\top}", ")", "+", r"\beta_t",
                                          r"v_t", r"k_t^{\top}"), r"edits one direction", DELTA),
            (r"gated delta \ (Qwen3-Next)", (r"S_t", "=", r"S_{t-1}", r"\,", r"\alpha_t", r"(I - ", r"\beta_t", r"k_t", r"k_t^{\top}", ")",
                                             "+", r"\beta_t", r"v_t", r"k_t^{\top}"), r"both", C.BITS),
            (r"Kimi Delta Attention", (r"S_t", "=", r"S_{t-1}", r"\,", r"\mathrm{Diag}(\alpha_t)", r"(I - ", r"\beta_t", r"k_t",
                                       r"k_t^{\top}", ")", "+", r"\beta_t", r"v_t", r"k_t^{\top}"), r"each channel its own gate",
             C.NEURAL),
        ]
        rows = VGroup()
        for i, (name, parts, note_, col) in enumerate(rows_):
            y = 2.2 - i * 1.0
            nm = label(name, font_size=24, color=col).move_to([-4.7, y, 0])
            eq = cmath(*parts, colors=colors, font_size=30).move_to([-2.2, y, 0], aligned_edge=LEFT)
            nt = label(note_, font_size=20, color=GREY_B).move_to([5.5, y, 0])
            rows.add(VGroup(nm, eq, nt))
        common = cmath(r"S_t", "=", r"S_{t-1}", r"\,M_t", "+", r"\text{(write)}", colors=colors, font_size=34).to_edge(DOWN, buff=1.25)
        cl = label(r"every one: \ the old memory times a transition $M_t$, \ plus a write; \ "
                   r"$M_t$ is a diagonal plus a low-rank matrix", font_size=22, color=GREY_A).next_to(common, DOWN, buff=0.15)
        cite_ = cite(r"S.~Yang et al.\ (2025); \ Kimi Team, \textit{Kimi Linear} (2025); \ T.~Dao \& A.~Gu (2024)", corner=DR)
        with self.voiceover(
            "Now the whole family side by side. <bookmark mark='a'/> Linear attention only adds. Decay, as in "
            "Mamba-2 and gated linear attention, shrinks the whole memory by alpha before each write: everything "
            "fades a little. <bookmark mark='b'/> The delta rule edits only the direction of the current key. "
            "<bookmark mark='c'/> The gated delta rule does both: a decay alpha to clear the memory out when the "
            "topic changes, and a delta step to correct one fact at a time. That's the rule in three of every four "
            "layers of Qwen3-Next. <bookmark mark='d'/> Kimi Linear's version gives each channel of the memory its "
            "own decay, a diagonal matrix instead of one number, so some features fade fast and others hold for "
            "thousands of tokens. <bookmark mark='e'/> Written this way, every member is the same shape: the old "
            "memory times a transition matrix, plus a write, and the transition is always a diagonal plus a "
            "low-rank part. That shape is what makes them fast to train."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(rows[0], shift=RIGHT * 0.2))
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.2))
            self.play(Indicate(rows[3][0], color=C.BITS))
            vo.wait_until("d")
            self.play(FadeIn(rows[4], shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(Write(common), FadeIn(cl))
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
        dp, dg = float(d["diff_plain"]), float(d["diff_gated"])

        res = VGroup(label(rf"step by step \ vs \ by chunks, \ on these ${T:,}$ tokens: \ largest difference "
                           rf"${sci(max(dp, dg))}$".replace(",", "{,}"), font_size=24, color=C.INTERVAL),
                     label(rf"sequential steps: \ ${T:,}$ \ vs \ ${nC}$ \ (each chunk is matrix products)".replace(",", "{,}"),
                           font_size=24, color=WHITE)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.55)
        cite_ = cite(r"S.~Yang, B.~Wang, Y.~Zhang, Y.~Shen \& Y.~Kim, \textit{Parallelizing Linear Transformers with the Delta "
                     r"Rule over Sequence Length} (2024)", corner=UR)
        with self.voiceover(
            "But a rule that updates the memory one token at a time looks hopeless to train: thousands of steps, "
            "each waiting for the last, while the hardware wants big matrix products. <bookmark mark='a'/> The way "
            "out is to cut the text into chunks of sixty-four and handle each chunk at once. <bookmark mark='b'/> "
            "Within a chunk, the memory gets multiplied by sixty-four of those I minus beta k k transpose matrices. "
            "Their product has a compact form, found by Householder-era numerical analysts: the identity minus a sum "
            "of sixty-four rank-one terms, w times k transpose. <bookmark mark='c'/> And all the w's come from one "
            "triangular solve. With them, a chunk's outputs and its final memory are just matrix products, and the "
            "decay of the gated version folds into the same form. <bookmark mark='d'/> We checked it on our "
            f"computer: for {T} random tokens, step by step and chunk by chunk agree to rounding error, with "
            f"{nC} sequential steps instead of {T}. On this little processor the plain loop is still quicker; on a "
            "GPU, the matrix products win by far, and that's how Qwen3-Next and Kimi Linear were trained."
        ) as vo:
            self.play(FadeIn(chunks), FadeIn(tl), FadeIn(cite_))
            self.add(cursor)
            self.play(cursor.animate.move_to(chunks[3].get_center()), run_time=2.0, rate_func=linear)
            self.remove(cursor)
            vo.wait_until("a")
            self.play(LaggedStart(*[c_.animate.set_fill(STATE, 0.55) for c_ in chunks], lag_ratio=0.03), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(f1), FadeIn(l1))
            vo.wait_until("c")
            self.play(Write(f2), FadeIn(l2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in res], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duality(self):
        d = load("delta")
        L, a = np.asarray(d["ssd_L"]), np.asarray(d["ssd_a"])
        n = L.shape[0]
        S = 4.6
        img = heat_image(L, S, S, color=DECAY, gamma=0.5, mask_upper=True).move_to([-2.5, -0.4, 0])
        frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        il = label(r"the mask $L$: \ row $i$, column $j$ \\ how much of token $j$ is left at step $i$", font_size=22,
                   color=GREY_A).next_to(img, UP, buff=0.15)
        cell = S / n
        blk = Rectangle(width=cell * 16, height=cell * 16, stroke_color=WHITE, stroke_width=2.5)
        blk.move_to(img.get_corner(DL) + np.array([cell * 8, cell * 8, 0]))
        forgets = [int(i) for i in np.where(a < 0.2)[0]]
        marks = VGroup(*[Line(img.get_left() + np.array([0, S / 2 - cell * (i + 0.5), 0]),
                              img.get_left() + np.array([-0.25, S / 2 - cell * (i + 0.5), 0]), color=GATE, stroke_width=4)
                         for i in forgets])
        ml = label(r"the gate forgets", font_size=20, color=GATE).next_to(marks, LEFT, buff=0.1)
        colors = {r"L": DECAY, r"Q": Q, r"K": K, r"V": V, r"a": GATE}
        f1 = cmath(r"O", "=", r"(", r"L", r"\circ", r"Q", r"K", r"^{\top}", r")\,", r"V", colors=colors, font_size=40).move_to([3.9, 1.8, 0])
        f2 = cmath(r"L", r"_{ij} = ", r"a", r"_{j+1}\, ", r"a", r"_{j+2} \cdots ", r"a", r"_i", colors=colors, font_size=36)
        f2.next_to(f1, DOWN, buff=0.35)
        rk = label(rf"every block below the diagonal has rank one \\ (second singular value $/$ first: "
                   rf"${sci(float(d['ssd_rank_ratio']))}$)", font_size=20, color=GREY_A).next_to(f2, DOWN, buff=0.35)
        agree = label(rf"masked attention vs the recurrence: \\ largest difference ${sci(float(d['ssd_diff']))}$",
                      font_size=22, color=C.INTERVAL).next_to(rk, DOWN, buff=0.35)
        msg = label(r"one layer, \ two algorithms: \\ a recurrence to generate, \ masked attention to train", font_size=24,
                    color=WHITE).next_to(agree, DOWN, buff=0.4)
        cite_ = cite(r"T.~Dao \& A.~Gu, \textit{Transformers are SSMs: \ Generalized Models and Efficient Algorithms Through "
                     r"Structured State Space Duality} (2024)", corner=DR)
        with self.voiceover(
            "For the decaying rule there's an even neater view, Mamba-2's state-space duality. <bookmark mark='a'/> "
            "Unroll the recurrence, and every output is a weighted sum of earlier values: exactly attention, with "
            "the query-key scores multiplied by a mask L. <bookmark mark='b'/> Entry i, j of the mask is the "
            "product of the gates between token j and token i: how much of token j survives until step i. Where "
            "the gate forgets, the mask goes dark below that row. <bookmark mark='c'/> That mask is semiseparable: "
            "every block below the diagonal has rank one, because each entry is a product of two numbers, one for "
            "the row and one for the column. <bookmark mark='d'/> We checked: masked attention and the recurrence "
            "agree to rounding error. So the same layer can run as a recurrence while it writes, using constant "
            "memory, and as masked attention while it trains, using big matrix products."
        ) as vo:
            self.play(FadeIn(cite_), Write(f1))
            vo.wait_until("a")
            self.play(FadeIn(img), Create(frame), FadeIn(il))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(marks), FadeIn(ml))
            vo.wait_until("c")
            self.play(Create(blk), FadeIn(rk))
            vo.wait_until("d")
            self.play(FadeIn(agree), FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()
