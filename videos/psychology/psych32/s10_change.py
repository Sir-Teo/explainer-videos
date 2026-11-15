from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Change(VoiceoverScene):
    def construct(self):
        self.card()
        self.heritability()
        self.schooling()
        self.flynn()

    def card(self):
        card = chapter_card(9, r"Genes, \ schools and generations", r"How fixed is a score?",
                            lit={1984: r"Flynn", 2010: r"Haworth et al.", 2018: r"Ritchie \& Tucker-Drob"},
                            part=PART, scale=("gene", "person", "society"), marr=("what",))
        with self.voiceover("Chapter nine. Genes, schools and generations."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def heritability(self):
        head = heading(r"Heritability rises with age")
        A = axes([7, 19], [0, 0.8], x_length=5.6, y_length=3.8, xticks=[9, 12, 17], yticks=[0, 0.2, 0.4, 0.6, 0.8],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"age", ylabel=r"heritability",
                 center=[-3.0, -0.3, 0], font_size=15)
        b = bars(A.ax, [9, 12, 17], [0.41, 0.55, 0.66], G, width=1.6)
        vals = VGroup(*[label(t, font_size=18, color=G).next_to(b[i], UP, buff=0.08)
                        for i, t in enumerate((r"41\%", r"55\%", r"66\%"))])
        rows = rows_of([
            (r"Claire Haworth and colleagues, \ 2010: \ about 11{,}000 pairs of twins in six studies, \ four "
             r"countries", WHITE),
            (r"the heritability of general cognitive ability: \ 41\% at 9, \ 55\% at 12, \ 66\% at 17", G),
            (r"one reading: \ as children grow up, \ they increasingly choose and shape their own environments, \ "
             r"partly by their genes \ (Part 9's gene--environment correlation)", VERB),
            (r"and Part 9's warning: \ heritability describes variation in one population and environment; \ it "
             r"does not say a trait cannot change", LOST),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = published_tag(r"Haworth et al.\ (2010)")
        with self.voiceover(
            "How fixed is a score? Start with genes. <bookmark mark='a'/> In 2010 Claire Haworth and colleagues "
            "pooled about eleven thousand pairs of twins from six studies in four countries. "
            "<bookmark mark='b'/> The heritability of general cognitive ability was forty-one percent at nine, "
            "fifty-five percent at twelve, and sixty-six percent at seventeen. It rises with age. "
            "<bookmark mark='c'/> One reading is that as children grow up they increasingly choose and shape their "
            "own environments, partly according to their genes, Part 9's gene-environment correlation. "
            "<bookmark mark='d'/> And Part 9's warning applies: heritability describes variation in one population "
            "in one range of environments. It doesn't say a trait can't change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(vals), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def schooling(self):
        head = heading(r"A year of school")
        A = axes([0, 6], [-0.5, 2.5], x_length=6.0, y_length=2.6, xticks=[0, 1, 2, 3, 4, 5, 6], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"IQ points per extra year of education", center=[-2.6, 0.8, 0],
                 font_size=15)
        rng_bar = Line(A.ax.c2p(1.197, 1.0), A.ax.c2p(5.229, 1.0), color=G, stroke_width=10)
        ends = VGroup(label(r"1.2", font_size=17, color=G).next_to(A.ax.c2p(1.197, 1.0), UP, buff=0.15),
                      label(r"5.2", font_size=17, color=G).next_to(A.ax.c2p(5.229, 1.0), UP, buff=0.15),
                      label(r"range across the three designs", font_size=16, color=GREY_A)
                      .next_to(A.ax.c2p(1.9, 1.0), DOWN, buff=0.25))
        dots = VGroup(rng_bar, ends)
        avg = VGroup(DashedLine(A.ax.c2p(3.394, -0.5), A.ax.c2p(3.394, 2.5), color=GOOD, stroke_width=3),
                     label(r"average 3.4", font_size=16, color=GOOD).next_to(A.ax.c2p(3.394, 2.5), RIGHT, buff=0.1))
        rows = rows_of([
            (r"Stuart Ritchie and Elliot Tucker-Drob, \ 2018: \ 142 effect sizes from 42 data sets, \ more than "
             r"600{,}000 people, \ three kinds of quasi-experiment", WHITE),
            (r"each extra year of education raised scores by about 1 to 5 points, \ depending on the design; \ about "
             r"3.4 on average", G),
            (r"the effects lasted into later life, \ and appeared on every broad kind of ability tested", GOOD),
            (r"whether schooling raises $g$ itself, \ or the skills the tests sample, \ is open", YOU),
        ], 12.4, 22, 0.34).move_to([0, -2.0, 0])
        tag = published_tag(r"Ritchie \& Tucker-Drob (2018)")
        with self.voiceover(
            "Now environments. <bookmark mark='a'/> In 2018 Stuart Ritchie and Elliot Tucker-Drob pooled a hundred "
            "and forty-two effect sizes from forty-two data sets and more than six hundred thousand people, using "
            "three kinds of quasi-experiment: studies that control for earlier IQ, changes in school-leaving laws, "
            "and school-entry age cutoffs. <bookmark mark='b'/> Each extra year of education raised scores by about "
            "one to five points, depending on the design, and about three and a half on average. "
            "<bookmark mark='c'/> The effects lasted into later life, and appeared on every broad kind of ability "
            "they looked at. <bookmark mark='d'/> Whether schooling raises g itself, or the skills that the tests "
            "sample, is still open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), FadeIn(avg), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def flynn(self):
        head = heading(r"Generations: \ the Flynn effect, \ again")
        rows = rows_of([
            (r"James Flynn, \ 1984: \ every American norming sample from 1932 to 1978 set a higher standard than "
             r"the one before: \ 13.8 points in 46 years", WHITE),
            (r"Flynn, \ 1987: \ fourteen nations, \ gains of 5 to 25 points in a generation, \ largest on "
             r"reasoning tests like Raven's", G),
            (r"Part 31: \ about 2.8 points a decade across 31 countries, \ and a reversal within Norwegian "
             r"families", COHORT),
            (r"Jelte Wicherts and colleagues, \ 2004: \ the gains are not measurement-invariant: \ the tests did "
             r"not measure the same thing in the same way across cohorts", VERB),
            (r"high heritability within generations, \ large gains between them: \ the two are compatible, \ which "
             r"is Part 9's lesson in numbers", YOU),
        ], 12.4, 22, 0.32).move_to([0, -1.55, 0])
        A = axes([1928, 1982], [98, 116], x_length=6.4, y_length=1.9, xticks=[1932, 1978], yticks=[100, 113.8],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", ylabel=r"mean IQ on 1932 norms",
                 center=[0.3, 1.75, 0], font_size=14)
        rise = Line(A.ax.c2p(1932, 100), A.ax.c2p(1978, 113.8), color=COHORT, stroke_width=5)
        ends = VGroup(Dot(A.ax.c2p(1932, 100), color=COHORT), Dot(A.ax.c2p(1978, 113.8), color=COHORT),
                      label(r"13.8 points in 46 years: \ about 0.3 a year", font_size=17, color=COHORT)
                      .next_to(A.ax.c2p(1957, 101.5), RIGHT, buff=0.3))
        tag = published_tag(r"Flynn (1984); \ Flynn (1987); \ Wicherts et al.\ (2004)")
        with self.voiceover(
            "And between generations. <bookmark mark='a'/> In 1984 James Flynn showed that every American norming "
            "sample from 1932 to 1978 had set a higher standard than the one before: 13.8 points in forty-six years. "
            "<bookmark mark='b'/> In 1987 he found gains of five to twenty-five points in a single generation in "
            "fourteen nations, largest on reasoning tests like Raven's. <bookmark mark='c'/> Part 31 met the "
            "pooled rate, about 2.8 points a decade across thirty-one countries, and its reversal within Norwegian "
            "families. <bookmark mark='d'/> In 2004 Jelte Wicherts and colleagues showed that the gains are not "
            "measurement-invariant: the tests didn't measure the same thing in the same way across cohorts, so the "
            "gains can't simply be read as more g. <bookmark mark='e'/> High heritability within generations and "
            "large gains between them are compatible. That's Part 9's lesson, in numbers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(rise), FadeIn(ends), FadeIn(rows[0]))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
