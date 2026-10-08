from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import label, load, note, polyline, schematic_tag

P_GAUSS, G_ROOT = 37, 2  # Gauss-sum walk for a sextic character mod 37 (2 is a primitive root)


def sextic_gauss_terms(p=P_GAUSS, g=G_ROOT) -> np.ndarray:
    ind = {pow(g, k, p): k for k in range(p - 1)}
    assert len(ind) == p - 1
    xs = np.arange(1, p)
    chi = np.exp(2j * np.pi * np.array([ind[int(x)] for x in xs]) / 6)
    return chi * np.exp(2j * np.pi * xs / p)


class ThetaReflection(VoiceoverScene):
    def construct(self):
        self.large_sieve()
        self.poisson()
        self.gauss_sums()
        self.absorb()
        self.kummer()
        self.theta()
        self.quadratic()

    # ------------------------------------------------------------------
    def large_sieve(self):
        o = np.array([-4.2, -0.9, 0])
        e1 = Arrow(o, o + 2.6 * RIGHT, buff=0, color=C.SIEVE, stroke_width=5)
        e2 = Arrow(o, o + 2.6 * UP, buff=0, color=C.SIEVE, stroke_width=5)
        a_vec = np.array([2.0, 1.4, 0])
        a = Arrow(o, o + a_vec, buff=0, color=C.MOBIUS, stroke_width=6)
        al = MathTex(r"a", font_size=36, color=C.MOBIUS).next_to(o + a_vec, UR, buff=0.05)
        p1 = DashedLine(o + a_vec, o + [a_vec[0], 0, 0], color=GREY_B)
        p2 = DashedLine(o + a_vec, o + [0, a_vec[1], 0], color=GREY_B)
        b1 = Line(o, o + [a_vec[0], 0, 0], color=C.SIEVE, stroke_width=9).set_opacity(0.6)
        b2 = Line(o, o + [0, a_vec[1], 0], color=C.SIEVE, stroke_width=9).set_opacity(0.6)
        bessel = MathTex(r"\sum_u |\langle a, e_u\rangle|^2 \le \|a\|^2", font_size=38).next_to(o, DOWN, buff=0.7).shift(RIGHT * 1.2)
        pic = note(r"perpendicular directions $e_u$: \\the squared shadows can't add up\\to more than the whole", font_size=24)
        pic.next_to(bessel, DOWN, buff=0.25)
        right = VGroup(
            label(r"\textbf{the large sieve}", font_size=34, color=C.SIEVE),
            label(r"each $u$ gives a direction $\big((\tfrac{u}{n})\big)_n$;\\different $u$'s are \emph{nearly} perpendicular", font_size=28),
            MathTex(r"\sum_{u} \Big|\sum_n a_n \Big(\frac{u}{n}\Big)\Big|^2 \lesssim (\#u + \#n)\sum_n |a_n|^2", font_size=36),
            label(r"for sixth-power symbols, the best version\\loses too much --- and it knows nothing about $\mu$",
                  font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.0 + UP * 0.2)

        with self.voiceover(
            "Mean squares like this one are the territory of a tool called the large sieve. <bookmark mark='p'/> Here's the idea "
            "in a picture. If you have perpendicular directions, then the squared shadows of any vector on them can't add up to "
            "more than the vector's own length squared. <bookmark mark='u'/> Now think of each u as giving a direction, with one "
            "coordinate for every n. Different u's point in nearly perpendicular directions, <bookmark mark='b'/> so no single "
            "vector can line up with too many of them at once."
        ) as vo:
            self.play(GrowArrow(e1), GrowArrow(e2))
            vo.wait_until("p")
            self.play(GrowArrow(a), FadeIn(al))
            self.play(Create(p1), Create(p2), FadeIn(b1), FadeIn(b2))
            self.play(FadeIn(bessel), FadeIn(pic))
            vo.wait_until("u")
            self.play(FadeIn(right[:2]))
            vo.wait_until("b")
            self.play(FadeIn(right[2]))
        with self.voiceover(
            "But for sixth-power symbols, the best general large sieve loses too much. And on its own, it knows nothing special "
            "about the Möbius function, which is exactly what we can't control."
        ) as vo:
            self.play(FadeIn(right[3]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def poisson(self):
        t = 0.04
        left = Axes(x_range=[-14, 14, 7], y_range=[0, 1.1, 0.5], x_length=5.6, y_length=2.6, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": False})
        right = left.copy()
        VGroup(left, right).arrange(RIGHT, buff=1.6).move_to(DOWN * 0.6)
        gl = left.plot(lambda x: np.exp(-np.pi * x * x * t), x_range=[-14, 14], color=C.THETA, stroke_width=2.5)
        gr = right.plot(lambda x: np.exp(-np.pi * x * x / t), x_range=[-1, 1, 0.005], color=C.THETA, stroke_width=2.5)
        stems_l = VGroup(*[Line(left.c2p(n, 0), left.c2p(n, np.exp(-np.pi * n * n * t)), color=WHITE, stroke_width=2.5)
                           for n in range(-14, 15)])
        stems_r = VGroup(*[Line(right.c2p(n, 0), right.c2p(n, np.exp(-np.pi * n * n / t)), color=WHITE, stroke_width=2.5)
                           for n in range(-14, 15) if np.exp(-np.pi * n * n / t) > 1e-3])
        dots_r = VGroup(*[Dot(right.c2p(n, 0), radius=0.03, color=GREY_B) for n in range(-14, 15) if n])
        lhs_val = float(np.sum(np.exp(-np.pi * np.arange(-200, 201) ** 2 * t)))
        rhs_val = float(np.sum(np.exp(-np.pi * np.arange(-200, 201) ** 2 / t)) / np.sqrt(t))
        assert abs(lhs_val - rhs_val) < 1e-9
        eq = MathTex(r"\sum_{n\in\mathbb Z} e^{-\pi n^2 t}", r"=", r"\frac{1}{\sqrt t}\sum_{n\in\mathbb Z} e^{-\pi n^2 / t}",
                     font_size=44).to_edge(UP, buff=0.5)
        eq[0].set_color(C.THETA)
        eq[2].set_color(C.THETA)
        name = label(r"Poisson summation (Jacobi's theta identity)", font_size=28, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        vl = MathTex(rf"= {lhs_val:.6f}", font_size=32).next_to(left, DOWN, buff=0.3)
        vr = MathTex(rf"= {rhs_val:.6f}", font_size=32).next_to(right, DOWN, buff=0.3)
        tl = label(r"$t = 0.04$: \ many terms", font_size=26).next_to(left, UP, buff=0.15)
        tr = label(r"essentially one term", font_size=26).next_to(right, UP, buff=0.15)
        eqs = MathTex("=", font_size=60).move_to((left.get_right() + right.get_left()) / 2)

        with self.voiceover(
            "The way out is a change of perspective, called Poisson summation. It trades a sum over u for a sum over a dual "
            "frequency. <bookmark mark='e'/> Here's the classic example. <bookmark mark='l'/> Sample a wide Gaussian bump at every "
            "integer, and add: many terms. <bookmark mark='r'/> Poisson summation says this equals a sum of narrow bumps, where "
            "essentially one term survives. <bookmark mark='v'/> Both sides give exactly the same number. Long sums turn into short "
            "ones, and short into long."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(eq), FadeIn(name))
            vo.wait_until("l")
            self.play(Create(left), Create(gl), FadeIn(tl))
            self.play(LaggedStart(*[Create(s) for s in stems_l], lag_ratio=0.05), run_time=1.2)
            vo.wait_until("r")
            self.play(Create(right), Create(gr), FadeIn(tr), FadeIn(eqs))
            self.play(Create(stems_r), FadeIn(dots_r), run_time=0.8)
            vo.wait_until("v")
            self.play(FadeIn(vl), FadeIn(vr))
        self.wait(0.5)
        self.clear_scene()
        self.jacobi = eq

    # ------------------------------------------------------------------
    def gauss_sums(self):
        terms = sextic_gauss_terms()
        S = np.concatenate([[0], np.cumsum(terms)])
        assert abs(abs(S[-1]) - np.sqrt(P_GAUSS)) < 1e-9
        o = np.array([-2.6, -0.4, 0])
        k = 0.47
        to = lambda z: o + k * np.array([z.real, z.imag, 0])
        arrows = VGroup(*[Arrow(to(S[i]), to(S[i + 1]), buff=0, color=interpolate_color(ManimColor(C.GAUSS), ManimColor(C.CHARACTER), i / len(terms)),
                                stroke_width=3, max_tip_length_to_length_ratio=0.25) for i in range(len(terms))])
        circ = Circle(radius=k * np.sqrt(P_GAUSS), color=GREY_B, stroke_width=1.5).move_to(o)
        rad = Line(o, to(S[-1]), color=C.GAUSS, stroke_width=3)
        rl = MathTex(r"\sqrt{37}", font_size=32, color=C.GAUSS).next_to(rad.get_center(), RIGHT, buff=0.15)
        start = Dot(o, radius=0.06, color=WHITE)
        g = MathTex(r"G(\chi)", r"=", r"\sum_{x \bmod p} \chi(x)\, e^{2\pi i x/p}", font_size=42)
        g[0].set_color(C.GAUSS)
        g.move_to(RIGHT * 3.5 + UP * 2.4)
        gl = label(r"a \textbf{Gauss sum}:\\character value $\times$ a rotating unit arrow", font_size=28).next_to(g, DOWN, buff=0.3)
        ex = label(r"here: a sixth-order character mod $p = 37$", font_size=26, color=GREY_A).next_to(gl, DOWN, buff=0.4)
        mag = MathTex(r"|G(\chi)| = \sqrt{p}\quad\text{always}", font_size=40, color=C.GAUSS).next_to(ex, DOWN, buff=0.5)

        with self.voiceover(
            "When you Poisson-sum a character like our sixth-power symbol, <bookmark mark='g'/> what comes out are Gauss sums. "
            "A Gauss sum adds up the character's values, each multiplied by a rotating unit arrow. <bookmark mark='w'/> Here's one "
            "for a sixth-order character mod 37. The walk wanders around, <bookmark mark='e'/> but it always ends at distance "
            "exactly the square root of p from where it started."
        ) as vo:
            vo.wait_until("g")
            self.play(Write(g), FadeIn(gl))
            vo.wait_until("w")
            self.play(FadeIn(ex), FadeIn(start))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.6), run_time=vo.until("e") - 0.2)
            vo.wait_until("e")
            self.play(Create(circ), Create(rad), FadeIn(rl), FadeIn(mag))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def absorb(self):
        ident = MathTex(r"\mu(n)", r"\cdot", r"\gamma_{-1}(n)", r"=", r"(\text{simple unit-size factors})", r"\cdot", r"\gamma_{2}(n)",
                        font_size=40).move_to(UP * 1.2)
        ident[0].set_color(C.MOBIUS)
        ident[2].set_color(C.GAUSS)
        ident[4].set_color(GREY_B)
        ident[6].set_color(C.THETA)
        b1 = Brace(ident[2], DOWN, buff=0.15, color=C.GAUSS)
        b1l = label(r"sextic Gauss sum\\(from Poisson)", font_size=26, color=C.GAUSS).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(ident[6], DOWN, buff=0.15, color=C.THETA)
        b2l = label(r"\emph{cubic} Gauss sum", font_size=26, color=C.THETA).next_to(b2, DOWN, buff=0.1)
        src = note(r"for squarefree $n$; the identity goes back to Hasse, and was used by Heath-Brown (2000)", font_size=24)
        src.next_to(ident, UP, buff=0.4)
        gone = label(r"the M\"obius function is \emph{absorbed}", font_size=38, color=YELLOW).to_edge(DOWN, buff=1.2)
        quad = label(r"(with quadratic symbols instead, the flip just returns another M\"obius sum: it goes in a circle)",
                     font_size=26, color=GREY_A).next_to(gone, DOWN, buff=0.3)
        cross = Cross(ident[0], stroke_color=YELLOW, stroke_width=5)

        with self.voiceover(
            "And now something special happens. <bookmark mark='i'/> An identity going back to Hasse, and used by Heath-Brown, "
            "says that mu of n, times the sextic Gauss sum that Poisson summation produced, <bookmark mark='c'/> equals a cubic "
            "Gauss sum, up to simple factors of size one. <bookmark mark='g'/> The Möbius function disappears. The randomness "
            "we couldn't control gets absorbed into Gauss sums. <bookmark mark='q'/> That's the reason for sixth powers: with "
            "ordinary quadratic symbols, the flip just hands you back another Möbius sum."
        ) as vo:
            vo.wait_until("i")
            self.play(Write(ident[:3]), FadeIn(src))
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("c")
            self.play(Write(ident[3:]), GrowFromCenter(b2), FadeIn(b2l))
            vo.wait_until("g")
            self.play(Create(cross), FadeIn(gone))
            vo.wait_until("q")
            self.play(FadeIn(quad))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kummer(self):
        k = load("kummer")
        p, cs = k["p"], k["cos"]
        theta = np.arccos(np.clip(cs, -1, 1))
        c = np.array([-3.3, -1.6, 0])
        R = 2.6
        arc = Arc(radius=R, start_angle=0, angle=PI, color=GREY_B, stroke_width=2).move_arc_center_to(c)
        cuts = VGroup(*[DashedLine(c, c + R * 1.08 * np.array([np.cos(a), np.sin(a), 0]), color=GREY_C, stroke_width=1.5)
                        for a in (PI / 3, 2 * PI / 3)])
        names = VGroup(*[MathTex(s, font_size=30).move_to(c + (R + 0.45) * np.array([np.cos(a), np.sin(a), 0]))
                         for s, a in [("I", PI / 6), ("II", PI / 2), ("III", 5 * PI / 6)]])

        def dots_for(mask, radius, opacity):
            return VGroup(*[Dot(c + R * np.array([np.cos(a), np.sin(a), 0]), radius=radius, color=C.THETA).set_opacity(opacity)
                            for a in theta[mask]])

        small = p < 500
        d_small = dots_for(small, 0.07, 0.9)
        d_big = dots_for(p < 60_000, 0.03, 0.35)

        def counts(mask):
            th = theta[mask]
            return [int(np.sum(th < PI / 3)), int(np.sum((th >= PI / 3) & (th < 2 * PI / 3))), int(np.sum(th >= 2 * PI / 3))]

        c500, c60k = counts(small), counts(p < 60_000)
        assert c500 == [24, 14, 7], c500

        def bars(cnt, x0):
            tot = sum(cnt)
            g = VGroup()
            for i, v in enumerate(cnt):
                h = 3.2 * v / tot
                r = Rectangle(width=0.55, height=h, stroke_width=0, fill_color=C.THETA, fill_opacity=0.8)
                r.move_to([x0 + 0.75 * i, -2.6 + h / 2, 0])
                lab = MathTex(["I", "II", "III"][i], font_size=24).next_to(r, DOWN, buff=0.1)
                val = MathTex(str(v), font_size=24).next_to(r, UP, buff=0.08)
                g.add(VGroup(r, lab, val))
            return g

        b500 = bars(c500, 2.0)
        b60k = bars(c60k, 5.0)
        t500 = label(r"$p < 500$\\(Kummer, 1846)", font_size=24).next_to(b500, UP, buff=0.2)
        t60k = label(r"$p < 60{,}000$\\(computed here)", font_size=24).next_to(b60k, UP, buff=0.2)
        head = label(r"Angles of the cubic Gauss sums, \ one per prime $p \equiv 1 \pmod 3$", font_size=32).to_edge(UP, buff=0.4)
        kummer_l = note(r"$\sum_{x} e^{2\pi i x^3/p} = 2\sqrt{p}\,\cos\theta_p$", font_size=26).next_to(head, DOWN, buff=0.15)
        later = VGroup(
            label(r"\textbf{1979}, Heath-Brown \& Patterson: in the limit, evenly spread", font_size=26),
            label(r"the slow drift is real: Patterson's $X^{5/6}$ bias\\(proved assuming GRH: Dunn \& Radziwi\l\l, 2024)", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.4).shift(DOWN * 1.0)

        with self.voiceover(
            "Cubic Gauss sums have a history. <bookmark mark='k'/> In 1846, Kummer computed their angles for every prime up to "
            "500, and found them bunched toward one end, in proportions of roughly three to two to one. "
            "<bookmark mark='c'/> Here is the same computation: twenty-four, fourteen, seven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(kummer_l))
            vo.wait_until("k")
            self.play(Create(arc), Create(cuts), FadeIn(names))
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in d_small], lag_ratio=0.05), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(b500), FadeIn(t500))
        with self.voiceover(
            "Go further, out to sixty thousand, <bookmark mark='s'/> and the angles slowly spread out. Heath-Brown and Patterson "
            "proved in 1979 that in the limit they're perfectly even. <bookmark mark='d'/> But the slow drift is real too: it's a "
            "bias that Patterson predicted, proved assuming the generalized Riemann hypothesis by Dunn and Radziwiłł in 2024."
        ) as vo:
            self.play(FadeOut(d_small), FadeIn(d_big), FadeIn(b60k), FadeIn(t60k), run_time=1.5)
            vo.wait_until("s")
            self.play(FadeIn(later[0]))
            vo.wait_until("d")
            self.play(FadeIn(later[1]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theta(self):
        head = label(r"Why they're special: \ \textbf{Kubota (1969), Patterson (1977)}", font_size=34).to_edge(UP, buff=0.5)
        text = label(r"cubic Gauss sums are the Fourier coefficients of the\\\textbf{cubic theta function}, "
                     r"a function on 3-dimensional hyperbolic space\\with a hidden symmetry", font_size=32, color=C.THETA)
        text.next_to(head, DOWN, buff=0.5)
        jac = VGroup(
            label(r"its simpler cousin, Jacobi's theta function:", font_size=28, color=GREY_A),
            MathTex(r"\theta(\tau) = \sum_{n} e^{\pi i n^2 \tau}, \qquad \theta\!\Big(\!-\frac{1}{\tau}\Big) = \sqrt{\frac{\tau}{i}}\;\theta(\tau)",
                    font_size=40, color=C.THETA),
            label(r"(that is exactly the Gaussian identity from before)", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(text, DOWN, buff=0.6)
        with self.voiceover(
            "The reason behind all of this is deep. <bookmark mark='k'/> Kubota and Patterson showed that cubic Gauss sums are "
            "the Fourier coefficients of a special function, the cubic theta function, which lives on three-dimensional "
            "hyperbolic space and has a hidden symmetry. <bookmark mark='j'/> Its simpler cousin is Jacobi's theta function, "
            "whose symmetry is exactly the Gaussian identity we just saw."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("k")
            self.play(FadeIn(text))
            vo.wait_until("j")
            self.play(FadeIn(jac))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quadratic(self):
        flow = VGroup(
            label(r"long sum of cubic Gauss sums", font_size=30, color=C.THETA),
            label(r"short dual sum", font_size=30, color=C.THETA),
        ).arrange(RIGHT, buff=3.2).to_edge(UP, buff=0.7)
        arr = Arrow(flow[0].get_right(), flow[1].get_left(), buff=0.25, color=C.THETA)
        arr_l = label(r"the theta symmetry", font_size=26, color=C.THETA).next_to(arr, UP, buff=0.1)
        clock_c = [np.array([-4.3, -1.0, 0]), np.array([-1.5, -1.0, 0]), np.array([1.3, -1.0, 0])]
        clocks = VGroup()
        for c, ang, tex in [(clock_c[0], -PI / 3, r"\chi_p^{-1}"), (clock_c[1], -2 * PI / 3, r"\chi_p^{-2}"), (clock_c[2], -PI, r"\chi_p^{-3}")]:
            circ = Circle(radius=0.85, color=GREY_C, stroke_width=1.5).move_to(c)
            ticks = VGroup(*[Dot(c + 0.85 * np.array([np.cos(k * PI / 3), np.sin(k * PI / 3), 0]), radius=0.035, color=GREY_B) for k in range(6)])
            hand = Arrow(c, c + 0.85 * np.array([np.cos(ang), np.sin(ang), 0]), buff=0, color=C.CHARACTER, stroke_width=4)
            t = MathTex(tex, font_size=34, color=C.CHARACTER).next_to(circ, DOWN, buff=0.2)
            clocks.add(VGroup(circ, ticks, hand, t))
        ops = VGroup(MathTex(r"\times", font_size=44).move_to((clock_c[0] + clock_c[1]) / 2),
                     MathTex(r"=", font_size=44).move_to((clock_c[1] + clock_c[2]) / 2))
        res = VGroup(
            MathTex(r"\chi_p^{-3} = \chi_p^{3} = \pm 1", font_size=40, color=C.CHARACTER),
            label(r"a \emph{quadratic} character", font_size=28),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 4.6 + DOWN * 1.0)
        note1 = note(r"at each prime $p \mid h$: one factor from the Fourier side, two from the theta side", font_size=24)
        note1.to_edge(DOWN, buff=1.0)

        with self.voiceover(
            "Applying that symmetry turns the long sum of cubic Gauss sums into a short dual sum. <bookmark mark='c'/> And at each "
            "prime, the characters combine: one factor of chi to the minus one, from the Fourier side, <bookmark mark='t'/> two "
            "more from the theta side, <bookmark mark='r'/> and chi to the minus three is a sixth root of one cubed: just plus or "
            "minus one. <bookmark mark='q'/> The sixth-power family has turned into a quadratic one."
        ) as vo:
            self.play(FadeIn(flow[0]))
            self.play(GrowArrow(arr), FadeIn(arr_l), FadeIn(flow[1]))
            vo.wait_until("c")
            self.play(FadeIn(clocks[0]), FadeIn(note1))
            vo.wait_until("t")
            self.play(FadeIn(ops[0]), FadeIn(clocks[1]))
            vo.wait_until("r")
            self.play(FadeIn(ops[1]), FadeIn(clocks[2]))
            vo.wait_until("q")
            self.play(FadeIn(res))
        self.wait(0.5)
        self.clear_scene()

        qls = VGroup(
            label(r"\textbf{Heath-Brown's quadratic large sieve} (1995)", font_size=34, color=C.SIEVE),
            label(r"extended to number fields by Goldmakher \& Louvel", font_size=28, color=GREY_A),
            MathTex(r"\sum_{m \le M}^{\ \ \flat}\ \Big|\sum_{n \le N}^{\ \ \flat} a_n \Big(\frac{n}{m}\Big)\Big|^2 \;\lesssim\; (MN)^{\varepsilon}\,(M + N) \sum_n |a_n|^2",
                    font_size=40),
            note(r"($\flat$: squarefree indices) \ --- essentially the best possible", font_size=24),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        concl = label(r"$\Rightarrow$ the dual mean square is small $\Rightarrow$ the family is small on average", font_size=32,
                      color=YELLOW).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "And for quadratic families, there's a sharp tool: <bookmark mark='h'/> Heath-Brown's quadratic large sieve, from "
            "1995, extended to number fields by Goldmakher and Louvel. <bookmark mark='b'/> It bounds mean squares of quadratic "
            "symbols with essentially no loss. <bookmark mark='c'/> That gives the bound we need on the dual side, and with it, "
            "the crucial estimate for the family. Well, almost."
        ) as vo:
            vo.wait_until("h")
            self.play(FadeIn(qls[:2]))
            vo.wait_until("b")
            self.play(Write(qls[2]), FadeIn(qls[3]))
            vo.wait_until("c")
            self.play(FadeIn(concl, shift=UP * 0.2))
        self.wait(0.8)
        self.clear_scene()
