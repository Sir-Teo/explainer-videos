from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403

ERAS = [
    (1790, r"moral treatment", r"Pinel in Paris and Tuke in York unchain patients and offer work, routine and "
                               r"kindness", GOOD),
    (1850, r"the asylum", r"public asylums multiply and fill; \ custody replaces cure", GREY_A),
    (1899, r"Kraepelin", r"two great psychoses, \ told apart by their course over years: \ dementia praecox "
                         r"(later schizophrenia) and manic-depressive illness", SYMP),
    (1900, r"Freud", r"the neuroses: \ anxiety and hysteria as conflicts in the mind; \ talk as treatment", MODEL),
    (1952, r"DSM-I", r"the first American diagnostic manual: \ short prose descriptions", WHITE),
    (1961, r"anti-psychiatry", r"Szasz's \emph{The Myth of Mental Illness}: \ diagnosis as social control", AUTH),
    (1980, r"DSM-III", r"explicit criteria, \ counted symptoms, \ tested for agreement", PERSON),
]


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.timeline()

    def card(self):
        card = chapter_card(2, r"A short history of madness", r"How did suffering become diagnosis?",
                            lit={1899: r"Kraepelin", 1952: r"DSM-I", 1961: r"Szasz", 1980: r"DSM-III"}, part=PART,
                            scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter two. A short history of madness."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def timeline(self):
        head = heading(r"Two centuries in seven steps")
        line = Line([-6.4, 2.2, 0], [6.4, 2.2, 0], color=GREY_D, stroke_width=3)
        x0, x1 = 1780, 1990

        def xx(year):
            return -6.2 + 12.4 * (year - x0) / (x1 - x0)

        ticks = VGroup()
        rows = VGroup()
        for k, (yr, name, text, c) in enumerate(ERAS):
            ticks.add(VGroup(Dot([xx(yr), 2.2, 0], radius=0.07, color=c),
                             label(str(yr), font_size=13, color=GREY_B).move_to([xx(yr), 2.5 + 0.25 * (k % 2), 0])))
            rows.add(VGroup(word_chip(name, color=c, font_size=17, width=2.8), wrapped_label(text, 9.0, 18, WHITE))
                     .arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([0, -0.6, 0])
        with self.voiceover(
            "Madness is old. Its classification is young. <bookmark mark='a'/> Around 1800, moral treatment: "
            "Philippe Pinel in Paris and William Tuke in York unchained patients and offered work, routine and "
            "kindness. <bookmark mark='b'/> Through the nineteenth century, public asylums multiplied and filled, and "
            "custody replaced cure. <bookmark mark='c'/> Around 1900, Emil Kraepelin sorted the great psychoses by "
            "their course over years, into dementia praecox, later called schizophrenia, and manic-depressive "
            "illness. <bookmark mark='d'/> At the same time Sigmund Freud described the neuroses, anxiety and "
            "hysteria, as conflicts in the mind, with talk as treatment. <bookmark mark='e'/> In 1952 the first "
            "American diagnostic manual, DSM-I, gave short prose descriptions. <bookmark mark='f'/> In 1961 Thomas "
            "Szasz called mental illness a myth, and diagnosis a form of social control. <bookmark mark='g'/> And in "
            "1980 DSM-III answered the critics with explicit criteria: count the symptoms, and test whether "
            "clinicians agree."
        ) as vo:
            self.play(FadeIn(head), Create(line))
            for m, t, r in zip("abcdefg", ticks, rows):
                vo.wait_until(m)
                self.play(FadeIn(t), FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
