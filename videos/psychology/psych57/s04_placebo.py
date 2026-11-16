from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Placebo(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Placebo", r"What do sugar pills really do?")
        self.powerful()
        self.rtm()
        self.survives()
        self.openlabel()

    def powerful(self):
        rows_section(self, r"The powerful placebo, \ reconsidered", [
            (r"1955: \ Henry Beecher's ``The powerful placebo'' reported that about 35\% of patients improved on "
             r"placebo across trials", WHITE),
            (r"but improvement on placebo includes natural recovery and regression to the mean: \ people enrol when "
             r"symptoms are worst (Part 2)", AUTH),
            (r"Hr\'objartsson and G\o tzsche, \ 2001: \ trials with a placebo arm and a no-treatment arm; \ little "
             r"effect on objective or binary outcomes, \ a small one on subjective outcomes like pain", MODEL),
            (r"the placebo's real effect is the difference between placebo and no treatment, \ not placebo against "
             r"baseline", YOU),
        ], "What do sugar pills really do? <bookmark mark='a'/> In 1955 Henry Beecher's paper The powerful placebo "
           "reported that about thirty-five percent of patients improved on placebo across trials. "
           "<bookmark mark='b'/> But improvement on placebo includes natural recovery and regression to the mean, "
           "because people enrol when their symptoms are at their worst. That's Part 2. <bookmark mark='c'/> In 2001 "
           "Asbjorn Hrobjartsson and Peter Gotzsche pooled trials that had both a placebo arm and a no-treatment arm. "
           "They found little effect on objective or yes-or-no outcomes, and a small one on subjective outcomes like "
           "pain. <bookmark mark='d'/> The placebo's real effect is the difference between placebo and no treatment, "
           "not placebo against baseline.", tag=published_tag(r"Hr\'objartsson \& G\o tzsche (2001)"))

    def survives(self):
        rows_section(self, r"What survives: \ placebo analgesia", [
            (r"Levine, \ Gordon and Fields, \ 1978: \ after dental surgery, \ patients given a placebo reported less "
             r"pain; \ naloxone, \ which blocks opioid receptors, \ abolished part of the effect", WHITE),
            (r"the brain's own opioids carry part of placebo pain relief: \ a mechanism, \ not just a reporting "
             r"bias", GOOD),
            (r"imaging and pharmacology since then have found expectation changing pain processing, \ with effects "
             r"that vary greatly between people", MODEL),
            (r"placebo effects are largest for symptoms that are themselves inferences: \ pain, \ nausea, \ fatigue",
             PERSON),
        ], "So what survives? <bookmark mark='a'/> In 1978 Jon Levine, Newton Gordon and Howard Fields gave patients a "
           "placebo after dental surgery, and they reported less pain. Naloxone, which blocks opioid receptors, "
           "abolished part of the effect. <bookmark mark='b'/> The brain's own opioids carry part of placebo pain "
           "relief. That's a mechanism, not just a bias in reporting. <bookmark mark='c'/> Imaging and pharmacology "
           "since then have found expectation changing how pain is processed, with effects that vary greatly between "
           "people. <bookmark mark='d'/> Placebo effects are largest for symptoms that are themselves inferences: "
           "pain, nausea and fatigue.", tag=published_tag(r"Levine, \ Gordon \& Fields (1978)"))

    def openlabel(self):
        rows_section(self, r"Open-label placebo", [
            (r"Kaptchuk and colleagues, \ 2010: \ 80 patients with irritable bowel syndrome; \ half got pills openly "
             r"described as inert, \ with an encouraging explanation", WHITE),
            (r"after three weeks, \ more of the placebo group reported adequate relief: \ about 59\% against 35\%", GOOD),
            (r"later small trials in back pain and fatigue found similar results; \ the outcomes are self-reported, \ "
             r"and no one can be blind to taking a pill", AUTH),
            (r"contested: \ a real benefit from ritual and expectation, \ or reports shaped by attention and hope? \ "
             r"larger, \ longer trials are needed", YOU),
        ], "And the answer to your first number. <bookmark mark='a'/> In 2010 Ted Kaptchuk and colleagues gave eighty "
           "patients with irritable bowel syndrome either no treatment or pills openly described as inert, with an "
           "encouraging explanation. <bookmark mark='b'/> After three weeks, more of the placebo group reported "
           "adequate relief: about fifty-nine percent against thirty-five. <bookmark mark='c'/> Later small trials in "
           "back pain and fatigue found similar results. But the outcomes are self-reported, and no one can be blind "
           "to taking a pill. <bookmark mark='d'/> So it's contested. Is it a real benefit from ritual and "
           "expectation, or reports shaped by attention and hope? Larger, longer trials are needed.",
           tag=published_tag(r"Kaptchuk et al.\ (2010)"))

    def rtm(self):
        d = load("rtm")
        head = heading(r"Improvement with nothing done")
        A = axes([0, 10.2], [0, 10.2], x_length=3.8, y_length=3.6, xticks=[0, 5, 10], yticks=[0, 5, 10],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"pain on the screening day",
                 ylabel=r"pain a week later", center=[-3.9, 0.1, 0], font_size=12)
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        inn = x >= 7
        out_ = scatter(A.ax, x[~inn], y[~inn], GREY_C, radius=0.03)
        enr = scatter(A.ax, x[inn], y[inn], AUTH, radius=0.04)
        diag = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(10.2, 10.2), color=GREY_B, stroke_width=1.5)
        cut = DashedLine(A.ax.c2p(7, 0), A.ax.c2p(7, 10.2), color=YOU, stroke_width=2)
        rows = rows_of([
            (r"Psyche: \ 20{,}000 people, \ each with a stable level of pain plus day-to-day variation; \ no "
             r"treatment at all", WHITE),
            (rf"a trial enrols those scoring 7 or more on the screening day: \ {100 * d['enrolled_share']:.0f}\% of "
             rf"them", AUTH),
            (rf"a week later the enrolled average {d['after']:.1f}, \ down from {d['before']:.1f}; \ "
             rf"{100 * d['improved_share']:.0f}\% improved by more than a point", MODEL),
            (r"they were chosen on a bad day, \ and bad days pass: \ regression to the mean (Part 2), \ which a "
             r"placebo arm alone mistakes for a placebo effect", PERSON),
            (r"only a no-treatment arm, \ enrolled the same way, \ separates the two", YOU),
        ], 6.6, 18, 0.32).move_to([2.9, -0.2, 0])
        tag = psyche_tag(r"simulated, \ no treatment given")
        with self.voiceover(
            "Here's how much improvement comes from nothing. <bookmark mark='a'/> Psyche simulates twenty thousand "
            "people, each with a stable level of pain plus day-to-day variation, and gives no treatment at all. "
            "<bookmark mark='b'/> A trial enrols those scoring seven or more on the screening day, about fifteen "
            "percent of them. <bookmark mark='c'/> A week later the enrolled average about six point two, down from "
            "eight, and two thirds improved by more than a point. <bookmark mark='d'/> They were chosen on a bad day, "
            "and bad days pass. That's regression to the mean, from Part 2, and a placebo arm on its own mistakes it "
            "for a placebo effect. <bookmark mark='e'/> Only a no-treatment arm, enrolled the same way, separates "
            "the two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(out_), FadeIn(enr))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cut), out_.animate.set_opacity(0.25))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
