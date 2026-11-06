from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono, tag_box

OWNER = {"c1": DATA, "c2": LAM, "c3": YES, "c4": KERN}
KEYC = {"the": DATA, "whale": HEAD, "and": LAM, "sea": YES, "ship": KERN}


def cell(w=0.62, h=0.5, color=GREY_B, fill=None, text=None, size=16):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.5, fill_color=fill or BG,
                  fill_opacity=0.55 if fill else 1)
    g = VGroup(r)
    if text is not None:
        g.add(mono(text, size=size, color=WHITE).move_to(r))
    return g


class Partitioned(VoiceoverScene):
    def construct(self):
        self.card()
        self.segments()
        self.keys()
        self.groups()
        self.retention()
        self.replicas()

    def card(self):
        card = chapter_card(1, r"The partitioned log", r"How does one log carry a whole company's events?",
                            lit=(2011,), extra=((2011, r"Kreps, \ Narkhede and Rao: \ Kafka"),), part=PART)
        with self.voiceover("Chapter one. The partitioned log."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def segments(self):
        head = label(r"Partitions, \ segments and offsets", font_size=36).to_edge(UP, buff=0.3)
        per, nseg, filled = 5, 3, 12
        segs = VGroup()
        cells = []
        for s in range(nseg):
            row = VGroup(*[cell(fill=DATA if s * per + i < filled else None, text=str(s * per + i)
                                if s * per + i < filled else None) for i in range(per)]).arrange(RIGHT, buff=0)
            frame = SurroundingRectangle(row, buff=0.1, corner_radius=0.08, stroke_width=1.5,
                                         color=HEAD if s == nseg - 1 else GREY_C)
            name = label(rf"segment file, \ base offset {s * per}" + (r" \ (active)" if s == nseg - 1 else ""),
                         font_size=16, color=HEAD if s == nseg - 1 else GREY_B).next_to(frame, UP, buff=0.12)
            segs.add(VGroup(frame, row, name))
            cells += list(row)
        segs.arrange(RIGHT, buff=0.3).move_to([0, 1.5, 0])
        new = [cell(fill=DATA, text=str(k)).move_to(cells[k]) for k in range(filled, nseg * per)]
        prod = Arrow(cells[-1].get_right() + RIGHT * 0.9, cells[-1].get_right() + RIGHT * 0.15, buff=0,
                     color=HEAD, stroke_width=3)
        prod_l = label(r"append", font_size=16, color=HEAD).next_to(prod, DOWN, buff=0.08)

        def pointer(k):
            a = Arrow(cells[k].get_bottom() + DOWN * 0.75, cells[k].get_bottom() + DOWN * 0.05, buff=0, color=YES,
                      stroke_width=3)
            t = label(rf"consumer: \ next offset {k}", font_size=16, color=YES).next_to(a, DOWN, buff=0.08)
            return VGroup(a, t)
        ptr = pointer(6)
        illus = note(r"illustrative: \ five records to a segment", font_size=16).next_to(segs, DOWN, buff=0.3)
        illus.align_to(segs, LEFT)
        notes = VGroup(
            wrapped_label(r"a \textbf{topic} is split into \textbf{partitions}; \ each partition is an append-only "
                          r"log whose records are numbered by \textbf{offset} and never changed", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"on disk a partition is a run of segment files, \ each named by its first offset and with "
                          r"a sparse index from offset to byte position; \ only the last is written", 12.4,
                          font_size=20, color=HEAD),
            wrapped_label(r"a consumer's whole state is one number per partition, \ the next offset to read, \ "
                          r"which it commits back to the broker", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(segs, DOWN, buff=1.75).set_x(0)
        with self.voiceover(
            "Kafka was built at LinkedIn by Jay Kreps, Neha Narkhede and Jun Rao, and described in 2011. "
            "<bookmark mark='a'/> A topic, a named stream such as page views, is split into partitions, and each "
            "partition is a log: records appended at the end, numbered by offset, and never changed. "
            "<bookmark mark='b'/> On disk a partition is a run of segment files, each named by its first offset, with"
            " a sparse index into it. Only the last segment is written; by default a new one starts every gigabyte. "
            "<bookmark mark='c'/> A consumer's whole state is one number per partition, the next offset to read, "
            "which it commits back to the broker and resumes from after a crash."
        ) as vo:
            self.play(FadeIn(head), FadeIn(segs), FadeIn(illus))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), GrowArrow(prod), FadeIn(prod_l))
            for c in new:
                self.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(segs[-1][0], color=HEAD))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), FadeIn(ptr))
            for k in (8, 10):
                self.play(Transform(ptr, pointer(k)), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    def keys(self):
        o = load("ordering")
        words = "the whale and the sea and the ship and the whale".split()
        parts = {int(p): v for p, v in o["partitions"].items()}
        n = max(parts) + 1
        head = label(r"Keys choose partitions", font_size=36).to_edge(UP, buff=0.3)
        src = VGroup(*[tag_box(w, color=KEYC[w], size=16) for w in words]).arrange(RIGHT, buff=0.12)
        src.next_to(head, DOWN, buff=0.45).set_x(0)
        idx = VGroup(*[label(f"{i}", font_size=16, color=GREY_B).next_to(b, UP, buff=0.06) for i, b in
                       enumerate(src)])
        rows = VGroup()
        for p in range(n):
            name = label(rf"partition {p}", font_size=18, color=GREY_A)
            line = Line(ORIGIN, RIGHT * 6.6, color=GREY_D, stroke_width=1.5)
            rows.add(VGroup(name, line).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.62).next_to(src, DOWN, buff=0.6).to_edge(LEFT, buff=0.4)
        slot_w = 1.15
        placed = {}
        moves = []
        for p, recs in parts.items():
            for j, (w, i) in enumerate(recs):
                x = rows[p][1].get_left()[0] + 0.1 + slot_w * (j + 0.5)
                tgt = tag_box(w, color=KEYC[w], size=16, w=1.0).move_to([x, rows[p][1].get_y(), 0])
                off = mono(str(j), size=14, color=GREY_B).next_to(tgt, DOWN, buff=0.08)
                placed[i] = (tgt, off)
        for i in range(len(words)):
            tgt, off = placed[i]
            moves.append((i, tgt, off))
        notes = VGroup(
            wrapped_label(rf"partition = hash(key) mod {n} \ (CRC-32 here; \ Kafka's default partitioner uses "
                          r"murmur2)", 4.4, font_size=19, color=WHITE),
            wrapped_label(r"every record of one key lands in one partition, \ so its order is kept: \ checked "
                          r"for every key, \ " + (r"\textbf{true}" if o["per_key_in_order"] else r"\textbf{false}"),
                          4.4, font_size=19, color=YES),
            wrapped_label(r"across partitions there is no order at all; \ and hot keys make hot partitions", 4.4,
                          font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).set_y(rows.get_y())
        with self.voiceover(
            "Which partition does a record go to? <bookmark mark='a'/> The producer hashes the record's key. Here the"
            " keys are words, hashed with CRC thirty-two into four partitions. <bookmark mark='b'/> Every record with"
            " the same key lands in the same partition, so one key's records keep their order, and our simulator "
            "checks this for every key. Order per key is Kafka's guarantee, and usually what an application needs: "
            "all the changes to one customer, in order. <bookmark mark='c'/> Across partitions there is no order at "
            "all. And hot keys make hot partitions: the common words fill two partitions, while another holds a "
            "single ship."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(idx), FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for i, tgt, off in moves:
                self.play(TransformFromCopy(src[i], tgt), FadeIn(off), run_time=0.45)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def groups(self):
        r = load("rebalance")
        head = label(r"Consumer groups and rebalancing", font_size=36).to_edge(UP, buff=0.3)
        N = 12

        def owners(asg):
            return {p: m for m, ps in asg.items() for p in ps}

        def squares(asg):
            ow = owners(asg)
            return VGroup(*[cell(w=0.7, h=0.62, color=OWNER[ow[p]], fill=OWNER[ow[p]], text=str(p), size=17)
                            for p in range(N)]).arrange(RIGHT, buff=0.1)
        rows = VGroup()
        for name in (r"range", r"sticky"):
            t = label(name, font_size=21, color=GREY_A)
            rows.add(VGroup(t, squares(r["three"])))
        for row in rows:
            row[1].move_to([1.0, 0, 0])
            row[0].next_to(row[1], LEFT, buff=0.5)
        rows[0].shift(UP * 1.45)
        rows[1].shift(UP * 0.05)
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.8),
                                 mono(m, size=16, color=c)).arrange(RIGHT, buff=0.1) for m, c in OWNER.items()])
        legend.arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.3).set_x(1.0)
        stage = label(r"three members", font_size=20, color=HEAD).next_to(legend, LEFT, buff=0.6)

        def moved(k, v):
            return label(rf"moved: \ {v}", font_size=18, color=NO if v > 3 else YES).next_to(
                rows[k][0], DOWN, buff=0.12)
        notes = VGroup(
            wrapped_label(r"each partition is read by exactly one member of a group, \ so a group scales out to as "
                          r"many members as there are partitions; \ another group reads the same log independently",
                          12.4, font_size=20, color=WHITE),
            wrapped_label(r"a member joining or leaving triggers a \textbf{rebalance}; \ range assignment recuts "
                          r"contiguous runs, \ a sticky assignor moves only what it must", 12.4, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.4)

        def recolor(k, before, after):
            a, b = owners(before), owners(after)
            sq = rows[k][1]
            anims = []
            for p in range(N):
                anims.append(sq[p][0].animate.set_stroke(OWNER[b[p]]).set_fill(OWNER[b[p]], opacity=0.55))
            return anims, [sq[p] for p in range(N) if a[p] != b[p]]
        with self.voiceover(
            "Readers share the work through a consumer group. <bookmark mark='a'/> Each partition is read by exactly "
            "one member, so a group can grow to as many members as there are partitions, and another group reads the "
            "same log independently. Here three members hold four partitions each. <bookmark mark='b'/> A fourth "
            "member joins, and the group rebalances. Range assignment recuts four contiguous runs and moves six "
            "partitions. A sticky assignor moves only three, the fewest possible, since the newcomer needs three. "
            "<bookmark mark='c'/> Then member two leaves: range moves four partitions, sticky just the three that "
            "member two owned. Each moved partition pauses while its new owner resumes from the committed offset."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(legend[:3]), FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            st2 = label(r"c4 joins", font_size=20, color=HEAD).move_to(stage)
            self.play(Transform(stage, st2), FadeIn(legend[3]), FadeIn(notes[1]))
            for k, key in ((0, "join_range"), (1, "join_sticky")):
                anims, mv = recolor(k, r["three"], r[key])
                self.play(*anims, run_time=1.0)
                self.play(*[Indicate(s, color=WHITE, scale_factor=1.15) for s in mv], run_time=0.8)
            m0, m1 = moved(0, r["moved_range"]), moved(1, r["moved_sticky"])
            self.play(FadeIn(m0), FadeIn(m1))
            vo.wait_until("c")
            st3 = label(r"c2 leaves", font_size=20, color=HEAD).move_to(stage)
            self.play(Transform(stage, st3), legend[1].animate.set_opacity(0.25))
            for k, a, b, key in ((0, "join_range", "leave_range", "moved_leave_range"),
                                 (1, "join_sticky", "leave_sticky", "moved_leave_sticky")):
                anims, mv = recolor(k, r[a], r[b])
                self.play(*anims, Transform(m0 if k == 0 else m1, moved(k, r[key])), run_time=1.0)
                self.play(*[Indicate(s, color=WHITE, scale_factor=1.15) for s in mv], run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    def retention(self):
        c = load("compaction")
        head = label(r"Retention and compaction", font_size=36).to_edge(UP, buff=0.3)
        segs = VGroup(*[VGroup(Rectangle(width=1.75, height=0.55, stroke_color=GREY_B, stroke_width=1.5,
                                         fill_color=DATA, fill_opacity=0.15 + 0.12 * i),
                               label(rf"segment {i + 1}", font_size=16, color=WHITE)) for i in range(5)])
        for s in segs:
            s[1].move_to(s[0])
        segs.arrange(RIGHT, buff=0.12)
        t1 = label(r"by time:", font_size=20, color=HEAD)
        top = VGroup(t1, segs).arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.75).set_x(0)
        ends = VGroup(label(r"oldest", font_size=16, color=GREY_B).next_to(segs[0], UP, buff=0.08),
                      label(r"newest", font_size=16, color=GREY_B).next_to(segs[-1], UP, buff=0.08))
        start = Arrow(segs[0].get_bottom() + DOWN * 0.55, segs[0].get_bottom(), buff=0.03, color=YES,
                      stroke_width=3)
        start_l = label(r"log start offset", font_size=16, color=YES).next_to(start, RIGHT, buff=0.1)
        start_l.shift(DOWN * 0.12)
        recs = [("a", "1"), ("b", "4"), ("c", "7"), ("a", "2"), ("b", "5"), ("a", "3"), ("d", "8"), ("b", "6")]
        last = {k: i for i, (k, _) in enumerate(recs)}
        kc = {"a": DATA, "b": LAM, "c": YES, "d": KERN}
        row = VGroup(*[tag_box(f"{k}={v}", color=kc[k], size=16, w=1.0) for k, v in recs]).arrange(RIGHT, buff=0.15)
        t2 = label(r"by key:", font_size=20, color=HEAD)
        mid = VGroup(t2, row).arrange(RIGHT, buff=0.35).next_to(top, DOWN, buff=0.95).align_to(top, LEFT)
        offs = VGroup(*[mono(str(i), size=14, color=GREY_B).next_to(b, UP, buff=0.06) for i, b in enumerate(row)])
        kept = VGroup(*[row[i].copy() for i in range(len(recs)) if last[recs[i][0]] == i])
        kept_offs = VGroup(*[offs[i].copy() for i in range(len(recs)) if last[recs[i][0]] == i])
        t3 = label(r"compacted:", font_size=18, color=YES).align_to(t2, LEFT).set_y(row.get_y() - 1.05)
        res = wrapped_label(rf"our simulator: \ {c['events']:,} updates to {c['keys']} keys compact to "
                            rf"{c['after_compaction']} records, \ and replaying them rebuilds the same state: \ "
                            + (r"\textbf{true}" if c["same_state"] else r"\textbf{false}"), 12.4, font_size=21,
                            color=YES).next_to(t3, DOWN, buff=0.8).set_x(0)
        illus = note(r"illustrative", font_size=16).next_to(row, RIGHT, buff=0.15)
        with self.voiceover(
            "A log cannot grow for ever, and there are two ways to forget. <bookmark mark='a'/> By time: whole "
            "segments older than the retention period, seven days by default, are deleted, and the start offset moves"
            " forward. Deleting a file is cheap, which is one reason segments exist. <bookmark mark='b'/> By key: a "
            "compacted topic keeps only the latest record for each key, at its original offset, and a record with an "
            "empty value, a tombstone, deletes its key. <bookmark mark='c'/> What remains is the latest state, and it"
            " is enough: in our simulator, two thousand updates to fifty keys compact to fifty records, which rebuild"
            " exactly the same table."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top), FadeIn(ends), GrowArrow(start), FadeIn(start_l))
            vo.wait_until("a")
            self.play(segs[0].animate.set_opacity(0.15), segs[1].animate.set_opacity(0.15),
                      start.animate.shift(RIGHT * (segs[2].get_x() - segs[0].get_x())),
                      start_l.animate.shift(RIGHT * (segs[2].get_x() - segs[0].get_x())), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(mid), FadeIn(offs), FadeIn(illus))
            self.play(FadeIn(t3), kept.animate.shift(DOWN * 1.05), kept_offs.animate.shift(DOWN * 1.05),
                      run_time=1.5)
            self.play(*[row[i].animate.set_opacity(0.25) for i in range(len(recs)) if last[recs[i][0]] != i])
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def replicas(self):
        head = label(r"In-sync replicas \ (ISR)", font_size=36).to_edge(UP, buff=0.3)
        W = 10
        ends = [9, 8, 5]
        names = [r"leader, \ broker 1", r"follower, \ broker 2", r"follower, \ broker 3"]
        rows = VGroup()
        for k, (nm, e) in enumerate(zip(names, ends)):
            cs = VGroup(*[cell(w=0.6, h=0.48, fill=(HEAD if k == 0 else DATA) if i < e else None,
                               text=str(i) if i < e else None, size=15) for i in range(W)]).arrange(RIGHT, buff=0)
            t = label(nm, font_size=18, color=HEAD if k == 0 else GREY_A)
            rows.add(VGroup(t, cs))
        for k, row in enumerate(rows):
            row[1].move_to([-0.4, 1.7 - 0.75 * k, 0])
            row[0].next_to(row[1], LEFT, buff=0.3)
        status = VGroup(*[label(r"in sync", font_size=18, color=YES).next_to(rows[k][1], RIGHT, buff=0.3)
                          for k in range(3)])

        def hw(i):
            x = rows[0][1][0].get_left()[0] + 0.6 * i
            ln = DashedLine([x, rows[0][1].get_top()[1] + 0.15, 0], [x, rows[2][1].get_bottom()[1] - 0.1, 0],
                            color=YES, stroke_width=3)
            t = label(r"high watermark", font_size=16, color=YES).next_to(ln, UP, buff=0.05)
            return VGroup(ln, t)
        mark = hw(min(ends))
        later = [cell(w=0.6, h=0.48, fill=DATA, text=str(i), size=15).move_to(rows[2][1][i]) for i in range(5, 9)]
        illus = note(r"illustrative", font_size=16).next_to(rows[2][1], DOWN, buff=0.15).align_to(rows[2][1], LEFT)
        notes = VGroup(
            wrapped_label(r"the leader takes every write; \ followers fetch from it as consumers do; \ a record is "
                          r"\textbf{committed}, \ and visible to consumers, \ once every in-sync replica has it",
                          12.4, font_size=20, color=WHITE),
            wrapped_label(r"a follower that falls behind leaves the ISR, \ so one slow disk cannot stall the topic; "
                          r"\ with \texttt{acks=all} and \texttt{min.insync.replicas=2} a write needs two copies",
                          12.4, font_size=20, color=HEAD),
            wrapped_label(r"Part 39's single-leader replication, \ not Raft's majority \ (Part 38): \ $f+1$ replicas "
                          r"survive $f$ failures, \ and a controller, \ itself a Raft log since KRaft, \ picks "
                          r"leaders from the ISR", 12.4, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Finally, a partition must survive losing a machine, so it is replicated. <bookmark mark='a'/> One broker"
            " leads each partition and takes every write; followers fetch from it as consumers do. A record is "
            "committed, and shown to consumers, once every replica in the in-sync set has it; that point is the high "
            "watermark. <bookmark mark='b'/> A follower that falls behind is dropped from the set, so one slow disk "
            "cannot stall the topic, and the watermark moves on. With acknowledgements from all and at least two in "
            "sync, every acknowledged write has two copies. <bookmark mark='c'/> This is Part 39's single-leader "
            "replication, not Raft's majority: f plus one replicas survive f failures, and a controller, itself now a"
            " Raft log, picks new leaders only from the in-sync set."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows), FadeIn(status), FadeIn(illus))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(mark))
            vo.wait_until("b")
            out = label(r"out of sync", font_size=18, color=NO).move_to(status[2], aligned_edge=LEFT)
            rows[2].save_state()
            self.play(Transform(status[2], out), rows[2].animate.fade(0.6), FadeIn(notes[1]))
            self.play(Transform(mark, hw(ends[1])))
            self.wait(1.5)
            back = label(r"in sync", font_size=18, color=YES).move_to(status[2], aligned_edge=LEFT)
            self.play(*[FadeIn(c) for c in later], Restore(rows[2]), Transform(status[2], back),
                      run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, NO)
