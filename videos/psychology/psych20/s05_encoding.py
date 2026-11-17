from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403


class Encoding(VoiceoverScene):
    def construct(self):
        self.card()
        self.levels()
        self.generation()
        self.loci()

    def card(self):
        card = chapter_card(4, r"What you do with it", r"Does how you study a word decide whether it stays?",
                            lit={1972: r"Craik \& Lockhart", 1975: r"Craik \& Tulving", 1977: r"Morris et al.",
                                 1978: r"Slamecka \& Graf", 2017: r"Dresler et al."},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter four. What you do with it."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def levels(self):
        c = archive.CRAIK_TULVING_1975.data
        head = heading(r"Levels of processing")
        qs = VGroup(
            label(r"``Is the word in capital letters?'' \ \ TABLE", font_size=24, color=LOST),
            label(r"``Does the word rhyme with WEIGHT?'' \ \ crate", font_size=24, color=WORD),
            label(r"``Does it fit: \ He met a \underline{\ \ \ \ \ \ } in the street?'' \ \ friend", font_size=24,
                  color=MODEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.0, 2.0, 0])
        qn = VGroup(*[label(t, font_size=20, color=GREY_B).next_to(q, LEFT, buff=0.25)
                      for t, q in zip((r"case", r"rhyme", r"meaning"), qs)])
        A = axes([0, 3], [0, 1], x_length=5.2, y_length=2.9, xticks=[], yticks=[0, 0.5, 1], xlabel=r"",
                 ylabel=r"recognised later", center=[-2.8, -1.5, 0], font_size=18, yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        inc = bars(ax, [0.35, 1.35, 2.35], c["incidental"], GREY_B, width=0.55)
        intl = bars(ax, [0.85, 1.85, 2.85], c["intentional"], CUE, width=0.55)
        for b, col in zip(inc, (LOST, WORD, MODEL)):
            b.set_fill(col, 0.85)
        names = VGroup(*[label(t, font_size=19, color=GREY_A).move_to(ax.c2p(x, 0) + DOWN * 0.3)
                         for t, x in zip((r"case", r"rhyme", r"meaning"), (0.6, 1.6, 2.6))])
        vals = VGroup(*[label(f"{100 * v:.0f}", font_size=17, color=GREY_A).next_to(b, UP, buff=0.06)
                        for v, b in zip(list(c["incidental"]) + list(c["intentional"]), list(inc) + list(intl))])
        key = legend([(GREY_A, r"left bar: \ not told of a test"), (CUE, r"right bar: \ told to learn")],
                     font_size=18).next_to(A, UP, buff=0.1)
        key.shift(RIGHT * 1.0)
        rows = rows_of([
            (r"Craik and Lockhart, \ 1972: \ memory is a by-product of the processing done at study", WHITE),
            (r"Craik and Tulving, \ 1975: \ the same words, \ three kinds of question; \ then a surprise test", WHITE),
            (r"the deeper the question, \ the better the memory: \ about 15, \ 48 and 81\% recognised", MODEL),
            (r"telling people to learn adds little: \ what they did with the word is what counts", CUE),
            (r"Morris, \ Bransford and Franks, \ 1977: \ on a test of rhymes, \ rhyme study wins", LOST),
            (r"so ``deep'' is not absolute: \ memory is best when study and test ask for the same thing", WORD),
        ], 6.1, 21, 0.24).move_to([3.6, -0.75, 0])
        tag = published_tag(archive.CRAIK_TULVING_1975.cite)
        with self.voiceover(
            "If memory is a store, what goes into it should depend on whether you try to put it there. In 1972 "
            "Fergus Craik and Robert Lockhart proposed instead that memory is a by-product of processing: of what "
            "you do with the thing at the time. <bookmark mark='a'/> Craik and Endel Tulving tested it with one "
            "word at a time and a question about it. Is the word in capital letters? Does it rhyme with weight? Does "
            "it fit the sentence, he met a blank in the street? <bookmark mark='b'/> Then, without warning, a "
            "recognition test. Words judged for their case were recognised about fifteen percent of the time; for "
            "their rhyme, forty-eight; for their meaning, eighty-one. <bookmark mark='c'/> In another experiment "
            "people were told in advance that there would be a test. It helped the shallow questions a little, and "
            "the meaning question not at all. Trying to remember matters much less than what you do while you try. "
            "<bookmark mark='d'/> But deep is not simply better. In 1977 Donald Morris, John Bransford and Jeffery "
            "Franks tested memory by asking which test words rhymed with studied words. On that test, words studied "
            "for their rhyme won. <bookmark mark='e'/> Memory works best when the processing at test matches the "
            "processing at study, a principle called transfer-appropriate processing. It's the first sign of the "
            "idea this part keeps returning to: remembering is a match between a cue and a trace."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(q, shift=RIGHT * 0.15) for q in qs], lag_ratio=0.5), FadeIn(qn),
                      FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(names), LaggedStart(*[GrowFromEdge(b, DOWN) for b in inc], lag_ratio=0.3),
                      FadeIn(vals[:3]), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in intl], lag_ratio=0.3), FadeIn(vals[3:]),
                      FadeIn(key), FadeIn(rows[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def generation(self):
        g = archive.BERTSCH_2007.data
        head = heading(r"Making the word yourself")
        read = VGroup(label(r"read:", font_size=26, color=GREY_B), label(r"RAPID \ -- \ FAST", font_size=40))
        gen = VGroup(label(r"generate:", font_size=26, color=GREY_B),
                     label(r"RAPID \ -- \ F\underline{\ \ \ \ \ \ }", font_size=40, color=WORD))
        for v in (read, gen):
            v.arrange(RIGHT, buff=0.4)
        pair = VGroup(read, gen).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 1.8, 0])
        rows = rows_of([
            (r"Slamecka and Graf, \ 1978: \ a word you produce from a cue is remembered better than one you read",
             WORD),
            (r"not explained by time on the word; \ found in recognition, \ cued recall and free recall", WHITE),
            (rf"Bertsch and colleagues, \ 2007: \ {g['studies']} studies, \ {g['effects']} effect sizes, \ "
             rf"a mean of $d = {g['d']:.2f}$: \ about half a standard deviation", DATA),
            (r"smallest in free recall, \ where generating each word may cost the links between words", LOST),
            (r"the same family as the testing effect of Part 21: \ effort spent retrieving is spent well", MODEL),
        ], 12.4, 25, 0.3).move_to([0, -1.1, 0])
        tag = published_tag(r"Slamecka \& Graf (1978); \ Bertsch et al.\ (2007)")
        with self.voiceover(
            "A second way to change what you remember is to make the word yourself. <bookmark mark='a'/> In 1978 "
            "Norman Slamecka and Peter Graf had people either read a pair, rapid and fast, or generate the second "
            "word from a clue, rapid and a word beginning with f that means the same. Generated words were "
            "remembered better. <bookmark mark='b'/> The advantage was not just more time spent on the word, and "
            "it appeared in recognition, cued recall and free recall. <bookmark mark='c'/> It has been tested "
            "hundreds of times since. Sharon Bertsch and her colleagues combined "
            f"{g['effects']} effect sizes from {g['studies']} studies in 2007: a mean advantage of about "
            f"{g['d']:.1f} standard deviations, real and moderate. <bookmark mark='d'/> It's smallest in free recall, "
            "where generating each word on its own seems to cost the links between them. <bookmark mark='e'/> It "
            "belongs with the testing effect of Part 21: work you put into producing a memory is work well spent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(read), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(gen), FadeIn(rows[0]))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def loci(self):
        d = archive.DRESLER_2017.data
        head = heading(r"The method of loci")
        path = VMobject(stroke_color=CTX, stroke_width=4).set_points_smoothly(
            [np.array(p) for p in ([-6.2, 0.1, 0], [-5.0, 1.9, 0], [-3.5, 0.8, 0], [-2.2, 2.1, 0], [-0.9, 0.5, 0])])
        stops = VGroup(*[Dot(path.point_from_proportion(t), radius=0.11, color=CTX) for t in (0.05, 0.3, 0.55, 0.8,
                                                                                            1.0)])
        where = (r"door", r"hall", r"stairs", r"kitchen", r"window")
        pegs = VGroup(*[label(rf"{w}: \ {x}", font_size=19, color=WORD).next_to(s, UP if k % 2 else DOWN, buff=0.15)
                        for k, (w, x, s) in enumerate(zip(where, WORDS[:5], stops))])
        rows = rows_of([
            (r"walk a route you know, \ and leave each word at a place on it, \ as a vivid picture; \ to recall, \ "
             r"walk it again", CTX),
            (rf"memory athletes recalled {d['athletes']:.1f} of {d['words']} words after 20 minutes; \ matched "
             rf"controls, \ {d['controls']:.1f}", WORD),
            (rf"novices, \ {d['sessions']} sessions of 30 minutes over six weeks: \ large gains, \ far above active "
             r"and passive controls, \ kept four months later", MODEL),
            (r"their brain networks moved toward the athletes': \ the skill is learnt, \ not born", GREY_A),
            (r"the trick: \ a known order of places supplies the cues; \ context, \ made deliberately", CUE),
        ], 6.1, 22, 0.3).move_to([3.6, -0.3, 0])
        tag = published_tag(archive.DRESLER_2017.cite)
        with self.voiceover(
            "The oldest technique of all is said to go back to the Greek poet Simonides. <bookmark mark='a'/> Take "
            "a route you know well, your house say, and leave each thing you have to remember at a place along it, "
            "as a vivid picture: a candle burning at the door, a horse in the hall, a pencil on the stairs. To "
            "recall, walk the route again. <bookmark mark='b'/> In 2017 Martin Dresler and his colleagues studied "
            f"twenty-three of the world's best memory athletes. After twenty minutes they recalled "
            f"{d['athletes']:.0f} of {d['words']} words on average, against about {d['controls']:.0f} for matched "
            "controls. <bookmark mark='c'/> Then they trained novices: thirty minutes a day for forty days. Their "
            "recall rose far more than that of two control groups, one of which trained working memory instead, and "
            "it was still higher four months later. <bookmark mark='d'/> And the way their brain regions worked "
            "together came to resemble the athletes'. The athletes, it seems, weren't born different; they "
            "practised. <bookmark mark='e'/> Notice why it works. The route supplies a fixed sequence of cues, one "
            "for each item. The method of loci is context, built on purpose, and by chapter seven you'll see why "
            "that is exactly what memory needs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(path), FadeIn(stops), run_time=1.5)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pegs], lag_ratio=0.4), FadeIn(rows[0]), run_time=2.5)
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
