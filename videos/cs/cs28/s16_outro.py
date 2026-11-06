from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ Error-Correcting Codes", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"H r^{\mathsf T} = 5", font_size=50, color=DATA), r"Hamming(7,4); \ distance", DATA),
            tile(MathTex(r"4096 \times 2048 = 2^{23}", font_size=40, color=HEAD), r"bounds; \ the Golay code", HEAD),
            tile(MathTex(r"d = n - k + 1", font_size=46, color=YES), r"GF(256); \ Reed--Solomon", YES),
            tile(MathTex(r"\textsf{QR}", font_size=64, color=LAM), r"a QR code, \ scratched", LAM),
            tile(MathTex(r"C = 1 - H(p)", font_size=46, color=NO), r"CRCs; \ Shannon", NO),
            tile(MathTex(r"0.084", font_size=56, color=CTRL), r"Viterbi, \ LDPC, \ polar", CTRL),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. The noisy channel and the repetition code. Hamming distance, and Hamming's "
            "code, whose syndrome names the bad bit. The bounds on how good any code can be, and the perfect Golay "
            "code, enumerated. The field of bytes, Reed-Solomon codes decoded by Berlekamp and Welch, and our own QR "
            "code, scratched three ways. CRCs from Part 5's shift registers. Shannon's theorem, watched in random "
            "codes. And the codes that reach his limit: Viterbi's trellis, an LDPC waterfall, and polarization."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"AES's S-box: \ inversion in GF(256)", [29]),
            (r"Shamir's secret sharing is a Reed--Solomon code", [30]),
            (r"RAID and checksums in file systems", [34]),
            (r"the CRC in every Ethernet frame", [36]),
            (r"erasure coding, \ failure domains, \ MTTDL", [45]),
            (r"quantum error correction and the surface code", [53]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 29 builds AES, whose S-box is inversion in the field of bytes. Part 30's "
            "secret sharing splits a key with exactly a Reed-Solomon code. Part 34 puts RAID and checksums into "
            "file systems, Part 36 puts a CRC on every Ethernet frame, and Part 45 computes how long erasure-coded "
            "cloud storage survives. And Part 53 needs codes to make quantum computers work at all."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"detect", r"a CRC or checksum on every message and block; \ retry on mismatch"),
            (r"correct", r"ECC memory on servers; \ FEC on links too slow or one-way to retransmit"),
            (r"erase", r"know what is lost: \ erasure codes repair twice as much"),
            (r"choose", r"replication for speed of repair, \ RS or LRC for cost"),
            (r"never roll your own", r"use a tested library: \ the field arithmetic is easy to get subtly wrong"),
        ])
        with self.voiceover(
            "In practice. Detect errors everywhere, with a CRC or checksum, and retry when it fails. Correct them "
            "where retrying is impossible or too slow: memory, deep space, broadcast. Prefer erasures: if you know "
            "what is missing, a code repairs twice as much. Choose replication when repairs must be fast, and "
            "erasure codes when storage costs dominate. And use a tested library: the arithmetic is easy to get "
            "subtly wrong, which is why we checked ours against zlib and a QR library."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that a code with minimum distance $d$ detects $d - 1$ errors and corrects $\lfloor (d-1)/2 "
            r"\rfloor$, \ and that no code can do better.",
            r"Show that a Reed--Solomon code with $n$ evaluation points and messages of degree $< k$ has distance "
            r"exactly $n - k + 1$.",
            r"Prove that a CRC with generator $g(x)$, \ $g(0) = 1$, \ of degree $r$ detects every burst of length "
            r"$\le r$, \ and every odd number of errors if $(x + 1) \mid g(x)$.",
            r"Derive the BEC density-evolution recursion $x \mapsto \epsilon (1 - (1 - x)^{5})^{2}$ for the (3,6) "
            r"code, \ and find its threshold numerically.",
            r"\textit{Build.} \ Encode a version-1 QR code \ (21 $\times$ 21) \ by hand with this part's "
            r"functions, \ and check it against a phone.",
            r"$\bigstar$ \textit{Research.} \ For block lengths 64 to 256 at rate $\tfrac12$ on the BSC, \ compare "
            r"polar SC-list, \ LDPC with BP, \ and the finite-length bound of Polyanskiy, \ Poor and Verd\'u.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: a smaller QR code, made with this part's functions and read by your phone. The last, marked "
            "with a star, is a research problem: its answer is not known, and the notes say where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 29, \ Secrets", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"frequency analysis, \ Enigma, \ and Bletchley Park", DATA),
            (r"perfect secrecy, \ and why it is impractical", YES),
            (r"AES from scratch: \ the field of bytes again", LAM),
            (r"the ECB penguin, \ modes, \ MACs and hashes", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"Act V: \ limits and secrets", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time: secrets. Codes in this part fought random noise. Part 29 faces an adversary. From frequency "
            "analysis and the Enigma to Shannon's perfect secrecy, and then AES, built from scratch on the same "
            "field of bytes, with the modes, hashes and message authentication codes that make it safe to use. Part "
            "29, Secrets."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"MacKay, \textit{Information Theory, Inference, and Learning Algorithms}; \ Cover and Thomas, ch. 7",
             r"Guruswami, Rudra and Sudan, \textit{Essential Coding Theory}; \ Roth, \textit{Introduction to Coding "
             r"Theory}",
             r"MacWilliams and Sloane; \ Richardson and Urbanke, \textit{Modern Coding Theory}; \ Lin and Costello"],
            [r"Shannon (1948); \ Hamming (1950); \ Golay (1949); \ Reed and Solomon (1960); \ Gallager (1962)",
             r"Berlekamp (1968); \ Massey (1969); \ Viterbi (1967); \ Forney (1966); \ Berrou, Glavieux and "
             r"Thitimajshima (1993)",
             r"MacKay and Neal (1996); \ Ar\i kan (2009); \ Luby (2002); \ Guruswami and Rudra (2008); \ Abbe and "
             r"Sandon (2023)",
             r"Dinur, Evra, Livne, Lubotzky and Mozes (2022); \ Panteleev and Kalachev (2022); \ ISO/IEC 18004"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
