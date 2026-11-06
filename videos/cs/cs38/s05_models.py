from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load)


class Models(VoiceoverScene):
    def construct(self):
        self.card()
        self.failures()
        self.timing()
        self.consensus()
        self.floodset()
        self.lower_bound()

    def card(self):
        card = chapter_card(4, r"Models and consensus", r"What exactly must machines agree on, and under what rules?",
                            lit=(1980, 1988), extra=((1982, r"Dolev and Strong"), (1988, r"Dwork, Lynch \\ and "
                                                                                          r"Stockmeyer")), part=PART)
        with self.voiceover("Chapter four. Models and consensus."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def failures(self):
        head = label(r"How machines fail", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(box(2.8, 0.75, r"crash", KERN, font_size=25),
                   wrapped_label(r"stops, \ and sends nothing more; \ the kind failure", 8.6, font_size=24,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(2.8, 0.75, r"crash-recovery", DATA, font_size=25),
                   wrapped_label(r"stops, \ then restarts with what it saved to disk: \ Raft's model", 8.6,
                                 font_size=24, color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(2.8, 0.75, r"omission", LAM, font_size=25),
                   wrapped_label(r"some messages it sends or should receive are lost", 8.6, font_size=24,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(2.8, 0.75, r"Byzantine", NO, font_size=25),
                   wrapped_label(r"anything at all: \ bugs, \ corrupted memory, \ or an adversary who lies "
                                 r"differently to each listener", 8.6, font_size=24, color=WHITE)).arrange(
                RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Every result in this part depends on two choices of model. The first is how machines may fail. "
            "<bookmark mark='a'/> A crash: the machine stops and never sends another message. "
            "<bookmark mark='b'/> Crash and recovery: it stops, then restarts with whatever it had saved on disk, "
            "which is the model Raft is designed for. <bookmark mark='c'/> Omission: some of its messages vanish. "
            "<bookmark mark='d'/> And Byzantine failure, named for Lamport's generals: the machine may do "
            "anything at all, including telling different lies to different listeners. A bug, a flipped bit in "
            "memory and a hostile operator all look like this."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(0.4)
        self.clear_scene()

    def timing(self):
        head = label(r"How time behaves", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"synchronous", r"known bounds on message delay and on relative speed", r"rounds; \ timeouts "
                 r"detect failures exactly"],
                [r"asynchronous", r"no bounds at all", r"a slow machine and a dead one are indistinguishable"],
                [r"partially synchronous", r"bounds exist but are unknown, \ or hold only after some unknown time",
                 r"the Internet, \ on a good day"]]
        tab = grid_table([r"model", r"assumption", r"what it means"], rows, widths=[3.0, 5.0, 4.4], row_h=0.8,
                         font_size=22, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for k, c in ((1, YES), (2, NO), (3, HEAD)):
            tab.cells[k][0].set_color(c)
        fd = wrapped_label(r"\textbf{failure detectors} \ (Chandra and Toueg, 1996): \ each machine has an oracle "
                           r"that suspects others, \ sometimes wrongly. \ The weakest that makes consensus possible, "
                           r"\ $\Diamond W$, \ only has to stop suspecting \textit{some} correct machine "
                           r"\textit{eventually}.", 12.4, font_size=22, color=LAM).next_to(tab, DOWN, buff=0.8)
        with self.voiceover(
            "The second choice is how time behaves. <bookmark mark='a'/> In a synchronous system there are known "
            "bounds on how long a message takes and how slow a machine can be, so computation proceeds in rounds, "
            "and a missing message proves a crash. In an asynchronous system there are no bounds at all, and a slow "
            "machine looks exactly like a dead one. Between them, Cynthia Dwork, Nancy Lynch and Larry Stockmeyer's "
            "partial synchrony: bounds exist but are unknown, or hold only after some unknown moment. That is the "
            "Internet on a good day. <bookmark mark='b'/> Tushar Chandra and Sam Toueg packaged timing as an "
            "oracle, a failure detector that suspects machines and may be wrong, and found the weakest one that "
            "makes consensus possible: it need only, eventually, stop suspecting one correct machine."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(fd))
        self.wait(0.4)
        self.clear_scene()

    def consensus(self):
        head = label(r"Consensus", font_size=36).to_edge(UP, buff=0.3)
        props = VGroup(
            label(r"each process proposes a value; \ each correct process must eventually \textbf{decide} one, \ "
                  r"so that:", font_size=23, color=WHITE),
            label(r"\textbf{agreement}: \ no two correct processes decide differently", font_size=24, color=YES),
            label(r"\textbf{validity}: \ the decision was someone's proposal", font_size=24, color=DATA),
            label(r"\textbf{termination}: \ every correct process decides", font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        uses = wrapped_label(r"agree on one value, \ and you can agree on a sequence: \ the next log entry, \ the next "
                             r"leader, \ whether to commit a transaction \ (Part 39), \ who holds a lock", 12.4,
                             font_size=22, color=GREY_A).next_to(props, DOWN, buff=0.8)
        with self.voiceover(
            "Now the problem itself. Each process proposes a value, and each correct process must eventually "
            "decide on one. <bookmark mark='a'/> Agreement: no two correct processes decide differently. "
            "<bookmark mark='b'/> Validity: the decision is one of the proposals, so the trivial protocol, always "
            "decide zero, is ruled out. <bookmark mark='c'/> Termination: every correct process does decide. "
            "<bookmark mark='d'/> Solve this for one value and you can solve it for a sequence: the next entry in "
            "a log, the next leader, whether a transaction commits, who holds a lock. Consensus is the core of "
            "every replicated system."
        ) as vo:
            self.play(FadeIn(head), FadeIn(props[0]))
            for mk, p in zip("abc", props[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(p))
            vo.wait_until("d")
            self.play(FadeIn(uses))
        self.wait(0.4)
        self.clear_scene()

    def floodset(self):
        f = load("floodset")
        head = label(r"With a clock: \ $f + 1$ rounds", font_size=36).to_edge(UP, buff=0.3)
        alg = wrapped_label(r"\textbf{FloodSet}: \ each round, \ every process sends everything it has seen to "
                            r"everyone; \ after $r$ rounds decide the smallest value seen. \ A crash may happen "
                            r"\textit{part-way} through a round: \ some get the message, \ some do not.", 12.4,
                            font_size=21, color=WHITE).next_to(head, DOWN, buff=0.4)
        rows = [[f"{r['n']}", f"{r['f']}", f"{r['rounds']}", f"{r['patterns']:,}", r"always" if r["agreement"]
                 else r"\textbf{broken}"] for r in f["rows"]]
        tab = grid_table([r"$n$", r"crashes $f$", r"rounds", r"crash patterns", r"agreement"], rows,
                         widths=[1.0, 1.8, 1.4, 2.4, 2.0], row_h=0.4, font_size=20, mono_cols=())
        tab.next_to(alg, DOWN, buff=0.4).set_x(-2.0)
        for k, r in enumerate(f["rows"], start=1):
            tab.cells[k][4].set_color(YES if r["agreement"] else NO)
        ce = f["rows"][0]["counterexample"]
        cex = wrapped_label(rf"one round, \ inputs {ce['inputs']}: \ $P_0$ crashes after reaching only $P_1$; \ "
                            r"$P_1$ saw 0, \ $P_2$ did not: \ they decide 0 and 1", 3.8, font_size=19,
                            color=NO).move_to([4.5, -0.6, 0])
        with self.voiceover(
            "If time is kept, consensus is easy, given enough rounds. <bookmark mark='a'/> In FloodSet, each "
            "round every process sends every value it has seen to everyone, and after the last round each decides "
            "the smallest value it has seen. The difficulty is a crash part-way through a round, when some "
            "processes get the dying machine's message and others do not. <bookmark mark='b'/> We checked every "
            "crash pattern: who crashes, in which round, and exactly which messages get out first. With f crashes "
            "allowed, f rounds always have a counterexample, and f plus one rounds never do. "
            "<bookmark mark='c'/> Here is the simplest: three processes, one round. Process zero, holding the only "
            "zero, crashes after its message reaches process one but not process two. One decides zero, two "
            "decides one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(alg))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(cex))
        self.wait(0.4)
        self.clear_scene()

    def lower_bound(self):
        head = label(r"Why $f + 1$ is necessary, \ and sufficient", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"\textbf{Sufficient.} \ In $f + 1$ rounds with at most $f$ crashes, \ some round has "
                          r"\textbf{no} crash. \ In that round every live process sends its whole set to every "
                          r"other, \ so afterwards all live sets are equal, \ and stay equal: \ the same minimum.",
                          12.4, font_size=25, color=YES),
            wrapped_label(r"\textbf{Necessary} \ (Fischer and Lynch, 1982; \ Dolev and Strong, 1983). \ Any "
                          r"protocol deciding in $f$ rounds can be attacked by crashing one process per round, \ "
                          r"each just after telling a single other: \ a chain of runs, \ each indistinguishable from "
                          r"the next to someone, \ leads from all-0 to all-1, \ so two neighbours must decide "
                          r"differently.", 12.4, font_size=25, color=NO),
            wrapped_label(r"the bound counts \textit{time}: \ even with perfect clocks, \ tolerating $f$ crashes "
                          r"costs $f + 1$ round trips", 12.4, font_size=25, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "Both halves are provable. <bookmark mark='a'/> Sufficiency first. With at most f crashes in f plus "
            "one rounds, some round has no crash at all. In that clean round every live process sends its whole set "
            "to every other, so afterwards all the live sets are equal, and later rounds keep them equal: everyone "
            "sees the same minimum. <bookmark mark='b'/> Necessity was proved by Michael Fischer and Nancy Lynch, "
            "and by Danny Dolev and Ray Strong. Against any protocol that decides in f rounds, crash one process "
            "per round, each just after it has told a single other. This builds a chain of executions, each "
            "indistinguishable from the next to some correct process, running from all inputs zero to all inputs "
            "one, and somewhere along it two neighbouring executions must decide differently. "
            "<bookmark mark='c'/> So even with perfect clocks, tolerating f crashes costs f plus one rounds of "
            "messages. And without clocks it gets much worse."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abc", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN,)
