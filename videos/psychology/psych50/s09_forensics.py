from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Forensics(VoiceoverScene):
    def construct(self):
        self.card()
        self.grim()
        self.sprite()
        self.statcheck()

    def card(self):
        card = chapter_card(8, r"Forensic statistics", r"Can reported numbers be checked without the data?", lit=(),
                            part=PART, scale=("society",), marr=("how",))
        with self.voiceover("Chapter eight. Forensic statistics."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def grim(self):
        d = load("grim")
        head = heading(r"GRIM: \ granularity-related inconsistency of means")
        rows = VGroup()
        for m, n, ok in zip(d["means"], d["ns"], d["ok"]):
            rows.add(VGroup(label(rf"mean {m:.2f}, \ $n$ = {int(n)}", font_size=24, color=WHITE),
                            label(r"possible" if ok else r"impossible", font_size=24, color=GOOD if ok else AUTH))
                     .arrange(RIGHT, buff=0.6))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.4, 0.2, 0])
        text = rows_of([
            (r"Nick Brown and James Heathers, \ 2017: \ a mean of $n$ whole-number answers must be a multiple of "
             r"$1/n$, \ up to rounding", WHITE),
            (r"for small samples, \ many reported means cannot occur", MODEL),
            (r"they tested means in published articles and found many inconsistent; \ some led to corrections and "
             r"retractions", PERSON),
            (r"it needs only the mean, \ the sample size, \ and the scale", YOU),
        ], 6.2, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{meta.grim}")
        tag2 = published_tag(r"Brown \& Heathers (2017)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "The opening's test has a name. <bookmark mark='a'/> In 2017 Nick Brown and James Heathers called it "
            "GRIM: a mean of n whole-number answers must be a multiple of one over n, up to rounding. "
            "<bookmark mark='b'/> For small samples, many reported means simply can't occur. Here are five; two are "
            "impossible. <bookmark mark='c'/> They tested means in published articles and found many inconsistent, and "
            "some led to corrections and retractions. <bookmark mark='d'/> It needs only the mean, the sample size, "
            "and the scale."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3),
                      run_time=2.0)
            for m, r in zip("abcd", text):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def sprite(self):
        d = load("grim")
        head = heading(r"SPRITE: \ what samples could give these numbers?")
        s1 = np.asarray(d["sprite"]); s2 = np.asarray(d["sprite2"])
        A = axes([0.4, 7.6], [0, 9], x_length=4.6, y_length=2.6, xticks=list(range(1, 8)), yticks=[0, 4, 8],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"answer (1 to 7)", ylabel=r"people",
                 center=[-3.6, 0.6, 0], font_size=12)
        c1 = np.bincount(s1, minlength=8)[1:]
        c2 = np.bincount(s2, minlength=8)[1:]
        b1 = bars(A.ax, np.arange(1, 8) - 0.18, c1, MODEL, width=0.34)
        b2 = bars(A.ax, np.arange(1, 8) + 0.18, c2, PERSON, width=0.34)
        key = VGroup(label(r"mean 3.50, \ SD 1.50", font_size=13, color=MODEL),
                     label(r"mean 3.50, \ SD 1.00", font_size=13, color=PERSON)).arrange(RIGHT, buff=0.4)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Heathers and colleagues, \ 2018: \ from a reported mean, \ SD, \ sample size and scale, \ search for "
             r"samples that fit", WHITE),
            (r"Psyche's search finds a sample of 20 for each reported pair: \ the numbers are possible", MODEL),
            (r"if no sample fits, \ or the only ones that do are absurd (everyone answering 1 or 7), \ the numbers "
             r"deserve a question", AUTH),
            (r"a reconstruction is not the data: \ it shows what the data could have been", YOU),
        ], 6.2, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{meta.sprite}")
        tag2 = published_tag(r"Heathers et al.\ (2018)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "GRIM checks a mean. SPRITE checks a mean and a standard deviation together. <bookmark mark='a'/> James "
            "Heathers and colleagues proposed searching for samples that fit the reported mean, standard deviation, "
            "sample size and scale. <bookmark mark='b'/> Psyche's search finds a sample of twenty for each of these "
            "pairs, so the numbers are possible. <bookmark mark='c'/> If no sample fits, or the only ones that do are "
            "absurd, with everyone answering one or seven, the numbers deserve a question. <bookmark mark='d'/> A "
            "reconstruction isn't the data. It shows what the data could have been."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b1), FadeIn(b2))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def statcheck(self):
        d = load("statcheck")
        head = heading(r"statcheck: \ does the p match its test?")
        rows = VGroup()
        for t, df, rp, rel, rc, ok, gross in zip(d["t"], d["df"], d["reported"], d["rel"], d["recomputed"],
                                                 d["consistent"], d["gross"]):
            col = GOOD if ok else (AUTH if gross else PERSON)
            verdict = r"consistent" if ok else (r"wrong side of 0.05" if gross else r"inconsistent")
            rows.add(VGroup(label(rf"$t({int(df)}) = {t:.2f},\ p {rel} {rp:g}$", font_size=22, color=WHITE),
                            label(rf"recomputed {rc:.3f}", font_size=20, color=GREY_A),
                            label(verdict, font_size=20, color=col)).arrange(RIGHT, buff=0.45))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([-2.4, 0.4, 0])
        text = rows_of([
            (r"a reported $t$, \ its degrees of freedom and its $p$ must agree", WHITE),
            (r"Nuijten and colleagues, \ 2016: \ over 250,000 $p$-values from eight journals, \ checked by program: \ "
             r"about half of articles had at least one inconsistency, \ about one in eight one that crossed 0.05", AUTH),
            (r"most errors are small; \ the ones that cross the line lean towards significance", PERSON),
        ], 4.6, 18, 0.34).move_to([4.5, -0.3, 0])
        tag = psyche_tag(r"\texttt{meta.statcheck}")
        tag2 = published_tag(r"Nuijten et al.\ (2016)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "A third check reads the statistics themselves. <bookmark mark='a'/> A reported t, its degrees of freedom, "
            "and its p have to agree. Here are six; one claims p below zero point zero five when the test gives "
            "about zero point zero eight. <bookmark mark='b'/> In 2016 Michele Nuijten and colleagues ran a program "
            "over more than a quarter of a million p-values from eight journals. About half of the articles had at "
            "least one inconsistency, and about one in eight had one that crossed zero point zero five. "
            "<bookmark mark='c'/> Most errors are small. The ones that cross the line lean towards significance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3),
                      run_time=2.5)
            for m, r in zip("abc", text):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
