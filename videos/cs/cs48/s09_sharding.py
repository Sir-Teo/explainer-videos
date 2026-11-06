from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.compute import load as load39
from videos.cs.cs48.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box, mono, tag_box


class Sharding(VoiceoverScene):
    def construct(self):
        self.card()
        self.keys()
        self.hot()
        self.reshard()
        self.secondary()
        self.cross()

    def card(self):
        card = chapter_card(8, r"Sharding", r"How do you split data that no longer fits on one machine?",
                            lit=(2006, 2012), extra=((2006, r"Bigtable's tablets: \ ranges of keys"),
                                                     (2007, r"Dynamo: \ a hashed ring"),
                                                     (2012, r"Spanner: \ shards that move")), part=PART)
        with self.voiceover("Chapter eight. Sharding."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ ranges against hashes
    def keys(self):
        head = label(r"Ranges or hashes", font_size=36).to_edge(UP, buff=0.3)
        sq, step, base_y = 0.22, 0.26, -1.85

        def panel(cx, title, color, ranges):
            boxes = VGroup(*[module_box(r, KERN, w=1.25, h=0.5, font=17).move_to([cx + (i - 1.5) * 1.45, -2.2, 0])
                             for i, r in enumerate(ranges)])
            t = label(title, font_size=23, color=color).move_to([cx, 2.15, 0])
            stacks = [VGroup(*[Square(side_length=sq, stroke_width=0, fill_color=GREY_B, fill_opacity=0.7)
                               .move_to([b.get_x(), base_y + 0.12 + j * step, 0]) for j in range(2)]) for b in boxes]
            return VGroup(t, boxes), boxes, stacks
        rp, rboxes, rstacks = panel(-3.5, r"range partitioning", DATA,
                                    [r"keys 0--24", r"25--49", r"50--74", r"75--99"])
        hp, hboxes, hstacks = panel(3.5, r"hash partitioning", YES,
                                    [r"$h \bmod 4 = 0$", r"$= 1$", r"$= 2$", r"$= 3$"])
        divider = DashedLine([0, 2.4, 0], [0, -2.6, 0], color=GREY_D, stroke_width=1.5)
        hash_dest = [2, 0, 3, 1, 1, 3, 0, 2]
        new_r = [Square(side_length=sq, stroke_width=0, fill_color=HEAD, fill_opacity=1).move_to([-3.5, 1.6, 0])
                 for _ in hash_dest]
        new_h = [Square(side_length=sq, stroke_width=0, fill_color=HEAD, fill_opacity=1).move_to([3.5, 1.6, 0])
                 for _ in hash_dest]
        inl = label(r"new rows, \ keyed by time", font_size=18, color=HEAD).move_to([0, 1.6, 0])
        anims_r, anims_h, hcount = [], [], [2, 2, 2, 2]
        for k, d in enumerate(hash_dest):
            anims_r.append(new_r[k].animate.move_to([rboxes[3].get_x(), base_y + 0.12 + (2 + k) * step, 0]))
            anims_h.append(new_h[k].animate.move_to([hboxes[d].get_x(), base_y + 0.12 + hcount[d] * step, 0]))
            hcount[d] += 1
        hot = label(r"one shard takes every write", font_size=18, color=NO).move_to(
            [rboxes[3].get_x() - 0.4, base_y + 0.12 + 10 * step + 0.25, 0])
        scan_r = SurroundingRectangle(rboxes[1], color=YES, buff=0.07)
        scan_h = VGroup(*[SurroundingRectangle(b, color=NO, buff=0.07) for b in hboxes])
        notes = VGroup(
            wrapped_label(r"a range scan reads one or two shards", 6.0, font_size=19, color=YES).next_to(
                rboxes, DOWN, buff=0.3),
            wrapped_label(r"writes spread evenly; \ a range scan asks every shard", 6.0, font_size=19,
                          color=NO).next_to(hboxes, DOWN, buff=0.3),
        )
        mix = label(r"a common compromise: \ hash the user, \ sort within it: \ key = (user, time)", font_size=20,
                    color=HEAD).next_to(head, DOWN, buff=0.12)
        foot = note(r"illustrative", font_size=16).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Sharding splits one dataset across machines, each holding a part, and the choice that matters most "
            "is the shard key. <bookmark mark='a'/> Range partitioning gives each shard a contiguous run of keys, "
            "as Bigtable does with its tablets. But if the key grows with time, every new row lands on the last "
            "shard, and one machine takes all the writes. <bookmark mark='b'/> Hash partitioning scatters keys by "
            "their hash, Part 17's trick, and spreads the writes evenly. <bookmark mark='c'/> The price is order. "
            "A range scan touches one shard of a range-partitioned table, but every shard of a hashed one. "
            "<bookmark mark='d'/> Many systems compromise: hash a prefix, such as the user, and keep rows sorted "
            "within it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rp), FadeIn(hp), Create(divider), FadeIn(foot),
                      *[FadeIn(s) for s in rstacks + hstacks])
            vo.wait_until("a")
            self.add(*new_r)
            self.play(FadeIn(inl), LaggedStart(*anims_r, lag_ratio=0.3), run_time=3.0)
            self.play(FadeIn(hot), rboxes[3][0].animate.set_stroke(NO, width=3))
            vo.wait_until("b")
            self.add(*new_h)
            self.play(LaggedStart(*anims_h, lag_ratio=0.3), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(scan_r), FadeIn(notes[0]))
            self.play(Create(scan_h), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(mix))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ hot keys
    def hot(self):
        h = load39("hot")
        rows = h["rows"]
        head = label(r"Hot keys and celebrities", font_size=36).to_edge(UP, buff=0.3)
        Hmax, vmax, y0, x0, bw = 3.7, 20.0, -2.0, -6.0, 0.55
        bars_p, bars_s, vals_p, vals_s, names = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
        for i, r in enumerate(rows):
            x = x0 + i * 1.5
            for v, col, bars, vals, dx in ((r["max_over_mean"], NO, bars_p, vals_p, 0),
                                          (r["salted_max_over_mean"], YES, bars_s, vals_s, bw + 0.06)):
                b = Rectangle(width=bw, height=max(0.03, Hmax * v / vmax), stroke_width=0, fill_color=col,
                              fill_opacity=0.85)
                b.move_to([x + dx + bw / 2, y0 + b.height / 2, 0])
                bars.add(b)
                vals.add(label(rf"{v:.1f}", font_size=17, color=col).next_to(b, UP, buff=0.06))
            nm = r"uniform" if r["s"] == 0 else rf"$s = {r['s']:.1f}$"
            names.add(label(nm, font_size=18, color=GREY_A).next_to([x + bw + 0.03, y0, 0], DOWN, buff=0.15))
        axis = Line([x0 - 0.2, y0, 0], [x0 + 3 * 1.5 + 2 * bw + 0.3, y0, 0], color=GREY_C, stroke_width=1.5)
        ttl = label(r"busiest shard \ / \ mean shard", font_size=20, color=WHITE).move_to([-3.6, 2.45, 0])
        leg = VGroup(label(r"plain", font_size=18, color=NO), label(r"hottest 10 keys salted", font_size=18,
                                                                         color=YES)).arrange(RIGHT, buff=0.4)
        leg.next_to(ttl, DOWN, buff=0.12)
        zl = label(r"Zipf exponent of key popularity", font_size=17, color=GREY_B).next_to(names, DOWN, buff=0.15)
        # salting: one key split into many
        key = tag_box("celebrity", HEAD, size=17).move_to([3.6, 1.5, 0])
        subs = VGroup(*[tag_box(f"celebrity#{k}", HEAD, size=16) for k in (0, 1, 19)])
        dots = label(r"\dots", font_size=24, color=HEAD)
        subrow = VGroup(subs[0], subs[1], dots, subs[2]).arrange(RIGHT, buff=0.15).move_to([3.6, 0.35, 0])
        fan = VGroup(*[Arrow(key.get_bottom(), s.get_top(), buff=0.06, stroke_width=2, color=HEAD,
                             max_tip_length_to_length_ratio=0.15) for s in subs])
        s1 = next(r for r in rows if r["s"] == 1.0)
        notes = VGroup(
            wrapped_label(rf"at $s = 1$ the hottest key alone is {100 * s1['top_key_share']:.0f}\% of all "
                          r"requests, \ and no hash can split one key", 5.4, font_size=19, color=NO),
            wrapped_label(rf"salting: \ append one of {h['salt_ways']} suffixes per write, \ spread them, \ merge "
                          r"them on read", 5.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -1.35, 0])
        foot = note(rf"Part 39's simulation: \ {h['keys']:,} keys over {h['shards']} shards", font_size=16).to_edge(
            DOWN, buff=0.15)
        with self.voiceover(
            "Even a perfect hash cannot split a single key. <bookmark mark='a'/> In Part 39's simulation, a "
            "million keys are hashed over a hundred shards, and requests follow Zipf's law. With uniform "
            "popularity, the busiest shard carries one point zero four times the mean. <bookmark mark='b'/> With a "
            "Zipf exponent of one, the hottest key alone takes seven percent of all requests, and its shard "
            "nearly eight times the mean; at one point two, almost twenty. That is the celebrity problem: one "
            "account, followed by millions. <bookmark mark='c'/> The fix is to split the hot keys themselves. "
            "Append one of twenty suffixes to each of the ten hottest, spread the pieces, and merge them on read. "
            "<bookmark mark='d'/> At exponent one, the busiest shard falls below twice the mean. Part 49's feeds "
            "meet the celebrity again."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(names), FadeIn(ttl), FadeIn(zl), FadeIn(foot),
                      FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars_p[0], DOWN), FadeIn(vals_p[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v))
                                    for b, v in zip(bars_p[1:], vals_p[1:])], lag_ratio=0.4), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(key))
            self.play(LaggedStart(*[GrowArrow(a) for a in fan], lag_ratio=0.2), FadeIn(subrow), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(leg[1]), LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v))
                                                    for b, v in zip(bars_s, vals_s)], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ resharding
    def reshard(self):
        mv = load39("hashing")["moved"]
        head = label(r"Resharding", font_size=36).to_edge(UP, buff=0.3)
        xs = [-5.9, -4.3, -2.7, -1.1]
        cols = [DATA, KERN, LAM, YES]
        nodes = VGroup(*[module_box(rf"node {c}", col, w=1.35, h=0.5, font=18).move_to([x, 2.35, 0])
                         for c, col, x in zip("ABCD", cols, xs)])

        def slot(n, k):
            return [xs[n] - 0.27 + (k % 2) * 0.54, 1.75 - (k // 2) * 0.54, 0]
        parts = []
        for n in range(3):
            for k in range(8):
                p = n * 8 + k
                sq = VGroup(Square(side_length=0.46, stroke_width=0, fill_color=cols[n], fill_opacity=0.55),
                            mono(f"p{p}", size=16, color=WHITE))
                sq[1].move_to(sq[0])
                parts.append(sq.move_to(slot(n, k)))
        parts = VGroup(*parts)
        moving = [(n, k) for n in range(3) for k in (6, 7)]
        moves = [parts[n * 8 + k].animate.move_to(slot(3, i)) for i, (n, k) in enumerate(moving)]
        # keys moved when an eleventh machine joins ten
        bars = VGroup()
        for i, (nm, v, col) in enumerate(((r"hash mod $N$", mv["modulo"], NO), (r"hash ring", mv["ring"], KERN),
                                          (r"ideal, \ 1/11", mv["ideal"], YES))):
            y = 1.75 - i * 0.6
            n_ = label(nm, font_size=19, color=col).move_to([1.9, y, 0]).align_to([0.8, 0, 0], LEFT)
            b = Rectangle(width=max(0.03, 3.0 * v), height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([3.0 + b.width / 2, y, 0])
            vl = label(rf"{100 * v:.1f}\%", font_size=18, color=col).next_to(b, RIGHT, buff=0.1)
            bars.add(VGroup(n_, b, vl))
        bt = label(r"keys moved, \ 10 machines to 11", font_size=20, color=WHITE).move_to([3.4, 2.45, 0])
        steps = VGroup(*[module_box(t, HEAD, w=2.65, h=0.6, font=18) for t in
                         (r"1. \ copy the partition", r"2. \ stream new writes", r"3. \ switch the routing",
                          r"4. \ delete the old copy")]).arrange(RIGHT, buff=0.42).move_to([0, -1.35, 0])
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.05, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3) for i in range(3)])
        st = label(r"moving one partition while writes keep flowing", font_size=20, color=HEAD).next_to(
            steps, UP, buff=0.2)
        notes = VGroup(
            wrapped_label(r"many more partitions than machines, \ fixed at the start: \ a new machine takes a few "
                          r"whole partitions from each of the others, \ and no key changes partition", 12.6,
                          font_size=19, color=WHITE),
            wrapped_label(r"a routing table, \ kept in a coordination service such as ZooKeeper or etcd, \ says "
                          r"which machine owns each partition", 12.6, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(steps, DOWN, buff=0.35)
        foot = note(r"partitions illustrative; \ moved fractions computed in Part 39", font_size=16).to_edge(
            DOWN, buff=0.12)
        with self.voiceover(
            "Data grows, and shards must split or move. <bookmark mark='a'/> Hashing modulo the number of "
            "machines is the trap from chapter two. Going from ten machines to eleven moved ninety-one percent of "
            "the keys in Part 39's measurement, when the ideal is one in eleven; a ring moved under nine percent. "
            "<bookmark mark='b'/> Many systems instead create far more partitions than machines at the start, "
            "and move whole partitions: a new machine takes a few from each of the others, and no key ever "
            "changes partition. <bookmark mark='c'/> The move itself is a careful dance. Copy the partition, "
            "stream the writes made during the copy, switch the routing table, and only then delete the old copy. "
            "Writes keep flowing throughout."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes[:3]), FadeIn(parts), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(bt), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.5),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(nodes[3]))
            self.play(LaggedStart(*moves, lag_ratio=0.25), run_time=3.0)
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(st), LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.4), Create(arrows),
                      run_time=3.0)
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ secondary indexes
    def secondary(self):
        t = load39("tail")
        tail = {r["fanout"]: r["frac_slow"] for r in t["plain"]}
        head = label(r"Local or global secondary indexes", font_size=36).to_edge(UP, buff=0.3)
        query = tag_box("language = 'rust'", HEAD, size=17).move_to([-3.0, 2.45, 0])
        shards = VGroup(*[module_box(rf"shard {i + 1}", KERN, w=1.45, h=0.6, font=18) for i in range(4)]).arrange(
            RIGHT, buff=0.25).move_to([-3.0, 0.85, 0])
        local = VGroup(*[module_box(r"local index", LAM, w=1.3, h=0.4, font=16).next_to(s, DOWN, buff=0.12)
                         for s in shards])
        fan = VGroup(*[Arrow(query.get_bottom(), s.get_top(), buff=0.06, stroke_width=2, color=HEAD,
                             max_tip_length_to_length_ratio=0.12) for s in shards])
        gidx = VGroup(*[module_box(rf"index {r}", YES, w=1.45, h=0.55, font=17) for r in
                        (r"a--f", r"g--m", r"n--s", r"t--z")]).arrange(RIGHT, buff=0.25).move_to([-3.0, -1.55, 0])
        gl = label(r"a global index, \ sharded by the indexed value", font_size=19, color=YES).next_to(
            gidx, DOWN, buff=0.15)
        one = CurvedArrow(query.get_left() + DOWN * 0.05, gidx[2].get_left() + UP * 0.1, angle=PI / 2.4,
                          color=YES, stroke_width=2.5, tip_length=0.15)
        new = Square(side_length=0.2, stroke_width=0, fill_color=DATA, fill_opacity=1).move_to([-6.4, 0.85, 0])
        upd = DashedLine(shards[0].get_bottom() + DOWN * 0.05, gidx[2].get_top(), buff=0.05, color=NO,
                         stroke_width=2, dash_length=0.1).add_tip(tip_length=0.15)
        ul = label(r"second write, \ often asynchronous", font_size=17, color=NO).move_to([-3.6, -0.55, 0])
        tab = grid_table([r"shards asked", r"queries slow"],
                         [[f"{k}", rf"{100 * tail[k]:.1f}\%"] for k in (1, 10, 100)], widths=[2.3, 2.3],
                         row_h=0.5, font_size=20, colors=[[WHITE, NO]] * 3, mono_cols=())
        tab.move_to([4.2, 1.5, 0])
        tl = wrapped_label(rf"each shard slow one time in {round(1 / t['p_slow'])} \ (Part 39)", 5.0,
                           font_size=18, color=GREY_A).next_to(tab, UP, buff=0.2)
        notes = VGroup(
            wrapped_label(r"\textbf{local}: \ writes stay on one shard; \ a query on any other field asks every "
                          r"shard and waits for the slowest", 5.0, font_size=19, color=LAM),
            wrapped_label(r"\textbf{global}: \ the query asks one index shard; \ the write touches two, \ and the "
                          r"index lags: \ DynamoDB's global secondary indexes are eventually consistent", 5.0,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, DOWN, buff=0.4).align_to(tl, LEFT)
        with self.voiceover(
            "A shard key serves one access path; others need secondary indexes, and there are two ways to shard "
            "those. <bookmark mark='a'/> A local index lives beside the data: each shard indexes its own rows. "
            "Writes stay on one shard, but a query on any other field must ask every shard, and wait for the "
            "slowest. <bookmark mark='b'/> In Part 39's model, each server is slow one time in a hundred. A query "
            "to ten shards is then slow nearly one time in ten, and to a hundred shards, nearly two times in "
            "three. <bookmark mark='c'/> A global index is sharded by the indexed value itself, so the query asks "
            "one index shard. <bookmark mark='d'/> Now a write touches two shards, and the index is usually "
            "updated asynchronously. DynamoDB's global secondary indexes, for example, are eventually consistent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(query), FadeIn(shards))
            vo.wait_until("a")
            self.play(FadeIn(local), FadeIn(notes[0]))
            self.play(LaggedStart(*[GrowArrow(a) for a in fan], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*row)) for row in tab.cells[1:]], lag_ratio=0.5))
            vo.wait_until("c")
            self.play(FadeOut(fan), FadeOut(local), FadeIn(gidx), FadeIn(gl))
            self.play(Create(one))
            vo.wait_until("d")
            self.play(FadeIn(new))
            self.play(new.animate.move_to(shards[0]))
            self.play(Create(upd), FadeIn(ul), FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ across shards
    def cross(self):
        tx = load39("txn")["two_pc"]
        head = label(r"Across shards", font_size=36).to_edge(UP, buff=0.3)
        # co-location: each customer's rows on one shard
        def shard(name, cust, color):
            box = RoundedRectangle(width=2.5, height=2.2, corner_radius=0.1, stroke_color=KERN, stroke_width=2)
            t = label(name, font_size=19, color=KERN).next_to(box.get_top(), DOWN, buff=0.12)
            tags = VGroup(*[tag_box(f"{cust}.{x}", color, size=16) for x in ("users", "orders", "invoices")])
            tags.arrange(DOWN, buff=0.12).next_to(t, DOWN, buff=0.15)
            return VGroup(box, t, tags)
        sA = shard(r"shard 1", "acme", DATA)
        sB = shard(r"shard 2", "zeta", LAM)
        sh = VGroup(sA, sB).arrange(RIGHT, buff=0.4).move_to([-3.9, 0.55, 0])
        q = tag_box("acme: orders JOIN invoices", YES, size=16).next_to(sA, UP, buff=0.35).align_to(sh, LEFT)
        qa = Arrow(q.get_bottom(), sA.get_top(), buff=0.04, stroke_width=2.5, color=YES,
                   max_tip_length_to_length_ratio=0.2)
        cl = wrapped_label(r"shard by customer: \ each customer's joins stay on one machine", 5.3, font_size=19,
                           color=YES).next_to(sh, DOWN, buff=0.3)
        # two-phase commit with a coordinator that crashes after deciding
        lanes_y = {"coordinator": 1.75, "P1": 1.05, "P2": 0.45, "P3": -0.15}
        lx0, lx1 = 1.9, 6.7
        lanes = VGroup()
        for nm, y in lanes_y.items():
            lanes.add(VGroup(label(nm, font_size=17, color=GREY_A).move_to([1.2, y, 0]).align_to([0.55, 0, 0],
                                                                                                  LEFT),
                             Line([lx0, y, 0], [lx1, y, 0], color=GREY_D, stroke_width=1.5)))
        tt = label(r"two-phase commit across three shards", font_size=20, color=WHITE).move_to([3.6, 2.4, 0])
        xp, xv, xd, xr = 2.1, 2.55, 2.95, 5.9
        cy = lanes_y["coordinator"]
        prep = VGroup(*[Arrow([xp, cy, 0], [xv, lanes_y[p], 0], buff=0, stroke_width=1.8, color=DATA,
                              max_tip_length_to_length_ratio=0.12) for p in ("P1", "P2", "P3")])
        votes = VGroup(*[Arrow([xv, lanes_y[p], 0], [xd, cy, 0], buff=0, stroke_width=1.8, color=YES,
                               max_tip_length_to_length_ratio=0.12) for p in ("P1", "P2", "P3")])
        crash = Cross(scale_factor=0.14, stroke_color=NO, stroke_width=5).move_to([xd + 0.2, cy, 0])
        dl = label(r"decides COMMIT, \ crashes", font_size=16, color=NO).next_to(crash, UP, buff=0.1).shift(
            RIGHT * 0.5)
        locks = VGroup(*[Rectangle(width=xr - xv, height=0.2, stroke_width=0, fill_color=NO, fill_opacity=0.6)
                         .move_to([(xv + xr) / 2, lanes_y[p], 0]) for p in ("P1", "P2", "P3")])
        ll = label(rf"locks held, \ waiting: \ {tx['blocked_seconds']:.1f} s", font_size=18, color=NO).next_to(
            locks, DOWN, buff=0.18)
        rec = VGroup(*[Arrow([xr, cy, 0], [xr + 0.45, lanes_y[p], 0], buff=0, stroke_width=1.8, color=YES,
                             max_tip_length_to_length_ratio=0.12) for p in ("P1", "P2", "P3")])
        rl = label(r"recovers, \ resends", font_size=16, color=YES).next_to([xr, cy, 0], UP, buff=0.1)
        brk = VGroup(Line([4.2, 2.0, 0], [4.35, -0.4, 0], color=GREY_B, stroke_width=1.5),
                     Line([4.35, 2.0, 0], [4.5, -0.4, 0], color=GREY_B, stroke_width=1.5))
        tl = label(r"time: \ the first 10 ms, \ then a break", font_size=16, color=GREY_B).next_to(
            ll, DOWN, buff=0.12)
        final = wrapped_label(r"design for one shard per operation; \ treat the cross-shard path as the rare, \ "
                              r"slow, \ carefully guarded exception", 12.6, font_size=20, color=HEAD).to_edge(
            DOWN, buff=0.45)
        foot = note(r"customers illustrative; \ the two-phase commit run is Part 39's", font_size=16).to_edge(
            DOWN, buff=0.1)
        with self.voiceover(
            "Some queries span shards anyway. <bookmark mark='a'/> Choose the key so that the common ones do not: "
            "shard by customer, and keep each customer's users, orders and invoices together, so their joins stay "
            "on one machine. <bookmark mark='b'/> A transaction that must change two shards needs Part 39's "
            "two-phase commit. Every shard votes yes and locks its rows. <bookmark mark='c'/> In Part 39's run, "
            "the coordinator crashed just after deciding to commit, and every participant held its locks, unable "
            "to finish, for thirty-one seconds, until the coordinator recovered. <bookmark mark='d'/> So design "
            "for one shard per operation, and treat the cross-shard path as the rare, slow, carefully guarded "
            "exception."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sh), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(q), GrowArrow(qa), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(tt), FadeIn(lanes))
            self.play(LaggedStart(*[GrowArrow(a) for a in prep], lag_ratio=0.2))
            self.play(LaggedStart(*[GrowArrow(a) for a in votes], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(Create(crash), FadeIn(dl))
            self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in locks], lag_ratio=0.1), FadeIn(brk),
                      run_time=2.0)
            self.play(FadeIn(ll), FadeIn(tl))
            self.play(FadeIn(rl), LaggedStart(*[GrowArrow(a) for a in rec], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(final))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, load)
