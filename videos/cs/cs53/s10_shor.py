from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, tag_box


def frac_tex(frac: str) -> str:
    n, d = frac.split("/")
    return "0" if n == "0" else rf"\tfrac{{{n}}}{{{d}}}"


def shot_chip(s, w=1.12, h=0.5, size=20):
    """One measured outcome y and the fraction continued fractions turn it into; green if its denominator is the
    order."""
    col = YES if s["ok"] else NO
    box = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=col, stroke_width=1.6, fill_color=BG,
                           fill_opacity=1)
    t = MathTex(rf"{s['y']} \to {frac_tex(s['fraction'])}", font_size=size, color=col).move_to(box)
    if t.width > w - 0.1:
        t.width = w - 0.1
    return VGroup(box, t)


def spikes(probs, x0, y0, width, scale, color=DATA, w=0.07, lo=1e-4):
    """A probability distribution over many outcomes drawn as thin bars on one baseline (tiny bars omitted)."""
    n = len(probs)
    step = width / n
    g = VGroup()
    for y, p in enumerate(probs):
        if p > lo:
            g.add(Rectangle(width=w, height=p * scale, stroke_width=0, fill_color=color, fill_opacity=0.95).move_to(
                [x0 + (y + 0.5) * step, y0, 0], aligned_edge=DOWN))
    base = Line([x0, y0, 0], [x0 + width, y0, 0], color=GREY_C, stroke_width=1.5)
    return base, g, (lambda y: x0 + (y + 0.5) * step)


