# Computer Science, Built — Part 53: Quantum Computation

Part 53 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act X, *Horizons and Trust*. Feynman asked in 1981 whether a
classical computer can simulate quantum physics, and suspected it cannot: n two-state particles need 2ⁿ amplitudes.
A computer made of quantum parts lets those amplitudes interfere; Shor used that to factor and break Part 30's
cryptography, Grover to search in √N steps and no faster, and it is the one serious challenge to Part 1's extended
Church–Turing thesis. We build a state-vector simulator of about a hundred lines and run every algorithm in this part
on it, from Deutsch–Jozsa and Simon to Shor factoring 15 and 21, Grover's search, BB84 and the repetition code.

The instruments are in `explainer/cs/quantum/` (tested in `tests/test_cs53_quantum.py`):
* `sim.py`: the state-vector simulator. n qubits are 2ⁿ complex amplitudes, qubit 0 the most significant bit of the
  index; the gates H, X, Y, Z, S, T and the rotations Rx, Ry, Rz and phase(t); a k-qubit gate applied by viewing the
  state as a 2 × 2 × ⋯ × 2 array, moving the gate's axes to the front and multiplying; controlled gates and CNOT;
  Born-rule probabilities, marginals and sampled measurement; the Bloch vector of a qubit, and the trajectories of H,
  T, S and Rx(π) on the sphere; a unitarity check.
* `algorithms.py`: Landauer's kT ln 2; the Bell state; the CHSH game (the exact quantum value, a sampled one, and a
  search over all 16 deterministic classical strategies); a CNOT "copying" |+⟩; phase oracles; Deutsch–Jozsa on four
  qubits for four functions; Bernstein–Vazirani; Simon's problem, run until one candidate secret is left; the QFT
  circuit checked against its matrix and numpy's FFT, with gate counts; phase estimation; Shor's order finding (the
  work register holding aˣ mod N written in directly, not built from gates) with continued fractions, and the factors;
  Grover's success probability against iterations, amplitude snapshots, and the iterations needed as N grows; BB84
  with and without an intercept-and-resend eavesdropper.
* `qec.py`: the three-qubit bit-flip code (encode, flip, read the two parities, correct); the repetition code of
  distance 1 to 11 under independent bit flips, logical against physical error rate simulated and exact, and the
  factor Λ by which each step in distance divides the logical error rate.

## Chapters

* **Hook.** Feynman's question (1981): n two-state particles need 2ⁿ amplitudes, at 16 bytes each 16 kB for 10,
  16 MB for 20, 16 GB, 16 TB and 16 PB for 30, 40 and 50; at 300, 2³⁰⁰ ≈ 10⁹⁰, more than the roughly 10⁸⁰ atoms in the
  observable universe. The extended Church–Turing thesis challenged: Deutsch (1985), Shor (1994), Grover (1996),
  error correction below threshold in hardware (2024). The part's six objectives.
* **1. The cost of forgetting.** An AND gate maps four inputs to two; erasing a one-molecule memory (illustrative).
  Landauer's principle derived: entropy falls by k ln 2, so Q ≥ kT ln 2 = 2.87 × 10⁻²¹ J ≈ 0.018 eV per bit at 300 K;
  10¹⁸ erasures a second at the limit cost 2.9 mW; measured by Bérut et al. (2012). Toffoli's and Fredkin's gates as
  permutations of the eight states; Bennett's compute, copy, uncompute (1973), the pattern of every oracle in the
  part; permutation matrices are exactly the 0–1 unitaries, and allowing any unitary turns shuffles into rotations
  (Benioff 1980, Feynman 1982, Deutsch 1985).
* **2. The qubit.** α|0⟩ + β|1⟩ and the Born rule; negative amplitudes can cancel; global and relative phase, and
  cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩ as a point on the Bloch sphere, orthogonal states at opposite poles; |+⟩ and |−⟩
  with the same probabilities; P(0) = (1 + z)/2, the arrow's height; measurement leaves a pole; Holevo (1973): n
  qubits sent on their own carry at most n bits; superconducting circuits, trapped ions, neutral atoms, photons.
* **3. Gates, tensor products and entanglement.** H, T, S and Rx(π) as rotations, their paths on the sphere computed
  by our simulator; U†U = I; the tensor product and 2ⁿ amplitudes (2n numbers for a product state); H then CNOT gives
  the Bell state, amplitudes 0.707 on |00⟩ and |11⟩ and probabilities 0.50, proved not to factor. The CHSH game: any
  classical strategy wins at most 3/4 = 0.75 (checked over all sixteen deterministic ones), a shared Bell pair
  measured at 0, π/4 and ±π/8 wins cos²(π/8): 0.854 exact, 0.852 sampled; Tsirelson (1980) and Part 27's MIP* = RE.
  No-cloning in three lines (Wootters and Zurek; Dieks, 1982): a CNOT fed |+⟩|0⟩ makes a Bell pair whose overlap with
  |+⟩|+⟩ is 0.50.
* **4. Circuits and universality.** Reading a circuit right to left as a matrix product; H ⊗ I written out. Toffoli
  from 6 CNOTs, 7 T or T† and 2 H gates, multiplied out to exactly Toffoli's permutation; Barenco et al. (1995).
  THTH = Rz(π/4)Rx(π/4) (up to a global phase) is a rotation by an irrational fraction of a turn
  (cos(θ/2) = cos²(π/8)), its first 160 powers on |0⟩ filling a circle; without T, Gottesman–Knill. The Solovay–Kitaev
  recursion: error to the power 3/2 and five times the gates per level, so length ∝ log^3.97(1/ε); Ross and Selinger's
  O(log 1/ε) for H and T. Our simulator's `apply` in eight lines: a gate mixes amplitudes in pairs, like an FFT stage,
  memory-bound on Part 9's roofline. The Bell circuit in our simulator, Qiskit and Cirq: amplitudes 0.707, 0.000,
  0.000, 0.707; real devices return only samples, after compilation to native gates and routing.
