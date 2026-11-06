from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs32.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ Virtual Memory", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\textsf{VPN} \,|\, \textsf{offset}", font_size=48, color=DATA), r"paging; \ the walk", DATA),
            tile(MathTex(r"\textsf{TLB}: 63 \text{ misses}", font_size=44, color=YES), r"translation, \ cached", YES),
            tile(MathTex(r"\textsf{OPT} \le \textsf{LRU}", font_size=48, color=LAM), r"replacement; \ Belady", LAM),
            tile(MathTex(r"\textsf{fork} \to \textsf{copy on write}", font_size=40, color=HEAD), r"sharing pages",
                 HEAD),
            tile(MathTex(r"(n+1)(m+1)-1", font_size=48, color=KERN), r"virtual machines", KERN),
            tile(MathTex(r"\textsf{pid } 1,\ \textsf{uid } 0", font_size=44, color=NO), r"containers", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Address translation, from Atlas to the four-level radix tree, and a TLB "
            "that makes it nearly free. Page faults, demand paging, and Belady's optimum, his anomaly, and the stack "
            "property that rules it out for LRU. Working sets, thrashing, copy-on-write, and the allocators the "
            "kernel uses for itself. Virtual machines, from Popek and Goldberg to the nested walk, and containers. "
            "And PebbleOS, with an MMU, running every process at the same addresses."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"threads share one address space: \ races, \ and TLB shootdowns", [33]),
            (r"the page cache, \ mmap'd files, \ and a disk under PebbleOS", [34]),
            (r"buffer pools: \ a database's own replacement policy", [35]),
            (r"microVMs, \ containers and Kubernetes", [45]),
            (r"caching at scale: \ LRU and Che's approximation", [48]),
            (r"memory-safety attacks, \ and ASLR", [55]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. In Part 33, threads share one address space, which brings races, and the TLB "
            "shootdowns we just met. Part 34 adds a disk to PebbleOS, with a page cache and memory-mapped files. Part "
            "35's databases keep their own buffer pool, with their own replacement policy. Part 45 builds the cloud "
            "from microVMs and containers. Part 48 meets LRU again, as caches in front of services. And Part 55 "
            "attacks memory safety, and the address-space randomisation that defends it."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"observe", r"\texttt{/proc/<pid>/smaps}, \ \texttt{vmstat}, \ \texttt{perf stat -e dTLB-load-misses}"),
            (r"huge pages", r"databases and JVMs: \ explicit 2 MiB pages; \ watch transparent huge pages' latency spikes"),
            (r"out of memory", r"the OOM killer's choice is in \texttt{dmesg}; \ set cgroup \texttt{memory.max}, \ not "
                               r"just swap"),
            (r"fork", r"a big parent's fork copies its tables; \ prefer \texttt{posix\_spawn}, \ or fork early"),
            (r"isolation", r"containers share a kernel: \ untrusted code gets a VM \ (Firecracker, \ gVisor)"),
        ])
        with self.voiceover(
            "In practice. Look before you tune: the smaps file of a process, vmstat, and perf's count of TLB misses. "
            "Databases and Java virtual machines usually want explicit huge pages, and transparent huge pages can "
            "cause latency spikes while the kernel compacts memory. When a process vanishes, the out-of-memory "
            "killer's reasons are in the kernel log; put limits on control groups rather than relying on swap. A "
            "large process's fork copies its page tables, so spawn helpers early, or use posix-spawn. And remember "
            "that containers share one kernel: untrusted code belongs in a virtual machine."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove by an exchange argument that Belady's OPT \ (evict the page used farthest in the future) \ "
            r"minimises faults.",
            r"Prove that LRU has the stack property, \ so it has no anomaly; \ show that FIFO's three- and four-frame "
            r"contents are not nested.",
            r"Derive $(n+1)(m+1) - 1$ for the nested walk, \ and the count when a walk cache holds every upper level "
            r"of both tables.",
            r"Show that a buddy block is always more than half used, \ and find the expected waste for request sizes "
            r"uniform on $1..2^k$.",
            r"\textit{Build.} \ Give PebbleOS a copy-on-write \texttt{fork}: \ share frames read-only, \ copy on the "
            r"store fault, \ count the copies.",
            r"$\bigstar$ \textit{Research.} \ Offline huge-page promotion: \ given a trace, \ a TLB of $k$ entries and a "
            r"budget of wasted frames, \ choose the aligned regions to promote. \ Is it NP-hard? \ How close is greedy on "
            r"the Job's trace?",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give PebbleOS a copy-on-write fork. The last, marked with a star, is a research problem: "
            "deciding, with hindsight, which regions deserve huge pages within a budget of wasted memory, the "
            "offline version of the question Ingens and HawkEye answer by heuristics."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 33, \ Concurrency", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"two threads add one to a counter, \ and it goes up by one", NO),
            (r"Peterson's lock, \ proved, \ and broken by the hardware", YES),
            (r"locks, \ semaphores, \ monitors, \ deadlock", HEAD),
            (r"memory models, \ and the hierarchy of atomic operations", LAM))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"threads share everything this part kept apart", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Part 33: Concurrency. Two threads each add one to a counter, and the count goes up by one. "
            "Peterson's lock, proved correct, and then broken by the hardware's reordering; locks, semaphores, "
            "monitors and deadlock; and the theory of memory models and of which atomic operations can build which. "
            "Threads share everything this part worked to keep apart. Part 33, Concurrency."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Arpaci-Dusseau and Arpaci-Dusseau, \textit{Operating Systems: Three Easy Pieces} \ (memory "
             r"virtualization); \ Tanenbaum and Bos, ch.~3",
             r"Gorman, \textit{Understanding the Linux Virtual Memory Manager}; \ Bhattacharjee and Lustig, "
             r"\textit{Architectural Support for Virtual Memory}",
             r"Denning, \ ``Virtual memory'' \ (1970); \ Smith and Nair, \textit{Virtual Machines}"],
            [r"Kilburn et al. \ (1962); \ Belady \ (1966); \ Belady, Nelson and Shedler \ (1969); \ Mattson et al. "
             r"\ (1970)",
             r"Denning \ (1968); \ Sleator and Tarjan \ (1985); \ Knowlton \ (1965); \ Bonwick \ (1994); \ Megiddo and "
             r"Modha, \ ARC \ (2003)",
             r"Popek and Goldberg \ (1974); \ Adams and Agesen \ (2006); \ Bhargava et al. \ (2008); \ Lipp et al., "
             r"\ Meltdown \ (2018)",
             r"Basu et al. \ (2013); \ Maruf et al., \ TPP \ (2023); \ Simner et al. \ (2022)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
