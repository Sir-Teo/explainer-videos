from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, box, fmt,
                                  load, mono)

VICTIM = ["victim: lw   t2, 0(s1)       # array1_size",
          "        bgeu a0, t2, out     # the bounds check: x < size?",
          "        add  t3, s0, a0",
          "        lbu  t3, 0(t3)       # array1[x]",
          "        slli t3, t3, 6",
          "        add  t3, t3, s2",
          "        lbu  t3, 0(t3)       # probe[array1[x] * 64]",
          "out:    ret"]


class Spectre(VoiceoverScene):
    def construct(self):
        self.card()
        self.channel()
        self.gadget()
        self.attack()
        self.probe()
        self.mitigate()
        self.world()

    def card(self):
        card = chapter_card(9, r"Spectre", "Can squashed execution leave a cache trace?", lit=(2014, 2018),
                            extra=((2014, r"Flush+Reload"), (2018, r"Spectre and Meltdown")), part=PART)
        with self.voiceover("Chapter nine. Spectre."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def channel(self):
        head = label(r"A cache remembers what was touched", font_size=36).to_edge(UP, buff=0.35)
        n = 16
        lines = VGroup(*[Rectangle(width=0.6, height=0.6, stroke_color=GREY_C, stroke_width=1.5) for _ in range(n)])
        lines.arrange(RIGHT, buff=0.08).move_to(UP * 1.0)
        idx = VGroup(*[label(str(k), font_size=16, color=GREY_B).next_to(l, DOWN, buff=0.08) for k, l in
                       enumerate(lines)])
        cap = note(r"a probe array: \ 256 cache lines, \ one per possible byte \ (16 shown)", font_size=20).next_to(
            lines, UP, buff=0.2)
        hot = lines[11].copy().set_fill(YES, opacity=0.8).set_stroke(YES)
        times = VGroup()
        for k, l in enumerate(lines):
            t = 2 if k == 11 else 60
            times.add(label(str(t), font_size=18, color=YES if k == 11 else NO).next_to(idx[k], DOWN, buff=0.25))
        tl = note(r"cycles to read each line", font_size=20).next_to(times, DOWN, buff=0.15)
        facts = VGroup(
            label(r"1. \ flush every line \quad 2. \ let the victim run \quad 3. \ time a read of every line",
                  font_size=24, color=GREY_A),
            label(r"the fast one is the line the victim touched: \ Flush+Reload \ (Yarom and Falkner, 2014)",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "We will demonstrate a cache timing channel entirely inside the functional simulator. The victim and "
            "observer share its byte-array memory and a probe array. The observer can evict and time probe lines "
            "using model devices. <bookmark mark='a'/> Allocate two hundred fifty-six probe lines, one for each "
            "possible byte value. The diagram shows sixteen of them. <bookmark mark='b'/> A victim access leaves "
            "its selected line in the modeled cache. Access assigns a two-cycle hit or sixty-cycle miss and "
            "allocates a missed line immediately; it is a simplified cache model. <bookmark mark='c'/> Timing later "
            "accesses distinguishes a warm line from cold ones; the measured interval includes the timer and "
            "surrounding instructions. <bookmark mark='d'/> Flush-and-reload-style attacks exploit this kind of "
            "observable shared state on suitable hardware. Our demonstration supplies those sharing and timing "
            "assumptions explicitly and does not extract secrets from the host processor."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.05), FadeIn(idx))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(hot))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in times], lag_ratio=0.05), FadeIn(tl))
            vo.wait_until("d")
            self.play(FadeIn(facts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gadget(self):
        head = label(r"The victim: \ a bounds check", font_size=36).to_edge(UP, buff=0.3)
        c = VGroup(mono("if (x < array1_size)", 24), mono("    y = probe[array1[x] * 64];", 24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to(UP * 2.0)
        code = VGroup(*[mono(s, 19) for s in VICTIM]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(c, DOWN,
                                                                                                    buff=0.45)
        mem = VGroup()
        cells = ["0"] * 4 + ["…"] + ["0"] * 2 + ["P", "E", "B", "B", "L", "E"]
        for k, t in enumerate(cells):
            r = Rectangle(width=0.5, height=0.5, stroke_color=INF if k < 7 else NO, stroke_width=1.5)
            mem.add(VGroup(r, Text(t, font="DejaVu Sans Mono", font_size=16, color=GREY_A if k < 7 else NO).move_to(r)))
        mem.arrange(RIGHT, buff=0.03).to_edge(DOWN, buff=0.9)
        b1 = Brace(mem[:7], DOWN, color=INF)
        l1 = label(r"array1: \ 16 bytes", font_size=20, color=INF).next_to(b1, DOWN, buff=0.08)
        b2 = Brace(mem[7:], DOWN, color=NO)
        l2 = label(r"a secret, \ just past the end", font_size=20, color=NO).next_to(b2, DOWN, buff=0.08)
        with self.voiceover(
            "The victim interface accepts an unsigned word-sized index and a nonempty sixteen-byte array. <bookmark "
            "mark='a'/> On architectural execution, the unsigned bounds check rejects indices at or above the array "
            "size. An accepted byte selects one probe line. <bookmark mark='b'/> The assembly uses an unsigned "
            "branch, then loads the byte and shifts it by six to select a sixty-four-byte line. The adjacent secret "
            "is outside the victim interface's permitted array, but inside the same modeled address space. This is "
            "a software bounds policy, not a hardware page-permission boundary. <bookmark mark='c'/> The secret "
            "bytes spell PEBBLE and begin at index sixteen. Correct architectural control flow rejects those "
            "indices. The experiment asks whether transient execution can nevertheless encode their values in the "
            "simulated cache."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(c))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in code], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(mem), FadeIn(b1), FadeIn(l1), FadeIn(b2), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attack(self):
        head = label("The attack in the simulated core/cache", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            label("1. \\ flush probes, then train six in-bounds calls; \\ line 0 becomes warm", font_size=24, color=DATA),
            label("2. \\ evict \\texttt{array1\\_size}, \\ then execute the model timer barrier", font_size=24,
                  color=INF),
            label(r"3. \ call it with x = 16, \ 17, \ \dots: \ past the end", font_size=24, color=NO),
            label("4. \\ time probe lines 1 to 255; \\ omit training-warmed line 0", font_size=24, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(UL, buff=0.45).shift(DOWN * 0.5)
        # a schematic of step 3, from the core's behaviour
        x0, y0, cw = -2.2, -1.2, 0.075
        bars = VGroup()
        rows = [(r"\texttt{lw t2, size}", 0, 60, INF, r"a miss: \ 60 cycles"),
                (r"\texttt{bgeu}: \ guessed \textit{in bounds}", 60, 61, NO, r""),
                (r"\texttt{lbu}: \ array1[16] = `P'", 3, 5, CTRL, r""),
                (r"\texttt{lbu}: \ probe[`P' $\times$ 64]", 7, 67, CTRL, r"fills a cache line"),
                (r"check resolves: \ squash", 61, 62, NO, r"")]
        for k, (nm, a, b, col, side) in enumerate(rows):
            y = y0 - k * 0.48
            lab = label(nm, font_size=19, color=GREY_A).move_to([x0 - 0.2, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=(b - a) * cw, height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.8)
            bar.move_to([x0 + a * cw + (b - a) * cw / 2, y, 0])
            s = label(side, font_size=17, color=col).next_to(bar, UP, buff=0.04).align_to(bar, RIGHT) if side else \
                VectorizedPoint()
            bars.add(VGroup(lab, bar, s))
        bars.shift(RIGHT * 2.2)
        squash = DashedLine([x0 + 2.2 + 61 * cw, y0 + 0.4, 0], [x0 + 2.2 + 61 * cw, y0 - 2.3, 0], color=NO)
        after = label("younger architectural results are squashed; \\\\ the transient access leaves a modeled cache effect",
                      font_size=22, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Follow the actual program order in the simulated attack. <bookmark mark='a'/> First flush all probe "
            "lines, then make six in-bounds training calls. The allowed array contains zeros, so those calls warm "
            "probe line zero. <bookmark mark='b'/> Next evict the size variable and execute the model's timer "
            "barrier before the attack call. The next bounds check must wait for the modeled miss. <bookmark "
            "mark='c'/> Call with index sixteen, then successive secret positions. Prediction follows the in-bounds "
            "path while the size is delayed. A transient byte load reads P and a dependent access selects its probe "
            "line. The timing diagram illustrates that overlap; it is not a gate-level timing trace. <bookmark "
            "mark='d'/> Once the size arrives, the branch rejects the index and squashes younger architectural "
            "results. The selected probe line remains warm in this model. That observable cache effect is exactly "
            "why saying the access never happened would be wrong."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("ab", steps[:2]):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
            self.play(FadeIn(bars[0]))
            self.play(FadeIn(bars[2]), FadeIn(bars[3]))
            vo.wait_until("d")
            self.play(FadeIn(bars[1]), FadeIn(bars[4]), Create(squash))
            self.play(FadeIn(after), FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def probe(self):
        d = load("spectre")
        head = label("Step 4: \\ time lines 1 to 255; \\ training warmed line 0", font_size=36).to_edge(UP, buff=0.3)
        r = d["rounds"][0]
        ax = Axes(x_range=[0, 256, 32], y_range=[0, 70, 20], x_length=11.5, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(UP * 0.2)
        ax.y_axis.add_numbers([0, 20, 40, 60], font_size=16, num_decimal_places=0)
        bars = VMobject(color=NO, stroke_width=2.5).set_points_as_corners([ax.c2p(k + 1, v) for k, v in enumerate(r)])
        k = int(np.argmin(r)) + 1
        dip = Dot(ax.c2p(k, min(r)), radius=0.1, color=YES)
        tag = label(rf"line {k} \ = \ `{chr(k)}': \ {min(r)} cycles", font_size=24, color=YES).next_to(
            ax.c2p(k, 30), RIGHT, buff=0.2)
        xl = note(r"probe line \ (a byte value)", font_size=20).next_to(ax, DOWN, buff=0.15)
        yl = note(r"cycles to read it", font_size=20).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        out = d["leaked"]
        letters = VGroup(*[Text(ch, font="DejaVu Sans Mono", font_size=40, color=NO) for ch in out]).arrange(
            RIGHT, buff=0.25).to_edge(DOWN, buff=0.6)
        cap = label(rf"six rounds, \ {d['cycles']:,} cycles: \ the console prints", font_size=24,
                    color=GREY_A).next_to(letters, UP, buff=0.25)
        with self.voiceover(
            "The actual attack probes indices one through two hundred fifty-five. Line zero is intentionally "
            "omitted because the training calls warm it, so this simple decoder cannot recover a zero-valued secret "
            "byte. <bookmark mark='a'/> Each plotted measurement is the difference between two model-counter reads "
            "around one probe access. <bookmark mark='b'/> In the first round, line eighty, ASCII P, is the "
            "uniquely fast tested line. It takes five measured cycles versus sixty-three for the other tested "
            "lines, including timing overhead. <bookmark mark='c'/> Repeating the procedure recovers the six "
            "supplied nonzero secret bytes, PEBBLE, in this model. That is a concrete simulated witness under the "
            "stated shared-memory and timing capabilities, not evidence of a leak from arbitrary host memory."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(bars), run_time=2.5)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(dip, scale=2), FadeIn(tag))
            vo.wait_until("c")
            self.play(FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(l, scale=1.4) for l in letters], lag_ratio=0.35), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mitigate(self):
        d = load("spectre")
        m = d["mitigations"]
        v = d["victim_cost"]
        head = label(r"Two fixes, \ and what they cost", font_size=36).to_edge(UP, buff=0.3)
        fence = VGroup(mono("bgeu a0, t2, out", 17), mono("lw   t3, 8(a5)    # barrier", 17,
                                                          color=HEAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        mask = VGroup(mono("bgeu a0, t2, out", 17), mono("sltu t3, a0, t2   # 1 if in bounds", 17, color=HEAD),
                      mono("sub  t3, zero, t3  # all ones, or 0", 17, color=HEAD),
                      mono("and  a0, a0, t3    # x, or 0", 17, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        t1 = label("custom model timer barrier; follow ISA-specific rules on hardware", font_size=22, color=DATA)
        t2 = label("unsigned index mask; valid element zero and preserved dependency", font_size=22, color=YES)
        col1 = VGroup(t1, fence).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        col2 = VGroup(t2, mask).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cols = VGroup(col1, col2).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(UP * 1.2)
        if cols.width > 13.0:
            cols.scale_to_fit_width(13.0)
        res = VGroup(
            label("both decoders fail to recover \\texttt{PEBBLE}; \\\\ tested nonzero lines: 63 cycles each in these mitigated runs", font_size=22, color=GREY_A),
            label(rf"cost per call of the victim: \ {v['None']['per_call']:.1f} \ $\to$ \ "
                  rf"{v['fence']['per_call']:.1f} cycles \ (barrier), \ {v['mask']['per_call']:.1f} \ (mask)",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 1.3)
        why = label("finite gadget result; barrier and masking guarantees depend on the model", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Compare two mitigations for this gadget. <bookmark mark='a'/> The first inserts our custom serializing "
            "timer read after the check. In this program its known device address lets the model recognize the "
            "barrier and prevent younger issue until it retires. This is not a universal description of x86 RDTSC "
            "or LFENCE; real barriers require the specified ISA and vendor protocol. <bookmark mark='b'/> The "
            "second makes the array index depend on the unsigned bounds result: all ones for an allowed index, zero "
            "otherwise. <bookmark mark='c'/> Here array element zero exists, so the out-of-bounds transient path is "
            "redirected to a valid element. Compilers and hardware must preserve the dependency for such hardening "
            "to work. <bookmark mark='d'/> Both tested runs fail to recover the supplied secret from the nonzero "
            "probe lines. That finite result is not a proof against every speculative channel. <bookmark mark='e'/> "
            "The benign-call costs shown below are specific to this program and model. Real applications need their "
            "own correctness, performance and threat-model evaluation."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(col1))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(col2))
            vo.wait_until("c")
            self.play(FadeIn(res[0]))
            vo.wait_until("d")
            self.play(FadeIn(res[1]))
            vo.wait_until("e")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def world(self):
        head = label(r"January 2018", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"Spectre \ (Kocher et al.; \ Horn, \ Google Project Zero): \ this attack, \ and one through "
                  r"indirect branches", font_size=22, color=NO),
            label(r"Meltdown \ (Lipp et al.): \ on many Intel cores, \ a load from kernel memory passed its value on "
                  r"\\ before the permission check took effect", font_size=22, color=NO),
            label(r"the fixes: \ separate kernel page tables, \ retpolines, \ coarser timers and site isolation in "
                  r"browsers, \ new hardware", font_size=22, color=YES),
            label("variants affect different implementations; precise state alone is not security", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Spectre and Meltdown were publicly disclosed in January 2018, with variants affecting different "
            "processor implementations. <bookmark mark='a'/> Spectre-style attacks manipulate predictions to induce "
            "transient computations that reveal information through observable microarchitectural state. Our "
            "example is bounds-check bypass, not every Spectre variant. <bookmark mark='b'/> Meltdown's original "
            "attack exploited delayed enforcement of access restrictions on affected processors. Its prerequisites "
            "and mitigations differ from this shared-address-space victim-interface experiment. <bookmark "
            "mark='c'/> Operating systems, browsers, compilers and processors have adopted multiple defenses, "
            "including isolation, hardening and prediction controls. Their applicability depends on architecture, "
            "version, configuration and threat model. Speculation does not by itself imply that every "
            "implementation is vulnerable to every attack, and precise architectural exceptions alone do not "
            "establish security."
        ) as vo:
            self.play(FadeIn(head), FadeIn(items[0]))
            for mk, it in zip("abc", items[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
