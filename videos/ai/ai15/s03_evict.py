from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import fmt_int, ATT, HIST, PART, axes, heat_fixed, heat_image, load

POL_C = {"full": GREY_B, "window": C.SURPRISE, "sinks": C.INTERVAL, "h2o": C.BITS, "ref": WHITE}
POL_NAME = {"full": r"keep everything", "window": r"the last $W$ tokens", "sinks": r"4 sinks $+$ the last $W-4$",
            "h2o": r"heavy hitters $+$ recent"}


def masks(T=32, w=6, glob=(0, 1), rnd=2, seed=0):
    """Attention patterns, row = query, column = key (1 = attended): full causal; a sliding window (Longformer's
    local attention); the window plus a few global tokens; BigBird's window, global and random keys."""
    g = np.random.default_rng(seed)
    i, j = np.indices((T, T))
    causal = (j <= i).astype(float)
    window = ((i - j < w) & (j <= i)).astype(float)
    glob_m = window.copy()
    for c in glob:
        glob_m[:, c] = causal[:, c]
    big = glob_m.copy()
    for r in range(T):
        if r > w:
            big[r, g.choice(r - w + 1, min(rnd, r - w + 1), replace=False)] = 1
    return causal, window, glob_m, big


def smooth(x, n=100):
    x = np.asarray(x, float)
    c = np.cumsum(np.insert(x, 0, 0))
    out = np.empty(len(x))
    for t in range(len(x)):
        lo = max(0, t - n + 1)
        out[t] = (c[t + 1] - c[lo]) / (t + 1 - lo)
    return out


