from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import PART, POS_COLORS, POS_NAMES, bars_chart, curve, load, seed_lines

ORDER = ("sin", "rope", "alibi", "nope")
SPOKEN = {"sin": "sinusoids", "rope": "RoPE", "alibi": "ALiBi", "nope": "no positions at all"}
CAP = {"sin": "Sinusoids", "rope": "RoPE", "alibi": "ALiBi", "nope": "No positions at all"}


def spoken_list(names):
    names = list(names)
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


class SideBySide(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_()
        self.inside()
        self.beyond()
        self.why()

    def card(self):
        card = chapter_card(10, r"Four answers, trained side by side", r"Which way of giving positions reads past its "
                            r"training length?", part=PART)
        with self.voiceover("Chapter ten. Four answers, trained side by side."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def setup_(self):
        p = load("positions")
        c = dict(p["cfg"])
        seeds = list(p["seeds"])
        steps = np.asarray(p["curve_steps"], float)
        lo = min(float(np.asarray(p[f"curve_{m}"]).min()) for m in ORDER)
        hi = max(float(np.asarray(p[f"curve_{m}"])[:, 0].max()) for m in ORDER)
        lo, hi = np.floor(lo * 4) / 4 - 0.1, np.ceil(hi * 2) / 2
        g = axes([0, steps[-1], steps[-1] / 4], [lo, hi, 0.25], x_length=6.8, y_length=4.0,
                 xlabel=r"training steps", ylabel=r"bits per character, \ held-out text, \ $128$ characters",
                 xticks=[0, steps[-1] / 2, steps[-1]], xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"),
                 yticks=[v for v in np.arange(np.ceil(lo * 2) / 2, hi + 0.01, 0.5)], yfmt=lambda v: f"{v:.1f}",
                 center=[-2.8, -0.45, 0])
        ax = g.ax
        lines = {m: seed_lines(ax, steps, np.asarray(p[f"curve_{m}"]), POS_COLORS[m], 3) for m in ORDER}
        key = legend([(POS_COLORS[m], POS_NAMES[m]) for m in ORDER], font_size=22).move_to([4.6, 1.9, 0])
        spec = VGroup(
            label(rf"the same model: \ ${c['L']}$ layers, \ width ${c['d']}$, \ ${c['H']}$ heads", font_size=20, color=GREY_A),
            label(rf"the same text, in the same order: \ ${c['steps']:,}$ steps of ${c['batch']} \times {c['ctx']}$".replace(",", "{,}"),
                  font_size=20, color=GREY_A),
            label(rf"${len(seeds)}$ seeds each: \ lines are means, \\ bands the range", font_size=20, color=GREY_A),
            label(rf"only the positions differ", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, -0.9, 0])
        keep_in_frame(spec)
        # when the ranking settles: the first checkpoint from which the order of the means never changes
        M = {m: np.asarray(p[f"curve_{m}"]).mean(0) for m in ORDER}
        ranks = [tuple(sorted(ORDER, key=lambda m: M[m][i])) for i in range(len(steps))]
        i_fix = next(i for i in range(len(steps)) if all(r_ == ranks[-1] for r_ in ranks[i:]))
        s_fix, s_end = int(steps[i_fix]), int(steps[-1])
        g_fix = float(max(M[m][i_fix] for m in ORDER) - min(M[m][i_fix] for m in ORDER))
        g_end = float(max(M[m][-1] for m in ORDER) - min(M[m][-1] for m in ORDER))
        if i_fix == len(steps) - 1:
            v_train = f"The order keeps changing until the very last checkpoint, step {s_end:,}."
        elif g_end > g_fix:
            v_train = (f"From step {s_fix:,} on, the order never changes, and the gap between best and worst widens, "
                       f"from {g_fix:.2f} bits then to {g_end:.2f} at the end.")
        else:
            v_train = (f"From step {s_fix:,} on, the order never changes, while the gap between best and worst "
                       f"narrows, from {g_fix:.2f} bits then to {g_end:.2f} at the end.")
        fix_line = DashedLine(ax.c2p(s_fix, lo), ax.c2p(s_fix, hi), color=GREY_B, stroke_width=1.5)
        fix_l = label(rf"order fixed \ from step ${s_fix:,}$".replace(",", "{,}"), font_size=18,
                      color=GREY_B).next_to(ax.c2p(s_fix, hi), RIGHT, buff=0.1).shift(DOWN * 0.3)
        ends = VGroup(*[MathTex(f"{M[m][-1]:.2f}", font_size=20, color=POS_COLORS[m]) for m in ORDER])
        for e_, m in zip(ends, ORDER):
            e_.next_to(ax.c2p(steps[-1], M[m][-1]), RIGHT, buff=0.1)
        order_y = sorted(range(len(ORDER)), key=lambda i: -ends[i].get_y())  # keep close end values apart
        for k in range(1, len(order_y)):
            up, dn = ends[order_y[k - 1]], ends[order_y[k]]
            if up.get_bottom()[1] - dn.get_top()[1] < 0.05:
                dn.next_to(up, DOWN, buff=0.05).align_to(up, LEFT)
        with self.voiceover(
            "Now the experiment. Four small transformers, identical except for how they learn where each character "
            "is: sinusoids added to the input, rotary positions, ALiBi's linear penalty, and nothing at all. Here "
            "they are learning, replayed: held-out bits per character, step by step. "
            f"<bookmark mark='a'/> Each is trained on the novels for {c['steps']:,} steps of {c['ctx']}-character "
            "windows, the same windows in the same order, and each three times with different random starts; the "
            f"bands show the spread between the three. <bookmark mark='b'/> {v_train}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(key), FadeIn(spec[0]))
            self.play(*[Create(lines[m][1]) for m in ORDER], *[FadeIn(lines[m][0]) for m in ORDER], run_time=6.0,
                      rate_func=linear)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in spec[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(fix_line), FadeIn(fix_l), FadeIn(ends))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inside(self):
        p = load("positions")
        c = dict(p["cfg"])
        T = int(c["ctx"])
        vals = {m: np.asarray(p[f"in_{m}"], float) for m in ORDER}
        mu = [float(vals[m].mean()) for m in ORDER]
        sp = [(float(vals[m].min()), float(vals[m].max())) for m in ORDER]
        base = min(min(v) for v in vals.values()) - 0.15
        ch = bars_chart([m_ - base for m_ in mu], [POS_COLORS[m] for m in ORDER], width=7.0, height=3.2, x0=-3.5,
                        base_y=-2.0, vmax=max(mu) - base + 0.05, labels=[POS_NAMES[m] for m in ORDER], font_size=22,
                        spread=[(a - base, b_ - base) for a, b_ in sp])
        for v, m_ in zip(ch.vals, mu):
            v.become(MathTex(f"{m_:.3f}", font_size=24, color=v.get_color()).move_to(v))
        head = label(rf"within the training length: \ bits per character on positions $1$--${T}$", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.5)
        cut = note(rf"bars start at ${base:.2f}$ bits; \ whiskers: the range over the seeds").to_corner(DR, buff=0.3)
        order = sorted(ORDER, key=lambda m: vals[m].mean())
        best, worst = order[0], order[-1]
        gap = vals[worst].mean() - vals[best].mean()
        spread = max(b_ - a for a, b_ in sp)
        clear = vals[best].max() < min(vals[m].min() for m in ORDER if m != best)
        if clear:
            v1 = (f"{CAP[best]} is best, at {vals[best].mean():.3f}, and every one of its seeds beats every seed of "
                  "the others. ")
        else:
            v1 = (f"The best mean is {SPOKEN[best]}'s, {vals[best].mean():.3f}, but the seeds overlap: the "
                  f"differences here, up to {gap:.3f} bits, are not much larger than the {spread:.3f} spread "
                  "between seeds of one design. ")
        nope_rank = order.index("nope") + 1
        behind = float(vals["nope"].mean() - vals[best].mean())
        rank_word = ["first", "second", "third", "last"][nope_rank - 1]
        nope_v = float(vals["nope"].mean())
        if nope_rank == 1:
            v2 = f"No positions at all comes first, at {nope_v:.3f}: the causal mask alone tells it where it is."
        elif behind < 0.05:
            v2 = (f"No positions at all comes {rank_word}, at {nope_v:.3f}, only {behind:.3f} behind: the causal mask "
                  "really does tell it where it is.")
        else:
            v2 = (f"No positions at all comes {rank_word}, at {nope_v:.3f}, {behind:.2f} bits behind the best: the mask "
                  "tells it something, but not everything.")
        with self.voiceover(
            f"First, inside the length they were trained on, the first {T} characters. <bookmark mark='a'/> "
            + v1 + "<bookmark mark='b'/> " + v2
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch.base), FadeIn(ch.names), FadeIn(cut))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in ch.bars], lag_ratio=0.15), FadeIn(ch.whisk),
                      FadeIn(ch.vals))
            vo.wait_until("b")
            self.play(Indicate(ch.bars[ORDER.index("nope")], color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beyond(self):
        p = load("positions")
        c = dict(p["cfg"])
        T, R = int(c["ctx"]), int(c["read"])
        B = {m: np.asarray(p[f"bucket_{m}"], float) for m in ORDER}  # seed, bucket of 32
        nb = B["rope"].shape[1]
        xs = np.arange(nb) * (R / nb) + R / nb / 2
        allv = np.concatenate([b.ravel() for b in B.values()])
        lo = np.floor(allv.min() * 2) / 2 - 0.25
        hi = min(np.ceil(allv.max() * 2) / 2, lo + 4.0)
        g = axes([0, R, R / 4], [lo, hi, 0.5], x_length=8.2, y_length=4.4, xlabel=r"position in the text",
                 ylabel=r"bits per character, \ by position \ (means and seed ranges)",
                 xticks=[0, T, 2 * T, 3 * T, R], xfmt=lambda v: f"{int(v)}",
                 yticks=[v for v in np.arange(np.ceil(lo * 2) / 2, hi + 0.01, 0.5)], yfmt=lambda v: f"{v:.1f}",
                 center=[-2.0, -0.4, 0])
        ax = g.ax
        edge = DashedLine(ax.c2p(T, lo), ax.c2p(T, hi), color=GREY_B, stroke_width=2)
        el = label(rf"trained up to ${T}$", font_size=20, color=GREY_B).next_to(edge.get_top(), RIGHT, buff=0.1).shift(DOWN * 0.2)
        lines = {m: seed_lines(ax, xs, np.minimum(B[m], hi), POS_COLORS[m], 3) for m in ORDER}
        rise = {m: float(np.asarray(p[f"far_{m}"]).mean() - np.asarray(p[f"in_{m}"]).mean()) for m in ORDER}
        rows = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=POS_COLORS[m], stroke_width=5),
                               label(POS_NAMES[m], font_size=20, color=POS_COLORS[m]),
                               MathTex(f"{rise[m]:+.2f}", font_size=24, color=POS_COLORS[m])).arrange(RIGHT, buff=0.15)
                        for m in ORDER]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.9, 0.6, 0])
        for r_ in rows:
            r_[2].set_x(6.5)
        rh = label(rf"bits at $3$--$4\times$ the length, \\ minus within it", font_size=20, color=GREY_A).next_to(rows, UP, buff=0.25)
        held = [m for m in ORDER if rise[m] < 0.15]
        broke = [m for m in ORDER if rise[m] >= 0.5]
        mid = [m for m in ORDER if m not in held and m not in broke]
        n_held, n_mid, n_broke = (spoken_list(SPOKEN[m] for m in g_) if g_ else "" for g_ in (held, mid, broke))
        hr = max(rise[m] for m in held) if held else 0.0
        mlo, mhi = (min(rise[m] for m in mid), max(rise[m] for m in mid)) if mid else (0.0, 0.0)
        br = max(rise[m] for m in broke) if broke else 0.0
        if not held:
            v_held = ""
        elif hr > 0.005:
            v_held = f"Steady past the training length, within {hr:.2f} bits: {n_held}."
        else:
            v_held = (f"Steady past the training length, and even {-hr:.2f} bits better, with more text behind each "
                      f"character: {n_held}.")
        if not mid:
            v_mid = ""
        elif len(mid) == 1:
            v_mid = f"Drifting up, by {mhi:.2f} bits: {n_mid}."
        else:
            v_mid = f"Drifting up, by {mlo:.2f} to {mhi:.2f} bits: {n_mid}."
        v_broke = f"Broken, up by as much as {br:.1f} bits: {n_broke}." if broke else ""
        rope_txt = ("RoPE's slow hands point at angles they never saw in training, and its queries stop "
                    "matching their keys: the problem the next chapter takes on." if rise["rope"] >= 0.15 else
                    "RoPE holds up here; the next chapter shows where it does break.")
        with self.voiceover(
            f"Now read four times as far, {R} characters, though none of them saw more than {T}. "
            f"<bookmark mark='a'/> Bits per character at each position, three seeds each. <bookmark mark='b'/> {v_held} "
            f"<bookmark mark='e'/> {v_mid} <bookmark mark='f'/> {v_broke} "
            f"<bookmark mark='d'/> {rope_txt}"
        ) as vo:
            self.play(FadeIn(g), Create(edge), FadeIn(el))
            self.play(*[Create(lines[m][1]) for m in ORDER], *[FadeIn(lines[m][0]) for m in ORDER], run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rh), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(Indicate(rows[ORDER.index("rope")], color=POS_COLORS["rope"]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        """Why ALiBi holds and no positions drifts: the penalties only grow past the training length; 1/t only shrinks."""
        p = load("positions")
        c = dict(p["cfg"])
        T, R = int(c["ctx"]), int(c["read"])
        m = [float(v) for v in p["slopes"]]
        cap_ = 40.0
        g1 = axes([0, R, R / 4], [-cap_, 0, 10], x_length=5.4, y_length=3.4, xlabel=r"distance back, \ characters",
                  ylabel=r"ALiBi's bias \ $-m_h \times$ distance", xticks=[0, T, R], xfmt=lambda v: f"{int(v)}",
                  yticks=[-cap_, -20, 0], yfmt=lambda v: f"{int(v)}", center=[-3.5, -0.5, 0])
        a1 = g1.ax
        hl = VGroup()
        for i, m_ in enumerate(m):
            xe = min(R, cap_ / m_)
            ln = Line(a1.c2p(0, 0), a1.c2p(xe, -m_ * xe), color=POS_COLORS["alibi"], stroke_width=3)
            ln.set_stroke(opacity=1.0 - 0.18 * i)
            tag = MathTex(rf"m = 1/{int(round(1 / m_))}", font_size=22, color=POS_COLORS["alibi"])
            tag.next_to(ln.get_end(), RIGHT, buff=0.08)
            if xe < R:  # a steep line ends on the floor of the plot: its name sits just above that end
                tag.shift(UP * 0.2)
            hl.add(VGroup(ln, tag))
        sh1 = Rectangle(width=a1.c2p(T, 0)[0] - a1.c2p(0, 0)[0], height=a1.c2p(0, 0)[1] - a1.c2p(0, -cap_)[1],
                        stroke_width=0, fill_color=GREY_B, fill_opacity=0.12).move_to(a1.c2p(T / 2, -cap_ / 2))
        sl1 = label(r"seen in \\ training", font_size=18, color=GREY_B).next_to(sh1.get_bottom(), UP, buff=0.12)
        # no positions: the share of a marked first token in a uniform average, 1/t, on a log scale
        g2 = axes([0, R, R / 4], [-3, 0, 1], x_length=5.0, y_length=3.4, xlabel=r"position $t$",
                  ylabel=r"no positions: \ the mark's share, \ $1/t$", xticks=[0, T, R], xfmt=lambda v: f"{int(v)}",
                  yticks=[-3, -2, -1, 0], yfmt=lambda v: f"10^{{{int(v)}}}", center=[3.6, -0.5, 0])
        a2 = g2.ax
        ts = np.arange(1, R + 1)
        inv = curve(a2, ts, -np.log10(ts), POS_COLORS["nope"], 3)
        sh2 = Rectangle(width=a2.c2p(T, 0)[0] - a2.c2p(0, 0)[0], height=a2.c2p(0, 0)[1] - a2.c2p(0, -3)[1],
                        stroke_width=0, fill_color=GREY_B, fill_opacity=0.12).move_to(a2.c2p(T / 2, -1.5))
        lowest = DashedLine(a2.c2p(0, -np.log10(T)), a2.c2p(R, -np.log10(T)), color=GREY_B, stroke_width=1.5)
        lw = label(rf"the smallest in training, \ $1/{T}$", font_size=18, color=GREY_B).next_to(
            a2.c2p(R, -np.log10(T)), UP, buff=0.08).align_to(a2.c2p(R, 0), RIGHT)
        head = label(r"why one holds, \ and why one drifts", font_size=30).to_edge(UP, buff=0.35)
        c0, c3, ratio = T * m[0], T * m[-1], T / R
        with self.voiceover(
            "Why does one hold and another drift? <bookmark mark='a'/> ALiBi's four heads subtract a penalty that "
            f"grows with distance, with slopes from {m[0]:.2f} down to {m[-1]:.4f}. A key at the training length, "
            f"{T} characters back, already costs the steepest head {c0:.0f} and the shallowest {c3:.1f}. "
            "<bookmark mark='b'/> Past the training length a key only costs more, so nothing new happens: the heads "
            "go on looking at what is near, and the text past the edge looks just like the text before it. "
            "<bookmark mark='c'/> No positions at all drifts for its own reason. The signal it reads, one over t, "
            f"only shrinks: at position {R} it is {ratio:.2f} of its smallest value in training, a value the model "
            "never had to tell apart. <bookmark mark='d'/> The sinusoids and RoPE meet something worse past the "
            "edge: vectors and angles they never saw at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(sh1), FadeIn(sl1))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(h_[0]) for h_ in hl], lag_ratio=0.3), FadeIn(VGroup(*[h_[1] for h_ in hl])),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(g2), FadeIn(sh2), Create(lowest), FadeIn(lw))
            self.play(Create(inv), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(head))
        self.wait(0.3)
        self.clear_scene()
