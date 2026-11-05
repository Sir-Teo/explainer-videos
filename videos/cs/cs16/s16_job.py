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
        note = label(r"compiled by Part 13's compiler, \ \texttt{-O2}; \ checked against the reference on 43 passages",
                     font_size=19, color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now the Job, rewritten around a sort. <bookmark mark='a'/> As it reads the text it records every word "
            "as an occurrence: where its letters begin, and how many there are. <bookmark mark='b'/> Then it sorts "
            "the occurrences with a stable, bottom-up merge sort, comparing letters. <bookmark mark='c'/> After the "
            "sort, equal words are neighbours, so one pass turns each run into a count, and because the sort was "
            "stable, the first member of each run is the word's first appearance. <bookmark mark='d'/> Picking the "
            "twenty largest counts, ties broken by first appearance, gives exactly the output of version zero. It "
            "is written in the Pebble language, compiled by our compiler, and checked against the reference on "
            "every passage we ran."
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
        head = label(r"All thirty novels, \ counted exactly", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"on all thirty novels", r"the Job v0 \ (search)", r"the Job v1 \ (sort)"], [
            [r"words", words(f["words"]), words(f["words"])],
            [r"distinct words", words(v0["distinct"]), words(f["runs"])],
            [r"key comparisons", big(v0["scanned"]), big(f["sort_cmp"] + f["scan_cmp"])],
            [r"letters compared inside them", big(v0["same_length"]), big(f["k_steps"])],
        ], widths=[5.0, 3.4, 3.4], row_h=0.5, font_size=20, mono_cols=(),
            colors=[[WHITE, WHITE, WHITE], [WHITE, WHITE, WHITE], [WHITE, NO, YES], [WHITE, NO, YES]]).next_to(
            head, DOWN, buff=0.45)
        pts = VGroup(
            label(r"v0 compares each word with the table entries before it; \ v1 makes $\approx n \lg n$ "
                  r"comparisons", font_size=20, color=GREY_A),
            label(rf"instructions: \ a linear model in {len(d['model']['names']) - 1} counted events, \ fitted on 30 "
                  rf"passages, \ within {100 * d['held_err']:.1f}\% on 10 more", font_size=20, color=GREY_A),
            label(rf"applied to the novels: \ {big(d['instructions'])} Pebble instructions; \ on Part 8's core at "
                  rf"{d['ipc']:.2f} per cycle", font_size=20, color=YES),
            label(r"the comparisons and letters are counted by a C program that follows v1 step for step", font_size=18,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.13).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "How long would it take on all thirty novels? <bookmark mark='a'/> The table compares the two versions' "
            "work on the whole corpus. Both read four point six million words. Version zero searches its table for "
            "each one: fifteen billion key comparisons. Version one sorts: about a hundred million. <bookmark "
            "mark='b'/> To turn the counts into time, we fitted the emulator's instruction count, on thirty "
            "passages, as a linear function of the events the program performs: comparisons, letters compared, "
            "elements moved, and so on. On ten passages it had not seen, the prediction is within half a percent. "
            "<bookmark mark='c'/> A small C program counts the same events on the whole corpus, step for step, in "
            "two seconds. The model then gives ten billion instructions, which Part 8's out-of-order core runs at "
            "about two and a quarter per cycle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2:]))
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
        head = label(r"Where the instructions go", font_size=34).to_edge(UP, buff=0.3)
        W = 7.5
        rows = VGroup()
        for (name, _, col), v in zip(groups, vals):
            share = max(v / tot, 0)
            bar = Rectangle(width=max(W * share, 0.04), height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85)
            rows.add(VGroup(label(name, font_size=21, color=WHITE), bar,
                            label(rf"{100 * share:.0f}\%", font_size=20, color=col)))
        for k, r in enumerate(rows):
            y = 1.6 - 0.75 * k
            r[1].move_to([-1.6 + r[1].width / 2, y, 0])
            r[0].move_to([-1.9 - r[0].width / 2, y, 0])
            r[2].next_to(r[1], RIGHT, buff=0.15)
        if rows.width > 13:
            rows.scale_to_fit_width(13)
        pts = VGroup(
            label(r"half the work is comparing words; \ the letters themselves are a quarter", font_size=21,
                  color=GREY_A),
            label(r"a fifth is copying each pass back: \ swapping the two arrays instead would save it all",
                  font_size=21, color=NO),
            label(r"the model says not only how long, \ but where to look next", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The fitted model does more than predict a total; it says where the time goes. <bookmark mark='a'/> "
            "About half of the ten billion instructions are spent calling the comparison function and returning "
            "from it, and a quarter on the letters it compares. <bookmark mark='b'/> A fifth is spent copying each "
            "merged pass from the scratch array back into the main one. Alternating the roles of the two arrays "
            "would remove that entirely: a twenty percent saving, found by counting. <bookmark mark='c'/> That is "
            "the habit this part is about: count the steps, and the counts tell you where to look."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(r[0]) for r in rows])
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
            label(rf"sort, then count: \ {human_time(d['seconds'])} \ on one core", font_size=24, color=COST),
            label(rf"{d['speedup_vs_row5']:.0f}$\times$ faster than the same machine searching; \ "
                  rf"{d['speedup_vs_row4']:.1f}$\times$ faster than four cores", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And so the ledger gets row seven. <bookmark mark='a'/> Sorting, then counting, on one core of Part 8's "
            "machine: about five seconds for all thirty novels. <bookmark mark='b'/> Eleven times faster than the "
            "same compiled program searching a list, and more than twice as fast as the four cores of Part 10, "
            "running the old algorithm. One idea beat every core we built. And n log n is not the end. A hash "
            "table, in Part 17, does the counting in expected linear time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(res[0]), Indicate(tab.rows[len(led) - 1], color=COST))
            vo.wait_until("b")
            self.play(FadeIn(res[1]))
        self.wait(0.3)
        self.clear_scene()
