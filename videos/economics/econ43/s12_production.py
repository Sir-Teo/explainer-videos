from __future__ import annotations

from videos.economics.econ43.common import *  # noqa: F403


class Production(VoiceoverScene):
    def construct(self):
        card(self, 10, r"The supply side: \ production functions", r"How do you estimate what inputs produce?",
             "Chapter ten. The supply side: production functions.",
             lit={1996: r"Olley and Pakes", 2003: r"Levinsohn and Petrin", 2015: r"Ackerberg, \ Caves and Frazer"},
             scale=("firm",), horizon=("a year", "a decade"))
        self.problem()
        self.proxy()
        self.results()
        self.fact()

    def problem(self):
        P = load("plants")
        T = TRUTH["plants"]
        l, yk, om = (np.array(P[c]) for c in ("l", "yk", "omega"))
        xr_ = (float(np.quantile(l, 0.01)) - 0.1, float(np.quantile(l, 0.99)) + 0.1)
        yr_ = (float(np.quantile(yk, 0.01)) - 0.1, float(np.quantile(yk, 0.99)) + 0.1)
        ax = plane(list(xr_), list(yr_),
                   center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6, xticks=[], yticks=[],
                   xlabel=r"log labour, \ $l$", ylabel=r"log output less capital's part, \ $y - 0.3k$", font_size=14)
        lo, hi = np.quantile(om, 0.05), np.quantile(om, 0.95)
        pts = VGroup()
        for x, y, o in zip(l, yk, om):
            if not (xr_[0] <= x <= xr_[1] and yr_[0] <= y <= yr_[1]):
                continue
            f = float(np.clip((o - lo) / (hi - lo), 0, 1))
            pts.add(dot(ax, x, y, interpolate_color(ManimColor(DEMAND), ManimColor(PRICE), f), 0.045))
        xr = np.array([np.quantile(l, 0.03), np.quantile(l, 0.97)])
        mid = float(np.mean(l))
        b_ols = (P["ols"]["bl"], float(np.mean(yk)) - P["ols"]["bl"] * mid)
        ols = seg(ax, xr[0], np.polyval(b_ols, xr[0]), xr[1], np.polyval(b_ols, xr[1]), OLS_C, 3.0)
        c0 = float(np.mean(yk)) - T["bl"] * mid
        true = seg(ax, xr[0], c0 + T["bl"] * xr[0], xr[1], c0 + T["bl"] * xr[1], TRUTH_C, 3.0)
        side = VGroup(
            label(r"$y = \beta_l\, l + \beta_k\, k + \omega + \varepsilon$", font_size=22, color=WHITE),
            label(r"colour: \ productivity $\omega$, \\ which the plant sees \\ and we do not \\ (blue low, \ gold "
                  r"high)", font_size=17, color=PRICE),
            label(rf"red: \ the OLS slope, \ {b_ols[0]:.2f}", font_size=19, color=OLS_C),
            label(rf"green: \ the true \\ elasticity, \ {T['bl']}", font_size=19, color=TRUTH_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Markups can also be read from the supply side, but first we need production functions, which have "
            "their own famous problem. <bookmark mark='a'/> A plant's output depends on its labour and capital and "
            "on its productivity, omega, which the plant knows and the economist does not. "
            f"<bookmark mark='b'/> Here are three hundred of the Island's {T['n']:,} plants. Colour shows "
            "productivity. The productive "
            "plants, in gold, hire more workers, because each worker produces more there. "
            "<bookmark mark='c'/> So a regression of output on labour credits labour with productivity's work: "
            f"ordinary least squares finds a slope of {b_ols[0]:.2f}. <bookmark mark='d'/> The true elasticity, "
            f"planted on the Island, is {T['bl']}. This is the simultaneity problem, noticed by Marschak and Andrews "
            "in 1944: inputs are chosen with knowledge the economist lacks."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(VGroup(*[p for p in pts]), color=PRICE, scale_factor=1.0))
            vo.wait_until("c")
            self.play(Create(ols), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(true), FadeIn(side[3]))
        self.clear_scene()

    def proxy(self):
        steps = flow_chain([(r"a proxy", DEMAND), (r"stage one", BLP_C), (r"stage two", PRICE)],
                           notes=[r"materials (or investment) \\ rise with $\omega$: \ invert \\ to recover it",
                                  r"$y$ on a flexible function \\ of $(l, k, m)$: \ strips \\ the noise $\varepsilon$",
                                  r"$\omega_t = g(\omega_{t-1}) + \xi_t$: \\ the surprise $\xi_t$ is \\ uncorrelated "
                                  r"with $k_t$, \ $l_{t-1}$"],
                           box_w=3.2, font_size=22, note_size=16).move_to(UP * 0.7)
        names = VGroup(
            label(r"Olley and Pakes \ (1996): \ investment; \ telecommunications equipment after AT\&T's break-up",
                  font_size=18, color=GREY_A),
            label(r"Levinsohn and Petrin \ (2003): \ intermediate inputs", font_size=18, color=GREY_A),
            label(r"Ackerberg, \ Caves and Frazer \ (2015): \ both coefficients from stage two", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.55)
        tag = published_tag(tables.PRODUCTION_1996.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The modern fix uses the plant's own choices as a window on its productivity. "
            "<bookmark mark='a'/> Some input, such as materials, rises with productivity given the other inputs, "
            "so it can be inverted to recover productivity. <bookmark mark='b'/> Stage one regresses output on a "
            "flexible function of labour, capital and materials, stripping out pure noise. "
            "<bookmark mark='c'/> Stage two uses timing. Productivity is persistent, and its surprise this year "
            "cannot have been known when capital was installed last year, or when last year's labour was hired. "
            "Those zero correlations pin down both elasticities. <bookmark mark='d'/> Steven Olley and Ariel Pakes "
            "used investment as the proxy in 1996, studying telecommunications equipment after the break-up of "
            "AT and T; James Levinsohn and Amil Petrin used intermediate inputs; and Daniel Ackerberg, Kevin Caves "
            "and Garth Frazer showed in 2015 that labour's coefficient must come from the second stage."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            for k, mk in zip(range(2), "bc"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in names], lag_ratio=0.4), run_time=1.5)
        self.clear_scene()

    def results(self):
        P = load("plants")
        T = TRUTH["plants"]
        rows = [(r"OLS", P["ols"], OLS_C), (r"within a plant", P["within"], IV_C),
                (r"Ackerberg, \ Caves \\ and Frazer", P["acf"], BLP_C), (r"the truth", {"bl": T["bl"], "bk": T["bk"]},
                                                                          TRUTH_C)]
        ax = plane([0, 1.1], [0, 0.4], center=LEFT * 1.4 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], yticks=[0, 0.1, 0.2, 0.3, 0.4],
                   xlabel=r"labour's elasticity, \ $\beta_l$", ylabel=r"capital's elasticity, \ $\beta_k$",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        dts = VGroup()
        for nm, e, col in rows:
            d = dot(ax, e["bl"], e["bk"], col, 0.11)
            t = label(rf"{nm}: \\ ({e['bl']:.2f}, \ {e['bk']:.2f})", font_size=16, color=col)
            dts.add(VGroup(d, t))
        dts[0][1].next_to(dts[0][0], UP, buff=0.12)
        dts[1][1].next_to(dts[1][0], DOWN, buff=0.12)
        dts[2][1].next_to(dts[2][0], LEFT, buff=0.18)
        dts[3][1].next_to(dts[3][0], UR, buff=0.12)
        side = VGroup(
            label(r"OLS: \ labour takes \\ productivity's credit, \\ capital too little", font_size=18, color=OLS_C),
            label(r"within a plant: \ only \\ partly better, \ and \\ noisier", font_size=18, color=IV_C),
            label(r"the proxy method \\ lands on the truth", font_size=18, color=BLP_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "On the Island's plants, the methods land in very different places. <bookmark mark='a'/> Ordinary least "
            f"squares gives labour an elasticity of {P['ols']['bl']:.2f} and capital {P['ols']['bk']:.2f}: labour "
            "takes productivity's credit, and capital, chosen a year earlier, gets too little. "
            "<bookmark mark='b'/> Comparing each plant with itself over time helps only partly, because "
            "productivity changes from year to year. <bookmark mark='c'/> Ackerberg, Caves and Frazer's estimator "
            f"gives {P['acf']['bl']:.2f} and {P['acf']['bk']:.2f}, <bookmark mark='d'/> against the truth of "
            f"{T['bl']} and {T['bk']}."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(dts[0], scale=1.3), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(dts[1], scale=1.3), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dts[2], scale=1.3), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(dts[3], scale=1.3))
        self.clear_scene()

    def fact(self):
        P = load("plants")
        f = facts.BY_KEY["dispersion"]
        data_m = label(rf"American manufacturing: \\ the 90th-percentile plant \\ makes {P['syverson']} times \\ the "
                       r"10th's, \ same inputs", font_size=18, color=WHITE)
        theory_m = label(r"management, \ technology, \\ selection and \\ distortions \ (Part 62)", font_size=18,
                         color=THEORY)
        agora_m = label(rf"the Island's plants: \\ a 90/10 ratio of \\ {P['ratio']:.2f}, \ planted \\ to match",
                        font_size=18, color=E.AGORA)
        fc = fact_card(tex_safe(f.statement), columns=((r"the data", data_m), (r"the theory", theory_m),
                                                         (r"Agora", agora_m)), width=12.4, font_size=22,
                       colors=(WHITE, THEORY, None)).move_to(UP * 0.3)
        tag = published_tag(r"Syverson, \emph{JEL} (2011)", corner=DR, font_size=11)
        with self.voiceover(
            "Estimating productivity this way revealed one of the series' facts. <bookmark mark='a'/> Within "
            "narrow American manufacturing industries, Chad Syverson found, the plant at the ninetieth percentile "
            f"of productivity makes about {P['syverson']} times as much output from the same inputs as the plant "
            "at the tenth. <bookmark mark='b'/> Why such gaps persist, from management to technology to which plants "
            "survive, is the subject of Part sixty-two. <bookmark mark='c'/> The Island's plants were planted with "
            f"a ratio of {P['ratio']:.2f}, to match."
        ) as vo:
            self.play(FadeIn(fc.card), FadeIn(fc[1][0]), *[FadeIn(c[:2]) for c in fc.cols], FadeIn(tag))
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(fc.cols[k][2:]))
        self.clear_scene()
