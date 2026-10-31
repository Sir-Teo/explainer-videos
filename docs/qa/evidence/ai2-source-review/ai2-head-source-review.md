# Part2 head source/factual review

Observed: 2026-10-31T13:57:31.532934+00:00. Scope: manifest indices0–7. Read-only source review, not rendered QA.

All eight scene modules, relevant compute expressions, machines/search/local/play implementations, first-eight-chapter Chinese narration, manifest/README/lecture guide were read. Existing repaired algorithms were rechecked by source only. No compute function or Cache.load was called; no source was changed. Completed raw JSON was inspected where present; NPZ arrays were not loaded.

## Per-chapter coverage

### 0. Hook — videos/ai/ai2/s01_hook.py

Checked: Simon/Newell forecast; publication date vs speech date; 1950–1997 timeline; winters explicitly approximate; Objectives and bridges to Parts26/modern systems.

Methods: construct, prediction, era, question, plan.

Data: .

Findings: no confirmed new defect; historical verification limits below. Rendered frames, full playback, audio and sync: untested.

### 1. Turing — videos/ai/ai2/s02_turing.py

Checked: Incrementer state/head/rule replay and universal-machine explanation; Halting diagonal argument and Church comparison; Binary busy-beaver scope and run counts; Turing1950 standard-test simplification; Jones/Bergen persona-dependent results; Dartmouth quotation, LogicTheorist and physical-symbol hypothesis.

Methods: construct, card, machine, halting, beaver, imitation, dartmouth.

Data: tm: completed rawJSONinspected;arraysinNPZnotloaded.

Findings: H02. Rendered frames, full playback, audio and sync: untested.

### 2. Search — videos/ai/ai2/s03_search.py

Checked: Puzzle transitions and9!/2 reachable-state count; BFS layer plot and shortest-depth reasoning; BFS/DFS/iterative-deepening ordering, memory and historical attribution; Dijkstra cost units,16moves, obstacles and goal count.

Methods: construct, card, state_space, layers, orders, dijkstra.

Data: puzzle8: completed rawJSONinspected;arraysinNPZnotloaded; grid: completed rawJSONinspected;arraysinNPZnotloaded.

Findings: H07, H08. Rendered frames, full playback, audio and sync: untested.

### 3. AStar — videos/ai/ai2/s04_astar.py

Checked: f=g+h and Euclidean heuristic; Separate path identity vs optimal cost; Circle/ellipse boundary inequalities and units; Admissibility/reopening proof; consistency and nondecreasing f; Batch medians,paired ratios,weighted/greedy guarantees.

Methods: construct, card, idea, race, optimal, consistent, batch.

Data: grid: completed rawJSONinspected;arraysinNPZnotloaded.

Findings: H03, H04. Rendered frames, full playback, audio and sync: untested.

### 4. Heuristics — videos/ai/ai2/s05_heuristics.py

Checked: Relaxed-puzzle Manhattan/misplaced derivations; Dominance repair; mandatory interior vs tie boundary; Effective branching factor N+1 convention; 15-puzzle state count,IDA thresholds,disjoint pattern-database cost accounting; Censoring/sample-count scope; DeepCubeA60.3% and bridge to AlphaZero.

Methods: construct, card, relax, dominance, fifteen, learned.

Data: puzzle8: completed rawJSONinspected;arraysinNPZnotloaded; puzzle15: completed rawJSONinspected;arraysinNPZnotloaded.

Findings: H05, H13. Rendered frames, full playback, audio and sync: untested.

### 5. Local — videos/ai/ai2/s06_local.py

Checked: Landscape hill climbing and queen attacking-pair descent; Restart expectation and finite-vs-almost-sure language; Metropolis rule,detailed balance,stationary vs cooling claim; Actual TSPevaluation currency and seed spread; Nearest-neighbour baselines and OX/GAtrace; FunSearch/AlphaEvolve.

Methods: construct, card, hills, queens, metropolis, cooling, budgets, genetic.

Data: queens: completed rawJSONinspected;arraysinNPZnotloaded; tsp: completed rawJSONinspected;arraysinNPZnotloaded.

Findings: H06, H09, H10, H14. Rendered frames, full playback, audio and sync: untested.

### 6. Games — videos/ai/ai2/s07_games.py

Checked: Minimax recurrences and complete-game vs unique-position counting; Full toyLEAVES and fail-soft alpha-beta trace values; Window semantics,cutoffbound display and root preservation; Perfect-order exact leaf formula; odd/even approximation; ConnectFour counted search/oracle setup and reported means.

