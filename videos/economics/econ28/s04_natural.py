from __future__ import annotations

from videos.economics.econ28.common import *  # noqa: F403


class Natural(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The natural rate", r"What happens if policy holds unemployment below it?", "Chapter three. "
             "The natural rate.", lit={1967: r"Phelps", 1968: r"Friedman"}, scale=("nation",), horizon=("years",))
        self.idea()
        self.accelerate()
        self.lesson()

    def idea(self):
        rows = VGroup(
            label(r"Friedman (1968) and Phelps (1967): \ workers and firms care about \emph{real} wages", font_size=24,
                  color=E.ACCENT),
            label(r"a wage deal builds in the inflation both sides expect", font_size=23, color=WAGE),
            MathTex(r"\pi = \pi^e - \beta\,(u - u^*)", font_size=46, color=WHITE),
            label(r"$u^*$: \ the natural rate, \ set by the labour market's frictions \ (Part 24)", font_size=22,
                  color=OUTPUT),
            label(r"unemployment is below $u^*$ only while inflation runs above what people expect", font_size=23,
                  color=INFL),
            label(r"so there is a curve for every level of expected inflation", font_size=23, color=EXPECT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Friedman, \ AER 58(1) (1968); \ Phelps, \ Economica 34(135) (1967): \ 254--281",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Friedman's argument, which Edmund Phelps had made a year earlier in a different form, starts with what "
            "people bargain over. <bookmark mark='a'/> Workers care about what their wages buy, and so do firms. So "
            "a wage deal builds in the inflation both sides expect. <bookmark mark='b'/> The curve becomes this: "
            "inflation equals expected inflation, minus a term in how far unemployment is from its natural rate. "
            "<bookmark mark='c'/> The natural rate is the unemployment that the labour market's frictions produce "
            "on their own, the search and matching of Part twenty-four. <bookmark mark='d'/> Unemployment can sit "
            "below it only while inflation runs above what people expect: only while they are surprised. "
            "<bookmark mark='e'/> So there is not one curve but a whole family, one for every level of expected "
            "inflation."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def accelerate(self):
        A = load("accelerate")
        f, s = A["fast"], A["slow"]
        yrs = np.arange(1, A["years"] + 1)
        ax = plane([0, A["years"] + 1], [0, 10], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0, 5, 10, 15], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"year", ylabel=r"inflation, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        fast = path(ax, yrs, f["pi"], color=INFL, width=4, smooth=False)
        fexp = path(ax, yrs, f["expected"], color=EXPECT, width=2, smooth=False)
        slow = path(ax, yrs, s["pi"], color=SURPRISE, width=4, smooth=False)
        side = VGroup(
            label(rf"the council holds unemployment at {A['u_target']:.0f}\%, \\ a point below the natural "
                  rf"{A['ustar']:.0f}\%", font_size=19, color=CB),
            label(r"expectations: \ last year's inflation", font_size=19, color=EXPECT),
            label(rf"inflation rises {A['fast']['step']:.1f} a point every year: \\ "
                  rf"{f['pi'][0]:.1f}, \ {f['pi'][1]:.1f}, \ {f['pi'][2]:.1f}, \ ... \ {f['pi'][-1]:.1f}",
                  font_size=19, color=INFL),
            label(rf"slower-learning expectations \\ ({100 * A['lam_slow']:.0f}\% of each surprise): \\ a slower "
                  r"climb, \ that never stops", font_size=19, color=SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Watch it on the Island. <bookmark mark='a'/> The council decides to hold unemployment at "
            f"{A['u_target']:.0f} percent, a point below the natural rate of {A['ustar']:.0f}. Each point of "
            f"unemployment below the natural rate adds {A['beta']} of a point to inflation, over what people "
            "expect. <bookmark mark='b'/> People expect whatever inflation they saw last year. "
            f"<bookmark mark='c'/> In the first year inflation rises from two percent to {f['pi'][0]:.1f}. Next "
            f"year people expect {f['pi'][0]:.1f}, so to stay surprised inflation must reach {f['pi'][1]:.1f}. "
            f"Then {f['pi'][2]:.1f}, and on: after fifteen years, {f['pi'][-1]:.1f} percent, and still rising. "
            "Holding unemployment below its natural rate does not take high inflation; it takes accelerating "
            "inflation. <bookmark mark='d'/> If expectations learn more slowly, inflation climbs more slowly, but "
            "it never stops."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(fexp), run_time=1)
            vo.wait_until("c")
            self.play(Create(fast), FadeIn(side[2]), run_time=3)
            vo.wait_until("d")
            self.play(Create(slow), FadeIn(side[3]), run_time=2)
        self.clear_scene()

    def lesson(self):
        rows = VGroup(
            label(r"the accelerationist lesson", font_size=28, color=E.ACCENT),
            label(r"in the long run the curve is vertical at $u^*$: \ no permanent trade-off", font_size=24,
                  color=OUTPUT),
            label(r"in the short run, \ surprises move unemployment; \ surprises cannot last", font_size=24,
                  color=INFL),
            label(r"so steady inflation buys nothing; \ rising inflation buys a little, \ for a while", font_size=24,
                  color=EXPECT),
            label(r"the NAIRU: \ the non-accelerating-inflation rate of unemployment", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "The lesson. <bookmark mark='a'/> In the long run the curve is vertical, at the natural rate: there is "
            "no permanent trade-off. <bookmark mark='b'/> In the short run, surprises move unemployment, but "
            "surprises cannot be kept up. <bookmark mark='c'/> So steady inflation buys nothing, and rising "
            "inflation buys a little, for a while. <bookmark mark='d'/> Economists later called the natural rate "
            "the NAIRU, the unemployment rate at which inflation does not accelerate. It is the number every "
            "central bank tries to estimate, and nobody can see directly."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