class Evict(VoiceoverScene):
    def construct(self):
        self.card()
        self.patterns()
        self.sinks()
        self.measured()
        self.heavy()

    def card(self):
        card = chapter_card(2, r"Keeping less of the cache", r"Which tokens can a model forget?", part=PART)
        with self.voiceover("Chapter two. Keeping less of the cache."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def patterns(self):
        ms = masks()
        names = [r"full: \ every earlier token", r"a window \ (Sparse Transformer, \ Longformer)",
                 r"window $+$ global tokens \ (Longformer)", r"$+$ random keys \ (BigBird)"]
        cols = [ATT, C.SURPRISE, C.INTERVAL, C.BITS]
        imgs = Group()
        for M, nm, c_ in zip(ms, names, cols):
            im = heat_image(M, 2.85, 2.85, color=c_, gamma=1.0, mask_upper=True)
            t = label(nm, font_size=18, color=c_).next_to(im, DOWN, buff=0.15)
            if t.width > 3.0:
                t.width = 3.0
            imgs.add(Group(im, SurroundingRectangle(im, buff=0, color=GREY_D, stroke_width=1), t))
        imgs.arrange(RIGHT, buff=0.3).move_to(UP * 0.55)
        ax_l = label(r"row: \ the token reading; \ column: \ the tokens it may look at", font_size=20, color=GREY_B)
        ax_l.next_to(imgs, UP, buff=0.25)
        cost = label(r"keys read per token: \ $t$ \ $\rightarrow$ \ a fixed $W$ \ (plus a few globals)", font_size=24,
                     color=WHITE).next_to(imgs, DOWN, buff=0.35)
        # Transformer-XL: the previous segment's states, kept and read (without gradients)
        segs = VGroup(*[Rectangle(width=2.2, height=0.42, stroke_color=GREY_B, stroke_width=1.5, fill_color=HIST,
                                  fill_opacity=0.12 + 0.12 * k) for k in range(4)]).arrange(RIGHT, buff=0.12)
        arcs = VGroup(*[CurvedArrow(segs[k].get_top() + UP * 0.03, segs[k + 1].get_top() + UP * 0.03, angle=-PI / 3,
                                    color=HIST, stroke_width=2.5, tip_length=0.12) for k in range(3)])
        sl = label(r"Transformer-XL: \ each segment reads the cached states of the one before; \ $L$ layers reach "
                   r"$L$ segments back", font_size=20, color=HIST)
        xl = VGroup(segs, arcs, sl.next_to(segs, DOWN, buff=0.12)).to_edge(DOWN, buff=0.35)
        tag = note(r"schematic").to_corner(UR, buff=0.25)
        cite_ = cite(r"R.~Child et al.\ (2019); \ Z.~Dai et al., \textit{Transformer-XL} (2019); \ I.~Beltagy et al., "
                     r"\textit{Longformer} (2020); \ M.~Zaheer et al., \textit{BigBird} (2020)", corner=UL, font_size=16)
        with self.voiceover(
            "The cache can't grow forever, so the first question is which tokens a model can do without. "
            "<bookmark mark='a'/> Full attention lets every token look at every earlier one. In 2019 Rewon Child's "
            "Sparse Transformer looked only at a window of recent tokens, plus a strided pattern, "
            "<bookmark mark='b'/> and in 2020 Longformer kept a window and added a few global tokens that see and are "
            "seen by everything. <bookmark mark='c'/> BigBird added a few random keys too, and proved that this "
            "sparse pattern can still compute anything full attention can. <bookmark mark='d'/> Each token now "
            "reads a fixed number of keys, so the cache stops growing. <bookmark mark='e'/> Transformer-XL, in 2019, "
            "went the other way: it cached the previous segment's states and let each segment read them, so a stack "
            "of layers reaches many segments back."
        ) as vo:
            self.play(FadeIn(ax_l), FadeIn(imgs[0]), FadeIn(cite_), FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(imgs[k + 1], shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(cost))
            vo.wait_until("e")
            self.play(FadeIn(segs), FadeIn(sl))
            self.play(LaggedStart(*[Create(a_) for a_ in arcs], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sinks(self):
        s = load("sinks")
        F = np.asarray(s["first"])
        L_, H_ = F.shape
        uni = float(s["uniform"])
        img = heat_fixed(F, 0.62 * H_, 0.62 * L_, color=C.INTERVAL, vmax=0.5, gamma=0.6).move_to([-3.2, -0.5, 0])
        fr = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1)
        vals = VGroup()
        for li in range(L_):
            for hh in range(H_):
                c = img.get_corner(UL) + np.array([0.62 * (hh + 0.5), -0.62 * (li + 0.5), 0])
                vals.add(MathTex(f"{100 * F[li, hh]:.0f}", font_size=17,
                                 color=BLACK if F[li, hh] > 0.25 else GREY_A).move_to(c))
        rl = VGroup(*[label(rf"layer {li + 1}", font_size=16, color=GREY_B).next_to(img.get_corner(UL) + DOWN * 0.62 * (li + 0.5),
                                                                               LEFT, buff=0.12) for li in range(L_)])
        hl = label(rf"heads $1$--${H_}$", font_size=16, color=GREY_B).next_to(img, UP, buff=0.1)
        head = label(r"the series' model: \ \% of each head's attention on the first token", font_size=24).to_edge(UP, buff=0.35)
        n_sink = int((F > 10 * uni).sum())
        mean = float(F.mean())
        k1 = label(rf"if attention were spread evenly: \ ${100 * uni:.1f}\%$", font_size=22, color=GREY_A)
        k2 = label(rf"heads above ten times that: \ ${n_sink}$ of ${L_ * H_}$", font_size=22, color=C.INTERVAL)
        k3 = label(rf"average over all heads: \ ${100 * mean:.0f}\%$", font_size=22, color=WHITE)
        keys = VGroup(k1, k2, k3).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.4, 0])
        note_ = note(rf"$24$ held-out windows of ${int(s['seq'])}$ tokens, \\ queries from position $64$ on").next_to(keys, DOWN, buff=0.4).align_to(keys, LEFT)
        cite_ = cite(r"G.~Xiao et al., \textit{Efficient Streaming Language Models with Attention Sinks} (2023)", corner=DR)
        strong = n_sink >= 0.25 * L_ * H_
        verdict = (f"{n_sink} of its {L_ * H_} heads put more than ten times that on the first token, and on "
                   f"average a head gives it {100 * mean:.0f} percent: sinks, as in the large models."
                   if strong else
                   f"only {n_sink} of its {L_ * H_} heads put more than ten times that on the first token; on average "
                   f"a head gives it {100 * mean:.0f} percent. Our small model leans on the first token less than the "
                   "large ones do." if n_sink > 0 else
                   f"not one of its {L_ * H_} heads gives the first token even ten times that; on average a head gives "
                   f"it {100 * mean:.1f} percent. This model never grew a sink: trained on windows cut at random from "
                   "the novels, it found other places to park.")
        with self.voiceover(
            "A sliding window has a hidden flaw, found in 2023 by Guangxuan Xiao and colleagues. Part 13 showed that "
            "many heads park their attention on the very first token, an attention sink, when they have nothing "
            "to do. <bookmark mark='a'/> Here is the series' own model, the one trained on the thirty novels: each "
            "square is a head, and the number is the share of its attention that lands on the first token of the "
            f"window. <bookmark mark='b'/> Spread evenly, the first token would get {100 * uni:.1f} percent. Instead, "
            + verdict
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(img), Create(fr), FadeIn(rl), FadeIn(hl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(v_) for v_ in vals], lag_ratio=0.01))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k_, shift=RIGHT * 0.1) for k_ in keys], lag_ratio=0.5), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        s = load("sinks")
        n = int(s["n"])
        W = 64
        ref = np.asarray(s["ref"])
        series = [("ref", ref, r"windows of $256$, recomputed \ (Part 14's scoring)")]
        for p in ("window", "sinks", "full"):
            key = f"{p}_{W if p != 'full' else 0}"
            series.append((p, np.asarray(s[f"loss_{key}"]), POL_NAME[p].replace("$W$", f"${W}$").replace("$W-4$", f"${W - 4}$")))
        sm = {p: smooth(x, 100) for p, x, _ in series}
        top = math.ceil(max(float(v[150:].max()) for v in sm.values()) * 2) / 2
        lo = math.floor(min(float(v[150:].min()) for v in sm.values()) * 2) / 2
        g = axes([0, n], [lo, top], x_length=8.2, y_length=4.2, xlabel=r"position in the passage \ (tokens)",
                 ylabel=r"loss on the next token \ (nats, \ average of the last 100)", xticks=[0, 256, 1000, 2000],
                 yticks=[lo, (lo + top) / 2, top], center=[-1.9, -0.45, 0], yfmt=lambda v: f"{v:g}")
        ax = g.ax
        lines = VGroup(*[curve(ax, np.arange(len(sm[p]))[20:], np.clip(sm[p][20:], lo, top), POL_C[p], 3) for p, _, _ in series])
        leg = legend([(POL_C[p], t) for p, _, t in series], font_size=17).move_to([4.6, 1.6, 0])
        trained = DashedLine(ax.c2p(256, lo), ax.c2p(256, top), dash_length=0.06, color=GREY_B, stroke_width=1.5)
        tl = label(r"trained on $256$", font_size=16, color=GREY_B).next_to(trained, UP, buff=0.05)
        bits = {p: float(s[f"bits_{p}_{W if p != 'full' else 0}"]) for p in ("window", "sinks", "full")}
        br = float(s["bits_ref"])
        bars = VGroup(*[label(rf"{POL_NAME[p].replace('$W$', f'${W}$').replace('$W-4$', f'${W - 4}$')}: \ ${bits[p]:.3f}$",
                              font_size=18, color=POL_C[p]) for p in ("window", "sinks", "full")],
                      label(rf"recomputed windows: \ ${br:.3f}$", font_size=18, color=WHITE))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.6, -1.5, 0])
        bh = label(rf"bits per character, \ first ${fmt_int(n)}$ tokens", font_size=18, color=GREY_A)
        bh.next_to(bars, UP, buff=0.15).align_to(bars, LEFT)
        hurt = bits["window"] - bits["sinks"]
        v1 = (f"Keep only the last {W} tokens, and once the first token is evicted the loss jumps, and it stays "
              f"high: {bits['window']:.2f} bits per character. " if hurt > 0.05 else
              f"Keep only the last {W} tokens, and the loss barely moves when the first token is evicted: "
              f"{bits['window']:.2f} bits per character. ")
        v2 = (f"Keep the first four tokens as well, and it recovers: {bits['sinks']:.2f}, close to recomputing every "
              f"window from scratch, {br:.2f}. " if hurt > 0.05 else
              f"Keeping the first four tokens as well gives {bits['sinks']:.2f}, and recomputing every window from "
              f"scratch {br:.2f}: with no sink to lose, this model doesn't need them. ")
        v3 = (f"And keeping everything fails differently: past position 256 the model meets positions it never "
              f"saw in training, and ends at {bits['full']:.2f}. That is why long windows need the context extension "
              "of Part 13." if bits["full"] > br + 0.1 else
              f"Keeping everything, with positions beyond the 256 it trained on, gives {bits['full']:.2f}: rotary "
              "positions stretch a little further than they were trained, here.")
        cite_ = cite(r"StreamingLLM keeps $4$ sink tokens: \ stable for $4$ million tokens \ (Xiao et al.\ 2023)", corner=UL,
                     font_size=17)
        with self.voiceover(
            "That matters for the cache. We had the series' model read the first "
            f"{n:,} tokens of the scoreboard's passage one at a time, as a server would, with room for only {W} "
            "tokens of keys and values per head, positions counted inside the cache. <bookmark mark='a'/> " + v1
            + "<bookmark mark='b'/> " + v2 + "<bookmark mark='c'/> " + v3
        ) as vo:
            self.play(FadeIn(g), Create(trained), FadeIn(tl), FadeIn(cite_))
            self.play(Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(leg[1]), FadeIn(bh), FadeIn(bars[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[2]), FadeIn(leg[2]), FadeIn(bars[1]), FadeIn(bars[3]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines[3]), FadeIn(leg[3]), FadeIn(bars[2]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heavy(self):
        s = load("sinks")
        B = [int(b) for b in s["budgets"]]
        br = float(s["bits_ref"])
        pols = ("window", "sinks", "h2o")
        vals = {p: [float(s[f"bits_{p}_{b}"]) for b in B] for p in pols}
        lo = math.floor(min(min(v) for v in vals.values()) * 5 - 0.5) / 5
        hi = math.ceil(max(min(max(v), br + 1.5) for v in vals.values()) * 5) / 5
        g = axes([0, len(B)], [lo, hi], x_length=7.0, y_length=4.0,
                 ylabel=r"bits per character", yticks=[lo, (lo + hi) / 2, hi], center=[-2.4, -0.5, 0],
                 yfmt=lambda v: f"{v:.1f}")
        ax = g.ax
        xt = VGroup(*[MathTex(str(b), font_size=20, color=GREY_B).next_to(ax.c2p(i + 0.5, lo), DOWN, buff=0.12)
                      for i, b in enumerate(B)])
        xt.add(label(r"cache: \ tokens kept per head", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.5))
        bw = 0.6
        bars = VGroup()
        for i, b in enumerate(B):
            for j, p in enumerate(pols):
                v = min(vals[p][i], hi)
                x = ax.c2p(i + 0.5, lo)[0] + (j - 1) * (bw + 0.05)
                y0, y1 = ax.c2p(0, lo)[1], ax.c2p(0, v)[1]
                bars.add(Rectangle(width=bw, height=max(y1 - y0, 0.02), stroke_width=0, fill_color=POL_C[p],
                                   fill_opacity=0.85).move_to([x, (y0 + y1) / 2, 0]))
        refl = DashedLine(ax.c2p(0, br), ax.c2p(len(B), br), dash_length=0.08, color=WHITE, stroke_width=1.5)
        rl = label(r"recomputed windows of $256$", font_size=16, color=WHITE).next_to(refl, UP, buff=0.05).align_to(refl, RIGHT)
        leg = legend([(POL_C[p], POL_NAME[p].replace("$W$", r"$W$")) for p in pols], font_size=18).move_to([4.4, 1.6, 0])
        colors = {r"\sum_{t}": WHITE, r"a_{t,j}": ATT}
        f = cmath(r"\text{score}(j)", "=", r"\sum_{t}", r"a_{t,j}", colors=colors, font_size=34).move_to([4.4, -0.1, 0])
        fl = label(r"the attention token $j$ has drawn so far: \\ evict the smallest, \ but never the recent half",
                   font_size=18, color=GREY_A).next_to(f, DOWN, buff=0.2)
        cite_ = cite(r"Z.~Zhang et al., \textit{H$_2$O: Heavy-Hitter Oracle} (2023): \ $20\%$ heavy hitters, \ up to "
                     r"$29\times$ throughput", corner=DR, font_size=17)
        bh, bs, bwd = vals["h2o"], vals["sinks"], vals["window"]
        best = min(pols, key=lambda p: vals[p][0])
        name = {"window": "the plain window", "sinks": "sinks plus a window", "h2o": "the heavy hitters"}
        v = (f"With the smallest cache, {B[0]} tokens, {name[best]} does best: heavy hitters "
             f"{bh[0]:.2f} bits per character, sinks {bs[0]:.2f}, the plain window {bwd[0]:.2f}. ")
        v_b = (f"With {B[-1]} tokens all three are close to recomputing, {br:.2f}, and the choice hardly matters."
               if max(bh[-1], bs[-1]) - br < 0.08 else
               f"Even with {B[-1]} tokens they stay above recomputing, {br:.2f}.")
        with self.voiceover(
            "A second idea, H2O from Zhenyu Zhang and colleagues, also in 2023, is to keep the tokens that matter. "
            "<bookmark mark='a'/> Add up the attention each cached token has drawn so far; when the cache is full, "
            "evict the one with the least, but always keep the most recent half. A few heavy hitters draw most of "
            "the attention, and the sink is one of them. <bookmark mark='b'/> Here are the three policies on the "
            "same passage, with caches of " + f"{B[0]}, {B[1]} and {B[2]} tokens per head. " + v
            + "<bookmark mark='d'/> " + v_b + " <bookmark mark='c'/> Evicting is a guess about the future made from the past: a token that seemed "
            "unimportant may be the one a later question needs. Part 16 chooses tokens by content instead."
        ) as vo:
            self.play(FadeIn(g), FadeIn(xt), FadeIn(cite_), Create(refl), FadeIn(rl))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(leg), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("d")
            self.play(Indicate(bars, color=WHITE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(Indicate(fl, color=C.BITS, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()
