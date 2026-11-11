from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load, module_box,
                                   mono)

# the arguments compute.py passes to deopt_trace (its input, not a result)
DEOPT_ARGS = ["1, 2", "3, 4", "5, 6", "7, 8", "'a', 1", "1, 2", "2, 3", "4, 5", "2³¹, 1", "1, 1", "2, 2", "3, 3"]
SHAPE_COLORS = [DATA, LAM, YES, HEAD, KERN, TEAL, PINK, GREY_B]


def _shape_name(s: str) -> str:
    """'.x.y' -> '{x, y}' (the instrument's path of added properties)."""
    return "{" + ", ".join(p for p in s.split(".") if p and p != "{}") + "}"


class Engines(VoiceoverScene):
    def construct(self):
        self.card()
        self.lazy()
        self.tiers()
        self.shapes()
        self.caches()
        self.deopt()
        self.gc()

    def card(self):
        card = chapter_card(7, r"JavaScript engines", r"How does a dynamic language run fast?",
                            lit=(2008, 2017), extra=((2008, r"V8 ships in Chrome"),
                                                     (2017, r"V8's Ignition and TurboFan")), part=PART)
        with self.voiceover("Chapter seven. JavaScript engines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lazy(self):
        head = label(r"Lazy parsing", font_size=36).to_edge(UP, buff=0.3)
        src = ["function init() { render(); }", "function render() { /* draw */ }",
               "function onCheckout() { /* 400 lines */ }", "function onRefund() { /* 300 lines */ }", "",
               "init();"]
        code = code_block(src, size=22).move_to([-2.6, 0.9, 0])
        tags = VGroup()
        for i in range(4):
            t = label(r"pre-parsed", font_size=20, color=GREY_B).next_to(code[i], RIGHT, buff=0.25)
            tags.add(t.set_x(code.get_right()[0] + 1.2))
        full = [label(r"parsed in full", font_size=20, color=YES).move_to(tags[i]) for i in range(2)]
        ill = note(r"illustrative page", font_size=18).next_to(code, DOWN, buff=0.3).align_to(code, LEFT)
        notes = VGroup(
            wrapped_label(r"the \textbf{pre-parser} checks a function body's syntax and notes which outer variables "
                          r"it uses \ (for closures), \ but builds no tree and emits no code", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"the full parse, \ the syntax tree and the bytecode wait until the function is first "
                          r"called; \ code that never runs costs only the quick scan", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A page arrives with its JavaScript as text, often far more than this visit will run. "
            "<bookmark mark='a'/> So the engine pre-parses each function body: a quick scan that checks "
            "the syntax and notes which outer variables the function uses, for closures, but builds no "
            "tree. <bookmark mark='b'/> When init is called, it is parsed in full and compiled, and so is"
            " render when init calls it. The checkout and refund handlers stay as text until someone "
            "clicks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(ill))
            vo.wait_until("a")
            self.play(*[code[i].animate.set_opacity(0.45) for i in range(4)], FadeIn(tags), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Indicate(code[5], color=HEAD))
            for i in range(2):
                self.play(code[i].animate.set_opacity(1), Transform(tags[i], full[i]), run_time=0.7)
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def tiers(self):
        head = label(r"Bytecode, \ then machine code", font_size=36).to_edge(UP, buff=0.3)
        names = [(r"source text", GREY_B), (r"parser", GREY_B), (r"bytecode", DATA), (r"interpreter", DATA),
                 (r"baseline JIT", HEAD), (r"optimizing JIT", YES)]
        boxes = VGroup(*[module_box(n, c, w=1.75, h=0.62, font=18) for n, c in names]).arrange(RIGHT, buff=0.32)
        boxes.next_to(head, DOWN, buff=1.2)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.04, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.3) for i in range(5)])
        fb = CurvedArrow(boxes[3].get_top() + UP * 0.05, boxes[5].get_top() + UP * 0.05, angle=-PI / 3,
                         color=LAM, stroke_width=2.5)
        fbl = label(r"type feedback", font_size=17, color=LAM).next_to(fb, UP, buff=0.05)
        de = CurvedArrow(boxes[5].get_bottom() + DOWN * 0.05, boxes[3].get_bottom() + DOWN * 0.05, angle=-PI / 3,
                         color=NO, stroke_width=2.5)
        del_ = label(r"deoptimize", font_size=17, color=NO).next_to(de, DOWN, buff=0.05)
        dot = SurroundingRectangle(boxes[0], color=HEAD, buff=0.07, corner_radius=0.1, stroke_width=3)
        rows = [[r"V8 \ (Chrome)", r"Ignition", r"Sparkplug, \ Maglev", r"TurboFan"],
                [r"SpiderMonkey \ (Firefox)", r"interpreters", r"Baseline", r"Warp"],
                [r"JavaScriptCore \ (Safari)", r"LLInt", r"Baseline, \ DFG", r"FTL"]]
        tab = grid_table([r"engine", r"interpreter", r"middle tiers", r"top tier"], rows,
                         widths=[3.6, 2.4, 3.0, 2.2], row_h=0.44, font_size=19, mono_cols=())
        tab.next_to(boxes, DOWN, buff=1.5).set_x(0)
        with self.voiceover(
            "Then comes the pipeline Part 15 measured. <bookmark mark='a'/> Bytecode runs at once in an "
            "interpreter, which records what it sees: the types reaching each operation, the shapes "
            "reaching each property access. <bookmark mark='b'/> Hot functions move up, to a baseline "
            "compiler and then to an optimizing one, which specialises the code using that feedback, with"
            " a way back if its guesses fail. <bookmark mark='c'/> V8's tiers are Ignition, Sparkplug, "
            "Maglev and TurboFan; Firefox and Safari climb a similar ladder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[:2]), Create(arrows[0]))
            vo.wait_until("a")
            self.play(FadeIn(boxes[2:4]), Create(arrows[1:3]), FadeIn(dot))
            self.play(dot.animate.move_to(boxes[3]), run_time=1.5, rate_func=linear)
            self.play(Create(fb), FadeIn(fbl))
            vo.wait_until("b")
            self.play(FadeIn(boxes[4:]), Create(arrows[3:]))
            self.play(dot.animate.move_to(boxes[4]), run_time=0.8)
            self.play(dot.animate.move_to(boxes[5]), run_time=0.8)
            self.play(Create(de), FadeIn(del_))
            vo.wait_until("c")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    def shapes(self):
        tr = load("ic")["transitions"]
        head = label(r"Hidden classes and transitions", font_size=36).to_edge(UP, buff=0.3)
        src = code_block(["a = {}; a.x = 1; a.y = 2;", "b = {}; b.x = 3; b.y = 4;", "c = {}; c.y = 5; c.x = 6;"],
                         size=19).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        pos = {"{}": [-5.0, -1.0], ".x": [-2.4, 0.0], ".x.y": [0.2, 0.0], ".y": [-2.4, -2.0], ".y.x": [0.2, -2.0]}
        nodes = {}
        for k, (x, y) in pos.items():
            col = GREY_B if k == "{}" else (DATA if k.startswith(".x") else LAM)
            nodes[k] = module_box(rf"\texttt{{\{{{_shape_name(k)[1:-1]}\}}}}", col, w=1.6, h=0.56, font=19).move_to(
                [x, y, 0])
        edges = VGroup()
        elabels = VGroup()
        for a, b in tr["edges"]:
            ar = Arrow(nodes[a][0].get_right(), nodes[b][0].get_left(), buff=0.06, stroke_width=2, color=GREY_B,
                       max_tip_length_to_length_ratio=0.12)
            edges.add(ar)
            diag = a == "{}"
            elabels.add(label(rf"add \texttt{{{b.split('.')[-1]}}}", font_size=17, color=GREY_A).next_to(
                ar.get_center(), (LEFT + (UP if b == ".x" else DOWN)) if diag else UP, buff=0.08))
        markers = [Dot(nodes["{}"][0].get_center(), radius=0.1, color=c) for c in (DATA, YES, LAM)]
        lay = VGroup(
            label(r"shape $\{x, y\}$: \ \texttt{x} in slot 0, \ \texttt{y} in slot 1", font_size=19, color=DATA),
            label(r"an object: \ a shape pointer and its slots", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.9, 0])
        res = VGroup(
            label(rf"a and b share a shape: \ \texttt{{{str(tr['same_shape_ab']).lower()}}}", font_size=21,
                  color=YES),
            label(rf"a and c share a shape: \ \texttt{{{str(tr['same_shape_ac']).lower()}}}", font_size=21,
                  color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.6, -0.4, 0])
        tip = wrapped_label(r"so build objects the same way every time: \ the same properties, \ in the same order",
                            4.6, font_size=19, color=HEAD).next_to(res, DOWN, buff=0.45).align_to(res, LEFT)
        VGroup(res, tip).to_edge(RIGHT, buff=0.45)
        lay.align_to(res, LEFT)
        def above(k, dx=0.0):
            return nodes[k][0].get_top() + UP * 0.2 + RIGHT * dx
        for m, dx in zip(markers, (-0.25, 0.25, 0.0)):
            m.move_to(above("{}", dx))
        tags_ = [label(n, font_size=16, color=m.get_color()).next_to(m, UP, buff=0.05) for n, m in
                 zip("abc", markers)]
        for t, m in zip(tags_, markers):
            t.add_updater(lambda t, m=m: t.next_to(m, UP, buff=0.05))
        path_x = [[above(".x", dx), above(".x.y", dx)] for dx in (-0.25, 0.25)]
        path_y = [above(".y"), above(".y.x")]
        with self.voiceover(
            "How can a property be found quickly, when any object can gain properties at any time? "
            "<bookmark mark='a'/> Every object points to a hidden class, a shape: a table of which "
            "property lives in which slot. Adding a property follows a shared transition to a new shape. "
            "<bookmark mark='b'/> a gains x, then y. b does the same, and lands on the very same shape. "
            "<bookmark mark='c'/> c adds y first, and ends on a different one. <bookmark mark='d'/> Part "
            "15 asked V8 itself, and it agrees: same order, same shape."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(nodes["{}"]))
            vo.wait_until("a")
            self.play(*[FadeIn(n) for k, n in nodes.items() if k != "{}"], Create(edges), FadeIn(elabels),
                      FadeIn(lay))
            vo.wait_until("b")
            for m, line in zip(markers[:2], (0, 1)):
                self.play(Indicate(src[line], color=HEAD), FadeIn(m), FadeIn(tags_[line]), run_time=0.6)
                for p in path_x[line]:
                    self.play(m.animate.move_to(p), run_time=0.6)
            vo.wait_until("c")
            self.play(Indicate(src[2], color=HEAD), FadeIn(markers[2]), FadeIn(tags_[2]), run_time=0.6)
            for p in path_y:
                self.play(markers[2].animate.move_to(p), run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(res), FadeIn(tip))
        self.wait(0.4)
        self.clear_scene()

    def caches(self):
        sites = load("ic")["sites"]
        head = label(r"Inline caches", font_size=36).to_edge(UP, buff=0.3)
        code = mono("for (const p of points) sum += p.x;", size=20).next_to(head, DOWN, buff=0.35)
        site_lbl = label(r"the site \texttt{p.x}: \ cached shapes", font_size=18, color=GREY_A)
        slots = VGroup(*[Square(0.55, stroke_color=GREY_C, stroke_width=1.5) for _ in range(4)]).arrange(
            RIGHT, buff=0.12)
        cache = VGroup(site_lbl, slots).arrange(DOWN, buff=0.15).move_to([-4.6, 1.0, 0])
        dict_box = module_box(r"dictionary lookup", NO, w=2.6, h=0.5, font=18).next_to(cache, DOWN, buff=0.35)
        dict_box.set_opacity(0.25)
        state = label(r"uninitialized", font_size=19, color=GREY_B).next_to(dict_box, DOWN, buff=0.3)
        rows = []
        for k in ("1", "2", "4", "8"):
            s = sites[k]
            rows.append([f"{s['shapes']}", s["state"], f"{s['shape checks']:,}", f"{s['dictionary lookups']:,}",
                         f"{s['per_access']:.1f}"])
        tab = grid_table([r"shapes", r"state", r"shape checks", r"dict.\ lookups", r"cost per access*"], rows,
                         widths=[1.1, 2.0, 1.7, 1.7, 2.1], row_h=0.5, font_size=19, mono_cols=())
        tab.move_to([2.4, 0.4, 0])
        for r in range(1, 5):
            for c in range(5):
                tab.cells[r][c].set_opacity(0)
        star = note(r"* illustrative weighting: \ a dictionary lookup counted as ten shape checks", font_size=17
                    ).next_to(tab, DOWN, buff=0.3).align_to(tab, LEFT)
        lines = wrapped_label(r"10{,}000 objects built with 1, \ 2, \ 4 or 8 property orders; \ the cache holds "
                              r"up to four shapes, \ as V8's does; \ the fifth sends the site megamorphic", 12.4,
                              font_size=19, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A shape lets the engine skip the table. <bookmark mark='a'/> Each access in the code, like p"
            " dot x here, keeps a small cache: the shapes it has seen, and where x was. <bookmark "
            "mark='b'/> We summed p dot x over ten thousand objects. Built one way, the site is "
            "monomorphic: one shape check per access. <bookmark mark='c'/> With two or four property "
            "orders it is polymorphic, trying up to four cached shapes in turn, two and a half checks per"
            " access. <bookmark mark='d'/> With eight, the cache overflows and the site goes megamorphic:"
            " a dictionary lookup on every one of the ten thousand accesses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(cache), FadeIn(dict_box), FadeIn(state), FadeIn(tab),
                      FadeIn(lines))
            vo.wait_until("a")
            self.play(Indicate(code, color=HEAD))
            chips = VGroup()

            def fill(k, new_state):
                anims = []
                for i in range(min(k, 4)):
                    if i >= len(chips):
                        c = Square(0.4, stroke_width=0, fill_color=SHAPE_COLORS[i], fill_opacity=0.9).move_to(
                            slots[i])
                        chips.add(c)
                        anims.append(FadeIn(c, scale=0.5))
                anims.append(Transform(state, label(new_state, font_size=19, color=WHITE).move_to(state)))
                return anims

            def row_in(r):
                return [tab.cells[r][c].animate.set_opacity(1) for c in range(5)]
            vo.wait_until("b")
            self.play(*fill(1, sites["1"]["state"]), *row_in(1))
            vo.wait_until("c")
            self.play(*fill(2, sites["2"]["state"]), *row_in(2))
            self.play(*fill(4, sites["4"]["state"]), *row_in(3))
            vo.wait_until("d")
            self.play(*[Indicate(c, color=NO) for c in chips])
            self.play(FadeOut(chips), dict_box.animate.set_opacity(1),
                      Transform(state, label(sites["8"]["state"], font_size=19, color=NO).move_to(state)),
                      *row_in(4))
            self.play(FadeIn(star), tab.cells[4][3].animate.set_color(NO), tab.cells[4][4].animate.set_color(NO))
        self.wait(0.4)
        self.clear_scene()

    def deopt(self):
        ev = load("ic")["deopt"]
        head = label(r"Speculate, \ check, \ deoptimize", font_size=36).to_edge(UP, buff=0.3)
        code = mono("function add(a, b) { return a + b; }", size=20).next_to(head, DOWN, buff=0.35)
        kinds = [DATA if k not in (4, 8) else (LAM if k == 4 else KERN) for k in range(12)]
        calls = VGroup()
        for k, a in enumerate(DEOPT_ARGS):
            box = RoundedRectangle(width=0.94, height=0.55, corner_radius=0.06, stroke_color=kinds[k],
                                   stroke_width=1.6)
            t = mono(a, size=16, color=kinds[k]).move_to(box)
            if t.width > 0.9:
                t.width = 0.9
            n = label(f"{k + 1}", font_size=16, color=GREY_B).next_to(box, UP, buff=0.08)
            calls.add(VGroup(box, t, n))
        calls.arrange(RIGHT, buff=0.06).move_to([0, 1.25, 0])
        callname = label(r"call", font_size=16, color=GREY_B).next_to(calls[0][2], LEFT, buff=0.15)
        opt_at = {e[0] for e in ev if e[1].startswith("optimized")}
        fail_at = {e[0] for e in ev if "deoptimize" in e[1]}
        # which tier ran each call: optimized code from the call after an optimization up to a failed guard
        tier, tiers = "interp", []
        for n in range(1, 13):
            if n in fail_at:
                tiers.append("fail")
                tier = "interp"
            else:
                tiers.append(tier)
            if n in opt_at:
                tier = "opt"
        band = VGroup()
        for k, t in enumerate(tiers):
            col = {"interp": GREY_C, "opt": YES, "fail": NO}[t]
            r = Rectangle(width=0.94, height=0.22, stroke_width=0, fill_color=col, fill_opacity=0.85)
            band.add(r.next_to(calls[k][0], DOWN, buff=0.15))
        legend = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=0.85),
                                 label(t, font_size=16, color=c)).arrange(RIGHT, buff=0.1)
                          for t, c in ((r"interpreter", GREY_B), (r"optimized code", YES),
                                       (r"guard failed", NO))]).arrange(RIGHT, buff=0.5).next_to(band, DOWN,
                                                                                                buff=0.25)
        flags = VGroup()
        for n in sorted(opt_at):
            tri = Triangle(color=YES, fill_opacity=1).scale(0.09).rotate(PI).next_to(calls[n - 1][0], UP, buff=0.32)
            flags.add(tri)
        evl = VGroup(*[label(rf"call {n}: \ {txt}", font_size=21, color=YES if txt.startswith("optimized") else NO)
                       for n, txt in ev]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        evl.next_to(legend, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        kinds_note = VGroup(label(r"small integers", font_size=17, color=DATA), label(r"a string", font_size=17,
                                                                                      color=LAM),
                            label(r"too big for a small integer", font_size=17, color=KERN)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).next_to(evl, RIGHT, buff=1.0).align_to(evl, UP)
        with self.voiceover(
            "The optimizer also bets on types. <bookmark mark='a'/> add is called three times with small "
            "integers, so it is compiled as one machine addition, guarded by checks that both arguments "
            "really are small integers. <bookmark mark='b'/> Call five passes a string. The guard fails, "
            "and the engine deoptimizes, rebuilding the interpreter's frame and carrying on there. "
            "<bookmark mark='c'/> At call eight, add is compiled again, for integers or strings. "
            "<bookmark mark='d'/> Call nine overflows a small integer: another deoptimization, and at "
            "call twelve a version wide enough for all three. Feedback only widens, so a function "
            "settles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(legend), FadeIn(kinds_note), FadeIn(callname))
            seq = {"a": (0, 4), "b": (4, 5), "c": (5, 8), "d": (8, 12)}
            ev_by_mark = {"a": [3], "b": [5], "c": [8], "d": [9, 12]}
            for mk, (i, j) in seq.items():
                vo.wait_until(mk)
                anims = []
                for k in range(i, j):
                    anims += [FadeIn(calls[k]), FadeIn(band[k])]
                    if k + 1 in opt_at:
                        anims.append(FadeIn(flags[sorted(opt_at).index(k + 1)]))
                self.play(LaggedStart(*anims, lag_ratio=0.25), run_time=1.6)
                self.play(*[FadeIn(evl[[n for n, _ in ev].index(c)]) for c in ev_by_mark[mk]])
        self.wait(0.4)
        self.clear_scene()

    def gc(self):
        head = label(r"Generational garbage collection", font_size=36).to_edge(UP, buff=0.3)
        young = VGroup(*[Rectangle(width=2.5, height=1.7, stroke_color=DATA, stroke_width=2) for _ in range(2)]
                       ).arrange(RIGHT, buff=0.15)
        yl = label(r"young generation: \ two halves", font_size=18, color=DATA).next_to(young, UP, buff=0.12)
        old = Rectangle(width=4.6, height=1.7, stroke_color=LAM, stroke_width=2)
        ol = label(r"old generation", font_size=18, color=LAM).next_to(old, UP, buff=0.12)
        heap = VGroup(VGroup(yl, young), VGroup(ol, old)).arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=0.4)
        live = {2, 7, 11}
        objs = VGroup(*[Square(0.32, stroke_width=0, fill_color=DATA, fill_opacity=0.9) for _ in range(15)])
        objs.arrange_in_grid(rows=3, cols=5, buff=0.12).move_to(young[0])
        ill = note(r"illustrative", font_size=17).next_to(heap, DOWN, buff=0.12).align_to(heap, RIGHT)
        # the main thread: JavaScript, with short pauses; marking of the old generation on a helper thread
        x0 = -6.0
        main = VGroup(Rectangle(width=12.0, height=0.36, stroke_width=0, fill_color=DATA, fill_opacity=0.55).move_to(
            [0, -0.35, 0]))
        pauses = VGroup(*[Rectangle(width=0.16, height=0.36, stroke_width=0, fill_color=KERN, fill_opacity=1
                                    ).move_to([x0 + x, -0.35, 0]) for x in (1.5, 3.6, 5.8, 8.1, 10.4)])
        helper = Rectangle(width=4.6, height=0.36, stroke_width=0, fill_color=LAM, fill_opacity=0.7).move_to(
            [x0 + 7.3, -0.95, 0])
        final = Rectangle(width=0.3, height=0.36, stroke_width=0, fill_color=NO, fill_opacity=1).move_to(
            [x0 + 9.75, -0.35, 0])
        tl = VGroup(label(r"main thread", font_size=16, color=GREY_A).next_to(main, UP, buff=0.08).align_to(main,
                                                                                                         LEFT),
                    label(r"helper thread", font_size=16, color=GREY_A).next_to(helper, LEFT, buff=0.2))
        notes = VGroup(
            wrapped_label(r"most objects die young: \ a \textbf{scavenge} copies the few survivors to the other half "
                          r"\ (Part 15's copying collector), \ so its cost is the live objects, \ not the garbage",
                          12.4, font_size=19, color=WHITE),
            wrapped_label(r"objects that survive twice move to the old generation, \ collected rarely by "
                          r"\textbf{mark-compact}; \ the marking runs \textbf{concurrently} on helper threads, \ "
                          r"leaving short pauses on the main thread", 12.4, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And all those objects need collecting, with Part 15's collectors. <bookmark mark='a'/> New "
            "objects fill one half of a small young generation. <bookmark mark='b'/> Most die young: a "
            "scavenge copies the few survivors to the other half, so its cost is the living, not the "
            "garbage. <bookmark mark='c'/> Objects that survive twice move to the old generation. "
            "<bookmark mark='d'/> That is collected rarely, by mark and compact, with the marking done "
            "concurrently on helper threads, so JavaScript sees only short pauses, often scheduled in "
            "idle time between frames."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heap), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(o, scale=0.5) for o in objs], lag_ratio=0.12), run_time=2)
            vo.wait_until("b")
            self.play(*[objs[i].animate.set_fill(GREY_D) for i in range(15) if i not in live], FadeIn(notes[0]))
            surv = VGroup(*[objs[i] for i in sorted(live)])
            self.play(surv.animate.arrange(RIGHT, buff=0.12).move_to(young[1]),
                      *[FadeOut(objs[i]) for i in range(15) if i not in live])
            vo.wait_until("c")
            self.play(surv[:2].animate.set_fill(LAM).arrange(RIGHT, buff=0.12).move_to(old), FadeOut(surv[2]))
            vo.wait_until("d")
            self.play(FadeIn(main), FadeIn(tl), FadeIn(notes[1]))
            self.play(LaggedStart(*[FadeIn(p) for p in pauses], lag_ratio=0.3), FadeIn(helper), FadeIn(final),
                      run_time=2)
        self.wait(0.4)
        self.clear_scene()


_ = (HEAD, YES)
