from __future__ import annotations

from videos.philosophy.philosophy1.common import *  # noqa: F403


class Axial(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"From myth to argument", r"What changed when people began to give reasons?",
                            lit=(-585, -500, -480, -400), part=PART)
        with self.voiceover("Chapter one. From myth to argument."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axial()
        self.thales()
        self.criticism()
        self.sophists()

    def axial(self):
        cols = [(r"Greece", [r"Thales", r"Heraclitus", r"Parmenides", r"Socrates"], P.CLAIM),
                (r"India", [r"the Upaniṣads", r"the Buddha", r"Mahāvīra", r"the debaters of the \textit{vāda}"],
                 P.AGENT),
                (r"China", [r"Confucius", r"Laozi", r"Mozi", r"Zhuangzi"], P.TRUE)]
        g = VGroup()
        for name, people, col in cols:
            head = label(name, font_size=34, color=col)
            rows = VGroup(*[label(p, font_size=26, color=WHITE) for p in people]).arrange(DOWN, buff=0.22)
            box = RoundedRectangle(width=3.6, height=3.4, corner_radius=0.16, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.05)
            inner = VGroup(head, rows).arrange(DOWN, buff=0.3).move_to(box)
            g.add(VGroup(box, inner))
        g.arrange(RIGHT, buff=0.5).move_to([0, -0.4, 0])
        span = label(r"roughly 800 to 200 BCE", font_size=28, color=HIST).to_edge(UP, buff=0.5)
        hc = history_card(1949, r"Karl Jaspers", r"`the Axial Age': a disputed label for a real convergence",
                          width=5.2, color=HIST, font_size=20).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Between roughly 800 and 200 years before our era, in three places that barely knew of one another, "
            "people began to do something new. <bookmark mark='a'/>In the Greek cities of the Aegean: Thales, "
            "Heraclitus, Parmenides, Socrates. <bookmark mark='b'/>In India: the Upaniṣads, the Buddha, Mahāvīra, "
            "and a culture of formal public debate. <bookmark mark='c'/>In China: Confucius, the Daoists, and the "
            "Mohists, who argued about argument itself. <bookmark mark='d'/>In 1949 the philosopher Karl Jaspers "
            "called this the Axial Age. Historians dispute how tidy the label is, but the convergence is real: "
            "in each place, a claim began to need reasons."
        ) as vo:
            self.play(FadeIn(span))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(g[k], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(hc, shift=LEFT * 0.2))
        self.clear_scene()

    def thales(self):
        hc = history_card(r"c.\ 585 BCE", r"Thales of Miletus", r"everything is water; credited (by Herodotus) "
                          r"with predicting an eclipse", width=5.6, color=HIST).to_corner(UL, buff=0.4)
        myth = VGroup(label(r"Why is there rain?", font_size=30, color=GREY_A),
                      label(r"because Zeus sends it", font_size=32, color=BAD)).arrange(DOWN, buff=0.2)
        nat = VGroup(label(r"Why is there rain?", font_size=30, color=GREY_A),
                     label(r"because water rises and falls", font_size=32, color=OK)).arrange(DOWN, buff=0.2)
        pair = VGroup(myth, nat).arrange(RIGHT, buff=1.6).move_to([0, -0.4, 0])
        tags = VGroup(label(r"an authority: \ accept it", font_size=24, color=BAD).next_to(myth, DOWN, buff=0.4),
                      label(r"a mechanism: \ check it, criticize it", font_size=24, color=OK).next_to(nat, DOWN,
                                                                                               buff=0.4))
        with self.voiceover(
            "The tradition usually starts with Thales of Miletus, early in the sixth century before our era. "
            "<bookmark mark='a'/>He is said to have held that everything is water, and Herodotus credits him with "
            "predicting an eclipse. <bookmark mark='b'/>The content matters less than the form. Compare two answers "
            "to 'why is there rain?' <bookmark mark='c'/>One cites an authority you can only accept. The other names "
            "a mechanism anyone can check, and argue with."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(pair))
            vo.wait_until("c")
            self.play(FadeIn(tags))
        self.clear_scene()

    def criticism(self):
        chain = VGroup(
            VGroup(label(r"Thales", font_size=30, color=P.CLAIM), label(r"everything is water", font_size=22,
                                                                          color=GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(label(r"Anaximander", font_size=30, color=P.CLAIM),
                   label(r"no: \ the boundless, \textit{apeiron}", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(label(r"Anaximenes", font_size=30, color=P.CLAIM), label(r"no: \ air", font_size=22,
                                                                              color=GREY_A)).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=1.4).move_to([0, 1.0, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.2, color=GREY_B) for a, b in zip(chain, chain[1:])])
        q = quote_card(r"The early Greek philosophers \dots\ invented the tradition of critical discussion.",
                       r"paraphrasing Karl Popper, `Back to the Presocratics' (1958)", width=9.6, font_size=26)
        q.move_to([0, -1.6, 0])
        thesis = label(r"the series' thesis: \ a reason is something anyone can check", font_size=30, color=GOAL)
        thesis.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And then something even newer happened. <bookmark mark='a'/>Thales' own student, Anaximander, disagreed "
            "with him, and said the origin was not water but something boundless. Anaximenes, in turn, said air. "
            "Students argued with their teachers, in public, and were remembered for it. <bookmark mark='b'/>Karl "
            "Popper argued that this, more than any doctrine, was the Greek invention: a tradition of criticism. "
            "<bookmark mark='c'/>That is the thread this series follows. A reason is something anyone can check. "
            "And the oldest question about checking reasons is the one Leibniz asked: could the checking be "
            "mechanical? To answer it, we first need to say exactly what an argument is."
        ) as vo:
            self.play(FadeIn(chain[0]))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(chain[1]))
            self.play(GrowArrow(arrows[1]), FadeIn(chain[2]))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(thesis))
        self.clear_scene()

    def sophists(self):
        hc = history_card(r"c.\ 490--420 BCE", r"Protagoras of Abdera", r"`man is the measure of all things'; "
                          r"famed for making the weaker argument the stronger", width=5.8, color=HIST)
        hc.to_corner(UL, buff=0.4)
        two = VGroup(
            VGroup(label(r"for", font_size=30, color=OK), label(r"good and bad are the same", font_size=24)).arrange(
                DOWN, buff=0.15),
            VGroup(label(r"against", font_size=30, color=BAD), label(r"good and bad differ", font_size=24)).arrange(
                DOWN, buff=0.15)).arrange(RIGHT, buff=1.8).move_to([0, -0.2, 0])
        src = label(r"the \textit{Dissoi Logoi}, `Twofold Arguments' (c.\ 400 BCE)", font_size=24, color=GREY_A)
        src.next_to(two, UP, buff=0.4)
        gap = label(r"persuasive \ $\neq$ \ valid", font_size=40, color=GOAL).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Criticism had a shadow. In fifth-century Athens, teachers called Sophists trained young men to win "
            "arguments, for a fee. <bookmark mark='a'/>Protagoras, the most famous, held that man is the measure of "
            "all things, and was said to be able to make the weaker argument the stronger. <bookmark mark='b'/>A "
            "surviving teaching text, the Twofold Arguments, argues both sides of every question: that good and bad "
            "are the same, and that they differ. <bookmark mark='c'/>If skill can defend anything, how do we tell a "
            "good argument from a merely persuasive one? Plato's answer was dialectic, the patient testing of "
            "definitions. Aristotle's was logic: a test of an argument's form that does not care who is speaking, or "
            "how well. That test is the next chapter."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(src), FadeIn(two))
            vo.wait_until("c")
            self.play(Write(gap))
        self.clear_scene()
