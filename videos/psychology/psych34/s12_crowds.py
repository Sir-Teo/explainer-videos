from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403


class Crowds(VoiceoverScene):
    def construct(self):
        self.card()
        self.galton()
        self.identity()
        self.influence()
        self.market()

    def card(self):
        card = chapter_card(11, r"The wisdom and the herd", r"When is a crowd smarter than its members?",
                            lit={1907: r"Galton", 2006: r"Salganik et al.", 2011: r"Lorenz et al."}, part=PART,
                            scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter eleven. The wisdom and the herd."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def galton(self):
        head = heading(r"1907: \ the weight of an ox")
        A = axes([1150, 1250], [0, 1.0], x_length=7.0, y_length=1.8, xticks=[1150, 1175, 1200, 1225, 1250],
                 yticks=None, xfmt=lambda v: f"{v:.0f}", xlabel=r"pounds", center=[-2.4, 1.2, 0], font_size=15)
        marks = VGroup()
        for v, t, c, up in ((1198, r"the ox: \ 1{,}198", GOOD, 0.75), (1207, r"middle guess: \ 1{,}207", PERSON, 0.35)):
            ln = Line(A.ax.c2p(v, 0), A.ax.c2p(v, 1.0), color=c, stroke_width=4)
            marks.add(VGroup(ln, label(t, font_size=18, color=c).next_to(A.ax.c2p(v, up), RIGHT if v > 1200 else LEFT,
                                                                         buff=0.12)))
        rows = rows_of([
            (r"Francis Galton, \ \emph{Nature}, \ 1907: \ at a livestock fair in Plymouth, \ visitors paid to "
             r"guess the dressed weight of an ox; \ 787 tickets could be read", WHITE),
            (r"the middlemost guess was 1{,}207 pounds; \ the ox weighed 1{,}198: \ 0.8\% too high", PERSON),
            (r"Galton called it ``vox populi'': \ the median of a crowd, \ not any expert, \ was nearly right", CROWD),
            (r"a later look at his notes found small transcription errors, \ and that the mean, \ about 1{,}196, \ "
             r"was closer still", MODEL),
        ], 12.4, 21, 0.3).move_to([0, -1.6, 0])
        tag = historical_tag(r"Galton (1907); \ Wallis (2014)")
        with self.voiceover(
            "Crowds can also be wiser than the people in them. <bookmark mark='a'/> In 1907 Francis Galton wrote to "
            "Nature about a weight-judging competition at a livestock fair in Plymouth. Visitors paid to guess the "
            "weight of an ox once it was slaughtered and dressed, and seven hundred and eighty-seven tickets could be "
            "read. <bookmark mark='b'/> The middlemost guess was one thousand two hundred and seven pounds. The ox "
            "weighed one thousand one hundred and ninety-eight: the middle guess was less than one percent too high. "
            "That's the answer to your fourth number. <bookmark mark='c'/> Galton called it vox populi, the voice of "
            "the people. <bookmark mark='d'/> A later look at his notes found small errors in transcription, and "
            "that the crowd's mean, about eleven hundred and ninety-six, was closer still."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(marks[0][0]), FadeIn(marks[0][1]), Create(marks[1][0]), FadeIn(marks[1][1]),
                      FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def identity(self):
        d = load("crowd")
        x0 = np.asarray(d["x"])[0]
        idt = d["identity"]
        head = heading(r"Why the average beats most guessers")
        A = axes([-2.4, 3.0], [0, 1.0], x_length=6.2, y_length=2.2, xticks=[-2, -1, 0, 1, 2, 3], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"guess \ (log of guess over truth)", center=[-2.9, 0.9, 0],
                 font_size=15)
        rng = np.random.default_rng(1)
        dots = scatter(A.ax, x0, 0.15 + 0.6 * rng.random(len(x0)), CROWD, radius=0.045)
        truth = Line(A.ax.c2p(0, 0), A.ax.c2p(0, 1.0), color=GOOD, stroke_width=3)
        mean = Line(A.ax.c2p(idt["mean"], 0), A.ax.c2p(idt["mean"], 1.0), color=PERSON, stroke_width=3)
        key = legend([(GOOD, r"the truth"), (PERSON, r"the crowd's mean")], font_size=16).next_to(A, DOWN, buff=0.35)
        eq = MathTex(r"\underbrace{(\bar x - \theta)^2}_{\text{crowd's error}}", "=",
                     r"\underbrace{\overline{(x_i - \theta)^2}}_{\text{average error}}", "-",
                     r"\underbrace{\overline{(x_i - \bar x)^2}}_{\text{diversity}}", font_size=34).move_to([-2.9, -2.5, 0])
        nums = label(rf"{idt['collective']:.3f} \ = \ {idt['individual']:.3f} \ - \ {idt['diversity']:.3f}",
                     font_size=24, color=MODEL).next_to(eq, DOWN, buff=0.2)
        rows = rows_of([
            (r"144 of Psyche's people guess a quantity; \ each guess is off, \ and the crowd as a whole leans a "
             r"little high", WHITE),
            (r"an identity, \ true of any numbers: \ the crowd's squared error is the average person's squared error "
             r"minus the spread of the guesses", MODEL),
            (rf"so the mean beats the average guesser whenever people disagree; \ here it beats "
             rf"{pct(idt['beaten_by_mean'])} of them", PERSON),
            (r"the diversity has to be independent errors, \ not shared bias: \ the lean stays in the mean", AUTH),
        ], 5.4, 19, 0.3).move_to([3.7, -0.2, 0])
        tag = psyche_tag(r"\texttt{social.crowd}")
        with self.voiceover(
             "Why does it work? <bookmark mark='a'/> A hundred and forty-four of "
            "Psyche's people each guess a quantity. Every guess is off, and the crowd as a whole leans a little "
            "high. <bookmark mark='b'/> Now an identity that's true of any set of numbers. The crowd's squared "
            "error equals the average person's squared error, minus the spread of the guesses. "
            "<bookmark mark='c'/> So the mean beats the average guesser whenever people disagree. Here it beats "
            f"{spct(idt['beaten_by_mean'])} of them. <bookmark mark='d'/> But the disagreement has to be "
            "independent error. A bias everyone shares stays in the mean, however many people you ask."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(truth))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in dots], lag_ratio=0.01), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(mean), FadeIn(key), Write(eq), FadeIn(nums), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def influence(self):
        d = load("crowd")
        X = np.asarray(d["x"])
        head = heading(r"Show people the others' guesses")
        A = axes([-0.5, 5.5], [-2.4, 3.0], x_length=5.6, y_length=4.0, xticks=[0, 1, 2, 3, 4, 5],
                 yticks=[-2, -1, 0, 1, 2, 3], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"round", ylabel=r"guess \ (log scale)", center=[-3.1, -0.2, 0], font_size=15)
        rng = np.random.default_rng(2)
        cols = VGroup(*[scatter(A.ax, k + 0.25 * (rng.random(X.shape[1]) - 0.5), X[k], CROWD, radius=0.035)
                        for k in range(X.shape[0])])
        truth = DashedLine(A.ax.c2p(-0.5, 0), A.ax.c2p(5.5, 0), color=GOOD, stroke_width=2)
        lab = label(r"the truth", font_size=16, color=GOOD).next_to(A.ax.c2p(5.5, 0), UP, buff=0.08).shift(LEFT * 0.4)
        div, col = np.asarray(d["diversity"]), np.asarray(d["collective"])
        inr = np.asarray(d["truth_in_range"])
        lost = int(np.argmax(~inr)) if (~inr).any() else len(inr)
        rows = rows_of([
            (r"Lorenz, \ Rauhut, \ Schweitzer and Helbing, \ 2011: \ 144 people estimated quantities such as "
             r"border lengths and crime rates, \ in rounds; \ some saw the others' answers in between", WHITE),
            (r"Psyche: \ each round, \ everyone moves 40\% of the way to the crowd's mean", MODEL),
            (rf"the diversity falls from {div[0]:.2f} to {div[-1]:.3f}; \ the crowd's error stays at "
             rf"{col[0]:.3f}: \ agreement without accuracy", PERSON),
            (rf"by round {lost}, \ the truth lies outside every guess: \ a crowd that now sounds sure of a wrong "
             r"answer", AUTH),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.influence\_rounds}")
        with self.voiceover(
            "Independence is exactly what social influence takes away. <bookmark mark='a'/> In 2011 Lorenz and "
            "colleagues asked a hundred and forty-four people to estimate quantities such as border lengths and "
            "crime rates, over several rounds, and let some of them see the others' answers in between. <bookmark mark='b'/> Psyche's version: each round, everyone moves forty percent "
            "of the way toward the crowd's mean. <bookmark mark='c'/> The guesses close in. Diversity collapses, "
            "but the crowd's error doesn't move at all, because the mean was never the problem. It's agreement "
            f"without accuracy. <bookmark mark='d'/> By round {lost} the truth lies outside every guess anyone "
            "gives. The crowd now sounds sure of a wrong answer, which is the opposite of wisdom."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(truth), FadeIn(lab), FadeIn(cols[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in cols[1:]], lag_ratio=0.4), FadeIn(rows[2]), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def market(self):
        d = load("market")
        q = np.asarray(d["quality"])
        ind, soc = np.asarray(d["ind"]), np.asarray(d["soc"])
        head = heading(r"A market for songs, \ run eight times")
        ymax = float(max(ind.max(), soc.max())) * 1.08
        panels = VGroup()
        for k, (S_, nm, c) in enumerate(((ind, r"independent: \ no one sees the counts", CROWD),
                                        (soc, r"social: \ download counts shown", PERSON))):
            A = axes([0, 0.8], [0, ymax], x_length=4.2, y_length=3.0, xticks=[0, 0.2, 0.4, 0.6, 0.8], yticks=None,
                     xfmt=lambda v: f"{v:g}", xlabel=r"song quality", ylabel=r"market share" if k == 0 else "",
                     center=[-4.6 + 4.9 * k, 0.6, 0], font_size=13)
            pts = VGroup(*[scatter(A.ax, q, S_[w], c, radius=0.035) for w in range(S_.shape[0])])
            cap = label(nm, font_size=18, color=c).next_to(A, UP, buff=0.12)
            panels.add(VGroup(A, pts, cap))
        g_i, g_s = float(np.mean(d["gini_ind"])), float(np.mean(d["gini_soc"]))
        rows = rows_of([
            (r"Salganik, \ Dodds and Watts, \ 2006: \ 14{,}341 people, \ 48 songs by unknown bands; \ eight "
             r"worlds saw the download counts, \ one did not", WHITE),
            (rf"Psyche's market, \ 48 songs: \ with social information the shares grow unequal \ (Gini {g_i:.2f} "
             rf"to {g_s:.2f}) \ and the same song lands in very different places from world to world \ "
             rf"(unpredictability {d['u_ind']:.4f} to {d['u_soc']:.4f})", PERSON),
            (r"the best songs rarely did badly and the worst rarely did well; \ in between, \ early luck decided",
             YOU),
        ], 12.4, 19, 0.24).move_to([0, -2.55, 0])
        tag = psyche_tag(r"\texttt{social.music\_market}")
        with self.voiceover(
            "Influence doesn't only make crowds agree. It makes outcomes unpredictable. <bookmark mark='a'/> In "
            "2006 Salganik, Dodds and Watts built an online market of forty-eight songs by "
            "unknown bands, and fourteen thousand three hundred and forty-one people used it. They were split into "
            "separate worlds. In eight, everyone could see how many times each song had been downloaded; in one, "
            "nobody could. <bookmark mark='b'/> Here's Psyche's version, run as eight worlds of each kind. "
            "With social information, the shares grow more unequal, and the same song lands in very different "
            "places from one world to the next. <bookmark mark='c'/> Quality still matters at the ends. The best "
            "songs rarely did badly, and the worst rarely did well. In between, early luck decided, and it would "
            "decide differently if you ran history again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[2]) for p in panels])
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(*[LaggedStart(*[FadeIn(w) for w in p[1]], lag_ratio=0.3) for p in panels], FadeIn(rows[1]),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
