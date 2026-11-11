from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (DATA, HEAD, KERN, LAM, NO, PART, T1C, T2C, YES, grid_table, load, num,
                                   precedence_view, schedule_view)


class Locking(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_phase()
        self.deadlock()
        self.policies()

    def card(self):
        card = chapter_card(10, r"Two-phase locking", r"How can a scheduler guarantee serializability as it goes?",
                            lit=(1976, 1978), extra=((1976, r"Eswaran et al.: \ two-phase locking"),
                                                     (1978, r"Rosenkrantz et al.: \ wait-die, \ wound-wait")),
                            part=PART)
        with self.voiceover("Chapter ten. Two-phase locking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def two_phase(self):
        head = label(r"Lock, \ then unlock: \ never lock again", font_size=36).to_edge(UP, buff=0.3)
        mat = grid_table([r"held \ $\backslash$ \ asked", r"shared \ (read)", r"exclusive \ (write)"],
                         [[r"shared", r"\checkmark", r"wait"], [r"exclusive", r"wait", r"wait"]],
                         widths=[2.3, 1.8, 2.0], row_h=0.45, font_size=19, mono_cols=())
        mat.move_to([-3.7, 1.6, 0])
        mat.cells[1][1].set_color(YES)
        for r, c in ((1, 2), (2, 1), (2, 2)):
            mat.cells[r][c].set_color(NO)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 4, 1], x_length=5.6, y_length=2.4,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False}).move_to([3.4, 1.3, 0])
        steps = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 3), (6, 2), (7, 1), (8, 1), (9, 0)]
        pts = []
        for (x0, y0), (x1, _) in zip(steps, steps[1:]):
            pts += [ax.c2p(x0, y0), ax.c2p(x1, y0)]
        curve_ = VMobject(color=HEAD, stroke_width=3).set_points_as_corners(pts)
        lp = DashedLine(ax.c2p(4.5, 0), ax.c2p(4.5, 3.6), color=KERN)
        lpl = label(r"lock point", font_size=17, color=KERN).next_to(lp, UP, buff=0.05)
        grow = label(r"growing", font_size=17, color=YES).move_to(ax.c2p(2, 3.3))
        shrink = label(r"shrinking", font_size=17, color=NO).move_to(ax.c2p(7, 3.3))
        yl = label(r"locks held", font_size=16, color=GREY_B).next_to(ax.y_axis, LEFT, buff=0.1).rotate(PI / 2)
        lines = VGroup(
            label(r"\textbf{2PL}: \ a transaction acquires all its locks before it releases any", font_size=20,
                  color=HEAD),
            label(r"why it works: \ if $T_i \rightarrow T_j$ in the conflict graph, \ $T_j$ got a lock $T_i$ "
                  r"released, \ so $T_i$'s lock point comes first", font_size=20, color=WHITE),
            label(r"a cycle would put a lock point before itself: \ so no cycle, \ and the schedule is "
                  r"serializable, \ in lock-point order", font_size=20, color=YES),
            label(r"\textbf{strict} 2PL holds write locks until commit, \ so no one reads a value that may yet be "
                  r"undone", font_size=20, color=LAM),
            label(r"what to lock: \ rows, \ pages, \ tables; \ Gray's \textit{intention} locks mix sizes; \ "
                  r"locking ranges stops \textit{phantoms} \ (rows that appear)", font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(mat, DOWN, buff=0.55).set_x(0)
        for ln in lines:
            if ln.width > 12.8:
                ln.width = 12.8
        with self.voiceover(
            "The classic answer is locking. <bookmark mark='a'/> Before reading an item, a transaction takes a shared "
            "lock on it; before writing, an exclusive lock. Many readers can share, but a writer excludes everyone, "
            "and a request that conflicts must wait. <bookmark mark='b'/> Locks alone are not enough. The rule that "
            "makes them work is two-phase locking: a transaction may acquire locks, then release them, but never "
            "acquire another after its first release. Its locks grow, peak, and shrink. <bookmark mark='c'/> Here is "
            "why this suffices. If T i comes before T j in the conflict graph, then T j obtained a lock that T i had "
            "released, so T i passed its peak, its lock point, first. <bookmark mark='d'/> A cycle in the graph would "
            "put some lock point before itself, which is impossible. So every schedule two-phase locking allows is "
            "serializable, equivalent to running the transactions in the order of their lock points. "
            "<bookmark mark='e'/> In practice the locks are held until commit, strict two-phase locking, so that "
            "nobody reads a value that might still be rolled back. <bookmark mark='f'/> And there are choices about "
            "what to lock, rows or pages or whole tables, and how to lock ranges, so that a new row cannot appear in "
            "the middle of someone's query."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mat))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(yl), FadeIn(lines[0]))
            self.play(Create(curve_), FadeIn(grow), FadeIn(shrink), run_time=1.4)
            vo.wait_until("c")
            self.play(Create(lp), FadeIn(lpl), FadeIn(lines[1]))
            for mk, ln in zip("def", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def deadlock(self):
        lk = load("locking")
        ex = lk["deadlock_example"]
        head = label(r"Deadlock", font_size=36).to_edge(UP, buff=0.3)
        progs = VGroup(label(r"$T_1$: \ read $A$, \ then write $B$", font_size=21, color=T1C),
                       label(r"$T_2$: \ read $B$, \ then write $A$", font_size=21, color=T2C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.4)
        wanted = [(1, "r", "A"), (2, "r", "B"), (1, "w", "B"), (2, "w", "A")]
        sv = schedule_view(wanted).next_to(progs, DOWN, buff=0.5)
        waits = VGroup(*[label(r"waits", font_size=16, color=NO).next_to(sv.chips[i], DOWN, buff=0.08) for i in (2, 3)])
        g = precedence_view([(1, 2), (2, 1)], [1, 2], r=1.0).next_to(sv, RIGHT, buff=1.2)
        gl = label(r"waits-for graph", font_size=18, color=GREY_B).next_to(g, UP, buff=0.12)
        actual = schedule_view([tuple(s) for s in ex["schedule"]]).next_to(sv, DOWN, buff=0.85).align_to(sv, LEFT)
        al = label(r"what our scheduler did", font_size=18, color=YES).next_to(actual, UP, buff=0.12).align_to(actual,
                                                                                                           LEFT)
        lines = VGroup(
            label(r"each holds a shared lock the other needs exclusively: \ neither can move, \ ever", font_size=20,
                  color=NO),
            label(rf"the scheduler finds the cycle and aborts a victim, \ $T_{ex['aborted'][0]}$, \ which "
                  r"releases its lock and can retry", font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Locking has a price. <bookmark mark='a'/> T1 reads A and will write B; T2 reads B and will write A. "
            "<bookmark mark='b'/> Run them interleaved. Each takes its shared lock. Then T1 asks for B, which T2 holds, "
            "and waits; T2 asks for A, which T1 holds, and waits. <bookmark mark='c'/> Each waits for the other, and "
            "will wait forever: a deadlock, the cycle in the waits-for graph that Part 33 met in the dining "
            "philosophers. <bookmark mark='d'/> A database does not prevent it by careful lock order, because "
            "transactions are written by users. It finds the cycle and aborts one transaction, which releases its "
            "locks. Our scheduler aborted T2, and T1 finished. T2 can simply be run again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(progs))
            vo.wait_until("b")
            self.play(FadeIn(sv), FadeIn(waits))
            vo.wait_until("c")
            self.play(FadeIn(g), FadeIn(gl), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(actual), FadeIn(al), FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def policies(self):
        lk = load("locking")
        P = lk["policies"]
        head = label(r"Detect, \ or prevent?", font_size=36).to_edge(UP, buff=0.3)
        desc = VGroup(
            label(r"\textbf{detect}: \ let them wait; \ look for cycles in the waits-for graph; \ abort one",
                  font_size=20, color=HEAD),
            label(r"\textbf{wait-die}: \ an older transaction may wait for a younger; \ a younger one asking an "
                  r"older \textit{dies}", font_size=20, color=LAM),
            label(r"\textbf{wound-wait}: \ an older one \textit{wounds} \ (aborts) \ a younger holder; \ a younger "
                  r"one waits", font_size=20, color=KERN),
            label(r"waits only ever go one way in age, \ so no cycle can form; \ the restarted keep their age, \ "
                  r"so none starves", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(head, DOWN, buff=0.35)
        rows = [[k, f"{v['serializable']} / {v['runs']}", num(v["deadlocks"]), num(v["aborts"]), num(v["waits"])]
                for k, v in P.items()]
        tab = grid_table([r"400 random runs: \ policy", r"serializable", r"deadlocks", r"aborts", r"waits"], rows,
                         widths=[3.6, 2.2, 2.0, 1.8, 1.8], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(desc, DOWN, buff=0.45).set_x(0)
        for r in range(1, 4):
            tab.cells[r][1].set_color(YES)
        foot = label(r"prevention never deadlocks, \ but aborts twice as often, \ often needlessly; \ detection "
                     r"aborts only real cycles, \ and waits more", font_size=19, color=HEAD).next_to(tab, DOWN,
                                                                                                  buff=0.35)
        with self.voiceover(
            "There are two families of remedy. <bookmark mark='a'/> Detection lets transactions wait, and looks for "
            "cycles. <bookmark mark='b'/> Prevention uses age. In wait-die, an older transaction may wait for a "
            "younger one, but a younger one that asks for an older one's lock is aborted on the spot. "
            "<bookmark mark='c'/> In wound-wait, it is the other way round: an older transaction aborts the younger "
            "holder, and a younger one waits. <bookmark mark='d'/> Either way, waiting only goes in one direction of "
            "age, so no cycle can form, and a restarted transaction keeps its original age, so it eventually becomes "
            "the oldest and wins. <bookmark mark='e'/> We ran four hundred random mixes of four transactions under "
            "each policy. Every resulting schedule passed the serializability check. Detection found 342 deadlocks "
            "and aborted only those; the prevention schemes never deadlocked, but aborted more than twice as many "
            "transactions, many of which would never have deadlocked. That is why most systems detect."
        ) as vo:
            self.play(FadeIn(head))
            for mk, d in zip("abcd", desc):
                vo.wait_until(mk)
                self.play(FadeIn(d))
            vo.wait_until("e")
            self.play(FadeIn(tab))
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA,)
