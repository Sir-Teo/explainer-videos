from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono)


class Beyond(VoiceoverScene):
    def construct(self):
        self.card()
        self.schnorr()
        self.sharing()
        self.computing()

    def card(self):
        card = chapter_card(15, r"Zero knowledge, \ sharing and computing on secrets",
                            r"What else can public-key ideas do?", lit=(1979, 1986, 2009),
                            extra=((1979, r"Shamir's secret sharing"), (1986, r"Yao's garbled circuits"),
                                   (2009, r"Gentry: \ FHE")), part=PART)
        with self.voiceover("Chapter fifteen. Zero knowledge, secret sharing, and computing on secrets."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def schnorr(self):
        b = load("beyond")
        head = label(r"Schnorr: \ prove you know $x$, \ reveal nothing", font_size=34).to_edge(UP, buff=0.3)
        lx, rx = -4.4, 4.4
        P = label(r"prover \ (knows $x$, \ $y = g^x$ public)", font_size=21, color=HEAD).move_to([lx, 2.3, 0])
        V = label(r"verifier", font_size=21, color=DATA).move_to([rx, 2.3, 0])
        msgs = [(1.5, r"commit: \ $R = g^k$, \ $k$ random", "R", HEAD), (0.7, r"challenge: \ random $e$", "L", DATA),
                (-0.1, r"response: \ $s = k + e x$", "R", HEAD)]
        arrows = VGroup()
        for y, t, d, c in msgs:
            a, bb = ([lx + 0.6, y, 0], [rx - 0.6, y, 0]) if d == "R" else ([rx - 0.6, y, 0], [lx + 0.6, y, 0])
            ar = Arrow(a, bb, buff=0, stroke_width=2.5, color=c, max_tip_length_to_length_ratio=0.03)
            arrows.add(VGroup(ar, label(t, font_size=21, color=WHITE).next_to(ar, UP, buff=0.05)))
        check = label(r"check: \ $g^s = R \cdot y^e$", font_size=24, color=YES).move_to([rx - 0.6, -0.8, 0])
        lines = VGroup(
            label(r"zero knowledge \ (Part 27): \ a simulator can fake transcripts without $x$", font_size=21,
                  color=WHITE),
            label(r"\textbf{Fiat--Shamir} \ (1986): \ replace the verifier by a hash, \ $e = H(R \,\|\, m)$: \ a "
                  r"\textbf{signature} on $m$", font_size=21, color=HEAD),
            label(rf"ours, \ in a 1024-bit group with a 160-bit subgroup: \ verifies: \ "
                  rf"{'yes' if b['schnorr_ok'] else 'no'}", font_size=21, color=YES),
            label(r"Ed25519 is Schnorr on an Edwards curve; \ Bitcoin added Schnorr signatures in 2021", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.17).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Public-key ideas do more than encrypt and sign. Claus Schnorr's protocol proves that you know a discrete "
            "logarithm without revealing it. <bookmark mark='a'/> The prover commits to a random power of g. <bookmark "
            "mark='b'/> The verifier sends a random challenge. <bookmark mark='c'/> The prover answers with k plus e "
            "times x, which, because k is random, says nothing about x by itself. <bookmark mark='d'/> The verifier "
            "checks one equation. <bookmark mark='e'/> As in Part 27, a simulator who knows the challenge in advance "
            "can produce transcripts that look the same without knowing x: zero knowledge. <bookmark mark='f'/> Amos "
            "Fiat and Adi Shamir's trick replaces the verifier with a hash of the commitment and a message, and the "
            "proof becomes a signature. <bookmark mark='g'/> Ours verifies. <bookmark mark='h'/> Ed25519, the "
            "signature in SSH and Signal, is Schnorr on an elliptic curve, and Bitcoin adopted Schnorr signatures in "
            "2021."
        ) as vo:
            self.play(FadeIn(head), FadeIn(P), FadeIn(V))
            for mk, a in zip("abc", arrows):
                vo.wait_until(mk)
                self.play(GrowArrow(a[0]), FadeIn(a[1]))
            vo.wait_until("d")
            self.play(FadeIn(check))
            for mk, ln in zip("efgh", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def sharing(self):
        b = load("beyond")
        head = label(r"Shamir's secret sharing", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 10, 2], x_length=4.6, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=0.9)
        f = lambda x: 2 + 2.6 * x - 0.36 * x * x    # noqa: E731
        curve = ax.plot(f, x_range=[0, 5.6], color=HEAD, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(x, f(x)), radius=0.08, color=DATA) for x in range(1, 6)])
        sec = Dot(ax.c2p(0, f(0)), radius=0.1, color=YES)
        sl = label(r"secret $= f(0)$", font_size=18, color=YES).next_to(sec, RIGHT, buff=0.1)
        cap = label(r"the picture over the reals; \ the real thing is in GF($p$)", font_size=16, color=GREY_A).next_to(
            ax, DOWN, buff=0.15)
        tab = grid_table([r"share", r"$x$", r"$f(x) \bmod (2^{61} - 1)$"],
                         [[str(i + 1), str(x), f"{y}"] for i, (x, y) in enumerate(b["shares"])],
                         widths=[1.0, 0.6, 3.6], row_h=0.42, font_size=19, mono_cols=(1, 2))
        tab.next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        res = VGroup(
            label(rf"shares 1, 2, 3 $\to$ \texttt{{{b['from_3']}}}", font_size=20, color=YES),
            label(rf"shares 2, 4, 5 $\to$ \texttt{{{b['from_other_3']}}}", font_size=20, color=YES),
            label(rf"shares 1, 2 $\to$ \texttt{{{b['from_2']}}}: \ nothing", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tab, DOWN, buff=0.3).align_to(tab, LEFT)
        lines = VGroup(
            label(r"hide the secret as $f(0)$ of a random degree-2 polynomial; \ give out $f(1), \ldots, f(5)$:\ any 3 "
                  r"rebuild $f$ \ (Lagrange), \ any 2 reveal nothing", font_size=20, color=WHITE),
            label(r"the shares are a Reed--Solomon codeword \ (Part 28); \ used for backup and threshold keys, \ "
                  r"like DNSSEC's root key", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A key that unlocks everything should not live in one place, or with one person. Adi Shamir's answer, "
            "from 1979, is a polynomial. <bookmark mark='a'/> Make the secret the value at zero of a random "
            "polynomial of degree two. Hand out its values at one, two, three, four and five as shares. <bookmark "
            "mark='b'/> Any three shares determine the polynomial, by Part 28's Lagrange interpolation, and so the "
            "secret. Over the integers modulo a prime, with our five shares: shares one, two and three give "
            "thirty-one thousand three hundred and thirty-seven, and so do two, four and five. <bookmark mark='c'/> "
            "Two shares are consistent with every possible secret, so they reveal nothing at all: here they produce "
            "garbage. <bookmark mark='d'/> The shares are exactly a Reed-Solomon codeword. The scheme guards backup "
            "keys and threshold signatures, including the recovery of the internet's DNSSEC root key."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(sec), FadeIn(sl), FadeIn(dots), FadeIn(lines[0]))
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(res[0]), FadeIn(res[1]))
            vo.wait_until("c")
            self.play(FadeIn(res[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def computing(self):
        head = label(r"Computing on secrets", font_size=34).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"\textbf{multiparty computation}: \ several parties compute $f(x_1, \ldots, x_n)$, \ learning only "
                  r"the result", font_size=22, color=WHITE),
            label(r"Yao's garbled circuits \ (1986); \ Goldreich, \ Micali and Wigderson \ (1987): \ \textit{any} "
                  r"function", font_size=22, color=HEAD),
            label(r"2008: \ Danish farmers' sugar-beet auction run by MPC; \ today: \ private set intersection, \ "
                  r"password breach checks", font_size=22, color=GREY_A),
            label(r"\textbf{fully homomorphic encryption}: \ compute on ciphertexts, \ decrypt the answer", font_size=22,
                  color=YES),
            label(r"lattice schemes add noise with every operation; \ Gentry \ (2009) \ found \textbf{bootstrapping}: "
                  r"\ decrypt homomorphically to clean it", font_size=22, color=YES),
            label(r"once a trillion times slower, \ now practical for some lookups \ (phone caller-ID services, \ "
                  r"2024)", font_size=22, color=DATA),
            label(r"and \textbf{differential privacy} \ (\textit{AI, Built} 31): \ release statistics, \ not people",
                  font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Two more ideas complete the picture. <bookmark mark='a'/> In multiparty computation, several parties each "
            "hold a private input, and together compute a function of all of them, learning only the result. "
            "<bookmark mark='b'/> Andrew Yao's garbled circuits of 1986, and Goldreich, Micali and Wigderson's protocol "
            "a year later, showed that any function can be computed this way. <bookmark mark='c'/> In 2008 Danish "
            "sugar-beet farmers set their contract prices by an auction run as a multiparty computation; today it "
            "checks passwords against breach lists without revealing them. <bookmark mark='d'/> Fully homomorphic "
            "encryption goes further: anyone can compute on ciphertexts, and only the key holder can read the result. "
            "<bookmark mark='e'/> Lattice encryption allows it, but each operation adds noise, and after a while the "
            "noise swamps the message. In 2009 Craig Gentry found the way out, bootstrapping: evaluate the decryption "
            "itself homomorphically, which removes the old noise. <bookmark mark='f'/> Once a trillion times slower "
            "than plain computation, it now runs in production for some private lookups. <bookmark mark='g'/> And "
            "differential privacy, from AI, Built part 31, protects what is learned from data that is released."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
