from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.arrivals()
        self.three()
        self.ledger()

    def card(self):
        card = chapter_card(13, r"The Job as a stream", r"Can a live answer equal the batch answer?",
                            lit=(2013, 2015), extra=((2013, r"Kreps: \ the log"),
                                                     (2015, r"Akidau et al.: \ the Dataflow model")), part=PART)
        with self.voiceover("Chapter thirteen. The Job as a stream."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def arrivals(self):
        j = load("job")
        head = label(r"Thirty novels, \ arriving", font_size=36).to_edge(UP, buff=0.3)
        x0, w, y = -6.0, 12.0, 0.6
        tmax = max(at for _, at in j["arrivals"]) + 1
        axis = Arrow([x0, y - 0.6, 0], [x0 + w, y - 0.6, 0], buff=0, color=GREY_C, stroke_width=2)
        al = label(r"arrival time \ (s)", font_size=17, color=GREY_B).next_to(axis, DOWN, buff=0.15).align_to(axis,
                                                                                                         RIGHT)
        ticks = VGroup(*[label(f"{t}", font_size=15, color=GREY_B).move_to([x0 + t / tmax * w, y - 0.85, 0])
                         for t in range(0, int(tmax), 5)])
        marks = VGroup()
        seen = set()
        for b, at in j["arrivals"]:
            col = NO if b in j["late"] else (HEAD if b in j["duplicated"] else DATA)
            dup = b in seen
            seen.add(b)
            r = Rectangle(width=0.16, height=0.5 if not dup else 0.3, stroke_width=0, fill_color=col,
                          fill_opacity=0.9).move_to([x0 + at / tmax * w, y + (0.0 if not dup else 0.55), 0])
            marks.add(r)
        legend = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.9),
                                 label(t, font_size=18, color=c)).arrange(RIGHT, buff=0.12)
                          for t, c in ((r"on time", DATA), (rf"late: \ books {', '.join(str(x + 1) for x in j['late'])}",
                                                            NO),
                                       (rf"sent twice: \ books {', '.join(str(x + 1) for x in j['duplicated'])}",
                                        HEAD))]).arrange(RIGHT, buff=0.6).move_to([0, 2.1, 0])
        foot = wrapped_label(rf"{j['words']:,} words in all; \ each book is one event carrying its words, \ keyed "
                             r"by the book, \ with its place in the publishing schedule as event time", 12.4,
                             font_size=20, color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The Job, one last time in a new shape. <bookmark mark='a'/> The thirty novels arrive as a stream, one "
            "event per book, each carrying its words and its place in a publishing schedule as its event time. "
            "<bookmark mark='b'/> Most arrive a second or two after they are due. Three arrive twenty seconds late, "
            "as if from a phone that was offline. <bookmark mark='c'/> And two are sent twice, by a producer that "
            "retried. The task is a top twenty that is correct at every moment, and in the end equal to the batch "
            "answer of every earlier part."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axis), FadeIn(al), FadeIn(ticks), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in marks], lag_ratio=0.05), FadeIn(legend[0]),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(legend[1]), *[Indicate(marks[k]) for k, (b, _) in enumerate(j["arrivals"])
                                          if b in j["late"]])
            vo.wait_until("c")
            self.play(FadeIn(legend[2]))
        self.wait(0.4)
        self.clear_scene()

    def three(self):
        j = load("job")
        r = j["results"]
        head = label(r"Three pipelines, \ one stream", font_size=36).to_edge(UP, buff=0.3)
        truth = dict(j["truth"])
        rows = []
        for name, key, col in ((r"exactly once: \ dedup by book, \ keep state", "exactly once", YES),
                               (r"no deduplication", "no dedup", NO),
                               (r"a 5 s watermark, \ late books dropped", "watermark lag 5 s", HEAD)):
            v = r[key]
            the = dict(v["top"]).get("the", 0)
            rows.append([name, f"{v['total']:,}", f"{the:,}", r"yes" if v["matches_batch"] else r"no"])
        tab = grid_table([r"pipeline", r"words counted", r"``the''", r"equals batch?"], rows,
                         widths=[5.4, 2.6, 1.8, 2.2], row_h=0.55, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6)
        for k, col in enumerate((YES, NO, HEAD)):
            tab.cells[k + 1][3].set_color(col)
        truth_l = label(rf"batch answer: \ {j['words']:,} words, \ ``the'' {truth['the']:,} times", font_size=20,
                        color=GREY_A).next_to(tab, DOWN, buff=0.4)
        lines = VGroup(
            wrapped_label(r"the stream's state is a fold over its events: \ keyed by book, \ applied once, \ and "
                          r"checkpointed with the source's offset \ (chapter 5)", 12.4, font_size=20, color=YES),
            wrapped_label(r"a top twenty over all time needs no watermark at all; \ a windowed one would have to "
                          r"choose between waiting and being wrong \ (chapter 4)", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "We ran three pipelines over the same stream. <bookmark mark='a'/> The first deduplicates by book and "
            f"keeps its counts as state: it counts {r['exactly once']['total']:,} words, and its top twenty is "
            "identical to the batch answer. <bookmark mark='b'/> The second does not deduplicate. The two books "
            f"sent twice are counted twice, {r['no dedup']['total']:,} words, and the counts are wrong. "
            "<bookmark mark='c'/> The third uses a watermark that waits five seconds and drops anything later, so "
            f"the three late books are missing: {r['watermark lag 5 s']['total']:,} words. "
            "<bookmark mark='d'/> The state of a stream is a fold over its events, applied once per key and "
            "checkpointed with the source's offset. And because this top twenty is over all time, it needs no "
            "watermark at all; a windowed answer would face chapter four's choice between waiting and being wrong."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(truth_l))
            for mk, k in zip("abc", (1, 2, 3)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*tab.cells[k])))
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        row = led[-1]
        head = label(r"Ledger row 17", font_size=36).to_edge(UP, buff=0.35)
        tab = ledger_table(led, shown=len(led), highlight=(len(led) - 1,), font_size=20, row_h=0.27,
                           label_width=4.8).scale(0.84).move_to(UP * 0.7)
        notes = VGroup(
            label(rf"the Job as a stream on one machine: \ {row['seconds']:.1f} s for all thirty books, \ exact", font_size=19,
                  color=HEAD),
            label(r"slower than the batch rows, \ but its answer is current after every book", font_size=19,
                  color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        for n in notes:
            if n.width > 12.8:
                n.width = 12.8
        with self.voiceover(
            "The ledger gets row seventeen. <bookmark mark='a'/> The Job as a stream on one machine: about "
            f"{row['seconds']:.0f} seconds for all thirty books, deduplicated and exact. <bookmark mark='b'/> It is "
            "slower than the best batch rows, because it does the bookkeeping a stream needs. What it buys is an "
            "answer that is current after every book, rather than after the last one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), FadeIn(tab.rows[:-1]))
            vo.wait_until("a")
            self.play(FadeIn(tab.rows[-1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM)
