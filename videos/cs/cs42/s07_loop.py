from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, module_box, tag_box

SYNC, MICRO, TASK, RAF = GREY_A, LAM, DATA, YES

# the four programs, as JavaScript (log is console.log); each output line's source, for colouring
PROGRAMS = {
    "nested": (['setTimeout(() => {', '  log("t1");', '  Promise.resolve().then(() => log("p-in-t1"));', '});',
                'setTimeout(() => log("t2"));', 'Promise.resolve().then(() => {', '  log("p1");',
                '  Promise.resolve().then(() => log("p2"));', '});', 'log("sync");'],
               {"sync": SYNC, "p1": MICRO, "p2": MICRO, "t1": TASK, "p-in-t1": MICRO, "t2": TASK}),
    "async": (['async function f() {', '  log("f starts");', '  await null;', '  log("f resumes");', '}',
               'log("before call");', 'f();', 'Promise.resolve().then(() => log("then"));', 'log("after call");'],
              {"before call": SYNC, "f starts": SYNC, "after call": SYNC, "f resumes": MICRO, "then": MICRO}),
    "async2": (['log("script start");', 'setTimeout(() => log("timeout"));', 'Promise.resolve().then(() => {',
                '  log("promise1");', '  Promise.resolve().then(() => log("promise2"));', '});',
                'requestAnimationFrame(() => log("raf"));', 'log("script end");'],
               {"script start": SYNC, "script end": SYNC, "promise1": MICRO, "promise2": MICRO, "timeout": TASK,
                "raf": RAF}),
}


