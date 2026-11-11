from __future__ import annotations

import re

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table,
                                   load, mono, words)


class JIT(VoiceoverScene):
    def construct(self):
        self.card()
        self.tiers()
        self.caches()
        self.shapes()
        self.deopt()

    def card(self):
        card = chapter_card(11, r"Just-in-time compilers", r"Can a program be compiled while it runs?", lit=(1991,),
                            extra=((1991, r"Self: \ polymorphic inline caches"),), part=PART)
        with self.voiceover("Chapter eleven. Just-in-time compilers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tiers(self):
        d = load("jit")
        head = label(r"Tiers: \ interpret first, \ compile what is hot", font_size=34).to_edge(UP, buff=0.3)
        lad = d["ladder"]
        mx = max(r["seconds"] for r in lad)
        W = 7.0
        rows = VGroup()
        for k, r in enumerate(lad):
            w = W * r["seconds"] / mx
            bar = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=[NO, FUNC, FUNC, YES][k],
                            fill_opacity=0.85)
            name = label(r["tier"], font_size=20, color=WHITE)
            val = label(human_time(r["seconds"]), font_size=19, color=GREY_A)
            rows.add(VGroup(name, bar, val))
        for k, r in enumerate(rows):
            y = 1.6 - 0.7 * k
            r[1].move_to([-1.0 + r[1].width / 2, y, 0])
            r[0].move_to([-1.25 - r[0].width / 2, y, 0])
            r[2].next_to(r[1], RIGHT, buff=0.15)
        cap = label(rf"V8 \ ({d['node']}), \ \texttt{{fib(32)}}, \ timed inside the program; \ later tiers enabled "
                    r"one by one", font_size=18, color=GREY_B).next_to(rows, UP, buff=0.3)
        trace = [re.sub(r" \(sfi = 0x[0-9a-f]+\)", "", re.sub(r"0x[0-9a-f]+ ", "", l)) for l in d["tiers_trace"][:2]]
        tr = VGroup(label(r"\texttt{node --trace-opt}:", font_size=18, color=GREY_B),
                    code(trace, size=13, color=CODE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                buff=0.1).next_to(rows, DOWN,
                                                                                                  buff=0.5)
        if tr.width > 12.6:
            tr.scale_to_fit_width(12.6)
        pts = label(r"start fast in the interpreter; \ spend compile time only where the program spends its time",
                    font_size=21, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "A JIT can use information gathered while a program runs. <bookmark mark='a'/> This installed V8 "
            "exposes Ignition, Sparkplug, Maglev and TurboFan configurations. Interpretation starts execution; "
            "later tiers trade compilation effort for more specialized code. Tier availability and policy vary "
            "with version and platform. <bookmark mark='b'/> The bars show Fibonacci of thirty-two with the "
            "stated tiers enabled, using the best of three runs. Enabling an extra tier need not make this short "
            "benchmark faster. <bookmark mark='c'/> The trace shows what this V8 actually compiled during a "
            "separate diagnostic run. <bookmark mark='d'/> Hotness predicts where compilation may pay off, but "
            "compilation, warmup, scheduling and speculation also cost time. A single best run does not establish "
            "stable long-term performance."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(*[FadeIn(r[0]) for r in rows])
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                                  lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(tr))
            vo.wait_until("d")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()

    def caches(self):
        d = load("jit")
        head = label(r"Inline caches", font_size=34).to_edge(UP, buff=0.3)
        src = code(["function getX(o) { return o.x; }"], size=20, color=CODE).next_to(head, DOWN, buff=0.4)
        expl = VGroup(
            label(r"where is \texttt{x} in \texttt{o}? \ in a dynamic language, \ it depends on the object",
                  font_size=21, color=GREY_A),
            label(r"the call site remembers the last \textbf{shape} it saw, \ and where \texttt{x} was \ (Deutsch and "
                  r"Schiffman, \ 1984)", font_size=21, color=GREY_A),
            label(r"a few shapes: \ a small table \ (\textbf{polymorphic}, \ Self, \ 1991); \ too many: \ a slow "
                  r"general lookup \ (\textbf{megamorphic})", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.14).next_to(src, DOWN, buff=0.35)
        ic = d["ic"]
        ax = Axes(x_range=[0, 5.5, 1], y_range=[0, max(r["seconds"] for r in ic) * 1.2 * 1000, 25],
                  x_length=6.6, y_length=2.6, axis_config={"color": GREY_D, "include_numbers": False}).next_to(
            expl, DOWN, buff=0.5).shift(LEFT * 2.4)
        pts = [ax.c2p(np.log2(r["shapes"]), 1000 * r["seconds"]) for r in ic]
        line = VMobject(color=COST, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=COST) for p in pts])
        xt = VGroup(*[label(str(r["shapes"]), font_size=16, color=GREY_B).next_to(ax.c2p(np.log2(r["shapes"]), 0),
                                                                                  DOWN, buff=0.1) for r in ic])
        xl = label('constructed shapes (base-2 log scale)', font_size=17, color=GREY_B).next_to(xt, DOWN, buff=0.1)
        yl = label('20.48 million calls, ms', font_size=17, color=GREY_B).next_to(ax, UP, buff=0.05).align_to(
            ax, LEFT)
        slow = ic[-1]["seconds"] / ic[0]["seconds"]
        side = VGroup(
            label(rf"1 shape: \ {1000 * ic[0]['seconds']:.0f} ms", font_size=21, color=YES),
            label(rf"{ic[-1]['shapes']} shapes: \ {1000 * ic[-1]['seconds']:.0f} ms, \ {slow:.0f}$\times$ slower",
                  font_size=21, color=NO),
            label('single-host construction; object layouts also change', font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        if side.width > 4.4:
            side.scale_to_fit_width(4.4)
        side.next_to(ax, RIGHT, buff=0.5)
        with self.voiceover(
            (
            "Property access can exploit repeated object structure. <bookmark mark='a'/> For getX, the runtime "
            "needs the location of x in the current object. <bookmark mark='b'/> An inline cache records a shape "
            "and an access strategy, guarding the fast path with a shape check. <bookmark mark='c'/> Polymorphic "
            "caches remember several cases. Megamorphic strategies handle more varied sites; their thresholds and "
            "lookup mechanisms depend on the engine. <bookmark mark='d'/> Our curve times twenty million four "
            "hundred and eighty thousand getX calls with one through thirty-two constructed shapes. The "
            "horizontal positions use a base-two logarithmic scale. The measured ratio is shown beside the graph. "
            "This construction changes object layouts too, so the curve does not isolate one instruction or prove "
            "a universal shape penalty."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(expl[0]))
            vo.wait_until("b")
            self.play(FadeIn(expl[1]))
            vo.wait_until("c")
            self.play(FadeIn(expl[2]))
            vo.wait_until("d")
            self.play(Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl))
            self.play(Create(line), FadeIn(dots), FadeIn(side), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    def shapes(self):
        d = load("jit")["shapes"]
        head = label(r"Hidden classes", font_size=34).to_edge(UP, buff=0.3)
        src = code(["const a = {x: 1, y: 2}, b = {x: 3, y: 4}, c = {y: 5, x: 6};",
                    "const d = {x: 1}; d.y = 2;",
                    "%HaveSameMap(a, b)", "%HaveSameMap(a, c)", "%HaveSameMap(a, d)"], size=18,
                   color=CODE).next_to(head, DOWN, buff=0.5)
        res = VGroup(*[mono(f"→ {str(d[k]).lower()}", 18, YES if d[k] else NO) for k in ("ab", "ac", "ad")])
        for r, line in zip(res, src[2:]):
            r.next_to(line, RIGHT, buff=0.4)
        pts = VGroup(
            label(r"V8 gives objects with the same properties, \ added in the same order, \ the same hidden "
                  r"\textbf{map}", font_size=21, color=GREY_A),
            label(r"the map records each property's offset: \ an inline cache compares maps, \ not names",
                  font_size=21, color=GREY_A),
            label(r"so build objects the same way every time: \ \texttt{c} and \texttt{d} hold the same data, \ "
                  r"in different shapes", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "What is a shape? In V8 it is a hidden class, called a map, and V8 can be asked about them directly. "
            "<bookmark mark='a'/> a and b were built with x and then y: same map, true. <bookmark mark='b'/> c "
            "has the same properties in the other order: a different map. And d got y later, by assignment: "
            "different again. <bookmark mark='c'/> A map records where each property lives, so an inline cache "
            "compares one map pointer instead of searching for a name. That is why JavaScript performance advice "
            "says: build your objects the same way every time. The engine is betting that you will."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src[:2]))
            vo.wait_until("a")
            self.play(FadeIn(src[2]), FadeIn(res[0]), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(src[3:]), FadeIn(res[1:]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()

    def deopt(self):
        d = load("jit")
        head = label(r"Speculate, \ and take it back", font_size=34).to_edge(UP, buff=0.3)
        src = code(["function add(a, b) { return a + b; }",
                    "for (let i = 0; i < 200000; i++) s += add(i, 1);   // hot, and always small integers",
                    'add("a", "b");                                       // a string'], size=17,
                   color=CODE).next_to(head, DOWN, buff=0.5)
        line = next((l for l in d["deopt"] if "add" in l), d["deopt"][0] if d["deopt"] else "")
        excerpt=re.sub(r'0x[0-9a-f]+','<addr>',line)
        excerpt=excerpt[:excerpt.find('opt id')] if 'opt id' in excerpt else excerpt
        import textwrap
        tr=VGroup(label('actual Node deoptimization trace (addresses abbreviated)',font_size=18,color=GREY_B),
                  code(textwrap.wrap(excerpt,88),size=14,color=NO)).arrange(DOWN,aligned_edge=LEFT,buff=.12)
        if tr.width>12.7:tr.scale_to_fit_width(12.7)
        tr.next_to(src,DOWN,buff=.4)
        pts = VGroup(
            label('optimized code can specialize observed types and guard its assumptions',
                  font_size=21, color=GREY_A),
            label('deoptimization reconstructs state for less specialized code',
                  font_size=21, color=NO),
            label(r"\textbf{deoptimization} \ (H\"olzle, Chambers and Ungar, \ 1992): \ what lets a JIT guess "
                  r"aggressively", font_size=21, color=YES),
            label(r"tracing JITs compile a hot \textit{loop path} instead: \ TraceMonkey, \ LuaJIT, \ PyPy",
                  font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "Optimized code can depend on assumptions learned from earlier calls. <bookmark mark='a'/> Our add "
            "function first sees numbers and later receives strings. A type guard can fail, forcing the runtime "
            "to leave code that relied on the old assumption. <bookmark mark='b'/> The displayed trace comes from "
            "the installed Node and V8 version. Its actual bailout reasons and tier names are evidence for this "
            "run, not promises about every V8 release. <bookmark mark='c'/> Deoptimization reconstructs a state "
            "that less specialized code can continue from. The string call still returns a followed by b; "
            "correctness must survive a failed guess. <bookmark mark='d'/> The destination can be another tier, "
            "and further calls may be optimized again. Speculation trades guards, compilation and reconstruction "
            "work for faster common cases."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src[:2]))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(src[2]), FadeIn(tr))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()
