from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


class Lattices(VoiceoverScene):
    def construct(self):
        self.card()
        self.basis()
        self.knapsack()
        self.lwe()
        self.mlkem()

    def card(self):
        card = chapter_card(14, r"Lattices", r"What problem might survive a quantum computer?", lit=(1982, 2005, 2024),
                            extra=((1982, r"LLL"), (2005, r"Regev: \ LWE"), (2024, r"ML-KEM")), part=PART)
        with self.voiceover("Chapter fourteen. Lattices."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def basis(self):
        L = load("lattices")
        head = label(r"One lattice, \ two bases", font_size=34).to_edge(UP, buff=0.3)
        steps = L["gauss"]
        b1, b2 = steps[0]
        r1, r2 = L["reduced"]
        sc = 0.13
        o = np.array([-3.0, -0.4, 0])
        P = lambda v: o + sc * np.array([v[0], v[1], 0])   # noqa: E731
        pts = VGroup()
        for i in range(-14, 15):
            for j in range(-14, 15):
                v = (i * r1[0] + j * r2[0], i * r1[1] + j * r2[1])
                if abs(v[0]) <= 28 and abs(v[1]) <= 24:
                    pts.add(Dot(P(v), radius=0.028, color=GREY_B))
        good = VGroup(Arrow(P((0, 0)), P(r1), buff=0, color=YES, stroke_width=4, max_tip_length_to_length_ratio=0.25),
                      Arrow(P((0, 0)), P(r2), buff=0, color=YES, stroke_width=4, max_tip_length_to_length_ratio=0.25))
        far = VGroup(Arrow(P((0, 0)), P((b1[0] / 6, b1[1] / 6)), buff=0, color=NO, stroke_width=3),
                     Arrow(P((0, 0)), P((b2[0] / 6, b2[1] / 6)), buff=0, color=NO, stroke_width=3))
        notes = VGroup(
            label(r"a \textbf{lattice}: \ all integer combinations \\ of some basis vectors", font_size=21, color=WHITE),
            label(rf"bad basis: \ $({b1[0]}, {b1[1]})$, \ $({b2[0]}, {b2[1]})$ \\ (red, \ drawn at a sixth of their length)",
                  font_size=21, color=NO),
            label(rf"Gauss's reduction, \ {len(steps) - 1} steps: \\ $({r1[0]}, {r1[1]})$, \ $({r2[0]}, {r2[1]})$: \ "
                  r"the same points", font_size=21, color=YES),
            label(r"in 2 dimensions, easy; \ in 500, \\ finding a short vector is \textbf{hard}, \\ even for quantum "
                  r"computers, \ as far as known", font_size=21, color=HEAD),
            label(r"LLL \ (1982): \ in polynomial time, \\ a vector within $2^{n/2}$ of the shortest", font_size=21,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.2, 0.2, 0])
        fit_right(notes)
        with self.voiceover(
            "A lattice is a regular grid of points in space: all whole-number combinations of a few basis vectors. "
            "<bookmark mark='a'/> The same lattice has many bases. These two long, nearly parallel vectors, ninety, "
            "one hundred and twenty-three and fifty-six, seventy-six, generate exactly the same points as these two "
            "short ones. <bookmark mark='b'/> Gauss's reduction, subtracting multiples of one vector from the other, "
            "finds the short basis in a few steps. <bookmark mark='c'/> In two dimensions that is easy. In hundreds of "
            "dimensions, finding a short vector given a bad basis is believed to be hard, and unlike factoring, no "
            "quantum algorithm is known to help. <bookmark mark='d'/> The LLL algorithm of Arjen Lenstra, Hendrik "
            "Lenstra and László Lovász, from 1982, finds a fairly short vector in polynomial time: within an "
            "exponential factor of the shortest. That factor is the gap cryptography lives in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pts), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(GrowArrow(far[0]), GrowArrow(far[1]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(GrowArrow(good[0]), GrowArrow(good[1]), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def knapsack(self):
        L = load("lattices")
        head = label(r"LLL as a weapon", font_size=34).to_edge(UP, buff=0.3)
        pub = ", ".join(f"{x:,}" for x in L["knap_pub"]).replace(",", "{,}")
        lines = VGroup(
            label(r"Merkle and Hellman \ (1978): \ encrypt bits as a subset sum of public weights", font_size=22,
                  color=WHITE),
            label(rf"public weights: \ {pub}, \ $\ldots$ \ ({L['knap_n']} of them)", font_size=20, color=GREY_A),
            label(r"the trapdoor: \ a hidden easy sequence, \ disguised by multiplying mod $q$", font_size=22,
                  color=HEAD),
            label(r"Shamir \ (1982): \ broken; \ Lagarias and Odlyzko: \ the message is a short vector in a lattice",
                  font_size=22, color=NO),
            label(rf"our LLL finds it: \ all {L['knap_n']} bits correct \ ({L['lll_s']:.0f} s, \ exact arithmetic "
                  r"in Python)", font_size=22, color=NO),
            label(r"also chapter 10's biased nonces, \ and Coppersmith's attacks on small RSA exponents", font_size=22,
                  color=GREY_A),
            label(r"so lattice cryptography must stay \textbf{far} beyond what LLL and its successors \ (BKZ) \ "
                  r"reach", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.24).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "LLL first appeared in cryptography as a weapon. <bookmark mark='a'/> In 1978 Merkle and Hellman proposed "
            "encrypting a string of bits as the sum of a subset of public weights. <bookmark mark='b'/> Here are some "
            "of the twenty weights of ours. <bookmark mark='c'/> The trapdoor was an easy, superincreasing sequence "
            "disguised by modular multiplication. <bookmark mark='d'/> Shamir broke it in 1982, and Lagarias and "
            "Odlyzko showed that for such knapsacks the secret bits form an unusually short vector in a lattice built "
            "from the weights. <bookmark mark='e'/> Our LLL finds it, and all twenty bits. <bookmark mark='f'/> The "
            "same tool finds ECDSA keys from biased nonces and breaks RSA with badly chosen small exponents. <bookmark "
            "mark='g'/> So lattice-based schemes must choose parameters far beyond the reach of LLL and its stronger "
            "successors."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def lwe(self):
        L = load("lattices")
        q = L["q"]
        head = label(r"Learning with errors", font_size=34).to_edge(UP, buff=0.3)
        eq = MathTex(r"b = A s + e \pmod q", font_size=42, color=WHITE).next_to(head, DOWN, buff=0.45)
        lo, hi, bw = -q // 4, 3 * q // 4, 32
        shift = lambda v: v if v < hi else v - q      # noqa: E731
        counts = {}
        for bit, vals in ((0, L["lwe_d0"]), (1, L["lwe_d1"])):
            for v in vals:
                b_ = (shift(v) - lo) // bw
                counts[(bit, b_)] = counts.get((bit, b_), 0) + 1
        top = max(counts.values())
        ax = Axes(x_range=[lo, hi, q // 4], y_range=[0, top * 1.15, max(1, top // 2)], x_length=7.2, y_length=2.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(eq, DOWN, buff=0.6)

        def hist(bit, col):
            g = VGroup()
            for (bb, b_), n in counts.items():
                if bb != bit:
                    continue
                x0 = lo + b_ * bw
                base, tp = ax.c2p(x0 + bw / 2, 0), ax.c2p(x0 + bw / 2, n)
                g.add(Rectangle(width=ax.c2p(bw, 0)[0] - ax.c2p(0, 0)[0], height=tp[1] - base[1], stroke_width=0,
                                fill_color=col, fill_opacity=0.85).move_to(base, aligned_edge=DOWN))
            return g
        h0, h1 = hist(0, DATA), hist(1, HEAD)
        xt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x, t in ((lo, r"$-q/4$"), (0, "0"), (q // 4, r"$q/4$"), (q // 2, r"$q/2$"),
                                   (3 * q // 4, r"$3q/4$"))])
        k = VGroup(label(r"encrypted 0", font_size=17, color=DATA), label(r"encrypted 1", font_size=17, color=HEAD)
                   ).arrange(RIGHT, buff=0.5).next_to(ax, UP, buff=0.1)
        lines = VGroup(
            label(r"Regev \ (2005): \ without the small noise $e$, \ Gaussian elimination finds $s$; \ with it, \ "
                  r"believed hard", font_size=21, color=WHITE),
            label(r"hard on \textbf{average} if lattice problems are hard in the \textbf{worst case} \ (a quantum "
                  r"reduction)", font_size=21, color=YES),
            label(r"decryption leaves $\textrm{bit} \cdot q/2$ plus small noise: \ near 0 means 0, \ near $q/2$ "
                  r"means 1 \ (ours: \ 400 of 400)", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The problem post-quantum encryption uses is Oded Regev's learning with errors, from 2005. <bookmark "
            "mark='a'/> A secret vector s; a public random matrix A; and b, which is A times s plus a small random "
            "error, everything modulo q. Without the error, Gaussian elimination would find s instantly. The small "
            "noise makes it, as far as anyone knows, hard: it is a lattice problem in disguise. <bookmark mark='b'/> "
            "Regev proved something unusual: breaking random instances is as hard as solving the worst-case lattice "
            "problem, by a quantum reduction. Cryptography rarely has guarantees that strong. <bookmark mark='c'/> To "
            "encrypt a bit, add up a random subset of the public samples and add the bit times half of q. Decryption "
            "subtracts the secret's contribution and is left with the bit times q over two, plus a little accumulated "
            "noise. Here are four hundred decryptions: zeros land near zero, ones near q over two, far from the "
            "boundary. Every one decrypted correctly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xt), FadeIn(k), FadeIn(h0), FadeIn(h1), FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def mlkem(self):
        L = load("lattices")
        b = load("beyond")
        head = label(r"ML-KEM, \ and hash-based signatures", font_size=34).to_edge(UP, buff=0.3)
        nbits = f"{L['kpke_trials'] * 256:,}".replace(",", "{,}")
        lines = VGroup(
            label(r"plain LWE keys are huge: \ ML-KEM uses \textbf{module} LWE over the ring $\mathbb{Z}_{3329}[x] / "
                  r"(x^{256} + 1)$", font_size=21, color=WHITE),
            label(rf"multiply polynomials by the NTT \ (Part 19's FFT, \ mod 3329): \ {L['ntt_ms']:.2f} ms against "
                  rf"{L['school_ms']:.1f} ms schoolbook \ (ours)", font_size=21, color=DATA),
            label(rf"our ML-KEM-512 arithmetic: \ {L['kpke_trials']} encryptions, \ {nbits} bits, \ "
                  rf"{L['kpke_wrong']} decryption errors", font_size=21, color=YES),
            label(r"keys of 800 bytes, \ ciphertexts of 768: \ larger than X25519's 32, \ small enough for every "
                  r"handshake", font_size=21, color=HEAD),
            label(r"\textbf{ML-DSA}: \ lattice signatures; \ \textbf{SLH-DSA}: \ signatures from hash functions alone",
                  font_size=21, color=WHITE),
            label(rf"their ancestor, \ Lamport \ (1979): \ reveal one of two secrets per hash bit: \ public key "
                  rf"{b['lamport_pk_bytes'] // 1024} KB, \ signature {b['lamport_sig_bytes'] // 1024} KB, \ "
                  r"\textbf{one} use", font_size=21, color=GREY_A),
            label(r"a Merkle tree \ (Part 29) \ of one-time keys gives many signatures \ (SPHINCS$^+$ $\to$ SLH-DSA)",
                  font_size=21, color=LAM),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Plain LWE needs enormous keys, so the standard uses structure. <bookmark mark='a'/> ML-KEM, formerly called "
            "Kyber, works with polynomials modulo x to the two hundred and fifty-six plus one, with coefficients "
            "modulo three thousand three hundred and twenty-nine, arranged in small vectors and matrices. <bookmark "
            "mark='b'/> Multiplying polynomials is done with the number-theoretic transform, Part 19's FFT over a "
            "finite field: in our Python, about twelve times faster than schoolbook multiplication. <bookmark "
            "mark='c'/> We implemented the arithmetic of the smallest parameter set, and encrypted a hundred random "
            "messages of two hundred and fifty-six bits. Every bit decrypted correctly. <bookmark mark='d'/> Keys are "
            "eight hundred bytes and ciphertexts seven hundred and sixty-eight: bigger than elliptic curves, small "
            "enough for every TLS handshake. <bookmark mark='e'/> For signatures there is a lattice scheme, ML-DSA, "
            "and a conservative one built only from hash functions, SLH-DSA. <bookmark mark='f'/> Its ancestor is "
            "Leslie Lamport's one-time signature from 1979: publish hashes of two secrets for each bit of the message "
            "hash, and sign by revealing one secret per bit. Big, and usable once. <bookmark mark='g'/> A Merkle tree "
            "over many one-time keys turns it into a scheme for many signatures, whose security rests only on the "
            "hash function."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
