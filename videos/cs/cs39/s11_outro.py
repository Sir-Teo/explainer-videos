from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Scale", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"R + W > N", font_size=56, color=HEAD), r"quorums", HEAD),
            tile(MathTex(r"a \sqcup b = b \sqcup a", font_size=48, color=YES), r"CRDTs converge", YES),
            tile(MathTex(r"\tfrac{1}{n+1}", font_size=64, color=LAM), r"keys moved, \ consistent hashing", LAM),
            tile(MathTex(r"2\varepsilon", font_size=64, color=KERN), r"Spanner's commit wait", KERN),
            tile(MathTex(r"\text{map} \to \text{shuffle} \to \text{reduce}", font_size=36, color=DATA),
                 r"re-execution, \ not replication", DATA),
            tile(MathTex(r"1 - 0.99^{100}", font_size=52, color=NO), r"the tail at scale", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. The datacenter as one computer, and what its distances cost. Replicas, "
            "their lag, and quorums whose overlap buys fresh reads, with the staleness of sloppier quorums "
            "measured. The hierarchy of consistency models, CAP stated precisely, and CRDTs, whose merges cannot "
            "conflict. A hash ring that moves almost no keys, and Chord's fingers. Two-phase commit, which can "
            "block for ever, and Spanner, which waits out its clock uncertainty. The Job as MapReduce on sixteen "
            "Pebbles, surviving a crash. And the tail: one slow server in a hundred, hedged requests, two choices, "
            "and failures that feed themselves."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"CRDTs in version control and local-first apps", [41, 42]),
            (r"latency budgets across a call graph; \ the tail again", [43, 47]),
            (r"streams, \ watermarks, \ exactly-once; \ MPP shuffles", [46]),
            (r"sharding, \ hot keys, \ replicas and fencing in system design", [48, 49]),
            (r"load shedding, \ retry budgets, \ hedging in production", [50]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. CRDTs return in version control and in local-first web apps, Parts 41 and 42. "
            "The tail returns as latency budgets across a graph of services and in search engines. Part 46 builds "
            "streams with watermarks and exactly-once state, and query engines that shuffle like MapReduce. Parts "
            "48 and 49 design real systems with sharding, hot keys and fencing tokens. And Part 50 keeps them "
            "running, with the load shedding and retry budgets that cure metastable failures."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"consistency", r"a product decision: \ which anomalies may users see? \ default to strong, \ relax "
                             r"where measured"),
            (r"stores", r"Cassandra and DynamoDB \ (quorums), \ Spanner and CockroachDB \ (consensus and clocks), \ "
                        r"Redis Cluster \ (hash slots)"),
            (r"batch and streams", r"Spark, \ Flink, \ Beam: \ MapReduce's model with memory and watermarks"),
            (r"the tail", r"measure the 99th percentile, \ not the mean; \ hedge idempotent reads; \ two choices "
                          r"in the balancer"),
            (r"retries", r"deadlines, \ exponential backoff with jitter, \ retry budgets, \ and dropping expired "
                         r"work"),
        ])
        with self.voiceover(
            "In practice. Treat consistency as a product decision: which anomalies may a user see? Start strong and "
            "relax only where you have measured the cost. Cassandra and DynamoDB use quorums; Spanner and "
            "CockroachDB use consensus and clocks; Redis Cluster splits keys into hash slots. Spark, Flink and "
            "Beam are MapReduce's model with memory and watermarks. Watch the ninety-ninth percentile, not the "
            "mean, hedge reads that are safe to repeat, and let the load balancer use two choices. And give every "
            "request a deadline: back off with jitter, budget your retries, and throw away work nobody is waiting "
            "for."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that if $R + W > N$, \ every read quorum meets every write quorum, \ and give a run with "
            r"$R + W \le N$ that returns a stale value.",
            r"Prove that a state-based CRDT whose merge is the join of a semilattice converges: \ replicas that have "
            r"received the same updates are equal, \ in any order, \ with repeats.",
            r"Show that adding an $(n+1)$th node to a consistent-hashing ring moves $1/(n+1)$ of the keys in "
            r"expectation, \ and that $h(k) \bmod n$ moves a fraction $n/(n+1)$.",
            r"Show that two-phase commit blocks if the coordinator crashes after one participant votes yes, \ and "
            r"explain why Spanner's commit wait of $2\varepsilon$ makes timestamps respect real time.",
            r"\textit{Build.} \ Let our MapReduce survive the master's crash: \ log its task table, \ restart it "
            r"mid-Job, \ and show the answer is unchanged.",
            r"$\bigstar$ \textit{Research.} \ Design a retry and admission policy for our metastable simulator that "
            r"provably recovers from any finite spike, \ while keeping hedging's tail benefit; \ test it against "
            r"adversarial spikes.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: our MapReduce survives any worker's crash, but not its master's. Make it survive that too, "
            "and show that the answer does not change. The last, marked with a star, is a research problem: a retry policy that "
            "provably recovers from any finite spike, without giving up what hedging bought."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 40, \ Software Engineering", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"Parnas' information hiding, \ and one change rippling through", HEAD),
            (r"abstraction, \ contracts, \ behavioural subtyping", YES),
            (r"this repository's own dependency graph, \ measured", LAM),
            (r"testing, \ flakiness, \ Brooks' and Conway's laws", NO))]).arrange(DOWN, buff=0.35)
        q = label(r"Act VIII: \ Building Software", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "That ends Act Seven, Many Machines. Next time, Part 40 opens Act Eight, Building Software, with "
            "software engineering: Parnas' information hiding, contracts and subtyping, testing and flaky tests, "
            "Brooks' and Conway's laws, and the dependency graph of the very repository that built this series, "
            "measured."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kleppmann, \textit{Designing Data-Intensive Applications}; \ Barroso, H\"olzle and Ranganathan, "
             r"\textit{The Datacenter as a Computer}",
             r"Saltzer and Kaashoek, \textit{Principles of Computer System Design}; \ van Steen and Tanenbaum, "
             r"\textit{Distributed Systems}"],
            [r"DeCandia et al. \ (2007); \ Bailis et al. \ (2012, 2014); \ Gilbert and Lynch \ (2002); \ Shapiro et "
             r"al. \ (2011)",
             r"Karger et al. \ (1997); \ Stoica et al. \ (2001); \ Corbett et al. \ (2012); \ Dean and Ghemawat \ "
             r"(2004)",
             r"Zaharia et al. \ (2012); \ Akidau et al. \ (2015); \ Burrows \ (2006); \ Hunt et al. \ (2010)",
             r"Dean and Barroso \ (2013); \ Huang et al. \ (2017, 2022); \ Mahajan et al. \ (2011); \ Hellerstein "
             r"and Alvaro \ (2019)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES)
