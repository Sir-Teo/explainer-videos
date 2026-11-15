from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403

GAP_COL = (LOST, CUE, TRACE)


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.study()
        self.apps()
        self.hlr()
        self.calibration()
        self.lineups()

    def card(self):
        card = chapter_card(13, r"In practice: \ study, \ apps, \ line-ups",
                            r"Where has knowing how memory fails changed what people do?",
                            lit={2013: r"Dunlosky et al.", 2016: r"Settles \& Meeder", 2020: r"Wells et al."},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: study, apps, line-ups."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def study(self):
        d = archive.DUNLOSKY_2013.data
        head = heading(r"Ten ways to study, \ rated")
        cols = VGroup()
        for name, items, col in ((r"high utility", d["high"], GOOD), (r"moderate", d["moderate"], CUE),
                                 (r"low utility", d["low"], LOST)):
            cols.add(VGroup(label(name, font_size=28, color=col),
                            *[label(i, font_size=23, color=GREY_A) for i in items]).arrange(DOWN, buff=0.18))
        cols.arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 0.8, 0])
        rows = rows_of([
            (r"Dunlosky, \ Rawson, \ Marsh, \ Nathan and Willingham, \ 2013: \ ten techniques, \ judged on how well "
             r"they work across learners, \ materials, \ tests and delays", WHITE),
            (r"the two at the top are this part's chapters 5 and 6; \ the most popular, \ re-reading and "
             r"highlighting, \ are at the bottom", TRACE),
            (r"students choose by how fluent study feels, \ and chapter 6 showed that feeling misleads", FALSE),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(archive.DUNLOSKY_2013.cite)
        with self.voiceover(
            "Three places where this part's science is put to work. The first is study. <bookmark mark='a'/> In "
            "2013 John Dunlosky, Katherine Rawson, Elizabeth Marsh, Mitchell Nathan and Daniel Willingham rated ten "
            "techniques students use, by how well each works across learners, materials, kinds of test and delays. "
            "<bookmark mark='b'/> Two came out at the top: practice testing and distributed practice, chapters five "
            "and six. And at the bottom, among others, the two that students use most: re-reading and "
            "highlighting. <bookmark mark='c'/> Students choose by how study feels, and as Roediger and Karpicke "
            "showed, that feeling misleads."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cols], lag_ratio=0.4), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def apps(self):
        head = heading(r"Spacing by machine")
        boxes = VGroup(*[VGroup(Rectangle(width=1.5, height=1.0, color=c), label(t, font_size=20, color=c))
                         for t, c in ((r"box 1: \ daily", LOST), (r"box 2: \ every 2 days", CUE),
                                      (r"box 3: \ every 4 days", CTX), (r"box 4: \ every 8 days", TRACE))])
        for b in boxes:
            b[1].move_to(b[0])
        boxes.arrange(RIGHT, buff=0.5).move_to([0, 1.7, 0])
        fwd = VGroup(*[CurvedArrow(a.get_top(), b.get_top(), angle=-0.8, color=GOOD, stroke_width=2)
                       for a, b in zip(boxes[:-1], boxes[1:])])
        back = CurvedArrow(boxes[-1].get_bottom(), boxes[0].get_bottom(), angle=-0.5, color=LOST, stroke_width=2)
        fl = label(r"right: \ move up", font_size=18, color=GOOD).next_to(fwd, UP, buff=0.05)
        bl = label(r"wrong: \ back to the start", font_size=18, color=LOST).next_to(back, DOWN, buff=0.05)
        rows = rows_of([
            (r"Leitner's boxes, \ 1970s: \ a flashcard's interval doubles each time you get it right", WHITE),
            (r"SuperMemo, \ Anki and their descendants: \ an interval set by how hard each card has been for you", CUE),
            (r"Duolingo, \ 2016: \ \emph{half-life regression}, \ a forgetting curve whose half-life is learnt from "
             r"millions of practice sessions", TRACE),
        ], 12.4, 24, 0.3).to_edge(DOWN, buff=0.65)
        with self.voiceover(
            "The second is software. If the best time to review depends on how strong a memory is, a computer can "
            "keep track for you. <bookmark mark='a'/> The oldest scheme is Sebastian Leitner's boxes, from the "
            "1970s: flashcards sit in boxes reviewed at doubling intervals. Get a card right and it moves up a box; "
            "get it wrong and it goes back to the start. <bookmark mark='b'/> Programs like SuperMemo and Anki set "
            "each card's interval from how hard it has been for you. <bookmark mark='c'/> And in 2016 Burr Settles "
            "and Brendan Meeder described the model Duolingo built, half-life regression: a forgetting curve for "
            "every word and every learner, whose half-life is learnt from the practice data of millions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(rows[0]))
            self.play(LaggedStart(*[Create(a) for a in fwd], lag_ratio=0.3), FadeIn(fl), Create(back), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def hlr(self):
        d = load("hlr")
        th = d["theta"]
        head = heading(r"Derivation: \ half-life regression")
        eqs = VGroup(
            MathTex(r"p = 2^{-\Delta / h}", font_size=40, color=TRACE),
            MathTex(r"h = 2^{\,\boldsymbol{\theta} \cdot \mathbf{x}}", font_size=40, color=MODEL),
            MathTex(r"\mathbf{x} = \big(\sqrt{\text{times right}},\ \sqrt{\text{times wrong}},\ 1\big)",
                    font_size=30),
            MathTex(r"\min_{\boldsymbol\theta} \sum (y - p)^2 + \lambda \|\boldsymbol\theta\|^2", font_size=34,
                    color=CUE),
        ).arrange(DOWN, buff=0.32).move_to([-3.8, 0.4, 0])
        A = axes([0, 14], [0, 1], x_length=5.4, y_length=3.0, xticks=[0, 7, 14], yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"days since the last practice $\Delta$",
                 ylabel=r"predicted recall", center=[3.4, 0.9, 0], font_size=18)
        cs = VGroup(*[curve(A.ax, d["gaps"], d[f"curve_right{r}"], GAP_COL[i], 4) for i, r in enumerate((0, 2, 6))])
        key = legend([(GAP_COL[i], rf"right {r} times before") for i, r in enumerate((0, 2, 6))],
                     font_size=19).move_to([4.9, 1.6, 0])
        rows = rows_of([
            (r"recall halves every $h$ days: \ a forgetting curve with one number", TRACE),
            (rf"each right answer lengthens the half-life, \ each wrong one shortens it: \ fitted "
             rf"$\theta = ({th[0]:.2f},\ {th[1]:.2f},\ {th[2]:.2f})$", MODEL),
            (rf"on {num(d['rows'])} simulated practice events \ (the true $\theta$ was "
             rf"$({d['true_theta'][0]:.1f},\ {d['true_theta'][1]:.1f},\ {d['true_theta'][2]:.1f})$, \ plus a "
             r"difficulty for each word)", GREY_A),
        ], 6.0, 20, 0.25).move_to([3.4, -1.75, 0])
        ptag = psyche_tag(r"\texttt{memory.fit\_hlr}, \ on simulated learners")
        with self.voiceover(
            "Here's the model. <bookmark mark='a'/> The chance of recalling a word falls by half every h days: p "
            "equals two to the minus delta over h, a forgetting curve with one number, the half-life. "
            "<bookmark mark='b'/> The half-life is two to the power theta dot x, where x describes the learner's "
            "history with the word: the square roots of how many times they've got it right and how many times "
            "wrong, and a constant. In the paper, x also holds features of the word itself. "
            "<bookmark mark='c'/> Fit theta by least squares on whether each practice was recalled. "
            "<bookmark mark='d'/> We can't use Duolingo's data here, so this fit is to simulated learners whose "
            f"true theta we know. The fit recovers it: right answers lengthen the half-life, by {th[0]:.2f} doublings "
            f"per root of a right answer, and wrong ones shorten it, by {abs(th[1]):.2f}. "
            "<bookmark mark='e'/> And the curves show the result: the more times you've got a word right, the "
            "longer you can wait before you're likely to forget it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), Write(eqs[2]))
            vo.wait_until("c")
            self.play(Write(eqs[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(A), LaggedStart(*[Create(c) for c in cs], lag_ratio=0.3), FadeIn(key))
        self.clear_scene()

    def calibration(self):
        d = load("hlr")
        head = heading(r"Does it predict? \ Checked on held-out practice")
        A = axes([0, 1], [0, 1], x_length=4.4, y_length=4.0, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"predicted recall", ylabel=r"recalled", center=[-3.9, -0.1, 0], font_size=18)
        diag = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 1), color=GREY_D)
        ok = np.isfinite(d["cal_pred"]) & (d["cal_n"] >= 30)
        pts = scatter(A.ax, d["cal_pred"][ok], d["cal_obs"][ok], MODEL, 0.09, 1.0)
        line = curve(A.ax, d["cal_pred"][ok], d["cal_obs"][ok], MODEL, 3)
        B = axes([0, 3], [0, 0.4], x_length=4.0, y_length=3.0, xticks=[], yticks=[0, 0.2, 0.4],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"mean absolute error", center=[1.2, 0.1, 0], font_size=18)
        mae = [d["mae_const"], d["mae_leitner"], d["mae_hlr"]]
        bb = bars(B.ax, np.arange(3) + 0.5, mae, GREY_B, width=0.55)
        bb[2].set_fill(MODEL)
        names = VGroup(*[label(t, font_size=19, color=GREY_A).next_to(B.ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
                         for i, t in enumerate((r"one average", r"Leitner", r"HLR"))])
        vals = VGroup(*[label(f"{v:.3f}", font_size=19, color=GREY_A).next_to(b, UP, buff=0.06) for b, v in
                        zip(bb, mae)])
        rows = rows_of([
            (rf"every fifth event held out: \ {num(d['test_rows'])} of them", GREY_A),
            (r"the predictions are calibrated: \ when it says 80\%, \ about 80\% are recalled", MODEL),
            (r"Settles and Meeder, \ on 13 million real practice traces: \ error cut by 45\% or more against the "
             r"baselines, \ and 12\% more daily engagement in a live test", DATA),
            (r"the same object as Ebbinghaus's curve, \ now estimated for every learner and word", TRACE),
        ], 4.0, 20, 0.3).move_to([5.1, -0.1, 0])
        with self.voiceover(
            "The test of a model like this is prediction, on practice it never saw. <bookmark mark='a'/> We held "
            "out every fifth practice event. Group them by the predicted chance of recall: when the model says "
            "eighty percent, about eighty percent were recalled. The predictions are calibrated. "
            "<bookmark mark='b'/> And its error is lower than a single average, and lower than Leitner's boxes. "
            "<bookmark mark='c'/> On real data, thirteen million practice traces, Settles and Meeder reported "
            "errors forty-five percent or more below those of the baselines, and when Duolingo used it to "
            "schedule practice, daily engagement went up by twelve percent. <bookmark mark='d'/> It's Ebbinghaus's curve, a hundred and thirty "
            "years on, estimated for every learner and every word."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(diag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(pts), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(names), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bb], lag_ratio=0.3),
                      FadeIn(vals))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lineups(self):
        head = heading(r"Line-ups, \ interviews, \ therapy")
        rows = rows_of([
            (r"line-ups: \ the procedures of chapter 10 are now recommended practice \ (Wells and colleagues, \ "
             r"2020), \ and the US Department of Justice adopted many of them in 2017", CUE),
            (r"record the witness's confidence at the first identification, \ in their own words, \ before any "
             r"feedback", TRACE),
            (r"interviews: \ open questions first, \ no leading ones; \ the cognitive interview of Part 20", CTX),
            (r"therapy: \ imagining an event can make people more confident it happened \ (imagination inflation, \ "
             r"Garry and colleagues, \ 1996); \ techniques that ask people to imagine or recover memories carry "
             r"that risk", FALSE),
            (r"memory evidence is like physical evidence: \ it can be contaminated, \ and procedures can prevent "
             r"that \ (Wixted and Wells)", MODEL),
        ], 12.4, 24, 0.34).move_to([0, -0.2, 0])
        tag = historical_tag(r"Wells et al.\ (2020); \ Garry et al.\ (1996)")
        with self.voiceover(
            "The third place is the justice system, and the clinic. <bookmark mark='a'/> The line-up procedures of "
            "chapter ten are now the field's formal recommendations, set out by Gary Wells and colleagues in 2020, "
            "and the United States Department of Justice adopted many of them in 2017. <bookmark mark='b'/> Above "
            "all: record the witness's confidence at the first identification, in their own words, before anyone "
            "says anything. <bookmark mark='c'/> In interviews, open questions first, and none that lead, as in the "
            "cognitive interview of the last part. <bookmark mark='d'/> And in therapy, a caution. Maryanne Garry "
            "and colleagues showed in 1996 that just imagining a childhood event makes people more confident it "
            "happened, so techniques that ask people to imagine, or to recover, memories carry that risk. "
            "<bookmark mark='e'/> Wixted and Wells put the principle simply: memory is like trace evidence. It can "
            "be contaminated, and good procedures prevent that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
