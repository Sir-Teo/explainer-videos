from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403

LISTS = ("58193", "7294163", "518274936")


class Hook(VoiceoverScene):
    def construct(self):
        self.span()
        self.miller()
        self.question()
        self.objectives()

    def _flash(self, stage, digits: str):
        """Show a list one digit a second, then a cue to recall, then the answer."""
        spot = stage.box.get_center() + UP * 0.35
        for ch in digits:
            d = label(ch, font_size=96, color=WHITE).move_to(spot)
            self.add(d)
            self.wait(0.75)
            self.remove(d)
            self.wait(0.25)
        cue = label(r"now say them back, \ in order", font_size=30, color=YOU).move_to(spot)
        self.play(FadeIn(cue), run_time=0.4)
        self.wait(3.0)
        ans = digits_row(digits, font_size=56, color=MEM, buff=0.3).move_to(spot)
        self.play(FadeOut(cue), run_time=0.3)
        self.play(FadeIn(ans), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(ans), run_time=0.4)

    def span(self):
        stage = demo_stage(9.6, 4.6, center=[0, 0.5, 0])
        note = label(r"digits at one a second; \ when they stop, \ say them back aloud", font_size=24,
                     color=GREY_A).next_to(stage, DOWN, buff=0.3)
        lens = VGroup(*[label(rf"{len(s)} digits", font_size=24, color=GREY_B) for s in LISTS])
        with self.voiceover(
            "Before anything else, a test you can take right now. <bookmark mark='a'/> Digits will appear one a "
            "second. When they stop, say them back, out loud, in order. Five digits first."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(note))
        self._flash(stage, LISTS[0])
        with self.voiceover("Now seven."):
            pass
        self._flash(stage, LISTS[1])
        with self.voiceover("And nine."):
            pass
        self._flash(stage, LISTS[2])
        lens.arrange(RIGHT, buff=1.4).move_to(stage.box.get_center() + UP * 0.2)
        marks = VGroup(*[label(t, font_size=30, color=c).next_to(l_, DOWN, buff=0.25)
                         for l_, (t, c) in zip(lens, ((r"most people", GOOD), (r"about half", MEM),
                                                      (r"few people", LOST)))])
        with self.voiceover(
            "Most adults get five digits right. <bookmark mark='a'/> Seven is about where people start to fail: "
            "a typical adult's digit span, the longest list repeated correctly half the time, is around seven. "
            "<bookmark mark='b'/> Nine is beyond most people, unless they do something clever with the digits, "
            "and we'll see what. Hold on to your own result. By the end of this part you'll know what it measured, "
            "and what it didn't."
        ) as vo:
            self.play(FadeIn(lens[0]), FadeIn(marks[0]))
            vo.wait_until("a")
            self.play(FadeIn(lens[1]), FadeIn(marks[1]))
            vo.wait_until("b")
            self.play(FadeIn(lens[2]), FadeIn(marks[2]))
        self.clear_scene()

    def miller(self):
        p = archive.MILLER_1956.data
        q = quote_card(r"My problem is that I have been persecuted by an integer.",
                       r"George A. Miller, \ Psychological Review (1956)", width=10.0, font_size=34)
        q.move_to([0, 1.7, 0])
        rows = rows_of([
            (rf"memory span: \ about {p['binary_span']} binary digits, \ about 7 decimal digits, \ "
             rf"about {p['word_span']} words", WHITE),
            (r"judging a tone's pitch on one scale: \ about 6 categories before mistakes, \ about 2.6 bits", GREY_A),
            (r"Miller's point: \ the span is a number of chunks, \ not of bits", MEM),
            (r"seventy years later: \ the number is closer to four, \ and perhaps not a number at all", LOST),
        ], 12.4, 27, 0.3).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.MILLER_1956.cite)
        with self.voiceover(
            "In 1956 the psychologist George Miller opened a paper with a confession. <bookmark mark='a'/> My problem "
            "is that I have been persecuted by an integer. The integer was seven, and it kept turning up. "
            "<bookmark mark='b'/> The number of digits a person can repeat back is about seven; the number of binary "
            "digits, about nine; the number of words, about five. <bookmark mark='c'/> The number of pitches a "
            "listener can label without errors is about six, a little over two and a half bits of information. "
            "<bookmark mark='d'/> Miller's real point was subtler than the slogan it became. The span is not a fixed "
            "amount of information. It is a fixed number of chunks, and a chunk can hold a lot. "
            "<bookmark mark='e'/> And seventy years later the integer itself looks wrong. The best estimate is closer "
            "to four, and there's a serious case that the limit is not a number of things at all."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ how much can you hold in mind, \ and what is the limit made of?")
        rows = rows_of([
            (r"how much reaches a brief store, \ and how fast does it fade?", WHITE),
            (r"why do we forget in seconds: \ time, \ or other memories?", LOST),
            (r"is the limit a number of slots, \ or a resource spread thinner?", MEM),
            (r"how does a network of neurons hold a thought for a few seconds?", MODEL),
            (r"and can the limit be raised by practice, \ as an industry promises?", EXEC),
        ], 11.8, 30, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "This part is about the small, fast, fragile memory you just used. <bookmark mark='a'/> How much of what "
            "you see reaches a brief store, and how quickly does it fade? <bookmark mark='b'/> Why can you forget a "
            "three-letter string in eighteen seconds: is it time, or other memories getting in the way? "
            "<bookmark mark='c'/> Is the limit a number of slots, or a resource that is spread thinner the more you "
            "hold? <bookmark mark='d'/> How does a network of neurons keep a thought alive once the thing itself is "
            "gone? <bookmark mark='e'/> And can practice raise the limit, as a whole industry has promised?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 19", font_size=34, color=GREY_B), label(r"Working Memory", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"span and chunks: \ Miller's seven, \ and recoding performed",
            r"a brief visual store: \ Sperling's partial report",
            r"forgetting in seconds: \ decay or interference, \ and a model that settles it",
            r"working memory as a system: \ the loop, \ the sketchpad, \ the executive; \ memory scanning",
            r"four, \ not seven: \ change detection and the K formula, \ derived",
            r"slots or resources: \ four models fitted to open data; \ a ring attractor; \ training",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 19 of Psychology, Built, the second part of Act Five, on thinking: working memory. "
            "<bookmark mark='a'/> We'll start with Miller's seven, and perform the trick that let one man repeat forty "
            "binary digits. Then a visual store that holds more than you can report, for a fraction of a second. Then "
            "forgetting in eighteen seconds, and a small model that explains why the first trial shows none. Then "
            "working memory as a system with parts, and how you search it. Then the evidence that the number is four, "
            "not seven, with the formula for counting it. Then the deepest argument in the field, slots against "
            "resources, settled as far as it can be by fitting four models to an open dataset of seven thousand "
            "trials. Then a network that holds a thought, and an industry that promised to make it bigger."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=26.0)
        self.clear_scene()
