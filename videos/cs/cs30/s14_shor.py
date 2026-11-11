from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono)


class Shor(VoiceoverScene):
    def construct(self):
        self.card()
        self.period()
        self.harvest()

    def card(self):
        card = chapter_card(13, r"Shor's threat", r"What would a quantum computer break?", lit=(1994, 2024),
                            extra=((1994, r"Shor"), (2024, r"FIPS 203, \ 204, \ 205")), part=PART)
        with self.voiceover("Chapter thirteen. Shor's threat."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def period(self):
        s = load("shor")["rows"]
        head = label(r"Factoring is finding a period", font_size=34).to_edge(UP, buff=0.3)
        r0 = s[0]
        cells = VGroup()
        for k, v in enumerate(r0["powers"]):
            sq = Square(side_length=0.62, stroke_color=GREY_B, fill_color=HEAD if v == 1 else BG,
                        fill_opacity=0.3 if v == 1 else 1)
            cells.add(VGroup(sq, mono(str(v), 20, WHITE).move_to(sq), mono(str(k), 14, GREY_C).next_to(sq, UP,
                                                                                                       buff=0.06)))
        cells.arrange(RIGHT, buff=0.06).next_to(head, DOWN, buff=0.9)
        cl = label(rf"${r0['a']}^k \bmod {r0['N']}$", font_size=22, color=GREY_A).next_to(cells, LEFT, buff=0.3)
        br = Brace(cells[:r0["r"]], DOWN, color=YES)
        bl = label(rf"period $r = {r0['r']}$", font_size=20, color=YES).next_to(br, DOWN, buff=0.1)
        others = VGroup(*[label(rf"$N = {r['N']}$, \ $a = {r['a']}$: \ $r = {r['r']}$, \ factors "
                                rf"$\gcd(a^{{r/2}} \pm 1, N) = {r['f1']}, {r['f2']}$", font_size=21, color=GREY_A)
                          for r in s[1:]]).arrange(DOWN, buff=0.12)
        lines = VGroup(
            label(rf"$a^r \equiv 1$, \ so $N \mid (a^{{r/2}} - 1)(a^{{r/2}} + 1)$: \ $\gcd(7^2 - 1, 15) = {r0['f1']}$, "
                  rf"\ $\gcd(7^2 + 1, 15) = {r0['f2']}$", font_size=22, color=WHITE),
            others,
            label(r"classically, \ finding the period is as hard as factoring", font_size=22, color=NO),
            label(r"\textbf{Shor} \ (1994): \ a quantum computer finds it in polynomial time, \ with the quantum "
                  r"Fourier transform \ (Part 53)", font_size=22, color=YES),
            label(r"the same algorithm takes discrete logarithms: \ RSA, \ Diffie--Hellman, \ and elliptic curves "
                  r"all fall", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.22).next_to(bl, DOWN, buff=0.45)
        with self.voiceover(
            "Every public-key system so far rests on factoring or discrete logarithms. In 1994 Peter Shor showed that a "
            "quantum computer could do both. The key is that factoring reduces to finding a period. <bookmark "
            "mark='a'/> Take N equals fifteen and a equals seven, and list the powers of seven mod fifteen: one, seven, "
            "four, thirteen, one, and around again. The period is four. <bookmark mark='b'/> Seven to the fourth is "
            "one, so fifteen divides seven squared minus one times seven squared plus one, and the gcds give three and "
            "five. <bookmark mark='c'/> The same works for twenty-one and thirty-five. <bookmark mark='d'/> For a "
            "large N, the period is astronomically long, and no classical method finds it faster than factoring "
            "itself. <bookmark mark='e'/> A quantum computer can put all the powers in superposition and read the "
            "period off with the quantum Fourier transform, in polynomial time. Part 53 builds it, and factors fifteen "
            "on our simulator. <bookmark mark='f'/> The same idea solves discrete logarithms, in any group. RSA, "
            "Diffie-Hellman and elliptic curves fall together."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cl), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.2), run_time=2.5)
            self.play(GrowFromCenter(br), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
            vo.wait_until("f")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def harvest(self):
        head = label(r"Harvest now, \ decrypt later", font_size=34).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"today's largest quantum computers: \ about a thousand noisy physical qubits", font_size=22,
                  color=WHITE),
            label(r"breaking RSA-2048 needs error-corrected qubits: \ under a million noisy ones, \ for about a week "
                  r"\ (Gidney, 2025)", font_size=22, color=HEAD),
            label(r"nobody knows when: \ estimates range from a decade to never", font_size=22, color=GREY_A),
            label(r"but traffic recorded \textbf{today} can be decrypted \textbf{then}: \ secrets with a long life are "
                  r"already at risk", font_size=22, color=NO),
            label(r"NIST, \ August 2024: \ ML-KEM \ (FIPS 203), \ ML-DSA \ (204), \ SLH-DSA \ (205); \ HQC added in "
                  r"2025", font_size=22, color=YES),
            label(r"browsers and big websites already combine X25519 \textbf{with} ML-KEM: \ \textbf{hybrid}, \ secure "
                  r"if either holds", font_size=22, color=DATA),
            label(r"symmetric cryptography survives: \ Grover only halves key bits \ (Part 29)", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "How close is the threat? <bookmark mark='a'/> The largest quantum computers today have about a thousand "
            "physical qubits, too noisy for Shor's algorithm at any useful size. <bookmark mark='b'/> Breaking a "
            "two-thousand-bit RSA key needs error correction, Part 28's subject transplanted into quantum hardware; a "
            "2025 estimate by Craig Gidney put it at under a million noisy qubits running for about a week. <bookmark "
            "mark='c'/> When such a machine will exist, nobody knows. <bookmark mark='d'/> But an adversary can record "
            "encrypted traffic now and decrypt it whenever the machine arrives, so any secret that must last a decade "
            "is already exposed. <bookmark mark='e'/> In August 2024 the US standards institute published the first "
            "post-quantum standards: a key-encapsulation mechanism, ML-KEM, and two signature schemes. <bookmark "
            "mark='f'/> Browsers and large websites have already switched on hybrid key exchange, X25519 together with "
            "ML-KEM, which stays secure as long as either one does. <bookmark mark='g'/> Symmetric cryptography is in "
            "much better shape: Grover's algorithm only halves the effective key length. The next chapter builds the "
            "mathematics under ML-KEM."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
