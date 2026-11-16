from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Scales(VoiceoverScene):
    def construct(self):
        self.card()
        self.likert()
        self.points()

    def card(self):
        card = chapter_card(10, r"Rating scales", r"How many points should a scale have?", lit={1932: r"Likert"},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter ten. Rating scales."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def likert(self):
        head = heading(r"Likert's shortcut")
        cats = VGroup(*[word_chip(t, color=c, font_size=16, width=2.3) for t, c in (
            (r"strongly disagree", AUTH), (r"disagree", PERSON), (r"neither", GREY_B), (r"agree", SYMP),
            (r"strongly agree", GOOD))]).arrange(RIGHT, buff=0.2).move_to([0, 1.6, 0])
        rows = rows_of([
            (r"Likert, \ 1932: \ Thurstone's scaling took weeks of judges' work; \ instead, \ ask people to agree or "
             r"disagree with many statements, \ and add up the answers", WHITE),
            (r"the sum is nearly as good, \ and far cheaper: \ it became the survey's standard format", GOOD),
            (r"each item is a graded response (Part 45): \ thresholds on a latent attitude, \ not equal steps", MODEL),
            (r"response styles live in the categories: \ some people use the extremes, \ others the middle, \ "
             r"whatever their attitude", AUTH),
        ], 12.4, 21, 0.4).move_to([0, -1.1, 0])
        tag = historical_tag(r"Likert (1932)")
        with self.voiceover(
            "Thurstone's scaling was slow. <bookmark mark='a'/> In 1932 Rensis Likert proposed a shortcut. Instead "
            "of weeks of judges' work, ask people to agree or disagree with many statements, and add up the answers. "
            "<bookmark mark='b'/> The sum was nearly as good, and far cheaper, and it became the standard format of "
            "surveys. <bookmark mark='c'/> Each item is a graded response, as in Part 45: thresholds on a latent "
            "attitude, not equal steps. <bookmark mark='d'/> And response styles live in the categories. Some people "
            "use the extremes, others the middle, whatever their attitude."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cats))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def points(self):
        d = load("points")
        head = heading(r"How many points?")
        A = axes([1, 12], [0.75, 1.0], x_length=5.6, y_length=3.2, xticks=[2, 3, 4, 5, 7, 11], yticks=[0.8, 0.9, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"points on the scale",
                 ylabel=r"correlation with the attitude", center=[-3.3, 0.3, 0], font_size=13)
        dots = VGroup(*[Dot(A.ax.c2p(k, r), radius=0.08, color=MODEL) for k, r in zip(d["k"], d["r"])])
        line = curve(A.ax, d["k"], d["r"], MODEL, stroke_width=2)
        rows = rows_of([
            (r"Psyche cuts a continuous attitude into equally likely categories, \ and asks how much of it survives",
             WHITE),
            (rf"two points keep a correlation of {d['r'][0]:.2f}; \ five keep {d['r'][3]:.2f}; \ seven "
             rf"{d['r'][4]:.2f}; \ beyond that, \ almost nothing more", MODEL),
            (r"real respondents add their own costs: \ more points, \ more effort, \ more room for styles", AUTH),
            (r"five or seven labelled points is the usual compromise", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"200{,}000 simulated answers")
        with self.voiceover(
            "How many points should a scale have? <bookmark mark='a'/> Psyche cuts a continuous attitude into "
            "equally likely categories, and asks how much of it survives. <bookmark mark='b'/> Two points keep a "
            "correlation of about zero point eight. Five keep about zero point nine four, seven about zero point nine "
            "six. Beyond that, almost nothing more. <bookmark mark='c'/> Real respondents add their own costs: more "
            "points mean more effort, and more room for styles. <bookmark mark='d'/> Five or seven labelled points "
            "is the usual compromise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(dots), Create(line))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
