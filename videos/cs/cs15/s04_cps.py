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
        tab = grid_table([r"\texttt{fact 1000} on our VM", 'deepest stack, slots', r"closures built",
                          'heap slots'], [
            [r"direct", words(r["direct"]["max_stack"]), words(r["direct"]["closures"]),
             words(r["direct"]["words"])],
            [r"CPS", words(r["cps"]["max_stack"]), words(r["cps"]["closures"]), words(r["cps"]["words"])],
        ], widths=[3.6, 3.0, 2.4, 2.2], row_h=0.5, font_size=20,
            colors=[[WHITE, NO, WHITE, WHITE], [WHITE, YES, LAM, LAM]]).next_to(blk, DOWN, buff=0.45)
        qual=label('logical VM slots; excludes host big-integer storage and time',font_size=18,color=HEAD).next_to(tab,DOWN,buff=.2)
        pts = VGroup(
            label('these CPS calls are tail calls; pending work is explicit in closures', font_size=21,
                  color=GREY_A),
            label(r"the stack has become a chain of closures on the heap: \ the \textbf{continuation}", font_size=21,
                  color=YES),
            label('CPS is one compiler representation (Steele, 1978; Appel, 1992)', font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover("A call computes a value and remembers the pending work. <bookmark mark='a'/> In direct factorial, multiplication waits for the recursive result, so our VM keeps frames. <bookmark mark='b'/> In continuation-passing style, k represents what to do next. A new closure remembers multiplication by n and the previous continuation. <bookmark mark='c'/> For factorial of a thousand, the table counts logical stack and heap slots in our Python reference VM. Its arbitrary-precision arithmetic is not Pebble's fixed-width arithmetic; these counts exclude the host's big-integer storage and computation. <bookmark mark='d'/> Pending work moves into closures and becomes explicit data. CPS is a useful compiler representation, including in influential ML and Scheme compilers, but it does not guarantee a universal space or speed saving.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(dl), FadeIn(direct), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(cl), FadeIn(cps))
            vo.wait_until('c')
            self.play(FadeIn(tab), FadeIn(qual))
            vo.wait_until('d')
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
        W = 4.5
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
            r[1].move_to([-5.6 + r[1].width / 2, -0.4 - 0.9 * k, 0])
            r[0].next_to(r[1], UP, buff=0.08).align_to(r[1], LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.15)
        cap = label(rf"the Job's deepest stack on Part 7's chapter \ ({words(d['bytes'])} bytes); \ "
                    rf"{words(on['tailcalls'])} calls were tail calls", font_size=19, color=GREY_B).next_to(
            rows, UP, buff=0.35)
        pts = VGroup(
            label('tail calls remove frames from the character loop; other recursion remains',
                  font_size=21, color=NO),
            label('proper tail calls bound a tail-call chain, not every source of stack growth', font_size=21, color=GREY_A),
            label(r"``Debunking the expensive procedure call myth'' \ (Steele, \ 1977): \ a call in tail position is a "
                  r"\texttt{goto} with arguments", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        vtab=grid_table(['distinct words','deepest stack'],
            [[str(r['distinct_words']),words(r['max_stack'])] for r in d['vocabulary']],
            widths=[2.0,2.0],row_h=.43,font_size=19).move_to(RIGHT*3.7+DOWN*.35)
        vcap=label('TCO on; bump still has pending CONS work',font_size=17,color=HEAD).next_to(vtab,DOWN,buff=.2)
        with self.voiceover(
            (
            "When no work waits after a call, the caller's frame can be reused. <bookmark mark='a'/> The Job's "
            "character loop calls words in tail position. Our compiler marks that position and the VM turns the "
            "call into a jump with arguments. <bookmark mark='b'/> On the measured chapter, disabling this "
            "optimization greatly increases the deepest stack. <bookmark mark='c'/> Reusing tail-call frames does "
            "not bound the entire Job independently of its input. The table-update function bump still has "
            "non-tail recursive work. Our separate tests with twenty, eighty and two hundred distinct words show "
            "its stack growing with vocabulary. <bookmark mark='d'/> Proper tail calls bound the active tail-call "
            "chain. Scheme requires them; other implementations differ. Always identify which recursion is tail "
            "recursive before making a space claim."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(Indicate(src[3], color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(cap), FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]))
            vo.wait_until("d")
            self.play(FadeIn(vtab),FadeIn(vcap),LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.4), run_time=2.5)
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
            label('continuations can express exceptions and coroutines; effects are not undone',
                  font_size=20, color=GREY_A),
            label(r"its type is Peirce's law, \ $((A \to B) \to A) \to A$: \ Part 14's classical logic, \ now running",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "A program can capture its continuation. <bookmark mark='a'/> call/cc passes a representation of the "
            "current continuation to a function. In product_exit, invoking it with zero abandons the "
            "multiplications waiting between the capture and the invocation. <bookmark mark='b'/> Our CEK machine "
            "makes this concrete with control, environment and linked continuation frames. <bookmark mark='c'/> "
            "The measured list produces zero multiplications in the escaping version, while ordinary product "
            "performs the displayed work. <bookmark mark='d'/> Continuations can express exceptions and, with "
            "suitable protocols, coroutines. Control transfer does not undo arbitrary effects. The classical type "
            "of call/cc connects this jump to Peirce's law, beyond the pure intuitionistic core studied in Part "
            "fourteen."
        )
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
