from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def box(name, color, w=2.3, h=0.7, size=19):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2, fill_color=BG,
                         fill_opacity=1)
    return VGroup(r, label(name, font_size=size, color=color).move_to(r))


class Hook(VoiceoverScene):
    def construct(self):
        self.everywhere()
        self.pipes()
        self.two_places()
        self.plan()

    def everywhere(self):
        head = label(r"The same structure, \ again and again", font_size=36).to_edge(UP, buff=0.3)
        cells = VGroup(*[Square(0.55, stroke_color=GREY_B, stroke_width=1.5) for _ in range(12)]).arrange(RIGHT, buff=0)
        cells.move_to(UP * 1.4)
        nums = VGroup(*[label(f"{i}", font_size=16, color=GREY_B).next_to(c, UP, buff=0.08) for i, c in
                        enumerate(cells)])
        arrow = Arrow(cells[-1].get_right() + RIGHT * 0.1, cells[-1].get_right() + RIGHT * 1.0, buff=0, color=HEAD)
        al = label(r"append", font_size=18, color=HEAD).next_to(arrow, UP, buff=0.05)
        uses = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (r"Part 35: \ a database's write-ahead log", DATA),
            (r"Part 38: \ Raft's replicated log", YES),
            (r"Part 41: \ git's history, \ append-only and content-addressed", LAM),
            (r"Part 43: \ the transactional outbox", KERN))]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        uses.next_to(cells, DOWN, buff=0.7)
        quote = wrapped_label(r"Jay Kreps, \ ``The Log: \ what every software engineer should know about real-time "
                              r"data's unifying abstraction'' \ (LinkedIn, \ 2013)", 12.0, font_size=19,
                              color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A log, in the sense of this part, is the simplest data structure that remembers time: records "
            "appended one after another, each with a number, its offset, and never changed. <bookmark mark='a'/> "
            "We have met it again and again. A database writes every change to a log before it touches the data. "
            "Raft agrees on a log, and every replica applies it in order. Git's history is a log of snapshots. "
            "The outbox of Part 43 is a log of events. <bookmark mark='b'/> In 2013 Jay Kreps, who had built "
            "LinkedIn's data infrastructure, argued that the log is the unifying abstraction of real-time data: "
            "the right way to move data between all of a company's systems."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.08), FadeIn(nums))
            self.play(GrowArrow(arrow), FadeIn(al))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u, shift=RIGHT * 0.15) for u in uses], lag_ratio=0.5), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(quote))
        self.wait(0.4)
        self.clear_scene()

    def pipes(self):
        head = label(r"Pipes, \ or a log", font_size=36).to_edge(UP, buff=0.3)
        srcs = [r"orders DB", r"users DB", r"clicks", r"payments"]
        dsts = [r"search", r"cache", r"warehouse", r"fraud model"]
        left = VGroup(*[box(t, DATA) for t in srcs]).arrange(DOWN, buff=0.35).move_to([-5.2, -0.3, 0])
        right = VGroup(*[box(t, YES) for t in dsts]).arrange(DOWN, buff=0.35).move_to([-0.6, -0.3, 0])
        mesh = VGroup(*[Line(a.get_right(), b.get_left(), color=NO, stroke_width=1.5) for a in left for b in right])
        ml = label(r"$4 \times 4 = 16$ pipelines", font_size=20, color=NO).next_to(VGroup(left, right), UP, buff=0.3)
        left2 = left.copy().move_to([1.6, -0.3, 0]).scale(0.85)
        right2 = right.copy().move_to([6.0, -0.3, 0]).scale(0.85)
        hub = box(r"the log", HEAD, w=1.4, h=3.2, size=20).move_to([3.8, -0.3, 0])
        spokes = VGroup(*[Line(a.get_right(), hub.get_left(), color=HEAD, stroke_width=1.5) for a in left2],
                        *[Line(hub.get_right(), b.get_left(), color=HEAD, stroke_width=1.5) for b in right2])
        hl = label(r"$4 + 4 = 8$ connections", font_size=20, color=HEAD).next_to(VGroup(left2, right2), UP, buff=0.3)
        foot = wrapped_label(r"each consumer reads at its own pace, \ from its own offset, \ and can replay "
                             r"history; \ a new consumer starts from the beginning", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is the argument. <bookmark mark='a'/> A company has sources of data, databases and streams of "
            "clicks, and systems that need them: a search index, a cache, a warehouse, a fraud model. Connect each "
            "source to each consumer directly and you build sixteen pipelines, each with its own format and its own "
            "failures. <bookmark mark='b'/> Put a log in the middle instead. Every source appends to it, and every "
            "consumer reads from it: eight connections. <bookmark mark='c'/> Each consumer keeps its own position, "
            "reads at its own pace, and can go back and replay history. A new consumer starts at the beginning and "
            "catches up."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right))
            self.play(Create(mesh), FadeIn(ml), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(left2), FadeIn(right2), FadeIn(hub))
            self.play(Create(spokes), FadeIn(hl))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def two_places(self):
        head = label(r"Two places for every company's data", font_size=36).to_edge(UP, buff=0.3)
        logb = box(r"an append-only log", HEAD, w=4.0, h=0.9, size=22).move_to([-4.0, 0.8, 0])
        whb = box(r"a column-oriented warehouse", DATA, w=4.4, h=0.9, size=22).move_to([3.8, 0.8, 0])
        mid = box(r"stream processors", YES, w=3.0, h=0.8, size=20).move_to([0, 0.8, 0])
        arr = VGroup(Arrow(logb.get_right(), mid.get_left(), buff=0.05, color=GREY_B),
                     Arrow(mid.get_right(), whb.get_left(), buff=0.05, color=GREY_B))
        notes = VGroup(label(r"everything, \ as it happens", font_size=18, color=HEAD).next_to(logb, DOWN, buff=0.2),
                       label(r"answers, \ continuously", font_size=18, color=YES).next_to(mid, DOWN, buff=0.2),
                       label(r"questions about all of it", font_size=18, color=DATA).next_to(whb, DOWN, buff=0.2))
        hard = wrapped_label(r"the hard part is time: \ events arrive late, \ out of order, \ and more than once", 12.4,
                             font_size=24, color=NO).move_to(DOWN * 1.6)
        with self.voiceover(
            "So every company's data ends up in two places. <bookmark mark='a'/> An append-only log, recording "
            "everything as it happens. <bookmark mark='b'/> A column-oriented warehouse, laid out to answer "
            "questions about all of it at once. <bookmark mark='c'/> And between them, stream processors that "
            "compute answers continuously, as the data flows. <bookmark mark='d'/> The hard part, we will see, is "
            "time: events arrive late, out of order, and more than once, and a correct answer has to survive all "
            "three."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(logb), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(whb), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(mid), GrowArrow(arr[0]), GrowArrow(arr[1]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(hard))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Logs, \ Streams and Warehouses", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the partitioned log: \ offsets, \ keys, \ consumer groups",
            r"change data capture and event sourcing",
            r"event time, \ windows and watermarks",
            r"exactly-once state by barrier snapshots",
            r"columnar files: \ encodings and Dremel's levels",
            r"lakehouses, \ distributed joins, \ and the Job as a stream",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 46 of Computer Science, Built. <bookmark mark='a'/> We will build a partitioned log with "
            "consumer groups; turn a database's changes into a stream; give windows of events a notion of time that "
            "survives lateness; checkpoint a running computation so that it recovers with exactly-once state; take "
            "apart a columnar file down to its encodings and the levels that let nested data live in columns; and "
            "end with the Job as a live top twenty over a stream of novels."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN, LAM, NO, YES)
