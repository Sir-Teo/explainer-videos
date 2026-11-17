from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.relative_age()
        self.justice()
        self.screening()

    def card(self):
        card = chapter_card(14, r"In practice: \ ages and rules", r"Where does a society write age into its rules?",
                            lit={2005: r"\emph{Roper v. Simmons}", 2014: r"school start times",
                                 2018: r"Layton et al."}, part=PART, scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: ages and rules."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def relative_age(self):
        head = heading(r"The youngest in the class")
        A = axes([-0.6, 1.6], [0, 100], x_length=4.2, y_length=3.8, xticks=None, yticks=[0, 25, 50, 75, 100],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"ADHD diagnoses per 10{,}000", center=[-4.0, -0.4, 0],
                 font_size=15)
        b = bars(A.ax, [0, 1], [85.1, 63.6], [LOST, AGE], width=0.6)
        nm = VGroup(label(r"born in August", font_size=17, color=LOST).next_to(A.ax.c2p(0, 0), DOWN, buff=0.2),
                    label(r"born in September", font_size=17, color=AGE).next_to(A.ax.c2p(1, 0), DOWN, buff=0.2))
        vals = VGroup(label(r"85.1", font_size=18, color=LOST).next_to(b[0], UP, buff=0.08),
                      label(r"63.6", font_size=18, color=AGE).next_to(b[1], UP, buff=0.08))
        rows = rows_of([
            (r"Timothy Layton and colleagues, \ 2018: \ insurance records of more than 407{,}000 American children "
             r"born 2007 to 2009", WHITE),
            (r"in states where children must be 5 by September 1 to start school, \ those born in August are the "
             r"youngest in their class, \ those born in September the oldest", PERIOD),
            (r"the August-born were diagnosed with ADHD about a third more often; \ in states without that "
             r"cutoff, \ no clear difference", LOST),
            (r"an eleven-month gap in age, \ read as a disorder: \ a judgement against the class, \ not against "
             r"the child's age", YOU),
        ], 7.4, 21, 0.36).move_to([2.6, -0.3, 0])
        tag = published_tag(r"Layton et al.\ (2018)")
        with self.voiceover(
            "Societies write age into rules, and the rules interact with development. <bookmark mark='a'/> In 2018 "
            "Timothy Layton and colleagues used the insurance records of more than four hundred thousand American "
            "children born from 2007 to 2009. <bookmark mark='b'/> In states where children must be five by "
            "September the first to start school, those born in August are the youngest in their class, and those "
            "born in September the oldest. <bookmark mark='c'/> The August-born were diagnosed with ADHD about a "
            "third more often: eighty-five per ten thousand, against sixty-four. In states without that cutoff there "
            "was no clear difference. <bookmark mark='d'/> An eleven-month gap in age was being read as a disorder: "
            "behaviour judged against the class, not against the child's own age. The cutoff makes it a natural "
            "experiment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(nm), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(vals), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def justice(self):
        head = heading(r"Adolescents in court")
        steps = VGroup(*[word_chip(t, color=c, font_size=21, width=4.0) for t, c in (
            (r"2005: \ \emph{Roper v. Simmons}", AGE), (r"2010: \ \emph{Graham v. Florida}", PERIOD),
            (r"2012: \ \emph{Miller v. Alabama}", COHORT))]).arrange(RIGHT, buff=0.3).move_to([0, 1.8, 0])
        rows = rows_of([
            (r"the US Supreme Court barred the death penalty for crimes committed under 18, \ then life without "
             r"parole for juveniles who had not killed, \ then mandatory life without parole for any juvenile", WHITE),
            (r"the American Psychological Association and medical groups filed briefs on adolescent development: "
             r"\ peers, \ reward seeking, \ and control still maturing", AGE),
            (r"the Court's majority in \emph{Roper} drew on those arguments: \ adolescents are less culpable, \ "
             r"and more capable of change", GOOD),
            (r"the hazard: \ group averages used about individuals; \ chapter six's caution, \ in a courtroom", LOST),
        ], 12.4, 23, 0.36).move_to([0, -0.9, 0])
        with self.voiceover(
            "The lifespan research of chapter six went to court. <bookmark mark='a'/> In three cases, in 2005, "
            "2010 and 2012, the United States Supreme Court barred the death penalty for crimes committed under "
            "eighteen, then life without parole for juveniles who hadn't killed, then mandatory life without parole "
            "for any juvenile. <bookmark mark='b'/> The American Psychological Association and medical groups filed "
            "briefs on adolescent development: the pull of peers, heightened reward seeking, and control still "
            "maturing. <bookmark mark='c'/> The Court's majority in the first case drew on those arguments: "
            "adolescents are less culpable than adults, and more capable of change. <bookmark mark='d'/> The hazard "
            "is the one from chapter six: group averages used to judge individuals."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.3))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def screening(self):
        head = heading(r"Later life: \ screening, \ driving and work")
        rows = rows_of([
            (r"short cognitive screens in the clinic: \ a score against a threshold, \ with Part 12's hits and "
             r"false alarms; \ norms must match age and education, \ or the poorly schooled are flagged", AGE),
            (r"a positive screen starts an assessment, \ not a diagnosis; \ the best evidence is change against "
             r"the person's own past", GOOD),
            (r"driving and work: \ some rules use a birthday, \ such as the international upper age of 65 for "
             r"airline pilots; \ others test function, \ which ageing affects very unequally", PERIOD),
            (r"chapter two's lesson for policy: \ average curves are made of very different lives", YOU),
        ], 12.4, 24, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "At the other end of life, the same issues return. <bookmark mark='a'/> Short cognitive screens in "
            "the clinic set a score against a threshold, with Part 12's hits and false alarms. The norms must match "
            "age and education, or people with little schooling are flagged wrongly. <bookmark mark='b'/> A positive "
            "screen starts an assessment, not a diagnosis, and the best evidence is change against the person's own "
            "past. <bookmark mark='c'/> For driving and work, some rules use a birthday, such as the international "
            "upper age of sixty-five for airline pilots. Others test function, which ageing affects very unequally. "
            "<bookmark mark='d'/> That's chapter two's lesson for policy: average curves are made of very different "
            "lives."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
