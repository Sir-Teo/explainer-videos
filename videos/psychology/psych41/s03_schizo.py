from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


class Schizo(VoiceoverScene):
    def construct(self):
        self.card()
        self.symptoms()
        self.course()

    def card(self):
        card = chapter_card(2, r"Schizophrenia", r"What is it, \ and how does it unfold?",
                            lit={1908: r"Bleuler", 1963: r"Rosenthal"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter two. Schizophrenia."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def symptoms(self):
        head = heading(r"Three kinds of symptom")
        cols = VGroup()
        for name, c, items in (
                (r"positive", AUTH, [r"hallucinations, \ most often voices", r"delusions: \ fixed false beliefs",
                                     r"disorganized speech and behaviour"]),
                (r"negative", SYMP, [r"little motivation", r"flattened expression", r"withdrawal, \ less speech"]),
                (r"cognitive", MODEL, [r"working memory", r"attention", r"processing speed"])):
            chip = word_chip(name, color=c, font_size=24, width=3.4)
            body = VGroup(*[wrapped_label(t, 3.6, 19, WHITE) for t in items]).arrange(DOWN, aligned_edge=LEFT,
                                                                                        buff=0.22)
            cols.add(VGroup(chip, body).arrange(DOWN, aligned_edge=LEFT, buff=0.35))
        cols.arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, 0.6, 0])
        rows = rows_of([
            (r"``positive'' means added to experience, \ ``negative'' taken away; \ neither means good or bad", GREY_A),
            (r"the name, \ from Bleuler in 1908, \ means a split between thought, \ feeling and action, \ not a split "
             r"personality", YOU),
        ], 12.4, 21, 0.3).move_to([0, -2.4, 0])
        with self.voiceover(
            "Schizophrenia has three kinds of symptom. <bookmark mark='a'/> Positive symptoms are added to "
            "experience: hallucinations, most often voices; delusions, fixed false beliefs; and disorganized speech "
            "and behaviour. <bookmark mark='b'/> Negative symptoms take something away: motivation, expression, "
            "speech, contact with others. <bookmark mark='c'/> And cognitive symptoms: working memory, attention and "
            "speed of thought, often the strongest predictors of how life goes. <bookmark mark='d'/> Positive and "
            "negative don't mean good and bad. And the name, coined by Eugen Bleuler in 1908, means a split between "
            "thought, feeling and action. It doesn't mean a split personality."
        ) as vo:
            self.play(FadeIn(head))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(rows))
        self.clear_scene()

    def course(self):
        head = heading(r"Course, \ and four sisters")
        A = axes([12, 40], [0, 1], x_length=5.4, y_length=2.6, xticks=[15, 20, 25, 30, 35], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age", ylabel=r"onsets", center=[-3.5, 0.8, 0], font_size=13)
        a = np.linspace(12, 40, 200)
        dens = np.exp(-0.5 * ((a - 22) / 4.5) ** 2)
        onset = curve(A.ax, a, 0.9 * dens, PERSON, stroke_width=3)
        lm = label(r"schematic", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.3)
        sisters = VGroup(*[little_person(0.55, color=c) for c in (AUTH, SYMP, SYMP, MODEL)]).arrange(RIGHT, buff=0.3)
        sisters.move_to([-3.5, -2.3, 0])
        s_l = label(r"identical quadruplets: \ same genes, \ four courses", font_size=15, color=GREY_A).next_to(
            sisters, DOWN, buff=0.12)
        rows = rows_of([
            (r"about one person in 200 to 300 is diagnosed over a lifetime; \ onset is usually in late adolescence "
             r"or early adulthood", WHITE),
            (r"the course varies widely: \ some people recover fully, \ many have episodes with good periods "
             r"between, \ some have lasting difficulties", GOOD),
            (r"Rosenthal, \ 1963: \ identical quadruplets, \ all four diagnosed, \ with very different severity and "
             r"outcomes", SYMP),
            (r"shared genes set a risk; \ they did not set the course", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Rosenthal (1963)")
        with self.voiceover(
            "How does it unfold? <bookmark mark='a'/> Somewhere around one person in two or three hundred is "
            "diagnosed over a lifetime, and onset is usually in late adolescence or early adulthood. "
            "<bookmark mark='b'/> The course varies widely. Some people recover fully. Many have episodes with good "
            "periods between. Some have lasting difficulties. <bookmark mark='c'/> In 1963 the psychologist David "
            "Rosenthal described identical quadruplets in the United States, all four diagnosed with schizophrenia, "
            "with very different severity and outcomes. <bookmark mark='d'/> Shared genes set a risk. They didn't "
            "set the course."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(onset), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(sisters), FadeIn(s_l))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
