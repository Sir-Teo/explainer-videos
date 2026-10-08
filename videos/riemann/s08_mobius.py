from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import MU_COLORS, label, load, mobius_small, note, polyline


def factor_tex(n: int) -> str:
    out, m, p = [], n, 2
    while p * p <= m:
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        if e:
            out.append(f"{p}^{{{e}}}" if e > 1 else str(p))
        p += 1
    if m > 1:
        out.append(str(m))
    return r"\cdot".join(out) if out else "1"


class MobiusRandomness(VoiceoverScene):
    def construct(self):
        self.definition()
        self.inverse_zeta()
        self.walk()
        self.logic()

    # ------------------------------------------------------------------
    def definition(self):
        mu = [mobius_small(n) for n in range(1, 31)]
        assert mu == [int(v) for v in load("mobius")["mu_head"][1:31]]
        cells = VGroup()
        for n, m in zip(range(1, 31), mu):
            sq = Square(0.42, stroke_width=1.5, stroke_color=GREY_B, fill_color=MU_COLORS[m], fill_opacity=0.85)
            num = MathTex(str(n), font_size=22).move_to(sq)
            cells.add(VGroup(sq, num))
        cells.arrange(RIGHT, buff=0.04).move_to(DOWN * 0.6)
        defn = MathTex(r"\mu(n)", r"=", r"\begin{cases} \;\;\,0 & \text{if a square } > 1 \text{ divides } n \\ "
                       r"+1 & \text{if } n \text{ has an even number of prime factors} \\ "
                       r"-1 & \text{if } n \text{ has an odd number of prime factors} \end{cases}", font_size=36)
        defn[0].set_color(C.MOBIUS)
        defn.to_edge(UP, buff=0.5)
        name = label(r"the M\"obius function", font_size=30, color=C.MOBIUS).next_to(defn, DOWN, buff=0.25)
        examples = VGroup()
        for n in (6, 7, 12, 30):
            m = mobius_small(n)
            lhs = rf"{n} = {factor_tex(n)}" if factor_tex(n) != str(n) else rf"{n} \text{{ is prime}}"
            ex = MathTex(lhs, r"\;\Rightarrow\;", rf"\mu({n}) = {m:+d}" if m else rf"\mu({n}) = 0", font_size=32)
            ex[2].set_color(MU_COLORS[m] if m else GREY_B)
            examples.add(ex)
        examples.arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.35), col_alignments="ll").next_to(cells, DOWN, buff=0.6)
        legend = VGroup(*[VGroup(Square(0.25, fill_color=MU_COLORS[v], fill_opacity=0.85, stroke_width=1, stroke_color=GREY_B),
                                 MathTex(t, font_size=26)).arrange(RIGHT, buff=0.12)
                          for v, t in [(1, "+1"), (-1, "-1"), (0, "0")]]).arrange(RIGHT, buff=0.5).next_to(cells, UP, buff=0.35)

        with self.voiceover(
            "There's another way to state the Riemann hypothesis, and it's the one the new proof uses. <bookmark mark='m'/> "
            "Meet the Möbius function, mu of n. <bookmark mark='z'/> It's zero if n is divisible by a perfect square. "
            "<bookmark mark='e'/> Otherwise it's plus one if n has an even number of prime factors, and minus one if it has an "
            "odd number."
        ) as vo:
            vo.wait_until("m")
            self.play(Write(defn[:2]), FadeIn(name))
            vo.wait_until("z")
            self.play(FadeIn(defn[2]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cells], lag_ratio=0.04), FadeIn(legend), run_time=2)
        with self.voiceover(
            "So six, which is two times three, gets plus one. Seven gets minus one. Twelve has a square factor, so it gets zero. "
            "And thirty, a product of three primes, gets minus one."
        ) as vo:
            for ex in examples:
                self.play(FadeIn(ex, shift=UP * 0.1), run_time=0.9)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inverse_zeta(self):
        f = MathTex(r"\frac{1}{\zeta(s)}", r"=", r"\prod_p \Big(1 - \frac{1}{p^s}\Big)", r"=",
                    r"1 - \frac{1}{2^s} - \frac{1}{3^s} - \frac1{5^s} + \frac{1}{6^s} - \frac1{7^s} + \frac{1}{10^s} - \cdots",
                    font_size=40).move_to(UP * 0.8)
        f[2].set_color(C.PRIME)
        f[4].set_color(C.MOBIUS)
        g = MathTex(r"\frac{1}{\zeta(s)}", r"=", r"\sum_{n=1}^{\infty} \frac{\mu(n)}{n^s}", font_size=54).next_to(f, DOWN, buff=0.8)
        g[2].set_color(C.MOBIUS)
        with self.voiceover(
            "Why this odd function? Flip Euler's product upside down. <bookmark mark='p'/> One over zeta is a product of factors "
            "one minus p to the minus s. <bookmark mark='x'/> Multiply it out: each squarefree number appears once, with a sign "
            "for each prime in it. <bookmark mark='m'/> Those signs are exactly mu. One over zeta of s is the sum of mu of n "
            "over n to the s."
        ) as vo:
            vo.wait_until("p")
            self.play(Write(f[:3]))
            vo.wait_until("x")
            self.play(Write(f[3:]))
            vo.wait_until("m")
            self.play(Write(g))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def walk(self):
        d = load("mobius")
        xs, M = d["x"].astype(float), d["M"].astype(float)
        N = int(xs[-1])
        step = 4
        xs, M = xs[::step], M[::step]
        top = Axes(x_range=[0, N, N // 5], y_range=[-4000, 4000, 2000], x_length=11.2, y_length=2.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "font_size": 20},
                   x_axis_config={"include_numbers": False}, y_axis_config={"include_numbers": True})
        bot = top.copy()
        VGroup(top, bot).arrange(DOWN, buff=0.75).move_to(DOWN * 0.35 + RIGHT * 0.4)
        env = lambda ax: VGroup(*[ax.plot(lambda x, s=s: s * np.sqrt(x), x_range=[1, N, N / 400], color=GREY_A, stroke_width=1.5)
                                   .set_stroke(opacity=0.6) for s in (1, -1)])
        m_curve = polyline(top, xs, M, color=C.MOBIUS, stroke_width=2)
        rng = np.random.default_rng(2)  # a seed whose walk fits the same axes as M(x)
        steps = rng.choice([1, -1], size=N) * (rng.random(N) < 6 / np.pi**2)
        R = np.concatenate([[0], np.cumsum(steps)])[xs.astype(int)]
        r_curve = polyline(bot, xs, R, color=GREY_A, stroke_width=2)
        tl = label(r"$M(x) = \mu(1) + \mu(2) + \cdots + \mu(x)$, \ up to $x = 10^7$", font_size=28, color=C.MOBIUS).next_to(top, UP, buff=0.12)
        bl = label(r"a random walk: \ $\pm1$ coin flips (and a 0 as often as $\mu$ has one)", font_size=28, color=GREY_A).next_to(bot, UP, buff=0.12)
        sq = MathTex(r"\pm\sqrt{x}", font_size=28, color=GREY_A).next_to(top.c2p(0.93 * N, np.sqrt(0.93 * N)), UP, buff=0.12)
        ten7 = MathTex(r"10^7", font_size=24).next_to(bot.c2p(N, -4000), DOWN, buff=0.1)
        ratio = float(d["max_ratio_beyond_200"][0])
        Mmax = int(d["M_max_abs"][0])

        with self.voiceover(
            "Now add up the signs. <bookmark mark='m'/> M of x is the running total of mu, here all the way out to ten million. "
            "<bookmark mark='r'/> It wanders up and down like a random walk, <bookmark mark='c'/> just like a running tally of "
            "coin flips."
        ) as vo:
            vo.wait_until("m")
            self.play(Create(top), FadeIn(tl), FadeIn(ten7))
            self.play(Create(m_curve), run_time=3, rate_func=linear)
            vo.wait_until("r")
            self.play(Create(bot), FadeIn(bl))
            vo.wait_until("c")
            self.play(Create(r_curve), run_time=2.5, rate_func=linear)

        e1, e2 = env(top), env(bot)
        with self.voiceover(
            "A random walk of x steps typically drifts about the square root of x away from zero. <bookmark mark='e'/> And so "
            "does M. Up to ten million, it never gets more than about 0.57 times the square root of x away, once x is past a "
            "couple hundred."
        ) as vo:
            vo.wait_until("e")
            self.play(Create(e1), Create(e2), FadeIn(sq))
        assert 0.5 < ratio < 0.6 and Mmax < 2000

        self.play(FadeOut(VGroup(bot, r_curve, bl, e2)), FadeOut(ten7))
        eq = VGroup(
            MathTex(r"\text{RH}", r"\iff", r"M(x) = O\big(x^{1/2 + \varepsilon}\big)\ \text{ for every } \varepsilon > 0", font_size=42),
            note(r"J.\ E.\ Littlewood, 1912", font_size=24),
        ).arrange(DOWN, buff=0.15).move_to(bot.get_center() + UP * 0.2)
        eq[0][2].set_color(C.MOBIUS)
        mertens = note(r"(Mertens guessed $|M(x)| < \sqrt{x}$ always; Odlyzko and te Riele showed in 1985 that this eventually fails, barely.)",
                       font_size=24).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here's the remarkable fact. <bookmark mark='r'/> The Riemann hypothesis is true exactly when M of x stays below x to "
            "the one half plus epsilon, for every epsilon. In other words, the signs of mu are as random as coin flips, in the "
            "strongest sense. <bookmark mark='m'/> Square-root cancellation."
        ) as vo:
            vo.wait_until("r")
            self.play(FadeIn(eq, shift=UP * 0.2))
            vo.wait_until("m")
            self.play(FadeIn(mertens))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def logic(self):
        steps = VGroup(
            MathTex(r"\Big|\sum_{n \le x} \mu(n)\Big| \le C\,x^{\theta}", font_size=40),
            MathTex(r"\sum_{n} \frac{\mu(n)}{n^s} \ \text{converges when } \Real(s) > \theta", font_size=40),
            MathTex(r"\frac{1}{\zeta(s)} \ \text{is finite when } \Real(s) > \theta", font_size=40),
            MathTex(r"\zeta(s) \ne 0 \ \text{ when } \Real(s) > \theta", font_size=40, color=C.ZERO_FREE),
        ).arrange(DOWN, buff=0.75).move_to(LEFT * 3.6)
        steps[0].set_color(C.MOBIUS)
        arrows = VGroup(*[Arrow(steps[i].get_bottom(), steps[i + 1].get_top(), buff=0.1, color=GREY_B) for i in range(3)])
        why = VGroup(
            label(r"partial summation", font_size=24, color=GREY_A),
            label(r"it equals $1/\zeta$ wherever it converges", font_size=24, color=GREY_A),
            label(r"a zero of $\zeta$ would make $1/\zeta$ infinite", font_size=24, color=GREY_A),
        )
        for w, a in zip(why, arrows):
            w.next_to(a, RIGHT, buff=0.25)
        head = label(r"Why cancellation keeps zeros away", font_size=34).to_corner(UL, buff=0.4)
        VGroup(steps, arrows, why).shift(DOWN * 0.25)

        with self.voiceover(
            "Why does cancellation in mu keep zeros away? Follow the chain. <bookmark mark='a'/> Suppose the partial sums of mu "
            "grow no faster than x to some power theta. <bookmark mark='b'/> Then the series for one over zeta converges whenever "
            "the real part of s is bigger than theta. <bookmark mark='c'/> A convergent series gives a finite number, so one "
            "over zeta is finite there. <bookmark mark='d'/> But at a zero of zeta, one over zeta would be infinite. So there "
            "are no zeros to the right of theta."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(why[0]), FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(why[1]), FadeIn(steps[2]))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[2]), FadeIn(why[2]), FadeIn(steps[3]))

        key = VGroup(
            label(r"To keep zeros out of $\Real(s) > \theta$,\\it's enough to show that M\"obius sums\\beat the trivial bound $x$\\"
                  r"by a fixed power:", font_size=28),
            MathTex(r"\sum_{n \le x} \mu(n) \ll x^{\theta}, \quad \theta < 1", font_size=36, color=C.MOBIUS),
            label(r"(the new proof does this for a smoothed,\\twisted version of this sum)", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 4.35)
        box = SurroundingRectangle(key, color=YELLOW, buff=0.25, corner_radius=0.1)
        with self.voiceover(
            "So to keep zeros out of a half-plane, it's enough to show the Möbius function cancels: <bookmark mark='p'/> that its "
            "sums beat the trivial bound, x, by some fixed power. A bound like x to the seven eighths would mean no zeros beyond "
            "seven eighths. <bookmark mark='s'/> That is precisely the shape of OpenAI's argument, applied to a smoothed and "
            "twisted version of this sum."
        ) as vo:
            self.play(FadeIn(key[0]), Create(box))
            vo.wait_until("p")
            self.play(Write(key[1]))
            vo.wait_until("s")
            self.play(FadeIn(key[2]))
        self.wait(0.8)
        self.clear_scene()