* **5. Interference as a resource.** A coin flipped twice stays a coin; HH|0⟩ = |0⟩ because the two paths to |1⟩
  cancel. Phase kickback: U_f|x⟩|−⟩ = (−1)^f(x)|x⟩|−⟩. Deutsch's problem in one query (the always-correct circuit of
  Cleve, Ekert, Macchiavello and Mosca, 1998), for all four functions. Deutsch–Jozsa on four qubits: the sixteen
  amplitudes after H, the oracle and H again for f = 0, the top bit and the parity; the all-zeros amplitude is the
  average sign, so P(0000) = 1.000 for constant and 0.000 for balanced, against 9 = 2ⁿ⁻¹ + 1 classical queries in the
  worst case. Spread, mark, interfere; measuring straight after the oracle is one classical query; a randomized test
  of k queries is fooled with probability at most 2^(1−k).
* **6. Bernstein–Vazirani and Simon.** f(x) = s·x for s = 1011: four classical queries, one quantum one, which our
  simulator answers with 1011 at probability 1.000. Simon's problem on three bits with s = 110: classically the
  birthday bound, about 2^(n/2) queries; one run yields a y with y·s = 0. Our runs gave 110 and 001, which rule out
  four and then two of the seven candidates and leave 110 after 2 runs; in general a little over n runs and Gaussian
  elimination mod 2. Simon against Shor in one table (the hidden subgroup problem); the separation is relative to an
  oracle.
* **7. The quantum Fourier transform.** The 8 × 8 matrix ω^{jk}/√8 drawn as arrows; the product formula, so a basis
  state's transform is unentangled (j = 5: half, a quarter and five eighths of a turn); from Part 19's butterflies to
  Hadamards, controlled rotations R_k and final swaps. n(n+1)/2 rotations and Hadamards plus ⌊n/2⌋ swaps: 4, 7, 12,
  24 and 40 gates for n = 2, 3, 4, 6, 8, against N log₂ N = 8, 24, 64, 384 and 2,048 for the FFT; our circuit agrees
  with numpy's FFT on a random state to between 1.4 × 10⁻¹⁶ and 2.8 × 10⁻¹⁶. A period-4 state on 16 points becomes
  peaks at 0, 4, 8 and 12; the coefficients cannot be read out, nor arbitrary data loaded cheaply; Coppersmith's
  approximate QFT in O(n log n) gates (1994).
* **8. Phase estimation.** An eigenvalue is a phase e^{2πiθ}, kicked back onto a control; θ = 0.3, a turn of 108°.
  Six counting qubits controlling U^(2^k) turn by 0.3, 0.6, 0.2, 0.4, 0.8 and 0.6; the register is a QFT in product
  form. The inverse QFT gives a geometric series; for the nearest m, |a_m|² ≥ 4/π² ≈ 0.405; phasor chains for m = 19
  (0.875) and m = 20 (0.0547). Our run: θT = 19.2, the peak at m = 19 = 010011, θ ≈ 19/64 = 0.296875 with probability
  0.875, neighbours 0.055 and 0.024. Uses (factoring, chemistry, counting) and the cost: 2⁶ − 1 = 63 applications of
  U for six bits; Kitaev's one-qubit version (1995).
* **9. Shor's algorithm.** Powers of 7 mod 15: 1, 7, 4, 13, period 4; 7² = 49, gcd(48, 15) = 3 and gcd(50, 15) = 5; a
  random a works with probability at least ½. Order finding as phase estimation of multiplication by a, with
  eigenvectors |u_s⟩ that sum to |1⟩. Fifteen with nine counting qubits (512 outcomes): four spikes of 0.25 at 0, 128,
  256 and 384; of 20 shots, 9 give r = 4 at once (384 → 3/4), 256 → 1/2 gives a divisor, 0 nothing. Twenty-one with
  a = 2 and eleven counting qubits (2,048 outcomes): r = 6 does not divide 2,048, so 0.114 on the nearest outcome and
  0.028 on the next; 1707/2048 expanded as a continued fraction gives 5/6, 2³ = 8, gcd(7, 21) = 7 and gcd(9, 21) = 3;
  2,048 ≥ 21² = 441, so s/r is a convergent (Legendre); 7 of 20 shots give s/6 in lowest terms, and an lcm of divisors
  recovers the rest. The number field sieve against n³ gates; RSA-250 (829 bits, about 2,700 core-years, 2020);
  discrete logarithms fall too; "factoring" 15 and 21 on hardware with circuits simplified by the answer (Smolin,
  Smith and Vargo, 2013).
* **10. Grover's search.** Two reflections, the oracle in |s′⟩ and the diffusion in |s⟩, make a rotation by 2θ with
  sin θ = 1/√N; for N = 64 six rounds carry the state just past |w⟩. Inversion about the mean in the 64 amplitudes:
  from 0.125 each, the marked one reaches 0.998 after six rounds and then falls. Success against rounds follows
  sin²((2k+1)θ) exactly: 0.9966 at k = 6 (the formula's 5.77, rounded), 0.0001 at k = 12. Rounds against N: 3, 6, 12,
  25, 50, 100 and 201 for N = 16 to 65,536, against (N + 1)/2 = 8.5 to 32,768.5 classical looks. Quantum counting
  from the eigenvalues e^{±2iθ} (2θ = 0.251 rad for N = 64; Brassard, Høyer and Tapp, 1998); amplitude amplification;
  the BBBV lower bound T ≥ (c/2)√N, sketched.
* **11. What quantum computers cannot do.** BQP defined (accept with probability at least 2/3 or at most 1/3,
  amplified by majority); BPP ⊆ BQP, and BQP ⊆ PP ⊆ PSPACE by Feynman's sum over paths with H and Toffoli (Bernstein
  and Vazirani, 1993; Adleman, DeMarrais and Huang, 1997). NP-complete problems: brute force over 2¹⁶ = 65,536
  assignments still needs 201 Grover rounds; NP ⊄ BQP relative to a random oracle (Bennett et al., 1997); BQP outside
  PH relative to an oracle (Raz and Tal, 2018). Supremacy claims and the replies: Aaronson and Arkhipov and Bremner,
  Jozsa and Shepherd (2011); Google's 53 qubits in about 200 s against an estimated 10,000 years (2019); IBM's 2.5
  days; USTC's boson sampling (2020); tensor networks (Pan, Chen and Zhang, 2022). Query limits: search Θ(√N), parity
  N/2 by the polynomial method, D(f) = O(Q(f)⁶) without a promise (Beals et al., 1998); Holevo's bound.
