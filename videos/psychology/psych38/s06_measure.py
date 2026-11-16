from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Measure(VoiceoverScene):
    def construct(self):
        self.card()
        self.translation()
        self.reference()

    def card(self):
        card = chapter_card(5, r"Measuring across cultures", r"Can the same question mean different things?",
                            lit={2002: r"Heine et al."}, part=PART, scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter five. Measuring across cultures."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def translation(self):
        head = heading(r"Four ways a comparison fails")
        items = [
            (r"translation", r"a word carries different shades; \ translate, \ translate back, \ and check that "
                             r"the item means the same", WEST),
            (r"invariance", r"the items must relate to the trait in the same way in each group, \ or a difference "
                            r"in scores is not a difference in the trait (Part 44 tests this)", MODEL),
            (r"reference groups", r"people rate themselves against the people around them, \ and those people "
                                  r"differ", WORLD),
            (r"convenience", r"students in one city are not their country, \ and online samples are not their "
                             r"population", AUTH),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=3.2), wrapped_label(how, 8.6, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "Comparing cultures means asking the same question in different places, and that can fail in four "
            "ways. <bookmark mark='a'/> Translation: a word carries different shades. The standard check is to "
            "translate, translate back, and confirm the item means the same. <bookmark mark='b'/> Invariance: the "
            "items have to relate to the trait in the same way in each group, or a difference in scores isn't a "
            "difference in the trait. Part 44 shows how to test it. <bookmark mark='c'/> Reference groups: people "
            "rate themselves against the people around them, and those people differ. <bookmark mark='d'/> And "
            "convenience: students in one city aren't their country, and an online sample isn't its population."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def reference(self):
        d = load("refgroup")
        head = heading(r"The reference-group effect")
        A = axes([0.4, 7.6], [0, 0.5], x_length=4.6, y_length=2.1, xticks=[1, 2, 3, 4, 5, 6, 7], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"``I am hard-working'', \ 1 to 7", center=[-3.6, 1.1, 0],
                 font_size=14)
        xs = np.arange(1, 8)
        ra = bars(A.ax, xs - 0.18, d["report_a"], WEST, width=0.34)
        rb = bars(A.ax, xs + 0.18, d["report_b"], WORLD, width=0.34)
        B = axes([-4, 5], [0, 0.07], x_length=4.6, y_length=1.6, xticks=None, yticks=None,
                 xlabel=r"behaviour: \ hours of work observed", center=[-3.6, -2.0, 0], font_size=14)
        mids = (np.linspace(-4, 5, 37)[:-1] + np.linspace(-4, 5, 37)[1:]) / 2
        ba = bars(B.ax, mids, d["beh_a"], WEST, width=0.22, opacity=0.6)
        bb = bars(B.ax, mids, d["beh_b"], WORLD, width=0.22, opacity=0.6)
        key = legend([(WEST, r"culture A"), (WORLD, r"culture B")], font_size=14).move_to([-1.6, 2.3, 0])
        rows = rows_of([
            (r"Psyche: \ two cultures, \ B higher than A on a trait by 0.8 standard deviations", WHITE),
            (rf"asked to rate themselves, \ each person compares with the people around them: \ the means are "
             rf"{d['mean_report'][0]:.2f} and {d['mean_report'][1]:.2f}, \ a gap of {abs(d['gap_report']):.2f} SD",
             WORLD),
            (rf"a behavioural measure, \ noisier but absolute, \ shows the gap: \ {d['gap_behaviour']:.2f} SD", GOOD),
            (r"Heine, \ Lehman, \ Peng and Greenholtz, \ 2002: \ experts agreed East Asians were more collectivist, \ "
             r"yet self-reports did not show it; \ changing the reference group brought the difference back", YOU),
        ], 6.0, 19, 0.34).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{culture.reference\_group}; \ Heine et al.\ (2002)")
        with self.voiceover(
            "The reference-group effect can hide a real difference completely. <bookmark mark='a'/> In Psyche, two "
            "cultures differ on a trait, say hard work, by eight tenths of a standard deviation. "
            "<bookmark mark='b'/> Asked to rate themselves from one to seven, each person compares themselves with "
            "the people around them. In a hard-working culture, average looks hard-working. So the two means come "
            f"out the same: {d['mean_report'][0]:.1f} and {d['mean_report'][1]:.1f}. <bookmark mark='c'/> A "
            "behavioural measure, noisier but absolute, shows the gap. <bookmark mark='d'/> In 2002 Steven Heine and "
            "colleagues showed the effect in people. Experts agreed that East Asians were more collectivist than "
            "North Americans, yet self-reports didn't show it. When the reference group was changed, the difference "
            "came back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[GrowFromEdge(x, DOWN) for x in ra], *[GrowFromEdge(x, DOWN) for x in rb])
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(B), *[GrowFromEdge(x, DOWN) for x in ba],
                      *[GrowFromEdge(x, DOWN) for x in bb])
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
