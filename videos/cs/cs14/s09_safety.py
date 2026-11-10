from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, load, mono


class Safety(VoiceoverScene):
    def construct(self):
        self.card()
        self.statement()
        self.progress()
        self.preservation()
        self.checked()
        self.beyond()

    def card(self):
        card = chapter_card(8, r"Well-typed programs cannot go wrong", r"What exactly does a type promise?",
                            lit=(1978,), extra=((1978, r"Lamport's clocks; \ Milner's slogan"),), part=PART)
        with self.voiceover("Chapter eight. Well-typed programs cannot go wrong."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def statement(self):
        head = label(r"Safety \ $=$ \ progress \ $+$ \ preservation", font_size=36).to_edge(UP, buff=0.3)
        prog = VGroup(label(r"\textbf{Progress}", font_size=26, color=YES),
                      MathTex(r"\vdash t : T \;\implies\; t \text{ is a value, \ or } t \to t' \text{ for some } t'",
                              font_size=32)).arrange(DOWN, buff=0.15)
        pres = VGroup(label(r"\textbf{Preservation}", font_size=26, color=DATA),
                      MathTex(r"\vdash t : T \;\text{ and }\; t \to t' \;\implies\; \vdash t' : T", font_size=32)).arrange(
            DOWN, buff=0.15)
        VGroup(prog, pres).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.6)
        chain = MathTex(r"t_0 \to t_1 \to t_2 \to \cdots", font_size=38).next_to(pres, DOWN, buff=0.6)
        ch_l = label(r"every term along the way has type $T$ \ (preservation), \ so it is never stuck \ (progress)",
                     font_size=22, color=HEAD).next_to(chain, DOWN, buff=0.25)
        with self.voiceover("Milner's slogan is a theorem with two halves. <bookmark mark='a'/> Progress: a closed well-typed term is either a value, a finished answer, or it can take a step. It is never stuck. <bookmark mark='b'/> Preservation: if a well-typed term takes a step, the result has the same type. <bookmark mark='c'/> Put them together along any run of the program. Each term has type T, by preservation, so each one is either an answer or can step again, by progress. A well-typed program never reaches a stuck state.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(prog), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pres))
            vo.wait_until('c')
            self.play(Write(chain), FadeIn(ch_l))
        self.wait(0.3)
        self.clear_scene()

    def progress(self):
        head = label(r"Proving progress: \ induction on the derivation", font_size=34).to_edge(UP, buff=0.3)
        steps = VGroup(
            label(r"case \textsc{App}: \ \ $\vdash f : A \to B$ \ and \ $\vdash a : A$", font_size=24, color=WHITE),
            label(r"by induction, \ $f$ is a value or steps; \ if it steps, \ so does $f\,a$ \ (\textsc{E-App1})",
                  font_size=22, color=GREY_A),
            label(r"if $f$ is a value of type $A \to B$, \ it must be a $\lambda$ \ (\textit{canonical forms})",
                  font_size=22, color=GREY_A),
            label(r"then $a$ is a value or steps \ (\textsc{E-App2}); \ if a value, \ $(\lambda x.\,t)\;a$ is a "
                  r"redex \ (\textsc{E-AppAbs})", font_size=22, color=GREY_A),
            label(r"case \textsc{If}: \ the condition is a value of type $\mathsf{Bool}$, \ so \textsf{true} or "
                  r"\textsf{false}, \ or it steps", font_size=22, color=GREY_A),
            label(r"the other cases are alike: \ types say which values can appear where", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        with self.voiceover("The proofs go by induction on the typing derivation, one case per rule. Here is the interesting case of progress. <bookmark mark='a'/> The term is an application, f of a, where f has type A to B and a has type A. <bookmark mark='b'/> By induction, f is a value or can step. If it can step, so can f of a. <bookmark mark='c'/> If f is a value, then because its type is an arrow, it must be a lambda: the only values of function type are functions. This little lemma, canonical forms, is where the types do their work. <bookmark mark='d'/> Then the argument is a value or can step, and if it is a value, the whole term is a redex. <bookmark mark='e'/> For an if, the condition is either a step away or a value of type bool, which can only be true or false. In every case, the types say which values can appear in which positions, and no stuck combination survives.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, s in zip('abcde', steps[:5]):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            self.play(FadeIn(steps[5]))
        self.wait(0.3)
        self.clear_scene()

    def preservation(self):
        head = label(r"Proving preservation: \ the substitution lemma", font_size=34).to_edge(UP, buff=0.3)
        lem = MathTex(r"\Gamma,\, x{:}A \vdash t : B \quad\text{and}\quad \Gamma \vdash s : A \;\implies\; \Gamma \vdash "
                      r"t[x := s] : B", font_size=34, color=HEAD).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"the only step that changes much is \textsc{E-AppAbs}: \ $(\lambda x{:}A.\, t)\; s \to t[x := s]$",
                  font_size=22, color=GREY_A),
            label(r"typing the redex gave: \ $x{:}A \vdash t : B$, \ and $s : A$", font_size=22, color=GREY_A),
            label(r"the lemma: \ putting an $A$ where an $A$ was assumed keeps the type $B$", font_size=22,
                  color=YES),
            label(r"proved itself by induction on $t$'s derivation", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.25).next_to(lem, DOWN, buff=0.6)
        with self.voiceover(
            "Preservation rests on one lemma. <bookmark mark='a'/> The only step that changes a term's shape much "
            "is beta reduction, which substitutes an argument for a parameter. <bookmark mark='b'/> When we typed "
            "the redex, we typed the body t assuming x is an A, and we typed the argument s as an A. <bookmark "
            "mark='c'/> The substitution lemma says that putting a real A where an A was assumed leaves the "
            "body's type unchanged. It is proved, in turn, by induction on the derivation of t. With it, "
            "preservation follows case by case."
        ) as vo:
            self.play(FadeIn(head), Write(lem))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()

    def checked(self):
        s = load("safety")
        head = label(r"Both theorems, \ checked on random programs", font_size=34).to_edge(UP, buff=0.3)
        h = s["hist"]
        vals = [c for k, c in h if k >= 1]
        names = [str(k) if k % 10 == 0 else " " for k, c in h if k >= 1]
        ch = bar_chart(vals, names, [DATA] * len(vals), height=2.8, bar_w=0.12, gap=0.03, fmt_=lambda v: " ",
                       font_size=16)
        ch.remove(ch.vals)
        ch.move_to(LEFT * 3.3 + DOWN * 0.4)
        zero = label(rf"(plus {h[0][1]:,} terms that were values already: \ 0 steps)", font_size=16,
                     color=GREY_B).next_to(ch, UP, buff=0.3)
        ch.add(zero)
        xl = label(r"steps to finish", font_size=17, color=GREY_B).next_to(ch, DOWN, buff=0.4)
        side = VGroup(
            label(rf"{s['terms']:,} random closed well-typed terms", font_size=22, color=WHITE),
            label(rf"{s['steps_checked']:,} steps: \ after each one, \ the type re-checked", font_size=22,
                  color=DATA),
            label(r"never stuck; \ type never changed", font_size=24, color=YES),
            label(rf"every one finished: \ at most {s['max_steps']} steps", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)
        note = label("finite regression samples support an implementation check; the theorem needs a proof", font_size=19,
                     color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover("Finite checks exercise the implementation of the safety rules. <bookmark mark='a'/> The generator constructs five thousand closed, well-typed terms from its stated grammar and seed. <bookmark mark='b'/> In the recorded run, all finish after fifty thousand five hundred and sixteen small steps in total, with typing checked after every step. <bookmark mark='c'/> No sampled state is stuck and no step changes its type. A failed case would expose a bug in the generator, checker or evaluator; passing this sample is not a proof of the general theorems. <bookmark mark='d'/> The longest sampled run takes forty-seven steps. That bound belongs only to these generated terms. The next chapter's normalization theorem explains why every term in the recursion-free typed calculus terminates, without giving this particular sample bound to all programs.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(side[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(side[1]), FadeIn(ch), FadeIn(xl))
            vo.wait_until('c')
            self.play(FadeIn(side[2]))
            vo.wait_until('d')
            self.play(FadeIn(side[3]), FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def beyond(self):
        head = label(r"Safety, \ in real languages", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            label(r"Standard ML: \ a formal definition \ (Milner, Tofte, Harper, \ 1990), \ its safety later machine-"
                  r"checked", font_size=21, color=GREY_A),
            label("Java and C\\#: managed type safety relies on the runtime and native-code boundary", font_size=21,
                  color=GREY_A),
            label("RustBelt: a verified Rust subset, with obligations for unsafe libraries (2018)", font_size=21, color=GREY_A),
            label(r"C and C++: \ not safe: \ a well-typed program can still write past an array \ (Part 11)",
                  font_size=21, color=NO),
            label(r"``cannot go wrong'' means: \ never stuck. \ It does not mean: \ terminates, \ or is correct",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=0.7)
        with self.voiceover(
            (
            "Safety results belong to a language and its operational model. <bookmark mark='a'/> Standard ML has "
            "a formal definition and machine-checked metatheoretic work; the precise theorem depends on the "
            "modeled features. <bookmark mark='b'/> Managed Java and C sharp designs enforce important safety "
            "properties, and the JVM verifies bytecode. Native interfaces, unsafe facilities and implementation "
            "defects lie outside a simple blanket claim. <bookmark mark='c'/> RustBelt's 2018 work proves "
            "soundness for a realistic Rust subset and verifies selected unsafe library abstractions against "
            "explicit contracts. It is not a proof of every Rust feature, library or compiler version. Safe "
            "clients rely on those contracts being upheld. <bookmark mark='d'/> C and C plus plus permit "
            "well-typed programs with out-of-bounds accesses and other undefined behavior. Their static types do "
            "not establish this lesson's safety guarantee. <bookmark mark='e'/> In our calculus, cannot go wrong "
            "means no reachable stuck term. It does not establish termination, intended answers or the absence of "
            "every operational failure in a production system."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
