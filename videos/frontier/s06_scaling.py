from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Plot, bar_rows, calc, label, load, note, part_card, pipeline_map, pow10_label, source

BUDGET_COLORS = [YELLOW_A, YELLOW_C, GOLD_C, GOLD_E]
# Chinchilla's parametric loss L = E + A/N^alpha + B/D^beta, as re-estimated by Besiroglu et al. (Epoch AI, 2024,
# arXiv 2404.10102, Table 1). Hoffmann et al.'s published values (E 1.69, A 406.4, B 410.7, alpha 0.34, beta 0.28)
# imply ~70 tokens per parameter, inconsistent with their own Approaches 1-2 and with how Chinchilla was trained.
CHINCHILLA = dict(E=1.8172, A=482.01, B=2085.43, alpha=0.3478, beta=0.3658)


def isoflop_fits(rows, k: int = 5):
    """Per budget: a parabola in log10(N) through the k runs around the lowest loss (the valley floor; far-off
    runs would skew it); its vertex is the compute-optimal size."""
    budgets = sorted({r["budget"] for r in rows})
    fits = []
    for C in budgets:
        rs = sorted([r for r in rows if r["budget"] == C], key=lambda r: r["params"])
        i = int(np.argmin([r["val"] for r in rs]))
        assert 0 < i < len(rs) - 1, f"budget {C:g}: the best size is at the edge of the sweep"
        lo = max(0, min(i - k // 2, len(rs) - k))
        near = rs[lo:lo + k]
        x = np.log10([r["params"] for r in near])
        y = np.array([r["val"] for r in near])
        a, b, c = np.polyfit(x, y, 2)
        xv = -b / (2 * a)
        fits.append(dict(C=C, rows=rs, near=near, coef=(a, b, c), n_opt=10**xv, l_opt=a * xv**2 + b * xv + c,
                         flops=np.mean([r["flops"] for r in rs])))
    slope, icpt = np.polyfit(np.log10([f["C"] for f in fits]), np.log10([f["n_opt"] for f in fits]), 1)
    return fits, slope, icpt


class ScalingLaws(VoiceoverScene):
    def construct(self):
        self.opening()
        self.rectangle()
        self.six_nd()
        self.isoflop()
        self.chinchilla()
        self.optimal_split()
        self.overtraining()

    # ------------------------------------------------------------------
    def opening(self):
        card = part_card(2, r"The recipe", r"how big, what shape, how to optimize").to_edge(UP, buff=1.0)
        m = pipeline_map(width=13.0, highlight="pretrain").to_edge(DOWN, buff=0.7)
        with self.voiceover("Part two: the recipe."):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(m), run_time=1.2)
        self.wait(0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rectangle(self):
        area = 6.0
        w = ValueTracker(4.0)

        def rect():
            ww = w.get_value()
            r = Rectangle(width=ww, height=area / ww, stroke_color=C.COMPUTE, stroke_width=3, fill_color=C.COMPUTE,
                          fill_opacity=0.25)
            r.move_to(LEFT * 2.6 + DOWN * 0.4)
            return r
        R = always_redraw(rect)
        nl = always_redraw(lambda: label(r"$N$ parameters", font_size=28, color=C.PARAMS).next_to(R, DOWN, buff=0.15))
        dl = always_redraw(lambda: label(r"$D$ tokens", font_size=28, color=C.DATA).rotate(PI / 2).next_to(R, LEFT, buff=0.15))
        cl = always_redraw(lambda: MathTex(r"C", font_size=44, color=C.COMPUTE).move_to(R))
        formula = MathTex(r"C \approx 6\,N D", font_size=56).move_to(RIGHT * 3.6 + UP * 1.6)
        formula[0][0].set_color(C.COMPUTE)
        formula[0][3].set_color(C.PARAMS)
        formula[0][4].set_color(C.DATA)
        why = VGroup(
            label(r"each parameter, for each token:", font_size=26, color=GREY_A),
            label(r"forward: a multiply and an add (2)", font_size=26),
            label(r"backward: about twice that (4)", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(formula, DOWN, buff=0.4)
        q = label(r"fixed budget $C$: big model on few tokens,\\or small model on many?", font_size=28, color=C.COMPUTE)
        q.next_to(why, DOWN, buff=0.5)
        with self.voiceover(
            "Before training anything, a lab has to decide how big the model should be. The budget is compute, and "
            "there's a simple rule for it: training costs about six times the number of parameters, times the number "
            "of tokens. <bookmark mark='w'/> Two operations per parameter per token on the forward pass, a multiply "
            "and an add, and about four more on the backward pass. <bookmark mark='q'/> So a fixed budget is a fixed "
            "area: you can spend it on a big model trained on fewer tokens, <bookmark mark='s'/> or a small model "
            "trained on many. Which is better?"
        ) as vo:
            self.play(FadeIn(R), FadeIn(nl), FadeIn(dl), FadeIn(cl), FadeIn(formula))
            vo.wait_until("w")
            self.play(FadeIn(why))
            vo.wait_until("q")
            self.play(FadeIn(q), w.animate.set_value(5.5), run_time=1.5)
            vo.wait_until("s")
            self.play(w.animate.set_value(1.4), run_time=2.0)
            self.play(w.animate.set_value(3.0), run_time=1.0)
        for m in (R, nl, dl, cl):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def six_nd(self):
        rows = {r["model"]: r for r in load("epoch")["rows"]}
        N, D = 405e9, 15.6e12
        flops = 6 * N * D
        epoch = rows["Llama 3.1-405B"]["flop"]
        assert round(flops / 1e25, 1) == 3.8 and epoch == 3.8e25
        head = label(r"The rule on a real model: Llama 3.1 405B", font_size=34).to_edge(UP, buff=0.45)
        per = calc(r"\text{per token: } 6N &= 6 \times 405\times10^{9}", r"\\ &= 2.43\times10^{12}\ \text{operations}",
                   font_size=36)
        total = calc(r"C \approx 6\,N\,D &= 2.43\times10^{12} \times 15.6\times10^{12}",
                     r"\\ &= 3.79\times10^{25}\ \text{operations}", font_size=36)
        VGroup(per, total).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(UP * 0.3)
        per[1].set_color(C.PARAMS)
        total[1].set_color(C.COMPUTE)
        tags = VGroup(label(r"$N$ = 405 billion parameters", font_size=26, color=C.PARAMS),
                      label(r"$D$ = 15.6 trillion training tokens", font_size=26, color=C.DATA)
                      ).arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=0.35)
        chk = label(rf"Epoch AI's independent estimate of this run: $3.8\times10^{{25}}$", font_size=30, color=C.COMPUTE)
        chk.next_to(total, DOWN, buff=0.6).set_x(0)
        box = SurroundingRectangle(total[1], buff=0.12, color=C.COMPUTE, stroke_width=2)
        src = source(r"Llama 3 paper (405B on 15.6T tokens); Epoch AI, \emph{Data on AI models}")
        with self.voiceover(
            "Check the rule on a real model. Llama 3.1's largest version has 405 billion parameters, so every "
            "token costs six times that: <bookmark mark='p'/> 2.4 trillion operations. <bookmark mark='d'/> It was "
            "trained on 15.6 trillion tokens. <bookmark mark='c'/> Multiply, and the whole run comes to 3.8 times "
            "ten to the twenty-five operations. <bookmark mark='e'/> Epoch AI's independent estimate of that run: the "
            "same, 3.8 times ten to the twenty-five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags[0]), FadeIn(src), Write(per[0]))
            vo.wait_until("p")
            self.play(Write(per[1]))
            vo.wait_until("d")
            self.play(FadeIn(tags[1]), Write(total[0]))
            vo.wait_until("c")
            self.play(Write(total[1]), Create(box))
            vo.wait_until("e")
            self.play(FadeIn(chk, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def isoflop(self):
        d = load("isoflop")
        rows = d["rows"]
        assert len(rows) == 25 and len({r["budget"] for r in rows}) == 4
        fits, slope, icpt = isoflop_fits(rows)
        assert 0.7 < slope < 0.82 and all(np.diff([f["n_opt"] for f in fits]) > 0)
        self.slope = slope
        self.fits = fits
        allN = [r["params"] for r in rows]
        allL = [r["val"] for r in rows]
        plot = Plot(x_range=(min(allN) / 1.8, max(allN) * 1.5), y_range=(min(allL) - 0.15, min(7.6, max(allL) + 0.1)),
                    width=7.4, height=4.8, log_x=True, x_ticks=[1e5, 1e6],
                    y_ticks=list(np.arange(np.ceil((min(allL) - 0.15) * 2) / 2, min(7.6, max(allL) + 0.1), 0.5)),
                    x_fmt=lambda v: pow10_label(int(round(np.log10(v)))), x_label=r"model size $N$ (parameters)",
                    y_label=r"final validation loss")
        plot.move_to(LEFT * 2.6 + DOWN * 0.35)
        groups = VGroup()
        curves = VGroup()
        stars = VGroup()
        for f, col in zip(fits, BUDGET_COLORS):
            pts = plot.dots([r["params"] for r in f["rows"]], [min(r["val"], plot.y_range[1]) for r in f["rows"]], col, radius=0.07)
            xs = np.linspace(np.log10(f["near"][0]["params"]) - 0.05, np.log10(f["near"][-1]["params"]) + 0.05, 60)
            a, b, c = f["coef"]
            ys = a * xs**2 + b * xs + c
            m = ys <= plot.y_range[1]
            cv = plot.line(10 ** xs[m], ys[m], color=col, stroke_width=2.5)
            st = Star(n=5, outer_radius=0.14, color=col, fill_opacity=1).move_to(plot.c2p(f["n_opt"], f["l_opt"]))
            groups.add(pts)
            curves.add(cv)
            stars.add(st)
        legend = VGroup(*[VGroup(Dot(radius=0.07, color=col), MathTex(rf"C = {f['C']:.0e}".replace("e+", r"\times10^{") + "}", font_size=24))
                          .arrange(RIGHT, buff=0.12) for f, col in zip(fits, BUDGET_COLORS)])
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(plot, RIGHT, buff=0.15).align_to(plot, UP)
        head = label(rf"Our IsoFLOP experiment: {len(rows)} real training runs", font_size=32).to_edge(UP, buff=0.3)
        head.set_x(-2.2)
        # right panel: N_opt vs C
        Cs = np.array([f["C"] for f in fits])
        Ns = np.array([f["n_opt"] for f in fits])
        p2 = Plot(x_range=(Cs.min() / 2, Cs.max() * 2), y_range=(1e4, 1e6), width=3.6, height=3.2,
                  log_x=True, log_y=True, x_ticks=[1e12, 1e13], y_ticks=[1e4, 1e5, 1e6],
                  x_fmt=lambda v: pow10_label(int(round(np.log10(v))), font_size=20),
                  y_fmt=lambda v: pow10_label(int(round(np.log10(v))), font_size=20),
                  x_label=r"compute $C$", y_label=r"best $N$", font_size=20)
        p2.move_to(RIGHT * 4.6 + DOWN * 1.5)
        pd = VGroup(*[Star(n=5, outer_radius=0.11, color=col, fill_opacity=1).move_to(p2.c2p(c, n))
                      for c, n, col in zip(Cs, Ns, BUDGET_COLORS)])
        xx = np.array([Cs.min() / 1.6, Cs.max() * 1.6])
        fl = p2.line(xx, 10 ** (icpt + slope * np.log10(xx)), color=C.PARAMS, stroke_width=3)
        sl = MathTex(rf"N_{{\rm opt}} \propto C^{{{slope:.2f}}}", font_size=30, color=C.PARAMS).next_to(p2, UP, buff=0.15)
        tpp = np.array([f["C"] / (6 * f["n_opt"]) / f["n_opt"] for f in fits])
        self.tpp = tpp
        with self.voiceover(
            "The way to find out is an experiment, so we ran one. Pick a compute budget, and train models of "
            "several sizes, each on exactly the number of tokens the budget allows. <bookmark mark='a'/> Plot final "
            "loss against model size, and you get a valley: too small a model can't hold what it sees, too large a "
            "model doesn't get to see enough. <bookmark mark='b'/> Repeat at four budgets, twenty-five runs in all, "
            "and fit a parabola to each valley floor. <bookmark mark='c'/> The best size grows with the budget, as a "
            "power law, with an exponent of about three quarters. That's close to what OpenAI found in 2020 with small "
            "models. The much larger study we'll see next found about one half, and later work traced the gap to "
            "details of how very small models like ours are measured and tuned."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot))
            vo.wait_until("a")
            self.play(FadeIn(groups[2], lag_ratio=0.2), FadeIn(legend[2]))
            self.play(Create(curves[2]), FadeIn(stars[2]))
            vo.wait_until("b")
            for k in (0, 1, 3):
                self.play(FadeIn(groups[k], lag_ratio=0.2), FadeIn(legend[k]), Create(curves[k]), FadeIn(stars[k]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(p2), FadeIn(pd), Create(fl), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chinchilla(self):
        E, A, B, al, be = (CHINCHILLA[k] for k in ("E", "A", "B", "alpha", "beta"))
        lN = np.linspace(7, 12, 260)
        lD = np.linspace(9, 14, 260)
        NN, DD = np.meshgrid(10**lN, 10**lD)
        L = E + A / NN**al + B / DD**be
        v = np.clip((L - E) / 1.6, 0, 1) ** 0.6
        rgb = np.stack([0.08 + 0.25 * (1 - v), 0.12 + 0.55 * (1 - v), 0.25 + 0.55 * (1 - v)], -1)
        img = ImageMobject((np.flipud(rgb) * 255).astype(np.uint8))
        W, H = 6.4, 5.0
        img.stretch_to_fit_width(W).stretch_to_fit_height(H).move_to(LEFT * 2.6 + DOWN * 0.4)

        def p(ln, ld):
            return img.get_corner(DL) + RIGHT * W * (ln - 7) / 5 + UP * H * (ld - 9) / 5
        iso = VGroup()
        for lc in (19, 21, 23, 25):
            # 6 N D = C  =>  log D = log(C/6) - log N
            ln0, ln1 = max(7, lc - np.log10(6) - 14), min(12, lc - np.log10(6) - 9)
            iso.add(Line(p(ln0, lc - np.log10(6) - ln0), p(ln1, lc - np.log10(6) - ln1), color=C.COMPUTE, stroke_width=2))
        # compute-optimal path: minimize L along each iso line
        opt = []
        for lc in np.linspace(18, 26, 30):
            ln = np.linspace(7, 12, 400)
            ld = lc - np.log10(6) - ln
            ok = (ld >= 9) & (ld <= 14)
            Ls = E + A / (10 ** ln[ok]) ** al + B / (10 ** ld[ok]) ** be
            if ok.sum():
                k = np.argmin(Ls)
                opt.append(p(ln[ok][k], ld[ok][k]))
        path = VMobject(stroke_color=WHITE, stroke_width=4).set_points_smoothly(opt)
        ax = VGroup(
            label(r"parameters $N$ ($10^7$ to $10^{12}$)", font_size=22, color=C.PARAMS).next_to(img, DOWN, buff=0.15),
            label(r"tokens $D$ ($10^9$ to $10^{14}$)", font_size=22, color=C.DATA).rotate(PI / 2).next_to(img, LEFT, buff=0.15),
        )
        formula = MathTex(r"L(N, D) = E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}", font_size=36).move_to(RIGHT * 3.7 + UP * 2.2)
        vals = MathTex(r"E{=}1.82,\ A{=}482,\ B{=}2085", r"\\ \alpha{=}0.348,\ \beta{=}0.366", font_size=26, color=GREY_A).next_to(formula, DOWN, buff=0.15)
        notes = VGroup(
            label(r"dark: lower loss", font_size=22, color=GREY_A),
            label(r"yellow: equal compute", font_size=22, color=C.COMPUTE),
            label(r"white: the best split", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(vals, DOWN, buff=0.35)
        res = VGroup(
            label(r"$\Rightarrow$ grow $N$ and $D$ together:", font_size=26),
            label(r"about 20 tokens per parameter", font_size=28, color=C.DATA),
            label(r"GPT-3: 175B params on 300B tokens (1.7)", font_size=22, color=GREY_A),
            label(r"Chinchilla 70B on 1.4T beat the 280B Gopher", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(notes, DOWN, buff=0.35)
        src = source(r"Hoffmann et al.\ (2022), Eq.\ 10, with the coefficients as re-estimated by Besiroglu et al.\ (Epoch AI, 2024)")
        study = VGroup(label(r"400+ training runs", font_size=34, color=C.COMPUTE),
                       label(r"70M to 16B parameters", font_size=28, color=C.PARAMS),
                       label(r"5B to 500B tokens", font_size=28, color=C.DATA)).arrange(DOWN, buff=0.25).move_to(img)
        with self.voiceover(
            "In 2022, DeepMind's Chinchilla paper did this with more than four hundred models, up to sixteen billion "
            "parameters, and fitted a formula for the loss as a function of model size and data. <bookmark mark='l'/> "
            "Here is the landscape it describes, with the coefficients as corrected by a 2024 replication; darker means "
            "lower loss. <bookmark mark='i'/> Each yellow line is a "
            "fixed compute budget. <bookmark mark='o'/> Along each one there's a best point, and together they trace "
            "this path: grow parameters and tokens together, about twenty tokens for every parameter. "
            "<bookmark mark='g'/> By that measure, GPT-3 had been trained on far too little data, and the 70-billion "
            "parameter Chinchilla, trained on 1.4 trillion tokens, beat a model four times its size."
        ) as vo:
            self.play(FadeIn(formula), FadeIn(vals), FadeIn(src), LaggedStart(*[FadeIn(x) for x in study], lag_ratio=0.4))
            vo.wait_until("l")
            self.play(FadeOut(study), FadeIn(img), FadeIn(ax), FadeIn(notes[0]))
            vo.wait_until("i")
            self.play(LaggedStart(*[Create(i) for i in iso], lag_ratio=0.2), FadeIn(notes[1]))
            vo.wait_until("o")
            self.play(Create(path), FadeIn(notes[2]), run_time=1.5)
            self.play(FadeIn(res[:2]))
            vo.wait_until("g")
            self.play(FadeIn(res[2:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def optimal_split(self):
        E, A, B, al, be = (CHINCHILLA[k] for k in ("E", "A", "B", "alpha", "beta"))
        a = be / (al + be)
        G = (al * A / (be * B)) ** (1 / (al + be))
        Cb = 5.76e23  # Chinchilla's (and Gopher's) training budget
        N = G * (Cb / 6) ** a
        D = Cb / (6 * N)
        assert round(a, 2) == 0.51 and round(G, 2) == 0.12 and round(N / 1e9) == 72 and round(D / 1e12, 2) == 1.33
        assert round(D / N) == 18
        head = label(r"How to split a budget, from the formula", font_size=34).to_edge(UP, buff=0.4)
        der = calc(r"L &= E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}, \qquad D = \frac{C}{6N}",
                   r"\\ L(N) &= E + A\,N^{-\alpha} + B\left(\frac{6N}{C}\right)^{\beta}",
                   r"\\ \frac{dL}{dN} &= -\alpha A\,N^{-\alpha-1} + \beta B\left(\frac{6}{C}\right)^{\beta} N^{\beta-1} = 0",
                   r"\\ \Rightarrow\; N_{\rm opt} &= G\left(\frac{C}{6}\right)^{\frac{\beta}{\alpha+\beta}},"
                   r"\quad G = \left(\frac{\alpha A}{\beta B}\right)^{\frac{1}{\alpha+\beta}}", font_size=29)
        der.to_edge(LEFT, buff=0.35).shift(UP * 0.4)
        num = calc(rf"\frac{{\beta}}{{\alpha+\beta}} &= \frac{{0.366}}{{0.714}} = {a:.3f},\quad G = {G:.3f}",
                   rf"\\ C &= 5.76\times10^{{23}}\ \text{{(Chinchilla's budget)}}",
                   rf"\\ N_{{\rm opt}} &= {G:.3f}\times(9.6\times10^{{22}})^{{{a:.3f}}} = {N / 1e10:.1f}\times10^{{10}}",
                   rf"\\ D_{{\rm opt}} &= \frac{{C}}{{6N_{{\rm opt}}}} = {D / 1e12:.2f}\times10^{{12}}",
                   rf"\\ \frac{{D_{{\rm opt}}}}{{N_{{\rm opt}}}} &\approx {D / N:.0f}\ \text{{tokens per parameter}}", font_size=29)
        num.to_edge(RIGHT, buff=0.35).align_to(der, UP)
        num[3:].set_color(C.DATA)
        real = label(r"DeepMind trained Chinchilla with\\70B parameters on 1.4T tokens", font_size=28, color=C.DATA)
        real.next_to(num, DOWN, buff=0.5)
        src = source(r"coefficients: Besiroglu et al.\ (Epoch AI, 2024), Table 1; budget: Hoffmann et al.\ (2022)")
        with self.voiceover(
            "The formula also tells you how to split any budget. Since C is six N D, the number of tokens is C over "
            "six N, so the loss becomes a function of the model size alone. <bookmark mark='d'/> Set its derivative "
            "to zero, and the best size turns out to be a power of the budget: C to the beta over alpha plus beta. "
            "<bookmark mark='n'/> With the corrected coefficients, that exponent is 0.51, so model size and data "
            "should grow at almost the same rate. <bookmark mark='c'/> Now plug in Chinchilla's own budget, 5.76 "
            "times ten to the twenty-three operations. <bookmark mark='r'/> The formula asks for 72 billion "
            "parameters and 1.3 trillion tokens, about eighteen tokens per parameter. <bookmark mark='k'/> DeepMind "
            "trained Chinchilla with 70 billion parameters on 1.4 trillion tokens."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Write(der[0]))
            self.play(Write(der[1]))
            vo.wait_until("d")
            self.play(Write(der[2]))
            self.play(Write(der[3]))
            vo.wait_until("n")
            self.play(Write(num[0]))
            vo.wait_until("c")
            self.play(Write(num[1]))
            vo.wait_until("r")
            self.play(Write(num[2]))
            self.play(Write(num[3]), Write(num[4]))
            vo.wait_until("k")
            self.play(FadeIn(real, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def overtraining(self):
        bars = [
            (r"Chinchilla rule", 20, C.DATA),
            (r"Llama 3.1 405B", 15.6e12 / 405e9, C.PARAMS),
            (r"DeepSeek-V3 (per active param.)", 14.8e12 / 37e9, C.PARAMS),
            (r"Qwen3-235B (per active param.)", 36e12 / 22e9, C.PARAMS),
            (r"Llama 3 8B", 15e12 / 8e9, C.PARAMS),
        ]
        assert round(bars[4][1]) == 1875
        rows = bar_rows([(name, np.log10(v), col, rf"{v:,.0f}".replace(",", "{,}")) for name, v, col in bars],
                        6.5 / np.log10(2500), font_size=26, bar_h=0.4, buff=0.25)
        rows.move_to(DOWN * 0.3)
        head = label(r"Training tokens per parameter (log scale)", font_size=34).to_edge(UP, buff=0.5)
        why = label(r"a smaller model trained longer is cheaper to serve to millions of people", font_size=26,
                    color=GREY_A).to_edge(DOWN, buff=0.6)
        src = source(r"Llama 3 paper and blog; DeepSeek-V3, Qwen3 reports")
        with self.voiceover(
            "But nobody actually stops at twenty. Llama 3's team used the same kind of IsoFLOP experiment, up to ten "
            "to the twenty-two operations, to choose the size of their 405-billion-parameter model, and then trained "
            "their small models far longer: the 8-billion-parameter Llama 3 saw fifteen trillion tokens, almost "
            "nineteen hundred per parameter, and it kept improving. <bookmark mark='w'/> The reason is cost after "
            "training: a smaller model trained for longer is much cheaper to run for millions of people. Frontier "
            "mixtures of experts land in between, at hundreds to over a thousand tokens per active parameter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                                  lag_ratio=0.3), run_time=3.0)
            vo.wait_until("w")
            self.play(FadeIn(why))
        self.wait(0.4)
        self.clear_scene()
