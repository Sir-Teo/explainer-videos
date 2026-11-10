from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table,
                                   load, mono, words)


def box_(text, color, w=2.2, h=0.55, fs=17):
    r = Rectangle(width=w, height=h, color=color, stroke_width=2).set_fill(color, 0.1)
    return VGroup(r, label(text, font_size=fs, color=color).move_to(r))


class Dispatch(VoiceoverScene):
    def construct(self):
        self.card()
        self.vtables()
        self.beyond()
        self.exceptions()

    def card(self):
        card = chapter_card(12, r"Dynamic dispatch and exceptions", r"Which code runs, \ and how does it get out?",
                            lit=(1967,), extra=((1967, r"Simula 67: \ virtual procedures"),), part=PART)
        with self.voiceover("Chapter twelve. Dynamic dispatch and exceptions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def vtables(self):
        d = load("dispatch")
        head = label(r"Virtual calls and vtables", font_size=34).to_edge(UP, buff=0.3)
        src = code(["struct Shape { virtual uint64_t area(uint64_t x) const = 0; };",
                    "struct Sq  : Shape { uint64_t area(uint64_t x) const override { return x * x; } };",
                    "struct Tri : Shape { uint64_t area(uint64_t x) const override { return x * x / 2; } };",
                    "s->area(i);      // which area?"], size=15, color=CODE).next_to(head, DOWN, buff=0.35)
        obj_sq = box_("Sq object: vptr", DATA, w=2.6)
        obj_tr = box_("Tri object: vptr", DATA, w=2.6)
        vt_sq = box_("Sq vtable: area", FUNC, w=2.8)
        vt_tr = box_("Tri vtable: area", FUNC, w=2.8)
        f_sq = box_("Sq::area", YES, w=2.0)
        f_tr = box_("Tri::area", YES, w=2.0)
        col1 = VGroup(obj_sq, obj_tr).arrange(DOWN, buff=0.5)
        col2 = VGroup(vt_sq, vt_tr).arrange(DOWN, buff=0.5)
        col3 = VGroup(f_sq, f_tr).arrange(DOWN, buff=0.5)
        diag = VGroup(col1, col2, col3).arrange(RIGHT, buff=0.9).next_to(src, DOWN, buff=0.45)
        ars = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=2, tip_length=0.12)
                       for a, b in ((obj_sq, vt_sq), (obj_tr, vt_tr), (vt_sq, f_sq), (vt_tr, f_tr))])
        tab = grid_table([r"one call, \ on this machine \ (g++ \texttt{-O2})", r"ns"], [
            [r"a direct call", f"{d['direct_ns']:.2f}"],
            [r"a virtual call, \ always the same class", f"{d['virtual_mono_ns']:.2f}"],
            [r"a virtual call, \ alternating classes", f"{d['virtual_poly_ns']:.2f}"],
        ], widths=[6.2, 1.6], row_h=0.46, font_size=19, mono_cols=(),
            colors=[[WHITE, YES], [WHITE, DATA], [WHITE, NO]]).next_to(diag, DOWN, buff=0.4)
        protocol=label('devirtualization disabled; best of three; checked uint64 arithmetic',font_size=17,color=GREY_B).next_to(tab,DOWN,buff=.16)
        with self.voiceover(
            (
            "When s points to a shape, which area function runs? <bookmark mark='a'/> A common C++ ABI gives a "
            "polymorphic object a vptr leading to a table of method addresses. This diagram shows that "
            "implementation, rather than a language-mandated object layout. <bookmark mark='b'/> The virtual call "
            "reads the method address and calls through it. Compilers can remove this dispatch when they can "
            "prove the target. <bookmark mark='c'/> Our repaired benchmark deliberately disables "
            "devirtualization, uses opaque call boundaries and defined unsigned arithmetic, checks every "
            "checksum, and verifies an indirect call in the virtual loop's assembly. The table shows the best of "
            "three runs on this host. Loop overhead and branch prediction remain part of the measurement; the "
            "ordering is not a universal law."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(col1), FadeIn(col2), Create(ars[:2]))
            vo.wait_until("b")
            self.play(FadeIn(col3), Create(ars[2:]))
            vo.wait_until("c")
            self.play(FadeIn(tab),FadeIn(protocol))
        self.wait(0.3)
        self.clear_scene()

    def beyond(self):
        head = label(r"Interfaces, \ and dispatch on every argument", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"\textbf{single} dispatch: \ the receiver's class picks the method \ (C++, Java, Python)",
                  font_size=22, color=GREY_A),
            label(r"an \textbf{interface} can be implemented by unrelated classes: \ no fixed slot for its method",
                  font_size=22, color=GREY_A),
            label(r"Java searches an itable, \ and caches the answer at the call site; \ Go builds one table "
                  r"per (type, interface) pair", font_size=21, color=GREY_A),
            label(r"\textbf{multiple} dispatch: \ every argument's type picks the method \ (CLOS, \ Julia)",
                  font_size=22, color=DATA),
            label(r"\texttt{collide(a::Asteroid, b::Ship)}: \ the classic case single dispatch handles badly",
                  font_size=21, color=CODE),
            label('static specialization can remove dispatch; dyn traits and dictionaries may remain',
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            (
            "A dispatch mechanism chooses code from runtime type information. <bookmark mark='a'/> Single "
            "dispatch uses the receiver's type. <bookmark mark='b'/> An interface may be implemented by unrelated "
            "concrete types, so a runtime needs an appropriate method mapping rather than assuming one universal "
            "class-table slot. <bookmark mark='c'/> JVM implementations use interface lookup and caching; Go "
            "interface values carry type-and-method information. These details are implementation choices. "
            "<bookmark mark='d'/> Multiple dispatch, as in Julia or CLOS, chooses using several argument types. "
            "<bookmark mark='e'/> Rust can monomorphize generic trait calls, but dyn trait objects dispatch "
            "dynamically. Haskell type-class dictionaries can also survive at runtime unless specialization "
            "removes them. Static types alone do not imply that every call has zero dispatch cost."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", [pts[0], pts[1], pts[2], pts[3:5], pts[5]]):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def exceptions(self):
        d = load("dispatch")
        head = label('Table-driven exception costs', font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"g++ \texttt{-O2}, \ on this machine", r"per call"], [
            [r"a plain call", f"{d['plain_ns']:.2f} ns"],
            [r"the same call inside \texttt{try \{ \} catch}, \ nothing thrown", f"{d['try_ns']:.2f} ns"],
            [r"\texttt{setjmp} before each call \ (C's way)", f"{d['setjmp_ns']:.2f} ns"],
            [r"a \texttt{throw}, \ caught one frame up", f"{d['throw_ns']:.0f} ns"],
        ], widths=[7.2, 2.2], row_h=0.5, font_size=20, mono_cols=(),
            colors=[[WHITE, WHITE], [WHITE, YES], [WHITE, DATA], [WHITE, NO]]).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"\textbf{zero-cost} exceptions: \ the compiler writes tables, \ beside the code, \ from each "
                  r"range of instructions to its handler", font_size=20, color=GREY_A),
            label(r"nothing runs on entry to a \texttt{try}; \ a \texttt{throw} searches the tables and unwinds the "
                  r"stack frame by frame", font_size=20, color=GREY_A),
            label(r"\texttt{setjmp} pays on every entry instead, \ to make the jump cheap", font_size=20,
                  color=GREY_A),
            label('zero-cost fast path does not mean zero metadata or optimization cost',
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        ratio = d["throw_ns"] / d["plain_ns"]
        with self.voiceover(
            (
            "Exception implementations move costs to different paths. <bookmark mark='a'/> The table compares a "
            "plain call and a call that may throw, inside a handler, using our checked benchmark. Their measured "
            "times need not be identical. <bookmark mark='b'/> This platform uses table-driven unwinding: "
            "entering a try region does not register a handler dynamically. A throw searches metadata and unwinds "
            "frames. Zero-cost names this fast-path strategy, not zero code-size, optimization or cache cost. "
            "<bookmark mark='c'/> setjmp instead saves state on entry. This test measures that registration path; "
            "it does not time a longjmp. <bookmark mark='d'/> Throwing and constructing the exception has the "
            "displayed cost in this shallow example. The number depends on the exception, stack depth, ABI and "
            "machine, so use it as a measured case rather than a fixed ratio for all programs."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]],
                      FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[4])), FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()
