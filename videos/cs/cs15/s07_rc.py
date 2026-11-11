from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table,
                                   load, mono, words)


def node(name, color=DATA, r=0.32):
    c = Circle(radius=r, color=color, stroke_width=2.5).set_fill(BG, 1)
    return VGroup(c, mono(name, 18, color).move_to(c))


def edge(a, b, color=GREY_B):
    return Arrow(a[0].get_center(), b[0].get_center(), buff=0.34, color=color, stroke_width=2, tip_length=0.13)


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.reach()
        self.counts()
        self.cycles()
        self.traffic()

    def card(self):
        card = chapter_card(6, r"Why collect, \ and counting references", r"Who frees the memory?", lit=(1960,),
                            extra=((1960, r"McCarthy: \ garbage collection; \ Collins: \ reference counts"),),
                            part=PART)
        with self.voiceover("Chapter six. Why collect, and counting references."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def reach(self):
        head = label('Reachable, not necessarily used again', font_size=34).to_edge(UP, buff=0.3)
        roots = VGroup(*[VGroup(Rectangle(width=1.0, height=0.5, color=CTRL, stroke_width=2),
                                mono(n, 16, CTRL)) for n in ("stack", "globals")])
        for r in roots:
            r[1].move_to(r[0])
        roots.arrange(DOWN, buff=0.9).move_to(LEFT * 5.2 + UP * 0.2)
        pos = {"a": (-2.6, 1.3), "b": (-0.6, 1.8), "c": (-0.8, 0.0), "d": (1.4, 0.9), "e": (1.6, -1.0),
               "f": (3.6, 1.5), "g": (3.6, -0.4), "h": (-2.4, -1.4)}
        ns = {k: node(k).move_to([x, y, 0]) for k, (x, y) in pos.items()}
        es = [("a", "b"), ("a", "c"), ("c", "d"), ("b", "d"), ("f", "g"), ("g", "f"), ("h", "e")]
        ev = VGroup(*[edge(ns[a], ns[b]) for a, b in es])
        rv = VGroup(Arrow(roots[0].get_right(), ns["a"][0].get_left(), buff=0.05, color=CTRL, stroke_width=2.2,
                          tip_length=0.13),
                    Arrow(roots[1].get_right(), ns["c"][0].get_left(), buff=0.05, color=CTRL, stroke_width=2.2,
                          tip_length=0.13))
        live = ["a", "c", "b", "d"]
        pts = VGroup(
            label(r"the \textbf{roots}: \ what the program can name right now", font_size=21, color=CTRL),
            label(r"live: \ reachable from a root by following pointers", font_size=21, color=YES),
            label(r"garbage: \ everything else, \ including $f$ and $g$, \ which point at each other", font_size=21,
                  color=NO),
            label(r"freeing by hand: \ forget, \ and it leaks; \ too early, \ and it is use after free \ (Part 11)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "An allocator finds space; a collector decides which space can safely be reused. <bookmark mark='a'/> "
            "The roots are the references held by active program state, including the stack and globals in our "
            "VM. <bookmark mark='b'/> Follow their pointers through the heap. An unreachable object cannot be "
            "accessed again through these references, under this model's rules. <bookmark mark='c'/> Reachability "
            "is conservative: an object can remain reachable even if the program will never use it again. It is "
            "not the same as semantic last use. <bookmark mark='d'/> Our core omits weak references and "
            "finalizers. Real runtimes need additional rules for them, but the root-to-object graph is the "
            "starting point for tracing collection."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(roots), *[FadeIn(n) for n in ns.values()], Create(ev))
            vo.wait_until("a")
            self.play(Create(rv), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(*[ns[k][0].animate.set_fill(YES, 0.35) for k in live], FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(*[ns[k].animate.set_opacity(0.35) for k in ("e", "f", "g", "h")], FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def counts(self):
        head = label(r"Reference counting \ (Collins, \ 1960)", font_size=34).to_edge(UP, buff=0.3)
        ns = [node(n, r=0.36) for n in ("a", "b", "c")]
        VGroup(*ns).arrange(RIGHT, buff=2.2).move_to(UP * 0.6)
        root = VGroup(Rectangle(width=1.1, height=0.5, color=CTRL, stroke_width=2), mono("x", 18, CTRL))
        root[1].move_to(root[0])
        root.next_to(ns[0], LEFT, buff=1.4)
        e0 = Arrow(root.get_right(), ns[0][0].get_left(), buff=0.05, color=CTRL, stroke_width=2.2, tip_length=0.13)
        e1, e2 = edge(ns[0], ns[1]), edge(ns[1], ns[2])
        cnt = [Integer(1, font_size=26, color=HEAD).next_to(n, UP, buff=0.12) for n in ns]
        pts = VGroup(
            label(r"every object counts the pointers to it", font_size=22, color=GREY_A),
            label(r"each new pointer: \ $+1$; \ each pointer overwritten or dropped: \ $-1$", font_size=22,
                  color=GREY_A),
            label(r"at zero, \ free it, \ and decrement whatever it pointed at", font_size=22, color=YES),
            label('zero-count cascades can reclaim a large graph synchronously', font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "Reference counting attaches a count to each object. <bookmark mark='a'/> In this simple model the "
            "count records incoming owned references, including roots. <bookmark mark='b'/> Creating or copying a "
            "reference increments the count; overwriting or dropping one decrements it. <bookmark mark='c'/> When "
            "the root is removed, a reaches zero and is reclaimed. Releasing its outgoing reference can make b "
            "reach zero, and then c. Watch that cascade through the graph. <bookmark mark='d'/> This is prompt "
            "reclamation, but a large graph can cause a large synchronous cascade. The model therefore does not "
            "establish pause-free execution, and cycles need additional treatment."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(root), *[FadeIn(n) for n in ns], Create(e0), Create(e1), Create(e2))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in cnt], FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeOut(e0), FadeOut(root))
            for k, n in enumerate(ns):
                new = Integer(0, font_size=26, color=NO).move_to(cnt[k])
                anims = [Transform(cnt[k], new), n.animate.set_opacity(0.25)]
                if k < 2:
                    anims.append(FadeOut((e1, e2)[k]))
                self.play(*anims, run_time=0.8)
            self.play(FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def cycles(self):
        d = load("rc")["cpython"]
        head = label(r"The weakness: \ cycles", font_size=34).to_edge(UP, buff=0.3)
        f, g = node("f", r=0.4), node("g", r=0.4)
        VGroup(f, g).arrange(RIGHT, buff=2.0).move_to(LEFT * 3.4 + UP * 1.0)
        a1 = CurvedArrow(f[0].get_top(), g[0].get_top(), angle=-1.0, color=GREY_B, stroke_width=2.2, tip_length=0.13)
        a2 = CurvedArrow(g[0].get_bottom(), f[0].get_bottom(), angle=-1.0, color=GREY_B, stroke_width=2.2,
                         tip_length=0.13)
        c1 = Integer(1, font_size=26, color=NO).next_to(f, LEFT, buff=0.2)
        c2 = Integer(1, font_size=26, color=NO).next_to(g, RIGHT, buff=0.2)
        unreach = label(r"unreachable, \ yet each count is 1: \ never freed", font_size=21, color=NO).next_to(
            VGroup(f, g), DOWN, buff=1.0)
        py = d.get("python3.12", {}).get("raw", [])
        th = next((l for l in py if l.startswith("threshold")), "")
        col = next((l for l in py if l.startswith("collected")), "")
        n_col = int(col.split()[1]) if col else 0
        t_col = float(col.split()[2]) * 1000 if col else 0
        src = code(["import gc", "gc.disable()", "for i in range(100000):", "    x = Node(); y = Node()",
                    "    x.other = y; y.other = x", "gc.collect()"], size=17, color=CODE).to_edge(RIGHT, buff=0.6).shift(
            UP * 1.0)
        res = VGroup(
            label(rf"CPython 3.12, \ on this machine: \ \texttt{{gc.collect()}} found {words(n_col)} objects \ "
                  rf"in {t_col:.0f} ms", font_size=20, color=YES),
            label(r"every pair but the last, \ which \texttt{x} and \texttt{y} still hold", font_size=19,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(src, DOWN, buff=0.4)
        if res.width > 6.4:
            res.scale_to_fit_width(6.4)
        res.to_edge(RIGHT, buff=0.4)
        pts = VGroup(
            label(r"so CPython counts references \textit{and} runs a tracing collector for cycles", font_size=21,
                  color=GREY_A),
            label(rf"a generational one: \ \texttt{{gc.get\_threshold()}} \ $=$ \ \texttt{{{th.split(' ', 1)[-1]}}} "
                  r"\ on 3.12", font_size=21, color=GREY_A),
            label(r"in our VM a recursive closure refers to itself through \texttt{SELF}, \ not a pointer: \ no "
                  r"cycle", font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Counting has one famous weakness. <bookmark mark='a'/> Two objects that point at each other each have "
            "a count of one, even when nothing else can reach them. They are garbage, and their counts will never "
            "reach zero. <bookmark mark='b'/> We can watch this happen in CPython on this machine. Make a hundred "
            "thousand pairs of objects that point at each other, with automatic collection switched off, and "
            "then call the collector by hand. <bookmark mark='c'/> It finds almost two hundred thousand objects "
            "that reference counting had left behind: every pair except the last, which the variables x and y "
            "still hold. <bookmark mark='d'/> So CPython does both: it counts references, and it also runs a "
            "tracing collector to find cycles, itself generational, with thresholds you can read and tune. In our "
            "own VM, a recursive closure refers to itself through the SELF instruction rather than a pointer, so "
            "recursion makes no cycles at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f), FadeIn(g), Create(a1), Create(a2))
            vo.wait_until("a")
            self.play(FadeIn(c1), FadeIn(c2), FadeIn(unreach))
            vo.wait_until("b")
            self.play(FadeIn(src))
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def traffic(self):
        d = load("rc")
        tr = load("tracing")
        head = label(r"What counting would cost the Job", font_size=34).to_edge(UP, buff=0.3)
        cheney = tr["rows"][0]["work"]
        tab = grid_table([r"on Part 7's chapter", r"count"], [
            [r"objects allocated", words(d["objects"])],
            [r"count updates for pointers pushed on the stack", words(d["rc_stack"])],
            [r"count updates for pointers stored in new objects", words(d["rc_heap"])],
            [r"words a copying collector moves, \ in all", words(cheney)],
        ], widths=[7.6, 2.6], row_h=0.55, font_size=21, mono_cols=(),
            colors=[[WHITE, WHITE], [WHITE, NO], [WHITE, COST], [WHITE, YES]]).next_to(head, DOWN, buff=0.6)
        per = (d["rc_stack"] + d["rc_heap"]) / d["objects"]
        pts = VGroup(
            label(rf"about {per:.0f} count updates per object: \ every \texttt{{LOCAL}} of a pointer is one",
                  font_size=22, color=NO),
            label(r"\textbf{deferred} counting ignores the stack and scans it now and then \ (Deutsch and Bobrow, "
                  r"\ 1976)", font_size=21, color=GREY_A),
            label('shared counts may need atomics; Rc and thread-local optimizations differ',
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            (
            "Reference counting makes pointer updates part of memory management. <bookmark mark='a'/> Our "
            "instrumentation counts increments and decrements for the Job; it measures traffic in this model, not "
            "the elapsed time of a complete reference-counting collector. <bookmark mark='b'/> A count reaching "
            "zero can trigger a cascade through a large object graph. Prompt reclamation therefore does not imply "
            "a small worst-case pause. <bookmark mark='c'/> Rust's Rc uses non-atomic counts; Arc supports "
            "sharing with atomic operations. Other runtimes have their own thread and ownership optimizations. "
            "Tracing trades per-update counting for graph walks and can reclaim cycles. Which trade wins depends "
            "on the workload, implementation and latency requirements; this one traffic count cannot settle it."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:4]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[4])), FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()
