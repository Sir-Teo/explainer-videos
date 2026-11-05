from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs17.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, big, code,
                                   grid_table, load, mono, words)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.program()
        self.counts()
        self.where()
        self.ledger()
        self.verdict()

    def card(self):
        card = chapter_card(15, r"The Job, \ hashed", r"How fast is constant time?", lit=(1953,),
                            extra=((1953, r"Luhn's hash table"),), part=PART)
        with self.voiceover("Chapter fifteen. The Job, hashed."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def program(self):
        d = load("job")
        src = d["source"]
        k = next(i for i, l in enumerate(src) if l.startswith("fn count"))
        head = label(r"The Job v2, \ in the Pebble language", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"1. \ hash each word as its letters arrive: \ $h = (33h + c) \bmod 16{,}777{,}213$", font_size=21,
                  color=GREY_A),
            label(r"2. \ probe a table of entry numbers linearly from $h \bmod \mathit{cap}$; \ compare hash, \ "
                  r"length, \ then letters", font_size=21, color=DATA),
            label(r"3. \ a new word gets an entry; \ past half full, \ the table doubles and re-inserts by stored "
                  r"hash", font_size=21, color=LAM),
            label(r"4. \ entries are in first-occurrence order: \ the report is v0's, \ exactly", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(head, DOWN, buff=0.4)
        if steps.width > 12.8:
            steps.scale_to_fit_width(12.8)
        snippet = code(src[k:k + 12], size=15, color=CODE)
        if snippet.width > 12.0:
            snippet.scale_to_fit_width(12.0)
        snippet.next_to(steps, DOWN, buff=0.35)
        note_ = label(r"no bitwise operators in the Pebble language: \ a prime modulus instead of a mask; \ "
                      r"compiled by Part 13's compiler, \ checked on 48 passages", font_size=18,
                      color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the Job rewritten around a hash table. <bookmark mark='a'/> As each letter arrives it is mixed "
            "into a hash: thirty-three times the hash so far, plus the letter, modulo a prime. The Pebble language "
            "has no bitwise operators, so a prime modulus does the mixing. <bookmark mark='b'/> At the end of a "
            "word, the table is probed linearly from the hash modulo its size. Each occupied slot names an entry; "
            "the stored hash is compared first, then the length, and only then the letters. <bookmark mark='c'/> A "
            "new word gets an entry, and when the table would pass half full it doubles and re-inserts every entry "
            "by its stored hash, Part 16's amortized doubling. <bookmark mark='d'/> Entries are created in order of "
            "first appearance, so the report, the twenty largest counts with ties to the earliest word, is exactly "
            "the output of version zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(snippet))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def counts(self):
        d = load("job")
        f = d["features"]
        led = d["ledger"]
        head = label(r"All thirty novels, \ counted exactly", font_size=34).to_edge(UP, buff=0.3)
        slots_per = (f["probes"] + f["new"]) / f["words"]
        tab = grid_table([r"on all thirty novels", r"the Job v1 \ (sort)", r"the Job v2 \ (hash)"], [
            [r"words", words(f["words"]), words(f["words"])],
            [r"word comparisons", big(load("hook")["v1_cmp"]), big(f["len_eq"])],
            [r"slots examined per word", r"---", f"{slots_per:.3f}"],
            [r"Pebble instructions", big(led[7]["instructions"]), big(d["instructions"])],
        ], widths=[4.6, 3.2, 3.2], row_h=0.55, font_size=21, mono_cols=(),
            colors=[[WHITE, GREY_A, GREY_A], [WHITE, NO, YES], [WHITE, GREY_A, YES], [WHITE, NO, YES]]).next_to(
            head, DOWN, buff=0.55)
        cap = 64 * 2 ** f["grows"]
        pts = VGroup(
            label(rf"the table ends at {words(cap)} slots, \ {100 * f['new'] / cap:.0f}\% full: \ Knuth predicts 1.4 "
                  rf"probes for a random key, \ yet we see {slots_per:.2f}", font_size=20, color=GREY_A),
            label(r"because frequent words arrive first, \ and land in their home slot", font_size=20, color=YES),
            label(rf"instructions: \ an exact linear model in {d['n_features']} counted events, \ fitted on "
                  rf"{d['n_train']} passages, \ within {100 * d['held_err']:.2f}\% on {d['n_held']} more", font_size=19,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "How long would it take on all thirty novels? <bookmark mark='a'/> Both versions read four point six "
            "million words. Version one compared words a hundred million times to sort them. Version two compares "
            "each word in full about once, with the entry that matches it. A lookup examines barely more than "
            "one slot. <bookmark mark='b'/> That is better than Knuth's formula predicts for a table that ends "
            "forty-four percent full, and the reason is the data: the commonest words arrive first, when the table "
            "is nearly empty, and sit in their home slots, so the lookups that happen most cost one probe. "
            "<bookmark mark='c'/> As in Part 16, the emulator's instruction count is an exact linear function of "
            "events the program performs; fitted on thirty-six passages, it predicts twelve more to a hundredth of "
            "a percent, and a C program that follows version two step for step counts the events on the whole "
            "corpus. Under a billion instructions, against ten billion for the sort."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def where(self):
        d = load("job")
        parts = d["parts"]
        mem = d["memory"]
        head = label(r"Where the time goes", font_size=34).to_edge(UP, buff=0.3)
        tot = d["instructions"]
        names = list(parts.keys())
        vals = [parts[k] / tot for k in names]
        cols = [DATA, LAM, CTRL, GREY_A, GREY_B]
        bars = VGroup()
        for i, (n, v, c) in enumerate(zip(names, vals, cols)):
            b = Rectangle(width=max(7.0 * v, 0.03), height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.85)
            lab = label(n, font_size=19, color=GREY_A)
            pct = label(rf"{100 * v:.0f}\%", font_size=19, color=c)
            row = VGroup(lab, b, pct)
            lab.move_to([-3.2, -i * 0.62, 0], aligned_edge=RIGHT)
            b.move_to([-3.0 + b.width / 2, -i * 0.62, 0])
            pct.next_to(b, RIGHT, buff=0.15)
            bars.add(row)
        bars.next_to(head, DOWN, buff=0.6).shift(RIGHT * 0.8)
        pts = VGroup(
            label(r"half the instructions now go to reading and hashing the text: \ the table is no longer the "
                  r"bottleneck", font_size=21, color=YES),
            label(rf"the corpus through Part 9's caches: \ {big(mem['accesses'])} table accesses, \ "
                  rf"{100 * mem['L1_miss'] / mem['accesses']:.0f}\% miss L1, \ "
                  rf"{100 * mem['L2_miss'] / mem['accesses']:.2f}\% miss L2", font_size=20, color=GREY_A),
            label(rf"charging every miss its full latency adds {100 * mem['stall_share']:.0f}\% \ "
                  r"(an upper estimate: the core overlaps some)", font_size=20, color=GREY_B),
            label(rf"IPC on Part 8's core: \ {d['ipc']:.2f}, \ lower than the sort's 2.24: \ a division per letter",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where do the instructions go now? <bookmark mark='a'/> Half go to reading the text and hashing it, a "
            "third to probing the table, and the rest mostly to comparing the letters of the matching entry. The "
            "table is no longer the bottleneck; the text is. <bookmark mark='b'/> A hash table scatters its "
            "accesses, so this time we ran the corpus through Part 9's caches as well. Eighty-two million accesses "
            "touch the table; about one in seven misses the first-level cache, but almost none miss the second, "
            "because the part of the table the common words use fits there easily. <bookmark mark='c'/> Charging every miss its full latency "
            "adds about six percent. <bookmark mark='d'/> And the core runs this program less efficiently than the "
            "sort, one and a half instructions per cycle instead of two and a quarter, because every letter needs "
            "a division for the modulus, and Pebble's divider takes sixteen cycles and cannot overlap them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in bars], lag_ratio=0.2), FadeIn(pts[0]), run_time=2)
            for mk, p in zip("bcd", pts[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        d = load("job")
        led = d["ledger"]
        head = label(r"Ledger row 8", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=21, row_h=0.42,
                           label_width=4.8).move_to(DOWN * 0.2)
        cap = VGroup(
            label(rf"a hash table: \ {human_time(d['seconds'])} \ on one core", font_size=24, color=COST),
            label(rf"{d['speedup_vs_row7']:.1f}$\times$ the sort; \ {d['speedup_vs_row5']:.0f}$\times$ the same core "
                  rf"searching a list; \ {d['speedup_vs_row4']:.0f}$\times$ four cores", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And so the ledger gets row eight. <bookmark mark='a'/> The Job with a hash table, on one core of Part "
            "8's machine with Part 9's caches: eight tenths of a second for all thirty novels. <bookmark "
            "mark='b'/> Six times faster than sorting; seventy times faster than the same compiled code searching "
            "a list; fifteen times faster than all four cores of Part 10 running the old algorithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
        self.wait(0.3)
        self.clear_scene()

    def verdict(self):
        d = load("job")
        led = d["ledger"]
        head = label(r"Silicon against thinking", font_size=36).to_edge(UP, buff=0.35)
        hw = d["hardware_gain"]
        alg = d["algorithm_gain"]
        ch = bar_chart([hw, alg], [r"rows 0 $\to$ 4: \ hardware \ (Parts 6--10)",
                                   r"rows 5 $\to$ 8: \ algorithms \ (Parts 16--17)"], [GREY_A, YES], height=3.4,
                       bar_w=1.6, gap=2.4, fmt_=lambda v: rf"{v:.0f}$\times$", font_size=22).move_to(DOWN * 0.2)
        pts = VGroup(
            label(r"the same corpus, \ the same answer; \ the hardware rows built a new machine each time, \ the last "
                  r"with four cores",
                  font_size=21, color=GREY_A),
            label(r"the algorithm rows changed a few dozen lines, \ and run on one core", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Act Four began by asking whether thinking could beat silicon. Here is the answer from the data. "
            "<bookmark mark='a'/> From row zero to row four, a pipeline, an out-of-order core, caches and four cores "
            "made the Job about twenty-four times faster. <bookmark mark='b'/> From row five to row eight, on one "
            "core, a sort and then a hash table made it seventy times faster. <bookmark mark='c'/> The hardware "
            "took five parts and, in the end, four cores; the algorithms took a few dozen lines. Both matter, and "
            "they multiply, but the second kind of improvement is the one no faster chip will ever deliver."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch[0]), FadeIn(ch.names))
            vo.wait_until("a")
            self.play(GrowFromEdge(ch.bars[0], DOWN), FadeIn(ch.vals[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(ch.bars[1], DOWN), FadeIn(ch.vals[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()
