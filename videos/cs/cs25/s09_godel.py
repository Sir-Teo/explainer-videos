from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono)


class Godel(VoiceoverScene):
    def construct(self):
        self.card()
        self.numbering()
        self.halting()
        self.sentence()
        self.second()

    def card(self):
        card = chapter_card(8, r"G\"odel, through halting", r"Can a theory prove every true statement about "
                            r"programs?", lit=(1931, 1936), extra=((1931, r"G\"odel"), (1936, r"Turing")), part=PART)
        with self.voiceover("Chapter eight. Gödel, through halting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def numbering(self):
        g = load("godel")
        head = label(r"Statements are numbers", font_size=34).to_edge(UP, buff=0.35)
        syms = list(g["codes"].items())
        sym_tex = {"¬": r"$\neg$", "∀": r"$\forall$", "→": r"$\to$", "=": r"$=$", "+": r"$+$"}
        tab = grid_table([r"symbol"] + [sym_tex.get(k, rf"\texttt{{{k}}}") for k, _ in syms],
                         [[r"code"] + [str(v) for _, v in syms]], widths=[1.3] + [0.75] * len(syms), row_h=0.42,
                         font_size=20, mono_cols=(), colors=[[GREY_A] + [HEAD] * len(syms)])
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        rows = []
        for r in g["rows"]:
            f = r["formula"].replace("∀", r"\forall ").replace("=", " = ")
            pw = r" \cdot ".join(rf"{p}^{{{e}}}" for p, e in zip([2, 3, 5, 7, 11, 13, 17, 19, 23], r["codes"]))
            rows.append((MathTex(f, font_size=30, color=WHITE), MathTex(pw, font_size=26, color=DATA),
                         r["number"], r["digits"]))
        lines = VGroup()
        for f, pw, num, dg in rows:
            n_ = mono(num if len(num) < 30 else num[:26] + "...", 20, YES)
            dl = label(rf"({dg} digits)", font_size=18, color=GREY_A)
            line = VGroup(f, MathTex(r"\mapsto", font_size=30), pw, MathTex("=", font_size=30), n_, dl).arrange(
                RIGHT, buff=0.2)
            lines.add(line)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(tab, DOWN, buff=0.5)
        if lines.width > 13.2:
            lines.width = 13.2
        lines.set_x(0)
        notes = VGroup(
            label(r"factoring recovers the formula: \ the $k$-th prime's exponent is the $k$-th symbol", font_size=21,
                  color=WHITE),
            label(r"so ``$n$ is a proof of $m$'' \ is a property of two numbers, \ checkable by a program", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1931 Kurt Gödel needed arithmetic to talk about itself. <bookmark mark='a'/> Give every symbol a "
            "code number. <bookmark mark='b'/> Then encode a formula as a product of prime powers: two to the code "
            "of the first symbol, times three to the code of the second, and so on. Zero equals zero is two times "
            "twenty-seven times five: two hundred and seventy. A short statement that adding zero changes nothing "
            "has forty-seven digits. <bookmark mark='c'/> Factoring recovers the formula, so nothing is lost. "
            "<bookmark mark='d'/> A proof is a list of formulas, so it has a number too, and whether one number is "
            "a proof of another is a mechanical check. Part 1 did the same for machines, with description strings. "
            "Gödel did it first, for logic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(ln, shift=RIGHT * 0.15) for ln in lines], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def halting(self):
        head = label(r"Incompleteness from the halting problem", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"a \textbf{theory} $T$: \ axioms plus rules, \ so a program can list every theorem", font_size=22,
                  color=WHITE),
            label(r"\textbf{sound}: \ everything $T$ proves is true; \ and $T$ can state ``$M$ halts on $w$''",
                  font_size=22, color=WHITE),
            label(r"\textbf{suppose} $T$ proves every true statement ``$M$ does not halt on $w$''", font_size=22,
                  color=HEAD),
            label(r"then decide halting: \ run $M$ on $w$, \ and \textbf{at the same time} search $T$'s theorems "
                  r"for ``$M$ does not halt''", font_size=22, color=DATA),
            label(r"one of the two must finish, \ and soundness makes its answer right", font_size=22, color=DATA),
            label(r"impossible: \ so some \textbf{true} statement ``$M$ does not halt on $w$'' \ has no proof in $T$",
                  font_size=23, color=NO),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        box_ = SurroundingRectangle(lines[-1], color=NO, buff=0.15)
        with self.voiceover(
            "Here is Gödel's first theorem, proved from Part 1's result in a minute. <bookmark mark='a'/> A theory "
            "is a set of axioms and rules of proof, mechanical enough that a program can list all its theorems. "
            "<bookmark mark='b'/> Suppose it is sound, proving only true things, and strong enough to state that a "
            "machine halts on an input. Ordinary arithmetic is. <bookmark mark='c'/> Now suppose it could prove "
            "every true statement of the form, machine M does not halt on w. <bookmark mark='d'/> Then we could "
            "decide halting. Run M on w, and at the same time list the theorems, looking for M does not halt. "
            "<bookmark mark='e'/> If M halts, the run finishes. If it does not, the proof turns up. Either way we "
            "get an answer, and soundness makes it correct. <bookmark mark='f'/> That cannot be. So there are true "
            "statements, that some machine runs forever, which the theory cannot prove. Every sound theory of "
            "arithmetic is incomplete."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
            self.play(Create(box_))
        self.wait(0.3)
        self.clear_scene()

    def sentence(self):
        head = label(r"Which statement? \ Write the program", font_size=32).to_edge(UP, buff=0.35)
        code_lines = [
            "def R():",
            "    me = my_own_source()            # chapter 4",
            "    for proof in all_proofs_of(T):  # in order of length",
            "        if proof.shows(f'{me} never halts'):",
            "            return                  # halt",
        ]
        prog = VGroup(*[mono(ln, 21, LAM) for ln in code_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        prog.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=1.0)
        frame = SurroundingRectangle(prog, color=LAM, buff=0.2, corner_radius=0.08)
        lines = VGroup(
            label(r"if $T$ proved ``$R$ never halts'', \ $R$ would find that proof and \textbf{halt}: \ $T$ would "
                  r"have proved a falsehood", font_size=22, color=NO),
            label(r"so a sound $T$ never proves it, \ so $R$ searches forever, \ so ``$R$ never halts'' is "
                  r"\textbf{true}", font_size=22, color=YES),
            label(r"``$R$ never halts'' \ says, \ in effect, \ ``I am not provable in $T$'': \ G\"odel's sentence",
                  font_size=22, color=HEAD),
            label(r"G\"odel needed only consistency, \ not soundness, \ with Rosser's refinement \ (1936)",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(frame, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "The proof says some such statement exists. The recursion theorem lets us write it down. <bookmark "
            "mark='a'/> Program R obtains its own source, the trick of chapter four, and then searches through "
            "every proof in the theory, shortest first, for a proof that R never halts. If it finds one, it stops. "
            "<bookmark mark='b'/> If the theory proved that R never halts, R would find the proof and halt, and the "
            "theory would have proved something false. <bookmark mark='c'/> So a sound theory never proves it, R "
            "searches forever, and the statement R never halts is true, and unprovable. <bookmark mark='d'/> It "
            "says, in effect, I cannot be proved: Gödel's sentence, as a program. <bookmark mark='e'/> Gödel's own "
            "version needed less: only that the theory be consistent, with a refinement by Barkley Rosser in 1936."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(frame), LaggedStart(*[FadeIn(x) for x in prog], lag_ratio=0.25))
            for mk, ln in zip("bcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def second(self):
        head = label(r"The second theorem, \ and the end of Hilbert's program", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"$T$ can follow the argument just given: \ $T$ proves \ ``if $T$ is consistent, \ $R$ never halts''",
                  font_size=22, color=WHITE),
            label(r"so if $T$ proved its own consistency, \ it would prove ``$R$ never halts'', \ which it cannot",
                  font_size=22, color=DATA),
            label(r"\textbf{second incompleteness theorem}: \ a consistent theory that can do arithmetic \ "
                  r"\textbf{cannot prove its own consistency}", font_size=22, color=NO),
            label(r"Hilbert \ (1920s): \ prove mathematics consistent by finite, \ mechanical means. \ G\"odel "
                  r"\ (1931): \ impossible", font_size=22, color=HEAD),
            label(r"ZFC's consistency is a $\Pi_1$ statement: \ ``this proof-searching program never halts''",
                  font_size=22, color=LAM),
            label(r"that is why a busy beaver's value can be unprovable \ (Part 1; \ chapter 12)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Push one step further. <bookmark mark='a'/> The argument we just gave can itself be carried out "
            "inside the theory. The theory can prove: if I am consistent, then R never halts. <bookmark mark='b'/> "
            "So if it could also prove its own consistency, it would prove that R never halts, which we just saw it "
            "cannot do. <bookmark mark='c'/> That is the second incompleteness theorem: no consistent theory strong "
            "enough for arithmetic proves its own consistency. <bookmark mark='d'/> It ended the program David "
            "Hilbert had led in the 1920s, to prove all of mathematics consistent by finite, mechanical means. "
            "<bookmark mark='e'/> Notice the shape of the statement. The consistency of set theory says that one "
            "program, the one hunting for a contradiction, never halts. <bookmark mark='f'/> And that is why Part 1 "
            "could build a Turing machine whose busy-beaver value set theory cannot determine. Chapter twelve "
            "comes back to it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
