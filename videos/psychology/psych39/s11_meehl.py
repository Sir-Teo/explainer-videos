from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Meehl(VoiceoverScene):
    def construct(self):
        self.card()
        self.book()
        self.meta()
        self.why()

    def card(self):
        card = chapter_card(10, r"Clinical against statistical prediction", r"Who predicts better, \ the expert or "
                            r"the formula?", lit={1954: r"Meehl", 1979: r"Dawes", 2000: r"Grove et al."}, part=PART,
                            scale=("person",), marr=("how",))
        with self.voiceover("Chapter ten. Clinical against statistical prediction."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def book(self):
        head = heading(r"A disturbing little book")
        rows = rows_of([
            (r"Meehl, \ 1954: \ \emph{Clinical versus Statistical Prediction}", WHITE),
            (r"the same information about a patient, \ a parolee or a student, \ combined two ways: \ by an "
             r"expert's judgment, \ or by a fixed formula", SYMP),
            (r"in the studies he could find, \ the formula did as well or better, \ almost every time", AUTH),
            (r"he later called it ``my disturbing little book'': \ clinicians did not welcome it", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        tag = historical_tag(r"Meehl (1954)")
        with self.voiceover(
            "If diagnosis is hard, maybe expert judgment can rescue it. <bookmark mark='a'/> In 1954 Paul Meehl "
            "published Clinical versus Statistical Prediction. <bookmark mark='b'/> It compared two ways of combining "
            "the same information about a patient, a parolee or a student: an expert's judgment, or a fixed formula. "
            "<bookmark mark='c'/> In the studies he could find, the formula did as well or better, almost every time. "
            "<bookmark mark='d'/> He later called it his disturbing little book. Clinicians didn't welcome it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def meta(self):
        head = heading(r"Half a century later")
        A = axes([-0.6, 2.6], [0, 50], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 25, 50],
                 yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"share of studies", center=[-3.6, -0.2, 0], font_size=14)
        lo = bars(A.ax, [0, 2], [33, 6], [GOOD, AUTH], width=0.6, opacity=0.9)
        hi = bars(A.ax, [0, 2], [47, 16], [GOOD, AUTH], width=0.6, opacity=0.35)
        names = VGroup(wrapped_label(r"formula clearly better", 1.6, 14, GOOD).next_to(A.ax.c2p(0, 0), DOWN,
                                                                                     buff=0.15),
                       wrapped_label(r"about equal", 1.6, 14, GREY_A).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15),
                       wrapped_label(r"clinician clearly better", 1.6, 14, AUTH).next_to(A.ax.c2p(2, 0), DOWN,
                                                                                       buff=0.15))
        tops = VGroup(label(r"33 to 47\%", font_size=15, color=GOOD).next_to(A.ax.c2p(0, 47), UP, buff=0.08),
                      label(r"6 to 16\%", font_size=15, color=AUTH).next_to(A.ax.c2p(2, 16), UP, buff=0.08),
                      label(r"the rest", font_size=15, color=GREY_A).next_to(A.ax.c2p(1, 5), UP, buff=0.08))
        rows = rows_of([
            (r"Grove and colleagues, \ 2000: \ a meta-analysis of studies comparing clinical and mechanical "
             r"prediction of human health and behaviour", WHITE),
            (r"the formula was clearly better in 33 to 47\% of studies, \ depending on the analysis; \ the clinician "
             r"in 6 to 16\%; \ the rest were close", GOOD),
            (r"the advantage held across tasks, \ types of judge and amounts of experience; \ clinicians did "
             r"relatively worse when they had interview data", AUTH),
            (r"more information can make judgment worse, \ when it is vivid and irrelevant", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Grove et al.\ (2000)")
        with self.voiceover(
            "The question was asked again and again. <bookmark mark='a'/> In 2000 William Grove and colleagues "
            "meta-analysed the studies comparing clinical and mechanical prediction of health and behaviour. "
            "<bookmark mark='b'/> The formula was clearly better in a third to a half of studies, depending on the "
            "analysis. The clinician was clearly better in six to sixteen percent. The rest were close. "
            "<bookmark mark='c'/> The advantage held across tasks, types of judge and amounts of experience. And "
            "clinicians did relatively worse when they had interview data. <bookmark mark='d'/> More information "
            "can make judgment worse, when it's vivid and irrelevant."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[GrowFromEdge(x, DOWN) for x in hi], *[GrowFromEdge(x, DOWN) for x in lo],
                      FadeIn(tops))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def why(self):
        d = load("meehl")
        head = heading(r"Why formulas win")
        keys = [("ceiling", r"the true weights", GREY_A), ("fitted", r"weights fitted on 200 cases", SYMP),
                ("unit", r"equal weights", GOOD), ("clinician", r"a clinician, \ weights wandering", AUTH)]
        A = axes([0, 0.8], [-0.6, 3.6], x_length=4.6, y_length=3.0, xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"correlation with the outcome, \ new cases", center=[-2.6, -0.2, 0],
                 font_size=14)
        bs = VGroup()
        labs = VGroup()
        for k, (key, name, c) in enumerate(keys):
            y = 3 - k
            lo_, hi_ = A.ax.c2p(0, y), A.ax.c2p(d[key], y)
            bs.add(Rectangle(width=hi_[0] - lo_[0], height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.85)
                   .move_to([(lo_[0] + hi_[0]) / 2, lo_[1], 0]))
            labs.add(VGroup(wrapped_label(name, 2.2, 14, c).next_to(A.ax.c2p(0, y), LEFT, buff=0.15),
                            label(f"{d[key]:.2f}", font_size=14, color=c).next_to(bs[-1], RIGHT, buff=0.08)))
        rows = rows_of([
            (r"Psyche: \ an outcome depends on five cues; \ every method sees the same cues", WHITE),
            (r"the clinician knows the right cues and roughly the right weights, \ but applies them a little "
             r"differently to each case", AUTH),
            (r"Dawes, \ 1979: \ even equal weights, \ an ``improper'' model, \ beat that, \ because a formula is "
             r"consistent and a person is not", GOOD),
            (r"the lesson is not that clinicians are useless, \ but that their judgments should be combined by "
             r"rule", YOU),
        ], 5.2, 19, 0.36).move_to([3.8, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.clinician\_vs\_formula}, \ 50 samples; \ Dawes (1979)")
        with self.voiceover(
            "Why do formulas win? <bookmark mark='a'/> In Psyche, an outcome depends on five cues, and every method "
            "sees the same cues. <bookmark mark='b'/> The clinician knows the right cues and roughly the right "
            "weights, but applies them a little differently to each case. <bookmark mark='c'/> In 1979 Robyn Dawes "
            "showed that even equal weights, an improper model, beat that, because a formula is consistent and a "
            "person is not. <bookmark mark='d'/> The lesson isn't that clinicians are useless. It's that their "
            "judgments should be combined by rule."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), GrowFromEdge(bs[0], LEFT), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), GrowFromEdge(bs[3], LEFT), FadeIn(labs[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), GrowFromEdge(bs[1], LEFT), GrowFromEdge(bs[2], LEFT), FadeIn(labs[1]),
                      FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
