from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (COST, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class TheJob(VoiceoverScene):
    def construct(self):
        self.card()
        self.engineered()
        self.breakdown()
        self.ledger()

    def card(self):
        card = chapter_card(14, r"The Job, \ engineered", r"How fast can the word count go on this machine?",
                            lit=(2017,), extra=((2017, r"Swiss tables"),), part=PART)
        with self.voiceover("Chapter fourteen. The Job, engineered."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def engineered(self):
        d = load("job")
        tb, en = d["textbook"], d["engineered"]
        head = label(r"Part 17's hash table, \ engineered for this machine", font_size=32).to_edge(UP, buff=0.3)
        changes = VGroup(
            label(r"\textbf{1.} \ words found 32 bytes at a time \ (chapter 10's AVX2 scan)", font_size=22, color=DATA),
            label(r"\textbf{2.} \ hash 8 letters per multiply, \ not one letter per step", font_size=22, color=LAM),
            label(r"\textbf{3.} \ a Swiss-style table: \ 16 control bytes per group, \ one SSE2 compare", font_size=22,
                  color=HEAD),
            label(r"\textbf{4.} \ the first 8 letters, \ the length and the count live \textbf{in the slot}: \ a short "
                  r"word never leaves the table", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.45)
        rows = [[r"Part 17's open addressing", f"{tb['best'] * 1000:.0f} ms", f"{tb['median'] * 1000:.0f} ms",
                 f"{tb['best'] * 1e9 / d['bytes']:.1f}"],
                [r"engineered", f"{en['best'] * 1000:.0f} ms", f"{en['median'] * 1000:.0f} ms",
                 f"{d['ns_per_byte']:.1f}"]]
        tab = grid_table([r"C, \ the 30 novels", r"best of 7", r"median", r"ns per byte"], rows,
                         widths=[4.6, 2.0, 2.0, 2.2], row_h=0.48, font_size=22, mono_cols=(),
                         colors=[[GREY_A] * 4, [YES] * 4])
        tab.next_to(changes, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(rf"{words(d['words'])} words, \ {words(d['distinct'])} distinct; \ both print the same twenty lines, "
                  r"byte for byte, \ as the Python reference", font_size=21, color=WHITE),
            label(rf"{d['speedup']:.1f}$\times$ by best time; \ the engineered runs spread widely \ (chapter 12: "
                  r"this machine is shared)", font_size=21, color=YES),
            label(r"what is left: \ one hash and one cache miss per word, \ the floor for a table of 58 thousand "
                  r"words", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "The Job counts the words of thirty novels and lists the twenty most common. Part 17 did it with an "
            "open-addressing hash table, and we ran that program in C on this machine. Now we engineer it. "
            "<bookmark mark='a'/> First, find the words with the vector scan of chapter ten. <bookmark mark='b'/> "
            "Second, hash eight letters at a time with one multiplication instead of one letter per step. <bookmark "
            "mark='c'/> Third, a Swiss-style table, sixteen control bytes compared at once. <bookmark mark='d'/> And "
            "fourth, store the first eight letters, the length and the count inside the slot itself, so that a short "
            "word, which is most words, is found and counted without touching any other memory. <bookmark "
            "mark='e'/> Best of seven runs: a hundred and fifty-five milliseconds for the textbook version, seventy-"
            "five for the engineered one, about twice as fast, with identical output. <bookmark mark='f'/> The "
            "engineered runs varied a lot, so the honest claim is the best time and the median together. What is "
            "left is about one hash and one cache miss per word."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", changes):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.4), FadeIn(notes[0]))
            vo.wait_until("f")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def breakdown(self):
        d = load("job")
        tk = load("simd")["token"]
        tb, en = d["textbook"]["best"], d["engineered"]["best"]
        scan_t, scan_e = tk["scalar_s"], tk["simd_s"]
        head = label(r"Where the time went: \ Amdahl's law", font_size=32).to_edge(UP, buff=0.35)
        sc = 60.0
        x0 = -4.6

        def bar(y, parts, cap):
            g = VGroup()
            x = x0
            for v, col, txt in parts:
                r = Rectangle(width=v * sc, height=0.6, stroke_width=0).set_fill(col, 0.75)
                r.move_to([x + v * sc / 2, y, 0])
                g.add(r)
                if v * sc > 0.9:
                    g.add(label(txt, font_size=17, color=WHITE).move_to(r))
                x += v * sc
            g.add(label(cap, font_size=20, color=GREY_A).next_to(g[0], LEFT, buff=0.2))
            g.add(mono(f"{sum(p[0] for p in parts) * 1000:.0f} ms", 18, WHITE).next_to(g[-2] if len(parts) > 1 else g[0],
                                                                                    RIGHT, buff=0.2))
            return g
        b1 = bar(1.3, [(scan_t, DATA, r"finding words"), (tb - scan_t, NO, r"the table")], r"textbook")
        b2 = bar(0.2, [(scan_e, DATA, r""), (tb - scan_t, NO, r"the old table")], r"SIMD scan only")
        b3 = bar(-0.9, [(scan_e, DATA, r""), (en - scan_e, YES, r"the new table")], r"engineered")
        notes = VGroup(
            label(rf"finding words was {scan_t / tb * 100:.0f}\% of the textbook time; \ the SIMD scan makes that "
                  rf"part {scan_t / scan_e:.0f}$\times$ faster", font_size=21, color=DATA),
            label(rf"alone, \ that buys only {tb / (tb - scan_t + scan_e):.2f}$\times$: \ Amdahl (1967), \ the part you "
                  r"don't speed up decides", font_size=21, color=NO),
            label(r"so the table had to change too: \ profile first, \ then engineer the biggest part", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Before engineering anything, measure where the time goes. <bookmark mark='a'/> In the textbook program, "
            "finding the words took about a quarter of the time, and the hash table the rest. <bookmark mark='b'/> "
            "The vector scan makes the first part nine times faster. But on its own that would make the whole "
            "program only about thirty percent faster, because the table is untouched. That is Amdahl's law, from 1967: "
            "the part you do not speed up decides the total. <bookmark mark='c'/> So the table had to change as "
            "well, and the slot that carries the word's first letters is what took it from about a hundred and "
            "fifteen milliseconds to seventy. Profile first; then engineer the largest part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(b1))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(b2), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(b3), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        d = load("job")
        led = d["ledger"]
        row = led[-1]
        head = label(r"Ledger row 10", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.34,
                           label_width=4.8).scale(0.92).move_to(UP * 1.0)
        notes = VGroup(
            label(r"rows 1--9 priced the Job on the Pebble cores of Parts 6--10; \ row 10 is measured on real "
                  r"hardware", font_size=21, color=WHITE),
            label(rf"the same textbook C on this machine: \ {row['textbook_native_seconds'] * 1000:.0f} ms, \ against "
                  rf"Pebble's {d['pebble_hash_s']:.2f} s: \ a real 2.1 GHz core, \ wider and with larger caches",
                  font_size=21, color=COST),
            label(rf"engineering on top: \ {d['speedup']:.1f}$\times$ more, \ {row['seconds'] * 1000:.0f} ms for 25 MB",
                  font_size=21, color=YES),
            label(r"from the first row, \ 281 seconds on a single-cycle Pebble, \ to 75 milliseconds: \ hardware, "
                  r"\ compilers and algorithms all contributed", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So the ledger gets its tenth row, and it is a new kind of row. <bookmark mark='a'/> Rows one to nine "
            "priced the Job on the cores we built, from the single-cycle Pebble of Part 6 to the four cores of Part "
            "10. Row ten is measured on the real processor that rendered this video. <bookmark mark='b'/> Part 17's "
            "textbook program alone runs five times faster here than on our modelled core, because a real core is "
            "wider, faster and has far larger caches. <bookmark mark='c'/> The engineering then doubles that again: "
            "seventy-five milliseconds for twenty-five megabytes. <bookmark mark='d'/> From two hundred and eighty-one "
            "seconds on the first row to seventy-five milliseconds, a factor of nearly four thousand, and every layer "
            "of the tower contributed to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            self.play(FadeIn(tab.rows[-1]))
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
