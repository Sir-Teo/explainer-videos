from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Limits(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Models of limits", r"Can a limited mind be modelled as precisely as a perfect one?",
             "Chapter thirteen. Models of limits.",
             lit={2003: r"Sims", 2014: r"Gabaix", 2020: r"Bordalo, Gennaioli, Ma and Shleifer"},
             scale=("person", "nation"), horizon=("a month", "a year"))
        self.attention()
        self.sparsity()
        self.forecasts()

    def attention(self):
        R = load("ri")
        x = np.array(R["x"])
        ax = plane([-1, 1], [0, 1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[-1, -0.5, 0, 0.5, 1], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"how much better the new product really is", ylabel=r"chance of choosing it",
                   xfmt=lambda v: f"{v:+.1f}" if v else "0", yfmt=lambda v: f"{v:.2f}", font_size=14)
        cols = {"0.02": GAIN, "0.1": SOPH, "0.3": GYM, "1.0": LOSS}
        lines = VGroup(*[path(ax, x, R["curves"][k], cols[k], 3.0, smooth=False) for k in ("0.02", "0.1", "0.3",
                                                                                           "1.0")])
        eq = MathTex(r"P(a \mid x) = \frac{P(a)\, e^{u(a, x)/\lambda}}{\sum_b P(b)\, e^{u(b, x)/\lambda}}",
                     font_size=32, color=THEORY)
        side = VGroup(
            eq,
            label(r"$\lambda$: \ the cost of a unit \\ of information", font_size=18, color=WHITE),
            label(r"green, \ teal, \ gold, \ red: \\ $\lambda$ = 0.02, \ 0.1, \ 0.3, \ 1", font_size=18,
                  color=GREY_A),
            label(r"dear attention: \\ choices barely respond \\ to what is at stake", font_size=18, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.3)
        tag = published_tag(tables.LIMITS_45.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "A critic might say behavioural economics is a list of exceptions. Its most ambitious work tries to "
            "model limited minds as precisely as Part five modelled perfect ones. <bookmark mark='a'/> Christopher "
            "Sims proposed rational inattention: information is free to look at but costly to absorb, so people "
            "choose how much to learn, paying lambda for each unit of information. Filip Matejka and Alisdair "
            "McKay showed that the resulting choices follow a logit, tilted toward options that are often good. "
            "<bookmark mark='b'/> On the Island a shopper chooses between a familiar product and a new one whose "
            "value is uncertain. When attention is cheap, the shopper chooses the new product almost exactly when "
            "it is better. <bookmark mark='c'/> As attention gets dearer, the curve flattens: choices barely "
            "respond to what is at stake. <bookmark mark='d'/> And when the new product is usually worse, a shopper "
            "facing dear attention can rationally never look at it at all. Inattention, on this view, is a choice."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(eq), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), Create(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Indicate(lines[0], color=WHITE))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(ln) for ln in lines[1:]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def sparsity(self):
        R = load("ri")
        w = R["sparse"]
        names = (r"price", r"quality", r"running costs", r"resale value", r"warranty terms")
        imp = (4.0, 1.5, 1.0, 0.5, 0.2)
        bars = VGroup()
        for i, (nm, v, m) in enumerate(zip(names, imp, w)):
            y = 1.6 - 0.75 * i
            r0 = Rectangle(width=3.0, height=0.45, stroke_color=GREY_B, stroke_width=1.2, fill_opacity=0).move_to(
                np.array([1.0, y, 0]))
            r1 = Rectangle(width=max(3.0 * m, 0.001), height=0.45, stroke_width=0, fill_color=SOPH,
                           fill_opacity=0.85).align_to(r0, LEFT).set_y(y)
            bars.add(VGroup(label(nm, font_size=19, color=WHITE).next_to(r0, LEFT, buff=0.3),
                            label(rf"importance {v}", font_size=15, color=GREY_A).next_to(r0, LEFT, buff=2.3), r0, r1,
                            label(f"{m:.2f}", font_size=17, color=SOPH).next_to(r0, RIGHT, buff=0.2)))
        eq = MathTex(r"m_i = \max\!\left(0,\; 1 - \frac{\kappa}{v_i}\right)", font_size=36,
                     color=THEORY).to_edge(UP, buff=0.5)
        foot = label(r"small things get exactly no attention: \ a sparse model of the world", font_size=21,
                     color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.LIMITS_45.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Xavier Gabaix proposed a related idea: sparsity. <bookmark mark='a'/> A decision maker starts from a "
            "simple default model of the world and pays attention to each feature only in proportion to how much it "
            "matters, minus a fixed cost kappa. <bookmark mark='b'/> Attention to a feature is one minus kappa over "
            "its importance, but never below zero. <bookmark mark='c'/> A car buyer weighs the price almost fully, "
            "quality somewhat, running costs less, and resale value and warranty terms not at all. "
            "<bookmark mark='d'/> The result is a model with exact zeros, like the lasso of Statistics, Built: small "
            "things are ignored completely, which is what left-digit bias and shrouded fees look like from the "
            "inside."
        ) as vo:
            self.play(FadeIn(tag), *[FadeIn(b[0]) for b in bars], *[FadeIn(b[2]) for b in bars])
            vo.wait_until("a")
            self.play(*[FadeIn(b[1]) for b in bars])
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[3], LEFT), FadeIn(b[4])) for b in bars],
                                  lag_ratio=0.3), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def forecasts(self):
        F = load("forecast")
        r, d = F["rational"], F["diagnostic"]
        eq = MathTex(r"x_{t+h} - F_t x_{t+h} = a + b\,\big(F_t x_{t+h} - F_{t-1} x_{t+h}\big) + e",
                     font_size=32, color=THEORY).to_edge(UP, buff=0.5)
        sub = label(r"forecast error \ on \ forecast revision \ (Coibion and Gorodnichenko)", font_size=18,
                    color=GREY_A).next_to(eq, DOWN, buff=0.2)
        tbl = VGroup()
        hdr = VGroup(label(r"forecasters", font_size=19, color=GREY_A), label(r"each person's $b$", font_size=19,
                                                                              color=GREY_A),
                     label(r"the average forecast's $b$", font_size=19, color=GREY_A))
        tbl.add(hdr)
        for nm, R_, col in ((r"rational, \ noisy information", r, TC),
                            (rf"diagnostic \ ($\theta$ = {F['theta']})", d, NAIF)):
            tbl.add(VGroup(label(nm, font_size=20, color=col), label(f"{R_['individual']:+.2f}", font_size=22,
                                                                       color=WHITE),
                           label(f"{R_['consensus']:+.2f}", font_size=22, color=WHITE)))
        for row in tbl:
            for j, c in enumerate(row):
                c.move_to(np.array([-3.6 + 3.9 * j, 0, 0]))
        tbl.arrange(DOWN, buff=0.5).move_to(DOWN * 0.3)
        for row in tbl:
            for j, c in enumerate(row):
                c.set_x(-3.6 + 3.9 * j)
        notes = VGroup(
            label(r"$b > 0$: \ too little response to news \ (under-reaction)", font_size=19, color=PLAN),
            label(r"$b < 0$: \ too much \ (over-reaction)", font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.LIMITS_45.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Limits also shape expectations, the subject of Part twenty-eight. <bookmark mark='a'/> Olivier Coibion "
            "and Yuriy Gorodnichenko's test regresses the error in a forecast on the revision that produced it. "
            "If forecasters use their information well, revisions should not predict errors. "
            "<bookmark mark='a2'/> A positive slope means forecasts move too little when news arrives; "
            "<bookmark mark='a3'/> a negative slope, too much. "
            "<bookmark mark='b'/> On the Island, forty forecasters each see the economy through private noise. "
            f"When they are rational, each one's slope is {say_num(r['individual'], 2)}, about zero, but the "
            f"average forecast's slope is {r['consensus']:.2f}: the consensus under-reacts, because each person's "
            "news reaches the average only gradually. <bookmark mark='c'/> Now make them diagnostic, in the sense of "
            "Pedro Bordalo, Nicola Gennaioli and Andrei Shleifer: news that makes a state more likely than before "
            "makes it seem much more likely. Each forecaster now over-reacts, with a slope of "
            f"{say_num(d['individual'], 2)}, while the average still under-reacts, at {d['consensus']:.2f}. "
            "<bookmark mark='d'/> That is the pattern Bordalo, Gennaioli, Yueran Ma and Shleifer found in "
            "professional forecasts: individuals over-react, the consensus under-reacts. One model, two facts."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), FadeIn(sub), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(tbl[0]))
            vo.wait_until("a2")
            self.play(FadeIn(notes[0], shift=UP * 0.1))
            vo.wait_until("a3")
            self.play(FadeIn(notes[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(tbl[1]))
            vo.wait_until("c")
            self.play(FadeIn(tbl[2]))
            vo.wait_until("d")
            self.play(Indicate(tbl[2][1], color=WHITE), Indicate(tbl[1][2], color=WHITE))
        self.clear_scene()
