from __future__ import annotations

from videos.psychology.psych37.common import *  # noqa: F403

PROBLEMS = [
    r"A responder has Fehr-Schmidt utility with $\alpha$ for disadvantageous inequity. \ Show that an offer $s$ of a "
    r"pie of 1 is accepted iff $s \ge \alpha / (1 + 2\alpha)$, \ and find the threshold for $\alpha = 0.5$ and $2$.",
    r"Responders' thresholds are uniform on $[0, 0.4]$. \ Find the offer that maximizes a selfish proposer's "
    r"expected share $(1 - s) P(\text{accept})$.",
    r"In a one-shot prisoner's dilemma with payoffs $T > R > P > S$, \ show that defecting is dominant. \ In the "
    r"repeated game with continuation probability $\delta$, \ find the $\delta$ above which Grim Trigger against itself "
    r"is a best response.",
    r"Hamilton's rule: \ helping a full sibling costs you $C$ and gives them $B$. \ For which $B/C$ is helping "
    r"favoured, \ and for a first cousin?",
    r"A classifier is fitted to $n$ couples with $p$ predictors and an intercept by least squares. \ Show that if "
    r"$p + 1 \ge n$ the fit can reproduce any outcome exactly, \ and explain what this means for in-sample accuracy.",
    r"An odds ratio of 1.5 for survival: \ if 80\% survive in the reference group, \ what share survive in the other?",
    r"$\star$ \ Design a study that could detect compatibility specific to a pair, \ and say what it would have to "
    r"predict that actor and partner effects cannot.",
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
        d = load("divorce")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n, q, ans, c in (
                (r"1", r"lowest average offer in fifteen societies", r"26\%", CROWD),
                (r"2", r"desire for a particular partner predicted from 100+ traits", r"none of it", PERSON),
                (r"3", r"odds of survival with stronger relationships", r"1.5 times", GOOD),
                (r"4", r"a divorce model's accuracy on new couples, \ in Psyche", pct(d["mean_loo"]), AUTH)):
            rows.add(VGroup(label(n, font_size=30, color=c), wrapped_label(q, 6.8, 23, WHITE),
                            label(ans, font_size=28, color=c)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"bargains are predictable in the aggregate; \ particular bonds are not", 12.0, 22,
                             YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> The lowest average offer in fifteen societies: twenty-"
            "six percent. Desire for a particular partner, predicted from over a hundred traits: none of it. The "
            "odds of survival with stronger relationships: one and a half times. And a divorce model's accuracy on "
            f"new couples, in Psyche: {spct(d['mean_loo'])}, worse than guessing. <bookmark mark='b'/> Bargains "
            "are predictable in the aggregate. Particular bonds are not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.8), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"proposers offer about 40\%, \ and low offers are rejected at a cost", PERSON),
            (r"five games: \ people are neither selfish nor saints", CROWD),
            (r"kin, \ reciprocity, \ reputation and punishment make cooperation pay", GOOD),
            (r"which strategy wins a tournament depends on the field and on noise", MODEL),
            (r"public goods decay; \ punishment holds them up, \ unless it targets cooperators", AUTH),
            (r"inequity aversion turns fairness into a utility function", MODEL),
            (r"offers ranged from 26\% to 58\% across fifteen societies", CROWD),
            (r"proximity and exposure make liking", GOOD),
            (r"stated preferences do not predict desire in person; \ pair chemistry is unpredicted", PERSON),
            (r"in-sample accuracy is not prediction: \ cross-validate", AUTH),
            (r"relationships and survival are linked; \ the cause is open", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 37, \ in eleven lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part thirty-seven in eleven lines. <bookmark mark='a'/> Proposers offer about forty percent, and low "
            "offers are rejected at a cost. Across five games, people are neither selfish nor saints. Kin, "
            "reciprocity, reputation and punishment make cooperation pay. Which strategy wins a tournament depends "
            "on the field, and on noise. Public goods decay, and punishment holds them up, unless it targets "
            "cooperators. Inequity aversion turns fairness into a utility function. Offers ranged from twenty-six "
            "to fifty-eight percent across fifteen societies. Proximity and exposure make liking. Stated "
            "preferences don't predict desire in person, and the chemistry of a pair goes unpredicted. In-sample "
            "accuracy isn't prediction, so cross-validate. And relationships and survival are linked, while the "
            "cause is still open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=40.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"utility functions for fairness, \ a tournament, \ Hamilton's rule and cross-validation",
             STATUS_COLOR["replicated"]),
            (r"games with real money, \ played on every continent", STATUS_COLOR["replicated"]),
            (r"people's accounts of what they want in a partner do not predict whom they want", STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "utility functions for fairness, a tournament, Hamilton's rule and cross-validation. "
            "<bookmark mark='b'/> The second, that the mind can't be experimented on, met games with real money, "
            "played on every continent. <bookmark mark='c'/> And the third, about introspection: people's accounts "
            "of what they want in a partner don't predict whom they want. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"culture, \ morals and which findings travel", [38]),
            (r"does therapy work, \ couple therapy included?", [42]),
            (r"incentives and teams at work", [53]),
            (r"games played with machines", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Culture, morals and which findings travel are next, in Part "
            "38. The evidence for therapies, couple therapy included, is in Part 42. Incentives and teams at work "
            "are Part 53, and games played with machines Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=7.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One derives the "
            "responder's threshold. One finds the proposer's best offer. One proves defection dominant, and finds "
            "when Grim Trigger holds. One applies Hamilton's rule. One shows why a model can fit any couples "
            "exactly. One converts an odds ratio. And the last, with the star, asks you to design a study that "
            "could find compatibility specific to a pair. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. F. Camerer, \emph{Behavioral Game Theory} (2003)",
             r"R. Axelrod, \emph{The Evolution of Cooperation} (1984)",
             r"E. J. Finkel et al., \ Online dating: \ a critical analysis, \ \emph{Psychological Science in the "
             r"Public Interest} (2012)"],
            [r"W. G\"uth, \ R. Schmittberger \& B. Schwarze (1982); \ H. Oosterbeek et al.\ (2004)",
             r"E. Fehr \& S. G\"achter (2002); \ B. Herrmann, \ C. Th\"oni \& S. G\"achter (2008)",
             r"E. Fehr \& K. M. Schmidt (1999); \ J. Henrich et al.\ (2001); \ J. Dana, \ D. M. Cain \& R. M. Dawes "
             r"(2006)",
             r"L. Festinger, \ S. Schachter \& K. Back (1950); \ R. B. Zajonc (1968); \ R. F. Bornstein (1989); \ S. M. Kalick \& T. E. Hamilton (1986)",
             r"P. W. Eastwick \& E. J. Finkel (2008); \ S. Joel, \ P. W. Eastwick \& E. J. Finkel (2017); \ S. Joel et "
             r"al.\ (2020)",
             r"R. E. Heyman \& A. M. Smith Slep (2001); \ C. Hazan \& P. Shaver (1987)",
             r"D. M. Buss (1989); \ K. V. Walter et al.\ (2020); \ J. Holt-Lunstad et al.\ (2010, \ 2015)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Camerer's Behavioral Game "
            "Theory is the field's handbook; Axelrod's book is the tournament and what he made of it; and Finkel "
            "and colleagues' review of online dating weighs the matching algorithms against the evidence."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act IX: \ other people", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 38", font_size=32, color=GREY_B), label(r"Culture and Morals", font_size=40),
                     wrapped_label(r"How much of psychology is the psychology of one kind of society?", 6.0, 26,
                                   GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Act Nine has one part left. <bookmark mark='a'/> This part found that fairness itself varies with the "
            "society people live in. <bookmark mark='b'/> The next asks how far that goes: how much of psychology "
            "is the psychology of one kind of society, and where morals come from. Part 38: culture and morals."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
