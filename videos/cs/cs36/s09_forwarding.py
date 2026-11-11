from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs36.common import (CODE, DATA, HEAD, IPC, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load,
                                   mono, num)


class Forwarding(VoiceoverScene):
    def construct(self):
        self.card()
        self.lpm()
        self.tries()
        self.speed()
        self.fabric()

    def card(self):
        card = chapter_card(8, r"Forwarding", r"Which way, \ in a nanosecond?", lit=(1997, 1998),
                            extra=((1997, r"Degermark et al.: \ small forwarding tables"),
                                   (1998, r"Srinivasan and Varghese: \ multibit tries")), part=PART)
        with self.voiceover("Chapter eight. Forwarding."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lpm(self):
        head = label(r"Longest-prefix match", font_size=36).to_edge(UP, buff=0.3)
        rows = [["0.0.0.0/0", "upstream"], ["10.0.0.0/8", "port 1"], ["10.4.0.0/16", "port 3"],
                ["10.4.0.0/24", "port 7"], ["10.7.0.0/16", "port 2"]]
        tab = grid_table([r"prefix", r"next hop"], rows, widths=[3.0, 2.4], row_h=0.44, font_size=20, mono_cols=(0, 1))
        tab.next_to(head, DOWN, buff=0.5).shift(LEFT * 3)
        q = VGroup(label(r"packet for", font_size=20, color=GREY_A), mono("10.4.0.2", 24, IPC)).arrange(RIGHT, buff=0.2)
        q.next_to(tab, RIGHT, buff=1.2).align_to(tab, UP)
        matches = label(r"four prefixes contain it: \ \texttt{/0}, \ \texttt{/8}, \ \texttt{/16}, \ \texttt{/24}",
                        font_size=20, color=WHITE).next_to(q, DOWN, buff=0.4).align_to(q, LEFT)
        win = label(r"the longest, \ \texttt{/24}, \ wins: \ port 7", font_size=22, color=YES).next_to(matches, DOWN,
                                                                                                    buff=0.25).align_to(
            q, LEFT)
        lines = VGroup(
            label(r"a more specific route overrides a general one: \ that is how CIDR's aggregation and its "
                  r"exceptions coexist", font_size=20, color=HEAD),
            label(r"\texttt{0.0.0.0/0}, \ the \textbf{default route}: \ if nothing else matches, \ send it upstream",
                  font_size=20, color=GREY_A),
            label(r"a core router's table today: \ about a million IPv4 prefixes, \ consulted for every packet",
                  font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A router's forwarding table maps prefixes to next hops. <bookmark mark='a'/> A packet arrives for ten "
            "dot four dot zero dot two. <bookmark mark='b'/> Four entries contain it, from the default route, which "
            "contains everything, to a slash twenty-four. <bookmark mark='c'/> The rule is that the longest "
            "matching prefix wins, so it leaves on port seven. <bookmark mark='d'/> That rule is what lets a provider "
            "announce one large aggregate and still route a few exceptions differently. <bookmark mark='e'/> The "
            "difficulty is size. A router in the core of the Internet holds about a million IPv4 prefixes and must "
            "search them for every packet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(matches), *[Indicate(tab.cells[r][0], color=HEAD) for r in (1, 2, 3, 4)])
            vo.wait_until("c")
            self.play(FadeIn(win), tab.cells[4][1].animate.set_color(YES))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def tries(self):
        lp = load("lpm")
        head = label(r"Tries, \ counted", font_size=36).to_edge(UP, buff=0.3)
        names = ["linear", "binary trie", "multibit, stride 4", "multibit, stride 8"]
        rows = []
        for n in names:
            t = lp["tables"][n]
            rows.append([n, f"{t['steps']:.1f}", f"{t['us']:.1f}" if t["us"] < 1000 else f"{t['us'] / 1000:.1f} ms",
                         num(t["nodes"])])
        rows[0][2] = f"{lp['tables']['linear']['us'] / 1000:.0f} ms"
        for r in rows[1:]:
            r[2] = r[2] + r" $\mu$s"
        tab = grid_table([rf"{num(lp['prefixes'])} prefixes", r"memory reads per lookup", r"Python, \ per lookup",
                          r"nodes"], rows, widths=[3.4, 3.0, 2.6, 1.8], row_h=0.44, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for r in range(2, 5):
            tab.cells[r][1].set_color(YES)
        tab.cells[1][1].set_color(NO)
        lines = VGroup(
            label(r"\textbf{binary trie}: \ follow the address one bit at a time, \ remembering the last prefix "
                  r"passed: \ about 21 steps", font_size=20, color=WHITE),
            label(r"\textbf{multibit}: \ eight bits a step, \ expanding short prefixes to fill the stride: \ under 3 "
                  r"reads, \ for more memory per node", font_size=20, color=YES),
            label(r"all four answer identically on 1{,}000 test addresses; \ the trade is memory against reads",
                  font_size=20, color=HEAD),
            label(r"prefix lengths in our table: \ 62\% are /24, \ as in the real Internet's", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.4)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "We built a table of a hundred thousand prefixes with the real Internet's mix of lengths, and searched "
            "it four ways. <bookmark mark='a'/> Checking every prefix is hopeless: a hundred thousand comparisons, "
            "thirty milliseconds in Python. <bookmark mark='b'/> The binary trie of Part 17 follows the address one "
            "bit at a time down a tree of prefixes, remembering the last next hop it passed: about twenty-one memory "
            "reads. <bookmark mark='c'/> A multibit trie takes eight bits at each step, expanding short prefixes so "
            "that every slot of a node is filled: under three reads, at the cost of more memory per node. "
            "<bookmark mark='d'/> All four give the same answer for every address we tried. The design choice is how "
            "much memory to spend to save reads."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]),
                      FadeIn(tab.cells[0][3]), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in tab.cells[1]])
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in tab.cells[2]], FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in tab.cells[3] + tab.cells[4]], FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]), FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def speed(self):
        lp = load("lpm")
        head = label(r"A nanosecond and a half", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"\frac{400 \times 10^9 \ \text{bits/s}}{(64 + 20) \times 8 \ \text{bits}} \approx "
                     rf"{lp['pps_400g'] / 1e6:.0f} \times 10^6 \ \text{{packets/s}}", font_size=36, color=WHITE)
        eq.next_to(head, DOWN, buff=0.6)
        per = MathTex(rf"\Rightarrow \ {lp['ns_per_packet']:.2f} \ \text{{ns per packet, per port}}", font_size=38,
                      color=NO).next_to(eq, DOWN, buff=0.35)
        lines = VGroup(
            label(r"a DRAM access takes about 50 ns \ (Part 9): \ thirty packets arrive while one read completes",
                  font_size=20, color=NO),
            label(r"\textbf{TCAM}: \ memory that compares a key with \textit{every} entry at once, \ with don't-care "
                  r"bits, \ and returns the first match", font_size=20, color=YES),
            label(r"sort entries longest-first, \ and the first match is the longest prefix: \ one lookup per clock",
                  font_size=20, color=HEAD),
            label(r"the price: \ power and area; \ so routers also use compressed tries in SRAM, \ and pipeline the "
                  r"steps", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(per, DOWN, buff=0.6)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "How fast must this be? <bookmark mark='a'/> A port at four hundred gigabits a second receives a "
            "minimum-size packet, sixty-four bytes plus twenty of preamble and gap, every one point seven "
            "nanoseconds. <bookmark mark='b'/> A read from DRAM takes about fifty: thirty packets arrive while one "
            "memory access completes. Software cannot keep up. <bookmark mark='c'/> So routers use a special memory, "
            "the ternary content-addressable memory, which compares a key against every entry in parallel, with "
            "don't-care bits, and reports the first match. <bookmark mark='d'/> Store the prefixes longest first, and "
            "the first match is the longest match: one lookup every clock cycle. <bookmark mark='e'/> TCAMs are "
            "power-hungry, so routers also pipeline compressed tries in fast on-chip memory. Forwarding is "
            "algorithms and hardware designed together."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(FadeIn(per), FadeIn(lines[0]))
            for mk, ln in zip("cde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


    def fabric(self):
        h = load("hol")
        head = label(r"Inside the router: \ head-of-line blocking", font_size=34).to_edge(UP, buff=0.3)
        rows = [[str(r["N"]), f"{r['fifo']:.3f}", f"{r['voq']:.3f}"] for r in h["rows"]]
        tab = grid_table([r"ports $N$", r"FIFO inputs", r"virtual output queues"], rows, widths=[1.8, 2.4, 3.4],
                         row_h=0.42, font_size=19, mono_cols=())
        tab.move_to([-3.2, 0.5, 0])
        for r in range(1, len(rows) + 1):
            tab.cells[r][1].set_color(NO)
            tab.cells[r][2].set_color(YES)
        lim = MathTex(rf"N \to \infty: \quad 2 - \sqrt{{2}} \approx {h['limit']:.3f}", font_size=30, color=NO)
        lim.next_to(tab, DOWN, buff=0.35)
        lines = VGroup(
            wrapped_label(r"a router is many line cards joined by a \textbf{switching fabric}; \ each slot, \ every input "
                          r"may send one cell to one output", 6.4, font_size=19, color=WHITE),
            wrapped_label(r"with one FIFO per input, \ a cell waiting for a busy output blocks the cells behind it, \ "
                          r"even those for idle outputs", 6.4, font_size=19, color=NO),
            wrapped_label(r"Karol, \ Hluchyj and Morgan \ (1987): \ saturated throughput falls to 58.6\%", 6.4,
                          font_size=19, color=HEAD),
            wrapped_label(r"the cure: \ a queue per output at each input, \ and a matching each slot \ (McKeown's iSLIP, "
                          r"\ 1999): \ 100\%", 6.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.5, 0.2, 0])
        with self.voiceover(
            "A fast lookup is only half of a router. <bookmark mark='a'/> The other half is the switching fabric that "
            "joins its line cards: in each time slot, every input may send one cell to one output. "
            "<bookmark mark='b'/> If each input keeps a single queue, a cell whose output is busy blocks every cell "
            "behind it, even cells for outputs sitting idle. <bookmark mark='c'/> We simulated saturated switches. Two "
            "ports deliver seventy-five percent; as the switch grows, throughput falls towards two minus the square "
            "root of two, fifty-eight point six percent, the limit Karol, Hluchyj and Morgan derived in 1987. "
            "<bookmark mark='d'/> The cure is a separate queue at each input for each output, and a matching computed "
            "every slot between inputs and outputs, as Nick McKeown's iSLIP does. Then the fabric runs at full rate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lim), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()


_ = (CODE, DATA, KERN, bar_chart)
