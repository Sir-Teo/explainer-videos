from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (HEAD, NO, PART, T0C, T1C, YES, grid_table, load, mono)


class Models(VoiceoverScene):
    def construct(self):
        self.card()
        self.compiler()
        self.hb()
        self.drf()
        self.langs()

    def card(self):
        card = chapter_card(9, r"Memory models", r"What may a load return?", lit=(1979, 1990, 2011),
                            extra=((1979, r"Lamport: \ SC"), (1990, r"Adve and Hill: \ DRF"), (2011, r"C11, \ C++11")),
                            part=PART)
        with self.voiceover("Chapter nine. Memory models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def compiler(self):
        d = load("hoist")
        head = label(r"The compiler reorders too", font_size=36).to_edge(UP, buff=0.3)
        src = VGroup(*[mono(t, 17, WHITE) for t in d["plain"]["src"][2:6]]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        asm = VGroup(*[mono(t, 17, NO if "jmp .L3" in t else GREY_A) for t in d["plain"]["asm"]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        sa = VGroup(label(r"C, \ \texttt{int done}:", font_size=19, color=T0C), src).arrange(DOWN, aligned_edge=LEFT,
                                                                                              buff=0.1)
        aa = VGroup(label(r"\texttt{gcc -O2}, \ on this machine:", font_size=19, color=NO), asm).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        asm2 = VGroup(*[mono(t, 17, YES if "je" in t else GREY_A) for t in d["atomic"]["asm"]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        ab = VGroup(label(r"with \texttt{atomic\_load(acquire)}:", font_size=19, color=YES), asm2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        g = VGroup(sa, aa, ab).arrange(RIGHT, buff=0.55, aligned_edge=UP).next_to(head, DOWN, buff=0.4)
        if g.width > 13.4:
            g.width = 13.4
            g.next_to(head, DOWN, buff=0.4)
        lines = VGroup(
            label(r"the compiler sees no write to \texttt{done} in the loop: \ it reads it \textbf{once}; \ if it "
                  r"was 0, \ \texttt{jmp .L3} spins forever", font_size=20, color=NO),
            label(r"legal, \ because a data race has no defined meaning: \ the compiler may assume no other thread "
                  r"writes", font_size=20, color=WHITE),
            label(r"an atomic load must be done every time: \ the loop reads \texttt{done} on each pass", font_size=20,
                  color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Hardware is not the only thing that reorders. <bookmark mark='a'/> Here is a thread waiting for another "
            "to set a flag, written in plain C, with an ordinary int. <bookmark mark='b'/> And here is what the C "
            "compiler on this machine makes of it, with optimisation on. It loads done once. If it is not set, it "
            "jumps to a label that jumps to itself, forever. <bookmark mark='c'/> The compiler saw no write to done "
            "inside the loop, so it read it only once. <bookmark mark='d'/> That is perfectly legal, because a data "
            "race has no defined meaning, so the compiler may assume that no other thread writes the flag. <bookmark "
            "mark='e'/> Declare the flag atomic, and every pass of the loop must load it again. The same model tells "
            "both the processor and the compiler what they may not do."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sa))
            vo.wait_until("b")
            self.play(FadeIn(aa))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(ab), FadeIn(lines[2]))
        del g
        self.wait(0.3)
        self.clear_scene()

    def hb(self):
        head = label(r"Happens-before", font_size=36).to_edge(UP, buff=0.3)
        ta = VGroup(*[RoundedRectangle(width=2.6, height=0.55, corner_radius=0.06, stroke_color=T0C,
                                       fill_color=T0C, fill_opacity=0.15) for _ in range(3)]).arrange(DOWN, buff=0.5)
        tb = VGroup(*[RoundedRectangle(width=2.6, height=0.55, corner_radius=0.06, stroke_color=T1C,
                                       fill_color=T1C, fill_opacity=0.15) for _ in range(3)]).arrange(DOWN, buff=0.5)
        VGroup(ta, tb).arrange(RIGHT, buff=3.0).move_to([-1.2, 0.3, 0])
        for b, t in zip(ta, ("data = 42", "unlock(m)", "...")):
            b.add(mono(t, 18, WHITE).move_to(b))
        for b, t in zip(tb, ("...", "lock(m)", "r = data")):
            b.add(mono(t, 18, WHITE).move_to(b))
        po = VGroup(*[Arrow(x[i].get_bottom(), x[i + 1].get_top(), buff=0.05, color=GREY_B, stroke_width=2)
                      for x in (ta, tb) for i in range(2)])
        sync = Arrow(ta[1].get_right(), tb[1].get_left(), buff=0.08, color=YES, stroke_width=3)
        sl = label(r"synchronizes with", font_size=18, color=YES).next_to(sync, UP, buff=0.08)
        notes = VGroup(
            label(r"\textbf{program order} within a thread", font_size=20, color=GREY_A),
            label(r"\textbf{synchronizes-with}: \\ an unlock and the next lock of it", font_size=20, color=YES),
            label(r"\textbf{happens-before}: \\ the transitive closure of both \\ (Lamport 1978, \ Part 38)",
                  font_size=20, color=WHITE),
            label(r"a \textbf{data race}: \ two accesses to one \\ variable, \ at least one a write, \\ not ordered by "
                  r"happens-before", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.1)
        with self.voiceover(
            "Every modern language answers the question of what a load may return with the same idea. <bookmark "
            "mark='a'/> Within a thread, operations are ordered by the program. <bookmark mark='b'/> Between threads, "
            "certain pairs synchronize: an unlock of a mutex, and a later lock of the same mutex. <bookmark mark='c'/> "
            "Happens-before is the order you get by following both kinds of arrow, transitively, Lamport's idea from "
            "1978 that Part 38 uses between computers. Here the write of data happens before the read. <bookmark "
            "mark='d'/> A data race is two accesses to the same variable, at least one a write, that happens-before "
            "does not order. The hook's counter is full of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ta), FadeIn(tb))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in po], lag_ratio=0.2), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(sync), FadeIn(sl), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def drf(self):
        d = load("drf")
        lt = load("litmus")["models"]
        head = label(r"The bargain: \ data-race-free means sequentially consistent", font_size=32).to_edge(UP, buff=0.3)
        fmt = lambda xs: r", \ ".join(f"({a},{b})" for a, b in xs)
        tab = grid_table([r"model", r"store buffering, \ racy", r"the same, \ every access locked"], [
            [r"SC", fmt(lt["sc"]["sb"]), fmt(d["locked"]["sc"])],
            [r"TSO", fmt(lt["tso"]["sb"]), fmt(d["locked"]["tso"])],
            [r"PSO", fmt(lt["pso"]["sb"]), fmt(d["locked"]["pso"])],
        ], widths=[1.6, 5.0, 5.0], row_h=0.6, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        for i in (2, 3):
            tab.cells[i][1].set_color(NO)
        lines = VGroup(
            label(r"outcomes $(r_1, r_2)$ the checker finds: \ with the races removed, \ TSO and PSO give exactly SC's",
                  font_size=21, color=WHITE),
            label(r"\textbf{Adve and Hill, \ 1990}: \ if every SC execution of a program is race-free, \ the hardware "
                  r"may reorder as it likes \ and the program still behaves as if SC", font_size=21, color=YES),
            label(r"the programmer's side: \ no races; \ the hardware's and compiler's: \ fences at every "
                  r"synchronization", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.16).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Modern memory models rest on one bargain. <bookmark mark='a'/> Take the store-buffering test. With its "
            "races, total and partial store order allow an outcome that sequential consistency forbids: both loads "
            "read zero. <bookmark mark='b'/> Now put every shared access under a lock. The checker finds that under "
            "all three models, exactly the same outcomes remain, the sequentially consistent ones. <bookmark "
            "mark='c'/> Sarita Adve and Mark Hill made this a theorem in 1990. If a program has no data races in any "
            "sequentially consistent execution, then the hardware may reorder as much as it likes, and the program "
            "will still behave as if executed in sequence. <bookmark mark='d'/> So the programmer's side of the "
            "bargain is: no data races. The other side, for the hardware and the compiler, is to put the right fences "
            "at every lock, unlock and atomic operation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(r[0], r[1])) for r in tab.cells[1:]])
            vo.wait_until("b")
            self.play(*[FadeIn(r[2]) for r in tab.cells[1:]], FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def langs(self):
        head = label(r"Atomics in C++ and Java", font_size=36).to_edge(UP, buff=0.3)
        code = VGroup(mono("std::atomic<bool> ready{false};  int data;", 19, GREY_A),
                      mono("// writer", 19, T0C),
                      mono("data = 42;", 19, WHITE),
                      mono("ready.store(true, std::memory_order_release);", 19, WHITE),
                      mono("// reader", 19, T1C),
                      mono("while (!ready.load(std::memory_order_acquire)) ;", 19, WHITE),
                      mono("assert(data == 42);    // guaranteed", 19, YES)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.08)
        box = SurroundingRectangle(code, color=GREY_D, buff=0.18, corner_radius=0.08)
        cg = VGroup(box, code).next_to(head, DOWN, buff=0.4)
        items = VGroup(
            label(r"\textbf{release}: \ nothing before it moves after it; \ \textbf{acquire}: \ nothing after it moves "
                  r"before it", font_size=20, color=WHITE),
            label(r"a release-store read by an acquire-load is a synchronizes-with edge: \ chapter 4's message "
                  r"passing, \ repaired", font_size=20, color=YES),
            label(r"Java 5 \ (Manson, Pugh and Adve, 2005); \ C11 and C++11 \ (Boehm and Adve, 2008): \ races are "
                  r"undefined behaviour in C++", font_size=20, color=HEAD),
            label(r"still unsolved: \ \textbf{out-of-thin-air} values, \ which relaxed atomics seem to permit and no "
                  r"machine produces", font_size=20, color=NO),
        ).arrange(DOWN, buff=0.15).next_to(cg, DOWN, buff=0.35)
        with self.voiceover(
            "Languages give programmers atomic variables to synchronize with. <bookmark mark='a'/> Here the writer "
            "stores the data, then sets a flag with release ordering: nothing before the release may be moved after "
            "it. The reader loads the flag with acquire ordering: nothing after it may be moved before it. <bookmark "
            "mark='b'/> When the acquire reads the value the release wrote, the two synchronize, and the data is "
            "guaranteed to be there. This is chapter four's message passing, repaired. <bookmark mark='c'/> Java "
            "adopted such a model in 2005, and C and C plus plus in 2011, after work by Hans Boehm and Sarita Adve. In "
            "C plus plus, a data race is undefined behaviour: the program has no meaning at all. <bookmark mark='d'/> "
            "And one problem is still open. With the weakest, relaxed atomics, the formal models seem to allow a "
            "value to appear out of thin air, justified by a circular argument, though no real machine produces one. "
            "Nobody has yet found a definition that forbids it without forbidding useful optimisations too."
        ) as vo:
            self.play(FadeIn(head), Create(box), FadeIn(code))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
        self.wait(0.3)
        self.clear_scene()
