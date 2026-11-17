# Psychology, Built: Part 23, Language

*Colorless green ideas sleep furiously* has never been said before, means nothing, and every English speaker knows
it is a sentence. This part asks what you know when you know a language, and how a mind gets it. B. F. Skinner said
language is behaviour learned by reinforcement; Noam Chomsky said no learner could get a grammar that way. Seventy
years later the argument is still going, and it now has numbers: the time it takes to read a word, the probability a
model gives that word, two minutes of a made-up language that infants learn from, a network that says *goed*, and
two-thirds of a million people taking a grammar quiz.

Productivity at every level, from sounds to sentences; Berko's wug; Zipf's law fitted on thirty novels, and the same
law from a monkey at a typewriter; frequency and length against reading time in the Natural Stories corpus; a spoken
word's cohort as it arrives; Reicher's word superiority effect and McClelland and Rumelhart's interactive activation
model, built with a fourteen-segment font and run; garden paths, Bever's horse and Frazier and Rayner's eye movements;
surprisal derived as a change of belief and a trigram model's blindness to syntax; surprisal fitted to the reading
times of ten thousand words, with the cost landing on the word after; Saffran, Aslin and Newport's stream and
transitional probabilities derived and run; the poverty of the stimulus, Gold's theorem and its answers, and fast
mapping; the past-tense debate, with a network that over-regularizes; critical periods, from Genie to Hartshorne,
Tenenbaum and Pinker's quiz; Broca, Wernicke, the language network and the N400 and P600; Whorf, Berlin and Kay,
Russian blues and Pirahã numbers. The practice chapter is readability formulas, the teaching of reading, aphasia
therapy and second languages; the frontier is what language models do and do not show about human learning.

## Where the numbers come from

