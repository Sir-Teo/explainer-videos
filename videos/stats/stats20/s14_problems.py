from __future__ import annotations

from videos.stats.stats20.common import *  # noqa: F403

PROBLEMS = [
    {"part": r"Parts 2 and 15", "color": RES,
     "q": r"A condition affects 1\% of adults. \ Two independent tests each detect it 90\% of the time and give false alarms 5\% of the time. \ Both are positive: \ how likely is the condition?",
     "steps": [r"P(\text{both} + \mid \text{sick}) = 0.9^2 = 0.81", r"P(\text{both} + \mid \text{well}) = 0.05^2 = 0.0025",
               r"\frac{0.01 \times 0.81}{0.01 \times 0.81 + 0.99 \times 0.0025} = \frac{0.0081}{0.010575} \approx 0.77"],
     "say": "From Parts 2 and 15: a condition affecting one percent of adults, and two independent tests, each detecting it ninety "
            "percent of the time with five percent false alarms. Both come back positive. How likely is the condition? Given the "
            "condition, both are positive with probability point eight one; without it, point oh oh two five. Bayes's rule gives "
            "point eight one times one percent, over that plus point oh oh two five times ninety-nine percent: about seventy-seven "
            "percent. One positive test alone would give only fifteen."},
    {"part": r"Parts 8 and 18", "color": DES,
     "q": r"A survey of $n = 4{,}948$ measures systolic pressure with SD 17 mm Hg; \ its design effect is 3.6. \ The 95\% margin of error, \ with and without the design?",
     "steps": [r"\text{SRS}: \ 1.96 \times 17 / \sqrt{4948} = 0.47", r"\text{design}: \ 0.47 \times \sqrt{3.6} = 0.90",
               r"n_{\text{eff}} = 4948 / 3.6 \approx 1{,}374"],
     "say": "From Parts 8 and 18: a survey of four thousand nine hundred and forty-eight people measures systolic pressure, with a "
            "standard deviation of seventeen, and a design effect of three point six. What's the margin of error? As a simple random "
            "sample, one point nine six times seventeen over the square root of n: point four seven. With the design, multiply by the "
            "square root of three point six: point nine oh, nearly double. The survey is worth about thirteen hundred and seventy "
            "random people."},
    {"part": r"Part 12", "color": SALT,
     "q": r"Usual intake $X$ has variance 1; \ one day's recall $W = X + U$ adds independent noise of variance 2. \ A true slope of 2.5 mm Hg per g: \ what slope does a regression on $W$ find?",
     "steps": [r"\lambda = \frac{\mathrm{Var}\,X}{\mathrm{Var}\,X + \mathrm{Var}\,U} = \frac{1}{3}",
               r"\hat\beta_W \to \lambda \beta = 2.5 / 3 \approx 0.83",
               r"\text{with } k \text{ recall days}: \ \lambda_k = \frac{1}{1 + 2/k}; \ \ k = 7: \ 0.78"],
     "say": "From Part 12: usual intake has variance one, and a single day's recall adds independent noise with variance two, "
            "roughly the proportions in NHANES. If the true slope is two point five, what does the regression on one day's recall "
            "find? The reliability lambda is one over one plus two, a third, so the slope shrinks to point eight three. Averaging k "
            "days divides the noise variance by k: with a week of recalls, lambda is point seven eight."},
    {"part": r"Parts 10 and 13", "color": HIT,
     "q": r"Plan a parallel trial: \ low vs high sodium, \ a difference of 2.3 g at 2.5 mm Hg per g, \ SD 15 within arms. \ How many per arm for 80\% power at the 5\% level?",
     "steps": [r"\Delta = 2.3 \times 2.5 = 5.75 \text{ mm Hg}",
               r"n = \frac{2 (z_{0.975} + z_{0.80})^2 \sigma^2}{\Delta^2} = \frac{2 (1.96 + 0.84)^2 \times 225}{5.75^2}",
               r"\approx 107 \text{ per arm}"],
     "say": "From Parts 10 and 13: plan a trial comparing low and high sodium diets, two point three grams apart, expecting two "
            "point five millimetres per gram, with a standard deviation of fifteen within each arm. How many people per arm for "
            "eighty percent power at the five percent level? The difference to detect is five point seven five. The sample size "
            "formula is two times one point nine six plus point eight four, squared, times the variance, over the difference "
            "squared: about a hundred and seven per arm. Our World trial, with two hundred per arm, had power to spare."},
    {"part": r"Parts 16 and 18", "color": DES,
     "q": r"NHANES's public design: \ 15 strata with 2 PSUs each. \ How many different Rao--Wu bootstrap replicates are there?",
     "steps": [r"\text{each stratum draws } n_h - 1 = 1 \text{ of its 2 PSUs}", r"2^{15} = 32{,}768 \text{ replicates in all}",
               r"\text{so 1,000 replicates sample this set; \ the SE has 15 df}"],
     "say": "From Parts 16 and 18: NHANES's public design has fifteen strata with two PSUs each. How many different Rao–Wu "
            "bootstrap replicates are possible? Each stratum draws n h minus one, that is one, of its two PSUs, so there are two to "
            "the fifteenth: thirty-two thousand seven hundred and sixty-eight. Our thousand replicates sample from that set, and "
            "however many we draw, the standard error carries only fifteen degrees of freedom."},
    {"part": r"Parts 10 and 19", "color": OBS,
     "q": r"Sixty-four analyses, \ each with a 5\% false-positive rate, \ if independent: \ the chance at least one is ``significant''? \ And with a Bonferroni correction?",
     "steps": [r"1 - 0.95^{64} \approx 0.96", r"\text{Bonferroni}: \ \alpha / 64 \approx 0.00078 \text{ each}: \ \le 0.05 \text{ overall}",
               r"\text{correlated analyses: \ fewer effective forks; \ ours: \ 0 of 64}"],
     "say": "From Parts 10 and 19: sixty-four analyses, each with a five percent false-positive rate. What is the chance that "
            "at least one comes out significant? If they were independent, it's one minus point nine five to the sixty-fourth: "
            "ninety-six percent. With a Bonferroni correction, each must reach a p-value of point oh oh oh seven eight, and the overall "
            "rate is at most five percent. Our sixty-four analyses are strongly correlated, which is why none of them was "
            "significant: they're closer to a handful of independent forks."},
]


