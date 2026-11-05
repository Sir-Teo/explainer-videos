from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table,
                                   load, mono, words)


def box_(text, color, w=2.2, h=0.55, fs=17):
    r = Rectangle(width=w, height=h, color=color, stroke_width=2).set_fill(color, 0.1)
    return VGroup(r, mono(text, fs, color).move_to(r))


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
        src = code(["struct Shape { virtual long area(long x) const = 0; };",
                    "struct Sq  : Shape { long area(long x) const override { return x * x; } };",
                    "struct Tri : Shape { long area(long x) const override { return x * x / 2; } };",
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
        with self.voiceover(
            "Chapter eleven's inline caches answer a question every object-oriented language asks: when the "
            "program says s arrow area, which area runs? <bookmark mark='a'/> C++ answers it with a table, as "
            "Simula did in 1967. Each object holds a hidden pointer, the vptr, to its class's virtual table, and "
            "the table holds the addresses of the class's methods. <bookmark mark='b'/> A virtual call is two "
            "loads and an indirect call: the object's table, the method's entry, then jump. <bookmark mark='c'/> "
            "We timed two hundred million calls on this machine. A direct call: half a nanosecond. A virtual call "
            "to the same class every time: about one, because the branch predictor learns the target. Alternate "
            "between two classes and it costs a little more again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(col1), FadeIn(col2), Create(ars[:2]))
            vo.wait_until("b")
            self.play(FadeIn(col3), Create(ars[2:]))
            vo.wait_until("c")
            self.play(FadeIn(tab))
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
            label(r"and Rust's traits and Haskell's classes resolve most calls at compile time: \ no dispatch at all",
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Vtables work because a class has one fixed list of virtual methods. <bookmark mark='a'/> That is single "
            "dispatch: only the receiver's class chooses. <bookmark mark='b'/> Interfaces break the fixed list. "
            "Unrelated classes can implement the same interface, so its methods cannot sit at the same slot in "
            "every table. <bookmark mark='c'/> Java looks the method up in an interface table and caches the "
            "result at the call site, an inline cache again; Go builds a small table for each pair of a concrete "
            "type and an interface, the first time it is needed. <bookmark mark='d'/> Some languages dispatch on "
            "every argument. In Common Lisp's object system and in Julia, the method for collide is chosen by the "
            "types of both the asteroid and the ship. <bookmark mark='e'/> And languages with traits or type "
            "classes resolve most calls during compilation, where dispatch costs nothing at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", [pts[0], pts[1], pts[2], pts[3:5], pts[5]]):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def exceptions(self):
        d = load("dispatch")
        head = label(r"Exceptions: \ zero cost, \ until thrown", font_size=34).to_edge(UP, buff=0.3)
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
            label(r"exceptions are for the exceptional: \ a thrown one costs as much as two thousand calls",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        ratio = d["throw_ns"] / d["plain_ns"]
        with self.voiceover(
            "Chapter three built an exception from a continuation. Compiled languages implement them differently, "
            "and again we can measure the trade. <bookmark mark='a'/> A plain call costs half a nanosecond. Put it "
            "inside a try block, where nothing is ever thrown, and it costs exactly the same. <bookmark mark='b'/> "
            "That is because C++ compilers use zero-cost exceptions. Nothing happens when a try block is entered. "
            "Instead the compiler writes tables next to the code, mapping each range of instructions to its "
            "handler, and only a throw reads them, unwinding the stack one frame at a time. <bookmark mark='c'/> "
            "C's setjmp makes the opposite trade: it saves the registers on every entry, two and a half "
            "nanoseconds here, so that the jump out is cheap. <bookmark mark='d'/> And the throw itself costs "
            "about nine hundred nanoseconds, nearly two thousand plain calls. Exceptions are free if they are "
            "exceptional."
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
