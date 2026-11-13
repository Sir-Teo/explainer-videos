"""Act V, Limits and Secrets: undecidability, complexity, proofs, codes, ciphers, public keys (Parts 25-30)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=25, level="U", widget="pcpoverhang", prereq=(1, 2, 12),
        question="Which questions about programs, tiles and equations can no algorithm ever settle?",
        story="The part opens with three questions: whether eleven Wang tiles cover the plane, whether "
              "x^2 - 61 y^2 = 1 has a solution, and whether a program can print its own source. It separates "
              "deciding from recognizing, and uses mapping reductions to carry Part 1's halting problem to "
              "acceptance, emptiness and equivalence. Rice's theorem then makes every nontrivial extensional "
              "property of programs undecidable, and Kleene's recursion theorem builds programs that hold their own "
              "description: a Pebble quine of 13,380 bytes runs on the emulator. The same impossibility is found in "
              "Post's dominoes, where one four-domino set has a shortest match of 206, in Wang tilings and the hat, "
              "and in Hilbert's tenth problem, where every recognizable set is Diophantine. The part turns from "
              "computation to proof and information: Godel's theorem follows from halting, plain complexity C is "
              "uncomputable by Berry's paradox, and Chaitin's Omega packs halting into one real number. It ends at "
              "the busy beaver, which outgrows every computable function, and at the map of where decidability "
              "stops: Presburger arithmetic on one side, PRIMEGAME and matrix mortality on the other.",
        handoff="The diagonal returns as the time hierarchy theorem in Part 26, which asks how fast instead of "
                "whether. Part 54 checks proofs and specifications by restriction and incomplete search, Part 55 "
                "proves safety in access control undecidable and builds Thompson's trojan compiler on a quine, "
                "Part 57 turns Kolmogorov's idea into Occam's razor for learning, and Part 58 makes recursion a "
                "fixed point.",
        outside="Comfort with proofs by contradiction and with reading a program; nothing beyond the earlier parts.",
        objectives={
            "U": ["Tell a decider from a recognizer, and place K, its complement and TOT in the picture of "
                  "recognizable and co-recognizable sets.",
                  "Prove a problem undecidable by a mapping reduction from halting or acceptance.",
                  "State Rice's theorem and say which questions about a program it covers and which it does not."],
            "M": ["Prove Rice's theorem, and write a quine by the head, data and tail construction.",
                  "Build the modified PCP dominoes of a Turing machine and read an accepting history off a match.",
                  "Prove that fewer than a 2^-c fraction of n-bit strings have C below n - c, and that C is "
                  "uncomputable."],
            "D": ["Classify FIN and TOT in the arithmetic hierarchy and state what the Friedberg-Muchnik theorem "
                  "settles.",
                  "Explain why the first n bits of Omega decide halting for programs of at most n bits, and why no "
                  "sound effective theory proves more than finitely many values of S.",
                  "State Hilbert's tenth problem over rings of integers and over the rationals, and which is open."],
            "I": ["Explain why a static analyzer or a virus scanner must miss cases or raise false alarms, and how "
                  "restricting the language buys decidability.",
                  "Report a bounded search honestly: matched, exhausted, or cut off with no verdict."],
        },
        results=[
            ("Decidable", r"L\text{ decidable}\iff L\text{ and }\overline{L}\text{ are both recognizable}"),
            ("Mapping reduction", r"A\le_m B:\ \ w\in A\iff f(w)\in B,\quad f\text{ computable}"),
            ("Rice's theorem", r"\{\langle M\rangle:\ \varphi_M\in P\}\text{ is undecidable for nontrivial }P"),
            ("Recursion theorem", r"\forall f\text{ total computable}\ \ \exists e:\ \ \varphi_e=\varphi_{f(e)}"),
            ("Incompressible strings", r"\#\{x\in\{0,1\}^n:\ C(x)<n-c\}<2^{\,n-c}"),
            ("Busy beaver", r"S(n)>f(n)\ \text{ for all large }n,\ \text{ for every total computable }f"),
        ],
        U=(0, 1, 2, 3, 6), D=(9, 11, 15), I=(14,),
        also=(("The computability instrument", "explainer/cs/algo/computability.py"),),
    ),
    Part(
        n=26, level="U", widget="satthreshold", prereq=(1, 16, 25),
        question="Is finding a solution ever fundamentally harder than checking one?",
        story="In March 1956 Godel wrote to the dying von Neumann asking how fast the best machine could find a "
              "proof of length n. The part makes the question precise: polynomial time as the definition of "
              "efficient, the time hierarchy theorem and Savitch's theorem to separate and relate classes, and NP as "
              "the problems whose answers can be checked. Cook-Levin is built rather than quoted: a small "
              "nondeterministic machine becomes a tableau of 2 by 3 windows, a formula of 3,416 to 23,324 variables, "
              "and the series' clause-learning solver decodes an accepting run from a model. One five-clause formula "
              "is then carried through independent set, clique, vertex cover, 3-colouring and subset sum, with each "
              "solution mapped back. The part widens to coNP and Pratt certificates, to PSPACE and games, and to "
              "Williams's 2025 simulation of time t in about the square root of t space. It turns on why the "
              "question resists proof: relativization, natural proofs and algebrization each rule out a family of "
              "techniques. It ends with Impagliazzo's five worlds and what P = NP would and would not give.",
        handoff="Part 27 adds randomness and interaction to proofs and reaches the PCP theorem. Part 29 builds "
                "cryptography on one-way functions and Part 30 on factoring and discrete logarithms, the suspects "
                "between P and NP-complete. Part 41 resolves package dependencies with a SAT solver, Part 53 tests "
                "the extended Church-Turing thesis against quantum computers, and Part 54 sends verification "
                "conditions to a solver.",
        outside="Big-O notation and graphs from Act IV; propositional logic (and, or, not, CNF).",
        objectives={
            "U": ["Define P and NP with a verifier and a certificate, and show that a given problem is in NP.",
                  "Explain what a polynomial reduction is and what NP-complete means.",
                  "Reduce 3-SAT to independent set and map a satisfying assignment to an independent set and back."],
            "M": ["Prove the time hierarchy theorem by diagonalization and Savitch's theorem by midpoint recursion.",
                  "Prove Cook-Levin by the tableau and count the variables and clauses of the formula.",
                  "Tell weak from strong NP-hardness, and say when a pseudo-polynomial algorithm or an FPTAS exists."],
            "D": ["State the relativization, natural-proofs and algebrization barriers and what each rules out.",
                  "State Williams's time-space simulation and Ladner's theorem, and name the open separations "
                  "around them.",
                  "Explain what the minimum circuit size problem asks and why meta-complexity ties it to "
                  "cryptography."],
            "I": ["Recognize scheduling, packing and dependency resolution as NP-hard models, and choose between a "
                  "SAT or ILP solver, an approximation and a heuristic.",
                  "Encode a puzzle or a configuration problem as CNF, run a CDCL solver, and report UNKNOWN "
                  "separately from UNSAT."],
        },
        results=[
            ("Time hierarchy", r"f\log f=o(g)\ \Longrightarrow\ \mathrm{DTIME}(f)\subsetneq\mathrm{DTIME}(g)"),
            ("Savitch", r"\mathrm{NSPACE}(s)\subseteq\mathrm{SPACE}(s^2),\qquad s\ge\log n"),
            ("NP by certificates", r"x\in L\iff\exists c,\ |c|\le p(|x|):\ V(x,c)=1,\quad V\text{ in P}"),
            ("Cook-Levin", r"\mathrm{SAT}\in\mathrm{NP},\qquad A\le_p\mathrm{SAT}\ \text{ for every }A\in\mathrm{NP}"),
            ("The known chain", r"\mathrm{P}\subseteq\mathrm{NP}\subseteq\mathrm{PSPACE}\subseteq\mathrm{EXP},"
                                r"\qquad\mathrm{P}\ne\mathrm{EXP}"),
            ("Williams 2025", r"\mathrm{TIME}(t)\subseteq\mathrm{SPACE}\bigl(\sqrt{t\log t}\bigr),\qquad t\ge n"),
        ],
        U=(0, 1, 3, 4, 6, 15), D=(11, 14, 16), I=(7, 13),
        also=(("The complexity instrument", "explainer/cs/algo/complexity.py"),),
    ),
    Part(
        n=27, level="U", widget="sumcheckcheat", prereq=(20, 25, 26),
        question="How can a verifier be convinced by a proof it never reads in full?",
        story="The part opens with three ways a proof can be more than a document read from start to end: sampled, "
              "interactive, and zero-knowledge. It first sorts the randomized classes RP, ZPP and BPP, amplifies a "
              "one-third error by majority vote, and shows by Adleman's union bound that one coin string works for "
              "every input of a length. Circuit lower bounds and communication complexity supply the tools: random "
              "restrictions collapse a DNF, and a fingerprint decides equality of n bits with two field elements. "
              "Then proofs become conversations. A prover shows that two graphs are not isomorphic by answering random "
              "challenges, and "
              "sum-check over the field of 97 elements verifies that a formula has seven satisfying assignments, "
              "one variable a round; Shamir's extension gives IP = PSPACE. A three-colouring is proved in zero "
              "knowledge with salted-hash commitments, where a colouring with two bad edges among fifteen survives "
              "k rounds with probability (13/15)^k. The part turns on the PCP theorem: a constant number of queried "
              "bits suffices, and that is why MAX-E3SAT cannot be approximated beyond 7/8. It ends with the Unique "
              "Games Conjecture, fine-grained, parameterized and counting complexity, and MIP* = RE.",
        handoff="Part 28 develops error-correcting codes and local testing, Part 29 pseudorandom generators and "
                "one-way functions, and Part 30 identification, signatures, lattices and succinct arguments. Part "
                "53 studies the entanglement behind MIP*, Part 56 returns to expanders, and Part 57 connects "
                "learning hardness with computational assumptions.",
        outside="Discrete probability (independence, the union bound), arithmetic modulo a prime, and polynomials "
                "over a field.",
        objectives={
            "U": ["Define RP, ZPP and BPP, and compute how many independent runs push a one-third error below a "
                  "target.",
                  "Explain the graph non-isomorphism protocol and why a cheating prover is caught in half the rounds.",
                  "Explain with Ali Baba's cave what zero knowledge means and what a simulator is."],
            "M": ["Run sum-check by hand on a small formula over a prime field and bound a cheating prover's "
                  "success by nd / p.",
                  "Prove BPP is in P/poly, and prove that deterministic equality needs n bits by fooling sets.",
                  "State the PCP theorem with its completeness and soundness, and derive the 7/8 guarantee of a "
                  "random assignment for MAX-E3SAT."],
            "D": ["State the Nisan-Wigderson and Impagliazzo-Wigderson implications from circuit lower bounds to "
                  "derandomization.",
                  "State the Unique Games Conjecture and what it would make optimal for vertex cover and MAX-CUT.",
                  "State MIP* = RE with its quantifiers, and what it settles about Tsirelson's problem."],
            "I": ["Use a conditional lower bound from SETH or 3SUM to decide when to stop looking for a faster "
                  "algorithm.",
                  "Solve vertex cover for small k by a bounded search tree and Buss's kernel.",
                  "Name the assumptions, setup and proof size behind a succinct argument before relying on it."],
        },
        results=[
            ("Amplification", r"\Pr[\text{majority of }k\text{ runs errs}]\le e^{-k/18}\quad(\text{error }\tfrac13)"),
            ("Adleman", r"\mathrm{BPP}\subseteq\mathrm{P/poly}"),
            ("Equality by fingerprint", r"x\ne y\ \Longrightarrow\ \Pr_r\bigl[x(r)=y(r)\bigr]\le\frac{n-1}{q}"),
            ("Sum-check soundness", r"\Pr[\text{false claim accepted}]\le 1-\bigl(1-\tfrac dp\bigr)^{n}\le\frac{nd}{p}"),
            ("Proof systems", r"\mathrm{IP}=\mathrm{PSPACE},\quad\mathrm{NP}=\mathrm{PCP}(\log n,1),\quad"
                              r"\mathrm{MIP}^*=\mathrm{RE}"),
            ("MAX-E3SAT", r"\mathbb{E}[\text{clauses satisfied by a random assignment}]=\tfrac78\,m"),
        ],
        U=(0, 1, 5, 7), D=(2, 10, 15), I=(11, 12),
        also=(("The proofs instrument", "explainer/cs/algo/proofs.py"),),
    ),
    Part(
        n=28, level="U", widget="noisypicture", prereq=(2, 5, 19),
        question="How can a message survive a channel that flips its bits?",
        story="In 1947 Hamming's weekend jobs on a Bell Labs relay computer died whenever its two-out-of-five code "
              "detected a bad bit, and he asked why the machine could not locate the error and fix it. The part "
              "starts from the binary symmetric channel and the repetition code, which buys reliability only by "
              "giving up rate, and from Hamming distance, which says what a code can detect and correct. "
              "Hamming(7,4) is built from its parity checks, whose syndrome names the flipped bit, and shown to be "
              "perfect; the bounds of the rate-distance plane say how good any code can be. Finite fields give "
              "Reed-Solomon codes, polynomials evaluated at many points, and the series' QR code is scratched across "
              "56 modules, which corrupts 8 of its 44 bytes, and still reads. The part turns on Shannon's theorem "
              "of 1948: below the capacity 1 - H(p) the error can be made as small as you like, which random codes "
              "decoded by table begin to show, at a decoding cost nobody can pay. Viterbi's trellis, LDPC codes "
              "under belief propagation and polar codes are the fifty years of work that made the limit reachable. "
              "It ends with codes for storage and the open questions of capacity and locality.",
        handoff="Part 29 builds AES, whose S-box is inversion in the field of bytes, and Part 30's secret sharing "
                "is a Reed-Solomon code. Part 34 puts RAID and checksums into file systems, Part 36 a CRC on every "
                "Ethernet frame, Part 45 computes how long erasure-coded storage survives, and Part 53 needs codes "
                "to make quantum computers work.",
        outside="Binary arithmetic and XOR, polynomials, and the binomial distribution.",
        objectives={
            "U": ["Compute the Hamming distance of a code and say how many errors it detects and corrects.",
                  "Encode four bits with Hamming(7,4), flip one bit, and locate it from the syndrome.",
                  "Compute the error rate and the rate of an n-fold repetition code on a binary symmetric channel."],
            "M": ["Prove the Hamming and Singleton bounds, and show that Reed-Solomon codes meet the Singleton bound "
                  "by counting roots.",
                  "Multiply in GF(256) with log tables, and recover erased Reed-Solomon symbols by Lagrange "
                  "interpolation.",
                  "State Shannon's theorem for the binary symmetric channel and outline the random-coding argument."],
            "D": ["State what it means for Reed-Muller codes to achieve capacity and what list decoding buys beyond "
                  "half the distance.",
                  "Analyse the two-query local decoder of the Hadamard code against 1 - 2 delta, and state the open "
                  "length trade-off for three queries."],
            "I": ["Choose an error level for a QR code, and explain why erasures cost half of what errors cost.",
                  "Say which damage a CRC of r bits is guaranteed to catch and why it is not a cryptographic hash.",
                  "Compare replication, Reed-Solomon RS(10,4) and a locally repairable code for storage overhead "
                  "and repair cost."],
        },
        results=[
            ("Distance", r"d\ \text{detects}\ d-1\ \text{errors and corrects}\ \bigl\lfloor\tfrac{d-1}{2}\bigr\rfloor"),
            ("Hamming bound", r"2^k\sum_{i=0}^{t}\binom ni\le 2^n,\qquad\text{Hamming}(7,4):\ 16\cdot 8=128"),
            ("Singleton, and Reed-Solomon", r"k+d\le n+1,\qquad d_{\mathrm{RS}}=n-k+1"),
            ("Errors and erasures", r"\text{RS corrects } e \text{ errors and } f \text{ erasures if } 2e+f\le n-k"),
            ("Shannon, for the BSC", r"C=1-H(p),\qquad H(p)=-p\log_2p-(1-p)\log_2(1-p)"),
            ("CRC bursts", r"\deg g=r,\ g(0)\ne 0\ \Longrightarrow\ \text{every burst of length}\le r\text{ is caught}"),
        ],
        U=(0, 1, 2, 3), D=(14,), I=(7, 8, 13),
        also=(("The codes instrument", "explainer/cs/algo/codes.py"),),
    ),
    Part(
        n=29, level="U", widget="aesavalanche", prereq=(26, 27, 28),
        question="What makes a cipher secure, and what does that security rest on?",
        story="The part opens with the series' logo encrypted by AES block by block: only 85 distinct blocks appear "
              "among 768 and the logo is still visible, though nothing is wrong with AES. It then follows two "
              "thousand years in which ciphers fell to counting: a substitution cipher on 600 letters of Moby-Dick "
              "is broken by hill climbing on quadgram scores, Vigenere by the index of coincidence, and Enigma by "
              "Rejewski's observation that cycle type survives the plugboard. Shannon's theorem of 1949 ends that "
              "contest and sets the price: perfect secrecy needs as many keys as messages. The part turns there. "
              "Modern cryptography limits the attacker to polynomial time, defines security as a game with "
              "negligible advantage, and proves schemes by reduction to pseudorandom generators, functions and "
              "permutations. AES is built from inversion in the field of bytes and matches FIPS-197, and one "
              "flipped bit spreads to half the state in two rounds. The rest is how it breaks in use: ECB, a "
              "padding oracle that recovers a message in 6,412 queries, malleable counter mode, length extension, "
              "a differential attack on a toy cipher, timing leaks and a key seeded from a process ID.",
        handoff="Part 30 adds public keys, and two Pebbles run a TLS 1.3 handshake with this part's authenticated "
                "encryption and HMAC. Merkle trees return in the file systems of Part 34, the blockchains of Part "
                "38 and the git objects of Part 41, and Part 55 returns to passwords, one-time codes built from "
                "HMAC, and passkeys.",
        outside="Modular arithmetic, XOR, and elementary probability; the finite field of bytes from Part 28.",
        objectives={
            "U": ["Break a Caesar or Vigenere cipher by frequency counts and the index of coincidence.",
                  "State Shannon's perfect secrecy, and prove that it needs at least as many keys as messages.",
                  "Explain why reusing a one-time pad or encrypting block by block leaks the message."],
            "M": ["Define IND-CPA security as a game, and explain why a secure cipher must be randomized.",
                  "Build a pseudorandom function from a generator by the GGM tree, and a permutation from a function "
                  "by Feistel rounds.",
                  "Trace one AES round on a state, and compute the birthday cost of a collision on an n-bit hash."],
            "D": ["State what is known about basing one-way functions on the hardness of Kolmogorov complexity "
                  "(Liu-Pass).",
                  "Explain what Grover's and Simon's algorithms do to symmetric keys and to modes, and state the "
                  "known bounds for key-alternating ciphers."],
            "I": ["Choose a mode and a MAC: authenticated encryption, verified before decrypting, with a nonce "
                  "that never repeats under a key.",
                  "Store passwords with a salted, slow, memory-hard hash, and compare tags with a fixed-work "
                  "comparison.",
                  "Recognize a padding oracle, a length-extension forgery and a weak seed in a code review."],
        },
        results=[
            ("Index of coincidence", r"\mathrm{IC}=\frac{\sum_i n_i(n_i-1)}{N(N-1)}:\ \ \text{English }0.062,\ "
                                     r"\text{random }0.038"),
            ("Perfect secrecy", r"\Pr[M=m\mid C=c]=\Pr[M=m]\ \Longrightarrow\ |\mathcal K|\ge|\mathcal M|"),
            ("IND-CPA", r"\bigl|\Pr[\mathcal A\text{ guesses }b]-\tfrac12\bigr|\le\operatorname{negl}(n)"
                        r"\ \text{ for every efficient }\mathcal A"),
            ("Switching lemma", r"\bigl|\mathrm{Adv}^{\mathrm{PRP}}-\mathrm{Adv}^{\mathrm{PRF}}\bigr|\le"
                                r"\frac{q^2}{2^{\,n+1}}"),
            ("Birthday collisions", r"\mathbb{E}[\text{hashes until a collision}]\approx\sqrt{\pi/2}\;2^{\,n/2}"),
            ("Meet in the middle", r"\text{double encryption costs about }2^{\,k+1}\text{ cipher calls, not }2^{2k}"),
        ],
        U=(0, 1, 2, 3, 4), D=(16,), I=(10, 13, 15),
        also=(("The cryptography instrument", "explainer/cs/algo/crypto.py"),),
    ),
    Part(
        n=30, level="U", widget="curvemultiples", prereq=(2, 20, 29),
        question="How can two strangers agree on a secret while everyone listens?",
        story="Alice and Bob agree in public on the prime 23 and the number 5, send 8 and 19, and both arrive at "
              "the secret 2, which was never said: Diffie and Hellman's exchange of 1976. The part builds what makes "
              "it work. Merkle's puzzles give a first, quadratic gap between the parties and the eavesdropper; "
              "extended Euclid, square-and-multiply and the cyclic group of units give the toolkit; RSA is generated "
              "at 2048 bits from the series' own Miller-Rabin and proved correct by Euler and the CRT. The attacks "
              "set the key sizes: Bleichenbacher's padding oracle reads a message under a 256-bit key in 33,392 queries, "
              "Pollard's "
              "rho and a quadratic sieve factor, and baby-step giant-step, Pohlig-Hellman and index calculus take "
              "discrete logarithms. Elliptic curves escape index calculus, so 256 bits suffice, and one repeated "
              "ECDSA nonce gives away the private key. Certificates bind keys to names, and two of the series' "
              "machines run a TLS 1.3 handshake in which every check passes. The part turns on Shor's algorithm, "
              "which breaks all of it on a quantum computer. It ends with the lattices that answer it (LLL, LWE, "
              "ML-KEM's arithmetic) and with cryptography that proves and computes on secrets.",
        handoff="Part 37's QUIC carries TLS 1.3 inside the transport, Part 38 uses signatures to reach agreement "
                "when some machines lie, Part 41 signs software releases and Part 43 puts mutual TLS between "
                "services. Part 53 runs Shor's algorithm on the series' quantum simulator, and Part 55 returns to "
                "authentication with passkeys.",
        outside="Modular arithmetic and the idea of a group; the symmetric tools of Part 29.",
        objectives={
            "U": ["Carry out a Diffie-Hellman exchange by hand with a small prime, and explain what the "
                  "eavesdropper would have to compute.",
                  "Compute a modular inverse by extended Euclid and a modular power by square-and-multiply.",
                  "Generate a small RSA key, encrypt and decrypt with it, and explain why decryption inverts "
                  "encryption."],
            "M": ["Prove RSA correct by Euler's theorem and the CRT, and explain why textbook RSA needs OAEP.",
                  "Compute a discrete logarithm by baby-step giant-step, and explain why Pohlig-Hellman forces "
                  "groups of large prime order.",
                  "Add and double points on an elliptic curve over a prime field, and recover an ECDSA key from "
                  "two signatures that share a nonce."],
            "D": ["State the LWE problem and what its worst-case to average-case reduction claims, and what is "
                  "not known about the quantum hardness of lattice problems.",
                  "Explain what the breaks of Rainbow and SIKE show about the evidence behind post-quantum "
                  "schemes."],
            "I": ["Read a TLS 1.3 handshake: key share, certificate chain, CertificateVerify, Finished, and where "
                  "forward secrecy comes from.",
                  "Recognize a padding oracle, nonce reuse and an unauthenticated key exchange as protocol "
                  "failures, not failures of the mathematics.",
                  "Plan a migration to hybrid and post-quantum key exchange against harvest now, decrypt later."],
        },
        results=[
            ("Diffie-Hellman", r"(g^a)^b\equiv(g^b)^a\equiv g^{ab}\pmod p"),
            ("RSA", r"ed\equiv 1\!\!\pmod{\varphi(n)}\ \Longrightarrow\ (m^e)^d\equiv m\pmod n"),
            ("Generic attacks", r"\text{discrete log, order }n:\ O(\sqrt n);\quad"
                                r"\text{rho, factor }p:\ \approx\sqrt p\text{ steps}"),
            ("The group law", r"\lambda=\frac{y_2-y_1}{x_2-x_1}\ \text{or}\ \frac{3x_1^2+a}{2y_1},\quad "
                              r"x_3=\lambda^2-x_1-x_2,\quad y_3=\lambda(x_1-x_3)-y_1"),
            ("ECDSA with a repeated nonce", r"k=\frac{z_1-z_2}{s_1-s_2},\qquad d=\frac{s_1k-z_1}{r}\pmod n"),
            ("Shamir sharing", r"f(0)=s,\ \deg f=k-1:\ \text{any }k\text{ shares give }s,\ "
                               r"k-1\text{ give nothing}"),
        ],
        U=(0, 1, 2, 3, 4, 5), D=(16,), I=(6, 11, 12),
        also=(("The public-key instrument", "explainer/cs/algo/pubkey.py"),),
    ),
]
