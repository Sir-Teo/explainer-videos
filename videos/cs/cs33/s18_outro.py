from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ Concurrency", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\binom{6}{3} = 20", font_size=52, color=NO), r"the race, \ model-checked", NO),
            tile(MathTex(r"\textsf{flag}, \textsf{turn}", font_size=48, color=DATA), r"Peterson, \ proved", DATA),
            tile(MathTex(r"\mathcal{B}_{\rm SC} \subseteq \mathcal{B}_{\rm TSO} \subseteq \mathcal{B}_{\rm PSO}", font_size=40, color=HEAD),
                 r"allowed behaviors in our models", HEAD),
            tile(MathTex(r"O(1)\ \text{per handoff}", font_size=40, color=YES), r"locks; \ MCS", YES),
            tile(MathTex(r"\textsf{DRF} \Rightarrow \textsf{SC}", font_size=48, color=LAM), r"memory models", LAM),
            tile(MathTex(r"\textsf{CAS}: \infty", font_size=48, color=KERN), r"consensus numbers", KERN),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. A model checker that tries every interleaving, and the race it finds in one "
            "line of code. Peterson's lock, proved, then broken by store buffers and repaired with fences. Spin locks "
            "and the coherence traffic they cost, semaphores, monitors and deadlock. Memory models and the data-race-"
            "free bargain, linearizability, and lock-free structures with their ABA trap. Herlihy's hierarchy, with "
            "compare-and-swap at the top. And PebbleOS, with threads and an atomic instruction."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"a crash in the middle of a write: \ journals and fsync", [34]),
            (r"transactions, \ two-phase locking, \ MVCC", [35]),
            (r"agreement when machines fail: \ FLP, \ Paxos, \ Raft", [38]),
            (r"replication, \ consistency models, \ CRDTs", [39]),
            (r"verifying programs: \ invariants and model checking", [54]),
            (r"the LOCAL model and distributed lower bounds", [59]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 34 faces the cousin of the race: a crash in the middle of a write. Part 35's "
            "databases turn locks into transactions. Part 38 asks this part's consensus question between computers "
            "that can fail, and meets Fischer, Lynch and Paterson. Part 39 weakens consistency deliberately, for "
            "speed. Part 54 builds the verification methods we used informally here, and Part 59 the theory of "
            "distributed computation."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"default", r"share less: \ message passing, \ immutable data, \ one owner per object"),
            (r"locks", r"one lock order, \ written down; \ hold locks briefly; \ never call unknown code holding one"),
            (r"waiting", r"condition variables in a \texttt{while} loop; \ prefer library queues and channels"),
            (r"atomics", r"default to sequentially consistent ones; \ use acquire/release only with a proof"),
            (r"tools", r"ThreadSanitizer, \ Go's \texttt{-race}, \ Rust's \texttt{Send}/\texttt{Sync}; \ "
                       r"model-check the tricky core"),
        ])
        with self.voiceover(
            "In practice. Share less: pass messages, use immutable data, give each object one owner. When you need "
            "locks, write down one lock order, hold them briefly, and never call unknown code while holding one. Wait "
            "on condition variables in a while loop, or better, use the library's queues and channels. Use "
            "sequentially consistent atomics unless you can prove the weaker ones correct. And run a race detector "
            "in every test, and a model checker on the small, tricky core."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that two threads each doing $k \ge 2$ increments, \ load-add-store, \ can leave the counter at 2, \ "
            r"and never below 2.",
            r"Prove that Peterson's algorithm guarantees bounded waiting: \ a thread enters after at most one entry of "
            r"the other.",
            r"Show that the bakery algorithm is correct even if a read that overlaps a write returns any value.",
            r"Prove that a FIFO queue solves 2-thread consensus, \ and that it cannot solve 3-thread consensus.",
            r"\textit{Build.} \ Give PebbleOS \texttt{futex\_wait} and \texttt{futex\_wake}, \ and a mutex that "
            r"sleeps instead of yielding; \ compare instructions.",
            r"$\bigstar$ \textit{Research.} \ Minimum fence insertion: \ for a program and TSO or PSO, \ find the fewest "
            r"fences that restore a safety property; \ is it NP-hard for PSO? \ Solve Peterson, \ the bakery and "
            r"Dekker with the checker.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give PebbleOS the futex system calls, and a mutex that sleeps instead of yielding. The last, "
            "marked with a star, is a research problem: finding the fewest fences that make a program correct on a "
            "weak memory model, with our checker as the oracle."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 34, \ Storage", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"memory forgets when the power goes", NO),
            (r"disks and flash: \ seeks, \ erase blocks, \ write amplification", DATA),
            (r"file systems, \ and a crash between two writes", HEAD),
            (r"journals, \ logs and copy-on-write trees", YES))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"PebbleOS gets a disk and a file system", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Part 34: Storage. Memory forgets when the power goes, so data must live on spinning disks or "
            "in flash that wears out. Disks and flash, measured; file systems; and the crash that cuts an update short "
            "between two of its writes, with the journals, logs and copy-on-write trees that survive it. PebbleOS "
            "gets a disk and a file system. Part 34, Storage."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Herlihy, Shavit, Luchangco and Spear, \textit{The Art of Multiprocessor Programming} \ (2nd ed.); \ "
             r"OSTEP, \ concurrency",
             r"Downey, \textit{The Little Book of Semaphores}; \ McKenney, \textit{Is Parallel Programming Hard?}; "
             r"\ Lynch, \textit{Distributed Algorithms}",
             r"Sorin, Hill and Wood, \textit{A Primer on Memory Consistency and Cache Coherence}"],
            [r"Dijkstra \ (1965); \ Lamport \ (1974, \ 1979); \ Peterson \ (1981); \ Burns and Lynch \ (1980)",
             r"Hoare \ (1974, \ 1978); \ Lampson and Redell \ (1980); \ Coffman et al. \ (1971); \ Mellor-Crummey "
             r"and Scott \ (1991)",
             r"Adve and Hill \ (1990); \ Boehm and Adve \ (2008); \ Sewell et al., \ x86-TSO \ (2010)",
             r"Herlihy and Wing \ (1990); \ Herlihy \ (1991); \ Treiber \ (1986); \ Michael and Scott \ (1996); \ "
             r"Herlihy and Moss \ (1993)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