* **12. Quantum error correction.** Why it seemed impossible: no-cloning, measurement, continuous errors. The
  three-qubit code on 0.6|0⟩ + 0.8|1⟩: syndromes 00, 10, 11 and 01 for no error and a flip of qubit 1, 2 or 3, and
  our simulator restores the amplitudes in all four cases. Measuring the syndrome makes errors discrete (ε = 0.1 rad:
  no error with probability 0.990, a whole flip with 0.010). Shor's nine-qubit code, 6 + 2 = 8 checks; stabilizers
  (Gottesman, 1997). The surface code at distance 5: 24 checks on 25 data qubits, 49 physical qubits in all, a chain
  lighting its ends, any 2 errors corrected. The repetition code for d = 1 to 11 (lines exact, dots from 200,000
  trials): threshold at p = ½, and at p = 1% each step in distance divides the logical error by Λ ≈ 30; surface-code
  thresholds near 1% (Fowler et al., 2012); Google Quantum AI (2024), distance 3 to 5 to 7, Λ ≈ 2.
* **13. Frontier: keys, chemistry and the hardware.** BB84 on 4,000 bits: 1,939 kept, 0% errors without an
  eavesdropper and 26.9% with one measuring and resending (theory 25%); NIST's 2024 post-quantum standards (ML-KEM,
  ML-DSA, SLH-DSA). RSA-2048 resource estimates: about 20 million noisy qubits for about 8 hours (Gidney and Ekerå,
  2019), under a million for under a week (Gidney, 2025), against today's hundreds to about a thousand physical
  qubits; below threshold in 2024, and our repetition code's factor of about 30 per step, which catches only bit
  flips. Simulating nature, cryptanalysis, and weaker cases (Tang, 2018). Four open problems and the ★ research
  problem.
* **Outro.** Recap, payoffs (Parts 54, 55, 56, 58 and 60), practice, problems, next part.

## Build

```bash
python -m videos.cs.cs53.compute
python -m unittest tests.test_cs53_quantum
python tools/build.py cs53
```

## Problems, with solutions

1. **No-cloning.** Prove that no unitary U maps |ψ⟩|0⟩ to |ψ⟩|ψ⟩ for every state |ψ⟩.

   *Solution.* Suppose U|ψ⟩|0⟩ = |ψ⟩|ψ⟩ and U|φ⟩|0⟩ = |φ⟩|φ⟩ for two unit vectors. A unitary preserves inner products,
   so the inner product of the two left sides equals that of the two right sides: ⟨φ|ψ⟩⟨0|0⟩ = ⟨φ|ψ⟩², that is x = x²
   with x = ⟨φ|ψ⟩. So x = 0 or x = 1: the states are orthogonal or, by Cauchy–Schwarz, equal. A machine that copied
   every state would copy |0⟩ and |+⟩, whose overlap is 1/√2, a contradiction. Linearity gives the same answer
   directly: if U copies |0⟩ and |1⟩, then U|+⟩|0⟩ = (|00⟩ + |11⟩)/√2, a Bell pair, not
   |+⟩|+⟩ = (|00⟩ + |01⟩ + |10⟩ + |11⟩)/2; their overlap is 2 · (1/√2)(1/2) = 1/√2 and the fidelity 1/2, which is what
   our simulator's CNOT gives (0.50). Extra working space does not help: if U|ψ⟩|0⟩|0⟩ = |ψ⟩|ψ⟩|e_ψ⟩, then
   x = x²⟨e_φ|e_ψ⟩, so |x| ≤ |x|² and |x| is 0 or 1 again. The theorem forbids copying unknown states, not known
   orthogonal ones: CNOT fans out basis states, which is why classical bits can be copied.

2. **CHSH.** Show that the CHSH game's classical value is 3/4, and that the quantum strategy achieves cos²(π/8).

   *Solution.* A deterministic strategy fixes Alice's answers a₀, a₁ and Bob's b₀, b₁. Winning on all four questions
   needs a₀ ⊕ b₀ = 0, a₀ ⊕ b₁ = 0, a₁ ⊕ b₀ = 0 and a₁ ⊕ b₁ = 1. The XOR of the left sides is 0, since each variable
   appears twice, and the XOR of the right sides is 1, so at most three hold, and with uniform questions the strategy
   wins at most 3/4; always answering 0 achieves it. A randomized strategy, with private or shared coins, is a mixture
   of deterministic ones and its winning probability is their average, so it too is at most 3/4. Our instrument's
   search over all sixteen deterministic strategies returns 0.75. Quantumly, share |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 and let
   measuring at angle A mean the basis |A⟩ = cos A|0⟩ + sin A|1⟩ (answer 0), |A⊥⟩ = −sin A|0⟩ + cos A|1⟩ (answer 1).
   Then ⟨A|⟨B|Φ⁺⟩ = (cos A cos B + sin A sin B)/√2 = cos(A − B)/√2, and likewise ⟨A⊥|⟨B⊥|Φ⁺⟩ = cos(A − B)/√2, so
   P(a = b) = cos²(A − B). Take A = 0 or π/4 for x = 0 or 1, and B = π/8 or −π/8 for y = 0 or 1. In the three cases
   other than x = y = 1, |A − B| = π/8 and agreement wins: cos²(π/8). For x = y = 1, A − B = 3π/8 and disagreement
   wins: sin²(3π/8) = cos²(π/8). The value is cos²(π/8) = (2 + √2)/4 ≈ 0.8536; our simulator gives 0.854 exactly and
   0.852 over 200,000 sampled rounds. Each side's answers alone are fair coins, so no message passes; Tsirelson (1980)
   proved that no quantum strategy does better.

