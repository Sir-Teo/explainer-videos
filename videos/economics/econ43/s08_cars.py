from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Cars(VoiceoverScene):
    def construct(self):
        card(self, 7, r"BLP on the Island, \ then on real cars", r"Does the estimator find the truth?",
             "Chapter seven. BLP on the Island, then on real cars.", lit={1995: r"Berry, \ Levinsohn and Pakes"},
             scale=("market",), horizon=("a year", "a decade"))
        self.monte()
        self.slope()
        self.real()
        self.dollars()

    def monte(self):
        C = load("cars")
        R = C["runs"]
        T = TRUTH["cars"]
        ax = plane([0.0, 1.0], [0, 3.6], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.6, y_length=4.4,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[], xlabel=r"estimated average price sensitivity, "
                   r"\ $\alpha$", xfmt=lambda v: f"{v:.1f}", font_size=14)
        rows = ((r"OLS logit", R["ols"], OLS_C, 3.0), (r"IV logit", R["iv"], IV_C, 1.9),
                (r"BLP", R["blp_alpha"], BLP_C, 0.8))
        strips = VGroup()
        rng = np.random.default_rng(1)
        for nm, vals, col, y in rows:
            g = VGroup(*[dot(ax, v, y + rng.uniform(-0.18, 0.18), col, 0.055) for v in vals])
            mean_ = float(np.mean(vals))
            strips.add(VGroup(label(nm, font_size=19, color=col).next_to(ax.ax.c2p(0.0, y), LEFT, buff=0.15), g,
                              label(rf"mean {mean_:.2f}", font_size=16, color=col).next_to(ax.ax.c2p(1.0, y),
                                                                                          RIGHT, buff=0.1)))
        truth = VGroup(vline(ax, T["alpha"], 0, 3.6, TRUTH_C, 2.6),
                       label(rf"the truth: \ {T['alpha']}", font_size=17, color=TRUTH_C).next_to(
                           ax.ax.c2p(T["alpha"], 3.6), UP, buff=0.08))
        head = label(rf"{T['runs']} simulated Islands, \ {T['T']} years of {T['firms'] * T['per_firm']} car models "
                     r"each", font_size=22, color=E.ACCENT).to_edge(UP, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Does the estimator find the truth? On the Island we know it, because we planted it. "
            f"<bookmark mark='a'/> Here are {T['runs']} simulated Islands, each with {T['T']} years of "
            f"{T['firms'] * T['per_firm']} car models, priced by six firms competing in the way of Part twelve, with "
            f"buyers whose price sensitivity averages {T['alpha']}. <bookmark mark='b'/> Plain logit by ordinary "
            f"least squares finds a sensitivity of about {C['mean']['ols']:.2f} every time: far too low, because the "
            "expensive cars are also the good ones. <bookmark mark='c'/> Instrumenting price, with an input price "
            f"and measures of how crowded each car's neighbourhood is, raises it to about {C['mean']['iv']:.2f}: "
            "better, but plain logit is the wrong model, so even good instruments cannot rescue it. "
            "<bookmark mark='d'/> The full random-coefficient estimator is centred on the truth, at "
            f"{C['mean']['blp_alpha']:.2f}, with a wider spread: the price of a richer model estimated from forty "
            "years of data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(tag), *[FadeIn(s_[0]) for s_ in strips], run_time=1.2)
            vo.wait_until("a")
            self.play(Create(truth[0]), FadeIn(truth[1]))
            for mk, s_ in zip("bcd", strips):
                vo.wait_until(mk)
                self.play(Indicate(s_[0], color=WHITE), LaggedStart(*[FadeIn(d) for d in s_[1]], lag_ratio=0.02),
                          FadeIn(s_[2]), run_time=1.5)
        self.clear_scene()

    def slope(self):
        C = load("cars")
        p = np.array(C["price"])
        ax = plane([3, 19], [-8, 0], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[4, 8, 12, 16], yticks=[-8, -6, -4, -2, 0], xlabel=r"price",
                   ylabel=r"own-price elasticity", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        tr = VGroup(*[dot(ax, x, y, TRUTH_C, 0.045) for x, y in zip(p, C["true_own"]) if y > -8])
        iv = VGroup(*[dot(ax, x, y, IV_C, 0.04) for x, y in zip(p, C["iv_own"]) if y > -8])
        side = VGroup(
            label(r"green: \ the truth, \\ one Island", font_size=18, color=TRUTH_C),
            label(r"purple: \ the IV logit; \\ elasticity proportional \\ to price", font_size=18, color=IV_C),
            label(rf"medians, \ 40 Islands: \\ truth {C['mean']['el_true']:.2f}, \\ OLS {C['mean']['el_ols']:.2f}, "
                  rf"\\ IV {C['mean']['el_iv']:.2f}, \ BLP {C['mean']['el_blp']:.2f}", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The difference shows in the elasticities. <bookmark mark='a'/> In green, each car's true own-price "
            "elasticity on one Island, against its price. Dearer cars face somewhat more elastic demand, but the "
            "buyers of dear cars are the less sensitive ones, so the rise is gentle. <bookmark mark='b'/> The plain "
            "logit, even with good instruments, makes the elasticity proportional to price: too low for cheap cars, "
            "too high for dear ones. <bookmark mark='c'/> Across the forty Islands the median elasticity is "
            f"{say_num(C['mean']['el_true'])}; ordinary least squares says {say_num(C['mean']['el_ols'])}, the IV "
            f"logit {say_num(C['mean']['el_iv'])}, and the random-coefficient estimator "
            f"{say_num(C['mean']['el_blp'])}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(d) for d in tr], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in iv], lag_ratio=0.004), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def real(self):
        B = load("blpdata")
        S = B["scatter"]
        ax = plane([0, 50], [-9, 0.5], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40, 50], yticks=[-8, -6, -4, -2, -1, 0],
                   xlabel=r"price, \ thousands of 1983 dollars", ylabel=r"own-price elasticity",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        one = seg(ax, 0, -1, 50, -1, LOSS, 2.0, dashed=True)
        ols = VGroup(*[dot(ax, x, y, OLS_C, 0.04) for x, y in zip(S["price"], S["el_ols"]) if x <= 50 and y > -9])
        iv = VGroup(*[dot(ax, x, y, IV_C, 0.04) for x, y in zip(S["price"], S["el_iv"]) if x <= 50 and y > -9])
        o, v = B["ols"], B["iv"]
        side = VGroup(
            label(rf"{B['n']:,} models, \\ {B['years'][0]}--{B['years'][1]}", font_size=19, color=WHITE),
            label(rf"OLS: \ {o['inelastic']:,} with \\ inelastic demand", font_size=19, color=OLS_C),
            label(rf"IV: \ {v['inelastic']:,} \ (first-stage \\ F = {v['F']:.0f})", font_size=19, color=IV_C),
            label(r"above the dashed line: \\ no profit-maximizing \\ firm would price there", font_size=18,
                  color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Berry, \ Levinsohn and Pakes's data \ (BLPestimatoR); \ computed", corner=DR,
                       font_size=11)
        with self.voiceover(
            "Now the real thing: the data Berry, Levinsohn and Pakes used. <bookmark mark='a'/> "
            f"{B['n']:,} car models sold in the United States between {B['years'][0]} and {B['years'][1]}, with "
            "prices, shares and characteristics. <bookmark mark='b'/> Plain logit by ordinary least squares says "
            f"that {o['inelastic']:,} of them face inelastic demand, an elasticity below one. "
            "<bookmark mark='c'/> That cannot be right: a firm facing inelastic demand could raise its price, sell "
            "a little less, and earn more. Instrumenting price with the characteristics of each firm's other models "
            f"and of its rivals' models, as they did, cuts the count to {v['inelastic']:,}, with a strong first "
            "stage. <bookmark mark='d'/> Better, but still hundreds of impossible answers, which their paper also "
            "reports for simple specifications. Plain logit cannot describe this market."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(one), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in ols], lag_ratio=0.004), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(d) for d in iv], lag_ratio=0.004), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def dollars(self):
        B = load("blpdata")
        S = B["scatter"]
        v = B["iv"]
        ax = plane([0, 50], [0, 12], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40, 50], yticks=[0, 3, 6, 9, 12],
                   xlabel=r"price, \ thousands of 1983 dollars", ylabel=r"markup, \ thousands of 1983 dollars",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}", font_size=14)
        pts = VGroup(*[dot(ax, x, y, IV_C, 0.045) for x, y in zip(S["price"], S["dollars_iv"]) if x <= 50])
        lvl = seg(ax, 0, v["single_dollars"], 50, v["single_dollars"], PRICE, 2.0, dashed=True)
        eq = MathTex(r"p - c \;=\; \frac{1}{\alpha\,(1 - s)} \;\approx\; \frac{1}{\alpha}", font_size=38,
                     color=PRICE).to_corner(UR, buff=0.6)
        side = VGroup(
            label(rf"the IV logit: \ about \\ \${1000 * v['single_dollars']:,.0f} on every car", font_size=19,
                  color=IV_C),
            label(r"the cheapest and the \\ dearest, \ alike", font_size=19, color=LOSS),
            label(r"random coefficients: \\ the buyers of dear cars \\ care less about price, \\ so dear cars carry "
                  r"\\ larger markups", font_size=18, color=BLP_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).next_to(eq, DOWN, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Berry, \ Levinsohn and Pakes's data; \ computed", corner=DR, font_size=11)
        with self.voiceover(
            "There is a deeper problem, and it is the one that matters for market power. <bookmark mark='a'/> A "
            "single-product firm facing plain logit demand sets a markup, in dollars, of one over alpha times one "
            "minus its share, and with tiny shares that is just one over alpha. So the IV logit gives every car "
            f"almost the same markup: about {round(1000 * v['single_dollars'], -2):,.0f} dollars of 1983 money. "
            "<bookmark mark='b'/> The cheapest small car and the dearest luxury saloon, alike. "
            "<bookmark mark='c'/> With random coefficients the buyers of dear cars are the ones who care least "
            "about price, so dear cars carry larger markups, which is what Berry, Levinsohn and Pakes found. The "
            "flexibility is not a refinement. It is what lets the data, rather than the model's shape, decide where "
            "market power lies."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in pts], lag_ratio=0.004), Create(lvl), FadeIn(side[0]),
                      run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
