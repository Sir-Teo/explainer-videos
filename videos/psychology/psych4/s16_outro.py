from __future__ import annotations

from videos.psychology.psych4.common import *  # noqa: F403

PROBLEMS = [
    r"Two groups differ by $d = 0.3$. \ What share of the two distributions overlaps, and how often does a "
    r"randomly chosen member of the higher group beat one of the lower? \ About how many people per group give "
    r"an 80\% chance of detecting it?",
    r"For each sentence say whether it follows from $p = .03$, and why. \ (a) ``There is a 3\% chance the result "
    r"is a fluke.'' \ (b) ``If nothing were going on, data this extreme would turn up 3\% of the time.'' \ "
    r"(c) ``A repeat has a 97\% chance of succeeding.''",
    r"Of 1,000 hypotheses, a share $\pi$ are true; studies have power $1 - \beta$ and use $\alpha = .05$. \ Show "
    r"that the share of significant findings that are true is $\pi(1-\beta) / [\pi(1-\beta) + (1-\pi)\alpha]$. \ "
    r"Evaluate it for $\pi = 0.1$ with power 0.35, and with power 0.8.",
    r"An analyst has four independent yes-or-no choices, and each of the 16 analyses has a 5\% false-positive "
    r"rate. \ Give an upper bound for the chance that at least one is significant. \ Why was the figure in "
    r"chapter 4 far below it?",
    r"A study with 20 people a group reports $d = 0.70$, $p = .03$, and only significant studies are printed. \ "
    r"What is the smallest effect such a study could have printed? \ What does that say about the true effect?",
    r"With \texttt{explainer.psychology.evidence}: build a literature of 1,000 laboratories on a true effect of "
    r"0.2 with 30 people a group, publish the significant ones, and replicate each with 90\% power for the effect it printed. \ Report "
    r"the replication rate. \ Then explain it to someone who concludes that most of the findings were false.",
    r"$\star$ \ Design a study that could show whether registered reports produce truer findings, and not merely "
    r"fewer positive ones. \ State what ``truer'' means and what would be compared.",
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
        b, o, f, s = archive.BEM_2011.data, archive.OSC_2015.data, load("forking"), load("stopping")
        items = [
            (rf"2011: \ {b['experiments']} experiments, run by the book, show people feeling the future", KANT),
            (r"an effect size says how big; \ ``significant'' does not", SIZE["0.5"]),
            (r"a p-value: \ how rare the data would be if nothing were going on", NULLC),
            (r"small studies miss real effects, and overstate the ones they catch", SIZE["0.2"]),
            (rf"four defensible choices: \ nothing becomes ``something'' {pct(f['rates']['any'])} of the time", SIG),
            (r"print only the successes, and a literature of nothing reports a medium effect", ORIG),
            (rf"look ten times and stop when it works: \ {pct(s['rate_10'])}; \ honesty is not the remedy", BAD),
            (r"Meehl: \ rejecting ``no effect'' is a weak test of a theory", "#B48EF0"),
            (rf"{o['studies']} studies run again: \ {pct(o['original_significant'])} $\rightarrow$ "
             rf"{pct(o['replication_significant'])} significant, at half the size", REP),
            (r"the repairs are procedures: \ decide first, publish regardless, repeat", TRUTH),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=32, color=c) for i, (t, c) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 4, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part four in ten lines. <bookmark mark='a'/> In 2011, nine experiments run by the book showed "
            "people feeling the future. An effect size tells you how big a difference is; significance "
            "doesn't. A p-value says how rare the data would be if nothing were going on, and nothing more. "
            "Small studies miss real effects, and overstate the ones they catch. Four defensible choices turn "
            f"nothing into something {100 * f['rates']['any']:.0f} per cent of the time. Print only the successes, and a "
            "literature about nothing reports a medium effect. Look ten times and stop when it works, and one "
            "study in five succeeds; and since none of that feels like cheating, honesty isn't the remedy. "
            "Meehl: rejecting no effect is a weak test of a theory. A hundred studies run again went from "
            f"{100 * o['original_significant']:.0f} per cent significant to "
            f"{100 * o['replication_significant']:.0f}, at half the size. And the repairs are procedures: "
            "decide first, publish regardless, repeat."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.9), run_time=44.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"numbers with a stated scale, a stated error, and an argument for what they measure",
             STATUS_COLOR["replicated"]),
            (r"minds can be compared fairly: \ a control, a shuffle, a balanced order", STATUS_COLOR["replicated"]),
            (r"blinds for the experimenter; \ for the analyst, a plan fixed before the data and a second "
             r"laboratory", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager, at the end of the first act. <bookmark mark='a'/> No mathematics: answered in Parts "
            "1 and 3, with a corner still his. <bookmark mark='b'/> No experiments: answered in Part 2. "
            "<bookmark mark='c'/> And the third, the observer who disturbs what's observed. Part 2 dealt with "
            "the experimenter in the room. Part 3 dealt with people observing themselves. Today was the last "
            "observer, the one Kant never imagined: the scientist at the desk, looking at the data and hoping. "
            "The reply is the same kind of thing as the blind. Tie the analyst's hands before the data arrive, "
            "and let a second laboratory check. So the first act closes with a method that knows how it "
            "fails. Nothing in the next fifty-eight parts is exempt from it. That's what the Ledger is for."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows])
            for mark, r in zip("abc", board.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"every later part closes with its Ledger rows", [5, 62]),
            (r"the classic social experiments, re-examined", [34]),
            (r"social priming, and what is left of it", [35]),
            (r"you run a replication, preregistered, on screen", [43]),
            (r"Bayes factors and the comparison of models", [48]),
            (r"meta-science: \ p-curves, corrections for bias", [50]),
            (r"nudges at scale, and the winner's curse again", [55]),
        ], font_size=30)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Everywhere, in one sense: every part from here ends "
            "with its Ledger rows. The classic social experiments are re-examined in Part 34, and social priming "
            "gets its reckoning in Part 35. In Part 43 you run a replication yourself, preregistered, on "
            "screen. Bayes factors are built properly in Part 48. The p-curve and the corrections for bias are "
            "Part 50. And the winner's curse returns in Part 55, when nudges are tested at scale."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.4), run_time=9.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=24)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One turns an "
            "effect size into a picture. One sorts true sentences about a p-value from false ones. One derives "
            "the share of significant findings that are true. One bounds what four choices can do, and asks "
            "why the real figure is lower. One reads a small published study the way chapter five taught. One "
            "uses the false-positive lab to build a literature and replicate it. And the last, with the star, "
            "is the research problem from the frontier. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=6.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"C. Chambers, \emph{The Seven Deadly Sins of Psychology} (2017)",
             r"S. Ritchie, \emph{Science Fictions} (2020)",
             r"J. Cohen, \emph{Statistical Power Analysis for the Behavioral Sciences} (2nd ed., 1988)"],
            [r"D. J. Bem (2011); \ S. J. Ritchie, R. Wiseman \& C. C. French (2012); \ J. Galak et al.\ (2012)",
             r"J. Cohen (1962); \ P. Sedlmeier \& G. Gigerenzer (1989); \ R. Rosenthal (1979); \ P. E. Meehl "
             r"(1967, 1978)",
             r"J. P. Simmons, L. D. Nelson \& U. Simonsohn (2011); \ N. L. Kerr (1998); \ A. Gelman \& E. Loken "
             r"(2013)",
             r"Open Science Collaboration (2015); \ D. T. Gilbert et al.\ (2016); \ C. J. Anderson et al.\ (2016)",
             r"R. A. Klein et al.\ (2014, 2018); \ C. F. Camerer et al.\ (2018); \ A. Dreber et al.\ (2015); \ "
             r"A. M. Scheel, M. Schijen \& D. Lakens (2021)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. If you read one, read "
            "Simmons, Nelson and Simonsohn. It's short, it's funny, and it changed how a science works."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=1, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act I complete: \ the method, and its limits", font_size=26, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        nxt = VGroup(label(r"Act II \ $\cdot$ \ Part 5", font_size=32, color=GREY_B),
                     label(r"The Neuron", font_size=54),
                     wrapped_label(r"A frog's leg twitches when two metals touch it. \ What moves along a nerve, "
                                   r"and what is the smallest part of a mind?", 6.0, 28, GREY_A)).arrange(
            DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That's the end of the first act. <bookmark mark='a'/> We have a way of asking a mind a question: "
            "an experiment, a measurement, and a standard of evidence that knows its own weaknesses. What we "
            "don't yet have is a mind to ask. So far Psyche is a stopwatch and a spotlight. "
            "<bookmark mark='b'/> The second act opens her up. In the seventeen-eighties Luigi Galvani watched "
            "a dead frog's leg kick when it was touched with two metals. Helmholtz, whom you met in Part 1, "
            "timed whatever it was that ran along the nerve. And a century after him, two physiologists with "
            "the giant nerve fibre of a squid wrote four equations that reproduce that signal to the "
            "millisecond. It's the best model psychology has of anything, and it's where the machine begins. "
            "Part 5: the neuron."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