class BScProblems(VoiceoverScene):
    def construct(self):
        self.card()
        for p in PROBLEMS:
            self.problem(p)
        self.close()

    def card(self):
        card = chapter_card(13, r"The BSc problem set", r"Stages I and II, \ in six problems", part=PART)
        with self.voiceover("Chapter thirteen. The bachelor's problem set: six problems that draw on the whole of the first two "
                            "stages, each solved on screen."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self, p):
        tag = label(p["part"], font_size=22, color=p["color"]).to_edge(UP, buff=0.4)
        q = label(p["q"], font_size=24)
        if q.width > 12.6:
            q = VGroup(*[label(s.strip(), font_size=24) for s in p["q"].split(r"\ ") if s.strip()])
            q.arrange(DOWN, buff=0.15)
        q.next_to(tag, DOWN, buff=0.4)
        if q.width > 12.6:
            q.width = 12.6
        steps = VGroup(*[MathTex(s, font_size=30) for s in p["steps"]]).arrange(DOWN, buff=0.4)
        for s in steps:
            if s.width > 12.4:
                s.width = 12.4
        steps.next_to(q, DOWN, buff=0.6)
        steps[-1].set_color(p["color"])
        text = p["say"]
        n = len(text)
        cut1, cut2 = text.find("?") + 1, int(n * 0.68)
        cut2 = text.find(" ", cut2)
        narr = text[:cut1] + " <bookmark mark='a'/>" + text[cut1:cut2] + " <bookmark mark='b'/>" + text[cut2:]
        with self.voiceover(narr) as vo:
            self.play(FadeIn(tag), FadeIn(q, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(steps[0], shift=RIGHT * 0.2))
            self.play(FadeIn(steps[1], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(steps[2], shift=RIGHT * 0.2))
        self.wait(1.0)
        self.clear_scene()

    def close(self):
        rows = fit_rows(VGroup(
            label(r"Bayes's rule; \ survey margins; \ attenuation; \ power; \ the bootstrap; \ multiplicity", font_size=24),
            label(r"each one appeared in this capstone", font_size=24, color=SALT),
            label(r"full solutions, \ and more problems, \ in the README", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Bayes's rule, a survey's margin of error, attenuation, power, the bootstrap and multiplicity: "
            "<bookmark mark='b'/> every one of them turned up in this one analysis. <bookmark mark='c'/> Full solutions, with "
            "more detail, are in the README."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
