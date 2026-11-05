from __future__ import annotations

import textwrap

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table,
                                   load, mono, words)


class Machines(VoiceoverScene):
    def construct(self):
        self.card()
        self.wasm()
        self.validate()
        self.prolog()
        self.others()

    def card(self):
        card = chapter_card(13, r"WebAssembly, \ and other machines", r"What else can a runtime be?", lit=(2017,),
                            extra=((2017, r"WebAssembly"),), part=PART)
        with self.voiceover("Chapter thirteen. WebAssembly, and other machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def wasm(self):
        d = load("wasm")
        head = label(r"A stack machine for the web", font_size=34).to_edge(UP, buff=0.3)
        wat = code(d["wat"], size=15, color=CODE).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        b = d["bytes"]
        hexl = [" ".join(f"{x:02x}" for x in b[i:i + 12]) for i in range(0, len(b), 12)]
        hx = VGroup(label(rf"the whole module: \ {d['size']} bytes, \ assembled by hand", font_size=19,
                          color=GREY_B), code(hexl, size=14, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        run = VGroup(label(rf"run by node \ ({d['node']}):", font_size=19, color=GREY_B),
                     mono(f"fact(20n)  =  {d['fact20']}", 18, YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        right = VGroup(hx, run).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        pts = VGroup(
            label(r"a stack machine like ours, \ with types: \ \texttt{i32}, \ \texttt{i64}, \ \texttt{f32}, \ "
                  r"\texttt{f64}", font_size=20, color=GREY_A),
            label(r"no arbitrary jumps: \ only \texttt{block}, \ \texttt{loop}, \ \texttt{if} \ and branches to their ends",
                  font_size=20, color=GREY_A),
            label(r"in every major browser since 2017 \ (Haas et al., \ 2017)", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In 2017 the four major browsers shipped a new virtual machine together: WebAssembly. <bookmark "
            "mark='a'/> It is a stack machine, much like ours. Here is factorial, written in its text format. "
            "local.get pushes the argument; i64.eqz tests it for zero; i64.mul multiplies the two values on top of "
            "the stack. <bookmark mark='b'/> We assembled the binary by hand, fifty-five bytes, and node ran it: "
            "factorial of twenty, correct to the last digit. <bookmark mark='c'/> Two things set WebAssembly "
            "apart from our VM. Its values are typed, thirty-two- and sixty-four-bit integers and floats. And it "
            "has no arbitrary jumps: control flow is structured, in blocks, loops and ifs, and a branch may only go "
            "to the end of an enclosing block. That second choice is what makes the next trick possible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(wat))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(hx), FadeIn(run))
            vo.wait_until("c")
            self.play(FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()

    def validate(self):
        d = load("wasm")
        head = label(r"Validation is type checking", font_size=34).to_edge(UP, buff=0.3)
        bad = code(d["bad_wat"], size=18, color=CODE).next_to(head, DOWN, buff=0.5)
        err = VGroup(label(r"node, \ before running a single instruction:", font_size=19, color=GREY_B),
                     code(textwrap.wrap(d["error"], 64), size=15, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(bad, DOWN, buff=0.45)
        stack = VGroup(*[VGroup(Rectangle(width=1.4, height=0.42, color=c, stroke_width=2).set_fill(c, 0.12),
                                mono(t, 16, c)) for t, c in (("i64", DATA),)])
        for s_ in stack:
            s_[1].move_to(s_[0])
        pts = VGroup(
            label(r"the validator runs each function once, \ on \textit{types} instead of values: \ a stack of "
                  r"\texttt{i32}s and \texttt{i64}s", font_size=20, color=GREY_A),
            label(r"structured control flow means each block's stack shape is known: \ one pass, \ linear time",
                  font_size=20, color=GREY_A),
            label(r"so untrusted code from any web page can run at near-native speed, \ sandboxed", font_size=21,
                  color=YES),
            label(r"the specification is formal, \ and its soundness is machine-checked \ (Watt, \ 2018): \ "
                  r"Part 14's progress and preservation, \ in production", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Before a browser runs WebAssembly from a stranger's web page, it checks it. <bookmark mark='a'/> Here "
            "is a broken version of factorial: in the else branch, i64.mul has only one value to multiply. "
            "<bookmark mark='b'/> node refuses the module before running a single instruction: not enough "
            "arguments on the stack for i64.mul, need two, got one. <bookmark mark='c'/> This check is type "
            "checking. The validator runs over each function once, keeping a stack of types instead of values, "
            "and because control flow is structured it always knows the shape of the stack at every point. One "
            "pass, in linear time. <bookmark mark='d'/> That is what lets untrusted code run at nearly the speed "
            "of native code, in a sandbox. And WebAssembly's specification is formal enough that Conrad Watt "
            "checked its soundness by machine in 2018: progress and preservation, Part 14's theorems, protecting "
            "billions of browsers."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bad))
            vo.wait_until("b")
            self.play(FadeIn(err))
            vo.wait_until("c")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()

    def prolog(self):
        d = load("prolog")
        head = label(r"A machine that searches: \ Prolog", font_size=34).to_edge(UP, buff=0.3)
        prog = code(d["program"], size=20, color=CODE).next_to(head, DOWN, buff=0.5)
        q = mono("?- append(X, Y, [1, 2, 3]).", 20, WHITE).next_to(prog, DOWN, buff=0.45)
        ans = VGroup(*[mono(f"X = {a}, Y = {b}".replace("'", ""), 19, YES) for a, b in d["backwards"]]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(q, DOWN, buff=0.3)
        st = d["stats"]
        pts = VGroup(
            label(r"a program is a set of facts and rules; \ running it is a search for proofs \ (Colmerauer and "
                  r"Kowalski, \ 1972)", font_size=20, color=GREY_A),
            label(rf"our tiny Prolog: \ depth-first resolution, \ {st['unify']} unifications, \ "
                  rf"{len(d['backwards'])} answers", font_size=20, color=GREY_A),
            label(r"the same \textbf{unification} that inferred types in Part 14 \ (Robinson, \ 1965)",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Not every runtime runs functions. <bookmark mark='a'/> In Prolog, a program is a set of facts and "
            "rules. These two lines define append: the empty list followed by Ys is Ys; and X followed by Xs, "
            "followed by Ys, is X followed by Zs, if Xs followed by Ys is Zs. <bookmark mark='b'/> Running a program "
            "means asking a question. Ask which X and Y append to give one, two, three, and our small Prolog engine "
            "finds all four answers, by searching. <bookmark mark='c'/> The same two lines run forwards, to join "
            "lists, or backwards, to split them. The engine underneath is resolution with backtracking, and at its "
            "heart is unification, exactly the algorithm that inferred the Job's types in Part 14. Prolog's runtime "
            "is a unification machine, and AI, Built, Part 2, meets it as logic programming."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prog))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(q))
            self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.1) for a in ans], lag_ratio=0.4), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()

    def others(self):
        head = label(r"Other ways to run", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"\textbf{actors} \ (Hewitt, \ 1973; \ Erlang, \ 1986): \ processes that share nothing and send "
                  r"messages", font_size=21, color=DATA),
            label(r"Erlang's runtime: \ millions of tiny processes, \ each with its own heap and its own small "
                  r"collections", font_size=20, color=GREY_A),
            label(r"``let it crash'': \ a supervisor restarts what fails \ (Part 50)", font_size=20, color=GREY_A),
            label(r"\textbf{dataflow}: \ an operation runs when its inputs arrive \ --- \ spreadsheets, \ TensorFlow's "
                  r"graphs, \ Part 8's out-of-order core", font_size=21, color=LAM),
            label(r"every one is a different answer to: \ what does it mean for a program to take a step?",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Two more models deserve a mention. <bookmark mark='a'/> Actors, proposed by Carl Hewitt in 1973 and "
            "built into Erlang at Ericsson in 1986, are processes that share nothing and only send each other "
            "messages. Erlang's runtime runs millions of them, each with its own small heap, so each collects its "
            "own garbage without stopping the others. <bookmark mark='b'/> And its philosophy, let it crash, "
            "restarts failed processes from a supervisor, an idea Part 50 brings to distributed systems. <bookmark "
            "mark='c'/> In dataflow, an operation runs as soon as its inputs exist. A spreadsheet is a dataflow "
            "program, so is a TensorFlow graph, and so, inside, is Part 8's out-of-order core. <bookmark "
            "mark='d'/> Each runtime is an answer to the same question: what does it mean for a program to take a "
            "step?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[3]))
            vo.wait_until("d")
            self.play(FadeIn(pts[4]))
        self.wait(0.3)
        self.clear_scene()
