from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import DECAY, DELTA, K, PART, Q, SSM_C, STATE, V, load

GATE = C.SURPRISE  # the gate alpha


def sci(x: float) -> str:
    """3.1e-15 as TeX: 3 \\times 10^{-15}."""
    m, e = f"{x:.0e}".split("e")
    return rf"{m} \times 10^{{{int(e)}}}"


def parity_picture() -> VGroup:
    """Parity as a light switch: the bits so far, and a lamp that flips at every 1 (lit = odd)."""
    bits = [1, 0, 1, 1, 0, 1]
    cols = VGroup()
    on = 0
    for b in bits:
        on ^= b
        lamp = Circle(radius=0.17, stroke_color=C.BITS, stroke_width=2, fill_color=C.BITS, fill_opacity=0.9 if on else 0.0)
        cols.add(VGroup(MathTex(str(b), font_size=30, color=WHITE), lamp,
                        label(r"odd" if on else r"even", font_size=18, color=C.BITS if on else GREY_B)).arrange(DOWN, buff=0.12))
    cols.arrange(RIGHT, buff=0.35)
    flips = VGroup(*[Arrow(a[1].get_right(), b_[1].get_left(), buff=0.05, color=DELTA if bits[i + 1] else GREY_D,
                           stroke_width=2.5, max_tip_length_to_length_ratio=0.35)
                     for i, (a, b_) in enumerate(zip(cols[:-1], cols[1:]))])
    return VGroup(cols, flips)


