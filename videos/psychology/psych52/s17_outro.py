from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403

PROBLEMS = [
    r"Predict with the keystroke-level model: \ \texttt{H M P B B H M K K K K} (K = 0.28 s).",
    r"Fitts's law $MT = 0.2 + 0.2\,ID$, \ $ID = \log_2(D/W + 1)$: \ a 20-pixel button 300 pixels away.",
    r"Endpoints with SD 6 pixels, \ distance 256, \ mean time 0.9 s: \ find $W_e$, \ $ID_e$ and the throughput.",
    r"Each problem is found by each user with $p = 0.2$: \ what share do 5 users find, \ and how many users for 90\%?",
    r"A patch gives $g(t) = 10(1 - e^{-t/30})$ facts; \ travel takes 20 s. \ Check that leaving at about 29 s "
    r"satisfies $g'(t) = g(t)/(t + 20)$.",
    r"Relative luminances 0.18 and 1.0: \ find the contrast ratio. \ Does it pass AA for normal text?",
    r"$\star$ \ Plan a test of a redesigned settings page: \ a keystroke-level comparison, \ a usability test, \ and an "
    r"experiment, \ with what each can and cannot tell you.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.your_numbers()
        self.recap()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def your_numbers(self):
        k, ds, c, h = load("klm"), load("discovery"), load("charts"), load("habit")
        head = heading(r"Your four numbers, \ checked")
        rows = VGroup()
        for n_, q, ans, col in (
                (r"1", r"the menu route against the shortcut", rf"{k['times'][2] / k['times'][0]:.0f} times as long",
                 PERSON),
                (r"2", r"problems found by five users", rf"{100 * ds['homog'][4]:.0f}\% if all alike; \ "
                                                         rf"{100 * ds['hetero'][4]:.0f}\% if not", AUTH),
                (r"3", r"angle error against length error", rf"about {c['mae'][2] / c['mae'][1]:.1f} times", MODEL),
                (r"4", r"days to a new habit", rf"median about {h['median']:.0f}; \ 18 to 254", GOOD)):
            rows.add(VGroup(label(n_, font_size=30, color=col), wrapped_label(q, 5.6, 22, WHITE),
                            label(ans, font_size=24, color=col)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.4, 0])
        foot = wrapped_label(r"where the psychology is quantitative, \ design can be predicted before it is built",
                             12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "First, your four numbers. <bookmark mark='a'/> The menu route to delete a word takes about three times as "
            "long as the shortcut. Five users find about eighty-four percent of the problems if every problem is "
            "equally findable, and about sixty percent if they differ. Angles are misjudged almost twice as much as "
            "lengths. And a new habit takes a median of about sixty-six days, with a range from eighteen to two "
            "hundred and fifty-four. <bookmark mark='b'/> Where the psychology is quantitative, design can be "
            "predicted before it's built."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def recap(self):
        items = [
            (r"the Model Human Processor: \ three processors, \ cycle times", WHITE),
            (r"the keystroke-level model: \ add the operators", SYMP),
            (r"overlapping operators: \ shorten the critical path", SYMP),
            (r"throughput from where the clicks land", MODEL),
            (r"steering is a ratio, \ not a logarithm", MODEL),
            (r"Hick's law needs a practised user", MODEL),
            (r"foragers leave a page by the marginal value theorem", PERSON),
            (r"two gulfs; \ affordances need signifiers", PERSON),
            (r"five users find less than promised", AUTH),
            (r"position beats length beats angle beats area", GOOD),
            (r"contrast and colour as psychophysics", GOOD),
            (r"habits take months; \ dark patterns turn biases against users", YOU),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=28, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        head = label(r"Part 52, \ in twelve lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part fifty-two in twelve lines. <bookmark mark='a'/> The Model Human Processor: three processors with "
            "cycle times. The keystroke-level model: add the operators. When operators overlap, shorten the critical "
            "path. Measure throughput from where the clicks land. Steering is a ratio, not a logarithm. Hick's law "
            "needs a practised user. Foragers leave a page by the marginal value theorem. There are two gulfs, and "
            "affordances need signifiers. Five users find less than promised. Position beats length beats angle beats "
            "area. Contrast and colour are psychophysics. And habits take months, while dark patterns turn our biases "
            "against us."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=34.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"selection, \ training and work design", [53]),
            (r"learning, \ practice and spacing in classrooms", [54]),
            (r"defaults and nudges at scale", [55]),
            (r"minds and machines", [60]),
        ], font_size=27)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Selection, training and the design of work are Part 53. "
            "Learning and practice in classrooms are Part 54. Defaults and nudges at scale are Part 55. And minds and "
            "machines return in Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One adds keystroke-level "
            "operators. One applies Fitts's law to a button. One computes throughput. One works the problem-discovery "
            "curve. One checks the marginal value theorem. One computes a contrast ratio. And the last, with the star, "
            "asks you to plan a test of a redesigned page by three methods. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. K. Card, \ T. P. Moran \& A. Newell, \ \emph{The Psychology of Human-Computer Interaction} (1983)",
             r"D. A. Norman, \ \emph{The Design of Everyday Things}",
             r"C. Ware, \ \emph{Information Visualization: \ Perception for Design}"],
            [r"W. D. Gray, \ B. E. John \& M. E. Atwood (1993); \ I. S. MacKenzie (1992)",
             r"J. Accot \& S. Zhai (1997); \ P. Pirolli \& S. Card (1999)",
             r"J. Nielsen \& T. K. Landauer (1993); \ L. Faulkner (2003)",
             r"W. S. Cleveland \& R. McGill (1984); \ J. Heer \& M. Bostock (2010)",
             r"P. Lally et al.\ (2010); \ A. Mathur et al.\ (2019)",
             r"B. Reeves \& C. Nass (1996)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Card, Moran and Newell's book "
            "founded the engineering models; Norman's is the classic on everyday design; and Ware's is the best on "
            "perception for visualization."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act XII: \ psychology at work, \ 2 of 7", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 53", font_size=32, color=GREY_B),
                     label(r"People at Work", font_size=36),
                     wrapped_label(r"can a test predict who will do a job well?", 6.0, 26, GREY_A))
        nxt.arrange(DOWN, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Two parts of Act Twelve are done. <bookmark mark='a'/> This one designed the interface around the "
            "person. <bookmark mark='b'/> The next turns to the people themselves: who to hire, how to train them, and "
            "what makes work go well. Can a test predict who will do a job well? Part 53: people at work."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
