# Part2 tail source/factual review

Reviewed manifest entries8–16inclusive (**Samuel through Outro**,9scenes), plus supporting algorithms,computeexpressions,READMEexercises,ZHnarration,andrelevantdocs. Sourcecheckpoint `a70adf01089d532c08c830f0118ee5ce5395e0a8`. **No repository edits,compute/cacheloadhelpercalls,renders,continuousplaybackoraudioreview.**

## Main correction candidates

### T01 · high · Survives · verified

Multiplier panel says there is no short proof to learn.

This experiment is a solver run, not a proof-size lower bound. Beame and Liew construct polynomial regular-resolution proofs for degree2 identities on array multipliers; commutativity is one of their explicit cases. The local circuit is a shift-and-add array multiplier returning only low n product bits.

Suggested correction: Replace with an empirical solver-search statement: dense bit interactions make short useful clauses difficult for this solver to find. Label low n product bits/modulo2^n, and preserve completed widths and measured conflict counts.

Locations: [videos/ai/ai2/s15_survives.py:144](/workspace/explainer-videos/videos/ai/ai2/s15_survives.py:144), [videos/ai/ai2/sat.py:464](/workspace/explainer-videos/videos/ai/ai2/sat.py:464).

Primary evidence: [arxiv.org](https://arxiv.org/html/1705.04302v3).

### T02 · high · Survives · verified

LLM-to-PDDL-to-planner pipeline promises a plan guaranteed to work.

LLM+P §3 assumes a provided domain PDDL file and translates the problem/initial state/goal. The paper gives a generated PDDL example with invented predicate and omitted initial fact. Planner soundness is relative to encoded domain/problem; it does not certify natural-language translation or physical model fidelity.

Suggested correction: Say a plan valid in the supplied formal model, conditional on faithful translation; show that the translation/model must be checked. Preserve historical PlanBench percentages.

Locations: [videos/ai/ai2/s15_survives.py:227](/workspace/explainer-videos/videos/ai/ai2/s15_survives.py:227), [videos/ai/ai2/s15_survives.py:237](/workspace/explainer-videos/videos/ai/ai2/s15_survives.py:237), [videos/ai/ai2/zh_lines.py:347](/workspace/explainer-videos/videos/ai/ai2/zh_lines.py:347).

Primary evidence: [arxiv.org](https://arxiv.org/html/2304.11477v2).

### T03 · medium · Knowledge · verified

MYCIN65% is labeled as percent of cases.

Yu et al. evaluated10test cases using8independent expert evaluators. The reported65% is acceptability rating, while the five faculty specialist ratings were42.5–62.5%. It is not65% of10cases. Main comparative conclusion is supported.

Suggested correction: Use acceptability rating65%, with10cases/8evaluators as context; do not present it as clinical efficacy or case success rate.

Locations: [videos/ai/ai2/s12_knowledge.py:150](/workspace/explainer-videos/videos/ai/ai2/s12_knowledge.py:150), [videos/ai/ai2/s12_knowledge.py:163](/workspace/explainer-videos/videos/ai/ai2/s12_knowledge.py:163).

Primary evidence: [jamanetwork.com](https://jamanetwork.com/journals/jama/article-abstract/366606).

### T04 · medium · Eliza · verified

Recovered original code is immediately described as the ELIZA judged human23% in2025.

Jones/Bergen §4.1 specifies a Python implementation of DOCTOR citing Brainerd2023. The recovered original program is a separate historical object. The23% result and5minute simultaneous three-party setup are verified.

Suggested correction: Separate the claims explicitly: original reanimated in2024; a Python DOCTOR implementation was judged human23% in2025. Do not imply the recovered original was the tested implementation.

Locations: [videos/ai/ai2/s13_eliza.py:188](/workspace/explainer-videos/videos/ai/ai2/s13_eliza.py:188), [videos/ai/ai2/s13_eliza.py:198](/workspace/explainer-videos/videos/ai/ai2/s13_eliza.py:198), [videos/ai/ai2/zh_lines.py:312](/workspace/explainer-videos/videos/ai/ai2/zh_lines.py:312).

Primary evidence: [arxiv.org](https://arxiv.org/html/2503.23674v1).

### T05 · medium · Outro · verified

Recap says admissible A* examines a fraction of the space and alpha-beta searches twice as deep for the same work, unconditionally.

An admissible h may be identically0, yielding uniform-cost search. Alpha-beta can approach minimax work under poor move ordering; the b^(d/2) benefit is the best case discussed correctly in the problem set.

Suggested correction: Use A* can reduce search, and alpha-beta can reach roughly twice the depth with excellent move ordering. Keep the earlier exact best-case theorem.

Locations: [videos/ai/ai2/s16_outro.py:98](/workspace/explainer-videos/videos/ai/ai2/s16_outro.py:98), [videos/ai/ai2/s16_outro.py:100](/workspace/explainer-videos/videos/ai/ai2/s16_outro.py:100), [videos/ai/ai2/zh_lines.py:354](/workspace/explainer-videos/videos/ai/ai2/zh_lines.py:354).

### T06 · medium · Outro · verified

Exercise6 parenthetical says correlated clusters inflate the expected number of satisfying assignments.

The solution correctly derives E[X]=2^n(7/8)^m by linearity. Dependence between assignment indicators does not change that expectation. Correlations/uneven solution counts make the first-moment bound loose; they do not add an extra inflation to the derived mean. Main bound5.19 and refutation examples are correct.

Suggested correction: Replace parenthetical with: the first moment is only an upper bound; a large expectation need not mean a formula is likely satisfiable, since solutions can be concentrated in a small fraction of formulas. Label4.267 as physics prediction rather than proved exact3SATthreshold.

Locations: [videos/ai/ai2/README.md:165](/workspace/explainer-videos/videos/ai/ai2/README.md:165), [videos/ai/ai2/README.md:167](/workspace/explainer-videos/videos/ai/ai2/README.md:167), [videos/ai/ai2/README.md:211](/workspace/explainer-videos/videos/ai/ai2/README.md:211).

### T07 · medium · Plans · verified_distinction_wording_ambiguous

Delete relaxation, a fast solution cost, h_max and FF-style extraction are presented as one easy-cost construction.

An arbitrary relaxed plan can be found in polynomial time, but minimum relaxed-plan length h+ is NP-hard. h_max is a cheaper admissible fact-cost approximation. The local ff implementation chooses h_add-cost achievers and counts their union; original FF extracts from a relaxed planning graph. Existing wording can be interpreted charitably as finding any relaxed plan, so this is precision repair rather than demonstrated solver failure.

Suggested correction: State that cheap approximations to delete relaxation guide search: h_max is admissible, while an FF-style extracted relaxed-plan length need not be. Label local heuristic FF-style unless exactly reproducing originalFF.

Locations: [videos/ai/ai2/s11_plans.py:280](/workspace/explainer-videos/videos/ai/ai2/s11_plans.py:280), [videos/ai/ai2/s11_plans.py:293](/workspace/explainer-videos/videos/ai/ai2/s11_plans.py:293), [videos/ai/ai2/plan.py:85](/workspace/explainer-videos/videos/ai/ai2/plan.py:85), [videos/ai/ai2/zh_lines.py:271](/workspace/explainer-videos/videos/ai/ai2/zh_lines.py:271).

Primary evidence: [aiinternational.org](https://aiinternational.org/Library/JAIR/Vol24/jair24-018.php), [fai.cs.uni-saarland.de](https://fai.cs.uni-saarland.de/hoffmann/ff.html).

### T08 · medium · Survives · verified

A Lean proof that compiles is called correct without assumptions.

Lean accepts proofs relative to their statement, definitions and axioms. Compiling can succeed with sorry/custom axioms or unintended statement meaning; the official validation guide requires examining axioms and meaning. The actual1+1=2 toy statement itself is fine.

Suggested correction: Say kernel-checked proof of the formal statement under its declared assumptions, with no unproved placeholders; relate semantic/formalization checking to the PDDL qualification.

Locations: [videos/ai/ai2/s15_survives.py:187](/workspace/explainer-videos/videos/ai/ai2/s15_survives.py:187), [videos/ai/ai2/zh_lines.py:344](/workspace/explainer-videos/videos/ai/ai2/zh_lines.py:344).

Primary evidence: [lean-lang.org](https://lean-lang.org/doc/reference/latest/ValidatingProofs/).

### T09 · low · Winters · source_record_verified_broader_attribution_unresolved

Schank and Minsky are described as naming AI winter atAAAI1984.

The actualAAAI84panel transcript lists DrewMcDermott, Waldrop, Schank, Chandrasekaran, JohnMcDermott, and DARPARonOhlander. DrewMcDermott introducesAIwinter as an already-used phrase. Minsky is mentioned as a participant in a different Asimov seminar. This does not prove no other1984warning byMinsky existed, but the directly available panel does not establish that attribution/coinage.

Suggested correction: Safest source-backed wording: a1984AAAIpanel discussed a possibleAIwinter, with Schank warning about exaggerated expectations. Cite the1985published panel rather than assert coinage.

Locations: [videos/ai/ai2/s14_winters.py:90](/workspace/explainer-videos/videos/ai/ai2/s14_winters.py:90), [videos/ai/ai2/s14_winters.py:106](/workspace/explainer-videos/videos/ai/ai2/s14_winters.py:106), [videos/ai/ai2/zh_lines.py:322](/workspace/explainer-videos/videos/ai/ai2/zh_lines.py:322).

Primary evidence: [ojs.aaai.org](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/494), [www.researchgate.net](https://www.researchgate.net/publication/220604602_The_dark_ages_of_AI_A_panel_discussion_at_AAAI-84).

### T10 · low · SAT · verified

FirstUIP is a point every path passes through; every competitive solver is said to useCDCL.

UIP quantifies paths from the most recent decision literal to the conflict; graph has other decision roots. The implementation docstring278–280 correctly describes current-level resolution. Competitive incomplete SAT solvers/portfolios need not all be pureCDCL.

Suggested correction: Specify latest-decision-to-conflict paths and say leading complete general-purpose solvers commonly useCDCL. Current textbook implication graph hardcoded decisions appear internally consistent; completedcdclJSONabsent.

Locations: [videos/ai/ai2/s10_sat.py:385](/workspace/explainer-videos/videos/ai/ai2/s10_sat.py:385), [videos/ai/ai2/s10_sat.py:388](/workspace/explainer-videos/videos/ai/ai2/s10_sat.py:388), [videos/ai/ai2/zh_lines.py:243](/workspace/explainer-videos/videos/ai/ai2/zh_lines.py:243).

### T11 · low · Samuel · modernization_explicit_in_local_code_historical_detail_partial

Modern gradient update is displayed inside a block labeled Samuel learning rule.

Local implementation uses tanh(w·features), a differentiable semi-gradient update and bootstrapped search target. This is a Samuel-inspired modernTDanalogue, not a literal reconstruction of1959feature-correlation and replacement machinery. Publisher abstract verifies general learning claim but full1959primarytext was unavailable from attempted public academicPDF; exact historical-rule comparison remains reference-limited.

Suggested correction: Label displayed gradient a modernTD-style analogue inspired bySamuel; preserve originaldelta/search idea and separate currentConnectFour experiment. Avoid treating this as a demonstrated learning bug.

Locations: [videos/ai/ai2/s08_samuel.py:85](/workspace/explainer-videos/videos/ai/ai2/s08_samuel.py:85), [videos/ai/ai2/s08_samuel.py:90](/workspace/explainer-videos/videos/ai/ai2/s08_samuel.py:90), [videos/ai/ai2/play.py:320](/workspace/explainer-videos/videos/ai/ai2/play.py:320).

Primary evidence: [ieeexplore.ieee.org](https://ieeexplore.ieee.org/abstract/document/5392560/authors).

### T12 · low · Samuel · source_fragility_current_result_untested

Crossing0.5byanyruns selects roughly-even/some-ahead-some-behind narration.

Predicate max(vp)>=0.5 and not min(vp)>0.5 also permits allruns exactly0.5 or an arbitrarily large spread. Thus that predicate alone does not establish its prose. CurrentSamuleJSONabsent, so no actualbadverdict observed.

Suggested correction: Use neutral numerically statedrange or explicit tolerances/strictsignchecks if this branch occurs. No training change needed.

Locations: [videos/ai/ai2/s08_samuel.py:238](/workspace/explainer-videos/videos/ai/ai2/s08_samuel.py:238), [videos/ai/ai2/s08_samuel.py:242](/workspace/explainer-videos/videos/ai/ai2/s08_samuel.py:242).

## Actual per-chapter coverage

|Scene|Source coverage|CompletedJSON dependencies|Findings|
|---|---|---|---|
|Samuel|historical scoring equation,delta/modernupdate,alphaBeta selfplay; feature/replay/evaluation source and verdictbranches; DeepBlue/Chinook/Go narrative; EN/ZHstatictext|samuel:absent/untested, testset:absent/untested|T11, T12|
|Logic|truth-table entailment; FOL/completeness/undecidability; binaryresolution+factoring+unification/source; actualprop/FOLcachedprooftexts; set-of-support capstatus and familyfacts; EN/ZHstatictext|resolution:available|No additional concrete defect found|
|SAT|smallDPLLformula and trace source; random3SATgenerator/firstmoment link; censoring/outcome/widthreporting source; firstUIP/watchers/circuits and addercomparisons; EN/ZHstatictext|sat3:absent/untested, cdcl:absent/untested|T10|
|Plans|SudokuAC3,backtracksource/cache; STRIPS pre/add/delete lists; Sussmanstartgoal/interleaving/source; Lahcountformula/greedy/A* hmax/FFstyle source; EN/ZHstatictext|sudoku:available, blocks:absent/untested|T07|
|Knowledge|semanticnet/defaultframes narrative; forwardchain R1R5R6 trace/cache; positivecertaintyfactor arithmetic/cache; MYCINprimaryevaluation; XCON/Cyc/KnowledgeGraphhistorysource; EN/ZHstatictext|rules:available|T03|
|Eliza|keyword/decomposition/reassembly algorithm and rotation; all15cachedtranscriptrows/newqueries; recoveredcode vs testedimplementation; ELIZAeffect narrative; EN/ZHstatictext|eliza:available|T04|
|Winters|ALPACprimaryreportcomparison; funding/Perceptrons/Lighthill/FGCSchronology source; AAAI84primarypanelrecord; Moravecinterpretation; wordtypes/tokenlongtail/cache vs knowledgegeneralization; EN/ZHstatictext|tail:available|T09|
|Survives|AlphaZero/Stockfish primarypositionrate; SATmiter/adders/lowproductbits source; proofcomplexity primarycounterevidence; AWSprimarybillionSMTclaim; AlphaGeometry/AlphaProof/Gemini2025primaryresults; PlanBenchprimarytable andLLM+Pformalizationassumptions; Leanofficialtrustconditions; EN/ZHstatictext|cdcl:absent/untested|T01, T02, T08|
|Outro|recaptiles and conditionalSATbounds source; search/alphaBetaguaranteequalifiers; Parts3/9/26/28/29/31continuity; sixEN/ZHexerciseanswers/refutation/recurrences/firstmoment; bibliography/sourceattribution|sat3:absent/untested, cdcl:absent/untested, tail:available|T05, T06|

## Measured completed-cache evidence

RawcompletedJSONonly; no cacheloadhelper or missing-itemcompute. Each file hash is preserved in theJSONreport.

```json
{
  "resolution": {
    "schema_version": 3,
    "explode_saturate": {
      "found": false,
      "status": "limit",
      "clause_cap": 4000,
      "made": 4000,
      "levels": 3,
      "proof_len": 0
    },
    "explode_support": {
      "found": true,
      "status": "refuted",
      "clause_cap": 4000,
      "made": 2823,
      "levels": 8,
      "proof_len": 15
    },
    "proof_texts": {
      "prop": [
        "¬Rain ∨ Wet",
        "¬Sprinkler ∨ Wet",
        "Rain ∨ Sprinkler",
        "¬Wet",
        "¬Rain",
        "¬Sprinkler",
        "Rain",
        "□"
      ],
      "fol": [
        "Grandparent(x, y) ∨ ¬Parent(x, z) ∨ ¬Parent(z, y)",
        "Parent(Anne, Byron)",
        "Parent(Byron, Ada)",
        "¬Grandparent(Anne, Ada)",
        "¬Parent(Anne, x) ∨ ¬Parent(x, Ada)",
        "¬Parent(Anne, Byron)",
        "□"
      ]
    }
  },
  "sudoku": {
    "clues": 26,
    "ac3_solved": 3,
    "nodes_plain": 3642,
    "nodes_fc": 1669,
    "nodes_mrv": 182,
    "nodes_mac": 93,
    "deletions": 313,
    "initial_empty": 55,
    "candidates_left": 182
  },
  "rules": {
    "fired": [
      "R1",
      "R5",
      "R6"
    ],
    "derived": [
      "mammal",
      "carnivore",
      "cheetah"
    ],
    "cf": [
      0.6,
      0.5,
      0.4
    ],
    "cf_combined": [
      0.6,
      0.8,
      0.88
    ]
  },
  "eliza": {
    "matches": 14,
    "total": 15,
    "differences": [
      {
        "user": "Bullies.",
        "ours": "LETS DISCUSS FURTHER WHY YOUR BOYFRIEND MADE YOU COME HERE",
        "1966": "DOES THAT HAVE ANYTHING TO DO WITH THE FACT THAT YOUR BOYFRIEND MADE YOU COME HERE",
        "same": false
      }
    ],
    "new": [
      [
        "I feel that nobody understands me.",
        "REALLY, NOBODY"
      ],
      [
        "What is the capital of France?",
        "WHY DO YOU ASK"
      ],
      [
        "Can you prove that every even number is the sum of two primes?",
        "YOU BELIEVE I CAN PROVE THAT EVERY EVEN NUMBER IS THE SUM OF TWO PRIMES DON'T YOU"
      ],
      [
        "I am a computer program.",
        "DO COMPUTERS WORRY YOU"
      ],
      [
        "Why can't I sleep?",
        "DO YOU THINK YOU SHOULD BE ABLE TO SLEEP"
      ],
      [
        "My dog died last week.",
        "YOUR DOG DIED LAST WEEK"
      ]
    ]
  },
  "tail": {
    "n_tokens": 4326411,
    "n_types": 59639,
    "need": {
      "0.5": 76,
      "0.9": 4177,
      "0.95": 9144,
      "0.99": 28193,
      "0.999": 55313
    },
    "once": 21797,
    "passage_tokens": 3909,
    "unseen_passage_final": 0.027884369403939627
  }
}
```

## Validation and remaining limits

Statictranslationcoverage: **119/119Part2sourcelines covered**. Existingwarning: computed `try {variable} {true/false}` adjacentvalues. This checks source-keycoverage, not actualbilingualrenderedcaptionsorpronunciation.

- samuel/testset/sat3/cdcl/blocks completedJSONabsent atlast inventory; no training/solverexecution permitted in this review.
- NoNPZarrayreads, so array-backedplotgeometry/curves/countdata not verified independently.
- No full primary re-reading for every historicaldetail: DeepBlue30processor/480chips/126M/8000details and literal1959Samuelweightalgorithm remain citation-backed but independently unverified; currentIBMsummary says32processors ratherthan30, do not blindlyoverwrite authors2002specs.
- No renderedlayout/playback/audioquality/AVsync tested.
- OriginalAAAIofficialPDFdownload returned503; author-uploadedprimarytranscript and officialarticlemetadata were available. OtherunavailablepublicPDFs recorded as partialreferencecoverage, no bypassorpaidaccess.

Themainexerciseequations, STRIPS action effects, cachedresolutionproof sequence, availableSudoku/rule/ELIZA/tailnumbers were checked. Longtaildemonstration is illustrative evidence about wordfrequency; it does not prove arbitraryknowledge has this exactdistribution or that learning eliminates rare-casefailures. ThelocalFFimplementation is best described asFF-style ratherthan a literaloriginalFFreimplementation. HistoricalMoravecandwinterend-datephrasing are interpretivenarrative; no newnumerical result is asserted from them.

Machine-read evidence and sourcehashes: [ai2-tail-source-review.json](/workspace/runtime/ai2-tail-source-review.json).


## Follow-up correction batch applied

Applied the six confirmed areas in local tail scenes and their six Chinese narration entries: relaxed planning cost/FF-style labeling, MYCIN rating units, recovered ELIZA versus tested Python DOCTOR, empirical multiplier difficulty and low-product-bit scope, model-conditional PDDL guarantees, and qualified A*/alpha-beta recap.

Seven changed caption strings and suggested Chinese translations are ready for the parent's central merge in [ai2-tail-caption-add.json](/workspace/runtime/ai2-tail-caption-add.json). No shared caption table or README edits were made by this agent. The exact bilingual README first-moment answer replacement is included in [ai2-tail-correction-handoff.json](/workspace/runtime/ai2-tail-correction-handoff.json), along with old/new voiceover AST expressions and actual formatted English/Chinese samples.

Validation: seven formatting/translation samples preserve all bookmarks; all edited Python parses; `git diff --check` passes. Three literal samples, one completed rules-cache sample, and three explicitly synthetic Plans/multiplier formatting samples are distinguished in the JSON. No algorithm runs or rendered output were used. The initial source review above is a before-correction checkpoint; its source hashes and line evidence remain historical evidence. The parent's final render pass must validate the revised source.
