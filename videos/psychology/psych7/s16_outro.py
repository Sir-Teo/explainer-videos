from __future__ import annotations

from videos.psychology.psych7.common import *  # noqa: F403

PROBLEMS = [
    r"In the diagram of chapter 3, a lesion cuts the link between word sounds and concepts and leaves everything "
    r"else. \ Which of understanding, speaking and repeating survive? \ Name the lesion that gives the opposite "
    r"pattern for repeating.",
    r"Under one resource, a share $p_A = 0.20$ of patients fail only task A and, with noisy tests, "
    r"$p_B = 0.007$ fail only task B. \ Show that the chance a screen of $N$ patients contains both kinds is "
    r"$1 - (1 - p_A)^N - (1 - p_B)^N + (1 - p_A - p_B)^N$, and evaluate it for $N = 100$.",
    r"With $M(E) = 17.3 / (E + 0.75)$ mm per degree, show that the cortical distance from the centre of gaze to "
    r"eccentricity $E$ is $17.3 \ln(1 + E/0.75)$ mm. \ How much larger must a letter be at $8^{\circ}$ than at "
    r"$1^{\circ}$ to cover the same length of cortex?",
    r"Your blind spot is centred $15^{\circ}$ from fixation and is $5.5^{\circ}$ wide. \ Two marks are 10 cm apart. "
    r"\ How far from them must your eye be for one to vanish while you fix the other? \ How many full moons "
    r"($0.5^{\circ}$) fit across the hole?",
    r"Eight controls score a mean of 33.25 with standard deviation 3.11; a patient scores 24. \ Compute $z$ and "
    r"the single-case $t$. \ Repeat for thirty controls with the same mean and standard deviation, and explain "
    r"the change.",
    r"With \texttt{explainer.psychology.psyche.brain}: build an \texttt{Architecture} in which two tasks share "
    r"one module and each has a module of its own. \ Which lesions dissociate them? \ Then run "
    r"\texttt{lesion\_study} with and without \texttt{vascular} and compare where the maps point.",
    r"$\star$ \ Design the lesion study that would tell ``this region is needed'' from ``a connection passing "
    r"under this region is needed'', and say what each outcome would look like.",
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
        t, m, d, mp, b = load("tour"), load("massaction"), load("dissociation"), load("maps"), load("blindspot")
        chance = float(d["chance_typical"][99])
        items = [
            (r"Gage survived, and something changed: \ the record is a few sentences", DATA),
            (rf"{t['neurons'] / 1e9:.0f} billion neurons; \ {pct(t['mass_share'])} of your weight, \ "
             rf"{pct(t['energy_share'])} of your energy", VOLT),
            (r"Gall asked the right question with the wrong method; \ Lashley's maze could be run six ways",
             CEREBELLUM),
            (r"Broca and Wernicke: \ two aphasias, \ and a diagram that predicted a third", FRONTAL),
            (rf"a double dissociation rules out one resource, \ unless noise fakes it: \ {pct(chance)} in a "
             r"screen of 100", THRESH),
            (rf"maps: \ $M = 17.3/(E + 0.75)$ mm per degree; \ {pct(mp['share_at'][0])} of the map for the "
             r"central degree", OCCIPITAL),
            (rf"a hole in each eye's view, \ {b['centre_deg']:.0f} degrees out, \ that the brain fills in",
             PARIETAL),
            (r"H.M.: \ no new memories of events, \ and a skill learned all the same", TEMPORAL),
            (r"the split brain: \ one half knows what the other cannot say; \ brain ``types'' failed", LESION),
            (r"maps rewire with use; \ the unit is a network; \ the ten-percent myth fails on the energy bill",
             GREY_A),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=32, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 7, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part seven in ten lines. <bookmark mark='a'/> Gage survived, and something changed, and the "
            "record of what is a few sentences long. A brain has eighty-six billion neurons, and it takes a "
            "fifth of your energy. Gall asked the right question with the wrong method, and Lashley got the "
            "wrong answer from a task that could be done six ways. Broca and Wernicke found two aphasias, "
            "and a diagram predicted a third. A double dissociation rules out a single resource, unless "
            "noisy tests and a large screen fake one. The cortex holds maps, and the visual one spends a "
            "great deal on the centre of gaze. Each eye has a hole in its view that the brain fills in. "
            "H.M. could lay down no new memories of events, and learned a skill all the same. In the split "
            "brain, one half knows what the other can't say, and the idea of left-brained and right-brained "
            "people failed. And the maps rewire with use, the unit is a network, and the ten-percent myth "
            "fails on the energy bill."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows[1:]], lag_ratio=0.9), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"equations that predict what they were not fitted to: \ a nerve's speed, Mach's bands", STATUS_COLOR[
                "replicated"]),
            (r"the mind does come apart: \ speech without understanding, \ a skill without the memory of "
             r"learning it. \ But not at will: \ damage is not assigned at random", STATUS_COLOR["replicated"]),
            (r"blinds for the experimenter; \ for the analyst, a plan fixed before the data and a second "
             r"laboratory", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> Today belongs to the second objection. Kant said there can "
            "be no experiment on the mind, because its contents can't be taken apart and put together "
            "again at will. Half of that is now answered. The mind does come apart. Speech goes and "
            "understanding stays. The memory of a lesson goes and the skill stays. Those are joints that "
            "nobody found by introspection. The other half of the objection stands. It isn't done at will. "
            "Nobody assigns a stroke, so every lesion study is a comparison of groups that formed "
            "themselves, and the frontier showed what that costs. The next part looks for a way to see a "
            "healthy brain at work."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows], FadeIn(board.rows[0].reply),
                      FadeIn(board.rows[2].reply))
            vo.wait_until("a")
            self.play(FadeIn(board.rows[1].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"watching an intact brain at work", [8]),
            (r"the map of the visual field, from the retina in", [13]),
            (r"filling in: \ seeing what is not there", [14]),
            (r"neglect, and what attention is", [18]),
            (r"H.M. and the kinds of memory", [20]),
            (r"aphasia, and how language is built", [23]),
            (r"blindsight: \ seeing without knowing it", [27]),
            (r"critical periods", [30]),
            (r"maps of brain data as statistics", [49]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Watching an intact brain at work is the next part. "
            "The map of the visual field, starting from the retina, is Part 13. Filling in, and seeing what "
            "isn't there, is Part 14. Neglect comes back with attention in Part 18. H.M. and the kinds of "
            "memory are Part 20. Aphasia returns with language in Part 23. Blindsight, seeing without "
            "knowing it, is in Part 27. Critical periods belong to Part 30. And maps of brain data, treated "
            "as the statistics they are, get Part 49."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One uses the "
            "diagram to predict a fourth aphasia. One works out how often a large screen of patients fakes "
            "a double dissociation. One integrates the magnification formula. One has you compute where "
            "your own blind spot falls. One compares a patient with eight controls, and then with thirty. "
            "One uses Psyche's brain module to build an architecture and to run a lesion study. And the "
            "last, with the star, is the frontier's problem. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"B. Kolb \& I. Q. Whishaw, \emph{Fundamentals of Human Neuropsychology} (8th ed., 2021)",
             r"T. Shallice, \emph{From Neuropsychology to Mental Structure} (1988)",
             r"M. Macmillan, \emph{An Odd Kind of Fame: Stories of Phineas Gage} (2000)",
             r"S. Corkin, \emph{Permanent Present Tense} (2013); \ M. S. Gazzaniga, \emph{Tales from Both Sides of "
             r"the Brain} (2015)"],
            [r"J. M. Harlow (1868); \ P. Broca (1861); \ N. F. Dronkers et al.\ (2007)",
             r"C. Wernicke (1874); \ L. Lichtheim (1885); \ K. S. Lashley (1929)",
             r"W. Penfield \& E. Boldrey (1937); \ J. C. Horton \& W. F. Hoyt (1991)",
             r"W. B. Scoville \& B. Milner (1957); \ L. Weiskrantz et al.\ (1974)",
             r"T. N. Wiesel \& D. H. Hubel (1963); \ M. M. Merzenich et al.\ (1984)",
             r"E. A. Maguire et al.\ (2000); \ K. Woollett \& E. A. Maguire (2011); \ J. A. Nielsen et al.\ (2013)",
             r"J. R. Crawford \& D. C. Howell (1998); \ Y.-H. Mah et al.\ (2014)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. If you read one, make "
            "it Macmillan on Gage. It's a lesson in how a case turns into a legend."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"so far: \ neurons, synapses, circuits, \ and a map", font_size=26, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 8", font_size=32, color=GREY_B), label(r"Reading the Brain", font_size=50),
                     wrapped_label(r"2009. \ A dead salmon is put in a brain scanner and shown photographs of "
                                   r"people. \ The scanner finds ``activity''.", 6.0, 28, GREY_A)).arrange(
            DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So now the machine has a map. <bookmark mark='a'/> Parts with different jobs, cables between "
            "them, and a logic for telling which part a task needs. But all of it came from brains that "
            "were broken, by accidents nobody chose. What we want is to watch a healthy brain while it "
            "reads a word or makes a choice. There are machines that claim to do that, and the pictures "
            "they make are very persuasive. <bookmark mark='b'/> In 2009 a group of researchers put a dead "
            "salmon in a brain scanner, showed it photographs of people, and asked it what the people were "
            "feeling. The scanner found activity in its brain. What that fish teaches about a coloured "
            "blob, and what the blobs have and haven't delivered, is Part 8: reading the brain."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
