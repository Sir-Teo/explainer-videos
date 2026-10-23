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
        with self.voiceover(
            "Now the experiment. Four small transformers, identical except for how they learn where each character "
            f"is: sinusoids added to the input, rotary positions, ALiBi's linear penalty, and nothing at all. "
            f"<bookmark mark='a'/> Each is trained on the novels for {c['steps']:,} steps of {c['ctx']}-character "
            f"windows, the same windows in the same order, and each three times with different random starts, so "
            "we can see how much of any gap is luck. <bookmark mark='b'/> Here is their training, replayed: "
            "held-out bits per character as they learn."
        ) as vo:
            self.play(FadeIn(g), FadeIn(key), FadeIn(spec[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in spec[1:]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(*[Create(lines[m][1]) for m in ORDER], *[FadeIn(lines[m][0]) for m in ORDER], run_time=4.0,
                      rate_func=linear)
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
        v2 = (f"No positions at all comes {['first', 'second', 'third', 'last'][nope_rank - 1]}, at "
              f"{vals['nope'].mean():.3f}"
              + (": the causal mask alone tells it where it is." if nope_rank == 1 else
                 f", only {behind:.3f} behind: the causal mask really does tell it where it is." if behind < 0.05 else
                 f", {behind:.2f} behind the best: the mask tells it something, but not everything."))
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
        parts = []
        if held:
            parts.append(f"{spoken_list(SPOKEN[m] for m in held)} {'holds' if len(held) == 1 else 'hold'} steady "
                         f"past the training length, within {max(rise[m] for m in held):.2f} bits")
        if mid:
            parts.append(f"{spoken_list(SPOKEN[m] for m in mid)} {'drifts' if len(mid) == 1 else 'drift'} up by "
                         f"{min(rise[m] for m in mid):.2f} to {max(rise[m] for m in mid):.2f}")
        if broke:
            parts.append(f"{spoken_list(SPOKEN[m] for m in broke)} {'breaks' if len(broke) == 1 else 'break'}, up "
                         f"by as much as {max(rise[m] for m in broke):.1f} bits")
        v = "; ".join(parts) + "."
        why_ = ("ALiBi's penalty means a distant key matters less and less, so new lengths look like old ones. "
                if "alibi" in held else "")
        rope_txt = ("RoPE's slow hands point at angles they never saw in training, and its queries stop "
                    "matching their keys: the problem the next chapter takes on." if rise["rope"] >= 0.15 else
                    "RoPE holds up here; the next chapter shows where it does break.")
        with self.voiceover(
            f"Now read four times as far, {R} characters, though none of them saw more than {T}. "
            f"<bookmark mark='a'/> Bits per character at each position, three seeds each. <bookmark mark='b'/> {v} "
            f"<bookmark mark='c'/> {why_}{rope_txt}"
        ) as vo:
            self.play(FadeIn(g), Create(edge), FadeIn(el))
            vo.wait_until("a")
            self.play(*[Create(lines[m][1]) for m in ORDER], *[FadeIn(lines[m][0]) for m in ORDER], run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rh), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(Indicate(rows[ORDER.index("rope")], color=POS_COLORS["rope"]))
        self.wait(0.3)
        self.clear_scene()
