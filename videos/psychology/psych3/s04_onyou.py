from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403


class OnYou(VoiceoverScene):
    def construct(self):
        self.card()
        self.reading()
        self.reveal()
        self.why()

    def card(self):
        card = chapter_card(3, r"On you: \ a reading of your character", r"How accurate is this description of you?",
                            lit={1949: r"Forer's classroom demonstration"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter three. On you: a reading of your character."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def reading(self):
        d = archive.FORER_1949.data
        stage = demo_stage(13.0, 6.3, tag=r"On you", center=[0, -0.15, 0])
        ask = label(r"How well does this describe you? \ \ 0 = poorly \ \dots\ 5 = perfectly", font_size=28,
                    color=P.ACCENT).move_to([0, 2.45, 0])
        lines = VGroup(*[wrapped_label(t, 11.4, 29, WHITE) for t in d["sample"]])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([0, -0.05, 0])
        ring = countdown_ring(0.36).move_to([5.6, -2.75, 0])
        hold = label(r"settle on one number for the whole description", font_size=26, color=GREY_A)
        hold.move_to([-0.6, -2.75, 0])
        with self.voiceover(
            "Before we take scores apart, I'd like one from you. Here is a short description of a personality. "
            "Read it as if it had been written about you, after a test you had taken, and decide how well it "
            "fits: zero if it describes you poorly, five if it's perfect. <bookmark mark='a'/> You have a great "
            "need for other people to like and admire you. <bookmark mark='b'/> You have a tendency to be "
            "critical of yourself. <bookmark mark='c'/> You have a great deal of unused capacity, which you have "
            "not turned to your advantage. <bookmark mark='d'/> Disciplined and self-controlled outside, you tend "
            "to be worrisome and insecure inside. <bookmark mark='e'/> At times you have serious doubts as to "
            "whether you have made the right decision, or done the right thing. <bookmark mark='f'/> At times "
            "you are extroverted, affable, sociable, while at other times you are introverted, wary, reserved. "
            "<bookmark mark='g'/> Now settle on one number, zero to five, for the whole description."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(ask))
            for m, ln in zip("abcdef", lines):
                vo.wait_until(m)
                self.play(FadeIn(ln, shift=RIGHT * 0.15), run_time=0.8)
            vo.wait_until("g")
            self.play(FadeIn(hold), FadeIn(ring))
        self.play(ring.t.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        d = archive.FORER_1949.data
        hc = history_card(1949, r"Bertram Forer", rf"{d['n']} students take a personality test; a week "
                          r"later each is handed ``their'' result", color=P.ARCHIVE, width=7.4, font_size=26)
        hc.move_to([-3.2, 2.35, 0])
        high = d["n"] - d["below_4"]
        crowd = people_row(d["n"], [P.ACCENT] * high + [GREY_C] * d["below_4"], height=0.62, buff=0.15, per_row=13)
        crowd.move_to([-3.2, -0.55, 0])
        cap = label(rf"{high} of {d['n']} rated it 4 or 5", font_size=30, color=P.ACCENT).next_to(crowd, DOWN, buff=0.3)
        big = VGroup(label(r"mean rating", font_size=26, color=GREY_A),
                     label(rf"{d['mean']:.2f}", font_size=96, color=P.ACCENT),
                     label(r"out of 5", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.1).move_to([3.9, 1.5, 0])
        same = VGroup(label(r"Every student had been given", font_size=30, color=WHITE),
                      label(r"the same description.", font_size=38, color=ERRC)).arrange(DOWN, buff=0.12)
        same.move_to([3.9, -0.85, 0])
        origin = wrapped_label(rf"{d['statements']} statements, taken largely from an astrology book bought at a "
                               r"newsstand; \ you read six of them", 5.6, 27, GREY_A).next_to(same, DOWN, buff=0.35)
        src = historical_tag(archive.FORER_1949.cite + r"; \ Dickson \& Kelly (1985)")
        with self.voiceover(
            "Keep your number. <bookmark mark='a'/> In 1949 a psychologist named Bertram Forer gave his "
            f"students a personality test, and a week later handed each of the {d['n']} a sketch of their "
            "character, as the result. They rated it the way you just did. "
            f"<bookmark mark='b'/> The average was {d['mean']:.2f} out of five. <bookmark mark='c'/> "
            f"{high} of the {d['n']} gave it a four or a five. <bookmark mark='d'/> Only when the ratings were "
            "in did the class find out. Every one of them had been handed the same sketch. "
            f"<bookmark mark='e'/> Forer had put it together, {d['statements']} statements in all, largely out of "
            "an astrology book from a newsstand. You've just read six of them. If your number was a four or a "
            "five, you're in the majority, and it says nothing against you. The demonstration has been repeated "
            "many times since, and a review of those studies in 1985 found the effect throughout."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.08) for p_ in crowd], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(big, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cap))
            vo.wait_until("d")
            self.play(FadeIn(same, scale=1.1))
            vo.wait_until("e")
            self.play(FadeIn(origin))
        self.clear_scene()

    def why(self):
        head = heading(r"Why it fits everyone, and what that costs")
        rows = VGroup()
        for title, text, color in (
                (r"true of nearly everybody", r"``You have a tendency to be critical of yourself.''", GROUP_A),
                (r"says a thing and its opposite", r"``At times you are extroverted \dots\ at other times introverted.''",
                 GROUP_B),
                (r"mostly flattering", r"``A great deal of unused capacity.''", TRUE)):
            rows.add(VGroup(label(title, font_size=38, color=color), label(text, font_size=32, color=GREY_A))
                     .arrange(DOWN, aligned_edge=LEFT, buff=0.12))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.85, 0])
        lesson = VGroup(
            label(r"``It fits me'' is not evidence that a test measures anything.", font_size=32, color=P.ACCENT),
            label(r"A measurement has to tell people apart: \ if everyone gets the same answer, nothing was "
                  r"measured.", font_size=28, color=WHITE),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> Look at how the statements are built. Some are true of nearly "
            "everybody. <bookmark mark='b'/> Some say a thing and its opposite, so one half is bound to fit. "
            "<bookmark mark='c'/> And most are a little flattering, which makes them easy to accept. None of this "
            "is a trick on stupid people. Each statement really is true of you. It's just as true of the person "
            "next to you. <bookmark mark='d'/> So here's the first lesson about measurement, and it's the one "
            "that horoscopes, and a good many personality quizzes, depend on your not learning. The feeling that "
            "a result fits you is not evidence that the test measured you. Forer called it the fallacy of "
            "personal validation. <bookmark mark='e'/> A measurement has to tell people apart. A scale that reads "
            "seventy kilos for everyone who steps on it is always plausible, and it weighs nothing. That idea, "
            "differences between people, is where the theory of test scores begins."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(lesson[0], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(lesson[1]))
        self.clear_scene()
