from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.review()
        self.colorless()
        self.on_you()
        self.question()
        self.objectives()

    def review(self):
        head = heading(r"1959: \ a review")
        book = VGroup(label(r"B. F. Skinner, \ \emph{Verbal Behavior} \ (1957)", font_size=34, color=STAT),
                      label(r"language as behaviour, \ shaped by reinforcement", font_size=27, color=GREY_A)
                      ).arrange(DOWN, buff=0.25).move_to([-3.3, 2.0, 0])
        rev = VGroup(label(r"N. Chomsky, \ review in \emph{Language} \ (1959)", font_size=34, color=RULE),
                     label(r"a thirty-year-old linguist, \ thirty-three pages", font_size=27, color=GREY_A)
                     ).arrange(DOWN, buff=0.25).move_to([3.3, 0.75, 0])
        arrow = Arrow(book[0].get_right() + DOWN * 0.15, rev[0].get_left() + UP * 0.1, buff=0.2, color=GREY_B)
        rows = rows_of([
            (r"almost every sentence you hear or say is new: \ no history of reinforcement can have shaped it", WHITE),
            (r"children learn a language fast, \ from what they happen to hear, \ and all reach much the same grammar",
             RULE),
            (r"the review helped start cognitive science; \ the argument it began, \ how much is built in and how "
             r"much learned from statistics, \ is seventy years old", STAT),
        ], 12.6, 29, 0.45).move_to([0, -1.75, 0])
        tag = historical_tag(r"Skinner (1957); \ Chomsky (1959), \ \emph{Language} 35")
        with self.voiceover(
            "In 1957 B. F. Skinner, the most famous psychologist in America, published a book explaining language "
            "as behaviour shaped by reinforcement, like a pigeon's peck. <bookmark mark='a'/> Two years later a "
            "thirty-year-old linguist named Noam Chomsky reviewed it, in thirty-three pages that are still read. "
            "<bookmark mark='b'/> His central point was simple. Almost every sentence you hear or say is new. You "
            "have never met it before, so no history of reinforcement can have shaped it. <bookmark mark='c'/> And "
            "children learn a language fast, from whatever they happen to hear, and all end up with much the same "
            "grammar. <bookmark mark='d'/> The review helped start cognitive science. The argument it began, about "
            "how much of language is built in and how much is learned from statistics, has now run for nearly "
            "seventy years, and machines have joined it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(book))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(rev))
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def colorless(self):
        head = heading(r"Grammatical, \ and meaningless")
        s1 = label(r"\emph{Colorless green ideas sleep furiously.}", font_size=40, color=RULE).move_to([0, 1.6, 0])
        s2 = label(r"\emph{Furiously sleep ideas green colorless.}", font_size=40, color=GREY_B).move_to([0, 0.4, 0])
        ok = label(r"English", font_size=24, color=GOOD).next_to(s1, RIGHT, buff=0.4)
        no = label(r"not English", font_size=24, color=LOST).next_to(s2, RIGHT, buff=0.4)
        rows = rows_of([
            (r"neither sentence has ever been said before 1957, \ and both mean nothing", WHITE),
            (r"yet everyone who speaks English knows the first is English and the second is not", RULE),
            (r"so knowing a language is more than knowing which word sequences you have heard", STAT),
        ], 12.6, 29, 0.45).move_to([0, -1.6, 0])
        for m in (ok, no):
            keep_in_frame(m)
        tag = historical_tag(r"Chomsky (1957), \ \emph{Syntactic Structures}")
        with self.voiceover(
            "Chomsky's most famous example came from his book of 1957. <bookmark mark='a'/> Colorless green ideas "
            "sleep furiously. <bookmark mark='b'/> Now reverse it: furiously sleep ideas green colorless. "
            "<bookmark mark='c'/> Neither sentence had ever been said before, and both mean nothing. "
            "<bookmark mark='d'/> Yet everyone who speaks English knows that the first is English and the second is "
            "not. <bookmark mark='e'/> So knowing a language is more than knowing which strings of words you have "
            "heard. Whether it's more than statistics is another question, and this part ends with machines that "
            "learn only statistics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(s1))
            vo.wait_until("b")
            self.play(Write(s2))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(ok), FadeIn(no), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def on_you(self):
        d = load("stream")
        syl = list(d["syllables"])
        stage = demo_stage(11.0, 2.6, center=[0, 1.0, 0])
        note = label(r"an unknown language: \ read the syllables as they come, \ in your head", font_size=24,
                     color=GREY_A).next_to(stage, DOWN, buff=0.25)
        line = Tex(*syl, font_size=40, color=SOUND)  # one line, one baseline, no spaces: as heard
        line.move_to(stage.get_center()).align_to(stage, LEFT).shift(RIGHT * 0.4)
        clip = line.copy()
        q = VGroup(label(r"which was a word of the language?", font_size=28, color=WHITE),
                   VGroup(word_chip("golabu", SOUND, 34), label(r"or", font_size=26, color=GREY_B),
                          word_chip("labubi", SOUND, 34)).arrange(RIGHT, buff=0.5)).arrange(DOWN, buff=0.35)
        q.move_to([0, -1.9, 0])
        with self.voiceover(
            "Before going on, an experiment on you. <bookmark mark='a'/> Here is a stream of syllables from a "
            "language you don't know. There are no spaces and no pauses. Just read the syllables in your head as "
            "they go past. <bookmark mark='b'/> Keep reading. <bookmark mark='c'/> Now a question. Which of these "
            "two was a word of the language: golabu, or labubi? Pick one, and keep it in mind. Chapter six will tell "
            "you whether you were right, and how an eight-month-old does it."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(note))
            vo.wait_until("a")
            self.add(line)
            line.set_opacity(0)
            for k in range(len(syl)):
                self.play(line[k].animate.set_opacity(1), run_time=0.33, rate_func=linear)
                if line[k].get_right()[0] > stage.get_right()[0] - 0.4:
                    shift = line[k].get_right()[0] - (stage.get_right()[0] - 0.4)
                    line.shift(LEFT * shift)
                    for j in range(len(syl)):
                        if line[j].get_left()[0] < stage.get_left()[0] + 0.2:
                            line[j].set_opacity(0)
            vo.wait_until("c")
            self.play(FadeOut(line), FadeIn(q))
        del clip
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how does a finite experience give an infinite language?")
        rows = rows_of([
            (r"the levels of language, \ and productivity at each", WORD),
            (r"recognizing a word: \ a network that reads, \ and the cost of a surprising word, \ fitted to "
             r"reading times", MODEL),
            (r"finding words in a stream, \ the past tense, \ and a critical period", STAT),
            (r"language in the brain, \ and whether it shapes thought", RULE),
            (r"and what machines that learn language from text alone show about all of it", SOUND),
        ], 12.0, 27, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "This part asks how a finite experience gives an infinite language. <bookmark mark='a'/> We'll start with "
            "the levels of language, from sounds to meaning, and the productivity at each level. "
            "<bookmark mark='b'/> Then reading: a network that recognizes words, and the cost of a surprising word, "
            "measured in thousands of reading times. <bookmark mark='c'/> Then learning: finding words in a stream, "
            "the most argued-over network in psychology, and whether there is a critical period. "
            "<bookmark mark='d'/> Then language in the brain, and whether your language shapes how you think. "
            "<bookmark mark='e'/> And finally what machines that learn language from text alone tell us about all "
            "of it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 23", font_size=34, color=GREY_B), label(r"Language", font_size=60))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the levels of language, \ the wug test, \ Zipf's law and a typing monkey",
            r"the mental lexicon, \ and the interactive activation model computed",
            r"garden paths, \ and surprisal fitted to the Natural Stories reading times",
            r"statistical segmentation, \ and a past-tense network's U-shaped curve",
            r"critical periods, \ the brain's language network, \ the N400 and P600",
            r"linguistic relativity: \ Russian blues and numbers without words",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 23 of Psychology, Built, the sixth part of Act Five, on thinking: language. "
            "<bookmark mark='a'/> We'll compute Zipf's law for thirty novels and for a monkey at a typewriter. "
            "We'll build the interactive activation model and watch it read. We'll measure the surprise of every "
            "word in ten stories and fit it to how long people looked at each one. We'll find words in a stream by "
            "statistics alone, and watch a network learn the past tense, and unlearn it. Then critical periods, the "
            "brain's language network, and the old question of whether language shapes thought."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=24.0)
        self.clear_scene()
