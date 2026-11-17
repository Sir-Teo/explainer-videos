from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.scale()
        self.child()
        self.fit_worse()

    def card(self):
        card = chapter_card(14, r"Frontier: \ what language models show", r"Does a machine that learns language "
                            r"from text settle the old argument?", lit={2020: r"Warstadt et al.",
                                                                        2023: r"Oh \& Schuler",
                                                                        2024: r"Vong et al."},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter fourteen. Frontier: what language models show."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def scale(self):
        head = heading(r"Grammar from text, \ at a price")
        A = axes([0, 4], [6, 12.5], x_length=5.6, y_length=3.4, xticks=[], yticks=[6, 8, 10, 12],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", ylabel=r"words of language", center=[-3.3, 0.2, 0],
                 font_size=16)
        vals = [(r"Psyche's novels", np.log10(4.3e6), MODEL), (r"a child by 10, \ roughly", np.log10(5e7), WORD),
                (r"BabyLM's limit", 8.0, STAT), (r"GPT-3, \ 2020", np.log10(3e11), LOST)]
        bs = VGroup(*[bars(A.ax, [k + 0.5], [v], c, 0.6) for k, (_, v, c) in enumerate(vals)])
        names = VGroup(*[label(t, font_size=18, color=GREY_A).next_to(A.ax.c2p(k + 0.5, 6), DOWN,
                                                                      buff=0.12 + 0.22 * (k % 2))
                         for k, (t, _, _) in enumerate(vals)])
        rows = rows_of([
            (r"language models judge minimal pairs like \emph{the keys to the cabinet are} / \emph{is} \ mostly as "
             r"people do \ (BLiMP, \ Warstadt et al., \ 2020)", WHITE),
            (r"so a great deal of grammar can be learnt from strings alone: \ a blow to the strongest poverty-of-"
             r"stimulus claims", MODEL),
            (r"but from thousands of times more words than a child hears, \ and with no world attached", LOST),
            (r"the BabyLM challenge trains models on 100 million words or fewer, \ to ask what a child-sized input "
             r"allows", STAT),
        ], 5.4, 22, 0.33).move_to([3.7, 0.0, 0])
        note = label(r"orders of magnitude only; \ a child's input varies widely", font_size=18,
                     color=GREY_B).next_to(A, DOWN, buff=0.55)
        tag = published_tag(r"Warstadt et al. (2020); \ Brown et al. (2020)")
        with self.voiceover(
            "Machines that learn language from text alone have joined the old argument. <bookmark mark='a'/> Large "
            "language models judge pairs of sentences that differ in one grammatical point, like the keys to the "
            "cabinet are, against is, mostly as people do. <bookmark mark='b'/> So a great deal of grammar can be "
            "learned from strings alone, which is a blow to the strongest claims that the input is too poor. "
            "<bookmark mark='c'/> But look at the price. GPT-3 was trained on about three hundred billion tokens of "
            "text, thousands of times more words than a child hears by the age of ten, and none of it attached to a "
            "world. <bookmark mark='d'/> So researchers now train models on a child's budget. The BabyLM challenge "
            "limits them to a hundred million words or fewer, to ask what a child-sized input allows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b, DOWN) for b in bs], FadeIn(names), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def child(self):
        head = heading(r"Through the eyes of one child")
        cam = VGroup(RoundedRectangle(corner_radius=0.1, width=2.6, height=1.7, color=WORD),
                     Circle(radius=0.35, color=WORD).shift(RIGHT * 0.2)).move_to([-4.1, 1.5, 0])
        cl = label(r"a head-mounted camera", font_size=20, color=GREY_A).next_to(cam, DOWN, buff=0.15)
        # words linked to what the camera saw: a schematic of the model's test
        rng_ = np.random.default_rng(3)
        glyphs = [
            Circle(radius=0.28, color=WORD, fill_opacity=0.6),
            VGroup(RoundedRectangle(corner_radius=0.08, width=0.8, height=0.3, color=SOUND, fill_opacity=0.6),
                   Dot([-0.22, -0.2, 0], radius=0.08, color=GREY_A), Dot([0.22, -0.2, 0], radius=0.08, color=GREY_A)),
            VGroup(*[Dot([x_, y_, 0], radius=0.03, color=WORD) for x_, y_ in rng_.uniform(-0.4, 0.4, (40, 2))]),
            VGroup(Rectangle(width=0.8, height=0.45, color=GREY_A),
                   *[Line([x_, -0.22, 0], [x_, 0.22, 0], color=GREY_A, stroke_width=2) for x_ in (-0.2, 0, 0.2)]),
        ]
        frames = VGroup()
        for k, (g, w) in enumerate(zip(glyphs, ["ball", "car", "sand", "crib"])):
            fr = Square(1.1, color=GREY_B, stroke_width=1.5)
            g.move_to(fr)
            frames.add(VGroup(fr, g, word_chip(w, MODEL, 24).next_to(fr, DOWN, buff=0.12)))
        frames.arrange(RIGHT, buff=0.2).move_to([-4.1, -1.55, 0])
        fl = label(r"words matched to new pictures \ (schematic)", font_size=18, color=GREY_B).next_to(
            frames, DOWN, buff=0.15)
        rows = rows_of([
            (r"Vong, \ Wang, \ Orhan \& Lake, \ 2024: \ a network trained on about 61 hours of one child's "
             r"head-camera video and the speech heard with it, \ from 6 to 25 months", WHITE),
            (r"it learnt to link many everyday words to what they name, \ \emph{ball}, \ \emph{car}, \ "
             r"\emph{sand}, \ and to generalize to new pictures", MODEL),
            (r"a small slice of one child's life, \ with no innate grammar built in: \ evidence that word meaning, \ "
             r"at least, \ is learnable from what a child sees and hears", STAT),
            (r"what such models cannot yet show is how a child gets grammar from so little", LOST),
        ], 7.2, 22, 0.33).move_to([2.6, -0.2, 0])
        tag = published_tag(r"Vong, \ Wang, \ Orhan \& Lake (2024), \ \emph{Science}")
        with self.voiceover(
            "A different approach starts from the child. <bookmark mark='a'/> In 2024 Wai Keen Vong and colleagues "
            "trained a network on about sixty-one hours of video from a camera worn on one child's head, between six "
            "and twenty-five months of age, together with the speech the child heard. <bookmark mark='b'/> It learned "
            "to link many everyday words to what they name, like ball, car and sand, and to recognize new pictures "
            "of them. <bookmark mark='c'/> It's a small slice of one child's life, with no grammar built in, and it "
            "shows that word meaning, at least, can be learned from what a child sees and hears. "
            "<bookmark mark='d'/> What such models can't yet show is how a child gets a grammar from so little."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cam), FadeIn(cl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), LaggedStart(*[FadeIn(f_) for f_ in frames], lag_ratio=0.3),
                      FadeIn(fl), run_time=2.5)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def fit_worse(self):
        head = heading(r"Better models, \ worse readers?")
        rows = rows_of([
            (r"surprisal from better language models predicted reading times better, \ up to a point", WHITE),
            (r"Oh \& Schuler, \ 2023: \ beyond that point, \ larger transformers' surprisal fits human reading "
             r"times \emph{worse}", LOST),
            (r"they predict rare names and facts far better than a reader can, \ so their surprise and ours part "
             r"company", STAT),
            (r"the best model of a reader is not the best model of text: \ a reader's expectations are limited, \ "
             r"and that limit is the psychology", MODEL),
            (r"and this part's crude trigram already captured a cost of surprise: \ how much more a reader-shaped "
             r"model adds is open", GREY_A),
        ], 6.2, 24, 0.36).move_to([3.4, -0.1, 0])
        A = axes([0, 10], [0, 1.1], x_length=5.4, y_length=3.4, xticks=[], yticks=[],
                 xlabel=r"language model quality \ (lower perplexity)", ylabel=r"fit to reading times",
                 center=[-3.4, 0.3, 0], font_size=18)
        x = np.linspace(0, 10, 200)
        y = 0.15 + 0.75 * np.exp(-((x - 5.5) / 3.0) ** 2)
        up_ = curve(A.ax, x[x <= 5.5], y[x <= 5.5], MODEL, 3)
        down_ = curve(A.ax, x[x >= 5.5], y[x >= 5.5], LOST, 3)
        ends = VGroup(label(r"$n$-grams", font_size=19, color=GREY_A).next_to(A.ax.c2p(1.3, 0.0), UP, buff=0.1),
                      label(r"largest transformers", font_size=19, color=GREY_A).next_to(A.ax.c2p(9.0, 0.0), UP,
                                                                                     buff=0.1))
        sch = label(r"schematic of the reported pattern, \ not data", font_size=18, color=GREY_B).next_to(
            A, DOWN, buff=0.4)
        tag = published_tag(r"Oh \& Schuler (2023), \ \emph{TACL}")
        with self.voiceover(
            "And one more turn. <bookmark mark='a'/> For years, surprisal from better language models predicted "
            "reading times better. <bookmark mark='b'/> But in 2023 Byung-Doh Oh and William Schuler found that "
            "beyond a point, the surprisal of larger transformer models fits human reading times worse. "
            "<bookmark mark='c'/> The large models predict rare names and facts far better than a reader can, so "
            "their surprise and ours part company. <bookmark mark='d'/> The best model of a reader is not the best "
            "model of text. A reader's expectations are limited, and the shape of that limit is the psychology. "
            "<bookmark mark='e'/> Our crude trigram model already found a cost of surprise. How much more a "
            "reader-shaped model adds is an open question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(sch), FadeIn(ends))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), Create(up_))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.15), Create(down_))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
