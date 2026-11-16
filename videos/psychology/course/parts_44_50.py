"""Psychology, Built as a course: Parts 44 to 50 (Act XI, the graduate toolkit)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=44, level="M", widget="diagrams", prereq=(3, 32, 43),
        question="How do you model something you cannot observe, and how do you know the model is not a fiction?",
        story="In 1921 Sewall Wright drew arrows between variables and showed how correlations follow from them; in "
              "1969 Karl Jöreskog joined his paths to Spearman's factors, and the structural equation model became "
              "psychology's way to state a theory about unobservables. The part derives the tracing rule, builds and "
              "identifies the factor model, fits Holzinger and Swineford's nine tests by maximum likelihood (checked "
              "against lavaan), judges fit and shows fixed cut-offs passing a wrong model, undoes attenuation, tests "
              "invariance across two schools, finds a significant indirect effect that is not there, shows that "
              "equivalent diagrams fit identically, that a cross-lagged panel confuses stable people with change, and "
              "that a factor and a network can imply the same covariances, and ends with eight questions for reading "
              "an SEM paper.",
        handoff="Item response theory is Part 45; within-person models over time Part 47; models of behaviour Part 48; "
                "the weight of evidence Part 50.",
        outside="Part 3's reliability, Part 32's factor analysis and Part 43's workflow; matrices, the normal "
                "likelihood and least squares.",
        objectives={
            "U": ["Read a path diagram: latent and observed variables, loadings, errors, and what an arrow claims.",
                  "Explain why a good fit does not show that the arrows point the right way."],
            "M": ["Derive model-implied correlations by the tracing rule and as Σ = ΛΦΛᵀ + Θ; count parameters to check "
                  "identification, and fit a confirmatory factor model by maximum likelihood.",
                  "Compute χ², RMSEA, CFI and SRMR, and test configural, metric and scalar invariance.",
                  "Simulate a confounded mediator and show the product-of-coefficients estimate is biased."],
            "D": ["Say what causal discovery can orient from conditional independences, and what its assumptions "
                  "demand of psychological data."],
            "I": ["Audit a survey or people-analytics model by asking which equivalent diagram fits as well, and "
                  "whether the score is comparable across groups."],
        },
        results=[
            ("Tracing rule", r"\rho_{XY} = \sum_{\text{paths}} \prod \text{path coefficients}"),
            ("Factor model", r"\Sigma = \Lambda \Phi \Lambda^\top + \Theta"),
            ("ML discrepancy", r"F = \log|\Sigma| + \operatorname{tr}(S\Sigma^{-1}) - \log|S| - p, \quad T = nF"),
            ("RMSEA", r"\sqrt{\max(T - df, 0)/(df\, n)}"),
            ("Attenuation", r"r_{\text{true}} = r_{xy}/\sqrt{r_{xx} r_{yy}}"),
        ],
        U=(0, 1, 9, 12), D=(15,), I=(14,),
        also=(("Psyche's sem module", "explainer/psychology/psyche/sem.py"),
              ("Its tests", "tests/psychology/test_sem.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=45, level="M", widget="adaptive", prereq=(3, 12, 44),
        question="How can two people who took different questions be put on the same scale?",
        story="In the 1950s the Danish mathematician Georg Rasch was asked to compare reading across tests that share "
              "no items. Classical scores cannot do it: difficulty depends on the sample and scores on the test. Rasch "
              "modelled the single encounter of one person with one item, and person and item separate. The part "
              "derives the model's specific objectivity and the sufficiency of the sum score, adds discrimination and "
              "guessing, measures information, fits the Law School Admission Test's items by marginal maximum "
              "likelihood (matching the published fits), builds an adaptive test that needs about half the items of "
              "the best fixed form, fits graded responses to attitude items, separates bias from impact with "
              "Mantel and Haenszel, links two forms through anchors, shows why national surveys report plausible "
              "values drawn from a conditioning model, and tracks learning with knowledge tracing and Elo.",
        handoff="What happens between a question and its answer is Part 46; ability and learning over time Part 47; "
                "response-time models Part 48; the weight of evidence Part 50.",
        outside="Part 3's classical test theory, Part 12's logistic functions and Part 44's latent variables; the "
                "logistic function, likelihood and Fisher information.",
        objectives={
            "U": ["Explain why a classical score depends on the test and an item's difficulty on the sample.",
                  "Read an item characteristic curve: difficulty, discrimination and guessing.",
                  "Say why a group gap on an item is not by itself evidence that the item is unfair."],
            "M": ["Derive the sufficiency of the sum score in the Rasch model and fit it by conditional ML.",
                  "Fit Rasch and two-parameter models by marginal ML with EM; compute item and test information, and "
                  "build an adaptive test.",
                  "Run a Mantel-Haenszel DIF analysis, a mean-sigma linking and a plausible-value analysis."],
            "D": ["Argue how response times, generated items or learning test-takers change what a calibrated scale "
                  "can claim."],
            "I": ["Plan an adaptive questionnaire: bank, stopping rule, exposure control and a DIF check."],
        },
        results=[
            ("Rasch model", r"P(X_{pi} = 1) = \frac{e^{\theta_p - b_i}}{1 + e^{\theta_p - b_i}}"),
            ("Sufficiency", r"P(\mathbf{x} \mid r) = e^{-\sum_i x_i b_i} / \gamma_r(e^{-b_1}, \dots, e^{-b_k})"),
            ("Item information", r"I_i(\theta) = a_i^2 P_i(\theta)(1 - P_i(\theta))"),
            ("Mantel-Haenszel", r"\hat\alpha_{MH} = \frac{\sum_s A_s D_s/N_s}{\sum_s B_s C_s/N_s}, \ \Delta = -2.35 \ln \hat\alpha_{MH}"),
            ("Mean-sigma linking", r"A = \mathrm{SD}(b^{old})/\mathrm{SD}(b^{new}), \ B = \bar b^{old} - A \bar b^{new}"),
        ],
        U=(0, 1, 2, 3, 9), D=(15,), I=(14,),
        also=(("Psyche's irt module", "explainer/psychology/psyche/irt.py"),
              ("Its tests", "tests/psychology/test_irt.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=46, level="M", widget="pairs", prereq=(12, 26, 45),
        question="How do you turn \"I prefer this one\" into a number, and what happens between a question and its "
                 "answer?",
        story="In 1927 Louis Thurstone asked students which of two offences was worse, for every pair, and derived a "
              "scale from their inconsistencies. Luce replaced his normal curves with one axiom; McFadden made the "
              "logit a forecasting tool. The part fits Case V and Bradley-Terry to Guilford's vegetables, derives the "
              "logit from Gumbel noise, breaks the axiom with a red bus and a blue bus, builds the decoy and compromise "
              "effects from one comparing chooser, recovers part-worths in a conjoint study, follows a survey answer "
              "through Tourangeau's four steps, shows acquiescence and careless responding manufacturing "
              "correlations, and puts an error bar on the net promoter score.",
        handoff="People over time are Part 47; fitting and comparing models of behaviour Part 48; language models as "
                "respondents Part 60.",
        outside="Part 12's signal detection, Part 26's choice models and Part 45's graded responses; the normal and "
                "logistic distributions, and maximum likelihood.",
        objectives={
            "U": ["Explain how paired comparisons give a scale, and why inconsistency is information.",
                  "Describe the decoy and compromise effects, and why they break Luce's axiom.",
                  "Name the four steps of answering a survey question and an error at each."],
            "M": ["Derive Case V from two normal impressions and fit it; fit Bradley-Terry by the MM algorithm.",
                  "Show by simulation that Gumbel random utility gives the logit, and recover part-worths and "
                  "willingness to pay from a simulated conjoint study.",
                  "Show how acquiescence and straightlining distort correlations, and how balanced keys help."],
            "D": ["Argue what a model of context effects must explain, and design a test of its prediction about "
                  "deliberation time."],
            "I": ["Plan a conjoint or a survey: design, wording experiments, data-quality rules and reported "
                  "uncertainty."],
        },
        results=[
            ("Case V", r"P(j \succ i) = \Phi\big((s_j - s_i)/(\sigma\sqrt{2})\big)"),
            ("Luce's axiom", r"P(i \mid M) = v_i / \textstyle\sum_{k \in M} v_k"),
            ("MM update", r"v_i \leftarrow w_i / \textstyle\sum_j n_{ij}/(v_i + v_j)"),
            ("Logit from Gumbel noise", r"P(j) = e^{V_j} / \textstyle\sum_k e^{V_k}"),
            ("Willingness to pay", r"\mathrm{WTP}_k = -\beta_k / \beta_{\text{price}}"),
        ],
        U=(0, 1, 5, 8, 9), D=(15,), I=(14,),
        also=(("Psyche's scaling module", "explainer/psychology/psyche/scaling.py"),
              ("Its tests", "tests/psychology/test_scaling.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=47, level="M", widget="withinbetween", prereq=(31, 44, 46),
        question="When is a finding about people a finding about a person?",
        story="In 1973 Herbert Clark showed that a generation of language studies tested generalization to new people "
              "but not to new words. The part simulates his fallacy (half of null studies significant), builds "
              "multilevel models and partial pooling, crosses participants with items and plans the number of "
              "stimuli, then turns to the deeper point: Simpson's paradox inside a person and person-mean centring, "
              "a non-ergodic population whose group correlation describes almost no one, experience sampling and the "
              "bias of inertia, cause over time, and critical slowing down before a tipping point, with the false "
              "alarms that noisy diaries bring.",
        handoff="Models of behaviour fitted person by person are Part 48; the brain's data with subjects and voxels "
                "Part 49; the weight of evidence Part 50; computational psychiatry Part 59.",
        outside="Part 31's growth curves and Part 44's latent variables; regression, variance components and "
                "autoregression.",
        objectives={
            "U": ["Explain why stimuli must be treated as a sample, and what goes wrong when they are not.",
                  "Recognize when a relation across people differs from the relation within a person."],
            "M": ["Fit a multilevel model with random slopes, and explain partial pooling.",
                  "Compute min F', plan the number of stimuli, and separate within- and between-person effects by "
                  "person-mean centring.",
                  "Estimate inertia from diary data and correct for its small-sample bias."],
            "D": ["Argue which psychological processes could be ergodic, and design a test of critical slowing down "
                  "that controls false alarms."],
            "I": ["Audit a product or health metric for whether it describes users or a user."],
        },
        results=[
            ("Multilevel model", r"y_{pt} = (\alpha + u_p) + (\beta + v_p) x_{pt} + \varepsilon_{pt}"),
            ("min F'", r"\min F' = F_1 F_2 / (F_1 + F_2)"),
            ("Within and between", r"y_{pt} = \beta_W (x_{pt} - \bar x_p) + \beta_B \bar x_p + \dots"),
            ("Inertia's bias", r"E[\hat\phi] \approx \phi - (1 + 3\phi)/T"),
        ],
        U=(0, 1, 5, 7, 8), D=(15,), I=(14,),
        also=(("Psyche's within module", "explainer/psychology/psyche/within.py"),
              ("Its tests", "tests/psychology/test_within.py"),
              ("statkit's mixed models", "explainer/stats/kit/mixed.py")),
    ),
    Part(
        n=48, level="M", widget="fitme", prereq=(17, 25, 47),
        question="When is a computational model of the mind more than a curve fit?",
        story="In 1956 William Estes showed that a smooth learning curve can be the average of learners who each "
              "learned in one jump. The part opens the fitting harness the whole series has used: four generative "
              "models of a reversal bandit, maximum likelihood with restarts, parameter recovery and the ridge where "
              "learning rate and inverse temperature trade off, model comparison and model recovery, a posterior "
              "predictive check that catches a missing mechanism, people fitted as a population, and the power law "
              "of practice unmasked as an average; then rational analysis, connectionism and language models given "
              "the Battery.",
        handoff="The brain's data, with subjects and voxels, are Part 49; the weight of evidence Part 50; "
                "computational psychiatry and its parameters Part 59; whether a language model is a model of a mind "
                "Part 60.",
        outside="Part 17's Q-learner and Part 25's diffusion model; likelihood, AIC and BIC, and shrinkage.",
        objectives={
            "U": ["Explain what a cognitive model is: a program that turns parameters into trial-by-trial behaviour.",
                  "Explain why an average curve can misdescribe every individual in it."],
            "M": ["Fit a learning model by maximum likelihood with several starting points, and show parameter "
                  "recovery for the number of trials collected.",
                  "Compare models by BIC or cross-validation, and check the comparison by model recovery.",
                  "Run a posterior predictive check on a qualitative effect such as staying after a loss."],
            "D": ["Design the full set of checks for a new model of a new task before collecting data."],
            "I": ["Judge whether a parameter fitted to users or patients is reliable enough to act on."],
        },
        results=[
            ("Softmax choice", r"P(a) = e^{\beta Q_a} / \sum_b e^{\beta Q_b}"),
            ("Q-learning", r"Q_a \leftarrow Q_a + \alpha (r - Q_a)"),
            ("BIC", r"\mathrm{BIC} = -2 \ln \hat L + k \ln n"),
            ("Shrinkage", r"\hat\theta_p = \frac{\hat\theta_p^{\text{own}} / v_p + \mu / \tau^2}{1 / v_p + 1 / \tau^2}"),
        ],
        U=(0, 1, 2, 9), D=(15,), I=(14,),
        also=(("Psyche's fit module", "explainer/psychology/psyche/fit.py"),
              ("Its tests", "tests/psychology/test_fit.py"),
              ("Part 17's Q-learner", "explainer/psychology/psyche/rl.py")),
    ),
    Part(
        n=49, level="D", widget="pipelines", prereq=(8, 47, 48),
        question="What must be true for a brain map to be evidence?",
        story="In 2020 seventy teams analysed one brain-imaging dataset and answered the same questions differently. "
              "The part builds the analysis chain on a synthetic brain where the truth is known: 72 pipelines and 44 "
              "different maps, head motion that makes connections, fixed effects that treat scans as people, cluster "
              "inference that fails at lenient thresholds and permutation that does not, a decoder that reads noise "
              "at 94% when it peeks, representational geometry and encoding models judged against noise ceilings, "
              "anticorrelations made by global-signal regression, ERP windows chosen from the answer, the population "
              "vector, brain-computer interfaces and their bit rates, and the samples of thousands that "
              "brain-behaviour claims need.",
        handoff="Reading a whole literature is Part 50; the predictive brain Part 58; computational psychiatry's "
                "biomarkers Part 59; brains and machines compared Part 60.",
        outside="Part 8's measurement chain; Part 47's multilevel models; permutation tests, ridge regression and "
                "principal components.",
        objectives={
            "U": ["Explain why one dataset analysed through many defensible pipelines can give different answers.",
                  "Explain why a brain-behaviour correlation from a few dozen people is usually inflated."],
            "M": ["Fit a two-level model of brain data and threshold it by permutation, and explain when cluster "
                  "inference fails.",
                  "Cross-validate a decoder with every selection step inside the loop, and compare a model with "
                  "brain data by representational similarity against a noise ceiling."],
            "D": ["Plan a brain-behaviour study from the smallest effect of interest, the measures' reliabilities "
                  "and a registered pipeline."],
            "I": ["Audit a claim made for a neurotechnology product or a brain-based biomarker."],
        },
        results=[
            ("Random-effects t", r"t_v = \bar c_v \big/ (s_v/\sqrt{n})"),
            ("Permutation threshold", r"u = q_{0.95}\big(\max_v t_v^{(\pi)}\big)"),
            ("Attenuation", r"r_{\text{obs}} = r\sqrt{\rho_{x}\rho_{y}}"),
            ("Wolpaw's bit rate", r"B = \log_2 N + P\log_2 P + (1-P)\log_2\tfrac{1-P}{N-1}"),
        ],
        U=(0, 1, 5, 12), D=(15,), I=(14,),
        also=(("Psyche's neurodata module", "explainer/psychology/psyche/neurodata.py"),
              ("Its tests", "tests/psychology/test_neurodata.py"),
              ("Part 8's synthetic brain", "explainer/psychology/psyche/imaging.py")),
    ),
]
