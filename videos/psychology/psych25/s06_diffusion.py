from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Diffusion(VoiceoverScene):
    def construct(self):
        self.card()
        self.anatomy()
        self.derive()
        self.densities()

    def card(self):
        card = chapter_card(5, r"The diffusion model", r"What happens in half a second of deciding?",
                            lit={1978: r"Ratcliff", 2008: r"Ratcliff \& McKoon", 2009: r"Navarro \& Fuss"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter five. The diffusion model."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def anatomy(self):
        d = load("ddm")
        head = heading(r"Four numbers")
        a, z = d["a"], d["a"] * d["w"]
        A = axes([0, 1.4], [-0.9, 2.1], x_length=7.4, y_length=4.8, xticks=[0, 0.5, 1.0], yticks=[],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"decision time, \ s", center=[-2.6, -0.2, 0], font_size=16)
        top = Line(A.ax.c2p(0, a), A.ax.c2p(1.4, a), color=BOUND, stroke_width=3)
        bot = Line(A.ax.c2p(0, 0), A.ax.c2p(1.4, 0), color=BOUND, stroke_width=3)
        tl = label(r"``word''", font_size=20, color=BOUND).next_to(top, RIGHT, buff=0.1)
        bl = label(r"``not a word''", font_size=20, color=BOUND).next_to(bot, RIGHT, buff=0.1)
        brace = BraceBetweenPoints(A.ax.c2p(1.42, 0), A.ax.c2p(1.42, a), RIGHT, color=BOUND)
        bt = label(r"$a$, \ caution", font_size=20, color=BOUND).next_to(brace, RIGHT, buff=0.08)
        zd = Dot(A.ax.c2p(0, z), radius=0.08, color=WHITE)
        zt = label(r"$z$, \ start", font_size=18, color=WHITE).next_to(zd, UR, buff=0.06)
        ds = A.ax.c2p(0.0, z)
        de = A.ax.c2p(0.35, z + d["v"] * 0.35)
        darr = Arrow(ds, de, buff=0, color=DRIFT, stroke_width=5, max_tip_length_to_length_ratio=0.15)
        dt_ = label(r"$v$, \ drift", font_size=20, color=DRIFT).next_to(darr.get_end(), UP, buff=0.05)
        paths = VGroup()
        for p, n in zip(d["paths"], d["path_len"]):
            p = p[:n]
            t = np.arange(n) * d["dt"]
            keep = t <= 1.4
            paths.add(VMobject(color=EVIDENCE, stroke_width=1.6, stroke_opacity=0.7).set_points_as_corners(
                [A.ax.c2p(float(tt), float(v)) for tt, v in zip(t[keep], p[keep])]))
        sc = 0.55 / max(d["up"].max(), d["lo"].max())
        tt = d["t"][d["t"] <= 1.4]
        up = VMobject(color=MODEL, stroke_width=3).set_points_smoothly(
            [A.ax.c2p(float(x), a + sc * float(y)) for x, y in zip(tt, d["up"][: len(tt)])])
        lo = VMobject(color=LOST, stroke_width=3).set_points_smoothly(
            [A.ax.c2p(float(x), -sc * float(y)) for x, y in zip(tt, d["lo"][: len(tt)])])
        t0b = VGroup(Rectangle(width=1.2, height=0.3, stroke_width=0, fill_color=TIME, fill_opacity=0.7),
                     label(r"$t_0$: \ seeing and pressing", font_size=17, color=TIME)).arrange(RIGHT, buff=0.12)
        t0b.next_to(A, DOWN, buff=0.35).align_to(A, LEFT)
        rows = rows_of([
            (r"evidence starts at $z$ and drifts at rate $v$, \ jostled by noise", EVIDENCE),
            (r"the first bound it touches is the answer; \ when, \ the decision time", BOUND),
            (r"the response time adds $t_0$: \ seeing the stimulus and moving the finger", TIME),
            (r"where the paths end, \ stacked up: \ the two distributions of response times, \ right and wrong",
             MODEL),
        ], 4.0, 21, 0.34).move_to([4.9, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.simulate}; \ $v = 1.5$, \ $a = 1.2$, \ $z = a/2$")
        with self.voiceover(
            "The diffusion model has four main numbers. <bookmark mark='a'/> Evidence starts at a point z, between "
            "two bounds. Every instant it moves a little in the direction the stimulus favours, at a rate v, the "
            "drift, and is jostled by noise. Here are twelve trials. <bookmark mark='b'/> The first bound a path "
            "touches is the answer, and when it touches is the decision time. The distance between the bounds, a, "
            "is how much evidence the person demands: their caution. <bookmark mark='c'/> A response also takes "
            "time that isn't deciding: seeing the letters, and moving the finger. That's t zero. "
            "<bookmark mark='d'/> Now stack up where thousands of paths end. Above the top bound, the distribution "
            "of correct response times, and below the bottom one, the errors. Both skewed, like the real ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(top), FadeIn(bot), FadeIn(tl), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(zd), FadeIn(zt), GrowArrow(darr), FadeIn(dt_), FadeIn(rows[0]))
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.15), run_time=4)
            vo.wait_until("b")
            self.play(GrowFromCenter(brace), FadeIn(bt), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(t0b), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(up), Create(lo), FadeIn(rows[3]), run_time=2)
        self.clear_scene()

    def derive(self):
        d = load("ddm")
        head = heading(r"Derivation: \ accuracy and mean time in closed form")
        eqs = VGroup(
            MathTex(r"\tfrac{s^2}{2}\,P''(x) + v\,P'(x) = 0, \qquad P(0) = 0,\; P(a) = 1", font_size=32,
                    color=WHITE),
            MathTex(r"P(\text{upper}) = \frac{1 - e^{-2vz/s^2}}{1 - e^{-2va/s^2}}", font_size=40, color=MODEL),
            MathTex(r"\mathbb{E}[x_T] = z + v\,\mathbb{E}[T] \;\;\Rightarrow\;\; "
                    r"\mathbb{E}[T] = \frac{a\,P(\text{upper}) - z}{v}", font_size=34, color=EVIDENCE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([-2.9, 0.7, 0])
        check = VGroup(
            label(rf"$P(\text{{upper}})$: \ formula {d['p_upper']:.3f}, \ 40{{,}}000 simulated trials "
                  rf"{d['sim_p_upper']:.3f}", font_size=22, color=MODEL),
            label(rf"$\mathbb{{E}}[T]$: \ formula {d['mean_dt']:.3f} s, \ simulated {d['sim_mean_dt']:.3f} s "
                  r"\ (steps of half a millisecond overshoot a little)", font_size=22, color=EVIDENCE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=1.0).align_to(eqs, LEFT)
        assert abs(d["p_upper"] - d["sim_p_upper"]) < 0.01 and 0 < d["sim_mean_dt"] - d["mean_dt"] < 0.02
        rows = rows_of([
            (r"$P(x)$: \ the chance of reaching the top first, \ starting from $x$", WHITE),
            (r"a step of noise is as likely up as down, \ so $P$ must average out over a small step: \ that is the "
             r"equation", GREY_A),
            (r"the gambler's ruin, \ made continuous: \ with $v = 0$ it is just $z/a$", MODEL),
            (r"Wald's identity: \ on average the evidence ends where it started plus drift times time", EVIDENCE),
        ], 4.6, 22, 0.34).move_to([4.5, 0.6, 0])
        tag = psyche_tag(r"\texttt{decide.p\_upper}, \ \texttt{mean\_dt}, \ \texttt{simulate}")
        with self.voiceover(
            "Two of the model's predictions have exact formulas, and they're worth deriving. "
            "<bookmark mark='a'/> Let P of x be the chance of reaching the top bound first, starting from x. In a "
            "tiny step the evidence moves by the drift plus a bit of noise, as likely up as down, and P at x must "
            "equal the average of P over where that step could land. Expand that average, and you get this "
            "equation, with P zero at the bottom and one at the top. <bookmark mark='b'/> Its solution is an "
            "exponential, and it gives the probability of the upper answer. It's the gambler's ruin, made "
            "continuous. With no drift at all it's simply z over a. <bookmark mark='c'/> For the mean time, Wald "
            "found an identity: on average, where the evidence ends equals where it started plus the drift times "
            "the time it took. Where it ends is a or zero, with known chances, so the mean decision time follows. "
            "<bookmark mark='d'/> Psyche checks both against forty thousand simulated trials. The probabilities "
            "agree to three places; the simulated time runs a hundredth of a second long, because steps of "
            "half a millisecond overshoot the bound a little."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(check))
        self.clear_scene()

    def densities(self):
        d = load("ddm")
        head = heading(r"The distributions, \ computed")
        A = axes([0, 1.6], [0, 3.2], x_length=6.6, y_length=4.0, xticks=[0, 0.4, 0.8, 1.2, 1.6], yticks=[0, 1, 2, 3],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"decision time, \ s",
                 ylabel=r"density", center=[-3.0, -0.2, 0], font_size=16)
        mids = (d["edges"][:-1] + d["edges"][1:]) / 2
        w = float(np.diff(d["edges"])[0]) * 0.9
        keep = mids <= 1.6
        hu = bars(A.ax, mids[keep], d["h_up"][keep], MODEL, width=w, opacity=0.35)
        hl = bars(A.ax, mids[keep], d["h_lo"][keep], LOST, width=w, opacity=0.35)
        cu = curve_in(A.ax, d["t"], d["up"], MODEL, 3)
        cl = curve_in(A.ax, d["t"], d["lo"], LOST, 3)
        key = legend([(MODEL, r"correct \ (upper bound)"), (LOST, r"error \ (lower bound)")], font_size=17
                     ).move_to(A.ax.c2p(1.15, 2.7))
        assert d["up"].max() < 3.2 and abs(d["cond_up"] - d["cond_lo"]) < 1e-6
        rows = rows_of([
            (r"Navarro \& Fuss, \ 2009: \ the density of the first passage, \ as two series that converge fast, "
             r"\ one for short times and one for long", WHITE),
            (r"curves: \ Psyche's series; \ bars: \ 40{,}000 simulated trials", MODEL),
            (rf"the error curve is the correct one, \ shrunk: \ with the start halfway, \ both have the same mean, "
             rf"\ {d['cond_up']:.3f} s", LOST),
            (r"in data, \ errors are often faster or slower than correct answers: \ chapter seven", BOUND),
        ], 5.4, 22, 0.34).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.fpt\_density}; \ Navarro \& Fuss (2009)")
        with self.voiceover(
            "The whole distributions have no simple formula, but they can be computed exactly. "
            "<bookmark mark='a'/> Daniel Navarro and Ian Fuss gave the density of the first passage as two infinite "
            "series, one that converges fast for short times and one for long times, so a handful of terms will do. "
            "<bookmark mark='b'/> Psyche's curves land on the simulated trials. <bookmark mark='c'/> Notice something "
            "odd. The error distribution is just the correct one, scaled down. With the start halfway between the "
            "bounds, errors and correct answers take exactly the same time on average. <bookmark mark='d'/> Real "
            "errors are often faster than correct answers, or slower. That's the puzzle of chapter seven. First, "
            "fit the model to people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hu), FadeIn(hl), Create(cu), Create(cl), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
