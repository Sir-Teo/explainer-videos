from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, big, code, grid_table, load,
                                   mono, words)


class JobSketch(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.program()
        self.memory()
        self.ledger()
        self.gamble()

    def card(self):
        card = chapter_card(10, r"The Job in kilobytes", r"Can we count the top words without remembering the words?",
                            lit=(2002,), extra=((2002, r"conservative update"),), part=PART)
        with self.voiceover("Chapter ten. The Job in kilobytes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def design(self):
        head = label(r"The Job v3: \ a sketch and a heap", font_size=34).to_edge(UP, buff=0.35)
        parts = VGroup(
            VGroup(label(r"\textbf{Count-Min}, \ 4 rows $\times$ 1021 counters", font_size=24, color=DATA),
                   label(r"every word's count, \ estimated; \ no word stored", font_size=20, color=GREY_A)),
            VGroup(label(r"\textbf{32 candidates} \ in a min-heap by estimate", font_size=24, color=LAM),
                   label(r"a word enters when its estimate beats the smallest candidate's", font_size=20,
                         color=GREY_A)),
            VGroup(label(r"\textbf{128 slots}, \ linear probing", font_size=24, color=CTRL),
                   label(r"finds a word among the candidates; \ eviction by backward shifting (Knuth's Algorithm R)",
                         font_size=20, color=GREY_A)),
            VGroup(label(r"\textbf{conservative update} \ (Estan and Varghese, 2002)", font_size=24, color=YES),
                   label(r"raise only the counters at the minimum: \ still never an undercount, \ far less excess",
                         font_size=20, color=GREY_A)),
            VGroup(label(r"\textbf{double hashing} \ (Kirsch and Mitzenmacher, 2006)", font_size=24, color=HEAD),
                   label(r"row $r$ uses $(h + r g) \bmod 1021$, \ $g = 1 + \lfloor h / 1021 \rfloor \bmod 1020$: \ "
                         r"one division for four rows", font_size=20, color=GREY_A)),
        )
        for p in parts:
            p.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        parts.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Now the Job itself, rebuilt so that it never stores the vocabulary. <bookmark mark='a'/> A Count-Min "
            "sketch of four rows of 1021 counters estimates every word's count. <bookmark mark='b'/> Only thirty-two "
            "words are kept, candidates for the top twenty, in a heap ordered by estimate; a word replaces the "
            "weakest when its estimate beats it. <bookmark mark='c'/> A table of a hundred and twenty-eight slots "
            "finds a word among the candidates, and an evicted one is deleted by shifting its neighbours back, "
            "Knuth's Algorithm R. <bookmark mark='d'/> Estan and Varghese's conservative update raises only the "
            "counters at the minimum: it still never undercounts, but it adds far less to other words. <bookmark "
            "mark='e'/> And double hashing gives all four row positions from one division per word."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", parts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def program(self):
        d = load("job")
        src = d["source"]
        k = next(i for i, ln in enumerate(src) if ln.startswith("fn seen"))
        body = src[k:k + 40]

        def ln(i):
            return body[i].split("//")[0].rstrip()
        groups = [
            ([ln(0)], None),
            ([ln(1), ln(2), ln(4), ln(5), "    ...   (y and z the same way: the rows at x, y, z)"], 0),
            ([ln(14), ln(15), "    ...   (and the other two rows)"], 1),
            ([ln(19), "    ...", ln(23)], 2),
            ([ln(24), ln(25)], 3),
            ([ln(26), ln(27)], 4),
            ([ln(28), "        ...   (join the heap, sift up)", "    }", ln(35), ln(36) + " " + ln(37).strip() + " " +
              ln(38).strip()], 5),
            ([ln(39)], None),
        ]
        lines = [x for g, _ in groups for x in g]
        head = label(r"The heart of it, \ in the Pebble language", font_size=34).to_edge(UP, buff=0.3)
        snippet = code(lines, size=17, color=CODE)
        if snippet.height > 6.2:
            snippet.scale_to_fit_height(6.2)
        snippet.next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        texts = [r"four row indices, \ one division", r"the estimate: \ the smallest counter",
                 r"conservative update", r"most words stop here", r"already a candidate: \ sift down",
                 r"else join, \ or replace the weakest"]
        cols = [HEAD, DATA, YES, LAM, CTRL, CTRL]
        side = VGroup()
        boxes = VGroup()
        at = 0
        for g, gi in groups:
            if gi is not None:
                grp = VGroup(*snippet[at:at + len(g)])
                boxes.add(SurroundingRectangle(grp, color=cols[gi], buff=0.05, stroke_width=1.5))
                side.add(label(texts[gi], font_size=20, color=cols[gi]).set_y(grp.get_y()))
            at += len(g)
        x0 = max(b.get_right()[0] for b in boxes) + 0.4
        for t in side:
            t.align_to([x0, 0, 0], LEFT)
        with self.voiceover(
            "Here is the function that runs once per word, compiled by Part 13's compiler. <bookmark mark='a'/> "
            "First the four counter positions, each the last plus the step g, wrapped by a subtraction instead of "
            "a division. <bookmark mark='b'/> The estimate is the smallest of the four counters, <bookmark "
            "mark='c'/> and only the counters equal to it are raised. <bookmark mark='d'/> Then the test that makes "
            "the program cheap: if the heap is full and this word's estimate can't beat the weakest candidate, we "
            "are done. Almost every word in English stops here. <bookmark mark='e'/> A word that is already a "
            "candidate gets its new estimate and moves down the heap. <bookmark mark='f'/> Anything else joins, "
            "or replaces the weakest candidate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(snippet))
            for mk, s_, b in zip("abcdef", side, boxes):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=LEFT * 0.1), Create(b))
        self.wait(0.3)
        self.clear_scene()

    def memory(self):
        d = load("job")
        g = d["globals"]
        head = label(r"What the program remembers", font_size=34).to_edge(UP, buff=0.35)
        items = [("cm", r"the sketch", DATA), ("cword", r"candidates' letters", LAM), ("slot", r"slots", CTRL),
                 ("chash", r"hash", LAM), ("clen", r"length", LAM), ("cest", r"estimate", LAM),
                 ("cpos", r"heap place", LAM), ("heap", r"heap", LAM), ("word", r"current word", GREY_B)]
        total = d["footprint"]
        W = 12.0
        x = -W / 2
        strip = VGroup()
        labels_ = VGroup()
        for key, name, col in items:
            w = W * g[key] / total
            r = Rectangle(width=max(w, 0.02), height=0.7, stroke_width=0.5, stroke_color=BLACK, fill_color=col,
                          fill_opacity=0.8).move_to([x + w / 2, 1.2, 0])
            strip.add(r)
            x += w
        labels_.add(label(rf"the sketch: \ {words(g['cm'])} bytes", font_size=20, color=DATA).next_to(strip[0], DOWN,
                                                                                                   buff=0.2))
        labels_.add(label(rf"everything else: \ {words(total - g['cm'])} bytes", font_size=20, color=LAM
                          ).next_to(VGroup(*strip[1:]), DOWN, buff=0.2).shift(LEFT * 0.4))
        tot = label(rf"{words(total)} bytes, \ about {total / 1000:.1f} KB, \ in one contiguous block", font_size=24,
                    color=YES).next_to(strip, UP, buff=0.3)
        v2 = VGroup(
            label(rf"the Job v2, \ Part 17: \ every distinct word \ ({words(d['vocab'])}), \ its entry and "
                  r"its slot", font_size=22, color=WHITE),
            label(rf"{d['v2_bytes'] / 1e6:.1f} MB", font_size=30, color=NO),
            label(rf"the v3 needs {d['memory_ratio']:.0f}$\times$ less", font_size=28, color=YES),
            label(r"and $18.6$ KB fits in Part 9's 32 KB L1 cache: \ after the first few hundred words, \ no misses",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "What does it remember? <bookmark mark='a'/> The sketch is sixteen thousand bytes. The candidates, "
            "their letters, the heap and the slots take about two thousand more. <bookmark mark='b'/> In all, "
            f"{words(total)} bytes, eighteen and a half kilobytes, in one block. <bookmark mark='c'/> Part 17's "
            "version kept every distinct word, almost fifty-eight thousand of them, with an entry and a slot each: "
            f"{d['v2_bytes'] / 1e6:.1f} megabytes. <bookmark mark='d'/> A hundred times less. <bookmark mark='e'/> "
            "And eighteen and a half kilobytes fits in Part 9's level-one cache, so once the first few hundred words "
            "have touched every line, the program never misses again. We checked by tracing every load and store "
            f"of a {d['passage_bytes'] // 1000}-kilobyte passage through the cache model: {d['traced_lines']} lines "
            f"in all, never more than {d['max_lines_per_set']} in a set of eight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in strip], lag_ratio=0.15), FadeIn(labels_))
            vo.wait_until("b")
            self.play(FadeIn(tot))
            vo.wait_until("c")
            self.play(FadeIn(v2[0]), FadeIn(v2[1]))
            vo.wait_until("d")
            self.play(FadeIn(v2[2]))
            vo.wait_until("e")
            self.play(FadeIn(v2[3]))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        d = load("job")
        led = d["ledger"]
        r8, r9 = led[-2], led[-1]
        head = label(r"Ledger row 9", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.34,
                           label_width=4.8).scale(0.92).move_to(UP * 1.25)
        rows = [
            [r"instructions", big(r8["instructions"]), big(r9["instructions"])],
            [r"instructions per cycle", f"{r8['ipc']:.2f}", f"{r9['ipc']:.2f}"],
            [r"cycles waiting for memory", big(r8["stall_cycles"]), words(r9["stall_cycles"])],
            [r"memory", f"{r8['memory_bytes'] / 1e6:.1f} MB", f"{r9['memory_bytes'] / 1000:.1f} KB"],
            [r"seconds", f"{r8['seconds']:.2f}", f"{r9['seconds']:.2f}"],
        ]
        cmp_ = grid_table([r"", r"row 8: \ a hash table", r"row 9: \ Count-Min"], rows, widths=[4.0, 3.0, 3.0],
                          row_h=0.34, font_size=18, mono_cols=(),
                          colors=[[GREY_A, GREY_A, COST]] * 4 + [[WHITE, GREY_A, COST]]).to_edge(DOWN, buff=0.3)
        cmp_.set_x(0)
        with self.voiceover(
            "So the ledger gets its ninth row. Every one of the program's "
            f"{big(d['instructions'])} instructions was run on the emulator, about {d['per_byte']:.0f} per byte of "
            "text, and the output matched the exact counts, word for word and digit for digit. <bookmark "
            "mark='a'/> Priced on Part 8's core: one second, a quarter slower than the hash table. <bookmark "
            "mark='b'/> The sketch does more work per word, and its chains of comparisons run fewer instructions "
            "per cycle. <bookmark mark='c'/> The hash table lost forty-four million cycles waiting for memory; the "
            "sketch, forty-six thousand. <bookmark mark='d'/> Row nine is not a speed-up. It buys memory: a hundred "
            "times less, for a quarter more time. That trade is the whole point of streaming algorithms, because "
            "for a real stream the vocabulary doesn't fit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            self.play(FadeIn(tab.rows[-1]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*cmp_.cells[0])), FadeIn(cmp_.rule), FadeIn(VGroup(*cmp_.cells[5])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*cmp_.cells[1])), FadeIn(VGroup(*cmp_.cells[2])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*cmp_.cells[3])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*cmp_.cells[4])), Indicate(cmp_.cells[4][2], color=YES))
        self.wait(0.3)
        self.clear_scene()

    def gamble(self):
        sw = {(r["d"], r["w"], r["conservative"]): r for r in load("sweep")["rows"]}
        head = label(r"How lucky was that?", font_size=36).to_edge(UP, buff=0.35)
        order = [((2, 1021, True), r"2 rows $\times$ 1021"), ((4, 509, True), r"4 $\times$ 509"),
                 ((4, 1021, False), r"4 $\times$ 1021, \ plain update"), ((4, 1021, True), r"4 $\times$ 1021 \ "
                                                                                           r"(the program)"),
                 ((4, 2039, True), r"4 $\times$ 2039"), ((4, 4093, True), r"4 $\times$ 4093")]
        rows = [[name, f"{sw[k]['kb']:.0f} KB", f"{sw[k]['mean_overlap']:.1f}", f"{sw[k]['worst_overlap']}",
                 f"{sw[k]['exact_share'] * 100:.0f}\\%"] for k, name in order]
        tab = grid_table([r"sketch", r"size", r"top 20 right \ (mean)", r"worst", r"all exact"], rows,
                         widths=[4.6, 1.4, 3.0, 1.3, 1.8], row_h=0.44, font_size=19, mono_cols=(),
                         colors=[[GREY_A, GREY_A, LAM, NO, YES]] * len(rows)).next_to(head, DOWN, buff=0.4)
        hl = SurroundingRectangle(VGroup(*tab.cells[4]), color=HEAD, buff=0.06, stroke_width=1.5)
        ex = sw[(4, 1021, True)]["example_intruder"]
        occ = "once" if ex[2] == 1 else f"{ex[2]} times"
        notes = VGroup(
            label(r"twenty different hash functions per row, \ the same text", font_size=20, color=GREY_A),
            label(rf"an intruder: \ \textit{{{ex[0]}}}, \ which occurs {ex[2]} time, \ estimated at "
                  rf"{words(ex[1])}", font_size=20, color=NO),
            label(r"a Monte Carlo algorithm: \ the memory is guaranteed, \ the answer is probably right", font_size=22,
                  color=HEAD),
            label(r"the true top 20 were always among the 32 candidates: \ a second pass, \ counting only them, "
                  r"\ is exact every time", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "But was the exact answer luck? The hash function is the algorithm's coin, so we reran the same "
            "algorithm, in C, with twenty different hash functions, for several sketch sizes. <bookmark mark='a'/> "
            "With the program's own size, four rows of 1021 counters, the reported top twenty were exactly right, "
            "words and counts, for five of the twenty hash functions, and the program's own was one of the five. "
            "On average 19.1 of the twenty words were right, and never fewer than eighteen. <bookmark mark='b'/> "
            f"The typical intruder is a rare word that collides with common ones in every row: {ex[0]}, which "
            f"appears in the novels {occ}, was estimated at almost "
            "fifty-nine thousand. <bookmark mark='c'/> The plain update was never exact, and a sketch of two rows "
            "got only fourteen words right on average. Doubling the width to 32 kilobytes made seventy percent of "
            "the runs exact, and 64 kilobytes, ninety-five. <bookmark mark='d'/> This is a Monte Carlo algorithm: "
            "the memory and the time are guaranteed, the answer is probably right, and more memory buys more "
            "probability. <bookmark mark='e'/> And there is a cheap fix. In every one of the twenty runs, the "
            "true top twenty were among the thirty-two candidates. A second pass over the text, counting just "
            "those thirty-two words exactly, would have given the exact answer every time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(notes[0]))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
            vo.wait_until("a")
            self.play(Create(hl))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(VGroup(*tab.cells[3]), color=NO), Indicate(VGroup(*tab.cells[6]), color=YES))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
