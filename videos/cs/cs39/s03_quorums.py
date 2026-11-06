from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load)


class Quorums(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.pbs()
        self.antientropy()
        self.hierarchy()
        self.cap()

    def card(self):
        card = chapter_card(2, r"Quorums and consistency", r"How many replicas must agree, and on what?",
                            lit=(2000, 2012), extra=((2000, r"Brewer: \ CAP"), (2002, r"Gilbert and Lynch"),
                                                     (2007, r"DeCandia et al.: \ Dynamo"),
                                                     (2012, r"Bailis et al.: \ PBS")), part=PART)
        with self.voiceover("Chapter two. Quorums and consistency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rule(self):
        head = label(r"$R + W > N$", font_size=40).to_edge(UP, buff=0.3)
        reps = VGroup(*[Circle(radius=0.4, color=GREY_B, stroke_width=2.5) for _ in range(5)]).arrange(RIGHT, buff=0.6)
        reps.move_to([0, 1.3, 0])
        for i in range(3):
            reps[i].set_fill(DATA, 0.4).set_stroke(DATA)
        wq = Brace(VGroup(*reps[:3]), UP, color=DATA)
        wl = label(r"written: \ $W = 3$", font_size=20, color=DATA).next_to(wq, UP, buff=0.05)
        rq = Brace(VGroup(*reps[2:]), DOWN, color=LAM)
        rl = label(r"read: \ $R = 3$", font_size=20, color=LAM).next_to(rq, DOWN, buff=0.05)
        lines = VGroup(
            wrapped_label(r"write to $W$ of the $N$ replicas, \ read from $R$, \ keep the value with the newest "
                          r"version: \ if $R + W > N$ every read set meets every write set, \ so some replica read "
                          r"has the latest write", 12.4, font_size=22, color=WHITE),
            wrapped_label(r"Dynamo's typical choice: \ $N = 3$, \ $R = W = 2$. \ To favour speed, \ $R = W = 1$, \ "
                          r"and reads may be stale.", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"\textbf{sloppy quorums}: \ when home replicas are unreachable, \ write to others and hand "
                          r"the data back later \ (``hinted handoff''): \ always writable, \ no longer strictly "
                          r"intersecting", 12.4, font_size=22, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Leaderless systems count. <bookmark mark='a'/> Write to W of the N replicas, read from R of them, and "
            "keep whichever value carries the newest version number. If R plus W is greater than N, every set of "
            "replicas you read overlaps every set that was written, so at least one replica you read has the "
            "latest write: the majorities of Paxos, generalized. <bookmark mark='b'/> Amazon's Dynamo, in 2007, "
            "typically used three replicas, writing and reading two. For speed you can write and read one, and "
            "accept that reads may be stale. <bookmark mark='c'/> And when a home replica is unreachable, Dynamo "
            "writes to some other machine that hands the data back later, so writes never fail, at the cost that "
            "quorums no longer strictly overlap."
        ) as vo:
            self.play(FadeIn(head), FadeIn(reps))
            vo.wait_until("a")
            self.play(GrowFromCenter(wq), FadeIn(wl))
            self.play(GrowFromCenter(rq), FadeIn(rl), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def pbs(self):
        q = load("quorum")
        head = label(r"How stale is ``eventually''?", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{r['N']}, {r['R']}, {r['W']}", r"yes" if r["strict"] else r"no",
                 *[f"{s * 100:.1f}\\%" for s in r["stale"]]] for r in q["rows"]]
        tab = grid_table([r"$N, R, W$", r"$R + W > N$", r"0 ms after", r"5 ms", r"20 ms", r"50 ms"], rows,
                         widths=[2.0, 2.0, 1.8, 1.6, 1.6, 1.6], row_h=0.42, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for k, r in enumerate(q["rows"], start=1):
            for j in range(2, 6):
                v = r["stale"][j - 2]
                tab.cells[k][j].set_color(YES if v == 0 else (NO if v > 0.05 else KERN))
        foot = wrapped_label(r"Bailis et al.'s \textbf{probabilistically bounded staleness}: \ replicas receive each write "
                             r"after random delays \ (mean 10 ms); \ 20{,}000 simulated reads per cell. \ Strict "
                             r"quorums are never stale; \ $R = W = 1$ is stale half the time at once, \ and almost "
                             r"never after 50 ms.", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Peter Bailis and his colleagues asked how stale non-strict quorums actually are. We simulated it: a "
            "write reaches each replica after a random delay averaging ten milliseconds, and a read starts some "
            "time after the write was acknowledged. <bookmark mark='a'/> When R plus W exceeds N, no read was ever "
            "stale, as the argument says. With three replicas, reading and writing one, a read issued at the "
            "instant of acknowledgement misses the write more than half the time; five milliseconds later, a "
            "third; fifty milliseconds later, three in a thousand. <bookmark mark='b'/> Eventual consistency is "
            "usually very soon, and now we can say how soon."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hierarchy(self):
        head = label(r"A map of consistency models", font_size=36).to_edge(UP, buff=0.3)
        levels = [(r"linearizable", NO, r"one copy, \ real-time order \ (Part 33)"),
                  (r"sequential", KERN, r"one order all agree on, \ not tied to real time"),
                  (r"causal", HEAD, r"effects never seen before their causes \ (Part 38's happened-before)"),
                  (r"session guarantees", LAM, r"read your writes, \ monotonic reads"),
                  (r"eventual", DATA, r"if writes stop, \ replicas converge")]
        boxes = VGroup()
        for i, (n, c, d) in enumerate(levels):
            b = box(3.6, 0.7, n, c, font_size=21)
            t = wrapped_label(d, 6.4, font_size=20, color=WHITE)
            boxes.add(VGroup(b, t).arrange(RIGHT, buff=0.5))
        boxes.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.5)
        arrow = Arrow(boxes[-1][0].get_left() + LEFT * 0.4, boxes[0][0].get_left() + LEFT * 0.4, buff=0,
                      color=GREY_B)
        al = label(r"stronger, \\ slower", font_size=17, color=GREY_B).next_to(arrow, LEFT, buff=0.1)
        foot = wrapped_label(r"stronger models need more coordination: \ linearizability needs a round trip to a "
                             r"majority per operation; \ causal consistency can be served by any replica that has "
                             r"seen the causes", 12.4, font_size=20, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "What should a read return? There is a ladder of answers. <bookmark mark='a'/> At the top, "
            "linearizability, from Part 33: the system behaves like a single copy, and every operation takes "
            "effect at one instant between its start and its end. Sequential consistency keeps a single order but "
            "loosens its tie to real time. Causal consistency promises only that you never see an effect before "
            "its cause. Session guarantees are promises to one user, like reading your own writes. And eventual "
            "consistency promises only that if writes stop, the replicas converge. <bookmark mark='b'/> Each step "
            "down needs less coordination. Linearizability needs a round trip to a majority for every operation; "
            "causal consistency can be served by any replica that has seen the causes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in boxes], lag_ratio=0.3), GrowArrow(arrow),
                      FadeIn(al), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def cap(self):
        c = load("cap")
        head = label(r"CAP, \ precisely", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"\textbf{Theorem} \ (Gilbert and Lynch, 2002). \ No system can guarantee both "
                          r"\textbf{linearizability} and \textbf{availability} \ (every request to a live replica "
                          r"gets an answer) \ in a network that may \textbf{partition}.", 12.4, font_size=22,
                          color=HEAD),
            wrapped_label(r"\textit{Proof.} \ Partition replicas $A$ and $B$. \ A client writes $x = 1$ at $A$; \ "
                          r"availability makes $A$ accept it. \ Another client reads $x$ at $B$; \ availability makes "
                          r"$B$ answer, \ without hearing from $A$: \ it returns the old value, \ which is not "
                          r"linearizable.", 12.4, font_size=21, color=WHITE),
            wrapped_label(rf"so during a partition choose: \ \textbf{{CP}} \ refuses the minority side \ "
                          rf"({(1 - c['cp']['available']) * 100:.0f}\% of requests in our example fail), \ or "
                          rf"\textbf{{AP}} \ answers everyone and reconciles conflicting writes later", 12.4,
                          font_size=21, color=NO),
            wrapped_label(r"\textbf{PACELC} \ (Abadi, 2012): \ if Partitioned, \ Availability or Consistency; \ "
                          r"Else, \ Latency or Consistency \ --- \ the everyday trade-off, \ since partitions are rare "
                          r"and round trips are not", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Eric Brewer conjectured in 2000, and Seth Gilbert and Nancy Lynch proved in 2002, the CAP theorem. "
            "<bookmark mark='a'/> No system can be both linearizable and available, meaning every request to a "
            "live replica gets an answer, in a network that can partition. <bookmark mark='b'/> The proof is two "
            "lines. Cut replica A off from replica B. A client writes at A, and availability forces A to accept. "
            "Another reads at B, and availability forces B to answer, without being able to hear from A, so it "
            "returns the old value. <bookmark mark='c'/> So during a partition, a system either refuses the side "
            "without a majority, as Raft did in the last part, or answers everyone and sorts out the conflicting "
            "writes afterwards. <bookmark mark='d'/> Daniel Abadi pointed out that the more important choice is "
            "the everyday one: partitions are rare, but round trips are constant, so even without partitions every "
            "system trades latency against consistency."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.5)
        self.clear_scene()

    def antientropy(self):
        m = load("merkle")
        head = label(r"Repairing replicas: \ Merkle trees", font_size=36).to_edge(UP, buff=0.3)
        # a small tree: 1 root, 4 children, 16 leaves; one leaf differs
        root = [-3.6, 2.0, 0]
        mids = [[-5.7 + 1.4 * i, 0.9, 0] for i in range(4)]
        leaves = [[-6.35 + 0.36 * j + 0.08 * (j // 4), -0.2, 0] for j in range(16)]
        bad_mid, bad_leaf = 2, 9
        tree = VGroup()
        edges = VGroup()
        nodes = VGroup()
        r0 = Square(0.34, color=NO, fill_opacity=0.5).move_to(root)
        nodes.add(r0)
        for i, p in enumerate(mids):
            sq = Square(0.3, color=NO if i == bad_mid else GREY_B, fill_opacity=0.5 if i == bad_mid else 0.15).move_to(p)
            nodes.add(sq)
            edges.add(Line(r0.get_bottom(), sq.get_top(), color=GREY_D, stroke_width=1.5))
        for j, p in enumerate(leaves):
            sq = Square(0.24, color=NO if j == bad_leaf else GREY_B,
                        fill_opacity=0.5 if j == bad_leaf else 0.15).move_to(p)
            nodes.add(sq)
            edges.add(Line(nodes[1 + j // 4].get_bottom(), sq.get_top(), color=GREY_D, stroke_width=1))
        tree.add(edges, nodes)
        cap = wrapped_label(r"each node hashes its children; \ compare roots, \ then descend only where the hashes "
                            r"differ", 5.6, font_size=18, color=GREY_A).move_to([-3.6, -0.95, 0])
        rows = [[f"{r['diffs']:,}", f"{r['merkle_bytes'] / 1024:,.1f} KB", f"{r['rounds']}",
                 r"yes" if r["found_all"] else r"no"] for r in m["rows"]]
        tab = grid_table([r"keys that differ", r"Merkle tree sends", r"round trips", r"all found"], rows,
                         widths=[2.1, 2.3, 1.7, 1.4], row_h=0.42, font_size=19, mono_cols=())
        tab.move_to([3.4, 0.9, 0])
        for k in range(1, len(rows) + 1):
            tab.cells[k][1].set_color(YES)
        foot = VGroup(
            wrapped_label(rf"two replicas of {m['keys']:,} keys; \ sending one 16-byte hash per key costs "
                          rf"{m['rows'][0]['naive_bytes'] / 2 ** 20:.0f} MB \ whatever the difference", 6.2,
                          font_size=18, color=NO),
            wrapped_label(r"the three repair paths of a Dynamo-style store: \ \textbf{read repair} \ (fix stale "
                          r"replicas seen during a read), \ \textbf{hinted handoff} \ (deliver writes held for a "
                          r"replica that was down), \ \textbf{anti-entropy} \ (compare Merkle trees in the "
                          r"background)", 6.2, font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -2.0, 0])
        with self.voiceover(
            "Sloppy quorums and failed replicas leave copies that disagree, and something must find the "
            "differences. Comparing two replicas of a million keys by sending one hash per key costs sixteen "
            "megabytes, even when nothing differs. <bookmark mark='a'/> Ralph Merkle's tree of hashes does better. "
            "Each leaf hashes a small range of keys, each node hashes its children, and the root summarizes "
            "everything. Two replicas compare roots; if they match, they are done. If not, they compare the "
            "children, and descend only into the branches whose hashes differ. <bookmark mark='b'/> With ten keys "
            "out of a million differing, our replicas exchanged eleven kilobytes in six round trips and found every "
            "one. Even with ten thousand differences, the cost stays below a third of the naive one. "
            "<bookmark mark='c'/> Dynamo-style stores combine three repairs: read repair fixes stale replicas that a "
            "read happens to notice, hinted handoff delivers writes held for a replica that was down, and "
            "anti-entropy compares Merkle trees in the background. The same trees check the integrity of Git "
            "repositories, of BitTorrent's pieces, and of certificate transparency logs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot[0]))
            vo.wait_until("a")
            self.play(Create(edges), FadeIn(nodes), FadeIn(cap), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA,)
