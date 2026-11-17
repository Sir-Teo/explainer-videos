from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Confidence(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Confidence", r"Can a witness's certainty be trusted?")
        self.cac()
        self.inflation()

    def cac(self):
        d = load("cac")
        head = heading(r"Initial confidence, \ under clean procedure")
        A = axes([0.5, 5.5], [0.4, 1.0], x_length=5.6, y_length=3.2, xticks=[1, 2, 3, 4, 5], yticks=[0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"confidence level",
                 ylabel=r"suspect IDs that are correct", center=[-3.3, 0.3, 0], font_size=12)
        lv = np.asarray(d["levels"])
        ci = curve(A.ax, lv, d["initial"], GOOD, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(float(x), float(y)), radius=0.07, color=GOOD) for x, y in zip(lv, d["initial"])])
        rows = rows_of([
            (r"the old view: \ confidence is nearly useless, \ because overall the confidence-accuracy correlation is "
             r"low", AUTH),
            (r"the better question: \ among identifications made with high confidence, \ what share are right? \ the "
             r"confidence-accuracy characteristic", MODEL),
            (rf"Psyche: \ {100 * d['initial'][0]:.0f}\% at the lowest confidence, \ {100 * d['initial'][-1]:.0f}\% at "
             rf"the highest, \ with equal numbers of culprit-present and culprit-absent line-ups", GOOD),
            (r"Wixted and Wells, \ 2017: \ a high-confidence initial identification, \ made under clean procedure, \ "
             r"is highly diagnostic; \ a low-confidence one is a warning", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.confidence\_feedback}")
        with self.voiceover(
            "Can a witness's certainty be trusted? <bookmark mark='a'/> The old view said confidence is nearly "
            "useless, because overall the correlation between confidence and accuracy is low. <bookmark mark='b'/> "
            "The better question asks: among identifications made with high confidence, what share are right? That's "
            "the confidence-accuracy characteristic. <bookmark mark='c'/> In Psyche, about half are right at the "
            "lowest confidence, and ninety-six percent at the highest. <bookmark mark='d'/> John Wixted and Gary "
            "Wells concluded in 2017 that a high-confidence initial identification, made under clean procedure, is "
            "highly diagnostic, and a low-confidence one is a warning."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(ci), FadeIn(dots))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def inflation(self):
        d = load("cac")
        rows_section(self, r"Confidence grows after the fact", [
            (r"Wells and Bradfield, \ 1998: \ witnesses told ``good, \ you identified the suspect'' became more "
             r"confident, \ and remembered a better view", WHITE),
            (rf"in Psyche, \ the same feedback raises every suspect-picker by about one level: \ at the top level, \ "
             rf"accuracy falls from {100 * d['initial'][-1]:.0f}\% to {100 * d['after'][-1]:.0f}\%, \ and the top "
             rf"level holds twice as many IDs", AUTH),
            (r"by the trial, \ months later, \ a witness who said ``maybe number three'' says ``I'll never forget that "
             r"face''", PERSON),
            (r"so the confidence that counts is the first one, \ recorded at the line-up, \ in the witness's words",
             YOU),
        ], "But confidence grows after the fact. <bookmark mark='a'/> In 1998 Gary Wells and Amy Bradfield found that "
           "witnesses told good, you identified the suspect became more confident, and remembered having a better "
           "view. <bookmark mark='b'/> In Psyche, the same feedback raises every suspect-picker by about one level. "
           "At the top level, accuracy falls from ninety-six percent to ninety-three, and the top level now holds "
           "twice as many identifications. <bookmark mark='c'/> By the trial, months later, a witness who said maybe "
           "number three says I'll never forget that face. <bookmark mark='d'/> So the confidence that counts is the "
           "first one, recorded at the line-up, in the witness's own words.",
           tag=published_tag(r"Wells \& Bradfield (1998)"))
