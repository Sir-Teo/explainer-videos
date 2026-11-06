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
            "In 1990 Carsten Lund, Lance Fortnow, Howard Karloff and Noam Nisan found the key idea: turn logic into "
            "algebra. <bookmark mark='a'/> Not x becomes one minus x; and becomes multiplication; an OR of three "
            "literals becomes one minus the product of their negations. <bookmark mark='b'/> On zeros and ones this "
            "polynomial agrees with the formula, so the number of satisfying assignments is the sum of the "
            "polynomial over the Boolean cube. <bookmark mark='c'/> But the polynomial is also defined at any point of "
            "a finite field; we use the integers modulo ninety-seven. Its degree in each variable is at most the "
            "number of clauses, five. <bookmark mark='d'/> The prover claims the sum is seven. <bookmark mark='e'/> "
            "The verifier cannot add up two to the n terms. Here is how it checks anyway."
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
            label(r"the verifier did $n$ rounds of a few field operations, \ plus one evaluation, \ instead of $2^n$",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "The protocol peels off one variable per round. <bookmark mark='a'/> In round one the prover sends a "
            "polynomial in a single variable: the sum with x one left free and everything else summed over zero and "
            "one. It sends it as six values, enough to pin down a polynomial of degree five. <bookmark mark='b'/> "
            "The verifier checks that its values at zero and one add up to the claim, seven, then picks a random "
            "field element, thirty, and the claim becomes the polynomial's value there: thirty-three. Round two does "
            "the same with x one fixed at thirty, and so on. <bookmark mark='c'/> After the last round the verifier "
            "evaluates the arithmetized formula once, at the four random values, and gets ninety-one, exactly the "
            "final claim. Accept. <bookmark mark='d'/> The verifier did a few field operations per round and a single "
            "evaluation, instead of adding up two to the n terms."
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
            "What if the prover lies? <bookmark mark='a'/> Say it claims eight. Its first polynomial must add up to "
            "eight at zero and one, so it is not the true polynomial. <bookmark mark='b'/> Two different polynomials "
            "of degree d agree on at most d points. <bookmark mark='c'/> So the only hope is that the verifier's random "
            "point happens to be one where the false polynomial and the true one agree; then the lie disappears. "
            "That happens with probability at most d over p. <bookmark mark='d'/> Otherwise the false claim moves "
            "into the next round, and if it survives every round, the final evaluation exposes it. <bookmark "
            "mark='e'/> We built the best possible cheater, one whose false polynomial agrees with the true one at "
            "as many points as it can. Modulo ninety-seven, it survived nineteen point three percent of three thousand "
            "runs, against a bound of nineteen point one. <bookmark mark='f'/> With a field of a million elements, it "
            "never survived."
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
