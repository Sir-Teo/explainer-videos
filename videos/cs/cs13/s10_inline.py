from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, mono, region)


class Inline(WatchScene):
    def construct(self):
        self.card()
        self.inline()
        self.alias()

    def card(self):
        self.chapter(9, r"Inlining and aliasing", r"What can one function know about another?", lit=(1953,), extra=((1953, r"Rice's theorem"),), part=PART, said="Chapter nine. Inlining and aliasing.")

    def inline(self):
        self.ask(r"Inline a small function. \\ Besides the call itself, what do you gain?", [r"nothing",
                 r"the optimizer can see both sides at once"], 1,
                 say="Inline a small function into its caller. Apart from saving the call, what do you gain?",
                 reveal="The optimizer sees caller and callee together, and can simplify across the old boundary.")
        p = load("passes")
        head = label(r"Inlining: \ copy the callee into the caller", font_size=34).to_edge(UP, buff=0.3)
        caller = code(["while p != null {", "    if p.length == n &&", "       same(p.letters, w, n) {",
                       "        return p;", "    }", "    p = p.next;", "}"], size=16)
        callee = code(["fn same(a: *char, b: *char, n: int) -> int {", "    var i: int = 0;", "    while i < n {",
                       "        if a[i] != b[i] { return 0; }", "        i = i + 1;", "    }", "    return 1;", "}"],
                      size=16, color=FUNC)
        VGroup(caller, callee).arrange(RIGHT, buff=1.0, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        call = SurroundingRectangle(caller[2], color=FUNC, buff=0.05)
        arr = CurvedArrow(callee.get_left() + DOWN * 0.3, caller[2].get_right() + RIGHT * 0.1, angle=-0.6,
                          color=FUNC, stroke_width=2, tip_length=0.14)
        gains = VGroup(
            label(r"no call: \ no argument moves, \ no saved registers, \ no jump and return", font_size=20,
                  color=GREY_A),
            label(r"and the body now sees the caller's context: \ its constants, \ its loop", font_size=20,
                  color=GREY_A),
            label(r"the price: \ code size. \ Ours copies only small, non-recursive functions \ (under 40 IR "
                  r"instructions)", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(VGroup(caller, callee), DOWN, buff=0.5)
        r = p["rows"]
        meas = label(rf"list Job: \ {r[7]['list']:,} $\to$ {r[8]['list']:,} \ "
                     rf"({100 * (r[8]['list'] - r[7]['list']) / r[7]['list']:+.1f}\%); \ array Job: \ no small "
                     r"function to inline, \ no change", font_size=20, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So far every optimization has worked inside one function. But a call is a wall: the caller cannot "
            "see what the callee does. <bookmark mark='a'/> In the list Job, lookup calls same for every entry "
            "of the right length, to compare the letters. <bookmark mark='b'/> Inlining copies same's body into "
            "lookup, in place of the call, with the arguments substituted for the parameters. <bookmark mark='c'/> "
            "That saves the call itself: moving the arguments, saving registers, the jump and the return. And "
            "more importantly, the body now sits inside the caller's loop, where the other passes can see it "
            "together with everything around it. <bookmark mark='d'/> The price is code size, and a copy for every "
            "call site. Our compiler inlines only small functions that are not recursive. Clang weighs an "
            "estimated cost against a threshold for each call site. <bookmark mark='e'/> On the list Job, inlining "
            "saves four percent. The array Job has no small function in its hot loop, so nothing changes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(caller))
            vo.wait_until("a")
            self.play(Create(call))
            vo.wait_until("b")
            self.play(FadeIn(callee), Create(arr))
            vo.wait_until("c")
            self.play(FadeIn(gains[:2]))
            vo.wait_until("d")
            self.play(FadeIn(gains[2]))
            vo.wait_until("e")
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()


    def alias(self):
        head = label(r"Aliasing: \ can two names mean the same memory?", font_size=34).to_edge(UP, buff=0.3)
        ex = code(["*p = 1;", "*q = 2;", "x = *p;     // 1?"], size=22).next_to(head, DOWN, buff=0.5).to_edge(LEFT,
                                                                                                         buff=1.0)
        ans = VGroup(label(r"only if $p$ and $q$ cannot point to the same place", font_size=21, color=GREY_A),
                     label(r"if they may: \ reload, \ every time", font_size=21, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(ex, RIGHT, buff=0.8)
        kinds = VGroup(
            label("\\textbf{overlap}: different widths may alias; C character accesses can inspect object bytes",
                  font_size=20, color=GREY_A),
            label(r"\textbf{by address taken}: \ a local whose address is never taken has no alias at all",
                  font_size=20, color=GREY_A),
            label(r"\textbf{points-to analysis}: \ the set of objects each pointer may hold \ (Andersen 1994, "
                  r"\ Steensgaard 1996)", font_size=20, color=GREY_A),
            label("\\textbf{contracts}: C \\texttt{restrict}; Rust reference rules and unsafe obligations", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ex, DOWN, buff=0.6).to_edge(LEFT, buff=1.0)
        with self.voiceover("A central memory question is whether two accesses can overlap. <bookmark mark='a'/> Store one through p, then two through q, then load through p. If the addresses overlap, the second store can change the answer. Even different access widths can overlap in byte-addressed memory. <bookmark mark='b'/> Compilers combine several kinds of evidence: object identities, address calculations, points-to sets, language aliasing rules and function summaries. C's character-type access is an important exception to type-based alias assumptions: a byte store can change an integer's representation. Our conservative repaired loop pass does not use width alone as proof of independence. C restrict is a contract the program must honor; Rust's reference rules and unsafe code have their own requirements. A missed optimization is preferable to silently assuming an alias cannot exist.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(ex), run_time=0.6)
            vo.wait_until('a')
            self.play(FadeIn(ans))
            vo.wait_until('b')
            self.play(LaggedStart(*[FadeIn(k) for k in kinds], lag_ratio=0.6), run_time=6)
        self.wait(0.3)
        self.clear_scene()

