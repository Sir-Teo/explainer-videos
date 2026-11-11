from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table

V0, V1, VB = DATA, LAM, HEAD          # 0-valent, 1-valent, bivalent


def node(color=GREY_B, r=0.17, fill=0.9):
    return Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=fill)


def edge(a, b, txt=None, color=GREY_B, dashed=False, side=UP, size=18, buff=0.2):
    """An arrow between two mobjects, optionally labelled (text) beside its middle."""
    if dashed:
        ar = DashedLine(a.get_center(), b.get_center(), buff=buff, color=color, stroke_width=2,
                        dash_length=0.08).add_tip(tip_length=0.16)
    else:
        ar = Arrow(a.get_center(), b.get_center(), buff=buff, color=color, stroke_width=2.5,
                   max_tip_length_to_length_ratio=0.18)
    if txt is None:
        return VGroup(ar)
    t = label(txt, font_size=size, color=color).next_to(ar.get_center(), side, buff=0.1)
    return VGroup(ar, t)


def cell(content, w=1.25, h=0.62, color=GREY_B):
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=1.6,
                          fill_color=BG, fill_opacity=1)
    return VGroup(fr, content.move_to(fr))


def vs(v, s, color=WHITE):
    """A register's content: a value and its sequence number."""
    return VGroup(MathTex(str(v), font_size=28, color=color),
                  MathTex(rf"\#{s}", font_size=19, color=GREY_B)).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)


