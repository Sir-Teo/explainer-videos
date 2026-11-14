from __future__ import annotations

from videos.psychology.psych6.common import *  # noqa: F403

PROBLEMS = [
    r"A synapse has $n = 5$ release sites, each releasing with probability $p = 0.3$, and one packet gives "
    r"$q = 0.4$ mV. \ Find the mean response, its variance, and the share of impulses that release nothing. \ If "
    r"learning doubled the mean and left the share of failures unchanged, which of $n$, $p$, $q$ changed?",
    r"Treat an EPSP as a jump of 2.5 mV that decays as $e^{-t/\tau}$ with $\tau = 10$ ms. \ Two arrive a time "
    r"$\Delta$ apart. \ Find the peak of the sum, and how close they must be for it to reach 4 mV.",
    r"For a passive membrane with $g_L = 0.1$ mS/cm$^2$ and $E_E - E_L = 65$ mV, find the steady response to "
    r"$g_E = 0.05$ with and without a shunt $g_I = 0.15$ whose battery is at rest. \ Show that for small $g_E$ the "
    r"shunt divides the response by $(g_L + g_I)/g_L$.",
    r"Average Hebb's rule over the inputs to get $\dot w = \eta\, C w$, with $C$ the inputs' correlation matrix, "
    r"and show that $w$ grows fastest along the first eigenvector. \ Then show that a fixed point of Oja's rule "
    r"satisfies $C w = (w^{\top} C w)\, w$, so that $w$ is an eigenvector of length 1.",
    r"A BCM cell sees two patterns equally often and responds $y_1$ and $y_2$; its threshold is "
    r"$\theta = \langle y^2 \rangle$. \ Show that in the selective state ($y_2 = 0$) the response settles at "
    r"$y_1 = 2$. \ Where does it settle if pattern 1 is shown only a quarter of the time?",
    r"With \texttt{explainer.psychology.psyche.circuits}: apply \texttt{lateral} to a step of light with the "
    r"strength of inhibition at 0.1, 0.25 and 0.4. \ How does the ratio across the edge change? \ What does a "
    r"wider reach (\texttt{space=4}) do to the bands?",
    r"$\star$ \ Design the experiment that would tell ``the memory is the pattern of strengthened synapses'' from "
    r"``the memory is which cells were chosen'', and say what each outcome would look like.",
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
        q, d, h, la = load("quanta"), load("integration"), load("hebb"), load("lateral")
        items = [
            (r"Loewi's two hearts: \ the signal crosses the gap as a chemical", EXC),
            (r"it is released in packets, by chance: \ strength $= n\,p\,q$", RULE),
            (r"a handful of transmitters, \ and six places where a drug can act", DATA),
            (rf"inputs add if they arrive within about {d['tau']:.0f} ms; \ a shunt divides", VOLT),
            (r"Hebb's rule, $\Delta w = \eta\,x\,y$: \ local, and it runs away", BAD),
            (rf"Oja's repair finds the direction of most variance: \ {pct(h['share'])} of it here", MODEL),
            (r"LTP, the NMDA receptor, spike timing: \ Hebb's rule in a molecule", EXC),
            (rf"lateral inhibition turns a ratio of 2 into {la['edge_out']:.1f} at an edge; \ it does not explain "
             r"the grid", INH),
            (r"the same motif with self-excitation holds a choice; \ with fatigue, it keeps time", THRESH),
            (r"populations swing when excitation and inhibition balance; \ modulators set gain and learning "
             r"rate", GREY_A),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t}", font_size=32, color=col) for k, (t, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 6, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part six in ten lines. <bookmark mark='a'/> Loewi's two hearts showed that the signal crosses "
            "the gap as a chemical. It's released in packets, by chance, so a synapse's strength is a "
            "product of three numbers. A handful of transmitters do the work, and there are six places where "
            "a drug can interfere. A neuron adds the inputs that arrive within about ten milliseconds of "
            "each other, and one kind of inhibition divides. Hebb's rule is local, and as stated it runs "
            "away. Oja's repair makes a cell find the direction in which its inputs vary most. Long-term "
            "potentiation, the NMDA receptor and spike timing are Hebb's rule in a molecule. Lateral "
            "inhibition exaggerates edges, and it doesn't explain the Hermann grid. The same motif with "
            "self-excitation holds a choice, and with fatigue it keeps time. And populations swing when "
            "excitation and inhibition are in balance, while the modulators set the gain and the learning "
            "rate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.9), run_time=42.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"equations that predict what they were not fitted to: \ a nerve's speed, Mach's bands. \ And one "
             r"that failed the same test: \ the grid", STATUS_COLOR["replicated"]),
            (r"minds can be compared fairly: \ a control, a shuffle, a balanced order", STATUS_COLOR["replicated"]),
            (r"blinds for the experimenter; \ for the analyst, a plan fixed before the data and a second "
             r"laboratory", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection was that the mind admits no mathematics. "
            "Part 5 gave the strongest reply we have. Today adds two things to it. A model of an eye, "
            "measured in a crab, predicted an illusion that Mach had described a century earlier. That's the "
            "reply getting stronger. And a model of the Hermann grid was mathematical, was computed, fitted "
            "what people see, and failed the first new test anyone gave it. That's a warning about what the "
            "reply requires. Equations aren't enough. What counts is a prediction made before the "
            "measurement, about something the model was never fitted to. The second and third objections "
            "stand as Act one left them."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows],
                      *[FadeIn(r.reply) for r in board.rows[1:]])
            vo.wait_until("a")
            self.play(FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"where things are: \ damage as an experiment", [7]),
            (r"what a recording of the brain measures", [8]),
            (r"lateral inhibition in your own retina", [13]),
            (r"dopamine as the third factor", [17]),
            (r"a choice held in activity", [19]),
            (r"is long-term potentiation how memories are stored?", [20]),
            (r"a circuit that decides, against people's reaction times", [25]),
            (r"what these drugs do for a disorder", [40]),
            (r"learning without a local rule", [58]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Where things are in a brain, with damage as the "
            "experiment, is the next part. What a recording of the brain measures is Part 8. Lateral "
            "inhibition in your own retina is Part 13. Dopamine as the third factor, Part 17. A choice held "
            "in activity becomes working memory in Part 19. Whether long-term potentiation is how memories "
            "are stored is argued in Part 20. The circuit that decides is tested against people's reaction "
            "times in Part 25. What these drugs do for a disorder begins in Part 40. And learning without a "
            "local rule is Part 58."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.5), run_time=13.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One works out "
            "what a synapse's failures tell you about where learning changed it. One adds two inputs in "
            "time. One shows that a shunt divides. One proves that Hebb's rule runs away along the first "
            "principal component, and that Oja's rule stops there. One finds where a BCM cell settles. One "
            "uses Psyche's circuits to see what sets the size of Mach's bands. And the last, with the star, "
            "is the frontier's problem. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=6.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"E. R. Kandel et al., \emph{Principles of Neural Science} (6th ed., 2021), the chapters on synaptic "
             r"transmission and plasticity",
             r"P. Dayan \& L. F. Abbott, \emph{Theoretical Neuroscience} (2001), chs.\ 7 and 8",
             r"D. O. Hebb, \emph{The Organization of Behavior} (1949)",
             r"E. S. Valenstein, \emph{The War of the Soups and the Sparks} (2005); \ F. Ratliff, \emph{Mach Bands} "
             r"(1965)"],
            [r"O. Loewi (1921); \ J. del Castillo \& B. Katz (1954)",
             r"E. Oja (1982); \ E. L. Bienenstock, L. N. Cooper \& P. W. Munro (1982)",
             r"T. V. P. Bliss \& T. L\o mo (1973); \ G.-Q. Bi \& M.-M. Poo (1998)",
             r"H. K. Hartline \& F. Ratliff (1957); \ J. Geier et al.\ (2008)",
             r"T. Graham Brown (1911); \ K. Matsuoka (1985); \ H. R. Wilson \& J. D. Cowan (1972)",
             r"X. Liu et al.\ (2012); \ E. H. Turner et al.\ (2008)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Hebb's book is still "
            "worth reading, seventy-five years on, for how much he got right from an armchair."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"the machine so far: \ neurons, synapses, small circuits", font_size=26, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        nxt = VGroup(label(r"Part 7", font_size=32, color=GREY_B), label(r"The Brain", font_size=50),
                     wrapped_label(r"Vermont, September 1848. \ An iron rod is blown through the head of a "
                                   r"railway foreman. \ He stays conscious, and he lives.", 6.0, 28, GREY_A)).arrange(
            DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So now the machine has connections. <bookmark mark='a'/> Neurons that talk through chemical "
            "synapses, synapses that change with use, and small circuits that sharpen, decide and keep time. "
            "What we haven't done is say where anything is. A brain has eighty-six billion of these cells. "
            "Is a memory, or a word, or a decision, in one place, or spread through all of it? For a long "
            "time the only way to find out was to wait for an accident. <bookmark mark='b'/> In September "
            "1848, in Vermont, an explosion blew an iron rod more than a metre long through the head of a "
            "railway foreman called Phineas Gage. He stayed conscious, and he lived for years. What "
            "happened to him afterwards, what the record really supports, and what a century of retelling "
            "added to it, is where Part 7 begins: the brain."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