3. **The QFT on three qubits.** Write the QFT on three qubits as gates, and check it against the 8 × 8 DFT matrix.

   *Solution.* Write j = 4j₁ + 2j₂ + j₃ and k = 4k₁ + 2k₂ + k₃ (qubit 1 the most significant) and ω = e^{2πi/8}. Then
   ω^{jk} = e^{2πi jk₁/2} e^{2πi jk₂/4} e^{2πi jk₃/8}, and whole turns drop out, so
   QFT|j⟩ = (1/√8)(|0⟩ + e^{2πi 0.j₃}|1⟩)(|0⟩ + e^{2πi 0.j₂j₃}|1⟩)(|0⟩ + e^{2πi 0.j₁j₂j₃}|1⟩) in binary fractions.
   With R_k = diag(1, e^{2πi/2^k}) the circuit is: H on qubit 1, which gives |0⟩ + e^{2πi 0.j₁}|1⟩; R₂ on qubit 1
   controlled by qubit 2, adding j₂/4 of a turn; R₃ on qubit 1 controlled by qubit 3, adding j₃/8, so qubit 1 holds
   0.j₁j₂j₃; H on qubit 2 and R₂ controlled by qubit 3, giving 0.j₂j₃; H on qubit 3, giving 0.j₃; and a SWAP of qubits
   1 and 3, because the factors come out in reverse order. That is six gates and one swap, n(n + 1)/2 + ⌊n/2⌋ = 7, as
   our instrument counts. Check: on |001⟩ (j = 1) the circuit leaves phases of 1/8, 1/4 and 1/2 of a turn on qubits 1,
   2 and 3, and after the swap the amplitude of |k⟩ is e^{2πi(k₁/2 + k₂/4 + k₃/8)}/√8 = ω^k/√8, column 1 of the matrix
   ω^{jk}/√8; on |101⟩ (j = 5) the phases after the swap are 1/2, 1/4 and 5/8, as in chapter 7. Equality on the eight
   basis states proves equality of the matrices, by linearity. Numerically, `qft_check(3)` applies the circuit to a
   random state and agrees with the matrix to 1.7 × 10⁻¹⁵, and with numpy's FFT of the +i sign convention (`ifft`
   times √8) to 2.5 × 10⁻¹⁶.

4. **Grover.** Show that Grover's iteration is a rotation by 2θ with sin θ = 1/√N, and find the best number of
   iterations for N = 2²⁰.

   *Solution.* Let |s′⟩ be the even superposition of the N − 1 unmarked states. The start |s⟩ = sin θ|w⟩ + cos θ|s′⟩,
   with sin θ = ⟨w|s⟩ = 1/√N, lies in the plane of |s′⟩ and |w⟩, and both O = I − 2|w⟩⟨w| and D = 2|s⟩⟨s| − I map that
   plane to itself. In coordinates (|s′⟩, |w⟩), O fixes |s′⟩ and negates |w⟩, a reflection in the line at angle 0; D
   fixes |s⟩ and negates the direction perpendicular to it, a reflection in the line at angle θ. A reflection in the
   line at angle α has matrix [[cos 2α, sin 2α], [sin 2α, −cos 2α]], so DO = [[cos 2θ, sin 2θ],
   [sin 2θ, −cos 2θ]] · [[1, 0], [0, −1]] = [[cos 2θ, −sin 2θ], [sin 2θ, cos 2θ]], the rotation by 2θ. Hence
   (DO)^k|s⟩ = sin((2k + 1)θ)|w⟩ + cos((2k + 1)θ)|s′⟩, and the success probability is sin²((2k + 1)θ), largest when
   (2k + 1)θ is nearest π/2, at k ≈ π/(4θ) − 1/2. For N = 2²⁰ = 1,048,576, θ = arcsin(2⁻¹⁰) = 9.765627 × 10⁻⁴ rad and
   π/(4θ) − 1/2 = 803.75, so k = 804 (close to (π/4)√N = 804.2). Then P = sin²(1609θ) = 0.99999976, a failure
   probability of 2.4 × 10⁻⁷, against 2.1 × 10⁻⁶ at 803 and 6.0 × 10⁻⁶ at 805; a classical search in random order
   needs (N + 1)/2 = 524,288.5 looks on average.

5. **Build.** Use our simulator to run Shor on N = 35, and count the shots needed to find the order.

   *Solution notes.* Call `algorithms.shor(35, a)` (or `order_finding(a, 35, shots=...)` for more shots) for an a
   coprime to 35. The orders divide λ(35) = lcm(4, 6) = 12; of the 24 residues coprime to 35, 18 have an even order r
   with a^(r/2) ≢ −1 (the exceptions are 1, 11 and 16, of odd order, and 19, 24 and 34, with a^(r/2) ≡ −1), so a
   random a works with probability 3/4. With a = 2, r = 12 (2¹² = 4,096 = 117 · 35 + 1); the instrument uses
   t = 2⌈log₂ 35⌉ + 1 = 13 counting qubits, Q = 8,192 ≥ 35² = 1,225. Since 12 does not divide 8,192, only the four
   peaks at 0, 2,048, 4,096 and 6,144 are sharp (1/12 each); the other eight are smeared over neighbours (0.057 on the
   nearest outcome), and the twelve nearest outcomes hold 0.789 of the probability. Each shot y becomes y/Q in lowest
   terms with denominator at most 35 (`Fraction.limit_denominator`); its denominator is 12 exactly when the nearby
   s/12 has s coprime to 12. The exact probability that one shot gives r = 12 at once is 0.329, so about 3.0 shots on
   average; keeping the lcm of the denominators seen so far, and stopping when 2^lcm ≡ 1, needs 2.3 on average (from
   100,000 simulated runs of the exact distribution: one shot 33% of the time, two 33%, three 18%). Our seed-0 run of
   20 shots: the first, 4,779 → 7/12, already gives 12, and 4 of the 20 do (4,779 twice, 7,509 → 11/12 and
   3,412 → 5/12); the rest give 5/6, 3/4, 2/3, 1/2, 1/4, 1/6 or 0. Then 2⁶ = 64 ≡ 29 ≢ −1, gcd(63, 35) = 7 and
   gcd(65, 35) = 5: 35 = 5 × 7. A complete answer tabulates the count for several a (a = 4 or 9 has r = 6, a = 8 has
   r = 4, a = 6 has r = 2) and states the caveat honestly: our simulator writes aˣ mod N into the work register, so
   the count is of shots, not gates; a full state vector would need 13 + 6 = 19 qubits, 2¹⁹ amplitudes or 8 MB, and a
   reversible modular multiplier built from chapter 1's Toffoli gates would change the gate count but not these
   statistics.

