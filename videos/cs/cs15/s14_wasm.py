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
        control=VGroup()
        block=RoundedRectangle(width=2.2,height=1.7,corner_radius=.1,color=DATA).move_to([2,.5,0])
        loop=RoundedRectangle(width=2.2,height=1.7,corner_radius=.1,color=YES).move_to([5,.5,0])
        control.add(block,loop,label('block',font_size=23,color=DATA).next_to(block,UP,buff=.12),
                    label('loop',font_size=23,color=YES).next_to(loop,UP,buff=.12))
        control.add(Arrow(block.get_center()+UP*.2,block.get_bottom()+DOWN*.4,buff=0,color=DATA,tip_length=.13),
                    Arrow(loop.get_bottom()+UP*.2,loop.get_top()-UP*.2,buff=0,color=YES,tip_length=.13))
        control.add(label('exit',font_size=19,color=DATA).next_to(block,DOWN,buff=.45),
                    label('restart at header',font_size=19,color=YES).next_to(loop,DOWN,buff=.45))
        pts = VGroup(
            label(r"a stack machine like ours, \ with types: \ \texttt{i32}, \ \texttt{i64}, \ \texttt{f32}, \ "
                  r"\texttt{f64}", font_size=20, color=GREY_A),
            label('branch to block: exit; branch to loop: restart at the header',
                  font_size=20, color=GREY_A),
            label(r"in every major browser since 2017 \ (Haas et al., \ 2017)", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "WebAssembly is a typed virtual instruction set supported by major browsers. <bookmark mark='a'/> Our "
            "factorial uses a value stack: local.get pushes an argument and i64.mul consumes two integers. "
            "<bookmark mark='b'/> We assembled this module by hand and ran it in Node; the table shows the exact "
            "factorial-of-twenty result. Arithmetic uses WebAssembly's specified fixed-width rules. <bookmark "
            "mark='c'/> Control transfers target enclosing labels. For a block, branching exits at its end; for a "
            "loop, branching returns to its beginning. The two arrows show that essential difference. Structured "
            "control and declared types support validation, but a sandbox also relies on runtime bounds checks "
            "and the capabilities supplied through host imports."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(wat))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(hx), FadeIn(run))
            vo.wait_until("c")
            self.play(FadeOut(right),FadeIn(control),FadeIn(pts[1:]))
        self.wait(0.3)
        self.clear_scene()

    def validate(self):
        d = load("wasm")
        head = label(r"Validation is type checking", font_size=34).to_edge(UP, buff=0.3)
        bad = code(d["bad_wat"], size=18, color=CODE).next_to(head, DOWN, buff=0.5)
        if bad.width>7.0:bad.scale_to_fit_width(7.0)
        bad.to_edge(LEFT,buff=.65)
        err = VGroup(label(r"node, \ before running a single instruction:", font_size=19, color=GREY_B),
                     code(textwrap.wrap(d["error"], 64), size=15, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(bad, DOWN, buff=0.45)
        if err.width>12.7:err.scale_to_fit_width(12.7)
        err.set_x(0)
        def typed_cell(text,color):
            r=Rectangle(width=1.0,height=.42,color=color,fill_color=color,fill_opacity=.12)
            return VGroup(r,mono(text,17,color).move_to(r))
        stack=VGroup(
            label('expected before i64.mul',font_size=18,color=YES),
            VGroup(typed_cell('i64',YES),typed_cell('i64',YES)).arrange(RIGHT,buff=.12),
            label('actual operand types',font_size=18,color=NO),
            VGroup(typed_cell('i64',DATA),typed_cell('?',NO)).arrange(RIGHT,buff=.12),
        ).arrange(DOWN,buff=.12).move_to([3.8,bad.get_center()[1],0])
        pts = VGroup(
            label(r"the validator runs each function once, \ on \textit{types} instead of values: \ a stack of "
                  r"\texttt{i32}s and \texttt{i64}s", font_size=20, color=GREY_A),
            label(r"structured control flow means each block's stack shape is known: \ one pass, \ linear time",
                  font_size=20, color=GREY_A),
            label('isolation also needs runtime bounds checks and a host-import policy', font_size=21,
                  color=YES),
            label('Watt (2018): mechanized specification/checker/interpreter; not all browser engines', font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover("Validation rejects malformed typed code before execution. <bookmark mark='a'/> The broken factorial reaches i64.mul with only one operand. <bookmark mark='b'/> Node's validator rejects it; the diagnostic shown here is the actual output of this installed version. <bookmark mark='c'/> The validator tracks operand types and control contexts, checking branch signatures and each instruction's stack effect. Structured code supports a linear pass under the validation model. <bookmark mark='d'/> Conrad Watt's 2018 work mechanized a specification, checker and interpreter in Isabelle, finding and correcting specification issues. That is a specification-level soundness result, not a proof of every browser's optimizing engine. Validation, runtime memory checks and host policy each contribute to isolation.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(bad), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(err))
            vo.wait_until('c')
            self.play(FadeIn(stack), FadeIn(pts[:2]))
            vo.wait_until('d')
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
            label('related unification ideas; details such as occurs checks depend on the engine',
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            "A runtime can search rather than just execute a function. <bookmark mark='a'/> These Prolog rules "
            "define append through the relationship among two input lists and their concatenation. <bookmark "
            "mark='b'/> Ask which X and Y concatenate to one, two, three. Our small engine searches and finds all "
            "four displayed splits. <bookmark mark='c'/> Resolution and backtracking explore alternatives, while "
            "unification matches terms and propagates variable bindings. Type inference also uses unification, "
            "but concrete algorithms differ: occurs checks, cyclic terms and type constructors need their own "
            "rules. The common idea connects logic programming with the type checker without making the two "
            "implementations identical."
        )
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
        with self.voiceover("Two more models deserve a mention. <bookmark mark='a'/> Actors, proposed by Carl Hewitt in 1973 and built into Erlang at Ericsson in 1986, are processes that share nothing and only send each other messages. Erlang's runtime runs millions of them, each with its own small heap, so each collects its own garbage without stopping the others. <bookmark mark='b'/> And its philosophy, let it crash, restarts failed processes from a supervisor, an idea Part 50 brings to distributed systems. <bookmark mark='c'/> In dataflow, an operation runs as soon as its inputs exist. A spreadsheet is a dataflow program, so is a TensorFlow graph, and so, inside, is Part 8's out-of-order core. <bookmark mark='d'/> Each runtime is an answer to the same question: what does it mean for a program to take a step?") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pts[:2]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[2]))
            vo.wait_until('c')
            self.play(FadeIn(pts[3]))
            vo.wait_until('d')
            self.play(FadeIn(pts[4]))
        self.wait(0.3)
        self.clear_scene()
