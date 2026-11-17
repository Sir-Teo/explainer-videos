from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Seven(VoiceoverScene):
    def construct(self):
        self.card()
        self.judgment()
        self.chunks()
        self.recoding()

    def card(self):
        card = chapter_card(1, r"The magical number seven", r"Is the limit a number of bits, \ or of things?",
                            lit={1956: r"Miller"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter one. The magical number seven."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def judgment(self):
        d = load("judgment")
        head = heading(r"Absolute judgment: \ a channel with a capacity")
        A = axes([1, 5], [0, 3.2], x_length=6.6, y_length=3.8, xticks=[1, 2, 3, 4, 5], yticks=[0, 1, 2, 3],
                 xlabel=r"information in the stimulus, \ bits \ ($\log_2$ of the number of categories)",
                 ylabel=r"information transmitted, \ bits", center=[-2.4, 0.2, 0], font_size=18)
        ax = A.ax
        diag = DashedLine(ax.c2p(1, 1), ax.c2p(3.2, 3.2), color=GREY_C, stroke_width=2)
        dl = label(r"perfect labelling", font_size=18, color=GREY_B).next_to(ax.c2p(3.0, 3.0), RIGHT, buff=0.1)
        c = curve_in(ax, d["input"], d["bits"], MODEL, 4)
        plateau = float(d["bits"][-1])
        pl = label(rf"levels off near {plateau:.1f} bits: \ about {2 ** plateau:.0f} categories", font_size=20,
                   color=MODEL).next_to(ax.c2p(3.95, plateau), DOWN, buff=0.3)
        rows = rows_of([
            (r"tones of different pitch, \ one at a time; \ name each with a number", WHITE),
            (r"with up to five or six tones, \ almost no mistakes; \ beyond that, \ errors rise as fast as the "
             r"choices", GREY_A),
            (r"the same ceiling for loudness, \ position on a line, \ taste concentration: \ about 2 to 3 bits", MEM),
            (r"computed: \ a percept with noise, \ labelled by the nearest category; \ the information is the mutual "
             r"information of stimulus and label", MODEL),
        ], 5.6, 22, 0.3).move_to([3.95, 0.3, 0])
        ptag = psyche_tag(r"\texttt{wm.absolute\_judgment}: \ noise s.d. 4\% of the range")
        tag = historical_tag(archive.MILLER_1956.cite)
        with self.voiceover(
            "Miller's paper began somewhere unexpected: with judgments, not memory. <bookmark mark='a'/> Play someone "
            "a tone and ask them to label its pitch with a number from one to n. With two or three tones, nobody makes "
            "mistakes. <bookmark mark='b'/> By five or six tones, mistakes start, and beyond that adding more tones "
            "adds nothing: errors rise as fast as the choices do. <bookmark mark='c'/> Measured in bits, the "
            "information the labels carry about the stimulus climbs along the diagonal and then levels off. "
            "<bookmark mark='d'/> Psyche's version is a single noisy percept, labelled by the nearest category, and "
            "the curve is computed exactly as the mutual information between stimulus and label. With noise about "
            f"four percent of the range, it levels off near {plateau:.1f} bits, about {2 ** plateau:.0f} categories, "
            "which is Miller's number. <bookmark mark='e'/> Loudness, position on a line, the saltiness of water all "
            "gave a ceiling of two to three bits. Information theory had found a channel with a capacity."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(ptag), FadeIn(pl))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def chunks(self):
        p = archive.MILLER_1956.data
        head = heading(r"Span counts chunks, \ not bits")
        items = [(r"binary digits", p["binary_span"], 1.0, LOOP),
                 (r"decimal digits", 7, float(np.log2(10)), MEM),
                 (r"words \ (1,000 known)", p["word_span"], float(np.log2(1000)), EXEC)]
        A = axes([0, 3], [0, 55], x_length=5.4, y_length=3.0, xticks=[], yticks=[0, 25, 50],
                 ylabel=r"bits held in the span", center=[-3.2, 0.85, 0], font_size=18)
        B = axes([0, 3], [0, 10], x_length=5.4, y_length=3.0, xticks=[], yticks=[0, 5, 10],
                 ylabel=r"items held in the span", center=[3.4, 0.85, 0], font_size=18)
        bits_b, item_b, labs_a, labs_b = VGroup(), VGroup(), VGroup(), VGroup()
        for k, (name, span, b, col) in enumerate(items):
            x = k + 0.5
            bits_b.add(bars(A.ax, [x], [span * b], col, width=0.55))
            item_b.add(bars(B.ax, [x], [span], col, width=0.55))
            labs_a.add(VGroup(wrapped_label(name, 1.7, 18, col).next_to(A.ax.c2p(x, 0), DOWN, buff=0.15),
                              label(rf"{span * b:.0f}", font_size=20, color=col).next_to(A.ax.c2p(x, span * b), UP,
                                                                                        buff=0.08)))
            labs_b.add(VGroup(wrapped_label(name, 1.7, 18, col).next_to(B.ax.c2p(x, 0), DOWN, buff=0.15),
                              label(rf"{span}", font_size=20, color=col).next_to(B.ax.c2p(x, span), UP, buff=0.08)))
        rows = rows_of([
            (r"a constant amount of information would hold about 25 binary digits, \ or 2 words", GREY_A),
            (r"instead the number of items is roughly constant, \ and the bits vary five-fold", MEM),
            (r"a chunk: \ a unit the person already knows, \ whatever it contains", EXEC),
        ], 12.4, 24, 0.2).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.MILLER_1956.cite)
        with self.voiceover(
            "Then Miller turned to memory span, and the channel analogy broke. <bookmark mark='a'/> If short-term "
            "memory held a fixed amount of information, it would hold far more binary digits than words. A binary "
            "digit carries one bit; a word from a vocabulary of a thousand carries about ten. <bookmark mark='b'/> But "
            f"the spans were about {p['binary_span']} binary digits, seven decimal digits, and {p['word_span']} words. "
            "The number of items stays roughly the same while the bits vary five-fold. <bookmark mark='c'/> So the "
            "unit of the limit is not the bit. Miller called it a chunk: any unit you already know, however much it "
            "contains. A letter, a word, a familiar phrase or a date can each be one chunk."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(b, DOWN) for b in bits_b], FadeIn(labs_a), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[GrowFromEdge(b, DOWN) for b in item_b], FadeIn(labs_b), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def recoding(self):
        d = load("recode")
        p = archive.MILLER_1956.data
        head = heading(r"Recoding, \ performed")
        stage = demo_stage(12.6, 3.2, center=[0, 1.45, 0])
        binary = d["binary"]
        octal = d["octal"]
        row = digits_row(binary, font_size=46, color=LOOP, buff=0.12).move_to(stage.box.get_center() + UP * 0.45)
        groups = VGroup(*[VGroup(*row[3 * k:3 * k + 3]) for k in range(len(binary) // 3)])
        names = VGroup(*[label(o, font_size=52, color=MEM).next_to(g, DOWN, buff=0.35) for g, o in zip(groups, octal)])
        braces = VGroup(*[Brace(g, DOWN, buff=0.06, color=GREY_C) for g in groups])
        key = label(r"000 = 0 \quad 001 = 1 \quad 010 = 2 \quad 011 = 3 \quad 100 = 4 \quad 101 = 5 \quad 110 = 6 "
                    r"\quad 111 = 7", font_size=22, color=GREY_B).next_to(stage.box, DOWN, buff=0.2)
        rows = rows_of([
            (rf"eighteen binary digits: \ far beyond a span of about {p['binary_span']}", LOOP),
            (r"read in threes, \ each triple is one octal digit: \ six chunks, \ inside the span", MEM),
            (rf"Sidney Smith trained himself to recode in fives, \ and repeated about {p['smith_binary_recoded']} "
             r"binary digits", EXEC),
            (r"chess masters recall real positions after a glance, \ random ones barely better than novices", GREY_A),
        ], 12.4, 25, 0.24).to_edge(DOWN, buff=0.8)
        tag = historical_tag(archive.MILLER_1956.cite)
        with self.voiceover(
            "Chunks can be made on purpose. <bookmark mark='a'/> Here are eighteen binary digits. Read once, at one a "
            f"second, they are far beyond a span of about {p['binary_span']}. <bookmark mark='b'/> Now read them in "
            "threes. Each triple is one octal digit: one, zero, one is five; zero, zero, zero is zero; one, zero, zero "
            "is four; and so on. Eighteen binary digits become six octal digits, comfortably inside the span, and to "
            "recall them you translate back. <bookmark mark='c'/> Miller reported that his colleague Sidney Smith "
            f"drilled this until it was automatic, in groups of up to five, and could repeat about "
            f"{p['smith_binary_recoded']} binary digits. <bookmark mark='d'/> Expertise does the same thing without "
            "the drill: a chess master glancing at a position from a real game sees a few familiar configurations, "
            "not twenty-five pieces, and recalls it almost perfectly, but does barely better than a novice when the "
            "pieces are placed at random. Chunks are knowledge. Which is why a span of seven digits says something "
            "about what you know about digits, as well as what you can hold."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(stage), FadeIn(row))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(braces), FadeIn(key))
            self.play(LaggedStart(*[FadeIn(n_, shift=DOWN * 0.15) for n_ in names], lag_ratio=0.5), FadeIn(rows[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
