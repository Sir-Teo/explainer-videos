from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace)


class Partition(VoiceoverScene):
    def construct(self):
        self.card()
        self.ring()
        self.balance()
        self.hot()
        self.chord()

    def card(self):
        card = chapter_card(4, r"Partitioning", r"Which machine holds which key, as machines come and go?",
                            lit=(1997, 2002), extra=((1997, r"Karger et al.: \ consistent hashing"),
                                                     (2001, r"Stoica et al.: \ Chord"),
                                                     (2002, r"Maymounkov and Mazi\`eres: \ Kademlia")), part=PART)
        with self.voiceover("Chapter four. Partitioning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ring(self):
        h = load("hashing")
        mv = h["moved"]
        head = label(r"The hash ring", font_size=36).to_edge(UP, buff=0.3)
        circle = Circle(radius=2.2, color=GREY_C, stroke_width=2).move_to([-3.4, -0.4, 0])
        rng = np.random.default_rng(3)
        angs = sorted(rng.uniform(0, 2 * math.pi, 6))
        cols = [DATA, LAM, KERN, YES, HEAD, NO]
        nodes = VGroup(*[Dot(circle.point_at_angle(a), radius=0.13, color=cols[i]) for i, a in enumerate(angs)])
        keys = VGroup()
        for a in rng.uniform(0, 2 * math.pi, 24):
            nxt = next((i for i, b in enumerate(angs) if b >= a), 0)
            keys.add(Dot(circle.point_at_angle(a) * 0 + circle.get_center() + 1.75 * np.array([math.cos(a),
                                                                                          math.sin(a), 0]),
                         radius=0.06, color=cols[nxt]))
        new = Dot(circle.point_at_angle((angs[2] + angs[3]) / 2), radius=0.15, color=WHITE)
        rows = [[r"modulo: \ $h(k) \bmod n$", f"{mv['modulo'] * 100:.0f}\\%"],
                [r"consistent hashing ring", f"{mv['ring'] * 100:.1f}\\%"],
                [r"jump hash \ (2014)", f"{mv['jump'] * 100:.1f}\\%"],
                [r"rendezvous hashing \ (1996)", f"{mv['rendezvous'] * 100:.1f}\\%"],
                [r"the minimum: \ $1/(n+1)$", f"{mv['ideal'] * 100:.1f}\\%"]]
        tab = grid_table([r"10 nodes $\to$ 11", r"keys moved"], rows, widths=[4.0, 1.8], row_h=0.42, font_size=19,
                         mono_cols=())
        tab.move_to([3.4, 0.4, 0])
        tab.cells[1][1].set_color(NO)
        for k in (2, 3, 4):
            tab.cells[k][1].set_color(YES)
        lines = wrapped_label(r"each key belongs to the first node clockwise from its hash; \ a new node takes keys "
                              r"only from its clockwise neighbour", 5.4, font_size=19, color=WHITE).move_to([3.4, -2.2, 0])
        with self.voiceover(
            "With more data than one machine holds, keys must be spread over many. The obvious rule, hash the key "
            "and take it modulo the number of machines, has a fatal flaw. <bookmark mark='a'/> Add an eleventh "
            "machine to ten, and ninety-one percent of all keys move. In 1997 David Karger and his colleagues, "
            "working on what became Akamai, proposed a ring instead. <bookmark mark='b'/> Hash the machines onto a "
            "circle, and hash each key onto the same circle; a key belongs to the first machine clockwise from it. "
            "<bookmark mark='c'/> A new machine lands somewhere on the circle and takes keys only from its "
            "neighbour. Adding the eleventh machine moves eight point six percent of the keys, close to the "
            "minimum possible, one eleventh. Jump hashing and rendezvous hashing achieve the same with less memory "
            "or simpler code."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), Create(tab.rule),
                      FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("a")
            self.play(Indicate(tab.cells[1][1], color=NO))
            vo.wait_until("b")
            self.play(Create(circle), FadeIn(nodes), LaggedStart(*[FadeIn(k) for k in keys], lag_ratio=0.05))
            vo.wait_until("c")
            self.play(FadeIn(new, scale=2), FadeIn(lines),
                      LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(2, 6)], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def balance(self):
        h = load("hashing")
        head = label(r"Virtual nodes", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{x['vnodes']}", f"{x['max_over_mean']:.2f}", f"{x['min_over_mean']:.2f}", f"{x['cv']:.2f}"]
                for x in h["loads"]]
        tab = grid_table([r"points per node", r"busiest / mean", r"idlest / mean", r"spread \ (CV)"], rows,
                         widths=[2.6, 2.4, 2.4, 2.2], row_h=0.46, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][1].set_color(NO if h["loads"][k - 1]["max_over_mean"] > 1.5 else YES)
        lines = VGroup(
            wrapped_label(r"with one point each, \ 10 nodes split the circle into very unequal arcs: \ the busiest "
                          r"holds 3.4 times its share \ (100{,}000 keys)", 12.4, font_size=21, color=NO),
            wrapped_label(r"give each node many points, \ and the arcs average out \ (the spread falls like "
                          r"$1/\sqrt{\text{points}}$): \ Dynamo and Cassandra use hundreds; \ bigger machines simply "
                          r"get more points", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "One problem remains. <bookmark mark='a'/> With one point per machine, ten machines cut the circle into "
            "very unequal arcs. In our test with a hundred thousand keys, the busiest machine held three point four "
            "times its share and the idlest an eighth. <bookmark mark='b'/> So each machine is placed on the circle "
            "many times, as virtual nodes. With two hundred and fifty-six points each, the busiest holds sixteen "
            "percent more than its share, and the spread keeps falling as one over the square root of the number of "
            "points. A machine twice as large simply gets twice as many points."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def chord(self):
        c = load("chord")
        head = label(r"Chord: \ finding a key with no directory", font_size=36).to_edge(UP, buff=0.3)
        rows = c["rows"]
        g = axes([0, 15, 2], [0, 9, 2], x_length=6.0, y_length=3.6, x_label=r"nodes \ (log$_2$)",
                 y_label=r"hops per lookup", xticks=range(4, 15, 2), yticks=(2, 4, 6, 8),
                 fx=lambda v: rf"$2^{{{int(v)}}}$").move_to([-3.0, -0.6, 0])
        ax = g.ax
        meas = VGroup(trace(ax, [(math.log2(r["n"]), r["mean"]) for r in rows], DATA, width=3),
                      *[Dot(ax.c2p(math.log2(r["n"]), r["mean"]), radius=0.06, color=DATA) for r in rows])
        half = trace(ax, [(math.log2(r["n"]), 0.5 * math.log2(r["n"]) + 1) for r in rows], GREY_B, width=2)
        notes = VGroup(
            wrapped_label(r"each node keeps \textbf{fingers}: \ the node responsible for (its id $+ 2^i$) for $i = 0, "
                          r"1, \dots$ \ --- \ 32 entries for $2^{32}$ ids", 5.4, font_size=19, color=WHITE),
            wrapped_label(r"forward each lookup to the farthest finger not past the key: \ the remaining distance at "
                          r"least halves each hop, \ so at most $\log_2 n$ hops", 5.4, font_size=19, color=YES),
            wrapped_label(rf"measured: \ {rows[0]['mean']:.1f} hops for 16 nodes, \ {rows[-1]['mean']:.1f} for "
                          rf"16{{,}}384: \ about $\tfrac12 \log_2 n + 1$ \ (grey)", 5.4, font_size=19, color=DATA),
            wrapped_label(r"\textbf{Kademlia} \ (2002) \ measures distance by XOR, \ symmetric: \ it runs BitTorrent's "
                          r"tracker-less peers and Ethereum's discovery", 5.4, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Inside one datacenter, a table of who owns which arc fits on every machine. Across millions of peers "
            "it does not. In 2001 Ion Stoica and his colleagues built Chord. <bookmark mark='a'/> Each node keeps a "
            "small table of fingers: the node responsible for its own identifier plus one, plus two, plus four, and "
            "so on, doubling, thirty-two entries in all. <bookmark mark='b'/> To find a key, a node forwards the "
            "lookup to its farthest finger that does not pass the key. The distance remaining at least halves with "
            "each hop, so a lookup takes at most log n hops. <bookmark mark='c'/> We built rings of sixteen to sixteen "
            "thousand nodes: lookups took on average about half of log n, plus one, under eight hops with sixteen "
            "thousand nodes. <bookmark mark='d'/> Kademlia measures distance by exclusive-or instead, which is "
            "symmetric, and runs BitTorrent's peer discovery to this day."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(meas), Create(half), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def hot(self):
        h = load("hot")
        head = label(r"Hot keys", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for r in h["rows"]:
            nm = r"uniform" if r["s"] == 0 else rf"Zipf, \ $s = {r['s']:g}$"
            rows.append([nm, f"{r['top_key_share'] * 100:.2g}\\%", f"{r['max_over_mean']:.1f}$\\times$",
                         f"{r['salted_max_over_mean']:.1f}$\\times$"])
        tab = grid_table([r"key popularity", r"hottest key's share", r"busiest shard / mean",
                          rf"top {h['salt_top']} keys split {h['salt_ways']} ways"], rows,
                         widths=[2.6, 2.8, 3.0, 3.8], row_h=0.46, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        for k in range(1, len(rows) + 1):
            v = h["rows"][k - 1]["max_over_mean"]
            tab.cells[k][2].set_color(NO if v > 1.5 else YES)
            tab.cells[k][3].set_color(YES if h["rows"][k - 1]["salted_max_over_mean"] < 2 else KERN)
        lines = VGroup(
            wrapped_label(rf"{h['keys']:,} keys hashed onto {h['shards']} shards, \ two million requests: \ hashing "
                          r"spreads \textit{keys} evenly, \ not \textit{requests}; \ one celebrity's key lands on one "
                          r"shard however good the hash", 12.4, font_size=21, color=NO),
            wrapped_label(r"remedy: \ split a hot key into sub-keys \ (a random suffix on each write, \ all read and "
                          r"merged), \ cache it in front, \ or replicate it more widely", 12.4, font_size=21,
                          color=YES),
            wrapped_label(r"\textbf{range partitioning} \ (Bigtable, \ HBase, \ Spanner) \ keeps scans cheap but "
                          r"invites a worse hot spot: \ keys that are timestamps send every new write to the last "
                          r"range", 12.4, font_size=21, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Even a perfect hash spreads keys evenly, not requests. Real popularity follows Zipf's law: the most "
            "popular key gets a large share of all traffic, the second half as much, and so on. "
            "<bookmark mark='a'/> We sent two million requests for a million keys to a hundred shards. With uniform "
            "popularity, the busiest shard is within four percent of the mean. With Zipf's exponent one, the hottest "
            "key alone carries seven percent of all requests, and its shard is almost eight times busier than "
            "average; at one point two, twenty times. This is the celebrity problem: one account followed by "
            "millions. <bookmark mark='b'/> The remedy is to split the hot key: add a random suffix to every write, "
            "so it spreads over twenty sub-keys, and have readers fetch and merge them all. Splitting only the ten "
            "hottest keys brings the worst shard, at exponent one, under two times the mean. Caching the key in front of the "
            "shards, or replicating it more widely, works for reads. <bookmark mark='c'/> Range partitioning, used "
            "by Bigtable, HBase and Spanner, keeps neighbouring keys together so that scans are cheap, but it "
            "invites an even worse hot spot: if keys are timestamps, every new write goes to the last range."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, NO)