Methods: construct, card, minimax, pruning, best_case, counts.

Data: ttt: completed rawJSONinspected;arraysinNPZnotloaded; uniform: completed rawJSONinspected;arraysinNPZnotloaded; alphabeta: completed rawJSONinspected;arraysinNPZnotloaded.

Findings: H01. Rendered frames, full playback, audio and sync: untested.

### 7. Samuel — videos/ai/ai2/s08_samuel.py

Checked: HistoricalSamuel features/AlphaBeta/delta vs moderngradient analogue; tanh evaluation/gradient update and two-ply temporal alignment; Replay weight units,sign thresholds and data-dependent verdicts; Fixed-opponent scores,last-three checkpoints,selected solved-position grading; DeepBlue/Chinook historical scope and Go/Part26 bridge.

Methods: construct, card, samuel, rule, replay, verdict, deep_blue, solved.

Data: samuel: missing completionJSON;unverified; testset: missing completionJSON;unverified.

Findings: H11, H12. Rendered frames, full playback, audio and sync: untested.

## Findings and proposed coherent correction batch

### H01 [P1] Cutoff bound is displayed as an exact internal minimax value

References: videos/ai/ai2/s07_games.py:30, videos/ai/ai2/s07_games.py:51, videos/ai/ai2/s07_games.py:175.

For the actual27LEAVES, the third root-child MIN has exact value min(max(6,5,3),max(8,1,9),max(4,2,5))=5. With inheritedalpha6, it cuts after its firstMAXchild6 and returns fail-soft6. The renderer writes bare6 at that node. The root exactvalue remains6. This is an analytic trace review, not executed playback.

Proposed repair: Record bound type atcutoffs and label MINupperbounds≤v/MAXlowerbounds≥v (or hide incomplete values); retain exactroot. Add actualtoy regression.

Evidence status: confirmed-source-or-completed-JSON.

### H02 [P2] Busy-beaver definition omits fixed binary alphabet

References: videos/ai/ai2/s02_turing.py:166, videos/ai/ai2/s02_turing.py:177.

The displayed definition quantifies all n-state machines, but quoted BB(5)=47,176,870 applies to the standard2-symbol model. No spoken/on-screen2-symbol qualification occurs in the block; implementation is binary. Officialbbchallenge explicitly fixes5states/2symbols.

Proposed repair: State n nonhalting states and2 tape symbols (plus a separate halt state), blank/all-zero tape, in caption/narration.

Evidence status: confirmed-source-or-completed-JSON.

### H03 [P2] Two different optimal routes are called the same path

References: videos/ai/ai2/s04_astar.py:115, videos/ai/ai2/s04_astar.py:144, videos/ai/ai2/zh_lines.py:81.

CompletedgridJSON: Dijkstra cost30.386970613475885, A*cost30.38697061347589; both routes18moves but differ at route index1 ([33,32] versus[31,33]). The EN/ZH label and narration assert identical path.

Proposed repair: Say sameoptimalcost; show both legitimate routes without equating identities.

Evidence status: confirmed-source-or-completed-JSON.

### H04 [P2] Strict interior wording excludes boundary expansions and the counted goal

References: videos/ai/ai2/s04_astar.py:146, videos/ai/ai2/search.py:110.

grid_search records/closes/increments the goal beforereturning; itsg+h=C*. Other tie-boundary nodes may alsoexpand. Caption correctlyuses≤ while EN/ZHVO saysbelow/closerthan.

Proposed repair: Use atmostC* (and g not Euclidean distance when provingDijkstra); retain mandatoryf<C* vs optionalboundary distinction.

Evidence status: confirmed-source-or-completed-JSON.

### H05 [P2] A hundred samples per depth overstates low-depth sample counts

References: videos/ai/ai2/s05_heuristics.py:119, videos/ai/ai2/s05_heuristics.py:122, videos/ai/ai2/compute.py:188.

Sampling usesmin(per_depth,len(layer)). At depth2 only4states exist from the corner-blank goal, so100cannotbe sampled; existingcacheper_depth=100isrequestedcap, not actualperdepthcount.

Proposed repair: Say up to100; if showing actualcounts deriveexistinglayers/readactualsample metadata, no newproductioncomputationneeded.

Evidence status: confirmed-source-or-completed-JSON.

### H06 [P2] Best nearest-neighbour tour and best polished tour come from different starts

References: videos/ai/ai2/s06_local.py:295, videos/ai/ai2/compute.py:386.

