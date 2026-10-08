from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import label, load, note, polyline, region


class DirichletL(VoiceoverScene):
    def construct(self):
        self.race()
        self.characters()
        self.ghost()
        self.consequences()

    # ------------------------------------------------------------------
    def race(self):
        r = load("race")
        p, lead = r["p_head"], r["lead_head"]
        first = int(r["first_flip"][0])
        primes = load("primes")["primes"]
        small = [int(q) for q in primes[1:24]]
        row1 = VGroup(*[MathTex(str(q), font_size=30, color=C.PRIME) for q in small if q % 4 == 1]).arrange(RIGHT, buff=0.3)
        row3 = VGroup(*[MathTex(str(q), font_size=30, color=C.CHARACTER) for q in small if q % 4 == 3]).arrange(RIGHT, buff=0.3)
        l1 = MathTex(r"p \equiv 1 \pmod 4:", font_size=32, color=C.PRIME)
        l3 = MathTex(r"p \equiv 3 \pmod 4:", font_size=32, color=C.CHARACTER)
        g1 = VGroup(l1, row1).arrange(RIGHT, buff=0.4)
        g3 = VGroup(l3, row3).arrange(RIGHT, buff=0.4)
        rows = VGroup(g1, g3).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.5)

        ax = Axes(x_range=[0, 100_000, 20_000], y_range=[-20, 100, 20], x_length=11, y_length=3.9, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 20}).move_to(DOWN * 1.5)
        curve = polyline(ax, p, lead, color=C.CHARACTER, stroke_width=2)
        yl = label(r"(primes $\equiv 3$) $-$ (primes $\equiv 1$) \ up to $x$", font_size=26).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        flip = Dot(ax.c2p(first, -1), radius=0.07, color=C.PRIME)
        flip_l = label(rf"first lead change: $x = {first:,}$".replace(",", "{,}"), font_size=26, color=C.PRIME)
        flip_l.move_to(ax.c2p(first + 22_000, 82))
        flip_a = Arrow(flip_l.get_bottom(), flip.get_center(), buff=0.12, color=C.PRIME, stroke_width=2.5)
        n1, n3 = int(r["n1"][0]), int(r["n3"][0])

        with self.voiceover(
            "Riemann's zeta is just the first of an infinite family. <bookmark mark='s'/> Sort the odd primes by their remainder "
            "when divided by four. <bookmark mark='a'/> Some are one more than a multiple of four, others one less. In the long "
            "run, each class gets half of the primes. Up to ten million, it's 332,180 against 332,398."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeIn(l1), FadeIn(l3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in row1], lag_ratio=0.1), LaggedStart(*[FadeIn(m) for m in row3], lag_ratio=0.1))
        assert (n1, n3) == (332_180, 332_398)
        with self.voiceover(
            "But it's a race, and the three team leads almost all the time. <bookmark mark='f'/> It falls behind for the first "
            "time at 26,861. Chebyshev noticed this bias in 1853, and to understand races like this one, you need more than "
            "zeta."
        ) as vo:
            self.play(Create(ax), FadeIn(yl))
            self.play(Create(curve), run_time=2.5, rate_func=linear)
            vo.wait_until("f")
            self.play(FadeIn(flip, scale=2), FadeIn(flip_l), GrowArrow(flip_a))
        self.clear_scene()

    # ------------------------------------------------------------------
    def characters(self):
        vals = [1, 0, -1, 0] * 3
        cols = {1: C.PRIME, -1: C.CHARACTER, 0: GREY_D}
        cells = VGroup()
        for n, v in zip(range(1, 13), vals):
            sq = Square(0.62, stroke_width=1.5, stroke_color=GREY_B, fill_color=cols[v], fill_opacity=0.35 if v else 0.2)
            cells.add(VGroup(sq, MathTex(str(n), font_size=26).move_to(sq.get_top() + DOWN * 0.17),
                             MathTex(f"{v:+d}" if v else "0", font_size=28, color=cols[v] if v else GREY_B).move_to(sq.get_bottom() + UP * 0.2)))
        cells.arrange(RIGHT, buff=0.06).to_edge(UP, buff=1.0)
        chi = MathTex(r"\chi_4(n)", font_size=36, color=C.CHARACTER).next_to(cells, LEFT, buff=0.3)
        L = MathTex(r"L(s, \chi_4)", r"=", r"1 - \frac{1}{3^s} + \frac{1}{5^s} - \frac{1}{7^s} + \frac{1}{9^s} - \cdots", r"=",
                    r"\prod_p \frac{1}{1 - \chi_4(p)\, p^{-s}}", font_size=40).next_to(cells, DOWN, buff=0.7)
        L[0].set_color(C.CHARACTER)
        L[4].set_color(C.PRIME)
        leib = note(r"(at $s = 1$: \ $1 - \tfrac13 + \tfrac15 - \cdots = \pi/4$)", font_size=26).next_to(L, DOWN, buff=0.25)
        gen = VGroup(
            label(r"one $L$-function for every modulus $q$ and every character $\chi$ mod $q$ \ (Dirichlet, 1837)", font_size=28),
            label(r"their zeros control how primes split among the remainders mod $q$", font_size=28),
            label(r"\textbf{Generalized Riemann hypothesis:}\\all their nontrivial zeros have real part $\tfrac12$", font_size=30, color=C.ZERO),
        ).arrange(DOWN, buff=0.3).next_to(leib, DOWN, buff=0.55)

        with self.voiceover(
            "To separate the two classes, <bookmark mark='c'/> Dirichlet attached a repeating pattern of signs to the remainders: "
            "plus one, zero, minus one, zero. This is a Dirichlet character, chi. <bookmark mark='l'/> Put chi into the zeta "
            "series and you get an L-function, <bookmark mark='p'/> which also has an Euler product over the primes."
        ) as vo:
            vo.wait_until("c")
            self.play(FadeIn(chi), LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cells], lag_ratio=0.06))
            vo.wait_until("l")
            self.play(Write(L[:3]))
            vo.wait_until("p")
            self.play(Write(L[3:]), FadeIn(leib))
        with self.voiceover(
            "There's one for every modulus q, and every pattern of this kind, <bookmark mark='z'/> and their zeros control how the "
            "primes split among the remainders mod q. <bookmark mark='g'/> The generalized Riemann hypothesis says that all of "
            "their nontrivial zeros lie on the critical line, too."
        ) as vo:
            self.play(FadeIn(gen[0]))
            vo.wait_until("z")
            self.play(FadeIn(gen[1]))
            vo.wait_until("g")
            self.play(FadeIn(gen[2]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ghost(self):
        ax = Axes(x_range=[0.0, 1.2, 0.25], y_range=[-6, 6, 2], x_length=6.2, y_length=5.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to(LEFT * 3.3 + DOWN * 0.3)
        one = Line(ax.c2p(1, -6), ax.c2p(1, 6), color=GREY_B, stroke_width=2)
        half = DashedLine(ax.c2p(0.5, -6), ax.c2p(0.5, 6), color=C.ZERO, stroke_width=2)
        lab = VGroup(MathTex(r"\tfrac12", font_size=28, color=C.ZERO).next_to(ax.c2p(0.5, -6), DOWN, buff=0.1),
                     MathTex("1", font_size=28).next_to(ax.c2p(1, -6), DOWN, buff=0.12))
        ts = np.linspace(-6, 6, 300)
        w = 0.1 / np.log(np.abs(ts) + 3)
        pts = [ax.c2p(1 - wi, t) for wi, t in zip(w, ts)] + [ax.c2p(1, 6), ax.c2p(1, -6)]
        zf = Polygon(*pts, stroke_width=0, fill_color=C.ZERO_FREE, fill_opacity=0.45)
        zf_l = label(r"classical zero-free region\\$\Real(s) > 1 - \dfrac{c}{\ln\!\big(q(|t|+3)\big)}$", font_size=26, color=C.ZERO_FREE)
        zf_l.move_to(RIGHT * 3.4 + UP * 2.3)
        ghost = Dot(ax.c2p(0.985, 0), radius=0.1, color=C.DANGER)
        ghost_l = label(r"a possible \textbf{Landau--Siegel zero}:\\real, simple, just left of 1,\\for a character of $\pm1$'s",
                        font_size=28, color=C.DANGER).move_to(RIGHT * 3.4 + UP * 0.2)
        arrow = Arrow(ghost_l.get_left(), ghost.get_center(), buff=0.15, color=C.DANGER, stroke_width=3)
        schem = note(r"schematic, near $s = 1$", font_size=22).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        effect = label(r"its wave would be almost as big as $x$:\\primes would shun half the remainders mod $q$\\for an enormously long time",
                       font_size=26, color=GREY_A).move_to(RIGHT * 3.4 + DOWN * 1.7)

        with self.voiceover(
            "For these L-functions there's a famous ghost. <bookmark mark='z'/> The classical zero-free regions leave room for "
            "exactly one possible exception: <bookmark mark='g'/> a single real zero, extremely close to one, for an L-function "
            "whose character takes only the values plus and minus one. It's called a Landau–Siegel zero. "
            "<bookmark mark='e'/> If one existed, its wave in the explicit formula would be almost as big as x itself, and the "
            "primes would avoid half the remainders mod q for an enormously long time."
        ) as vo:
            self.play(Create(ax), Create(one), Create(half), FadeIn(lab), FadeIn(schem))
            vo.wait_until("z")
            self.play(FadeIn(zf), FadeIn(zf_l))
            vo.wait_until("g")
            self.play(FadeIn(ghost, scale=2), GrowArrow(arrow), FadeIn(ghost_l))
            vo.wait_until("e")
            self.play(FadeIn(effect))

        siegel = label(r"Siegel (1935): it can't be \emph{too} close to 1 ---\\but the proof can't say how large $q$ must be.",
                       font_size=28).move_to(RIGHT * 3.4 + DOWN * 1.7)
        with self.voiceover(
            "Nobody has been able to rule these ghosts out. <bookmark mark='s'/> Siegel proved in 1935 that they can't be too "
            "close to one, but his proof is ineffective: it can't tell you how large q has to be before the bound kicks in. "
            "Many theorems in number theory carry an asterisk because of this."
        ) as vo:
            vo.wait_until("s")
            self.play(FadeOut(effect), FadeIn(siegel))

        line78 = DashedLine(ax.c2p(7 / 8, -6), ax.c2p(7 / 8, 6), color=C.ZERO_FREE, stroke_width=3)
        shade = region(ax, 7 / 8, 1.2, -6, 6, opacity=0.3)
        l78 = MathTex(r"\tfrac78", font_size=38, color=C.ZERO_FREE).next_to(ax.c2p(7 / 8, 6), UP, buff=0.1)
        claim = label(r"The 2026 claim: one line, $\Real(s) = \tfrac78$,\\for \emph{every} Dirichlet $L$-function at once",
                      font_size=28, color=C.ZERO_FREE).move_to(RIGHT * 3.4 + DOWN * 1.7)
        with self.voiceover(
            "That's why the new claim is stated for every Dirichlet L-function at once, <bookmark mark='l'/> with a single "
            "line, seven eighths, that works for every modulus. <bookmark mark='k'/> That kills the ghost: a real zero near one "
            "would sit to the right of seven eighths. A separate nine-page manuscript in the release also excludes these zeros "
            "directly."
        ) as vo:
            self.play(FadeOut(siegel), FadeIn(claim))
            vo.wait_until("l")
            self.play(FadeIn(shade), Create(line78), FadeIn(l78))
            vo.wait_until("k")
            self.play(FadeOut(ghost, scale=0.2), FadeOut(arrow), ghost_l.animate.set_opacity(0.3))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def consequences(self):
        head = label(r"If correct, these would follow (as the manuscripts note):", font_size=36).to_edge(UP, buff=0.5)
        fl = dict(font_size=28, tex_environment="flushleft")
        items = VGroup(
            label(r"$\bullet$ \ the least quadratic non-residue mod $p$ is at most $C(\ln p)^A$:\\"
                  r"\phantom{$\bullet$ \ }Vinogradov's conjecture", **fl),
            label(r"$\bullet$ \ square roots mod a prime by a fast \emph{deterministic} algorithm", **fl),
            label(r"$\bullet$ \ Miller's primality test becomes deterministic", **fl),
            label(r"$\bullet$ \ effective class-number bounds; \ Euler's list of 65 ``idoneal numbers'' is complete", **fl),
            label(r"$\bullet$ \ primes in every progression $a \bmod q$: a power-saving error, uniform in $q$", **fl),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        cond = note(r"each of these was previously known only by assuming GRH (or something like it)",
                    font_size=24).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "If it's correct, several old questions fall as consequences, as the manuscripts point out. "
            "<bookmark mark='a'/> The smallest number that isn't a perfect square mod a prime p would be at most a fixed power of "
            "log p, proving a conjecture of Vinogradov. <bookmark mark='b'/> Square roots mod a prime could be computed by a fast, "
            "deterministic algorithm, <bookmark mark='c'/> and Miller's primality test would become deterministic. "
            "<bookmark mark='d'/> Euler's list of 65 so-called idoneal numbers would be confirmed complete. "
            "<bookmark mark='e'/> And primes would be counted in every arithmetic progression with a power-saving error. "
            "<bookmark mark='f'/> Until now, all of these were known only by assuming some form of the generalized Riemann "
            "hypothesis."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(items[i], shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("f")
            self.play(FadeIn(cond))
        self.wait(0.8)
        self.clear_scene()
