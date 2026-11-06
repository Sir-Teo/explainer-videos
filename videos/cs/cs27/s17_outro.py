from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES)


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
        head = label(rf"Part {PART}: \ Proofs and Randomness", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\mathrm{BPP} \subseteq \mathrm{P/poly}", font_size=44, color=DATA),
                 r"randomness and hardness", DATA),
            tile(MathTex(r"\oplus \notin \mathrm{AC}^0", font_size=50, color=HEAD), r"circuits; \ communication",
                 HEAD),
            tile(MathTex(r"\mathrm{IP} = \mathrm{PSPACE}", font_size=44, color=YES), r"sum-check, \ run", YES),
            tile(MathTex(r"(1 - \tfrac1m)^k", font_size=54, color=LAM), r"zero knowledge", LAM),
            tile(MathTex(r"\tfrac78", font_size=64, color=NO), r"PCP; \ approximation; \ UGC", NO),
            tile(MathTex(r"2^k, \ \mathrm{perm}", font_size=50, color=CTRL), r"fine-grained; \ FPT; \ \#P", CTRL),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Randomized classes, amplification and Adleman's theorem in numbers; "
            "pseudorandomness from hardness. Random restrictions collapsing a formula, and the communication cost "
            "of equality. Interactive proofs, and sum-check run step by step, catching a cheater at the predicted "
            "rate. Zero knowledge, with a simulator nobody can tell from the real thing. The PCP theorem, the "
            "linearity test, and why a coin is the best approximation for MAX-3SAT; the Unique Games Conjecture. "
            "Fine-grained and parameterized complexity, counting, and the average case that cryptography needs."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"codes: \ Reed--Solomon, \ locally testable codes", [28]),
            (r"pseudorandom generators from one-way functions", [29]),
            (r"Fiat--Shamir, \ lattices, \ SNARKs", [30]),
            (r"BQP, \ entanglement and the CHSH game", [53]),
            (r"expanders and Dinur's gap amplification", [56]),
            (r"the hardness of learning", [57]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 28 builds the codes that PCPs are made of: Reed-Solomon, which is "
            "polynomial evaluation, and codes you can test by reading a few symbols. Part 29 builds pseudorandom "
            "generators from one-way functions. Part 30 turns zero knowledge into signatures with Fiat and Shamir, "
            "builds public keys on lattices, and sketches succinct proofs. Part 53 meets entanglement and the game "
            "behind MIP star. Part 56 builds expanders, the engine of Dinur's proof. And Part 57 shows why some "
            "learning problems are hard, using cryptographic assumptions like those of chapter fourteen."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"fingerprints", r"compare huge files by a hash or a polynomial: \ $O(\log n)$ bits"),
            (r"proofs you can check", r"rollups, \ zkVMs, \ delegated computation: \ sum-check inside"),
            (r"zero knowledge", r"prove you know a secret without revealing it: \ identity, \ private payments"),
            (r"stopping rules", r"a SETH or 3SUM lower bound: \ stop chasing the exponent"),
            (r"small parameters", r"exponential in $k$, \ not $n$: \ kernels first, \ then search"),
        ])
        with self.voiceover(
            "In practice. Compare huge files by fingerprints, a few dozen bits instead of all of them. Use "
            "succinct proofs to check computations you did not run yourself. Use zero knowledge to prove you know "
            "a secret without revealing it. Treat a conditional lower bound as a stopping rule. And when a hard "
            "problem has a small parameter, shrink the instance to a kernel and search."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that $O(k)$ independent runs and a majority vote reduce a BPP algorithm's error from $\tfrac13$ "
            r"to $2^{-k}$, \ using a Chernoff bound.",
            r"Prove that deterministic communication for equality on $n$ bits needs $n$ bits, \ with a fooling set.",
            r"Prove that in sum-check a cheating prover survives with probability at most $nd/p$, \ where $d$ is the "
            r"degree in each variable.",
            r"Show that for vertex cover, \ after Buss's rule, \ a yes-instance has at most $k^2$ edges and $k^2 + k$ "
            r"non-isolated vertices.",
            r"\textit{Build.} \ Make chapter 6's sum-check non-interactive with Fiat--Shamir: \ derive each "
            r"challenge by hashing the transcript, \ and verify a proof for a 20-variable formula.",
            r"$\bigstar$ \textit{Research.} \ For functions on $n \le 4$ bits, \ find by exhaustive search the "
            r"minimum BLR rejection rate at each distance $\delta$, \ and compare it with $3\delta - 6\delta^2$, "
            r"\ $\delta$, \ and the known bounds.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: a non-interactive sum-check proof with the Fiat-Shamir transform. The last, marked with a "
            "star, is a research problem: its general answer is not known, and the notes say where to start."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 28, \ Error-Correcting Codes", font_size=42).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"Hamming's weekend jobs, \ and the code that fixed them", DATA),
            (r"Reed--Solomon: \ polynomials that survive scratches", YES),
            (r"Shannon's theorem: \ noise costs only a fixed rate", LAM),
            (r"a scratched QR code, \ recovered", HEAD))]).arrange(DOWN, buff=0.35)
        items.move_to(UP * 0.0)
        q = label(r"Act V: \ limits and secrets", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Next time: errors. In 1947 Richard Hamming's weekend jobs kept dying on bad bits, so he taught the "
            "machine to fix them. Polynomials, the same ones that powered sum-check, become codes that survive "
            "scratches. Claude Shannon proved how much noise costs, and it took fifty years to reach his limit. "
            "We will scratch a QR code and recover its message. Part 28, Error-Correcting Codes."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Arora and Barak, \textit{Computational Complexity}, \ ch. 7--11, 13--14, 18--22; \ Wigderson, "
             r"\textit{Mathematics and Computation}",
             r"Goldreich, \textit{Computational Complexity: A Conceptual Perspective}; \ Thaler, \textit{Proofs, "
             r"Arguments, and Zero-Knowledge}",
             r"Kushilevitz and Nisan, \textit{Communication Complexity}; \ Cygan et al., \textit{Parameterized "
             r"Algorithms}; \ O'Donnell, \textit{Analysis of Boolean Functions}"],
            [r"Lund, Fortnow, Karloff and Nisan (1990); \ Shamir (1990); \ Goldreich, Micali and Wigderson (1986)",
             r"Arora and Safra (1992); \ Arora, Lund, Motwani, Sudan and Szegedy (1992); \ H\aa stad (2001); \ Dinur "
             r"(2007)",
             r"Khot (2002); \ Khot, Minzer and Safra (2018); \ Impagliazzo and Wigderson (1997); \ Valiant (1979)",
             r"Vassilevska Williams (2018); \ Ji, Natarajan, Vidick, Wright and Yuen (2020)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
