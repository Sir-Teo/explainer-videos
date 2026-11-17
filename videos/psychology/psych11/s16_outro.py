from __future__ import annotations

from videos.psychology.psych11.common import *  # noqa: F403

PROBLEMS = [
    r"Weber's fraction for a task is 0.05. \ Starting at an absolute threshold of 1, \ how many just noticeable steps lie "
    r"between 1 and 1{,}000? \ Between 1{,}000 and 2{,}000? \ What does Fechner's law say about the sensation at 2{,}000 "
    r"compared with 1{,}000?",
    r"A two-interval observer's impression of each stimulus has a standard deviation of $\sigma$. \ Show that it is right "
    r"75\% of the time when the increment is $\sqrt2\,z_{0.75}\,\sigma \approx 0.95\,\sigma$. \ If $\sigma = 0.08\,I$, \ what "
    r"is Weber's fraction?",
    r"Derive where a 3-down 1-up staircase settles. \ Which rule would you use to measure the 84\% point? \ Why does a "
    r"large step size bias the estimate?",
    r"At one level, \ 30 of 40 trials are right. \ Write the binomial log-likelihood of a proportion $p$ and find its "
    r"maximum. \ Use $\sqrt{p(1-p)/n}$ to give an approximate 95\% interval.",
    r"Brightness has exponent 0.33 and loudness 0.67. \ By what factor must light increase to double brightness? \ In a "
    r"cross-modality match, \ by what factor must sound pressure rise when light rises tenfold?",
    r"With \texttt{explainer.psychology.psyche.psychophysics}: run \texttt{staircase} 200 times with step factors 1.1 and "
    r"1.5, \ and \texttt{quest} with 20 and 60 trials; \ compare each with the level it aims at.",
    r"$\star$ \ Psyche's two observers of chapter 10 have the same thresholds. \ Design a measurement other than a threshold "
    r"that would tell them apart, \ and say what each predicts.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def recap(self):
        w, f, fit, st, q, s = (load(k) for k in ("weber", "fechner", "fit", "stairs", "quest", "stevens"))
        items = [
            (r"Fechner's morning, 1850: \ measure the mind by counting just noticeable steps", FECHC),
            (rf"Weber: \ $\Delta I = k I$; \ on Psyche, \ $k = {w['w']:.3f}$ over the middle, \ larger near the floor", WEBERC),
            (rf"Fechner: \ count the steps and get a logarithm; \ {f['jnds_to_1000']:.0f} steps from 1 to 1{{,}}000", FECHC),
            (r"three methods: \ limits, \ adjustment, \ constant stimuli; \ yes-no mixes seeing with willingness", WHITE),
            (r"a threshold is a curve with four numbers: \ guess, \ threshold, \ spread, \ lapse", MODEL),
            (rf"fitted by maximum likelihood: \ ${fit['threshold']:.1f}$, \ between ${fit['ci'][0]:.1f}$ and "
             rf"${fit['ci'][1]:.1f}$; \ one slip without $\lambda$ moves it to ${fit['th_no_lapse']:.1f}$", MODEL),
            (r"a 2-down staircase settles at 70.7\%; \ QUEST keeps a belief and is fastest", THRESH),
            (r"Stevens: \ ask for numbers, \ get power laws, \ exponents 0.33 to 3.5, \ moved by the range", STEVC),
            (r"growing noise or a compressed code give the same thresholds; \ the slope says which noise rules", WEBERC),
            (rf"Weber's law for number ($k \approx {load('elsewhere')['w_adult']:.2f}$), \ for time, \ and Bernoulli's "
             rf"for money", GREY_A),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=32, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 11, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part eleven in ten lines. <bookmark mark='a'/> On a morning in 1850, Fechner saw how to "
            "measure the mind: by counting just noticeable steps. Weber had found that the step is a "
            "constant fraction of the stimulus, over the middle of each range, and larger near the floor. "
            "Count the steps, and sensation is a logarithm. Three classical methods find the steps, and a "
            "yes-or-no question mixes what you see with what you're willing to say. A threshold is a curve "
            "with four numbers: a guess rate, a threshold, a spread and a lapse rate. Maximum likelihood "
            "fits it, with an interval, and leaving out the lapse rate lets one slip move the answer. A "
            "two-down staircase settles at seventy point seven percent, and QUEST, which keeps a belief, "
            "is fastest. Stevens asked for numbers and got power laws, whose exponents the experiment "
            "itself moves. Growing noise and a compressed code give the same thresholds, and the slope of "
            "a threshold against its background says which noise is in charge. And a constant fraction "
            "holds for number, for time, and in Bernoulli's hands, for money."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=44.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a law of the mind with a constant in it, \ thresholds fitted with intervals, \ a staircase derived. \ Whether "
             r"a sensation has a size: \ still argued", STATUS_COLOR["replicated, smaller"]),
            (r"experiments by the dozen: \ assignment by lot, \ lesions, \ twins, \ a cave", STATUS_COLOR["replicated"]),
            (r"a forced choice: \ no yes to be cautious about, \ so the observer's habits drop out", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today was the first objection's day. Kant said the mind "
            "admits no mathematics. Fechner answered with a law that has a constant in it, and a century "
            "and a half of laboratories have found Weber's law where he said it would be. Thresholds come "
            "with intervals, and the staircase that finds them was derived on a single line. "
            "<bookmark mark='b'/> But the deepest part of the objection still stands: whether a "
            "sensation has a size, or only differences that can be told apart. So the reply is strong, "
            "not total. <bookmark mark='c'/> And on the third objection, that observing disturbs: the "
            "forced choice is a reply. With two intervals and no yes to be cautious about, the observer's "
            "habits drop out of the measurement."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[1].reply))
            vo.wait_until("a")
            self.play(FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(Indicate(board.rows[0].reply, color=WHITE, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(board.rows[2].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"seeing against saying: \ signal detection", [12]),
            (r"the eye's thresholds, \ and contrast", [13]),
            (r"prices, \ money and whether anyone notices", [26]),
            (r"number sense in children", [30]),
            (r"scaling people's judgments", [46]),
            (r"displays built for human thresholds", [51]),
            (r"why perception compresses: \ efficient coding", [58]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Seeing against saying, signal detection, is the "
            "very next part. The eye's thresholds and contrast are Part 13. Prices, and whether anyone "
            "notices a change, are in Part 26. Number "
            "sense in children is Part 30. Scaling people's judgments, Stevens's heirs, is Part 46. "
            "Displays built around human thresholds are Part 51. And why perception compresses at all, "
            "efficient coding, is Part 58."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One counts "
            "Fechner's steps. One derives Weber's fraction from noise. One derives a staircase's target. "
            "One fits a proportion by maximum likelihood, by hand. One does Stevens's arithmetic. One uses "
            "Psyche's psychophysics module to test staircases and QUEST. And the last, with the star, is "
            "the frontier's problem. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. T. Fechner, \emph{Elemente der Psychophysik} (1860)",
             r"G. A. Gescheider, \emph{Psychophysics: The Fundamentals} (3rd ed., 1997)",
             r"F. A. A. Kingdom \& N. Prins, \emph{Psychophysics: A Practical Introduction} (2nd ed., 2016)",
             r"S. S. Stevens, \emph{Psychophysics} (1975)"],
            [r"E. H. Weber (1834); \ E. G. Boring (1961)",
             r"S. S. Stevens (1957); \ E. C. Poulton (1968); \ R. Teghtsoonian (1971)",
             r"H. Levitt (1971); \ A. B. Watson \& D. G. Pelli (1983)",
             r"F. A. Wichmann \& N. J. Hill (2001); \ W. J. McGill \& J. P. Goldberg (1968)",
             r"J. Halberda, M. M. M. Mazzocco \& L. Feigenson (2008); \ J. Gibbon (1977)",
             r"L. A. Lesmes, Z.-L. Lu, J. Baek \& T. D. Albright (2010)",
             r"D. Bernoulli (1738); \ J. Plateau (1872); \ L. L. Thurstone (1927)",
             r"Hl. de Vries (1943); \ A. Rose (1948)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. For doing "
            "psychophysics yourself, Kingdom and Prins is the place to start."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act III begins: \ the senses", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 12", font_size=32, color=GREY_B), label(r"Signal and Noise", font_size=50),
                     wrapped_label(r"Radar operators in wartime miss real targets and report ghosts, \ and no instruction "
                                   r"fixes one error without causing the other.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So a sensation can be measured, at least at its edges, and a law of the mind has a constant "
            "in it. <bookmark mark='a'/> But chapter three left a problem unsolved. Ask someone whether "
            "they saw something, and the answer mixes two things: how well they can see, and how willing "
            "they are to say yes. <bookmark mark='b'/> In wartime, radar operators watching for aircraft "
            "missed real targets and reported ghosts, and no instruction could fix one kind of error "
            "without causing more of the other. Out of that trade-off came a theory with two numbers, "
            "one for seeing and one for saying, and it became the most exported idea in psychology. It's "
            "Part 12: signal and noise."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
