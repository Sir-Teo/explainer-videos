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
]
