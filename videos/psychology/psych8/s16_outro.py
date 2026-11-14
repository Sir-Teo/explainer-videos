from __future__ import annotations

from videos.psychology.psych8.common import *  # noqa: F403

PROBLEMS = [
    r"A cell fires 40 impulses a second to its preferred orientation and 2 with no stimulus; its tuning is a bell "
    r"curve with standard deviation $20^{\circ}$. \ What is its rate to a line $30^{\circ}$ off? \ If counts are "
    r"Poisson, how many half-second showings tell that rate from the peak rate with a $z$ of 3?",
    r"$N$ unit dipoles point in random directions in a plane. \ Show that the mean square of their sum is $N$. \ "
    r"A patch of cortex has $10^{6}$ aligned cells, and a hundred times as many unaligned ones around it. \ "
    r"Which contributes more to the scalp?",
    r"A response of 5 microvolts sits in noise of 20. \ How many trials bring the noise in the average down to 1 "
    r"microvolt? \ How many are needed to tell two conditions apart, if the test needs the difference to be 4 "
    r"times its standard error?",
    r"The response to one brief event is $h(t)$. \ Write the predicted signal for events at times $t_1, \dots, "
    r"t_k$, and show that a block of events 2 s apart for 20 s gives a plateau. \ Why does the plateau start "
    r"about 5 s late?",
    r"A map has 100{,}000 voxels and nothing is there. \ How many pass at $p < 0.001$? \ What threshold does "
    r"Bonferroni give for a 5\% chance of any? \ Why is that too strict when neighbouring voxels are alike?",
    r"With \texttt{explainer.psychology.psyche.imaging}: run \texttt{voodoo} for 10, 16 and 40 subjects at the "
    r"threshold that gives $p < 0.001$ for each. \ How does the reported correlation depend on the sample? \ "
    r"Then use \texttt{reverse\_inference} to find how selective a region must be to take a prior of 0.1 above 0.5.",
    r"$\star$ \ Design the study that could show a brain measure predicts something about one person that their "
    r"behaviour and their history do not, and say what would count as failure.",
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
        e, b, d, v, c, r, p = (load(k) for k in ("erp", "bold", "tests", "voodoo", "ceiling", "reverse", "power"))
        items = [
            (r"the salmon: \ enough tests on noise always find something", DATA),
            (r"one neuron has a tuning curve: \ the real signal, through a keyhole", SPIKE),
            (r"the scalp hears only cells that are aligned and in step; \ \emph{when}, not \emph{where}", EEGC),
            (rf"averaging: \ noise falls as $1/\sqrt{{n}}$; \ {e['trials_for_1uv']} trials turn 20 microvolts into 1",
             EEGC),
            (rf"fMRI measures blood: \ an echo that peaks {b['peak_s']:.0f} s late; \ \emph{{where}}, not "
             r"\emph{when}", BLOOD),
            (r"a map is a regression in every voxel, \ of a difference between two tasks", MODEL),
            (rf"uncorrected, {pct(d['rate_uncorrected'])} of empty slices show activity; \ every correction "
             r"costs misses", THRESH),
            (rf"voxels chosen by the answer: \ $r = {r2(v['r_same'])}$ from noise, \ above the ceiling of "
             rf"{r2(c['ceiling'])}", BAD),
            (rf"reading backwards is Bayes' rule: \ 0.5 becomes {archive.POLDRACK_2006.data['posterior']:.2f}, \ and "
             r"to know a region is needed you must intervene", THRESH),
            (rf"links between brains and behaviour are small: \ {fmt_int(round(p['small_need'], -2))} people "
             rf"for $r = {p['small_r']:.2f}$", GREY_A),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=32, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 8, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part eight in ten lines. <bookmark mark='a'/> The salmon showed that enough tests on noise "
            "always find something. One neuron has a tuning curve, and it's the real signal, seen through "
            "a keyhole. The scalp hears only cells that are aligned and in step, which gives you when and "
            "not where. Averaging pulls a signal out of noise at the rate of the square root of the number "
            "of trials. Functional MRI measures blood, an echo that peaks five seconds late, which gives "
            "you where and not when. A map is a regression in every voxel, of a difference between two "
            "tasks. Without correction, most empty brains show activity, and every correction costs "
            "misses. Choose voxels by the answer, and you get a strong correlation from nothing, above "
            "the ceiling the measures allow. Reading a map backwards is Bayes' rule, and to know a region "
            "is needed you have to intervene. And the links between brains and behaviour are small, so "
            "finding them takes thousands of people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"equations that predict what they were not fitted to. \ And today, numbers read off a scalp that "
             r"follow meaning as it happens", STATUS_COLOR["replicated"]),
            (r"the mind does come apart, \ though not at will: \ damage is not assigned at random",
             STATUS_COLOR["replicated"]),
            (r"an instrument that records without asking. \ But the analyst still chooses: \ a hundred thousand "
             r"tests are a hundred thousand forking paths", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today touches the first objection and the third. On the "
            "first, that the mind admits no mathematics: the N400 is a number, read off a scalp, that "
            "tracks understanding four tenths of a second after a word. That isn't yet an equation that "
            "predicts, but it's a quantity where Kant said there could be none. <bookmark mark='b'/> On "
            "the third, that observing a mind disturbs it: here, for once, is an instrument that doesn't "
            "ask the person anything. It records while they read. But the disturbance moves. It's no "
            "longer in the subject. It's in the analyst, who has a hundred thousand tests to choose "
            "among, and Part 4 said what happens then. The remedy is Part 4's as well: decide the analysis "
            "first, correct for the tests, and check on fresh data."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows], FadeIn(board.rows[1].reply))
            vo.wait_until("a")
            self.play(FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(board.rows[2].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"what the brain's rhythms do in sleep", [10]),
            (r"tuning curves and receptive fields, in the eye", [13]),
            (r"a face area, and what it is for", [14]),
            (r"attention, measured on the scalp", [18]),
            (r"the N400 and how sentences are understood", [23]),
            (r"evidence building up in the brain before a choice", [25]),
            (r"what a scan can say about awareness", [27]),
            (r"why findings fail to repeat", [43]),
            (r"the statistics of brain data, in full", [49]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> The brain's rhythms in sleep are Part 10. Tuning "
            "curves and receptive fields, starting in the eye, are Part 13. The face area, and the "
            "argument about what it's for, is in Part 14. Attention measured on the scalp is Part 18. The "
            "N400 returns with language in Part 23. Evidence building up in the brain before a choice is "
            "Part 25. What a scan can say about awareness is Part 27. Why findings fail to repeat gets "
            "the whole of Part 43. And the statistics of brain data, done in full, are Part 49."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One reads a "
            "tuning curve and asks how many showings it takes to tell two rates apart. One shows why "
            "unaligned cells are invisible from the scalp. One counts the trials an average needs. One "
            "builds the response to a block of events from the echo. One does the salmon's arithmetic for "
            "a whole brain. One uses Psyche's imaging module to see how circular selection depends on the "
            "sample. And the last, with the star, is the frontier's problem. Pause here if you'd like to "
            "try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"S. A. Huettel, A. W. Song \& G. McCarthy, \emph{Functional Magnetic Resonance Imaging} (3rd ed., 2014)",
             r"R. A. Poldrack, J. A. Mumford \& T. E. Nichols, \emph{Handbook of Functional MRI Data Analysis} (2011)",
             r"S. J. Luck, \emph{An Introduction to the Event-Related Potential Technique} (2nd ed., 2014)",
             r"R. A. Poldrack, \emph{The New Mind Readers} (2018)"],
            [r"C. M. Bennett et al.\ (2009); \ A. Eklund, T. E. Nichols \& H. Knutsson (2016)",
             r"D. H. Hubel \& T. N. Wiesel (1959); \ H. Berger (1929)",
             r"M. Kutas \& S. A. Hillyard (1980); \ M. Kutas \& K. D. Federmeier (2011)",
             r"S. Ogawa et al.\ (1990); \ G. M. Boynton et al.\ (1996); \ N. K. Logothetis et al.\ (2001)",
             r"E. Vul et al.\ (2009); \ N. Kriegeskorte et al.\ (2009); \ R. A. Poldrack (2006)",
             r"A. M. Owen et al.\ (2010); \ G. Ganis et al.\ (2011); \ A. T. Barker et al.\ (1985)",
             r"M. L. Elliott et al.\ (2020); \ S. Marek et al.\ (2022); \ J. Tang et al.\ (2023)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. The salmon poster is "
            "one page long, and it's the most useful page in the field."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"so far: \ the parts, a map, \ and instruments to read them", font_size=26, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 9", font_size=32, color=GREY_B), label(r"Genes and Evolution", font_size=50),
                     wrapped_label(r"Two men, separated as babies, meet at thirty-nine and find they share their "
                                   r"habits. \ The story proves nothing. \ The design behind it is another "
                                   r"matter.", 6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So now we have the machine's parts, a map of where they are, and instruments for watching "
            "them work. <bookmark mark='a'/> Every brain we've described so far has been a brain in "
            "general. But the people those brains belong to aren't alike, and the last chapter said how "
            "hard it is to read their differences off a scan. There's an older way to ask where "
            "differences between people come from, and it doesn't need a scanner. <bookmark mark='b'/> "
            "Two men, twins separated as babies and raised in different families, meet for the first time "
            "at thirty-nine, and find they share a startling list of habits. As evidence, that story is "
            "worth nothing, and you know why. The research design behind it is one of the most repeated in "
            "psychology. What it measures, and what it can't, is Part 9: genes and evolution."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
