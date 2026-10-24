from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (AWQC, ERRC, F, GPTQC, LEVELC, PART, RTNC, WEIGHTC, load)

COLORS = {r"H": C.MLP, r"\delta": GPTQC, r"w": WEIGHTC, r"\hat w": LEVELC, r"e_q": GREY_A}


class GPTQ(VoiceoverScene):
    def construct(self):
        self.card()
        self.objective()
        self.obs()
        self.columns()
        self.awq()
        self.results()

    def card(self):
        card = chapter_card(10, r"GPTQ, \ from Optimal Brain Surgeon", r"Can the error of rounding one weight be "
                            r"undone by moving the others?", part=PART)
        with self.voiceover("Chapter ten. GPTQ, from Optimal Brain Surgeon."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def objective(self):
        rows = [
            cmath(r"\big\|W X - \hat W X\big\|^2", r"=", r"\sum_{\text{rows}} (w - \hat w)^\top H\, (w - \hat w)",
                  colors=COLORS, font_size=38),
            cmath(r"H", r"=", r"X X^\top", colors=COLORS, font_size=38),
        ]
        whys = [why(r"each output row on its own"), why(r"the inputs' second moments, \ from calibration text")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=0.6, edge=6.8)
        # what H does: errors along correlated inputs cancel or add
        pic = VGroup()
        ell = Ellipse(width=4.0, height=1.4, stroke_color=C.MLP, stroke_width=2.5).rotate(0.5)
        ell2 = Ellipse(width=2.4, height=0.84, stroke_color=C.MLP, stroke_width=1.8).rotate(0.5)
        c = Dot(ORIGIN, radius=0.06, color=WEIGHTC)
        pic.add(ell, ell2, c)
        r1 = Arrow(ORIGIN, np.array([0.9, -0.6, 0]), buff=0, color=ERRC, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        r2 = Arrow(ORIGIN, np.array([1.3, 0.75, 0]), buff=0, color=GPTQC, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        pic.add(r1, r2)
        pic.scale(1.2).move_to([-3.4, -2.0, 0])
        pl = label(r"output error, \ as a function of two weights' errors", font_size=20, color=C.MLP)
        pl.next_to(pic, UP, buff=0.15)
        # both labels outside the ellipses, beside their arrows' tips
        l1 = label(r"across the valley: \ costly", font_size=18, color=ERRC).next_to(r1.get_end(), RIGHT, buff=0.12)
        l2 = label(r"along it: \ cheap", font_size=18, color=GPTQC).next_to(ell, RIGHT, buff=0.15).set_y(
            r2.get_end()[1])
        tag = schematic_tag(corner=DL)
        with self.voiceover(
            "Plain rounding treats each weight alone. But what matters is the layer's output. "
            "<bookmark mark='a'/> For a layer W, on real inputs X, the output's error is a sum over rows of a "
            "quadratic form in the rounding errors, with the matrix H. <bookmark mark='b'/> H is X times X "
            "transposed, the second moments of the inputs, estimated from a little calibration text. "
            "<bookmark mark='c'/> When two inputs move together, an error in one weight can be cancelled by "
            "nudging the other: moving along the valley of this quadratic is cheap, across it costly. So round a "
            "weight, then fix the damage with the weights not yet rounded."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(Create(ell), Create(ell2), FadeIn(c), FadeIn(pl), FadeIn(tag))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(GrowArrow(r1), FadeIn(l1))
            self.play(GrowArrow(r2), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def obs(self):
        rows = [
            cmath(r"\min_\delta\ \tfrac12\, \delta^\top H \delta", r"\quad\text{s.t.}\quad",
                  r"e_q^\top \delta = \hat w_q - w_q", colors=COLORS, font_size=34),
            cmath(r"H\delta", r"=", r"\lambda\, e_q", colors=COLORS, font_size=34),
            cmath(r"\delta", r"=", r"\frac{\hat w_q - w_q}{[H^{-1}]_{qq}}\; H^{-1} e_q", colors=COLORS, font_size=34),
            cmath(r"\Delta\text{error}", r"=", r"\frac{(w_q - \hat w_q)^2}{2\,[H^{-1}]_{qq}}", colors=COLORS,
                  font_size=34),
        ]
        whys = [why(r"set weight $q$ to its rounded value; \ move the rest freely"), why(r"Lagrange: \ the gradient "
                r"is parallel to the constraint"), why(r"$\lambda$ from the constraint"),
                why(r"the price of rounding weight $q$")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.4, buff=0.4, edge=6.8)
        hist = VGroup(
            history_card(1990, r"Yann LeCun, John Denker \& Sara Solla", r"Optimal Brain Damage: \ prune the weights "
                         r"whose removal costs least, \ by the Hessian's diagonal", width=4.4, font_size=16,
                         color=GPTQC),
            history_card(1993, r"Babak Hassibi \& David Stork", r"Optimal Brain Surgeon: \ the full inverse Hessian, "
                         r"\ and the update that repairs the rest", width=4.4, font_size=16, color=GPTQC),
            history_card(2022, r"Elias Frantar \& Dan Alistarh", r"Optimal Brain Compression: \ the same update, \ "
                         r"for rounding instead of removing", width=4.4, font_size=16, color=GPTQC),
        ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The question is old. <bookmark mark='a'/> Fix weight q at its rounded value, and move all the "
            "others by delta to keep the output error, one half delta H delta, as small as possible. "
            "<bookmark mark='b'/> With a Lagrange multiplier, the optimum has H delta parallel to the direction of "
            "weight q. <bookmark mark='c'/> Solving: delta is the rounding error over the q-th diagonal entry of H "
            "inverse, times H inverse's q-th column. <bookmark mark='d'/> And the error that's left is the "
            "rounding error squared, over twice that diagonal entry. <bookmark mark='e'/> This is the Optimal "
            "Brain Surgeon of Babak Hassibi and David Stork, from 1993, which followed Yann LeCun's Optimal Brain "
            "Damage: they used it to prune networks. In 2022 Elias Frantar and Dan Alistarh used it to round."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(h_, shift=UP * 0.2) for h_ in hist], lag_ratio=0.4), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def columns(self):
        q = load("gptq")
        tr = np.asarray(q["trace"])  # (16 steps, 16 values): the row after each column is rounded
        w0, qf, rt = np.asarray(q["trace_w"]), np.asarray(q["trace_q"]), np.asarray(q["trace_rtn"])
        n = len(w0)
        top = float(np.abs(np.concatenate([w0, qf, tr.ravel()])).max())
        X0, dx, Y0, Hh = -5.2, 0.62, -0.3, 1.6
        base = Line([X0 - 0.4, Y0, 0], [X0 + dx * n, Y0, 0], color=GREY_C, stroke_width=1.5)
        levels = sorted(set(np.round(np.concatenate([qf, rt]), 9)))
        lv = VGroup(*[DashedLine([X0 - 0.4, Y0 + Hh * v / top, 0], [X0 + dx * n, Y0 + Hh * v / top, 0],
                                 color=LEVELC, dash_length=0.05, stroke_width=1).set_stroke(opacity=0.45)
                      for v in levels])

        def bars(v, done):
            return VGroup(*[Rectangle(width=dx * 0.62, height=max(abs(Hh * x / top), 0.01), stroke_width=0,
                                      fill_color=LEVELC if i < done else WEIGHTC, fill_opacity=0.85)
                            .move_to([X0 + dx * i, Y0 + Hh * x / top / 2, 0]) for i, x in enumerate(v)])

        ghost = VGroup(*[Rectangle(width=dx * 0.62, height=max(abs(Hh * x / top), 0.01), stroke_color=GREY_B,
                                   stroke_width=1, fill_opacity=0).move_to([X0 + dx * i, Y0 + Hh * x / top / 2, 0])
                         for i, x in enumerate(w0)])
        cur = bars(w0, 0)
        head = label(r"one row of a real layer: \ $16$ weights, \ $3$ bits, \ GPTQ from left to right", font_size=22,
                     color=GREY_A).to_edge(UP, buff=0.4)
        ptr = Triangle(fill_color=GPTQC, fill_opacity=1, stroke_width=0).scale(0.1).rotate(PI)
        ptr.move_to([X0, Y0 + Hh + 0.3, 0])
        er, eg = float(q["trace_err_rtn"]), float(q["trace_err_gptq"])
        lr_, lg_ = float(q["layer_err"]["rtn_3"]), float(q["layer_err"]["gptq_3"])
        res = VGroup(label(rf"this row's output error, \ rounding each alone: \ ${er:.3f}$", font_size=21, color=RTNC),
                     label(rf"this row's output error, \ GPTQ: \ ${eg:.3f}$", font_size=21, color=GPTQC),
                     label(rf"the whole layer \ (\texttt{{{q['layer']}}}): \ ${lr_:.3f}$ $\to$ ${lg_:.3f}$",
                           font_size=21, color=GPTQC))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.4, -2.55, 0])
        if eg < 0.85 * er:
            trace_say = (f"but together they make a better output: an error of {eg:.3f} on the calibration inputs, "
                         f"against {er:.3f} for rounding each weight alone.")
        else:
            trace_say = (f"but together they make a slightly better output: an error of {eg:.3f} on the calibration "
                         f"inputs, against {er:.3f} for rounding each weight alone. Sixteen weights leave little room "
                         "to make up for an error.")
        hc = history_card(2022, r"Elias Frantar, Saleh Ashkboos, Torsten Hoefler \& Dan Alistarh", rf"GPTQ: \ one "
                          rf"column order for every row, \ ${F.GPTQ['params'] / 1e9:.0f}$B parameters in about "
                          rf"${F.GPTQ['hours']}$ GPU-hours", width=5.2, font_size=16, color=GPTQC).move_to([-3.4, 2.45, 0])
        with self.voiceover(
            "Rounding one weight at a time, with the best update, is too slow for billions of weights. "
            "<bookmark mark='a'/> GPTQ, from Frantar, Ashkboos, Hoefler and Alistarh in 2022, makes three "
            "changes: round the columns in one fixed order, the same for every row; get every update from one "
            "Cholesky factorization of H inverse; and apply them in blocks. A 175-billion-parameter model took "
            "about four GPU-hours. <bookmark mark='b'/> Here it is on one row of a real layer of our model, at "
            "three bits. Each column is rounded, and its error is pushed onto the columns still to come. "
            "<bookmark mark='c'/> The final weights aren't the nearest levels to the originals, the grey outlines, "
            + trace_say + " <bookmark mark='d'/> Over "
            f"the whole layer, with every input to spread it across, GPTQ's error is {lg_:.3f}, against {lr_:.3f}."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(lv), FadeIn(cur), FadeIn(ghost))
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(ptr))
            for j in range(n):
                nxt = bars(tr[j], j + 1)
                self.play(Transform(cur, nxt), ptr.animate.move_to([X0 + dx * min(j + 1, n - 1), Y0 + Hh + 0.3, 0]),
                          run_time=0.45)
            vo.wait_until("c")
            self.play(FadeOut(ptr), FadeIn(res[:2]))
            vo.wait_until("d")
            self.play(FadeIn(res[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def awq(self):
        rows = [
            cmath(r"Q(w\,s) \cdot \tfrac{x}{s}", r"\quad\text{error} \approx", r"\tfrac{\Delta}{s}\, |x|",
                  font_size=36),
            cmath(r"s_j", r"=", r"\overline{|x_j|}^{\,\alpha}", r",\quad \alpha \in [0, 1] \text{ chosen on calibration}",
                  font_size=36),
        ]
        rows[0][2].set_color(AWQC)
        rows[1][2].set_color(AWQC)
        whys = [why(r"scale a channel up before rounding; \ its step shrinks relative to it"),
                why(r"large where the inputs are large")]
        step = ladder(self, rows, whys, keep=2, top=2.9, x=-1.0, buff=0.7, edge=6.8)
        hc = history_card(2023, r"Ji Lin et al., \ AWQ", rf"protect the ${F.AWQ['salient']}\%$ of weights whose "
                          r"inputs are largest; \ MLSys 2024 best paper", width=4.4, font_size=16,
                          color=AWQC).move_to([4.5, -0.95, 0])
        o = load("outliers")
        prof = np.asarray(o["profile_qkv"], float)
        nc = len(prof)
        cut = np.sort(prof)[-max(1, nc // 100)]
        chans = VGroup(*[Rectangle(width=9.0 / nc * 0.8, height=max(1.3 * v / prof.max(), 0.01), stroke_width=0,
                                   fill_color=AWQC if v >= cut else C.TOKEN, fill_opacity=0.85)
                         .move_to([-6.0 + 9.0 * (i + 0.5) / nc, -3.1 + 0.65 * v / prof.max(), 0])
                         for i, v in enumerate(prof)])
        chl = label(rf"the inputs of one of our layers, \ channel by channel \ (largest seen): \\ AWQ's scales grow "
                    rf"with them; \ the top $1\%$ in orange", font_size=18, color=GREY_A).next_to(chans, UP, buff=0.2)
        chl.align_to(chans, LEFT)
        q = load("gptq")
        alphas = [v for k, v in q["res"].items() if k.endswith("_alpha")]
        with self.voiceover(
            "A simpler idea came next. In 2023 Ji Lin and colleagues noticed that a weight matters in proportion "
            "to the size of its input. <bookmark mark='a'/> So multiply each input channel's weights by s before "
            "rounding, and divide the input by s, which folds away for free. The rounding error, relative to that "
            "channel, shrinks by s. <bookmark mark='b'/> AWQ makes s the average size of the channel's input, to "
            "a power alpha chosen on calibration text: activation-aware weight quantization. "
            f"<bookmark mark='c'/> On our model the best alpha came out small, {min(alphas):.2f} to "
            f"{max(alphas):.2f}: our inputs are fairly even, so there is little to protect."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in chans], lag_ratio=0.004), FadeIn(chl),
                      run_time=1.5)
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(hc))
            vo.wait_until("c")
            self.play(Indicate(rows[1][2], color=AWQC))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        q = load("gptq")
        base = float(q["fp32"])
        res = q["res"]
        seeds = q["seeds"]
        configs = [(4, "row"), (4, "64"), (3, "row"), (3, "64")]
        g = VGroup()
        hi = max(max([res[f"rtn_{b}_{gg}"]] + [res[f"{m}_{b}_{gg}_s{s}"] for m in ("gptq", "awq") for s in seeds])
                 for b, gg in configs) - base
        for b, gg in configs:
            r_ = res[f"rtn_{b}_{gg}"] - base
            gp = [res[f"gptq_{b}_{gg}_s{s}"] - base for s in seeds]
            aw = [res[f"awq_{b}_{gg}_s{s}"] - base for s in seeds]
            rows = VGroup()
            for k, (nm, vals, col) in enumerate(((r"rounding", [r_], RTNC), (r"AWQ", aw, AWQC), (r"GPTQ", gp, GPTQC))):
                m = float(np.mean(vals))
                w = max(m / (hi * 1.1) * 3.4, 0.02)
                bar = Rectangle(width=w, height=0.26, stroke_width=0, fill_color=col, fill_opacity=0.85)
                bar.move_to([w / 2, -k * 0.34, 0])
                spread = VGroup()
                if len(vals) > 1:
                    lo_, hi_ = min(vals) / (hi * 1.1) * 3.4, max(vals) / (hi * 1.1) * 3.4
                    spread = Line([lo_, -k * 0.34, 0], [hi_, -k * 0.34, 0], color=WHITE, stroke_width=2.5)
                nm_ = label(nm, font_size=18, color=col).move_to([-0.15, -k * 0.34, 0], aligned_edge=RIGHT)
                v_ = MathTex(f"{m:+.3f}", font_size=18, color=col).next_to(bar, RIGHT, buff=0.1)
                rows.add(VGroup(nm_, bar, spread, v_))
            t = label(rf"${b}$ bits, \ " + (r"a scale per row" if gg == "row" else r"a scale per $64$"), font_size=20,
                      color=GREY_A)
            g.add(VGroup(t, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        g.arrange_in_grid(rows=2, cols=2, buff=(1.0, 0.5))
        g.scale(min(1.2, 12.6 / g.width)).move_to([0, -0.4, 0])
        head = label(r"extra loss on held-out novels \ (nats per token): \ weights only, \ $3$ calibration sets "
                     r"\ (white: \ their range)", font_size=22, color=GREY_A).to_edge(UP, buff=0.35)
        r3 = res["rtn_3_row"] - base
        g3 = float(np.mean([res[f"gptq_3_row_s{s}"] - base for s in seeds]))
        a3 = float(np.mean([res[f"awq_3_row_s{s}"] - base for s in seeds]))
        r4 = res["rtn_4_64"] - base
        g4 = float(np.mean([res[f"gptq_4_64_s{s}"] - base for s in seeds]))
        cut3 = 1 - g3 / r3
        g3s = [res[f"gptq_3_row_s{s}"] - base for s in seeds]
        if cut3 > 0.25 and max(g3s) < 0.85 * r3:
            gptq_say = (f"the difference is large: rounding costs {r3:.3f}, GPTQ {g3:.3f}, {100 * cut3:.0f} percent "
                        "less, whichever calibration text it saw.")
        else:
            gptq_say = (f"rounding costs {r3:.3f}, GPTQ {g3:.3f} on average, {100 * cut3:.0f} percent less, and how "
                        "much depends on the calibration text.")
        awq_say = (f"it costs {a3:.3f}: on our model, it barely helps." if a3 > 0.9 * r3 else
                   f"it costs {a3:.3f}, {100 * (1 - a3 / r3):.0f} percent less than rounding.")
        with self.voiceover(
            "All three, on the whole model: every block matrix rounded, the loss measured on held-out novels, and "
            "GPTQ and AWQ each calibrated on three different samples of text. <bookmark mark='a'/> At four bits "
            f"with a scale per 64 weights, rounding costs {r4:.3f} nats a token and GPTQ {g4:.3f}. "
            "<bookmark mark='b'/> At three bits with a scale per row, " + gptq_say + " As for AWQ, " + awq_say +
            " <bookmark mark='c'/> Spending the error where the inputs don't look is what makes three and four "
            "bits usable."
        ) as vo:
            self.play(FadeIn(head))
            self.wait(2.0)
            self.play(FadeIn(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(g[2]), FadeIn(g[3]))
            vo.wait_until("c")
            self.play(Indicate(g[2], color=GPTQC, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()
