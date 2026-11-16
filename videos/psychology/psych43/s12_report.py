from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Report(VoiceoverScene):
    def construct(self):
        self.card()
        self.layout()
        self.checklist()

    def card(self):
        card = chapter_card(11, r"The report", r"What does the paper say?", lit={2022: r"Chambers \& Tzavella"},
                            part=PART, scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter eleven. The report."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def layout(self):
        c, v = load("confirm"), load("verdict")
        head = heading(r"A registered report")
        stage1 = VGroup(word_chip(r"stage 1", color=SYMP, font_size=20, width=2.4),
                        wrapped_label(r"introduction, \ methods, \ planned analysis, \ power: \ reviewed and accepted "
                                      r"before the data exist", 4.6, 18, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        stage2 = VGroup(word_chip(r"stage 2", color=GOOD, font_size=20, width=2.4),
                        wrapped_label(r"results as registered, \ deviations listed, \ exploratory section labelled, \ "
                                      r"data and code linked", 4.6, 18, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(stage1, stage2).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([-3.6, 0.0, 0])
        vo_line = f"{-100 * c['vo_est']:.0f}"
        ed_line = f"{c['ed_est']:.2f}"
        abstract = rows_of([
            (r"abstract, \ as this part would write it:", GREY_A),
            (rf"in 22 laboratories, \ describing a face reduced correct line-up identifications by {vo_line} per 100, "
             rf"\ a smaller effect than originally reported", GOOD),
            (rf"in 23 laboratories, \ the depletion manipulation had no detectable effect on self-control, \ $g = "
             rf"{ed_line}$, \ and effects as large as the original's were ruled out", AUTH),
            (r"both analyses were registered in advance; \ data and code are open", MODEL),
        ], 6.0, 19, 0.36).move_to([3.4, 0.0, 0])
        tag = published_tag(r"Chambers \& Tzavella (2022)")
        with self.voiceover(
            f"Last, the report. <bookmark mark='a'/> A registered report comes in two stages. In stage one, the "
            f"introduction, methods, planned analysis and power are reviewed and accepted before the data exist. "
            f"<bookmark mark='b'/> In stage two come the results as registered, any deviations listed, a labelled "
            f"exploratory section, and links to the data and code. Chris Chambers and Loukia Tzavella reviewed the "
            f"format's first decade in 2022. <bookmark mark='c'/> Here's the abstract this part would write. In "
            f"twenty-two laboratories, describing a face reduced correct line-up identifications by {vo_line} per "
            f"hundred, a smaller effect than first reported. In twenty-three laboratories, the depletion manipulation "
            f"had no detectable effect on self-control, and effects as large as the original's were ruled out. Both "
            f"analyses were registered in advance, and the data and code are open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(stage1))
            vo.wait_until("b")
            self.play(FadeIn(stage2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in abstract], lag_ratio=0.7), run_time=6.0)
        self.clear_scene()

    def checklist(self):
        head = heading(r"Before it is sent")
        data = (
            (r"deviations", r"every change from the plan, \ with its reason and its effect on the result", AUTH),
            (r"everything", r"every registered outcome reported, \ including the dull ones", PERSON),
            (r"labels", r"exploratory results marked as exploratory, \ in the text and in the abstract", MODEL),
            (r"open", r"data, \ code and materials linked, \ with a frozen version that reproduces every number", GOOD),
            (r"who did what", r"each author's contribution, \ and any conflict of interest", SYMP),
            (r"limits", r"what the study cannot say: \ the population, \ the setting, \ the measures", YOU),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=2.8), wrapped_label(how, 9.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, -0.3, 0])
        with self.voiceover(
            "Before the report is sent, a last check. <bookmark mark='a'/> Deviations: every change from the plan, "
            "with its reason and its effect on the result. <bookmark mark='b'/> Everything: every registered outcome "
            "reported, including the dull ones. <bookmark mark='c'/> Labels: exploratory results marked as "
            "exploratory, in the text and in the abstract. <bookmark mark='d'/> Open: data, code and materials linked, "
            "with a frozen version that reproduces every number. This part's own code does that. "
            "<bookmark mark='e'/> Who did what: each author's contribution, and any conflict of interest. "
            "<bookmark mark='f'/> And limits: what the study can't say, about its population, its setting and its "
            "measures."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
