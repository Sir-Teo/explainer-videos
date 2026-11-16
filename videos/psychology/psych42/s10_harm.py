from __future__ import annotations

from videos.psychology.psych42.common import *  # noqa: F403


class Harm(VoiceoverScene):
    def construct(self):
        self.card()
        self.list_()
        self.why()
        self.detect()

    def card(self):
        card = chapter_card(9, r"Treatments that harm", r"Can talking make people worse?",
                            lit={2000: r"Mayou et al.", 2007: r"Lilienfeld", 2013: r"Petrosino et al."}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter nine. Treatments that harm."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def list_(self):
        head = heading(r"Good intentions, \ bad outcomes")
        data = (
            (r"debriefing", r"one session after a trauma, \ retelling it in detail: \ no prevention of PTSD, \ and in a "
                            r"three-year follow-up those debriefed did worse", AUTH),
            (r"Scared Straight", r"young offenders taken to prisons to be confronted by inmates: \ randomized trials "
                                 r"found more offending afterwards", AUTH),
            (r"recovered-memory techniques", r"hypnosis and guided imagery to ``recover'' abuse: \ they can create "
                                             r"false memories (Part 21)", SYMP),
            (r"conversion therapy", r"attempts to change sexual orientation: \ no evidence that it works, \ and "
                                    r"evidence of harm; \ professional bodies oppose it", PERSON),
        )
        rows = VGroup()
        for what, how, c in data:
            rows.add(VGroup(word_chip(what, color=c, font_size=17, width=4.0), wrapped_label(how, 8.0, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.0, 0])
        tag = published_tag(r"Mayou, \ Ehlers \& Hobbs (2000); \ Petrosino et al.\ (2013); \ Lilienfeld (2007)")
        with self.voiceover(
            "Therapy can also harm. <bookmark mark='a'/> Psychological debriefing: a single session soon after a "
            "trauma, retelling it in detail. Trials found it didn't prevent post-traumatic stress, and in a "
            "three-year follow-up of road-accident victims, those debriefed did worse. <bookmark mark='b'/> Scared "
            "Straight: young offenders taken into prisons to be confronted by inmates. Randomized trials found more "
            "offending afterwards, not less. <bookmark mark='c'/> Recovered-memory techniques: hypnosis and guided "
            "imagery used to recover memories of abuse. As Part 21 showed, they can create false ones. "
            "<bookmark mark='d'/> And conversion therapy, attempts to change sexual orientation. There's no "
            "evidence that it works, there's evidence of harm, and professional bodies oppose it. Scott Lilienfeld "
            "collected such cases in 2007."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def why(self):
        head = heading(r"Why harm goes unseen")
        rows = rows_of([
            (r"everyone improves anyway (chapter two), \ so a harmful treatment can look helpful without a control", WHITE),
            (r"a minority of clients get worse in any therapy, \ often put at 5 to 10\%, \ and therapists tend not to "
             r"notice", AUTH),
            (r"trials rarely measure harms with the care they give to benefits", PERSON),
            (r"so the same tools that test benefit, \ controls and monitoring, \ are needed to find harm", YOU),
        ], 12.4, 24, 0.48).move_to([0, -0.3, 0])
        with self.voiceover(
            "Why does harm go unseen? <bookmark mark='a'/> Because everyone improves anyway, as chapter two showed, "
            "a harmful treatment can look helpful without a control group. <bookmark mark='b'/> A minority of clients "
            "get worse in any therapy, often put at five to ten percent, and therapists tend not to notice. "
            "<bookmark mark='c'/> And trials rarely measure harms with the care they give to benefits. "
            "<bookmark mark='d'/> So the same tools that test benefit, controls and monitoring, are needed to find "
            "harm."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def detect(self):
        d = load("categories")
        head = heading(r"Could a clinic see the harm?")
        A = axes([0.3, 2.7], [0, 0.4], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 0.1, 0.2, 0.3],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"share of clients", center=[-3.6, 0.5, 0], font_size=13)
        b = VGroup()
        for i, (a, c) in enumerate((("none", GREY_B), ("harmful", AUTH))):
            for j, (k, col) in enumerate((("recovered", GOOD), ("deteriorated", AUTH))):
                x = i + 1 + (j - 0.5) * 0.36
                b.add(bars(A.ax, [x], [d[f"{a}_{k}"]], col, width=0.3))
        names = VGroup(wrapped_label(r"no treatment", 1.6, 13, GREY_A).next_to(A.ax.c2p(1, 0), DOWN, buff=0.15),
                       wrapped_label(r"a therapy that harms", 1.6, 13, AUTH).next_to(A.ax.c2p(2, 0), DOWN, buff=0.15))
        key = VGroup(label(r"recovered", font_size=12, color=GOOD), label(r"deteriorated", font_size=12, color=AUTH))
        key.arrange(RIGHT, buff=0.4).next_to(names, DOWN, buff=0.2)
        rows = rows_of([
            (r"Psyche: \ a therapy that leaves people 3 points worse than no treatment", WHITE),
            (rf"reliable deterioration rises from {pct(d['none_deteriorated'])} to "
             rf"{pct(d['harmful_deteriorated'])}: \ a handful of clients in a busy caseload", AUTH),
            (rf"and {pct(d['harmful_recovered'])} of its clients still count as recovered, \ because people come at "
             rf"their worst", GOOD),
            (r"one therapist, \ watching clients one at a time, \ would see mostly improvement: \ harm shows only "
             r"against a control", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.therapy\_trial}, \ \texttt{jt\_categories}")
        with self.voiceover(
            "Could a clinic see the harm for itself? <bookmark mark='a'/> Psyche gives a therapy that leaves people "
            "three points worse than no treatment at all. <bookmark mark='b'/> Reliable deterioration rises from "
            "about two percent to about six: a handful of clients in a busy caseload. <bookmark mark='c'/> And about "
            "one in six of its clients still count as recovered, because people come at their worst. "
            "<bookmark mark='d'/> One therapist, watching clients one at a time, would see mostly improvement. Harm "
            "shows only against a control."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
