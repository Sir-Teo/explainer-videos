from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, CTRL, DATA, HEAD, KERN, LAM, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ The Kernel", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\textsf{ecall}\;/\;\textsf{eret}", font_size=48, color=KERN), r"the mode bit; \ traps",
                 KERN),
            tile(MathTex(r"\textsf{ready} \rightleftarrows \textsf{running}", font_size=44, color=YES),
                 r"processes; \ switches", YES),
            tile(MathTex(r"\textsf{fork} + \textsf{exec}", font_size=48, color=DATA), r"the shell; \ pipes", DATA),
            tile(MathTex(r"\textsf{SJF}, \textsf{MLFQ}, \textsf{CFS}", font_size=44, color=HEAD), r"scheduling",
                 HEAD),
            tile(MathTex(r"U \le n(2^{1/n} - 1)", font_size=48, color=LAM), r"real time", LAM),
            tile(MathTex(r"W = \frac{1}{\mu - \lambda}", font_size=52, color=NO), r"queueing", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Time-sharing, from CTSS to Linux. A mode bit, traps and a timer for Pebble, "
            "and a kernel that uses them. Processes, context switches, and fork, exec and a shell, measured on this "
            "machine. Schedulers from first come first served to MLFQ, lottery, stride and Linux's own, with the "
            "proof that shortest first is optimal. Rate monotonic and earliest deadline first, and a bug on Mars. "
            "And queueing theory: Little's law, the hockey stick, and why variance and order matter."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"virtual memory, \ copy-on-write fork, \ hypervisors", [32]),
            (r"preemption makes races: \ locks and the kernel", [33]),
            (r"disk interrupts; \ a file system on PebbleOS", [34]),
            (r"work in progress is a queue: \ Little's law for teams", [40]),
            (r"backpressure and load shedding between services", [43]),
            (r"Erlang C and capacity planning; \ off-CPU time and eBPF", [45, 50]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 32 gives every process its own addresses, which makes fork cheap and lets "
            "one machine pretend to be several. Part 33 deals with the races that preemption creates. Part 34 adds a "
            "disk, its interrupts and a file system to PebbleOS. Part 40 applies Little's law to work in progress, "
            "and Part 43 to queues between services. And Parts 45 and 50 plan capacity with queueing theory, and "
            "find where time goes with eBPF."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"observe", r"\texttt{strace -c}, \ \texttt{perf}, \ \texttt{bpftrace}: \ count calls before you optimise"),
            (r"system calls", r"batch them: \ big buffers, \ \texttt{io\_uring}; \ the vDSO for clocks"),
            (r"processes", r"\texttt{posix\_spawn} over fork in big programs; \ pin latency-critical threads"),
            (r"scheduling", r"\texttt{nice} and cgroup weights are CFS shares; \ real-time classes need a budget"),
            (r"capacity", r"keep utilisation near 50--70\%; \ watch the p99, \ not the mean"),
        ])
        with self.voiceover(
            "In practice. Before optimising, count the system calls with strace, perf or bpftrace. Batch them, with "
            "big buffers or Linux's io-uring, and let the vDSO answer the clock. Prefer posix-spawn to fork in large "
            "programs, and pin latency-critical threads to cores. Remember that nice values and control-group "
            "weights are just shares in the fair scheduler. And plan servers to run at fifty to seventy percent, "
            "watching the ninety-ninth percentile, not the mean."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove by an exchange argument that SRPT minimises the mean response time for jobs arriving over time, "
            r"on one server.",
            r"Derive Liu and Layland's bound for two tasks, \ $2(\sqrt{2} - 1)$, \ by finding the worst period ratio "
            r"and work split.",
            r"For M/M/1, \ show that the response time is exponential with rate $\mu - \lambda$, \ and find its 99th "
            r"percentile.",
            r"Show that a job that yields just before its quantum ends keeps the top queue under the old MLFQ rule, "
            r"\ and bound its share.",
            r"\textit{Build.} \ Add \texttt{sleep(n)} and a stride scheduler to PebbleOS, \ and show two processes "
            r"sharing 3 to 1.",
            r"$\bigstar$ \textit{Research.} \ For $k$ servers, \ bimodal sizes and preemption overhead $\delta$, "
            r"\ find the quantum that minimises the shorts' p99.9, \ and how it scales with $\delta$ and load.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give PebbleOS a sleep call and a stride scheduler. The last, marked with a star, is a research "
            "problem: how short the quantum should be when preemption costs time, which the microsecond schedulers "
            "of the frontier chapter set by trial."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 32, \ Virtual Memory", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"every process believes it owns a huge, \ private memory", DATA),
            (r"page tables, \ the TLB, \ and page faults", YES),
            (r"which page to evict: \ Belady's optimum and his anomaly", LAM),
            (r"virtual machines and containers", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"PebbleOS gains an MMU: \ two processes at the same address", font_size=26,
                  color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Part 32: Virtual Memory. Every process believes it owns a huge, private, contiguous memory, "
            "and none of them does. Page tables, the translation cache that makes them fast, and page faults; which "
            "page to throw out when memory is full, and the surprise that more memory can mean more faults; and the "
            "virtual machines and containers built on top. PebbleOS gains an MMU. Part 32, Virtual Memory."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Arpaci-Dusseau and Arpaci-Dusseau, \textit{Operating Systems: Three Easy Pieces}; \ Tanenbaum and Bos, "
             r"\textit{Modern Operating Systems}",
             r"Anderson and Dahlin, \textit{Operating Systems: Principles and Practice}; \ Cox, Kaashoek and Morris, "
             r"\textit{xv6}",
             r"Harchol-Balter, \textit{Performance Modeling and Design of Computer Systems}; \ Kleinrock, "
             r"\textit{Queueing Systems}"],
            [r"Corbat\'o, Merwin-Daggett and Daley (1962); \ Ritchie and Thompson (1974); \ Liu and Layland (1973)",
             r"Little (1961); \ Schrage (1968); \ Waldspurger and Weihl (1994); \ Blumofe and Leiserson (1999)",
             r"Sha, Rajkumar and Lehoczky (1990); \ Liedtke (1995); \ Engler et al. (1995); \ Klein et al. (2009)",
             r"Baumann et al. (2019); \ Kaffes et al., Shinjuku (2019); \ Gershuni et al., PREVAIL (2019)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
