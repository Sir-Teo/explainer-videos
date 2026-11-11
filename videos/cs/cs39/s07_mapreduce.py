from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, box, gantt, grid_table, load, trace)


class MapReduce(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.runs()
        self.scaling()
        self.ledger()
        self.beyond()

    def card(self):
        card = chapter_card(6, r"MapReduce", r"How do you run one program on a thousand unreliable machines?",
                            lit=(2003, 2015), extra=((2003, r"Ghemawat et al.: \ GFS"),
                                                     (2004, r"Dean and Ghemawat: \ MapReduce"),
                                                     (2012, r"Zaharia et al.: \ Spark"),
                                                     (2015, r"Akidau et al.: \ Dataflow")), part=PART)
        with self.voiceover("Chapter six. MapReduce."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def model(self):
        j = load("job")
        head = label(r"Map, \ shuffle, \ reduce", font_size=36).to_edge(UP, buff=0.3)
        splits = VGroup(*[box(1.5, 0.55, rf"split {i + 1}", DATA, font_size=16) for i in range(4)]).arrange(
            DOWN, buff=0.25).move_to([-5.0, 0.4, 0])
        maps = VGroup(*[box(1.5, 0.55, r"map", DATA, font_size=17) for _ in range(4)]).arrange(DOWN, buff=0.25).move_to(
            [-2.6, 0.4, 0])
        reds = VGroup(*[box(1.6, 0.55, t, LAM, font_size=16) for t in (r"reduce a--h", r"reduce i--p",
                                                                       r"reduce q--z")]).arrange(DOWN, buff=0.45).move_to([1.6, 0.4, 0])
        outs = VGroup(*[box(1.4, 0.55, r"counts", YES, font_size=16) for _ in range(3)]).arrange(DOWN, buff=0.45).move_to(
            [4.4, 0.4, 0])
        a1 = VGroup(*[Arrow(s.get_right(), m.get_left(), buff=0.08, color=GREY_B, stroke_width=2) for s, m in
                      zip(splits, maps)])
        cols = [DATA, KERN, HEAD]
        shuffle = VGroup(*[Line(m.get_right(), r.get_left(), color=cols[k], stroke_width=1.6).set_opacity(0.7)
                           for m in maps for k, r in enumerate(reds)])
        a3 = VGroup(*[Arrow(r.get_right(), o.get_left(), buff=0.08, color=GREY_B, stroke_width=2) for r, o in
                      zip(reds, outs)])
        code_l = VGroup(
            label(r"\texttt{map(split)}: \ for each word $w$: \ emit $(w, 1)$ \ --- \ combined locally into $(w, c)$",
                  font_size=19, color=DATA),
            label(r"\texttt{reduce}$(w, [c_1, c_2, \dots])$: \ emit $(w, \sum c_i)$", font_size=19, color=LAM),
            label(rf"the novels: \ {j['bytes'] / 1e6:.0f} MB in, \ "
                  rf"{j['runs']['plain']['shuffle_bytes'] / 1e6:.1f} MB shuffled, \ "
                  rf"{j['runs']['plain']['distinct']:,} distinct words out", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Jeffrey Dean and Sanjay Ghemawat's MapReduce, of 2004, let a programmer write two small functions and "
            "run them on thousands of machines. <bookmark mark='a'/> The input, stored in pieces across the cluster, "
            "is split, and a map function runs on each split: for the Job, it emits each word with a count of one, "
            "combined locally into a count per word. <bookmark mark='b'/> The shuffle sends every word to one "
            "reducer, chosen by hashing the word, so all the counts for a word meet in one place. "
            "<bookmark mark='c'/> Each reducer adds them up. <bookmark mark='d'/> For the novels: twenty-five "
            "megabytes in, six megabytes of partial counts shuffled, fifty-eight thousand distinct words out. The "
            "programmer writes none of the distribution, the scheduling or the recovery."
        ) as vo:
            self.play(FadeIn(head), FadeIn(splits))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in a1], lag_ratio=0.1), FadeIn(maps), FadeIn(code_l[0]))
            vo.wait_until("b")
            self.play(Create(shuffle), FadeIn(reds), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a) for a in a3], lag_ratio=0.1), FadeIn(outs), FadeIn(code_l[1]))
            vo.wait_until("d")
            self.play(FadeIn(code_l[2]))
        self.wait(0.4)
        self.clear_scene()

    def runs(self):
        j = load("job")
        head = label(r"Five runs on sixteen Pebbles", font_size=36).to_edge(UP, buff=0.3)
        names = [("plain", r"no trouble"), ("crash", r"Pebble 4 crashes at 0.4 s"),
                 ("straggler", r"Pebble 6 runs 8$\times$ slow"),
                 ("straggler, no backups", r"\ \ the same, \ no backup tasks"),
                 ("crash and straggler", r"both")]
        rows = []
        for key, nm in names:
            r = j["runs"][key]
            rows.append([nm, f"{r['time']:.2f} s", f"{r['reexecuted']}", f"{r['backups']}",
                         r"identical" if r["correct"] else r"\textbf{wrong}"])
        tab = grid_table([r"run", r"time", r"maps redone", r"backup copies", r"top 20"], rows,
                         widths=[4.6, 1.6, 2.0, 2.2, 1.8], row_h=0.46, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][4].set_color(YES)
        tab.cells[4][1].set_color(NO)
        tab.cells[3][1].set_color(YES)
        lines = VGroup(
            wrapped_label(r"\textbf{failure}: \ the master pings workers; \ a dead worker's running tasks, \ and its "
                          r"\textit{completed} maps \ (their output was on its disk), \ are run again elsewhere. \ "
                          r"Functional map and reduce make re-execution safe.", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{stragglers}: \ near the end, \ idle workers run backup copies of tasks still in "
                          r"progress; \ the first copy to finish wins. \ Google reported a sort 44\% slower without "
                          r"them.", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "We ran the Job five ways. <bookmark mark='a'/> With nothing going wrong, half a second. With Pebble four "
            "crashing at four tenths of a second, six tenths, three finished maps redone, and the same answer. "
            "<bookmark mark='b'/> Re-execution is safe because map and reduce are functions: running a task twice "
            "gives the same output, and the master simply uses whichever copy it hears about first. "
            "<bookmark mark='c'/> Now make Pebble six eight times slower, a straggler, like a machine with a failing "
            "disk. With backup tasks the Job takes point five nine seconds; without them, point eight one, a third "
            "longer, because everyone waits for the slow machine's last task. Google's paper reported the same "
            "effect: a large sort forty-four percent slower with backup tasks turned off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in (3, 4, 5)], lag_ratio=0.3),
                      FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def scaling(self):
        j = load("job")
        head = label(r"More Pebbles, \ diminishing returns", font_size=36).to_edge(UP, buff=0.3)
        sc = j["scaling"]
        import math
        g = axes([0, 6.5, 1], [0, 4.2, 1], x_length=6.6, y_length=3.8, x_label=r"workers \ (log scale)",
                 y_label=r"seconds", xticks=range(0, 7), yticks=(1, 2, 3, 4),
                 fx=lambda v: f"{2 ** int(v)}").move_to([-2.8, -0.4, 0])
        ax = g.ax
        meas = VGroup(trace(ax, [(math.log2(x["workers"]), x["seconds"]) for x in sc], DATA, width=3),
                      *[Dot(ax.c2p(math.log2(x["workers"]), x["seconds"]), radius=0.06, color=DATA) for x in sc])
        ideal = trace(ax, [(math.log2(x["workers"]), sc[0]["seconds"] / x["workers"]) for x in sc], GREY_B, width=2)
        notes = VGroup(
            wrapped_label(rf"1 worker: \ {sc[0]['seconds']:.2f} s; \ 16: \ {sc[4]['seconds']:.2f} s \ "
                          rf"({sc[0]['seconds'] / sc[4]['seconds']:.1f}$\times$); \ 64: \ {sc[-1]['seconds']:.2f} s",
                          5.4, font_size=20, color=DATA),
            wrapped_label(r"grey: \ perfect scaling. \ Each task pays a fixed start-up cost, \ the shuffle and the "
                          r"reduces do not shrink with more mappers, \ and the last task to finish sets the time: \ "
                          r"Amdahl's law \ (Part 10) \ again", 5.4, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "How far does it scale? <bookmark mark='a'/> One worker takes three point eight seconds, more than the "
            "plain Job, because of the overheads of splitting, scheduling and shuffling. Sixteen workers are seven "
            "times faster, not sixteen; sixty-four, barely faster than thirty-two. <bookmark mark='b'/> Every task "
            "pays a fixed start-up cost, the shuffle and the reduces do not shrink as mappers are added, and the "
            "slowest task sets the finishing time. It is Amdahl's law from Part 10 again, at the scale of a "
            "datacenter. MapReduce was built for jobs of terabytes, where these overheads vanish into the work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(ideal), Create(meas), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        row = led[-1]
        head = label(r"Ledger row 15", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.3,
                           label_width=4.8).scale(0.86).move_to(UP * 0.85)
        prev = next(x for x in led if x["part"] == 34)
        notes = VGroup(
            label(rf"the Job as MapReduce on sixteen Pebbles, \ one crashing: \ {row['seconds']:.2f} s, \ against "
                  rf"{prev['seconds']:.2f} s on one", font_size=19, color=HEAD),
            label(r"the novels already spread across the cluster's disks, \ as in GFS: \ moving the computation to "
                  r"the data, \ not the data across an ocean \ (row 14)", font_size=19, color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        for n in notes:
            if n.width > 12.8:
                n.width = 12.8
        with self.voiceover(
            "The ledger gets row fifteen. <bookmark mark='a'/> The Job as MapReduce on sixteen Pebbles, one of which "
            "crashes: six tenths of a second, four and a half times faster than one Pebble, and correct despite the "
            "crash. <bookmark mark='b'/> The novels start out spread across the cluster's disks, as Google's file "
            "system kept its data. That is the real lesson of row fourteen: move the computation to the data, not "
            "the data across an ocean."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def beyond(self):
        head = label(r"After MapReduce", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{Spark} \ (Zaharia et al., 2012): \ resilient distributed datasets kept in memory; \ "
                          r"a lost partition is recomputed from its \textbf{lineage}, \ the chain of transformations "
                          r"that made it, \ instead of being replicated", 12.4, font_size=22, color=YES),
            wrapped_label(r"\textbf{streaming} \ (Dataflow, \ Flink): \ unbounded input, \ windows by \textit{event} "
                          r"time, \ \textbf{watermarks} that say ``no older events are coming'', \ and handling for the "
                          r"late ones \ (Part 46)", 12.4, font_size=22, color=LAM),
            wrapped_label(r"\textbf{exactly-once} state: \ periodic Chandy--Lamport snapshots of every operator \ "
                          r"(Part 38), \ and replay of the input since the last one", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"the ideas that last: \ deterministic tasks, \ re-execution instead of replication, \ and "
                          r"computation moved to the data", 12.4, font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "MapReduce wrote everything to disk between stages, which made long pipelines slow. "
            "<bookmark mark='a'/> Matei Zaharia's Spark, in 2012, kept datasets in memory, and handled failure by "
            "remembering each dataset's lineage, the chain of transformations that produced it: a lost piece is "
            "simply recomputed. <bookmark mark='b'/> Streaming systems run the same model on input that never ends, "
            "grouping events into windows by when they happened rather than when they arrived, with watermarks to "
            "say that no older events are expected, and a policy for those that arrive anyway. "
            "<bookmark mark='c'/> They get exactly-once results by taking Chandy and Lamport's snapshots of every "
            "operator, and replaying the input since the last one after a crash. <bookmark mark='d'/> The ideas "
            "that last are MapReduce's: deterministic tasks, recovery by re-execution, and computation moved to "
            "the data."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, NO, gantt)