class GatedDelta(VoiceoverScene):
    def construct(self):
        self.card()
        self.geometry()
        self.family()

    def card(self):
        card = chapter_card(6, r"The delta rule as geometry", r"How do Qwen3-Next and Kimi Linear write to memory?",
                            lit=(1960,), part=PART)
        with self.voiceover("Chapter six. The delta rule as geometry."):
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

        def square(M, r=1.0):  # the square [-r, r]^2 carried by the map: a filled patch, so the map is seen acting
            return Polygon(*[P(M @ c_) for c_ in ([-r, -r], [r, -r], [r, r], [-r, r])], stroke_width=0, fill_color=STATE,
                           fill_opacity=0.28)

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
        neg = label(r"with $\beta$ up to $2$, \ the memory can flip signs: \\ enough to track parity, \ as in Part 28",
                    font_size=20, color=GREY_A).next_to(steps, DOWN, buff=0.3).align_to(steps, LEFT)
        par = gloss(r"parity", r"is the count of $1$s so far odd or even? \\ a switch that flips at every $1$: "
                    r"$\beta = 2$'s reflection is that flip", parity_picture(), width=5.6, color=DELTA)
        par.move_to([-3.4, -0.3, 0])
        # what the memory does: a key goes in, an answer comes out (shown until the update rule takes its place)
        mp = VGroup(label(r"the memory $S$: \ a linear map", font_size=26, color=STATE),
                    MathTex(r"k", r"\;\longmapsto\;", r"S\,k", font_size=40),
                    label(r"key in, \ answer out", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.2).move_to([3.4, 2.1, 0])
        mp[1][0].set_color(K)
        mp[1][2].set_color(STATE)
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
            "these memories track parity, the very problem part twenty-eight's transformer could not solve in one go. "
            "<bookmark mark='f'/> Parity asks: is the count of ones so far odd or even? It's a light switch that "
            "flips at every one, and a reflection is exactly that flip."
        ) as vo:
            gI, sq = grid(np.eye(2)), square(np.eye(2))
            self.play(FadeIn(base), FadeIn(sq), Create(gI), FadeIn(cite_), FadeIn(mp[0]), run_time=1.5)
            self.play(FadeIn(mp[1:]))
            vo.wait_until("p")
            self.play(ReplacementTransform(gI, gS), Transform(sq, square(S0)), run_time=2.0)
            vo.wait_until("a")
            self.play(GrowArrow(ak), FadeIn(kl), GrowArrow(ans), FadeIn(al))
            self.play(Create(tgt), FadeIn(tip), FadeIn(vl), GrowArrow(ap), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeOut(mp), Write(f), FadeIn(e1))
            vo.wait_until("c")
            cur = S0
            for i, b in enumerate((0.5, 1.0, 2.0)):
                if i:
                    vo.wait_until("d" if b == 1.0 else "e")
                M = Ss[b]
                self.play(Transform(gS, grid(M)), Transform(sq, square(M)), Transform(ans, arrow(M @ k, STATE)),
                          al.animate.next_to(P(M @ k), LEFT if b == 2.0 else RIGHT, buff=0.1), Transform(ap, arrow(M @ perp, GREY_B, 3)),
                          FadeIn(steps[i]), run_time=1.8)
                cur = M
            self.play(FadeIn(neg))
            vo.wait_until("f")
            self.play(FadeIn(par, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        colors = {r"S_{t-1}": STATE, r"S_t": STATE, r"k_t^{\top}": K, r"k_t": K, r"v_t": V, r"\beta_t": DELTA,
                  r"\alpha_t": GATE, r"\mathrm{Diag}(\alpha_t)": GATE, r"C_t": STATE, r"C_{t-1}": STATE, r"f_t": GATE,
                  r"i_t": DELTA}
        rows_ = [
            (r"linear attention", (r"S_t", "=", r"S_{t-1}", "+", r"v_t", r"k_t^{\top}"), r"chapter 3", C.SURPRISE),
            (r"decay \ (Mamba-2, \ GLA)", (r"S_t", "=", r"\alpha_t", r"S_{t-1}", "+", r"v_t", r"k_t^{\top}"), r"forgets everything a little",
             DECAY),
            (r"delta rule \ (DeltaNet)", (r"S_t", "=", r"S_{t-1}", r"(I - ", r"\beta_t", r"k_t", r"k_t^{\top}", ")", "+", r"\beta_t",
                                          r"v_t", r"k_t^{\top}"), r"edits one direction", DELTA),
            (r"gated delta \ (Qwen3-Next)", (r"S_t", "=", r"S_{t-1}", r"\,", r"\alpha_t", r"(I - ", r"\beta_t", r"k_t", r"k_t^{\top}", ")",
                                             "+", r"\beta_t", r"v_t", r"k_t^{\top}"), r"both", C.BITS),
            (r"Kimi Delta Attention", (r"S_t", "=", r"S_{t-1}", r"\,", r"\mathrm{Diag}(\alpha_t)", r"(I - ", r"\beta_t", r"k_t",
                                       r"k_t^{\top}", ")", "+", r"\beta_t", r"v_t", r"k_t^{\top}"), r"each channel its own gate",
             C.NEURAL),
            (r"mLSTM \ (xLSTM)", (r"C_t", "=", r"f_t", r"C_{t-1}", "+", r"i_t", r"v_t", r"k_t^{\top}"),
             r"Part 10's LSTM, \ a matrix for a cell", SSM_C),
            (r"RWKV-7", (r"S_t", "=", r"S_{t-1}", r"\big(\mathrm{Diag}(w_t) - \hat\kappa_t (a_t \odot \hat\kappa_t)^{\top}\big)", "+",
                         r"v_t", r"k_t^{\top}"), r"erase along one key, \ write along another", "#F48FB1"),
        ]
        rows = VGroup()
        for i, (name, parts, note_, col) in enumerate(rows_):
            y = 2.95 - i * 0.66
            nm = label(name, font_size=21, color=col).move_to([-5.0, y, 0])
            eq = cmath(*parts, colors=colors, font_size=26).move_to([-3.25, y, 0], aligned_edge=LEFT)
            nt = label(note_, font_size=17, color=GREY_B)
            nt.move_to([6.85 - nt.width / 2, y, 0])
            rows.add(VGroup(nm, eq, nt))
        common = cmath(r"S_t", "=", r"S_{t-1}", r"\,M_t", "+", r"\text{(write)}", colors=colors, font_size=30).to_edge(DOWN, buff=1.05)
        cl = label(r"every one: \ the old memory times a transition $M_t$, \ plus a write; \ "
                   r"$M_t$ is a diagonal plus a low-rank matrix", font_size=20, color=GREY_A).next_to(common, DOWN, buff=0.12)
        cite_ = cite(r"Yang et al.\ (2025); \ Kimi Team (2025); \ Dao \& Gu (2024); \ Beck et al., \textit{xLSTM} (2024); \ "
                     r"Peng et al., \textit{RWKV-7} (2025)", corner=DR, font_size=16)
        with self.voiceover(
            "Now the whole family side by side. <bookmark mark='a'/> Linear attention only adds. Decay, as in "
            "Mamba-2 and gated linear attention, shrinks the whole memory by alpha before each write: everything "
            "fades a little. <bookmark mark='b'/> The delta rule edits only the direction of the current key. "
            "<bookmark mark='c'/> The gated delta rule does both: a decay alpha to clear the memory out when the "
            "topic changes, and a delta step to correct one fact at a time. That's the rule in three of every four "
            "layers of Qwen3-Next. <bookmark mark='d'/> Kimi Linear's version gives each channel of the memory, each of its feature "
            "dimensions, its own decay, a diagonal matrix instead of one number, so some features fade fast and others hold for "
            "thousands of tokens. <bookmark mark='f'/> Two more members came by their own roads. The matrix LSTM of "
            "xLSTM, from Sepp Hochreiter's group in 2024, is Part 10's LSTM with a matrix for its memory cell: a "
            "decaying memory with an exponential gate on what it writes. <bookmark mark='g'/> RWKV-7, from Bo Peng and "
            "the RWKV community in 2025, generalizes the delta rule: a decay for every channel, and a learned rate, "
            "channel by channel, at which it erases along one key before writing along another. Its authors prove "
            "that it can track the state of any finite automaton, which, under standard assumptions, a transformer of "
            "fixed depth cannot. "
            "<bookmark mark='e'/> Written this way, every member is the same shape: the old "
            "memory times a transition matrix, plus a write, and the transition is always a diagonal plus a "
            "low-rank part. That shape is what makes them fast to train."
        ) as vo:
            for r_ in rows[2:]:  # the whole family is there from the start, faint; each lights up in turn
                r_.set_opacity(0.15)
            self.play(FadeIn(cite_), FadeIn(rows))
            vo.wait_until("a")
            self.play(Indicate(rows[0][0], color=C.SURPRISE), Indicate(rows[1][0], color=DECAY))
            vo.wait_until("b")
            self.play(rows[2].animate.set_opacity(1))
            vo.wait_until("c")
            self.play(rows[3].animate.set_opacity(1))
            self.play(Indicate(rows[3][0], color=C.BITS))
            vo.wait_until("d")
            self.play(rows[4].animate.set_opacity(1))
            vo.wait_until("f")
            self.play(rows[5].animate.set_opacity(1))
            vo.wait_until("g")
            self.play(rows[6].animate.set_opacity(1))
            vo.wait_until("e")
            self.play(Write(common), FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()
