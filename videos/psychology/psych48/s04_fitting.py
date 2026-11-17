from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Fitting(VoiceoverScene):
    def construct(self):
        self.card()
        self.ml()
        self.traps()
        self.starts()

    def card(self):
        card = chapter_card(3, r"Fitting", r"Which parameters make the data most likely?", lit=(), part=PART,
                            scale=("person",), marr=("how",))
        with self.voiceover("Chapter three. Fitting."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ml(self):
        d = load("example")
        head = heading(r"Maximum likelihood, \ and a scorecard")
        eq = MathTex(r"\hat\theta = \arg\max_\theta \sum_t \log P(c_t \mid c_{<t}, r_{<t}, \theta)", font_size=38,
                     color=MODEL).move_to([0, 2.0, 0])
        models = ("random", "wsls", "q", "q_persev")
        names = (r"biased coin", r"win-stay lose-shift", r"Q-learner", r"Q + perseveration")
        A = axes([0.3, 4.7], [0, 300], x_length=5.4, y_length=2.8, xticks=None, yticks=[0, 100, 200, 300],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"BIC (lower is better)", center=[-3.4, -0.6, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3, 4], [d[f"{m}_bic"] for m in models], [GREY_B, SYMP, GOOD, PERSON], width=0.6)
        labs = VGroup(*[wrapped_label(t, 1.2, 11, GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1)
                        for i, t in enumerate(names)])
        rows = rows_of([
            (r"for each model, \ search for the parameters that make Psyche's 200 choices most likely", WHITE),
            (r"BIC adds a penalty of $k \log n$ for $k$ parameters: \ an extra parameter must earn its place", MODEL),
            (rf"the Q-learner wins ({d['q_bic']:.0f}); \ adding perseveration fits a little better but not enough "
             rf"({d['q_persev_bic']:.0f})", GOOD),
            (r"a win is relative: \ the best of four models may still be wrong", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.6, 0])
        tag = psyche_tag(r"\texttt{fit.fit}, \ four models, \ one simulated learner")
        with self.voiceover(
            "Fitting is a search. <bookmark mark='a'/> For each model, find the parameters that make Psyche's two "
            "hundred choices most likely. <bookmark mark='b'/> The Bayesian information criterion adds a penalty for "
            "every parameter, so an extra parameter must earn its place. <bookmark mark='c'/> The Q-learner wins. "
            "Adding perseveration fits a little better, but not enough to pay for itself. <bookmark mark='d'/> And a "
            "win is relative. The best of four models may still be wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(A), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def traps(self):
        head = heading(r"Traps in the search")
        data = (
            (r"local optima", r"the likelihood surface can have several peaks; \ start the search from several "
                              r"places, \ and keep the best", AUTH),
            (r"bounds", r"a learning rate must lie between 0 and 1; \ estimates that land on a bound are a warning",
             PERSON),
            (r"no likelihood", r"some models can only be simulated; \ then fit by comparing simulated and real "
                               r"summaries (approximate Bayesian computation), \ or train a network to invert the "
                               r"simulator", MODEL),
            (r"too few trials", r"a few dozen choices may barely constrain two parameters: \ the next two chapters",
             SYMP),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=17, width=3.0), wrapped_label(how, 9.2, 19, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Four traps in the search. <bookmark mark='a'/> Local optima: the likelihood surface can have several "
            "peaks, so start from several places and keep the best. <bookmark mark='b'/> Bounds: a learning rate "
            "must lie between zero and one, and an estimate that lands on a bound is a warning. "
            "<bookmark mark='c'/> No likelihood: some models can only be simulated. Then fit by comparing simulated "
            "and real summaries, or train a network to invert the simulator. <bookmark mark='d'/> And too few trials: "
            "a few dozen choices may barely constrain two parameters. That's the next two chapters."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def starts(self):
        d = load("starts")
        head = heading(r"Two answers from one learner")
        nll = np.sort(np.asarray(d["nll"]))
        A = axes([0, 41], [25, 31], x_length=5.6, y_length=3.0, xticks=[1, 10, 20, 30, 40], yticks=[26, 28, 30],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"random starting point (sorted)",
                 ylabel=r"final $-\log L$", center=[-3.3, 0.3, 0], font_size=12)
        dots = VGroup(*[Dot(A.ax.c2p(i + 1, v), radius=0.07, color=GOOD if v < d["best"] + 0.5 else AUTH)
                        for i, v in enumerate(nll)])
        b, o = np.asarray(d["best_params"]), np.asarray(d["other_params"])
        rows = rows_of([
            (r"a slow, \ decisive learner who tends to repeat choices; \ 80 trials; \ the three-parameter model fitted "
             r"from 40 random starting points", WHITE),
            (rf"{100 * d['share_best']:.0f}\% end at the best fit: \ learning rate {b[0]:.2f}, \ inverse temperature "
             rf"{b[1]:.0f}, \ perseveration {b[2]:.2f}", GOOD),
            (rf"the rest stop {d['other_nll'] - d['best']:.0f} log-likelihood units short, \ at a different story: \ "
             rf"learning rate {o[0]:.2f}, \ inverse temperature {o[1]:.0f}, \ perseveration {o[2]:.2f}", AUTH),
            (r"one start can land anywhere; \ use many, \ keep the best, \ and report how many agreed", YOU),
        ], 6.0, 18, 0.34).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.loglik}, \ L-BFGS-B from 40 starts")
        with self.voiceover(
            "Here's why restarts matter. <bookmark mark='a'/> Psyche makes a slow, decisive learner who tends to "
            "repeat choices, and fits the three-parameter model to eighty trials, from forty random starting points. "
            "<bookmark mark='b'/> Seven in ten end at the best fit: a very low learning rate and a high inverse "
            "temperature. <bookmark mark='c'/> The rest stop three log-likelihood units short, at a different story: a "
            "faster learner who chooses more randomly and perseverates more. <bookmark mark='d'/> One start can land "
            "anywhere. Use many, keep the best, and report how many agreed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.03), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
