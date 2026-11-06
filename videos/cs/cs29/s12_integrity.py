from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.algo import crypto as K
from videos.cs.cs29.common import (DATA, HEAD, NO, PART, YES, flow_box, load, mono)


def hexrow(b, color, font=18, hi=()):
    return VGroup(*[mono(f"{x:02x}", font, YES if i in hi else color) for i, x in enumerate(b)]).arrange(RIGHT,
                                                                                                         buff=0.12)


class Integrity(VoiceoverScene):
    def construct(self):
        self.card()
        self.malleable()
        self.macs()
        self.aead()

    def card(self):
        card = chapter_card(11, r"Integrity", r"How do you know nobody changed the message?", lit=(1996, 2007),
                            extra=((1996, r"HMAC"), (2007, r"GCM \ (NIST SP 800-38D)"),
                                   (2015, r"ChaCha20-Poly1305")), part=PART)
        with self.voiceover("Chapter eleven. Integrity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def malleable(self):
        head = label(r"Encryption is not protection", font_size=34).to_edge(UP, buff=0.3)
        aes = K.AES(bytes(range(16)))
        nonce = bytes(8)
        m = b"PAY ALICE $0010."
        want = b"PAY ALICE $9910."
        c = K.ctr_encrypt(aes, nonce, m)
        delta = K.xor(m, want)
        c2 = K.xor(c, delta)
        got = K.ctr_encrypt(aes, nonce, c2)
        hi = [i for i, x in enumerate(delta) if x]
        rows = VGroup(
            VGroup(label(r"message", font_size=19, color=GREY_A), mono(m.decode(), 22, WHITE)),
            VGroup(label(r"ciphertext \ (CTR)", font_size=19, color=GREY_A), hexrow(c, DATA)),
            VGroup(label(r"attacker XORs", font_size=19, color=GREY_A), hexrow(delta, GREY_C, hi=hi)),
            VGroup(label(r"modified ciphertext", font_size=19, color=GREY_A), hexrow(c2, NO, hi=hi)),
            VGroup(label(r"receiver decrypts", font_size=19, color=GREY_A), mono(got.decode(), 22, NO)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        for r in rows:
            r[1].align_to(rows[1][1], LEFT)
        lines = VGroup(
            label(r"the attacker knows the format, \ not the key: \ XOR in \texttt{0010} $\oplus$ \texttt{9910}, "
                  r"\ and the amount changes", font_size=21, color=WHITE),
            label(r"CTR, \ CBC and the one-time pad are \textbf{malleable}: \ secrecy says nothing about tampering",
                  font_size=21, color=NO),
            label(r"a \textbf{MAC}: \ a tag $t = \mathrm{MAC}_k(m)$; \ without $k$, \ no one can make a valid tag for "
                  r"any new message", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Encryption keeps a message secret. It does not keep it intact. <bookmark mark='a'/> Here is a payment "
            "instruction, encrypted in counter mode. The attacker cannot read it, but suppose they know its format. "
            "<bookmark mark='b'/> Counter mode XORs a keystream into the message, so XORing something into the "
            "ciphertext XORs the same thing into the plaintext. The attacker XORs in the difference between zero "
            "zero one zero and nine nine one zero, at the right position. <bookmark mark='c'/> The receiver "
            "decrypts and pays Alice nine thousand nine hundred and ten dollars instead of ten. No key was needed. Counter mode, CBC and "
            "the one-time pad are all malleable like this. <bookmark mark='d'/> Protection needs a different tool: "
            "a message authentication code. The sender attaches a tag computed with a key, and the requirement is "
            "that without the key nobody can produce a valid tag for any message they have not seen tagged, even "
            "after seeing many."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def macs(self):
        d = load("mac")
        head = label(r"CBC-MAC, \ its splice, \ and HMAC", font_size=34).to_edge(UP, buff=0.3)
        es = VGroup(*[flow_box(r"$E_k$", DATA, w=1.0, h=0.6, font=22) for _ in range(3)]).arrange(RIGHT, buff=1.4)
        es.next_to(head, DOWN, buff=1.2)
        ms = VGroup(*[MathTex(rf"m_{i + 1}", font_size=28, color=WHITE).next_to(e, UP, buff=0.6) for i, e in
                      enumerate(es)])
        xs = VGroup(*[MathTex(r"\oplus", font_size=30).next_to(e, UP, buff=0.12) for e in es[1:]])
        wires = VGroup(*[Arrow(ms[0].get_bottom(), es[0].get_top(), buff=0.08, stroke_width=2, color=GREY_B)])
        for i in (1, 2):
            wires.add(Arrow(ms[i].get_bottom(), xs[i - 1].get_top(), buff=0.05, stroke_width=2, color=GREY_B))
            wires.add(Arrow(xs[i - 1].get_bottom(), es[i].get_top(), buff=0.03, stroke_width=2, color=GREY_B))
            wires.add(CurvedArrow(es[i - 1].get_right(), xs[i - 1].get_left(), angle=TAU / 8, stroke_width=2,
                                  color=GREY_B))
        tag = MathTex(r"t", font_size=30, color=YES).next_to(es[2], RIGHT, buff=0.6)
        wires.add(Arrow(es[2].get_right(), tag.get_left(), buff=0.08, stroke_width=2, color=GREY_B))
        m1, m2 = d["m1"], d["m2"]
        forged = bytes.fromhex(d["forged_hex"])
        lines = VGroup(
            label(r"CBC-MAC: \ CBC with a zero IV; \ the tag is the last block: \ secure for messages of one fixed "
                  r"length", font_size=21, color=WHITE),
            label(rf"seen: \ \texttt{{{m1.replace(' ', '~').replace('$', chr(92) + '$')}}} with tag $t_1$, \ "
                  rf"\texttt{{{m2.replace(' ', '~').replace('$', chr(92) + '$')}}} with tag $t_2$", font_size=21,
                  color=GREY_A),
            label(r"forge: \ $m_1 \,\|\, (m_2 \oplus t_1)$ \ has tag $t_2$: \ the chain arrives at $E_k(m_2)$ again",
                  font_size=21, color=NO),
            label(rf"our forgery \ ({len(forged)} bytes) \ verifies: \ {'valid' if d['forgery_valid'] else 'invalid'}",
                  font_size=21, color=NO),
            label(r"\textbf{HMAC} \ (Bellare, \ Canetti, \ Krawczyk, \ 1996): \ $H\bigl((k \oplus \mathrm{opad})"
                  r"\,\|\, H((k \oplus \mathrm{ipad}) \,\|\, m)\bigr)$: \ any length, \ any good hash", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first MACs were built from block ciphers. <bookmark mark='a'/> CBC-MAC runs CBC encryption with a "
            "zero starting value and keeps only the last block as the tag. For messages of one fixed length, it is "
            "provably secure if the cipher is a pseudorandom permutation. <bookmark mark='b'/> But allow different "
            "lengths, and here is what an attacker can do with two tagged one-block messages. <bookmark mark='c'/> "
            "Append to the first message the second message XORed with the first tag. Running the chain, the first "
            "tag cancels, and the chain is back to encrypting the second message alone: the tag of the new, "
            "two-block message is the second tag. <bookmark mark='d'/> Our forgery verifies. Prefixing the length "
            "fixes it; the standard mode, CMAC, fixes it by treating the last block specially. <bookmark mark='e'/> The other "
            "standard is HMAC, from 1996: hash the key with the message, then hash the key with that result. It "
            "works with any good hash function and any message length, and it secures most web APIs' signed "
            "requests and tokens."
        ) as vo:
            self.play(FadeIn(head), FadeIn(es), FadeIn(ms), FadeIn(xs), FadeIn(wires), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()

    def aead(self):
        d = load("mac")
        head = label(r"Authenticated encryption", font_size=34).to_edge(UP, buff=0.3)
        f = MathTex(r"\mathrm{tag} = E_k(N \| 1) \;\oplus\; \sum_{i=1}^{m} B_i \, H^{\,m-i+1}, \qquad "
                    r"H = E_k(0^{128})", font_size=36, color=YES).next_to(head, DOWN, buff=0.5)
        fl = label(r"GCM's GHASH: \ the ciphertext blocks $B_i$ are the coefficients of a polynomial, \ evaluated at "
                   r"a secret point $H$ of $\mathrm{GF}(2^{128})$", font_size=20, color=GREY_A).next_to(f, DOWN,
                                                                                                      buff=0.2)
        lines = VGroup(
            label(r"encrypt-then-MAC \ (Bellare and Namprempre, 2000): \ the generic composition that is always "
                  r"secure", font_size=21, color=WHITE),
            label(r"\textbf{AEAD}: \ one mode does both: \ GCM = CTR encryption + GHASH; \ TLS 1.3 allows nothing "
                  r"else", font_size=21, color=DATA),
            label(rf"ours matches NIST's GCM test vectors: \ tag \texttt{{{d['gcm_tag'][:16]}}}$\ldots$", font_size=21,
                  color=YES),
            label(r"two polynomials sharing a nonce give an equation in $H$: \ its roots let anyone forge \ (Joux, "
                  r"2006)", font_size=21, color=NO),
            label(r"2016: \ 184 HTTPS servers found repeating GCM nonces", font_size=21, color=NO),
            label(r"ChaCha20-Poly1305: \ the same idea, \ a polynomial modulo the prime $2^{130} - 5$", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, buff=0.16).next_to(fl, DOWN, buff=0.4)
        with self.voiceover(
            "Combine encryption and a MAC, and in which order? <bookmark mark='a'/> Mihir Bellare and Chanathip "
            "Namprempre showed in 2000 that encrypting first and then computing a MAC over the ciphertext is always "
            "secure, while the other orders can fail, as the padding oracle did. Receivers check the tag first and "
            "never decrypt a forgery. <bookmark mark='b'/> Modern modes do both at once: authenticated encryption. "
            "Galois counter mode, GCM, encrypts in counter mode and computes its tag with a polynomial: the "
            "ciphertext blocks are the coefficients, evaluated at a secret point H of the field with two to the one "
            "hundred and twenty-eight elements. Part 28's algebra again. TLS 1.3 allows only modes like this. "
            "<bookmark mark='c'/> Ours matches the standard's test vectors. <bookmark mark='d'/> The polynomial "
            "makes nonces critical. Two messages tagged with the same nonce give an equation whose roots include H, "
            "and with H anyone can forge tags. <bookmark mark='e'/> A 2016 survey found a hundred and eighty-four "
            "HTTPS servers repeating GCM nonces. <bookmark mark='f'/> ChaCha20 pairs with Poly1305, the same idea "
            "with a polynomial modulo the prime two to the hundred and thirty minus five."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(f), FadeIn(fl), FadeIn(lines[1]))
            for mk, ln in zip("cdef", lines[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
