from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.checking()
        self.bounds()
        self.open()

    def card(self):
        card = chapter_card(11, r"Frontier: \ proving and breaking", r"How do we know a distributed system is correct?",
                            lit=(2013, 2022), extra=((2015, r"Newcombe et al.: \ TLA$^+$ at Amazon"),
                                                     (2015, r"Verdi, \ IronFleet"),
                                                     (2022, r"Lewis-Pye: \ quadratic BFT")), part=PART)
        with self.voiceover("Chapter eleven. Frontier: proving and breaking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def checking(self):
        r = load("raft")
        head = label(r"Three ways to be sure", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            wrapped_label(r"\textbf{model checking a specification}: \ Amazon engineers wrote TLA$^+$ models of "
                          r"S3, \ DynamoDB and others; \ the checker found subtle bugs, \ one needing a 35-step "
                          r"trace, \ that reviews and tests had missed \ (Newcombe et al., 2015; \ Part 54)", 12.4,
                          font_size=23, color=HEAD),
            wrapped_label(r"\textbf{testing the real system}: \ Kyle Kingsbury's Jepsen partitions real databases and "
                          r"checks the histories for linearizability \ (Part 33); \ since 2013 it has found lost writes "
                          r"or stale reads in a long list of products whose documentation promised otherwise", 12.4,
                          font_size=23, color=KERN),
            wrapped_label(r"\textbf{proving the implementation}: \ Verdi \ (Coq) \ and IronFleet \ (Dafny) \ proved "
                          r"Raft and Paxos implementations correct \ (2015): \ thousands of lines of proof per "
                          r"thousand of code", 12.4, font_size=23, color=YES),
            wrapped_label(rf"\textbf{{ours}}: \ random storms found the Figure 8 bug once in 1{{,}}000 runs, \ and the "
                          rf"forgotten vote never; \ one aimed fault found it in "
                          rf"{r['forget-vote targeted']['violating_runs']}", 12.4, font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "How does anyone know a distributed system is correct? There are three answers, and the field uses "
            "all of them. <bookmark mark='a'/> Check a model. Engineers at Amazon wrote specifications of S3, "
            "DynamoDB and other systems in Lamport's TLA plus, and the model checker found bugs that design "
            "reviews and testing had missed, one needing a precise sequence of thirty-five steps. "
            "<bookmark mark='b'/> Test the real thing. Kyle Kingsbury's Jepsen partitions real databases and checks "
            "the histories against linearizability, the property of Part 33, and it has found lost writes and stale "
            "reads in a long list of systems whose documentation promised otherwise. <bookmark mark='c'/> Or prove "
            "the implementation itself. In 2015 the Verdi project, in Coq, and IronFleet, in Dafny, verified "
            "working implementations of Raft and Paxos, at the cost of several lines of proof for every line of "
            "code. <bookmark mark='d'/> Our own campaign shows why the first two are hard: the Figure 8 bug "
            "surfaced once in a thousand random storms, and the forgotten vote never, until one well-aimed fault "
            "exposed it in eighty-seven."
        ) as vo:
            self.play(FadeIn(head))
            for mk, rw in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(rw))
        self.wait(0.4)
        self.clear_scene()

    def bounds(self):
        b = load("byzantine")
        head = label(r"What consensus must cost", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"crash, \ synchronous", r"$f + 1$ rounds", r"Fischer and Lynch 1982"],
                [r"crash, \ asynchronous, \ deterministic", r"impossible", r"FLP 1985"],
                [r"Byzantine, \ any timing", r"$n \ge 3f + 1$ \ (no signatures)", r"Lamport et al. 1982"],
                [r"Byzantine, \ deterministic", r"$\Omega(n^2)$ messages", r"Dolev and Reischuk 1985"],
                [r"Byzantine, \ partial synchrony", r"$O(n^2)$ worst case, \ matched", r"Lewis-Pye; \ Civit et al. "
                 r"2022"]]
        tab = grid_table([r"setting", r"bound", r"who"], rows, widths=[4.8, 3.8, 3.6], row_h=0.5, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k, c in ((1, YES), (2, NO), (3, HEAD), (4, KERN), (5, LAM)):
            tab.cells[k][1].set_color(c)
        foot = wrapped_label(rf"HotStuff is linear per leader, \ {b['messages'][-1]['hotstuff']} messages at $n = 100$, "
                             r"\ but a run of faulty leaders makes it quadratic again; \ protocols that are linear "
                             r"when leaders are good \textit{and} optimal when they are not appeared only recently",
                             12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Fifty years of lower bounds say what agreement must cost. <bookmark mark='a'/> Crash failures with "
            "clocks: f plus one rounds. Without clocks, no deterministic protocol at all. Lying machines: n at "
            "least three f plus one, unless messages are signed. And Danny Dolev and Rüdiger Reischuk proved that "
            "any deterministic Byzantine agreement must, in the worst case, send a number of messages growing as n "
            "squared. Only in 2022 did protocols for partial synchrony match that bound in the worst case. "
            "<bookmark mark='b'/> HotStuff's linear cost per leader is the good case: a run of faulty leaders makes "
            "it quadratic again, and designing protocols that are cheap when things go well and optimal when they "
            "do not is current research."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(len(rows) + 1)], lag_ratio=0.3),
                      Create(tab.rule))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Finding bugs efficiently}: \ which fault schedules expose which bugs? \ "
                          r"Random search is hopeless for deep ones; \ coverage-guided and ``lineage-driven'' fault "
                          r"injection help, \ with no theory of how many runs suffice.", 12.4, font_size=25,
                          color=WHITE),
            wrapped_label(r"2. \ \textbf{Verifying what runs}: \ proofs cover protocols, \ but real systems add "
                          r"reconfiguration, \ snapshots, \ storage faults \ (``protocol-aware recovery'', \ 2018) \ "
                          r"--- \ and the proofs rarely keep up with the code.", 12.4, font_size=25, color=YES),
            wrapped_label(r"3. \ \textbf{Communication}: \ the best latency and message complexity achievable "
                          r"together, \ for Byzantine agreement with optimistic fast paths.", 12.4, font_size=25,
                          color=HEAD),
            wrapped_label(r"4. \ \textbf{Gray failure}: \ machines that are slow, \ or fail only some requests, \ "
                          r"defeat every model in this part; \ detecting them is largely empirical.", 12.4,
                          font_size=25, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ a fault-injection strategy that finds our "
                             r"three planted Raft bugs in few runs", 12.4, font_size=24, color=LAM).to_edge(DOWN,
                                                                                                    buff=0.35)
        with self.voiceover(
            "Where this leaves the field. <bookmark mark='a'/> Finding bugs efficiently: which fault schedules "
            "expose which bugs? Random search is hopeless for deep ones, and smarter strategies, guided by coverage "
            "or by which messages each result depended on, help in practice, without any theory of how many runs "
            "suffice. <bookmark mark='b'/> Verifying what actually runs: proofs cover protocols, but real systems "
            "add changes of membership, snapshots and storage that silently corrupts data, and the proofs rarely "
            "keep pace with the code. <bookmark mark='c'/> The best achievable combination of latency and message "
            "count for Byzantine agreement. <bookmark mark='d'/> And gray failure: machines that are slow, or fail "
            "only some requests, which defeat every clean model in this part. <bookmark mark='e'/> This part's "
            "research problem asks for a fault-injection strategy that finds all three of our planted Raft bugs in "
            "as few runs as possible."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, NO)