class Shared(VoiceoverScene):
    def construct(self):
        self.card()
        self.registers()
        self.snapshot()
        self.ladder()
        self.regproof()
        self.tasproof()

    def card(self):
        card = chapter_card(6, r"Shared memory and the consensus hierarchy", r"Which shared objects let $n$ "
                            r"processes agree?", lit=(1991, 1993),
                            extra=((1991, r"Herlihy: \ consensus numbers"), (1993, r"Afek et al.: \ snapshots")),
                            part=PART)
        with self.voiceover("Chapter six. Shared memory and the consensus hierarchy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def registers(self):
        head = label(r"Registers, \ and waiting for no one", font_size=36).to_edge(UP, buff=0.3)
        ys = [1.7, 0.85, 0.0]
        x0, x1 = -6.0, 1.2
        lanes = VGroup()
        for y, nm in zip(ys, ("p", "q", "r")):
            lanes.add(Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=1.5))
            lanes.add(MathTex(nm, font_size=26, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.15))
        ops = [(0, -5.6, -3.8, r"write 1", -4.4, LAM), (1, -4.6, -2.4, r"read: \ 1", -3.0, DATA),
               (2, -3.4, -1.0, r"write 2", -1.8, LAM), (0, -1.6, 0.9, r"read: \ 2", -0.5, DATA)]
        bars, pts = VGroup(), VGroup()
        for lane, a, b, t, lx, c in ops:
            r = RoundedRectangle(width=b - a, height=0.4, corner_radius=0.08, stroke_color=c, stroke_width=1.6,
                                 fill_color=c, fill_opacity=0.25).move_to([(a + b) / 2, ys[lane], 0])
            bars.add(VGroup(r, label(t, font_size=17, color=WHITE).move_to(r)))
            pts.add(Dot([lx, ys[lane] - 0.2, 0], radius=0.07, color=HEAD).set_z_index(3))
        yseq = -1.15
        seq = Line([x0, yseq, 0], [x1, yseq, 0], color=GREY_B, stroke_width=2)
        drops = VGroup(*[DashedLine(p.get_center(), [p.get_x(), yseq, 0], color=HEAD, stroke_width=1.2,
                                    dash_length=0.06) for p in pts])
        sdots = VGroup(*[Dot([p.get_x(), yseq, 0], radius=0.07, color=HEAD) for p in pts])
        snames = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(d, DOWN, buff=0.12) for d, t in
                          zip(sdots, (r"write 1", r"read 1", r"write 2", r"read 2"))])
        seql = label(r"one sequential history", font_size=18, color=HEAD).next_to(seq, LEFT, buff=0.15)
        seql.next_to(seq, DOWN, buff=0.6).align_to(seq, LEFT)
        ill = note(r"illustrative history", font_size=16).next_to(seql, RIGHT, buff=0.4)
        W = 4.7
        notes = VGroup(
            wrapped_label(r"an \textbf{atomic register}: \ read and write, \ each as if at one instant inside its "
                          r"interval \ (linearizable, \ Part 33)", W, font_size=19),
            wrapped_label(r"\textbf{wait-free}: \ every operation ends in a bounded number of its own steps, \ "
                          r"even if every other process has crashed", W, font_size=19, color=HEAD),
            wrapped_label(r"so up to $n - 1$ crashes: \ no locks, \ no waiting for anyone", W, font_size=19,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.35, 0.5, 0])
        with self.voiceover(
            "Now the processes share memory instead of sending messages. <bookmark mark='a'/> The simplest shared "
            "object is an atomic register. Processes read it and write it, and each operation, though it takes "
            "time, behaves as if it happened at one instant inside its interval. Part 33 called this "
            "linearizability. <bookmark mark='b'/> A read that overlaps a write may return the old value or the "
            "new one, but the instants line up into one sequential history. <bookmark mark='c'/> The standard of "
            "progress is wait-freedom: every operation finishes in a bounded number of its own steps, even if all "
            "the other processes have crashed. No locks, and no waiting for anyone. That is the shared-memory "
            "version of surviving n minus one crashes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.35), FadeIn(notes[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.3))
            self.play(Create(seq), FadeIn(seql), FadeIn(ill))
            self.play(*[Create(d) for d in drops], *[TransformFromCopy(p, s) for p, s in zip(pts, sdots)])
            self.play(FadeIn(snames))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def snapshot(self):
        head = label(r"A snapshot from registers", font_size=36).to_edge(UP, buff=0.3)
        xs = [-4.4, -2.9, -1.4]
        regs = VGroup(*[cell(vs(v, s)).move_to([x, 1.75, 0]) for x, (v, s) in zip(xs, ((5, 1), (7, 1), (2, 1)))])
        rn = VGroup(*[MathTex(rf"R_{k + 1}", font_size=24, color=GREY_A).next_to(regs[k], UP, buff=0.1)
                      for k in range(3)])
        wn = label(r"each written only by its owner", font_size=16, color=GREY_B).next_to(rn, UP, buff=0.1)
        rows_y = [0.55, -0.35, -1.25]
        rl = VGroup(*[label(rf"collect {k + 1}", font_size=18, color=GREY_A).move_to([-6.0, y, 0])
                      for k, y in enumerate(rows_y)])
        vals = [[(5, 1), (7, 1), (2, 1)], [(5, 1), (8, 2), (2, 1)], [(5, 1), (8, 2), (2, 1)]]

        def row(k):
            return VGroup(*[cell(vs(v, s), color=GREY_D).move_to([x, rows_y[k], 0]) for x, (v, s) in
                            zip(xs, vals[k])])
        crow = [row(k) for k in range(3)]
        ptr = SurroundingRectangle(regs[0], buff=0.06, color=HEAD, stroke_width=2.4)
        verdict = [label(r"$R_2$ changed: \ retry", font_size=18, color=NO).next_to(crow[1], RIGHT, buff=0.25),
                   label(r"equal: \ a snapshot", font_size=18, color=YES).next_to(crow[2], RIGHT, buff=0.25)]
        W = 5.3
        notes = VGroup(
            wrapped_label(r"\textbf{scan}: \ all $n$ values at one instant; \ \textbf{update}: \ write your own", W,
                          font_size=19),
            wrapped_label(r"two equal collects in a row: \ nothing changed between them \ (sequence numbers), \ so "
                          r"the collect is a true snapshot", W, font_size=19, color=YES),
            wrapped_label(r"but busy writers can make a scanner retry for ever", W, font_size=19, color=NO),
            wrapped_label(r"fix: \ each update first scans and stores that scan beside its value; \ a scanner that "
                          r"sees one process move \textit{twice} borrows its scan, \ taken wholly inside its own", W,
                          font_size=19, color=HEAD),
            wrapped_label(r"at most $n + 1$ collects: \ wait-free, \ from registers alone", W, font_size=19,
                          color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([3.95, 0.1, 0])
        src = note(r"Afek, \ Attiya, \ Dolev, \ Gafni, \ Merritt and Shavit \ (1993)", font_size=16).next_to(
            notes, DOWN, buff=0.25).align_to(notes, LEFT)
        ill = note(r"illustrative values", font_size=16).next_to(crow[2], DOWN, buff=0.3).align_to(rl, LEFT)

        def collect(k, between=None):
            for j in range(3):
                self.play(ptr.animate.move_to(regs[j]), run_time=0.25)
                self.play(TransformFromCopy(regs[j], crow[k][j]), run_time=0.45)
                if between is not None and j == between[0]:
                    between[1]()
        new2 = cell(vs(8, 2)).move_to(regs[1])

        def write2():
            self.play(Transform(regs[1], new2), Flash(regs[1], color=LAM), run_time=0.7)
        with self.voiceover(
            "Reading many registers at once is harder than it looks. <bookmark mark='a'/> A snapshot object lets "
            "each process update its own register, and scan all of them as if at one instant. Can we build it from "
            "registers? <bookmark mark='b'/> Collect: read the registers one by one. <bookmark mark='c'/> Meanwhile "
            "process two writes, and a second collect differs. <bookmark mark='d'/> Collect again. Two equal "
            "collects in a row mean nothing changed in between, so that collect is a true snapshot. "
            "<bookmark mark='e'/> But busy writers could make a scanner retry for ever. The fix, by Afek, Attiya, "
            "Dolev, Gafni, Merritt and Shavit in 1993: every update first takes a scan and stores it beside its "
            "value. A scanner that sees one process move twice borrows that process's scan, taken entirely during "
            "its own. After at most n plus one collects someone has moved twice, so every scan is wait-free."
        ) as vo:
            self.play(FadeIn(head), FadeIn(regs), FadeIn(rn), FadeIn(wn))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(rl[0]), FadeIn(ptr), FadeIn(ill))
            collect(0, between=(1, write2))
            vo.wait_until("c")
            self.play(FadeIn(rl[1]))
            collect(1)
            self.play(crow[1][1][0].animate.set_stroke(NO, width=2.4), FadeIn(verdict[0]))
            vo.wait_until("d")
            self.play(FadeIn(rl[2]))
            collect(2)
            self.play(*[c[0].animate.set_stroke(YES, width=2.4) for c in crow[2]], FadeIn(verdict[1]),
                      FadeOut(ptr))
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
            self.play(FadeIn(notes[3]))
            self.play(FadeIn(notes[4]), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def ladder(self):
        head = label(r"Herlihy's consensus hierarchy", font_size=36).to_edge(UP, buff=0.3)
        dfn = wrapped_label(r"the \textbf{consensus number} of an object $X$: \ the largest $n$ for which copies of "
                            r"$X$ and registers solve wait-free consensus among $n$ processes", 12.4, font_size=21,
                            color=WHITE).next_to(head, DOWN, buff=0.35)
        rungs = VGroup()
        for num, txt, c, y in ((r"1", r"read/write registers, \ snapshots", GREY_A, -2.2),
                               (r"2", r"test-and-set, \ swap, \ fetch-and-add, \ queues, \ stacks", DATA, -0.85),
                               (r"\infty", r"compare-and-swap, \ load-linked / store-conditional", KERN, 0.5)):
            n = MathTex(num, font_size=46, color=c).move_to([-5.9, y, 0])
            bar = Line([-5.4, y - 0.38, 0], [-0.4, y - 0.38, 0], color=c, stroke_width=3)
            t = wrapped_label(txt, 4.8, font_size=19, color=c).next_to(bar, UP, buff=0.12).align_to(bar, LEFT)
            rungs.add(VGroup(n, bar, t))
        rail = Line([-6.4, -2.75, 0], [-6.4, 1.0, 0], color=GREY_D, stroke_width=2).add_tip(tip_length=0.18)
        prog = code_block(["Q = [win, lose]   # shared", "prop[me] := v", "if deq(Q) == win:", "    decide v",
                           "else:", "    decide prop[other]"], size=18)
        pbox = SurroundingRectangle(prog, buff=0.2, color=GREY_D, corner_radius=0.08, stroke_width=1.4)
        pg = VGroup(pbox, prog).move_to([3.5, 0.0, 0])
        pcap = label(r"two processes agree with a queue", font_size=18, color=DATA).next_to(pg, UP, buff=0.15)
        conseq = wrapped_label(r"no object implements a higher one wait-free: \ no wait-free queue from registers; "
                               r"\ with compare-and-swap, \ anything \ (universality, \ Part 33)", 6.0, font_size=19,
                               color=HEAD).next_to(pg, DOWN, buff=0.35)
        src = note(r"Herlihy \ (1991)", font_size=16).next_to(conseq, DOWN, buff=0.15).align_to(conseq, LEFT)
        with self.voiceover(
            "Maurice Herlihy turned this into a ranking in 1991. <bookmark mark='a'/> The consensus number of an "
            "object is the largest number of processes that can solve wait-free consensus using copies of it and "
            "registers. <bookmark mark='b'/> Registers, and even snapshots, have consensus number one. "
            "<bookmark mark='c'/> Test-and-set, swap, fetch-and-add, queues and stacks have two. Part 33 built "
            "two-process consensus from test-and-set; a queue does it too. Put win and then lose in the queue. "
            "Each process writes its proposal and dequeues: whoever gets win decides its own value, the other "
            "decides its rival's. <bookmark mark='d'/> Compare-and-swap, and load-linked with store-conditional, "
            "sit at infinity. <bookmark mark='e'/> The ranking has teeth: no object implements a higher one "
            "wait-free, so there is no wait-free queue built from registers alone."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dfn), Create(rail))
            vo.wait_until("b")
            self.play(FadeIn(rungs[0], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(rungs[1], shift=UP * 0.15))
            self.play(FadeIn(pg), FadeIn(pcap))
            vo.wait_until("d")
            self.play(FadeIn(rungs[2], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(conseq), FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def regproof(self):
        head = label(r"Registers cannot agree, \ even for two", font_size=36).to_edge(UP, buff=0.3)
        C = node(VB).move_to([-4.5, 2.0, 0])
        Cp = node(V0).move_to([-5.7, 0.75, 0])
        Cq = node(V1).move_to([-3.3, 0.75, 0])
        X = node(V0).move_to([-5.7, -0.5, 0])
        lc = MathTex(r"C", font_size=26, color=VB).next_to(C, RIGHT, buff=0.12)
        e1 = edge(C, Cp, r"$p$ steps", color=V0, side=LEFT)
        e2 = edge(C, Cq, r"$q$ steps", color=V1, side=RIGHT)
        e3 = edge(Cp, X, r"$q$ steps", color=V0, side=LEFT)
        lx = MathTex(r"q(p(C))", font_size=22, color=V0).next_to(X, DOWN, buff=0.12)
        lq = MathTex(r"q(C)", font_size=22, color=V1).next_to(Cq, DOWN, buff=0.12)
        crit = wrapped_label(r"\textbf{critical}: \ bivalent, \ and each next step fixes the valency \ (wait-free "
                             r"runs are finite, \ so following bivalent steps we reach one)", 5.6, font_size=18,
                             color=GREY_A).move_to([-3.7, -1.5, 0])
        rows = [[r"read", r"anything", r"the read changed only $p$"],
                [r"anything", r"read", r"the same, \ roles swapped"],
                [r"write $R$", r"write $S \ne R$", r"the steps commute"],
                [r"write $R$", r"write $R$", r"$q$'s write hides $p$'s"]]
        tab = grid_table([r"$p$'s step", r"$q$'s step", r"why $q$ cannot tell"], rows, widths=[1.35, 1.75, 3.4],
                         row_h=0.5, font_size=19, mono_cols=())
        tab.move_to([3.4, 1.15, 0])
        fs = 28
        der = [MathTex(r"q(p(C))", r"\overset{q}{\sim}", r"q(C)", font_size=fs),
               MathTex(r"d_q(q(p(C)))", r"=", r"d_q(q(C))", font_size=fs),
               MathTex(r"0", r"=", r"1", font_size=fs)]
        der[2][0].set_color(V0)
        der[2][2].set_color(V1)
        whys = [label(r"same memory, \ same state of $q$", font_size=18, color=GREY_B),
                label(r"$q$ runs alone \ ($p$ may have crashed): \ it must decide, \ and decides alike", font_size=18,
                      color=GREY_B),
                label(r"but one is 0-valent, \ the other 1-valent", font_size=18, color=NO)]
        col = VGroup()
        for r, w in zip(der, whys):
            w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
            col.add(VGroup(r, w))
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        concl = label(r"registers: \ consensus number 1", font_size=22, color=HEAD).to_edge(DOWN, buff=0.3).set_x(
            -3.7)
        with self.voiceover(
            "Why can registers not do it for even two processes? Part 33 sketched the argument; here are its "
            "cases. <bookmark mark='a'/> Every run of a wait-free protocol is finite, so following bivalent "
            "configurations we reach a critical one: bivalent, but p's next step makes it zero-valent and q's next "
            "step makes it one-valent. <bookmark mark='b'/> If p's step is a read, it changes only p. After q's "
            "step, the two configurations differ only inside p. A read by q is the same with roles swapped. "
            "<bookmark mark='c'/> If they write different registers, the steps commute, and the order cannot "
            "matter. <bookmark mark='d'/> If they write the same register, q's write hides p's. "
            "<bookmark mark='e'/> Either way q, running alone, sees the same memory and its own same state. It must "
            "decide, and decides alike, though one side was zero-valent and the other one-valent."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(C), FadeIn(lc))
            self.play(GrowArrow(e1[0]), FadeIn(e1[1]), FadeIn(Cp), GrowArrow(e2[0]), FadeIn(e2[1]), FadeIn(Cq))
            self.play(FadeIn(crit))
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            vo.wait_until("b")
            self.play(GrowArrow(e3[0]), FadeIn(e3[1]), FadeIn(X), FadeIn(lx), FadeIn(lq))
            self.play(FadeIn(VGroup(*tab.cells[1])))
            self.play(FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[3])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[4])))
            vo.wait_until("e")
            self.play(FadeIn(col[0]))
            self.play(TransformMatchingTex(der[0].copy(), der[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(der[1].copy(), der[2]), FadeIn(whys[2]))
            self.play(FadeIn(concl))
        self.wait(0.4)
        self.clear_scene()

    def tasproof(self):
        head = label(r"Why test-and-set stops at two", font_size=36).to_edge(UP, buff=0.3)
        C = node(VB).move_to([-3.4, 2.0, 0])
        A1 = node(V0).move_to([-5.0, 0.95, 0])
        B1 = node(V1).move_to([-1.8, 0.95, 0])
        X = node(V0).move_to([-5.0, -0.15, 0])
        Y = node(V1).move_to([-1.8, -0.15, 0])
        lc = label(r"critical, \ three processes", font_size=17, color=VB).next_to(C, UP, buff=0.12)
        ar = VGroup(edge(C, A1, r"$p$: \ TAS", color=V0, side=LEFT), edge(A1, X, r"$q$: \ TAS", color=V0, side=LEFT),
                    edge(C, B1, r"$q$: \ TAS", color=V1, side=RIGHT), edge(B1, Y, r"$p$: \ TAS", color=V1, side=RIGHT))

        def mem(won, color):
            g = VGroup(label(r"$T = 1$, \ registers equal", font_size=16, color=WHITE),
                       label(won, font_size=16, color=color)).arrange(DOWN, buff=0.08)
            fr = SurroundingRectangle(g, buff=0.12, color=color, corner_radius=0.08, stroke_width=1.4)
            return VGroup(fr, g)
        mx = mem(r"$p$ won, \ $q$ lost", V0).next_to(X, DOWN, buff=0.2)
        my = mem(r"$q$ won, \ $p$ lost", V1).next_to(Y, DOWN, buff=0.2)
        same = MathTex(r"\overset{r}{\sim}", font_size=34, color=HEAD).move_to((mx.get_center() + my.get_center()) / 2)
        rx = node(KERN, r=0.15).next_to(mx, DOWN, buff=0.6)
        ry = node(KERN, r=0.15).next_to(my, DOWN, buff=0.6)
        ra = VGroup()
        for box, tgt, sd in ((mx, rx, LEFT), (my, ry, RIGHT)):
            a = Arrow(box.get_bottom(), tgt.get_top(), buff=0.06, color=KERN, stroke_width=2.5,
                      max_tip_length_to_length_ratio=0.25)
            ra.add(VGroup(a, label(r"$r$ alone", font_size=18, color=KERN).next_to(a, sd, buff=0.1)))
        rd = label(r"$r$ decides the same: \ $0 = 1$", font_size=19, color=NO).next_to(VGroup(rx, ry), DOWN,
                                                                                      buff=0.2)
        W = 5.4
        notes = VGroup(
            wrapped_label(r"the two decisive steps must be test-and-sets on the \textit{same} object: \ reads and "
                          r"writes fall to the last proof, \ steps on different objects commute", W, font_size=19,
                          color=WHITE),
            wrapped_label(r"in either order the bit ends set and memory is equal; \ only $p$ and $q$ know who won",
                          W, font_size=19, color=GREY_A),
            wrapped_label(r"with two processes there is no $r$: \ test-and-set works for two \ (Part 33)", W,
                          font_size=19, color=YES),
            wrapped_label(r"compare-and-swap returns what it found, \ so even a third process learns who won", W,
                          font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.85, 0.1, 0])
        with self.voiceover(
            "The same method shows why test-and-set stops at two. <bookmark mark='a'/> Take three processes and a "
            "critical configuration. The two decisive steps must be test-and-sets on the same object: reads and "
            "writes fall to the last proof, and steps on different objects commute. <bookmark mark='b'/> Let p go "
            "first and then q, or q first and then p. Either way the bit ends up set and every register holds the "
            "same; only p and q know who won. <bookmark mark='c'/> Now the third process, r, runs alone. It sees "
            "the same memory and has the same state, so it decides the same, yet one side is zero-valent and the "
            "other one-valent. <bookmark mark='d'/> With only two processes there is no r, which is why "
            "test-and-set works for two. <bookmark mark='e'/> Compare-and-swap escapes because it returns what it "
            "found: anyone who looks learns who won."
        ) as vo:
            self.play(FadeIn(head), FadeIn(C), FadeIn(lc))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(ar[0][0]), FadeIn(ar[0][1]), FadeIn(A1), GrowArrow(ar[2][0]), FadeIn(ar[2][1]),
                      FadeIn(B1))
            self.play(GrowArrow(ar[1][0]), FadeIn(ar[1][1]), FadeIn(X), GrowArrow(ar[3][0]), FadeIn(ar[3][1]),
                      FadeIn(Y))
            self.play(FadeIn(mx), FadeIn(my), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(same))
            self.play(*[GrowArrow(a[0]) for a in ra], *[FadeIn(a[1]) for a in ra], FadeIn(rx), FadeIn(ry))
            self.play(FadeIn(rd))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM, YES)
