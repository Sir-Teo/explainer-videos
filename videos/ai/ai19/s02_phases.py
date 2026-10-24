from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.specs import GPUS
from videos.ai.ai19.common import (BYTEC, DECODEC, FLOPC, PART, PREFILLC, WEIGHTC, fmt, load, loglog, node_box,
                                   take_away, times)


class Phases(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.stack()
        self.ours()

    def card(self):
        card = chapter_card(1, r"Prefill and decode", r"Why is reading a prompt fast, and writing an answer slow?",
                            part=PART)
        with self.voiceover("Chapter one. Prefill and decode."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        H = GPUS["H100"]
        ridge = H["tensor"] / H["bw"]
        colors = {r"N": WEIGHTC, r"B": DECODEC, r"T": PREFILLC, r"I": FLOPC}
        rows = [
            cmath(r"\text{FLOPs}", r"=", r"2N", r"\text{ per token}", colors=colors, font_size=36),
            cmath(r"\text{bytes}", r"=", r"2N", r"\text{ per pass}", colors=colors, font_size=36),
            cmath(r"I_{\text{decode}}", r"=", r"\frac{2N \cdot B}{2N}", r"= B", colors=colors, font_size=36),
            cmath(r"I_{\text{prefill}}", r"=", r"\frac{2N \cdot T}{2N}", r"= T", colors=colors, font_size=36),
            cmath(r"\text{fast when}", r"\;I\;\ge\;", rf"\frac{{P}}{{\beta}} \approx {ridge:.0f}", colors=colors,
                  font_size=36),
        ]
        whys = [why(r"a multiply and an add per weight"), why(r"$16$-bit weights, \ each read once"),
                why(r"$B$ conversations share one read"), why(r"a prompt's $T$ tokens share it too"),
                why(r"H100's ridge \ (Part 17)")]
        step = ladder(self, rows, whys, keep=5, top=3.2, x=-3.2, buff=0.36, edge=6.8)
        # the picture: two phases on the roofline (schematic)
        g = axes([0, 4], [0, 3], x_length=4.2, y_length=2.2, xlabel=r"intensity $I$ (log)",
                 ylabel=r"speed (log)", center=[4.3, -2.35, 0], font_size=18)
        ax = g.ax
        xr = 2.2
        roof = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([ax.c2p(0, 0.3), ax.c2p(xr, 2.5),
                                                                           ax.c2p(4, 2.5)])
        dec = Dot(ax.c2p(0.25, 0.3 + 2.2 * 0.25 / xr), radius=0.08, color=DECODEC)
        decl = label(r"decode, $B = 1$", font_size=18, color=DECODEC).next_to(dec, RIGHT, buff=0.1)
        pre = Dot(ax.c2p(3.3, 2.5), radius=0.08, color=PREFILLC)
        prel = label(r"prefill", font_size=18, color=PREFILLC).next_to(pre, DOWN, buff=0.12)
        tag = schematic_tag(corner=UR)
        with self.voiceover(
            "A model with N parameters does about two N operations for every token it reads: one multiply and one "
            "add per weight. <bookmark mark='a'/> And every pass through the model reads every weight once: two N "
            "bytes in sixteen-bit numbers. <bookmark mark='b'/> When it writes an answer, a pass handles one new "
            "token per conversation. With B conversations in a batch, the intensity, operations per byte, is just "
            "B. <bookmark mark='c'/> When it reads a prompt, all T of its tokens go through in one pass, the way they "
            "do in training: that's called prefill, and its intensity is T. <bookmark mark='d'/> Part 17's roofline "
            f"says an H100 only reaches full speed above about {ridge:.0f} operations per byte. A prompt of a "
            "thousand tokens is there. Writing for a single conversation, at an intensity of one, is not: decode is "
            "bound by memory."
        ) as vo:
            step(0)
            self.play(FadeIn(g), FadeIn(tag), Create(roof))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(dec, scale=0.5), FadeIn(decl))
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(pre, scale=0.5), FadeIn(prel))
            vo.wait_until("d")
            step(4)
            self.play(Indicate(dec, color=DECODEC, scale_factor=1.6))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stack(self):
        r = load("roof")
        B = np.asarray(r["batches"], float)
        t = np.asarray(r["stack_t"]) * 1e3
        pred = np.asarray(r["stack_pred"]) * 1e3
        bw, peak = float(r["bw"]), float(r["peak"])
        mb = float(r["stack_mb"])
        knee_p, knee_m = float(r["knee_pred"]), float(r["knee_meas"])
        g = loglog((0, math.log10(600)), (math.floor(math.log10(t.min() * 0.6)), math.log10(t.max() * 2.2)),
                   x_length=6.6, y_length=4.2, xlabel=r"batch $B$: \ vectors per pass",
                   ylabel=r"time per pass \ (ms, \ this computer, \ one core)", center=[-2.6, -0.4, 0])
        ax = g.ax
        Lx = np.log10(B)
        mem_t = 4.0 * r["stack_layers"] * r["stack_n"] ** 2 / bw * 1e3
        bs = np.logspace(0, math.log10(600), 80)
        floor = DashedLine(ax.c2p(0, math.log10(mem_t)), ax.c2p(math.log10(600), math.log10(mem_t)), color=BYTEC,
                           dash_length=0.08)
        comp = np.array([2.0 * r["stack_layers"] * r["stack_n"] ** 2 * b / peak * 1e3 for b in bs])
        cl = VMobject(color=FLOPC, stroke_width=3).set_points_as_corners(
            [ax.c2p(math.log10(b), math.log10(c)) for b, c in zip(bs, comp) if math.log10(c) >= ax.y_range[0]])
        best = VMobject(color=WHITE, stroke_width=2.5).set_points_as_corners(
            [ax.c2p(math.log10(b), math.log10(max(mem_t, c))) for b, c in zip(bs, comp)])
        dots = VGroup(*[Dot(ax.c2p(x, math.log10(y)), radius=0.07, color=DECODEC) for x, y in zip(Lx, t)])
        fl = label(rf"reading ${mb:.0f}$ MB at ${bw / 1e9:.0f}$ GB/s", font_size=20, color=BYTEC)
        fl.next_to(ax.c2p(0.05, math.log10(mem_t)), UP, buff=0.1, aligned_edge=LEFT)
        cll = label(rf"arithmetic at ${peak / 1e9:.0f}$ GFLOP/s", font_size=20, color=FLOPC)
        cll.next_to(ax.c2p(math.log10(300), math.log10(2.0 * r['stack_layers'] * r['stack_n'] ** 2 * 300 / peak * 1e3)),
                    RIGHT, buff=0.1).shift(DOWN * 0.35 + LEFT * 0.6)
        stk = VGroup(*[Rectangle(width=0.9, height=0.12, stroke_width=0, fill_color=WEIGHTC, fill_opacity=0.25 + 0.05 * k)
                       for k in range(12)]).arrange(DOWN, buff=0.04).move_to([4.6, 1.6, 0])
        sl = label(rf"$12$ weight matrices, \\ ${int(r['stack_n']):,} \times {int(r['stack_n']):,}$: \ ${mb:.0f}$ MB, \\"
                   r"more than any cache here".replace(",", "{,}"), font_size=20, color=WEIGHTC).next_to(stk, DOWN, buff=0.2)
        tps = B / (t / 1e3)
        k16 = list(B).index(16)
        k512 = len(B) - 1
        rl = VGroup(label(rf"$B = 1$: \ ${tps[0]:.0f}$ vectors a second", font_size=22, color=DECODEC),
                    label(rf"$B = 16$: \ ${tps[k16]:.0f}$", font_size=22, color=DECODEC),
                    label(rf"$B = 512$: \ ${tps[k512]:.0f}$", font_size=22, color=DECODEC))
        rl.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.5, -1.6, 0])
        r16 = t[k16] / t[0]
        if knee_m >= 0.5 * knee_p:
            how = (f"The measured points stay close to that: the time first doubles at a batch of about "
                   f"{knee_m:.0f}, where the roofline says {knee_p:.0f}.")
        else:
            how = (f"The measured time starts climbing sooner than the roofline says: it has doubled by a batch of "
                   f"about {knee_m:.0f}, not {knee_p:.0f}, because this processor's matrix library is tuned for big "
                   f"products, not for a handful of vectors. Even so, sixteen vectors cost {r16:.1f} times one, not "
                   "sixteen.")
        with self.voiceover(
            "We can watch this happen on this computer. <bookmark mark='a'/> Twelve weight matrices, "
            f"{mb:.0f} megabytes, more than any of its caches hold: a model too big to stay close to the processor. "
            "Multiply a batch of B vectors through all twelve, and time it. <bookmark mark='b'/> The roofline "
            f"predicts a floor: just reading the weights takes {mem_t:.0f} milliseconds, whatever B is, until the "
            "arithmetic catches up with the reading. <bookmark mark='c'/> " + how + " <bookmark mark='d'/> So "
            f"vectors per second climb from {tps[0]:.0f} at a batch of one to {tps[k512]:.0f} at {int(B[k512])}: "
            f"{times(tps[k512] / tps[0])} as much work out of the same weights."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, shift=DOWN * 0.1) for s_ in stk], lag_ratio=0.08), FadeIn(sl))
            vo.wait_until("b")
            self.play(Create(floor), FadeIn(fl))
            self.play(Create(cl), FadeIn(cll))
            self.play(Create(best))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeOut(stk), FadeOut(sl), LaggedStart(*[FadeIn(x_) for x_ in rl], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        ph, rf = load("phases"), load("roof")
        T = np.asarray(ph["prefill_T"], float)
        B = np.asarray(ph["decode_B"], float)
        ptps, dtps = np.asarray(ph["prefill_tps"]), np.asarray(ph["decode_tps"])
        n = ph["sizes"]["read"]
        top = max(ptps.max(), dtps.max())
        g = loglog((0, math.log10(300)), (2, math.log10(top * 2.5)), x_length=6.4, y_length=4.0,
                   xlabel=r"tokens in one pass: \ prompt length $T$, \ or batch $B$",
                   ylabel=r"tokens a second \ (our novels model, \ one core)", center=[-2.8, -0.35, 0])
        ax = g.ax
        pd = VGroup(*[Dot(ax.c2p(math.log10(x), math.log10(y)), radius=0.07, color=PREFILLC) for x, y in zip(T, ptps)])
        dd = VGroup(*[Dot(ax.c2p(math.log10(x), math.log10(y)), radius=0.07, color=DECODEC) for x, y in zip(B, dtps)])
        pl = curve(ax, np.log10(T), np.log10(ptps), PREFILLC, 2.5)
        dl = curve(ax, np.log10(B), np.log10(dtps), DECODEC, 2.5)
        kp, kd = len(T) - 1, list(B).index(256)
        lp = label(r"prefill: \ one prompt", font_size=22, color=PREFILLC).next_to(pd[-1], UP, buff=0.15).shift(LEFT * 0.8)
        ld = label(r"decode: \ $B$ conversations", font_size=22, color=DECODEC).next_to(dd[-1], DOWN, buff=0.2).shift(LEFT * 0.8)
        model = node_box(rf"our novels model: \ ${n / 1e6:.1f}$ million weights read per pass", C.NEURAL,
                         font_size=20).move_to([3.9, 2.6, 0])
        ratio = ptps[kp] / dtps[0]
        k1 = label(rf"one conversation writes \ ${dtps[0]:.0f}$ tokens/s", font_size=22, color=DECODEC)
        k2 = label(rf"it reads a ${int(T[kp])}$-token prompt \ at ${ptps[kp]:,.0f}$ tokens/s".replace(",", "{,}"),
                   font_size=22, color=PREFILLC)
        k3 = label(rf"${int(B[kd])}$ conversations: \ ${dtps[kd]:,.0f}$ tokens/s in all".replace(",", "{,}"),
                   font_size=22, color=DECODEC)
        keys = VGroup(k1, k2, k3).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.9, 0.6, 0])
        per_user = dtps[kd] / B[kd]
        tw = take_away(r"prefill is arithmetic; \ decode is memory: \ batch the decodes", color=WHITE, font_size=26)
        # the bandwidth this machine's decode at batch 1 reaches: 4-byte weights read per step
        bwu = 4 * n * dtps[0]
        with self.voiceover(
            "Now our own model, the series' novels model, on the inference engine we wrote for this part. "
            "<bookmark mark='a'/> Prefill: one prompt, of T tokens, in a single pass. <bookmark mark='b'/> Decode: "
            "one new token for each of B conversations per pass. <bookmark mark='c'/> One conversation is written "
            f"at {dtps[0]:.0f} tokens a second; each step reads all {n / 1e6:.1f} million weights, "
            f"{bwu / 1e9:.1f} gigabytes a second of them. The same model reads a {int(T[kp])}-token prompt at "
            f"{ptps[kp]:,.0f} tokens a second: {times(ratio)} faster, because its tokens share the reading. "
            f"<bookmark mark='d'/> Batching the decodes buys most of that back: {int(B[kd])} conversations at once "
            f"get {dtps[kd]:,.0f} tokens a second between them. But each of them now gets only {per_user:.0f}. "
            "That trade, the speed of one against the work of all, is what a server is built around."
        ) as vo:
            self.play(FadeIn(g), FadeIn(model))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in pd], lag_ratio=0.1), Create(pl), FadeIn(lp))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dd], lag_ratio=0.1), Create(dl), FadeIn(ld))
            vo.wait_until("c")
            self.play(FadeIn(k1), Indicate(dd[0], color=DECODEC, scale_factor=1.8))
            self.play(FadeIn(k2), Indicate(pd[-1], color=PREFILLC, scale_factor=1.8))
            vo.wait_until("d")
            self.play(FadeIn(k3), Indicate(dd[kd], color=DECODEC, scale_factor=1.8))
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()
