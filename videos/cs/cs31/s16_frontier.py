from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, curve, fit_right, grid_table, load)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.verified()
        self.tail()
        self.quantum()
        self.ebpf()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ verified kernels and microsecond scheduling",
                            r"What is still unsolved inside the kernel?", lit=(2009, 2019, 2020),
                            extra=((2009, r"seL4 verified"), (2019, r"Shinjuku; \ Shenango"),
                                   (2020, r"Caladan; \ Jitterbug")), part=PART)
        with self.voiceover("Chapter fifteen. The frontier: verified kernels, and scheduling in microseconds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def verified(self):
        head = label(r"Kernels with proofs", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"system", r"year", r"what was proved"], [
            [r"seL4", r"2009", r"8{,}700 lines of C implement their specification: \ no crashes, \ no overflows"],
            [r"seL4, \ later", r"2011--14", r"down to the binary; \ integrity and confidentiality"],
            [r"CertiKOS", r"2016", r"a \textbf{concurrent} kernel, \ on several cores"],
            [r"Hyperkernel", r"2017", r"push-button: \ an SMT solver checks each call \ (Part 26's SAT, \ grown up)"],
        ], widths=[2.6, 1.6, 8.0], row_h=0.55, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        lines = VGroup(
            label(r"seL4's proof: \ about 200{,}000 lines of Isabelle, \ some twenty person-years \ (Klein et al., "
                  r"2009)", font_size=21, color=WHITE),
            label(r"it has flown an autonomous helicopter \ (DARPA's HACMS); \ Part 54 builds the method", font_size=21,
                  color=YES),
            label(r"open: \ a verified kernel with Linux's speed and features, \ and proof effort that scales",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.16).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "The kernel is the one program everything else trusts, so it is where proofs pay most. <bookmark "
            "mark='a'/> In 2009 a team at NICTA in Sydney proved that seL4, a microkernel of eight thousand seven "
            "hundred lines of C, implements its formal specification exactly: it cannot crash, overflow a buffer or "
            "dereference a bad pointer. Later work carried the proof down to the machine code, and proved that seL4 "
            "keeps processes' data both intact and secret. <bookmark mark='b'/> CertiKOS, in 2016, verified a kernel "
            "that runs on several cores at once. Hyperkernel, in 2017, made verification push-button, with an SMT "
            "solver checking each system call automatically. <bookmark mark='c'/> The cost is the obstacle. seL4's "
            "proof is about two hundred thousand lines, some twenty person-years of work. <bookmark mark='d'/> Still, "
            "it has flown an autonomous helicopter, in a DARPA programme where professional attackers failed to break "
            "in. <bookmark mark='e'/> The open problem is to verify a kernel "
            "with the speed and the features of Linux, with proof effort that does not grow faster than the code."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(VGroup(*tab.cells[4])))
            for mk, ln in zip("cde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def tail(self):
        d = load("frontier")
        head = label(r"Scheduling in microseconds", font_size=36).to_edge(UP, buff=0.3)
        rows = d["rows"]
        ax = Axes(x_range=[0.1, 0.8, 0.1], y_range=[-0.5, 4.0, 1], x_length=6.2, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.1).shift(DOWN * 0.3)
        xt = VGroup(*[label(f"{x:.1f}", font_size=15, color=GREY_A).next_to(ax.c2p(x, -0.5), DOWN, buff=0.08)
                      for x in (0.2, 0.4, 0.6, 0.8)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0.1, k), LEFT, buff=0.08)
                      for k in range(0, 4)])
        xl = label(r"load, \ 16 cores", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"p99.9 of the \textbf{short} requests, \ $\mu$s", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        cols = {"dfcfs": NO, "cfcfs": HEAD, "ps": YES}
        cvs = VGroup(*[curve(ax, [r["load"] for r in rows], [math.log10(max(r[k], 0.4)) for r in rows], c)
                       for k, c in cols.items()])
        r7 = next(r for r in rows if abs(r["load"] - 0.7) < 1e-9)
        notes = VGroup(
            label(r"requests: \ 99.5\% take 0.5 $\mu$s, \ 0.5\% take 500 $\mu$s \ (a key-value store's gets and "
                  r"scans)", font_size=19, color=WHITE),
            label(rf"a queue per core, \ like receive-side scaling: \ {r7['dfcfs']:,.0f} $\mu$s at 0.7".replace(",",
                                                                                                       "{,}"),
                  font_size=19, color=NO),
            label(rf"one shared queue: \ {r7['cfcfs']:.0f} $\mu$s: \ shorts still wait when 16 scans hold every core",
                  font_size=19, color=HEAD),
            label(rf"preempt every 5 $\mu$s \ (1 $\mu$s lost each time): \ {r7['ps']:.0f} $\mu$s", font_size=19,
                  color=YES),
            label(r"Shinjuku \ (2019) \ preempts at 5 $\mu$s; \ Linux's timer ticks every 1--4 \textbf{milli}seconds",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "The second frontier is speed. A data-centre service may answer requests in half a microsecond, and its "
            "users care about the slowest one in a thousand. <bookmark mark='a'/> We simulated sixteen cores serving "
            "a mix like a key-value store's: nearly all requests take half a microsecond, and one in two hundred is a "
            "scan of five hundred. <bookmark mark='b'/> With a queue per core, as network cards usually spread "
            "requests, a short request that lands behind a scan waits for it: four thousand microseconds at the "
            "ninety-ninth point nine percentile, at seventy percent load. <bookmark mark='c'/> One shared queue is "
            "much better, but when all sixteen cores happen to be busy with scans, the short requests still wait. "
            "<bookmark mark='d'/> Preempting every five microseconds, even losing one microsecond at every "
            "preemption, brings it down to ten. <bookmark mark='e'/> That is what the Shinjuku system did in 2019, "
            "with tricks from virtualisation hardware to interrupt a core that fast. Linux's timer, by comparison, "
            "ticks every one to four milliseconds."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.wait(0.1)
            for mk, c, n_ in zip("bcd", cvs, notes[1:4]):
                vo.wait_until(mk)
                self.play(Create(c), FadeIn(n_), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def quantum(self):
        d = load("frontier")
        head = label(r"But how short a quantum?", font_size=36).to_edge(UP, buff=0.3)
        qs = d["quanta"]
        ax = Axes(x_range=[0, 2.8, 0.5], y_range=[0, 3.0, 1], x_length=6.2, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.1).shift(DOWN * 0.3)
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(math.log10(x), 0), DOWN, buff=0.08)
                      for x in (1, 5, 20, 100, 500)])
        yt = VGroup(*[MathTex(rf"10^{{{k}}}", font_size=18, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.08)
                      for k in range(0, 4)])
        xl = label(r"quantum, \ $\mu$s \ (load 0.6, \ 1 $\mu$s per preemption)", font_size=17, color=GREY_A).next_to(
            xt, DOWN, buff=0.1)
        cv = curve(ax, [math.log10(q["q"]) for q in qs], [math.log10(q["p999"]) for q in qs], YES)
        lc = curve(ax, [math.log10(q["q"]) for q in qs], [math.log10(q["long_mean"] / 10) for q in qs], NO)
        k1 = label(r"shorts' p99.9", font_size=17, color=YES).move_to(ax.c2p(2.2, 2.4))
        k2 = label(r"scans' mean $\div$ 10", font_size=17, color=NO).move_to(ax.c2p(0.9, 2.75))
        best = min(qs, key=lambda q: q["p999"])
        notes = VGroup(
            label(r"too long: \ shorts wait behind scans", font_size=20, color=WHITE),
            label(rf"too short: \ the overhead eats the cores; \ at 1 $\mu$s the scans take "
                  rf"{qs[0]['long_mean'] / 1000:.1f} ms", font_size=20, color=NO),
            label(rf"best here: \ about {best['q']} $\mu$s", font_size=20, color=HEAD),
            label(r"no formula gives it: \ even the mean of M/G/$k$ has no exact closed form", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "How short should the quantum be? <bookmark mark='a'/> Too long, and short requests wait behind scans. "
            "<bookmark mark='b'/> Too short, and the cost of preempting eats the cores. At one microsecond, the scans "
            "spend as long being preempted as running, the machine is overloaded, and a scan takes seven and a half "
            "milliseconds. <bookmark mark='c'/> "
            "Here the best quantum is about two microseconds. <bookmark mark='d'/> But no formula tells us that. "
            "Even the mean response time of a queue with several servers and general job sizes has no exact closed "
            "form, so these choices are made by simulation and by trial."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl))
            self.play(Create(cv), Create(lc), FadeIn(k1), FadeIn(k2), run_time=1.5)
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def ebpf(self):
        head = label(r"Programs inside the kernel: \ eBPF", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (r"1. \ a user writes a small program: \ count system calls, \ filter packets, \ enforce a policy", WHITE),
            (r"2. \ the kernel's \textbf{verifier} checks it: \ every path ends, \ every memory access in bounds", YES),
            (r"3. \ a JIT compiles it to machine code \ (Part 15), \ and the kernel runs it on events", HEAD),
            (r"used by \texttt{bpftrace}, \ Cilium's networking, \ Android, \ Meta's load balancers", GREY_A),
            (r"the risk: \ verifier and JIT bugs became kernel exploits", NO),
            (r"research: \ PREVAIL \ (2019, \ abstract interpretation); \ Jitterbug \ (2020, \ verified JITs); \ "
             r"Agni \ (2023, \ the range analysis checked)", LAM),
        )]).arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(head, DOWN, buff=0.55)
        fit_right(steps)
        with self.voiceover(
            "The third frontier changes what a kernel is. eBPF lets an ordinary user load small programs into the "
            "running Linux kernel. <bookmark mark='a'/> Count system calls, filter network packets, enforce a "
            "security policy. <bookmark mark='b'/> Before running anything, the kernel's verifier checks that every "
            "path through the program ends, and that every memory access stays in bounds: the halting problem of "
            "Part 25, avoided by allowing only programs simple enough to check. <bookmark mark='c'/> Then a "
            "just-in-time compiler turns it into machine code, and the kernel runs it whenever its event occurs. "
            "<bookmark mark='d'/> It now traces production systems and routes packets for large websites. <bookmark "
            "mark='e'/> But the verifier and the compilers are themselves complicated code, and their bugs have "
            "become ways to take over the kernel. <bookmark mark='f'/> So researchers are verifying the verifier: "
            "with abstract interpretation in PREVAIL, with proofs of the just-in-time compilers in Jitterbug, and "
            "by machine-checking the verifier's arithmetic on ranges in Agni."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=36).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ Can a formally verified kernel match Linux's performance and breadth?", font_size=22,
                  color=WHITE),
            label(r"2. \ Exact response times for M/G/$k$: \ several servers, \ general job sizes", font_size=22,
                  color=WHITE),
            label(r"3. \ Optimal scheduling for tail latency, \ on many cores, \ when preemption costs time",
                  font_size=22, color=WHITE),
            label(r"4. \ Worst-case timing on multicore chips, \ where caches and memory are shared", font_size=22,
                  color=WHITE),
            label(r"5. \ How expressive can a sound eBPF verifier be, \ and still be fast?", font_size=22,
                  color=WHITE),
            label(r"6. \ Scheduling without knowing job sizes: \ how close to SRPT?", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        star = label(r"$\bigstar$ \ the part's research problem takes a small case of the third", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Six open problems. <bookmark mark='a'/> Whether a verified kernel can have the performance and breadth "
            "of Linux. <bookmark mark='b'/> Exact response times for a queue with several servers and general job "
            "sizes, which queueing theory still lacks. <bookmark mark='c'/> The best schedule for tail latency on "
            "many cores, when every preemption costs time. <bookmark mark='d'/> Worst-case timing on multicore "
            "chips, where one core's memory traffic slows another, which is what blocks multicore processors in "
            "safety-critical systems. <bookmark mark='e'/> How much an eBPF verifier can accept while staying sound "
            "and fast. <bookmark mark='f'/> And how close a scheduler that does not know job sizes can come to "
            "shortest remaining time first; Mor Harchol-Balter's group has made progress with the Gittins index. "
            "<bookmark mark='g'/> This part's research problem takes a small, computable case of the third."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
