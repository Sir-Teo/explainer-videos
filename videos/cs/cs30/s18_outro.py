from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ Public Keys", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"(g^a)^b = (g^b)^a", font_size=48, color=DATA), r"Diffie--Hellman; \ groups", DATA),
            tile(MathTex(r"m^{ed} \equiv m", font_size=52, color=HEAD), r"RSA; \ its padding", HEAD),
            tile(MathTex(r"\rho", font_size=80, color=NO), r"factoring; \ discrete logs", NO),
            tile(MathTex(r"P + Q", font_size=60, color=YES), r"curves; \ signatures", YES),
            tile(MathTex(r"\textsf{TLS 1.3}", font_size=52, color=LAM), r"certificates; \ handshake", LAM),
            tile(MathTex(r"b = As + e", font_size=52, color=CTRL), r"Shor; \ lattices", CTRL),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Merkle's puzzles, and the number theory of groups, from Euclid to Lagrange. "
            "Diffie-Hellman, and RSA from scratch, with the padding oracle that haunted it for twenty years. Factoring "
            "by rho and by a sieve, and discrete logarithms by baby steps, Pohlig-Hellman and index calculus, which set "
            "the key sizes. Elliptic curves, ECDSA, and the repeated nonce that gave away a console's key. "
            "Certificates and a TLS 1.3 handshake. And Shor's threat, with the lattices that answer it."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"QUIC: \ TLS 1.3 inside the transport", [37]),
            (r"signatures in Byzantine agreement", [38]),
            (r"signed releases, \ SBOMs and SLSA", [41]),
            (r"mutual TLS between services", [43]),
            (r"Shor's algorithm factors 15 on our simulator", [53]),
            (r"passkeys; \ Needham--Schroeder and Lowe's attack", [55]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 37's QUIC carries TLS 1.3 inside the transport protocol itself. Part 38 uses "
            "signatures to reach agreement when some machines lie. Part 41 signs software releases, and Part 43 puts "
            "mutual TLS between every pair of services. Part 53 runs Shor's algorithm on our quantum simulator. And "
            "Part 55 returns to authentication: passkeys, and a famous protocol whose flaw went unnoticed for "
            "seventeen years."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"transport", r"TLS 1.3 everywhere, \ certificates from an automated CA \ (ACME)"),
            (r"key types", r"X25519 and Ed25519 or P-256; \ RSA only at 3072 bits or more"),
            (r"signatures", r"deterministic or well-seeded nonces; \ a vetted library, \ never your own"),
            (r"post-quantum", r"enable hybrid X25519 + ML-KEM; \ list which secrets must outlive a decade"),
            (r"private keys", r"in hardware \ (HSMs, \ enclaves); \ backups split with Shamir"),
        ])
        with self.voiceover(
            "In practice. Use TLS 1.3 everywhere, with certificates renewed automatically. Prefer X25519, Ed25519 or "
            "P-256, and RSA only with large keys. Let a vetted library make signatures, with deterministic or "
            "well-seeded nonces. Turn on hybrid post-quantum key exchange, and find out which of your secrets must "
            "stay secret for more than a decade. And keep private keys in hardware, with backups split among people."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that RSA decryption is correct for \textbf{every} $m$ in $\mathbb{Z}_n$, \ including those "
            r"sharing a factor with $n$, \ using the CRT.",
            r"Show that knowing $\varphi(n)$ for $n = pq$ factors $n$; \ and that knowing $e$ and $d$ factors $n$ "
            r"with high probability.",
            r"Show that Pohlig--Hellman takes $O\bigl(\sum_i e_i (\log n + \sqrt{q_i})\bigr)$ group operations "
            r"in a group of order $\prod_i q_i^{e_i}$.",
            r"Derive ECDSA's nonce-reuse recovery, \ and show that knowing $k$ for a \textbf{single} signature "
            r"reveals $d$.",
            r"\textit{Build.} \ Extend the TLS-like handshake to a \textbf{hybrid}, \ X25519 + this part's K-PKE, "
            r"\ and check both sides derive the same keys.",
            r"$\bigstar$ \textit{Research.} \ For LWE with $q = 3329$ and small secrets, \ find the dimension where "
            r"LLL and BKZ stop recovering $s$, \ against the lattice estimator.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build problem: "
            "a hybrid post-quantum handshake between our machines. The last, marked with a star, is a research problem: "
            "where small lattice attacks stop working is a question the standards depend on, and the notes say where "
            "to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 31, \ The Kernel", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"time-sharing: \ one machine, \ many users", DATA),
            (r"user and kernel mode, \ traps and the system call", YES),
            (r"processes, \ fork and exec, \ and the scheduler", LAM),
            (r"queueing theory: \ why 90\% load feels ten times slower", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"Act VI: \ one machine, \ many programs", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "That completes Act Five, on limits and secrets. Next, Act Six: one machine, many programs. Part 31 builds "
            "the kernel: how time-sharing gave every user the illusion of a whole computer, the protection that "
            "required, processes and system calls, the scheduler, and the queueing theory that explains why a busy "
            "server feels so much slower than a quiet one. Part 31, The Kernel."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Katz and Lindell, \textit{Introduction to Modern Cryptography}; \ Boneh and Shoup, \textit{A Graduate "
             r"Course in Applied Cryptography}",
             r"Silverman, \textit{The Arithmetic of Elliptic Curves}; \ Washington, \textit{Elliptic Curves}; \ "
             r"Crandall and Pomerance, \textit{Prime Numbers}",
             r"Peikert, \textit{A Decade of Lattice Cryptography}; \ Galbraith, \textit{Mathematics of Public Key "
             r"Cryptography}"],
            [r"Diffie and Hellman (1976); \ Rivest, Shamir and Adleman (1978); \ Merkle (1978); \ Pollard (1975); \ "
             r"Pomerance (1982)",
             r"Bleichenbacher (1998); \ Bellare and Rogaway (1994); \ Koblitz (1987); \ Miller (1985); \ Bernstein "
             r"(2006)",
             r"Shor (1994); \ LLL (1982); \ Regev (2005); \ FIPS 203--205 (2024); \ RFC 8446, \ 7748, \ 6979, \ 5869",
             r"Schnorr (1991); \ Fiat and Shamir (1986); \ Shamir (1979); \ Gentry (2009); \ Castryck and Decru (2023)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
