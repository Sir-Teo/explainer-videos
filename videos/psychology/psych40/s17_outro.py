from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403

PROBLEMS = [
    r"A Rescorla-Wagner learner has fear $V = 0.9$ and avoids on every trial with probability "
    r"$0.95\,\sigma(10(V - 0.3))$. \ With extinction rate $0.08$, \ how many full exposures does it take to bring $V$ "
    r"below 0.3, \ and roughly how many trials will that take?",
    r"In the renewal model, \ excitation $E$ is expressed everywhere and inhibition $I$ only in context B. \ Write "
    r"the fear in A, \ B and C after extinction, \ and suggest one way to make extinction generalize.",
    r"A learner starts with a Beta(1, 1) belief about control. \ After 10 tries that all fail, \ what is its "
    r"probability of trying? \ After 10 that all succeed?",
    r"Happiness $H_t = w_0 + w_3 \sum_j \gamma^{t-j} \delta_j$. \ If every prediction error is 0.5 for ten trials, \ "
    r"find $H_{10}$ for $\gamma = 0.7$, \ $w_0 = 0.5$, \ $w_3 = 0.6$.",
    r"A drug and a placebo improve depression by 9.6 and 7.8 points, \ with SD 8 in both groups. \ What is the "
    r"standardized effect size, \ and how many people need to be treated for one extra response if response rates "
    r"are 50\% and 40\%?",
    r"A risk factor has sensitivity 0.8 and specificity 0.8 for suicide death within a year, \ where the base rate "
    r"is 1 in 2{,}000. \ What share of people it flags will die by suicide in that year?",
    r"$\star$ \ Design a study that could tell whether a person's anhedonia is a problem of liking, \ of learning "
    r"or of effort.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n, q, ans, c in (
                (r"1", r"trials in the network meta-analysis", r"522", PERSON),
                (r"2", r"drug against placebo, \ 52-point scale", r"about 1.8", MODEL),
                (r"3", r"the gene-by-stress finding in 38{,}000 people", r"no", SYMP),
                (r"4", r"predicting suicidal behaviour from risk factors", r"slightly above chance", GOOD)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 6.8, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"the learning models hold; \ the simple chemical and genetic stories did not", 12.0, 22,
                             YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> Trials in the network meta-analysis: five hundred and "
            "twenty-two. Drug against placebo on the fifty-two-point scale: about one point eight. The gene-by-stress "
            "finding in thirty-eight thousand people: it didn't hold. And predicting suicidal behaviour from risk "
            "factors: only slightly better than chance. <bookmark mark='b'/> The learning models hold. The simple "
            "chemical and genetic stories didn't."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"control protects; \ the explanation of helplessness was reversed", PERSON),
            (r"avoidance keeps fear alive by preventing the test", AUTH),
            (r"exposure works; \ extinction is new, \ context-bound learning, \ so fear can return", GOOD),
            (r"anxiety disorders differ in what is feared and share what maintains it", SYMP),
            (r"attention to threat is a group effect, \ not a measure or a treatment", MODEL),
            (r"depression: \ negative thinking, \ lost control, \ blunted reward", PERSON),
            (r"momentary mood tracks recent reward prediction errors", MODEL),
            (r"the serotonin-deficit story failed as stated", AUTH),
            (r"antidepressants beat placebo, \ modestly, \ on average", GOOD),
            (r"stress matters; \ the celebrated gene did not", SYMP),
            (r"suicide cannot be predicted well for individuals; \ care must not wait on prediction", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 40, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part forty in eleven lines. <bookmark mark='a'/> Control protects, and the explanation of helplessness "
            "was reversed. Avoidance keeps fear alive by preventing the test. Exposure works, and because extinction "
            "is new, context-bound learning, fear can return. Anxiety disorders differ in what is feared and share "
            "what maintains it. Attention to threat is a group effect, not a measure or a treatment. Depression "
            "brings negative thinking, lost control and blunted reward. Momentary mood tracks recent reward "
            "prediction errors. The serotonin-deficit story failed as stated. Antidepressants beat placebo, "
            "modestly, on average. Stress matters, and the celebrated gene didn't. And suicide can't be predicted "
            "well for individuals, so care must not wait on prediction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"Rescorla-Wagner avoidance, \ context-bound extinction, \ a belief about control and a model of mood",
             STATUS_COLOR["replicated"]),
            (r"exposure trials, \ shuttle boxes and 522 drug trials", STATUS_COLOR["replicated"]),
            (r"mood rated moment by moment is fitted by a model, \ though the ratings remain reports",
             STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "Rescorla-Wagner avoidance, context-bound extinction, a belief about control, and a model of mood. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met exposure trials, shuttle "
            "boxes and five hundred and twenty-two drug trials. <bookmark mark='c'/> And the third, about "
            "introspection: mood rated moment by moment is fitted by a model, though the ratings remain reports. "
            "Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"psychosis, \ addiction and development", [41]),
            (r"does therapy work, \ and which?", [42]),
            (r"people over time: \ symptoms tracked day by day", [47]),
            (r"computational psychiatry", [59]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Psychosis, addiction and development are next, in Part 41. "
            "Whether therapy works, and which, is Part 42. Symptoms tracked day by day are Part 47, and "
            "computational psychiatry Part 59."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One counts the "
            "exposures avoidance allows. One writes the renewal model. One updates a belief about control. One "
            "computes a mood. One turns a drug-placebo gap into an effect size and a number needed to treat. One "
            "works the base rate for a suicide risk factor. And the last, with the star, asks you to design a study "
            "that could tell liking, learning and effort apart. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"D. H. Barlow, \ V. M. Durand \& S. G. Hofmann, \ \emph{Abnormal Psychology} (textbook)",
             r"A. T. Beck, \ \emph{Depression: Clinical, Experimental and Theoretical Aspects} (1967)",
             r"G. W. Brown \& T. Harris, \ \emph{Social Origins of Depression} (1978)"],
            [r"M. E. P. Seligman \& S. F. Maier (1967); \ S. F. Maier \& M. E. P. Seligman (2016)",
             r"O. H. Mowrer (1947); \ M. E. Bouton (2002); \ M. G. Craske et al.\ (2014); \ D. M. Clark (1986)",
             r"I. A. Cristea, \ R. N. Kok \& P. Cuijpers (2015); \ R. B. Rutledge et al.\ (2014)",
             r"J. Moncrieff et al.\ (2022); \ I. Kirsch et al.\ (2008); \ A. Cipriani et al.\ (2018)",
             r"A. Caspi et al.\ (2003); \ R. C. Culverhouse et al.\ (2018); \ R. Border et al.\ (2019)",
             r"J. F. J. Cade (1949); \ J. C. Franklin et al.\ (2017)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Barlow, Durand and Hofmann's "
            "textbook covers the disorders; Beck's book is the founding statement of cognitive therapy; and Brown "
            "and Harris's Social Origins of Depression is still the model of how to study life events."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act X: \ when minds suffer", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 41", font_size=32, color=GREY_B),
                     label(r"Psychosis, \ Addiction and Development", font_size=36),
                     wrapped_label(r"What happens when perception, \ reward and development go wrong?", 6.0, 26,
                                   GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Act Ten continues. <bookmark mark='a'/> This part built fear and sadness from learning, reward and "
            "control. <bookmark mark='b'/> The next takes the same models further: psychosis as inference gone wrong, "
            "addiction as reward learning gone wrong, and the conditions of development. Part 41: psychosis, "
            "addiction and development."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
