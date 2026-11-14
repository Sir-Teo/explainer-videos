"""Act III, Sensing (Parts 11-15)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=11, level="U", widget="threshold",
        question="What is the smallest difference you can notice, and is there a law to it?",
        story="On a morning in October 1850 Fechner, lying in bed, sees how to answer Kant's first objection: not "
              "by putting a ruler to a sensation, but by counting the just noticeable steps between two stimuli. "
              "Weber had found that the step is a constant fraction of the stimulus. On Psyche, noise with a "
              "fixed floor and a part that grows with the stimulus gives that law over the middle of the range "
              "and its failure near the floor; loud tones show a near miss. Count the steps and sensation is a "
              "logarithm, ninety steps from 1 to 1,000 at a fraction of 0.08, on one assumption: that every step "
              "is the same amount of sensation. Fechner's three methods find the steps; the method of limits "
              "has a stopping rule that biases it, and its yes-or-no question mixes what the observer sees with "
              "how willing it is to say so, while a forced choice between two intervals does not. A threshold "
              "is a curve with four numbers, a guess rate, a threshold, a spread and a lapse rate. The viewer "
              "does eight trials. One study of 320 trials is fitted by maximum likelihood, with a bootstrap "
              "interval of about thirty percent either way, and one slip moves a fit with no lapse rate by a "
              "quarter. A two-down staircase settles at 70.7%, derived in a line, if its steps are small; QUEST "
              "keeps a belief and is fastest. Stevens asks for numbers and gets power laws, exponents from a "
              "third to three and a half, checked by matching one sense against another, and moved by the range "
              "of stimuli shown. Fechner's logarithm and Stevens's power come from the same steps and two "
              "assumptions; growing noise and a compressed code give the same thresholds. Weber's law holds for "
              "number and for time.",
        handoff="Seeing against saying is Part 12, signal detection. The eye's thresholds and contrast are Part "
                "13. Prices and noticing are Part 26, number sense in children Part 30, scaling judgments Part "
                "46, displays built for human thresholds Part 51, and why perception compresses, efficient "
                "coding, Part 58.",
        outside="Part 3's scales of measurement and Part 9's maximum likelihood. Logarithms and the idea of an "
                "integral are used and explained; the bootstrap is introduced here.",
        objectives={
            "U": ["State Weber's law and where it fails, and explain why a threshold is a curve and not a point.",
                  "Describe the three classical methods, and why a yes-no question mixes seeing with willingness.",
                  "Describe magnitude estimation and Stevens's power law, and say what the exponents mean."],
            "M": ["Derive Fechner's law from Weber's law and its assumption, and the power law from Ekman's.",
                  "Fit a psychometric function by maximum likelihood, with a lapse rate and a bootstrap interval.",
                  "Derive the point a k-down 1-up staircase converges to, and say when the result holds."],
            "D": ["Explain why thresholds alone cannot tell growing noise from a compressed code, and what could.",
                  "Assess what magnitude estimates measure, given range and context effects."],
            "I": ["Recognise the staircase in a hearing test and the method of limits in an eye chart.",
                  "Explain what a just noticeable difference means for a codec, a display or a price change."],
        },
        results=[
            ("Weber's law", r"\Delta I = k\,I"),
            ("Fechner's law", r"S = \frac{1}{k}\,\ln\frac{I}{I_0}"),
            ("The psychometric function", r"\psi(x) = \gamma + (1-\gamma-\lambda)\,F(x;\alpha,\beta)"),
            ("Two-interval threshold", r"\Delta I_{75} = \sqrt{2}\,z_{0.75}\,\sigma \approx 0.95\,\sigma"),
            ("Where a staircase settles", r"p^{k} = \tfrac12 \;\Rightarrow\; p = 0.5^{1/k}"),
            ("Stevens's power law", r"S = c\,I^{a},\qquad a_{\text{match}} = a_1 / a_2"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's psychophysics module", "explainer/psychology/psyche/psychophysics.py"),
              ("Its tests", "tests/psychology/test_psychophysics.py"),
              ("The Battery's threshold task", "explainer/psychology/battery.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
]
