from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403

WORDS = [("talkative", E_), ("anxious", N_), ("kind", A_), ("careful", C_), ("curious", O_), ("moody", N_),
         ("bold", E_), ("tidy", C_), ("warm", A_), ("imaginative", O_), ("shy", E_), ("stubborn", A_),
         ("reliable", C_), ("irritable", N_), ("artistic", O_), ("cheerful", E_), ("lazy", C_), ("trusting", A_),
         ("calm", N_), ("inventive", O_), ("quiet", E_), ("thorough", C_), ("rude", A_), ("tense", N_)]


class Hook(VoiceoverScene):
    def construct(self):
        self.dictionary()
        self.three_turns()
        self.question()
        self.objectives()

    def dictionary(self):
        head = heading(r"1936: \ a dictionary, \ read for people")
        book = VGroup(RoundedRectangle(corner_radius=0.08, width=2.6, height=3.4, stroke_color=GREY_B,
                                       fill_color="#1B2029", fill_opacity=1),
                      label(r"Webster's", font_size=22, color=GREY_A), label(r"New International", font_size=18,
                                                                              color=GREY_A),
                      label(r"Dictionary", font_size=22, color=GREY_A)).move_to([-4.6, 0.0, 0])
        book[1:].arrange(DOWN, buff=0.15).move_to(book[0])
        rng = np.random.default_rng(1936)
        cloud = VGroup()
        for i, (w, c) in enumerate(WORDS):
            x = -1.6 + 1.9 * (i % 4) + rng.uniform(-0.25, 0.25)
            y = 2.0 - 0.75 * (i // 4) + rng.uniform(-0.12, 0.12)
            cloud.add(label(w, font_size=24, color=c).move_to([x, y, 0]))
        count = VGroup(label(r"17{,}953", font_size=64, color=YOU), label(r"words that describe a person",
                                                                          font_size=24, color=GREY_A))
        count.arrange(DOWN, buff=0.15).move_to([2.6, -2.6, 0])
        tag = historical_tag(r"Allport \& Odbert (1936)")
        with self.voiceover(
            "In 1936, at Harvard, Gordon Allport and Henry Odbert set out to read a dictionary. <bookmark mark='a'/> "
            "They went through Webster's New International Dictionary, some four hundred thousand entries, and copied "
            "out every word that could be used to tell one person's behaviour from another's. <bookmark mark='b'/> "
            "Talkative, anxious, kind, careful, curious, moody. <bookmark mark='c'/> They found seventeen thousand, "
            "nine hundred and fifty-three. <bookmark mark='d'/> Behind the exercise was an idea now called the "
            "lexical hypothesis: the differences between people that matter in daily life are the ones a language "
            "bothers to name."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(book, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(w, scale=0.8) for w in cloud], lag_ratio=0.12), run_time=3.5)
            vo.wait_until("c")
            self.play(FadeIn(count, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Indicate(count[0], color=YOU))
        self.clear_scene()

    def three_turns(self):
        head = heading(r"Three turns in one story")
        rows = rows_of([
            (r"fifty years of factor analysis reduced the dictionary's words to five broad dimensions", YOU),
            (r"in between, \ in 1968, \ Walter Mischel nearly ended the field: \ traits predicted any single act only "
             r"weakly", LOST),
            (r"the answer was a lesson in measurement: \ one act is a noisy sample, \ and many acts are not", GOOD),
            (r"and now a trail of clicks can estimate the five traits, \ which raises new questions about what "
             r"they are for", MODEL),
        ], 12.4, 26, 0.45).move_to([0, -0.2, 0])
        tag = historical_tag(r"Mischel (1968)")
        with self.voiceover(
            "The story of personality psychology has three turns. <bookmark mark='a'/> Fifty years of factor "
            "analysis reduced the dictionary's words to five broad dimensions. <bookmark mark='b'/> In between, in "
            "1968, Walter Mischel nearly ended the field, by showing how weakly a trait predicted any single act. "
            "<bookmark mark='c'/> The answer turned out to be a lesson in measurement: one act is a noisy sample, "
            "and many acts are not. <bookmark mark='d'/> And now a trail of clicks can estimate the five traits, "
            "which raises new questions about what they're for."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ is there a ``you'' that stays the same?")
        rows = rows_of([
            (r"across situations: \ at a party and at a funeral, \ at work and at home", SITUATION),
            (r"across years: \ at twenty and at sixty", AGE),
            (r"and if there is, \ what is it made of, \ what does it predict, \ and who gets to measure it?", YOU),
        ], 12.4, 28, 0.5).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks whether there's a you that stays the same. <bookmark mark='a'/> Across situations: at "
            "a party and at a funeral, at work and at home. <bookmark mark='b'/> Across years: at twenty and at "
            "sixty. <bookmark mark='c'/> And if there is, what it's made of, what it predicts, and who gets to "
            "measure it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 33", font_size=34, color=GREY_B), label(r"Personality", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"from 17{,}953 words to five factors, \ recomputed in 2{,}800 people's answers",
            r"types against traits: \ what a median split throws away",
            r"the person and the situation: \ why one act says little and many acts say a lot",
            r"stability and change across life, \ and whether you can change on purpose",
            r"where traits come from, \ what they predict, \ and Freud's tradition under Part 3's standards",
            r"women and men in one dimension and in many, \ and personality read from a trail of likes",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 33 of Psychology, Built: personality, the second part of Act Eight, on how people differ. "
            "<bookmark mark='a'/> We'll follow the words to five factors, and recompute them in two thousand eight "
            "hundred people's answers. We'll see what sorting people into types throws away. We'll take the person "
            "and the situation apart, and see why one act says little and many acts say a lot. We'll measure "
            "stability and change across life, and ask whether you can change on purpose. We'll weigh where traits "
            "come from and what they predict, and hold Freud's tradition to Part 3's standards. And we'll compare "
            "women and men in one dimension and in many, and read personality from a trail of likes."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=22.0)
        self.clear_scene()
