from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, load)


def blob(color, pos, r=0.42, label_=None):
    c = Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=1).move_to(pos)
    g = VGroup(c)
    if label_:
        g.add(label(label_, font_size=18, color=GREY_A).next_to(c, DOWN, buff=0.1))
    return g


def mix(*cols):
    return interpolate_color(ManimColor(cols[0]), ManimColor(cols[1]), 0.5) if len(cols) == 2 else cols[0]


class DiffieHellman(VoiceoverScene):
    def construct(self):
        self.card()
        self.paint()
        self.maths()
        self.mitm()

    def card(self):
        card = chapter_card(4, r"Diffie--Hellman", r"How do two strangers agree on a key?", lit=(1976,), part=PART)
        with self.voiceover("Chapter four. Diffie-Hellman."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def paint(self):
        head = label(r"Mixing paint", font_size=34).to_edge(UP, buff=0.3)
        common = "#e8d44d"
        ared, bblue = "#d0453a", "#3a6fd0"
        am = mix(common, ared)
        bm = mix(common, bblue)
        final = interpolate_color(ManimColor(am), ManimColor(bblue), 0.33)
        lx, rx = -4.5, 4.5
        A = label(r"Alice", font_size=24, color=DATA).move_to([lx, 2.4, 0])
        B = label(r"Bob", font_size=24, color=HEAD).move_to([rx, 2.4, 0])
        cpub = blob(common, [0, 1.6, 0], label_=r"public colour")
        asec = blob(ared, [lx, 1.4, 0], label_=r"Alice's secret")
        bsec = blob(bblue, [rx, 1.4, 0], label_=r"Bob's secret")
        amix = blob(am, [lx + 1.4, 0.0, 0], label_=r"public + Alice's")
        bmix = blob(bm, [rx - 1.4, 0.0, 0], label_=r"public + Bob's")
        a_got = blob(bm, [lx, -1.6, 0])
        b_got = blob(am, [rx, -1.6, 0])
        afin = blob(final, [lx + 1.3, -1.6, 0], label_=r"+ Alice's")
        bfin = blob(final, [rx - 1.3, -1.6, 0], label_=r"+ Bob's")
        swap = VGroup(Arrow(amix.get_right(), [rx - 0.6, -1.6, 0], buff=0.1, stroke_width=2, color=GREY_B),
                      Arrow(bmix.get_left(), [lx + 0.6, -1.6, 0], buff=0.1, stroke_width=2, color=GREY_B))
        note = label(r"Eve sees the public colour and both mixtures: \ unmixing paint is hard", font_size=22,
                     color=NO).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The idea is easiest with paint. <bookmark mark='a'/> Alice and Bob agree in public on a colour, yellow. "
            "Each secretly picks a colour of their own. <bookmark mark='b'/> Each mixes their secret colour into the "
            "public one, and sends the mixture. Mixing is easy; separating a mixture back into its colours is not. "
            "<bookmark mark='c'/> Alice adds her secret colour to Bob's mixture; Bob adds his to Alice's. Both end up "
            "with yellow, red and blue together: the same colour. <bookmark mark='d'/> Eve saw the yellow and both "
            "mixtures, but to get the final colour she would have to unmix one of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(cpub))
            vo.wait_until("a")
            self.play(FadeIn(asec), FadeIn(bsec))
            vo.wait_until("b")
            self.play(FadeIn(amix), FadeIn(bmix))
            vo.wait_until("c")
            self.play(GrowArrow(swap[0]), GrowArrow(swap[1]), FadeIn(a_got), FadeIn(b_got))
            self.play(FadeIn(afin), FadeIn(bfin))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def maths(self):
        d = load("toydh")
        head = label(r"The mathematics", font_size=34).to_edge(UP, buff=0.3)
        eqs = VGroup(
            MathTex(r"A = g^a \bmod p, \qquad B = g^b \bmod p", font_size=40, color=WHITE),
            MathTex(r"B^a = (g^b)^a = g^{ab} = (g^a)^b = A^b", font_size=40, color=YES),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            label(r"mixing $=$ exponentiation, \ unmixing $=$ the discrete logarithm", font_size=22, color=WHITE),
            label(r"\textbf{CDH}: \ from $g, g^a, g^b$, \ compute $g^{ab}$: \ believed hard \ (no harder than the "
                  r"discrete log)", font_size=22, color=HEAD),
            label(r"\textbf{DDH}: \ even \textit{telling} $g^{ab}$ from a random $g^c$ is hard: \ use a prime-order "
                  r"subgroup", font_size=22, color=DATA),
            label(r"then hash $g^{ab}$ into a key: \ HKDF \ (chapter 12)", font_size=22, color=GREY_A),
            label(rf"2048-bit group: \ {d['big_ms']:.0f} ms in Python; \ on an elliptic curve, \ smaller and faster",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.22).next_to(eqs, DOWN, buff=0.6)
        with self.voiceover(
            "Now the mathematics. <bookmark mark='a'/> The public colour is a generator g of a group modulo a prime. "
            "The secrets are exponents. Mixing is exponentiation: Alice sends g to the a, Bob sends g to the b. "
            "<bookmark mark='b'/> Alice raises Bob's number to a, Bob raises Alice's to b, and exponents multiply, so "
            "both get g to the a b. Unmixing is the discrete logarithm. <bookmark mark='c'/> The security assumption is "
            "called computational Diffie-Hellman: from g, g to the a and g to the b, nobody can compute g to the a b. "
            "<bookmark mark='d'/> Proofs usually need a stronger one, decisional Diffie-Hellman: the shared value cannot "
            "even be told apart from a random group element. It fails in the full group modulo p, so real systems work "
            "in a subgroup of prime order. <bookmark mark='e'/> The shared value is then hashed into a key. And the "
            "same exchange on an elliptic curve, chapter nine, is smaller and faster."
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
            self.play(FadeIn(lines[3]), FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def mitm(self):
        d = load("mitm")
        head = label(r"The man in the middle", font_size=34).to_edge(UP, buff=0.3)
        A = label(r"Alice", font_size=24, color=DATA).move_to([-5.0, 1.6, 0])
        M = label(r"Mallory", font_size=24, color=NO).move_to([0, 1.6, 0])
        B = label(r"Bob", font_size=24, color=HEAD).move_to([5.0, 1.6, 0])
        a1 = DoubleArrow([-4.3, 1.0, 0], [-0.8, 1.0, 0], buff=0, stroke_width=2.5, color=NO, tip_length=0.2)
        a2 = DoubleArrow([0.8, 1.0, 0], [4.3, 1.0, 0], buff=0, stroke_width=2.5, color=NO, tip_length=0.2)
        k1 = label(rf"key {d['alice']}", font_size=22, color=NO).next_to(a1, DOWN, buff=0.1)
        k2 = label(rf"key {d['bob']}", font_size=22, color=NO).next_to(a2, DOWN, buff=0.1)
        lines = VGroup(
            label(r"Mallory intercepts $g^a$ and $g^b$, \ and runs one exchange with each side", font_size=22,
                  color=WHITE),
            label(rf"Alice shares {d['alice']} with Mallory, \ Bob shares {d['bob']}: \ each thinks it is the other",
                  font_size=22, color=NO),
            label(r"Mallory decrypts, \ reads or changes, \ and re-encrypts every message", font_size=22, color=NO),
            label(r"Diffie--Hellman alone protects against listening, \ not against \textbf{impersonation}",
                  font_size=22, color=HEAD),
            label(r"the fix: \ sign the exchange with a key the other side can check \ (chapters 10 and 11)",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Diffie-Hellman defeats a listener. It does not defeat someone who can change the messages. <bookmark "
            "mark='a'/> Mallory sits between Alice and Bob, intercepts g to the a and g to the b, and runs one exchange "
            "with each side, using her own secret. <bookmark mark='b'/> In our run Alice ends up sharing fifteen, with "
            "Mallory, and Bob shares eight, also with Mallory. Each believes the key is shared with the other. "
            "<bookmark mark='c'/> Now Mallory decrypts everything Alice sends, reads or changes it, and re-encrypts it "
            "for Bob. <bookmark mark='d'/> The exchange protects against eavesdropping, not against impersonation. "
            "<bookmark mark='e'/> The fix is for Bob to sign his half with a key Alice can verify, which needs "
            "signatures and some way to trust a public key: chapters ten and eleven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(M), FadeIn(B))
            vo.wait_until("a")
            self.play(GrowFromCenter(a1), GrowFromCenter(a2), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(k1), FadeIn(k2), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()
