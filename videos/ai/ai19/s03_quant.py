from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.compute import FP4, load

MODE_NAMES = {"fp32": r"32-bit floats", "int8": r"8 bits", "int4": r"4 bits", "int3": r"3 bits", "fp4": r"FP4, \ scaled per $32$"}
MODE_COLORS = {"fp32": GREY_B, "int8": C.TRUE_P, "int4": C.INTERVAL, "int3": C.SURPRISE, "fp4": C.BITS}


class Quant(VoiceoverScene):
    def construct(self):
        self.card()
        self.rounding()
        self.results()
        self.formats()
        self.gptq()

    def card(self):
        card = chapter_card(2, r"Fewer bits per number", r"How coarsely can a model's numbers be stored?", part=19)
        with self.voiceover("Chapter two. Fewer bits per number."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def rounding(self):
        q = load("quant")
        h, e = np.asarray(q["hist_w"], float), np.asarray(q["hist_edges"])
        lo, hi = float(e[0]), float(e[-1])
        ax = CornerAxes(x_range=[lo, hi, (hi - lo) / 4], y_range=[0, 1.05, 0.5], x_length=9.0, y_length=2.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(UP * 0.9)
        bars = VGroup(*[Rectangle(width=9.0 / len(h) * 0.9, height=max(2.6 * v / h.max(), 0.005), stroke_width=0, fill_color=GREY_B,
                                  fill_opacity=0.8).move_to(ax.c2p((e[i] + e[i + 1]) / 2, 0) + UP * 1.3 * v / h.max())
                        for i, v in enumerate(h)])
        hl = label(r"the weights of one layer of Part 11's transformer", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        m = max(abs(lo), abs(hi))
        levels4 = np.linspace(-m, m, 15)
        ticks4 = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, 1.05), color=C.INTERVAL, stroke_width=1.5).set_stroke(opacity=0.8) for x in levels4])
        t4 = label(r"$4$ bits: \ $15$ evenly spaced values, \ symmetric about $0$", font_size=24, color=C.INTERVAL).to_edge(LEFT, buff=0.6).shift(DOWN * 1.4)
        s = m / 6
        levelsf = np.concatenate([-FP4[::-1][:-1], FP4]) * s
        ticksf = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, 1.05), color=C.BITS, stroke_width=1.5).set_stroke(opacity=0.8) for x in levelsf])
        tf = label(r"FP4: \ $\pm\{0, \tfrac12, 1, \tfrac32, 2, 3, 4, 6\}$ \ times a scale: \\ dense near zero, \ where the weights are",
                   font_size=24, color=C.BITS).next_to(t4, DOWN, buff=0.3).align_to(t4, LEFT)
        with self.voiceover(
            "The other way to cut memory traffic: store each number in fewer bits. Here are the weights of one layer "
            "of our transformer: most near zero, a few larger. <bookmark mark='a'/> With four bits, each weight is "
            "rounded to one of fifteen evenly spaced values, the same number either side of zero. <bookmark mark='b'/> "
            "The newest chips use FP4 instead: "
            "a tiny floating-point number, with more values near zero where the weights crowd, and a shared scale "
            "for every block of thirty-two."
        ) as vo:
            self.play(FadeIn(hl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(ticks4), FadeIn(t4))
            vo.wait_until("b")
            self.play(FadeOut(ticks4), Create(ticksf), FadeIn(tf))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        q = load("quant")
        modes = [str(m) for m in q["modes"]]
        vals = [float(q[f"bits_{m}"]) for m in modes]
        base = vals[0]
        lo = base - 0.05
        hi = max(vals) + 0.05
        g = VGroup()
        for i, (m, v) in enumerate(zip(modes, vals)):
            y = 1.8 - i * 0.8
            nm = label(MODE_NAMES[m], font_size=24, color=MODE_COLORS[m]).move_to([-1.6, y, 0], aligned_edge=RIGHT)
            w = (v - lo) / (hi - lo) * 6.0
            bar = Rectangle(width=max(w, 0.02), height=0.42, stroke_width=0, fill_color=MODE_COLORS[m], fill_opacity=0.85)
            bar.move_to([-1.3 + max(w, 0.02) / 2, y, 0])
            val = MathTex(f"{v:.3f}", font_size=26, color=MODE_COLORS[m]).next_to(bar, RIGHT, buff=0.12)
            g.add(VGroup(nm, bar, val))
        head = label(rf"bits per character on the passage \ (axis from ${lo:.2f}$)", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        d8, d4 = vals[modes.index("int8")] - base, vals[modes.index("int4")] - base
        d3, df = vals[modes.index("int3")] - base, vals[modes.index("fp4")] - base
        foot = label(r"real models are trained in low precision from the start \ (FP8, \ FP4)", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What does it cost? <bookmark mark='a'/> Rounded to eight bits, our transformer is "
            f"{'no worse' if d8 < 0.005 else f'{d8:.3f} bits worse'}. At four bits, {d4:.3f} bits worse per character, "
            f"for an eighth of the memory; at three, {d3:.2f} worse: it starts to break. "
            + (f"FP4, with its scale for every block of thirty-two, loses only {df:.3f}: better than plain four bits, "
               "for the same memory. " if df < d4 else f"FP4 loses {df:.3f}. ")
            + "<bookmark mark='b'/> Big models tolerate "
            "rounding even better, the newest are trained in eight or even four bits from the start, and there are "
            "better formats, and better ways to round, than the plain ones here."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in g], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formats(self):
        f = load("formats")
        bpw = f["bpw"]

        def card(x, name, sub, n, scale_name, scale_bits, col):
            cells = VGroup(*[Rectangle(width=0.1, height=0.42, stroke_color=col, stroke_width=1, fill_color=col, fill_opacity=0.35)
                             for _ in range(n)]).arrange(RIGHT, buff=0.02)
            sc = Rectangle(width=0.1 * scale_bits / 4, height=0.42, stroke_color=C.SURPRISE, stroke_width=1.5, fill_color=C.SURPRISE,
                           fill_opacity=0.5)
            row = VGroup(cells, sc).arrange(RIGHT, buff=0.1)
            t = VGroup(label(name, font_size=28, color=col), label(sub, font_size=20, color=GREY_A)).arrange(DOWN, buff=0.08)
            l1 = label(rf"${n}$ numbers in E2M1 \ ($4$ bits each)", font_size=18, color=col).next_to(cells, DOWN, buff=0.1)
            l2 = label(scale_name, font_size=18, color=C.SURPRISE).next_to(sc, UP, buff=0.1)
            g = VGroup(t, row, l1, l2)
            t.next_to(row, UP, buff=0.55)
            return g.move_to([x, 1.9, 0])

        mx = card(-3.5, r"MXFP4", r"OCP standard; \ gpt-oss ships its experts in it", 32, r"E8M0: \ a power of two", 8, C.BITS)
        nv = card(3.5, r"NVFP4", r"NVIDIA Blackwell", 16, r"E4M3: \ an 8-bit float", 8, C.TRUE_P)
        f_mx = MathTex(r"w \approx 2^{\lfloor \log_2 \max|w| \rfloor - 2} \cdot m", font_size=28, color=C.BITS).next_to(mx, DOWN, buff=0.3)
        f_nv = MathTex(r"w \approx s_{\text{tensor}} \cdot s_{\text{block}} \cdot m", font_size=28, color=C.TRUE_P).next_to(nv, DOWN, buff=0.3)
        b_mx = label(rf"${float(bpw['mxfp4']):.2f}$ bits per weight", font_size=20, color=GREY_A).next_to(f_mx, DOWN, buff=0.12)
        b_nv = label(rf"${float(bpw['nvfp4']):.2f}$ bits per weight", font_size=20, color=GREY_A).next_to(f_nv, DOWN, buff=0.12)
        mset = MathTex(r"m \in \pm\{0, \tfrac12, 1, \tfrac32, 2, 3, 4, 6\}", font_size=28).move_to([0, -0.85, 0])
        # results
        rows = [("fp32", r"32-bit floats", GREY_B), ("int4", r"$4$-bit integers, \ per row", C.INTERVAL),
                ("fp4", MODE_NAMES["fp4"], GREY_A), ("mxfp4", r"MXFP4", C.BITS), ("nvfp4", r"NVFP4", C.TRUE_P)]
        f = dict(f, fp4=float(load("quant")["bits_fp4"]))  # FP4 with an exact (fp32) scale per block, from the first section
        vals = [float(f[k]) for k, _, _ in rows]
        lo, hi = vals[0] - 0.03, max(vals) + 0.02
        bars = VGroup()
        for i, ((k, nm, col), v) in enumerate(zip(rows, vals)):
            y = -1.6 - i * 0.44
            w = max((v - lo) / (hi - lo) * 5.0, 0.02)
            b = Rectangle(width=w, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([-0.6 + w / 2, y, 0])
            bars.add(VGroup(label(nm, font_size=20, color=col).move_to([-0.85, y, 0], aligned_edge=RIGHT), b,
                            MathTex(f"{v:.3f}", font_size=22, color=col).next_to(b, RIGHT, buff=0.1)))
        bl = label(rf"bits per character \ (axis from ${lo:.2f}$)", font_size=18, color=GREY_A).next_to(bars, LEFT, buff=0.4).shift(UP * 0.5)
        keep_in_frame(bl)
        best = min(("int4", "mxfp4", "nvfp4"), key=lambda k: float(f[k]))
        d = {k: float(f[k]) - vals[0] for k in ("int4", "fp4", "mxfp4", "nvfp4")}
        say = {"int4": "plain four-bit integers", "mxfp4": "MXFP4", "nvfp4": "NVFP4"}
        with self.voiceover(
            "Two four-bit float formats now matter, and the difference between them is all in the scales. "
            "<bookmark mark='a'/> MXFP4, the open standard, shares one scale among thirty-two numbers, and the scale "
            "is a pure power of two: cheap to apply, but coarse, so a block's largest weight can land anywhere from "
            "four to eight on the E2M1 grid, and past six it's clipped. OpenAI's gpt-oss stores its experts this way. "
            "<bookmark mark='b'/> NVFP4, on NVIDIA's Blackwell chips, uses blocks of sixteen, and each scale is itself "
            "a small eight-bit float, so it can fit the block's largest weight to six almost exactly; one more scale "
            f"for the whole tensor keeps everything in range. It costs {float(bpw['nvfp4']):.1f} bits per weight "
            f"instead of {float(bpw['mxfp4']):.2f}. <bookmark mark='c'/> On our transformer: "
            f"{say['mxfp4']} loses {d['mxfp4']:.3f} bits a character, {say['nvfp4']} {d['nvfp4']:.3f}, and plain "
            f"four-bit integers with a scale per row {d['int4']:.3f}. The best here is {say[best]}. For comparison, "
            f"FP4 with an exact scale for every block of thirty-two, from before, lost {d['fp4']:.3f}: "
            + ("rounding the scale to a power of two is what costs MXFP4 its extra."
               if d["mxfp4"] > d["fp4"] + 0.003 else "the rounded scales cost almost nothing.")
        ) as vo:
            self.play(FadeIn(mx[0]), FadeIn(mx[1]), FadeIn(mx[2]), FadeIn(mx[3]), FadeIn(mset))
            vo.wait_until("a")
            self.play(Write(f_mx), FadeIn(b_mx))
            vo.wait_until("b")
            self.play(FadeIn(nv), Write(f_nv), FadeIn(b_nv))
            vo.wait_until("c")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in bars], lag_ratio=0.25), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gptq(self):
        from videos.ai.ai19.formats import gptq, rtn

        f = load("formats")
        # a small layer, in-scene: 6 outputs, 10 correlated inputs; round column by column, pushing errors right
        g = np.random.default_rng(22)
        X = g.normal(size=(400, 10)) @ (np.eye(10) + 0.8 * g.normal(size=(10, 10)) / np.sqrt(10))
        H = X.T @ X / len(X)
        W = g.normal(size=(6, 10))
        colors = {r"q_j": C.INTERVAL, r"\delta": C.SURPRISE, r"H": C.TRUE_P}
        eqs = VGroup(
            cmath(r"q_j", r"= \operatorname{round}(w_j)", colors=colors, font_size=30),
            cmath(r"\delta", r"= \frac{w_j -", r"q_j", r"}{[", r"H", r"^{-1}]_{jj}}", colors=colors, font_size=30),
            cmath(r"w_{k} \;\leftarrow\; w_{k} -", r"\delta", r"\, [", r"H", r"^{-1}]_{jk}, \quad k > j", colors=colors, font_size=30),
            cmath(r"H", r"= \mathbb{E}\big[x\,x^{\top}\big]", colors=colors, font_size=30),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([3.4, 1.9, 0])
        notes = VGroup(label(r"round one column of inputs", font_size=18, color=GREY_A),
                       label(r"its error, \ weighted", font_size=18, color=GREY_A),
                       label(r"the columns still to come absorb it", font_size=18, color=GREY_A),
                       label(r"from real inputs: \ which inputs move together", font_size=18, color=GREY_A))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.06).align_to(e_, LEFT)
        for k in range(1, len(eqs)):
            VGroup(*eqs[k:], *notes[k:]).shift(DOWN * 0.15)
        cell = 0.42

        def grid(M, top):
            gg = VGroup()
            for i in range(M.shape[0]):
                for j in range(M.shape[1]):
                    v = float(np.clip(M[i, j] / top, -1, 1))
                    gg.add(Square(cell, stroke_color=GREY_D, stroke_width=1,
                                  fill_color=interpolate_color(ManimColor(C.TRUE_P), ManimColor(C.SURPRISE), (v + 1) / 2),
                                  fill_opacity=0.15 + 0.75 * abs(v)).move_to([j * cell, -i * cell, 0]))
            return gg

        top = float(np.abs(W).max())
        gW = grid(W, top).move_to([-3.6, 1.2, 0])
        gl = label(r"a layer's weights: \ $6$ outputs, \ $10$ inputs", font_size=20, color=GREY_A).next_to(gW, UP, buff=0.12)
        # the GPTQ pass, column by column, from the real algorithm's intermediate states
        states = []
        Wk = W.astype(float).copy()
        Hd = H + 0.01 * np.mean(np.diag(H)) * np.eye(10)
        U = np.linalg.cholesky(np.linalg.inv(Hd)).T
        qmax, s = 3, np.abs(W).max(1) / 3
        for j in range(10):
            q = np.clip(np.round(Wk[:, j] / s), -qmax - 1, qmax) * s
            err = (Wk[:, j] - q) / U[j, j]
            Wk[:, j] = q
            Wk[:, j + 1:] -= np.outer(err, U[j, j + 1:])
            states.append(Wk.copy())
        cur = Square(cell * 1.06, stroke_color=C.INTERVAL, stroke_width=3)
        colbox = Rectangle(width=cell * 1.05, height=cell * 6.05, stroke_color=C.INTERVAL, stroke_width=3).move_to(
            VGroup(*[gW[i * 10] for i in range(6)]))
        er, eg = float(f["layer_err_rtn3"]), float(f["layer_err_gptq3"])  # a real layer of our transformer, real inputs
        res = VGroup(label(rf"one real layer \ ($512 \times 128$), \ $3$ bits: \\ output error \ rounding ${100 * er:.0f}\%$, "
                           rf"\ GPTQ ${100 * eg:.0f}\%$", font_size=20, color=C.INTERVAL)).next_to(gW, DOWN, buff=0.3)
        # the model: 4 and 3 bits, three ways
        rows = [("int4", r"$4$ bits, \ rounded", C.INTERVAL), ("had4", r"$4$ bits, \ rotated first", C.BITS),
                ("gptq4", r"$4$ bits, \ GPTQ", C.TRUE_P),
                ("int3", r"$3$ bits, \ rounded", C.INTERVAL), ("had3", r"$3$ bits, \ rotated first", C.BITS),
                ("gptq3", r"$3$ bits, \ GPTQ", C.TRUE_P)]
        base = float(f["fp32"])
        vals = [float(f[k]) for k, _, _ in rows]
        hi = max(vals)
        tab = VGroup()
        for i, ((k, nm, col), v) in enumerate(zip(rows, vals)):
            y = -1.05 - i * 0.36 - (0.15 if i >= 3 else 0)
            w = max((v - base) / (hi - base) * 3.6, 0.02)
            b = Rectangle(width=w, height=0.28, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([2.0 + w / 2, y, 0])
            tab.add(VGroup(label(nm, font_size=18, color=col).move_to([1.8, y, 0], aligned_edge=RIGHT), b,
                           MathTex(rf"+{v - base:.3f}", font_size=20, color=col).next_to(b, RIGHT, buff=0.08)))
        tl = label(r"our transformer: \ bits per character lost", font_size=18, color=GREY_A).next_to(tab, UP, buff=0.12)
        crest, crest_r = float(f["crest"]), float(f["crest_rot"])
        cite_ = cite(r"E.~Frantar et al., \textit{GPTQ} (2022); \ S.~Ashkboos et al., \textit{QuaRot} (2024)", corner=DR)
        g3 = float(f["gptq3"]) - base
        r3 = float(f["int3"]) - base
        h3 = float(f["had3"]) - base
        g4, r4, h4 = (float(f[k]) - base for k in ("gptq4", "int4", "had4"))
        # a row with one outlier, before and after a 16 x 16 Hadamard rotation (computed here)
        from videos.ai.ai19.formats import hadamard

        v = np.random.default_rng(5).normal(0, 0.25, 16)
        v[6] = 3.0
        vr = hadamard(16) @ v

        def bars(x, y, col):
            return VGroup(*[Rectangle(width=0.16, height=max(abs(float(z)) * 0.32, 0.01), stroke_width=0, fill_color=col, fill_opacity=0.85)
                            .move_to([-5.6 + 0.2 * i, y + float(z) * 0.16, 0]) for i, z in enumerate(x)])

        rb, ra = bars(v, -2.0, C.INTERVAL), bars(vr, -3.25, C.BITS)
        rbl = label(r"a row with one outlier", font_size=16, color=C.INTERVAL).next_to(rb, RIGHT, buff=0.2)
        ral = label(r"after a Hadamard rotation", font_size=16, color=C.BITS).next_to(ra, RIGHT, buff=0.2)
        spread = crest_r < 0.8 * crest
        with self.voiceover(
            "Two tricks make low precision work much better than plain rounding. The first is GPTQ. "
            "<bookmark mark='a'/> Round a layer's weights one input column at a time. <bookmark mark='b'/> Each "
            "rounding leaves an error; <bookmark mark='c'/> instead of accepting it, nudge the weights on the inputs "
            "not yet rounded, so the layer's output barely changes. How much to nudge comes from H, the inputs' "
            "second moment, measured on real text: inputs that move together can cover for each other. "
            f"<bookmark mark='d'/> On a real layer of our transformer, at three bits, the error in its output drops from "
            f"{100 * er:.0f} to {100 * eg:.0f} percent. <bookmark mark='e'/> The second trick is a rotation. In large models a few "
            "weights and activations are huge outliers, and one outlier forces a coarse scale on its whole row. "
            "Multiply by a Hadamard matrix first, an orthogonal matrix of plus and minus ones, and the outlier is "
            "spread evenly over the row; the rotation is undone exactly afterwards. "
            + (f"In one of our layers, the largest weight drops from {crest:.1f} to {crest_r:.1f} times the typical one. "
               if spread else
               f"Our small model has no such outliers: a row's largest weight is only about {crest:.1f} times the "
               f"typical one, before and after. ")
            + f"<bookmark mark='f'/> On our whole transformer at three bits: plain rounding loses {r3:.3f} bits a "
            f"character, GPTQ only {g3:.3f}, "
            + (f"and rotating first {h3:.3f}. " if h3 < r3 else
               f"and rotating first {h3:.3f}, worse: with nothing to spread, it only spreads each rounding error over "
               "every input, including the few that carry large activations. ")
            + "Real systems rotate the activations too, so they can be rounded as well, and pair the rotation with GPTQ."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(gW), FadeIn(gl))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(notes[0]), Create(colbox))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(notes[2]), Write(eqs[3]), FadeIn(notes[3]))
            for j in range(10):
                self.play(Transform(gW, grid(states[j], top).move_to(gW)),
                          colbox.animate.move_to(VGroup(*[gW[i * 10 + min(j + 1, 9)] for i in range(6)])), run_time=0.35)
            vo.wait_until("d")
            self.play(FadeIn(res), FadeOut(colbox))
            vo.wait_until("e")
            self.play(FadeIn(rb), FadeIn(rbl))
            self.play(TransformFromCopy(rb, ra), FadeIn(ral))
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[:3]], lag_ratio=0.2))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab[3:]], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()
