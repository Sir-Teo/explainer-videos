from __future__ import annotations

import re

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, box, fmt, load, say, sci)


def mono(s, size=19, color=CODE):
    return Text(s, font="DejaVu Sans Mono", font_size=size, color=color)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.algorithm()
        self.code()
        self.runs()
        self.formula()
        self.novels()

    def card(self):
        card = chapter_card(10, r"The Job, \ version 0", r"How long would Pebble take to count thirty novels?",
                            part=PART)
        with self.voiceover("Chapter ten. The Job, version zero."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def algorithm(self):
        j = load("job")
        para = j["paragraph"]["text"]
        # Eight words include both insertion and a repeated "a", within the
        # aligned lookup explanation. More rows overran the next speech cue.
        words = re.findall(r"[a-z]+", para.lower())[:8]
        head = label(r"Count the words: \ the simplest way", font_size=38).to_edge(UP, buff=0.35)
        tape_txt = para[:58]
        tape = VGroup(*[Text(ch if ch != " " else "·", font="DejaVu Sans Mono", font_size=20,
                             color=GREY_B if not ch.isalpha() else DATA) for ch in tape_txt]).arrange(RIGHT, buff=0.03)
        tape.move_to(UP * 2.3)
        tl = label(r"the tape", font_size=20, color=GREY_B).next_to(tape, LEFT, buff=0.2)
        table_rows = VGroup()
        table_head = VGroup(label(r"word", font_size=22, color=GREY_B), label(r"count", font_size=22,
                                                                            color=GREY_B)).arrange(RIGHT, buff=1.4)
        table_head.move_to(LEFT * 2.4 + UP * 1.4)
        ent_y0 = 0.95
        ptr = Arrow(LEFT * 0.5, ORIGIN, buff=0, color=HEAD, stroke_width=4)
        cur = label(r"current word", font_size=20, color=GREY_B).move_to(RIGHT * 3.6 + UP * 1.4)
        side = VGroup(
            label(r"for each word: \ compare it with every entry, \ from the top", font_size=22, color=GREY_A),
            label(r"found: \ add one to its count; \ not found: \ append it", font_size=22, color=GREY_A),
            label(r"at the end: \ twenty times, \ find and print the largest count", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.4 + DOWN * 1.5)
        entries: list[str] = []
        counts: dict[str, int] = {}
        with self.voiceover(
            "Now the Job, the task that travels through the whole series: count the words of thirty novels and list "
            "the twenty most common. Version zero does it in the most direct way there is. <bookmark mark='a'/> Read "
            "the text one character at a time from the tape, folding capitals to lower case, and collect letters into "
            "a word. <bookmark mark='b'/> At the end of each word, look it up in a table by comparing it with every "
            "entry in turn, from the top. If it is there, add one to its count. If not, append it at the bottom. "
            "<bookmark mark='c'/> At the end, find the largest count, print that word, cross it off, and repeat twenty "
            "times. No sorting, no hashing, nothing clever: Parts 16 and 17 will supply the clever versions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tape), FadeIn(tl))
            self.play(FadeIn(table_head), FadeIn(cur), FadeIn(side[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            for k, w in enumerate(words):
                wt = mono(w, 24, HEAD).next_to(cur, DOWN, buff=0.2)
                self.play(FadeIn(wt), run_time=0.25)
                hit = w in counts
                stop = entries.index(w) if hit else len(entries)
                if entries:
                    first_row = table_rows[0]
                    ptr.next_to(first_row, LEFT, buff=0.15)
                    self.add(ptr)
                    for i in range(min(stop + (1 if hit else 0), len(entries))):
                        self.play(ptr.animate.next_to(table_rows[i], LEFT, buff=0.15),
                                  run_time=1 / 15 if k > 4 else 2 / 15)
                if hit:
                    counts[w] += 1
                    i = entries.index(w)
                    row = table_rows[i]
                    nc = mono(str(counts[w]), 20, YES).move_to(row[1])
                    # A parent-row animation would overwrite the count's
                    # simultaneous Transform. Highlight only the word label.
                    self.play(Transform(row[1], nc), Indicate(row[0], color=YES), run_time=0.35)
                else:
                    entries.append(w)
                    counts[w] = 1
                    y = ent_y0 - 0.36 * (len(entries) - 1)
                    row = VGroup(mono(w, 20, DATA).move_to([-3.2, y, 0], aligned_edge=LEFT),
                                 mono("1", 20, YES).move_to([-1.0, y, 0]))
                    table_rows.add(row)
                    self.play(TransformFromCopy(wt, row[0]), FadeIn(row[1]), run_time=0.35)
                self.play(FadeOut(wt), run_time=0.15)
            self.remove(ptr)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def code(self):
        head = label(r"The inner loop, \ in Pebble assembly", font_size=36).to_edge(UP, buff=0.35)
        src = ["word:   mv   t0, s0          # the first entry", "        li   a2, 0", "scan:   beq  a2, s1, insert",
               "        lw   t1, 4(t0)       # same length?", "        bne  t1, a1, next", "        ...                 # compare the letters",
               "next:   addi t0, t0, 12      # the next entry", "        addi a2, a2, 1", "        j    scan"]
        lines = VGroup(*[mono(s_, 19) for s_ in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(LEFT * 1.6 +
                                                                                                         UP * 0.3)
        hot = VGroup(lines[2], lines[3], lines[4], lines[6], lines[7], lines[8])
        hb = VGroup(*[SurroundingRectangle(h, buff=0.04, color=NO, stroke_width=1.6) for h in hot])
        note = VGroup(
            label(r"6 instructions \\ for every entry \\ of a different length", font_size=24, color=NO),
            label(r"a few more \\ for each matching letter", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5)
        foot = label(r"about a hundred lines in all: \ reading, \ the table, \ and printing numbers by repeated "
                     r"subtraction \ (Pebble cannot divide yet)", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is the heart of it in Pebble assembly. <bookmark mark='a'/> For each table entry, the loop checks "
            "whether it has reached the end, loads the entry's length, and if the lengths differ, steps to the next "
            "entry. Six instructions per entry. <bookmark mark='b'/> Only entries of the right length go on to compare "
            "letters. The whole program, reading, the table, and printing the counts in decimal by repeated "
            "subtraction, since Pebble has no divide instruction yet, is about a hundred lines."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines),
                      LaggedStart(*[Create(b) for b in hb], lag_ratio=0.2), FadeIn(note[0]), run_time=1.5)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(note[1]), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def runs(self):
        j = load("job")
        p, c = j["paragraph"], j["chapter"]
        head = label(r"Gate by gate, \ and on the emulator", font_size=38).to_edge(UP, buff=0.35)
        para = label(r"``It is a truth universally acknowledged, \ that a single man in possession \\ of a good fortune, "
                     r"must be in want of a wife.'' \ \ldots", font_size=22, color=DATA).move_to(UP * 2.0)
        cols = VGroup(
            VGroup(label(r"the first paragraph, \ gate level", font_size=24, color=YES),
                   label(rf"{p['bytes']} bytes, \ {fmt(p['steps'])} cycles", font_size=24, color=GREY_A),
                   label(rf"{p['seconds']:.0f} s of simulation: \ {fmt(p['steps'] / p['seconds'])} cycles a second",
                         font_size=20, color=GREY_B)),
            VGroup(label(r"the whole first chapter, \ emulator", font_size=24, color=CODE),
                   label(rf"{fmt(c['bytes'])} bytes, \ {fmt(c['steps'])} instructions", font_size=24, color=GREY_A),
                   label("this paragraph: \\ equal output and step count \\\\ chapter: emulator only", font_size=20, color=GREY_B)),
        )
        for col in cols:
            col.arrange(DOWN, buff=0.15)
        cols.arrange(RIGHT, buff=1.2).move_to(UP * 0.4)
        out = c["output"].strip().split("\n")[:10]
        outs = VGroup(*[mono(o, 18, HEAD) for o in out]).arrange_in_grid(2, 5, buff=(0.6, 0.15)).move_to(DOWN * 1.6)
        ol = label(r"chapter 1's ten most common words, \ as Pebble prints them", font_size=20, color=GREY_B).next_to(
            outs, UP, buff=0.2)
        with self.voiceover(
            "Time to run it. <bookmark mark='a'/> The opening paragraph of Pride and Prejudice, six hundred and "
            "thirteen bytes, on the gate-level machine: fifty-three thousand six hundred and sixty-five clock cycles, "
            "with every gate evaluated in every cycle; the simulation time shown is specific to the recorded host run."
            " <bookmark mark='b'/> The whole first chapter is more than the gates can comfortably do, so it runs on "
            "the emulator: four thousand seven hundred bytes, eight hundred and twenty-seven thousand instructions. On"
            " the paragraph, the two machines print exactly the same thing in exactly the same number of steps. "
            "<bookmark mark='c'/> And here is what Pebble prints for chapter one: you, of, to, a, the. It is a chapter"
            " of conversation between Mr and Mrs Bennet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(para), FadeIn(cols[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(ol), LaggedStart(*[FadeIn(o) for o in outs], lag_ratio=0.12), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formula(self):
        j = load("job")
        checks = np.array(j["checks"], dtype=float)
        head = label(r"An exact count, \ without running it", font_size=38).to_edge(UP, buff=0.35)
        eq = MathTex(r"\text{cycles}", r"=", r"10 + 9B + 3L + c", r"+ \cdots", r"+ 6S", r"+ 9E", r"+ 8M", r"+ \cdots",
                     font_size=34).move_to(UP * 1.9)
        eq[0].set_color(COST)
        eq[4].set_color(NO)
        terms = VGroup(
            label(r"$B$ bytes, \ $L$ letters, \ $c$ capitals", font_size=20, color=GREY_A),
            label(r"$S$: \ table entries scanned", font_size=20, color=NO),
            label(r"$E$: \ entries of the same length, \ $M$: \ letters matched", font_size=20, color=GREY_A),
        ).arrange(RIGHT, buff=0.5).next_to(eq, DOWN, buff=0.25)
        logs = np.log10(checks[:, 1:])
        lo, hi = np.floor(logs.min() * 2) / 2, np.ceil(logs.max() * 2) / 2
        ax = Axes(x_range=[lo, hi, 0.5], y_range=[lo, hi, 0.5], x_length=4.2, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16}).move_to(LEFT * 2.4 + DOWN * 1.4)
        xl = note(r"emulator's instruction count", font_size=18).next_to(ax, DOWN, buff=0.4)
        yl = note(r"formula", font_size=18).rotate(PI / 2).next_to(ax, LEFT, buff=0.55)
        diag = DashedLine(ax.c2p(lo, lo), ax.c2p(hi, hi), color=GREY_D, stroke_width=1.5)
        ticks = VGroup()
        for e in np.arange(np.ceil(lo), hi + 0.01, 1.0):
            ticks.add(MathTex(rf"10^{{{int(e)}}}", font_size=16, color=GREY_B).next_to(ax.c2p(e, lo), DOWN, buff=0.08))
            ticks.add(MathTex(rf"10^{{{int(e)}}}", font_size=16, color=GREY_B).next_to(ax.c2p(lo, e), LEFT, buff=0.08))
        pts = VGroup(*[Dot(ax.c2p(np.log10(e), np.log10(f)), radius=0.06, color=YES) for _, e, f in checks])
        exact = int(np.sum(checks[:, 1] == checks[:, 2]))
        side = VGroup(
            label(r"each path through the program costs a fixed number of instructions, \\ so the count is a sum of "
                  r"events in the text", font_size=22, color=GREY_A),
            label(rf"checked on {len(checks)} random passages: \ {exact} of {len(checks)} exactly equal", font_size=24,
                  color=YES),
            label("count text events directly; \\ avoid executing every Pebble instruction", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.4 + DOWN * 1.3)
        with self.voiceover(
            "Running thirty novels instruction by instruction on this Python emulator would be expensive. But we do "
            "not need to run them to know exactly how long Pebble would take. <bookmark mark='a'/> Every path through "
            "the program costs a fixed number of instructions: each byte read costs nine, each letter three more, each"
            " table entry scanned six, each entry of the same length nine more, each matching letter eight. So the "
            "total is a sum over events in the text, which Python can count directly. <bookmark mark='b'/> The formula"
            " is not an estimate. On twenty random passages from the novels, it matches the emulator's instruction "
            "count exactly, every one, to the last instruction. These checks support the path-count derivation; they "
            "are not a formal proof for every input."
        ) as vo:
            self.play(FadeIn(head))
            self.play(Write(eq), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(terms), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(diag), FadeIn(ticks))
            self.play(LaggedStart(*[FadeIn(p_, scale=2) for p_ in pts], lag_ratio=0.1), FadeIn(side[1]), run_time=2.0)
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def novels(self):
        j = load("job")
        co = j["corpus"]
        f = co["features"]
        pr = j["projections"]
        head = label(r"Thirty novels, \ version 0", font_size=38).to_edge(UP, buff=0.3)
        facts = VGroup(
            label(rf"{fmt(f['bytes'])} bytes, \ {fmt(f['words'])} words, \ {fmt(f['distinct'])} different words",
                  font_size=24, color=GREY_A),
            label(rf"table entries scanned: \ ${sci(f['scanned'], 3)}$", font_size=24, color=NO),
            label(rf"Pebble cycles: \ ${sci(co['cycles'], 4)}$, \ {fmt(co['per_byte'])} per byte of text", font_size=26,
                  color=COST),
            label(rf"{100 * co['share']['scan'] / co['cycles']:.1f}\% of them inside the linear search", font_size=24,
                  color=NO),
        ).arrange(DOWN, buff=0.18).move_to(UP * 1.5)
        rows = [{"part": 6, "label": r"Pebble, assumed clock", "seconds": pr["single cycle"]}] + [
            {"part": p_, "label": t} for p_, t in ((7, r"a pipeline"), (9, r"caches"), (10, r"four cores"),
                                                   (13, r"an optimizing compiler"), (16, r"sort, then count"),
                                                   (17, r"a hash table"))]
        led = ledger_table(rows, shown=1, highlight=(0,), font_size=21, row_h=0.36, label_width=5.0).move_to(DOWN * 1.65)
        proj = VGroup(
            label(rf"rate analogy, \ 5.3/s: \ {human_time(pr['Z3 relays (5.3 Hz)'])}", font_size=22, color=GREY_A),
            label(rf"rate analogy, \ 5,000/s: \ {human_time(pr['ENIAC (5,000 additions per second)'])}", font_size=22,
                  color=GREY_A),
            label(rf"assumed Pebble, \ {j['clock_mhz']:.0f} MHz: \ {human_time(pr['single cycle'])}", font_size=22,
                  color=YES),
        ).arrange(RIGHT, buff=0.45).next_to(facts, DOWN, buff=0.25)
        with self.voiceover(
            "So here is version zero on all thirty novels. <bookmark mark='a'/> Twenty-five million bytes; four and a "
            "half million words, of fifty-eight thousand different kinds. Because the table is searched from the top "
            "every time, the program scans fifteen billion table entries. <bookmark mark='b'/> In total, a hundred and"
            " seven billion Pebble cycles, more than four thousand per byte of text, and more than ninety-nine percent"
            " of them inside the linear search. <bookmark mark='c'/> For scale, divide that same Pebble instruction "
            "count by historical operation rates: at five point three operations per second, six centuries; at five "
            "thousand, eight months. These are rate illustrations, not ports to the Z3 or ENIAC. Under our assumed "
            "single-cycle budget of about three hundred and eighty megahertz, the projection is under five minutes; we"
            " have not built that silicon machine. <bookmark mark='d'/> That is the first row of the ledger. Every "
            "later row will say what a better machine, or a better idea, buys; and the numbers on this screen already "
            "hint which will matter more."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]))
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
            self.play(FadeIn(facts[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in proj], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("d")
            self.play(FadeIn(led.axis), LaggedStart(*[FadeIn(r) for r in led.rows], lag_ratio=0.1), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
