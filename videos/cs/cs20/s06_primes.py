from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono)


class Primes(VoiceoverScene):
    def construct(self):
        self.card()
        self.fermat()
        self.carmichael()
        self.miller_rabin()
        self.measured()

    def card(self):
        card = chapter_card(5, r"Probable primes and primality tests", r"Is a 300-digit number prime?", lit=(1976, 2002),
                            extra=((1976, r"Miller's test"), (2002, r"PRIMES is in P")), part=PART)
        with self.voiceover((
            'Chapter five. Probable primes and primality tests.'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def fermat(self):
        head = label(r"Fermat's little theorem as a test", font_size=34).to_edge(UP, buff=0.35)
        why = label(r"Part 30 needs primes of 300 digits: \ trial division would need $10^{150}$ divisions",
                    font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.35)
        thm = MathTex(r"n \text{ prime},\ \gcd(a, n) = 1 \quad\Longrightarrow\quad a^{\,n-1} \equiv 1 \pmod n",
                      font_size=36, color=YES).next_to(why, DOWN, buff=0.5)
        ex = VGroup(
            MathTex(r"2^{90} \equiv 64 \pmod{91}", font_size=34, color=NO),
            label(r"so 91 is composite \ ($91 = 7 \times 13$), \ and we never factored it", font_size=22,
                  color=WHITE),
            MathTex(r"3^{90} \equiv 1 \pmod{91}", font_size=34, color=HEAD),
            label(r"base 3 is a \textbf{liar} for 91: \ it passes, \ though 91 is composite", font_size=22,
                  color=GREY_A),
            label(r"$a^{n-1} \bmod n$ costs about $\log_2 n$ squarings \ (repeated squaring, \ Part 16)",
                  font_size=20, color=LAM),
        ).arrange(DOWN, buff=0.25).next_to(thm, DOWN, buff=0.45)
        with self.voiceover(
            (
            'Part 30 will need prime numbers three hundred digits long, and lots of them. Testing one by trial '
            "division would take ten to the hundred and fifty divisions. <bookmark mark='a'/> Fermat's little "
            'theorem gives a shortcut. If n is prime, then for every a not divisible by n, a to the n minus one is '
            "one, modulo n. <bookmark mark='b'/> So if we find an a where it isn't, n is certainly composite. Two to"
            " the ninetieth, modulo ninety-one, is sixty-four, <bookmark mark='c'/> so ninety-one is composite, and "
            "we learned that without finding a factor. <bookmark mark='d'/> But some bases lie. Three to the "
            "ninetieth is one modulo ninety-one, as if ninety-one were prime. <bookmark mark='e'/> Each test is "
            'cheap: repeated squaring computes the power with about one squaring per bit of n.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(why))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(ex[0]))
            vo.wait_until("c")
            self.play(FadeIn(ex[1]))
            vo.wait_until("d")
            self.play(FadeIn(ex[2]), FadeIn(ex[3]))
            vo.wait_until("e")
            self.play(FadeIn(ex[4]))
        self.wait(0.3)
        self.clear_scene()

    def carmichael(self):
        d = load("primes")
        head = label('Composites that fool every coprime base', font_size=34).to_edge(UP, buff=0.35)
        n = d["n"]
        cells = VGroup()
        for a in range(1, 561):
            import math
            ok = math.gcd(a, n) == 1
            cells.add(Square(side_length=0.155, stroke_width=0, fill_color=NO if ok else GREY_D,
                             fill_opacity=0.85 if ok else 0.6))
        cells.arrange_in_grid(rows=14, cols=40, buff=0.025).next_to(head, DOWN, buff=0.45)
        cap = label(rf"$a = 1, \dots, 560$: \ red passes Fermat's test for $561 = 3 \cdot 11 \cdot 17$ \ "
                    rf"(all {d['fermat_liars']} bases coprime to it)", font_size=20, color=GREY_A
                    ).next_to(cells, DOWN, buff=0.2)
        facts = VGroup(
            label(r"Korselt (1899): \ $n$ is such a number iff it is squarefree and $p - 1 \mid n - 1$ for every "
                  r"prime $p \mid n$", font_size=20, color=WHITE),
            label(r"$560$ is divisible by $2$, \ $10$ and $16$", font_size=20, color=GREY_A),
            label(rf"Carmichael numbers below a million: \ {d['carmichael_count']}; \ infinitely many "
                  r"(Alford, Granville and Pomerance, 1994)", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            (
            f"Worse, some composites fool every coprime base. <bookmark mark='a'/> Here are the bases from one to "
            f'five hundred and sixty for n equals five hundred and sixty-one, which is three times eleven times '
            f'seventeen. Every base that shares no factor with it, all '
            f"{d['fermat_liars']}"
            f" of them, passes Fermat's test. <bookmark mark='b'/> Alwin Korselt explained why in 1899: this happens "
            f'exactly when n is squarefree and p minus one divides n minus one for each of its prime factors p. Five '
            f"hundred and sixty is divisible by two, ten and sixteen. <bookmark mark='c'/> Robert Carmichael found "
            f'the first examples in 1910. There are '
            f"{d['carmichael_count']}"
            f' below a million, and in 1994 Alford, Granville and Pomerance proved there are infinitely many. '
            f"Fermat's test needs repairing."
        )
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.004), run_time=3.0)
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    def miller_rabin(self):
        d = load("primes")
        head = label(r"Miller--Rabin: \ listen to the square roots", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"modulo a prime, \ $x^2 \equiv 1$ only for $x \equiv \pm 1$ \ (a field has no zero divisors: "
                  r"$(x-1)(x+1) = 0$)", font_size=21, color=WHITE),
            MathTex(r"n - 1 = 2^s d,\ d \text{ odd}: \qquad a^d,\ a^{2d},\ a^{4d},\ \dots,\ a^{2^s d} = a^{n-1}",
                    font_size=32, color=LAM),
            label(r"for a prime, \ the sequence is all $1$s, \ or reaches $-1$ before the first $1$", font_size=21,
                  color=WHITE),
            MathTex(r"561 - 1 = 2^4 \cdot 35: \quad 2^{35} \equiv 263,\ \ 263^2 \equiv 166,\ \ 166^2 \equiv 67,\ \ "
                    r"67^2 \equiv 1", font_size=30, color=CTRL),
            label(r"$67 \not\equiv \pm 1$ squares to 1: \ a square root of 1 that a prime can't have, \ so 561 is "
                  r"composite", font_size=21, color=NO),
            label(rf"Rabin (1980): \ at most $\tfrac14$ of the bases lie; \ for 561, \ {d['strong_liars']} of 560",
                  font_size=22, color=YES),
            label(rf"worst odd composite below 20{{,}}000: \ $n = {d['worst_n']}$, \ exactly $\tfrac14$", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            (
            f"Gary Miller in 1976 and Michael Rabin in 1980 found the repair. <bookmark mark='a'/> Modulo a prime, "
            f'the only square roots of one are one and minus one, because x squared minus one factors as x minus one '
            f"times x plus one, and in a field a product is zero only if a factor is. <bookmark mark='b'/> Write n "
            f'minus one as a power of two times an odd number d, and compute a to the d, then keep squaring until we '
            f"reach a to the n minus one. <bookmark mark='c'/> For a prime, the sequence is all ones, or it hits "
            f"minus one somewhere before the first one. <bookmark mark='d'/> Watch five hundred and sixty-one with "
            f'base two: two hundred and sixty-three, one hundred and sixty-six, sixty-seven, then one. <bookmark '
            f"mark='e'/> Sixty-seven squares to one but isn't plus or minus one: a square root of one that no prime "
            f"can have. Fermat was fooled; this test isn't. <bookmark mark='f'/> Rabin proved that for every odd "
            f'composite, at most a quarter of the bases in our stated range, one through n minus one, lie. Five '
            f'hundred and sixty-one has only '
            f"{d['strong_liars']}"
            f". <bookmark mark='g'/> Searching every odd composite below twenty thousand, the worst was nine, with "
            f"exactly a quarter, so the bound can't be improved. Forty random bases give false acceptance of any "
            f'fixed odd composite at most four to the minus forty, about ten to the minus twenty-four.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("primes")
        head = label(r"Generating probable primes, \ in Python", font_size=34).to_edge(UP, buff=0.35)
        rows = [[f"{t['bits']}", f"{round(t['bits'] * 0.30103)}", f"{t['candidates']}",
                 (f"{t['seconds'] * 1000:.0f} ms" if t["seconds"] < 1 else f"{t['seconds']:.1f} s")]
                for t in d["times"]]
        tab = grid_table([r"bits", r"digits", r"odd candidates \ (asymptotic expectation)", r"time"], rows,
                         widths=[1.4, 1.6, 5.0, 2.0], row_h=0.48, font_size=21, mono_cols=(),
                         colors=[[DATA, DATA, GREY_A, YES]] * len(rows)).next_to(head, DOWN, buff=0.5)
        notes = VGroup(
            label(r"prime number theorem: \ about one in $\ln n$ numbers near $n$ is prime; \ half that among odd "
                  r"ones", font_size=21, color=WHITE),
            label(rf"most candidates fail the first round; \ one round at 1024 bits: \ "
                  rf"{d['round_1024'] * 1000:.1f} ms", font_size=21, color=GREY_A),
            label(r"AKS (2002): \ deterministic polynomial-time primality; \ this table benchmarks randomized screening", font_size=21, color=HEAD),
            label(r"40-round screening + 64-round rescreen; \ no primality certificate is produced", font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            (
            'Now generate probable primes: choose random odd candidates of the requested bit length and keep one '
            "that passes forty Miller–Rabin rounds. Passing is not a primality certificate. <bookmark mark='a'/> The"
            ' prime number theorem suggests roughly three hundred and fifty odd candidates for a 1024-bit search; it'
            " is an asymptotic expectation, not a fixed search budget. <bookmark mark='b'/> The table reports "
            'complete generation times: the minimum of three for the smaller sizes and one observed run for 2048 '
            'bits. Every resulting candidate gets sixty-four additional independent screening rounds outside the '
            'timer, still without becoming a certified prime. Modular-power benchmarks are separate and exclude '
            "choosing their base. <bookmark mark='c'/> Agrawal, Kayal and Saxena proved deterministic polynomial-"
            "time primality testing in 2002. <bookmark mark='d'/> Practical prime generation often uses randomized "
            'screening or other tests and certificates. Cryptography also uses elliptic curves; not every secure '
            'connection generates random primes.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