class Shor(VoiceoverScene):
    def construct(self):
        self.card()
        self.reduction()
        self.eigen()
        self.fifteen()
        self.twentyone()
        self.cost()

    def card(self):
        card = chapter_card(9, r"Shor's algorithm", r"How does finding a period factor a number?", lit=(1994, 1997),
                            extra=((1994, r"Shor: \ factoring and discrete logarithms"),
                                   (1997, r"the journal version")), part=PART)
        with self.voiceover("Chapter nine. Shor's algorithm. How does finding a period factor a number?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ factoring reduces to order finding
    def reduction(self):
        s = load("shor15")
        a, N, r = s["a"], s["N"], s["r"]
        head = label(r"Factoring is finding a period", font_size=36).to_edge(UP, buff=0.3)
        seq = VGroup(*[tag_box(f"{pow(a, x, N)}", color=[DATA, LAM, KERN, HEAD][x % r], size=20, w=0.82, h=0.5)
                       for x in range(12)]).arrange(RIGHT, buff=0.14).next_to(head, DOWN, buff=0.75)
        xs = VGroup(*[MathTex(rf"{a}^{{{x}}}", font_size=20, color=GREY_B).next_to(b, UP, buff=0.1)
                      for x, b in enumerate(seq)])
        sl = label(rf"powers of {a}, \ modulo {N}", font_size=18, color=GREY_B).next_to(seq, DOWN, buff=0.15).align_to(
            seq, LEFT)
        br = Brace(VGroup(*seq[r:2 * r]), DOWN, color=HEAD, buff=0.08)
        bl = MathTex(rf"r = {r}", font_size=24, color=HEAD).next_to(br, DOWN, buff=0.08)
        fs = 33
        rows = VGroup(
            MathTex(r"a^r", r"\equiv", r"1", r"\pmod N", font_size=fs),
            MathTex(r"a^r", r"-", r"1", r"\equiv", r"0", r"\pmod N", font_size=fs),
            MathTex(r"(a^{r/2} - 1)", r"(a^{r/2} + 1)", r"\equiv", r"0", r"\pmod N", font_size=fs),
            MathTex(r"\gcd(a^{r/2} \pm 1,\, N)", r"=", r"\text{a factor}", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        rows.next_to(sl, DOWN, buff=0.75).to_edge(LEFT, buff=0.6)
        rows[3][2].set_color(YES)
        whys = VGroup(label(r"$r$: \ the order of $a$", font_size=18, color=GREY_B),
                      label(r"$N$ divides $a^r - 1$", font_size=18, color=GREY_B),
                      label(r"if $r$ is even: \ a difference of squares", font_size=18, color=GREY_B),
                      label(r"if $a^{r/2} \not\equiv -1$, \ $N$ divides neither bracket", font_size=18, color=GREY_B))
        for w_, row in zip(whys, rows):
            w_.next_to(row, DOWN, buff=0.06).align_to(row, LEFT).shift(RIGHT * 0.1)
        h = pow(a, r // 2)
        f1, f2 = math.gcd(h - 1, N), math.gcd(h + 1, N)
        assert sorted((f1, f2)) == s["factors"]
        ex = VGroup(
            MathTex(rf"{a}^{{{r}}} = {a ** r} \equiv 1 \pmod{{{N}}}", font_size=fs, color=DATA),
            MathTex(rf"{a}^{{{r // 2}}} = {h}", font_size=fs, color=DATA),
            MathTex(rf"\gcd({h - 1}, {N}) = {f1},\quad \gcd({h + 1}, {N}) = {f2}", font_size=fs, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        ex.next_to(rows, RIGHT, buff=1.0).align_to(rows, UP).shift(DOWN * 0.2)
        foot = wrapped_label(r"for odd $N$ with two or more distinct prime factors, \ a random $a$ works with "
                             r"probability at least $\tfrac12$; \ Euclid's gcd is fast \ (Part 30); \ only $r$ is "
                             r"hard", 5.6, font_size=19, color=HEAD).next_to(ex, DOWN, buff=0.45).align_to(ex, LEFT)
        with self.voiceover(
            "Part 30's RSA rests on factoring being hard. Shor reduced factoring to finding a period. <bookmark mark='a'/> List the powers of seven modulo fifteen: one, seven, four, "
            "thirteen, and then one again. The sequence repeats with period four, the order of seven. "
            "<bookmark mark='b'/> If the order r is even, a to the r minus one is a multiple of N, and it splits as "
            "a difference of squares. <bookmark mark='c'/> Unless a to the r over two is minus one, N divides "
            "neither bracket, so each shares a proper factor with N, and Euclid's algorithm finds it: forty-eight "
            "and fifty give three and five. <bookmark mark='d'/> A random a works at least half the time, "
            "and everything is fast except finding r."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(b, x)) for b, x in zip(seq, xs)], lag_ratio=0.15), FadeIn(sl),
                      run_time=2.5)
            self.play(GrowFromCenter(br), FadeIn(bl))
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.5), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ order finding is phase estimation
    def eigen(self):
        s = load("shor15")
        a, N, r = s["a"], s["N"], s["r"]
        head = label(r"Order finding is phase estimation", font_size=36).to_edge(UP, buff=0.3)
        c = np.array([-4.6, 0.35, 0])
        R = 1.45
        cyc = [pow(a, k, N) for k in range(r)]
        pos = [c + R * np.array([math.cos(PI / 2 - 2 * PI * k / r), math.sin(PI / 2 - 2 * PI * k / r), 0])
               for k in range(r)]
        nodes = VGroup(*[tag_box(f"{v}", color=DATA, size=22, w=0.7, h=0.5).move_to(p) for v, p in zip(cyc, pos)])
        arcs = VGroup(*[CurvedArrow(pos[k] + 0.45 * (pos[(k + 1) % r] - pos[k]) / R - 0.0,
                                    pos[(k + 1) % r] - 0.45 * (pos[(k + 1) % r] - pos[k]) / R, angle=-PI / 4,
                                    color=LAM, stroke_width=2.5, tip_length=0.16) for k in range(r)])
        ul = MathTex(rf"\times {a}", font_size=24, color=LAM).move_to(c)
        cl = wrapped_label(rf"$U|y\rangle = |{a}y \bmod {N}\rangle$ walks round a cycle of length $r = {r}$: \ "
                           rf"$U^{{{r}}} = I$ on it", 4.2, font_size=19, color=GREY_A).next_to(
            c + DOWN * R, DOWN, buff=0.55)
        fs = 31
        rows = VGroup(
            MathTex(r"U|y\rangle", r"=", r"|ay \bmod N\rangle", font_size=fs),
            MathTex(r"|u_s\rangle", r"=", r"\frac{1}{\sqrt r}\sum_{k=0}^{r-1} e^{-2\pi i\, sk/r}\,|a^k \bmod N\rangle",
                    font_size=fs),
            MathTex(r"U|u_s\rangle", r"=", r"e^{2\pi i\, s/r}", r"|u_s\rangle", font_size=fs),
            MathTex(r"\frac{1}{\sqrt r}\sum_{s=0}^{r-1}", r"|u_s\rangle", r"=", r"|1\rangle", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62)
        rows.move_to([2.6, 0.45, 0]).align_to([-1.7, 0, 0], LEFT)
        rows[2][2].set_color(HEAD)
        rows[3][3].set_color(YES)
        whys = VGroup(label(r"reversible: \ $a$ has an inverse mod $N$ \ (Part 30), \ so $U$ is unitary",
                            font_size=18, color=GREY_B),
                      label(r"a state spread round the cycle, \ twisted by $s/r$ of a turn per step", font_size=18,
                            color=GREY_B),
                      label(r"$U$ moves each term one step on: \ the twist comes out as a phase", font_size=18,
                            color=GREY_B),
                      label(r"the twists cancel except at $k = 0$: \ start the work register at $|1\rangle$",
                            font_size=18, color=YES))
        for w_, row in zip(whys, rows):
            w_.next_to(row, DOWN, buff=0.08).align_to(row, LEFT).shift(RIGHT * 0.1)
        foot = wrapped_label(r"phase estimation \ (chapter 8) \ on $|1\rangle$ returns $s/r$ for a random $s$; \ "
                             r"$U^{2^j}$ multiplies by $a^{2^j} \bmod N$, \ found by repeated squaring; \ this "
                             r"arithmetic, \ about $n^3$ gates for an $n$-bit $N$ done the schoolbook way, \ is most "
                             r"of the cost", 12.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Chapter eight promised that order finding is phase estimation. <bookmark mark='a'/> Multiplication by a "
            "modulo N is reversible, since a has an inverse, so it is a unitary, U. From one, it walks round a "
            "cycle: one, seven, four, thirteen, and back. <bookmark mark='b'/> Spread a state round the cycle, "
            "twisting its phase by s over r of a turn at each step. <bookmark mark='c'/> U moves every term one step "
            "on, and the twist comes out as a phase: an eigenvector, with eigenvalue e to the two pi i s over r. "
            "<bookmark mark='d'/> Add all r eigenvectors, and the twists cancel everywhere except at one. So the "
            "plain state one is an equal superposition of them. <bookmark mark='e'/> Phase estimation on it returns "
            "s over r, for a random s. The controlled powers come from repeated squaring, and this arithmetic, "
            "about n cubed gates, is most of the cost."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(FadeIn(nodes[0]))
            for k in range(r):
                self.play(Create(arcs[k]), FadeIn(nodes[(k + 1) % r]), run_time=0.6)
            self.play(FadeIn(ul), FadeIn(cl))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(Rotate(arcs, angle=-2 * PI / r, about_point=c), run_time=1.2)
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ 15 on our simulator
    def fifteen(self):
        s = load("shor15")
        a, N, r, t, Q = s["a"], s["N"], s["r"], s["t"], s["Q"]
        head = label(rf"Our simulator factors {N}: \ $a = {a}$, \ {t} counting qubits", font_size=36).to_edge(
            UP, buff=0.3)
        x0, y0, W, S = -6.0, -0.15, 11.6, 8.0
        base, bars, xp = spikes(s["probs"], x0, y0, W, S, color=DATA)
        ticks = VGroup(*[label(f"{v}", font_size=16, color=GREY_A).move_to([xp(v), y0 - 0.25, 0])
                         for v in [*s["peaks"], Q - 1]])
        xl = label(rf"measured $y$, \ out of $2^{{{t}}} = {Q}$", font_size=18, color=GREY_B).next_to(
            ticks, DOWN, buff=0.1)
        top = max(s["probs"]) * S
        pk = VGroup(*[label(f"{s['probs'][v]:.2f}", font_size=17, color=DATA).move_to([xp(v), y0 + top + 0.22, 0])
                      for v in s["peaks"]])
        gl = VGroup(*[DashedLine([xp(v), y0, 0], [xp(v), y0 + top + 0.02, 0], color=HEAD, dash_length=0.06,
                                 stroke_width=1.5) for v in s["peaks"]])
        ml = label(rf"multiples of $2^{{{t}}}/r = {Q}/{r} = {Q // r}$", font_size=20, color=HEAD).move_to(
            [(xp(s["peaks"][1]) + xp(s["peaks"][2])) / 2, y0 + top + 0.62, 0])
        chips = VGroup(*[shot_chip(x) for x in s["samples"]]).arrange_in_grid(rows=2, cols=10, buff=(0.1, 0.16))
        chips.next_to(xl, DOWN, buff=0.35)
        cl = label(r"20 shots, \ each $y/2^t$ put in lowest terms:", font_size=18, color=GREY_B).next_to(
            chips, UP, buff=0.08).align_to(chips, LEFT)
        k = sum(x["ok"] for x in s["samples"])
        res = label(rf"{k} of 20 shots give $r = {r}$ at once; \ ${a}^{{{r}}} \equiv 1$, \ so ${N} = "
                    rf"{s['factors'][0]} \times {s['factors'][1]}$", font_size=21, color=YES).next_to(
            chips, DOWN, buff=0.25)
        honest = note(r"our simulator writes $a^x \bmod N$ into the work register directly, \ rather than building "
                      r"the multiplier from gates", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Our simulator factors fifteen, with a equal to seven, using nine counting qubits, twice fifteen's "
            "four bits plus one: five hundred and twelve outcomes. <bookmark mark='a'/> After the "
            "inverse Fourier transform, all the probability sits on four spikes, a quarter each, at the multiples "
            "of five hundred and twelve over four, as chapter seven predicted. <bookmark mark='b'/> Three hundred and eighty-four over five hundred and twelve is three quarters, and its "
            "denominator is the order, four. <bookmark mark='c'/> A shot at two hundred and fifty-six gives one half, "
            "because s and r shared a factor, and a shot at nought gives nothing. Nine of our twenty shots found "
            "four at once. <bookmark mark='d'/> One honest caveat: our simulator writes a to the x modulo N "
            "straight into the work register."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(ticks), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), run_time=1.5)
            self.play(FadeIn(pk), Create(gl), FadeIn(ml))
            vo.wait_until("b")
            self.play(FadeIn(cl))
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in chips], lag_ratio=0.12), run_time=3)
            vo.wait_until("c")
            self.play(*[Indicate(c_, color=NO, scale_factor=1.08) for c_, x in zip(chips, s["samples"])
                        if not x["ok"]])
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(honest))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ 21, and continued fractions
    def twentyone(self):
        s = load("shor21")
        a, N, r, t, Q, P = s["a"], s["N"], s["r"], s["t"], s["Q"], s["probs"]
        head = label(rf"Twenty-one: \ $r = {r}$ does not divide $2^{{{t}}}$", font_size=36).to_edge(UP, buff=0.3)
        x0, y0, W, S = -6.4, 0.55, 6.2, 11.0
        base, bars, xp = spikes(P, x0, y0, W, S, color=DATA, w=0.05, lo=2e-3)
        ticks = VGroup(*[label(f"{v}", font_size=16, color=GREY_A).move_to([xp(v), y0 - 0.22, 0])
                         for v in (0, 1024, Q - 1)])
        tl = label(rf"$y$, \ out of {Q}; \ peaks near $k \cdot {Q}/{r}$", font_size=17, color=GREY_B).next_to(
            ticks, DOWN, buff=0.08)
        y = next(x["y"] for x in s["samples"] if x["ok"] and x["fraction"] == "5/6")
        ring = Circle(radius=0.16, color=HEAD, stroke_width=2.5).move_to([xp(y), y0 + P[y] * S + 0.2, 0])
        # the zoom around y
        zs = list(range(y - 3, y + 4))
        zw, zg, zS = 0.42, 0.14, 13.0
        zx0, zy0 = -6.0, -2.55
        zb = VGroup(*[Rectangle(width=zw, height=max(P[v] * zS, 0.005), stroke_width=0,
                                fill_color=HEAD if v == y else DATA, fill_opacity=0.9).move_to(
            [zx0 + i * (zw + zg), zy0, 0], aligned_edge=DOWN) for i, v in enumerate(zs)])
        zbase = Line([zx0 - zw, zy0, 0], [zx0 + (len(zs) - 1) * (zw + zg) + zw, zy0, 0], color=GREY_C)
        zt = VGroup(*[label(f"{v}", font_size=16, color=GREY_A).next_to(b, DOWN, buff=0.08).set_y(zy0 - 0.2)
                      for v, b in zip(zs, zb)])
        zp = VGroup(*[label(f"{P[v]:.3f}", font_size=16, color=HEAD if v == y else DATA).next_to(b, UP, buff=0.06)
                      .shift(RIGHT * (0.22 if v == y else 0)) for v, b in zip(zs, zb) if P[v] > 0.02])
        exact = Q * 5 / r
        mk = DashedLine([zx0 + (exact - zs[0]) * (zw + zg), zy0, 0], [zx0 + (exact - zs[0]) * (zw + zg),
                                                                     zy0 + 1.85, 0], color=YES, dash_length=0.06)
        mkl = MathTex(rf"5 \cdot \tfrac{{{Q}}}{{{r}}} = {exact:.2f}", font_size=20, color=YES).next_to(
            mk, UP, buff=0.05)
        zl = label(r"zoomed in:", font_size=17, color=GREY_B).next_to(zbase, UP, buff=1.95).align_to(zbase, LEFT)
        fs = 26
        rows = VGroup(
            MathTex(rf"\frac{{{y}}}{{{Q}}}", r"=", rf"\cfrac{{1}}{{1 + \cfrac{{{Q - y}}}{{{y}}}}}", font_size=fs),
            MathTex(r"=", rf"\cfrac{{1}}{{1 + \cfrac{{1}}{{5 + \cfrac{{{y - 5 * (Q - y)}}}{{{Q - y}}}}}}}",
                    font_size=fs),
            MathTex(r"\approx", r"\cfrac{1}{1 + \cfrac{1}{5}}", r"=", r"\frac{5}{6}", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35).align_to([0.6, 0, 0], LEFT)
        rows[1].align_to(rows[0][1], LEFT)
        rows[2].align_to(rows[0][1], LEFT)
        rows[2][3].set_color(YES)
        assert Q - y == 341 and y - 5 * (Q - y) == 2
        cfw = label(r"Euclid's algorithm, \ kept as a fraction: \ stop before the denominator passes $N$",
                    font_size=17, color=GREY_B).next_to(rows, DOWN, buff=0.12).align_to(rows, LEFT)
        h = pow(a, r // 2)
        fac = MathTex(rf"r = {r}:\quad {a}^{{{r // 2}}} = {h},\quad \gcd({h - 1}, {N}) = {math.gcd(h - 1, N)},\quad "
                      rf"\gcd({h + 1}, {N}) = {math.gcd(h + 1, N)}", font_size=24, color=YES).next_to(
            cfw, DOWN, buff=0.25).align_to(rows, LEFT)
        assert sorted((math.gcd(h - 1, N), math.gcd(h + 1, N))) == s["factors"]
        why = wrapped_label(rf"why it works: \ $2^t = {Q} \ge N^2 = {N * N}$, \ so the nearest $y$ is within "
                            r"$1/2^{t+1} < 1/(2r^2)$ of $s/r$, \ and then $s/r$ must be a convergent \ (Legendre)",
                            6.2, font_size=18, color=WHITE).next_to(fac, DOWN, buff=0.3).align_to(rows, LEFT)
        k = sum(x["ok"] for x in s["samples"])
        lcm = wrapped_label(rf"{k} of 20 shots give $\tfrac{{s}}{{6}}$ in lowest terms; \ $\tfrac23$ and $\tfrac12$ "
                            r"give divisors of $r$, \ and $\mathrm{lcm}(3, 2) = 6$ recovers it", 6.2, font_size=18,
                            color=HEAD).next_to(why, DOWN, buff=0.2).align_to(rows, LEFT)
        with self.voiceover(
            "Twenty-one, with a equal to two, is less tidy: the order is six, which does not divide two thousand and "
            "forty-eight. <bookmark mark='a'/> So the peaks fall between outcomes, and probability leaks to the "
            "neighbours: about eleven per cent on the nearest, almost three on the next. <bookmark mark='b'/> "
            "Suppose a shot gives seventeen hundred and seven. Expand it over two thousand and forty-eight as a "
            "continued fraction, Euclid's algorithm in disguise, and stop before the denominator passes twenty-one: "
            "five sixths. <bookmark mark='c'/> The order is six. Two cubed is eight, and seven and nine share the "
            "factors seven and three with twenty-one. <bookmark mark='d'/> Why does it work? With two to the t at "
            "least N squared, the nearest outcome is so close to s over r that s over r must be a convergent. "
            "<bookmark mark='e'/> A shot giving two thirds or one half yields a divisor of six, and the least common "
            "multiple of two such divisors recovers it."
        ) as vo:
            self.play(FadeIn(head), Create(base), FadeIn(ticks), FadeIn(tl))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(ring))
            self.play(FadeIn(zl), Create(zbase), FadeIn(zt), LaggedStart(*[GrowFromEdge(b, DOWN) for b in zb],
                                                                        lag_ratio=0.1))
            self.play(FadeIn(zp), Create(mk), FadeIn(mkl))
            vo.wait_until("b")
            self.play(Write(rows[0]))
            self.play(FadeIn(rows[1], shift=DOWN * 0.1))
            self.play(FadeIn(rows[2], shift=DOWN * 0.1), FadeIn(cfw))
            vo.wait_until("c")
            self.play(FadeIn(fac))
            vo.wait_until("d")
            self.play(FadeIn(why))
            vo.wait_until("e")
            self.play(FadeIn(lcm))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the gap, and a caution
    def cost(self):
        head = label(r"Polynomial against sub-exponential", font_size=36).to_edge(UP, buff=0.3)

        def nfs(n):          # log10 of exp((64/9)^(1/3) (ln N)^(1/3) (ln ln N)^(2/3)), N of n bits
            ln_n = n * math.log(2)
            return (64 / 9) ** (1 / 3) * ln_n ** (1 / 3) * math.log(ln_n) ** (2 / 3) / math.log(10)
        ax = Axes(x_range=[0, 4096, 1024], y_range=[0, 50, 10], x_length=6.2, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": True})
        ax.move_to([-3.2, 0.1, 0])
        xt = VGroup(*[label(f"{v:,}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (1024, 2048, 3072, 4096)])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (10, 20, 30, 40, 50)])
        xl = label(r"$n$, \ bits of $N$", font_size=18, color=GREY_B).next_to(xt, DOWN, buff=0.12)
        yl = label(r"operations \ (log scale)", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.15).align_to(
            ax, LEFT)
        cl = ax.plot(nfs, x_range=[16, 4096], color=NO, stroke_width=3)
        ql = ax.plot(lambda n: 3 * math.log10(n), x_range=[16, 4096], color=YES, stroke_width=3)
        cll = label(r"number field sieve: \ $e^{c\, n^{1/3} (\log n)^{2/3}}$", font_size=18, color=NO).move_to(
            ax.c2p(1450, 47))
        qll = label(r"Shor: \ about $n^3$ gates", font_size=18, color=YES).next_to(ax.c2p(4096, 3 * math.log10(4096)),
                                                                                 UP, buff=0.15).shift(LEFT * 1.2)
        sh = note(r"shapes of the two costs; \ constants omitted", font_size=16).next_to(xl, DOWN, buff=0.08)
        rsa = Dot(ax.c2p(829, nfs(829)), radius=0.07, color=HEAD)
        rsal = label(r"RSA-250", font_size=17, color=HEAD).next_to(rsa, LEFT, buff=0.12).shift(UP * 0.15)
        notes = VGroup(
            wrapped_label(r"the sieve's record \ (Part 30): \ RSA-250, \ 829 bits, \ about 2{,}700 core-years \ "
                          r"(Boudot et al., \ 2020)", 5.0, font_size=19, color=HEAD),
            wrapped_label(r"the same method finds discrete logarithms: \ Diffie--Hellman and elliptic curves fall "
                          r"with RSA \ (Shor, \ 1994)", 5.0, font_size=19, color=NO),
            wrapped_label(r"early hardware runs that ``factored'' 15 and 21 used circuits simplified with knowledge "
                          r"of the answer \ (Smolin, \ Smith and Vargo, \ 2013); \ how big a real machine must be is "
                          r"chapter 13's question", 5.0, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.15, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The best known classical method, Part 30's number field "
            "sieve, takes time growing roughly like e to the cube root of the number of bits. Shor's algorithm "
            "needs about n cubed gates. On a logarithmic scale, one curve keeps climbing and the other barely "
            "rises. <bookmark mark='b'/> The sieve's record, RSA-250, eight hundred and twenty-nine bits, took "
            "about two thousand seven hundred core-years in 2020. <bookmark mark='c'/> Shor's method also finds "
            "discrete logarithms, so Diffie–Hellman and elliptic curves fall with RSA. <bookmark mark='d'/> A "
            "caution: early hardware runs that factored fifteen and twenty-one used circuits "
            "simplified with knowledge of the answer, as Smolin, Smith and Vargo pointed out in 2013."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(sh))
            vo.wait_until("a")
            self.play(Create(cl), FadeIn(cll), run_time=1.5)
            self.play(Create(ql), FadeIn(qll), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rsa), FadeIn(rsal), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
