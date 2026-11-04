from __future__ import annotations

import numpy as np

from videos.stats.stats7.common import *  # noqa: F403


class Generators(VoiceoverScene):
    def construct(self):
        self.card()
        self.lehmer()
        self.clock()
        self.lattice()
        self.pcg()
        self.twister()
        self.tests()

    def card(self):
        card = chapter_card(1, r"Pseudo-random generators", r"Arithmetic that looks like chance", lit=(1949,), part=PART)
        with self.voiceover("Chapter one. Pseudo-random generators."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def lehmer(self):
        rows = [
            cmath(r"x_{k+1}", r"=", r"(a\,x_k + c) \bmod m", font_size=38),
            cmath(r"u_k", r"=", r"x_k / m \ \in [0, 1)", font_size=36),
        ]
        rows[0][2].set_color(GOOD)
        whys = [why(r"the linear congruential generator: \ Lehmer (1949), \ with $c = 0$"),
                why(r"divide by $m$ for a uniform")]
        facts = VGroup(label(r"fast, \ tiny, \ reproducible: \ the same seed gives the same sequence", font_size=24, color=GREY_A),
                       label(r"but its period is at most $m$, \ and its structure is linear", font_size=24, color=BAD))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In 1949 Derrick Lehmer proposed the scheme that dominated for fifty years. <bookmark mark='a'/> Keep "
            "one integer. To get the next, multiply by a constant a, add c, and take the remainder after dividing "
            "by m. <bookmark mark='b'/> Divide by m and you have a number between zero and one. <bookmark mark='c'/> "
            "It's fast, it needs almost no memory, and it's reproducible: the same starting seed always gives the "
            "same sequence, which is exactly what a scientist wants when a simulation must be checked. "
            "<bookmark mark='d'/> But it can never produce more than m different numbers before repeating, and its "
            "structure is linear, which is what doomed RANDU."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.8, buff=1.0, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(facts[0]))
            vo.wait_until("d")
            self.play(FadeIn(facts[1]))
        self.clear_scene()

    def ring(self, center, seq, color, title, m=64, r=2.1):
        c = np.asarray(center, float)
        pos = [c + r * np.array([np.sin(TAU * k / m), np.cos(TAU * k / m), 0]) for k in range(m)]
        dots = VGroup(*[Dot(p, radius=0.045, color=GREY_D) for p in pos])
        t = label(title, font_size=24, color=color).next_to(dots, UP, buff=0.35)
        path = VMobject(stroke_color=color, stroke_width=1.6, stroke_opacity=0.7)
        path.set_points_as_corners([pos[v] for v in seq])
        lit = VGroup(*[Dot(pos[v], radius=0.065, color=color) for v in sorted(set(seq))])
        return dots, t, path, lit

    def clock(self):
        d = load("lcg")
        bad, good = d["bad"], d["good"]
        d1, t1, p1, l1 = self.ring([-3.4, -0.6, 0], [1] + bad[:17], BAD, r"$a = 5,\ c = 0,\ m = 64$")
        d2, t2, p2, l2 = self.ring([3.4, -0.6, 0], [1] + good[:65], GOOD, r"$a = 5,\ c = 3,\ m = 64$")
        c1 = label(rf"period {d['per_bad']}: \ a quarter of the clock", font_size=24, color=BAD).next_to(d1, DOWN, buff=0.35)
        c2 = label(rf"period {d['per_good']}: \ every number, \ once", font_size=24, color=GOOD).next_to(d2, DOWN, buff=0.35)
        hd = label(r"Hull \& Dobell (1962): \ full period iff $c$ is coprime to $m$, \ $a - 1$ is divisible by every prime factor of "
                   r"$m$, \ and by 4 if $4 \mid m$", font_size=20, color=GREY_A).to_edge(UP, buff=0.3)
        if hd.width > 12.8:
            hd.width = 12.8
        with self.voiceover(
            "Picture the m possible values as hours on a clock, here with sixty-four of them. <bookmark mark='a'/> "
            "With a equal to five and no increment, starting at one, the generator hops around the clock and "
            "returns to where it started after only sixteen steps: three quarters of the values are never visited. "
            "<bookmark mark='b'/> Add an increment of three, and the same multiplier now visits every one of the "
            "sixty-four values before repeating. <bookmark mark='c'/> When that happens was worked out by Thomas "
            "Hull and Alan Dobell in 1962: three conditions on a, c and m. Real generators use m equal to two to the "
            "thirty-two or two to the sixty-four, and choose a with care."
        ) as vo:
            self.play(FadeIn(d1), FadeIn(d2), FadeIn(t1), FadeIn(t2))
            vo.wait_until("a")
            self.play(Create(p1), FadeIn(l1, lag_ratio=0.1), run_time=3.0)
            self.play(FadeIn(c1))
            vo.wait_until("b")
            self.play(Create(p2), FadeIn(l2, lag_ratio=0.02), run_time=4.0)
            self.play(FadeIn(c2))
            vo.wait_until("c")
            self.play(FadeIn(hd))
        self.clear_scene()

    def lattice(self):
        d = load("lcg")
        P = np.asarray(d["pairs"], float)
        A = axes([0, 256], [0, 256], x_length=5.0, y_length=5.0, xlabel=r"$x_k$", ylabel=r"$x_{k+1}$", xticks=[0, 128, 256],
                 yticks=[0, 128, 256], center=[-3.4, -0.4, 0])
        pts = scatter(A.ax, P[:, 0], P[:, 1], color=BAD, radius=0.035, opacity=0.9)
        rows = fit_rows(VGroup(
            MathTex(r"x_{k+1} = (37 x_k + 1) \bmod 256", font_size=30, color=BAD),
            label(r"all 256 pairs, \ on a handful of parallel lines", font_size=24),
            label(r"every LCG: \ pairs on lines, \ triples on planes, \ $d$-tuples on hyperplanes", font_size=24, color=GREY_A),
            label(r"the spectral test (Coveyou \& MacPherson 1967): \ the widest gap between hyperplanes", font_size=22,
                  color=GREY_B),
        ), 6.0, 0.3, [3.2, 0.4, 0])
        with self.voiceover(
            "The linear structure is easiest to see in pairs. <bookmark mark='a'/> Plot each value against the next, "
            "for a small generator modulo two hundred and fifty-six. <bookmark mark='b'/> The points aren't "
            "scattered; they sit on a few parallel lines. <bookmark mark='c'/> It's true of every linear "
            "congruential generator: pairs fall on lines, triples on planes, and d-tuples on hyperplanes. "
            "<bookmark mark='d'/> The spectral test, from 1967, measures the widest gap between those hyperplanes; "
            "a good multiplier makes the gaps small in every dimension that matters. RANDU's multiplier made them "
            "enormous in three."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.01), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def pcg(self):
        code = code_block([
            "state = state * 6364136223846793005 + inc   # a 64-bit LCG",
            "x = ((old >> 18) ^ old) >> 27              # xorshift: mix high bits down",
            "rot = old >> 59                            # top 5 bits choose a rotation",
            "out = rotate_right(x, rot)                 # 32 output bits",
        ], font_size=22).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            label(r"the state is a plain LCG, \ with period $2^{64}$", font_size=26),
            label(r"the output \emph{permutes} it: \ the rotation depends on the state, \ so no lattice survives", font_size=26,
                  color=GOOD),
            label(r"$2^{63}$ streams: \ different increments, \ independent sequences for parallel simulations", font_size=26,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -1.6, 0])
        hc = note(r"M. E. O'Neill, \ ``PCG: a family of simple fast space-efficient statistically good algorithms'' (2014)")
        hc.to_edge(DOWN, buff=0.3)
        built = label(r"Built: \ \texttt{statkit.random.PCG32}", font_size=24, color=S.ACCENT).to_corner(UR, buff=0.4)
        with self.voiceover(
            "Modern generators keep the speed and hide the structure. <bookmark mark='a'/> Here is PCG32, designed "
            "by Melissa O'Neill in 2014, in four lines. Its state is a sixty-four-bit linear congruential generator, "
            "with a period of two to the sixty-four. <bookmark mark='b'/> But it never outputs the state directly. "
            "It mixes the high bits down with a shift and an exclusive or, then rotates the result by an amount "
            "chosen by the state's own top five bits. That data-dependent rotation destroys the lattice. "
            "<bookmark mark='c'/> And by changing the increment you get two to the sixty-three separate streams, "
            "so parallel simulations never overlap. It's what we've built into statkit, and NumPy's default "
            "generator is its sixty-four-bit sibling."
        ) as vo:
            self.play(FadeIn(built), FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(code, shift=UP * 0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def tests(self):
        d = load("tests")
        r, p = d["randu"], d["pcg"]
        hdr = VGroup(*[label(t, font_size=26, color=GREY_A) for t in (r"test", r"RANDU", r"PCG32")])
        rows_ = [(r"$\chi^2$, \ 10 bins (1-D)", rf"$p = {r['p1']:.2f}$", rf"$p = {p['p1']:.2f}$", GOOD, GOOD),
                 (r"runs above / below the median", rf"$z = {r['runs_z']:+.2f}$", rf"$z = {p['runs_z']:+.2f}$", GOOD, GOOD),
                 (r"$\chi^2$, \ 1,000 cells (3-D)", r"$p = 5 \times 10^{-30}$", rf"$p = {p['p3']:.2f}$", BAD, GOOD)]
        tab = VGroup()
        xs = [-3.6, 1.4, 4.4]
        for j, h in enumerate(hdr):
            h.move_to([xs[j], 2.2, 0])
        for i, (t, a, b, ca, cb) in enumerate(rows_):
            y = 1.3 - 0.85 * i
            tab.add(label(t, font_size=26).move_to([xs[0], y, 0]), label(a, font_size=26, color=ca).move_to([xs[1], y, 0]),
                    label(b, font_size=26, color=cb).move_to([xs[2], y, 0]))
        line = Line([-6.4, 1.8, 0], [6.0, 1.8, 0], color=GREY_D)
        take = fit_rows(VGroup(
            label(r"a test can only reject: \ passing is evidence, \ never proof", font_size=26, color=S.ACCENT),
            label(r"modern batteries: \ TestU01's BigCrush (L'Ecuyer \& Simard 2007), \ 106 tests; \ PCG passes", font_size=22,
                  color=GREY_A),
        ), 12.6, 0.25, [0, -2.4, 0])
        tag = note(r"300,000 numbers from each").to_corner(UR, buff=0.3)
        with self.voiceover(
            "How do you test a generator? With statistics. <bookmark mark='a'/> Split three hundred thousand numbers "
            "into ten bins and compare the counts with a chi-squared test: both generators pass, with large p-values. "
            "<bookmark mark='b'/> Count runs above and below the median: both look like independent draws. "
            "<bookmark mark='c'/> Now group the numbers into triples and count them in a thousand little cubes. "
            "PCG passes. RANDU fails with a p-value of five times ten to the minus thirty: its triples avoid most of "
            "the cubes, because they live on fifteen planes. <bookmark mark='d'/> A test can only reject. Passing "
            "is evidence, never proof, so modern generators face batteries of over a hundred tests, like the "
            "BigCrush suite of Pierre L'Ecuyer and Richard Simard."
        ) as vo:
            self.play(FadeIn(hdr), Create(line), FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(tab[3 * k:3 * k + 3], shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(take))
        self.clear_scene()

    def twister(self):
        rows = fit_rows(VGroup(
            label(r"the Mersenne Twister \ (Matsumoto \& Nishimura, 1998)", font_size=28, color=S.MUSEUM),
            MathTex(r"\text{period } 2^{19937} - 1, \ \ 623\text{-dimensionally equidistributed}", font_size=30),
            label(r"the default in Python's \texttt{random}, \ in R, \ in MATLAB, \ for a quarter of a century", font_size=24,
                  color=GREY_A),
            label(r"but it is linear over the bits: \ it fails two of BigCrush's linear-complexity tests", font_size=24, color=BAD),
            label(r"and its 2.5 KB state recovers from a bad seed slowly", font_size=24, color=BAD),
            label(r"a long period is necessary, \ never sufficient", font_size=28, color=S.ACCENT),
        ), 12.6, 0.32, [0, 0.2, 0])
        with self.voiceover(
            "You've almost certainly used another generator. <bookmark mark='a'/> In 1998 Makoto Matsumoto and Takuji "
            "Nishimura published the Mersenne Twister. <bookmark mark='b'/> Its period is two to the nineteen thousand "
            "nine hundred and thirty-seven, minus one, a number with six thousand digits, and its output is evenly "
            "spread in up to six hundred and twenty-three dimensions. <bookmark mark='c'/> It became the default in "
            "Python, R and MATLAB. <bookmark mark='d'/> But it is linear in its bits, so it fails the tests in BigCrush "
            "that look for exactly that, <bookmark mark='e'/> and its large state recovers slowly from a seed with too "
            "many zeros. <bookmark mark='f'/> The lesson: an astronomically long period is necessary, but it is never "
            "enough."
        ) as vo:
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
