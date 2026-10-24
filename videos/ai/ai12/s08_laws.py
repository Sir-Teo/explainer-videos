from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import DCOL, FIT, HIST, NCOL, PART, load, predict_card, takeaway_card, width_ramp


class Laws(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.method()
        self.predict()
        self.laws()
        self.takeaway()

    def card(self):
        card = chapter_card(7, r"Scaling laws, measured", r"How does the loss depend on size and data?", lit=(2020,),
                            part=PART)
        with self.voiceover("Chapter seven. Scaling laws, measured."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        # Hestness et al.'s three regions of a learning curve (schematic)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 6, 1], x_length=5.4, y_length=3.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.6, -0.6, 0])
        xs = np.linspace(0.2, 9.8, 200)
        ys = 1.0 + 4.0 / (1 + np.exp(1.1 * (xs - 4.8)))  # flat, then a straight fall, then the floor
        lc = curve(ax, xs, ys, FIT, 3.5, smooth=True)
        regs = VGroup(label(r"small data", font_size=20, color=GREY_B).move_to(ax.c2p(1.0, 5.4)),
                      label(r"power law", font_size=20, color=C.BITS).move_to(ax.c2p(6.4, 3.9)),
                      label(r"irreducible", font_size=20, color=GREY_B).move_to(ax.c2p(8.6, 1.9)))
        floor = DashedLine(ax.c2p(0, 1.0), ax.c2p(10, 1.0), color=GREY_D, stroke_width=1.5)
        xl = label(r"training set size \ (log)", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        yl = label(r"error \ (log)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        sch = note(r"schematic, \ after Hestness et al.\ (2017)").next_to(xl, DOWN, buff=0.12)
        h1 = history_card(2017, r"Hestness et al.\ (Baidu Research)",
                          r"translation, language models, images, speech: \ error falls as a power law in the data, "
                          r"exponents $-0.07$ (words) to $-0.35$; \ a better model moves the curve, \ not its slope",
                          width=6.0, color=HIST)
        h2 = history_card(2020, r"Kaplan, McCandlish et al.\ (OpenAI)",
                          r"loss against parameters, data and compute: \ exponents $0.076$, $0.095$, $0.050$ over "
                          r"seven "
                          r"orders of magnitude; \ an $8\times$ larger model needs only $5\times$ the data", width=6.0,
                          color=HIST)
        cards = VGroup(h1, h2).arrange(DOWN, buff=0.3).move_to([3.4, -0.3, 0])
        link = note(r"the story, \ and GPT-3: \ Part 14").next_to(cards, DOWN, buff=0.2)
        with self.voiceover(
            "In 2017, Joel Hestness and colleagues at Baidu measured how the error of networks for translation, "
            "language, images and speech falls as the data grows. <bookmark mark='a'/> Each curve had three parts: "
            "too little data to learn anything; then a straight line on log axes, a power law; then a floor that "
            "more data cannot pass. <bookmark mark='b'/> Better architectures moved the line down, but they barely "
            "changed its slope: for language models, about minus 0.07. <bookmark mark='c'/> In 2020, Jared Kaplan, "
            "Sam McCandlish and colleagues at OpenAI found the same for parameters, data and compute together, over "
            "seven orders of magnitude, and concluded that a model eight times bigger needs only five times the "
            "data. Part fourteen told how that led to GPT-3. Here we measure such laws ourselves."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(sch), FadeIn(h1, shift=LEFT * 0.1))
            vo.wait_until("a")
            self.play(Create(lc), Create(floor), run_time=2.0)
            self.play(LaggedStart(*[FadeIn(r_) for r_ in regs], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(h2, shift=LEFT * 0.1), FadeIn(link))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def method(self):
        s = load("sweep")
        widths = [int(w) for w in s["widths"]]
        ks = [int(k) for k in s["ks"]]
        Lb = np.asarray(s["bits"], float)
        w = 128 if 128 in widths else widths[len(widths) // 2]
        i = widths.index(w)
        c = np.asarray(s[f"curve{w}"])
        B = int(s["batch"])
        hours = float(s["secs"]) / 3600
        n_runs = int(np.isfinite(Lb).sum())
        # top: the learning rate; bottom: the held-out loss of one width, trunk and cooled endpoints
        lsteps = np.log2(np.maximum(c[:, 0], 1))
        sx0, sx1 = 6.0, max(lsteps.max(), ks[-1] - math.log2(B)) + 0.3
        top = Axes(x_range=[sx0, sx1, 1], y_range=[0, 1.15, 0.5], x_length=8.2, y_length=1.5, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-1.6, 2.0, 0])
        tl = label(r"learning rate", font_size=20, color=GREY_A).next_to(top, LEFT, buff=0.15)
        trunk_lr = Line(top.c2p(sx0, 1.0), top.c2p(sx1, 1.0), color=WHITE, stroke_width=3)
        branches = VGroup()
        for k in ks:
            S = 2 ** k / B
            if math.log2(S) > sx1 or math.log2(S) < sx0 + 0.3:
                continue
            a = math.log2(0.8 * S)
            xs = np.linspace(a, math.log2(S), 20)
            ys = 1 - (2 ** xs - 0.8 * S) / (0.2 * S)
            branches.add(curve(top, xs, ys, C.BITS, 2.5))
        lo = float(np.nanmin(Lb[i]) - 0.08)
        hi = float(min(np.nanmax(c[:, 1]), np.nanmin(Lb[i]) + 1.3))
        bot = CornerAxes(x_range=[sx0, sx1, 1], y_range=[lo, hi, (hi - lo) / 4], x_length=8.2, y_length=3.2, tips=False,
                         axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.6, -1.25, 0])
        xt = VGroup(*[MathTex(rf"2^{{{k}}}", font_size=20, color=GREY_B).next_to(bot.c2p(k - math.log2(B), lo), DOWN, buff=0.08)
                      for k in ks if sx0 <= k - math.log2(B) <= sx1])
        xn = label(r"characters of training \ (log)", font_size=20, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yn = label(rf"held-out bits, \ width ${w}$", font_size=20, color=GREY_A).next_to(bot, LEFT, buff=0.15).rotate(PI / 2)
        sel = (lsteps >= sx0) & (c[:, 1] <= hi)
        trunk = curve(bot, lsteps[sel], c[sel, 1], WHITE, 3)
        ends = VGroup()
        for j, k in enumerate(ks):
            if np.isfinite(Lb[i, j]) and sx0 <= k - math.log2(B) <= sx1:
                ends.add(Dot(bot.c2p(k - math.log2(B), Lb[i, j]), radius=0.08, color=C.BITS))
        side = VGroup(label(r"one run per width at a constant rate,", font_size=22, color=WHITE),
                      label(r"and at each length a short branch", font_size=22, color=C.BITS),
                      label(r"that cools the rate to zero:", font_size=22, color=C.BITS),
                      label(r"a full schedule's result \\ for a fifth of the cost", font_size=22, color=GREY_A))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.95, 0.6, 0])
        tally = label(rf"${len(widths)}$ widths, \ ${n_runs}$ endpoints, \\ ${hours:.1f}$ CPU-hours", font_size=24,
                      color=C.BITS).next_to(side, DOWN, buff=0.4).align_to(side, LEFT)
        cite_ = cite(r"A.~H\"agele et al., \textit{Scaling Laws and Compute-Optimal Training Beyond Fixed Training "
                     r"Durations} (2024)", corner=DR)
        with self.voiceover(
            "A scaling law needs many runs, each trained to the end of its own schedule. That is expensive: a run "
            "planned for a million characters and stopped halfway is not a good half-million-character run, because "
            "its learning rate never came down. <bookmark mark='a'/> So we use a trick from 2024. Train each width "
            "once at a constant rate, <bookmark mark='b'/> and at every length we want, branch off and cool the "
            "rate to zero over the last fifth. <bookmark mark='c'/> Each branch lands where a full schedule of "
            "that length would, and the trunk carries on. <bookmark mark='d'/> "
            f"{len(widths)} widths, from {widths[0]} to {widths[-1]:,} units, lengths from two to the sixteen to two "
            f"to the twenty-four characters: {n_runs} finished runs in {hours:.1f} hours of one processor."
        ) as vo:
            self.play(Create(top), FadeIn(tl), Create(bot), FadeIn(xt), FadeIn(xn), FadeIn(yn), FadeIn(cite_))
            self.play(Create(trunk_lr), Create(trunk), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b_) for b_ in branches], lag_ratio=0.15), FadeIn(side[1:3]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in ends], lag_ratio=0.15), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(tally))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laws(self):
        s, ch = load("sweep"), load("chinchilla")
        LN, LD = ch["LN_fit"], ch["LD_fit"]
        Nn, Ln = np.asarray(ch["LN_N"], float), np.asarray(ch["LN_L"], float)
        Dd, Ld = np.asarray(ch["LD_D"], float), np.asarray(ch["LD_L"], float)
        wD = int(ch["LD_w"])
        pans = VGroup()
        for k, (x, y, fit, col, xname, sym) in enumerate(((Nn, Ln, LN, NCOL, r"parameters $N$", "N"),
                                                         (Dd, Ld, LD, DCOL, r"characters of training $D$", "D"))):
            lx = np.log10(x)
            x0, x1 = math.floor(lx.min() * 2) / 2 - 0.1, math.ceil(lx.max() * 2) / 2 + 0.1
            y0 = math.floor((min(y.min(), fit["E"]) - 0.05) * 10) / 10
            y1 = math.ceil((y.max() + 0.05) * 10) / 10
            ax = CornerAxes(x_range=[x0, x1, 1], y_range=[y0, y1, (y1 - y0) / 4], x_length=5.4, y_length=3.6, tips=False,
                            axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04})
            ax.move_to([-3.45 + 6.9 * k, -0.7, 0])
            xt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(v, y0), DOWN, buff=0.08)
                          for v in range(math.ceil(x0), math.floor(x1) + 1)])
            yt = VGroup(*[MathTex(f"{v:.1f}", font_size=20, color=GREY_B).next_to(ax.c2p(x0, v), LEFT, buff=0.08)
                          for v in np.arange(math.ceil(y0 * 5) / 5, y1 + 1e-9, 0.2)])
            xn = label(xname, font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.1)
            dts = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=col) for a, b in zip(lx, y)])
            xs = np.linspace(lx.min(), lx.max(), 120)
            fc = curve(ax, xs, fit["E"] + fit["A"] * (10 ** xs) ** -fit["a"], FIT, 3, smooth=True)
            fl = DashedLine(ax.c2p(x0, fit["E"]), ax.c2p(x1, fit["E"]), color=GREY_B, stroke_width=1.5)
            f = MathTex(rf"L = {fit['E']:.2f} + \frac{{{fit['A']:.3g}}}{{{sym}^{{{fit['a']:.2f}}}}}", font_size=30, color=col)
            f.next_to(ax.c2p(x1, y1), DL, buff=0.15)
            pans.add(VGroup(ax, xt, yt, xn, dts, fc, fl, f))
        t1 = label(r"every width, \ trained on $2^{24}$ characters", font_size=22, color=NCOL).next_to(pans[0], UP, buff=0.15)
        t2 = label(rf"width ${wD}$, \ every length", font_size=22, color=DCOL).next_to(pans[1], UP, buff=0.15)
        hd = label(r"held-out bits per character", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        # seed-to-seed spread, from the repeated widths
        spread = []
        ks = [int(k) for k in s["ks"]]
        for w, sd in [tuple(x) for x in np.asarray(s["extra"]).tolist()]:
            i = [int(v) for v in s["widths"]].index(int(w))
            base = np.asarray(s["bits"], float)[i]
            other = np.asarray(s[f"seed{int(sd)}_w{int(w)}"], float)
            ok = np.isfinite(base) & np.isfinite(other)
            spread.append(float(np.abs(base[ok] - other[ok]).max()))
        sp = max(spread)
        noise = note(rf"three seeds at widths $64$ and $256$: \ at most ${sp:.3f}$ bits apart").to_corner(DL, buff=0.2)
        aN, aD = float(LN["a"]), float(LD["a"])
        said1 = (
            "Our exponents are much larger than Kaplan's: our models see only eight characters at a time, so "
            "there is less to learn, and they learn it fast. A different task, a different exponent: what carries "
            "over is the shape." if min(aN, aD) > 0.15 else
            "Our exponents are close to Kaplan's, though the task is different: what carries over is the shape."
        )
        with self.voiceover(
            "First, one variable at a time, as Kaplan did. Hold the data large, two to the twenty-four characters, "
            "and vary the size. <bookmark mark='a'/> The loss falls toward a floor along a power law: "
            f"L equals {LN['E']:.2f} plus a constant over N to the {aN:.2f}. <bookmark mark='b'/> Hold the "
            f"size large, width {wD}, and vary the data: the exponent is {aD:.2f}. <bookmark mark='c'/> "
            f"Different seeds land at most {sp:.3f} bits apart, small next to these curves. "
            + said1
        ) as vo:
            self.play(FadeIn(hd), *[FadeIn(p[:4]) for p in pans], FadeIn(t1), FadeIn(t2))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in pans[0][4]], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(Create(pans[0][5]), Create(pans[0][6]), Write(pans[0][7]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in pans[1][4]], lag_ratio=0.1))
            self.play(Create(pans[1][5]), Create(pans[1][6]), Write(pans[1][7]))
            vo.wait_until("c")
            self.play(FadeIn(noise))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def predict(self):
        pc = predict_card(r"Our models are tiny and read only $8$ characters at a time. \ Will their loss fall "
                          r"faster or slower with size than Kaplan's language models?")
        with self.voiceover(
            "Pause and predict. Our models are tiny, and read only eight characters at a time. Will their loss fall "
            "faster or slower with size than in Kaplan's language models?"
        ):
            self.play(FadeIn(pc, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(pc))

    def takeaway(self):
        tk = takeaway_card(r"A power law plus a floor",
                           r"$L(N) = E + A/N^{\alpha}$ \ and \ $L(D) = E + B/D^{\beta}$: \ the exponents depend on "
                           r"the task, \ the shape carries over.",
                           r"next: \ size and data at once, \ and how to split a budget")
        with self.voiceover(
            "The takeaway: loss falls toward a floor along a power law, in size and in data, and the shape carries "
            "over from task to task even when the exponents do not. Next, both at once, and how to split a budget "
            "between them."
        ) as vo:
            self.play(FadeIn(tk[0], shift=UP * 0.2))
            self.wait(max(0.0, vo.duration * 0.5 - 1.0))
            self.play(FadeIn(tk[1]))
        self.wait(0.4)
        self.play(FadeOut(tk))
