from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, flow_box, load, mono)


def person(name, color, pos):
    c = Circle(radius=0.42, stroke_color=color, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(pos)
    return VGroup(c, label(name, font_size=22, color=color).next_to(c, DOWN, buff=0.15))


class Hook(VoiceoverScene):
    def construct(self):
        self.listen()
        self.scale()
        self.plan()

    def listen(self):
        d = load("toydh")
        head = label(r"Agreeing on a secret, \ in public", font_size=36).to_edge(UP, buff=0.3)
        alice = person("Alice", DATA, [-4.6, 1.2, 0])
        bob = person("Bob", HEAD, [4.6, 1.2, 0])
        eve = person("Eve", NO, [0, -0.6, 0])
        pub = label(rf"public: \ $p = {d['p']}$, \ $g = {d['g']}$", font_size=26, color=WHITE).move_to([0, 2.2, 0])
        a_secret = label(rf"secret $a = {d['a']}$", font_size=22, color=DATA).next_to(alice, LEFT, buff=0.2).shift(
            UP * 0.2)
        b_secret = label(rf"secret $b = {d['b']}$", font_size=22, color=HEAD).next_to(bob, RIGHT, buff=0.2).shift(
            UP * 0.2)
        aA = Arrow([-3.9, 1.35, 0], [3.9, 1.35, 0], buff=0, stroke_width=2.5, color=DATA)
        aB = Arrow([3.9, 0.95, 0], [-3.9, 0.95, 0], buff=0, stroke_width=2.5, color=HEAD)
        tA = label(rf"$A = g^a \bmod p = {d['A']}$", font_size=22, color=DATA).next_to(aA, UP, buff=0.05)
        tB = label(rf"$B = g^b \bmod p = {d['B']}$", font_size=22, color=HEAD).next_to(aB, DOWN, buff=0.05)
        kA = label(rf"$B^a \bmod p = {d['s_alice']}$", font_size=24, color=YES).next_to(alice, DOWN, buff=0.6)
        kB = label(rf"$A^b \bmod p = {d['s_bob']}$", font_size=24, color=YES).next_to(bob, DOWN, buff=0.6)
        eve_sees = label(rf"Eve sees \ {d['p']}, \ {d['g']}, \ {d['A']}, \ {d['B']}: \ but not {d['s_alice']}",
                         font_size=22, color=NO).next_to(eve, DOWN, buff=0.35)
        lines = VGroup(
            label(r"both get $g^{ab}$: \ the same secret, \ never sent", font_size=23, color=YES),
            label(r"Diffie and Hellman \ (1976): \ ``We stand today on the brink of a revolution in cryptography''",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Alice and Bob have never met. They want a secret only they know, and every word they say is overheard "
            "by Eve. <bookmark mark='a'/> They agree in public on two numbers: a prime, twenty-three, and five. "
            "<bookmark mark='b'/> Alice picks a secret number, six, and Bob picks fifteen. Neither tells anyone. "
            "<bookmark mark='c'/> Alice sends five to the sixth power, reduced mod twenty-three: eight. Bob sends five "
            "to the fifteenth: nineteen. <bookmark mark='d'/> Now Alice raises Bob's nineteen to her six, and Bob "
            "raises Alice's eight to his fifteen. Both get two. <bookmark mark='e'/> Eve heard every number, "
            "twenty-three, five, eight and nineteen, and the secret two was never said. <bookmark mark='f'/> Both "
            "computed five to the power six times fifteen, by different routes. Whitfield Diffie and Martin Hellman "
            "published this in 1976, and it changed what cryptography could do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(alice), FadeIn(bob), FadeIn(eve))
            vo.wait_until("a")
            self.play(FadeIn(pub))
            vo.wait_until("b")
            self.play(FadeIn(a_secret), FadeIn(b_secret))
            vo.wait_until("c")
            self.play(GrowArrow(aA), FadeIn(tA))
            self.play(GrowArrow(aB), FadeIn(tB))
            vo.wait_until("d")
            self.play(FadeIn(kA), FadeIn(kB))
            vo.wait_until("e")
            self.play(FadeIn(eve_sees))
            vo.wait_until("f")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def scale(self):
        d = load("toydh")
        head = label(r"The same, \ at full size", font_size=36).to_edge(UP, buff=0.35)
        rows = VGroup(
            VGroup(label(r"$p$", font_size=24, color=GREY_A),
                   label(rf"a {d['big_bits']}-bit prime \ (RFC 3526, \ group 14)", font_size=22, color=WHITE)),
            VGroup(label(r"$A$", font_size=24, color=DATA), mono(d["big_A"] + "...  (617 digits)", 20, DATA)),
            VGroup(label(r"$B$", font_size=24, color=HEAD), mono(d["big_B"] + "...  (617 digits)", 20, HEAD)),
            VGroup(label(r"$g^{ab}$", font_size=24, color=YES),
                   label(rf"equal on both sides: \ {'yes' if d['big_equal'] else 'no'}; \ {d['big_ms']:.0f} ms in "
                         r"Python", font_size=22, color=YES)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            label(r"to find the secret, \ Eve must solve $g^x = A$ for $x$: \ the \textbf{discrete logarithm}",
                  font_size=22, color=NO),
            label(r"every HTTPS connection begins with an exchange like this \ (on an elliptic curve, \ chapter 9)",
                  font_size=22, color=WHITE),
            label(r"and with a \textbf{signature}, \ so Alice knows she is talking to Bob \ (chapters 10--12)",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "With small numbers Eve could simply try every exponent. <bookmark mark='a'/> In practice the prime has "
            "two thousand and forty-eight bits, six hundred and seventeen decimal digits, and the exchange still takes "
            "a few hundredths of a second, even in Python. <bookmark mark='b'/> To learn the secret, Eve must find the "
            "exponent from the power: the discrete logarithm, which nobody knows how to compute at this size. "
            "<bookmark mark='c'/> Every HTTPS connection your browser makes begins with an exchange like this one, "
            "usually on an elliptic curve. <bookmark mark='d'/> And with a signature, because Alice must also know "
            "that the person she agreed a secret with is Bob, and not someone in the middle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Public Keys", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"key distribution, \ Merkle's puzzles, \ and the number theory of groups",
            r"Diffie--Hellman, \ RSA from scratch, \ and the oracle that broke its padding",
            r"factoring and discrete logarithms: \ rho, \ the sieve, \ index calculus",
            r"elliptic curves: \ the chord and tangent, \ ECDH, \ ECDSA and its fatal nonce",
            r"certificates and a TLS 1.3 handshake between two of our machines",
            r"Shor's threat, \ lattices and ML-KEM, \ and computing on secrets",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 30 of Computer Science, Built: Public Keys. <bookmark mark='a'/> In this part: why distributing keys "
            "was the hard problem, and the number theory that solved it; Diffie-Hellman, and RSA built from scratch, "
            "with an attack on its padding; how factoring and discrete logarithms are attacked, which is what sets "
            "the key sizes; elliptic curves, their signatures and how one repeated number destroyed a console's "
            "security; certificates, and a full TLS handshake between two of our machines; and then the quantum "
            "threat, the lattices that answer it, and cryptography that computes on secrets."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
