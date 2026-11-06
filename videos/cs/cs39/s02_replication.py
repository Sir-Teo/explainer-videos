from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, box, grid_table, load, trace)


class Replication(VoiceoverScene):
    def construct(self):
        self.card()
        self.latency()
        self.styles()
        self.lag()
        self.conflicts()

    def card(self):
        card = chapter_card(1, r"The datacenter, \ and replication", r"Why keep copies, and what do copies cost?",
                            lit=(2009, 2009), extra=((2009, r"Barroso and H\"olzle: \\ The Datacenter as a "
                                                           r"Computer"),), part=PART)
        with self.voiceover("Chapter one. The datacenter, and replication."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    @staticmethod
    def human(s):
        for unit, k in (("years", 3.15e7), ("days", 86400), ("hours", 3600), ("minutes", 60)):
            if s >= k:
                return f"{s / k:.0f} {unit}" if s / k >= 10 else f"{s / k:.1f} {unit}"
        return f"{s:.0f} s"

    def latency(self):
        l = load("latency")
        head = label(r"If one CPU cycle took a second", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r["name"], (f"{r['seconds'] * 1e9:.1f} ns" if r["seconds"] < 1e-6 else
                             f"{r['seconds'] * 1e6:.0f} $\\mu$s" if r["seconds"] < 1e-3 else
                             f"{r['seconds'] * 1e3:.0f} ms" if r["seconds"] < 1 else f"{r['seconds']:.0f} s"),
                 self.human(r["scaled_s"])] for r in l["rows"]]
        tab = grid_table([r"event", r"real time", r"if a cycle were 1 second"], rows, widths=[5.0, 2.4, 3.6],
                         row_h=0.42, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][2].set_color(YES if k <= 4 else (KERN if k <= 8 else NO))
        foot = wrapped_label(r"a request that crosses the datacenter costs what 1.5 million cycles of local work cost; \ "
                             r"one that crosses an ocean, \ half a billion. \ Every design in this part is a way of "
                             r"paying fewer of those trips.", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Luiz Barroso and Urs Hölzle called the modern datacenter a single computer: tens of thousands of "
            "servers, one program. Its distances are what shape everything in this part. Stretch time so that one "
            "processor cycle takes a second. <bookmark mark='a'/> Then a cache hit is three seconds and main memory "
            "five minutes. A round trip to another machine in the same building is seventeen days; reading a random "
            "spot on a solid-state disk, three and a half; a spinning disk's seek, a year. A round trip from "
            "California to Europe takes fifteen years, and a TCP retransmission timeout a century. "
            "<bookmark mark='b'/> So every protocol here is judged in round trips, and every clever idea is a way "
            "to make fewer of them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(1, len(rows) + 1)],
                                  lag_ratio=0.2), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def styles(self):
        head = label(r"Three ways to keep copies", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(box(3.4, 0.8, r"single leader", DATA, font_size=22),
                   wrapped_label(r"all writes go to one replica, \ which streams its log to followers \ "
                                 r"(PostgreSQL, \ MySQL, \ Raft): \ simple, \ but the leader is a bottleneck and a "
                                 r"single point of failover", 8.0, font_size=20, color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(3.4, 0.8, r"multi-leader", KERN, font_size=22),
                   wrapped_label(r"a leader per datacenter, \ replicating to each other: \ local writes everywhere, \ "
                                 r"and \textbf{conflicts} when two leaders accept different writes", 8.0, font_size=20,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(3.4, 0.8, r"leaderless", LAM, font_size=22),
                   wrapped_label(r"clients write to and read from several replicas at once \ (Dynamo, \ Cassandra): "
                                 r"\ no failover at all, \ correctness by quorum", 8.0, font_size=20,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        foot = wrapped_label(r"\textbf{synchronous} replication waits for followers \ (durable, \ slow, \ blocked by one "
                             r"dead follower); \ \textbf{asynchronous} does not \ (fast, \ but followers lag, \ and a "
                             r"failover can lose acknowledged writes)", 12.4, font_size=20, color=HEAD).to_edge(DOWN,
                                                                                                         buff=0.4)
        with self.voiceover(
            "Data is copied for three reasons: to survive failures, to serve more reads, and to be near users. "
            "There are three basic ways. <bookmark mark='a'/> A single leader takes every write and streams its "
            "log to followers, as PostgreSQL and MySQL do, and as Raft does. <bookmark mark='b'/> Several leaders, "
            "one per datacenter, let every region write locally, at the price of conflicts when two leaders accept "
            "different writes to the same thing. <bookmark mark='c'/> Or no leader at all: clients write to several "
            "replicas and read from several, and correctness comes from counting, as in Amazon's Dynamo. "
            "<bookmark mark='d'/> Independently, the leader can wait for followers before acknowledging a write, "
            "which is durable but slow and stalls if one follower dies, or not wait, which is fast, but leaves the "
            "followers behind."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lag(self):
        L = load("lag")
        head = label(r"Replication lag: \ reading your own writes", font_size=36).to_edge(UP, buff=0.3)
        rows = L["rows"]
        g = axes([0, 500, 100], [0, 0.7, 0.1], x_length=6.6, y_length=3.8, x_label=r"ms between the write and the "
                 r"read", y_label=r"reads that miss your own write", xticks=range(0, 501, 100),
                 yticks=(0.2, 0.4, 0.6), fy=lambda v: f"{v * 100:.0f}\\%").move_to([-2.8, -0.4, 0])
        ax = g.ax
        tr = VGroup(trace(ax, [(r["t_ms"], r["violations"]) for r in rows], NO, width=3),
                    *[Dot(ax.c2p(r["t_ms"], r["violations"]), radius=0.06, color=NO) for r in rows])
        notes = VGroup(
            wrapped_label(r"one leader, \ two asynchronous followers lagging 100 ms on average; \ the user's read goes "
                          r"to a random replica", 5.4, font_size=19, color=GREY_A),
            wrapped_label(rf"immediately after posting: \ {rows[0]['violations'] * 100:.0f}\% of reads do not show the "
                          r"post; \ after 200 ms, \ " + f"{rows[4]['violations'] * 100:.0f}" + r"\%", 5.4,
                          font_size=20, color=NO),
            wrapped_label(r"remedies: \ read your own data from the leader; \ remember the last write's position "
                          r"and wait for a replica that has it; \ \textbf{monotonic reads}: \ stick to one replica",
                          5.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Asynchronous followers lag, and users notice. Here is one leader and two followers that apply each "
            "write a hundred milliseconds late on average, and a user who posts something and immediately reloads "
            "the page, with the read sent to any replica. <bookmark mark='a'/> Two thirds of the time, the post is "
            "missing: the read went to a follower that has not seen it yet. After two hundred milliseconds, still "
            "nine percent. <bookmark mark='b'/> The usual remedies are small and specific: read your own data from "
            "the leader, or remember the position of your last write and wait for a replica that has reached it, "
            "and always read from the same replica, so that time never seems to run backwards."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(tr), FadeIn(notes[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def conflicts(self):
        c = load("lww")
        rows_d = c["rows"]
        head = label(r"Two leaders, \ one key", font_size=36).to_edge(UP, buff=0.3)
        x0, x1 = -6.2, 0.6
        yA, yB = 2.0, 0.6
        lanes = VGroup(Line([x0, yA, 0], [x1, yA, 0], color=GREY_C), Line([x0, yB, 0], [x1, yB, 0], color=GREY_C))
        names = VGroup(label(r"Europe", font_size=22, color=GREY_A).next_to(lanes[0], LEFT, buff=0.12),
                       label(r"US", font_size=22, color=GREY_A).next_to(lanes[1], LEFT, buff=0.12))

        def w(x, y, txt, col):
            d = Dot([x, y, 0], radius=0.09, color=col)
            t = label(txt, font_size=19, color=col).next_to(d, UP if y == yA else DOWN, buff=0.1)
            return VGroup(d, t)

        def rep(xa, ya, yb, col):
            return Arrow([xa, ya, 0], [xa + 0.9, yb, 0], buff=0.1, stroke_width=2, color=col,
                         max_tip_length_to_length_ratio=0.12)
        p1 = VGroup(w(-5.3, yA, r"cart $=$ \{book\}", HEAD), w(-5.0, yB, r"cart $=$ \{pen\}", LAM),
                    VGroup(rep(-5.3, yA, yB, GREY_B)), VGroup(rep(-5.0, yB, yA, GREY_B)))
        l1 = label(r"concurrent: \ neither saw the other", font_size=20, color=NO).move_to([-4.9, -0.25, 0])
        p2 = VGroup(w(-2.4, yB, r"ts 1{,}100 \ (clock 100 ms fast)", LAM), VGroup(rep(-2.4, yB, yA, GREY_B)),
                    w(-0.6, yA, r"ts 1{,}060, \ saw it", HEAD))
        l2 = label(r"inversion: \ the newer write loses", font_size=20, color=NO).move_to([-1.3, -0.7, 0])
        rows = [[f"{r['skew_ms']} ms", f"{r['concurrent'] * 100:.1f}\\%", f"{r['inversions'] * 100:.1f}\\%",
                 f"{r['lww_lost'] * 100:.1f}\\%", r"0, \ siblings kept"] for r in rows_d]
        tab = grid_table([r"clock skew", r"concurrent", r"inverted", r"lost by LWW", r"version vectors"], rows,
                         widths=[2.0, 2.0, 1.9, 2.2, 2.8], row_h=0.42, font_size=20, mono_cols=())
        tab.move_to([0, -2.35, 0])
        for k in range(1, len(rows) + 1):
            tab.cells[k][3].set_color(NO)
            tab.cells[k][4].set_color(YES)
        side = VGroup(
            wrapped_label(r"each region writes the key 5 times a second; \ a write takes 50 ms to reach the other",
                          4.6, font_size=19, color=GREY_A),
            wrapped_label(r"\textbf{last writer wins} keeps the larger timestamp and silently drops the other: \ "
                          r"Cassandra's default", 4.6, font_size=20, color=NO),
            wrapped_label(r"\textbf{version vectors} \ (one counter per replica, \ Part 38's vector clocks) \ tell "
                          r"``saw it'' from ``concurrent'', \ and hand both siblings to the application to merge, \ "
                          r"as Dynamo and Riak do", 4.6, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.5, 1.15, 0])
        with self.voiceover(
            "With more than one leader, two regions can accept writes to the same key at the same moment. "
            "<bookmark mark='a'/> Here Europe sets a shopping cart to a book while the US sets it to a pen; each "
            "write takes fifty milliseconds to cross, so neither saw the other. They are concurrent, and something "
            "must decide. <bookmark mark='b'/> The simplest rule, last writer wins, keeps the larger timestamp and "
            "silently throws the other away. Worse, timestamps come from clocks. <bookmark mark='c'/> If the US "
            "clock runs a hundred milliseconds fast, a write from Europe that had already seen the American one can "
            "still carry a smaller timestamp, and lose: the newer value is discarded for the older. "
            "<bookmark mark='d'/> We simulated a busy key written five times a second from each region. About one "
            "write in five is concurrent with another, so last writer wins silently loses one write in ten, and with "
            "clock skew beyond the replication delay, inversions add more: almost a quarter of all writes at a "
            "quarter of a second of skew. <bookmark mark='e'/> Version vectors, Part 38's vector clocks with one "
            "counter per replica, tell the two cases apart exactly. Causally later writes replace earlier ones, and "
            "concurrent writes are kept side by side as siblings for the application to merge, as Dynamo and Riak "
            "do. Merging them automatically is what the next chapter is about."
        ) as vo:
            self.play(FadeIn(head), Create(lanes), FadeIn(names), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(p1[0]), FadeIn(p1[1]))
            self.play(GrowArrow(p1[2][0]), GrowArrow(p1[3][0]), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(p2[0]), GrowArrow(p2[1][0]))
            self.play(FadeIn(p2[2]), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(tab))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM,)
