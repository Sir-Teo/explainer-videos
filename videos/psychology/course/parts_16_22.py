"""Act IV, Learning and Memory (Parts 16-22)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=16, level="U", widget="contingency",
        question="What, exactly, is learned when a signal comes to mean food?",
        story="Pavlov's dogs salivate to a signal paired with food; the response fades in extinction and part of it "
              "returns the next day. Thorndike's cats escape a puzzle box faster and faster, gradually: the law of "
              "effect. Watson builds behaviourism on it and conditions one infant to fear a white rat, a "
              "demonstration that grew in the retelling. Skinner's chamber records every response: shaping by "
              "successive approximation, and four schedules of reinforcement, each with its signature. Then the "
              "turn: Rescorla's random control shows that pairing teaches nothing without contingency, and Kamin's "
              "blocking that a paired cue teaches nothing when the outcome is already predicted. Rescorla and Wagner "
              "write surprise as one line, gradient descent on a squared prediction error, which predicts blocking, "
              "inhibition and overexpectation, and whose asymptote is the contingency itself. Its failures, latent "
              "inhibition, recovery and renewal, show that extinction is new learning bound to context; attention, "
              "time and choice extend it, and the matching law follows from melioration. Biology sets limits: taste "
              "goes with sickness, animals drift back to instinct, children learn by watching.",
        handoff="Prediction errors in dopamine neurons and temporal-difference learning are Part 17, learned attention "
                "Part 18, memory rewritten in use Part 21, choices over time Part 26, fear and exposure Part 40, "
                "addiction Part 41, and products built around habits Part 52.",
        outside="Part 2's experimental designs, Part 12's detection theory and Part 14's latent causes. Derivatives "
                "and the idea of a gradient; a little probability.",
        objectives={
            "U": ["Describe acquisition, extinction, spontaneous recovery, generalization and the four schedules.",
                  "Explain why contingency, not pairing, drives learning, and what blocking shows.",
                  "Explain why extinguished fears return, and what that means for exposure therapy."],
            "M": ["Derive the Rescorla-Wagner rule as gradient descent and run it on the classic designs.",
                  "Prove that its asymptote with a context cue is the contingency, delta P.",
                  "Derive the matching law from melioration, and show where melioration is a trap."],
            "D": ["Weigh associative against propositional and latent-cause accounts of human conditioning.",
                  "Assess the reliability of blocking and the evidence for reconsolidation."],
            "I": ["Explain how exposure therapy, contingency management and animal training use conditioning.",
                  "Recognize variable-ratio schedules in product design, and what the evidence on loot boxes shows."],
        },
        results=[
            ("Contingency", r"\Delta P = P(\text{US}\mid\text{CS}) - P(\text{US}\mid\neg\text{CS})"),
            ("Rescorla-Wagner", r"\Delta V_X = \alpha_X\beta\,\big(\lambda - \textstyle\sum_i V_i\big)"),
            ("As gradient descent", r"\Delta V = -\eta\,\nabla_V\,\tfrac12\big(\lambda - x^\top V\big)^2"),
            ("Its asymptote", r"V_X^\ast = \Delta P"),
            ("The matching law", r"\frac{B_L}{B_L + B_R} = \frac{R_L}{R_L + R_R}"),
            ("The I/T law", r"n_{\text{acq}} \approx 300\,(I/T)^{-1}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8, 11, 12, 13), D=(7, 9, 10, 15), I=(14,),
        also=(("Psyche's conditioning module", "explainer/psychology/psyche/conditioning.py"),
              ("Its tests", "tests/psychology/test_conditioning.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=17, level="U", widget="bandit",
        question="How does a brain learn what to do when the reward comes later?",
        story="A monkey's dopamine neurons fire at unannounced juice; after training they fire at the cue instead, and "
              "fall silent when promised juice is withheld. In 1997 those recordings were matched to the "
              "temporal-difference error of reinforcement learning, derived here from the Bellman equation: learn "
              "each prediction from the next one. On a delay line the error moves from reward to cue, and an "
              "artificial dopamine error, made with light, teaches as a real one does. The same error drives action: "
              "actor and critic, Q-learning, and the basal ganglia's Go and NoGo, tested in patients with "
              "Parkinson's disease. A bandit's learning rate can be read from choices, if parameter recovery says it "
              "can; directed exploration beats greedy choice. Tolman's rats learned maps without reward, and the "
              "brain has place and grid cells. Habits and plans are told apart by devaluation, the two-step task "
              "and revaluation, with the successor representation between them and replay offline. Dopamine also "
              "ramps, signals movement and encodes a distribution; a drug can fake its error; and the same "
              "mathematics runs recommender systems and the side effects of a medicine.",
        handoff="Attention is Part 18, memory and replay Part 21, decisions and risk Part 26, motivation Part 28, "
                "addiction Part 41, products built around habits Part 52, and the predictive brain Part 58.",
        outside="Part 16's Rescorla-Wagner rule and Part 11's maximum likelihood. Expected values, geometric sums "
                "and a little linear algebra.",
        objectives={
            "U": ["Describe Schultz's three dopamine recordings and what a reward prediction error is.",
                  "Explain the explore-exploit dilemma, latent learning, and the difference between habits and plans.",
                  "Explain why a drug that raises dopamine directly could hijack learning."],
            "M": ["Derive the TD error from the Bellman equation and run TD learning on a conditioning task.",
                  "Fit a Q-learning model to choices by maximum likelihood, and check it by parameter recovery.",
                  "Compute a successor matrix and predict reward and transition revaluation."],
            "D": ["Weigh the evidence that dopamine signals prediction errors against ramps and salience accounts.",
                  "Assess what the two-step task's mixture weight measures."],
            "I": ["Explain how bandit algorithms run recommendations and A/B tests.",
                  "Explain why dopamine agonists can cause impulse-control disorders."],
        },
        results=[
            ("Value", r"V(s_t) = \mathbb{E}\big[\textstyle\sum_k \gamma^k r_{t+k}\big]"),
            ("The TD error", r"\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)"),
            ("Q-learning", r"Q(s,a) \leftarrow Q(s,a) + \alpha\,[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]"),
            ("Softmax choice", r"P(a) \propto e^{\beta Q(a)}"),
            ("Successor representation", r"M = (I - \gamma T)^{-1},\ V = M r"),
        ],
        U=(0, 1, 3, 4, 5, 6, 7, 8, 11, 12), D=(2, 9, 10, 14), I=(13,),
        also=(("Psyche's rl module", "explainer/psychology/psyche/rl.py"),
              ("Its tests", "tests/psychology/test_rl.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=18, level="U", widget="search",
        question="Why do you miss a gorilla, and what were you doing instead?",
        story="Half of the observers counting basketball passes never see a gorilla walk through, and a large change "
              "in a flickering photograph can take ten seconds to find. Cherry's listeners repeat one ear and miss the "
              "other; Broadbent draws the first box-and-arrow diagram of a mind, with a filter. Your own name gets "
              "through, so Treisman turns the filter into an attenuator, others move selection late, and Lavie makes "
              "it depend on load. Posner's cue moves a spotlight without the eyes. A red item pops out and a red "
              "vertical one does not: feature integration, then guided search, a saliency map and selection history. "
              "What we attend decides what else we see, for radiologists too. In time there is a blink and a "
              "bottleneck; in the Stroop task, a word fights the ink and control fights back. Inside a neuron, "
              "attention is one multiplication before a division, which explains both contrast gain and response "
              "gain. Capacity is a race; vigilance decays; rare targets are missed; phones and media compete for the "
              "same channel.",
        handoff="Working memory is Part 19, perceptual decisions as evidence accumulation Part 25, self-control Part "
                "28, attention across the lifespan Part 31, human factors Part 51, design for and against attention "
                "Part 52, and attention in brains and machines Part 60.",
        outside="Part 1's stage models, Part 12's signal detection and Part 16's learned attention. Logistic and "
                "normal curves; a little algebra with fractions.",
        objectives={
            "U": ["Describe the gorilla, change blindness, Posner cueing, pop-out and the Stroop effect.",
                  "Explain early and late selection, attenuation and load theory.",
                  "Explain why a feature search is flat and a conjunction search is not."],
            "M": ["Derive the two-to-one slope ratio of serial search and the slope of minus one under a bottleneck.",
                  "Run guided search, the attentional blink and a Stroop diffusion, and read their signatures.",
                  "Derive contrast gain and response gain from the normalization model of attention."],
            "D": ["Weigh capacity-limit against strategic accounts of the blink and of load.",
                  "Assess the replication record of media multitasking and conflict adaptation."],
            "I": ["Explain prevalence effects and satisfaction of search in screening.",
                  "Explain why hands-free phones do not remove the driving cost, and what alarm fatigue is."],
        },
        results=[
            ("Serial search slopes", r"\text{present} = \tfrac{t}{2},\quad \text{absent} = t"),
            ("The PRP bottleneck", r"RT_2 = \max(\text{SOA} + A_2,\ A_1 + B_1) + B_2 + C_2 - \text{SOA}"),
            ("Normalization with attention", r"R = \frac{A\,E}{\text{pool}(A\,E) + \sigma}"),
            ("Bundesen's rate", r"v(x, i) = \eta(x, i)\,\beta_i\,\frac{w_x}{\sum_z w_z}"),
            ("Diffusion time", r"\mathbb{E}[T] = \frac{a}{v}\tanh(av)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13), D=(9, 10, 15), I=(14,),
        also=(("Psyche's attention module", "explainer/psychology/psyche/attention.py"),
              ("Its tests", "tests/psychology/test_attention.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=19, level="U", widget="change",
        question="How much can you hold in mind at once, and what is the limit made of?",
        story="George Miller was persecuted by an integer, seven, and showed that span counts chunks, not bits: "
              "recoded in threes, eighteen binary digits fit in six. Sperling's tone reveals a large visual store that "
              "fades in a second. Three consonants are forgotten in eighteen seconds, but not on the first trial: "
              "the cause is crowding by earlier memories, as a log-time model shows. Working memory becomes a system "
              "with a phonological loop that holds two seconds of speech. Sternberg's scanning is linear, and a "
              "parallel search with shared capacity draws the same line. Without rehearsal people hold about four "
              "items, counted by a formula that assumes slots; then continuous report shows precision falling "
              "smoothly with load, and four models fitted to seven thousand open trials pick variable precision. A "
              "ring of neurons holds a bump that diffuses. Working memory tracks reasoning, and an industry promised "
              "to raise both; against a placebo control, the far transfer is not there.",
        handoff="Long-term memory is Parts 20 and 21, the lifespan and ADHD Parts 31 and 41, intelligence Part 32, "
                "model recovery Part 48, read-backs and cognitive load Parts 51 and 54, the limit as an efficient code "
                "Part 58, and small workspaces against large contexts Part 60.",
        outside="Part 1's reaction-time stages, Part 3's reliability and attenuation, Part 12's hits and false alarms "
                "and Part 18's attention. Exponentials, logarithms, and maximum likelihood as in Part 16.",
        objectives={
            "U": ["Explain span, chunks and recoding, and why span overestimates capacity.",
                  "Describe partial report, the Brown-Peterson task and the multicomponent model.",
                  "Explain the word-length effect and articulatory suppression."],
            "M": ["Derive Cowan's and Pashler's K from a slot model with guessing.",
                  "Show that limited-capacity parallel search mimics serial exhaustive search.",
                  "Fit mixture, swap and process models to continuous-report data and compare them by AIC."],
            "D": ["Weigh slots against variable precision, and persistent against silent codes.",
                  "Explain why a mixture model's guess rate need not measure guessing."],
            "I": ["Design forms, codes and read-backs around a four-chunk limit.",
                  "Evaluate a brain-training claim: the control group, near and far transfer."],
        },
        results=[
            ("Cowan's K", r"K = N\,(H - F)"),
            ("Precision of a von Mises", r"J = \kappa\,\frac{I_1(\kappa)}{I_0(\kappa)}"),
            ("SIMPLE's discriminability", r"D_i = \Big(\sum_j e^{-c\,|\log T_i - \log T_j|}\Big)^{-1}"),
            ("Variable precision", r"J \sim \text{Gamma}\big(\text{mean } J_1 N^{-\alpha},\ \text{scale } \tau\big)"),
            ("A shared information budget", r"\sigma_N = \sigma_1\,2^{\,R - R/N}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 9, 10, 11), D=(7, 8, 13), I=(12,),
        also=(("Psyche's working-memory module", "explainer/psychology/psyche/wm.py"),
              ("Its tests", "tests/psychology/test_wm.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=20, level="U", widget="recall",
        question="When you remember, what is being searched, and with what?",
        story="In 1885 Hermann Ebbinghaus, his own only subject, learns invented syllables and measures what remains "
              "by the time saved relearning them; three laws fitted to his seven numbers show forgetting fast and "
              "then ever slower, like the odds that a memory will be needed. Free recall of 3,528 open lists shows "
              "primacy, recency, a start at the end, and contiguity that leans forward, in almost every person. What "
              "is done at study and the match at test decide what comes back; the famous underwater context effect "
              "did not replicate in sixteen divers whose data are open. SAM's rehearsal buffer gives both ends of the "
              "curve but symmetric contiguity; a slowly drifting context, derived step by step and fitted by maximum "
              "likelihood, gives recency, contiguity and its forward lean, predicts each next word far better than "
              "position alone, explains why a delay ends recency, and fails the continual-distractor test that shows "
              "what it lacks. A Hopfield network completes a memory from a fragment, up to about 0.14 memories per "
              "unit. Amnesia separates systems of memory, recognition splits into familiarity and recollection, and "
              "the hippocampus indexes and separates.",
        handoff="Forgetting, consolidation and false memories are Part 21, semantic memory Part 22, the lifespan Part "
                "31, model fitting and comparison Part 48, spacing and testing Part 54, witnesses and interviews Part "
                "56, and memory in machines Part 60.",
        outside="Part 12's ROCs and z-ROCs, Part 19's SIMPLE and choice rule, and Part 5's Hebbian learning. Vectors "
                "and dot products, logarithms, and maximum likelihood as in Parts 16 and 19.",
        objectives={
            "U": ["Describe savings, the serial-position curve, contiguity, levels of processing and encoding "
                  "specificity.",
                  "Explain what Glanzer and Cunitz's and Bjork and Whitten's experiments show about recency.",
                  "Describe H.M., the memory-systems taxonomy, and recognition by familiarity and recollection."],
            "M": ["Compute a lag-CRP with its denominators, and the serial-position and first-recall curves.",
                  "Derive the drift of context and the similarity of contexts at lag k.",
                  "Fit the context model by maximum likelihood and compare it with a baseline on held-out data."],
            "D": ["Weigh buffer models against context models, and one memory system against many.",
                  "Derive a Hopfield network's energy argument and the crosstalk that limits its capacity."],
            "I": ["Design a recall question or an interview around cues, context and landmarks.",
                  "Read a word-list test's learning curve, delayed recall and recognition in the clinic."],
        },
        results=[
            ("Savings", r"\text{savings} = \frac{T_{\text{first}} - T_{\text{again}}}{T_{\text{first}}}"),
            ("Lag-CRP", r"\text{CRP}(\ell) = \frac{\#\,\text{transitions of lag } \ell}{\#\,\text{times lag } "
                        r"\ell \text{ was possible}}"),
            ("The drift of context", r"\mathbf{c}_i = \rho_i\,\mathbf{c}_{i-1} + \beta\,\mathbf{c}^{\text{IN}}_i"),
            ("Context similarity", r"\mathbf{c}_i \cdot \mathbf{c}_j \approx \rho^{\,|i-j|}, \quad "
                                   r"\rho = \sqrt{1 - \beta^2}"),
            ("ACT-R's activation", r"B = \ln \sum_j t_j^{-d}"),
            ("Hopfield's rule and energy", r"W = \tfrac{1}{N}\sum_\mu \xi^\mu \xi^{\mu\top}, \quad "
                                           r"E = -\tfrac{1}{2}\,\mathbf{s}^\top W \mathbf{s}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 10, 11, 13), D=(6, 7, 8, 9, 12, 15), I=(14,),
        also=(("Psyche's memory module", "explainer/psychology/psyche/memory.py"),
              ("Its tests", "tests/psychology/test_memory.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=21, level="U", widget="drm",
        question="Why do we forget, and why do we remember things that never happened?",
        story="In 1974 one word in a question, smashed or hit, changes how fast people say two cars were going, and "
              "a week later those who heard smashed remember broken glass that was never there. Ebbinghaus's curve, "
              "repeated by three people up to 2015, is fast and then slow; a power law fits it best, with a warning "
              "that averaged exponentials make power laws too. Much forgetting is interference, from earlier lists, "
              "later lists, and even from remembering. Memories consolidate from hippocampus to cortex, helped by "
              "sleep's replay, and reopen when recalled; a fast learner and a slow one joined by replay can learn the "
              "penguin without losing the robin. Spacing and testing are the two best ways to remember more, each "
              "with a model fitted to a landmark study. Recall blends a trace with a schema, biased and more "
              "accurate on average; a memory that sums similar experiences recognises a word that was never shown; "
              "suggestion implants whole events in a minority; verbal overshadowing, replicated by 53 sets of labs, "
              "is real and smaller than first reported. A witness's first confidence, under good procedures, is "
              "strong evidence; their later confidence is not.",
        handoff="Concepts and categories, and the penguin again, are Part 22, the lifespan Part 31, fear and trauma "
                "Part 40, model comparison Part 48, the science of learning Part 54, line-ups and the courtroom Part "
                "56, and forgetting in machines Part 60.",
        outside="Part 12's signal detection, Part 14's cue combination, Part 17's replay and Part 20's ACT-R, "
                "Hopfield network and context model. Logarithms and power laws, least squares, and a little "
                "probability (the gamma distribution, the normal).",
        objectives={
            "U": ["Describe the forgetting curve, decay and interference, consolidation and reconsolidation.",
                  "Explain the spacing and testing effects and why students prefer re-reading.",
                  "Describe Bartlett's schemas, the DRM illusion, misinformation and implanted memories."],
            "M": ["Fit four forgetting laws and compare them by AIC; derive Jost's law from the hazard.",
                  "Show that a gamma mixture of exponentials is a power function.",
                  "Fit the bifurcation model to the testing effect, and derive the category adjustment model's weight."],
            "D": ["Explain catastrophic interference and the complementary-learning-systems answer to it.",
                  "Derive the confidence-accuracy characteristic of a line-up from signal detection."],
            "I": ["Design a study schedule from the spacing ridgeline, and fit half-life regression to practice data.",
                  "Specify a line-up and interview procedure that keeps memory evidence uncontaminated."],
        },
        results=[
            ("The power law's hazard", r"S = a\,t^{-b} \;\Rightarrow\; -\frac{d \ln S}{dt} = \frac{b}{t}"),
            ("Averaged exponentials", r"E_{\lambda \sim \Gamma(k, \theta)}\, e^{-\lambda t} = (1 + \theta t)^{-k}"),
            ("Two stores", r"c(t) = \frac{k}{a - b}\big(e^{-bt} - e^{-at}\big)"),
            ("Pavlik and Anderson's decay", r"d_j = c\, e^{m(t_j)} + a"),
            ("Category adjustment", r"\hat{x} = \lambda y + (1 - \lambda)\rho, \quad "
                                    r"\lambda = \frac{\sigma_c^2}{\sigma_c^2 + \sigma_y^2}"),
            ("Half-life regression", r"p = 2^{-\Delta/h}, \quad h = 2^{\boldsymbol\theta \cdot \mathbf{x}}"),
        ],
        U=(0, 2, 3, 6, 8, 9, 11, 12), D=(1, 4, 5, 7, 10, 14), I=(13,),
        also=(("Psyche's memory module", "explainer/psychology/psyche/memory.py"),
              ("Its tests", "tests/psychology/test_forget.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=22, level="U", widget="numbers",
        question="What do you know when you know what a bird is?",
        story="Is a penguin a bird? Everyone says yes, and everyone is slower to say it than for a robin. Aristotle's "
              "definitions fail for birds and games alike; membership is graded and its edges unstable. Two "
              "equations replace definitions: a prototype, recognised though never seen, and a memory of every "
              "member, whose summed similarity wins the 5-4 structure. Shepard, Hovland and Jenkins's six problems, "
              "refitted on the 1994 open data, need an attention that learns. Scaling turns Ekman's colour ratings "
              "into Newton's colour circle and Rothkopf's Morse confusions into a map, and in that map Shepard's "
              "law holds: generalization falls exponentially, as it must for a mind unsure how far a consequence "
              "extends. Tversky shows similarity is not distance, and his count of asymmetries is rerun on the open "
              "table. Knowledge is a network, not a tree; priming through it is real and small. Concepts are "
              "theories, as the pizza and the raccoon show; three examples can teach one by the size principle; and "
              "Jane Austen's words, placed by the company they keep, find their meanings and their opposites.",
        handoff="Language is Part 23, essences in the infant mind Part 30, categories against dimensions in "
                "diagnosis Part 39, scaling Part 46, model mimicry Part 48, design for minds Part 52, and the "
                "geometry of machine embeddings Part 60.",
        outside="Part 11's psychophysical scales, Part 13's opponent channels, Part 16's delta rule, Part 18's "
                "attention weights and Part 21's semantic network. Distances, eigenvectors, the SVD, Bayes' rule and "
                "a little integration.",
        objectives={
            "U": ["Explain why few everyday concepts have definitions, and what typicality and family resemblance are.",
                  "Contrast prototype and exemplar accounts, and describe the basic level.",
                  "Describe semantic networks, spreading activation and semantic priming."],
            "M": ["Derive the generalized context model and fit exemplar, prototype and ALCOVE models to data.",
                  "Derive classical multidimensional scaling and run its non-metric version.",
                  "Derive Shepard's exponential law from consequential regions and Tversky's contrast asymmetry."],
            "D": ["Compute a Bayesian concept learner's posterior with the size principle.",
                  "Build word vectors from co-occurrence by PPMI and the SVD, and compare spaces by RSA."],
            "I": ["Run and analyse a card sort to design a navigation scheme.",
                  "Explain why a polythetic diagnosis admits hundreds of symptom profiles."],
        },
        results=[
            ("The generalized context model", r"P(A \mid x) = \frac{\beta_A \sum_{a \in A} e^{-c\, d(x, a)}}"
                                              r"{\sum_K \beta_K \sum_{k \in K} e^{-c\, d(x, k)}}"),
            ("Classical scaling", r"B = -\tfrac{1}{2} J D^{(2)} J = X X^\top"),
            ("Shepard's law", r"g(d) = \int_0^\infty s e^{-s} \max(0, 1 - d/s)\, ds = e^{-d}"),
            ("The contrast model", r"S(a, b) = \theta f(A \cap B) - \alpha f(A - B) - \beta f(B - A)"),
            ("The size principle", r"p(X \mid h) = |h|^{-n} \ \text{for } X \subset h"),
            ("Category utility", r"\mathrm{CU}(c) = P(c) \sum_k \big[P(f_k \mid c)^2 - P(f_k)^2\big]"),
        ],
        U=(0, 1, 2, 3, 8, 12), D=(4, 5, 6, 7, 9, 10, 11, 14), I=(13,),
        also=(("Psyche's concepts module", "explainer/psychology/psyche/concepts.py"),
              ("Its tests", "tests/psychology/test_concepts.py"),
              ("The R data reader", "explainer/psychology/rdata.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
]
