from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403


class Invariance(VoiceoverScene):
    def construct(self):
        self.card()
        self.ladder()
        self.schools()

    def card(self):
        card = chapter_card(7, r"Measurement invariance", r"Does the test mean the same thing in both groups?",
                            lit={1993: r"Meredith"}, part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter seven. Measurement invariance."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ladder(self):
        head = heading(r"Three rungs")
        data = (
            (r"configural", r"the same diagram in each group: \ the same tests load on the same factors", SYMP),
            (r"metric", r"the same loadings: \ a unit of the factor moves each test by the same amount; \ needed to "
                        r"compare correlations and regressions", MODEL),
            (r"scalar", r"the same intercepts too: \ people with the same factor score expect the same test score; \ "
                        r"needed to compare means", GOOD),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=19, width=2.8), wrapped_label(how, 9.0, 21, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.5, 0])
        foot = wrapped_label(r"Meredith, \ 1993: \ without scalar invariance, \ a difference in mean scores can be a "
                             r"difference in the test, \ not in the people; \ owed since Parts 32 and 38", 12.0, 21,
                             YOU).move_to([0, -2.3, 0])
        tag = published_tag(r"Meredith (1993)")
        with self.voiceover(
            "Before comparing two groups on a test, ask whether the test means the same thing in both. "
            "<bookmark mark='a'/> Configural invariance: the same diagram in each group, the same tests loading on "
            "the same factors. <bookmark mark='b'/> Metric invariance: the same loadings, so a unit of the factor moves "
            "each test by the same amount. That's needed to compare correlations and regressions. "
            "<bookmark mark='c'/> Scalar invariance: the same intercepts too, so people with the same factor score "
            "expect the same test score. That's needed to compare means. <bookmark mark='d'/> William Meredith "
            "formalized the ladder in 1993. Without the third rung, a difference in mean scores can be a difference "
            "in the test, not in the people. Parts 32 and 38 owed this chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def schools(self):
        d = load("invariance")
        head = heading(r"Two schools")
        levels = ("configural", "metric", "scalar")
        A = axes([0.3, 3.7], [0, 180], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 50, 100, 150],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"$\chi^2$", center=[-3.4, 0.5, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], [d[f"{lv}_T"] for lv in levels], [SYMP, MODEL, GOOD], width=0.6)
        names = VGroup(*[label(rf"{lv}, \ {d[f'{lv}_df']:.0f} df", font_size=12, color=GREY_A).next_to(
            A.ax.c2p(i + 1, 0), DOWN, buff=0.15) for i, lv in enumerate(levels)])
        dm = d["metric_T"] - d["configural_T"]
        ds = d["scalar_T"] - d["metric_T"]
        k = d["kappa"]
        rows = rows_of([
            (rf"Pasteur ({d['n_pasteur']:.0f} children) and Grant-White ({d['n_gw']:.0f}): \ the three-factor model in "
             rf"both", WHITE),
            (rf"equal loadings cost $\Delta\chi^2 = {dm:.1f}$ on 6 df: \ acceptable", MODEL),
            (rf"equal intercepts cost $\Delta\chi^2 = {ds:.1f}$ on 6 df: \ rejected; \ some tests are easier in one "
             rf"school for children of equal ability", AUTH),
            (rf"if scalar invariance is assumed anyway, \ Grant-White looks {k[1]:.2f} points higher on the verbal "
             rf"factor: \ a comparison the data do not license as it stands", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{sem.fit\_multigroup}; \ checked against lavaan")
        with self.voiceover(
            "Holzinger and Swineford's children came from two schools. <bookmark mark='a'/> Fit the three-factor model "
            "in both at once. <bookmark mark='b'/> Holding the loadings equal costs little: an acceptable change in "
            "chi-square. <bookmark mark='c'/> Holding the intercepts equal costs about forty: rejected. Some tests are "
            "easier in one school for children of the same ability. <bookmark mark='d'/> If scalar invariance is "
            "assumed anyway, Grant-White looks more than half a point higher on the verbal factor. It's a comparison "
            "the data don't license as it stands. These numbers match lavaan exactly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