class Loop(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.basic()
        self.more()
        self.races()
        self.workers()

    def card(self):
        card = chapter_card(6, r"The event loop", r"In what order does a page's code run?", lit=(2015, 2017),
                            extra=((2015, r"ES2015: \ promises"), (2017, r"ES2017: \ async and await")), part=PART)
        with self.voiceover("Chapter six. The event loop."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the loop as the standard writes it
    def model(self):
        head = label(r"One thread, \ one loop", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(["while (true) {", "  task = oldestRunnableTask();", "  run(task);   // to completion",
                           "  while (microtasks.length)", "    run(microtasks.shift());", "  if (frameIsDue()) {",
                           "    runAnimationFrameCallbacks();", "    style(); layout(); paint();", "  }", "}"],
                          size=16).to_corner(UL, buff=0.5).shift(DOWN * 0.75)
        c, rad = np.array([3.75, -0.1, 0]), 1.9
        spots = [c + rad * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, 0, -PI / 2, PI)]
        st = VGroup(module_box(r"take one task", TASK, w=2.3, h=0.6, font=18),
                    module_box(r"run to completion", TASK, w=2.4, h=0.6, font=18),
                    module_box(r"drain microtasks", MICRO, w=2.4, h=0.6, font=18),
                    module_box(r"render, \ if a frame is due", RAF, w=2.6, h=0.6, font=18))
        for b, p in zip(st, spots):
            b.move_to(p)
        st[1].shift(LEFT * 0.15)
        st[3].shift(RIGHT * 0.25)
        arcs = VGroup(*[ArcBetweenPoints(c + rad * np.array([np.cos(a0), np.sin(a0), 0]),
                                         c + rad * np.array([np.cos(a1), np.sin(a1), 0]), angle=-PI / 4,
                                         color=GREY_B, stroke_width=2).add_tip(tip_length=0.15)
                        for a0, a1 in ((PI / 2 - 0.55, 0.45), (-0.45, -PI / 2 + 0.6), (-PI / 2 - 0.6, PI + 0.45),
                                       (PI - 0.45, PI / 2 + 0.6))])
        loop_path = Circle(radius=rad + 0.5, color=WHITE).move_to(c).rotate(PI / 2)
        loop_path.reverse_direction()
        token = Dot(radius=0.1, color=HEAD).move_to(loop_path.point_from_proportion(0))
        notes = VGroup(
            wrapped_label(r"tasks: \ timers, \ input events, \ network replies, \ messages; \ the browser may pick "
                          r"between task queues, \ but each queue keeps its order", 6.0, font_size=19, color=TASK),
            wrapped_label(r"microtasks: \ promise reactions and \texttt{queueMicrotask}; \ all of them run, \ even "
                          r"ones queued meanwhile, \ before anything else", 6.0, font_size=19, color=MICRO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(code, DOWN, buff=0.4).align_to(code, LEFT)
        std = note(r"after the HTML Living Standard's event-loop processing model", font_size=16).to_corner(
            DR, buff=0.15)
        with self.voiceover(
            "A web page's JavaScript runs on one thread, driven by a loop the HTML standard writes out step by "
            "step. <bookmark mark='a'/> Take one task from a task queue: a timer, a click, a network reply. Run it "
            "to completion; nothing interrupts it. <bookmark mark='b'/> Then drain the microtask queue, the "
            "reactions of promises, completely, including any microtasks queued while draining. "
            "<bookmark mark='c'/> Then, if a frame is due, run the rendering steps: animation frame callbacks, "
            "style, layout and paint. <bookmark mark='d'/> And go round again. Everything about ordering on the "
            "web follows from these four steps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(std))
            vo.wait_until("a")
            self.play(FadeIn(st[0]), FadeIn(st[1]), Create(arcs[0]), FadeIn(token), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(st[2]), Create(arcs[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(st[3]), Create(arcs[2]), Create(arcs[3]))
            vo.wait_until("d")
            self.play(MoveAlongPath(token, loop_path), run_time=2.5, rate_func=linear)
            self.play(MoveAlongPath(token, loop_path), run_time=2.5, rate_func=linear)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the basic program, animated
    def basic(self):
        want = list(load("orderings")["basic"])
        head = label(r"Tasks and microtasks, \ step by step", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(['console.log("A");', 'setTimeout(() => console.log("B"), 0);',
                           'Promise.resolve().then(() => console.log("C"));', 'console.log("D");'], size=17)
        code.to_corner(UL, buff=0.5).shift(DOWN * 0.7)
        cursor = SurroundingRectangle(code[0], color=HEAD, buff=0.06, stroke_width=1.5)

        def lane(title, y, col, x0=0.3, x1=6.6):
            box = Rectangle(width=x1 - x0, height=0.7, stroke_color=col, stroke_width=1.5).move_to(
                [(x0 + x1) / 2, y, 0])
            t = label(title, font_size=18, color=col).next_to(box, UP, buff=0.08).align_to(box, LEFT)
            return VGroup(box, t)
        tq = lane(r"task queue", 0.2, TASK)
        mq = lane(r"microtask queue", -1.3, MICRO)
        lg = lane(r"log", -2.8, WHITE)
        sbox = Rectangle(width=3.4, height=2.6, stroke_color=KERN, stroke_width=1.5).move_to([-4.7, -1.55, 0])
        stitle = label(r"call stack", font_size=18, color=KERN).next_to(sbox, UP, buff=0.08).align_to(sbox, LEFT)
        bottom = sbox.get_bottom() + UP * 0.35
        logged = VGroup()

        def emit(s):
            assert want[len(logged)] == s, (want, s)
            t = tag_box(s, color=WHITE, size=20, w=0.8).move_to(
                lg[0].get_left() + RIGHT * (0.6 + 1.0 * len(logged)))
            logged.add(t)
            return FadeIn(t, shift=DOWN * 0.2)

        def frame(name, col):
            return tag_box(name, color=col, size=16, w=3.0, h=0.45)
        script = frame("script", SYNC).move_to(bottom)
        cb_b = tag_box('() => log("B")', color=TASK, size=16).next_to(code[1], RIGHT, buff=0.2)
        cb_c = tag_box('() => log("C")', color=MICRO, size=16).next_to(code[2], DOWN, buff=0.05).align_to(
            code[2], RIGHT)
        with self.voiceover(
            "Watch the loop run four lines. <bookmark mark='a'/> The script itself is the first task, and goes on "
            "the call stack. It logs A. <bookmark mark='b'/> setTimeout, even with a delay of zero, puts a callback "
            "in the task queue, to run in some later task. <bookmark mark='c'/> A promise's then puts its callback "
            "in the microtask queue. <bookmark mark='d'/> The script logs D, and finishes; the stack is empty. "
            "<bookmark mark='e'/> Before any other task, the microtasks drain: C. <bookmark mark='f'/> Only then "
            "does the loop take the next task, and B is logged last. A, D, C, B: our interpreter computes this "
            "order from the processing model, and every browser agrees."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(tq), FadeIn(mq), FadeIn(lg), Create(sbox), FadeIn(stitle))
            vo.wait_until("a")
            self.play(FadeIn(script, shift=UP * 0.3), Create(cursor))
            self.play(emit("A"))
            vo.wait_until("b")
            self.play(cursor.animate.become(SurroundingRectangle(code[1], color=HEAD, buff=0.06, stroke_width=1.5)))
            self.play(FadeIn(cb_b))
            self.play(cb_b.animate.move_to(tq[0].get_left() + RIGHT * (cb_b.width / 2 + 0.2)))
            vo.wait_until("c")
            self.play(cursor.animate.become(SurroundingRectangle(code[2], color=HEAD, buff=0.06, stroke_width=1.5)))
            self.play(FadeIn(cb_c))
            self.play(cb_c.animate.move_to(mq[0].get_left() + RIGHT * (cb_c.width / 2 + 0.2)))
            vo.wait_until("d")
            self.play(cursor.animate.become(SurroundingRectangle(code[3], color=HEAD, buff=0.06, stroke_width=1.5)))
            self.play(emit("D"))
            self.play(FadeOut(script, shift=DOWN * 0.3), FadeOut(cursor))
            vo.wait_until("e")
            self.play(cb_c.animate.move_to(bottom))
            self.play(emit("C"))
            self.play(FadeOut(cb_c, shift=DOWN * 0.3))
            vo.wait_until("f")
            self.play(cb_b.animate.move_to(bottom))
            self.play(emit("B"))
            self.play(FadeOut(cb_b, shift=DOWN * 0.3))
            self.play(Indicate(logged, color=HEAD))
        assert len(logged) == len(want)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ three more programs
    def more(self):
        o = load("orderings")
        head = label(r"Three more orderings, \ computed", font_size=36).to_edge(UP, buff=0.3)
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.85),
                                 label(t, font_size=17, color=c)).arrange(RIGHT, buff=0.1)
                          for t, c in ((r"synchronous", SYNC), (r"microtask", MICRO), (r"task", TASK),
                                       (r"animation frame", RAF))]).arrange(RIGHT, buff=0.45)
        legend.to_edge(DOWN, buff=0.3)
        notes = {
            "nested": wrapped_label(r"a microtask queued by a microtask still runs before the next task; \ one "
                                    r"queued inside a task runs right after that task", 5.0, font_size=19,
                                    color=MICRO),
            "async": wrapped_label(r"an async function runs synchronously up to its first \texttt{await}; \ the rest "
                                   r"of it is a microtask", 5.0, font_size=19, color=MICRO),
            "async2": wrapped_label(r"here the next frame is 16.7 ms away, \ so the timer wins; \ in a browser, \ "
                                    r"timeout and animation frame can come in either order", 5.0, font_size=19,
                                    color=RAF),
        }

        def show(name):
            lines, src = PROGRAMS[name]
            code = code_block(lines, size=16).move_to([-3.0, 0.2, 0]).align_to([-6.6, 0, 0], LEFT)
            out = VGroup(*[tag_box(s, color=src[s], size=17) for s in o[name]]).arrange(DOWN, buff=0.12,
                                                                                         aligned_edge=LEFT)
            nums = VGroup(*[label(f"{i + 1}", font_size=17, color=GREY_B).next_to(t, LEFT, buff=0.15)
                            for i, t in enumerate(out)])
            col = VGroup(out, nums).move_to([2.6, 0.5, 0]).align_to([1.6, 0, 0], LEFT)
            n = notes[name].next_to(col, RIGHT, buff=0.4).align_to(col, UP)
            if n.get_right()[0] > 6.8:
                n.next_to(col, DOWN, buff=0.3).align_to(col, LEFT)
            return code, out, nums, n
        with self.voiceover(
            "The same four steps settle harder cases, and our interpreter computes each one. "
            "<bookmark mark='a'/> Here two timers and a promise whose reaction queues another. The synchronous log "
            "comes first, then both promise reactions, because a microtask queued while draining still runs in "
            "the same drain. Then the first timer, whose own microtask runs before the second timer. "
            "<bookmark mark='b'/> An async function runs synchronously until its first await. The rest of it "
            "becomes a microtask, queued before the promise below, so f resumes before then. "
            "<bookmark mark='c'/> Finally a timer against an animation frame. In our model the next frame is "
            "sixteen point seven milliseconds away, so the timer runs first; in a real browser those two can come "
            "in either order, and code should never depend on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend))
            prev = None
            for mk, name in zip("abc", ("nested", "async", "async2")):
                vo.wait_until(mk)
                code, out, nums, n = show(name)
                if prev:
                    self.play(FadeOut(prev))
                self.play(FadeIn(code))
                self.play(LaggedStart(*[FadeIn(VGroup(t, m), shift=LEFT * 0.2) for t, m in zip(out, nums)],
                                      lag_ratio=0.5), run_time=2.5)
                self.play(FadeIn(n))
                prev = VGroup(code, out, nums, n)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ run to completion, and logical races
    def races(self):
        head = label(r"No threads, \ still races", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(["async function buy() {", "  const n = await stockLeft();", "  if (n > 0)",
                           "    await placeOrder();", "}", "button.onclick = buy;"], size=17).to_corner(UL, buff=0.5)
        code.shift(DOWN * 0.7)
        x0, y = -6.4, -1.4
        segs = [(r"click 1: \ ask for stock", DATA, 2.4), (r"click 2: \ ask for stock", LAM, 2.4),
                (r"1 resumes: \ $n = 1$, \ order", DATA, 2.6), (r"2 resumes: \ $n = 1$, \ order", LAM, 2.6)]
        bars, x = VGroup(), x0
        for t, c, w in segs:
            r = Rectangle(width=w - 0.08, height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.8).move_to(
                [x + w / 2, y, 0])
            bars.add(VGroup(r, label(t, font_size=17, color=BLACK).move_to(r)))
            x += w
        awaits = VGroup(*[Triangle(color=HEAD, fill_opacity=1).scale(0.09).rotate(PI).move_to(
            [x0 + w, y + 0.42, 0]) for w in (2.4, 4.8)])
        tl = label(r"the main thread, \ one piece at a time", font_size=18, color=GREY_A).next_to(
            bars, UP, buff=0.25).align_to(bars, LEFT)
        bad = label(r"two orders for the last item", font_size=20, color=NO).next_to(bars, DOWN, buff=0.25).align_to(
            bars, RIGHT)
        notes = VGroup(
            wrapped_label(r"run to completion: \ no two pieces of script ever run at once, \ so the JavaScript heap "
                          r"has no data races \ (Part 33)", 5.6, font_size=19, color=YES),
            wrapped_label(r"but every \texttt{await} ends a piece: \ other tasks run there, \ and state read "
                          r"before it may be stale after it", 5.6, font_size=19, color=NO),
            wrapped_label(r"and a piece that never ends freezes the page: \ no rendering, \ no input \ "
                          r"(Chapter 5)", 5.6, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 1.0, 0])
        illus = note(r"illustrative", font_size=16).to_corner(DR, buff=0.2)
        with self.voiceover(
            "Run to completion is a strong guarantee. <bookmark mark='a'/> No two pieces of script ever run at "
            "once, so the JavaScript heap cannot have the data races of Part 33: no lock is ever needed. Promises "
            "and async functions are concurrency without threads, continuations the loop resumes later. "
            "<bookmark mark='b'/> But every await ends a piece. Two quick clicks each ask for the stock, each hear "
            "that one item is left, and each places an order: a logical race, with no threads at all. "
            "<bookmark mark='c'/> And the guarantee cuts the other way too. A piece that never ends blocks "
            "everything behind it, rendering and input included, which is the frozen page of the last chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(illus))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(tl), FadeIn(notes[1]))
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.6), FadeIn(awaits),
                      run_time=3)
            self.play(FadeIn(bad))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Web Workers
    def workers(self):
        head = label(r"Web Workers: \ parallel, \ by message", font_size=36).to_edge(UP, buff=0.3)

        def thread(name, col, x):
            box = RoundedRectangle(width=4.0, height=2.6, corner_radius=0.15, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.06).move_to([x, 0.9, 0])
            t = label(name, font_size=21, color=col).next_to(box.get_top(), DOWN, buff=0.15)
            loop = Arc(radius=0.35, start_angle=PI / 2, angle=-1.6 * PI, color=col, stroke_width=3).add_tip(
                tip_length=0.12)
            parts = VGroup(VGroup(loop, label(r"its own loop", font_size=17, color=col)).arrange(RIGHT, buff=0.15),
                           label(r"its own heap", font_size=17, color=col)).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.25)
            parts.next_to(t, DOWN, buff=0.3)
            return VGroup(box, t, parts)
        main = thread(r"main thread: \ the DOM", DATA, -3.6)
        work = thread(r"worker: \ no DOM", KERN, 3.6)
        p1 = main[0].get_right() + UP * 0.5
        p2 = work[0].get_left() + UP * 0.5
        wire = VGroup(Arrow(p1, p2, buff=0.1, color=GREY_B, stroke_width=2),
                      Arrow(p2 + DOWN * 1.0, p1 + DOWN * 1.0, buff=0.1, color=GREY_B, stroke_width=2))
        msg = tag_box("text", color=HEAD, size=16).move_to(p1 + RIGHT * 0.6)
        reply = tag_box("counts", color=HEAD, size=16).move_to(p2 + DOWN * 1.0 + LEFT * 0.7)
        code = code_block(['const w = new Worker("count.js");', 'w.postMessage(text);',
                           'w.onmessage = (e) => show(e.data);'], size=16).next_to(main, DOWN, buff=0.35).align_to(
            main, LEFT)
        notes = VGroup(
            wrapped_label(r"a message is copied \ (the structured clone), \ or \textbf{transferred}: \ an "
                          r"\texttt{ArrayBuffer} moves, \ and the sender's is left empty", 6.0, font_size=19,
                          color=WHITE),
            wrapped_label(r"\texttt{SharedArrayBuffer} with \texttt{Atomics} brings back shared memory, \ only for "
                          r"cross-origin-isolated pages, \ and with it real data races", 6.0, font_size=19,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(code, RIGHT, buff=0.5).align_to(code, UP)
        with self.voiceover(
            "For work that really is long, a page can use more than one core. <bookmark mark='a'/> A Web Worker is "
            "a second thread with its own event loop and its own heap, and no access to the page. "
            "<bookmark mark='b'/> The two share nothing; they talk by posting messages, which arrive as tasks. The "
            "main thread sends the text, the worker counts it, and the counts come back, while the animation keeps "
            "its frames. <bookmark mark='c'/> A message is copied, or its buffer is transferred, leaving the sender "
            "with nothing. Shared memory with atomic operations exists too, only for pages isolated from other "
            "origins, and it brings the data races back."
        ) as vo:
            self.play(FadeIn(head), FadeIn(main))
            vo.wait_until("a")
            self.play(FadeIn(work))
            vo.wait_until("b")
            self.play(GrowArrow(wire[0]), FadeIn(code), FadeIn(msg))
            self.play(msg.animate.move_to(p2 + LEFT * 0.6), run_time=1.5)
            self.play(Indicate(work[2]), FadeOut(msg))
            self.play(GrowArrow(wire[1]), FadeIn(reply))
            self.play(reply.animate.move_to(p1 + DOWN * 1.0 + RIGHT * 0.7), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, HEAD, YES)
