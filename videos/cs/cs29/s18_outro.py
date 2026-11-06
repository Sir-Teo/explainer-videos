from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs29.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Secrets", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"26! \approx 4 \times 10^{26}", font_size=42, color=DATA), r"substitution; \ Vigen\`ere",
                 DATA),
            tile(MathTex(r"S\,(R_1 R_4)\,S", font_size=50, color=CTRL), r"Enigma; \ Rejewski", CTRL),
            tile(MathTex(r"|K| \ge |M|", font_size=54, color=YES), r"perfect secrecy", YES),
            tile(MathTex(r"G,\ F_k,\ (R,\, L \oplus f(R))", font_size=38, color=LAM), r"PRGs, \ PRFs, \ PRPs", LAM),
            tile(Text("69c4e0d8", font="DejaVu Sans Mono", font_size=40, color=HEAD), r"AES; \ modes; \ MACs", HEAD),
            tile(MathTex(r"2^{n/2}", font_size=60, color=NO), r"hashes; \ attacks", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Substitution ciphers broken by counting and climbing, and Vigenère by the "
            "index of coincidence. Enigma, simulated, and Rejewski's theorem that the plugboard cannot hide the "
            "cycle structure. Shannon's perfect secrecy and its price. Pseudorandom generators, functions and "
            "permutations, with Feistel's networks. AES from scratch, matching the standard, its avalanche, and "
            "the modes and MACs that make it safe, with the padding oracle that shows why. And hash functions, the "
            "birthday bound, and the attacks: differential, timing, and a key that was never random."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"TLS 1.3: \ our AEAD and HMAC inside a handshake", [30]),
            (r"Certificate Transparency: \ Merkle logs of certificates", [30]),
            (r"checksummed, \ copy-on-write file systems", [34]),
            (r"hash chains and proof of work", [38]),
            (r"git's content-addressed objects", [41]),
            (r"passwords, \ TOTP as an HMAC over time, \ passkeys", [55]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 30 adds public keys, and two of our machines then run a TLS 1.3 handshake "
            "using this part's authenticated encryption and HMAC; its certificates are logged in Merkle trees. Part "
            "34's file systems checksum every block with a Merkle tree. Part 38's blockchains are hash chains. Part "
            "41's git names every object by its hash. And Part 55 returns to passwords, one-time codes built from "
            "HMAC, and passkeys."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"never invent", r"a cipher, \ a mode or a protocol: \ use TLS 1.3, \ libsodium, \ the platform's AEAD"),
            (r"nonces", r"never repeat one under a key; \ when unsure, \ a misuse-resistant mode \ (AES-GCM-SIV)"),
            (r"passwords", r"Argon2id or scrypt, \ a salt per user, \ never a plain hash"),
            (r"tokens", r"HMAC-signed, \ compared in constant time; \ no secret-dependent branches"),
            (r"randomness", r"only the operating system's: \ \texttt{os.urandom}, \ \texttt{secrets}, \ "
                            r"\texttt{getrandom()}"),
        ])
        with self.voiceover(
            "In practice. Never invent a cipher, a mode or a protocol; use TLS, a library like libsodium, or your "
            "platform's authenticated encryption. Never reuse a nonce, and if you cannot guarantee that, use a mode "
            "designed to survive it. Store passwords with Argon2 or scrypt and a salt per user. Sign tokens with "
            "HMAC and compare tags in constant time. And take randomness only from the operating system."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that perfect secrecy implies $|K| \ge |M|$, \ and that the one-time pad with a uniform key is "
            r"perfectly secret.",
            r"Show that if $G$ is a PRG, \ $c = m \oplus G(k)$ is secure for one message, \ by a reduction; \ then "
            r"break it for two messages under one key.",
            r"Give a distinguisher with advantage near 1 for the 2-round Feistel network, \ and one for 3 rounds "
            r"when decryption queries are allowed.",
            r"Show that CBC-MAC is insecure for messages of different lengths, \ and that prefixing the length "
            r"defeats the splice.",
            r"\textit{Build.} \ Write a padding-oracle server with this part's AES-CBC, \ recover a message and count "
            r"queries; \ then fix it with encrypt-then-MAC.",
            r"$\bigstar$ \textit{Research.} \ For Heys' SPN with 3 to 6 rounds, \ compute the exact expected "
            r"probability of the best differential over all trails, \ and compare it with the best single trail.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: attack your own server, then fix it. The last, marked with a star, is a research problem: how "
            "much trails cluster as rounds grow is not known even for this toy cipher's larger relatives, and the "
            "notes say where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 30, \ Public Keys", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"Diffie--Hellman: \ a secret agreed in public", DATA),
            (r"RSA from scratch, \ and how factoring attacks it", YES),
            (r"elliptic curves: \ the chord, \ the tangent, \ and Curve25519", LAM),
            (r"TLS 1.3 between two machines; \ lattices and ML-KEM", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"Act V: \ limits and secrets", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time: public keys. Everything in this part assumed the two sides already share a key. Part 30 "
            "shows how two strangers can agree on one while everyone listens: Diffie and Hellman's exchange, RSA "
            "built from scratch, elliptic curves, and a full TLS handshake between two of our machines, ending with "
            "the lattices meant to survive a quantum computer. Part 30, Public Keys."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Katz and Lindell, \textit{Introduction to Modern Cryptography}; \ Boneh and Shoup, \textit{A Graduate "
             r"Course in Applied Cryptography}",
             r"Goldreich, \textit{Foundations of Cryptography}; \ Menezes, van Oorschot and Vanstone, "
             r"\textit{Handbook of Applied Cryptography}",
             r"Daemen and Rijmen, \textit{The Design of Rijndael}; \ Ferguson, Schneier and Kohno; \ Kahn, "
             r"\textit{The Codebreakers}; \ Singh"],
            [r"Shannon (1949); \ Rejewski (1981); \ Goldwasser and Micali (1984); \ Yao (1982); \ Blum and Micali "
             r"(1984)",
             r"Goldreich, Goldwasser and Micali (1986); \ Luby and Rackoff (1988); \ H\aa stad et al.\ (1999); \ "
             r"Biham and Shamir (1991)",
             r"Matsui (1993); \ Kocher (1996); \ Bellare, Canetti and Krawczyk (1996); \ Vaudenay (2002); \ Wang "
             r"and Yu (2005)",
             r"Stevens et al.\ (2017); \ Bertoni et al.\ (Keccak); \ FIPS 197, \ RFC 8439, \ SP 800-38D; \ Heys' "
             r"tutorial; \ Liu and Pass (2020)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
