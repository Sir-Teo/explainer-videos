from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class RustModel(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Rust's model: \ when to rebuild", r"What costs must Zurcher have believed?",
             "Chapter two. Rust's model: when to rebuild.", lit={1987: r"Rust"}, scale=("firm",),
             horizon=("a month", "a decade"))
        self.model()
        self.loop()
        self.fit()
        self.myopia()

    def model(self):
        lines = VGroup(
            MathTex(r"v_{\text{keep}}(x) \;=\; -\,\theta\,x \;+\; \beta\,EV(x)", font_size=38, color=KEEP),
            MathTex(r"v_{\text{rebuild}} \;=\; -\,RC \;+\; \beta\,EV(0)", font_size=38, color=REBUILD),
            MathTex(r"P(\text{rebuild}\mid x) \;=\; \frac{e^{v_{\text{rebuild}}}}{e^{v_{\text{keep}}(x)} + "
                    r"e^{v_{\text{rebuild}}}}", font_size=38, color=WHITE),
            MathTex(r"EV(x) \;=\; \sum_j p_j \,\ln\!\big(e^{v_{\text{keep}}(x+j)} + e^{v_{\text{rebuild}}}\big)",
                    font_size=38, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.5)
        notes = VGroup(
            label(r"$x$: \ miles since the last rebuild, \ in steps of 5,000; \ $\theta$: \ upkeep per step",
                  font_size=19, color=GREY_A),
            label(r"surprises each month, \ unseen by us, \ make the choice a probability \ (a logit)",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.RUST_1987.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Rust wrote Zurcher's problem down. <bookmark mark='a'/> Keeping an engine at mileage x costs upkeep, "
            "theta times x, plus the value of continuing from there, discounted by beta. <bookmark mark='b'/> "
            "Rebuilding costs RC, and returns the bus to zero miles. <bookmark mark='c'/> Each month also brings "
            "surprises, which Zurcher sees and we do not. If they follow the logit's distribution, the chance of a "
            "rebuild at mileage x is a logit in the two values. <bookmark mark='d'/> And the expected value of "
            "the future, EV, must satisfy its own equation: next month's mileage rises by j steps with "
            "probability p j, and the bus is then worth the best of keeping and rebuilding, with the surprises "
            "averaged out. That equation is a fixed point: EV appears on both sides."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Write(lines[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Write(lines[3]))
        self.clear_scene()

    def loop(self):
        R = load("rust")
        steps = flow_chain([(r"guess $RC$, \ $\theta$", BUS), (r"solve for $EV$", E.ACCENT),
                            (r"choice probabilities", KEEP), (r"likelihood", GAIN)],
                           notes=[r"the costs to try", r"the fixed point, \\ to the last digit",
                                  r"$P(\text{rebuild}\mid x)$ \\ at every mileage", r"how probable \\ Zurcher's "
                                                                                    r"choices are"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.6)
        loop = CurvedArrow(steps.boxes[3].get_bottom() + DOWN * 1.05, steps.boxes[0].get_bottom() + DOWN * 1.05,
                           angle=-TAU / 6, color=GREY_B, stroke_width=2.2)
        lab = label(r"try better costs, \ and solve again", font_size=18, color=GREY_B).next_to(loop, DOWN, buff=0.1)
        foot = label(rf"each solution takes a fraction of a second today; \ the whole search, \ {R['seconds']:.1f} "
                     r"seconds", font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.45)
        tag = published_tag(tables.RUST_1987.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Rust's estimator is a loop inside a loop, the nested fixed point. <bookmark mark='a'/> Guess the "
            "costs. <bookmark mark='b'/> Solve the fixed point for the expected value, exactly. <bookmark mark='c'/> "
            "That gives the chance of a rebuild at every mileage. <bookmark mark='d'/> Multiply up the "
            "probabilities of the choices Zurcher actually made: the likelihood. <bookmark mark='e'/> Then try "
            "better costs, solve again, and repeat until the likelihood is as high as it can be. In 1987 each solve "
            f"was a serious computation; on Zurcher's buses today the whole search takes {R['seconds']:.1f} seconds."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            for k, mk in zip(range(3), "bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
            vo.wait_until("e")
            self.play(Create(loop), FadeIn(lab), FadeIn(foot))
        self.clear_scene()

    def fit(self):
        R = load("rust")
        nf = R["nfxp"]
        xs = np.arange(len(R["p1"])) * 5
        ax = plane([0, 450], [0, 0.06], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 100, 200, 300, 400], yticks=[0, 0.02, 0.04, 0.06],
                   xlabel=r"miles since the last rebuild, \ thousands", ylabel=r"chance of a rebuild this month",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, xs, R["p1"], REBUILD, 3.2, yr=(0, 0.06))
        obs = VGroup(*[dot(ax, m / 1000, f, BUS, 0.03 + 0.0009 * np.sqrt(c)) for m, f, c in
                       zip(R["mids"], R["freq"], R["counts"]) if f <= 0.06])
        p = R["p"]
        side = VGroup(
            label(rf"{R['buses_used']} buses \ (Rust's groups 1--4), \\ {R['n_obs']:,} bus-months, \\ "
                  rf"{R['n_repl']} rebuilds", font_size=18, color=WHITE),
            label(rf"monthly steps: \ 0, \ 1, \ 2 \\ with chances {100 * p[0]:.0f}\%, \ {100 * p[1]:.0f}\%, \ "
                  rf"{100 * p[2]:.0f}\%", font_size=17, color=KEEP),
            label(rf"$RC$ = {nf['RC']:.2f} \ (se {nf['se'][0]:.2f}) \\ $\theta$ = {nf['theta1']:.2f} \ (se "
                  rf"{nf['se'][1]:.2f}), \ per 1,000", font_size=18, color=E.ACCENT),
            label(rf"a rebuild costs as much as \\ {R['months_of_upkeep']:.0f} months of upkeep \\ at 150,000 miles",
                  font_size=18, color=BUS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Rust's data; \ estimated here", corner=DR, font_size=11)
        with self.voiceover(
            "Run it on Zurcher's buses. <bookmark mark='a'/> Rust's main estimates used four groups: "
            f"{R['buses_used']} buses, {R['n_obs']:,} bus-months and {R['n_repl']} rebuilds. The gold dots show, at "
            "each mileage, the share of bus-months in which Zurcher rebuilt the engine. <bookmark mark='b'/> First "
            "the mileage: in a month a bus moved zero, one or two steps of five thousand miles, with chances of "
            f"{say_pct(p[0], 0)}, {say_pct(p[1], 0)} and {say_pct(p[2], 0)}. <bookmark mark='c'/> Then the costs: a "
            f"rebuild cost of {nf['RC']:.2f} and an upkeep cost of {nf['theta1']:.2f} per thousand steps, both "
            "measured against the size of the monthly surprises, which is all the data can reveal. The red curve is "
            "the chance of a rebuild those costs imply, rising with mileage through the dots. "
            f"<bookmark mark='d'/> In plainer terms, a rebuild cost as much as {R['months_of_upkeep']:.0f} months "
            "of upkeep on an engine at a hundred and fifty thousand miles."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o, scale=1.4) for o in obs], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), Create(ln), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def myopia(self):
        R = load("rust")
        prof = R["profile"]
        labels_ = [rf"{p['beta']:g}" for p in prof]
        lls = np.array([p["loglik"] for p in prof])
        ax = plane([-0.5, len(prof) - 0.5], [-307, -298], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2,
                   y_length=4.6, xticks=list(range(len(prof))), yticks=[-306, -304, -302, -300, -298],
                   xlabel=r"monthly discount factor, \ $\beta$", ylabel=r"log likelihood of Zurcher's choices",
                   xfmt=lambda v: labels_[int(round(v))] if 0 <= round(v) < len(labels_) else "",
                   yfmt=lambda v: f"{v:.0f}", font_size=13)
        dts = VGroup(*[dot(ax, k, ll, PATIENT if p["beta"] > 0 else MYOPIC, 0.09) for k, (p, ll) in
                       enumerate(zip(prof, lls))])
        ln = path(ax, list(range(len(prof))), lls, PATIENT, 2.4, smooth=False)
        side = VGroup(
            label(r"$\beta$ = 0: \ a myopic \\ Zurcher, \ who ignores \\ the future", font_size=18, color=MYOPIC),
            label(rf"likelihood ratio: \ {R['lr']:.1f} \\ (5\% critical value 3.84): \\ myopia rejected",
                  font_size=18, color=GAIN),
            label(r"but among patient \\ values the curve \\ is nearly flat", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Rust's data; \ estimated here", corner=DR, font_size=11)
        with self.voiceover(
            "Was Zurcher looking ahead at all? <bookmark mark='a'/> Fix the discount factor at zero, a superintendent "
            "who ignores every future month, and estimate again. The fit is worse. <bookmark mark='b'/> The "
            f"likelihood-ratio statistic is {R['lr']:.1f}, far above the 3.84 needed to reject at five percent: "
            "the data reject myopia, as Rust found. <bookmark mark='c'/> But look at the patient end. From a "
            "discount factor of 0.99 a month to 0.9999 the likelihood barely changes, so the data cannot say "
            "precisely how patient Zurcher was. Rust fixed it at 0.9999. That the discount factor is hard to "
            "identify is a general lesson of dynamic models, and a dial in chapter thirteen."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[FadeIn(d, scale=1.4) for d in dts], lag_ratio=0.15),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(dts[0], color=WHITE))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(side[1]), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
