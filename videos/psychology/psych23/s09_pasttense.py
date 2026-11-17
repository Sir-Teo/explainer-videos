from __future__ import annotations

from videos.psychology.psych23.common import *  # noqa: F403


class PastTense(VoiceoverScene):
    def construct(self):
        self.card()
        self.ushape()
        self.network()
        self.debate()

    def card(self):
        card = chapter_card(8, r"Rules or associations?", r"Does a child who says \emph{goed} know a rule?",
                            lit={1986: r"Rumelhart \& McClelland", 1988: r"Pinker \& Prince", 1992: r"Marcus et al."},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter eight. Rules or associations?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ushape(self):
        head = heading(r"\emph{went}, \ then \emph{goed}, \ then \emph{went}")
        A = axes([0, 3], [0, 1], x_length=5.6, y_length=3.0, xticks=[], yticks=[0, 0.5, 1], yfmt=lambda v: f"{v:.1f}",
                 ylabel=r"irregular past tenses right", center=[-3.2, 0.4, 0], font_size=16)
        x = np.linspace(0, 3, 100)
        y = 0.92 - 0.25 * np.exp(-((x - 1.5) / 0.45) ** 2)
        y[x < 0.4] = 0.92 * (x[x < 0.4] / 0.4) ** 0.5
        c = curve(A.ax, x, y, WORD, 3)
        ages = VGroup(*[label(t, font_size=17, color=GREY_A).next_to(A.ax.c2p(xx, 0), DOWN, buff=0.15)
                        for t, xx in ((r"early: \ \emph{went}", 0.6), (r"\emph{goed}", 1.5), (r"later: \ \emph{went}",
                                                                                               2.5))])
        sl = label(r"schematic", font_size=15, color=GREY_B).next_to(A, DOWN, buff=0.45).align_to(A, RIGHT)
        rows = rows_of([
            (r"young children often say \emph{went}, \ then for a while also \emph{goed}, \ then \emph{went} again: \ "
             r"a U-shaped curve", WHITE),
            (r"the \emph{goed} stage looks like a rule being learnt, \ add \emph{-ed}, \ and over-applied", RULE),
            (r"Marcus and colleagues, \ 1992: \ in 25 children's recorded speech, \ over-regularization averaged "
             r"only 4.2\% of irregular past tenses", STAT),
            (r"so the dip is real, \ but shallow: \ errors at a low rate across years, \ not a collapse", GREY_A),
        ], 5.6, 22, 0.33).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Marcus et al. (1992)")
        with self.voiceover(
            "Children's errors are the best evidence about what they learn. <bookmark mark='a'/> Young children "
            "often say went correctly. Then, for a while, they also say goed. Later went comes back. That's the "
            "famous U-shaped curve. <bookmark mark='b'/> The goed stage looks like a rule being learned, add ed, "
            "and applied too widely. <bookmark mark='c'/> How deep is the dip? Gary Marcus and colleagues counted it "
            "in the recorded speech of twenty-five children in 1992. Over-regularization averaged only 4.2 percent "
            "of the irregular past tenses they used. <bookmark mark='d'/> So the dip is real but shallow: errors at a "
            "low rate across years, not a collapse. The curve drawn here is a schematic of the pattern."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(sl))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(ages), FadeIn(rows[0]), run_time=2)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def network(self):
        d = load("pasttense")
        head = heading(r"A network learns the past tense")
        n = len(d["right"])
        stage1 = int((d["stage"] == 0).sum())
        A = axes([0, n], [0, 1], x_length=6.2, y_length=3.4, xticks=[0, stage1, n], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"training epochs",
                 ylabel=r"probability, \ ten early irregulars", center=[-2.9, 0.3, 0], font_size=16)
        t = np.arange(1, n + 1)
        right = curve(A.ax, t, d["right"], WORD, 3)
        over = curve(A.ax, t, d["over"], LOST, 3)
        flood = DashedLine(A.ax.c2p(stage1, 0), A.ax.c2p(stage1, 1), color=GREY_B)
        fl = label(rf"{d['n_regular']} regular \\ verbs arrive", font_size=19, color=GREY_B).next_to(
            A.ax.c2p(stage1, 0.68), RIGHT, buff=0.12)
        key = legend([(WORD, r"the right form \ (\emph{went})"), (LOST, r"\emph{add -ed} \ (\emph{goed})")],
                     font_size=17).move_to(A.ax.c2p(n * 0.72, 0.5))
        k_dip = stage1 + int(np.argmin(d["right"][stage1:stage1 + 6]))
        rows = rows_of([
            (r"each verb is input two ways: \ a unit for the verb itself, \ and units for its last letters, \ shared "
             r"with every verb that ends the same", WHITE),
            (r"first, \ ten common verbs, \ mostly irregular: \ learnt by heart", WORD),
            (rf"then the vocabulary floods with regulars: \ \emph{{add -ed}} wins on shared endings, \ and the "
             rf"irregulars dip from {d['right'][stage1 - 1]:.2f} to {d['right'][k_dip]:.2f}", LOST),
            (r"with more training, \ each verb's own unit wins back: \ a U, \ from one mechanism with no rule in it",
             MODEL),
        ], 5.0, 22, 0.33).move_to([3.9, 0.0, 0])
        ptag = psyche_tag(r"\texttt{language.past\_tense\_learner}")
        with self.voiceover(
            "In 1986 David Rumelhart and James McClelland built a network that learned the past tense with no rule "
            "anywhere in it. Psyche's version is smaller. <bookmark mark='a'/> Each verb comes in two ways at once: "
            "a unit for the verb itself, and units for its last letters, shared with every verb that ends the same "
            "way. The output picks add ed, or one of the irregular forms. <bookmark mark='b'/> First it learns ten "
            "common verbs, mostly irregular, like go, be and have, and learns them by heart. <bookmark mark='c'/> "
            f"Then the vocabulary floods with {d['n_regular']} regular verbs. The add ed answer starts to win through "
            "the shared endings, and for a while the irregulars slip: the network says goed. "
            "<bookmark mark='d'/> With more training, each verb's own unit wins back its form. A U-shaped curve, "
            "from a single mechanism with no rule in it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(right), Create(over), FadeIn(key), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(flood), FadeIn(fl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def debate(self):
        head = heading(r"Words and rules")
        left = VGroup(label(r"Pinker \& Prince, \ 1988", font_size=28, color=RULE),
                      rows_of([(r"the original network's U came from changing its training set, \ as Psyche's does: "
                                r"\ children's vocabulary grows more smoothly", WHITE),
                               (r"it struggled with new verbs and with homophones: \ \emph{ring, rang} \ but \ "
                                r"\emph{wring, wrung}, \ one sound, \ two pasts", GREY_A),
                               (r"their account: \ irregulars are stored words; \ regulars come from a rule", RULE)],
                              5.5, 25, 0.38)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        right = VGroup(label(r"the networks' reply", font_size=28, color=STAT),
                       rows_of([(r"later networks learnt without the change of training set, \ and generalized to new "
                                 r"verbs much as people do", WHITE),
                                (r"irregulars come in families \ (\emph{sing, sang}; \ \emph{ring, rang}), \ "
                                 r"as one graded mechanism expects", GREY_A),
                                (r"the dispute moved to the brain and to other languages, \ and is not settled", STAT)],
                               5.5, 25, 0.38)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        for k, (side, col_) in enumerate(((left, RULE), (right, STAT))):
            box = RoundedRectangle(corner_radius=0.15, width=6.2, height=4.9, stroke_color=col_, stroke_width=2,
                                   fill_color=col_, fill_opacity=0.06).move_to([-3.35 + 6.7 * k, 0.35, 0])
            side.move_to(box.get_top() + DOWN * 0.3, aligned_edge=UP).align_to(box, LEFT).shift(RIGHT * 0.3)
            side.add_to_back(box)
        rows = rows_of([
            (r"what both sides agree: \ a child's past tense is generalization, \ not imitation", MODEL)],
            12.6, 27, 0.3).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Rumelhart \& McClelland (1986); \ Pinker \& Prince (1988)")
        with self.voiceover(
            "The network started the most argued-over debate in cognitive science. <bookmark mark='a'/> In 1988 "
            "Steven Pinker and Alan Prince pointed out that the original network's U came from changing its training "
            "set suddenly, just as Psyche's does, while children's vocabularies grow more smoothly. It also struggled "
            "with new verbs and with words that sound the same but take different pasts. Their alternative: "
            "irregular forms are stored as words, and regular forms come from a rule. <bookmark mark='b'/> The "
            "networks replied. Later models learned without the sudden change and generalized to new verbs much as "
            "people do, and irregular verbs come in families, like sing, sang and ring, rang, which a network "
            "captures naturally. The dispute moved on to the brain and to other languages, and it is not settled. "
            "<bookmark mark='c'/> What both sides agree on is this: a child's past tense is generalization, not "
            "imitation. No adult says goed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
        self.clear_scene()