6. **★ Research.** Find the least space-time volume of physical qubits needed to factor a 2048-bit number at a
   physical error rate of 10⁻³, with a matching lower bound.

   *Discussion.* Open. Every number we have is an upper bound from an explicit compilation: Shor's arithmetic laid out
   in logical qubits, the logical qubits in surface-code patches, and the cost of the non-Clifford gates and of idle
   storage counted. Taking the published headline figures at face value, about 20 million qubits for about 8 hours
   (Gidney and Ekerå, 2019) is about 1.6 × 10⁸ qubit-hours, and under a million qubits for under a week (Gidney, 2025)
   is under 1.7 × 10⁸: the qubit count fell more than twentyfold while the volume stayed of the same order, so the two
   figures of merit pull apart. A matching lower bound is out of reach for a deeper reason: a reversible classical
   circuit is a quantum circuit, so any nontrivial lower bound on the volume needed to factor would also bound
   classical circuits for factoring 2048-bit numbers, which Part 26's barriers put beyond current techniques. A good
   partial answer would fix the metric (physical qubits times surface-code cycles, under a stated noise model), lower
   the best upper bound with a resource estimate others can reproduce, or prove a lower bound inside a stated model,
   for example for Shor-style period finding with a fixed code and gate set, in terms of the logical qubits,
   non-Clifford gates and code distance it must use.

## 习题与解答

1. **不可克隆。** 证明不存在幺正算子 U，对每个态 |ψ⟩ 都把 |ψ⟩|0⟩ 映为 |ψ⟩|ψ⟩。

   *解答。* 设对两个单位向量有 U|ψ⟩|0⟩ = |ψ⟩|ψ⟩ 与 U|φ⟩|0⟩ = |φ⟩|φ⟩。幺正算子保持内积，所以两个左边的内积等于两个右边的
   内积：⟨φ|ψ⟩⟨0|0⟩ = ⟨φ|ψ⟩²，即 x = x²，其中 x = ⟨φ|ψ⟩。于是 x = 0 或 x = 1：两个态要么正交，要么（由柯西–施瓦茨不等式）
   相等。能复制一切态的机器必须复制 |0⟩ 和 |+⟩，而它们的重叠是 1/√2，矛盾。用线性也能直接看出：若 U 复制 |0⟩ 和 |1⟩，则
   U|+⟩|0⟩ = (|00⟩ + |11⟩)/√2，是一个贝尔对，而不是 |+⟩|+⟩ = (|00⟩ + |01⟩ + |10⟩ + |11⟩)/2；两者的重叠是
   2 · (1/√2)(1/2) = 1/√2，保真度 1/2，正是我们模拟器里的 CNOT 给出的 0.50。额外的工作空间也无济于事：若
   U|ψ⟩|0⟩|0⟩ = |ψ⟩|ψ⟩|e_ψ⟩，则 x = x²⟨e_φ|e_ψ⟩，所以 |x| ≤ |x|²，|x| 仍只能是 0 或 1。这个定理禁止的是复制未知的态，
   而不是已知的正交态：CNOT 可以扇出基态，所以经典比特可以复制。

2. **CHSH。** 证明 CHSH 博弈的经典值是 3/4，并证明量子策略达到 cos²(π/8)。

   *解答。* 确定性策略固定 Alice 的回答 a₀、a₁ 和 Bob 的 b₀、b₁。四个问题都赢需要 a₀ ⊕ b₀ = 0、a₀ ⊕ b₁ = 0、
   a₁ ⊕ b₀ = 0 和 a₁ ⊕ b₁ = 1。左边的异或为 0，因为每个变量出现两次；右边的异或为 1，所以至多三个成立，问题均匀随机时
   这个策略至多赢 3/4；总回答 0 就能达到。随机策略，无论用私有还是共享的硬币，都是确定性策略的混合，赢的概率是它们的
   平均，所以也至多 3/4。我们的工具搜索全部十六个确定性策略，得到 0.75。量子地，共享 |Φ⁺⟩ = (|00⟩ + |11⟩)/√2，并约定
   “沿角度 A 测量”指在基 |A⟩ = cos A|0⟩ + sin A|1⟩（回答 0）、|A⊥⟩ = −sin A|0⟩ + cos A|1⟩（回答 1）下测量。于是
   ⟨A|⟨B|Φ⁺⟩ = (cos A cos B + sin A sin B)/√2 = cos(A − B)/√2，同样 ⟨A⊥|⟨B⊥|Φ⁺⟩ = cos(A − B)/√2，所以
   P(a = b) = cos²(A − B)。x = 0 或 1 时取 A = 0 或 π/4，y = 0 或 1 时取 B = π/8 或 −π/8。除 x = y = 1 外的三种情形中
   |A − B| = π/8，一致就赢：cos²(π/8)。x = y = 1 时 A − B = 3π/8，不一致才赢：sin²(3π/8) = cos²(π/8)。博弈值为
   cos²(π/8) = (2 + √2)/4 ≈ 0.8536；我们的模拟器给出精确值 0.854，200,000 轮抽样得 0.852。单看任何一方，回答都是公平的
   硬币，所以没有传递任何消息；Tsirelson（1980）证明了没有量子策略能做得更好。

