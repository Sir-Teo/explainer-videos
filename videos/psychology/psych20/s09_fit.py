from __future__ import annotations

from videos.psychology.psych20.common import *  # noqa: F403

NAMES = (
    (r"\beta_{\text{enc}}", r"drift at study"),
    (r"\beta_{\text{rec}}", r"drift at each recall"),
    (r"\beta_{\text{start}}", r"return to the list's start, \ at test"),
    (r"\gamma", r"share of study context in what a recall brings back"),
    (r"\phi_s", r"extra strength of the first words"),
    (r"\phi_d", r"how fast that extra strength falls"),
    (r"\tau", r"how deterministic the choice rule is"),
    (r"s_0", r"chance of stopping before the first recall"),
    (r"s_r", r"growth of that chance per recall"),
)


class Fit(VoiceoverScene):
    def construct(self):
        self.card()
        self.likelihood()
        self.params()
        self.heldout()
        self.predictions()

    def card(self):
        card = chapter_card(8, r"Fitting the context model", r"How well does one drifting state account for real "
                            r"recall?", lit={2009: r"Polyn et al.", 2014: r"PEERS", 2016: r"Morton \& Polyn"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter eight. Fitting the context model."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def likelihood(self):
        c = load("cmr")
        head = heading(r"The likelihood of a recall sequence")
        seq = VGroup(*[word_chip(WORDS[p - 1], font_size=22) for p in (16, 15, 14, 1, 2)]).arrange(RIGHT, buff=0.25)
        seq.add(label(r"stop", font_size=24, color=LOST))
        seq.arrange(RIGHT, buff=0.25).move_to([0, 2.2, 0])
        eq = MathTex(r"\log L", r"=", r"\sum_{\text{lists}} \Big[ \sum_{j} \log\big( (1 - s_j)\,"
                     r"P(w_j \mid \mathbf{c}_j) \big)", r"+", r"\log s_{\text{end}} \Big]", font_size=38)
        eq.move_to([0, 0.9, 0])
        eq[2].set_color(MODEL)
        eq[4].set_color(LOST)
        rows = rows_of([
            (r"run the model along each person's actual sequence: \ at every step, \ what probability did it give "
             r"the word they said?", WHITE),
            (r"stopping is part of the data: \ $s_j = s_0\, e^{s_r j}$ after $j$ recalls", LOST),
            (rf"fit on every other list, \ {num(c['n_fit'])} lists; \ test on the other {num(c['n_test'])}", MODEL),
            (r"nine parameters, \ kept in range by a logistic transform, \ found by the simplex method", GREY_A),
            (r"exact, \ fast, \ and it uses every transition: \ better than matching a few curves", CUE),
        ], 12.4, 24, 0.28).to_edge(DOWN, buff=0.6)
        ptag = psyche_tag(r"\texttt{memory.cmr\_loglik}, \ \texttt{memory.fit\_cmr\_ml}")
        with self.voiceover(
            "A model this specific can be fitted properly. <bookmark mark='a'/> Take one person's recall of one "
            "list: sixteen, fifteen, fourteen, one, two, then stop. Run the model along that exact sequence. At "
            "each step, ask what probability it gave the word the person actually said, given everything said so "
            "far. <bookmark mark='b'/> Stopping is data too: the model has a probability of stopping after each "
            "recall, and the sequence ends with one. The product of all those probabilities, over all the lists, is "
            "the likelihood. <bookmark mark='c'/> We fit on half the lists, every other one, and keep the other half "
            "aside to test. <bookmark mark='d'/> There are nine parameters, held in their ranges by a logistic "
            "transform, and the simplex method of Nelder and Mead finds the values that make the observed sequences "
            "most probable. <bookmark mark='e'/> This uses every single transition people made, not just three "
            "summary curves, and it's exact, with no simulation noise. It's how the context model is fitted in "
            "current research."
        ) as vo:
            self.play(FadeIn(head), FadeIn(seq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(ptag))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def params(self):
        c = load("cmr")
        head = heading(r"The fitted parameters")
        vals = c["params"]
        rows = VGroup()
        for (sym, what), v in zip(NAMES, vals):
            fmt = f"{v:.3f}" if v < 0.1 else f"{v:.2f}"
            rows.add(VGroup(MathTex(sym, font_size=32, color=MODEL), MathTex(fmt, font_size=32),
                            label(what, font_size=22, color=GREY_A)))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.0)
        tab = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for r in rows:
            r[0].move_to([-6.1, r.get_center()[1], 0])
            r[1].move_to([-4.8, r.get_center()[1], 0])
            r[2].next_to([-4.1, r.get_center()[1], 0], RIGHT, buff=0.0)
        tab.move_to([-2.4, -0.15, 0])
        B_enc, B_rec, B_start, gamma = vals[0], vals[1], vals[2], vals[3]
        rho = np.sqrt(1 - B_enc ** 2)
        notes = rows_of([
            (rf"$\rho = \sqrt{{1 - \beta^2}} = {rho:.2f}$: \ most of the context is replaced at each word", CTX),
            (rf"$\gamma = {gamma:.2f}$: \ a recall brings back mostly the word's own features: \ forward-leaning",
             WORD),
            (rf"log-likelihood on the fitted half: \ {c['loglik']:.0f}", GREY_A),
        ], 3.9, 20, 0.3).move_to([4.95, -0.2, 0])
        ptag = psyche_tag(rf"\texttt{{memory.fit\_cmr\_ml}}: \ {num(c['evals'])} likelihood evaluations")
        with self.voiceover(
            "Here are the nine numbers. <bookmark mark='a'/> The drift at study is large: "
            f"beta is {B_enc:.2f}, so rho is {rho:.2f}, and most of the context is renewed with each word. Recency "
            "in immediate recall is steep, and the model has to make it so. <bookmark mark='b'/> Gamma, the share "
            f"of study context in what a recall brings back, is {gamma:.2f}. Most of what comes back is the word's "
            "own features, the forward-leaning part. <bookmark mark='c'/> The first words carry a large extra "
            "strength that falls away within a few positions, the model's stand-in for Rundus's extra rehearsal. And "
            "the stopping rule grows steeply with each recall. <bookmark mark='d'/> None of these numbers was chosen "
            "to make a picture. They are the values that make three and a half thousand recall sequences most "
            "probable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ptag))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=CTX), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Indicate(rows[3], color=WORD), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(rows[4]), Indicate(rows[5]), Indicate(rows[8]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def heldout(self):
        c = load("cmr")
        head = heading(r"Checked on the lists it never saw")
        x = np.arange(1, 17)
        A = position_axes([-4.5, 0.45, 0], x_length=3.8, y_length=2.4, font_size=16)
        B = position_axes([0.0, 0.45, 0], x_length=3.8, y_length=2.4, ymax=0.6, font_size=16,
                          ylabel=r"recalled first")
        C = lag_axes([4.5, 0.45, 0], x_length=3.8, y_length=2.4, font_size=16, max_lag=4)
        ax, bx, cx = A.ax, B.ax, C.ax
        keep = np.abs(c["lags"]) <= 4
        g = VGroup(
            curve_in(ax, x, c["test_spc"], DATA, 4), curve_in(ax, x, c["immediate_spc"], MODEL, 4),
            curve_in(bx, x, c["test_pfr"], DATA, 4), curve_in(bx, x, c["immediate_pfr"], MODEL, 4),
            crp_curves(cx, c["lags"][keep], c["test_crp"][keep], DATA),
            crp_curves(cx, c["lags"][keep], c["immediate_crp"][keep], MODEL),
        )
        key = legend([(DATA, r"held-out half of PEERS"), (MODEL, r"the fitted model, \ simulated")],
                     font_size=19)
        key.arrange(RIGHT, buff=0.8).move_to([0, 2.75, 0])
        head.to_edge(UP, buff=0.25)
        bits = rows_of([
            (rf"each held-out recall, \ {num(c['test_recalls'])} of them: \ how surprised is each account by the "
             r"word people said?", WHITE),
            (rf"chance among the words left: \ {c['bits_chance']:.2f} bits; \ the serial-position curve alone: \ "
             rf"{c['bits_position']:.2f} bits; \ the context model: \ {c['bits_cmr']:.2f} bits", MODEL),
            (r"what it misses: \ too little primacy and too low a peak at $+1$, \ too much in the middle; \ the full "
             r"model adds the words' meanings and a source context", LOST),
        ], 12.6, 22, 0.24).to_edge(DOWN, buff=0.55)
        ptag = psyche_tag(r"\texttt{memory.cmr\_simulate}: \ 4,000 lists at the fitted values")
        with self.voiceover(
            "Now the test. These are the lists held out from the fit. <bookmark mark='a'/> The serial-position "
            "curve, the probability of first recall, and the lag-conditional response probability, in the data and "
            "in the fitted model, simulated. The model starts recall at the end of the list as people do, reproduces "
            "the U shape, and gives a lag curve that peaks at plus one and leans forward. "
            "<bookmark mark='b'/> A sharper test uses every held-out recall. For each word a person said, how much "
            "did each account expect it? Measured in bits, lower is better. Choosing at random among the words left "
            f"costs {c['bits_chance']:.2f} bits per recall. Knowing only the serial-position curve, "
            f"{c['bits_position']:.2f}. The context model, {c['bits_cmr']:.2f}: it predicts which word comes next "
            "far better than position alone can. <bookmark mark='c'/> And it's honest to say what it misses. It "
            "gives the first words too little advantage, the peak at plus one too little height, and the middle of "
            "the list a little too much. The full versions of the model "
            "add each word's meaning, so that related words cue each other, and a separate context for the task at "
            "study; they close much of that gap."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(C), FadeIn(key), FadeIn(ptag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(m) for m in g], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(bits[0]), FadeIn(bits[1]))
            vo.wait_until("c")
            self.play(FadeIn(bits[2]))
        self.clear_scene()

    def predictions(self):
        c = load("cmr")
        head = heading(r"Tested on two other experiments")
        x = np.arange(1, 17)
        A = position_axes([-2.9, 0.35, 0], x_length=6.4, y_length=3.6)
        ax = A.ax
        cs = VGroup(curve_in(ax, x, c["immediate_spc"], MODEL, 4), curve_in(ax, x, c["delayed_spc"], LOST, 4),
                    curve_in(ax, x, c["continual_spc"], CTX, 4))
        key = legend([(MODEL, r"immediate"), (LOST, r"a filled delay before recall"),
                      (CTX, r"a filled gap after every word")], font_size=19).move_to(ax.c2p(8.5, 0.22))
        rows = rows_of([
            (r"the same fitted model; \ a distractor is a drift toward new context that belongs to no word", WHITE),
            (rf"a delay at the end: \ recency goes, \ {pct(c['immediate_spc'][-1])} to {pct(c['delayed_spc'][-1])}; "
             rf"\ recall now starts at the first word: \ Glanzer and Cunitz", LOST),
            (r"a gap after every word: \ recency does \emph{not} come back: \ this model fails Bjork and Whitten",
             CTX),
            (r"why: \ once every word is far away, \ the pull back to the list's start and the first word's extra "
             r"strength win", GREY_A),
            (r"the models that pass let the words race against noise, \ so that standing out from your neighbours "
             r"is what counts \ (Sederberg, \ Howard and Kahana, \ 2008)", MODEL),
        ], 5.6, 20, 0.26).move_to([3.8, -0.25, 0])
        ptag = psyche_tag(r"\texttt{memory.cmr\_simulate}: \ drift 0.99 toward new context, \ at the end or after "
                          r"every word")
        with self.voiceover(
            "Finally, the two experiments that broke the two-store story. A distractor task, in the model, is a drift "
            "toward new context that belongs to no word. <bookmark mark='a'/> Put a long stretch of it between the "
            "last word and recall. <bookmark mark='b'/> Recency goes, and recall now tends to start at the "
            "beginning of the list: Glanzer and Cunitz's result, with no short-term store to empty. "
            "<bookmark mark='c'/> Now put the same distraction after every word. If the ratio argument of the last "
            "chapter held in this model, the last words would stand out again. They don't. Our fitted model fails "
            "Bjork and Whitten's test. <bookmark mark='d'/> The reason is instructive. Once every word is far "
            "away, what's left is the pull back to the start of the list and the first word's extra strength, and "
            "they don't shrink with the rest, so they win. <bookmark mark='e'/> The versions of the model that "
            "pass this test, beginning with Per Sederberg, Howard and Kahana's in 2008, let the words race against "
            "noise, so that what matters is how much a word stands out from its neighbours. A model fitted to one "
            "kind of experiment and tested on another is how you find what it is missing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(key), Create(cs[0]), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cs[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
