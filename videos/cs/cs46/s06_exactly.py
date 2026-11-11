from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, module_box


def _box(text, color, w=1.6, h=0.6, font=18):
    return module_box(text, color, w=w, h=h, font=font)


def _barrier(edge, t=0.0):
    """A barrier: a short bar across an edge, at proportion t along it."""
    v = edge.get_end() - edge.get_start()
    b = Line(UP * 0.22, DOWN * 0.22, color=HEAD, stroke_width=6)
    b.rotate(np.arctan2(v[1], v[0]))
    return b.move_to(edge.point_from_proportion(t))


class Exactly(VoiceoverScene):
    def construct(self):
        self.card()
        self.keyed()
        self.barriers()
        self.recover()
        self.sinks()
        self.endtoend()

    def card(self):
        card = chapter_card(5, r"Exactly-once state", r"What does a crash do to a running count?",
                            lit=(1985, 2015), extra=((1985, r"Chandy and Lamport: \ snapshots"),
                                                     (2015, r"Carbone et al.: \ barrier snapshots")), part=PART)
        with self.voiceover("Chapter five. Exactly-once state."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def keyed(self):
        head = label(r"Keyed state", font_size=36).to_edge(UP, buff=0.3)
        keys = "a b a c b a c a b".split()
        col = {"a": DATA, "b": LAM, "c": KERN}
        cw, x0, y = 0.6, -6.3, 1.7
        cells = VGroup(*[VGroup(Square(cw, stroke_color=GREY_C, stroke_width=1.5),
                                mono(k, size=18, color=col[k])).move_to([x0 + cw * (i + 0.5), y, 0])
                         for i, k in enumerate(keys)])
        for c in cells:
            c[1].move_to(c[0])
        offs = VGroup(*[label(f"{i}", font_size=15, color=GREY_B).next_to(c, UP, buff=0.08)
                        for i, c in enumerate(cells)])
        logl = label(r"the log: \ one partition", font_size=18, color=GREY_A).next_to(offs, UP, buff=0.12).align_to(
            cells, LEFT)
        ptr = VGroup(Triangle(color=HEAD, fill_opacity=1).scale(0.09).rotate(PI),
                     label(r"next offset", font_size=15, color=HEAD))
        ptr[1].next_to(ptr[0], DOWN, buff=0.06)
        ptr.next_to(cells[0], DOWN, buff=0.08)
        workers, states = VGroup(), []
        for j, k in enumerate("abc"):
            box = RoundedRectangle(width=3.0, height=0.8, corner_radius=0.1, stroke_color=col[k], stroke_width=2,
                                   fill_color=col[k], fill_opacity=0.1).move_to([3.9, 2.0 - 1.25 * j, 0])
            name = label(rf"worker {j}", font_size=17, color=GREY_A).move_to(box).align_to(box, LEFT).shift(
                RIGHT * 0.2)
            st = mono(f"count[{k}] = 0", size=17, color=col[k]).move_to(box).align_to(box, RIGHT).shift(LEFT * 0.2)
            workers.add(VGroup(box, name, st))
            states.append(st)
        hub = Dot([0.4, y, 0], radius=0.05, color=GREY_B)
        feed = Arrow(cells[-1].get_right(), hub.get_center(), buff=0.1, color=GREY_B, stroke_width=2,
                     max_tip_length_to_length_ratio=0.08)
        fan = VGroup(*[Arrow(hub.get_center(), w[0].get_left(), buff=0.05, color=GREY_B, stroke_width=2,
                             max_tip_length_to_length_ratio=0.08) for w in workers])
        kl = label(r"by key", font_size=16, color=GREY_B).next_to(feed, UP, buff=0.08)
        ill = note(r"illustrative", font_size=16).next_to(workers, DOWN, buff=0.12).align_to(workers, RIGHT)
        cross = Cross(workers[1][0], stroke_color=NO, stroke_width=5)
        lines = VGroup(
            wrapped_label(r"state lives with the operator, \ partitioned by key like the log: \ each key's count on "
                          r"exactly one worker, \ updated by every event that passes", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"a crash loses it; \ the log still holds every event, \ but from which offset should the "
                          r"worker replay, \ and into what state? \ too late misses events, \ too early counts them "
                          r"twice", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(workers, DOWN, buff=0.7).set_x(0)
        with self.voiceover(
            "A stream processor keeps state: running counts, open windows, the buffers of a join. "
            "<bookmark mark='a'/> The state is partitioned by key, like the log it reads, so every key's count "
            "lives on exactly one worker, and each event updates it as it passes. <bookmark mark='b'/> Then a "
            "worker crashes, and its state is gone. The log still holds every event. The "
            "question is where to resume. Replay from too late, and events are missed; from too early, and they "
            "are counted twice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(offs), FadeIn(logl), FadeIn(ptr), FadeIn(workers),
                      GrowArrow(feed), *[GrowArrow(a) for a in fan], FadeIn(hub), FadeIn(kl), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            n = {"a": 0, "b": 0, "c": 0}
            for i, k in enumerate(keys):
                j = "abc".index(k)
                tok = cells[i][1].copy()
                n[k] += 1
                new = mono(f"count[{k}] = {n[k]}", size=17, color=col[k]).move_to(states[j], aligned_edge=RIGHT)
                nxt = cells[i + 1] if i + 1 < len(cells) else cells[i]
                self.play(tok.animate.move_to(workers[j][0]), ptr.animate.next_to(nxt, DOWN, buff=0.08)
                          .shift(RIGHT * (cw if i + 1 == len(cells) else 0)), run_time=0.45)
                self.play(FadeOut(tok), Transform(states[j], new), run_time=0.25)
            vo.wait_until("b")
            self.play(Create(cross), states[1].animate.set_opacity(0.15), workers[1][0].animate.set_stroke(NO),
                      FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def barriers(self):
        head = label(r"Barriers through the graph", font_size=36).to_edge(UP, buff=0.3)
        S = [_box(r"source 0", DATA).move_to([-5.9, 1.5, 0]), _box(r"source 1", DATA).move_to([-5.9, -0.5, 0])]
        C = [_box(r"count", KERN, w=1.3).move_to([-3.2, 1.5, 0]), _box(r"count", KERN, w=1.3).move_to([-3.2, -0.5, 0])]
        K = _box(r"sink", YES, w=1.2).move_to([-0.6, 0.5, 0])
        se = {(i, j): Line(S[i][0].get_right(), C[j][0].get_left(), buff=0.03, color=GREY_C, stroke_width=2)
              for i in range(2) for j in range(2)}
        ce = [Line(C[j][0].get_right(), K[0].get_left(), buff=0.03, color=GREY_C, stroke_width=2) for j in range(2)]
        store = RoundedRectangle(width=6.6, height=1.1, corner_radius=0.1, stroke_color=GREY_B, stroke_width=1.5,
                                 fill_opacity=0).move_to([-3.4, -2.35, 0])
        stl = label(r"durable storage \ (an object store, \ Part 45)", font_size=16, color=GREY_B).next_to(
            store, UP, buff=0.08).align_to(store, LEFT)
        chips = [tag_like(t, c) for t, c in ((r"offsets", DATA), (r"state", KERN), (r"state", KERN),
                                              (r"sink", YES))]
        VGroup(*chips).arrange(RIGHT, buff=0.3).move_to(store)
        done = label(r"checkpoint 1 complete", font_size=18, color=YES).next_to(store, DOWN, buff=0.12)
        notes = VGroup(
            wrapped_label(r"each source records its offset in the log \ and injects a \textbf{barrier} into every "
                          r"output, \ flowing with the records", 5.3, font_size=19, color=HEAD),
            wrapped_label(r"an operator holds back each input whose barrier has arrived until the barrier is in on "
                          r"all of them: \ \textbf{alignment}", 5.3, font_size=19, color=LAM),
            wrapped_label(r"then it copies its state to storage, \ in the background, \ and passes the barrier on", 5.3,
                          font_size=19, color=KERN),
            wrapped_label(r"when the sink has every barrier, \ offsets and states form one consistent cut: \ a "
                          r"\textbf{checkpoint}", 5.3, font_size=19, color=YES),
            wrapped_label(r"Chandy and Lamport's markers \ (Part 38), \ for an acyclic dataflow: \ aligned, \ no "
                          r"records in flight need saving \ (Carbone et al., \ 2015)", 5.3, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.1, -0.25, 0])

        def flow(edges, t0=0.0, t1=1.0, color=DATA):
            ds = [Dot(e.point_from_proportion(t0), radius=0.06, color=color) for e in edges]
            return ds, [d.animate.move_to(e.point_from_proportion(t1)) for d, e in zip(ds, edges)]
        with self.voiceover(
            "Paris Carbone and his colleagues gave Apache Flink its answer in 2015, a descendant of Chandy and "
            "Lamport's snapshots from Part 38. <bookmark mark='a'/> Records flow from two sources, through two "
            "keyed counters, to a sink. <bookmark mark='b'/> To take a checkpoint, each source records its offset "
            "and injects a barrier, a marker that travels with the records. <bookmark mark='c'/> A counter with "
            "two inputs waits until the barrier has arrived on both, holding back the input that delivered it "
            "first, so that its state reflects every event before the barrier and none after. That is alignment. "
            "<bookmark mark='d'/> Then it copies its state to storage, in the background, and passes the barrier "
            "on. <bookmark mark='e'/> When the sink has every barrier, the checkpoint is complete: offsets and "
            "states that describe one consistent cut through the computation. With no cycles and aligned barriers, "
            "no records in flight need saving."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(b) for b in S + C + [K]], *[Create(e) for e in list(se.values()) + ce],
                      Create(store), FadeIn(stl))
            vo.wait_until("a")
            for _ in range(2):
                ds, an = flow(list(se.values()))
                self.add(*ds)
                self.play(*an, run_time=0.8)
                self.remove(*ds)
                ds, an = flow(ce)
                self.add(*ds)
                self.play(*an, run_time=0.6)
                self.remove(*ds)
            vo.wait_until("b")
            off = [mono("offset", size=14, color=DATA).move_to(s) for s in S]
            self.play(FadeIn(notes[0]), *[FadeIn(o) for o in off])
            self.play(*[o.animate.move_to(chips[0]).set_opacity(0) for o in off], FadeIn(chips[0]), run_time=0.8)
            self.remove(*off)
            b0 = [_barrier(se[(0, j)], 0.02) for j in range(2)]
            b1 = [_barrier(se[(1, j)], 0.02) for j in range(2)]
            self.play(FadeIn(VGroup(*b0, *b1)))
            self.play(*[b.animate.move_to(se[(0, j)].point_from_proportion(0.97)) for j, b in enumerate(b0)],
                      *[b.animate.move_to(se[(1, j)].point_from_proportion(0.45)) for j, b in enumerate(b1)],
                      run_time=1.4)
            vo.wait_until("c")
            q = [Dot(se[(0, j)].point_from_proportion(0.85 - 0.08 * k), radius=0.06, color=GREY_B)
                 for j in range(2) for k in range(3)]
            hold = [label(r"aligning", font_size=16, color=LAM).next_to(c, UP, buff=0.1) for c in C]
            self.play(FadeIn(notes[1]), LaggedStart(*[FadeIn(d, shift=RIGHT * 0.2) for d in q], lag_ratio=0.15),
                      *[FadeIn(h) for h in hold])
            ds, an = flow([se[(1, j)] for j in range(2)], 0.6, 1.0)
            self.add(*ds)
            self.play(*[b.animate.move_to(se[(1, j)].point_from_proportion(0.97)) for j, b in enumerate(b1)], *an,
                      run_time=1.2)
            self.remove(*ds)
            vo.wait_until("d")
            snaps = [C[j][0].copy().set_fill(KERN, 0.3) for j in range(2)]
            self.play(FadeIn(notes[2]), *[FadeOut(h) for h in hold],
                      *[ReplacementTransform(s, chips[1 + j]) for j, s in enumerate(snaps)],
                      FadeOut(VGroup(*b0, *b1)), run_time=1.2)
            bc = [_barrier(e, 0.03) for e in ce]
            self.add(*bc)
            self.play(*[b.animate.move_to(e.point_from_proportion(0.97)) for b, e in zip(bc, ce)],
                      *[d.animate.move_to(C[0 if i < 3 else 1][0].get_left()).set_opacity(0) for i, d in enumerate(q)],
                      run_time=1.2)
            vo.wait_until("e")
            self.play(FadeOut(VGroup(*bc)), ReplacementTransform(K[0].copy(), chips[3]), FadeIn(notes[3]))
            self.play(store.animate.set_stroke(YES, width=3), FadeIn(done), FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()

    def recover(self):
        c = load("checkpoint")
        N, r0, rep = c["events"], c["restored_from"], c["replayed"]
        crash = r0 + rep
        head = label(r"A crash, \ and recovery", font_size=36).to_edge(UP, buff=0.3)

        def X(o):
            return -6.0 + 12.0 * o / N
        y1, y2 = 1.75, 0.95
        base = Rectangle(width=12.0, height=0.3, stroke_color=GREY_C, stroke_width=1.5).move_to([0, y1, 0])
        ends = VGroup(label(r"offset 0", font_size=16, color=GREY_B).next_to(base, UP, buff=0.1).align_to(base, LEFT),
                      label(rf"{N:,}", font_size=16, color=GREY_B).next_to(base, UP, buff=0.1).align_to(base, RIGHT))
        run1 = Rectangle(width=X(crash) - X(0), height=0.3, stroke_width=0, fill_color=DATA,
                         fill_opacity=0.7).move_to([(X(0) + X(crash)) / 2, y1, 0])
        tick = Line([X(r0), y1 - 0.3, 0], [X(r0), y1 + 0.3, 0], color=YES, stroke_width=4)
        tl = label(rf"last checkpoint: \ offset {r0:,}", font_size=17, color=YES).next_to(tick, UP, buff=0.08)
        tl.align_to(tick, RIGHT).shift(LEFT * 0.1)
        boom = Cross(Square(0.36).move_to([X(crash), y1, 0]), stroke_color=NO, stroke_width=5)
        bl = label(rf"crash at {crash:,}", font_size=17, color=NO).next_to(boom, UP, buff=0.1).align_to(
            boom, LEFT).shift(RIGHT * 0.15)
        back = CurvedArrow([X(crash), y1 - 0.25, 0], [X(r0) + 0.15, y2 + 0.42, 0], color=HEAD, stroke_width=2.5,
                           angle=-1.2)
        replay = Rectangle(width=X(crash) - X(r0), height=0.3, stroke_width=0, fill_color=HEAD,
                           fill_opacity=0.85).move_to([(X(r0) + X(crash)) / 2, y2, 0])
        rest = Rectangle(width=X(N) - X(crash), height=0.3, stroke_width=0, fill_color=DATA,
                         fill_opacity=0.7).move_to([(X(crash) + X(N)) / 2, y2, 0])
        rl = label(rf"{rep} events processed a second time", font_size=17, color=HEAD).next_to(replay, DOWN, buff=0.12)
        rl.align_to(replay, RIGHT)

        def panel(title, body, col, x):
            r = RoundedRectangle(width=6.3, height=1.9, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                 fill_color=col, fill_opacity=0.08).move_to([x, -0.75, 0])
            t = wrapped_label(title, 5.9, font_size=20, color=col)
            b = wrapped_label(body, 5.9, font_size=20, color=WHITE)
            VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(r)
            return VGroup(r, t, b)
        good = panel(r"restore the states \textit{and} the offsets of the checkpoint",
                     r"the replayed events meet the state as it was before they first arrived: \ final counts "
                     + ("equal" if c["exact_with_snapshots"] else "differ from") + r" a run that never failed",
                     YES, -3.35)
        bad = panel(r"rewind the offset, \ but keep the counts of the moment of the crash",
                    rf"{c['naive_overcount']} events counted twice: \ \textbf{{at-least-once}}", NO, 3.35)
        foot = wrapped_label(r"skip the replay instead and those events are lost: \ \textbf{at-most-once}; \ "
                             r"\textbf{exactly-once} state means state and position restored together", 12.4,
                             font_size=20, color=WHITE).next_to(good, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            f"We crashed our keyed counter on purpose. <bookmark mark='a'/> {N:,} events, three workers, and "
            f"checkpoints taken as the stream runs. At offset {crash:,}, every worker loses its state. "
            "<bookmark mark='b'/> Recovery loads the last complete checkpoint, from offset "
            f"{r0:,}, and rewinds the source to the same place. {rep} events are processed a second time. "
            "<bookmark mark='c'/> But they meet the state as it was before they first arrived, and the final "
            "counts equal those of a run that never failed. <bookmark mark='d'/> Rewind the source but keep the "
            f"counts as they stood at the crash, and those {c['naive_overcount']} events are counted twice: that is "
            "at-least-once. <bookmark mark='e'/> Skip the replay, and they are lost: at-most-once. Exactly-once "
            "means state and position restored together."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(ends))
            vo.wait_until("a")
            self.play(GrowFromEdge(run1, LEFT), run_time=2)
            self.play(Create(tick), FadeIn(tl), Create(boom), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(back))
            self.play(GrowFromEdge(replay, LEFT), FadeIn(rl))
            self.play(GrowFromEdge(rest, LEFT), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(good))
            vo.wait_until("d")
            self.play(FadeIn(bad))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def sinks(self):
        head = label(r"Sinks: \ idempotent or transactional", font_size=36).to_edge(UP, buff=0.3)
        lt = label(r"idempotent: \ upsert by window and key", font_size=21, color=YES).move_to([-3.5, 2.35, 0])
        tab = grid_table([r"window", r"key", r"count"], [[r"0--10 s", "a", "42"], [r"0--10 s", "b", "17"]],
                         widths=[1.8, 1.0, 1.2], row_h=0.48, font_size=19, mono_cols=(1, 2))
        tab.move_to([-3.5, 1.0, 0])
        frame = SurroundingRectangle(tab, buff=0.15, color=GREY_D, stroke_width=1.5)
        wr = mono("put((0-10 s, a), 42)", size=16, color=YES).next_to(frame, DOWN, buff=0.45)
        wl = label(r"replayed after a crash: \ same row, \ same value", font_size=18, color=GREY_A).next_to(
            wr, DOWN, buff=0.15)
        rt = label(r"transactional: \ commit with the checkpoint", font_size=21, color=KERN).move_to([3.5, 2.35, 0])
        x0, x1, ya = 0.6, 6.6, 0.75
        axis = Arrow([x0, ya, 0], [x1, ya, 0], buff=0, color=GREY_C, stroke_width=2,
                     max_tip_length_to_length_ratio=0.03)
        cks = VGroup()
        for x, t in ((1.0, r"checkpoint $n$"), (3.7, r"checkpoint $n{+}1$")):
            cks.add(VGroup(Line([x, ya - 0.2, 0], [x, ya + 0.2, 0], color=HEAD, stroke_width=4),
                           label(t, font_size=16, color=HEAD).next_to([x, ya - 0.2, 0], DOWN, buff=0.1)))
        tx1 = VGroup(*[Square(0.32, stroke_width=1, stroke_color=GREY_B, fill_color=GREY_D, fill_opacity=1).move_to(
            [1.45 + 0.5 * i, ya + 0.5, 0]) for i in range(4)])
        tx2 = VGroup(*[Square(0.32, stroke_width=1, stroke_color=GREY_B, fill_color=GREY_D, fill_opacity=1).move_to(
            [4.15 + 0.5 * i, ya + 0.5, 0]) for i in range(3)])
        crash = Cross(Square(0.34).move_to([5.9, ya + 0.5, 0]), stroke_color=NO, stroke_width=5)
        pend = label(r"open: \ invisible to readers", font_size=16, color=GREY_B).next_to(tx1, UP, buff=0.12)
        com = label(r"committed", font_size=16, color=YES).next_to(tx1, UP, buff=0.12)
        ab = label(r"aborted, \ written again", font_size=16, color=NO).next_to(VGroup(tx2, crash), UP, buff=0.12)
        ill = note(r"illustrative", font_size=16).next_to(cks, DOWN, buff=0.15).align_to(axis, RIGHT)
        lines = VGroup(
            wrapped_label(r"an \textbf{idempotent} sink makes a second write harmless; \ a \textbf{transactional} "
                          r"sink makes the first one invisible until its checkpoint completes", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"two-phase commit \ (Part 39) \ with the checkpoint as coordinator: \ prepare at the "
                          r"barrier, \ commit when the checkpoint is complete; \ Kafka added the transactions this "
                          r"needs in 2017", 12.4, font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(wl, DOWN, buff=0.8).set_x(0)
        with self.voiceover(
            "Inside, the state is now exact; outside, some results may have been seen twice. "
            "<bookmark mark='a'/> One fix is an idempotent sink. Each result is written as an upsert, keyed by its "
            "window and key, so writing the same answer again leaves the table unchanged. "
            "<bookmark mark='b'/> The other is a transactional sink. Everything written since the last checkpoint "
            "goes into an open transaction that readers cannot see; when the checkpoint completes, it commits. "
            "<bookmark mark='c'/> After a crash the open transaction is aborted and its records are written again, "
            "so readers see each one once. <bookmark mark='d'/> This is two-phase commit from Part 39, with the "
            "checkpoint as coordinator; Kafka gained the transactions it needs in 2017."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lt), FadeIn(tab), Create(frame), FadeIn(rt), GrowArrow(axis), FadeIn(cks),
                      FadeIn(ill))
            vo.wait_until("a")
            for k in range(2):
                w = wr.copy()
                self.play(FadeIn(w, shift=UP * 0.2), run_time=0.5)
                self.play(w.animate.move_to(tab.cells[1][2]).set_opacity(0), Indicate(tab.cells[1][2], color=YES),
                          run_time=0.9)
                self.remove(w)
            self.play(FadeIn(wr), FadeIn(wl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in tx1], lag_ratio=0.3), FadeIn(pend),
                      run_time=1.6)
            self.play(Indicate(cks[1]), tx1.animate.set_fill(YES, 0.8), ReplacementTransform(pend, com))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in tx2], lag_ratio=0.3), run_time=1.2)
            self.play(Create(crash), tx2.animate.set_fill(NO, 0.6), FadeIn(ab))
            vo.wait_until("d")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()

    def endtoend(self):
        head = label(r"Exactly-once is end to end", font_size=36).to_edge(UP, buff=0.3)
        parts = [(r"replayable source", DATA, r"a log with offsets that can be rewound \ (chapter 1)",
                  r"without it: \ a source that cannot rewind loses events"),
                 (r"checkpointed state", KERN, r"state saved together with those offsets \ (barriers)",
                  r"without it: \ replays count events twice"),
                 (r"idempotent or transactional sink", YES, r"a second write harmless, \ or the first one "
                  r"invisible until committed", r"without it: \ a sink that appends, \ or sends an email, \ "
                  r"does it twice")]
        boxes = VGroup(*[module_box(t, c, w=3.9, h=0.75, font=20) for t, c, _, _ in parts]).arrange(
            RIGHT, buff=0.55).next_to(head, DOWN, buff=0.6)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.2) for i in range(2)])
        does = VGroup(*[wrapped_label(d, 3.7, font_size=20, color=WHITE).next_to(b, DOWN, buff=0.3)
                        for b, (_, _, d, _) in zip(boxes, parts)])
        fails = VGroup(*[wrapped_label(f, 3.7, font_size=20, color=NO) for _, _, _, f in parts])
        for f, d in zip(fails, does):
            f.next_to(d, DOWN, buff=0.35).align_to(d, LEFT)
        top_f = min(f.get_top()[1] for f in fails)
        for f in fails:
            f.shift(UP * (top_f - f.get_top()[1]))
        lines = VGroup(
            wrapped_label(r"``exactly once'' is about \textit{effect}: \ an event may be \textit{processed} more "
                          r"than once, \ but it changes the result once", 12.4, font_size=21, color=HEAD),
            wrapped_label(r"the end-to-end argument \ (Saltzer, \ Reed and Clark, \ 1984; \ Part 36): \ a guarantee "
                          r"made in the middle of a system cannot replace one made at its ends", 12.4, font_size=21,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(fails, DOWN, buff=0.8).set_x(0)
        with self.voiceover(
            "So exactly-once is never the property of one component. <bookmark mark='a'/> It needs a source that "
            "can be rewound to an offset, which is why logs sit at the front of these pipelines; state checkpointed "
            "together with those offsets; and a sink that is idempotent or transactional. <bookmark mark='b'/> "
            "Remove any one and the guarantee falls: a source that cannot rewind loses events, and a sink that "
            "sends an email sends it twice. <bookmark mark='c'/> Even then, events may be processed more than once; "
            "what is exact is their effect. It is the end-to-end argument of Saltzer, Reed and Clark, from Part 36: "
            "a guarantee can only be made at the ends."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(b, d)) for b, d in zip(boxes, does)], lag_ratio=0.5),
                      *[GrowArrow(a) for a in arrows], run_time=2.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f) for f in fails], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(lines))
        self.wait(0.4)
        self.clear_scene()


def tag_like(text, color):
    """A small chip in the storage box: one piece of a checkpoint."""
    t = label(text, font_size=16, color=color)
    r = RoundedRectangle(width=t.width + 0.35, height=0.42, corner_radius=0.08, stroke_color=color, stroke_width=1.5,
                         fill_color=BG, fill_opacity=1)
    t.move_to(r)
    return VGroup(r, t)


_ = (LAM,)