3. **三个量子比特上的 QFT。** 把三个量子比特上的 QFT 写成门，并与 8 × 8 的 DFT 矩阵核对。

   *解答。* 记 j = 4j₁ + 2j₂ + j₃，k = 4k₁ + 2k₂ + k₃（量子比特 1 是最高位），ω = e^{2πi/8}。则
   ω^{jk} = e^{2πi jk₁/2} e^{2πi jk₂/4} e^{2πi jk₃/8}，整圈不起作用，所以用二进制小数写，
   QFT|j⟩ = (1/√8)(|0⟩ + e^{2πi 0.j₃}|1⟩)(|0⟩ + e^{2πi 0.j₂j₃}|1⟩)(|0⟩ + e^{2πi 0.j₁j₂j₃}|1⟩)。取
   R_k = diag(1, e^{2πi/2^k})，电路是：量子比特 1 上的 H，得到 |0⟩ + e^{2πi 0.j₁}|1⟩；由量子比特 2 控制、作用在量子比特 1
   上的 R₂，加上 j₂/4 圈；由量子比特 3 控制、作用在量子比特 1 上的 R₃，加上 j₃/8 圈，于是量子比特 1 存的是 0.j₁j₂j₃；
   量子比特 2 上的 H 和由量子比特 3 控制的 R₂，得到 0.j₂j₃；量子比特 3 上的 H，得到 0.j₃；最后交换量子比特 1 和 3，因为
   各因子是倒序出来的。一共六个门加一次交换，n(n + 1)/2 + ⌊n/2⌋ = 7，与我们的工具的计数一致。核对：在 |001⟩（j = 1）上，
   电路在量子比特 1、2、3 上留下 1/8、1/4、1/2 圈的相位，交换之后 |k⟩ 的振幅是
   e^{2πi(k₁/2 + k₂/4 + k₃/8)}/√8 = ω^k/√8，正是矩阵 ω^{jk}/√8 的第 1 列；在 |101⟩（j = 5）上，交换后的相位是 1/2、1/4
   和 5/8，与第 7 章一致。由线性，在八个基态上相等就证明了两个矩阵相等。数值上，`qft_check(3)` 把电路作用在一个随机态上，
   与矩阵相差 1.7 × 10⁻¹⁵，与 numpy 中取 +i 符号约定的 FFT（`ifft` 乘以 √8）相差 2.5 × 10⁻¹⁶。

4. **Grover。** 证明 Grover 迭代是转过 2θ 的旋转，其中 sin θ = 1/√N，并求 N = 2²⁰ 时最好的迭代次数。

   *解答。* 令 |s′⟩ 为 N − 1 个未标记态的均匀叠加。初态 |s⟩ = sin θ|w⟩ + cos θ|s′⟩，其中 sin θ = ⟨w|s⟩ = 1/√N，
   它位于 |s′⟩ 与 |w⟩ 张成的平面内，而 O = I − 2|w⟩⟨w| 和 D = 2|s⟩⟨s| − I 都把这个平面映到自身。在坐标 (|s′⟩, |w⟩) 下，
   O 保持 |s′⟩、把 |w⟩ 变号，是关于角度为 0 的直线的反射；D 保持 |s⟩、把与它垂直的方向变号，是关于角度为 θ 的直线的反射。
   关于角度为 α 的直线的反射矩阵是 [[cos 2α, sin 2α], [sin 2α, −cos 2α]]，所以
   DO = [[cos 2θ, sin 2θ], [sin 2θ, −cos 2θ]] · [[1, 0], [0, −1]] = [[cos 2θ, −sin 2θ], [sin 2θ, cos 2θ]]，即转过 2θ 的
   旋转。因此 (DO)^k|s⟩ = sin((2k + 1)θ)|w⟩ + cos((2k + 1)θ)|s′⟩，成功概率为 sin²((2k + 1)θ)，在 (2k + 1)θ 最接近 π/2
   时最大，即 k ≈ π/(4θ) − 1/2。N = 2²⁰ = 1,048,576 时，θ = arcsin(2⁻¹⁰) = 9.765627 × 10⁻⁴ 弧度，
   π/(4θ) − 1/2 = 803.75，所以 k = 804（接近 (π/4)√N = 804.2）。此时 P = sin²(1609θ) = 0.99999976，失败概率
   2.4 × 10⁻⁷，而 803 次时为 2.1 × 10⁻⁶，805 次时为 6.0 × 10⁻⁶；经典的随机顺序搜索平均要看 (N + 1)/2 = 524,288.5 次。

5. **动手。** 用我们的模拟器对 N = 35 运行 Shor 算法，数一数找到阶需要多少次测量（shot）。

   *解答要点。* 对与 35 互素的 a 调用 `algorithms.shor(35, a)`（要更多次测量就用 `order_finding(a, 35, shots=...)`）。各个
   阶都整除 λ(35) = lcm(4, 6) = 12；在与 35 互素的 24 个剩余中，有 18 个的阶 r 是偶数且 a^(r/2) ≢ −1（例外是阶为奇数的 1、
   11 和 16，以及 a^(r/2) ≡ −1 的 19、24 和 34），所以随机取 a 成功的概率是 3/4。取 a = 2，r = 12
   （2¹² = 4,096 = 117 · 35 + 1）；工具用 t = 2⌈log₂ 35⌉ + 1 = 13 个计数量子比特，Q = 8,192 ≥ 35² = 1,225。因为 12
   不整除 8,192，只有 0、2,048、4,096 和 6,144 处的四个峰是尖锐的（各 1/12）；其余八个峰摊到相邻结果上（最近的结果上
   0.057），离十二个峰最近的结果共占 0.789 的概率。每次测量得到的 y 化成分母不超过 35 的最简分数 y/Q
   （`Fraction.limit_denominator`）；当附近的 s/12 中 s 与 12 互素时，分母恰为 12。一次测量直接给出 r = 12 的精确概率是
   0.329，所以平均约需 3.0 次；若记下目前所见各分母的最小公倍数，在 2^lcm ≡ 1 时停止，平均只需 2.3 次（对精确分布模拟
   100,000 轮：33% 的情形一次，33% 两次，18% 三次）。我们 seed 0 的 20 次测量：第一次 4,779 → 7/12 就已给出 12，20 次中
   有 4 次如此（4,779 两次，7,509 → 11/12 和 3,412 → 5/12）；其余给出 5/6、3/4、2/3、1/2、1/4、1/6 或 0。然后
   2⁶ = 64 ≡ 29 ≢ −1，gcd(63, 35) = 7，gcd(65, 35) = 5：35 = 5 × 7。完整的答案应对几个 a 列出次数（a = 4 或 9 时
   r = 6，a = 8 时 r = 4，a = 6 时 r = 2），并如实说明前提：我们的模拟器直接把 aˣ mod N 写进工作寄存器，所以数的是测量
   次数而不是门数；完整的状态向量需要 13 + 6 = 19 个量子比特，即 2¹⁹ 个振幅、8 MB；用第 1 章的托福利门搭出可逆的模乘法器
   会改变门数，但不改变这些统计。