CompletedTSPJSON: bestNNstart39 length8181; polishing that same tour gives7711. The reportedminnn2opt7657comesstart44. Narration says2-optpolishesit to7657.

Proposed repair: Explain these are separately selected best-over-starts baselines, or report7711for the same tour.

Evidence status: confirmed-source-or-completed-JSON.

### H07 [P2] DFS memory bound uses solution depth instead of maximum explored depth

References: videos/ai/ai2/s03_search.py:140, videos/ai/ai2/s03_search.py:146.

A solution atdepthd doesnotbound ordinaryDFS depth; it canexplore an arbitrarilydeepwrongbranch while shallow solutionexists. O(bm)usesmaxexploreddepthm; O(bd)applies depth-limitedDFS/iterativedeepening to boundd. EN/ZHbothconflate.

Proposed repair: Usem for ordinaryDFSmaxdepth anddforfirstsolution/iterativedeepeningbound; qualify equalcost shortest-first.

Evidence status: confirmed-source-or-completed-JSON.

### H08 [P2] Iterative-deepening history conflates prior technique with Korf1985 analysis/IDA*

References: videos/ai/ai2/s03_search.py:141, videos/ai/ai2/s03_search.py:148.

Korf ownIJCAI1985introduction states iterativedeepening was repeatedlyrediscovered and credits earliestdocumenteduse toSlate/AtkinChess4.5(1977); his1985paperproposes/analyzesIDA*. CurrentVOcalls generaliterativedeepening fromKorf1985.

Proposed repair: Say analyzedbyKorf1985; preserve prioruse or use1977citation for nonheuristic technique; keep1985IDA*credit.

Evidence status: confirmed-source-or-completed-JSON.

### H09 [P2] Detailed balance is presented as a consequence of equilibrium in general

References: videos/ai/ai2/s06_local.py:144, videos/ai/ai2/s06_local.py:158.

Stationarity doesnotimply pairwiseflowequality: a3-state deterministicclockwisecycle hasuniformstationarydistribution butonlyone-wayflows. Symmetric-proposalMetropolisdoes satisfy detailedbalance, so itsBoltzmannalgebra iscorrect afterthatconditionisexplicit. The lowTstatementalso concerns stationaryequilibriumfamily, not arbitraryfinitecoolingschedule.

Proposed repair: Say impose/checkdetailedbalance for thissymmetricproposalchain; qualify lowTequilibrium and mixing/slowcooling. No needchangealgorithm.

Evidence status: confirmed-source-or-completed-JSON.

### H10 [P2] GA child-quality majority is unmeasured and does not follow from final gap

References: videos/ai/ai2/s06_local.py:360, videos/ai/ai2/local.py:274.

NeitherdefaultTSPJSONnorcompute measures fraction ofchildren worse thanbothparents. Finalbestgap doesnotestablish mostchildrenworse; exactcrossover/mutationoutcomesdependparents.

Proposed repair: Remove unsupportedmajority/causalclaim or instrument it in future; keep measuredGAresult and limitations.

Evidence status: confirmed-source-or-completed-JSON.

### H11 [P2] Modern gradient rule is not identified as a modern Samuel-inspired analogue

References: videos/ai/ai2/s08_samuel.py:84, videos/ai/ai2/s08_samuel.py:101, videos/ai/ai2/play.py:381.

Samuel1959original(IBMpaper scannedatMIT), pp.542–543inreprint, uses correlations betweenfeaturecontribution signsanddelta, quantizedpower-of-two coefficient assignment andtermreplacement; heexplicitlysayschanges are notmade directly. Scene underSamuellearningrule displaysw+=eta*delta*gradient, whichis the modernTDstyleanalogueimplementedhere.

Proposed repair: Label modernsemi-gradientanalogue/inspiredbySamual; separate historicaldeltainsight fromcurrentConnectFourupdate. No assertion that modernnotationwasliteral1959algorithm.

Evidence status: confirmed-source-or-completed-JSON.

### H12 [P2] Positive-feature count silently discards small positive weights

References: videos/ai/ai2/s08_samuel.py:175.

nposcountsfin>0.02,butVOsaysnumberof featurescountinfavour, whose naturalcriterion is positiveweight. Aweight0.01stilladdspositivevalueforpositivefeature. DefaultsamuelJSONnotyetpresent; occurrenceunverified.

Proposed repair: Count>0 or explicitthresholdwording; keepactualdata-dependentnumber.

