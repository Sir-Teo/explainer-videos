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
]
