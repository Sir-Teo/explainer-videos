from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403


class Identify(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Identification", r"What in the data pins down what in the model?",
             "Chapter eight. Identification.", lit={1949: r"Koopmans", 2017: r"Andrews, Gentzkow and Shapiro"},
             scale=("household",), horizon=("a century",))
        self.idea()
        self.bars()
        self.fragile()

    def idea(self):
        rows = VGroup(
            label(r"identified: \ with unlimited data, \ only one value of the parameters fits", font_size=22,
                  color=THEORY),
            label(r"the Play it: \ four facts, \ one line of values \ (weakly identified)", font_size=22,
                  color=CAUTION),
            label(r"Rust's buses: \ the discount factor, \ barely identified \ (Part 44's Dial)", font_size=22,
                  color=GREY_A),
            label(r"what identifies: \ variation that moves one parameter's footprint and not another's", font_size=22,
                  color=GAIN),
            label(r"in practice: \ which moments does this estimate lean on?", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(UP * 0.2)
        eq = MathTex(r"\Lambda = -\left(G'WG\right)^{-1} G'W", font_size=40, color=THEORY).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Koopmans (1949); \ Andrews, \ Gentzkow and Shapiro, \ QJE 132(4) (2017)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Behind every estimate is a question that has nothing to do with sample size. <bookmark mark='a'/> A "
            "parameter is identified if, with unlimited data, only one value of it would fit. Tjalling Koopmans "
            "and the Cowles Commission put the question at the centre of econometrics from 1949. <bookmark "
            "mark='b'/> The Play it showed a weak case: four facts that leave a whole line of values almost "
            "equally good. <bookmark mark='c'/> Rust's buses showed another: the discount factor barely moves the "
            "likelihood. <bookmark mark='d'/> What identifies a parameter is variation in the data that moves its "
            "footprint and not the others'. <bookmark mark='e'/> And in practice the useful question is: which "
            "moments is this estimate leaning on? Isaiah Andrews, Matthew Gentzkow and Jesse Shapiro answered it "
            "with one matrix, built from the same pieces as the standard errors. It says how far each estimate "
            "moves when each moment moves a little."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            self.play(Write(eq))
        self.clear_scene()

    def bars(self):
        L = load("lifecycle")
        lam = np.array(L["Lambda"])[1]
        d = np.array(L["data"])
        eff = lam * 0.01 * d
        n = len(eff)
        ax = plane([-0.7, n - 0.3], [-6.5, 4.5], center=LEFT * 1.3 + DOWN * 0.1, x_length=9.4, y_length=4.8,
                   xticks=[], yticks=[-6, -4, -2, 0, 2, 4], ylabel=r"change in $\hat\gamma$",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        zero = DashedLine(ax.ax.c2p(-0.7, 0), ax.ax.c2p(n - 0.3, 0), color=GREY_D, stroke_width=1.2)
        ages = L["ages"]
        bars = VGroup()
        labs = VGroup()
        for k, v in enumerate(eff):
            col = DATA if k < 10 else CAUTION
            p0, p1 = ax.ax.c2p(k - 0.35, 0), ax.ax.c2p(k + 0.35, v)
            h = p1[1] - p0[1]
            r = Rectangle(width=p1[0] - p0[0], height=max(abs(h), 0.01), fill_color=col, fill_opacity=0.85,
                          stroke_width=0).move_to(((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0))
            bars.add(r)
            age = ages[k] if k < 10 else ages[k - 6]
            labs.add(label(f"{age - 2.5:.0f}", font_size=12, color=col).next_to(ax.ax.c2p(k, -6.5), DOWN,
                                                                                buff=0.12))
        key = VGroup(label(r"blue: \ consumption at each age", font_size=18, color=DATA),
                     label(r"pink: \ wealth at each age", font_size=18, color=CAUTION)).arrange(
            RIGHT, buff=0.6).to_edge(UP, buff=0.5)
        side = VGroup(
            label(r"each bar: \ if this one \\ fact in the data were \\ 1\% higher", font_size=18, color=WHITE),
            label(rf"the standard error \\ of $\hat\gamma$: \ {L['se'][1]:.2f}", font_size=18, color=THEORY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = island_tag(r"simulated: \ the Island's households", corner=DR, font_size=13)
        with self.voiceover(
            "Here it is for caution, in the Island's life-cycle estimate. <bookmark mark='a'/> Each bar is one of "
            "the sixteen facts: consumption at ten ages in blue, wealth at six in pink. Its height is how far the "
            "estimate of caution would move if that one fact in the data were one percent higher. <bookmark "
            f"mark='b'/> The standard error of the estimate is {L['se'][1]:.2f}. <bookmark mark='c'/> The bars are "
            f"enormous by comparison, and they alternate in sign. One percent more wealth at sixty-five moves it by "
            f"{say_num(eff[-1], 1)}; one percent more wealth at sixty, by {say_num(eff[-2], 1)}. The efficient "
            "estimate is reading tiny differences between facts that move almost together, the line from the "
            "Play it, and amplifying them."
        ) as vo:
            self.play(FadeIn(ax), Create(zero), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v >= 0 else UP) for b, v in zip(bars, eff)],
                                  lag_ratio=0.08), FadeIn(labs), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(bars[-1], color=WHITE, scale_factor=1.05), Indicate(bars[-2], color=WHITE,
                                                                                    scale_factor=1.05))
        self.clear_scene()

    def fragile(self):
        F = load("fragile")
        L = load("lifecycle")
        e = F["efficient"]
        rows = VGroup(
            label(r"suppose the survey overstates every household's wealth by 1\%", font_size=23, color=CAUTION),
            label(rf"the matrix predicts: \ $\hat\gamma$ moves by {e['pred'][1]:+.2f}".replace("-", "{-}"),
                  font_size=23, color=THEORY),
            label(rf"estimating again: \ it moves by {e['actual'][1]:+.2f}".replace("-", "{-}"), font_size=23,
                  color=EST),
            label(rf"its standard error: \ {L['se'][1]:.2f}, \ so the shift is "
                  rf"{abs(e['actual'][1]) / L['se'][1]:.0f} standard errors", font_size=23, color=ERR),
            label(r"a standard error measures noise, \ not a wrong assumption about the data", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(UP * 0.1)
        tag = island_tag(r"simulated: \ the Island's households", corner=DR, font_size=13)
        with self.voiceover(
            "So test it. <bookmark mark='a'/> Suppose the survey overstated every household's wealth by one "
            "percent, a tiny error by the standards of any real survey. <bookmark mark='b'/> Adding up the pink "
            f"bars, the matrix predicts that caution's estimate moves by {say_num(e['pred'][1], 2)}. <bookmark "
            f"mark='c'/> Estimating the whole model again, it moves by {say_num(e['actual'][1], 2)}: the matrix "
            "was right, and it took no new estimation to know. <bookmark mark='d'/> That shift is "
            f"{abs(e['actual'][1]) / L['se'][1]:.0f} standard errors. <bookmark mark='e'/> A standard error "
            "measures how much the estimate would vary with a new sample from the same world. It says nothing "
            "about an assumption that is slightly wrong. The sensitivity matrix shows which assumptions matter, "
            "and a careful paper reports it beside the estimates."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
