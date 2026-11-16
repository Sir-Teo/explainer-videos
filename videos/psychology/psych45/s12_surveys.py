from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Surveys(VoiceoverScene):
    def construct(self):
        self.card()
        self.matrix()
        self.pvs()

    def card(self):
        card = chapter_card(11, r"Large-scale assessment", r"Why does a national survey not give each student a "
                            r"score?", lit={1991: r"Mislevy"}, part=PART, scale=("group", "society"),
                            marr=("what", "how"))
        with self.voiceover("Chapter eleven. Large-scale assessment."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def matrix(self):
        d = load("pv")
        head = heading(r"Many items, \ few per student")
        grid = VGroup()
        for k in range(4):
            row = VGroup(*[Square(0.32, stroke_width=1, stroke_color=GREY_B,
                                  fill_color=(SYMP, PERSON, GOOD, MODEL)[k] if j % 4 == k else BLACK,
                                  fill_opacity=0.9 if j % 4 == k else 0.2) for j in range(24)]).arrange(RIGHT, buff=0.04)
            grid.add(VGroup(label(rf"booklet {k + 1}", font_size=15, color=GREY_A), row).arrange(RIGHT, buff=0.3))
        grid.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, 1.4, 0])
        rows = rows_of([
            (r"a national survey wants to describe a country's students across a whole curriculum: \ far more items "
             r"than one student can answer", WHITE),
            (rf"matrix sampling: \ a pool of {d['pool']} items split into 4 booklets of {d['items_each']}; \ each "
             rf"student answers one booklet", MODEL),
            (r"the population is measured well; \ each student is measured badly: \ six items cannot place one person",
             AUTH),
            (r"so the survey reports groups, \ not students: \ the reason a national survey gives no individual "
             r"scores", YOU),
        ], 12.4, 21, 0.38).move_to([0, -1.6, 0])
        with self.voiceover(
            "National surveys of what students know have a different goal. <bookmark mark='a'/> They want to describe "
            "a country's students across a whole curriculum, which means far more items than one student can answer. "
            "<bookmark mark='b'/> So they use matrix sampling: a pool of items split into booklets, and each student "
            "answers one booklet. <bookmark mark='c'/> The population is measured well, and each student badly. Six "
            "items can't place one person. <bookmark mark='d'/> So the survey reports groups, not students. That's why "
            "a national survey gives no individual scores."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def pvs(self):
        d = load("pv")
        head = heading(r"Plausible values")
        A = axes([0.3, 4.7], [0, 1.2], x_length=5.4, y_length=2.4, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"spread (SD)", center=[-3.4, 1.0, 0], font_size=13)
        B = axes([0.3, 4.7], [0, 0.5], x_length=5.4, y_length=1.9, xticks=None, yticks=[0, 0.2, 0.4],
                 yfmt=lambda v: f"{v:g}", ylabel=r"group gap", center=[-3.4, -2.0, 0], font_size=13)
        cols = [GREY_B, AUTH, PERSON, GOOD]
        b1 = bars(A.ax, [1, 2, 3, 4], [d["true_sd"], d["eap_sd"], d["pv_sd"], d["pvc_sd"]], cols, width=0.6)
        b2 = bars(B.ax, [1, 2, 3, 4], [d["true_gap"], d["eap_gap"], d["pv_gap"], d["pvc_gap"]], cols, width=0.6)
        names = VGroup(*[wrapped_label(t, 1.3, 12, c).next_to(B.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"truth", GREY_B), (r"EAP scores", AUTH), (r"plausible values", PERSON),
                                    (r"with conditioning", GOOD)))])
        rows = rows_of([
            (rf"each student's EAP is shrunk toward the mean: \ the spread falls from {d['true_sd']:.2f} to "
             rf"{d['eap_sd']:.2f}, \ and a true gap of {d['true_gap']:.2f} between two groups shows as "
             rf"{d['eap_gap']:.2f}", AUTH),
            (rf"plausible values are draws from each posterior, \ not its mean: \ the spread comes back "
             rf"({d['pv_sd']:.2f}), \ but the gap is still shrunk", PERSON),
            (rf"draw them from a model that includes the group (the conditioning model): \ gap {d['pvc_gap']:.2f}",
             GOOD),
            (r"Mislevy, \ 1991: \ a plausible value is not a score; \ analyse each set and combine, \ as in multiple "
             r"imputation", YOU),
        ], 6.0, 18, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{irt.plausible\_values}, \ \texttt{irt.latent\_em}; \ 4{,}000 simulated students")
        with self.voiceover(
            "How then do you describe the population? <bookmark mark='a'/> Each student's expected a posteriori "
            "estimate is shrunk toward the mean. So the spread of the scores falls from one to about zero point seven, "
            "and a true gap of zero point four between two groups shows as about zero point two. "
            "<bookmark mark='b'/> Plausible values are random draws from each student's posterior, not its mean. The "
            "spread comes back, but the gap is still shrunk. <bookmark mark='c'/> Draw them from a model that "
            "includes the groups, called the conditioning model, and the gap comes back too. <bookmark mark='d'/> "
            "Robert Mislevy set this out in 1991. A plausible value isn't a score. Analyse each set, and combine them, "
            "as in multiple imputation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B), FadeIn(names), FadeIn(b1[0]), FadeIn(b2[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b1[1]), FadeIn(b2[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b1[2]), FadeIn(b2[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b1[3]), FadeIn(b2[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
