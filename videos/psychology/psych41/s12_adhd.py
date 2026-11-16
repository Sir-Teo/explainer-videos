from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Adhd(VoiceoverScene):
    def construct(self):
        self.card()
        self.what()
        self.age()
        self.mta()

    def card(self):
        card = chapter_card(11, r"ADHD", r"What is it, \ and what do stimulants do?",
                            lit={1999: r"MTA", 2018: r"Layton et al."}, part=PART, scale=("person", "society"),
                            marr=("what",))
        with self.voiceover("Chapter eleven. ADHD."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def what(self):
        head = heading(r"Attention-deficit hyperactivity disorder")
        rows = rows_of([
            (r"two clusters: \ inattention, \ and hyperactivity with impulsivity, \ beginning in childhood and "
             r"impairing life in more than one setting", WHITE),
            (r"a dimension, \ like most of Part 39's: \ the diagnosis is a line drawn across a continuum", MODEL),
            (r"Faraone and Larsson, \ 2019: \ twin studies put heritability near 0.74, \ again from many genes of "
             r"small effect", SYMP),
            (r"it often persists into adulthood, \ though symptoms change: \ restlessness becomes inner, \ and "
             r"disorganization matters more", PERSON),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = published_tag(r"Faraone \& Larsson (2019)")
        with self.voiceover(
            "ADHD, attention-deficit hyperactivity disorder. <bookmark mark='a'/> It has two clusters of symptoms: "
            "inattention, and hyperactivity with impulsivity, beginning in childhood and impairing life in more than "
            "one setting. <bookmark mark='b'/> Like most of Part 39's diagnoses, it's a dimension, with a line drawn "
            "across it. <bookmark mark='c'/> In 2019 Stephen Faraone and Henrik Larsson reviewed the twin studies, "
            "which put heritability near seventy-four percent, again from many genes of small effect. "
            "<bookmark mark='d'/> It often persists into adulthood, though the symptoms change. Restlessness turns "
            "inward, and disorganization matters more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def age(self):
        head = heading(r"The youngest in the class")
        A = axes([0.3, 2.7], [0, 100], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"diagnoses per 10{,}000", center=[-3.6, 0.5, 0], font_size=13)
        b = bars(A.ax, [1, 2], [63.6, 85.1], [GOOD, AUTH], width=0.6)
        names = VGroup(label(r"born in September: \ oldest", font_size=13, color=GOOD).next_to(A.ax.c2p(1, 0), DOWN,
                                                                                                buff=0.15),
                       label(r"born in August: \ youngest", font_size=13, color=AUTH).next_to(A.ax.c2p(2, 0), DOWN,
                                                                                              buff=0.15))
        rows = rows_of([
            (r"Layton and colleagues, \ 2018: \ in US states with a 1 September school cut-off, \ children born in "
             r"August are the youngest in their class", WHITE),
            (r"they were diagnosed with ADHD about a third more often than children born in September", AUTH),
            (r"a few months of age are read as a disorder: \ the line across the continuum is drawn relative to "
             r"classmates", MODEL),
            (r"a natural experiment: \ birth month is close to random, \ so the comparison is close to causal", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Layton et al.\ (2018)")
        with self.voiceover(
            "Where the line falls depends on the comparison. <bookmark mark='a'/> In 2018 Timothy Layton and "
            "colleagues used American insurance records. In states with a first of September school cut-off, "
            "children born in August are the youngest in their class. <bookmark mark='b'/> They were diagnosed with "
            "ADHD about a third more often than children born in September. <bookmark mark='c'/> A few months of age "
            "are being read as a disorder. The line across the continuum is drawn relative to classmates. "
            "<bookmark mark='d'/> And it's a natural experiment. Birth month is close to random, so the comparison is "
            "close to causal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def mta(self):
        head = heading(r"The largest trial")
        A = axes([0.3, 2.7], [0, 1.1], x_length=4.6, y_length=3.0, xticks=None, yticks=None,
                 ylabel=r"advantage of medication", center=[-3.6, 0.5, 0], font_size=13)
        b = bars(A.ax, [1, 2], [0.9, 0.05], [GOOD, GREY_B], width=0.6)
        names = VGroup(label(r"14 months", font_size=14, color=GOOD).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15),
                       label(r"3 years", font_size=14, color=GREY_B).next_to(A.ax.c2p(2, 0), DOWN, buff=0.15))
        lm = label(r"schematic", font_size=13, color=GREY_B).next_to(names, DOWN, buff=0.2)
        rows = rows_of([
            (r"the MTA trial, \ 1999: \ 579 children assigned to medication management, \ intensive behavioural "
             r"treatment, \ both, \ or usual community care", WHITE),
            (r"at 14 months, \ carefully managed medication reduced the core symptoms most", GOOD),
            (r"Jensen and colleagues, \ 2007: \ at three years, \ the groups no longer differed; \ many had changed "
             r"treatment by then", GREY_A),
            (r"stimulants work in the short term, \ in trial after trial; \ what they do over years is far less "
             r"certain", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"MTA Cooperative Group (1999); \ Jensen et al.\ (2007)")
        with self.voiceover(
            "What do stimulants do? <bookmark mark='a'/> The largest trial, the MTA study of 1999, assigned five "
            "hundred and seventy-nine children to carefully managed medication, intensive behavioural treatment, "
            "both, or usual community care. <bookmark mark='b'/> At fourteen months, managed medication reduced the "
            "core symptoms most. <bookmark mark='c'/> But at three years, the groups no longer differed, and many "
            "children had changed treatment by then. <bookmark mark='d'/> Stimulants work in the short term, in "
            "trial after trial. What they do over years is far less certain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
