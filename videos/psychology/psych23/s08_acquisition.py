from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403

MILESTONES = (  # (start, end, label, colour), months; typical ranges, schematic
    (6, 10, r"babbling: \ \emph{ba-ba-ba}", SOUND),
    (10, 14, r"first words", WORD),
    (16, 24, r"vocabulary spurt", WORD),
    (18, 26, r"two-word combinations", RULE),
    (24, 48, r"grammar: \ endings, \ questions, \ clauses", RULE),
)


class Acquisition(VoiceoverScene):
    def construct(self):
        self.card()
        self.milestones()
        self.poverty()
        self.words()

    def card(self):
        card = chapter_card(7, r"How children learn a language", r"Is the input too poor to explain the grammar?",
                            lit={1967: r"Gold", 1978: r"Carey \& Bartlett", 1995: r"Hart \& Risley"},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter seven. How children learn a language."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def milestones(self):
        head = heading(r"Two years from babbling to grammar")
        A = axes([0, 50], [0, 6], x_length=11.0, y_length=3.4, xticks=[0, 12, 24, 36, 48], yticks=[],
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age, \ months", center=[0.3, 0.6, 0], font_size=17)
        bars_ = VGroup()
        for k, (a, b, t, c) in enumerate(MILESTONES):
            y = 5.2 - k
            lo, hi = A.ax.c2p(a, y), A.ax.c2p(b, y)
            r = RoundedRectangle(corner_radius=0.08, width=hi[0] - lo[0], height=0.42, stroke_width=0, fill_color=c,
                                 fill_opacity=0.6).move_to([(lo[0] + hi[0]) / 2, lo[1], 0])
            t_ = label(t, font_size=21).next_to(r, RIGHT, buff=0.15)
            if t_.get_right()[0] > 6.7:  # no room on the right: put the name before the bar
                t_.next_to(r, LEFT, buff=0.15)
            bars_.add(VGroup(r, t_))
        note = label(r"typical ranges, \ schematic; \ individual children vary widely", font_size=17,
                     color=GREY_A).next_to(A, DOWN, buff=0.15).align_to(A, RIGHT)
        rows = rows_of([
            (r"every typically developing child, \ in every language, \ passes these points in this order, \ at "
             r"varying ages", WHITE),
            (r"nobody teaches grammar to a two-year-old, \ and corrections of grammar are rare and mostly ignored",
             RULE),
        ], 12.0, 26, 0.36).to_edge(DOWN, buff=0.65)
        with self.voiceover(
            "Children do all of this in about two years. <bookmark mark='a'/> Babbling from about six months, first "
            "words around the first birthday, a spurt in vocabulary in the second year, two-word combinations, and "
            "then grammar: endings, questions, clauses within clauses. These are typical ranges, and individual "
            "children vary widely. <bookmark mark='b'/> Every typically developing child, in every language, passes "
            "these points in this order. <bookmark mark='c'/> And nobody teaches grammar to a two-year-old. "
            "Corrections of grammar are rare, and children mostly ignore them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars_], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def poverty(self):
        head = heading(r"The poverty of the stimulus, \ as a learning problem")
        big = Ellipse(width=5.6, height=3.4, color=LOST, fill_opacity=0.08).move_to([-3.6, 0.6, 0])
        mid = Ellipse(width=3.8, height=2.3, color=RULE, fill_opacity=0.12).move_to([-3.6, 0.5, 0])
        heard = VGroup(*[Dot([-3.6 + x, 0.5 + y, 0], radius=0.06, color=WORD)
                         for x, y in ((-0.8, 0.2), (-0.3, -0.4), (0.4, 0.3), (0.9, -0.2), (0.1, 0.6), (-1.1, -0.3))])
        lb = label(r"a larger language", font_size=18, color=LOST).next_to(big, UP, buff=0.05)
        lm = label(r"the target", font_size=18, color=RULE).move_to(mid.get_top() + DOWN * 0.25)
        lh = label(r"sentences heard", font_size=17, color=WORD).next_to(heard, DOWN, buff=0.35)
        rows = rows_of([
            (r"every sentence a child hears fits the target language, \ and also every larger language containing it",
             WHITE),
            (r"Gold, \ 1967: \ from examples alone, \ with no negative evidence, \ a learner cannot be guaranteed "
             r"to find the right language among such families", RULE),
            (r"Chomsky's conclusion: \ children must bring constraints of their own, \ a universal grammar", LOST),
            (r"the reply: \ a learner that expects grammatical sentences to appear notices which ones never do; \ "
             r"probability is a kind of negative evidence \ (Horning, \ 1969; \ Chater \& Vit\'anyi, \ 2007)", STAT),
        ], 6.4, 22, 0.33).move_to([3.2, 0.0, 0])
        tag = published_tag(r"Gold (1967); \ Horning (1969); \ Chater \& Vit\'anyi (2007)")
        with self.voiceover(
            "Chomsky's strongest argument is about learning. <bookmark mark='a'/> Every sentence a child hears is "
            "consistent with the target language, and also with every larger language that contains it. Without "
            "being told which sentences are not allowed, what stops a child from settling on a language that is too "
            "big? <bookmark mark='b'/> In 1967 Mark Gold proved that a learner given only examples cannot be "
            "guaranteed to identify the right language in many such families. <bookmark mark='c'/> Chomsky "
            "concluded that children must bring constraints of their own, a universal grammar, which rules out most "
            "of the possible languages in advance. <bookmark mark='d'/> The reply is statistical. A learner that "
            "expects grammatical sentences to turn up notices which ones never do. If a construction should have "
            "appeared a hundred times by now and hasn't, that is evidence. Probability turns silence into a kind of "
            "negative evidence, and with it, the learning problem becomes far easier. The argument continues, and "
            "this chapter's frontier is machines that learn from text alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(big), FadeIn(lb), FadeIn(mid), FadeIn(lm))
            vo.wait_until("a")
            self.play(FadeIn(heard, lag_ratio=0.2), FadeIn(lh), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def words(self):
        head = heading(r"Words, \ fast and slow")
        cols = VGroup()
        items = [
            (r"fast mapping", WORD, [r"Carey \& Bartlett, \ 1978: \ told once, \ \emph{bring me} \ \emph{the chromium} \ "
                                     r"\emph{tray,} \ \emph{not the red one}, \ preschoolers kept something of the new colour word a "
                                     r"week later",
                                     r"one exposure starts a word; \ many finish it"]),
            (r"inference", MODEL, [r"Part 22's size principle: \ three Dalmatians called \emph{fep}, \ and the word "
                                   r"means Dalmatian",
                                   r"and a new word is assumed to name something without a name yet"]),
            (r"input", LOST, [r"Hart \& Risley, \ 1995: \ 42 families, \ and a gap in words heard by age three, \ "
                              r"often quoted as 30 million",
                              r"replications disagree on its size, \ which depends on what counts as speech to a "
                              r"child"]),
        ]
        for k, (t, c, lines) in enumerate(items):
            body = VGroup(label(t, font_size=32, color=c),
                          rows_of([(lines[0], WHITE), (lines[1], GREY_A)], 3.6, 24, 0.4)).arrange(DOWN, buff=0.4,
                                                                                                aligned_edge=LEFT)
            box = RoundedRectangle(corner_radius=0.15, width=4.1, height=4.3, stroke_color=c, stroke_width=2,
                                   fill_color=c, fill_opacity=0.06).move_to([-4.35 + 4.35 * k, 0.2, 0])
            body.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.25)
            cols.add(VGroup(box, body))
        tag = published_tag(r"Carey \& Bartlett (1978); \ Hart \& Risley (1995)")
        with self.voiceover(
            "Words are learned both fast and slowly. <bookmark mark='a'/> In 1978 Susan Carey and Elsa Bartlett "
            "told preschoolers once, in passing, bring me the chromium tray, not the red one. A week later many "
            "children still knew something about the new colour word. One exposure starts a word; many more finish "
            "it. <bookmark mark='b'/> Inference helps: the size principle of Part 22, and the assumption that a new "
            "word names something that doesn't have a name yet. <bookmark mark='c'/> And input matters. Betty Hart "
            "and Todd Risley recorded forty-two families in 1995 and estimated a large gap in the words children "
            "heard by age three, often quoted as thirty million. Later studies disagree about its size, which "
            "depends on what is counted as speech to a child. That the amount and kind of talk a child hears "
            "matters is not in dispute; how much, and how it should change policy, is Part 54's question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, c in zip("abc", cols):
                vo.wait_until(m)
                self.play(FadeIn(c, shift=UP * 0.15))
        self.clear_scene()
