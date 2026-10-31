# Part 1 tail: source and cached-measurement review

Reviewed 2026-10-31 against checkout head `ca4d22b3a87a153fa5295dadf2679bd48489fd2f` (line references below refer to source read during this review).

Scope: Counting (`s10`), Shannon1951 (`s11`), Likelihood (`s12`), Information's definition/data-processing sections (`s13`; memory reviewed separately), Knowledge (`s14`), Units (`s15`), Scoreboard (`s16`), Outro (`s17`), README exercises/answers, and their supporting arithmetic/counting/LM cache calculations. Also inspected the arithmetic section (`s09`) because the later round-trip and compression claims depend on it.

This pass made no repository source edits, ran no scene renders or experiment/model computations, and used only existing cached measurements for numeric evidence. Analytical cross-checks and primary-source browsing are distinguished below. It does not add playback/listening coverage.

## Verified corrections to batch

### 1. Current/historical Hutter record and units are mixed (Scoreboard)

- `videos/ai/ai1/s16_scoreboard.py:221` cites a record of 24 July 2026, but `:241` labels the September 2024 figure 110.8 MB, and `:251` calls that figure "the record." The README `:86` already reports the July 2026 record, so scene and notes disagree.
- The official [Hutter Prize records table](https://www.hutter1.net/prize/index.htm), read 2026-10-31, lists **Vladimir Ivanov, 24 Jul 2026, fx2-cmix-T, total 100,424,672 bytes**. It separately lists **Kaido Orav and Byron Knoll, 3 Sep 2024, fx2-cmix, total 110,793,128 bytes**. The task defines the scored total as compressor size S1 plus self-extracting archive size S2, not archive alone.
- The historical figure is valid if explicitly described as **the September 2024 record**; do not merely relabel 110.8 MB as July 2026. Alternatively use the actual July 2026 total and date consistently. As of this review the official table's current winning total is 100,424,672 bytes; smaller pending/benchmark entries are not interchangeable with the official awarded record.
- Dividing total bits by the 10^9-byte input gives **0.803397376 bits per input byte** for the July 2026 total, or **0.886345024 bits per input byte** for the September 2024 total. `:242`, `:252` and README `:87` say bits per character. The course elsewhere explicitly distinguishes Unicode characters from UTF-8 bytes, so use **bits per byte** here unless separately computing decoded-character counts.
- Chinese narration at `zh_lines.py:514` still repeats the 2024-as-current figure. Update relevant on-screen translations and any captured narration entries with the chosen historical/current wording.

### 2. Study inventory is 31 models; not every specialized model was scored on every benchmark (Units)

- `s15_units.py:162` and `:183` say 30 public models; `zh_lines.py:483` says 30. README `:79` already says 31.
- The primary [Huang et al. paper](https://arxiv.org/html/2404.09937), v2, 19 Aug 2024, abstract and introduction, states **31 public LLMs and 12 benchmarks**. Its §4 general setup specifies that general-purpose models are evaluated across all benchmarks, coding models only on coding, and math models only on math. Table 2 contains 19 general-purpose, 9 code, and 3 math models.
- The **overall Pearson coefficient −0.93** is supported by §4.1. Keep it, while avoiding a new claim that each of all 31 models received one average across all 12 benchmarks. Suggested factual structure: the study covered 31 models across 12 benchmarks; its overall comparison showed −0.93.
- The schematic scatter is correctly labeled schematic (`:179`); it should remain a schematic rather than being presented as the paper's actual point coordinates.

### 3. Rounded byte size and bitstream overhead are inconsistent in one sentence (Scoreboard)

- `s16_scoreboard.py:133` sets `nb = ceil(z['bits']/8)`; `:172` then says the `nb` bytes are `z['bits']-z['ideal']` bits over the ideal.
- Cached `lmzip`: payload **5,502 bits**, ideal **5,499.258367603147 bits**, `ok=True`, **4,331 characters / 4,335 UTF-8 bytes / 1,023 tokens**, xz **2,180 bytes**.
- Thus the payload overhead is **2.741632396853 bits**, but packing it into **688 bytes = 5,504 bits** gives **4.741632396853 bits** including two padding bits. The current narration's "688 bytes, 2.7 bits more" mixes these measures.
- Either explicitly state the 5,502-bit payload and separately its 688-byte packing, or compute the packed-byte overhead. The xz-to-688-byte comparison itself is numerically consistent (about 3.17×).
- The demo's decoder knows the output-token count from `len(ids)` (`compute.py:1430`); this is a fixed-length payload demonstration, not a complete self-framing file format. State a known-length/payload convention if describing a standalone compressor file. Do not silently add unmeasured framing overhead to the reported payload.

### 4. Outro KL thumbnail visibly flattens the actual reverse-KL Gaussian

- `s17_outro.py:62` caps the density chart at `max(p)*1.15`; `:69` and `:71` use `np.minimum` to flatten Gaussian values above that cap.
- Cached `kl` gives target-based cap **0.4376090297567172**, but the reverse fit's sampled peak is **0.6040907235131223**. **27 plotted samples** are clipped. This is a demonstrated current-data distortion, unlike the former main-section 0.7 cap, which did not clip the actual current fit.
- Give the thumbnail a scale containing both fitted peaks, then plot the unmodified densities. This also makes the recap consistent with the enhanced main KL comparison.

### 5. Huffman exercise answer gives an incorrect tie/merge explanation

- README `:153–155` and Chinese `:194–196` describe which tie decision produces the two length vectors. Both listed vectors `(2,2,2,3,3)` and `(1,2,3,4,4)` are valid optimal codes with average 2.2 bits; the entropy 2.121928... and gap about 0.07807 bits are correct. The mistake is the stated merge history.
- Let symbols a,b,c,d,e have probabilities .4,.2,.2,.1,.1. One valid explicit history for `(2,2,2,3,3)` is: merge d+e→.2, b+c→.4, a+(de)→.6, then combine .4+.6.
- A valid history for `(1,2,3,4,4)` is: d+e→.2, c+(de)→.4, b+(cde)→.6, then a+(bcde)→1.
- The text's claim that merging the two old .2's produces `(1,2,3,4,4)` is impossible: b and c then become siblings and must have equal lengths, whereas that vector assigns them lengths 2 and 3.
- Correct the merge description in both languages; do not discard the two valid final vectors.

### 6. Shannon comparison labels a different model as the guesser's own probabilities

- `s11_shannon.py:111` labels `orders.best_bits` as "its own probabilities, coded directly."
- The displayed rank experiment is the **six-context lexicographic backoff guesser** (`compute.py:643–659`, `:680`), using orders 0..6 to break ties. `orders.best_bits` is the **smoothed order-5 counting model**, currently **2.018353275820524 bits per letter**. The rank experiment also uses the first 11,994 scored passage letters, whereas the order score uses the broader test sample.
- `game.sentence_bits` does not supply the missing six-context probability measurement: it is the order-5 smoothed model on the separate 101-character Shannon sentence, totaling **182.22018791588192 bits**, mean **1.8041602763948705 bits per character**. Do not substitute that mean for the Falcon histogram comparison.
- The numerical comparison is useful but it is not the same model/probability experiment. Label it as a comparison with the best smoothed counting model, or actually measure the same guesser's explicitly defined probabilistic model. The rank entropy 2.365853... and illustrative lower expression 1.359568... are already honestly qualified in narration; preserve those qualifications.

### 7. Full-passage compression size is an estimate, not a completed coder output

- `s16_scoreboard.py:200`, `:223`, `:245` call `compress.sizes['GPT-2 small']` the whole passage compressed by GPT-2 plus the coder.
- `compute.py:1576` actually calculates **`bpc * n_chars / 8 + 0.25`**, yielding **3,120.551644882207 bytes**: log-loss-derived size plus an assumed two termination bits. It does not run the full passage through the integer coder or quantify frequency quantization, byte padding, or framing.
- The real independently decoded run is only the first 1,023 tokens / 4,331 characters (`compute_lmzip`), and its `ok=True` is good evidence for that subset.
- Label the full-passage number as an **estimate from log loss** or **ideal coded size estimate**, keeping the real subset round trip clearly separate. The chosen 2 bytes per parameter / 248 MB for the weights is explicitly a convention and is supported by Delétang et al.'s two-part-code comparison; it is not a measured local model-file size.

### 8. "Best" context length is selected on the scored passage

- `compute_orders` `compute.py:445` minimizes test loss; `compute_raw` `:866` does the same. Alpha is chosen on validation in `fit_orders`, but context length is not.
- Current cache: alphabet-27 test-optimal context **5** (2.0183533 bits), validation-optimal context **6** (test 2.0579106). Raw-character test-optimal context **4** (2.3229342 bits), validation-optimal context **5** (test 2.3788986).
- This is legitimate exploratory teaching if labeled **best on this passage among the tested orders**. It is not an unbiased held-out selection of the winning model. The scoreboard's "best counting model" should disclose the selection rule. If changing selection to validation, propagate the changed data everywhere and regenerate; wording alone can preserve the current exploratory measurements honestly.

## Mathematical qualifications / design choices, not demonstrated current crashes

- `s09_arithmetic.py:363`, `:373–374`: `q=2^{-ell}` for **any** compressor needs a Kraft/normalization qualification. A valid incomplete prefix code with codewords `00` and `01` has lengths 2 and implied masses .25+.25=.5, not a normalized distribution. Treat it as code-implied weights/semimeasure or normalize appropriately; prefix-to-next-token consistency is an additional issue for an arbitrary file compressor. Delétang et al. uses a similar exposition, so this is a mathematical qualification to improve, not a discrepancy with that citation.
- `s12_likelihood.py:255`, `:296–298`: averaged gradient `q-p_hat` is correct for the shared-logit categorical toy distribution. For varying language-model contexts it is the average of `q_i-one_hot(y_i)`; it is not the full parameter gradient without the network Jacobian. The pointwise softmax derivative shown at `:243–247` is correct. Qualify the transition from the toy model to language models rather than labeling the toy formula wrong.
- `s13_information.py:52`, `:61–62`: `I_two` is the information in the **previous two letters jointly**, not the single letter at lag two. `compute_dpi` does compute the joint quantity correctly; the caption "two letters back" is ambiguous beside "the second one alone." Prefer "the previous two letters jointly."
- `s10_counting.py:356–357`: one-letter contexts are not all seen millions of times. The cached q count is 18,496, with qu count 18,469 (consistent with the earlier on-screen example). Say common contexts are abundant, or that some occur millions of times.
- `s14_knowledge.py:88–103`, `:214–218`: lower surprise demonstrates predictive associations and a with/without-context effect, but does not by itself prove the claimed particular training fact or that the earlier telephone-bell sentence specifically caused the change. "Consistent with learning/using..." would distinguish interpretation from measured probability. The actual cached comparisons support the direction of the story.
- README exercise 4 (`:162–166`, Chinese `:201–204`) uses leading-exponential AEP approximations at n=100 without an epsilon or finite-n error. The numbers 2^(nH) and 2^(-nH) are reasonable labeled leading-exponential approximations, but the finite-n typical set and its mass are not defined without a tolerance. Avoid implying an exact finite-n count or an established "nearly all" probability from those formulas alone.
- `s17_outro.py:185` leaves the problem set for six seconds after narration, with an explicit instruction to pause. That is a defensible interaction choice, but differs from the syllabus's about-90-second problem-set standard; decide explicitly whether the pause prompt satisfies the intended lecture standard.
- Further result-dependent aborts remain in `compute.py:874`, `:956–957`, `:1017`, plus `:448`. They currently pass the measured caches, but assert hoped-for empirical outcomes rather than invariants. Preserve independent mathematical/round-trip invariants and branch empirical verdicts as needed when future data/model versions change. This is reproducibility fragility, not an observed failure in the present completed cache.

## Checks that supported the current story

- Counting's alpha choice really uses held-out validation; add-alpha probabilities and Laplace's beta-integral derivation are correct. The q→u integer count shown is 18,469 and matches the existing cache after rounding.
- The current smoothing plot is not clipped by its `min` safeguard: highest test value is 3.533618... and the computed chart ceiling is 3.633618.... Do not claim current-data clipping there.
- Arithmetic's cached `the falcon` exact code length is 29 bits at information 27.6610395 bits; the 16-bit integer example emits 28 bits. The data-dependent "one fewer" branch is correct. The finite-frequency/register sweeps assert every encode/decode round trip before publishing results.
- Softmax normalization, the nats gradient `q-one_hot(y)`, and the maximum-likelihood/cross-entropy/KL decomposition are consistent. The illustrative counts sum to 100 and the probabilities have the intended .40/.25/.18/.12/.05 values.
- Cached units satisfy equal totals across per-token and per-character calculations. GPT-2 small: 5,458 tokens, 4.573545833 bits/token, 1.166140949 bits/character. Counting: 2.322934223 bits/character, same per-token value because its token is one character. The intended reversal in comparing per-token versus per-character scores is real.
- The raw passage is 21,406 Unicode characters and 21,432 UTF-8 bytes. The plain-text scoreboard baseline 8.0097169 bits/character is correct, and "about eight" in narration is appropriately rounded.
- Knowledge probes support the shown comparisons: Qwen3-4B Paris .3412458 vs GPT-2 small .0637773; Qwen Au .2168662, with GPT-2 Au absent from a top-eight list whose lowest listed probability is .0079111 (so the current `<.01` label is a valid bound in this case). Qwen's arithmetic four .2844576 versus five .2215358 agrees with the actual sentence.
- Cached Qwen telephone surprise is 12.9727091 bits for the paragraph alone and 3.4511686 with the preceding context. Treat causal knowledge attribution as interpretation, but the measured context improvement is real.
- README exercises 1, 2, 5, 6 have consistent algebra/results; exercise 3's final code lengths and averages are also correct apart from the merge explanation identified above.

## Source verification limits

Primary sources read directly: [official Hutter Prize page](https://www.hutter1.net/prize/index.htm), [Huang et al. full paper](https://arxiv.org/html/2404.09937), and [Delétang et al. full paper](https://arxiv.org/html/2309.10668). The latter supports the cited enwik9 8.3%, gzip32.3%, LZMA223.0%, adjusted14,008.3%, and the float16 parameter convention. Its image/audio result concerns the paper's specific ImageNet patches/LibriSpeech samples, not every image/audio corpus; the narration's short summary should retain that scope when expanded.

Cover–King's publication identity/year were checked against [Cover's Stanford publication list](https://www-isl.stanford.edu/~cover/info-theory.html); full-paper retrieval did not succeed in this pass, so the 1.3-bit numerical estimate was not independently reverified from the original PDF. The Laplace historical sunrise figure and Shannon's original human-study endpoint numbers were not independently re-read from their original full texts during this pass. Those remain source-verification coverage limits, not newly identified factual errors.
