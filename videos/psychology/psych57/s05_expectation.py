from __future__ import annotations

from scipy import stats

from videos.psychology.psych57.common import *  # noqa: F403


class Expectation(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Expectation as a prior", r"Why would a belief change a sensation?", marr=("how",))
        self.model()
        self.nocebo()

    def model(self):
        d = load("placebo")
        head = heading(r"Pain as inference")
        x = np.linspace(0, 10, 300)
        A = axes([0, 10], [0, 0.55], x_length=5.6, y_length=2.6, xticks=[0, 2, 4, 6, 8, 10], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"pain intensity", center=[-3.3, 0.9, 0], font_size=12)
        sens = curve(A.ax, x, stats.norm.pdf(x, 6, 1.0) * 1.0, PERSON, stroke_width=3)
        prior = curve(A.ax, x, stats.norm.pdf(x, 4, 1.5) * 1.0, MODEL, stroke_width=3)
        post_mu, post_sd = d["placebo"], np.sqrt(1 / (1 / 1.0 + 1 / 1.5 ** 2))
        post = curve(A.ax, x, stats.norm.pdf(x, post_mu, post_sd), GOOD, stroke_width=4)
        key = VGroup(label(r"signal", font_size=13, color=PERSON), label(r"expectation", font_size=13, color=MODEL),
                     label(r"felt", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.35).next_to(A, UP, buff=0.15)
        B = axes([0.3, 3.3], [0, 1.8], x_length=4.0, y_length=1.8, xticks=[0.5, 1, 1.5, 2, 3], yticks=[0, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0f}", xlabel=r"noise in the bodily signal (SD)",
                 ylabel=r"placebo effect", center=[-3.6, -2.2, 0], font_size=11)
        cb = curve(B.ax, d["sensory_sd"], d["by_noise"], AUTH, stroke_width=4)
        rows = rows_of([
            (r"Part 14's observer, \ for the body: \ the felt intensity combines the signal with an expected level, \ "
             r"each weighted by its precision", WHITE),
            (rf"a stimulus at 6 with expectation lowered from 6 to 4: \ the felt pain falls to {d['placebo']:.1f}; \ "
             rf"the expectation carries a weight of {d['weight']:.2f}", GOOD),
            (r"the noisier the bodily signal, \ the more the expectation counts: \ the effect grows from 0.2 to 1.6 "
             r"points", AUTH),
            (r"so placebos move vague, \ interoceptive symptoms most, \ and a broken bone least", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.4, 0])
        tag = psyche_tag(r"\texttt{work.placebo\_pain}, \ illustrative precisions")
        with self.voiceover(
            "Why would a belief change a sensation? <bookmark mark='a'/> Part 14's observer, applied to the body: the "
            "felt intensity combines the signal with an expected level, each weighted by its precision. "
            "<bookmark mark='b'/> Take a stimulus at six, with the expectation lowered from six to four. The felt pain "
            "falls to about five point four, because the expectation carries a weight of about a third. "
            "<bookmark mark='c'/> The noisier the bodily signal, the more the expectation counts. The effect grows "
            "from a fifth of a point to more than a point and a half. <bookmark mark='d'/> So placebos move vague, "
            "internal symptoms most, and a broken bone least."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(sens), Create(prior))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(post))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(B), Create(cb))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def nocebo(self):
        chips_section(self, r"Nocebo and sham", [
            (r"nocebo", r"expecting harm produces symptoms: \ side effects reported on placebo in drug trials often "
                        r"match the drug's warning label", AUTH),
            (r"statins", r"in a 2020 n-of-1 trial, \ most of the muscle symptoms people felt on statins they also "
                         r"felt on placebo", PERSON),
            (r"sham surgery", r"knee arthroscopy for arthritis did no better than a sham operation (Moseley and "
                              r"colleagues, \ 2002)", MODEL),
            (r"the lesson", r"how a warning or a procedure is framed is part of the treatment, \ and part of the harm",
             GOOD),
        ], "Expectation cuts both ways. <bookmark mark='a'/> Nocebo: expecting harm produces symptoms, and the side "
           "effects reported on placebo in drug trials often match the drug's warning label. <bookmark mark='b'/> In a "
           "2020 trial in which each patient alternated between statins, placebo and no tablets, most of the muscle "
           "symptoms people felt on statins they also felt on placebo. <bookmark mark='c'/> Sham surgery: in 2002 "
           "Bruce Moseley and colleagues found that knee arthroscopy for arthritis did no better than a sham "
           "operation. <bookmark mark='d'/> The lesson is that how a warning or a procedure is framed is part of the "
           "treatment, and part of the harm.")
