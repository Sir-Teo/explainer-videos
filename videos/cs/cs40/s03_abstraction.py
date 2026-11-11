from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load)


class Abstraction(VoiceoverScene):
    def construct(self):
        self.card()
        self.adt()
        self.contracts()
        self.subtyping()
        self.hyrum()

    def card(self):
        card = chapter_card(2, r"Abstraction and contracts", r"What exactly does an interface promise?",
                            lit=(1974, 1994), extra=((1974, r"Liskov and Zilles: \ abstract data types"),
                                                     (1986, r"Meyer: \ design by contract"),
                                                     (1994, r"Liskov and Wing: \ behavioural subtyping")),
                            part=PART)
        with self.voiceover("Chapter two. Abstraction and contracts."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def adt(self):
        head = label(r"Abstract data types", font_size=36).to_edge(UP, buff=0.3)
        code = code_block([
            "class IntSet:",
            "    # rep: a sorted list with no repeats",
            "    def __init__(self):  self._xs = []",
            "    def add(self, x):",
            "        i = bisect_left(self._xs, x)",
            "        if i == len(self._xs) or self._xs[i] != x:",
            "            self._xs.insert(i, x)",
            "    def contains(self, x): ...",
            "    def size(self): return len(self._xs)",
        ], size=17).move_to([-3.2, -0.2, 0])
        notes = VGroup(
            wrapped_label(r"\textbf{abstract data type} \ (Liskov and Zilles, 1974): \ a type known only by its "
                          r"operations \ --- \ Parnas' hiding, \ built into the language \ (CLU)", 5.6, font_size=20,
                          color=WHITE),
            wrapped_label(r"\textbf{representation invariant}: \ which lists are legal: \ sorted, \ no repeats", 5.6,
                          font_size=20, color=HEAD),
            wrapped_label(r"\textbf{abstraction function}: \ what a legal list means: \ the set of its elements", 5.6,
                          font_size=20, color=YES),
            wrapped_label(r"each operation must keep the invariant; \ then \texttt{size} is correct \textit{because} "
                          r"there are no repeats", 5.6, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "Barbara Liskov and Stephen Zilles gave Parnas' idea a form a compiler can enforce. "
            "<bookmark mark='a'/> An abstract data type is known only by its operations; its representation is "
            "private. Here a set of integers is represented by a list. <bookmark mark='b'/> Two pieces of "
            "reasoning make such a type correct. The representation invariant says which lists are legal: sorted, "
            "with no repeats. <bookmark mark='c'/> The abstraction function says what a legal list means: the set "
            "of its elements. <bookmark mark='d'/> Every operation must preserve the invariant, and then the others "
            "may rely on it: size can simply return the length of the list, because the invariant guarantees there "
            "are no repeats. Liskov later received the Turing Award for this work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            for mk, n in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()

    def contracts(self):
        head = label(r"Design by contract", font_size=36).to_edge(UP, buff=0.3)
        code = code_block([
            "def withdraw(acct, amount):",
            "    # requires: 0 < amount <= acct.balance",
            "    # ensures:  acct.balance == old(acct.balance) - amount",
            "    # keeps:    acct.balance >= 0      (invariant)",
            "    assert 0 < amount <= acct.balance",
            "    acct.balance -= amount",
        ], size=18).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            wrapped_label(r"\textbf{precondition}: \ the caller's obligation; \ \textbf{postcondition}: \ the "
                          r"callee's \ (Meyer, \ Eiffel, \ 1986)", 12.4, font_size=23, color=HEAD),
            wrapped_label(r"a failed precondition is the caller's bug; \ a failed postcondition is the "
                          r"implementation's", 12.4, font_size=23, color=NO),
            wrapped_label(r"the same triples as Hoare logic \ (Part 54), \ checked at run time instead of proved: \ "
                          r"assertions, \ Python's type hints with checkers, \ Rust's types, \ Ada's \texttt{Pre} and "
                          r"\texttt{Post}", 12.4, font_size=23, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(code, DOWN, buff=0.55)
        with self.voiceover(
            "Bertrand Meyer turned interfaces into contracts. <bookmark mark='a'/> A precondition is what the caller "
            "must guarantee: here, a positive amount no larger than the balance. A postcondition is what the "
            "function then guarantees in return: the balance went down by exactly that amount. An invariant holds "
            "before and after every operation. <bookmark mark='b'/> Contracts settle arguments: if a precondition "
            "fails, the caller has the bug; if a postcondition fails, the implementation does. "
            "<bookmark mark='c'/> They are the triples of Hoare logic, which Part 54 will prove, checked at run time "
            "instead: assertions, type checkers, and contract clauses in languages like Eiffel and Ada. Checking "
            "contracts costs time, so many teams check them in tests and debug builds and switch the expensive "
            "ones off in production; others keep them on, preferring a clear crash to silently wrong results."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            for mk, l in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def subtyping(self):
        r = load("lsp")
        sq = r["square"]
        head = label(r"When is a subtype a subtype?", font_size=36).to_edge(UP, buff=0.3)
        code = code_block([
            "class Square(Rectangle):",
            "    def set_width(self, w):  self.w = self.h = w",
            "    def set_height(self, h): self.w = self.h = h",
            "# a client written for rectangles:",
            "def client_expects(r, w, h):",
            "    r.set_width(w); r.set_height(h)",
            "    return r.area() == w * h",
        ], size=17).move_to([-3.2, 0.6, 0])
        res = VGroup(
            label(rf"Rectangle: \ property holds in {r['rectangle']['trials']:,} random trials", font_size=20,
                  color=YES),
            label(rf"Square: \ fails at trial {sq['failed_after']}, \ $(w, h) = ({sq['first'][0]}, {sq['first'][1]})$",
                  font_size=20, color=NO),
            label(rf"shrunk to the smallest failing case: \ $(w, h) = ({sq['shrunk'][0]}, {sq['shrunk'][1]})$",
                  font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.5, 1.0, 0])
        rules = VGroup(
            label(r"\textbf{Liskov and Wing, 1994}: \ S is a subtype of T when, \ for every method,", font_size=21,
                  color=WHITE),
            label(r"preconditions are no stronger, \ postconditions no weaker,", font_size=21, color=HEAD),
            label(r"invariants are kept, \ and no new way of changing the state appears", font_size=21, color=HEAD),
            label(r"Square changes height when asked to change width: \ not a behavioural subtype", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Inheritance adds a trap. A square is a rectangle in geometry. <bookmark mark='a'/> So make Square a "
            "subclass of Rectangle, and keep the sides equal by changing both whenever either is set. "
            "<bookmark mark='b'/> A client that was written for rectangles expects that after setting width w and "
            "height h, the area is w times h. We tested that property the way QuickCheck does, on random inputs. "
            "<bookmark mark='c'/> On rectangles it held a thousand times out of a thousand. On squares it failed on "
            "the first try, and shrinking found the smallest failing case: width zero, height one, area one. "
            "<bookmark mark='d'/> Barbara Liskov and Jeannette Wing made the rule precise in 1994. A subtype may "
            "demand no more and promise no less than its parent, must keep its invariants, and must not add new "
            "ways of changing state. Square adds one: setting the width changes the height. In code, it is not a "
            "rectangle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code[:3]))
            vo.wait_until("b")
            self.play(FadeIn(code[3:]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in res], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(rules))
        self.wait(0.4)
        self.clear_scene()

    def hyrum(self):
        head = label(r"Interfaces in time", font_size=36).to_edge(UP, buff=0.3)
        inner = Circle(radius=1.05, color=YES, fill_opacity=0.15).set_fill(YES).move_to([-3.6, -0.2, 0])
        outer = Circle(radius=2.2, color=NO, stroke_width=2).move_to([-3.6, -0.2, 0])
        il = label(r"documented \\ interface", font_size=18, color=YES).move_to(inner)
        obs = VGroup(*[label(t, font_size=16, color=NO).move_to([-3.6 + 1.65 * math.cos(a), -0.2 + 1.65 *
                                                                 math.sin(a), 0])
                       for t, a in ((r"timing", 0.4), (r"error text", 1.5), (r"iteration order", 2.6),
                                    (r"rounding", 3.7), (r"bugs", 4.8), (r"memory use", 5.7))])
        lines = VGroup(
            wrapped_label(r"\textbf{Hyrum's law}: \ with enough users, \ every observable behaviour of an interface "
                          r"will be depended on by somebody, \ whatever the contract says \ (Hyrum Wright, Google)",
                          5.6, font_size=20, color=NO),
            wrapped_label(r"\textbf{semantic versioning}: \ MAJOR.MINOR.PATCH; \ bump MAJOR for any incompatible "
                          r"change, \ MINOR for additions, \ PATCH for fixes \ (Part 41 solves the constraints this "
                          r"creates)", 5.6, font_size=20, color=HEAD),
            wrapped_label(r"Python's dictionaries kept insertion order by accident in 3.6; \ so much code came to "
                          r"rely on it that 3.7 made it a promise", 5.6, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, -0.2, 0])
        with self.voiceover(
            "Contracts describe interfaces at one moment, but interfaces live for years. <bookmark mark='a'/> Inside "
            "is the documented behaviour. Around it is everything else a user can observe: timing, the text of "
            "error messages, the order in which a collection is iterated, rounding, even the bugs. "
            "<bookmark mark='b'/> Hyrum Wright, at Google, put it as a law: with enough users, every observable "
            "behaviour will be depended on by somebody, whatever the contract says. Changing any of it breaks "
            "someone. <bookmark mark='c'/> Semantic versioning tries to make change legible: the major number "
            "rises for incompatible changes, the minor for additions, the patch for fixes, and Part 41 will solve "
            "the constraint puzzles this creates. <bookmark mark='d'/> A real case: Python's dictionaries started "
            "keeping insertion order in version 3.6 as an accident of a new implementation. So much code came to "
            "rely on it that version 3.7 made it part of the language."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(inner), FadeIn(il), Create(outer), LaggedStart(*[FadeIn(o) for o in obs],
                                                                            lag_ratio=0.2))
            for mk, l in zip("bcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN)
