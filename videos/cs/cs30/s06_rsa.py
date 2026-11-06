from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono)


class Rsa(VoiceoverScene):
    def construct(self):
        self.card()
        self.toy()
        self.why()
        self.real()
        self.textbook()

    def card(self):
        card = chapter_card(5, r"RSA", r"Can a key be public and still lock a secret?", lit=(1977,),
                            extra=((1977, r"Rivest, \ Shamir, \ Adleman"),), part=PART)
        with self.voiceover("Chapter five. RSA."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def toy(self):
        s = load("rsa")["small"]
        head = label(r"RSA with small numbers", font_size=34).to_edge(UP, buff=0.3)
        rows = [(r"pick two primes", rf"$p = {s['p']}$, \ $q = {s['q']}$", WHITE),
                (r"multiply", rf"$n = pq = {s['n']}$ \ (public)", DATA),
                (r"count the coprimes", rf"$\varphi(n) = (p-1)(q-1) = {s['phi']}$ \ (secret)", GREY_A),
                (r"public exponent", rf"$e = {s['e']}$, \ with $\gcd(e, \varphi) = 1$", DATA),
                (r"private exponent", rf"$d = e^{{-1}} \bmod \varphi = {s['d']}$ \ (chapter 2's Euclid)", HEAD),
                (r"encrypt", rf"$c = m^e \bmod n$: \ $m = {s['m']}$ $\to$ $c = {s['c']}$", YES),
                (r"decrypt", rf"$m = c^d \bmod n$: \ ${s['c']}^{{{s['d']}}} \bmod {s['n']} = {s['m']}$", YES)]
        tab = VGroup()
        for a, b, c in rows:
            tab.add(VGroup(label(a, font_size=21, color=GREY_B), label(b, font_size=24, color=c)))
        for r in tab:
            r[1].next_to(r[0], RIGHT, buff=0.5)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.5)
        for r in tab:
            r[1].set_x(r[0].get_left()[0] + 3.4 + r[1].width / 2)
        note = label(r"anyone may encrypt with $(n, e)$; \ only the holder of $d$ \ (who knows $p$ and $q$) \ can "
                     r"decrypt", font_size=22, color=YES).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Diffie and Hellman described public-key encryption but did not build it. The next year Ron Rivest, Adi "
            "Shamir and Leonard Adleman did. <bookmark mark='a'/> Pick two primes, here sixty-one and fifty-three, and "
            "multiply them: three thousand two hundred and thirty-three. This product n is public. <bookmark mark='b'/> "
            "Count how many numbers below n share no factor with it: phi of n, which is easy only if you know the two "
            "primes: three thousand one hundred and twenty. <bookmark mark='c'/> Choose a public exponent, "
            "seventeen, and compute its inverse modulo phi with Euclid: two thousand seven hundred and fifty-three, "
            "the private exponent. <bookmark mark='d'/> To encrypt the message sixty-five, raise it to the seventeenth "
            "power mod n: two thousand seven hundred and ninety. To decrypt, raise that to the private exponent, and "
            "sixty-five comes back. <bookmark mark='e'/> The pair n and e can be published. Decrypting needs d, and "
            "computing d needs the primes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(tab[5]))
            self.play(FadeIn(tab[6]))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def why(self):
        head = label(r"Why decryption works", font_size=34).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"ed = 1 + k\,\varphi(n)", font_size=40, color=WHITE),
            MathTex(r"c^d = m^{ed} = m \cdot \bigl(m^{\varphi(n)}\bigr)^k \equiv m \cdot 1^k = m \pmod n",
                    font_size=40, color=YES),
        ).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.7)
        lines = VGroup(
            label(r"the middle step is Euler's theorem \ (chapter 3), \ for $m$ coprime to $n$", font_size=22,
                  color=WHITE),
            label(r"for the rare $m$ sharing a factor with $n$: \ check mod $p$ and mod $q$ separately, \ and combine "
                  r"by the \textbf{Chinese remainder theorem}", font_size=22, color=HEAD),
            label(r"security: \ from $n$ and $e$ alone, \ find $m$ from $m^e$: \ the \textbf{RSA problem}", font_size=22,
                  color=NO),
            label(r"factoring $n$ solves it; \ whether anything easier does is \textbf{open}", font_size=22,
                  color=DATA),
        ).arrange(DOWN, buff=0.25).next_to(eqs, DOWN, buff=0.7)
        with self.voiceover(
            "Why does this work? <bookmark mark='a'/> Because d is the inverse of e modulo phi of n, e times d is one "
            "more than a multiple of phi. <bookmark mark='b'/> So raising the ciphertext to d gives m to the e d, "
            "which is m times m to the phi, raised to some power. By Euler's theorem from chapter three, m to the phi "
            "is one, and m is left. <bookmark mark='c'/> Euler needs m to share no factor with n; for the vanishingly "
            "rare messages that do, check the equation modulo p and modulo q separately and combine the two with the "
            "Chinese remainder theorem. <bookmark mark='d'/> The security assumption is that, knowing only n and e, "
            "nobody can take e-th roots modulo n. <bookmark mark='e'/> Factoring n would break it. Whether there is "
            "an easier way to break it than factoring is still unknown."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
            vo.wait_until("e")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def real(self):
        r = load("rsa")
        head = label(r"A real key, \ from scratch", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"step", r"measured"], [
            [r"random odd 1024-bit numbers tried until one is prime", r", \ ".join(str(c) for c in r["cands"]) +
             rf" \ (expected about {r['expected_cands']:.0f})"],
            [r"Miller--Rabin \ (Part 20), \ 40 rounds per survivor", r"under half a second per prime"],
            [r"a 2048-bit key: \ $n$, \ $e = 65537$, \ $d$", rf"{r['keygen_s']:.1f} s"],
            [r"decrypt: \ $c^d \bmod n$ directly", rf"{r['plain_ms']:.0f} ms"],
            [r"decrypt with CRT: \ mod $p$ and mod $q$, \ then combine", rf"{r['crt_ms']:.1f} ms \ "
                                                                         rf"({r['plain_ms'] / r['crt_ms']:.1f}$\times$ faster)"],
        ], widths=[6.6, 4.6], row_h=0.6, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        nl = VGroup(label(r"$n$ = ", font_size=22, color=GREY_A), mono(r["n_hex"] + "...", 20, DATA)).arrange(
            RIGHT, buff=0.15).next_to(tab, DOWN, buff=0.45)
        lines = VGroup(
            label(r"primes are common: \ about one in $\ln 2^{1024} \approx 710$ numbers, \ one in 355 odd ones",
                  font_size=21, color=WHITE),
            label(r"the CRT works with half-size numbers: \ about four times less work, \ the reason every library "
                  r"keeps $p$ and $q$", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Real keys use primes of a thousand bits or more. <bookmark mark='a'/> To find one, pick a random odd "
            "number of the right size and test it with Part 20's Miller-Rabin test, and keep going until one passes. "
            "Primes are plentiful: by the prime number theorem, about one odd number in three hundred and fifty-five at "
            "this size is prime, and our three searches took three hundred and fifty-four, ninety-nine and three "
            "hundred and sixty tries. <bookmark mark='b'/> A complete two-thousand-bit key took under a second. "
            "<bookmark mark='c'/> Decrypting directly costs twenty-nine milliseconds. Decrypting modulo p and modulo q "
            "separately, with half-size numbers, and combining by the Chinese remainder theorem, costs nine: over "
            "three times faster, which is why every implementation keeps the primes in the private key."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1], *tab.cells[2])), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[4], *tab.cells[5])), FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def textbook(self):
        r = load("rsa")
        head = label(r"Textbook RSA is not secure", font_size=34).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"\textbf{deterministic}: \ the same message gives the same ciphertext \ (Part 29: \ not "
                  r"CPA-secure)", font_size=22, color=NO),
            label(r"\textbf{malleable}: \ $(c \cdot 2^e)^d = 2m$: \ multiply the ciphertext, \ multiply the message",
                  font_size=22, color=NO),
            label(rf"ours: \ \texttt{{PAY BOB \$100}} as a number, \ times $2^e$, \ decrypts to exactly twice it: \ "
                  rf"{'yes' if r['doubled_ok'] else 'no'}", font_size=22, color=WHITE),
            label(r"\textbf{OAEP} \ (Bellare and Rogaway, 1994): \ pad with randomness through two hash-based masks "
                  r"before encrypting", font_size=22, color=YES),
            label(rf"two encryptions of the same message now differ: \ {'yes' if r['oaep_differ'] else 'no'}; \ and "
                  rf"it decrypts to \texttt{{{r['oaep_back'].replace('$', chr(92) + '$')}}}", font_size=22,
                  color=YES),
            label(r"\textbf{signing}: \ $\sigma = H(m)^d$, \ checked as $\sigma^e = H(m)$: \ hash first, \ or "
                  r"$\sigma_1 \sigma_2$ signs $m_1 m_2$", font_size=22, color=HEAD),
            label(r"the trapdoor is the easy part: \ the padding is where RSA keeps failing \ (next chapter)",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Raising to a power is not yet encryption. <bookmark mark='a'/> Textbook RSA is deterministic, so by Part "
            "29's definition it is not secure: an attacker can encrypt guesses and compare. <bookmark mark='b'/> It is "
            "also malleable. Multiply a ciphertext by two to the e, and the message inside doubles. <bookmark "
            "mark='c'/> We encoded pay Bob one hundred dollars as a number, multiplied its ciphertext, and it decrypted "
            "to exactly twice the number. <bookmark mark='d'/> The standard fix is optimal asymmetric encryption "
            "padding, OAEP, from Mihir Bellare and Phillip Rogaway: mix the message with fresh randomness through two "
            "hash-based masks before encrypting. <bookmark mark='e'/> Now two encryptions of the same message differ, "
            "and the structure an attacker could exploit is gone. <bookmark mark='f'/> The same trapdoor signs: raise "
            "a hash of the message to the private exponent, and anyone can check it with the public one. Hashing first "
            "matters, because raw signatures multiply too. <bookmark mark='g'/> RSA's arithmetic has held for "
            "fifty years. The padding around it has not."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
