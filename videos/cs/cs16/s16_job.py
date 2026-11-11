from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, big, code, grid_table,
                                   load, mono, words)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.program()
        self.model()
        self.breakdown()
        self.ledger()

    def card(self):
        card = chapter_card(15, r"The Job, \ sorted", r"How much is one idea worth?", lit=(1957,),
                            extra=((1957, r"FORTRAN"),), part=PART)
        with self.voiceover("Chapter fifteen. The Job, sorted."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def program(self):
        d = load("job")
        src = d["source"]
        k = next(i for i, l in enumerate(src) if l.startswith("fn sortw"))
        head = label(r"The Job v1, \ in the Pebble language", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"1. \ record every word as an occurrence: \ where its letters start, \ and its length",
                  font_size=21, color=GREY_A),
            label(r"2. \ stable bottom-up merge sort of the occurrences, \ comparing letters", font_size=21,
                  color=DATA),
            label(r"3. \ one pass: \ each run of equal words is one count; \ its first member is the first "
                  r"occurrence", font_size=21, color=YES),
            label(r"4. \ the twenty largest counts, \ ties to the earliest word: \ the same output as v0", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(head, DOWN, buff=0.4)
        if steps.width > 12.6:
            steps.scale_to_fit_width(12.6)
        snippet = code(src[k:k + 11], size=15, color=CODE)
        if snippet.width > 12.0:
            snippet.scale_to_fit_width(12.0)
        snippet.next_to(steps, DOWN, buff=0.4)
        note = label(r"corpus-sized arrays, one compiled image; 40 emulator and 3 core passages checked against the reference",
                     font_size=19, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Version one sorts occurrences, then counts equal runs. <bookmark mark='a'/> Each occurrence records "
            "its letters' start and length. <bookmark mark='b'/> A stable bottom-up merge sort orders them by "
            "letters. <bookmark mark='c'/> Equal words become neighbors; stability preserves the first occurrence "
            "needed for tie breaking. <bookmark mark='d'/> Selecting the twenty largest counts therefore "
            "reproduces version zero's output. For the corpus projection, we enlarge the arrays explicitly and "
            "use that same compiled image for calibration passages and core samples. Their outputs are checked "
            "against the reference. The whole corpus is counted by the native event model; it is not fully "
            "executed on the emulator."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(snippet))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def model(self):
        d = load("job")
        f = d["features"]
        v0 = d["v0"]
        head = label(r"Corpus event counts; \ instructions and time projected", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"on all thirty novels", r"the Job v0 \ (search)", r"the Job v1 \ (sort)"], [
            [r"words", words(f["words"]), words(f["words"])],
            [r"distinct words", words(v0["distinct"]), words(f["runs"])],
            [r"key comparisons", big(v0["scanned"]), big(f["sort_cmp"] + f["scan_cmp"])],
            [r"letters compared inside them", big(v0["letter_cmp"]), big(f["k_steps"])],
        ], widths=[5.0, 3.4, 3.4], row_h=0.5, font_size=20, mono_cols=(),
            colors=[[WHITE, WHITE, WHITE], [WHITE, WHITE, WHITE], [WHITE, NO, YES], [WHITE, NO, YES]]).next_to(
            head, DOWN, buff=0.45)
        pts = VGroup(
            label(r"v0 compares each word with the table entries before it; \ v1 makes $\approx n \lg n$ "
                  r"comparisons", font_size=20, color=GREY_A),
            label(rf"instruction fit: \ a linear model in {len(d['model']['names']) - 1} counted events, \ fitted on 30 "
                  rf"passages, \ maximum error {100 * d['held_err']:.1f}\% on these 10 held-out passages", font_size=20, color=GREY_A),
            label(rf"projected corpus instructions: \ {big(d['instructions'])}; \ sampled IPC "
                  rf"{d['ipc']:.2f} per cycle", font_size=20, color=YES),
            label(r"the comparisons and letters are counted by a C program that follows v1 step for step", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.13).next_to(tab, DOWN, buff=0.4)
        capacity=label(rf"arrays: {words(d['capacities']['word_capacity'])} occurrences; {words(d['capacities']['letter_capacity'])} letters; {d['memory_bytes']//(1<<20)} MiB modeled RAM",font_size=17,color=GREY_B).to_edge(DOWN,buff=0.3)
        with self.voiceover(
            (
            "Separate exact event counts from projected runtime. <bookmark mark='a'/> The native model follows "
            "the sort-and-count control flow on the full corpus and checks the final word-count output. In "
            "version zero, the corrected letter-comparison count includes matched prefixes and the first "
            "mismatch; a same-length table entry is not itself one letter comparison. <bookmark mark='b'/> We fit "
            "instruction counts from thirty actual emulator passages and test ten held-out passages. The "
            "displayed maximum error applies only to those tests, not every possible text. <bookmark mark='c'/> "
            "Applying the fit to corpus events estimates instructions. Dividing by IPC measured on three core "
            "passages estimates cycles, then time at the stated clock. Neither corpus instructions nor its IPC "
            "has been measured by a full-corpus core run."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2:]),FadeIn(capacity))
        self.wait(0.3)
        self.clear_scene()

    def breakdown(self):
        d = load("job")
        m, f = d["model"], d["features"]
        parts = {k: c * f[k] for k, c in zip(m["names"][1:], m["coef"][1:])}
        tot = d["instructions"]
        groups = [(r"comparison calls and returns", ("sort_cmp", "scan_cmp", "ret_diff", "ret_len", "short_n",
                                                     "sort_right"), DATA),
                  (r"letters compared inside them", ("k_steps",), LAM),
                  (r"copying the merged pass back", ("copy_back",), NO),
                  (r"reading the text", ("bytes", "letters", "capitals", "words"), GREY_B),
                  (r"everything else", None, GREY_D)]
        used = set()
        vals = []
        for name, keys, col in groups:
            if keys is None:
                v = tot - sum(vals)
            else:
                v = sum(parts.get(k, 0) for k in keys)
                used |= set(keys)
            vals.append(v)
        head = label(r"Grouped terms of the fitted instruction model", font_size=34).to_edge(UP, buff=0.3)
        W = 7.5
        rows = VGroup()
        for (name, _, col), v in zip(groups, vals):
            share = v / tot
            bar = Rectangle(width=max(W * abs(share), 0.04), height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85)
            rows.add(VGroup(label(name, font_size=21, color=WHITE), bar,
                            label(rf"{100 * share:.1f}\%", font_size=20, color=col)))
        for k, r in enumerate(rows):
            y = 1.6 - 0.75 * k
            r[1].move_to([-1.6 + (1 if vals[k]>=0 else -1)*r[1].width / 2, y, 0])
            r[0].move_to([-1.9 - r[0].width / 2, y, 0])
            r[2].next_to(r[1], RIGHT, buff=0.15)
        if rows.width > 13:
            rows.scale_to_fit_width(13)
        pts = VGroup(
            label(r"correlated feature terms; \ grouped shares are not traced instruction categories", font_size=21,
                  color=GREY_A),
            label(r"candidate: alternate source/scratch arrays, \ then remeasure the changed program",
                  font_size=21, color=NO),
            label(r"fitted attribution does not establish a percentage saving in instructions or seconds", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        rank=label(rf"design rank {m['rank']}/{m['columns']}; correlated coefficients do not identify unique causal shares",font_size=18,color=GREY_B).next_to(head,DOWN,buff=0.25)
        with self.voiceover(
            (
            "A fitted decomposition suggests where to investigate. <bookmark mark='a'/> These bars group "
            "coefficient times corpus event count, not traced instruction categories. Correlated features can "
            "admit different coefficient allocations with similar total predictions. <bookmark mark='b'/> The "
            "copy-back term motivates a concrete experiment: alternate the two arrays instead of copying a full "
            "pass back. But removing a fitted term does not establish the same percentage reduction in "
            "instructions or seconds. That needs a changed program, checked output and a new measurement. "
            "<bookmark mark='c'/> Use the model to propose and test an optimization, while keeping attribution "
            "uncertainty visible."
        )
        ) as vo:
            self.play(FadeIn(head),FadeIn(rank), *[FadeIn(r[0]) for r in rows])
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                                  lag_ratio=0.3), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        d = load("job")
        led = d["ledger"]
        head = label(r"Ledger row 7", font_size=38).to_edge(UP, buff=0.35)
        rows = led + [{"part": 17, "label": r"a hash table"}]
        tab = ledger_table(rows, shown=len(led), highlight=(len(led) - 1,), font_size=21, row_h=0.42,
                           label_width=4.8).move_to(DOWN * 0.3)
        res = VGroup(
            label(rf"projected: \ {human_time(d['seconds'])}; \ passage-sampled IPC, one modeled core", font_size=24, color=COST),
            label(rf"{d['speedup_vs_row5']:.0f}$\times$ faster than the same machine searching; \ "
                  rf"{d['speedup_vs_row4']:.1f}$\times$ faster than four cores", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "The ledger gains an explicitly projected row. <bookmark mark='a'/> It combines full-corpus event "
            "counts, the held-out instruction fit and passage-sampled IPC on one modeled core. Its arrays and "
            "emulated memory are sized for the corpus, while the full corpus remains unexecuted on that core. "
            "<bookmark mark='b'/> Read the estimated time and speedups on screen. They compare the stated models "
            "and assumptions; they are not elapsed timings of full-corpus runs. The important algorithmic change "
            "is replacing repeated vocabulary scans with sorting. Part 17 asks whether hashing can remove that "
            "sorting step too."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(res[0]), Indicate(tab.rows[len(led) - 1], color=COST))
            vo.wait_until("b")
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()
