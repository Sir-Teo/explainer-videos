from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ Quantum Computation", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"kT \ln 2", font_size=56, color=KERN), r"the price of forgetting", KERN),
            tile(MathTex(r"\alpha|0\rangle + \beta|1\rangle", font_size=48, color=DATA), r"the qubit", DATA),
            tile(MathTex(r"\cos^2 \tfrac{\pi}{8} > \tfrac34", font_size=50, color=YES), r"entanglement wins CHSH", YES),
            tile(MathTex(r"\tfrac{1}{\sqrt{N}} \sum_k \omega^{jk} |k\rangle", font_size=44, color=HEAD), r"the QFT",
                 HEAD),
            tile(MathTex(r"15 = 3 \times 5", font_size=52, color=NO), r"Shor on our simulator", NO),
            tile(MathTex(r"\tfrac{\pi}{4}\sqrt{N}", font_size=56, color=LAM), r"Grover, \ and no faster", LAM),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. The energy cost of erasing a bit, and reversible computation that avoids "
            "it. The qubit, a unit vector of two complex amplitudes, and gates that rotate it on the Bloch sphere. "
            "Entanglement, which wins a game no classical strategy can, and the theorem that forbids copying. "
            "Interference as the resource behind every algorithm: Deutsch–Jozsa, Bernstein–Vazirani and Simon. The "
            "quantum Fourier transform, built from Part 19's butterflies; phase estimation; Shor's algorithm, "
            "factoring fifteen and twenty-one on our own simulator; Grover's square-root search, and the proof that "
            "it cannot be beaten; and error correction, which turns many noisy qubits into fewer good ones."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"verifying quantum and classical programs", [54]),
            (r"trust, \ and the post-quantum migration", [55]),
            (r"expander graphs and quantum codes", [56]),
            (r"semantics of programs, \ quantum ones included", [58]),
            (r"hardware built for one job", [60]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 54 proves programs correct, and the same logic extends to quantum ones. "
            "Part 55 asks what we can trust, the post-quantum migration included. Part 56's expander graphs build "
            "good codes, classical and quantum. Part 58 gives programs mathematical meaning. And Part 60 builds "
            "hardware for a single job, which is what every quantum computer is today."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"plan", r"inventory where RSA and elliptic curves are used; \ migrate to ML-KEM and ML-DSA"),
            (r"experiment", r"run small circuits in Qiskit or Cirq, \ on simulators first"),
            (r"simulate", r"state vectors to about 30 qubits; \ tensor networks beyond, \ for shallow circuits"),
            (r"judge", r"read speedup claims against the best classical algorithm, \ not the naive one"),
            (r"follow", r"logical error rates and code distance, \ not raw qubit counts"),
        ])
        with self.voiceover(
            "In practice. Find every place your systems rely on RSA or elliptic curves, and plan the move to the "
            "new standards. Experiment with small circuits in an open-source toolkit, on a simulator first. A "
            "laptop holds a full state vector of about thirty qubits; tensor networks go further for shallow "
            "circuits. Judge any claimed speedup against the best classical algorithm, not the naive one. And "
            "watch logical error rates, not raw qubit counts."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove the no-cloning theorem: \ no unitary $U$ maps $|\psi\rangle|0\rangle$ to $|\psi\rangle"
            r"|\psi\rangle$ for all $|\psi\rangle$.",
            r"Show that the CHSH game's classical value is $3/4$, \ and that the quantum strategy achieves "
            r"$\cos^2(\pi/8)$.",
            r"Write the QFT on three qubits as gates, \ and check it against the $8 \times 8$ DFT matrix.",
            r"Show that Grover's iteration is a rotation by $2\theta$ with $\sin\theta = 1/\sqrt N$, \ and find the "
            r"best number of iterations for $N = 2^{20}$.",
            r"\textit{Build.} \ Use our simulator to run Shor on $N = 35$, \ and count the shots needed to find the "
            r"order.",
            r"$\bigstar$ \textit{Research.} \ The least space-time volume to factor a 2048-bit number, \ with a "
            r"matching lower bound.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: run Shor's algorithm on thirty-five with our simulator, and count how many runs it takes to "
            "find the order. The last, marked with a star, is a research problem: the smallest machine that can "
            "factor a 2048-bit number, and a proof that nothing smaller can."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 54, \ Proving Programs Correct", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"Floyd and Hoare: \ assertions and invariants", HEAD),
            (r"weakest preconditions", YES),
            (r"separation logic and the heap", DATA),
            (r"verified compilers and kernels", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 54: proving programs correct. Testing can show the presence of bugs but never their "
            "absence. Floyd and Hoare turned programs into logical formulas, and today whole compilers and operating "
            "system kernels come with machine-checked proofs."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Nielsen and Chuang, \ \textit{Quantum Computation and Quantum Information}; \ Mermin, \ "
             r"\textit{Quantum Computer Science}",
             r"Aaronson, \ \textit{Quantum Computing Since Democritus}; \ Preskill's lecture notes"],
            [r"Feynman \ (1982); \ Deutsch \ (1985); \ Shor \ (1994, \ 1997); \ Grover \ (1996)",
             r"Bennett et al. \ (1997); \ Landauer \ (1961); \ Bennett \ (1973); \ Bennett and Brassard \ (1984)",
             r"Gottesman \ (1997); \ Fowler et al. \ (2012); \ Google Quantum AI \ (2024)",
             r"Gidney and Eker\aa{} \ (2019); \ Gidney \ (2025); \ Tang \ (2018)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