Evidence status: confirmed-code-condition; default-data-untested.

### H13 [P2] 15-puzzle capped-data branches can imply unknown optimal lengths and unqualified work ratios

References: videos/ai/ai2/s05_heuristics.py:148, videos/ai/ai2/s05_heuristics.py:162, videos/ai/ai2/s05_heuristics.py:188, videos/ai/ai2/compute.py:242.

Source usespdb_len as trueoptimalx evenif-1, andworkratio sums completedPDBwork vs possiblytruncatedManhattanwork. compute equalityassert assumesPDBmustsolvewheneverothermethoddoes. puzzle15JSONnotavailableatreadcheckpoint; no defaultcapfailureclaimed.

Proposed repair: Explicitunknownlength/censoredworkpaths; report matchedcompletedcases for completionwork or labelobservedtruncatedwork; preserve true invariantonlywhenbothsolved. Explain disjointtilecostpartition beforeaddingtables.

Evidence status: conditional-source-risk; default-data-untested.

### H14 [P3] Finite restart certainty is overstated

References: videos/ai/ai2/s06_local.py:103.

With estimatedsuccessprobabilityp=.1362, repeatedindependentrestarts succeedalmostsurelyintheunboundedlimit; nofinitebudgetguaranteessuccess. Caption sayssolvedforcertain beside expectedsteps.

Proposed repair: Labelalmostsure/eventualsuccess andexpectedsteps, not deterministicfinitecertainty.

Evidence status: confirmed-source-or-completed-JSON.

## Primary-source checks and limits

- https://bbchallenge.org/story — Binarymodel,47,176,870run,completionJuly2,2024; machine code agrees.
- https://arxiv.org/abs/2503.23674 — 2025preprint:5minute3party,personaGPT4.5=73%,ELIZA23%; not anunqualifiedallpromptclaim.
- https://www.pnas.org/doi/10.1073/pnas.2524472123 — 2026publishedversion supports samecore5minresults, adds15minstudy;2025preprintdate remains legitimate.
- https://academic.oup.com/mind/article/LIX/236/433/986238 — Original1950paperopened;text-only3playergameanduniversalcomputersread;70%forecastnotindependentlylocatedbeforefollowupfetchfailed.
- https://pubsonline.informs.org/doi/abs/10.1287/opre.6.1.1 — 1958paper publicationand1957speechdated;fullquotehiddenbehindabstract, not fullyverifiedhere.
- https://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf — IndexedprimaryproposalconfirmsAugust31,1955dateandconjecture;fullfetchtimeout.
- https://arxiv.org/html/2603.13514v1 — March2026report16/23forStefferud1963IPL-Vpedagogicalrecoding; sourceinternallydiffersabout1956workingprogramvs1957machineproofs, donotresolvehistoricalpriorityfromthisalone.
- https://ijcai.org/proceedings/1985/208 — Korfprimary1985introductionexplicitlydocumentspriorSlate/Atkin1977iterativedeepeningandIDA*extension.
- https://www.nature.com/articles/s42256-019-0070-z — DeepCubeA2019paperabstract100%testsolves,60.3%shortest. Scopeisitsownbenchmark.
- https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ — Developerprimary2025:4x4complexmatrices48scalarmultiplicationsvsStrassen49.
- https://webdocs.cs.ualberta.ca/~chinook/project/legacy.html — ChinookteamaccountNealeyrematchand1966fourgamesperopponentall8lost; not primarySamuel1959forlaterhistory.
- https://people.csail.mit.edu/brooks/idocs/Samuel.pdf — OriginalSamuelpaperdownloadednormallyfromindexedpublicMITcopy;localpdftotextpp.542–543correlation/coefficientprocedureandAlphaBetacopyrulechecked.
- https://research.ibm.com/publications/deep-blue — Author/publisherabstractconfirms1997matchandhardware/search/evaluationthemes; full2002paperfetch403,so30processors/480chips/126million/8000/manualtuningdetailsnotfullyreverified.

## Untested

- NoPart2renderedlayout/clipping/colorcontrast/motion/pacing/listening/sync/playerQAperformed.
- Noalgorithmsorbenchmarksraninthistask; toycutoffcounterexamplederivedanalytically.
- puzzle15,samuel,testsetcompletionJSONmissingattheendofreview; no measuredclaimsfor them.
- Primaryfulltextnotaccessibleforallhistoricalnumerics; explicitlimitedchecksabove.
- Runtimebudget/datarepairsalreadyreviewedare not fullPart2signoff.
