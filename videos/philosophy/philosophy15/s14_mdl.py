from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403

DEG_C = {"0": GREY_B, "1": BLUEC, "2": OK, "8": BAD}


class MDL(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Compression and prediction", r"Is learning the same as compressing?",
                            lit=(1978,), part=PART)
        with self.voiceover("Chapter thirteen. Compression and prediction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.codes()
        self.fits()
        self.lengths()
        self.modern()

    def codes(self):
        head = label(r"A probability is a code length", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        eq = MathTex(r"\text{length}(x) = -\log_2 P(x) \ \text{ bits}", font_size=40, color=FUT).next_to(
            head, DOWN, buff=0.45)
        ex = stack([(r"Shannon \ (1948): \ no code beats this on average; \ arithmetic coding achieves it", WHITE),
                    (r"a fair coin: \ 1 bit per toss; \ \ a 9-in-10 coin, \ with the right model: \ 0.47 bits per toss",
                     GREY_A),
                    (r"so: \ a better predictor \textit{is} a better compressor, \ and conversely \ (\textit{AI, Built}, \ "
                     r"Part 1)", GOAL)],
                   font_size=23).next_to(eq, DOWN, buff=0.5)
        bits = VGroup(*[Square(side_length=0.3, stroke_width=1, stroke_color=GREY_C, fill_color=PAST,
                               fill_opacity=0.6) for _ in range(20)]).arrange(RIGHT, buff=0.05)
        bits2 = VGroup(*[Square(side_length=0.3, stroke_width=1, stroke_color=GREY_C, fill_color=FUT,
                                fill_opacity=0.6) for _ in range(9)]).arrange(RIGHT, buff=0.05)
        row = VGroup(VGroup(label(r"20 tosses, \ no model", font_size=19, color=GREY_B), bits).arrange(RIGHT,
                                                                                                    buff=0.3),
                     VGroup(label(r"20 tosses, \ a good model", font_size=19, color=GREY_B), bits2).arrange(
                         RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Behind Solomonoff's idea is a simple equation of Claude Shannon's. <bookmark mark='a'/>If you assign a "
            "probability to a message, you can encode it in minus log two of that probability bits, and on average "
            "no code does better. Arithmetic coding achieves the bound. <bookmark mark='b'/>A fair coin costs a bit "
            "per toss. A coin that lands heads nine times in ten, encoded with the right model, costs under half a bit "
            "per toss. "
            "<bookmark mark='c'/>So a better predictor is a better compressor, and a better compressor is a better "
            "predictor. Twenty such tosses take twenty bits without a model, and about nine with one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(ex[0]))
            vo.wait_until("b")
            self.play(FadeIn(ex[1]))
            vo.wait_until("c")
            self.play(FadeIn(ex[2]), FadeIn(row))
        self.clear_scene()

    def fits(self):
        d = load("mdl")
        head = label(r"Which curve? \ Thirty noisy points", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[-1, 5, 1], x_length=7.0, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-2.6, -0.6, 0])
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=WHITE) for x, y in zip(d["x"], d["y"])])
        curves = {}
        for k, col in DEG_C.items():
            ys = [min(max(v, -1), 5) for v in d["fits"][k]]
            curves[k] = series_plot(ax, ys, col, xs=d["xf"], width=3.5)
        leg = stack([(r"degree 0: \ a constant: \ misses the shape", GREY_B),
                     (r"degree 1: \ a line: \ misses the bend", BLUEC),
                     (r"degree 2: \ the truth's own degree", OK),
                     (r"degree 8: \ chases the noise", BAD)], font_size=21, aligned_edge=LEFT).move_to([3.7, 0.6, 0])
        q = label(r"more parameters always fit better: \ where to stop?", font_size=22, color=GOAL).move_to(
            [3.7, -1.6, 0])
        with self.voiceover(
            "Jorma Rissanen turned this into a method for choosing models, minimum description length, in 1978. "
            "<bookmark mark='a'/>Here are thirty noisy points from a quadratic. <bookmark mark='b'/>A constant misses "
            "the shape. <bookmark mark='c'/>A line misses the bend. <bookmark mark='d'/>A quadratic, the true "
            "degree, follows it. <bookmark mark='e'/>A degree eight polynomial fits even better, because it chases "
            "the noise. <bookmark mark='f'/>Adding parameters always improves the fit. Where should we stop?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.03))
            for mk, k, r in zip("bcde", ("0", "1", "2", "8"), leg):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(q))
        self.clear_scene()

    def lengths(self):
        d = load("mdl")
        rows = d["rows"]
        head = label(r"Two-part code: \ the model, \ then the data given the model", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        eq = MathTex(r"L(M) + L(D \mid M) \;=\; \tfrac{k+1}{2}\log_2 n \;+\; \tfrac{n}{2}\log_2\!\big(2\pi e\, "
                     r"\tfrac{\mathrm{RSS}}{n}\big) + n \log_2 \tfrac{1}{\delta}", font_size=30, color=FUT).next_to(
            head, DOWN, buff=0.25)
        ks = [r["degree"] for r in rows]
        top = Axes(x_range=[0, 8, 1], y_range=[200, 280, 20], x_length=7.4, y_length=2.7, tips=False,
                   axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16},
                   x_axis_config={"include_numbers": False}).move_to([-2.4, -0.35, 0])
        bot = Axes(x_range=[0, 8, 1], y_range=[0, 25, 10], x_length=7.4, y_length=1.1, tips=False,
                   axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-2.4, -2.8, 0])
        ax = VGroup(top, bot)
        xl = label(r"degree", font_size=18, color=GREY_B).next_to(bot.x_axis, DOWN, buff=0.3)
        yl = label(r"bits", font_size=18, color=GREY_B).next_to(top.y_axis, UP, buff=0.1)
        cm = series_plot(bot, [r["model_bits"] for r in rows], PAST, xs=ks)
        cd = series_plot(top, [r["data_bits"] for r in rows], BLUEC, xs=ks)
        ct = series_plot(top, [r["total"] for r in rows], OK, xs=ks, width=4)
        dots = VGroup(*[Dot(top.c2p(r["degree"], r["total"]), radius=0.06, color=OK) for r in rows])
        best = rows[d["best"]]
        star = Circle(radius=0.16, color=GOAL, stroke_width=3).move_to(top.c2p(best["degree"], best["total"]))
        raw = DashedLine(top.c2p(0, d["raw_bits"]), top.c2p(8, d["raw_bits"]), color=GREY_B, stroke_width=1.5)
        rl = label(r"no model: \ " + f"{d['raw_bits']:.0f}" + r" bits", font_size=17, color=GREY_B).next_to(
            raw, UP, buff=0.05).align_to(raw, RIGHT)
        assert all(200 <= r["data_bits"] <= 280 and 200 <= r["total"] <= 280 for r in rows)
        assert all(0 <= r["model_bits"] <= 25 for r in rows)
        leg = stack([(r"model: \ grows with every coefficient", PAST),
                     (r"data given model: \ falls, \ then flattens", BLUEC),
                     (r"total: \ smallest at degree " + str(d["best"]) + r", \ " + f"{best['total']:.0f}" +
                      r" bits", OK),
                     (r"the shortest total description is the model to believe", GOAL),
                     (r"data recorded to $\delta = " + str(d["precision"]) + r"$", GREY_B)], font_size=20,
                    aligned_edge=LEFT).move_to([4.2, -1.0, 0])
        with self.voiceover(
            "Rissanen's answer: describe the data in two parts. <bookmark mark='a'/>First the model, its "
            "coefficients, each costing about half log n bits. Then the data, encoded with the model's help: "
            "only the residuals need to be written down. <bookmark mark='b'/>Every coefficient makes the model "
            "part longer. <bookmark mark='c'/>The data part falls steeply, then flattens once the true shape is "
            "captured. <bookmark mark='d'/>The total is smallest at degree two, the true degree. "
            "<bookmark mark='e'/>Writing the numbers down with no model at all would take about two hundred and "
            "sixty-five bits. The best model saves forty-five of them, and that saving is what it has learned. The "
            "shortest total description is the model to believe."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(leg[4]))
            vo.wait_until("b")
            self.play(Create(cm), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(Create(cd), FadeIn(leg[1]))
            vo.wait_until("d")
            self.play(Create(ct), FadeIn(dots), FadeIn(leg[2]))
            self.play(Create(star))
            vo.wait_until("e")
            self.play(Create(raw), FadeIn(rl), FadeIn(leg[3]))
        self.clear_scene()

    def modern(self):
        head = label(r"Compression in modern learning", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"AIC, \ BIC", r"penalized fit: \ BIC $\approx$ two-part MDL; \ AIC aims at prediction \ (Akaike, \ "
                            r"1973)", PAST),
            (r"double descent", r"huge networks fit noise, \ yet generalize: \ parameter count is the wrong "
                                r"measure \ (Belkin et al., \ 2019)", BAD),
            (r"PAC-Bayes", r"bounds by how far training moved the weights from a prior \ (McAllester, \ 1999)",
             FUT),
            (r"language models", r"trained to predict the next token: \ to compress text", OK),
        ]
        g = VGroup()
        for i, (a, b, c) in enumerate(rows):
            x = label(a, font_size=23, color=c)
            y = label(b, font_size=20)
            if y.width > 9.4:
                y.width = 9.4
            x.move_to([-6.3 + x.width / 2, 1.5 - i * 0.95, 0])
            y.move_to([-3.4 + y.width / 2, 1.5 - i * 0.95, 0])
            g.add(VGroup(x, y))
        foot = label(r"in each case simplicity is \textit{measured}, \ and the measure is itself a bias", font_size=23,
                     color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Compression runs through modern learning. <bookmark mark='a'/>The Bayesian information criterion is, "
            "to first order, two-part MDL; Akaike's criterion aims instead at predictive accuracy. "
            "<bookmark mark='b'/>Deep learning complicated the story: huge networks can fit pure noise and yet "
            "generalize well on real data, the phenomenon of double descent. Counting parameters is the wrong "
            "measure of complexity. <bookmark mark='c'/>PAC-Bayes bounds measure instead how far training moved the "
            "weights from a prior. <bookmark mark='d'/>And a language model, trained to predict the next token, is "
            "trained to compress text. <bookmark mark='e'/>In each case simplicity has to be measured, and the "
            "choice of measure is itself an inductive bias."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
