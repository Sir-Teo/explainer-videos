from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, BLACK_OBJ, CODE, COST, CTRL, DATA, FUNC, GRAY_OBJ, HEAD, LAM, NO, PART,
                                   WHITE_OBJ, YES, cell_obj, code, load, mono)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


def _evalapply():
    a = VGroup(Circle(radius=0.55, color=DATA, stroke_width=2.5), label(r"eval", font_size=22, color=DATA))
    b = VGroup(Circle(radius=0.55, color=LAM, stroke_width=2.5), label(r"apply", font_size=22, color=LAM))
    for x in (a, b):
        x[1].move_to(x[0])
    VGroup(a, b).arrange(RIGHT, buff=1.0)
    ar = VGroup(CurvedArrow(a[0].get_top(), b[0].get_top(), angle=-1.0, color=GREY_B, tip_length=0.12),
                CurvedArrow(b[0].get_bottom(), a[0].get_bottom(), angle=-1.0, color=GREY_B, tip_length=0.12))
    return VGroup(a, b, ar)


def _tricolor():
    g = VGroup()
    for c in (WHITE_OBJ, GRAY_OBJ, BLACK_OBJ):
        g.add(Circle(radius=0.4, stroke_color=GREY_A, stroke_width=2.5).set_fill(c, 1))
    g.arrange(RIGHT, buff=0.5)
    return g


