from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, PROCC, YES, axes, box, grid_table, load,
                                   trace)


class OurRaft(VoiceoverScene):
    def construct(self):
        self.card()
        self.invariants()
        self.upclose()
        self.campaign()
        self.rsm()
        self.reads()

    def card(self):
        card = chapter_card(8, r"Our Raft, \ attacked", r"How do you know a consensus implementation is right?",
                            lit=(1990, 2014), extra=((1990, r"Schneider: \ state machine replication"),
                                                     (2013, r"Kingsbury: \ Jepsen")), part=PART)
        with self.voiceover("Chapter eight. Our Raft, attacked."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def invariants(self):
        head = label(r"Four invariants, \ checked after every event", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(box(3.6, 0.75, r"election safety", YES, font_size=21),
                   wrapped_label(r"at most one leader in any term", 8.0, font_size=21, color=WHITE)).arrange(
                RIGHT, buff=0.5),
            VGroup(box(3.6, 0.75, r"log matching", DATA, font_size=21),
                   wrapped_label(r"same index and term $\Rightarrow$ identical up to there", 8.0, font_size=21,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(3.6, 0.75, r"leader completeness", HEAD, font_size=21),
                   wrapped_label(r"every committed entry is in every later leader's log", 8.0, font_size=21,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(3.6, 0.75, r"state machine safety", LAM, font_size=21),
                   wrapped_label(r"no two servers apply different commands at the same index", 8.0, font_size=21,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.55)
        foot = wrapped_label(r"our servers keep term, \ vote and log across crashes \ (as if on disk) \ and lose "
                             r"everything else; \ messages are delayed 5 to 80 ms, \ 10\% are lost, \ partitions "
                             r"come and go", 12.4, font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Our Raft is about three hundred lines of Python, following the paper's one-page summary of the rules. "
            "Correctness is not something you can see by reading it, so we check, after every single event, the "
            "four properties the paper proves. <bookmark mark='a'/> Election safety: at most one leader per term. "
            "<bookmark mark='b'/> Log matching. <bookmark mark='c'/> Leader completeness: a committed entry is in "
            "the log of every later leader. <bookmark mark='d'/> And the one that users care about: no two servers "
            "ever apply different commands at the same position. <bookmark mark='e'/> Servers keep their term, "
            "their vote and their log across crashes, as if on disk, and forget everything else; messages are "
            "delayed, lost one in ten, and cut off by partitions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def upclose(self):
        h = load("hook")
        head = label(r"The storm of the opening, \ up close", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 9, 1], [0, 250, 50], x_length=10.6, y_length=4.0, x_label=r"seconds",
                 y_label=r"commit index \ (entries known committed)", xticks=range(0, 10),
                 yticks=(50, 100, 150, 200, 250)).move_to(DOWN * 0.3)
        ax = g.ax
        lines = VGroup()
        for i in range(5):
            pts = [(t, nodes[i][3]) for t, nodes in h["timeline"]]
            lines.add(trace(ax, pts, PROCC[i], width=2.4))
        marks = VGroup()
        for t, kind, kw in h["events"]:
            if kind in ("crash", "partition", "heal"):
                c = {"crash": NO, "partition": KERN, "heal": YES}[kind]
                marks.add(DashedLine(ax.c2p(t, 0), ax.c2p(t, 250), color=c, stroke_width=1.4, dash_length=0.06),
                          label(kind, font_size=15, color=c).next_to(ax.c2p(t, 250), UP, buff=0.05))
        notes = VGroup(
            label(r"a crashed server's commit index drops to 0: \ it is volatile, \ relearned from the leader on "
                  r"restart", font_size=18, color=GREY_A),
            label(r"during the partition no line rises: \ neither side has a majority, \ so nothing commits", font_size=18,
                  color=KERN),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Here is the storm from the opening again, now as each server's commit index: how many log entries "
            "it knows to be committed. <bookmark mark='a'/> In calm weather the five lines climb together, a few "
            "milliseconds apart. When the leader crashes, its line drops to zero, because the commit index is not "
            "saved to disk, and the others pause for a fifth of a second, elect a new leader and climb on. "
            "<bookmark mark='b'/> Through the partition every line is flat. The side with the old leader has only "
            "two servers, and the other side has two live servers of three, so neither has a majority of five. "
            "Raft chooses consistency over availability, exactly as Part 39's CAP theorem says something must. "
            "<bookmark mark='c'/> When the network heals, the restarted servers relearn everything from the new "
            "leader, and within a second all five lines are together again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(marks))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.15), run_time=4)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Indicate(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def campaign(self):
        r = load("raft")
        head = label(r"A thousand storms each", font_size=36).to_edge(UP, buff=0.3)
        spec = [("correct", r"correct Raft", r"random"), ("correct targeted", r"correct Raft", r"targeted"),
                ("commit-old-term", r"commits old-term entries by counting", r"random"),
                ("no-log-check", r"votes without the log check", r"random"),
                ("forget-vote", r"forgets its vote on restart", r"random"),
                ("forget-vote targeted", r"forgets its vote on restart", r"targeted")]
        rows = []
        for key, name, mode in spec:
            x = r[key]
            kinds = ", ".join(sorted(x["kinds"]))
            rows.append([name, mode, f"{x['violating_runs']}", kinds if kinds else r"--"])
        tab = grid_table([r"implementation", r"faults", r"runs broken", r"invariants violated"], rows,
                         widths=[4.6, 1.6, 1.8, 4.6], row_h=0.46, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k, (key, _, _) in enumerate(spec, start=1):
            c = YES if r[key]["violating_runs"] == 0 and key.startswith("correct") else (
                NO if r[key]["violating_runs"] else KERN)
            for j in range(4):
                tab.cells[k][j].set_color(c)
        c = r["correct"]
        lines = VGroup(
            wrapped_label(rf"each run: \ 6 s, \ about 8 faults a second; \ on average {c['mean_committed']:.0f} commands "
                          rf"committed, \ {c['mean_terms']:.0f} terms, \ {c['mean_messages']:.0f} messages", 12.4,
                          font_size=20, color=GREY_A),
            wrapped_label(r"\textbf{targeted}: \ a voter crashes and restarts the moment it has voted, \ the one "
                          r"moment when forgetting the vote matters", 12.4, font_size=20, color=KERN),
            wrapped_label(r"a bug random faults never found, \ found in 87 runs of 1{,}000 by one well-aimed fault",
                          12.4, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "We ran a thousand six-second storms against correct Raft and against three versions with one rule "
            "broken each. <bookmark mark='a'/> Correct Raft: no violation in any run, with random faults or with "
            "targeted ones. <bookmark mark='b'/> A version that commits older terms' entries by counting replicas, "
            "the Figure 8 trap: broken once in a thousand. <bookmark mark='c'/> A version whose voters skip the "
            "up-to-date check: broken in eight hundred and seventy-seven, losing committed entries all over the "
            "place. <bookmark mark='d'/> A version that forgets its vote when it restarts, so it can vote twice in "
            "a term: random faults never caught it. But aim one fault, crash a voter in the instant after it "
            "votes, and eighty-seven runs elected two leaders in the same term. <bookmark mark='e'/> Testing "
            "distributed systems is a search problem, and where you look matters more than how long."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[4])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[5])), FadeIn(VGroup(*tab.cells[6])), FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def rsm(self):
        head = label(r"Replicated state machines", font_size=36).to_edge(UP, buff=0.3)
        log = VGroup(*[VGroup(Square(0.7, stroke_color=YES, stroke_width=2, fill_color=YES, fill_opacity=0.2),
                              label(t, font_size=16, color=YES)) for t in ("x=1", "y=2", "x+=y", "del y")]).arrange(
            RIGHT, buff=0.06).next_to(head, DOWN, buff=0.6)
        sms = VGroup(*[box(2.4, 0.9, rf"replica {i + 1}: \ x = 3", DATA, font_size=18) for i in range(3)]).arrange(
            RIGHT, buff=0.8).next_to(log, DOWN, buff=1.0)
        arrows = VGroup(*[Arrow(log.get_bottom(), s.get_top(), buff=0.1, color=GREY_B, stroke_width=2) for s in sms])
        lines = VGroup(
            wrapped_label(r"\textbf{Schneider} \ (1990): \ deterministic state machines, \ started equal, \ fed the "
                          r"same commands in the same order, \ stay equal. \ Consensus orders the commands.", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"commands must be deterministic: \ no clocks, \ no random numbers, \ no iteration over "
                          r"hash tables in a seed-dependent order \ (Part 17)", 12.4, font_size=21, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "What is the log for? Fred Schneider's state machine approach, of 1990. <bookmark mark='a'/> If every "
            "replica starts in the same state and applies the same deterministic commands in the same order, every "
            "replica ends in the same state. Consensus supplies the order. Any service, a lock server, a key-value "
            "store, a configuration database, can be made fault-tolerant this way. <bookmark mark='b'/> The "
            "commands must really be deterministic: no reading the clock, no random numbers, not even iterating "
            "over a hash table whose order depends on a random seed, as Part 17's tables do. etcd, ZooKeeper and "
            "Consul are exactly this, and Kubernetes keeps its whole state in etcd."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(x) for x in log], lag_ratio=0.15))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(s)) for a, s in zip(arrows, sms)],
                                  lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def reads(self):
        head = label(r"Reading without lying", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"a leader that answers reads from its own state may be \textbf{deposed} without knowing "
                          r"it: \ partitioned away, \ while a new leader commits writes", 12.4, font_size=25,
                          color=NO),
            wrapped_label(r"\textbf{linearizable reads}: \ confirm leadership with a round of heartbeats to a "
                          r"majority before answering \ (ReadIndex), \ or put the read in the log", 12.4,
                          font_size=25, color=YES),
            wrapped_label(r"\textbf{leases}: \ followers promise not to elect anyone for a lease period, \ so the "
                          r"leader can answer alone \ --- \ if clocks drift by less than the safety margin", 12.4,
                          font_size=25, color=HEAD),
            wrapped_label(r"with a 10 s lease and clocks drifting 100 ppm, \ the margin must exceed 2 ms; \ a paused "
                          r"process \ (a long garbage collection, \ Part 15) \ can break any lease", 12.4,
                          font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "One more trap: reads. <bookmark mark='a'/> A leader might answer a read from its own state, but it "
            "may have been deposed without knowing it, cut off by a partition while a new leader commits writes on "
            "the other side. Its answer would be stale. <bookmark mark='b'/> To be linearizable, the leader first "
            "confirms that it is still leader, with one round of heartbeats to a majority, or puts the read through "
            "the log like a write. <bookmark mark='c'/> Or it holds a lease: followers promise not to elect anyone "
            "else for some period, so the leader may answer alone until the lease runs out. That trades a round "
            "trip for an assumption about clocks. <bookmark mark='d'/> With a ten-second lease and clocks drifting "
            "by a hundred parts per million, the margin must exceed two milliseconds, which is easy, but a process "
            "paused for a long garbage collection, as in Part 15, can outlive any lease and wake up believing it "
            "still leads."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, LAM)
