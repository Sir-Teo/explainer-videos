from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403


class Reading(VoiceoverScene):
    def construct(self):
        self.card()
        self.abstract()
        self.checklist()

    def card(self):
        card = chapter_card(12, r"Reading an SEM paper", r"What should a reader ask?", lit=(), part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter twelve. Reading an SEM paper."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def abstract(self):
        head = heading(r"An abstract, \ invented for practice")
        box = RoundedRectangle(corner_radius=0.12, width=12.6, height=2.5, stroke_color=GREY_B, stroke_width=1.5)
        box.move_to([0, 1.3, 0])
        text = wrapped_label(r"``In 412 employees surveyed once, \ a structural equation model showed that workload "
                             r"leads to burnout, \ which leads to turnover intention. \ The model fit well (CFI = 0.96, "
                             r"\ RMSEA = 0.05), \ and burnout fully mediated the effect of workload.''", 12.0, 22,
                             WHITE).move_to(box)
        notes = rows_of([
            (r"surveyed once: \ ``leads to'' is a direction that one wave of data cannot show (chapters 9 and 10)", AUTH),
            (r"fit well: \ by fixed cut-offs, \ which pass wrong models (chapter 5); \ and the reversed chain fits "
             r"identically", AUTH),
            (r"fully mediated: \ the mediator was not manipulated, \ and here nothing was (chapter 8)", AUTH),
            (r"what it does show: \ the three measures are related as a chain would imply", GOOD),
        ], 12.4, 20, 0.3).move_to([0, -1.6, 0])
        tag = label(r"invented for this chapter", font_size=14, color=GREY_B).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here is an abstract, invented for practice, in a shape you'll meet often. Four hundred and twelve "
            "employees, surveyed once. Workload leads to burnout, which leads to turnover intention. The model fit "
            "well, and burnout fully mediated the effect. <bookmark mark='a'/> Surveyed once: leads to is a direction "
            "that one wave of data can't show. <bookmark mark='b'/> Fit well: by fixed cut-offs, which pass wrong "
            "models, and the reversed chain fits identically. <bookmark mark='c'/> Fully mediated: the mediator wasn't "
            "manipulated, and here nothing was. <bookmark mark='d'/> What it does show: the three measures are "
            "related the way a chain would imply. So would other diagrams."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box), FadeIn(text), FadeIn(tag))
            for m, r in zip("abcd", notes):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def checklist(self):
        head = heading(r"Eight questions")
        qs = [
            r"Is the diagram drawn, \ with every fixed and free parameter, \ and are the degrees of freedom given?",
            r"Which equivalent models fit as well, \ and why were they set aside?",
            r"Were the data collected over time, \ or in an experiment, \ for the arrows that need it?",
            r"Is the $\chi^2$ reported, \ and fit judged for this model, \ not by fixed cut-offs?",
            r"Was the model changed after looking at the fit, \ and is that said?",
            r"Was invariance tested before groups were compared?",
            r"Are the measures reliable, \ and is measurement modelled?",
            r"Are the data and code open, \ so another analyst can fit a different diagram?",
        ]
        rows = VGroup(*[VGroup(label(rf"{k + 1}", font_size=24, color=YOU), wrapped_label(q, 11.4, 20, WHITE))
                        .arrange(RIGHT, buff=0.35) for k, q in enumerate(qs)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([0, -0.3, 0])
        with self.voiceover(
            "Eight questions for any paper with a path diagram. <bookmark mark='a'/> Is the diagram drawn, with every "
            "fixed and free parameter, and the degrees of freedom? Which equivalent models fit as well, and why were "
            "they set aside? Were the data collected over time, or in an experiment, for the arrows that need it? Is "
            "the chi-square reported, and fit judged for this model, not by fixed cut-offs? Was the model changed "
            "after looking at the fit, and does the paper say so? Was invariance tested before groups were compared? "
            "Are the measures reliable, and is measurement modelled? And are the data and code open, so another "
            "analyst can fit a different diagram?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[1:]], lag_ratio=0.9), run_time=24.0)
        self.clear_scene()
