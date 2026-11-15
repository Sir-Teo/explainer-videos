from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403

REL_COL = [LOST, SPEED, G]


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.near_cut()
        self.diagnosis()
        self.utility()
        self.impact()

    def card(self):
        card = chapter_card(14, r"In practice: \ cutoffs, \ clinics and hiring",
                            r"What happens when a decision hangs on a score?",
                            lit={1949: r"Brogden", 1971: r"\emph{Griggs}", 1978: r"four-fifths rule"}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: cutoffs, clinics and hiring."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def near_cut(self):
        d = load("practice")
        head = heading(r"Near a cutoff, \ the error decides")
        A = axes([63.5, 80.5], [0, 1.05], x_length=6.2, y_length=3.9, xticks=[64, 66, 68, 70, 72, 74, 76, 78, 80],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"true score", ylabel=r"chance of scoring below 70", center=[-3.0, -0.3, 0], font_size=15)
        cut = DashedLine(A.ax.c2p(70, 0), A.ax.c2p(70, 1.05), color=GREY_B, stroke_width=2)
        curves = VGroup(*[curve(A.ax, d["true"], d[f"below_{int(r * 100)}"], REL_COL[i], stroke_width=4)
                          for i, r in enumerate(d["rels"])])
        key = legend([(REL_COL[i], rf"reliability {r:.2f}") for i, r in enumerate(d["rels"])], font_size=16)
        key.move_to(A.ax.c2p(76.5, 0.85))
        rows = rows_of([
            (r"an observed score is the true score plus error, \ with the standard error of chapter six", WHITE),
            (rf"a person whose true score is 72 scores below 70 {pct(d['at72'][2])} of the time at reliability 0.95, "
             rf"\ {pct(d['at72'][0])} at 0.80", G),
            (rf"and someone at 68 scores 70 or more {pct(1 - d['at68'][2])} of the time", LOST),
            (rf"Truman Kelley, \ 1927: \ the best guess of the true score behind an observed 69 is pulled toward 100: "
             rf"\ {d['kelley69'][2]:.1f} at 0.95, \ {d['kelley69'][0]:.1f} at 0.80", MODEL),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{traits.below\_cut, \ kelley}")
        with self.voiceover(
            "Chapter six gave every score an error bar. Here's what it does at a cutoff. "
            "<bookmark mark='a'/> An observed score is the true score plus error, with the standard error from "
            "chapter six. <bookmark mark='b'/> A person whose true score is seventy-two scores below seventy "
            f"{spct(d['at72'][2])} of the time on a test with a reliability of 0.95, and {spct(d['at72'][0])} of "
            "the time at 0.80. Each curve is one test. <bookmark mark='c'/> And someone whose true score is "
            f"sixty-eight scores seventy or more {spct(1 - d['at68'][2])} of the time. Near the line, the error "
            "decides which side a person lands on. <bookmark mark='d'/> In 1927 Truman Kelley gave the correction. "
            "The best estimate of the true score behind an observed sixty-nine is pulled toward a hundred, by the "
            f"test's unreliability: {d['kelley69'][2]:.1f} at a reliability of 0.95, and {d['kelley69'][0]:.1f} at "
            "0.80. It's regression to the mean, from Part 2, applied to one person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(cut))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.4), FadeIn(key), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def diagnosis(self):
        head = heading(r"A diagnosis is more than a score")
        cols = VGroup()
        for t, body, c in (
            (r"A: \ intellect", r"deficits in reasoning, \ problem solving and learning, \ confirmed by clinical "
             r"assessment and standardized tests", G),
            (r"B: \ adaptive life", r"deficits in at least one of three domains, \ conceptual, \ social or "
             r"practical, \ in everyday independence", VERB),
            (r"C: \ onset", r"both beginning during the developmental period", COHORT)):
            cols.add(VGroup(word_chip(t, color=c, font_size=23, width=3.6), wrapped_label(body, 3.8, 21, WHITE))
                     .arrange(DOWN, buff=0.3))
        cols.arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"DSM-5, \ 2013: \ the full-scale IQ is no longer a criterion, \ and severity, \ from mild to profound, "
             r"\ is graded by adaptive functioning", WHITE),
            (r"Binet's purpose, \ restored: \ the score finds the children who need help; \ it does not decide "
             r"who they are", YOU),
        ], 12.4, 23, 0.36).move_to([0, -2.2, 0])
        with self.voiceover(
            "Clinics have learned the same lesson. <bookmark mark='a'/> In DSM-5, intellectual disability needs "
            "three things. Deficits in reasoning, problem solving and learning, confirmed by clinical assessment "
            "and standardized tests. <bookmark mark='b'/> Deficits in adaptive functioning, in at least one of three "
            "domains, conceptual, social or practical: how a person manages everyday independence. "
            "<bookmark mark='c'/> And both beginning during the developmental period. <bookmark mark='d'/> Since "
            "2013 the full-scale IQ is no longer itself a criterion, and severity, from mild to profound, is graded "
            "by adaptive functioning. <bookmark mark='e'/> That's Binet's purpose, restored. The score finds the "
            "children who need help. It doesn't decide who they are."
        ) as vo:
            self.play(FadeIn(head))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.1))
            for m, r in zip("de", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def utility(self):
        d = load("practice")
        g = d["gain_at"]
        head = heading(r"What a test is worth to an employer")
        A = axes([0, 1.0], [0, 1.4], x_length=6.0, y_length=3.9, xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                 yticks=[0, 0.4, 0.8, 1.2], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"share of applicants hired", ylabel=r"hires' mean performance (SD)", center=[-3.0, -0.3, 0],
                 font_size=15)
        c51 = curve(A.ax, d["ratio"], np.minimum(d["gain51"], 1.4), G, stroke_width=4)
        c31 = curve(A.ax, d["ratio"], np.minimum(d["gain31"], 1.4), VERB, stroke_width=4)
        key = legend([(G, r"validity .51 \ (1998)"), (VERB, r"validity .31 \ (2022)")], font_size=16)
        key.move_to(A.ax.c2p(0.68, 1.15))
        rows = rows_of([
            (r"Hubert Brogden, \ 1949: \ hire the top share on a test, \ and the hires' average performance, \ in "
             r"standard deviations, \ is the validity times their average standardized test score", MODEL),
            (rf"hire the top tenth: \ {g['0.51_0.1']:.2f} SD above an unscreened hire at validity .51, \ "
             rf"{g['0.31_0.1']:.2f} at .31", G),
            (rf"hire half: \ {g['0.51_0.5']:.2f} and {g['0.31_0.5']:.2f}", VERB),
            (r"value is linear in validity: \ so Sackett's correction cut the classic estimate of a test's worth by "
             r"about 40\%", YOU),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{traits.selection\_gain}")
        with self.voiceover(
            "Employers use tests because they're worth money. <bookmark mark='a'/> In 1949 Hubert Brogden showed "
            "why. Hire the top share of applicants on a test, and the hires' average performance, measured in "
            "standard deviations, is the test's validity times their average standardized score on the test. "
            "<bookmark mark='b'/> Hire the top tenth, and the hires perform "
            f"{g['0.51_0.1']:.2f} of a standard deviation above an unscreened hire at a validity of point five one, "
            f"and {g['0.31_0.1']:.2f} at point three one. <bookmark mark='c'/> Hire half the applicants, and it's "
            f"{g['0.51_0.5']:.2f} and {g['0.31_0.5']:.2f}. <bookmark mark='d'/> The value is linear in the "
            "validity. So when Sackett and colleagues corrected the corrections, the classic estimate of a test's "
            "worth fell by about forty percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c51), Create(c31), FadeIn(key), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def impact(self):
        d = load("practice")
        ia = d["impact_at"]
        head = heading(r"The selection-rate ratio, \ and the four-fifths rule")
        A = axes([0, 1.0], [0, 1.0], x_length=6.0, y_length=3.9, xticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                 yticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"share of the higher-scoring group selected", ylabel=r"ratio of selection rates",
                 center=[-3.0, -0.3, 0], font_size=15)
        line = DashedLine(A.ax.c2p(0, 0.8), A.ax.c2p(1.0, 0.8), color=LOST, stroke_width=3)
        lt = label(r"four-fifths", font_size=16, color=LOST).next_to(A.ax.c2p(0.02, 0.8), UP, buff=0.08,
                                                                     aligned_edge=LEFT)
        c = curve(A.ax, d["ratio"], d["impact"], G, stroke_width=4)
        rows = rows_of([
            (r"\emph{Griggs v.\ Duke Power}, \ 1971: \ the US Supreme Court held that a diploma and aptitude-test "
             r"requirement that excluded Black workers disproportionately was unlawful unless shown to be related to "
             r"the job", WHITE),
            (r"the Uniform Guidelines, \ 1978: \ a group's selection rate below four-fifths of the highest group's is "
             r"generally taken as evidence of adverse impact; \ courts warn against applying it mechanically", VERB),
            (rf"Psyche: \ two groups half a standard deviation apart on a test; \ select the top tenth of the higher "
             rf"group and the ratio is {ia['0.1']:.2f}; \ half, \ {ia['0.5']:.2f}", G),
            (r"the more selective the cut, \ the larger the impact from the same gap: \ the tension between "
             r"validity and diversity is arithmetic, \ and so is the case for using several valid measures", YOU),
        ], 5.6, 19, 0.3).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{traits.impact\_ratio}")
        with self.voiceover(
            "And the law asks a second question: whom does the test exclude? <bookmark mark='a'/> In 1971, in "
            "Griggs versus Duke Power, the United States Supreme Court held that a diploma and aptitude-test "
            "requirement that excluded Black workers disproportionately was unlawful unless the employer showed it "
            "was related to the job. <bookmark mark='b'/> The Uniform Guidelines of 1978 gave a rule of thumb: a "
            "group's selection rate below four-fifths of the highest group's rate is generally taken as evidence of "
            "adverse impact, though courts warn against applying it mechanically. <bookmark mark='c'/> Psyche "
            "takes two groups whose averages differ by half a standard deviation on a test. Select the top tenth "
            f"of the higher group, and the ratio of selection rates is {ia['0.1']:.2f}. Select half, and it's "
            f"{ia['0.5']:.2f}. <bookmark mark='d'/> The more selective the cut, the larger the impact from the same "
            "gap. The tension between validity and diversity is arithmetic, and so is the case for combining "
            "several valid measures rather than one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(lt), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
