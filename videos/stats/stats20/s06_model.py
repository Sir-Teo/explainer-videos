from __future__ import annotations

from videos.stats.stats20.common import *  # noqa: F403

NAMES = {"intercept": r"intercept", "sodium": r"sodium, \ per g", "age": r"age, \ per year", "female": r"female",
         "bmi": r"BMI, \ per kg/m$^2$", "energy": r"energy, \ per 1,000 kcal"}


class FirstModel(VoiceoverScene):
    def construct(self):
        self.card()
        self.equation()
        self.weighting()
        self.table()
        self.reading()
        self.forest()
        self.verdict()

    def card(self):
        card = chapter_card(5, r"A first model", r"The plan, \ fitted", part=PART)
        with self.voiceover("Chapter five. A first model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def equation(self):
        rows = [
            cmath(r"\text{SBP}_i", r"=", r"\beta_0 + \beta_1\,\text{sodium}_i + \beta_2\,\text{age}_i + \beta_3\,\text{female}_i + \beta_4\,\text{BMI}_i + \beta_5\,\text{energy}_i + \varepsilon_i", font_size=26),
            cmath(r"\hat\beta", r"=", r"\arg\min \textstyle\sum_i w_i \big(\text{SBP}_i - x_i'\beta\big)^2", font_size=30),
            cmath(r"\beta_1", r":", r"\text{the estimand of chapter one}", font_size=30),
            cmath(r"\text{assumed}", r":", r"\text{linear in each; \ no interactions; \ for now}", font_size=28),
        ]
        rows[2][2].set_color(SALT)
        whys = [why(r"Part 12's least squares"), why(r"$w_i$: \ the day-1 dietary weights"),
                why(r"the difference per gram, \ others held fixed"), why(r"chapter six checks it")]
        with self.voiceover(
            "<bookmark mark='a'/> Here is the model from the plan: systolic pressure as a linear function of sodium, age, sex, "
            "body mass index and energy, plus an error. <bookmark mark='b'/> It's fitted by Part 12's least squares, with each "
            "adult's squared residual weighted by their survey weight. <bookmark mark='c'/> The coefficient on sodium, beta one, "
            "is chapter one's estimand: the difference in mean pressure per gram a day, among adults alike in the other four. "
            "<bookmark mark='d'/> We're assuming each relationship is a straight line and that sodium's slope is the same for "
            "everyone. Those are assumptions to check, which is chapter six."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.2, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def weighting(self):
        rows = fit_rows(VGroup(
            label(r"why weight a regression?", font_size=28),
            label(r"if the model is right and the slope the same for everyone: \ weights only cost precision", font_size=22, color=GREY_A),
            label(r"if slopes differ between groups: \ unweighted, \ a sample-shaped average", font_size=22, color=RES),
            label(r"weighted: \ the slope you'd get by fitting the whole population", font_size=22, color=DES),
            label(r"DuMouchel \& Duncan (1983); \ Solon, \ Haider \& Wooldridge (2015)", font_size=20, color=GREY_B),
            label(r"we pre-specified weights; \ chapter eight shows both", font_size=22, color=OBS),
        ), 12.4, 0.42, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Chapter two said weighting a mean isn't optional. For a regression slope the argument is "
            "subtler. <bookmark mark='b'/> If the model is exactly right and the slope is the same for everyone, the weights "
            "don't remove any bias, and because they're so unequal they cost precision. <bookmark mark='c'/> But if the slope "
            "differs between groups, an unweighted fit averages those slopes in the proportions of the sample, which "
            "oversampled some groups on purpose. <bookmark mark='d'/> The weighted fit estimates the slope you'd get by fitting "
            "the whole population: a well-defined descriptive estimand even when the model is wrong. <bookmark mark='e'/> "
            "William DuMouchel and Greg Duncan made this argument in 1983, and Gary Solon and colleagues revisited it in 2015. "
            "<bookmark mark='f'/> We chose weights in the plan, and chapter eight shows the answer both ways."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def table(self):
        d = load("model")
        hdr = [r"\textbf{term}", r"\textbf{estimate}", r"\textbf{design SE}", r"\textbf{95\% CI} \ ($t_{15}$)"]
        body = [[NAMES[n], f"{b:+.2f}", f"{s:.2f}", rf"[{lo:+.2f}, \ {hi:+.2f}]"]
                for n, b, s, lo, hi in zip(d["names"], d["b"], d["se"], d["lo"], d["hi"])]
        t = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.28,
                       colors=[GREY_A] + [SALT if n == "sodium" else None for n in d["names"]])
        t.move_to([0, 0.2, 0])
        foot = label(rf"$n = {d['n']:,}$ adults not on BP medicine; \ weighted; \ 15 degrees of freedom", font_size=22,
                     color=GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> And here is the fit, on three thousand and seventy-one adults, with design-based standard "
            "errors and intervals from the t distribution with fifteen degrees of freedom. <bookmark mark='b'/> Age: plus point "
            "four zero millimetres a year. Women: five lower than men of the same age and size. BMI: plus point five two per "
            "unit. Energy: nothing to speak of. <bookmark mark='c'/> And sodium: plus point zero seven millimetres per gram, "
            "with a standard error of point two seven, and an interval from minus point five to plus point six."
        ) as vo:
            self.add(nh_tag(corner=DR))
            vo.wait_until("a")
            self.play(FadeIn(t[0]), FadeIn(t[1]), FadeIn(foot))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t[i], shift=RIGHT * 0.15) for i in range(3, len(t))], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(t[2], shift=RIGHT * 0.15))
            self.play(Indicate(t[2], color=SALT))
        self.wait(4.0)
        self.clear_scene()

    def reading(self):
        d = load("model")
        b = dict(zip(d["names"], d["b"]))
        rows = [
            cmath(r"\text{ten years older}", r":", rf"+{10 * b['age']:.1f} \text{{ mm Hg}}", font_size=30),
            cmath(r"\text{five BMI units}", r":", rf"+{5 * b['bmi']:.1f} \text{{ mm Hg}}", font_size=30),
            cmath(r"\text{woman vs man}", r":", rf"{b['female']:.1f} \text{{ mm Hg}}", font_size=30),
            cmath(r"\text{one gram of sodium}", r":", rf"{b['sodium']:+.2f} \text{{ mm Hg}}", font_size=30),
        ]
        rows[3][2].set_color(SALT)
        whys = [why(r"precisely estimated: \ $\pm 0.5$"), why(r"obesity and pressure, \ well known"),
                why(r"of the same age, \ size and energy"), why(r"$p = 0.81$: \ indistinguishable from zero")]
        with self.voiceover(
            "<bookmark mark='a'/> Reading the coefficients as a reader would: ten years of age go with four millimetres more, "
            "precisely estimated. <bookmark mark='b'/> Five units of BMI, roughly the difference between a normal weight and "
            "obesity at a given height, go with two point six more. <bookmark mark='c'/> Women average five less than men "
            "like them. <bookmark mark='d'/> And a gram of sodium a day goes with seven hundredths of a millimetre, with a "
            "p-value of point eight one. Chapter one's descriptive estimand is, as far as these data can tell, zero."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.75, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def forest(self):
        d = load("model")
        j = d["names"].index("sodium")
        A = axes([-1, 4], [0, 3], x_length=10.0, y_length=3.0, xlabel=r"mm Hg per g/day of sodium", xticks=[-1, 0, 1, 2, 3, 4],
                 center=[0, 0.6, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 3), color=GREY_C, stroke_width=1.5)
        trial = Rectangle(width=ax.c2p(3, 0)[0] - ax.c2p(2, 0)[0], height=ax.c2p(0, 2.6)[1] - ax.c2p(0, 0.4)[1], stroke_width=0,
                          fill_color=HIT, fill_opacity=0.25).move_to(ax.c2p(2.5, 1.5))
        tl = label(r"the trials: \ 2--3", font_size=22, color=HIT).next_to(trial, UP, buff=0.1)
        est = Dot(ax.c2p(d["b"][j], 1.5), radius=0.1, color=SALT)
        ci = Line(ax.c2p(d["lo"][j], 1.5), ax.c2p(d["hi"][j], 1.5), color=SALT, stroke_width=6)
        el = label(r"NHANES: \ the survey's slope", font_size=22, color=SALT).next_to(ci, DOWN, buff=0.25)
        rows = fit_rows(VGroup(
            label(r"not ``no effect'': \ an interval that ends at $+0.63$", font_size=24),
            label(r"and excludes what the trials found", font_size=24, color=RES),
            label(r"the survey and the trials disagree: \ one of them is not measuring what we think", font_size=22, color=OBS),
        ), 12.0, 0.3, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Let's put it on a line with the trials. In gold, the survey's slope and its ninety-five "
            "percent interval. <bookmark mark='b'/> In green, the range randomized trials have found: two to three millimetres "
            "per gram. <bookmark mark='c'/> The honest reading is not no effect. It's an interval that runs up to plus point "
            "six three, <bookmark mark='d'/> and so excludes what the trials found, by a wide margin. <bookmark mark='e'/> Two "
            "careful bodies of evidence disagree. Either salt doesn't do what the trials say, or this survey slope is not "
            "measuring the effect of salt. The next four chapters find out which."
        ) as vo:
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(Create(ci), FadeIn(est, scale=1.5), FadeIn(el))
            vo.wait_until("b")
            self.play(FadeIn(trial), FadeIn(tl))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def verdict(self):
        rows = fit_rows(VGroup(
            label(r"the plan was followed; \ the primary result is reported as it came", font_size=24, color=HIT),
            label(r"a null result from a survey this size is still information", font_size=24),
            label(r"but before believing it: \ is the model wrong? \ chapter six", font_size=24, color=OBS),
            label(r"are the intervals right? \ chapter seven", font_size=24, color=DES),
            label(r"does it depend on our choices? \ is the exposure measured well? \ chapter eight", font_size=24, color=SALT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> We followed the plan, and the primary result goes in the report as it came out. "
            "<bookmark mark='b'/> A null result from three thousand people measured this carefully is information, not a "
            "failure. <bookmark mark='c'/> But before anyone believes it, three questions. Is the model wrong in some way that "
            "hides the effect? <bookmark mark='d'/> Are the intervals right? <bookmark mark='e'/> And does the answer depend on "
            "the choices we made, and on how badly one day's recall measures the usual diet?"
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
