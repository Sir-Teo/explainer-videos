from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Segmentation(VoiceoverScene):
    def construct(self):
        self.card()
        self.answer()
        self.derive()
        self.learning()

    def card(self):
        card = chapter_card(6, r"Finding the words", r"How does an infant find words in speech with no spaces?",
                            lit={1996: r"Saffran, \ Aslin \& Newport", 2017: r"Black \& Bergmann"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter six. Finding the words."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def answer(self):
        head = heading(r"Your answer, \ and an eight-month-old's")
        q = VGroup(word_chip("golabu", MODEL, 34), label(r"was a word; \ ", font_size=26, color=GREY_A),
                   word_chip("labubi", LOST, 34), label(r"straddled two", font_size=26, color=GREY_A)
                   ).arrange(RIGHT, buff=0.3).move_to([0, 2.1, 0])
        # a stretch of such a stream, coloured by word: the word sits inside, the part-word straddles a boundary
        sy = "tu pi ro go la bu bi da ku pa do ti".split()
        cols = [SOUND, SOUND, SOUND, MODEL, MODEL, MODEL, STAT, STAT, STAT, WORD, WORD, WORD]
        stream = Tex(*sy, font_size=44)
        for m_, c_ in zip(stream, cols):
            m_.set_color(c_)
        stream.move_to([0, 0.75, 0])
        b_word = Brace(stream[3:6], DOWN, color=MODEL)
        t_word = label(r"a word", font_size=22, color=MODEL).next_to(b_word, DOWN, buff=0.08)
        b_part = Brace(stream[4:7], UP, color=LOST)
        t_part = label(r"a part-word", font_size=22, color=LOST).next_to(b_part, UP, buff=0.08)
        rows = rows_of([
            (r"the stream was four made-up words, \ \emph{tupiro}, \ \emph{golabu}, \ \emph{bidaku}, \ "
             r"\emph{padoti}, \ in random order with no pauses", WHITE),
            (r"Saffran, \ Aslin \& Newport, \ 1996: \ 24 eight-month-olds heard two minutes of such a stream", SOUND),
            (r"then words and part-words, \ like \emph{labubi}, \ played one at a time: \ the infants listened "
             r"longer to the part-words, \ the novel sounds", MODEL),
            (r"two minutes, \ no meaning, \ no pauses: \ only the statistics of which syllable follows which", STAT),
        ], 12.6, 26, 0.36).move_to([0, -1.9, 0])
        tag = historical_tag(r"Saffran, \ Aslin \& Newport (1996), \ \emph{Science}")
        with self.voiceover(
            "In the stream at the start of this part, which was a word: golabu or labubi? <bookmark mark='a'/> Golabu. Labubi "
            "straddled the end of one word and the start of another. The stream was four made-up words, tupiro, "
            "golabu, bidaku and padoti, in random order with no pauses. <bookmark mark='b'/> In 1996 Jenny Saffran, "
            "Richard Aslin and Elissa Newport played two minutes of a stream like this to twenty-four "
            "eight-month-old infants. <bookmark mark='c'/> Then they played words and part-words, one at a time, and "
            "measured how long the infants kept looking toward the sound. The infants listened longer to the "
            "part-words, the sequences that were new to them. <bookmark mark='d'/> They had found the words, after "
            "two minutes, with no meaning and no pauses, using only the statistics of which syllable follows which."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(stream))
            self.play(GrowFromCenter(b_word), FadeIn(t_word), GrowFromCenter(b_part), FadeIn(t_part), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def derive(self):
        d = load("stream")
        head = heading(r"Derivation: \ transitional probabilities")
        eq = MathTex(r"P(y \mid x) = \frac{\#(x\,y)}{\#(x)}", font_size=40, color=STAT).move_to([-4.2, 2.1, 0])
        syl = [str(s) for s in d["syllables"][:16]]
        tp = d["tp"][:15]
        A = axes([0, 16], [0, 1.1], x_length=11.6, y_length=2.2, xticks=[], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"$P(\text{next} \mid \text{this})$", center=[0.3, 0.2, 0],
                 font_size=15)
        pts = VGroup(*[Dot(A.ax.c2p(k + 1, p), radius=0.07, color=MODEL if p > 0.9 else LOST) for k, p in
                       enumerate(tp)])
        line = VMobject(color=STAT, stroke_width=2).set_points_as_corners([p.get_center() for p in pts])
        names = VGroup(*[label(s, font_size=22, color=SOUND).move_to([A.ax.c2p(k + 0.5, 0)[0], -1.15, 0])
                         for k, s in enumerate(syl)])
        cuts = VGroup(*[DashedLine([A.ax.c2p(k + 1, 0)[0], -1.4, 0], [A.ax.c2p(k + 1, 0)[0], -0.8, 0],
                                   color=LOST) for k, p in enumerate(tp) if p < 0.9])
        rows = rows_of([
            (r"inside a word, \ the next syllable is certain: \ \emph{tu} is always followed by \emph{pi}", MODEL),
            (r"across a boundary it is one of three, \ about a third", LOST),
            (rf"cut where the probability dips: \ the stream falls into words, \ and part-words score lower "
             rf"\ ({d['part_scores'].mean():.2f} against {d['word_scores'].mean():.2f})", STAT),
        ], 12.0, 26, 0.36).to_edge(DOWN, buff=0.65)
        ptag = psyche_tag(r"\texttt{language.transitional\_probabilities}, \ \texttt{segment}")
        with self.voiceover(
            "Here's the statistic. <bookmark mark='a'/> The transitional probability from one syllable to the next "
            "is how often the pair occurs, divided by how often the first syllable does. <bookmark mark='b'/> Inside "
            "a word the next syllable is certain: tu is always followed by pi. <bookmark mark='c'/> Across a word "
            "boundary, the next syllable could start any of the other three words, so the probability is about a "
            "third. <bookmark mark='d'/> Cut wherever it dips, and the stream falls apart into words. Part-words, "
            "which straddle a dip, score lower than words. Psyche needs nothing else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag), FadeIn(names))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(A))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(pts), FadeIn(rows[0]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(cuts), FadeIn(rows[2]))
        self.clear_scene()

    def learning(self):
        d = load("stream")
        head = heading(r"How much exposure, \ and how strong the evidence")
        A = axes([0, 2.4], [0, 1], x_length=5.0, y_length=3.0, xticks=[0.5, 1, 1.5, 2],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 0.5, 1], yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"words heard", ylabel=r"cuts that give real words", center=[-3.4, 0.3, 0], font_size=16)
        c = VGroup(curve(A.ax, np.log10(d["exposure"]), d["correct"], MODEL, 3),
                   scatter(A.ax, np.log10(d["exposure"]), d["correct"], MODEL, 0.06, 1))
        rows = rows_of([
            (r"Psyche's segmenter needs only a few dozen words of the stream; \ the infants heard about 180", MODEL),
            (r"later work found the same learning for tones, \ shapes, \ and in other animals: \ a general "
             r"statistical learner, \ not only a language one", STAT),
            (r"Black \& Bergmann, \ 2017: \ a meta-analysis of infant studies finds a small, \ reliable effect "
             r"for close replications, \ and none across all transitional-probability designs", LOST),
            (r"and real speech has words of every length, \ so a dip in probability is a clue, \ not a recipe", GREY_A),
        ], 5.6, 22, 0.33).move_to([3.6, 0.1, 0])
        ptag = psyche_tag(r"\texttt{language.segment}, \ on the first $n$ words of the stream")
        tag = published_tag(r"Black \& Bergmann (2017)")
        with self.voiceover(
            "How much exposure does it take? <bookmark mark='a'/> Psyche's segmenter finds the words reliably after "
            "a few dozen words of the stream. The infants heard about a hundred and eighty. "
            "<bookmark mark='b'/> Later studies found the same kind of learning with tones and shapes, and in other "
            "animals: a general statistical learner, not only a linguistic one. <bookmark mark='c'/> How strong is "
            "the infant evidence? In 2017 Black and Bergmann pooled the studies in a meta-analysis. They found a "
            "small, reliable effect for close replications of the original, and no reliable effect across all the "
            "designs that use transitional probabilities. <bookmark mark='d'/> And real speech has words of every "
            "length, spoken by many voices, so a dip in probability is a clue to a word boundary, not a recipe."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
