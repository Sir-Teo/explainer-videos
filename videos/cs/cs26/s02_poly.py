from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, sci)


def dur(s):
    """A duration in seconds as words."""
    if s < 1e-3:
        return rf"{s * 1e6:.0f} $\mu$s"
    if s < 1:
        return rf"{s * 1e3:.0f} ms"
    if s < 60:
        return rf"{s:.1f} s"
    if s < 3600:
        return rf"{s / 60:.0f} min"
    if s < 86400 * 365.25:
        return rf"{s / 86400:.0f} days"
    y = s / (86400 * 365.25)
    if y < 1e4:
        return rf"{y:,.0f} years"
    return rf"${sci(y, 1)}$ years"


class Polynomial(VoiceoverScene):
    def construct(self):
        self.card()
        self.table()
        self.robust()

    def card(self):
        card = chapter_card(1, r"What counts as efficient", r"Why polynomial time?", lit=(1965,),
                            extra=((1965, r"Edmonds; \ Cobham"),), part=PART)
        with self.voiceover("Chapter one. What counts as efficient."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def table(self):
        g = load("growth")
        head = label(r"One step per microsecond", font_size=34).to_edge(UP, buff=0.35)
        rows = [[str(r["n"]), dur(r["n2"]), dur(r["n3"]), dur(r["2n"]), dur(r["fact"])] for r in g["rows"]]
        tab = grid_table([r"$n$", r"$n^2$", r"$n^3$", r"$2^n$", r"$n!$"], rows, widths=[1.2, 2.0, 2.0, 3.4, 3.4],
                         row_h=0.46, font_size=20, mono_cols=(),
                         colors=[[WHITE, YES, YES, NO, NO]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        age = g["age_universe_s"] / (86400 * 365.25)
        notes = VGroup(
            label(rf"the universe is about ${sci(age, 2)}$ years old", font_size=22, color=GREY_A),
            label('at fixed step cost: $1{,}000\\times$ speed gives $\\sqrt{1000}\\approx31.6\\times$ size for $n^2$; about 10 more for $2^n$', font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Suppose a computer takes a microsecond per step. <bookmark mark='a'/> An algorithm taking n squared "
            "steps handles a hundred items in ten milliseconds. N cubed takes a second. <bookmark mark='b'/> Two to "
            "the n is fine at twenty and hopeless at sixty: thirty-six thousand years. At a hundred, it is "
            "four times ten to the sixteen years. And n factorial at sixty is beyond any number of universes. "
            "<bookmark mark='c'/> The universe is fourteen billion years old. <bookmark mark='d'/> Faster hardware "
            "does not rescue exponential algorithms. A computer a thousand times faster lets an n squared algorithm "
            "handle inputs thirty-one times larger, but a two to the n algorithm only ten items more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(*[r[c] for r in tab.cells[1:]])) for c in (0, 1, 2)])
            vo.wait_until("b")
            self.play(*[FadeIn(VGroup(*[r[c] for r in tab.cells[1:]])) for c in (3, 4)])
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def robust(self):
        head = label(r"P: \ decidable in time $O(n^k)$ for some $k$", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"Edmonds \ (1965): \ a ``good'' algorithm is one that runs in polynomial time \ (his "
                  r"blossom algorithm for matching)", font_size=22, color=WHITE),
            label('Cobham (1965): polynomial equivalence of standard, appropriately costed machine models', font_size=22, color=WHITE),
            label('multitape to one tape: polynomial overhead; \\ RAM words and arithmetic require bit-cost bounds', font_size=22, color=DATA),
            label(r"polynomials compose: \ a polynomial algorithm calling a polynomial subroutine is polynomial",
                  font_size=22, color=DATA),
            label('extended Church--Turing thesis: efficient probabilistic classical simulation of physical computation', font_size=22, color=LAM),
            label('asymptotic polynomial time need not be practical: exponents, constants and input sizes matter', font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Polynomial time is a useful mathematical boundary. <bookmark mark='a'/> Edmonds's 1965 matching work helped establish this viewpoint. <bookmark mark='b'/> Cobham studied its independence from standard machine details. <bookmark mark='c'/> Deterministic multitape Turing machines and appropriately costed RAM models simulate one another with polynomial overhead. Unbounded integer arithmetic at unit cost would require a different analysis. <bookmark mark='d'/> Polynomially many calls to polynomial-time subroutines still take polynomial time, including the cost of writing their inputs. <bookmark mark='e'/> The extended Church-Turing thesis is a broader physical claim, commonly phrased using efficient probabilistic classical simulation. Quantum computation challenges that claim; it is not a theorem equating every model with P. <bookmark mark='f'/> Asymptotic membership also does not promise practical speed: large exponents and constants matter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