6. **★ 研究。** 求在物理错误率 10⁻³ 下分解一个 2048 位数所需物理量子比特的最小时空体积，并给出相匹配的下界。

   *讨论。* 尚未解决。我们手里的每个数都是来自显式编译的上界：把 Shor 算法的算术排成逻辑量子比特，把逻辑量子比特放进
   表面码的码块，再计入非 Clifford 门和空闲存储的代价。按发表的主要数字计算，约 2000 万个量子比特运行约 8 小时（Gidney
   与 Ekerå，2019）约为 1.6 × 10⁸ 量子比特·小时，不到一百万个量子比特运行不到一周（Gidney，2025）不到 1.7 × 10⁸：量子比特
   数降到二十分之一以下，体积却仍在同一量级，所以这两个指标并不一致。相匹配的下界之所以遥不可及，还有更深的原因：可逆的经典
   电路也是量子电路，所以任何非平凡的时空体积下界，也会给分解 2048 位数的经典电路一个下界，而第 26 部分的障碍表明这超出了
   现有技术。好的部分结果可以是：固定度量（物理量子比特数乘以表面码周期数，并说明噪声模型）；用别人能复现的资源估计
   降低最好的上界；或在一个明确的模型里证明下界，例如对固定编码和门集的 Shor 式周期寻找，用它必须使用的逻辑量子比特、
   非 Clifford 门和码距来表示。

## Glossary additions

* **Landauer's principle, reversible computing, Toffoli and Fredkin gates, uncomputation** — erasing a bit costs at
  least kT ln 2 of heat; computing by permutations of states; three-bit gates that lose nothing; running a circuit
  backwards to clear its garbage.
* **qubit, amplitude, Born rule, superposition** — a two-level quantum system; the complex coefficients of its state;
  probability as the squared size of an amplitude; a state with more than one nonzero amplitude.
* **global and relative phase, Bloch sphere** — a factor no measurement sees; the phase between amplitudes that
  interference does see; a qubit's state as a point on a sphere, orthogonal states at opposite points.
* **unitary, Hadamard, Pauli X, Y, Z, phase gates S and T, CNOT** — a matrix with U†U = I, a rotation of the state;
  the common one- and two-qubit gates.
* **tensor product, product state, entanglement, Bell state** — the joint state of independent systems; a state that
  factors; one that does not; (|00⟩ + |11⟩)/√2.
* **CHSH game, Tsirelson's bound, no-cloning theorem** — a nonlocal game won 3/4 of the time classically and
  cos²(π/8) quantumly; the quantum maximum; no unitary copies unknown states.
* **universal gate set, Clifford gates, Gottesman–Knill theorem, Solovay–Kitaev theorem** — gates that approximate
  every unitary; H, S and CNOT; circuits of them simulated efficiently classically; approximation with
  polylogarithmically many gates.
* **state-vector simulation** — storing all 2ⁿ amplitudes and applying gates as small matrix products along axes.
* **oracle, phase kickback, interference** — a reversible black box for f; f(x) written into a sign; amplitudes
  reinforcing and cancelling.
* **Deutsch–Jozsa, Bernstein–Vazirani, Simon's problem, hidden subgroup problem, oracle separation** — the first
  problems where interference wins; finding a hidden period of a function on a group; a gap proved relative to a black
  box.
* **quantum Fourier transform, controlled rotation R_k, approximate QFT** — the DFT on amplitudes in O(n²) gates; its
  phase gates; dropping the smallest rotations for O(n log n).
* **phase estimation, counting register** — reading an eigenvalue's phase to t bits with t control qubits and an
  inverse QFT.
* **order, order finding, Shor's algorithm, continued fractions, convergent** — the least r with aʳ ≡ 1 (mod N);
  finding it by phase estimation; factoring from it; recovering s/r from a measured y/2ᵗ.
* **Grover's algorithm, diffusion (inversion about the mean), amplitude amplification, quantum counting** — search in
  about (π/4)√N queries; the reflection in the start state; the same speed-up for any algorithm; counting solutions by
  phase estimation.
* **BQP, PP, PSPACE, polynomial method, Holevo bound** — bounded-error quantum polynomial time and the classes around
  it; lower bounds from the degree of acceptance polynomials; n qubits carry at most n classical bits.
* **quantum supremacy (advantage), random circuit sampling, boson sampling** — a task done by quantum hardware faster
  than by any known classical method; two such tasks.
* **bit flip, phase flip, syndrome, stabilizer, logical and physical qubit, code distance** — X and Z errors; the
  measured parities that locate an error; a Pauli product fixing every codeword; the encoded qubit and its carriers;
  the fewest errors that cause a logical error.
* **surface code, decoder, minimum-weight matching, threshold, Λ** — a code of local parity checks on a lattice; the
  algorithm that pairs lit checks; the physical error rate below which bigger codes are better; the factor gained per
  step in distance.
* **BB84, intercept-and-resend, post-quantum cryptography (ML-KEM, ML-DSA, SLH-DSA)** — key distribution whose
  eavesdroppers cause errors; the simplest attack, a 25% error rate; classical schemes not known to fall to Shor.
* **resource estimate, space-time volume** — the qubits and time a fault-tolerant algorithm needs; their product.

## Sources

