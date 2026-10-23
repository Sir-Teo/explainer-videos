from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, EXT_COLORS, EXT_NAMES, OURS, PART, POS, curve, heat_image, load

METHODS = [("plain", r"rotations as trained", C.SURPRISE), ("pi", r"position interpolation", C.TRUE_P),
           ("ntk", r"NTK-aware", C.INTERVAL), ("yarn", r"YaRN", C.BITS)]


SHORT = {"plain": r"as trained", "logn": r"$\log n$", "ntk": r"NTK", "ntk_logn": r"NTK \\ $+ \log n$", "yarn": r"YaRN"}
SPOKEN_EXT = {"plain": "the plain model", "pi": "position interpolation", "ntk": "the NTK-aware rescaling",
              "yarn": "YaRN", "logn": "log n scaling alone", "ntk_logn": "NTK-aware with log n scaling"}


class Longer(VoiceoverScene):
    def construct(self):
        self.card()
        self.breaks()
        self.fixes()
        self.yarn()
        self.logn()
        self.tune()

    def card(self):
        card = chapter_card(11, r"Longer than it was trained for", r"What happens past the end of the training context?",
                            part=PART)
        with self.voiceover("Chapter eleven. Longer than it was trained for."):
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
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.95, -2.3, 0])
        bl = label(r"each pair slowed by, \ fast $\to$ slow pairs", font_size=20, color=GREY_A).next_to(bx, UP, buff=0.1)
        yl = VGroup(MathTex(r"1\times", font_size=20, color=GREY_B).next_to(bx.c2p(0, 1), LEFT, buff=0.08),
                    MathTex(rf"{s}\times", font_size=20, color=GREY_B).next_to(bx.c2p(0, s), LEFT, buff=0.08))
        sl = {k: curve(bx, np.arange(len(th)), slow[k], c_, 3) for k, _, c_ in METHODS[1:]}
        b = {k: float(np.asarray(e[f"bucket_{k}"])[-4:].mean()) for k, _, _ in METHODS}
        w_far = float(np.asarray(e["bucket_window"])[-4:].mean())
        best = min(("pi", "ntk", "yarn"), key=lambda k: b[k])
        cites = cite(r"S.~Chen et al.\ (2023); \ bloc97 (2023); \ B.~Peng et al., \textit{YaRN} (2023)", corner=UR)
        win_txt = ("." if b[best] > w_far else f", and better even than the {ctx}-character window.")
        names = {"pi": "position interpolation", "ntk": "the NTK-aware rescaling", "yarn": "YaRN"}
        with self.voiceover(
            "So people rescale the clocks. <bookmark mark='a'/> Position interpolation slows every hand by the same "
            f"factor, {s}, so the longer text spans only angles seen in training, but the fast hands lose detail. "
            "<bookmark mark='b'/> The NTK-aware trick, named after part twelve's neural tangent kernel, slows the "
            "slow hands a lot and the fast ones hardly at all. <bookmark mark='c'/> YaRN leaves the fast hands alone, "
            "slows the slow ones fully, ramps in between, and sharpens the attention slightly. <bookmark mark='d'/> "
            f"On our model, with no retraining, the best is {names[best]}: {b[best]:.2f} bits at the far end, against "
            f"{b['plain']:.1f} for doing nothing" + win_txt + " Qwen and DeepSeek reach a hundred and twenty-eight "
            "thousand tokens with YaRN."
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
            "Here is YaRN's recipe exactly. <bookmark mark='a'/> For each pair, count the full turns its hand makes "
            "over the training context: r, the context length over the pair's wavelength. <bookmark mark='b'/> Our "
            f"fastest pair turns about {r[0]:.0f} times in {ctx} characters; it has seen every angle, so YaRN leaves "
            "it alone. <bookmark mark='c'/> The slowest pairs never finish a turn, so YaRN slows them by the full "
            f"factor of {s}. <bookmark mark='d'/> In between is a ramp, gamma: zero below one turn, one above "
            "thirty-two. <bookmark mark='e'/> Each new angle blends the slowed angle and the original by gamma. In "
            f"our heads, {kept} kept, {len(ramp_i)} on the ramp and {slowed} slowed fully. <bookmark mark='f'/> "
            "Slowing the hands also flattens the attention, so YaRN multiplies every score by zero point one log s "
            f"plus one, squared: for s of {s}, {mult:.2f}."
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
    def logn(self):
        e, t = load("extend"), load("tf")
        ctx, s = int(t["ctx"]), int(e["s"])
        rows = [
            cmath(r"p_{\text{best}}", r"=", r"\frac{e^{\Delta}}{e^{\Delta} + (n - 1)}", font_size=34, colors={r"p_{\text{best}}": A}),
            cmath(r"p_{\text{best}} \text{ fixed}", r"\;\Leftrightarrow\;", r"e^{\Delta} \propto n \;\Leftrightarrow\; \Delta \propto \log n",
                  font_size=34),
            cmath(r"s_{nj}", r"\;\leftarrow\;", r"s_{nj} \cdot \max\big(1, \log_{L} n\big)", font_size=34),
        ]
        whys = [why(r"one key $\Delta$ above $n - 1$ others", font_size=20), why(r"solve for the margin", font_size=20),
                why(rf"trained at $L = {ctx}$: \\ unchanged up to $L$", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-3.4, buff=0.5, edge=6.9)
        names = ["plain", "logn", "ntk", "ntk_logn", "yarn"]
        far = {k: float(np.asarray(e[f"bucket_{k}"])[-4:].mean()) for k in names}
        near = float(np.mean(np.asarray(e["bucket_plain"])[: ctx // 64]))
        vals = [far[k] for k in names]
        lo = min(vals + [near]) - 0.3
        g = axes([0, len(names), 1], [lo, max(vals) + 0.3, 0.5], x_length=6.0, y_length=2.6, xlabel="",
                 ylabel=rf"bits per character at positions ${3 * ctx}$--${4 * ctx}$", center=[2.6, -2.0, 0])
        ax = g.ax
        bars = VGroup()
        for i, k in enumerate(names):
            v = min(far[k], max(vals) + 0.3)
            r_ = Rectangle(width=0.7, height=max(ax.c2p(0, v)[1] - ax.c2p(0, lo)[1], 0.02), stroke_width=0,
                           fill_color=EXT_COLORS[k], fill_opacity=0.85).move_to(ax.c2p(i + 0.5, (v + lo) / 2))
            bars.add(VGroup(r_, MathTex(f"{far[k]:.2f}", font_size=20, color=EXT_COLORS[k]).next_to(r_, UP, buff=0.06),
                            label(SHORT[k], font_size=17, color=EXT_COLORS[k]).next_to(ax.c2p(i + 0.5, lo), DOWN, buff=0.1)))
        ref = DashedLine(ax.c2p(0, near), ax.c2p(len(names), near), color=GREY_B, stroke_width=1.5)
        refl = label(rf"within $1$--${ctx}$", font_size=16, color=GREY_B).next_to(ref, RIGHT, buff=0.08)
        hist = VGroup(label(r"Chiang \& Cholak (2022): \ scale logits by $\log n$", font_size=20, color=GREY_A),
                      label(r"Qwen (2023): \ dynamic NTK $+$ $\log n$ $+$ windows", font_size=20, color=GREY_A),
                      label(r"Llama 4 (2025): \ attention temperature at inference", font_size=20, color=GREY_A))
        hist.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.1, -2.1, 0])
        # the formula's effect, on screen from the first word: the best key's weight as more keys come into view, with
        # a margin that gives it 0.8 at the training length, as it is and with every score scaled by log_L n
        L_ = float(ctx)
        d0 = math.log(4 * (L_ - 1))
        ns = np.linspace(2, 4 * L_, 160)
        dn = d0 * np.maximum(1, np.log(ns) / math.log(L_))
        p_plain, p_scaled = np.exp(d0) / (np.exp(d0) + ns - 1), np.exp(dn) / (np.exp(dn) + ns - 1)
        pg = axes([0, 4 * L_, L_], [0, 1, 0.25], x_length=5.2, y_length=2.2, xlabel=r"keys in view, $n$",
                  ylabel=r"weight on the best key, \ margin set for $0.8$ at $n = L$",
                  xticks=[L_ * i for i in range(1, 5)], yticks=[0, 0.5, 1], xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"),
                  center=[2.4, -2.05, 0])
        pax = pg.ax
        pv = DashedLine(pax.c2p(L_, 0), pax.c2p(L_, 1), color=GREY_B, stroke_width=1.5)
        pc0, pc1 = curve(pax, ns, p_plain, EXT_COLORS["plain"]), curve(pax, ns, p_scaled, EXT_COLORS["logn"])
        pl0 = label(r"fixed $\Delta$", font_size=18, color=EXT_COLORS["plain"]).next_to(pax.c2p(4 * L_, p_plain[-1]), RIGHT, buff=0.1)
        pl1 = label(r"scaled by \ $\log_L n$", font_size=18, color=EXT_COLORS["logn"]).next_to(
            pax.c2p(4 * L_, p_scaled[-1]), RIGHT, buff=0.1)
        best = min(names, key=lambda k: far[k])
        help_l = far["logn"] < far["plain"] - 0.05
        help_n = far["ntk_logn"] < far["ntk"] - 0.02
        v1 = (f"On our model, scaling alone takes the far end from {far['plain']:.2f} to {far['logn']:.2f} bits. "
              if help_l else f"On our model, scaling alone barely changes the far end: {far['plain']:.2f} to "
              f"{far['logn']:.2f} bits, since the broken angles, not the spread, are its problem. ")
        v2 = (f"On top of the NTK rescaling it helps again, {far['ntk']:.2f} to {far['ntk_logn']:.2f}. " if help_n else
              f"On top of the NTK rescaling it changes little, {far['ntk']:.2f} to {far['ntk_logn']:.2f}. ")
        with self.voiceover(
            "A longer text also has more keys to share the weights. <bookmark mark='a'/> Say the best key scores "
            "delta above n minus one others: its weight is e to the delta over e to the delta plus n minus one. "
            "<bookmark mark='b'/> To keep that weight as n grows, delta must grow like log n. <bookmark mark='c'/> "
            "So scale every score by log n, in units of the training length: nothing changes up to it, and beyond it "
            "the attention stays as sharp as in training. David Chiang and Peter Cholak proposed it in 2022; Qwen "
            f"and Llama 4 use versions of it. <bookmark mark='d'/> {v1}<bookmark mark='e'/> {v2}"
            f"The best of all here is {SPOKEN_EXT[best]}, at {far[best]:.2f}."
        ) as vo:
            step(0)
            self.play(FadeIn(pg), Create(pv))
            vo.wait_until("a")
            self.play(Indicate(rows[0][2], color=A), Create(pc0), FadeIn(pl0))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(hist), Create(pc1), FadeIn(pl1))
            vo.wait_until("d")
            self.play(FadeOut(VGroup(pg, pv, pc0, pc1, pl0, pl1)))
            self.play(FadeIn(g), Create(ref), FadeIn(refl), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tune(self):
        e, t = load("extend"), load("tf")
        ctx, s, T = int(t["ctx"]), int(e["s"]), int(e["T"])
        steps, chars = int(e["ft_steps"]), int(e["ft_chars"])
        allb = np.concatenate([np.asarray(e[f"bucket_{k}"]) for k in ("pi", "yarn", "ft_pi", "ft_yarn")]
                              + [np.asarray(e["bucket_window"])])
        lo = math.floor(allb.min() * 2) / 2 - 0.25
        hi = math.ceil(allb.max() * 2) / 2 + 0.25
        ax, deco = self.axes(e, lo, hi)
        edge = DashedLine(ax.c2p(ctx, lo), ax.c2p(ctx, hi), color=GREY_B, stroke_width=2)

        def ln(key, col, sw=3.0, dashed=False):
            b = np.asarray(e[f"bucket_{key}"])
            xs = np.arange(len(b)) * 64 + 32
            c_ = curve(ax, xs, np.minimum(b, hi), col, sw)
            return DashedVMobject(c_, num_dashes=24) if dashed else c_

        before = VGroup(ln("pi", EXT_COLORS["pi"], 2.5, True), ln("yarn", EXT_COLORS["yarn"], 2.5, True))
        after = VGroup(ln("ft_pi", EXT_COLORS["pi"], 3.5), ln("ft_yarn", EXT_COLORS["yarn"], 3.5))
        win = ln("window", EXT_COLORS["window"], 2.0)
        key = VGroup(label(r"dashed: \ no training", font_size=20, color=GREY_B),
                     label(rf"solid: \ after ${steps}$ steps at ${T:,}$".replace(",", "{,}"), font_size=20, color=WHITE),
                     label(r"position interpolation", font_size=20, color=EXT_COLORS["pi"]),
                     label(r"YaRN", font_size=20, color=EXT_COLORS["yarn"]),
                     label(rf"just the last ${ctx}$", font_size=20, color=EXT_COLORS["window"]))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.8, 1.3, 0])
        # the fine-tuning itself: training loss at every step, both runs
        fc = {k: np.asarray(e[f"ft_curve_{k}"], float) for k in ("pi", "yarn")}
        ftop = float(np.ceil(max(fc[k].max() for k in fc)))
        fg = axes([0, steps, 50], [math.floor(min(fc[k].min() for k in fc)), ftop, 1], x_length=2.6, y_length=1.5,
                  xlabel=r"fine-tuning step", xticks=[0, steps], xfmt=lambda v: f"{int(v)}", font_size=16,
                  yticks=[math.floor(min(fc[k].min() for k in fc)), ftop], yfmt=lambda v: f"{v:.0f}",
                  center=[4.75, -1.75, 0])
        fl = VGroup(*[curve(fg.ax, np.arange(1, steps + 1), fc[k], EXT_COLORS[k], 2.0) for k in fc])
        ftl = label(rf"training loss, \ bits per character \\ (${T:,}$-character windows)".replace(",", "{,}"),
                    font_size=16, color=GREY_A).next_to(fg, UP, buff=0.12)
        far = {k: float(np.asarray(e[f"bucket_{k}"])[-4:].mean()) for k in ("pi", "yarn", "ft_pi", "ft_yarn", "window")}
        winner = "ft_yarn" if far["ft_yarn"] < far["ft_pi"] else "ft_pi"
        gap = abs(far["ft_yarn"] - far["ft_pi"])
        v = (f"Position interpolation falls from {far['pi']:.2f} to {far['ft_pi']:.2f} bits at the far end, YaRN "
             f"from {far['yarn']:.2f} to {far['ft_yarn']:.2f}.")
        if far[winner] < far["window"]:
            v_end = (f"YaRN ends ahead by {gap:.2f} bits, and beats reading the last {ctx} characters, {far['window']:.2f}."
                     if winner == "ft_yarn" else
                     f"Interpolation ends ahead by {gap:.2f} bits, and beats reading the last {ctx} characters, "
                     f"{far['window']:.2f}.")
        else:
            v_end = (f"YaRN ends ahead by {gap:.2f} bits, but neither yet beats simply reading the last {ctx} characters, "
                     f"{far['window']:.2f}." if winner == "ft_yarn" else
                     f"Interpolation ends ahead by {gap:.2f} bits, but neither yet beats simply reading the last {ctx} "
                     f"characters, {far['window']:.2f}.")
        with self.voiceover(
            f"Real models then train briefly at the new length. So did we: {steps} steps of {T:,}-character windows, "
            f"about {100 * chars / float(t['tokens']):.0f} percent of the original training, from position "
            "interpolation and from YaRN; in the corner, their training loss. <bookmark mark='a'/> Dashed, before; "
            f"solid, after. <bookmark mark='b'/> {v} <bookmark mark='c'/> {v_end} DeepSeek-V3 went from four thousand "
            "to a hundred and twenty-eight thousand tokens this way, with two thousand steps."
        ) as vo:
            self.play(Create(ax), FadeIn(deco), Create(edge), FadeIn(key[2:]), Create(before), Create(win), run_time=2.0)
            self.play(FadeIn(fg), FadeIn(ftl), Create(fl), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(key[:2]))
            vo.wait_until("b")
            self.play(Create(after), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
