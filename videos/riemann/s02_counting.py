from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import part_card, PI_POWERS_OF_TEN, fmt_int, label, load, note, polyline
from videos.riemann.compute import li


def table(rows, col_colors, font_size=30, h_buff=0.7, v_buff=0.2, aligns=None) -> VGroup:
    """rows: list of lists of TeX strings (first row = header). Columns right-aligned."""
    mobs = [[MathTex(c, font_size=font_size) if i else Tex(c, font_size=font_size - 2, color=GREY_B)
             for c in r] for i, r in enumerate(rows)]
    ncol = len(rows[0])
    widths = [max(m[j].width for m in mobs) for j in range(ncol)]
    heights = [max(m.height for m in r) for r in mobs]
    g = VGroup()
    y = 0.0
    for i, r in enumerate(mobs):
        x = 0.0
        row = VGroup()
        for j, m in enumerate(r):
            if i:
                m.set_color(col_colors[j])
            align = (aligns or ["r"] * ncol)[j]
            if align == "r":
                m.move_to([x + widths[j] - m.width / 2, y, 0])
            else:
                m.move_to([x + widths[j] / 2, y, 0])
            row.add(m)
            x += widths[j] + h_buff
        g.add(row)
        y -= heights[i] / 2 + v_buff + (heights[i + 1] / 2 if i + 1 < len(mobs) else 0)
    g.center()
    return g


