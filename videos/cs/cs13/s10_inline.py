from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, mono, region)


class Inline(VoiceoverScene):
    def construct(self):
        self.card()
        self.inline()
        self.callgraph()
        self.alias()
        self.rice()

    def card(self):
        card = chapter_card(9, r"Inlining and aliasing", r"What can one function know about another?",
                            lit=(1953,), extra=((1953, r"Rice's theorem"),), part=PART)
        with self.voiceover("Chapter nine. Inlining and aliasing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def inline(self):
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

    def callgraph(self):
        head = label(r"The call graph, \ and summaries", font_size=34).to_edge(UP, buff=0.3)
        pos = {"main": (0, 2.0), "lookup": (-2.6, 0.6), "report": (2.6, 0.6), "same": (-3.8, -0.8),
               "alloc": (-1.4, -0.8), "printnum": (2.6, -0.8), "getc": (-0.5, 0.6), "putc": (4.6, -0.8)}
        cols = {"getc": GREY_B, "putc": GREY_B, "alloc": GREY_B}
        nodes = {}
        for n, (x, y) in pos.items():
            t = mono(n, 16, WHITE)
            r = RoundedRectangle(width=t.width + 0.4, height=0.5, corner_radius=0.1, stroke_color=cols.get(n, YES),
                                 fill_color=cols.get(n, YES), fill_opacity=0.15, stroke_width=1.8).move_to([x, y, 0])
            nodes[n] = VGroup(r, t.move_to(r))
        calls = [("main", "lookup"), ("main", "report"), ("main", "getc"), ("lookup", "same"), ("lookup", "alloc"),
                 ("report", "printnum"), ("report", "putc"), ("printnum", "putc")]
        es = VGroup(*[Arrow(nodes[a][0].get_bottom(), nodes[b][0].get_top(), buff=0.05, color=GREY_B,
                            stroke_width=2, tip_length=0.13) if pos[b][1] < pos[a][1] else
                      Arrow(nodes[a][0].get_right(), nodes[b][0].get_left(), buff=0.05, color=GREY_B,
                            stroke_width=2, tip_length=0.13) for a, b in calls])
        g = VGroup(es, *nodes.values()).move_to(UP * 0.3)
        summ = VGroup(
            label(r"analyse bottom-up, \ callees first: \ a \textbf{summary} per function", font_size=21,
                  color=GREY_A),
            label(r"\texttt{same}: \ reads memory, \ never writes it, \ calls nothing", font_size=21, color=YES),
            label(r"so a call to \texttt{same} cannot change \texttt{p.next}: \ the load may be reused", font_size=21,
                  color=YES),
            label(r"our compiler has no summaries: \ a call stops LICM \ (until inlining removes it)",
                  font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where inlining does not apply, a compiler can still reason across calls. <bookmark mark='a'/> The call "
            "graph has a node for each function and an edge for each call. main calls lookup and report; lookup "
            "calls same and the allocator; report calls printnum. <bookmark mark='b'/> Analysing the graph from the "
            "bottom up, callees before callers, gives each function a summary. <bookmark mark='c'/> same reads "
            "memory but never writes it, and calls nothing. So a call to same cannot change p dot next, and a value "
            "loaded before the call is still good after it. <bookmark mark='d'/> Our compiler keeps no summaries, "
            "so for it any call is a wall: loop-invariant code motion gives up on a loop with a call in it, until "
            "inlining removes the call. Recursion makes the call graph cyclic, and then the summaries are found, "
            "once again, by iterating to a fixed point."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g))
            vo.wait_until("b")
            self.play(FadeIn(summ[0]))
            vo.wait_until("c")
            self.play(FadeIn(summ[1:3]), Indicate(nodes["same"], color=YES))
            vo.wait_until("d")
            self.play(FadeIn(summ[3]))
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
            label(r"\textbf{by type}: \ a byte store cannot change a word \ (our LICM); \ C's strict-aliasing rule",
                  font_size=20, color=GREY_A),
            label(r"\textbf{by address taken}: \ a local whose address is never taken has no alias at all",
                  font_size=20, color=GREY_A),
            label(r"\textbf{points-to analysis}: \ the set of objects each pointer may hold \ (Andersen 1994, "
                  r"\ Steensgaard 1996)", font_size=20, color=GREY_A),
            label(r"\textbf{by promise}: \ C's \texttt{restrict}; \ Rust's references, \ which the type system "
                  r"checks", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ex, DOWN, buff=0.6).to_edge(LEFT, buff=1.0)
        with self.voiceover(
            "Beneath all of this lies one question. <bookmark mark='a'/> Store one through p, store two through q, "
            "then load through p. Is the answer one? Only if p and q cannot point to the same place. If they might, "
            "the compiler must load again, and it cannot move either store past the other. <bookmark mark='b'/> "
            "Compilers answer the question in several ways. By type: a store of a byte cannot change a word, which "
            "is the rule our loop pass used, and C's strict aliasing rule extends the idea to every type. By "
            "address: a local whose address is never taken cannot be reached through any pointer. By points-to "
            "analysis, which computes the set of objects each pointer might hold; Andersen's and Steensgaard's "
            "algorithms trade precision against speed. And by promise: C's restrict keyword, or Rust's "
            "references, whose rules the type system checks."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ex))
            self.play(FadeIn(ans))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k) for k in kinds], lag_ratio=0.6), run_time=6)
        self.wait(0.3)
        self.clear_scene()

    def rice(self):
        head = label(r"Why it must be approximate: \ Rice's theorem", font_size=34).to_edge(UP, buff=0.3)
        thm = label(r"every nontrivial property of what a program \textit{does} \ is undecidable \ (Rice, 1953)",
                    font_size=23, color=HEAD).next_to(head, DOWN, buff=0.4)
        ex = code(["p = &y;", "run M on input w;     // any program", "p = &x;", "*p = 5;", "print(x);"],
                  size=20).next_to(thm, DOWN, buff=0.5)
        q = label(r"does \texttt{*p = 5} ever change \texttt{x}? \ \ Exactly when $M$ halts on $w$", font_size=22,
                  color=NO).next_to(ex, DOWN, buff=0.4)
        out = VGroup(
            label(r"so every analysis answers ``yes'', \ ``no'' \ or \ ``maybe''", font_size=21, color=GREY_A),
            label(r"and is \textbf{sound} if it treats ``maybe'' as ``yes'': \ never wrong, \ sometimes slower",
                  font_size=21, color=YES),
            label(r"exact alias analysis is undecidable \ (Landi 1992; \ Ramalingam 1994); \ the proof: \ Part 25",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.15).next_to(q, DOWN, buff=0.45)
        with self.voiceover(
            "Could a clever enough compiler always know? No. <bookmark mark='a'/> Rice's theorem, from 1953, says "
            "that every nontrivial question about what a program does is undecidable. <bookmark mark='b'/> Here is "
            "the idea for aliasing. Point p at y, run some arbitrary program M on some input, then point p at x, "
            "store through p and print x. <bookmark mark='c'/> Does the store through p ever change x? Only if the "
            "store is ever reached, which is exactly when M finishes. An exact alias analysis would solve the halting problem. <bookmark mark='d'/> So every "
            "real analysis answers yes, no, or maybe, and it is sound if it treats maybe as yes. It is never wrong, "
            "only sometimes slower than necessary. The proof of Rice's theorem is in Part 25. Every optimization "
            "in this part lives with that limit: it is allowed to miss chances, and never to change the meaning."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(ex))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(o) for o in out], lag_ratio=0.5), run_time=3)
        self.wait(0.3)
        self.clear_scene()
