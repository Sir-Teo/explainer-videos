from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ Agreement", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"V(a) < V(b) \iff a \to b", font_size=40, color=LAM), r"vector clocks", LAM),
            tile(MathTex(r"f + 1", font_size=60, color=YES), r"rounds, \ with clocks", YES),
            tile(MathTex(r"\text{bivalent}", font_size=52, color=NO), r"FLP", NO),
            tile(MathTex(r"Q_1 \cap Q_2 \neq \varnothing", font_size=44, color=HEAD), r"Paxos and Raft", HEAD),
            tile(MathTex(r"n \ge 3f + 1", font_size=52, color=KERN), r"Byzantine generals", KERN),
            tile(MathTex(r"(q/p)^z", font_size=56, color=DATA), r"Nakamoto", DATA),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. The two generals, who cannot be certain. Causality instead of time, with "
            "Lamport's clocks and vector clocks, and snapshots of a system that never stops. Consensus in f plus "
            "one rounds when time is kept, and FLP's proof that it cannot be guaranteed when it is not. Coins, "
            "failure detectors and partial synchrony as the ways around. Paxos and Raft, safe because majorities "
            "intersect, and our Raft surviving a thousand storms while its broken twins did not. And traitors: "
            "three f plus one, PBFT, HotStuff, and Nakamoto's chain of work."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"replication, \ quorums, \ two-phase commit, \ CAP and Spanner's clocks", [39]),
            (r"MapReduce on sixteen Pebbles, \ one of which crashes", [39]),
            (r"Kubernetes, \ built on etcd's Raft", [45]),
            (r"exactly-once streams: \ Chandy-Lamport checkpoints", [46]),
            (r"TLA$^+$ and proofs of distributed protocols", [54]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 39 replicates data at scale: quorums, two-phase commit, the CAP theorem, "
            "Spanner's atomic clocks, and the Job itself on sixteen Pebbles, one of which crashes. Part 45's "
            "Kubernetes keeps its state in etcd, which is Raft. Part 46's stream processors checkpoint with "
            "Chandy and Lamport's snapshots. And Part 54 returns to TLA plus and proofs."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"don't build it", r"use etcd, \ ZooKeeper or Consul for leader election, \ locks and configuration"),
            (r"cluster size", r"3 or 5 voters, \ not 4: \ an even number tolerates no more failures"),
            (r"timeouts", r"election timeout $\gg$ round trip; \ randomize it; \ watch for GC pauses"),
            (r"fencing", r"a lock or lease needs a fencing token, \ checked by the resource, \ or a paused holder "
                         r"wakes and writes"),
            (r"testing", r"inject faults: \ partitions, \ crashes at chosen moments, \ clock skew; \ check "
                         r"histories"),
        ])
        with self.voiceover(
            "In practice. Do not write your own consensus: use etcd, ZooKeeper or Consul for leader election, "
            "locks and configuration. Run three or five voters, never four, since four tolerate no more failures "
            "than three. Make election timeouts much longer than a round trip, randomize them, and beware of "
            "garbage-collection pauses. Give every lock a fencing token that the protected resource checks, or a "
            "paused holder will wake up and write. And test with injected faults, aimed at the moments that "
            "matter."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that vector clocks characterize causality: \ $a \to b$ iff $V(a) < V(b)$.",
            r"Prove that FloodSet with $f + 1$ rounds solves consensus with up to $f$ crashes, \ and give a run "
            r"defeating it in $f$ rounds for $n = 4$, $f = 2$.",
            r"Prove Paxos's invariant: \ if $v$ is chosen in ballot $b$, \ every accept request with ballot "
            r"$b' > b$ carries $v$.",
            r"Show that OM(1) fails for three generals and one traitor, \ and that no protocol can succeed, \ by "
            r"the indistinguishability argument.",
            r"\textit{Build.} \ Add Raft's membership change \ (joint consensus, \ or one server at a time) \ to our "
            r"Raft, \ and extend the checker to cover it.",
            r"$\bigstar$ \textit{Research.} \ Design a fault-injection strategy that exposes all three planted bugs "
            r"in our Raft in as few runs as possible; \ argue why it should work for bugs you have not seen.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add membership changes to our Raft, the part every real deployment needs, and extend the "
            "checker to cover them. The last, marked with a star, is a research problem: find a way of injecting "
            "faults that exposes all three of our planted bugs quickly, and argue that it would find bugs you have "
            "not planted."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 39, \ Distributed Systems II: \ Scale", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"replication and quorums; \ two-phase commit, \ and why it blocks", HEAD),
            (r"the CAP theorem, \ precisely; \ consistency models", NO),
            (r"Spanner and TrueTime: \ consistency from atomic clocks", YES),
            (r"MapReduce on sixteen Pebbles, \ one of which crashes", LAM))]).arrange(DOWN, buff=0.35)
        q = label(r"ledger row 15", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Part 39: Distributed systems, scale. Replication and quorums, two-phase commit and why it "
            "can block for ever, the CAP theorem stated precisely, and Spanner, which buys consistency with atomic "
            "clocks. And the Job runs on sixteen Pebbles, one of which crashes in the middle: ledger row fifteen."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Lynch, \textit{Distributed Algorithms}; \ Attiya and Welch, \textit{Distributed Computing}",
             r"Cachin, Guerraoui and Rodrigues, \textit{Reliable and Secure Distributed Programming}",
             r"van Steen and Tanenbaum, \textit{Distributed Systems}; \ Kleppmann, \textit{Designing Data-Intensive "
             r"Applications}, \ ch. 8--9"],
            [r"Lamport \ (1978, 1998, 2001); \ Chandy and Lamport \ (1985); \ Fischer, Lynch and Paterson \ (1985)",
             r"Dwork, Lynch and Stockmeyer \ (1988); \ Ben-Or \ (1983); \ Chandra and Toueg \ (1996); \ Schneider \ "
             r"(1990)",
             r"Ongaro and Ousterhout \ (2014); \ Lamport, Shostak and Pease \ (1982); \ Castro and Liskov \ (1999); "
             r"\ Yin et al. \ (2019)",
             r"Nakamoto \ (2008); \ Rosenfeld \ (2014); \ Eyal and Sirer \ (2014); \ Newcombe et al. \ (2015)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES)
