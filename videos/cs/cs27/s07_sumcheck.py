from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono,
                                   words)


def lit_tex(l):
    return rf"x_{l}" if l > 0 else rf"\bar x_{-l}"


class Sumcheck(VoiceoverScene):
    def construct(self):
        self.card()
        self.arith()
        self.rounds()
        self.cheat()
        self.ipspace()

    def card(self):
        card = chapter_card(6, r"Sum-check and IP = PSPACE", r"How can a verifier check an exponential sum?",
                            lit=(1990,), extra=((1990, r"Lund--Fortnow--Karloff--Nisan; \ Shamir"),), part=PART)
        with self.voiceover("Chapter six. Sum-check and IP equals PSPACE."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def arith(self):
        s = load("sumcheck")
        head = label(r"Arithmetization: \ formulas become polynomials", font_size=32).to_edge(UP, buff=0.35)
        f = MathTex(r" \wedge ".join("(" + r" \vee ".join(lit_tex(l) for l in c) + ")" for c in s["clauses"]),
                    font_size=30, color=HEAD).next_to(head, DOWN, buff=0.4)
        if f.width > 13:
            f.width = 13
        rules = VGroup(
            MathTex(r"\bar x \;\to\; 1 - x \qquad a \wedge b \;\to\; a \cdot b \qquad a \vee b \vee c \;\to\; "
                    r"1 - (1-a)(1-b)(1-c)", font_size=32, color=WHITE),
            MathTex(r"\#\mathrm{SAT}(\varphi) \;=\; \sum_{x \in \{0,1\}^n} P_\varphi(x)", font_size=38, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(f, DOWN, buff=0.45)
        notes = VGroup(
            label(r"on 0/1 inputs $P_\varphi$ equals the formula; \ but it is defined on any field: \ here $\mathbb{F}_{97}$",
                  font_size=21, color=WHITE),
            label(rf"degree $\le m$ = {len(s['clauses'])} in each variable \ (one factor per clause)", font_size=21,
                  color=DATA),
            label(rf"the prover claims the sum is {s['true']}: \ the number of satisfying assignments", font_size=21,
                  color=HEAD),
            label(r"a sum of $2^n$ terms: \ too many for the verifier to add up", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.2).next_to(rules, DOWN, buff=0.45)
        with self.voiceover(
            "Arithmetization converts a Boolean formula into a polynomial. <bookmark mark='a'/> Negation becomes one minus the variable; conjunction becomes multiplication; a clause becomes one minus the product of the false-literal indicators. <bookmark mark='b'/> On Boolean points this polynomial equals the formula. Summing over the Boolean cube therefore gives its satisfying-assignment count modulo the field characteristic. <bookmark mark='c'/> We use the prime field of ninety-seven elements. For this formula each variable occurs at most once per clause, so five is a valid individual-degree bound. Our implementation also handles repeated occurrences by enlarging that bound. <bookmark mark='d'/> The example has seven satisfying assignments, smaller than ninety-seven, so no ambiguity from modular counting arises. <bookmark mark='e'/> In general, a modulus larger than the possible count, or additional reconstruction information, is needed to recover the integer count. The protocol itself verifies a field-valued sum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]))
            for mk, n_ in zip("cde", [VGroup(notes[0], notes[1]), notes[2], notes[3]]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def rounds(self):
        s = load("sumcheck")
        head = label(r"One variable at a time", font_size=34).to_edge(UP, buff=0.3)
        log = [r for r in s["log"] if "round" in r]
        rows = []
        prev = s["true"]
        for r in log:
            g = r["g"]
            rows.append([str(r["round"]), ", ".join(map(str, g)), f"{g[0]} + {g[1]} = {(g[0] + g[1]) % s['p']}",
                         str(prev), str(r["r"]), str(r["next"])])
            prev = r["next"]
        tab = grid_table([r"round $i$", r"$g_i(0), \ldots, g_i(5)$", r"$g_i(0) + g_i(1)$", r"claim", r"random $r_i$",
                          r"new claim $g_i(r_i)$"], rows, widths=[1.4, 3.6, 2.4, 1.2, 1.8, 2.6], row_h=0.48,
                         font_size=19, mono_cols=(1,), colors=[[WHITE, DATA, YES, HEAD, LAM, HEAD]] * len(rows))
        tab.next_to(head, DOWN, buff=0.4).set_x(0)
        fin = s["log"][-1]
        lines = VGroup(
            label(r"$g_i(X)$ = the sum with $x_1..x_{i-1}$ fixed to the random values so far, \ $x_i = X$, \ and the "
                  r"rest summed over 0/1", font_size=20, color=WHITE),
            label(r"the verifier checks $g_i(0) + g_i(1)$ = the current claim, \ then replaces the claim by $g_i$ at "
                  r"a random point", font_size=20, color=DATA),
            label(rf"at the end one evaluation of $P_\varphi$ at the random point: \ {fin['final']} = {fin['claim']}: "
                  r"\ accepted", font_size=20, color=YES),
            label('$n$ rounds, degree-dependent field work, one final evaluation; field-valued sum',
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "The verifier reduces the claimed sum one variable at a time. <bookmark mark='a'/> In each round the prover sends a univariate polynomial as six values at distinct field points, fixing a degree-at-most-five polynomial. <bookmark mark='b'/> The values at zero and one must add to the current claim. Only after receiving the message does the verifier draw an independent uniform challenge and update the claim by interpolation. The table contains the actual retained transcript. <bookmark mark='c'/> After four rounds, the verifier evaluates the original arithmetized formula at the four challenges and compares it with the final claim. <bookmark mark='d'/> Communication and verifier arithmetic are polynomial in the number of variables, the degree bound and field-element bit length. This teaching Lagrange evaluator performs degree-dependent work; the prover still does exponential suffix summation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(VGroup(*tab.cells[1][:2])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[1][2:])), FadeIn(lines[1]))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[2:]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def cheat(self):
        s = load("sumcheck")
        head = label(r"Catching a liar", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(rf"a cheater claims {s['true'] + 1}: \ its round-1 polynomial cannot be the true one", font_size=22,
                  color=WHITE),
            label(r"two different polynomials of degree $\le d$ agree on at most $d$ points", font_size=22,
                  color=DATA),
            label(r"so the random $r_i$ hits a point where the lie becomes true \ with probability $\le d/p$",
                  font_size=22, color=HEAD),
            label(r"otherwise the lie is carried into the next round, \ and caught at the end", font_size=22,
                  color=WHITE),
            label(rf"over $\mathbb{{F}}_{{{s['p']}}}$: \ the best cheater survives {s['cheat_survive'] * 100:.1f}\% "
                  rf"of {words(s['trials'])} runs; \ the bound $1 - (1 - 5/97)^4$ is {s['bound'] * 100:.1f}\%",
                  font_size=22, color=NO),
            label(rf"over a field of about a million: \ survival 0 in 300 runs \ (bound {s['big_bound']:.0e})",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Soundness concerns every prover strategy, including adaptive ones. <bookmark mark='a'/> If the current claim is false, any polynomial that passes the sum-at-zero-and-one check must differ from the true polynomial. <bookmark mark='b'/> Two distinct polynomials of degree at most d agree at no more than d field points. <bookmark mark='c'/> Therefore, conditioned on any earlier transcript where the claim is still false, the next independent uniform challenge repairs that false claim with probability at most d divided by the field size. <bookmark mark='d'/> If no round repairs it, the final direct evaluation rejects. A union bound gives n d divided by the field size; a sequential conditional argument also gives one minus one minus d over p to the n. Independence between success events is unnecessary. <bookmark mark='e'/> Our specific cheating strategy adds a polynomial with chosen roots. Its measured frequency comes from three thousand trials, with ordinary sampling uncertainty. It is not a counterexample when a sample proportion lies above a theoretical probability bound. <bookmark mark='f'/> A larger field lowers the soundness bound. No observed success in three hundred trials remains a finite observation, not zero soundness error."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def ipspace(self):
        head = label(r"IP = PSPACE \ (Shamir, 1990)", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"sum-check puts \#SAT in IP: \ \textbf{counting} is checkable \ (Lund, \ Fortnow, \ Karloff, \ "
                  r"Nisan)", font_size=22, color=WHITE),
            label(r"Shamir: \ the same idea handles $\forall$ and $\exists$ \ ($\forall \to$ product, \ $\exists \to$ "
                  r"$1 - \prod(1 - \cdot)$), \ so TQBF $\in$ IP", font_size=22, color=DATA),
            label(r"a degree-reduction trick keeps the polynomials small through $n$ quantifiers", font_size=22,
                  color=GREY_A),
            label(r"and IP $\subseteq$ PSPACE: \ the best prover strategy can be computed in polynomial space",
                  font_size=22, color=HEAD),
            label(r"so \textbf{IP = PSPACE}: \ a polynomial-time verifier can be convinced of any PSPACE truth, \ such "
                  r"as who wins a game", font_size=22, color=YES),
            label(r"and the proof does \textbf{not} relativize: \ the first crack in Part 26's first barrier",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "This was a breakthrough. <bookmark mark='a'/> Sum-check shows that counting solutions has interactive "
            "proofs, far beyond NP. <bookmark mark='b'/> Weeks later Adi Shamir extended it to quantified formulas: "
            "a for-all becomes a product, an exists becomes one minus a product, and the same round-by-round checking "
            "works. <bookmark mark='c'/> A trick to keep the degree low makes it go through n quantifiers. <bookmark "
            "mark='d'/> In the other direction, an optimal prover can be simulated in polynomial space. <bookmark "
            "mark='e'/> So IP equals PSPACE: a polynomial-time verifier with coins can be convinced of anything "
            "provable in polynomial space, such as who wins a board game from a given position. <bookmark mark='f'/> "
            "And the proof does not relativize: there are oracles relative to which it is false. It was the first "
            "major technique to get past Part 26's first barrier."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
