from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import A, OURS, POS, curve, heat_image, load

METHODS = [("plain", r"rotations as trained", C.SURPRISE), ("pi", r"position interpolation", C.TRUE_P),
           ("ntk", r"NTK-aware", C.INTERVAL), ("yarn", r"YaRN", C.BITS)]


def saturating_softmax() -> VGroup:
    """The softmax of the same five scores, scaled up: the weights pile onto one key until they barely move."""
    s = np.array([1.0, 0.7, 0.4, 0.1, -0.2])
    panels = VGroup()
    for k in (1, 4, 16):
        p = np.exp(k * s) / np.exp(k * s).sum()
        bars = VGroup(*[Rectangle(width=0.18, height=1.1 * float(v) + 0.02, stroke_width=0, fill_color=A,
                                  fill_opacity=0.9) for v in p]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        base = Line(bars.get_corner(DL) + LEFT * 0.05, bars.get_corner(DR) + RIGHT * 0.05, color=GREY_C, stroke_width=1.5)
        lab = label(rf"scores $\times{k}$", font_size=18, color=GREY_B).next_to(base, DOWN, buff=0.08)
        panels.add(VGroup(bars, base, lab))
    panels.arrange(RIGHT, buff=0.45, aligned_edge=DOWN)
    arrows = VGroup(*[Arrow(a[1].get_right() + UP * 0.3, b[1].get_left() + UP * 0.3, buff=0.08, color=GREY_B,
                            stroke_width=2, max_tip_length_to_length_ratio=0.3) for a, b in zip(panels[:-1], panels[1:])])
    return VGroup(panels, arrows)


class Longer(VoiceoverScene):
    def construct(self):
        self.card()
        self.breaks()
        self.fixes()
        self.yarn()
        self.sinks()
        self.modern()

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
        el = label(rf"trained up to ${ctx}$", font_size=22, color=GREY_B).next_to(edge.get_top(), RIGHT, buff=0.1).shift(DOWN * 0.25)
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
            "fine detail of which character is next to which. <bookmark mark='b'/> The NTK-aware trick, named after "
            "part ten's neural tangent kernel, the theory of very wide networks, needs none of that theory here: it "
            "slows the slow hands a lot and the fast ones hardly at all. <bookmark mark='c'/> YaRN leaves the fast hands "
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
    def yarn(self):
        """YaRN's recipe exactly: turns per pair over the training context, the ramp, the blended angle, the temperature."""
        e, t = load("extend"), load("tf")
        ctx, s = int(t["ctx"]), int(e["s"])
        th, gam = np.asarray(e["theta"]), np.asarray(e["ramp"])
        r = ctx * th / (2 * np.pi)  # full turns each pair makes over the training context
        alpha, beta = 1.0, 32.0
        n = len(th)
        KEEP, SLOW = ManimColor(C.SURPRISE), ManimColor(C.TRUE_P)  # the colours of "as trained" and "position interpolation" in the last chart
        ax = CornerAxes(x_range=[0.5, n + 0.5, 1], y_range=[-2.5, 2.0, 0.5], x_length=6.0, y_length=4.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.5, 0])
        yt = VGroup(*[MathTex(v, font_size=22, color=GREY_B).next_to(ax.c2p(0.5, p), LEFT, buff=0.1)
                      for p, v in zip(range(-2, 3), ("0.01", "0.1", "1", "10", "100"))])
        xt = VGroup(label(r"pair $1$ \ (fastest)", font_size=20, color=GREY_B).next_to(ax.c2p(1, -2.5), DOWN, buff=0.12),
                    label(rf"pair ${n}$ \ (slowest)", font_size=20, color=GREY_B).next_to(ax.c2p(n, -2.5), DOWN, buff=0.12))
        yn = label(rf"$r$: \ full turns in ${ctx}$ positions", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lb, la = np.log10(beta), np.log10(alpha)

        def band(y0, y1, col):
            return Rectangle(width=ax.c2p(n + 0.5, 0)[0] - ax.c2p(0.5, 0)[0], height=ax.c2p(0, y1)[1] - ax.c2p(0, y0)[1],
                             stroke_width=0, fill_color=col, fill_opacity=0.12).move_to(ax.c2p((n + 1) / 2, (y0 + y1) / 2))

        bands = VGroup(band(lb, 2.0, KEEP), band(la, lb, interpolate_color(SLOW, KEEP, 0.5)), band(-2.5, la, SLOW))
        lines = VGroup(*[DashedLine(ax.c2p(0.5, y), ax.c2p(n + 0.5, y), dash_length=0.08, stroke_width=2, color=GREY_B) for y in (lb, la)])
        lline = VGroup(MathTex(r"\beta", font_size=24, color=GREY_B).next_to(lines[0], RIGHT, buff=0.08),
                       MathTex(r"\alpha", font_size=24, color=GREY_B).next_to(lines[1], RIGHT, buff=0.08))
        bl = VGroup(label(r"kept as trained, \ $\gamma = 1$", font_size=20, color=KEEP).next_to(ax.c2p(n + 0.5, 2.0), DL, buff=0.12),
                    label(r"the ramp", font_size=20, color=interpolate_color(SLOW, KEEP, 0.5))
                    .move_to(ax.c2p(n + 0.5, (la + lb) / 2), aligned_edge=RIGHT).shift(LEFT * 0.12),
                    label(rf"slowed by $s = {s}$, \ $\gamma = 0$", font_size=20, color=SLOW)
                    .next_to(ax.c2p(0.5, -2.5), UR, buff=0.12))
        dots = VGroup(*[Dot(ax.c2p(i + 1, np.log10(r[i])), radius=0.065, color=GREY_A) for i in range(n)])
        ramp_i = [i for i in range(n) if 0 < gam[i] < 1]
        gl = VGroup(*[MathTex(f"{gam[i]:.2f}", font_size=18, color=interpolate_color(SLOW, KEEP, float(gam[i])))
                      .next_to(dots[i], RIGHT, buff=0.1) for i in ramp_i])
        cols = [interpolate_color(SLOW, KEEP, float(g_)) for g_ in gam]
        # the recipe
        eqs = VGroup(
            MathTex(r"r_i = \frac{L}{\lambda_i} = \frac{L\,\theta_i}{2\pi}", font_size=30),
            MathTex(r"\gamma_i = \operatorname{clip}\!\left(\frac{r_i - \alpha}{\beta - \alpha},\ 0,\ 1\right)", font_size=30),
            MathTex(r"\theta_i' = (1 - \gamma_i)\,\frac{\theta_i}{s} + \gamma_i\,\theta_i", font_size=30),
            MathTex(r"\operatorname{softmax}\!\left(\frac{q^{\top} k}{t\,\sqrt{d}}\right), \quad \sqrt{1/t} = 0.1\ln s + 1",
                    font_size=30),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to([3.75, 0.15, 0])
        ab = label(rf"$L = {ctx}, \ \alpha = {alpha:.0f}, \ \beta = {beta:.0f}$", font_size=22, color=GREY_A) \
            .next_to(eqs[1], DOWN, buff=0.12).align_to(eqs, LEFT)
        eqs[2:].shift(DOWN * 0.3)
        kept, slowed = int((gam >= 1).sum()), int((gam <= 0).sum())
        cnt = label(rf"our heads: \ ${kept}$ kept, \ ${len(ramp_i)}$ on the ramp, \ ${slowed}$ slowed by ${s}$",
                    font_size=22, color=GREY_A).next_to(eqs[2], DOWN, buff=0.12).align_to(eqs, LEFT)
        eqs[3].shift(DOWN * 0.3)
        mult = (0.1 * math.log(s) + 1) ** 2
        tl = label(rf"$s = {s}$: \ every score $\times\,{mult:.2f}$", font_size=22, color=C.BITS) \
            .next_to(eqs[3], DOWN, buff=0.12).align_to(eqs, LEFT)
        cite_ = cite(r"B.~Peng et al., \textit{YaRN: Efficient Context Window Extension of Large Language Models} (2023)", corner=UR)
        kept_w = "pair" if kept == 1 else "pairs"
        with self.voiceover(
            "Here is YaRN's recipe exactly, since most open models use it. <bookmark mark='a'/> For each pair of "
            "numbers, count the full turns its hand makes over the training context: r is the context length over "
            f"the pair's wavelength. <bookmark mark='b'/> Our fastest pair turns about {r[0]:.0f} times in {ctx} "
            "characters; it has seen every angle many times over, so YaRN leaves it alone. <bookmark mark='c'/> The "
            "slowest pairs never finish a single turn. Past the training length they would point at angles never "
            f"seen, so YaRN slows them by the full factor of {s}. <bookmark mark='d'/> In between is a ramp, gamma: "
            "zero below one turn, one above thirty-two, a straight line between. <bookmark mark='e'/> Each new "
            "angle is a blend, one minus gamma of the slowed angle plus gamma of the original. In our heads that's "
            f"{kept} {kept_w} kept, {len(ramp_i)} on the ramp and {slowed} slowed fully. <bookmark mark='f'/> Slowing "
            "the hands also flattens the attention, spreading it over more positions, so YaRN adds a temperature: "
            f"every score is multiplied by zero point one log s plus one, squared; for s of {s}, {mult:.2f}."
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(yn), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bands[0]), Create(lines[0]), FadeIn(lline[0]), FadeIn(bl[0]), dots[0].animate.set_color(KEEP),
                      Flash(dots[0], color=KEEP))
            vo.wait_until("c")
            self.play(FadeIn(bands[2]), Create(lines[1]), FadeIn(lline[1]), FadeIn(bl[2]),
                      *[dots[i].animate.set_color(SLOW) for i in range(n) if gam[i] <= 0])
            vo.wait_until("d")
            self.play(FadeIn(eqs[1]), FadeIn(ab))
            self.play(FadeIn(bands[1]), FadeIn(bl[1]), *[dots[i].animate.set_color(cols[i]) for i in ramp_i],
                      LaggedStart(*[FadeIn(g_, shift=LEFT * 0.1) for g_ in gl], lag_ratio=0.2))
            vo.wait_until("e")
            self.play(FadeIn(eqs[2]))
            self.play(FadeIn(cnt))
            vo.wait_until("f")
            self.play(FadeIn(eqs[3]))
            self.play(FadeIn(tl))
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
        # bars: share of attention on the first position, every head; the dashed line is an even share
        ratio = float(sink.max() / uni)
        strong = ratio > 5
        bw, sy = 0.2, 1.6 / max(uni, float(sink.max()))
        bars = VGroup()
        for l_ in range(L):
            for h in range(H):
                v = float(sink[l_, h])
                bars.add(Rectangle(width=bw * 0.8, height=max(sy * v, 0.01), stroke_width=0,
                                   fill_color=POS if (l_, h) == (li, hi_) and strong else A, fill_opacity=0.85)
                         .move_to([0.9 + (l_ * (H + 1) + h) * bw, -2.2 + sy * v / 2, 0]))
        base = Line([0.8, -2.2, 0], [0.9 + (L * (H + 1)) * bw, -2.2, 0], color=GREY_C, stroke_width=2)
        ul = DashedLine([0.8, -2.2 + sy * uni, 0], [0.9 + (L * (H + 1)) * bw, -2.2 + sy * uni, 0], color=GREY_B, stroke_width=1.5)
        bl = label(r"every head's attention on the first character", font_size=22, color=GREY_A).next_to(base, DOWN, buff=0.15)
        ulab = label(r"if attention were spread evenly", font_size=20, color=GREY_B).next_to(ul, UP, buff=0.05).align_to(base, RIGHT)
        lyr = VGroup(*[label(rf"layer {l_ + 1}", font_size=18, color=GREY_B).move_to([0.9 + (l_ * (H + 1) + (H - 1) / 2) * bw,
                                                                                       -2.85, 0]) for l_ in range(L)])
        bl.next_to(lyr, DOWN, buff=0.1)
        why = label(r"softmax weights must add to one: \\ a head with nothing to find \\ parks its attention somewhere",
                    font_size=24, color=GREY_A).move_to([3.4, 2.0, 0])
        cite_ = cite(r"G.~Xiao et al., \textit{Efficient Streaming Language Models with Attention Sinks} (2023)", corner=DR)
        # what a sink head looks like in a large model (a sketch): most of each row's weight on the first token
        n = 48
        g = np.random.default_rng(3)
        sk = np.tril(np.exp(-np.abs(np.subtract.outer(np.arange(n), np.arange(n))) / 2.0) * 0.3 + g.random((n, n)) * 0.05)
        sk[:, 0] += 2.0
        sk = np.tril(sk) / np.tril(sk).sum(1, keepdims=True)
        simg = heat_image(sk, 4.2, 4.2, color=A, mask_upper=True).move_to(img)
        sframe = SurroundingRectangle(simg, buff=0, color=GREY_D, stroke_width=1.5)
        sl = label(r"a sink head in a large model \ (schematic)", font_size=22, color=GREY_A).next_to(simg, UP, buff=0.12)
        scol = Rectangle(width=4.2 / n * 1.5, height=4.2, stroke_color=POS, stroke_width=2.5).move_to(simg.get_left(), aligned_edge=LEFT)
        with self.voiceover(
            "Long contexts brought a strange discovery. Look at where heads put their attention. "
            + (f"<bookmark mark='a'/> Some heads in our model put a large share of it, up to {sink.max():.0%}, on the "
               f"very first character, whatever that character is: about {ratio:.0f} times what an even spread "
               "would give it. <bookmark mark='b'/> These are attention sinks. " if strong else
               "<bookmark mark='a'/> In our small model, nothing odd: every head gives the first character less than "
               "an even share. <bookmark mark='b'/> But in large models, many heads put most of their attention on "
               "the very first token, whatever that token is. These are attention sinks. ")
            + "<bookmark mark='c'/> A softmax has to hand out all of its weight, so a head that has nothing to look "
            "for parks its attention on a harmless spot. Guangxuan Xiao and colleagues found that keeping those first "
            "tokens lets a model run on and on; newer models like gpt-oss build a learnable sink into every head, and "
            "Qwen adds a gate that lets a head switch itself off instead."
        ) as vo:
            self.play(FadeIn(img), Create(frame), FadeIn(il), FadeIn(cite_))
            vo.wait_until("a")
            self.play(*([Create(col)] if strong else []), Create(base),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03),
                      Create(ul), FadeIn(ulab), FadeIn(lyr), FadeIn(bl), run_time=2.0)
            vo.wait_until("b")
            if not strong:
                self.play(FadeOut(Group(img, frame, il)), FadeIn(Group(simg, sframe, sl)))
                self.play(Create(scol))
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def modern(self):
        """Four small changes frontier models make to the attention we built, each with its equation and a tiny plot."""
        W, H = 6.6, 3.35

        def panel(c, title, col):
            box = RoundedRectangle(width=W, height=H, corner_radius=0.12, stroke_color=GREY_D, stroke_width=1.5).move_to(c)
            t_ = label(title, font_size=22, color=col).move_to(box.get_corner(UL) + RIGHT * 0.2 + DOWN * 0.28, aligned_edge=UL)
            return box, t_

        def mini(c, xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=2.5, y_length=1.55, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(c)

        cs = [np.array([-3.45, 1.78, 0]), np.array([3.45, 1.78, 0]), np.array([-3.45, -1.8, 0]), np.array([3.45, -1.8, 0])]
        # 1. a sink logit: one learned number b per head in the softmax's denominator (gpt-oss)
        b_, nk = 2.0, 8
        p_plain = 1 / nk
        p_sink = 1 / (math.exp(b_) + nk)
        sink_share = math.exp(b_) / (math.exp(b_) + nk)
        box1, t1 = panel(cs[0], r"a sink logit \ (gpt-oss, 2025)", POS)
        e1 = MathTex(r"p_j = \frac{e^{s_j}}{e^{\,b} + \sum_k e^{s_k}}", font_size=30).move_to(cs[0] + LEFT * 1.6 + DOWN * 0.15)
        sy, bw = 1.5 / 0.5, 0.2
        x0 = cs[0][0] + 0.75
        yb = cs[0][1] - 1.05
        bars = VGroup(*[Rectangle(width=bw * 0.75, height=sy * p_plain, stroke_width=0, fill_color=A, fill_opacity=0.85)
                        .move_to([x0 + j * bw, yb + sy * p_plain / 2, 0]) for j in range(nk)])
        bars_s = VGroup(*[Rectangle(width=bw * 0.75, height=sy * p_sink, stroke_width=0, fill_color=A, fill_opacity=0.85)
                          .move_to([x0 + j * bw, yb + sy * p_sink / 2, 0]) for j in range(nk)])
        sbar = Rectangle(width=bw * 0.75, height=sy * sink_share, stroke_width=0, fill_color=POS, fill_opacity=0.85) \
            .move_to([x0 + (nk + 0.6) * bw, yb + sy * sink_share / 2, 0])
        base1 = Line([x0 - bw, yb, 0], [x0 + (nk + 1.2) * bw, yb, 0], color=GREY_C, stroke_width=2)
        bl1 = label(rf"${nk}$ equal scores", font_size=18, color=GREY_B).next_to(base1, DOWN, buff=0.08).align_to(base1, LEFT)
        sl1 = MathTex(rf"{sink_share:.2f}", font_size=20, color=POS).next_to(sbar, UP, buff=0.06)
        pl1 = MathTex(rf"{p_plain:.3f}", font_size=20, color=A).next_to(bars, UP, buff=0.06)
        pl1s = MathTex(rf"{p_sink:.3f}", font_size=20, color=A).next_to(bars_s, UP, buff=0.06)
        bnote = label(rf"$b = {b_:.0f}$", font_size=18, color=POS).next_to(sbar, RIGHT, buff=0.08).align_to(sbar, DOWN)
        # 2. an output gate: each head's output times a sigmoid of the input (Qiu et al. 2025; Qwen3-Next)
        GATE = C.BITS
        box2, t2 = panel(cs[1], r"an output gate \ (Qwen3-Next, 2025)", GATE)
        e2 = MathTex(r"o = \operatorname{Attn}(x)\,\odot\,\sigma(x\,W_g)", font_size=30).move_to(cs[1] + LEFT * 1.4 + DOWN * 0.15)
        ax2 = mini(cs[1] + RIGHT * 1.75 + DOWN * 0.3, [-6, 6, 3], [0, 1, 0.5])
        g2 = ax2.plot(lambda z: 1 / (1 + math.exp(-z)), color=GATE, stroke_width=3.5)
        gl2 = VGroup(label(r"shut", font_size=18, color=GREY_B).next_to(ax2.c2p(-6, 0), UR, buff=0.08),
                     label(r"open", font_size=18, color=GREY_B).next_to(ax2.c2p(5, 0.95), DOWN, buff=0.12))
        # 3. QK-norm: queries and keys rescaled to a fixed size before the dot product
        QN = C.INTERVAL
        box3, t3 = panel(cs[2], r"QK-norm \ (OLMo 2, Qwen3, Gemma 3)", QN)
        e3 = VGroup(MathTex(r"\hat q = g_q \odot \frac{q}{\operatorname{rms}(q)}", font_size=28),
                    MathTex(r"\hat k = g_k \odot \frac{k}{\operatorname{rms}(k)}", font_size=28)) \
            .arrange(DOWN, buff=0.25).move_to(cs[2] + LEFT * 1.75 + DOWN * 0.2)
        cmax = 4
        ax3 = mini(cs[2] + RIGHT * 2.0 + DOWN * 0.3, [1, cmax, 1], [0, cmax ** 2, 4])
        raw3 = ax3.plot(lambda c: c * c, color=C.SURPRISE, stroke_width=3.5)
        nrm3 = ax3.plot(lambda c: 1.0, color=QN, stroke_width=3.5)
        l3 = VGroup(label(r"plain", font_size=18, color=C.SURPRISE).next_to(ax3.c2p(cmax, cmax ** 2), LEFT, buff=0.1),
                    label(r"normed", font_size=18, color=QN).next_to(ax3.c2p(cmax, 1), UP, buff=0.08).shift(LEFT * 0.3))
        x3 = label(rf"weights grown $\times 1 \ldots {cmax}$", font_size=18, color=GREY_B).next_to(ax3, DOWN, buff=0.08)
        y3 = label(r"score", font_size=18, color=GREY_B).next_to(ax3, LEFT, buff=0.08).shift(UP * 0.4)
        # 4. a soft cap on the scores (Gemma 2): c tanh(s / c), c = 50
        CAP = C.TRUE_P
        cap = 50.0
        box4, t4 = panel(cs[3], r"a soft cap \ (Gemma 2, 2024)", CAP)
        e4 = MathTex(r"s \;\leftarrow\; c\,\tanh(s / c)", font_size=30).move_to(cs[3] + LEFT * 1.6 + DOWN * 0.15)
        c4 = label(rf"$c = {cap:.0f}$", font_size=22, color=GREY_A).next_to(e4, DOWN, buff=0.2)
        ax4 = mini(cs[3] + RIGHT * 1.75 + DOWN * 0.3, [-150, 150, 50], [-150, 150, 50])
        id4 = DashedLine(ax4.c2p(-150, -150), ax4.c2p(150, 150), dash_length=0.06, stroke_width=1.5, color=GREY_B)
        cp4 = ax4.plot(lambda s: cap * math.tanh(s / cap), color=CAP, stroke_width=3.5)
        lim4 = VGroup(*[DashedLine(ax4.c2p(-150, v), ax4.c2p(150, v), dash_length=0.05, stroke_width=1.2, color=CAP,
                                   stroke_opacity=0.6) for v in (cap, -cap)])
        l4 = MathTex(rf"\pm{cap:.0f}", font_size=18, color=CAP).next_to(ax4.c2p(-150, cap), UP, buff=0.05) \
            .align_to(ax4.c2p(-150, cap), LEFT)
        sat = gloss(r"the softmax saturates", r"huge scores put nearly all the weight on one key, \\ and small "
                    r"changes stop moving it: learning stalls", saturating_softmax(), corner=UR, width=5.4, color=A)
        sat.move_to(cs[1] + UP * 0.05)
        with self.voiceover(
            "Sinks are one of several small changes that frontier models make to the attention we built. Here are "
            "four of them, exactly. <bookmark mark='a'/> gpt-oss gives every head one extra learned number, b, that "
            "sits in the softmax's denominator like the score of an invisible position. <bookmark mark='b'/> A head "
            f"with nothing to find can now send its weight there, onto nothing at all: with b equal to {b_:.0f} and "
            f"{nk} equal scores, {sink_share:.0%} of it. <bookmark mark='c'/> Qwen3-Next instead multiplies each "
            "head's output by a gate, a sigmoid of the input. A head with nothing to add can shut itself, and the "
            "sinks largely disappear. <bookmark mark='d'/> QK-norm rescales every query and key to a fixed size "
            "before the dot product. Without it, weights that grow make the scores grow with the square of their "
            "size, until the softmax saturates: <bookmark mark='s'/> nearly all the weight lands on one key, small "
            "changes to the scores no longer move it, and training stalls. With QK-norm, the scores stay bounded. "
            "<bookmark mark='e'/> Gemma 2 caps the scores softly instead: c times tanh of s over c. Small scores pass "
            f"unchanged, and none can pass {cap:.0f}. Gemma 3 dropped the cap for QK-norm."
        ) as vo:
            self.play(Create(box1), FadeIn(t1), FadeIn(e1))
            self.play(Create(base1), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(pl1), FadeIn(bl1))
            vo.wait_until("b")
            self.play(Transform(bars, bars_s), Transform(pl1, pl1s), GrowFromEdge(sbar, DOWN), FadeIn(sl1), FadeIn(bnote))
            vo.wait_until("c")
            self.play(Create(box2), FadeIn(t2), FadeIn(e2), Create(ax2))
            self.play(Create(g2), FadeIn(gl2))
            vo.wait_until("d")
            self.play(Create(box3), FadeIn(t3), FadeIn(e3), Create(ax3), FadeIn(x3), FadeIn(y3))
            self.play(Create(raw3), Create(nrm3), FadeIn(l3), run_time=1.5)
            vo.wait_until("s")
            self.play(FadeIn(sat, shift=UP * 0.2))
            vo.wait_until("e")
            self.play(FadeOut(sat))
            self.play(Create(box4), FadeIn(t4), FadeIn(e4), FadeIn(c4), Create(ax4), Create(id4))
            self.play(Create(cp4), Create(lim4), FadeIn(l4), run_time=1.5)
        self.wait(0.5)
        self.clear_scene()
