from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import A, OURS, POS, curve, heat_image, load

METHODS = [("plain", r"rotations as trained", C.SURPRISE), ("pi", r"position interpolation", C.TRUE_P),
           ("ntk", r"NTK-aware", C.INTERVAL), ("yarn", r"YaRN", C.BITS)]


class Longer(VoiceoverScene):
    def construct(self):
        self.card()
        self.breaks()
        self.fixes()
        self.sinks()

    def card(self):
        card = chapter_card(4, r"Longer than it was trained for", r"What happens past the end of the training context?",
                            part=11)
        with self.voiceover("Chapter four. Longer than it was trained for."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def axes(self, e, lo, hi):
        T = int(e["T"])
        ax = Axes(x_range=[0, T, T / 4], y_range=[lo, hi, 0.5], x_length=8.2, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.0, -0.5, 0])
        xt = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=22, color=GREY_B).next_to(ax.c2p(v, lo), DOWN, buff=0.1)
                      for v in np.linspace(0, T, 5)])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in np.arange(lo, hi + 0.01, 0.5)])
        xn = label(r"position in the text", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"bits per character, \ by position", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        return ax, VGroup(xt, yt, xn, yn)

    def line(self, ax, e, key, color, hi, sw=3.5):
        b = np.asarray(e[f"bucket_{key}"])
        xs = np.arange(len(b)) * 64 + 32
        return VGroup(curve(ax, xs, np.minimum(b, hi), color, sw),
                      *[Dot(ax.c2p(x, min(v, hi)), radius=0.05, color=color) for x, v in zip(xs, b)])

    # ------------------------------------------------------------------
    def breaks(self):
        e, t = load("extend"), load("tf")
        ctx, s = int(t["ctx"]), int(e["s"])
        allb = np.concatenate([np.asarray(e[f"bucket_{k}"]) for k, _, _ in METHODS] + [np.asarray(e["bucket_window"])])
        lo = math.floor(allb.min() * 2) / 2 - 0.5
        hi = min(math.ceil(allb.max() * 2) / 2, lo + 4.5)
        ax, deco = self.axes(e, lo, hi)
        edge = DashedLine(ax.c2p(ctx, lo), ax.c2p(ctx, hi), color=GREY_B, stroke_width=2)
        el = label(rf"trained up to ${ctx}$", font_size=22, color=GREY_B).next_to(edge, UP, buff=0.08)
        plain = self.line(ax, e, "plain", C.SURPRISE, hi)
        win = self.line(ax, e, "window", GREY_B, hi, 2.5)
        k1 = label(r"rotations as trained", font_size=24, color=C.SURPRISE).move_to([4.7, 1.8, 0])
        k2 = label(rf"just the last ${ctx}$ characters", font_size=24, color=GREY_B).next_to(k1, DOWN, buff=0.25).align_to(k1, LEFT)
        bp = np.asarray(e["bucket_plain"])
        far = float(bp[-4:].mean())
        near = float(bp[: ctx // 64].mean())
        with self.voiceover(
            f"Our model was trained on stretches of {ctx} characters. What if we hand it {s} times as many? "
            "<bookmark mark='a'/> Up to its training length, it does what it always did. <bookmark mark='b'/> Past "
            f"it, it falls apart: from {near:.1f} bits a character to {far:.1f}. The slow hands of its clocks now "
            "point at angles it never saw in training, and its queries and keys stop meaning what they meant. "
            "<bookmark mark='c'/> Doing nothing clever, just reading the last "
            f"{ctx} characters at a time, is far better. Long context isn't free."
        ) as vo:
            self.play(Create(ax), FadeIn(deco), Create(edge), FadeIn(el))
            vo.wait_until("a")
            self.play(Create(plain[0]), FadeIn(plain[1:]), FadeIn(k1), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(win[0]), FadeIn(win[1:]), FadeIn(k2), run_time=2.0)
        self.wait(0.3)
        self.next_section_objects = (ax, deco, edge, el, plain, win, k1, k2)

    # ------------------------------------------------------------------
    def fixes(self):
        e, t = load("extend"), load("tf")
        ax, deco, edge, el, plain, win, k1, k2 = self.next_section_objects
        ctx, s = int(t["ctx"]), int(e["s"])
        allb = np.concatenate([np.asarray(e[f"bucket_{k}"]) for k, _, _ in METHODS] + [np.asarray(e["bucket_window"])])
        lo = math.floor(allb.min() * 2) / 2 - 0.5
        hi = min(math.ceil(allb.max() * 2) / 2, lo + 4.5)
        lines = {k: self.line(ax, e, k, c_, hi) for k, _, c_ in METHODS}
        keys = VGroup(k1, k2, *[label(t_, font_size=24, color=c_) for k, t_, c_ in METHODS[1:]])
        for a, b in zip(keys[1:], keys[2:]):
            b.next_to(a, DOWN, buff=0.25).align_to(k1, LEFT)
        # the three rescalings, as how much each pair of numbers is slowed down
        th = np.asarray(e["theta"])
        slow = {"pi": np.full_like(th, float(s)), "ntk": th / np.asarray(e["theta_ntk"]), "yarn": th / np.asarray(e["theta_yarn"])}
        bx = Axes(x_range=[0, len(th) - 1, 5], y_range=[0.5, s + 0.5, 1], x_length=4.2, y_length=2.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.6, -2.1, 0])
        bl = label(r"each pair slowed by, \ fast $\to$ slow pairs", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.1)
        yl = VGroup(MathTex(r"1\times", font_size=20, color=GREY_B).next_to(bx.c2p(0, 1), LEFT, buff=0.08),
                    MathTex(rf"{s}\times", font_size=20, color=GREY_B).next_to(bx.c2p(0, s), LEFT, buff=0.08))
        sl = {k: curve(bx, np.arange(len(th)), slow[k], c_, 3) for k, _, c_ in METHODS[1:]}
        b = {k: float(np.asarray(e[f"bucket_{k}"])[-4:].mean()) for k, _, _ in METHODS}
        w_far = float(np.asarray(e["bucket_window"])[-4:].mean())
        best = min(("pi", "ntk", "yarn"), key=lambda k: b[k])
        cites = cite(r"S.~Chen et al.\ (2023); \ bloc97 (2023); \ B.~Peng et al., \textit{YaRN} (2023)", corner=UR)
        names = {"pi": "position interpolation", "ntk": "the NTK-aware rescaling", "yarn": "YaRN"}
        with self.voiceover(
            "So people rescale the clocks. <bookmark mark='a'/> Position interpolation slows every hand by the same "
            f"factor, {s}, so the longer text spans only the angles seen in training; but the fast hands lose the "
            "fine detail of which character is next to which. <bookmark mark='b'/> The NTK-aware trick slows the "
            "slow hands a lot and the fast ones hardly at all. <bookmark mark='c'/> YaRN leaves the fast hands "
            "alone, slows the slow ones fully, ramps in between, and sharpens the attention slightly to make up for "
            f"the longer context. <bookmark mark='d'/> On our model, with no retraining at all, the best here is "
            f"{names[best]}: {b[best]:.2f} bits at the far end, against {b['plain']:.1f} for doing nothing"
            + (". " if b[best] > w_far else f", and better even than the {ctx}-character window. ")
            + "Real models do this and then train briefly on long texts; Qwen and DeepSeek reach a hundred and "
            "twenty-eight thousand tokens with YaRN."
        ) as vo:
            self.play(FadeIn(cites), Create(bx), FadeIn(bl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(sl["pi"]), Create(lines["pi"][0]), FadeIn(lines["pi"][1:]), FadeIn(keys[2]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(sl["ntk"]), Create(lines["ntk"][0]), FadeIn(lines["ntk"][1:]), FadeIn(keys[3]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(sl["yarn"]), Create(lines["yarn"][0]), FadeIn(lines["yarn"][1:]), FadeIn(keys[4]), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(keys[2 + ["pi", "ntk", "yarn"].index(best)], scale_factor=1.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sinks(self):
        t = load("tf")
        sink = np.asarray(t["sink"])  # layer, head: mean weight on position 0
        uni = float(t["sink_uniform"])
        maps = np.asarray(t["maps"])
        L, H = sink.shape
        li, hi_ = np.unravel_index(np.argmax(sink), sink.shape)
        img = heat_image(maps[li, hi_], 4.2, 4.2, color=A, mask_upper=True).move_to([-3.6, -0.4, 0])
        frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        il = label(rf"layer {li + 1}, head {hi_ + 1}, \ on the passage", font_size=22, color=GREY_A).next_to(img, UP, buff=0.12)
        col = Rectangle(width=4.2 / maps.shape[-1] * 1.5, height=4.2, stroke_color=POS, stroke_width=2.5).move_to(img.get_left(), aligned_edge=LEFT)
        # bars: share of attention on the first position, every head
        bw = 0.2
        bars = VGroup()
        for l_ in range(L):
            for h in range(H):
                v = float(sink[l_, h])
                bars.add(Rectangle(width=bw * 0.8, height=max(3.2 * v, 0.01), stroke_width=0,
                                   fill_color=POS if (l_, h) == (li, hi_) else A, fill_opacity=0.85)
                         .move_to([0.9 + (l_ * (H + 1) + h) * bw, -2.2 + 1.6 * v, 0]))
        base = Line([0.8, -2.2, 0], [0.9 + (L * (H + 1)) * bw, -2.2, 0], color=GREY_C, stroke_width=2)
        ul = DashedLine([0.8, -2.2 + 3.2 * uni, 0], [0.9 + (L * (H + 1)) * bw, -2.2 + 3.2 * uni, 0], color=GREY_B, stroke_width=1.5)
        bl = label(r"every head's attention on the first character", font_size=22, color=GREY_A).next_to(base, DOWN, buff=0.15)
        ulab = label(r"if attention were spread evenly", font_size=20, color=GREY_B).next_to(ul, UP, buff=0.05).align_to(base, RIGHT)
        lyr = VGroup(*[label(rf"layer {l_ + 1}", font_size=18, color=GREY_B).move_to([0.9 + (l_ * (H + 1) + (H - 1) / 2) * bw,
                                                                                       -2.85, 0]) for l_ in range(L)])
        bl.next_to(lyr, DOWN, buff=0.1)
        ratio = float(sink.max() / uni)
        strong = ratio > 5
        why = label(r"softmax weights must add to one: \\ a head with nothing to find \\ parks its attention somewhere",
                    font_size=24, color=GREY_A).move_to([3.4, 2.0, 0])
        cite_ = cite(r"G.~Xiao et al., \textit{Efficient Streaming Language Models with Attention Sinks} (2023)", corner=DR)
        with self.voiceover(
            "Long contexts brought a strange discovery. Look at where heads put their attention. "
            + (f"<bookmark mark='a'/> Some heads in our model put a large share of it, up to {sink.max():.0%}, on the "
               f"very first character, whatever that character is: about {ratio:.0f} times what an even spread "
               "would give it. " if strong else
               f"<bookmark mark='a'/> In our small model, the first character gets a little extra attention, up to "
               f"{ratio:.1f} times an even share; in large models, some heads give it most of their attention. ")
            + "<bookmark mark='b'/> These are attention sinks. A softmax has to hand out all of its weight, so a "
            "head that has nothing to look for parks its attention on a harmless spot. Guangxuan Xiao and colleagues "
            "found that keeping those first tokens lets a model run on and on; newer models like gpt-oss build a "
            "learnable sink into every head, and Qwen adds a gate that lets a head switch itself off instead."
        ) as vo:
            self.play(FadeIn(img), Create(frame), FadeIn(il), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(col), Create(base), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03),
                      Create(ul), FadeIn(ulab), FadeIn(lyr), FadeIn(bl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()
