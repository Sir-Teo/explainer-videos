from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Workload(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"Attention at work", r"How much can one person do at once?")
        self.resources()
        self.tlx()

    def resources(self):
        chips_section(self, r"Multiple resources", [
            (r"one pool?", r"Part 18's attention as a single bottleneck predicts that any two tasks interfere", AUTH),
            (r"several pools", r"Christopher Wickens: \ tasks interfere more when they share modality (eyes or ears), "
                               r"\ code (spatial or verbal) and stage (perceiving or responding)", MODEL),
            (r"the design rule", r"a pilot flying by eye takes radio calls by ear; \ a driver's navigation speaks "
                                 r"rather than shows", GOOD),
            (r"the limit", r"even separate pools share a central executive: \ a phone conversation still slows a "
                           r"driver's braking (Part 18)", PERSON),
        ], "How much can one person do at once? <bookmark mark='a'/> If attention were one pool, as a single bottleneck, "
           "any two tasks would interfere. <bookmark mark='b'/> Christopher Wickens proposed several pools. Tasks "
           "interfere more when they share a modality, eyes or ears, a code, spatial or verbal, and a stage, "
           "perceiving or responding. <bookmark mark='c'/> So a pilot flying by eye takes radio calls by ear, and a "
           "driver's navigation speaks rather than shows. <bookmark mark='d'/> But even separate pools share a central "
           "executive. A phone conversation still slows a driver's braking, as Part 18 showed.")

    def tlx(self):
        d = load("tlx")
        head = heading(r"Measuring workload")
        A = axes([0.3, 6.7], [0, 100], x_length=5.6, y_length=3.0, xticks=None, yticks=[0, 50, 100],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"rating", center=[-3.3, 0.4, 0], font_size=12)
        cols = [MODEL, GREY_B, PERSON, SYMP, GOOD, AUTH]
        b = bars(A.ax, list(range(1, 7)), d["ratings"], cols, width=0.6)
        names = VGroup(*[VGroup(label(s, font_size=13, color=c), label(rf"weight {int(w)}", font_size=11, color=GREY_A))
                         .arrange(DOWN, buff=0.04).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1)
                         for i, (s, c, w) in enumerate(zip(d["scales"], cols, d["weights"]))])
        rows = rows_of([
            (r"NASA-TLX (Hart and Staveland, \ 1988): \ six ratings from 0 to 100, \ then 15 pairwise choices of "
             r"which scale mattered more", WHITE),
            (rf"the weighted score is the ratings weighted by those choices: \ here {d['score']:.0f}, \ against a "
             rf"raw mean of {d['raw']:.0f}", MODEL),
            (r"also: \ a secondary task whose performance falls as the main task takes more; \ pupil size and heart "
             r"rate variability", PERSON),
            (r"no single measure is workload; \ when they disagree, \ each is telling you something", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.nasa\_tlx}, \ a worked example")
        tag2 = published_tag(r"Hart \& Staveland (1988)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Workload has to be measured. <bookmark mark='a'/> The most used scale is NASA's task load index: six "
            "ratings from zero to a hundred, then fifteen pairwise choices of which scale mattered more for this "
            "task. <bookmark mark='b'/> The score weights each rating by those choices: here sixty, against a raw "
            "mean of fifty-one. <bookmark mark='c'/> There are other measures too: a secondary task whose performance "
            "falls as the main task takes more, and pupil size or heart-rate variability. <bookmark mark='d'/> No "
            "single measure is workload. When they disagree, each is telling you something."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
