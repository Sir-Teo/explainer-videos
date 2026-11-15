from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403

PROBLEMS = [
    r"Show that with no drift the chance of the upper bound is $z/a$, \ and that the general formula tends to it as "
    r"$v \to 0$.",
    r"With the start halfway, \ show that the mean decision time is $\frac{a}{2v}\tanh\!\big(\frac{va}{2}\big)$ "
    r"\ (unit noise), \ and that it tends to $a^2/4$ as $v \to 0$.",
    r"In Wald's test of $p = 0.5$ against $p = 0.7$ with $\alpha = \beta = 0.05$, \ what is the smallest number of "
    r"shots that can end the test, \ each way?",
    r"With corrections that each leave a share $r$ of the distance, \ how many does a 5-bit movement need when "
    r"$r = 0.25$? \ When $r = 0.5$?",
    r"Show that the integration estimate of the stop time equals mean go time minus mean delay when half the "
    r"stop trials escape and the go distribution is symmetric.",
    r"With \texttt{explainer.psychology.opendata}: \ fit EZ diffusion to each of the 17 people's two kinds of "
    r"block. \ Does EZ also put the bound lower under speed?",
    r"$\star$ \ Design an experiment whose response times could tell a collapsing bound from variability in "
    r"drift, \ and say what each predicts.",
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
        items = [
            (r"moving dots: \ you chose your own exchange rate between speed and accuracy", SPEED),
            (r"Hick and Fitts: \ a constant cost per bit, \ for choosing and for moving", BOUND),
            (r"17 people, \ every one slower and almost every one more accurate when told to be careful", CAREFUL),
            (r"response times are skewed; \ the mean misleads, \ the quantiles do not", EVIDENCE),
            (r"Wald's test: \ add up evidence to a line; \ about half the shots of a fixed test", BOUND),
            (r"the diffusion model: \ drift, \ bound, \ start, \ $t_0$; \ accuracy and mean time in closed form", MODEL),
            (r"speed instructions lower the bound for 16 of 17, \ though not only the bound", BOUND),
            (r"fast and slow errors: \ variability in start and in drift", LOST),
            (r"LIP: \ a population that diffuses; \ single neurons that may step", DRIFT),
            (r"races, \ stopping and confidence: \ the same accumulator, \ read three ways", TIME),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 25, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-five in ten lines. <bookmark mark='a'/> With the moving dots, you chose your own rate of "
            "exchange between speed and accuracy. Hick's and Fitts's laws put a constant price on each bit, for "
            "choosing and for moving. Seventeen people were all slower, and nearly all more accurate, when told to "
            "be careful. Response times are skewed, so the mean misleads and the quantiles don't. Wald's test adds "
            "up evidence to a line, and needs about half the shots of a fixed test. The diffusion model has four "
            "main numbers, and gives accuracy and mean time in closed form. Telling people to hurry lowered the "
            "bound for sixteen of seventeen, though not only the bound. Fast and slow errors come from variability "
            "in where a trial starts and how strong its evidence is. In LIP, a population diffuses, while single "
            "neurons may step. And races, stopping and confidence are the same accumulator, read three ways."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"Wald's test, \ the diffusion model's closed forms and densities, \ fitted to two open datasets",
             STATUS_COLOR["replicated"]),
            (r"instructions changed, \ stimuli held fixed: \ an experiment on a single parameter, \ caution",
             STATUS_COLOR["replicated"]),
            (r"no introspection needed: \ choices and times, \ and neurons recorded while a decision forms",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "Wald's test and the diffusion model, derived, computed and fitted to two sets of open data. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met an experiment that changes "
            "only an instruction and finds a single parameter, caution, moving in sixteen of seventeen people. "
            "<bookmark mark='c'/> And the third, that looking inward disturbs what you look at, met a part that never "
            "asked anyone to look inward: choices and times, and neurons recorded while a decision forms."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"judgement and choice: \ values, \ risk and framing", [26]),
            (r"consciousness: \ is the readiness potential an accumulator?", [27]),
            (r"modelling behaviour: \ fitting diffusion and race models properly", [48]),
            (r"designing for minds: \ Fitts and Hick at the interface", [52]),
            (r"individual differences: \ are decision parameters traits?", [59]),
            (r"minds and machines: \ when should a machine stop thinking?", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Choices between values, risks and frames are the next part. "
            "Whether the brain's readiness to move is just an accumulator is Part 27, on consciousness. Fitting these "
            "models properly is Part 48. Fitts and Hick at the interface are Part 52. Whether decision parameters are "
            "traits is Part 59. And when a machine should stop thinking is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=11.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> Two derive the "
            "diffusion model's limits and its mean time with an unbiased start. One finds the shortest possible run "
            "of Wald's test. One counts corrections in an aimed movement. One connects two ways of estimating the "
            "stop time. One fits EZ diffusion to the seventeen people's open data. And the last, with the star, asks "
            "you to design an experiment that tells a collapsing bound from variable evidence. Pause here if you'd "
            "like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. D. Luce, \emph{Response Times} (1986)",
             r"A. Wald, \emph{Sequential Analysis} (1947)",
             r"B. U. Forstmann, R. Ratcliff \& E.-J. Wagenmakers, \emph{Sequential sampling models in cognitive "
             r"neuroscience}, \ Annual Review of Psychology (2016)"],
            [r"W. E. Hick (1952); \ R. Hyman (1953); \ P. M. Fitts (1954); \ E. R. F. W. Crossman \& P. J. Goodeve (1963)",
             r"A. Wald (1945); \ A. Wald \& J. Wolfowitz (1948); \ M. Stone (1960); \ D. R. J. Laming (1968)",
             r"R. Ratcliff (1978, \ 1979); \ R. Ratcliff \& J. N. Rouder (1998); \ R. Ratcliff \& G. McKoon (2008)",
             r"E.-J. Wagenmakers et al.\ (2008); \ A. Voss et al.\ (2004); \ G. Dutilh et al.\ (2019)",
             r"J. D. Roitman \& M. N. Shadlen (2002); \ K. W. Latimer et al.\ (2015); \ N. A. Steinemann et al.\ (2024)",
             r"S. D. Brown \& A. Heathcote (2008); \ M. Usher \& J. L. McClelland (2001); \ R. Bogacz et al.\ (2006)",
             r"G. D. Logan \& W. B. Cowan (1984); \ F. Verbruggen et al.\ (2019); \ P. G. Bissett et al.\ (2021)",
             r"D. Vickers (1979); \ R. Kiani \& M. N. Shadlen (2009); \ I. Krajbich et al.\ (2010)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Duncan Luce's Response Times "
            "is still the deepest single book on the subject, and Forstmann, Ratcliff and Wagenmakers's review is the "
            "best short way into sequential sampling models today."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 26", font_size=32, color=GREY_B), label(r"Judgment and Choice", font_size=40),
                     wrapped_label(r"Six hundred lives, \ two programmes, \ two descriptions of the same outcome, "
                                   r"\ and opposite choices.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Today the mind decided against the clock. <bookmark mark='a'/> Next time, it chooses between values. "
            "<bookmark mark='b'/> In 1981 Amos Tversky and Daniel Kahneman described a disease expected to kill six "
            "hundred people, and two programmes to fight it. Described in lives saved, most people chose the safe "
            "programme. Described in lives lost, most chose the gamble, though the outcomes were identical. Why? "
            "It's Part 26: judgment and choice."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