* M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information* (10th anniversary ed., 2010);
  N. D. Mermin, *Quantum Computer Science: An Introduction* (2007); S. Aaronson, *Quantum Computing Since Democritus*
  (2013); A. Yu. Kitaev, A. H. Shen and M. N. Vyalyi, *Classical and Quantum Computation* (2002); J. Watrous, *The
  Theory of Quantum Information* (2018); R. de Wolf, *Quantum Computing: Lecture Notes*; J. Preskill, lecture notes
  for Caltech's Physics 219.
* R. Landauer, "Irreversibility and heat generation in the computing process", IBM J. Res. Dev. 1961; C. H. Bennett,
  "Logical reversibility of computation", IBM J. Res. Dev. 1973; E. Fredkin and T. Toffoli, "Conservative logic",
  Int. J. Theor. Phys. 1982; A. Bérut et al., "Experimental verification of Landauer's principle linking information
  and thermodynamics", Nature 2012.
* R. P. Feynman, "Simulating physics with computers", Int. J. Theor. Phys. 1982; D. Deutsch, "Quantum theory, the
  Church–Turing principle and the universal quantum computer", Proc. R. Soc. Lond. A 1985; D. Deutsch and R. Jozsa,
  "Rapid solution of problems by quantum computation", Proc. R. Soc. Lond. A 1992; R. Cleve, A. Ekert,
  C. Macchiavello and M. Mosca, "Quantum algorithms revisited", Proc. R. Soc. Lond. A 1998.
* E. Bernstein and U. Vazirani, "Quantum complexity theory", STOC 1993 (SIAM J. Comput. 1997); D. R. Simon, "On the
  power of quantum computation", FOCS 1994 (SIAM J. Comput. 1997).
* P. W. Shor, "Algorithms for quantum computation: discrete logarithms and factoring", FOCS 1994, and
  "Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer", SIAM J. Comput.
  1997; D. Coppersmith, "An approximate Fourier transform useful in quantum factoring", IBM research report, 1994;
  A. Yu. Kitaev, "Quantum measurements and the Abelian stabilizer problem", 1995.
* L. K. Grover, "A fast quantum mechanical algorithm for database search", STOC 1996; C. H. Bennett, E. Bernstein,
  G. Brassard and U. Vazirani, "Strengths and weaknesses of quantum computing", SIAM J. Comput. 1997; G. Brassard,
  P. Høyer and A. Tapp, "Quantum counting", ICALP 1998; G. Brassard, P. Høyer, M. Mosca and A. Tapp, "Quantum
  amplitude amplification and estimation", 2002.
* A. Barenco et al., "Elementary gates for quantum computation", Phys. Rev. A 1995; C. M. Dawson and M. A. Nielsen,
  "The Solovay–Kitaev algorithm", Quantum Inf. Comput. 2006; N. J. Ross and P. Selinger, "Optimal ancilla-free
  Clifford+T approximation of z-rotations", Quantum Inf. Comput. 2016.
* B. S. Tsirelson (Cirel'son), "Quantum generalizations of Bell's inequality", Lett. Math. Phys. 1980;
  W. K. Wootters and W. H. Zurek, "A single quantum cannot be cloned", Nature 1982; D. Dieks, "Communication by EPR
  devices", Phys. Lett. A 1982; A. S. Holevo, "Bounds for the quantity of information transmitted by a quantum
  communication channel", Probl. Inf. Transm. 1973.
* L. M. Adleman, J. DeMarrais and M.-D. A. Huang, "Quantum computability", SIAM J. Comput. 1997; R. Beals,
  H. Buhrman, R. Cleve, M. Mosca and R. de Wolf, "Quantum lower bounds by polynomials", FOCS 1998; R. Raz and A. Tal,
  "Oracle separation of BQP and PH", STOC 2019 (ECCC 2018).
* S. Aaronson and A. Arkhipov, "The computational complexity of linear optics", STOC 2011; M. J. Bremner, R. Jozsa
  and D. J. Shepherd, "Classical simulation of commuting quantum computations implies collapse of the polynomial
  hierarchy", Proc. R. Soc. A 2011; F. Arute et al., "Quantum supremacy using a programmable superconducting
  processor", Nature 2019; E. Pednault et al., "Leveraging secondary storage to simulate deep 54-qubit Sycamore
  circuits", 2019; H.-S. Zhong et al., "Quantum computational advantage using photons", Science 2020; F. Pan, K. Chen
  and P. Zhang, "Solving the sampling problem of the Sycamore quantum circuits", Phys. Rev. Lett. 2022.
* P. W. Shor, "Scheme for reducing decoherence in quantum computer memory", Phys. Rev. A 1995; A. M. Steane, "Error
  correcting codes in quantum theory", Phys. Rev. Lett. 1996; D. Gottesman, *Stabilizer Codes and Quantum Error
  Correction*, PhD thesis, Caltech 1997; A. Yu. Kitaev, "Fault-tolerant quantum computation by anyons", 1997
  (Ann. Phys. 2003); E. Dennis, A. Kitaev, A. Landahl and J. Preskill, "Topological quantum memory", J. Math. Phys.
  2002; A. G. Fowler, M. Mariantoni, J. M. Martinis and A. N. Cleland, "Surface codes: towards practical large-scale
  quantum computation", Phys. Rev. A 2012; Google Quantum AI and collaborators, "Quantum error correction below the
  surface code threshold", Nature 2024.
* C. H. Bennett and G. Brassard, "Quantum cryptography: public key distribution and coin tossing", Proc. IEEE Int.
  Conf. on Computers, Systems and Signal Processing, Bangalore 1984; NIST, FIPS 203, 204 and 205 (2024).
* C. Gidney and M. Ekerå, "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits", 2019
  (Quantum 2021); C. Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits", 2025;
  F. Boudot, P. Gaudry, A. Guillevic, N. Heninger, E. Thomé and P. Zimmermann, the factorization of RSA-250 (2020);
  J. A. Smolin, G. Smith and A. Vargo, "Oversimplifying quantum factoring", Nature 2013; E. Tang, "A quantum-inspired
  classical algorithm for recommendation systems", 2018 (STOC 2019).
