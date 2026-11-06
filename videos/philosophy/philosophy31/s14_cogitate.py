from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Cogitate(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"The theories, tested", r"Can rival theories agree in advance on what would refute "
                                                          r"them?", lit=(2025,), part=PART)
        with self.voiceover("Chapter thirteen. The theories, tested."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.bet()
        self.design()
        self.results()

    def bet(self):
        head = label(r"A bet, \ and an adversarial collaboration", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"1998", r"Christof Koch bets David Chalmers a case of wine that a neural signature of "
                          r"consciousness will be found within 25 years", HIST),
                (r"2019", r"the Templeton Foundation funds `structured adversarial collaborations': \ rival "
                          r"theorists design one experiment together", FUNC),
                (r"the rule", r"each side registers in advance what results would count against it", GOAL),
                (r"2023", r"Koch concedes the bet, \ and pays", HIST)]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Theories of consciousness have usually been tested by their own proponents. That began to change "
            "with a bet. <bookmark mark='a'/>In 1998 the neuroscientist Christof Koch bet Chalmers a case of wine "
            "that a clear neural signature of consciousness would be found within twenty five years. "
            "<bookmark mark='b'/>In 2019 the Templeton World Charity Foundation began funding structured "
            "adversarial collaborations: the proponents of rival theories design one experiment together. "
            "<bookmark mark='c'/>The rule is that each side says in advance, in public, which results would count "
            "against its own theory. <bookmark mark='d'/>The first such collaboration, called Cogitate, pitted "
            "integrated information against the global workspace. In June 2023, when its first results were "
            "presented, Koch conceded the bet."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def design(self):
        head = label(r"The Cogitate design", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        faces = VGroup(*[VGroup(RoundedRectangle(width=1.3, height=1.3, corner_radius=0.15, color=c,
                                                 fill_opacity=0.15), label(t, font_size=16, color=c))
                         for t, c in ((r"face", FEEL), (r"object", SIG), (r"letter", FUNC), (r"symbol", PRED))]
                       ).arrange(RIGHT, buff=0.4).move_to([0, 1.4, 0])
        durs = VGroup(*[VGroup(Rectangle(width=1.2 * w, height=0.22, color=GREY_B, fill_color=GREY_B,
                                         fill_opacity=0.6), label(f"{w}\\,s", font_size=16, color=GREY_A))
                        .arrange(RIGHT, buff=0.2) for w in (0.5, 1.0, 1.5)]).arrange(DOWN, buff=0.15,
                                                                                    aligned_edge=LEFT).move_to(
            [0, -0.2, 0])
        rows = stack([(r"pictures shown for half a second, \ one second, \ or a second and a half", GREY_A),
                      (r"three methods: \ fMRI, \ MEG, \ intracranial EEG; \ several laboratories; \ predictions "
                       r"registered in advance", FUNC),
                      (r"Melloni et al. \ (2021, \ 2023); \ results: \ Cogitate Consortium, \ \textit{Nature} \ "
                       r"(2025)", HIST)], font_size=20, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The design was simple to state. <bookmark mark='a'/>People looked at pictures of faces, objects, "
            "letters and meaningless symbols, <bookmark mark='b'/>each shown for half a second, a second, or a "
            "second and a half, so that the duration of the experience could be tracked in the brain. "
            "<bookmark mark='c'/>Brain activity was recorded with three methods, functional MRI, MEG and electrodes "
            "inside the skull in epilepsy patients, in several laboratories, with the predictions of each theory "
            "registered before any data were collected. <bookmark mark='d'/>The protocol was published by Lucia "
            "Melloni and colleagues, and the results appeared in Nature in 2025."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in faces], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(durs), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def results(self):
        head = label(r"What each theory predicted, \ and what was found", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        hd = [r"\text{question}", r"\text{IIT predicted}", r"\text{GNWT predicted}", r"\text{found}"]
        rows = [(r"where is the content?", r"posterior cortex", r"prefrontal cortex too",
                 r"posterior cortex; \ prefrontal only for some features"),
                (r"how long?", r"sustained posterior activity, \ the whole time", r"ignition at onset, \ and again "
                                                                                  r"at offset",
                 r"sustained posterior responses; \ no ignition at offset"),
                (r"what connects?", r"sustained synchrony within posterior cortex", r"brief long-range "
                                                                                    r"synchrony",
                 r"no sustained posterior synchrony")]
        cells = [[label(a, font_size=17, color=WHITE), wrapped_label(b, 3.0, 16, FUNC), wrapped_label(c, 3.0, 16, PRED),
                  wrapped_label(f, 3.4, 16, GOAL)] for a, b, c, f in rows]
        grid = ValueGrid(hd, cells, col_w=[2.6, 3.3, 3.3, 3.7], cell_h=1.0, font_size=18).move_to([0, -0.2, 0])
        foot = stack([(r"the paper: \ some predictions of each confirmed, \ `key tenets of both' challenged", GOAL),
                      (r"each side found its theory bruised but standing: \ a first, \ not a verdict", GREY_A)],
                     font_size=19, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The results challenged both. <bookmark mark='a'/>Where is the content of experience? IIT predicted the "
            "posterior cortex; the workspace theory predicted that prefrontal cortex would carry it too. Content "
            "was found in posterior regions, and in prefrontal cortex only for some of its features. "
            "<bookmark mark='b'/>How long does it last? IIT predicted activity sustained in the posterior cortex "
            "for as long as the experience lasts. The workspace theory predicted ignition when the picture "
            "appears, and again when it disappears. Posterior responses were sustained; ignition at the offset "
            "was not found. <bookmark mark='c'/>What connects? IIT predicted sustained synchronization within the "
            "posterior cortex; it was not found. <bookmark mark='d'/>The paper's own summary: some predictions of "
            "each theory were confirmed, and key tenets of both were substantially challenged. Each side found its "
            "theory bruised but standing. It was a first, not a verdict, and further collaborations are testing "
            "other theories the same way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
