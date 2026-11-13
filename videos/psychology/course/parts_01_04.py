"""Act I, Asking a Mind a Question (Parts 1-4)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="reactiontime",
        question="Can a mind be measured, and what would it take to explain one?",
        story="The part opens in 1786 with Kant's three reasons why psychology can never be a science: mathematics "
              "does not apply to the inner sense, the mind cannot be taken apart and recombined, and observing a "
              "mental state changes it. It keeps score against them. The viewer's own simple and choice reactions "
              "come first, then Helmholtz's 1850 measurement of the speed of a nerve signal, 25 to 43 metres a "
              "second in a frog, and the fifteen-year dispute over the human value that ended by finding "
              "temperature. Donders subtracts a simple reaction from a go/no-go and a go/no-go from a choice, and "
              "gives discrimination 36 ms and choice 47 ms; the part builds his reasoning as a chain of stages, the "
              "first model of the series, and then turns on it: a rival model has the same three means, and only "
              "the distributions can test whether a stage was purely inserted. Fechner's logarithm and "
              "Ebbinghaus's forgetting data follow, then the stalemate of introspection, the behaviourists' ban on "
              "the mind, and its return in 1956 with maps, plans and bits. It ends with Marr's three levels, the "
              "homunculus that an explanation must get rid of, and the four devices of the series.",
        handoff="Fechner's law is tested on your own threshold in Part 11, and the threshold is replaced by signal "
                "detection in Part 12. Donders' subtraction returns as the logic of brain imaging in Part 8 and "
                "additive factors as memory scanning in Part 19; Ebbinghaus's curve is taken apart in Parts 20 and "
                "21. The shape of a reaction-time distribution and Hick's law are derived in Part 25. Kant's "
                "third objection is the subject of Parts 2 and 4, and the Ledger opened here gains rows in every "
                "part.",
        outside="Nothing beyond school arithmetic for most chapters. Chapter 4 uses the mean and variance of a sum "
                "of independent random variables.",
        objectives={
            "U": ["State Kant's three objections to a science of the mind, and say which early measurement "
                  "answers each and which is still open.",
                  "Compute a conduction speed from two stimulation sites, and Donders' two stage durations from "
                  "his three mean reaction times.",
                  "Describe an explanation at Marr's three levels, and say why a homunculus explains nothing."],
            "M": ["Write a reaction time as a sum of independent stage durations, and derive what pure insertion "
                  "implies for its mean, its variance and its distribution.",
                  "Use additive-factor logic to decide from a table of mean reaction times whether two factors "
                  "act on the same stage."],
            "D": ["Explain why three mean reaction times cannot identify the stages that produced them, and "
                  "state a distributional test that can refute pure insertion.",
                  "Say how a cascade of continuous processes can mimic additive effects, and what data would "
                  "separate it from discrete stages."],
            "I": ["Report a timing result as a difference between conditions, and say what a constant device "
                  "delay changes and what it leaves alone.",
                  "Ask of any reaction-time claim what the number includes and which apparatus measured it."],
        },
        results=[
            ("Conduction speed", r"v=\frac{\Delta x}{\Delta t},\qquad \frac{0.050\ \text{m}}{0.0020\ \text{s}}"
                                 r"=25\ \text{m/s}"),
            ("Donders' subtraction", r"T_{\text{discriminate}}=\text{RT}_c-\text{RT}_a,\qquad "
                                     r"T_{\text{choose}}=\text{RT}_b-\text{RT}_c"),
            ("Pure insertion", r"\text{RT}_c=\text{RT}_a+D\ \Rightarrow\ \operatorname{Var}[\text{RT}_c]"
                               r"=\operatorname{Var}[\text{RT}_a]+\operatorname{Var}[D]"),
            ("Additive factors", r"\overline{\text{RT}}_{11}-\overline{\text{RT}}_{10}-\overline{\text{RT}}_{01}"
                                 r"+\overline{\text{RT}}_{00}=0\ \ \text{for different stages}"),
            ("Fechner's law", r"\frac{\Delta I}{I}=k\ \ \Rightarrow\ \ S=\frac{1}{k}\ln\frac{I}{I_0}"),
            ("Hick's law", r"\text{RT}=a+b\log_2 n"),
        ],
        U=(0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("psyche.chronometry", "explainer/psychology/psyche/chronometry.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=2, level="U", widget="berandom",
        question="How do you ask a mind a question without telling it the answer?",
        story="Berlin, 1904: a horse named Hans answers arithmetic with his hoof, and a commission of thirteen, a "
              "circus manager and the director of the Psychological Institute among them, finds no trick. A "
              "student, Oskar Pfungst, changes one thing at a time and counts. Hans is right 98 times in 100 when "
              "the questioner knows the answer and 8 in 100 when he does not; 89 in 100 when he can see the "
              "questioner and 6 when he cannot. The questioners were giving the answer away with a movement of the "
              "head of about a millimetre, and 23 of 25 people did the same for Pfungst in the laboratory. The part "
              "builds the rules of design from that story. A game that does nothing is studied on the Pool by one "
              "group tested twice, and appears to work; a control group shows why. Campbell and Stanley's six "
              "unsound designs each find an effect where the truth is zero. Peirce and Jastrow's shuffled deck of "
              "1884, the first randomized experiment, balances even what nobody measured and supplies its own "
              "test. Each person serving as their own control buys precision, if the order is counterbalanced. "
              "Expectations leak from experimenters to rats, pupils and police dogs, and from subjects who want "
              "to help; the blind is the remedy. The part ends with interactions and their dependence on scale, "
              "four kinds of validity, who gets studied, and the rules that protect the people in an experiment.",
        handoff="What a measurement measures is Part 3, and the analyst as the last unblinded observer is Part 4, "
                "where the randomization test returns. The curve fitted to Hans's eyesight is the psychometric "
                "function of Part 11, and false alarms are Part 12. Milgram's study is examined in Part 34, the "
                "reach of findings beyond Western samples in Part 38, placebo-controlled trials of therapy in "
                "Part 42, and a many-laboratory replication in Part 43. Every later part runs its designs through "
                "the laboratory built here.",
        outside="Means, standard deviations and the idea of a sampling distribution. The power calculations of "
                "chapter 6 use the normal curve.",
        objectives={
            "U": ["Explain what Pfungst varied, what he found, and why a blind removes the effect.",
                  "Name the six classical threats to a before-and-after study, and the change of design that "
                  "answers each.",
                  "Say what random assignment balances that matching cannot, and why people cannot do the "
                  "randomizing themselves."],
            "M": ["Derive the standard deviation of the difference between two randomized groups, and the number "
                  "of people a between-person and a within-person design need for a given power.",
                  "Carry out a randomization test, and construct a Williams square for four conditions.",
                  "Show by example that an interaction can be removed by a change of scale, and say which "
                  "interactions cannot."],
            "D": ["Separate a treatment's effect from the effect of knowing one's assignment, and state what each "
                  "available design assumes.",
                  "Say what a measurement of demand effects licenses, and what it does not."],
            "I": ["Ask of any study: compared with what, who decided who got what, who knew, who dropped out, and "
                  "who was studied.",
                  "Recognize an A/B test, a clinical trial and a counterbalanced user study as the designs of "
                  "this part, and name the analysis that answers attrition."],
        },
        results=[
            ("Balance after a shuffle", r"\operatorname{SD}\!\left[\bar x_1-\bar x_0\right]"
                                        r"=\sigma\sqrt{\tfrac{1}{n_1}+\tfrac{1}{n_0}}=\frac{2\sigma}{\sqrt n}"),
            ("People needed, two groups", r"n_{\text{per group}}=2\left(\frac{z_{1-\alpha/2}+z_{1-\beta}}{d}"
                                          r"\right)^{2}"),
            ("People needed, each both ways", r"n=2(1-\rho)\left(\frac{z_{1-\alpha/2}+z_{1-\beta}}{d}"
                                              r"\right)^{2}"),
            ("Randomization test", r"p=\Pr\nolimits_{\text{shuffles}}\!\left(|\bar y_1-\bar y_0|\ge "
                                   r"|\text{observed}|\right)"),
            ("Interaction contrast", r"(\bar y_{11}-\bar y_{10})-(\bar y_{01}-\bar y_{00})"),
            ("A cue read at a distance", r"p(\text{detect}\mid D)=(1-\lambda)\,\Phi\!\left("
                                         r"\frac{\ln(D_0/D)}{\sigma}\right)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("The laboratory", "explainer/psychology/lab.py"),
              ("psyche.cueing", "explainer/psychology/psyche/cueing.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=3, level="U", widget="forer",
        question="What does a number attached to a mind mean?",
        story="In 1932 the British Association appoints nineteen physicists and psychologists to decide whether a "
              "sensation can be measured; in 1940 they report that they cannot agree. The physicists' objection is "
              "that measurement means addition, as rods are laid end to end, and sensations cannot be added. "
              "Stevens replies by asking what may be done to a number without losing what it records, which gives "
              "four kinds of scale and a test for whether a sentence about numbers says anything. The part "
              "computes when the old quarrel over averaging ratings matters: exactly when two groups' answers "
              "cross. A second reply, conjoint measurement, shows that an order with enough structure implies a "
              "scale with nothing added to anything. The viewer then rates a personality sketch, and learns that "
              "Forer gave the same sketch to all 39 of his students, who rated it 4.26 out of 5: a measure has "
              "to tell people apart. From there the part builds classical test theory on the Pool, where true "
              "scores are known: a score as true score plus error, reliability as a share of variance, Spearman's "
              "correction for attenuation and its cost, the Spearman-Brown formula, Cronbach's alpha and what it "
              "does not show, and error that comes from the day or from the judge. Validity is treated as an "
              "argument: the nomological network, and a multitrait-multimethod matrix with method variance "
              "planted. Grit and conscientiousness show two names for nearly one thing. A hidden cause and a "
              "network of mutual causes are shown to imply the same correlations. The part ends with what people "
              "can report about themselves (choice blindness) and the reliability paradox.",
        handoff="Flexible analysis and what counts as evidence are Part 4. What an observer can report returns as "
                "the threshold in Part 11. Grit is examined in Part 28, factor analysis in Part 32, symptom "
                "networks in Part 39, and the two pictures of a construct are set against each other in Part 44. "
                "Conjoint measurement becomes the modern theory of test items in Part 46, and the reliability "
                "paradox is put to work in Parts 47 and 59. Every later part that shows a score uses the "
                "measurement library built here.",
        outside="Variance, covariance and correlation. The derivations use only that the variance of a sum of "
                "unrelated quantities is the sum of their variances.",
        objectives={
            "U": ["Name Stevens's four scales, the transformations each permits, and decide whether a statement "
                  "about numbers survives them.",
                  "Explain why agreement that a description fits is no evidence that a test measures anything.",
                  "Say what reliability and validity are, why a reliable measure need not be valid, and what the "
                  "jingle and jangle fallacies are."],
            "M": ["Derive reliability as the correlation of parallel forms, the Spearman-Brown formula and the "
                  "correction for attenuation from X = T + E.",
                  "Compute Cronbach's alpha, Cohen's kappa and an intraclass correlation, and say which source of "
                  "error each one counts.",
                  "Decide from two groups' answer shares whether a comparison of mean ratings can be reversed by "
                  "respacing the scale."],
            "D": ["State what a test of quantitative structure requires, and why it is hard to apply to data "
                  "with error.",
                  "Explain why a set of correlations cannot distinguish a common cause from a network of mutual "
                  "causes, and what could."],
            "I": ["Ask of any score: what kind of scale, how much error, consistent across what, what shows it "
                  "measures what its name says, and whether it is a new name for an old thing.",
                  "Explain why a task that gives a robust experimental effect can be a poor test of individuals, "
                  "and what follows for choosing a metric."],
        },
        results=[
            ("True score and error", r"X=T+E,\qquad \operatorname{Var}(X)=\operatorname{Var}(T)+\operatorname{Var}(E)"),
            ("Reliability", r"r_{xx}=\frac{\operatorname{Var}(T)}{\operatorname{Var}(X)}=\operatorname{corr}(X,X')"),
            ("Spearman-Brown", r"r_k=\frac{k\,r}{1+(k-1)\,r}"),
            ("Correction for attenuation", r"\rho_{T_xT_y}=\frac{r_{xy}}{\sqrt{r_{xx}\,r_{yy}}}"),
            ("Cronbach's alpha", r"\alpha=\frac{k}{k-1}\left(1-\frac{\sum_i\sigma_i^2}{\sigma_X^2}\right)"),
            ("Cohen's kappa", r"\kappa=\frac{p_{\text{observed}}-p_{\text{chance}}}{1-p_{\text{chance}}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("The measurement library", "explainer/psychology/measure.py"),
              ("The Pool", "explainer/psychology/pool.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=4, level="U", widget="forkingpaths",
        question="When should a finding be believed?",
        story="In 2011 a leading journal publishes nine experiments, on more than a thousand people, in which "
              "responses appear to be influenced by events that have not yet happened. The designs and the "
              "statistics are the field's ordinary ones, so either the future reaches back or those methods can "
              "produce a finding out of nothing. The part builds the tools first: an effect size as an overlap "
              "of two curves, the p-value and six things it is not, and power, which Cohen found in 1962 to be "
              "about a coin toss for an effect of ordinary size. Then it shows three ways in which honest work "
              "produces false results. The viewer makes a study of nothing significant with four defensible "
              "choices. A thousand simulated laboratories print only their successes, and a literature about "
              "nothing reports a medium effect. A researcher looks at the data after every ten people and stops "
              "when it works. Meehl's warning follows: with enough people everything correlates with everything, "
              "so rejecting no effect is a weak test of a theory. Fabrication is set apart from flexibility. "
              "The Reproducibility Project runs a hundred published studies again (97% significant becomes 36%, "
              "at half the size), and a simulated literature shows how most findings can be true while most "
              "replications fail. The repairs are procedures: preregistration, registered reports, many "
              "laboratories on one protocol, and equivalence tests for claiming an absence. The Ledger gets six "
              "rows, and Act I ends.",
        handoff="Every later part ends with its Ledger rows. The classic social experiments are re-examined in "
                "Part 34 and social priming in Part 35. Part 43 runs a preregistered replication on screen. "
                "Bayes factors are built in Part 48, and p-curves, corrections for bias and the evidence on "
                "registered reports in Part 50. The winner's curse returns with nudges at scale in Part 55. "
                "The false-positive lab built here is used wherever a later part asks how much to believe a "
                "result.",
        outside="The normal curve, a standard error, and the idea of a test from Part 2. The exact treatment of "
                "tests and intervals is Statistics, Built Parts 10 and 11.",
        objectives={
            "U": ["Read an effect size as an overlap and as the chance that one person beats another, and say "
                  "why a small p-value does not mean a large effect.",
                  "State what a p-value is, and reject six common readings of it.",
                  "Explain how flexible analysis, optional stopping and selective publication each produce "
                  "false or inflated findings without dishonesty."],
            "M": ["Compute power and the sample a study needs, and the share of significant findings that are "
                  "true from the share of hypotheses that are and the power.",
                  "Predict the mean printed effect and the replication rate of a filtered literature, and read "
                  "a funnel plot and a p-curve.",
                  "Decide from an interval and a stated bound whether a study has shown an absence."],
            "D": ["Say what a replication rate does and does not measure, and why the 2016 exchange could not "
                  "be settled by the project's own data.",
                  "State Meehl's paradox, and what kind of prediction escapes it."],
            "I": ["Recognize the garden of forking paths in a dashboard of many metrics, a subgroup analysis "
                  "or a set of backtests, and name the four repairs.",
                  "Judge a published finding by its sample, its p-value, its surprise and its replications "
                  "before relying on it."],
        },
        results=[
            ("Effect size", r"d=\frac{\bar x_1-\bar x_2}{s}"),
            ("Overlap of two groups", r"2\,\Phi\!\left(-\tfrac{|d|}{2}\right)"),
            ("Sample for a given power", r"n\approx\frac{2\,(z_{1-\alpha/2}+z_{1-\beta})^2}{d^2}\ \text{per group}"),
            ("Significant findings that are true",
             r"\frac{\pi(1-\beta)}{\pi(1-\beta)+(1-\pi)\alpha}"),
            ("At least one false alarm in k independent looks", r"1-(1-\alpha)^k"),
            ("Smallest effect a study can print", r"|d|\ge z_{1-\alpha/2}\sqrt{2/n}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("The false-positive lab", "explainer/psychology/evidence.py"),
              ("The Replication Ledger", "explainer/psychology/ledger.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
]
