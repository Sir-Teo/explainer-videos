from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono)


class Signatures(VoiceoverScene):
    def construct(self):
        self.card()
        self.ecdsa()
        self.reuse()

    def card(self):
        card = chapter_card(10, r"Signatures", r"How do you prove a message came from you?", lit=(1991, 2010),
                            extra=((1991, r"DSA"), (2010, r"the PS3 key")), part=PART)
        with self.voiceover("Chapter ten. Signatures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ecdsa(self):
        e = load("ecdsa")
        head = label(r"ECDSA", font_size=34).to_edge(UP, buff=0.3)
        sign = VGroup(
            label(r"\textbf{sign} \ (private key $d$, \ public $Q = dG$):", font_size=22, color=HEAD),
            MathTex(r"k \text{ random}, \quad r = (kG)_x \bmod n, \quad s = k^{-1}(z + r d) \bmod n", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        verify = VGroup(
            label(r"\textbf{verify} \ (anyone, \ with $Q$):", font_size=22, color=YES),
            MathTex(r"u_1 = z s^{-1}, \quad u_2 = r s^{-1}, \quad (u_1 G + u_2 Q)_x \overset{?}{=} r", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        block = VGroup(sign, verify).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.5)
        lines = VGroup(
            label(r"$z$: \ the message's hash; \ it works because $u_1 G + u_2 Q = s^{-1}(z + r d)\,G = kG$",
                  font_size=21, color=WHITE),
            label(r"a signature anyone can check, \ that only the holder of $d$ can make: \ \textbf{unforgeable}",
                  font_size=21, color=YES),
            label(r"RFC 6979 \ (2013): \ derive $k$ from $d$ and the message by HMAC, \ so no random generator is "
                  r"needed", font_size=21, color=DATA),
            label(rf"ours reproduces its P-256 test signature: \ $r = $ \texttt{{{e['r'][2:18]}}}$\ldots$ \ "
                  rf"({'matches' if e['r'] == e['r_expected'] else 'differs'})", font_size=21, color=YES),
            label(r"the nonce $k$ must be secret, \ uniform, \ and \textbf{never reused}", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.18).next_to(block, DOWN, buff=0.45)
        with self.voiceover(
            "Encryption hides; a signature proves who wrote something. The elliptic-curve digital signature algorithm, "
            "ECDSA, signs most of the web's certificates and most Bitcoin transactions. <bookmark mark='a'/> To sign, "
            "pick a fresh random number k, take the x coordinate of k times G as r, and combine k, the message's hash "
            "and the private key into s. <bookmark mark='b'/> To verify, anyone holding the public key computes two "
            "multipliers from s and checks that a combination of G and Q lands back on r. <bookmark mark='c'/> It works "
            "because that combination is exactly k times G. <bookmark mark='d'/> Only the holder of d can produce such "
            "a pair, while anyone can check it. <bookmark mark='e'/> Because bad random numbers ruin signatures, RFC "
            "6979 derives k deterministically from the key and the message with HMAC. <bookmark mark='f'/> Our "
            "implementation reproduces the standard's test signature exactly. <bookmark mark='g'/> Everything hangs on "
            "k: it must be secret, uniform, and never used twice."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sign))
            vo.wait_until("b")
            self.play(FadeIn(verify))
            for mk, ln in zip("cdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def reuse(self):
        e = load("ecdsa")
        head = label(r"One repeated nonce", font_size=34).to_edge(UP, buff=0.3)
        sigs = VGroup(
            VGroup(mono("game update 3.55", 20, WHITE), label(rf"$r = $ \texttt{{{e['r1'][2:]}}}$\ldots$", font_size=20,
                                                                 color=NO),
                   label(rf"$s_1 = $ \texttt{{{e['s1'][2:]}}}$\ldots$", font_size=20, color=GREY_A)),
            VGroup(mono("game update 3.56", 20, WHITE), label(rf"$r = $ \texttt{{{e['r1'][2:]}}}$\ldots$", font_size=20,
                                                                 color=NO),
                   label(rf"$s_2 = $ \texttt{{{e['s2'][2:]}}}$\ldots$", font_size=20, color=GREY_A)),
        )
        for s in sigs:
            s.arrange(RIGHT, buff=0.5)
        sigs.arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        same = SurroundingRectangle(VGroup(sigs[0][1], sigs[1][1]), color=NO, buff=0.08)
        eqs = VGroup(
            MathTex(r"s_1 - s_2 = k^{-1}(z_1 - z_2) \;\Rightarrow\; k = \frac{z_1 - z_2}{s_1 - s_2}", font_size=34,
                    color=HEAD),
            MathTex(r"d = \frac{s_1 k - z_1}{r}", font_size=34, color=NO),
        ).arrange(DOWN, buff=0.3).next_to(sigs, DOWN, buff=0.5)
        lines = VGroup(
            label(rf"recovered $k$: \ {'correct' if e['k_ok'] else 'wrong'}; \ private key $d$: \ "
                  rf"{'correct' if e['d_ok'] else 'wrong'}", font_size=22, color=NO),
            label(rf"and with it, \ a valid signature on \texttt{{homebrew loader}}: \ "
                  rf"{'verifies' if e['forged_ok'] else 'fails'}", font_size=22, color=NO),
            label(r"2010: \ Sony's PlayStation 3 used the same $k$ for every signature; \ fail0verflow recovered the "
                  r"master key", font_size=22, color=WHITE),
            label(r"biased nonces leak too: \ a few bits of bias in many signatures, \ and lattices \ (chapter 14) "
                  r"find $d$", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is what happens if k repeats. <bookmark mark='a'/> Two signatures on two different messages, made "
            "with the same nonce. The first half of each signature, r, is identical: the giveaway. <bookmark mark='b'/> "
            "Subtract the two s values: the private key cancels, and what is left gives k from the two hashes. "
            "<bookmark mark='c'/> With k known, one line of algebra gives the private key d. <bookmark mark='d'/> Our "
            "recovery finds both, correctly, and signs a message the key's owner never approved; it verifies. "
            "<bookmark mark='e'/> This is not hypothetical. In 2010 the fail0verflow group found that Sony signed "
            "PlayStation 3 software with the same k every time, and recovered the master signing key from two "
            "signatures. <bookmark mark='f'/> Even nonces that are merely biased by a few bits leak the key, given "
            "enough signatures, through the lattice methods of chapter fourteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sigs), Create(same))
            vo.wait_until("b")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
            vo.wait_until("f")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()
