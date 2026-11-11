from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(title, idea, part, col, w=3.1, h=1.55):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=21, color=col)
    i = wrapped_label(idea, w - 0.3, font_size=16, color=GREY_A)
    p = label(part, font_size=15, color=GREY_B)
    VGroup(t, i, p).arrange(DOWN, buff=0.1).move_to(frame)
    return VGroup(frame, t, i, p)


class Hook(VoiceoverScene):
    def construct(self):
        self.eight()
        self.method()
        self.plan()

    def eight(self):
        head = label(r"Eight systems, \ eight hard ideas", font_size=36).to_edge(UP, buff=0.3)
        specs = [(r"URL shortener", r"an ID space, \ and Zipf reads", r"Parts 17, 48", HEAD),
                 (r"news feed", r"fan-out on write or read", r"Parts 18, 47", DATA),
                 (r"chat", r"ordering per conversation", r"Parts 30, 38", YES),
                 (r"web crawler", r"politeness and dedup", r"Parts 20, 47", LAM),
                 (r"ride-hailing", r"matching as assignment", r"Parts 18, 48", KERN),
                 (r"video platform", r"bitrate as control", r"Parts 37, 45", NO),
                 (r"payment ledger", r"$\sum = 0$, \ exactly once", r"Parts 39, 43", HEAD),
                 (r"collaborative editor", r"convergence", r"Part 39", DATA)]
        tiles = VGroup(*[tile(*s) for s in specs]).arrange_in_grid(rows=2, cols=4, buff=(0.25, 0.3))
        tiles.next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"each designed from the napkin up, \ each turning on one idea the series has already "
                             r"built, \ each stress-tested in simulation", 12.4, font_size=21, color=WHITE).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "This part designs eight systems that almost everyone uses. <bookmark mark='a'/> A URL shortener, a news "
            "feed, a chat service and a web crawler. <bookmark mark='b'/> A ride-hailing dispatcher, a video "
            "platform, a payment ledger and a collaborative editor. <bookmark mark='c'/> Each one turns on a single "
            "hard idea, and every one of those ideas is something this series has already built: the birthday bound, "
            "fan-out, logical clocks, Bloom filters, the assignment problem, control loops, idempotency and CRDTs. "
            "Each design starts on a napkin and ends in a simulation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles[:4]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles[4:]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def method(self):
        head = label(r"The method, \ from Part 48", font_size=36).to_edge(UP, buff=0.3)
        steps = [(r"requirements", r"what it must do, \ and how well \ (SLOs, \ Part 50)", WHITE),
                 (r"the napkin", r"peak QPS, \ storage, \ bandwidth", HEAD),
                 (r"API and data model", r"the calls, \ the keys, \ the access patterns", DATA),
                 (r"high-level design", r"the blocks, \ and a request's path through them", YES),
                 (r"the hard part", r"one deep dive, \ with numbers", NO),
                 (r"trade-offs", r"consistency, \ latency, \ cost, \ complexity, \ operability", LAM)]
        boxes = VGroup()
        for t, d, c in steps:
            r = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            g = VGroup(label(t, font_size=21, color=c), wrapped_label(d, 3.3, font_size=16, color=GREY_A)).arrange(
                DOWN, buff=0.1).move_to(r)
            boxes.add(VGroup(r, g))
        boxes.arrange_in_grid(rows=2, cols=3, buff=(0.45, 0.45)).next_to(head, DOWN, buff=0.6)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.06, color=GREY_C,
                                stroke_width=2) for i in (0, 1, 3, 4)],
                        Arrow(boxes[2].get_bottom(), boxes[5].get_top(), buff=0.06, color=GREY_C, stroke_width=2))
        with self.voiceover(
            "Every case follows the method of Part 48. <bookmark mark='a'/> Requirements first: what the system must "
            "do, and how well, in numbers. <bookmark mark='b'/> Then the napkin: peak queries per second, storage "
            "and bandwidth. Then the interface and the data model, the calls and the keys. "
            "<bookmark mark='c'/> Then a high-level design built from the blocks, with one request traced through "
            "it. <bookmark mark='d'/> Then the hard part, the one place where the design could fail, examined with "
            "numbers. And last, the trade-offs it forced, because there is never a design without them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]))
            vo.wait_until("b")
            self.play(FadeIn(boxes[1]), GrowArrow(arrows[0]), FadeIn(boxes[2]), GrowArrow(arrows[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[4]), FadeIn(boxes[5]))
            self.play(FadeIn(boxes[3]))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[2]), FadeIn(boxes[4]), GrowArrow(arrows[3]))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ System Design II: \ Case Studies", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"a shortener's ID space and a feed's fan-out",
            r"ordering, \ receipts and offline sync in chat",
            r"a crawler's politeness and a dispatcher's matching",
            r"adaptive bitrate as a control problem",
            r"a ledger whose sum is always zero",
            r"editors that converge; \ a Dynamo; \ the Job at scale",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 49 of Computer Science, Built. <bookmark mark='a'/> We will size a shortener's identifiers "
            "and choose a feed's fan-out on a power-law graph; order a chat's messages; keep a crawler polite; match "
            "riders to drivers as an assignment problem; adapt a video's bitrate as a control loop; keep a ledger "
            "that always sums to zero; make two editors converge; assemble a Dynamo-style store; and run the Job at "
            "a million books a day."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (KERN, LAM, NO, YES)
