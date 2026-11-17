from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Eeg(VoiceoverScene):
    def construct(self):
        self.card()
        self.depth()
        self.dip()

    def card(self):
        card = chapter_card(9, r"EEG and MEG", r"What can milliseconds tell that seconds cannot?", lit=(), part=PART,
                            scale=("brain",), marr=("how",))
        with self.voiceover("Chapter nine. EEG and MEG."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def depth(self):
        head = heading(r"Three analyses, \ beyond the average")
        items = [
            (r"ERPs", r"average many trials time-locked to an event; \ noise falls with the square root of the count, "
                      r"\ as Part 8 showed; \ measure a component's amplitude or latency in a window", SYMP),
            (r"time-frequency", r"wavelets give power at each frequency over time: \ alpha (about 10 Hz) falls when "
                                r"attention is engaged, \ theta and gamma track memory and binding", MODEL),
            (r"source estimation", r"from scalp voltages back to sources is ill-posed (Part 8's silent sources); \ "
                                   r"priors such as minimum norm or beamforming choose one answer among many", PERSON),
            (r"MEG", r"the magnetic fields of the same currents: \ less blurred by the skull, \ blind to radial sources",
             GOOD),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 21, width=3.4), wrapped_label(what, 8.6, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        tag = published_tag(r"Luck (2014)")
        with self.voiceover(
            "EEG and MEG trade space for time. <bookmark mark='a'/> ERPs average many trials locked to an event. The "
            "noise falls with the square root of the count, as Part 8 showed, and a component is measured by its "
            "amplitude or latency in a window of time. <bookmark mark='b'/> Time-frequency analysis gives the power at "
            "each frequency over time. Alpha, around ten cycles a second, falls when attention is engaged. "
            "<bookmark mark='c'/> Source estimation runs from scalp voltages back to sources. It's ill-posed, as "
            "Part 8's silent sources showed, so a prior chooses one answer among many. <bookmark mark='d'/> And MEG "
            "records the magnetic fields of the same currents, less blurred by the skull. Every one of these has its "
            "own forks, and the most common is the window."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def dip(self):
        d = load("erp")
        head = heading(r"Choosing the window from the answer")
        A = axes([0.3, 3.7], [0, 0.5], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.25, 0.5],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"false positives", center=[-3.6, 0.3, 0], font_size=12)
        b = bars(A.ax, [1, 2, 3], [d["a_priori"], d["double_dip"], d["orthogonal"]], [GOOD, AUTH, GOOD], width=0.6)
        five = DashedLine(A.ax.c2p(0.3, 0.05), A.ax.c2p(3.7, 0.05), color=GREY_B, stroke_width=1.5)
        names = VGroup(*[wrapped_label(t, 1.4, 11, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"window fixed in advance", GOOD), (r"window at the difference's peak", AUTH),
                                    (r"window at the average's peak", GOOD)))])
        rows = rows_of([
            (r"24 people, \ two conditions with no difference at all, \ 2,000 simulated studies", WHITE),
            (rf"test a window fixed in advance: \ {100 * d['a_priori']:.0f}\% false positives, \ as promised", GOOD),
            (rf"look at the grand-average difference, \ put the window on its peak, \ then test: \ "
             rf"{100 * d['double_dip']:.0f}\%", AUTH),
            (rf"choose the window from the average of both conditions, \ which knows nothing of their difference: \ "
             rf"{100 * d['orthogonal']:.0f}\%", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.erp\_windows}")
        with self.voiceover(
            "Here's the most common fork in ERP research. <bookmark mark='a'/> Twenty-four people, two conditions "
            "with no difference at all, and two thousand simulated studies. <bookmark mark='b'/> Test a window fixed "
            "in advance, and five percent are false positives, as promised. <bookmark mark='c'/> Now look at the "
            "grand-average difference, put the window on its peak, and test there. Forty-five percent. It's Part 8's "
            "circular analysis, in time. <bookmark mark='d'/> Choose the window from the average of both conditions, "
            "which knows nothing about their difference, and it's back to five percent. Choose windows from prior "
            "studies, from an independent localizer, or from a collapsed average."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(five))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(b[2]))
        self.clear_scene()
