# AI, Built — Part 1: The Guessing Game

Part 1 of a twenty-part series on the mathematics of modern AI models (see [the series plan](../README.md)). It
starts where Claude Shannon did, with a game: guess the next letter of an English text. A hook and eleven
chapters:

* **Shannon's guessing game.** Shannon's 1951 experiment, played on his own sentence by a counting program; GPT-2
  (2019) and Qwen3-4B (2025) playing the same game on the next token; the same game in images, sound and robotics
  (schematic); the twenty-part map; the scoreboard and its passage.
* **Probability and the chain rule.** Letter frequencies of 22.8 million symbols from thirty novels; a distribution
  as one unit of belief shared out; the 27 × 27 table of P(next | previous), P(u | q) = 0.9985; the chain rule,
  derived, and drawn as nested slivers ("he said" → *the*).
* **Surprise.** Shannon's requirements, and the derivation that they leave only log₂(1/p) (g(x + y) = g(x) + g(y),
  integers, fractions, continuity); bits as halvings; the surprise of Shannon's sentence, letter by letter: 182 bits
  for 101 symbols.
* **Entropy.** Entropy as an area (slivers of width p and height log₂ 1/p): 4.08 bits for letters against log₂ 27 =
  4.75; the coin; H ≤ log₂ K by Jensen; conditional entropy as a mosaic chart: 3.33 bits given the previous letter.
* **Codes.** Fixed-length codes; prefix-free codes as trees and decoding; Kraft's inequality as disjoint dyadic
  intervals; L ≥ H by Jensen and Kraft; Shannon's rounded code (4.62 bits); Huffman's algorithm built merge by
  merge on the 27 letters (4.127 bits, *the falcon* in 43 bits instead of 50); the source coding theorem.
* **Cross-entropy and KL.** Coding with the wrong model as an area; H(p, q) = H(p) + D_KL(p‖q); Gibbs' inequality
  from ln x ≤ x − 1 (and H(Y | X) ≤ H(Y)); cross-entropy as the training loss of every language model; forward vs
  reverse KL, fitted by gradient descent to a two-peaked density, with both loss landscapes.
* **Arithmetic coding.** Huffman's whole bits; the chain-rule slivers continued for *the falcon*, with the binary
  expansions of the interval's ends agreeing digit by digit; the 29-bit codeword (information content 27.66 bits);
  decoding; prediction ⇔ compression; the Hutter Prize and *Language Modeling Is Compression*.
* **Learning by counting.** Shannon's 1948 approximations, regenerated from the books; the counting rule; bits per
  letter against context length on the books (down to 0.27 at 14 letters) and on the Falcon passage (best 2.02 at
  5 letters, worse than letter frequencies at 14); unseen contexts and add-α smoothing; generalization.
* **Shannon's 1951 experiment.** The identical-twin argument (guess counts are a code); our counting guesser's guess
  counts on 11,994 letters (first guess 58%); Shannon's upper and lower bounds (2.37 and 1.36 bits); his subjects
  (0.6–1.3 bits with 100 letters of context); Cover and King's 1978 estimate.
* **Likelihood, softmax and the gradient.** Maximum likelihood = minimum cross-entropy = minimum divergence; counting
  is maximum likelihood; the softmax, step by step; ∂(−ln q_y)/∂z_k = q_k − [k = y], derived; gradient descent on
  five logits down to the entropy floor.
* **What it takes to guess well.** One paragraph's per-token surprise under GPT-2 and Qwen3-4B (Bull Durham tobacco;
  the telephone, 12.8 bits without the earlier paragraphs and 3.4 with them); knowledge probes; the mutual
  information between letters d apart, a power law out to 1,000 letters; the ladder of knowledge.
* **The scoreboard.** Bits per character on the passage as printed: plain text 8, uniform over its 61 symbols 5.93,
  letter frequencies 4.55, one character of context 3.58, gzip 3.31, xz 3.20, bzip2 2.92, the best counting model
  2.32, GPT-2 small 1.17, GPT-2 XL 1.01, Qwen3-0.6B 1.02, Qwen3-4B 0.87; people 0.6–1.3 (letters only).
* **Recap**, where each idea comes back, a computed teaser for Part 3 (GPT-2's word vectors; random directions in
  768 dimensions), and the references.

Every number the narration states is computed in [`compute.py`](compute.py) and asserted, in the scene that shows it
or where it is computed. Schematics are labeled `schematic`, made-up examples `illustrative`.

## Build it

```bash
python -m videos.ai.ai1.compute          # once: downloads 31 Gutenberg books (~40 MB) and GPT-2, GPT-2 XL,
                                          # Qwen3-0.6B/1.7B/4B-Base (~19 GB); ~15 min on 4 cores, cached in .cache/ai1
python tools/build.py ai1 -q l            # preview
python tools/build.py ai1                 # final 1080p30 + subtitles + chapters
python tools/narrate.py ai1 --lang zh && python tools/build.py ai1 --lang zh   # the Chinese master
```

## Sources

Books: T. M. Cover & J. A. Thomas, *Elements of Information Theory*, 2nd ed. (2006), ch. 2, 5, 13; D. J. C. MacKay,
*Information Theory, Inference, and Learning Algorithms* (2003), ch. 2, 4–6; C. M. Bishop & H. Bishop, *Deep
Learning: Foundations and Concepts* (2024), ch. 2.

Papers: C. E. Shannon, *A Mathematical Theory of Communication* (1948) and *Prediction and Entropy of Printed
English* (1951); L. G. Kraft (MIT thesis, 1949); D. A. Huffman, *A Method for the Construction of Minimum-Redundancy
Codes* (1952); S. Kullback & R. A. Leibler, *On Information and Sufficiency* (1951); R. A. Fisher, *On the
Mathematical Foundations of Theoretical Statistics* (1922); J. Rissanen, *Generalized Kraft Inequality and
Arithmetic Coding* (1976); R. Pasco (Stanford thesis, 1976); I. H. Witten, R. M. Neal & J. G. Cleary, *Arithmetic
Coding for Data Compression* (1987); T. M. Cover & R. C. King, *A Convergent Gambling Estimate of the Entropy of
English* (1978); H. W. Lin & M. Tegmark, *Critical Behavior in Physics and Probabilistic Formal Languages* (2017);
G. Delétang et al., *Language Modeling Is Compression* (ICLR 2024); A. Radford et al., *Language Models are
Unsupervised Multitask Learners* (2019); Qwen Team, *Qwen3 Technical Report* (2025).

Data: Project Gutenberg (thirty novels, listed in `compute.BOOKS`; *The Maltese Falcon*, eBook #77600, released
1 January 2026).
