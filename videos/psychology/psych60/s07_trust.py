from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Trust(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"People trusting machines", r"Do people rely on machines too much, \ or too little?",
                     scale=("person", "society"))
        self.aversion()
        self.chart()
        self.minds()

    def aversion(self):
        rows_section(self, r"Aversion and appreciation", [
            (r"Dietvorst, \ Simmons and Massey, \ 2015: \ people who saw an algorithm make a mistake chose it less, \ "
             r"even when it beat them: \ algorithm aversion", AUTH),
            (r"Logg, \ Minson and Moore, \ 2019: \ people often weight advice more when told it comes from an "
             r"algorithm: \ algorithm appreciation", GOOD),
            (r"both hold, \ in different tasks: \ aversion after visible errors and in matters of taste; \ "
             r"appreciation for numerical forecasts", MODEL),
            (r"and Part 51's automation bias: \ supervisors of reliable systems stop checking them", PERSON),
        ], "Do people rely on machines too much, or too little? <bookmark mark='a'/> In 2015 Berkeley Dietvorst, "
           "Joseph Simmons and Cade Massey found that people who saw an algorithm make a mistake chose it less, even "
           "when it beat them. They called it algorithm aversion. <bookmark mark='b'/> In 2019 Jennifer Logg, Julia "
           "Minson and Don Moore found that people often weight advice more when told it comes from an algorithm: "
           "algorithm appreciation. <bookmark mark='c'/> Both hold, in different tasks: aversion after visible "
           "errors and in matters of taste, and appreciation for numerical forecasts. <bookmark mark='d'/> And "
           "there's Part 51's automation bias: supervisors of reliable systems stop checking them.",
           tag=published_tag(r"Dietvorst, \ Simmons \& Massey (2015)"))

    def chart(self):
        d = load("reliance")
        head = heading(r"What aversion costs")
        T = len(d["reliance_t"])
        A = axes([0, T], [0.3, 1.0], x_length=5.6, y_length=3.2, xticks=[0, 10, 20, 30, 40], yticks=[0.4, 0.6, 0.8, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"decisions", center=[-3.3, 0.2, 0],
                 font_size=12)
        t = np.arange(1, T + 1)
        cr = curve(A.ax, t, d["reliance_t"], AUTH, stroke_width=4)
        ca = curve(A.ax, t, d["acc_t"], PERSON, stroke_width=4)
        best = DashedLine(A.ax.c2p(0, d["best"]), A.ax.c2p(T, d["best"]), color=GOOD, stroke_width=2)
        key = VGroup(label(r"share relying on the aid", font_size=13, color=AUTH),
                     label(r"accuracy", font_size=13, color=PERSON),
                     label(r"always relying", font_size=13, color=GOOD)).arrange(RIGHT, buff=0.35)
        key.next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"Psyche's 2,000 people: \ an aid right 80\% of the time, \ their own judgment 70\%", WHITE),
            (r"each time the aid errs while they rely on it, \ they halve their reliance; \ their own errors are "
             r"forgiven", AUTH),
            (rf"reliance settles near {d['reliance_t'][-1]:.2f}, \ and accuracy near {d['acc_t'][-1]:.2f}, \ "
             rf"against {d['best']:.2f} by always relying", PERSON),
            (r"the remedies studied: \ letting people adjust the algorithm slightly, \ and showing its track record "
             r"against theirs", GOOD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{machines.aversion}")
        with self.voiceover(
            "What does aversion cost? <bookmark mark='a'/> Psyche's two thousand people have an aid that's right "
            "eighty percent of the time, and their own judgment, right seventy. <bookmark mark='b'/> Each time the "
            "aid errs while they rely on it, they halve their reliance, but their own errors are forgiven. "
            "<bookmark mark='c'/> Reliance settles near a half, and accuracy near seventy-five percent, against "
            "eighty by always relying. <bookmark mark='d'/> The remedies that have been studied: letting people "
            "adjust the algorithm slightly, and showing its track record against theirs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), Create(best))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cr), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(ca))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def minds(self):
        chips_section(self, r"Seeing a mind", [
            (r"two dimensions", r"Gray, \ Gray and Wegner, \ 2007: \ people judge minds by agency (can it plan, \ "
                                r"act?) \ and experience (can it feel?)", MODEL),
            (r"machines", r"rated moderate on agency and low on experience", PERSON),
            (r"anthropomorphism", r"a voice, \ a name and fluent language raise both, \ whatever is underneath", AUTH),
            (r"the design question", r"whether systems should present as minds at all", YOU),
        ], "How do people see a mind in a machine? <bookmark mark='a'/> In 2007 Heather Gray, Kurt Gray and Daniel "
           "Wegner found that people judge minds on two dimensions: agency, can it plan and act, and experience, can "
           "it feel? <bookmark mark='b'/> Machines were rated moderate on agency and low on experience. "
           "<bookmark mark='c'/> A voice, a name and fluent language raise both, whatever is underneath. "
           "<bookmark mark='d'/> So the design question is whether systems should present as minds at all.")
