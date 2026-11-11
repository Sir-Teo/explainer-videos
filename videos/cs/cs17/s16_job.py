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
            "Here is the Job rewritten around a hash table. <bookmark mark='a'/> As each letter arrives "
            "it is mixed into a hash: thirty-three times the hash so far, plus the letter, modulo a "
            "prime. The Pebble language has no bitwise operators, so a prime modulus does the mixing. "
            "<bookmark mark='b'/> At the end of a word, the table is probed linearly from the hash modulo"
            " its size. Each occupied slot names an entry; the stored hash is compared first, then the "
            "length, and only then the letters. <bookmark mark='c'/> A new word gets an entry, and when "
            "the table would pass half full it doubles and re-inserts every entry by its stored hash, "
            "Part 16's amortized doubling. <bookmark mark='d'/> Entries are created in order of first "
            "appearance, so the report, the twenty largest counts with ties to the earliest word, is "
            "exactly the output of version zero."
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
        head = label(r"Corpus events observed; \ instructions projected", font_size=34).to_edge(UP, buff=0.3)
        slots_per = (f["probes"] + f["new"]) / f["words"]
        tab = grid_table([r"on all thirty novels", r"the Job v1 \ (sort)", r"the Job v2 \ (hash)"], [
            [r"words", words(f["words"]), words(f["words"])],
            [r"word comparisons", big(load("hook")["v1_cmp"]), big(f["len_eq"])],
            [r"slots examined per word", r"---", f"{slots_per:.3f}"],
            [r"Pebble instructions (fitted)", big(led[7]["instructions"]), big(d["instructions"])],
        ], widths=[4.6, 3.2, 3.2], row_h=0.55, font_size=21, mono_cols=(),
            colors=[[WHITE, GREY_A, GREY_A], [WHITE, NO, YES], [WHITE, GREY_A, YES], [WHITE, NO, YES]]).next_to(
            head, DOWN, buff=0.55)
        cap = 64 * 2 ** f["grows"]
        pts = VGroup(
            label(rf"the table ends at {words(cap)} slots, \ {100 * f['new'] / cap:.0f}\% full: \ Knuth predicts 1.4 "
                  rf"probes for a random key, \ yet we see {slots_per:.2f}", font_size=20, color=GREY_A),
            label(r"fixed hash + frequency-weighted stream; \ not a random-key guarantee", font_size=20, color=YES),
            label(rf"instructions: \ a least-squares model in {d['n_features']} counted events, \ fitted on "
                  rf"{d['n_train']} passages, \ within {100 * d['held_err']:.3f}\% on {d['n_held']} more", font_size=19,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Separate observed events from predicted instructions. <bookmark mark='a'/> A native event "
            "counter processes all thirty novels and reproduces the complete reference report. It records"
            " the displayed word, comparison and slot counts. The sort and hash comparison counters "
            "follow different control paths, so read their definitions. <bookmark mark='b'/> The low "
            "average slot count reflects this fixed polynomial hash and this frequency-weighted access "
            "stream, not a random-key guarantee at the final load. <bookmark mark='c'/> We compile one "
            "explicitly corpus-sized image and use it for all forty-eight emulator passages and three "
            "core samples. Thirty-six passages fit a least-squares instruction model; twelve are held "
            "out. Their errors are displayed. Correlated features make coefficients nonunique, and "
            "full-corpus features exceed the training range. Full-corpus instructions remain an "
            "extrapolation, not an exact executed count."
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
        model, mem = d["model"], d["memory"]
        head = label(r"Audit the projection: \ which quantities were executed?", font_size=32).to_edge(UP, buff=0.3)
        tab = grid_table([r"evidence", r"what ran", r"scope"], [
            [r"native event counter", r"all thirty novels; \ full report checked", r"observed control-flow events"],
            [r"emulator", r"48 passages, \ one corpus-sized image", r"36 fit / 12 held out"],
            [r"out-of-order core", rf"3 passages; \ weighted IPC {d['ipc']:.2f}", r"passage throughput only"],
            [r"toy cache hierarchy", r"selected accesses; \ assumed array layout", r"partial trace model"],
        ], widths=[3.0, 6.0, 3.7], row_h=0.62, font_size=20, mono_cols=(),
            colors=[[DATA, GREY_A, DATA], [LAM, GREY_A, LAM], [HEAD, GREY_A, HEAD], [GREY_B, GREY_A, GREY_B]]).next_to(head, DOWN, buff=0.48)
        warnings = VGroup(
            label(rf"fit rank {model['rank']} of {model['columns']}: \ correlated coefficients do not identify unique category costs", font_size=21, color=NO),
            label(rf"{len(d['full_exceeds_training_max'])} corpus event features exceed the training maximum; \ held-out error is local validation", font_size=20, color=HEAD),
            MathTex(r"\text{scenario cycles}=\frac{\text{fitted instructions}}{\text{sampled IPC}}+\text{assumed miss penalties}", font_size=29, color=YES),
            label(r"overlap omitted; \ sampled stalls may be counted twice; \ not a proved upper bound", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "This panel is a model audit, not a measured time breakdown. <bookmark mark='a'/> The fitted "
            "event matrix is rank deficient. Different coefficient choices can predict the same sampled "
            "counts, so grouped coefficients cannot uniquely attribute instructions or identify a "
            "bottleneck. <bookmark mark='b'/> A separate C trace follows selected data accesses using an "
            "assumed array layout through the toy cache hierarchy. It is not the compiled program's full "
            "memory trace and omits some accesses. <bookmark mark='c'/> We add incremental miss penalties"
            " to instructions divided by sampled IPC. This additive scenario omits overlap and may double"
            " count stalls already reflected in IPC; it is not a proven upper bound. <bookmark mark='d'/>"
            " The three core samples use the same corpus-sized image. Their weighted IPC is observed on "
            "those passages. Neither that IPC nor the cache model is a full-corpus execution, and neither"
            " alone proves the causal effect of division."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a"); self.play(FadeIn(warnings[0]))
            vo.wait_until("b"); self.play(FadeIn(warnings[1]))
            vo.wait_until("c"); self.play(FadeIn(warnings[2:]))
            vo.wait_until("d"); self.play(Indicate(tab.cells[3][1], color=HEAD))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        d = load("job")
        led = d["ledger"]
        head = label(r"Ledger row 8: \ unexecuted corpus projection", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=21, row_h=0.42,
                           label_width=4.8).move_to(DOWN * 0.2)
        cap = VGroup(
            label(rf"a hash table: \ {human_time(d['seconds'])} \ projected on one core", font_size=24, color=COST),
            label(rf"{d['speedup_vs_row7']:.1f}$\times$ the sort; \ {d['speedup_vs_row5']:.0f}$\times$ the same core "
                  rf"searching a list; \ {d['speedup_vs_row4']:.0f}$\times$ four cores", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The ledger adds a projected row. <bookmark mark='a'/> Its time combines native corpus "
            "events, fitted instructions, three-passage core throughput and an assumed partial cache "
            "trace at the ledger clock. The number on screen is the scenario estimate; the full corpus "
            "was not executed by the emulator or core. <bookmark mark='b'/> The displayed speed ratios "
            "compare those ledger estimates under their stated assumptions. They illustrate the possible "
            "benefit of changing the algorithm, with model uncertainty carried forward."
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
            label(r"algorithm and hardware bars use different baselines; \ model uncertainty carries forward", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Both hardware and algorithms change the cost of a task. <bookmark mark='a'/> The first bar "
            "compares earlier hardware ledger rows on the same corpus. <bookmark mark='b'/> The second "
            "compares the compiled list-based baseline with this projected hash-table row on one core. "
            "They use different baselines, so do not multiply the bars as independent measured gains. "
            "<bookmark mark='c'/> The educational result is the change in work: replacing repeated linear"
            " search with a suitable dictionary can remove enormous lookup effort. The exact runtime "
            "benefit still depends on inputs, hashing, implementation, and the machine model."
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
