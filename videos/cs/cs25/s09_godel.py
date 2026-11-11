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
            label('an EFFECTIVELY axiomatized arithmetic theory $T$: a program enumerates every theorem', font_size=22,
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
            "An effective sound arithmetic theory cannot prove every true nonhalting statement. <bookmark mark='a'/> Effective means its theorems can be enumerated by a program. <bookmark mark='b'/> Assume soundness and enough arithmetic to express the machine computations and verify finite halting witnesses. <bookmark mark='c'/> Suppose every true nonhalting assertion had a proof. <bookmark mark='d'/> Dovetail the actual run of M on w with theorem enumeration seeking the assertion that it never halts. <bookmark mark='e'/> If it halts, the simulation finishes; otherwise the assumed proof appears. Soundness prevents a false answer. <bookmark mark='f'/> This would decide halting, so the theory is incomplete. Effective axiomatization is essential: the set of all true arithmetic statements is not a counterexample to this scoped theorem."
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
            label('Rosser (1936): consistency suffices for his modified sentence; usual effective arithmetic hypotheses',
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.28).next_to(frame, DOWN, buff=0.45).set_x(0)
        with self.voiceover(
            "Self-reference identifies a particular missing statement. <bookmark mark='a'/> Construct R with its own description embedded, and enumerate T's proofs searching for a proof that R never halts. Finding one makes R halt. <bookmark mark='b'/> If T proved nonhalting, R would halt, contradicting soundness. <bookmark mark='c'/> Thus R actually runs forever and its nonhalting is true but unprovable in this effective sound T. <bookmark mark='d'/> This is a program version of the Gödel self-reference idea. <bookmark mark='e'/> The exact historical assumptions differ: Gödel used consistency for unprovability and a stronger omega-consistency assumption for the opposite direction. Rosser's modified sentence obtains incompleteness from consistency alone, with the usual effective arithmetic hypotheses."
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
            label('standard provability predicate and derivability conditions let $T$ internalize the suitable G\\"odel argument',
                  font_size=22, color=WHITE),
            label(r"so if $T$ proved its own consistency, \ it would prove ``$R$ never halts'', \ which it cannot",
                  font_size=22, color=DATA),
            label('\\textbf{second incompleteness}: consistent, effective, sufficiently strong $T$ cannot prove standard Con($T$)', font_size=22, color=NO),
            label('Hilbert: blocked when proposed finitistic consistency reasoning is formalizable inside $T$', font_size=22, color=HEAD),
            label(r"ZFC's consistency is a $\Pi_1$ statement: \ ``this proof-searching program never halts''",
                  font_size=22, color=LAM),
            label(r"that is why a busy beaver's value can be unprovable \ (Part 1; \ chapter 12)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The second theorem needs a formal internal proof argument. <bookmark mark='a'/> Use an effective arithmetic theory with its standard provability predicate and the Hilbert-Bernays-Loeb derivability conditions. The suitable Gödel argument can then be formalized inside T. <bookmark mark='b'/> Internalized consistency implies the relevant Gödel sentence; proving consistency would therefore contradict the first theorem. <bookmark mark='c'/> A consistent sufficiently strong such T cannot prove its own standard consistency assertion. This does not follow just by repeating our informal soundness argument. <bookmark mark='d'/> It obstructs Hilbert's desired consistency proof when the proposed finitistic reasoning is formalizable within T; it does not prohibit every external consistency proof. <bookmark mark='e'/> For ZFC, standard consistency says that no encoded proof of contradiction exists. <bookmark mark='f'/> The corresponding proof-search machine connects the theorem to busy beavers, subject to the same effective arithmetic assumptions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
