from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ weighing an identification", r"How much should one identification "
                     r"move a jury?", scale=("society",))
        self.where()
        self.weigh()
        self.prior()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"police procedure", r"line-up protocols, \ interview training, \ recording", MODEL),
            (r"expert testimony", r"psychologists explaining memory, \ confession and risk research to courts", PERSON),
            (r"forensic laboratories", r"blinding, \ proficiency testing, \ error-rate studies", GOOD),
            (r"forensic assessment", r"competence, \ risk and capacity evaluations, \ with tests whose errors are "
                                     r"stated", SYMP),
        ], "Where is this a job? <bookmark mark='a'/> In police procedure: line-up protocols, interview training and "
           "recording. <bookmark mark='b'/> In expert testimony: psychologists explaining memory, confession and risk "
           "research to courts. <bookmark mark='c'/> In forensic laboratories: blinding, proficiency testing and "
           "error-rate studies. <bookmark mark='d'/> And in forensic assessment: competence, risk and capacity "
           "evaluations, with tests whose errors are stated.")

    def weigh(self):
        d = load("roc")
        lr = d["s_point"][1] / d["s_point"][0]
        rows_section(self, r"A worked case: \ the likelihood ratio of a pick", [
            (r"Bayes's rule (Part 14): \ posterior odds of guilt = prior odds $\times$ the likelihood ratio of the "
             r"evidence", WHITE),
            (rf"an identification of the suspect under Psyche's moderate criterion: \ correct-ID rate "
             rf"{d['s_point'][1]:.2f}, \ innocent-suspect rate {d['s_point'][0]:.2f}: \ a likelihood ratio of about "
             rf"{lr:.0f}", MODEL),
            (r"prior odds of 1 to 10 become about 1 to 2: \ important evidence, \ not proof", PERSON),
            (r"with high initial confidence the ratio is far larger; \ with low confidence, \ a biased line-up or "
             r"repeated viewing, \ much smaller", AUTH),
            (r"an expert's job: \ give the court the procedure's error rates and the confidence first recorded, \ not "
             r"a verdict", YOU),
        ], "Here's a worked case: the weight of one identification. <bookmark mark='a'/> Bayes's rule, from Part 14: "
           "the posterior odds of guilt are the prior odds times the likelihood ratio of the evidence. "
           "<bookmark mark='b'/> Take an identification of the suspect under Psyche's moderate criterion. The "
           "correct-identification rate is about zero point five six, and the rate of picking an innocent suspect "
           "about zero point one one, so the likelihood ratio is about five. <bookmark mark='c'/> Prior odds of one "
           "to ten become about one to two. That's important evidence, not proof. <bookmark mark='d'/> With high "
           "initial confidence the ratio is far larger. With low confidence, a biased line-up or repeated viewing, "
           "it's much smaller. <bookmark mark='e'/> An expert's job is to give the court the procedure's error rates "
           "and the confidence first recorded, not a verdict.", tag=psyche_tag(r"\texttt{work.lineup\_roc}"))

    def prior(self):
        d = load("roc")
        c = np.asarray(d["criteria"])
        picks = []
        for cc, col, name in ((0.0, AUTH, r"a lax witness"), (1.0, MODEL, r"moderate"), (2.5, GOOD, r"a strict witness")):
            i = int(np.argmin(np.abs(c - cc)))
            picks.append((float(d["s_hit"][i] / d["s_fa"][i]), col, name))
        head = heading(r"The same pick, \ different investigations")
        ps = np.linspace(0.01, 0.99, 99)
        A = axes([0, 1], [0, 1.02], x_length=4.6, y_length=3.4, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"chance the suspect is the culprit, \ before",
                 ylabel=r"after an identification", center=[-3.6, 0.2, 0], font_size=12)
        diag = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 1), color=GREY_C, stroke_width=1.5)
        cs = VGroup(*[curve(A.ax, ps, ps * lr / (ps * lr + 1 - ps), col, stroke_width=4) for lr, col, _ in picks])
        key = VGroup(*[label(rf"{n}: \ LR {lr:.0f}", font_size=13, color=col) for lr, col, n in picks]).arrange(
            RIGHT, buff=0.3).next_to(A, UP, buff=0.2)
        lr = picks[1][0]
        post = lambda p: p * lr / (p * lr + 1 - p)
        rows = rows_of([
            (r"the horizontal axis is how strong the case against the suspect was before the line-up: \ the "
             r"investigation, \ not the witness", WHITE),
            (rf"with the moderate witness, \ a suspect who was 50\% likely becomes {100 * post(0.5):.0f}\%; \ one "
             rf"who was 10\% likely becomes {100 * post(0.1):.0f}\%", MODEL),
            (r"a line-up built around a weak suspect turns a good witness into weak evidence: \ most of the "
             r"identification's meaning came from the police work before it", AUTH),
            (r"a strict witness (high confidence at the first viewing) moves the same prior much further: \ record "
             r"that confidence, \ in the witness's words, \ at once", GOOD),
        ], 6.4, 18, 0.32).move_to([3.0, -0.2, 0])
        tag = psyche_tag(r"\texttt{work.lineup\_roc}, \ three criteria")
        with self.voiceover(
            "The same pick means different things in different investigations. <bookmark mark='a'/> The horizontal "
            "axis is how strong the case against the suspect was before the line-up. That's the investigation, not "
            "the witness. <bookmark mark='b'/> With the moderate witness, a suspect who was fifty percent likely to be "
            "the culprit becomes eighty-four percent likely. One who was ten percent likely becomes only thirty-seven "
            "percent. <bookmark mark='c'/> A line-up built around a weak suspect turns a good witness into weak "
            "evidence. Most of the identification's meaning came from the police work before it. "
            "<bookmark mark='d'/> A strict witness, one with high confidence at the first viewing, moves the same "
            "prior much further. So record that confidence, in the witness's own words, at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(diag), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), *[Create(c_) for c_ in cs], run_time=2)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
