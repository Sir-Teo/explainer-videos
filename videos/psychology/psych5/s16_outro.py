from __future__ import annotations

from videos.psychology.psych5.common import *  # noqa: F403

PROBLEMS = [
    r"Calcium is at 2 mM outside a cell and 0.0001 mM inside, and its ion carries two charges. \ Find its Nernst "
    r"potential at body temperature ($RT/F = 26.7$ mV). \ Which way does calcium move when a calcium channel opens "
    r"at $-65$ mV?",
    r"A membrane has resistance 10 k$\Omega\,$cm$^2$ and capacitance 1 $\mu$F/cm$^2$. \ Find its time constant, and "
    r"the time a step of current takes to bring the voltage 95\% of the way. \ Two equal inputs arrive 30 ms "
    r"apart: \ how much of the first is left when the second comes?",
    r"A gate starts at $n = 0$ and relaxes as $n(t) = 1 - e^{-t/\tau}$. \ Show that $n$ starts rising at once, and "
    r"that $n^4$ starts with zero slope. \ What feature of the potassium record does that reproduce?",
    r"At the peak of an action potential $dV/dt = 0$, with no injected current. \ Show from the model's first "
    r"equation that the peak voltage is an average of the three batteries, weighted by the conductances at that "
    r"moment. \ Why must it lie below $E_{Na}$?",
    r"For the integrate-and-fire neuron derive the time to reach threshold $\theta$ from reset under a steady "
    r"current, and the firing rate. \ With $\tau = 10$ ms and a dead time of 2 ms, what is the rate at twice the "
    r"least current that fires the cell?",
    r"With \texttt{explainer.psychology.psyche.neuron}: find the threshold of \texttt{HH()} for pulses of 0.1, 0.5, "
    r"2 and 10 ms. \ Show that for short pulses the charge delivered is what matters, and that long pulses need a "
    r"least current. \ Why does each happen?",
    r"$\star$ \ Find the smallest change to the integrate-and-fire neuron that lets one cell compute ``one but not "
    r"both'', and say what measurement on a real cell would show whether it does.",
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
        i, c = load("ions"), load("cable")
        items = [
            (r"Galvani: \ nerves are electrical. \ Helmholtz: \ and far too slow to be wires", DATA),
            (r"the nervous system is separate cells, \ and a neuron has a direction", VOLT),
            (rf"a difference in concentration is a battery: \ $E_K = {i['nernst']['K']:.0f}$ mV, \ "
             rf"$E_{{Na}} = {i['nernst']['Na']:+.0f}$ mV", K),
            (r"the voltage moves because doors open, \ not because the salt moves", NA),
            (r"the membrane is a leaky capacitor: \ it adds up a few milliseconds", LEAK),
            (r"the voltage clamp: \ sodium on fast and off by itself, \ potassium late", GATE["m"]),
            (r"four equations, fitted to the clamp, give threshold, one size, a dead time", MODEL),
            (rf"on a cable the signal renews itself: \ {c['velocity']:.1f} m/s computed, {c['observed']} measured",
             MODEL),
            (r"two variables keep the behaviour; \ one keeps the rate", GATE["n"]),
            (r"strength is carried by rate; \ and a cell with dendrites is more than a switch", THRESH),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t}", font_size=32, color=col) for k, (t, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        head = label(r"Part 5, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part five in ten lines. <bookmark mark='a'/> Galvani showed that nerves are electrical, and "
            "Helmholtz that they're far too slow to be wires. The nervous system is made of separate cells, "
            "and a neuron has a direction. A difference in concentration across a membrane is a battery, "
            "negative for potassium and positive for sodium. The voltage moves because doors open, not "
            "because the salt moves. The membrane is a leaky capacitor, which adds up what arrives within a "
            "few milliseconds. The voltage clamp showed sodium turning on fast and off by itself, and "
            "potassium turning on late. Four equations fitted to the clamp give a threshold, a signal of one "
            "size, and a dead time. On a cable the signal renews itself at every point, and its computed "
            "speed matched the measured one. Two variables keep the behaviour, and one keeps the rate. And "
            "strength is carried by the rate of signals, in a cell that's more than a switch."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.9), run_time=44.0)
        self.clear_scene()

    def score(self):
        c = load("cable")
        board = wager_board((
            (rf"four equations that predicted a speed they were never fitted to: \ {c['published']} against "
             rf"{c['observed']} m/s", STATUS_COLOR["replicated"]),
            (r"minds can be compared fairly: \ a control, a shuffle, a balanced order", STATUS_COLOR["replicated"]),
            (r"blinds for the experimenter; \ for the analyst, a plan fixed before the data and a second "
             r"laboratory", STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> His first objection was that the mind admits no mathematics. "
            "Today is the strongest reply the series will ever be able to give, and notice where it comes "
            "from. Not from the mind as a whole. From its smallest part, where four equations predicted a "
            "number that nobody had fitted them to. That's the standard. Most of psychology doesn't meet it "
            "yet, and the rest of this series is partly a record of how close each field has come. The second "
            "and third objections stand as Act one left them."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows],
                      *[FadeIn(r.reply) for r in board.rows[1:]])
            vo.wait_until("a")
            self.play(FadeIn(board.rows[0].reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"how neurons talk, and how talking changes them", [6]),
            (r"what a recording of the brain measures", [8]),
            (r"detection as counting noisy signals", [12]),
            (r"where a sound is: \ coincidence detectors", [15]),
            (r"accumulating to a threshold, as a model of deciding", [25]),
            (r"units without spikes: \ artificial networks", [60]),
        ], font_size=30)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> How neurons talk to each other, and how that talk "
            "changes them, is the next part. What an electrode or a scanner is measuring when it records "
            "from a brain is Part 8. Detection as the counting of noisy signals is Part 12. Coincidence "
            "detectors locate a sound in Part 15. Accumulation to a threshold returns as a model of how "
            "people decide, in Part 25. And the unit with the spikes left out, in artificial networks, is "
            "set against the real thing in Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.4), run_time=9.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=24)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One finds the "
            "battery of an ion we didn't discuss, calcium. One works the charging curve. One shows why a "
            "fourth power buys a delay. One reads the peak of the signal off the first equation. One derives "
            "the firing rate of the integrate-and-fire neuron. One uses Psyche's neuron to find how the "
            "threshold depends on the length of the pulse. And the last, with the star, is the research "
            "problem from the frontier. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=6.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"E. R. Kandel et al., \emph{Principles of Neural Science} (6th ed., 2021), the chapters on the membrane "
             r"and the action potential",
             r"P. Dayan \& L. F. Abbott, \emph{Theoretical Neuroscience} (2001), chs.\ 5 and 6",
             r"E. M. Izhikevich, \emph{Dynamical Systems in Neuroscience} (2007); \ C. Koch, \emph{Biophysics of "
             r"Computation} (1999)",
             r"S. Finger, \emph{Minds Behind the Brain} (2000)"],
            [r"A. L. Hodgkin \& A. F. Huxley (1939, 1952); \ K. S. Cole \& H. J. Curtis (1939)",
             r"E. D. Adrian \& Y. Zotterman (1926); \ L. Lapicque (1907)",
             r"R. FitzHugh (1961); \ J. Nagumo, S. Arimoto \& S. Yoshizawa (1962)",
             r"A. Gidon et al.\ (2020)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Hodgkin and Huxley's "
            "paper of 1952 is long, and it's one of the few scientific papers that can be read as a detective "
            "story."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"the machine has its first part: \ a neuron", font_size=26, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        nxt = VGroup(label(r"Part 6", font_size=32, color=GREY_B), label(r"Synapses and Circuits", font_size=50),
                     wrapped_label(r"Easter Saturday, 1921. \ A physiologist wakes from a dream with an experiment "
                                   r"in his head: \ two frog hearts, and one bath of fluid.", 6.0, 28, GREY_A)).arrange(
            DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "So that's the smallest moving part. <bookmark mark='a'/> A cell that holds a voltage, adds up "
            "its inputs over a few milliseconds, and when they reach a threshold sends one signal of one size "
            "down its axon. We haven't said what happens when that signal reaches the end. For half a "
            "century there were two camps: those who thought the signal jumped the gap as a spark, and those "
            "who thought it crossed as a chemical. <bookmark mark='b'/> On the night before Easter Sunday in "
            "1921, the physiologist Otto Loewi woke from a dream with the experiment that would settle it, "
            "two frog hearts and a shared bath of fluid. He wrote it down, and went back to sleep. In the "
            "morning he couldn't read his own handwriting. What he did the following night, and what it "
            "means that the connection between two neurons is chemical, and can therefore be changed, is "
            "Part 6: synapses and circuits."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
