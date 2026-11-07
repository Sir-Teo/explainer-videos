from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, image, load

B3 = [1 / 16, 1 / 4, 3 / 8, 1 / 4, 1 / 16]          # the a-trous kernel of explainer/cs/graphics/path.py
CROP = (slice(62, 126), slice(52, 116))             # the blue ball and the white ball's shadow
CEIL = (slice(0, 32), slice(4, 68))                 # the ceiling, lit only indirectly


def crop(img, c=CROP):
    return np.ascontiguousarray(np.asarray(img)[c])


def secs(s: float) -> str:
    return f"{s:.3f} s" if s < 0.1 else f"{s:.2f} s"


class Ours(VoiceoverScene):
    def construct(self):
        self.card()
        self.convergence()
        self.loglog()
        self.strategies()
        self.roulette()
        self.mis()
        self.atrous()
        self.denoised()

    def card(self):
        card = chapter_card(12, r"Our path tracer, \ and denoising", r"How fast does the noise go away?",
                            lit=(1990, 2010), extra=((1990, r"Arvo and Kirk: \ Russian roulette"),
                                                     (2010, r"Dammertz et al.: \ \`a-trous denoising")), part=PART)
        with self.voiceover("Chapter twelve. Our path tracer, and denoising."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the noise, up close
    def convergence(self):
        p = load("path")
        rows = {r["spp"]: r for r in p["convergence"]["rows"]}
        head = label(r"The noise, \ up close", font_size=36).to_edge(UP, buff=0.3)
        tiles = Group()
        for k in (1, 4, 16, 64, 256):
            g = image(crop(p[f"spp{k}"]), height=1.85)
            c1 = label(rf"{k} path{'s' if k > 1 else ''}", font_size=18, color=WHITE).next_to(g, DOWN, buff=0.1)
            c2 = label(secs(rows[k]["seconds"]), font_size=17, color=HEAD).next_to(c1, DOWN, buff=0.06)
            tiles.add(Group(g, c1, c2))
        g = image(crop(p["reference"]), height=1.85)
        c1 = label(r"reference", font_size=18, color=GREY_A).next_to(g, DOWN, buff=0.1)
        c2 = label(r"2048 paths", font_size=17, color=GREY_A).next_to(c1, DOWN, buff=0.06)
        tiles.add(Group(g, c1, c2))
        tiles.arrange(RIGHT, buff=0.22).next_to(head, DOWN, buff=0.35)
        src = note(r"a 64 $\times$ 64 corner of our 128 $\times$ 128 render, \ enlarged; \ times on one core",
                   font_size=16).next_to(tiles, DOWN, buff=0.12)
        f0 = MathTex(r"\hat L_N", r"=", r"\frac{1}{N}\sum_{k=1}^{N} X_k", font_size=34)
        f1 = MathTex(r"\operatorname{Var}[\hat L_N]", r"=", r"\frac{1}{N^2}\cdot N\sigma^2", r"=",
                     r"\frac{\sigma^2}{N}", font_size=34)
        f2 = MathTex(r"\text{error}", r"=", r"\frac{\sigma}{\sqrt{N}}", font_size=38, color=YES)
        fs = VGroup(f0, f1, f2).arrange(RIGHT, buff=0.9).move_to([0, -1.5, 0])
        arrows = VGroup(*[MathTex(r"\Rightarrow", font_size=34, color=GREY_B).move_to(
            (fs[i].get_right() + fs[i + 1].get_left()) / 2) for i in range(2)])
        fn = VGroup(note(r"each path an independent estimate", font_size=17).next_to(f0, DOWN, buff=0.15),
                    note(r"variances of independent terms add", font_size=17).next_to(f1, DOWN, buff=0.15),
                    note(r"four times the paths, \ half the noise", font_size=17, color=YES).next_to(f2, DOWN,
                                                                                                    buff=0.15))
        with self.voiceover(
            "Here is one corner of our render, enlarged: the white ball, the blue ball and the green wall. <bookmark "
            "mark='a'/> One path per pixel is speckle. <bookmark mark='b'/> Each step multiplies the paths by four, "
            "and the time with them, from under three hundredths of a second to over six seconds. <bookmark "
            "mark='c'/> Each path is an independent random estimate, and the pixel is their average. <bookmark "
            "mark='d'/> The variance of an average of N independent terms is sigma squared over N, <bookmark "
            "mark='e'/> so the error falls as one over the square root of N: four times the work halves the noise."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0]), FadeIn(src))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t) for t in tiles[1:]], lag_ratio=0.4), run_time=3)
            vo.wait_until("c")
            self.play(Write(f0), FadeIn(fn[0]))
            vo.wait_until("d")
            self.play(FadeIn(arrows[0]), Write(f1), FadeIn(fn[1]))
            vo.wait_until("e")
            self.play(FadeIn(arrows[1]), Write(f2), FadeIn(fn[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the rate, measured
    def loglog(self):
        c = load("path")["convergence"]
        rows = c["rows"]
        head = label(r"$1/\sqrt{N}$, \ measured", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 2.5, 0.5], y_range=[0, 2, 0.5], x_length=6.0, y_length=4.4, tips=False,
                  axis_config={"color": GREY_D, "include_ticks": False}).move_to([-3.1, -0.1, 0])
        xt = VGroup(*[label(f"{r['spp']}", font_size=17, color=GREY_B).next_to(
            ax.c2p(math.log10(r["spp"]), 0), DOWN, buff=0.1) for r in rows])
        yt = VGroup(*[label(t, font_size=17, color=GREY_B).next_to(ax.c2p(0, v + 2), LEFT, buff=0.1)
                      for v, t in ((-2, "0.01"), (-1.5, "0.03"), (-1, "0.1"), (-0.5, "0.3"), (0, "1"))])
        xl = label(r"paths per pixel \ (log scale)", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"RMS error against the reference \ (log scale)", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)

        def series(key, col):
            pts = [ax.c2p(math.log10(r["spp"]), math.log10(r[key]) + 2) for r in rows]
            return VGroup(VMobject(color=col, stroke_width=3).set_points_as_corners(pts),
                          *[Dot(q, radius=0.07, color=col) for q in pts])
        surf = series("rmse_surfaces", YES)
        allp = series("rmse", GREY_B)
        r1 = rows[0]["rmse_surfaces"]
        ideal = DashedLine(ax.c2p(0, math.log10(r1) + 2), ax.c2p(2.5, math.log10(r1) + 0.75), color=HEAD,
                           stroke_width=2)
        tags = VGroup(label(r"surfaces", font_size=17, color=YES).next_to(surf[-1], RIGHT, buff=0.12),
                      label(r"all pixels", font_size=17, color=GREY_B).next_to(allp[-1], UP, buff=0.12),
                      label(r"slope $-\tfrac12$", font_size=17, color=HEAD).next_to(ideal.get_end(), DOWN,
                                                                                     buff=0.12).shift(LEFT * 0.5))
        ref_noise = r1 / math.sqrt(2048)
        last = rows[-1]
        notes = VGroup(
            wrapped_label(rf"fitted slopes: \ {c['slope_surfaces']:.2f} on surfaces, \ {c['slope']:.2f} over all "
                          r"pixels, \ against Monte Carlo's $-\tfrac12$", 5.0, font_size=19, color=YES),
            wrapped_label(rf"the reference has 2048 paths, \ so its own error is about "
                          rf"{r1:.3f}$/\sqrt{{2048}}$ = {ref_noise:.4f}: \ it lifts the last point "
                          rf"\ ({last['rmse_surfaces']:.4f})", 5.0, font_size=19, color=WHITE),
            wrapped_label(rf"time grows with the paths: \ {secs(rows[0]['seconds'])} to "
                          rf"{secs(last['seconds'])}; \ every halving of the error costs four times the time",
                          5.0, font_size=19, color=HEAD),
            wrapped_label(r"so every other idea in this chapter attacks the constant $\sigma$, \ not the rate",
                          5.0, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).set_y(-0.1)
        with self.voiceover(
            "Now the whole image, against a reference of two thousand and forty-eight paths per pixel. <bookmark "
            "mark='a'/> On logarithmic axes the error falls on a line. <bookmark mark='b'/> Its slope is minus "
            "nought point four six, close to Monte Carlo's minus one half. <bookmark mark='c'/> The last point sits "
            "a little high, because the reference is noisy too. <bookmark mark='d'/> Time grows with the paths, so "
            "each halving of the error costs four times the time. <bookmark mark='e'/> The rate is fixed; the rest "
            "of this chapter attacks the constant, sigma."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(surf), Create(allp), FadeIn(tags[:2]), run_time=2)
            vo.wait_until("b")
            self.play(Create(ideal), FadeIn(tags[2]), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), Indicate(surf[-1], color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ sampling strategies, measured
    def strategies(self):
        rows = load("sampling")["rows"]
        head = label(r"Four ways to sample, \ measured", font_size=36).to_edge(UP, buff=0.3)
        names = {"cosine + NEE": r"cosine $+$ NEE", "uniform + NEE": r"uniform $+$ NEE",
                 "cosine, no NEE": r"cosine, \ no NEE", "uniform, no NEE": r"uniform, \ no NEE"}
        cols = [YES, DATA, KERN, NO]
        tab = grid_table([r"strategy", r"error", r"time", r"efficiency"],
                         [[names[r["name"]], f"{r['rmse_surfaces']:.3f}", secs(r["seconds"]),
                           f"{r['efficiency']:.2f}"] for r in rows],
                         widths=[2.8, 1.3, 1.3, 1.5], row_h=0.5, font_size=20, mono_cols=(),
                         colors=[[c, WHITE, WHITE, c] for c in cols])
        tcap = label(r"our path tracer, \ 16 paths per pixel, \ error on surfaces", font_size=17, color=GREY_A)
        VGroup(tcap, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-3.0, 1.1, 0])
        eff = [r["efficiency"] for r in rows]
        bars = VGroup()
        bw, gap, H = 0.7, 0.45, 2.6
        for k, (v, c) in enumerate(zip(eff, cols)):
            b = Rectangle(width=bw, height=H * v / max(eff), stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([2.4 + k * (bw + gap), -0.9 + b.height / 2, 0])
            bars.add(VGroup(b, label(f"{v:.2f}", font_size=17, color=c).next_to(b, UP, buff=0.06)))
        base = Line([2.4 - 0.5, -0.9, 0], [2.4 + 3 * (bw + gap) + 0.5, -0.9, 0], color=GREY_C, stroke_width=1.5)
        bnames = VGroup(*[label(t, font_size=16, color=GREY_A).next_to([2.4 + k * (bw + gap), -0.9, 0], DOWN,
                                                                       buff=0.1)
                          for k, t in enumerate((r"cos, NEE", r"unif., NEE", r"cos", r"unif."))])
        bcap = wrapped_label(r"efficiency $= 1/(\text{error}^2 \times \text{time})$, \ relative: \ the inverse of the "
                             r"work for a given error", 4.6, font_size=17, color=GREY_A).next_to(
            VGroup(base, bars), UP, buff=0.25).align_to(base, LEFT)
        nee_gain = eff[0] / eff[2]
        cos_gain = eff[0] / eff[1]
        cos_gain2 = eff[2] / eff[3]
        notes = VGroup(
            wrapped_label(rf"aiming at the light \ (NEE): \ {nee_gain:.1f} times the efficiency", 6.0,
                          font_size=19, color=YES),
            wrapped_label(rf"sampling the cosine: \ {cos_gain:.2f} times with NEE, \ {cos_gain2:.2f} times "
                          r"without", 6.0, font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.0, -2.0, 0])
        with self.voiceover(
            "Our instrument renders the same image four ways, at sixteen paths per pixel, and scores each by its "
            "efficiency: one over the error squared times the time. <bookmark mark='a'/> Cosine sampling with "
            "next-event estimation is our default. <bookmark mark='b'/> Uniform hemisphere sampling is about seventy"
            " per cent as efficient. <bookmark mark='c'/> Without next-event estimation the small light is found "
            "only by chance, and efficiency collapses to about a ninth. <bookmark mark='d'/> Aiming at the light is "
            "worth nine times the work; sampling the cosine, about one and a half."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tcap), FadeIn(tab.cells[0][0]), FadeIn(VGroup(*tab.cells[0][1:])),
                      FadeIn(tab.rule), Create(base), FadeIn(bcap))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                anims = [FadeIn(VGroup(*tab.cells[k + 1])), GrowFromEdge(bars[k][0], DOWN), FadeIn(bars[k][1]),
                         FadeIn(bnames[k])]
                if k == 2:
                    anims += [FadeIn(VGroup(*tab.cells[4])), GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1]),
                              FadeIn(bnames[3])]
                self.play(*anims)
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Russian roulette, measured
    def roulette(self):
        r = load("roulette")
        head = label(r"Russian roulette, \ tested", font_size=36).to_edge(UP, buff=0.3)
        lo, hi = 0.2435, 0.2505
        nl = NumberLine(x_range=[lo, hi, 0.001], length=6.2, color=GREY_C, include_ticks=True,
                        include_numbers=False).move_to([-3.2, 0.6, 0])
        ticks = VGroup(*[label(f"{v:.3f}", font_size=16, color=GREY_B).next_to(nl.n2p(v), DOWN, buff=0.12)
                         for v in (0.244, 0.246, 0.248, 0.250)])
        nlab = label(r"mean brightness of the image, \ 12 renders each", font_size=17, color=GREY_A).next_to(
            nl, UP, buff=1.25)

        def interval(m, se, col, dy, text):
            y = nl.n2p(m)[1] + dy
            bar = Line([nl.n2p(m - 2 * se)[0], y, 0], [nl.n2p(m + 2 * se)[0], y, 0], color=col, stroke_width=5)
            caps = VGroup(*[Line([nl.n2p(v)[0], y - 0.1, 0], [nl.n2p(v)[0], y + 0.1, 0], color=col,
                                 stroke_width=3) for v in (m - 2 * se, m + 2 * se)])
            dot = Dot([nl.n2p(m)[0], y, 0], radius=0.08, color=col)
            t = label(text, font_size=17, color=col).next_to(bar, UP if dy > 0 else DOWN, buff=0.1)
            return VGroup(bar, caps, dot, t)
        a = interval(r["mean_rr"], r["se_rr"], YES, 0.45, rf"with roulette: \ {r['mean_rr']:.4f} $\pm$ "
                                                          rf"{r['se_rr']:.4f}")
        b = interval(r["mean_no_rr"], r["se_no_rr"], DATA, -0.95, rf"without: \ {r['mean_no_rr']:.4f} $\pm$ "
                                                                  rf"{r['se_no_rr']:.4f}")
        bnote = note(r"bars: \ $\pm$ two standard errors", font_size=16).next_to(nl, DOWN, buff=1.45).align_to(
            nl, LEFT)

        def pair(v1, v2, title, fmt, x):
            m = max(v1, v2)
            H = 2.2
            g = VGroup()
            for k, (v, c) in enumerate(((v1, YES), (v2, DATA))):
                bb = Rectangle(width=0.6, height=H * v / m, stroke_width=0, fill_color=c, fill_opacity=0.85)
                bb.move_to([x + k * 0.95, -1.6 + bb.height / 2, 0])
                g.add(bb, label(fmt(v), font_size=17, color=c).next_to(bb, UP, buff=0.06))
            base = Line([x - 0.5, -1.6, 0], [x + 1.45, -1.6, 0], color=GREY_C, stroke_width=1.5)
            t = wrapped_label(title, 2.2, font_size=17, color=GREY_A).next_to(base, DOWN, buff=0.15)
            return VGroup(base, g, t)
        p1 = pair(r["path_length_rr"], r["path_length_no_rr"], r"rays per path", lambda v: f"{v:.2f}", 2.0)
        p2 = pair(r["seconds_rr"], r["seconds_no_rr"], r"seconds for 12 renders", lambda v: f"{v:.2f}", 4.8)
        leg = VGroup(label(r"with roulette", font_size=17, color=YES), label(r"without", font_size=17,
                                                                              color=DATA)).arrange(
            RIGHT, buff=0.4).move_to([3.9, 1.6, 0])
        notes = VGroup(
            wrapped_label(rf"difference of the means: \ $z = {r['z']:.2f}$; \ per pixel, \ the RMS $z$-score is "
                          rf"{r['pixel_z_rms']:.2f} \ (noise alone gives about 1)", 6.3, font_size=19, color=YES),
            wrapped_label(rf"{100 * r['saved']:.0f}\% fewer rays; \ both capped at 32 bounces; \ 64 $\times$ 64 "
                          r"at 16 paths per pixel", 6.3, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3).set_x(-3.2)
        with self.voiceover(
            "The last chapter proved Russian roulette unbiased; now we test it. <bookmark mark='a'/> Twelve renders "
            "with roulette and twelve without, both capped at thirty-two bounces. <bookmark mark='b'/> The mean "
            "brightness agrees to within one standard error. <bookmark mark='c'/> Pixel by pixel, the differences "
            "are the size that noise alone would make: their root mean square z-score is one point nought four. "
            "<bookmark mark='d'/> And roulette ends paths early: three point one six rays per path instead of nearly"
            " seven, fifty-five per cent fewer, in about half the time."
        ) as vo:
            self.play(FadeIn(head), Create(nl), FadeIn(ticks), FadeIn(nlab))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b), FadeIn(bnote))
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Indicate(notes[0], color=HEAD, scale_factor=1.03))
            vo.wait_until("d")
            self.play(FadeIn(leg), FadeIn(p1), FadeIn(p2), FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ MIS, measured
    def mis(self):
        rows = load("mis")["rows"]
        head = label(r"Multiple importance sampling, \ measured", font_size=36).to_edge(UP, buff=0.3)
        ns = sorted({r["n"] for r in rows})
        rs = sorted({r["r"] for r in rows})
        cw, chh = 1.9, 1.35
        x0, y0 = -4.0, 1.25
        cells = VGroup()
        strat = (("light", HEAD), ("brdf", DATA), ("power", YES))
        for i, n in enumerate(ns):
            for j, rad in enumerate(rs):
                r = next(x for x in rows if x["n"] == n and x["r"] == rad)
                c = np.array([x0 + j * cw, y0 - i * chh, 0])
                fr = Rectangle(width=cw - 0.1, height=chh - 0.1, stroke_color=GREY_D, stroke_width=1.2).move_to(c)
                g = VGroup(fr)
                for k, (s, col) in enumerate(strat):
                    v = r[f"rel_rmse_{s}"]
                    h = max(0.04, (math.log10(v) + 3) / 4 * (chh - 0.3))
                    b = Rectangle(width=0.32, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9)
                    b.move_to(c + np.array([(k - 1) * 0.45, -(chh - 0.3) / 2 + h / 2 - 0.02, 0]))
                    g.add(b)
                cells.add(g)
        clab = VGroup(*[label(rf"{r_['cone_half_angle_deg']:.1f}$^\circ$", font_size=17, color=HEAD).next_to(
            [x0 + j * cw, y0 + chh / 2, 0], UP, buff=0.08) for j, r_ in
            enumerate(next(x for x in rows if x["n"] == ns[0] and x["r"] == rad) for rad in rs)])
        rlab = VGroup(*[label(rf"{next(x for x in rows if x['n'] == n)['lobe_width_deg']:.1f}$^\circ$",
                              font_size=17, color=DATA).next_to([x0 - cw / 2, y0 - i * chh, 0], LEFT, buff=0.1)
                        for i, n in enumerate(ns)])
        ctitle = label(r"light's angular radius $\rightarrow$", font_size=17, color=HEAD).next_to(clab, UP,
                                                                                                  buff=0.08)
        rtitle = label(r"lobe width $\downarrow$", font_size=17, color=DATA).next_to(rlab, UP, buff=0.25).shift(
            LEFT * 0.1)
        leg = VGroup(label(r"light sampling", font_size=17, color=HEAD), label(r"BRDF sampling", font_size=17,
                                                                                color=DATA),
                     label(r"MIS, \ power heuristic", font_size=17, color=YES)).arrange(RIGHT, buff=0.35)
        scale = note(r"bar height: \ relative error, \ log scale from 0.001 to 10", font_size=16)
        VGroup(leg, scale).arrange(DOWN, buff=0.08).next_to(cells, DOWN, buff=0.2)
        worst = {s: max(r[f"rel_rmse_{s}"] for r in rows) for s in ("light", "brdf", "balance", "power")}
        tab = grid_table([r"strategy", r"worst relative error"],
                         [[r"light sampling", f"{worst['light']:.2f}"], [r"BRDF sampling", f"{worst['brdf']:.2f}"],
                          [r"MIS, \ balance", f"{worst['balance']:.3f}"], [r"MIS, \ power", f"{worst['power']:.3f}"]],
                         widths=[2.3, 2.3], row_h=0.42, font_size=19, mono_cols=(),
                         colors=[[HEAD, HEAD], [DATA, DATA], [YES, YES], [YES, YES]])
        setup = wrapped_label(r"one glossy point \ (normalized Phong) \ under a round light; \ 32 samples, \ "
                              r"4000 trials per cell; \ MIS takes half from each strategy", 4.6, font_size=18,
                              color=GREY_A)
        verdict = wrapped_label(r"MIS is never the single best, \ and never a disaster", 4.6,
                                font_size=19, color=YES)
        VGroup(setup, tab, verdict).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35).set_y(
            -0.1)
        with self.voiceover(
            "Our box is all matte, so we test multiple importance sampling where it matters: one glossy point under "
            "a round light, thirty-two samples, four thousand times over. <bookmark mark='a'/> Down the grid the "
            "glossy lobe narrows; to the right the light grows. <bookmark mark='b'/> Light sampling wins at the top "
            "left, wrong by under a fifth of one per cent, but is wrong by ninety-three per cent at the bottom "
            "right. <bookmark mark='c'/> BRDF sampling is the reverse: wrong by four hundred and sixty per cent with"
            " the tiniest light. <bookmark mark='d'/> The power heuristic is never the single best, but its worst "
            "case is eight per cent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(setup), *[FadeIn(c[0]) for c in cells])
            vo.wait_until("a")
            self.play(FadeIn(clab), FadeIn(rlab), FadeIn(ctitle), FadeIn(rtitle), FadeIn(leg), FadeIn(scale))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(c[1], DOWN) for c in cells])
            vo.wait_until("c")
            self.play(*[GrowFromEdge(c[2], DOWN) for c in cells])
            vo.wait_until("d")
            self.play(*[GrowFromEdge(c[3], DOWN) for c in cells])
            self.play(FadeIn(tab), FadeIn(verdict))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the a-trous filter
    def atrous(self):
        head = label(r"Denoising: \ borrow from the neighbours", font_size=36).to_edge(UP, buff=0.3)
        n, s = 17, 0.24
        C = np.array([-4.2, -0.15, 0])
        grid = VGroup(*[Square(side_length=s, stroke_color=GREY_D, stroke_width=0.8).move_to(
            C + np.array([(i - n // 2) * s, (j - n // 2) * s, 0])) for i in range(n) for j in range(n)])
        centre = Square(side_length=s, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(C)

        def taps(step, col):
            g = VGroup()
            for a in range(5):
                for b in range(5):
                    if a == 2 and b == 2:
                        continue
                    w = B3[a] * B3[b] / (B3[2] * B3[2])
                    g.add(Square(side_length=s, stroke_width=0, fill_color=col, fill_opacity=0.25 + 0.7 * w)
                          .move_to(C + np.array([(a - 2) * step * s, (b - 2) * step * s, 0])))
            return g
        t1, t2, t3 = taps(1, HEAD), taps(2, YES), taps(4, DATA)
        caps = [label(rf"pass {k + 1}: \ taps {2 ** k} pixel{'s' if k else ''} apart", font_size=19, color=col)
                .next_to(grid, DOWN, buff=0.2) for k, col in enumerate((HEAD, YES, DATA))]
        reach = label(r"three passes: \ 75 taps reach a 17 $\times$ 17 square", font_size=19, color=WHITE).next_to(
            grid, DOWN, buff=0.2)
        r0 = MathTex(r"h", r"=", r"\left(\tfrac{1}{16},\ \tfrac14,\ \tfrac38,\ \tfrac14,\ \tfrac1{16}\right)",
                     font_size=30)
        r1 = MathTex(r"c_{i+1}(p)", r"=", r"\frac{\sum_q h(q)\,w(p,q)\,c_i(q)}{\sum_q h(q)\,w(p,q)}",
                     font_size=30)
        r2 = MathTex(r"w", r"=", r"e^{-\frac{\lVert c_p-c_q\rVert^2}{\sigma_c^2}}\,"
                     r"e^{-\frac{\lVert n_p-n_q\rVert^2}{\sigma_n^2}}\,"
                     r"e^{-\frac{\lVert a_p-a_q\rVert^2}{\sigma_a^2}}\,"
                     r"e^{-\frac{\lVert x_p-x_q\rVert^2}{\sigma_x^2}}", font_size=30)
        r3 = MathTex(r"\text{image}", r"\ \div\ \text{albedo}", r"\ \to\ \text{filter}\ \to\ ",
                     r"\times\ \text{albedo}", font_size=30, color=YES)
        pairs = [(r0, r"a smooth $5 \times 5$ kernel \ (the B3 spline)"),
                 (r1, r"pass $i$: \ taps $2^i$ pixels apart, \ with holes \ (\`a trous)"),
                 (r2, r"edge-stopping: \ colour, \ and the normal, \ albedo and position of the first hit"),
                 (r3, r"demodulate: \ blur the light, \ not the walls' colours")]
        rows = VGroup(*[r for r, _ in pairs])
        notes = VGroup(*[note(t, font_size=17) for _, t in pairs])
        blk = VGroup(*[VGroup(r, nn).arrange(DOWN, aligned_edge=LEFT, buff=0.07) for r, nn in zip(rows, notes)])
        blk.arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(RIGHT, buff=0.35).set_y(-0.15)
        with self.voiceover(
            "The other way to fight noise is to borrow from the neighbours, with the edge-avoiding à-trous filter of"
            " Holger Dammertz and colleagues, from 2010. <bookmark mark='a'/> A pass blends each pixel with "
            "twenty-five neighbours under a small, smooth kernel. <bookmark mark='b'/> Each pass spreads the taps "
            "twice as far apart, with holes between them: à trous. <bookmark mark='c'/> Three passes cover a "
            "seventeen-pixel square with seventy-five taps. <bookmark mark='d'/> To keep edges, each tap is also "
            "weighted by how alike the two pixels are, in colour, normal, albedo and position. <bookmark mark='e'/> "
            "And only the light is blurred: divide by the albedo, filter, and multiply it back, so the walls' "
            "colours stay sharp."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(centre))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(caps[0]), Write(r0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(ReplacementTransform(t1, t2), ReplacementTransform(caps[0], caps[1]), Write(r1),
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(ReplacementTransform(t2, t3), ReplacementTransform(caps[1], caps[2]))
            self.play(ReplacementTransform(caps[2], reach))
            vo.wait_until("d")
            self.play(Write(r2), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(Write(r3), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ what the filter does
    def denoised(self):
        d = load("denoise")
        p = load("path")
        c16 = next(r for r in p["convergence"]["rows"] if r["spp"] == d["spp"])
        head = label(r"What the filter does, \ and does not", font_size=36).to_edge(UP, buff=0.3)
        srcs = ((d["noisy"], rf"{d['spp']} paths", NO), (d["denoised"], r"denoised", YES),
                (p["reference"], r"reference", GREY_A))
        rowA = Group(*[image(crop(a), height=2.35) for a, _, _ in srcs]).arrange(RIGHT, buff=0.25)
        rowB = Group(*[image(crop(a, CEIL), height=1.2) for a, _, _ in srcs]).arrange(RIGHT, buff=0.25)
        tl = VGroup(*[label(t, font_size=19, color=c) for _, t, c in srcs])
        Group(rowA, rowB).arrange(DOWN, buff=0.55).move_to([-2.45, -0.35, 0])
        for t, im in zip(tl, rowA):
            t.next_to(im, UP, buff=0.1)
        la = note(r"the balls", font_size=17).rotate(PI / 2).next_to(rowA, LEFT, buff=0.12)
        lb = note(r"the ceiling", font_size=17).rotate(PI / 2).next_to(rowB, LEFT, buff=0.12)
        ratio = d["rmse_surfaces_before"] / d["rmse_surfaces_after"]
        notes = VGroup(
            wrapped_label(rf"surfaces: \ error {d['rmse_surfaces_before']:.3f} $\rightarrow$ "
                          rf"{d['rmse_surfaces_after']:.3f}, \ {ratio:.1f} times smaller; \ edges and shadows "
                          r"kept", 3.9, font_size=19, color=YES),
            wrapped_label(r"the ceiling, \ lit only indirectly: \ speckle turns into blotches, \ low-frequency "
                          r"error a filter cannot tell from light", 3.9, font_size=19, color=KERN),
            wrapped_label(rf"all pixels: \ {d['rmse_before']:.3f} $\rightarrow$ {d['rmse_after']:.3f}; \ the "
                          r"noise on the light's own edge is left alone", 3.9, font_size=19, color=WHITE),
            wrapped_label(rf"filter {secs(d['filter_seconds'])}, \ render {secs(c16['seconds'])}; \ biased: \ "
                          r"it trades noise for blur", 3.9, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).set_y(-0.2)
        with self.voiceover(
            "Here is the filter on sixteen paths per pixel. <bookmark mark='a'/> Around the balls the speckle is "
            "gone, while the edges and soft shadows survive: the error on the surfaces is four times smaller. "
            "<bookmark mark='b'/> On the ceiling, lit only indirectly, the noise turns into blotches, error at low "
            "frequencies that no filter can tell from real light. <bookmark mark='c'/> Over all pixels the error "
            "falls much less, because the noise on the light's own edge is left alone. <bookmark mark='d'/> The "
            "filter costs a third of a second, less than the render. But it is biased: it trades noise for blur."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tl), FadeIn(rowA[0]), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(rowA[1:]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(rowB), FadeIn(lb), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
