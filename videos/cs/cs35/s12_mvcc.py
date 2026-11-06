from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, KERN, LAM, NO, PART, T1C, T2C, YES, grid_table, load,
                                   precedence_view)


def version(txt, color, w=1.5):
    r = RoundedRectangle(width=w, height=0.5, corner_radius=0.06, stroke_color=color, stroke_width=1.8,
                         fill_color=BLACK, fill_opacity=0)
    return VGroup(r, Text(txt, font="DejaVu Sans Mono", font_size=15, color=color).move_to(r))


class Mvcc(VoiceoverScene):
    def construct(self):
        self.card()
        self.optimism()
        self.versions()
        self.doctors()
        self.ssi()

    def card(self):
        card = chapter_card(11, r"Optimism and snapshots", r"Can readers and writers stop blocking each other?",
                            lit=(1981, 1995, 2008), extra=((1981, r"Kung and Robinson: \ optimistic control"),
                                                           (2008, r"Cahill et al.: \ serializable snapshots")),
                            part=PART)
        with self.voiceover("Chapter eleven. Optimism and snapshots."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def optimism(self):
        head = label(r"Don't lock: \ check at the end", font_size=36).to_edge(UP, buff=0.3)
        phases = VGroup(*[box_ for box_ in (
            VGroup(Rectangle(width=4.2, height=0.7, stroke_color=DATA, fill_color=DATA, fill_opacity=0.15),
                   label(r"read: \ work on private copies", font_size=19, color=DATA)),
            VGroup(Rectangle(width=2.4, height=0.7, stroke_color=KERN, fill_color=KERN, fill_opacity=0.15),
                   label(r"validate", font_size=19, color=KERN)),
            VGroup(Rectangle(width=2.6, height=0.7, stroke_color=YES, fill_color=YES, fill_opacity=0.15),
                   label(r"write: \ install", font_size=19, color=YES)))]).arrange(RIGHT, buff=0.05)
        for p in phases:
            p[1].move_to(p[0])
        phases.next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            label(r"\textbf{optimistic} control \ (Kung and Robinson, 1981): \ at commit, \ did anyone who committed "
                  r"meanwhile write what I read? \ If so, \ restart", font_size=20, color=KERN),
            label(r"no waiting and no deadlock; \ wins when conflicts are rare, \ loses when they are common", font_size=20,
                  color=WHITE),
            label(r"\textbf{timestamp ordering}: \ give each transaction a number at start; \ reject any operation "
                  r"that arrives too late for that order", font_size=20, color=HEAD),
            label(r"all three \ (locks, \ validation, \ timestamps) \ yield serializable schedules; \ they differ in "
                  r"who waits and who restarts", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(phases, DOWN, buff=0.6).set_x(0)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Locking is pessimistic: it assumes conflict and makes transactions wait. <bookmark mark='a'/> H. T. Kung "
            "and John Robinson proposed the opposite in 1981. Let each transaction run freely on private copies, and "
            "check only at the end: did any transaction that committed in the meantime write something I read? If "
            "not, install my writes; if so, start again. <bookmark mark='b'/> Nobody waits and nothing deadlocks. "
            "When conflicts are rare this is fast; when they are common, work is thrown away again and again. "
            "<bookmark mark='c'/> A third method gives each transaction a timestamp when it starts, and rejects any "
            "read or write that arrives too late to fit that order. <bookmark mark='d'/> All three produce "
            "serializable schedules. They differ in who waits, and who starts over."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in phases], lag_ratio=0.3), FadeIn(lines[0]))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def versions(self):
        head = label(r"Keep the old versions", font_size=36).to_edge(UP, buff=0.3)
        chain = VGroup(version("x=10 @3", GREY_B), version("x=25 @7", DATA), version("x=40 @12", HEAD)).arrange(
            RIGHT, buff=0.55).next_to(head, DOWN, buff=0.8)
        arrows = VGroup(*[Arrow(chain[i + 1].get_left(), chain[i].get_right(), buff=0.05, color=GREY_C,
                                stroke_width=1.8) for i in range(2)])
        cl = label(r"each write makes a new version, \ stamped with its writer's commit time", font_size=19,
                   color=WHITE).next_to(chain, UP, buff=0.2)
        reader = VGroup(label(r"a reader that started at time 9 sees", font_size=19, color=T1C),
                        Text("x=25", font="DejaVu Sans Mono", font_size=18, color=T1C)).arrange(RIGHT, buff=0.2)
        reader.next_to(chain, DOWN, buff=0.5)
        lines = VGroup(
            label(r"\textbf{MVCC} \ (Reed, 1978): \ a transaction reads the \textbf{snapshot} as of its start, \ the "
                  r"newest version committed before it", font_size=20, color=HEAD),
            label(r"readers never wait for writers, \ and writers never wait for readers", font_size=20, color=YES),
            label(r"two writers of the same item: \ the first to commit wins, \ the other aborts", font_size=20,
                  color=NO),
            label(r"\textbf{snapshot isolation}: \ Oracle's \texttt{SERIALIZABLE}, \ PostgreSQL's \texttt{REPEATABLE READ}; "
                  r"\ old versions are garbage-collected \ (VACUUM)", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(reader, DOWN, buff=0.55).set_x(0)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "What most databases actually do today is keep the old versions. <bookmark mark='a'/> Each write creates "
            "a new version of the item, stamped with the time its transaction committed, and the old ones remain. "
            "<bookmark mark='b'/> A transaction that started at time nine reads the newest version committed before "
            "nine, here twenty-five, however many writes have come since. <bookmark mark='c'/> It sees a consistent "
            "snapshot of the whole database as of its start. This is multiversion concurrency control, from David "
            "Reed's thesis of 1978. <bookmark mark='d'/> Readers never wait for writers, and writers never wait for "
            "readers. <bookmark mark='e'/> Only two writers of the same item collide, and the first to commit wins. "
            "<bookmark mark='f'/> This is snapshot isolation. It is what Oracle gives when you ask for serializable, and "
            "what PostgreSQL gives at repeatable read. It feels serializable. It is not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(chain), FadeIn(arrows), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(reader), Indicate(chain[1], color=T1C))
            for mk, ln in zip("cdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def doctors(self):
        iso = load("isolation")
        d = iso["doctors"]
        head = label(r"Write skew: \ two doctors on call", font_size=36).to_edge(UP, buff=0.3)
        rule = label(r"the rule: \ at least one doctor on call. \ Each runs: \ if two are on call, \ take myself off",
                     font_size=20, color=WHITE).next_to(head, DOWN, buff=0.3)
        progs = VGroup()
        for t, who, c in ((1, "alice", T1C), (2, "bob", T2C)):
            p = VGroup(*[Text(s, font="DejaVu Sans Mono", font_size=16, color=c) for s in (
                f"T{t}: n = on_call(alice) + on_call(bob)",
                f"    if n >= 2: on_call({who}) = 0",
                "    COMMIT")]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            progs.add(p)
        progs.arrange(RIGHT, buff=0.9).next_to(rule, DOWN, buff=0.4)
        snap = label(r"under snapshot isolation both read the snapshot \ alice = 1, \ bob = 1, \ so both see $n = 2$",
                     font_size=20, color=HEAD).next_to(progs, DOWN, buff=0.4)
        rows = []
        for lv in ("read committed", "snapshot", "snapshot + SSI", "serializable"):
            r = d[lv]
            rows.append([lv, f"alice {r['db']['alice']}, bob {r['db']['bob']}",
                         ", ".join(f"T{t}" for t in r["committed"]) or "none",
                         ", ".join(f"T{t}" for t in r["aborted"]) or "none"])
        tab = grid_table([r"run in our database at", r"afterwards", r"committed", r"aborted"], rows,
                         widths=[3.4, 3.2, 2.0, 1.8], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(snap, DOWN, buff=0.35).set_x(0)
        for r, lv in enumerate(("read committed", "snapshot", "snapshot + SSI", "serializable"), start=1):
            ok = d[lv]["db"]["alice"] + d[lv]["db"]["bob"] >= 1
            tab.cells[r][1].set_color(YES if ok else NO)
        foot = label(r"the two transactions write \textit{different} rows, \ so first-committer-wins never fires; \ no "
                     r"serial order could leave nobody on call", font_size=19, color=NO).next_to(tab, DOWN, buff=0.3)
        with self.voiceover(
            "Here is the classic counterexample. A hospital requires at least one doctor on call. Alice and Bob are "
            "both on call, and both feel ill. <bookmark mark='a'/> Each runs the same transaction: count the doctors "
            "on call, and if there are two, take myself off. <bookmark mark='b'/> Under snapshot isolation, both "
            "start from the same snapshot, both count two, and Alice takes herself off while Bob takes himself off. "
            "<bookmark mark='c'/> Our database, run at each isolation level, shows the result. At read committed and "
            "at snapshot isolation, both commit, and nobody is on call. <bookmark mark='d'/> The two transactions "
            "wrote different rows, so the first-committer rule never fired. Yet in any serial order the second would "
            "have counted one and stayed. This anomaly is write skew. At the serializable level, with two-phase "
            "locking, one of them is aborted and the rule holds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rule))
            vo.wait_until("a")
            self.play(FadeIn(progs))
            vo.wait_until("b")
            self.play(FadeIn(snap))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    def ssi(self):
        head = label(r"Serializable snapshot isolation", font_size=36).to_edge(UP, buff=0.3)
        g = precedence_view([(1, 2), (2, 1)], [1, 2], r=1.3).next_to(head, DOWN, buff=0.7).shift(LEFT * 3)
        e1 = label(r"$T_1$ read bob, \ which $T_2$ then wrote", font_size=18, color=T1C)
        e2 = label(r"$T_2$ read alice, \ which $T_1$ then wrote", font_size=18, color=T2C)
        el = VGroup(label(r"\textbf{rw-antidependencies}: \ I read a version someone overwrote", font_size=20,
                          color=WHITE), e1, e2).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(g, RIGHT, buff=1.0)
        lines = VGroup(
            label(r"Fekete et al. \ (2005): \ every snapshot anomaly contains a transaction with an rw-edge \textit{in} "
                  r"and an rw-edge \textit{out}", font_size=20, color=HEAD),
            label(r"Cahill, \ R\"ohm and Fekete \ (2008): \ track rw-edges as transactions run, \ and abort such a "
                  r"\textit{pivot} before it commits", font_size=20, color=YES),
            label(r"in our database: \ $T_1$ aborted, \ alice stays on call; \ readers still never block", font_size=20,
                  color=LAM),
            label(r"PostgreSQL's \texttt{SERIALIZABLE} has worked this way since 2011; \ the price is some false "
                  r"aborts", font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(g, DOWN, buff=0.6).set_x(0)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "Can snapshots be made serializable without giving up their speed? <bookmark mark='a'/> Look at what "
            "happened. T1 read Bob's row, which T2 then overwrote: an arrow from T1 to T2, called a read-write "
            "antidependency. And T2 read Alice's row, which T1 overwrote: an arrow back. A cycle. "
            "<bookmark mark='b'/> Alan Fekete and colleagues proved in 2005 that every anomaly of snapshot isolation "
            "contains a transaction with such an arrow coming in and another going out. <bookmark mark='c'/> In 2008 "
            "Michael Cahill turned this into an algorithm: track the read-write arrows as transactions run, and abort "
            "any transaction that becomes such a pivot. <bookmark mark='d'/> Our database implements it. T1 is "
            "aborted, Alice stays on call, and readers still never wait. <bookmark mark='e'/> PostgreSQL has used this "
            "method for its serializable level since 2011. Its cost is an occasional abort that was not strictly "
            "necessary."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(el))
            for mk, ln in zip("bcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


_ = (CODE, DATA, NO)