class CountingPrimes(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.ratio_table()
        self.density()
        self.error_table()

    def card(self):
        c = part_card(1, r"The Riemann hypothesis", r"primes, zeta, and its zeros")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.8)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def definition(self):
        primes = load("primes")["primes"]
        nl = NumberLine(x_range=[0, 30, 1], length=12.5, include_numbers=True, font_size=24, color=GREY_B,
                        numbers_to_exclude=[]).shift(DOWN * 0.3)
        dots = VGroup(*[Dot(nl.n2p(p), radius=0.09, color=C.PRIME) for p in primes[primes <= 30]])
        defn = MathTex(r"\pi(x)", r"=", r"\text{number of primes} \le x", font_size=48).to_edge(UP, buff=0.8)
        defn[0].set_color(C.PRIME)
        disclaim = note(r"(just the letter $p$, for prime; nothing to do with $3.14159\ldots$)", font_size=26)
        disclaim.next_to(defn, DOWN, buff=0.25)
        brace = Brace(VGroup(Dot(nl.n2p(0.6)), Dot(nl.n2p(10.4))), DOWN, buff=0.45)
        b_l = MathTex(r"\pi(10) = 4", font_size=38, color=C.PRIME).next_to(brace, DOWN, buff=0.15)
        brace2 = Brace(VGroup(Dot(nl.n2p(0.6)), Dot(nl.n2p(29.4))), DOWN, buff=1.5)
        b2_l = MathTex(r"\pi(30) = 10", font_size=38, color=C.PRIME).next_to(brace2, DOWN, buff=0.15)
        assert np.count_nonzero(primes <= 10) == 4 and np.count_nonzero(primes <= 30) == 10

        with self.voiceover(
            "Let's start with the most basic question. How many primes are there up to some number x? "
            "<bookmark mark='d'/> Call that count pi of x. <bookmark mark='n'/> The pi here has nothing to do with circles; "
            "it's just the letter p, for prime. <bookmark mark='t'/> There are four primes up to ten, <bookmark mark='u'/> and ten "
            "primes up to thirty."
        ) as vo:
            self.play(Create(nl), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(Write(defn))
            vo.wait_until("n")
            self.play(FadeIn(disclaim))
            vo.wait_until("t")
            self.play(GrowFromCenter(brace), FadeIn(b_l))
            vo.wait_until("u")
            self.play(GrowFromCenter(brace2), FadeIn(b2_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def ratio_table(self):
        ks = list(range(1, 10))
        rows = [[r"$x$", r"$\pi(x)$", r"$x / \pi(x)$"]]
        ratios = []
        for k in ks:
            p = PI_POWERS_OF_TEN[k]
            ratios.append(10**k / p)
            rows.append([rf"10^{{{k}}}", fmt_int(p), f"{10**k / p:.2f}"])
        t = table(rows, [WHITE, C.PRIME, GREY_A], font_size=34, h_buff=1.1, v_buff=0.17)
        t.move_to(LEFT * 1.5 + DOWN * 0.1)
        diffs = VGroup()
        for i in range(2, len(rows)):
            d = ratios[i - 1] - ratios[i - 2]
            m = MathTex(rf"+{d:.2f}", font_size=26, color=YELLOW)
            m.move_to((t[i - 1][2].get_right() + t[i][2].get_right()) / 2 + RIGHT * 0.75)
            diffs.add(m)
        ln10 = MathTex(r"\ln 10 = 2.3026\ldots", font_size=36, color=YELLOW).next_to(diffs, RIGHT, buff=0.7).shift(DOWN * 1.2)
        avg = note(r"average gap between primes", font_size=24).next_to(t[0][2], UP, buff=0.15)
        assert abs(ratios[-1] - ratios[-2] - np.log(10)) < 0.01

        with self.voiceover(
            "Here are the real counts, going up by powers of ten. <bookmark mark='a'/> Up to a thousand, there are 168 primes. "
            "<bookmark mark='b'/> Up to a million, 78,498. <bookmark mark='c'/> Up to a billion, about fifty-one million."
        ) as vo:
            self.play(FadeIn(t[0]))
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1])) for r in t[1:]], lag_ratio=0.15), run_time=2.0)
            for m, i in zip("abc", [3, 6, 9]):
                vo.wait_until(m)
                self.play(Indicate(t[i][1], color=C.PRIME), run_time=0.8)

        with self.voiceover(
            "Now look at the ratio, x over pi of x. <bookmark mark='g'/> That's the average gap between consecutive primes. "
            "<bookmark mark='d'/> Each time x grows by a factor of ten, the average gap grows by about 2.3, "
            "<bookmark mark='l'/> which is the natural logarithm of ten."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r[2]) for r in t[1:]], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("g")
            self.play(FadeIn(avg))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d, shift=LEFT * 0.1) for d in diffs], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("l")
            self.play(Write(ln10))
        self.clear_scene()

    # ------------------------------------------------------------------
    def density(self):
        primes = load("primes")["primes"]
        ax = Axes(x_range=[0, 100, 10], y_range=[0, 1.05, 0.25], x_length=9.0, y_length=4.2,
                  axis_config={"stroke_color": GREY_B, "include_numbers": True, "font_size": 22},
                  tips=False).move_to(DOWN * 0.9 + LEFT * 0.6)
        dens = ax.plot(lambda t: 1 / np.log(t), x_range=[2, 100], color=C.SMOOTH, stroke_width=4)
        dl = MathTex(r"\frac{1}{\ln t}", font_size=40, color=C.SMOOTH).next_to(ax.c2p(12, 1 / np.log(12)), UR, buff=0.15)
        gauss = label(r"Gauss, as a teenager (c.\ 1792):\\near $x$, a fraction of about $1/\ln x$ of numbers are prime",
                      font_size=32).to_edge(UP, buff=0.4)
        lo, hi = 990_000, 1_000_000
        frac = np.count_nonzero((primes > lo) & (primes <= hi)) / (hi - lo)
        ex = VGroup(
            MathTex(r"x = 10^6:\quad \frac{1}{\ln x} \approx \frac{1}{13.8}", font_size=34),
            label(rf"(measured just below a million: 1 in {1 / frac:.1f})", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_corner(DR, buff=0.5).shift(UP * 1.8)
        assert abs(1 / frac - np.log(1e6)) < 0.6

        with self.voiceover(
            "As a teenager, Gauss noticed this pattern, and guessed that near a number x, the primes have density about one "
            "over the logarithm of x. <bookmark mark='e'/> For example, a random number near a million is prime with "
            "probability about one in fourteen."
        ) as vo:
            self.play(FadeIn(gauss))
            self.play(Create(ax), Create(dens), FadeIn(dl))
            vo.wait_until("e")
            self.play(FadeIn(ex))

        area = ax.get_area(dens, x_range=[2, 60], color=C.SMOOTH, opacity=0.35)
        li_def = MathTex(r"\li(x)", r"\approx", r"\int_2^x \frac{dt}{\ln t}", font_size=44)
        li_def[0].set_color(C.SMOOTH)
        li_def.next_to(ax.c2p(60, 0.75), RIGHT, buff=0.3)
        xmark = MathTex("x", font_size=30).next_to(ax.c2p(60, 0), DOWN, buff=0.35)
        with self.voiceover(
            "Add up that density, and you get the logarithmic integral, <bookmark mark='l'/> li of x: the area under the curve "
            "one over log t. That's the smooth curve we saw a moment ago."
        ) as vo:
            self.play(FadeOut(ex))
            self.play(FadeIn(area), FadeIn(xmark))
            vo.wait_until("l")
            self.play(Write(li_def))

        pnt = VGroup(
            label(r"\textbf{Prime number theorem}\\(Hadamard; de la Vall\'ee Poussin, 1896)", font_size=30),
            MathTex(r"\frac{\pi(x)}{\li(x)} \;\longrightarrow\; 1", font_size=46),
        ).arrange(DOWN, buff=0.3)
        pnt[1][0][0:4].set_color(C.PRIME)
        pnt[1][0][5:10].set_color(C.SMOOTH)
        pnt_bg = SurroundingRectangle(pnt, color=YELLOW, buff=0.3, corner_radius=0.1).set_fill(BACKGROUND, opacity=0.95)
        VGroup(pnt_bg, pnt).move_to(RIGHT * 3.6 + UP * 0.9)
        with self.voiceover(
            "The prime number theorem, <bookmark mark='p'/> proved in 1896 by Hadamard and by de la Vallée Poussin, says "
            "Gauss was right in the limit: the ratio of pi of x to li of x tends to one."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeOut(li_def), FadeIn(pnt_bg), FadeIn(pnt))
        self.clear_scene()

    # ------------------------------------------------------------------
    def error_table(self):
        d = load("primes")
        ks = [int(k) for k in d["k"]]
        lmp = {k: int(v) for k, v in zip(ks, d["li_minus_pi"])}
        show = [3, 6, 9, 12, 15, 18, 21, 24]
        rows = [[r"$x$", r"$\pi(x)$", r"$\mathrm{li}(x) - \pi(x)$", r"$\sqrt{x}$"]]
        for k in show:
            rows.append([rf"10^{{{k}}}", fmt_int(PI_POWERS_OF_TEN[k]), fmt_int(lmp[k]), rf"10^{{{k // 2}}}" if k % 2 == 0
                         else rf"10^{{{k / 2:.1f}}}"])
        t = table(rows, [WHITE, C.PRIME, C.ZERO, GREY_B], font_size=30, h_buff=0.75, v_buff=0.16)
        t.move_to(DOWN * 0.2)
        head = label(r"How good is the approximation?", font_size=40).to_edge(UP, buff=0.35)
        src = note(r"$\pi(x)$: sieved here up to $10^9$; beyond, OEIS A006880", font_size=20)
        src.to_corner(DL, buff=0.25)
        last = t[-1]
        b1 = Brace(last[1], DOWN, buff=0.1, color=C.PRIME)
        b1l = label(rf"{len(str(PI_POWERS_OF_TEN[24]))} digits", font_size=26, color=C.PRIME).next_to(b1, DOWN, buff=0.08)
        b2 = Brace(last[2], DOWN, buff=0.1, color=C.ZERO)
        b2l = label(rf"{len(str(lmp[24]))} digits", font_size=26, color=C.ZERO).next_to(b2, DOWN, buff=0.08)
        assert len(str(lmp[24])) * 2 <= len(str(PI_POWERS_OF_TEN[24])) + 1

        with self.voiceover(
            "But how good is this approximation, really? <bookmark mark='t'/> Here is the error, li of x minus pi of x, all "
            "the way out to ten to the twenty-four. <bookmark mark='s'/> The error is tiny compared with the count. "
            "<bookmark mark='h'/> In fact, it has only about half as many digits."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("t")
            self.play(FadeIn(t[0][:3]))
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:3])) for r in t[1:]], lag_ratio=0.12), FadeIn(src), run_time=2.5)
            vo.wait_until("s")
            self.play(Indicate(VGroup(*[r[2] for r in t[1:]]), color=C.ZERO, scale_factor=1.05))
            vo.wait_until("h")
            self.play(GrowFromCenter(b1), FadeIn(b1l), GrowFromCenter(b2), FadeIn(b2l))

        q = label(r"Is the error \emph{always} about $\sqrt{x}$ (or less)? \quad That is the Riemann hypothesis.",
                  font_size=34, color=YELLOW).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Half as many digits means the error is around the square root of x, or even a bit less. "
            "<bookmark mark='q'/> Does that stay true forever? That question is exactly the Riemann hypothesis. And to see "
            "why, we need Riemann's function."
        ) as vo:
            self.play(FadeOut(VGroup(b1, b1l, b2, b2l)))
            self.play(FadeIn(t[0][3]), LaggedStart(*[FadeIn(r[3]) for r in t[1:]], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("q")
            self.play(FadeOut(src), FadeIn(q, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