| What | Source |
|---|---|
| 4,326,411 tokens and 59,639 word types in thirty novels; Zipf's exponent 1.20 (R² 0.994, top 10,000 types) | The reading of *AI, Built* Part 1 (thirty Project Gutenberg novels); Psyche (`language.zipf_fit`), item `zipf` |
| A monkey typing 2,000,000 characters (space with probability 0.18): exponent 1.20, R² 0.79 (a staircase) | Psyche (`language.random_typing`, after G. A. Miller 1957), item `zipf` |
| 10,256 words of ten stories, read by a median of 84 people each; mean reading times by frequency (369 ms for the rarest eighth to 327 ms for the commonest) and by length | Natural Stories (Futrell et al. 2021), `processed_wordinfo.tsv`, fetched by `explainer.psychology.opendata` and checked by SHA-256, item `lexicon` |
| The cohorts of *elephant*, *candle* and *trespass* as their letters arrive (for *trespass* 1,547, 346, 54, 4, 2) | Psyche (`language.cohort`, on the novels' 30,361 commonest words, letters standing in for sounds), item `lexicon` |
| Letter and word activations in the interactive activation model, and two-choice accuracy against display time; K after WORK 0.534 against K alone 0.418 at the mask | Psyche (`language.InteractiveActivation`, McClelland and Rumelhart's 1981 parameters, the novels' 1,500 commonest four-letter words), item `ia` |
| Surprisal word by word for three garden-path sentences; *fell* costs 13 bits in the reduced and the unreduced sentence alike | Psyche (`language.KneserNey`, an interpolated Kneser-Ney trigram, discount 0.75, 30,000 words), item `garden` |
| Mean surprisal 8.66 bits (perplexity 405) on Natural Stories; reading time 324 to 361 ms across tenths of surprisal; 1.18 ms per bit on the next word (s.e. 0.08), about 0 on the word itself, −6.3 ms per tenfold frequency, 2.8 ms per letter; R² 0.116 | Psyche (`language.KneserNey`, `rt_regression`), item `surprisal` |
| 24 eight-month-olds, two minutes of a stream of four three-syllable words | Saffran, Aslin and Newport (1996) |
| Transitional probabilities in a stream of Saffran-style words; segmentation by dips, perfect after 20 words; part-word scores 0.67 against 1 | Psyche (`language.syllable_stream`, `transitional_probabilities`, `segment`), item `stream` |
| A small effect in close replications, none reliable across all designs | Black and Bergmann (2017), the meta-analysis's abstract and results |
| 65 irregular and 125 regular verbs; the early irregulars right 0.94 before the vocabulary grows, 0.83 at the dip, 0.92 at the end; over-regularization peaking at 0.12 | Psyche (`language.past_tense_learner`, stems and endings as features, a softmax), item `pasttense` |
| Over-regularization in 4.2% of irregular past tenses across 25 children | Marcus et al. (1992) |
| 46 Chinese and Korean speakers, arriving at 3 to 39 | Johnson and Newport (1989) |
| 669,498 people; ability near its peak until about 17.4 | Hartshorne, Tenenbaum and Pinker (2018) |
| 891 effect sizes from 152 studies; a very small advantage before correcting for publication bias, none after | Lehtonen et al. (2018) |
| Flesch's reading ease, about 75 for Natural Stories 1 and 5 and chapter 2 of *The Maltese Falcon* | Psyche (`language.flesch`, a rough syllable count), item `readability` |
| About 61 hours of one child's head-camera video and speech, from 6 to 25 months | Vong, Wang, Orhan and Lake (2024) |

## Built in this part

* `explainer/psychology/psyche/language.py`: word statistics (Zipf's law fitted, Miller's typing monkey, cohorts,
  syllable counts and Flesch's formula); the interactive activation model, with a fourteen-segment font for its letter
  features and a forced-choice readout; Saffran-style syllable streams, transitional probabilities, segmentation by
  dips and word scores; a past-tense learner whose vocabulary grows in stages; tokenizing, an interpolated Kneser-Ney
  trigram model and its surprisal; and the reading-time regression with spillover. Tested in
  `tests/psychology/test_language.py`.
* `explainer/psychology/opendata.py` gains the Natural Stories corpus's per-word reading times, pinned to one commit
  and checked by SHA-256.
* The Ledger gains six rows; the Archive five datasets.
* The course's interactive is a made-up language: watch a stream of syllables, then pick its words out of pairs, and
  see how you did against chance and against Psyche's learner.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| A letter in a briefly shown, masked word is reported more accurately than the same letter shown alone | Reicher 1969 | replicated |
| Infants can find the words of a continuous syllable stream from the transitional probabilities between syllables alone | Saffran, Aslin and Newport 1996 | replicated, smaller |
| The time a reader spends on a word grows linearly with the word's surprisal | Smith and Levy 2013 | replicated |
| There is a sharp age after which a second language's grammar cannot be fully learned | Johnson and Newport 1989 | contested |
| Speakers discriminate colours faster across a boundary their language names than within it | Winawer and colleagues 2007 | contested |
| Speaking two languages improves executive control | Bialystok, Craik, Klein and Viswanathan 2004 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Skinner and Chomsky (the history
of a debate), Chomsky's sentence (an example, not a finding), Berko (a demonstration of productivity), Bever and
Frazier and Rayner (garden paths, measured in the surprisal row), Gold, Horning and Chater and Vitányi (theorems),
Carey and Bartlett and Hart and Risley (Part 54), Marcus et al. (a corpus count), Rumelhart and McClelland and Pinker
and Prince (a model and its critique), Curtiss and Mayberry, Lock and Kazmi (a single case and a study of first
languages), Broca and Wernicke (history), Fedorenko, Behr and Kanwisher and Kutas and Hillyard with Osterhout and
Holcomb (Part 49), Whorf and Berlin and Kay (history), Frank et al. (one field study), the National Reading Panel and
Breitenstein et al. (Part 54), Warstadt et al., Brown et al. and Vong et al. (Part 60), Oh and Schuler (the surprisal
row's background).

## Build it

```bash
python -m videos.psychology.psych23.compute            # every number (a few minutes; fetches Natural Stories once)
python tools/qa_scene.py psych23 Surprisal             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych23 -q l   # the whole part, silent preview
python tools/build.py psych23                          # 1080p30 with narration
python tools/qa_scene.py psych23 Segmentation --lang zh   # the Chinese edition of one chapter
python tools/make.py psych23                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 23                    # the lab: Zipf's law to surprisal and reading time
python tools/check_ledger.py psych23                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's language module, the Ledger, the Archive
```

The language model learns from the thirty novels of *AI, Built* Part 1; if `.cache/ai1/train.txt` is missing, the
compute builds it first (it downloads the novels from Project Gutenberg). The Natural Stories files carry no licence,
so they are fetched on first use and never committed.

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | Colorless green ideas | Skinner and Chomsky; a sentence never said; a test on you; the questions; objectives |
| 1 | Levels and productivity | Sounds, words, sentences and meaning; the wug test; Zipf's law in the novels and from a monkey |
| 2 | The mental lexicon | Frequency and length against reading time in Natural Stories; the cohort of a spoken word |
| 3 | Recognizing a word | Reicher's paradigm; the interactive activation model derived; letters helped by words, run |
| 4 | Sentences in real time | Garden paths; eye movements at the breaking word; a trigram model's surprisal, and what it cannot see |
| 5 | The cost of a surprising word | Surprisal derived as a change of belief; a story word by word; the fit to ten thousand words |
| 6 | Finding the words | Saffran, Aslin and Newport; transitional probabilities derived; segmentation run; the meta-analysis |
| 7 | How children learn a language | Milestones; the poverty of the stimulus, Gold's theorem and its answers; fast mapping and the input |
| 8 | Rules or associations? | The U-shaped curve; a network that says *goed*; Pinker and Prince; words and rules |
| 9 | A critical period? | Genie and late first languages; age of arrival; two-thirds of a million grammar quizzes |
| 10 | Language in the brain | Broca and Wernicke; the language network, localized in each person; the N400 and the P600 |
| 11 | Language and thought | Whorf; Berlin and Kay; Russian blues; Pirahã numbers; the bilingual advantage |
| 12 | The Ledger | Word superiority; statistical segmentation; surprisal; the critical period; colour words; bilingualism |
| 13 | In practice: speech, reading, aphasia | Readability formulas computed; the teaching of reading; aphasia therapy; second languages |
| 14 | Frontier: what language models show | Models' input against a child's; one child's video; better models fitting readers worse |
| | Recap, problems, and the road ahead | Ten lines; Kant's three objections; payoffs; problems; references; Part 24 |

## Sources

* B. F. Skinner, Verbal Behavior (1957); N. Chomsky, Syntactic Structures (1957) and review of Verbal Behavior,
  Language 35 (1959) 26-58; J. Berko, The child's learning of English morphology, Word 14 (1958) 150-177.
* G. K. Zipf, Human Behavior and the Principle of Least Effort (1949); G. A. Miller, Some effects of intermittent
  silence, American Journal of Psychology 70 (1957) 311-314.
* W. D. Marslen-Wilson and A. Welsh, Processing interactions and lexical access during word recognition in
  continuous speech, Cognitive Psychology 10 (1978) 29-63; W. D. Marslen-Wilson, Functional parallelism in spoken
  word-recognition, Cognition 25 (1987) 71-102.
* G. M. Reicher, Perceptual recognition as a function of meaningfulness of stimulus material, Journal of Experimental
  Psychology 81 (1969) 275-280; D. D. Wheeler, Cognitive Psychology 1 (1970) 59-85; J. Baron and I. Thurston,
  Cognitive Psychology 4 (1973) 207-228; J. L. McClelland and D. E. Rumelhart, An interactive activation model of
  context effects in letter perception: Part 1, Psychological Review 88 (1981) 375-407.
* T. G. Bever, The cognitive basis for linguistic structures, in Cognition and the Development of Language (1970);
  L. Frazier and K. Rayner, Making and correcting errors during sentence comprehension, Cognitive Psychology 14 (1982)
  178-210.
* J. Hale, A probabilistic Earley parser as a psycholinguistic model, Proceedings of NAACL (2001) 159-166; R. Levy,
  Expectation-based syntactic comprehension, Cognition 106 (2008) 1126-1177; N. J. Smith and R. Levy, The effect of
  word predictability on reading time is logarithmic, Cognition 128 (2013) 302-319; A. Goodkind and K. Bicknell,
  Proceedings of CMCL (2018) 10-18; R. Futrell et al., The Natural Stories corpus, Language Resources and Evaluation
  55 (2021) 63-77; R. Kneser and H. Ney, Improved backing-off for m-gram language modeling, ICASSP (1995) 181-184.
* J. R. Saffran, R. N. Aslin and E. L. Newport, Statistical learning by 8-month-old infants, Science 274 (1996)
  1926-1928; A. Black and C. Bergmann, Quantifying infants' statistical word segmentation: a meta-analysis,
  Proceedings of the 39th Annual Conference of the Cognitive Science Society (2017) 124-129.
* E. M. Gold, Language identification in the limit, Information and Control 10 (1967) 447-474; J. J. Horning, A
  study of grammatical inference (Stanford, 1969); N. Chater and P. Vitányi, 'Ideal learning' of natural language,
  Journal of Mathematical Psychology 51 (2007) 135-163; S. Carey and E. Bartlett, Acquiring a single new word, Papers
  and Reports on Child Language Development 15 (1978) 17-29; B. Hart and T. R. Risley, Meaningful Differences in the
  Everyday Experience of Young American Children (1995).
* D. E. Rumelhart and J. L. McClelland, On learning the past tenses of English verbs, in Parallel Distributed
  Processing, vol. 2 (1986); S. Pinker and A. Prince, On language and connectionism, Cognition 28 (1988) 73-193; G. F.
  Marcus et al., Overregularization in language acquisition, Monographs of the Society for Research in Child
  Development 57 (1992); S. Pinker, Words and Rules (1999); S. Prasada and S. Pinker, Language and Cognitive Processes
  8 (1993) 1-56; A. Albright and B. Hayes, Rules vs. analogy in English past tenses, Cognition 90 (2003) 119-161.
* S. Curtiss, Genie: A Psycholinguistic Study of a Modern-Day "Wild Child" (1977); R. I. Mayberry, E. Lock and H.
  Kazmi, Linguistic ability and early language exposure, Nature 417 (2002) 38; J. S. Johnson and E. L. Newport,
  Critical period effects in second language learning, Cognitive Psychology 21 (1989) 60-99; K. Hakuta, E. Bialystok
  and E. Wiley, Psychological Science 14 (2003) 31-38; J. K. Hartshorne, J. B. Tenenbaum and S. Pinker, A critical
  period for second language acquisition, Cognition 177 (2018) 263-277.
* P. Broca, Bulletin de la Société Anatomique 36 (1861) 330-357; C. Wernicke, Der aphasische Symptomencomplex (1874);
  E. Fedorenko, M. K. Behr and N. Kanwisher, Functional specificity for high-level linguistic processing in the human
  brain, PNAS 108 (2011) 16428-16433; M. Kutas and S. A. Hillyard, Reading senseless sentences, Science 207 (1980)
  203-205; L. Osterhout and P. J. Holcomb, Journal of Memory and Language 31 (1992) 785-806.
* B. L. Whorf, Language, Thought, and Reality (1956); B. Berlin and P. Kay, Basic Color Terms (1969); J. Winawer et
  al., Russian blues reveal effects of language on color discrimination, PNAS 104 (2007) 7780-7785; C. Witzel and K. R.
  Gegenfurtner, Journal of Vision 11 (2011) 16; J. Martinovic, G. V. Paramei and W. J. MacInnes, Cognition 201 (2020)
  104281; M. C. Frank, D. L. Everett, E. Fedorenko and E. Gibson, Number as a cognitive technology, Cognition 108
  (2008) 819-824.
* E. Bialystok, F. I. M. Craik, R. Klein and M. Viswanathan, Psychology and Aging 19 (2004) 290-303; K. R. Paap and
  Z. I. Greenberg, Cognitive Psychology 66 (2013) 232-258; M. Lehtonen et al., Is bilingualism associated with
  enhanced executive functioning in adults?, Psychological Bulletin 144 (2018) 394-425.
* R. Flesch, A new readability yardstick, Journal of Applied Psychology 32 (1948) 221-233; National Reading Panel,
  Teaching Children to Read (2000); C. Breitenstein et al., Intensive speech and language therapy in patients with
  chronic aphasia after stroke, The Lancet 389 (2017) 1528-1538.
* A. Warstadt et al., BLiMP: the benchmark of linguistic minimal pairs for English, TACL 8 (2020) 377-392; T. B.
  Brown et al., Language models are few-shot learners, NeurIPS (2020); W. K. Vong, W. Wang, A. E. Orhan and B. M. Lake,
  Grounded language acquisition through the eyes and ears of a single child, Science 383 (2024) 504-511; B.-D. Oh and
  W. Schuler, Why does surprisal from larger transformer-based language models provide a poorer fit to human reading
  times?, TACL 11 (2023) 336-350.
* Books: S. Pinker, The Language Instinct (1994) and Words and Rules (1999); M. J. Traxler, Introduction to
  Psycholinguistics (2012); M. H. Christiansen and N. Chater, The Language Game (2022).

## Problems and solutions

**1. Surprisal is a change of belief.** A reader holds a probability over analyses $T$. Show that $D_{\mathrm{KL}}(P(T \mid w_{\le t}) \,\|\, P(T \mid w_{<t})) = -\log P(w_t \mid w_{<t})$ when each analysis fixes the words.

*Solution.* If each analysis T fixes the words, then P(w_t | T, w_{<t}) is 1 when T is
consistent with w_t and 0 otherwise. By Bayes's rule P(T | w_{≤t}) = P(T | w_{<t}) 1[T fits w_t] / P(w_t | w_{<t}).
So D_KL(P(T | w_{≤t}) ‖ P(T | w_{<t})) = Σ_T P(T | w_{≤t}) log [P(T | w_{≤t}) / P(T | w_{<t})] =
Σ_{T fits w_t} P(T | w_{≤t}) log [1 / P(w_t | w_{<t})] = −log P(w_t | w_{<t}), since the posterior sums to one over
the analyses that fit. This is Levy's (2008) result: the cost of a word is the amount by which it changes what the
reader believes about the sentence, whatever grammar the beliefs are over.

**2. The stream's transitional probabilities.** In a stream of four three-syllable words with no word repeated twice running, show that transitional probabilities are 1 inside words and $\tfrac{1}{3}$ across boundaries.

*Solution.* Inside a word, the syllable after the first is always the second and
after the second always the third, so P(next | this) = 1. The last syllable of word k is followed by the first
syllable of the next word, which is one of the other three words, each equally likely when the next word is drawn
uniformly with no repeat. The four first syllables are distinct, so each continuation has probability 1/3. (The
estimates in a finite stream scatter around 1/3: in Psyche's 540 syllables they run from 0.21 to 0.40.)

**3. How much the commonest words cover.** Under Zipf's law with exponent 1 and $N$ word types, show that the $k$ commonest words cover about $\ln k / \ln N$ of all tokens.

*Solution.* With frequencies f_r ∝ 1/r for r = 1, …, N, the k commonest words cover
H_k / H_N of the tokens, where H_n = Σ_{r≤n} 1/r = ln n + γ + O(1/n). So the share is (ln k + γ)/(ln N + γ) ≈
ln k / ln N. With N = 60,000 types, the 100 commonest cover about 0.45 and the 1,000 commonest about 0.65: a reader
who knows a thousand words still meets an unknown one every few lines, which is why vocabulary keeps growing for life.
(The novels' exponent is 1.2, so their real coverage is higher.)

**4. One unit's steady state.** For one unit of the interactive activation model with constant net input $n > 0$, find its steady activation, and say how decay and the ceiling share the work.

*Solution.* In the interactive activation model a unit with positive net input n changes by
Δa = n(M − a) − D(a − r), with maximum M, rest r and decay D. Setting Δa = 0 gives n(M − a) = D(a − r), so
a* = (nM + Dr)/(n + D), a weighted average of the ceiling and the rest with weights n and D. Strong input pulls the
unit towards M, but never past it, since the input's effect shrinks as a approaches M; decay pulls it back to rest in
proportion to how far it has gone. With M = 1 and r = 0, a* = n/(n + D): doubling the input does not double the
activation, which is what keeps a network of such units stable while letters and words excite each other.

**5. Gold's argument.** Sketch why no learner can identify every language in a family that contains all finite languages and one infinite one, from examples alone.

*Solution.* Take the family of every finite language L_1 ⊂ L_2 ⊂ … (L_k the first k sentences) and their
union L_∞. Suppose a learner identifies every finite language in the limit. Build a text: give sentences of L_1
until the learner guesses L_1 (it must, eventually, since this could be a text for L_1); then add the second
sentence and repeat it until the learner guesses L_2 (it must, since this could be a text for L_2); and so on. The
text that results contains every sentence of L_∞, so it is a text for L_∞, but the learner changes its guess
infinitely often and never settles on L_∞. So no learner identifies the whole family from positive examples alone.
Horning's answer is that probabilities change the problem: a learner that knows sentences are sampled can notice
what never comes, and the simplest grammar that fits is identified with probability one.

**6. Spillover two words back.** With `explainer.psychology.opendata`: add the surprisal of the word two back to the reading-time regression. Does the cost spill over further?

*Solution.* Adding the surprisal of the word two back to the regression on the ten stories
gives 1.18 ms per bit on the next word (s.e. 0.08) and 0.43 ms per bit two words on (s.e. 0.08), with the word's own
surprisal still near 0 (0.03, s.e. 0.11). The cost spills over further but fades. Self-paced reading is known for
this: readers press the key before they have finished with a word. Eye movements show more of the cost on the word
itself.

**7. ★ A nonce-verb study.** Design a nonce-verb study (*spling*, *plip*) whose results a words-and-rules account and a single-network account must predict differently.

*Solution.* Words and rules says irregular forms are stored and generalize by similarity, while *-ed*
is a rule that applies to anything. A single network says both kinds generalize by similarity. So vary two things
independently: how similar a made-up verb is to irregular families (*spling*, like *sing* and *cling*, against
*ploamph*, like nothing) and to regular ones (*plip*, like *slip* and *flip*). Both accounts predict that *splung* is an
acceptable past of *spling* and that no irregular past of *ploamph* is. They part on the regular forms: words and rules
predicts *ploamphed* is as acceptable as *plipped*, since the rule does not care about similarity; the network
predicts *plipped* is better. Prasada and Pinker (1993) found regulars insensitive to similarity; Albright and Hayes
(2003) found that regulars too are rated better in "islands of reliability". The design also needs ratings and
productions from the same people, and verbs matched for length and sound probability.

## Open checks

Before the narrated master:

* Marcus et al.'s 4.2% and Johnson and Newport's design are from summaries and the abstracts; no correlation from
  the 1989 paper is quoted.
* Black and Bergmann's meta-analytic result and Lehtonen et al.'s 891 effect sizes and 152 studies are from the
  abstracts; read the papers' tables before quoting effect sizes.
* Hart and Risley's 42 families and the "30 million" are as usually quoted; the film says the size of the gap is
  disputed.
* Vong et al.'s 61 hours and 6 to 25 months, and Oh and Schuler's result, are from the papers' abstracts.
* The Natural Stories files carry no licence: they are fetched on first use and never redistributed.
* The eye-movement path, the critical-period curves, the ERP waves and the language-network bars are schematics and
  say so on screen.
* The preflight's two text-overlap warnings in Levels (both editions) are the word *wugs* written into the blank of
  "There are two ___", as intended.
