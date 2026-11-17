from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Fairness(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Fairness", r"Can a valid test be unfair?", scale=("society",))
        self.impact()
        self.law()
        self.frontier()

    def impact(self):
        d = load("impact")
        head = heading(r"Adverse impact")
        A = axes([-0.05, 1.05], [0, 1.05], x_length=5.6, y_length=3.0, xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                 yticks=[0, 0.5, 0.8, 1.0], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"group difference on the predictor (SD)", ylabel=r"impact ratio", center=[-3.3, 0.3, 0],
                 font_size=12)
        c = curve(A.ax, d["d"], d["ratio"], AUTH, stroke_width=4)
        h = DashedLine(A.ax.c2p(-0.05, 0.8), A.ax.c2p(1.05, 0.8), color=GREY_B)
        hl = label(r"four-fifths rule", font_size=13, color=GREY_B).next_to(A.ax.c2p(1.0, 0.8), UP, buff=0.05)
        k = int(np.where(np.isclose(d["d"], 0.4))[0][0])
        rows = rows_of([
            (r"two groups of applicants, \ a top-down cut that hires 20\% overall; \ the impact ratio is the lower "
             r"group's selection rate over the higher's", WHITE),
            (r"US guidelines flag a ratio below 0.8: \ the four-fifths rule, \ a rule of thumb for scrutiny, \ not a "
             r"verdict", MODEL),
            (rf"a difference of just 0.4 SD gives {100 * d['min'][k]:.0f}\% against {100 * d['maj'][k]:.0f}\% hired: \ "
             rf"a ratio of {d['ratio'][k]:.2f}", AUTH),
            (r"selective cuts magnify small mean differences: \ the tails do the work (Part 32)", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.adverse\_impact}, \ 30\% of applicants in the lower-scoring group")
        with self.voiceover(
            "Can a valid test be unfair? <bookmark mark='a'/> Take two groups of applicants and a cut that hires a "
            "fifth overall. The impact ratio is the lower-scoring group's selection rate over the other's. "
            "<bookmark mark='b'/> American guidelines flag a ratio below zero point eight, the four-fifths rule. It's "
            "a trigger for scrutiny, not a verdict. <bookmark mark='c'/> A difference of just zero point four "
            "standard deviations gives thirteen percent hired against twenty-three, a ratio of about zero point five "
            "five. <bookmark mark='d'/> Selective cuts magnify small differences in means, because the tails do the "
            "work, as Part 32 showed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(h), FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(c))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def law(self):
        rows_section(self, r"Griggs and after", [
            (r"1971: \ in \emph{Griggs v. Duke Power}, \ the US Supreme Court ruled against a diploma requirement and "
             r"aptitude tests that excluded Black workers and were not shown to relate to the jobs", WHITE),
            (r"disparate impact: \ a practice with adverse impact must be shown to be job-related, \ and a less "
             r"discriminatory alternative can win", MODEL),
            (r"differential prediction: \ does the same score predict the same performance in each group? \ studies "
             r"mostly find similar slopes, \ and intercept differences that shrink with better criteria", PERSON),
            (r"a test can be equally valid for everyone and still produce adverse impact: \ fairness has several "
             r"definitions, \ and they conflict (Part 60)", YOU),
        ], "The law entered in 1971. <bookmark mark='a'/> In Griggs versus Duke Power, the US Supreme Court ruled "
           "against a diploma requirement and aptitude tests that excluded Black workers and weren't shown to relate "
           "to the jobs. <bookmark mark='b'/> That's disparate impact: a practice with adverse impact must be shown "
           "to be job-related, and a less discriminatory alternative can win. <bookmark mark='c'/> Psychologists "
           "also ask about differential prediction: does the same score predict the same performance in each group? "
           "Studies mostly find similar slopes, and differences in intercepts that shrink with better criteria. "
           "<bookmark mark='d'/> So a test can be equally valid for everyone and still produce adverse impact. "
           "Fairness has several definitions, and they conflict. Part 60 returns to that.")

    def frontier(self):
        d = load("frontier")
        head = heading(r"The validity-diversity frontier")
        A = axes([0.25, 0.7], [0.28, 0.48], x_length=5.4, y_length=3.2, xticks=[0.3, 0.4, 0.5, 0.6],
                 yticks=[0.3, 0.35, 0.4, 0.45], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.2f}",
                 xlabel=r"impact ratio", ylabel=r"validity", center=[-3.3, 0.3, 0], font_size=12)
        c = curve(A.ax, d["impact"], d["validity"], MODEL, stroke_width=4)
        ends = VGroup(Dot(A.ax.c2p(d["impact"][0], d["validity"][0]), color=GOOD, radius=0.08),
                      Dot(A.ax.c2p(d["impact"][-1], d["validity"][-1]), color=AUTH, radius=0.08))
        k = int(np.argmax(d["validity"]))
        best = Dot(A.ax.c2p(d["impact"][k], d["validity"][k]), color=PERSON, radius=0.09)
        rows = rows_of([
            (r"two predictors: \ an ability test (validity 0.31, \ group difference 0.8 SD) and a structured "
             r"interview (0.42, \ 0.3 SD), \ correlated 0.3 (illustrative)", WHITE),
            (rf"weight them in every proportion: \ the interview alone gives validity {d['validity'][0]:.2f} and "
             rf"impact ratio {d['impact'][0]:.2f}; \ the test alone {d['validity'][-1]:.2f} and {d['impact'][-1]:.2f}",
             GOOD),
            (rf"the most valid mix ({d['validity'][k]:.2f}) gives {d['impact'][k]:.2f}: \ a trade-off, \ chosen by "
             rf"an organization's values, \ not by the data", PERSON),
            (r"after 2022 the trade-off is gentler: \ the most valid predictors are no longer the ones with the "
             r"largest group differences", YOU),
        ], 6.0, 18, 0.34).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.frontier}, \ illustrative inputs")
        with self.voiceover(
            "Organizations can choose where to stand. <bookmark mark='a'/> Take two predictors: an ability test, with "
            "validity zero point three one and a group difference of zero point eight standard deviations, and a "
            "structured interview, with zero point four two and zero point three. These inputs are illustrative. "
            "<bookmark mark='b'/> Weight them in every proportion. The interview alone gives the higher impact ratio, "
            "and here also the higher validity; the test alone gives the lowest of both. <bookmark mark='c'/> The "
            "most valid mix gives an impact ratio of about zero point four two. Where to stand on the curve is a "
            "trade-off chosen by an organization's values, not by the data. <bookmark mark='d'/> And after the 2022 "
            "revision the trade-off is gentler, because the most valid predictors are no longer the ones with the "
            "largest group differences."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(ends))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(best, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
