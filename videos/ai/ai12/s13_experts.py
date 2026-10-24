from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import DCOL, FIT, HIST, NCOL, PART, SP, load, predict_card, takeaway_card

MOE = C.CONTEXT
BIT_COLORS = ["#7FD3FF", C.INTERVAL, C.BITS, C.MODEL_Q, C.SURPRISE]  # 8, 6, 5, 4, 3 bits


class Experts(VoiceoverScene):
    def construct(self):
        self.card()
        self.experts()
        self.predict()
        self.bits()
        self.takeaway()

    def card(self):
        card = chapter_card(12, r"Experts and bits", r"Do parameters need compute? \ Do they need precision?", part=PART)
        with self.voiceover("Chapter twelve. Experts and bits."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def experts(self):
        m = load("moe")
        Es = [int(e) for e in m["E"]]
        fin = np.asarray(m["final"], float)
        tot = np.asarray(m["total"], float)
        dN, dL = np.asarray(m["dense_N"], float), np.asarray(m["dense_L"], float)
        effN = np.asarray(m["effective_N"], float)
        okd = np.isfinite(dL)
        lx = np.log10(np.concatenate([tot, dN[okd]]))
        x0, x1 = math.floor(lx.min() * 2) / 2, math.ceil(lx.max() * 2) / 2
        allL = np.concatenate([fin.ravel(), dL[okd]])
        y0 = math.floor((allL.min() - 0.05) * 10) / 10
        y1 = min(math.ceil((allL.max() + 0.05) * 10) / 10, y0 + 1.6)
        ax = CornerAxes(x_range=[x0, x1, 0.5], y_range=[y0, y1, 0.2], x_length=6.6, y_length=4.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-2.7, -0.45, 0])
        xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.08)
                      for v in range(math.ceil(x0), math.floor(x1) + 1)])
        yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.08)
                      for v in np.arange(math.ceil(y0 * 5) / 5, y1 + 1e-9, 0.2)])
        xn = label(r"parameters, \ in all", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(rf"held-out bits after ${int(m['chars']) / 1e6:.1f}$ million characters", font_size=22,
                   color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        keep = okd & (dL <= y1)
        dense = VGroup(curve(ax, np.log10(dN[keep]), dL[keep], NCOL, 3),
                       *[Dot(ax.c2p(math.log10(a), b), radius=0.06, color=NCOL) for a, b in zip(dN[keep], dL[keep])])
        mm = fin.mean(1)
        moe = VGroup(curve(ax, np.log10(tot), mm, MOE, 3.5),
                     *[Dot(ax.c2p(math.log10(a), b), radius=0.08, color=MOE) for a, b in zip(tot, mm)],
                     *[Line(ax.c2p(math.log10(a), r.min()), ax.c2p(math.log10(a), r.max()), color=MOE, stroke_width=2)
                       for a, r in zip(tot, fin)])
        elab = VGroup(*[MathTex(rf"E{{=}}{e}", font_size=18, color=MOE).next_to(ax.c2p(math.log10(a), b), DOWN, buff=0.1)
                        for e, a, b in zip(Es, tot, mm) if e in (1, 4, 32)])
        lg = VGroup(label(r"dense: \ every parameter used for every character", font_size=20, color=NCOL),
                    label(rf"mixture: \ width ${int(m['width'])}$, \ $E$ experts, \ one used per character", font_size=20,
                          color=MOE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lg.to_corner(UR, buff=0.3).shift(DOWN * 0.6)
        i8 = Es.index(8) if 8 in Es else len(Es) // 2
        mult = effN[i8] / tot[0]
        cards = VGroup(
            history_card(2022, r"Clark et al.\ (DeepMind)", r"log loss bilinear in $\log N$ and $\log E$: \ experts help "
                         r"less as the base model grows, \ and saturate", width=5.0, color=HIST),
            history_card(2024, r"Krajewski et al.", r"many small experts beat a few large ones; \ the gap to dense "
                         r"models grows with the budget", width=5.0, color=HIST),
            history_card(2024, r"DeepSeek-V3", r"$671$ billion parameters, \ $37$ billion used per token: \ $256$ "
                         r"experts, \ $8$ chosen", width=5.0, color=HIST)).arrange(DOWN, buff=0.12)
        cards.scale(0.82).move_to([4.6, -1.35, 0])
        tag = note(r"two seeds each; \ the dense models are the sweep's").to_corner(DL, buff=0.2)
        router = RoundedRectangle(width=1.4, height=0.5, corner_radius=0.1, stroke_color=GREY_A, stroke_width=2)
        rl_ = label(r"router", font_size=20, color=GREY_A).move_to(router)
        exps = VGroup(*[RoundedRectangle(width=0.5, height=0.8, corner_radius=0.08, stroke_color=MOE, stroke_width=2,
                                         fill_color=MOE, fill_opacity=0.6 if i == 2 else 0.08) for i in range(8)])
        exps.arrange(RIGHT, buff=0.12).next_to(router, DOWN, buff=0.7)
        wires = VGroup(*[Line(router.get_bottom(), e.get_top(), stroke_width=3 if i == 2 else 1,
                              color=MOE if i == 2 else GREY_D) for i, e in enumerate(exps)])
        ch_ = data_text("e", font="DejaVu Sans Mono", font_size=30).next_to(router, UP, buff=0.35)
        arr = Arrow(ch_.get_bottom(), router.get_top(), buff=0.05, stroke_width=2.5, color=GREY_B)
        moe_pic = VGroup(ch_, arr, router, rl_, wires, exps)
        moe_cap = label(r"each character goes to one expert \\ (schematic)", font_size=20, color=GREY_A).next_to(exps, DOWN, buff=0.2)
        moe_pic = VGroup(moe_pic, moe_cap).move_to([4.4, -0.4, 0])
        better = mm[-1] < mm[0] - 0.01
        said1 = (
            f"The loss keeps falling as the experts are added, though each doubling helps less. With eight experts "
            f"it matches a dense model of about {effN[i8]:,.0f} parameters, {mult:.1f} times our base model, for "
            "the compute of the base model. " if better else
            "At our size the experts barely help: the router has too little to tell apart. "
        )
        with self.voiceover(
            "In a dense model, every parameter works on every character, so compute and parameters grow together. "
            "A mixture of experts, from part sixteen, breaks the link: many experts, and a router that sends each "
            "character to one. <bookmark mark='a'/> Split our model's hidden layer into more and more experts, "
            "keeping the work per character the same. "
            + said1
            + "<bookmark mark='b'/> DeepMind measured this in 2022: the loss falls with the number of experts, and "
            "the gain shrinks as the base model grows. Since then experts have become smaller and more numerous: "
            "DeepSeek-V3 has two hundred and fifty-six of them in each layer, and uses eight for each token."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(tag), FadeIn(moe_pic))
            self.play(Create(dense[0]), FadeIn(dense[1:]), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(Create(moe[0]), FadeIn(moe[1:]), FadeIn(elab), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(moe_pic))
            self.play(LaggedStart(*[FadeIn(c_, shift=LEFT * 0.1) for c_ in cards], lag_ratio=0.5), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bits(self):
        p = load("precision")
        D = np.asarray(p["D"], float)
        bits = [int(b) for b in p["bits"]]
        delta = np.asarray(p["delta"], float)
        widths = [int(w) for w in p["widths"]]
        i = widths.index(256) if 256 in widths else len(widths) // 2
        lD = np.log2(D)
        ok = np.isfinite(delta[i, :, 0])
        show = [b for b in bits if b in (6, 5, 4, 3)]
        vals = np.concatenate([delta[i, ok, bits.index(b)] for b in show])
        vals = vals[np.isfinite(vals) & (vals > 1e-4)]
        y0, y1 = math.floor(np.log10(vals.min())), math.ceil(np.log10(vals.max()))
        ax = CornerAxes(x_range=[lD[ok].min() - 0.3, lD[ok].max() + 0.3, 1], y_range=[y0, y1, 1], x_length=6.0, y_length=4.0,
                        tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
        ax.move_to([-3.0, -0.45, 0])
        xt = VGroup(*[MathTex(rf"2^{{{int(v)}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.08)
                      for v in lD[ok][::2]])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(lD[ok].min() - 0.3, v), LEFT, buff=0.08)
                      for v in range(y0, y1 + 1)])
        xn = label(r"characters of training", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(rf"extra bits after rounding the weights \ (width ${widths[i]}$)", font_size=22, color=GREY_A)
        yn.next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        lines = VGroup()
        for b in show:
            v = delta[i, :, bits.index(b)]
            good = ok & np.isfinite(v) & (v > 1e-4)
            col = BIT_COLORS[bits.index(b)]
            lines.add(VGroup(curve(ax, lD[good], np.log10(v[good]), col, 3),
                             *[Dot(ax.c2p(a, math.log10(c)), radius=0.055, color=col) for a, c in zip(lD[good], v[good])],
                             label(rf"{b} bits", font_size=20, color=col).next_to(ax.c2p(lD[good][-1], math.log10(v[good][-1])),
                                                                              RIGHT, buff=0.1)))
        gD, gN, gp = float(p["gD"]), float(p["gN"]), float(p["gpost"])
        law = MathTex(rf"\delta \approx C\, \frac{{D^{{{gD:.2f}}}}}{{N^{{{gN:.2f}}}}}\, e^{{-P/{gp:.2f}}}", font_size=34,
                      color=C.BITS).move_to([3.7, 2.1, 0])
        ll = label(rf"fitted to our sweep: \ every width and length, \ $P$ = bits kept", font_size=20, color=GREY_A)
        ll.next_to(law, DOWN, buff=0.15)
        cards = VGroup(
            history_card(2024, r"Kumar et al., \ \textit{Scaling Laws for Precision}", r"the same form, \ $465$ runs: \ "
                         r"over-trained models are harder to quantize; \ low precision in training acts like fewer "
                         r"parameters, $N(1 - e^{-P/\gamma})$; \ the best training precision: \ $7$ to $8$ bits",
                         width=5.4, color=HIST)).move_to([3.7, -1.0, 0])
        link = note(r"FP8 training: \ Part 18; \ quantized inference: \ Part 19").to_corner(DR, buff=0.2)
        # symmetric round-to-nearest, as compute.py does it: 3 bits, levels -3 ... 3 times (largest |w|) / 3
        nl = NumberLine(x_range=[-1, 1, 1 / 3], length=5.0, include_ticks=True, tick_size=0.12, color=GREY_C)
        g_ = np.random.default_rng(5)
        wv = np.clip(g_.normal(0, 0.4, 14), -0.95, 0.95)
        wv = wv / np.abs(wv).max()  # the largest weight sets the scale
        qv = np.round(wv * 3) / 3
        before = VGroup(*[Dot(nl.n2p(v) + UP * 0.45, radius=0.06, color=C.TRUE_P) for v in wv])
        seen: dict = {}
        after = VGroup()
        for v in qv:
            k_ = seen.get(round(v, 3), 0)
            seen[round(v, 3)] = k_ + 1
            after.add(Dot(nl.n2p(v) + DOWN * (0.35 + 0.14 * k_), radius=0.06, color=C.BITS))
        moves = VGroup(*[Line(b_.get_center(), a_.get_center(), stroke_width=1.2, color=GREY_B) for b_, a_ in zip(before, after)])
        qcap = label(r"rounding to the nearest level \\ ($3$ bits: \ $7$ levels; \ schematic)", font_size=20, color=GREY_A)
        qk = VGroup(label(r"weights", font_size=18, color=C.TRUE_P).next_to(nl, LEFT, buff=0.2).shift(UP * 0.45),
                    label(r"rounded", font_size=18, color=C.BITS).next_to(nl, LEFT, buff=0.2).shift(DOWN * 0.45))
        c0 = nl.get_center().copy()
        qpic = VGroup(nl, before, qk, qcap.next_to(nl, DOWN, buff=1.1)).move_to([3.9, 0.3, 0])
        rel = VGroup(moves, after)
        rel.shift(nl.get_center() - c0)
        grows = gD > 0.05
        d4 = delta[i, :, bits.index(4)]
        okk = np.isfinite(d4)
        said2 = (
            f"the damage grows with training: at four bits, {d4[okk][0]:.3f} bits after two to the "
            f"{int(lD[okk][0])} characters, {d4[okk][-1]:.3f} after two to the {int(lD[okk][-1])}. A model that "
            "has read more has packed more into each weight, so rounding hurts it more. "
            if grows and d4[okk][-1] > d4[okk][0] else
            "the damage barely depends on how long the model was trained. "
        )
        with self.voiceover(
            "Parameters also cost memory, and that can be cut by storing them with fewer bits. Round every weight "
            "of our trained models to a few bits, after training, and measure what it costs. "
            "<bookmark mark='a'/> At width 256, "
            + said2
            + f"<bookmark mark='b'/> Fitted to all our runs, the extra loss grows like D to the {gD:.2f}, shrinks like "
            f"N to the {gN:.2f}, and falls exponentially with every bit kept. <bookmark mark='c'/> In 2024 Tanishq "
            "Kumar and colleagues found the same form in four hundred and sixty-five runs: past some point, more "
            "training data makes a model worse once it is quantized. And training itself in low precision acts like "
            "having fewer parameters; by their fit, the best training precision is seven to eight bits."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(link), FadeIn(qpic))
            self.play(LaggedStart(*[Create(m_) for m_ in moves], lag_ratio=0.05), LaggedStart(*[FadeIn(a_) for a_ in after],
                                                                                           lag_ratio=0.05), run_time=1.5)
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), run_time=max(2.5, vo.until("a")))
            vo.wait_until("b")
            self.play(FadeOut(qpic), FadeOut(rel))
            self.play(Write(law), FadeIn(ll))
            vo.wait_until("c")
            self.play(FadeIn(cards, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"Round every weight to four bits after training. \ Which suffers more: \ a model that "
                          r"read a little, \ or the same model after reading much more?")
        with self.voiceover(
            "Pause and predict. Round every weight to four bits after training. Which suffers more: a model that read "
            "a little, or the same model after reading much more?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"Parameters, \ compute and bits are separate budgets",
                           r"Experts add parameters without adding compute; \ fewer bits save memory, \ at a price "
                           r"that grows with how much the model has read.",
                           r"next: \ why any of these laws are power laws")
        with self.voiceover(
            "The takeaway: parameters, compute and bits can be traded separately. Experts add parameters without "
            "adding compute; fewer bits save memory, at a price that grows with how much the model has read. Next: "
            "why any of these laws should be power laws."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
