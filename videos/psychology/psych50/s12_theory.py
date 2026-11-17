from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Theory(VoiceoverScene):
    def construct(self):
        self.card()
        self.paradox()
        self.crud()
        self.remedies()

    def card(self):
        card = chapter_card(11, r"The theory crisis", r"Was the deepest problem ever statistics?", lit=(), part=PART,
                            scale=("society",), marr=("what",))
        with self.voiceover("Chapter eleven. The theory crisis."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def paradox(self):
        head = heading(r"Meehl's paradox")
        rows = rows_of([
            (r"1967 to 1990: \ Paul Meehl contrasted physics with ``soft'' psychology", WHITE),
            (r"in physics a theory predicts a number; \ better measurement makes the test harder, \ and a theory can "
             r"fail it", GOOD),
            (r"in much of psychology a theory predicts only a direction; \ better measurement makes the test easier", AUTH),
            (r"because in real data almost everything correlates with almost everything a little: \ the crud factor",
             PERSON),
            (r"so a significant result in the predicted direction is weak evidence for a theory, \ however large "
             r"the sample", YOU),
        ], 12.4, 23, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Meehl (1978); \ Meehl (1990)")
        with self.voiceover(
            "Some argue the deepest problem was never statistics. <bookmark mark='a'/> Paul Meehl spent decades "
            "contrasting physics with what he called soft psychology. <bookmark mark='b'/> In physics a theory "
            "predicts a number, so better measurement makes the test harder, and the theory can fail it. "
            "<bookmark mark='c'/> In much of psychology a theory predicts only a direction, so better measurement "
            "makes the test easier. <bookmark mark='d'/> That's because in real data almost everything correlates "
            "with almost everything, a little. Meehl called it the crud factor. <bookmark mark='e'/> So a significant "
            "result in the predicted direction is weak evidence for a theory, however large the sample."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def crud(self):
        d = load("crud")
        head = heading(r"Confirmed by crud")
        A = axes([1.3, 4.1], [0, 0.55], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"directional predictions ``confirmed''",
                 center=[-3.3, 0.3, 0], font_size=12)
        x = np.log10(np.asarray(d["n"], float))
        c = curve(A.ax, x, d["confirmed"], AUTH, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(xi, v), radius=0.07, color=AUTH) for xi, v in zip(x, d["confirmed"])])
        names = VGroup(*[label(num(int(n)), font_size=13, color=GREY_A).next_to(A.ax.c2p(xi, 0), DOWN, buff=0.1)
                         for xi, n in zip(x, d["n"])])
        half = DashedLine(A.ax.c2p(1.3, 0.5), A.ax.c2p(4.1, 0.5), color=GREY_B, stroke_width=1.5)
        rows = rows_of([
            (r"Psyche: \ every pair of variables correlates a little (SD 0.15 around zero); \ a theory with no truth in "
             r"it predicts a direction at random", WHITE),
            (rf"with 30 people, \ {100 * d['confirmed'][0]:.0f}\% of its predictions come out significant in the "
             rf"predicted direction", MODEL),
            (rf"with 10,000, \ {100 * d['confirmed'][-1]:.0f}\%: \ approaching half, \ for a theory that knows nothing",
             AUTH),
            (r"large samples cure noise, \ not weak theory", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"crud factor, \ simulated")
        with self.voiceover(
            "Here's Meehl's paradox, computed. <bookmark mark='a'/> In Psyche's world every pair of variables "
            "correlates a little, and a theory with no truth in it predicts a direction at random. "
            "<bookmark mark='b'/> With thirty people, about six percent of its predictions come out significant in "
            "the predicted direction. <bookmark mark='c'/> With ten thousand, about forty-four percent: approaching "
            "half, for a theory that knows nothing. <bookmark mark='d'/> Large samples cure noise, not weak theory."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(half))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(dots))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def remedies(self):
        head = heading(r"Stronger theories")
        rows = rows_of([
            (r"predict numbers, \ or at least shapes and orderings, \ that the data could contradict: \ Part 48's "
             r"``what does the model rule out?''", GOOD),
            (r"formal models, \ written as programs, \ so that predictions are derived and not argued "
             r"(Oberauer and Lewandowsky, \ 2019)", MODEL),
            (r"strong inference: \ two rival theories, \ one experiment that one of them must fail", PERSON),
            (r"and say what a claim covers: \ which people, \ stimuli and settings (Part 47's generalizability "
             r"critique)", SYMP),
            (r"the reforms of Part 4 make tests honest; \ only better theories make them severe", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Oberauer \& Lewandowsky (2019)")
        with self.voiceover(
            "What would stronger theories look like? <bookmark mark='a'/> They predict numbers, or at least shapes and "
            "orderings, that the data could contradict. That's Part 48's question: what does the model rule out? "
            "<bookmark mark='b'/> They're formal models, written as programs, so that predictions are derived rather "
            "than argued. <bookmark mark='c'/> They're tested by strong inference: two rival theories, and one "
            "experiment that one of them must fail. <bookmark mark='d'/> And they say what a claim covers: which "
            "people, stimuli and settings. <bookmark mark='e'/> The reforms of Part 4 make tests honest. Only better "
            "theories make them severe."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
