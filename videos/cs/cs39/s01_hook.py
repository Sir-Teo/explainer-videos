from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, gantt, load)


class Hook(VoiceoverScene):
    def construct(self):
        self.job()
        self.plan()

    def job(self):
        j = load("job")
        r = j["runs"]["crash"]
        head = label(r"The Job on sixteen Pebbles", font_size=36).to_edge(UP, buff=0.3)
        g = gantt(r, y0=2.1, lane=0.24)
        T = g.t_max
        ax = Line([g.x0, g.y0 - 16 * g.lane, 0], [g.x0 + g.width, g.y0 - 16 * g.lane, 0], color=GREY_D)
        ticks = VGroup(*[label(f"{t:.1f} s", font_size=14, color=GREY_B).move_to(
            [g.x0 + t / T * g.width, g.y0 - 16 * g.lane - 0.2, 0]) for t in (0, 0.1, 0.2, 0.3, 0.4, 0.5)])
        cx = g.x0 + r["crash"][1] / T * g.width
        crash = DashedLine([cx, g.y0 + 0.2, 0], [cx, g.y0 - 16 * g.lane, 0], color=NO, dash_length=0.06)
        cl = label(r"Pebble 4 crashes", font_size=16, color=NO).next_to(crash, UP, buff=0.05)
        leg = VGroup(label(r"map", font_size=17, color=DATA), label(r"reduce", font_size=17, color=LAM),
                     label(r"lost with the crash", font_size=17, color=NO),
                     label(r"backup copy", font_size=17, color=GREY_C)).arrange(RIGHT, buff=0.5).to_edge(DOWN,
                                                                                                   buff=0.85)
        led = j["ledger"]
        row34 = next(x for x in led if x["part"] == 34)
        foot = label(rf"{r['time']:.2f} s, \ against {row34['seconds']:.2f} s on one Pebble; \ "
                     rf"{r['reexecuted']} finished map tasks run again; \ the answer identical to the one-machine "
                     r"Job", font_size=20, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The thirty novels, cut into forty-eight pieces and spread across sixteen Pebbles. Each Pebble counts "
            "the words in its pieces, the counts are shuffled so that every word goes to one place, and sixteen "
            "merges produce the answer: MapReduce, the way Google counted the web in 2004. <bookmark mark='a'/> "
            "Here is every task, on every machine, over time: maps in blue, then reduces in purple. "
            "<bookmark mark='b'/> At four tenths of a second, Pebble four dies. The task it was running is lost, "
            "and so are the outputs of the maps it had already finished, because they lived on its own disk. The "
            "master hands all of that work to the others. <bookmark mark='c'/> Near the end, idle machines run "
            "backup copies of the last slow tasks, and whichever copy finishes first wins. "
            "<bookmark mark='d'/> Six tenths of a second, against two point seven on one Pebble, with a machine lost "
            "along the way, and the twenty words and their counts identical to the one-machine Job's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.names), Create(ax), FadeIn(ticks), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in g.bars], lag_ratio=0.01), run_time=4)
            vo.wait_until("b")
            self.play(Create(crash), FadeIn(cl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Distributed Systems II: \ Scale", font_size=38).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the datacenter as a computer, \ and what its distances cost",
            r"replication: \ leaders, \ lag, \ quorums and staleness",
            r"consistency models, \ CAP precisely, \ and CRDTs that never conflict",
            r"partitioning: \ consistent hashing, \ Chord",
            r"transactions across machines: \ two-phase commit, \ Spanner's clocks",
            r"MapReduce, \ the tail at scale, \ and failures that feed themselves",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 39 of Computer Science, Built: Distributed systems at scale. <bookmark mark='a'/> At "
            "the scale of a datacenter, every guarantee has a price in latency or availability. We measure what "
            "replication costs and how stale its reads are, state the CAP theorem precisely and build data types "
            "that cannot conflict. We spread data with consistent hashing, commit across machines with two-phase "
            "commit and with Spanner's atomic clocks, run the Job as MapReduce, and watch one slow server in a "
            "hundred make most requests slow. "
            "Part 38 asked whether machines can agree at all. This part asks what agreement costs when there are "
            "thousands of machines, some always failing, and an ocean between them, and how much of it we can do "
            "without. Almost every system you use, from a search box to a shopping cart, is an answer to that "
            "question, and each answer is a choice about which anomalies its users are allowed to see. By the end we "
            "will have measured those choices, not just named them, and Act Seven will be complete."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (HEAD, KERN)
