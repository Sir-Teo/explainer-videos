from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Progress(VoiceoverScene):
    def construct(self):
        self.card()
        self.attention()
        self.meta()
        self.what_counts()

    def card(self):
        card = chapter_card(12, r"Attention, \ metacognition and progress", r"What would count as progress?",
                            lit={2007: r"Koch \& Tsuchiya", 2012: r"Fleming \& Dolan", 2022: r"Seth \& Bayne"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter twelve. Attention, metacognition and progress."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def attention(self):
        head = heading(r"Attention is not consciousness")
        grid = VGroup()
        cells = [(r"attended and conscious", r"most of ordinary seeing", SEEN),
                 (r"attended, \ not conscious", r"an invisible stimulus can still draw or use attention", UNSEEN),
                 (r"conscious, \ barely attended", r"the gist of a scene glimpsed while busy elsewhere", GNW),
                 (r"neither", r"the gorilla, \ for half the watchers", LOST)]
        for t, s, c in cells:
            b = RoundedRectangle(corner_radius=0.12, width=5.2, height=1.6, stroke_color=c, stroke_width=2,
                                 fill_color=BLACK, fill_opacity=0.5)
            grid.add(VGroup(b, VGroup(label(t, font_size=23, color=c), wrapped_label(s, 4.8, 19, WHITE)).arrange(
                DOWN, buff=0.15).move_to(b)))
        grid.arrange_in_grid(rows=2, cols=2, buff=0.3).move_to([0, 0.6, 0])
        foot = wrapped_label(r"Koch and Tsuchiya, \ 2007: \ the two can be dissociated both ways, \ so a theory of "
                             r"attention is not yet a theory of consciousness", 12.0, 23, MODEL).to_edge(DOWN,
                                                                                                         buff=0.75)
        tag = published_tag(r"Koch \& Tsuchiya (2007)")
        with self.voiceover(
            "Two neighbouring ideas are often confused with consciousness. The first is attention. "
            "<bookmark mark='a'/> Most of ordinary seeing is attended and conscious. But an invisible stimulus can "
            "still draw attention, or be used by it, as masked cues do. You can be conscious of the gist of a scene "
            "you barely attended to while busy with something else. And the gorilla was neither. "
            "<bookmark mark='b'/> Christof Koch and Naotsugu Tsuchiya argued in 2007 that the two dissociate in both "
            "directions, so a theory of attention, like Part 18's, is not yet a theory of consciousness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.7), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def meta(self):
        head = heading(r"Metacognition: \ knowing that you see")
        rows = rows_of([
            (r"metacognition: \ how well confidence tracks accuracy; \ measured by Part 12's meta-$d'$, \ and in "
             r"Part 25 as the balance of evidence", HOT),
            (r"it varies between people at the same accuracy, \ and with the anterior prefrontal cortex \ (Fleming "
             r"and colleagues, \ 2010)", WHITE),
            (r"higher-order theories say metacognition is close to what makes a state conscious; \ the workspace "
             r"and integrated information say it is a separate, \ later step", MODEL),
            (r"blindsight is the test case: \ accurate guesses, \ wagers that do not follow them", UNSEEN),
        ], 12.0, 24, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Fleming, \ Weil, \ Nagy, \ Dolan \& Rees (2010); \ Fleming \& Dolan (2012)")
        with self.voiceover(
            "The second neighbour is metacognition. <bookmark mark='a'/> It's how well your confidence tracks your "
            "accuracy, measured by Part 12's meta d prime, and modelled in Part 25 as the balance of evidence. "
            "<bookmark mark='b'/> People differ in it at the same level of accuracy, and in 2010 Stephen Fleming and "
            "colleagues linked those differences to the anterior prefrontal cortex. <bookmark mark='c'/> For "
            "higher-order theories, metacognition is close to what makes a state conscious; for the workspace and "
            "integrated information, it's a separate, later step. <bookmark mark='d'/> Blindsight is the test case: "
            "accurate guesses, with wagers that don't follow them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def what_counts(self):
        head = heading(r"What would count as progress")
        rows = rows_of([
            (r"theories that make risky predictions, \ agreed in advance, \ and some of them fail", GNW),
            (r"measures that do not depend on report: \ no-report designs, \ the complexity index", SEEN),
            (r"interventions, \ not just correlations: \ lesions, \ stimulation, \ anaesthetics", RPT),
            (r"the same answers from different methods, \ labs and species", IIT),
            (r"and a way to judge hard cases: \ infants, \ unresponsive patients, \ animals, \ machines \ (Part 60)",
             HOT),
        ], 12.0, 25, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Seth \& Bayne (2022)")
        with self.voiceover(
            "So what would count as progress? <bookmark mark='a'/> Theories that make risky predictions, agreed in "
            "advance, some of which then fail: chapter nine was a start. <bookmark mark='b'/> Measures that don't "
            "depend on report, like no-report designs and the complexity index. <bookmark mark='c'/> Interventions, "
            "not just correlations: lesions, stimulation, anaesthetics. <bookmark mark='d'/> The same answer from "
            "different methods, laboratories and species. <bookmark mark='e'/> And in the end, a principled way to "
            "judge the hard cases: infants, unresponsive patients, other animals, and machines, the subject of "
            "Part 60."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
