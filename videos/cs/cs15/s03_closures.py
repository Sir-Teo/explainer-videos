from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, cell_obj, code,
                                   load, mono, ptr)


class Closures(VoiceoverScene):
    def construct(self):
        self.card()
        self.scope()
        self.funarg()
        self.conversion()

    def card(self):
        card = chapter_card(2, r"Environments and closures", r"How does a function remember where it was made?",
                            lit=(1964,), extra=((1964, r"Landin: \ closures and the SECD machine"),), part=PART)
        with self.voiceover("Chapter two. Environments and closures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def scope(self):
        d = load("scope")
        head = label(r"Which $x$?", font_size=36).to_edge(UP, buff=0.3)
        prog = code(["let x = 1", "let f = fun y -> x + y in", "let x = 10 in", "f 0"], size=22,
                    color=CODE).next_to(head, DOWN, buff=0.5)
        lex = VGroup(label(r"\textbf{lexical} scope: \ the $x$ where $f$ was \textit{written}", font_size=23,
                           color=YES), mono(f"f 0  =  {d['lexical']}", 24, YES)).arrange(DOWN, buff=0.15)
        dyn = VGroup(label(r"\textbf{dynamic} scope: \ the $x$ where $f$ is \textit{called}", font_size=23,
                           color=NO), mono(f"f 0  =  {d['dynamic']}", 24, NO)).arrange(DOWN, buff=0.15)
        VGroup(lex, dyn).arrange(RIGHT, buff=1.2).next_to(prog, DOWN, buff=0.7)
        hist = VGroup(
            label(r"early LISPs and Emacs Lisp: \ dynamic, \ because it was easy to implement", font_size=21,
                  color=GREY_A),
            label(r"ALGOL 60, \ Scheme \ (1975) \ and nearly everything since: \ lexical", font_size=21,
                  color=GREY_A),
            label(r"lexical scope lets you read a function and know what its names mean", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "An environment raises a question that substitution never did. <bookmark mark='a'/> Here x is one, a "
            "function f adds x to its argument, and then a new x, ten, is introduced before f is called. Which x "
            "does f see? <bookmark mark='b'/> Under lexical scope, the one in force where f was written: f of zero "
            "is one. <bookmark mark='c'/> Under dynamic scope, the one in force where f is called: ten. Both "
            "answers come from interpreters we ran; the dynamic one simply evaluates the body in the caller's "
            "environment. <bookmark mark='d'/> The first LISPs were dynamic, because that was the easy thing to "
            "build, and Emacs Lisp still is by default. ALGOL 60 and Scheme chose lexical scope, and so has nearly "
            "every language since, for one reason: you can read a function and know what its names refer to."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog))
            vo.wait_until("a")
            self.play(Indicate(prog[0], color=HEAD), Indicate(prog[2], color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(lex))
            vo.wait_until("c")
            self.play(FadeIn(dyn))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(h) for h in hist], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    def funarg(self):
        d = load("scope")
        head = label(r"The funarg problem \ (Moses, \ 1970)", font_size=34).to_edge(UP, buff=0.3)
        prog = code(d["adder_source"], size=20, color=CODE).to_edge(LEFT, buff=0.6).shift(UP * 1.4)
        # a stack frame that disappears, and a closure that keeps n
        frame = VGroup(Rectangle(width=3.0, height=0.9, color=CTRL, stroke_width=2),
                       mono("make_adder:  n = 5", 18, CTRL))
        frame[1].move_to(frame[0])
        stack_l = label(r"the stack", font_size=19, color=GREY_B).next_to(frame, UP, buff=0.1)
        sg = VGroup(stack_l, frame).move_to(RIGHT * 3.6 + UP * 1.4)
        clo = cell_obj("closure", ["code", 5], w=1.1, font_size=17)
        clo.move_to(RIGHT * 3.6 + DOWN * 0.6)
        heap_l = label(r"the heap", font_size=19, color=GREY_B).next_to(clo, UP, buff=0.1)
        res = mono(f"(add5 1, add7 1)  =  ({d['adder'][0]}, {d['adder'][1]})", 22, YES).next_to(prog, DOWN,
                                                                                               buff=0.6).align_to(
            prog, LEFT)
        pts = VGroup(
            label(r"\texttt{add} is returned: \ it outlives the call that made it", font_size=21, color=GREY_A),
            label(r"so the $n$ it uses cannot live in that call's stack frame", font_size=21, color=NO),
            label(r"a \textbf{closure}: \ the code, \ plus the environment it needs, \ on the heap \ (Landin, \ 1964)",
                  font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "Lexical scope has a cost, and Joel Moses named it in 1970: the funarg problem. <bookmark mark='a'/> "
            "make_adder takes n and returns a function that adds n to its argument. add five and add seven are "
            "two such functions. <bookmark mark='b'/> When make_adder returns, its stack frame, with n equal to "
            "five, is gone. <bookmark mark='c'/> But add five still needs that n, every time it is called, for as "
            "long as anyone holds it. So n cannot live on the stack. <bookmark mark='d'/> The answer, which Peter "
            "Landin called a closure in 1964, is to package the function's code together with the part of the "
            "environment it needs, as an object on the heap. Our VM runs this program and gets six and eight. And "
            "here is the first reason this part needs a garbage collector: nobody knows when add five will be "
            "dropped."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(sg))
            self.wait(1.2)
            self.play(FadeOut(frame, shift=UP * 0.3), stack_l.animate.set_opacity(0.4))
            vo.wait_until("c")
            self.play(FadeIn(clo), FadeIn(heap_l), FadeIn(pts[1]))
            self.play(Indicate(clo.cells[1], color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def conversion(self):
        d = load("scope")
        head = label(r"Closure conversion", font_size=34).to_edge(UP, buff=0.3)
        src = code(["let make_adder n =", "  let add = fun x -> x + n in", "  add"], size=19,
                   color=CODE).to_edge(LEFT, buff=0.6).shift(UP * 1.6)
        l1 = VGroup(label(r"\texttt{make\_adder}, \ compiled", font_size=19, color=GREY_B),
                    code([l.strip() for l in d["make_adder"]], size=16, color=CODE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        l2 = VGroup(label(r"the inner \texttt{fun x}, \ compiled", font_size=19, color=GREY_B),
                    code([l.strip() for l in d["inner"]], size=16, color=CODE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.12)
        VGroup(l1, l2).arrange(RIGHT, buff=0.7, aligned_edge=UP).next_to(src, DOWN, buff=0.5).align_to(src, LEFT)
        # two closures sharing one code block
        c5 = cell_obj("closure", ["code", 5], w=0.95, font_size=17)
        c7 = cell_obj("closure", ["code", 7], w=0.95, font_size=17)
        VGroup(c5, c7).arrange(DOWN, buff=0.5).move_to(RIGHT * 4.0 + UP * 0.9)
        blk = VGroup(RoundedRectangle(width=2.3, height=0.8, corner_radius=0.1, color=FUNC, stroke_width=2),
                     mono("x + free 0", 17, FUNC))
        blk[1].move_to(blk[0])
        blk.move_to(RIGHT * 4.0 + DOWN * 1.4)
        arrows = VGroup(*[CurvedArrow(c.dots[0].get_center(), blk[0].get_top() + LEFT * (0.4 - 0.8 * k), angle=0.5,
                                      color=GREY_B, stroke_width=2, tip_length=0.12) for k, c in enumerate((c5, c7))])
        names = VGroup(mono("add5", 16, GREY_B).next_to(c5, LEFT, buff=0.15),
                       mono("add7", 16, GREY_B).next_to(c7, LEFT, buff=0.15))
        pts = VGroup(
            label(r"\texttt{CLOSURE}: \ copy the free variables \ (here, \ $n$) \ into a new heap object", font_size=20,
                  color=GREY_A),
            label(r"\texttt{FREE 0}: \ read them back from the running closure", font_size=20, color=GREY_A),
            label(r"\textbf{flat} closures copy values; \ \textbf{linked} closures keep a pointer to the frame: \ "
                  r"faster to make, \ slower to use \ (Shao and Appel, \ 1994)", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "A compiler turns this into something a machine can run by closure conversion. <bookmark mark='a'/> "
            "Our compiler finds the free variables of every inner function, here just n. In make_adder, the "
            "CLOSURE instruction copies n into a new heap object, next to a reference to the inner function's "
            "code. <bookmark mark='b'/> Inside that code, FREE zero reads n back out of whichever closure is "
            "running. <bookmark mark='c'/> So add five and add seven are two small objects, holding five and seven, "
            "that share one block of code. <bookmark mark='d'/> Copying the values is called a flat closure. The "
            "alternative is to keep a pointer to the enclosing frame, itself on the heap: cheaper to build, "
            "slower to use, and more likely to keep garbage alive, which is why Shao and Appel studied which to "
            "choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(l1), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(l2), FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(c5), FadeIn(c7), FadeIn(names), FadeIn(blk), Create(arrows))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