def _cheney():
    top = VGroup(*[Rectangle(width=0.5, height=0.4, stroke_color=GREY_B, stroke_width=1.5).set_fill(
        YES if k in (0, 2, 3) else NO, 0.3) for k in range(6)]).arrange(RIGHT, buff=0.06)
    bot = VGroup(*[Rectangle(width=0.5, height=0.4, stroke_color=YES, stroke_width=1.5).set_fill(YES, 0.3)
                   for _ in range(3)]).arrange(RIGHT, buff=0.06)
    VGroup(top, bot).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
    ars = VGroup(*[Arrow(top[k].get_bottom(), bot[j].get_top(), buff=0.03, color=GREY_B, stroke_width=1.5,
                         tip_length=0.1) for j, k in enumerate((0, 2, 3))])
    return VGroup(top, bot, ars)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        tiles = Group(
            tile(_evalapply(), r"interpreters", DATA),
            tile(cell_obj("closure", ["code", 5], w=0.9, font_size=18), r"closures", LAM),
            tile(code(["fact_cps n k =", "  ... (fun r -> k (n * r))"], size=18, color=CODE), r"continuations",
                 CTRL),
            tile(code(["LOCAL 3", "FST", "LOCAL 0", "EQ", "JF 184"], size=18, color=CODE), r"bytecode, \ on Pebble",
                 FUNC),
            tile(_cheney(), r"copying and generations", YES),
            tile(_tricolor(), r"three colours, \ two barriers", HEAD),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Runtimes", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. An interpreter, eval and apply, and environments instead of "
            "substitution. Closures, which carry their environment onto the heap, and closure conversion. "
            "Continuations, which turn the stack into data, and tail calls, which keep it from growing. A bytecode "
            "machine for the lambda core, written in the Pebble language and checked against a reference, count "
            "for count. Reference counting, mark–sweep, mark–compact, Cheney's copying collector and generations, "
            "all run on the Job. The tri-colour invariant and the barriers that protect it. And on real runtimes "
            "on this machine: JIT tiers, inline caches, deoptimization, vtables, zero-cost exceptions and "
            "WebAssembly."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"sort, \ then count: \ ledger row 7", [16]),
            (r"processes, \ threads and their stacks", [31]),
            (r"virtual memory under the heap", [32]),
            (r"atomics, \ memory barriers, \ lock-free structures", [33]),
            (r"the browser: \ V8 and WebAssembly at work", [42]),
            (r"supervisors and crash recovery", [50]),
            (r"verified compilers and runtimes", [54, 55]),
            (r"semantics: \ what programs mean", [58]),
        ], font_size=24)
        with self.voiceover(
            "Where this comes back. Part 16 opens Act Four by changing the Job's algorithm, for ledger row seven. "
            "Part 31's kernel gives every thread its own stack, and Part 32's virtual memory sits under every heap. "
            "Part 33 returns to atomic operations and memory barriers, the hardware relatives of the write "
            "barriers here. Part 42 opens the browser, where V8 and WebAssembly live. Part 50 brings Erlang's "
            "supervisors to whole services. Parts 54 and 55 prove compilers and runtimes correct, and Part 58 asks "
            "what a program means."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"runtimes", r"the JVM, \ V8, \ CPython, \ .NET, \ the Go runtime: \ which one, \ and why it is fast"),
            (r"tuning", r"heap size, \ pause targets \ (\texttt{-XX:MaxGCPauseMillis}, \ \texttt{GOGC}), \ "
                        r"choosing a collector"),
            (r"profiling", r"allocation profilers; \ fewer, \ shorter-lived objects; \ shapes that stay the same"),
            (r"embedding", r"Lua, \ JavaScript and WebAssembly inside games, \ databases and editors"),
            (r"sandboxing", r"WebAssembly runtimes \ (Wasmtime, \ browsers) \ for plug-ins and edge functions"),
        ])
        with self.voiceover(
            "In practice. Most code you will write runs on a runtime like these: the JVM, V8, CPython, .NET or "
            "Go's. Their collectors have knobs, heap sizes and pause targets, and choosing well is a matter of the "
            "trade chapter ten measured. Allocation profilers find the objects that should not exist, and the "
            "fastest JavaScript keeps its objects the same shape. Interpreters are embedded everywhere, Lua in "
            "games, JavaScript in databases. And WebAssembly is becoming the standard sandbox for running other "
            "people's code."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Closure-convert \texttt{let twice f = let g = fun x -> f (f x) in g} by hand: \ find the free "
            r"variables, \ and write the \texttt{CLOSURE} and \texttt{FREE} code our compiler would emit.",
            r"Rewrite $\mathit{sum}$ over a list in CPS and with an accumulator; \ give each version's stack depth "
            r"and heap use for a list of $n$ elements.",
            r"Run Cheney's algorithm by hand on the heap in the notes: \ give the to-space order and every "
            r"forwarding address.",
            r"Derive the work per allocated word of a copying collector and of mark--sweep, \ with live data $L$ in "
            r"the same total memory $M$; \ compare them at $M = 2L$, \ $4L$ and $8L$.",
            r"\textit{Build.} \ Give the Pebble VM a nursery, \ in the Pebble language, \ and measure the Job. \ Why "
            r"does the $\lambda$-core need no write barrier?",
            r"$\bigstar$ \textit{Research.} \ Find a collector with bounded pauses, \ constant memory overhead and "
            r"constant work per word allocated, \ or prove that no collector can have all three.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give the Pebble VM a generational nursery, written in the Pebble language, and measure what "
            "it saves on the Job. The last, marked with a star, is a research problem: its answer is not known, "
            "and the notes say where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 16, \ Counting Steps", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"the ledger so far: \ can thinking beat silicon?", COST), (r"merge sort and the master theorem", DATA),
            (r"a lower bound from information: \ $n \log_2 n$", YES),
            (r"quicksort's average, \ $2n \ln n$, \ by calculus", LAM))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"Act IV, \ Algorithms: \ seven rows of better machines, \ and then one better idea", font_size=26,
                  color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time, Act Four begins. Seven rows of the ledger have made the machine faster, and the runtime "
            "more comfortable. The Job is still quadratic. Part 16 counts steps: merge sort and the master "
            "theorem, a lower bound on sorting that comes from information, and quicksort's average case, which "
            "is a small piece of calculus. Part 16, Counting Steps."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Abelson and Sussman, \textit{Structure and Interpretation of Computer Programs}, \ chapters 4--5",
             r"Friedman and Wand, \textit{Essentials of Programming Languages}",
             r"Appel, \textit{Compiling with Continuations}",
             r"Jones, Hosking and Moss, \textit{The Garbage Collection Handbook}",
             r"Smith and Nair, \textit{Virtual Machines}; \ Nystrom, \textit{Crafting Interpreters}"],
            [r"McCarthy (1960); \ Collins (1960); \ Cheney, ``A nonrecursive list compacting algorithm'' (1970)",
             r"Dijkstra, Lamport, Martin, Scholten and Steffens, ``On-the-fly garbage collection'' (1978)",
             r"Lieberman and Hewitt (1983); \ Ungar, ``Generation scavenging'' (1984); \ Yuasa (1990)",
             r"Deutsch and Schiffman (1984); \ H\"olzle, Chambers and Ungar (1991, 1992); \ Steele (1977)",
             r"Felleisen and Friedman (1986); \ Ierusalimschy, de Figueiredo and Celes (2005); \ Shi et al. (2008)",
             r"Haas et al., ``Bringing the web up to speed with WebAssembly'' (2017); \ Watt (2018)",
             r"Hertz and Berger (2005); \ Bacon, Cheng and Rajan (2003); \ Bendersky and Petrank (2011)",
             r"Futamura (1971); \ Bolz et al. (2009); \ W\"urthinger et al. (2017); \ Barrett et al. (2017)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
