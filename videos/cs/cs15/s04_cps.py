from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table, load,
                                   mono, words)


class Continuations(VoiceoverScene):
    def construct(self):
        self.card()
        self.cps()
        self.tail()
        self.callcc()

    def card(self):
        card = chapter_card(3, r"Continuations and tail calls", r"Can ``what happens next'' be a value?",
                            lit=(1975,), extra=((1975, r"Scheme: \ Sussman and Steele"),), part=PART)
        with self.voiceover("Chapter three. Continuations and tail calls."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cps(self):
        d = load("cps")
        head = label(r"Continuation-passing style", font_size=34).to_edge(UP, buff=0.3)
        src = d["fact_source"]
        direct = code([src[0]], size=18, color=CODE)
        cps = code([src[1]], size=18, color=CODE)
        dl = label(r"direct: \ the multiplication waits on the stack", font_size=20, color=GREY_A)
        cl = label(r"CPS: \ $k$ is ``what to do with the answer''; \ the waiting work is a closure", font_size=20,
                   color=LAM)
        blk = VGroup(dl, direct, cl, cps).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.4)
        if blk.width > 13:
            blk.scale_to_fit_width(13)
        r = next(x for x in d["fact"] if x["n"] == 1000)
        tab = grid_table([r"\texttt{fact 1000} on our VM", r"deepest stack, words", r"closures built",
                          r"heap words"], [
            [r"direct", words(r["direct"]["max_stack"]), words(r["direct"]["closures"]),
             words(r["direct"]["words"])],
            [r"CPS", words(r["cps"]["max_stack"]), words(r["cps"]["closures"]), words(r["cps"]["words"])],
        ], widths=[3.6, 3.0, 2.4, 2.2], row_h=0.5, font_size=20,
            colors=[[WHITE, NO, WHITE, WHITE], [WHITE, YES, LAM, LAM]]).next_to(blk, DOWN, buff=0.45)
        pts = VGroup(
            label(r"every call is now the last thing its caller does: \ nothing waits on the stack", font_size=21,
                  color=GREY_A),
            label(r"the stack has become a chain of closures on the heap: \ the \textbf{continuation}", font_size=21,
                  color=YES),
            label(r"compilers for ML and Scheme use CPS inside \ (Steele, \ 1978; \ Appel, \ 1992)", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A function call does two things: it computes a value, and it remembers where to go back to. "
            "Continuation-passing style separates them. <bookmark mark='a'/> In direct style, factorial of n "
            "calls factorial of n minus one and then multiplies. The multiplication waits, in a stack frame, until "
            "the inner call returns. <bookmark mark='b'/> In CPS every function takes one more argument, k, the "
            "continuation: what to do with the answer. fact_cps never returns to multiply. It calls itself with a "
            "new continuation, a closure that will multiply by n and then pass the result to the old k. <bookmark "
            "mark='c'/> Run both on our VM for a thousand. Direct style needs a stack five thousand words deep. "
            "CPS needs five words of stack, and builds a thousand closures instead. <bookmark mark='d'/> Nothing "
            "has been saved: the waiting work has moved, from the stack into a chain of closures on the heap. But "
            "now it is data. It can be stored, inspected, called twice, or never, and compilers for Scheme and ML "
            "use exactly this form inside."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dl), FadeIn(direct))
            vo.wait_until("b")
            self.play(FadeIn(cl), FadeIn(cps))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def tail(self):
        d = load("cps")
        head = label(r"Tail calls are jumps", font_size=34).to_edge(UP, buff=0.3)
        src = code(["let rec words cs cur acc =", "  match cs with", "    [] -> ...",
                    "  | c :: rest -> ... words rest (c :: cur) acc     (* a tail call *)"], size=18,
                   color=CODE).next_to(head, DOWN, buff=0.45)
        on, off = d["tco"]["on"], d["tco"]["off"]
        W = 7.2
        mx = off["max_stack"]
        b_off = Rectangle(width=W, height=0.5, stroke_width=0, fill_color=NO, fill_opacity=0.85)
        b_on = Rectangle(width=max(W * on["max_stack"] / mx, 0.05), height=0.5, stroke_width=0, fill_color=YES,
                         fill_opacity=0.85)
        rows = VGroup()
        for name, bar, val, c in ((r"each call a new frame", b_off, off["max_stack"], NO),
                                  (r"tail calls reuse the frame", b_on, on["max_stack"], YES)):
            n = label(name, font_size=20, color=c)
            v = label(rf"{words(val)} words", font_size=20, color=c)
            rows.add(VGroup(n, bar, v))
        for k, r in enumerate(rows):
            r[1].move_to([-4.6 + r[1].width / 2, -0.4 - 0.9 * k, 0])
            r[0].next_to(r[1], UP, buff=0.08).align_to(r[1], LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.15)
        cap = label(rf"the Job's deepest stack on Part 7's chapter \ ({words(d['bytes'])} bytes); \ "
                    rf"{words(on['tailcalls'])} calls were tail calls", font_size=19, color=GREY_B).next_to(
            rows, UP, buff=0.35)
        pts = VGroup(
            label(r"without them, \ the stack grows with the text: \ the thirty novels would need gigabytes",
                  font_size=21, color=NO),
            label(r"Scheme requires proper tail calls; \ ML and Haskell rely on them; \ CPython and the JVM do not "
                  r"have them", font_size=21, color=GREY_A),
            label(r"``Debunking the expensive procedure call myth'' \ (Steele, \ 1977): \ a call in tail position is a "
                  r"\texttt{goto} with arguments", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Once nothing waits after a call, the call does not need a frame of its own. <bookmark mark='a'/> In "
            "the Job, words calls itself as the very last thing it does, once for every character of the text. "
            "A call in this position is a tail call. Our compiler marks it, and the VM reuses the caller's frame, "
            "so the call becomes a jump. <bookmark mark='b'/> We ran the Job both ways. With a new frame for every "
            "call, the stack reaches sixty-eight thousand words on one chapter, and it grows with the length of "
            "the text. <bookmark mark='c'/> With tail calls, three thousand words, however long the text. <bookmark "
            "mark='d'/> For the thirty novels the difference is between running and crashing. Scheme's standard "
            "requires proper tail calls, and functional languages depend on them; CPython and the Java virtual "
            "machine still do not provide them. Guy Steele argued in 1977 that a tail call is just a go-to that "
            "passes arguments, and he was right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(src[3], color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(cap), FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def callcc(self):
        d = load("cps")["product"]
        head = label(r"Grabbing the continuation: \ \texttt{call/cc}", font_size=34).to_edge(UP, buff=0.3)
        src = code(d["source"][:-1], size=16, color=CODE).next_to(head, DOWN, buff=0.4)
        lst = mono("l = " + d["list"], 19, WHITE).next_to(src, DOWN, buff=0.35)
        tab = grid_table([r"on our CEK machine", r"steps", r"multiplications", r"continuations captured"], [
            ["product l", str(d["plain"]["steps"]), str(d["plain"]["mults"]), "0"],
            ["product_exit l", str(d["exit"]["steps"]), str(d["exit"]["mults"]),
             str(d["exit"]["captured"])],
        ], widths=[3.6, 1.6, 2.6, 3.4], row_h=0.5, font_size=20,
            colors=[[WHITE, WHITE, NO, WHITE], [WHITE, WHITE, YES, LAM]]).next_to(lst, DOWN, buff=0.35)
        pts = VGroup(
            label(r"$k$ is the rest of the program at the \texttt{callcc}; \ calling $k\,0$ abandons everything "
                  r"in between", font_size=20, color=GREY_A),
            label(r"an exception is exactly this; \ a generator or coroutine is a continuation resumed later",
                  font_size=20, color=GREY_A),
            label(r"its type is Peirce's law, \ $((A \to B) \to A) \to A$: \ Part 14's classical logic, \ now running",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "If the continuation is data, a program can ask for it. <bookmark mark='a'/> Scheme's call with current "
            "continuation, call/cc, passes the rest of the program to a function, as a value k. product_exit "
            "multiplies a list's elements, but the moment it meets a zero it calls k with zero, and the "
            "multiplications still waiting are simply dropped. <bookmark mark='b'/> To run this we need a machine "
            "whose stack is data, so we built one: a CEK machine, for control, environment and continuation, from "
            "Felleisen and Friedman, with the continuation as a linked list of frames. <bookmark mark='c'/> The "
            "plain product does twelve multiplications. The one that escapes does none: it found the zero, and "
            "threw the pending work away. <bookmark mark='d'/> That is an exception, built from nothing but a "
            "continuation. Resuming a saved continuation later gives generators and coroutines. And the type of "
            "call/cc is Peirce's law, which Part 14 showed has no proof in pure functional programs. Classical "
            "logic, it turns out, is a jump."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(lst), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(Indicate(src, color=LAM, scale_factor=1.02))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()
