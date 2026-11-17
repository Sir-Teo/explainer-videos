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
    Part(
        n=12, level="U", widget="oldnew",
        question="When you say 'yes, I saw it', how much of that is seeing and how much is saying?",
        story="Radar observers on wartime patrols missed real contacts, more as the watch wore on, and Mackworth's "
              "Clock Test of 1948 reproduced the decline. But a miss can mean the target went unseen or that the "
              "observer was not sure enough to say so, and a hit rate cannot tell which. Detection theory can. "
              "Every detection has four outcomes, carried by two numbers, the hit and false-alarm rates; one "
              "observer under five reward schemes moves its hit rate from 97% to 37% while its sensitivity stays "
              "put. Two normal distributions and a criterion turn the two rates into d' for seeing and c for "
              "saying. Sliding the criterion traces the ROC, whose area is the two-choice score; confidence "
              "ratings trace a whole curve in one session. The viewer takes a recognition test and reads off a "
              "d'. The ideal observer compares the likelihood ratio with the odds and the stakes, and when signals "
              "are rare the most accurate rule is nearly silence. Rating ROCs fitted by maximum likelihood test "
              "whether the two spreads are equal; recognition's slope is about 0.8. Forced choice scores "
              "Phi(d'/root 2) with no criterion. Curved ROCs retired the gate-like threshold, though a "
              "recollection-plus-familiarity mixture fits recognition as well. A positive mammogram is cancer "
              "about 8% of the time, clearer in natural frequencies. Rare targets are missed more, partly because "
              "the criterion follows the base rate and partly because searches end too soon. On the watch, the "
              "false alarms tell caution from fatigue.",
        handoff="Single photons and the eye's own noise are Part 13. Recognition and false memories are Part 21, "
                "confidence over time Part 25, base rates and judgment Part 26, awareness measured with d' Part "
                "27, alarms and rare targets Part 51, and hiring as detection Part 53.",
        outside="Part 11's psychometric function and forced choice, and the normal distribution and its quantile. "
                "Likelihood ratios are introduced here; the Neyman-Pearson lemma is proved in Statistics, Built.",
        objectives={
            "U": ["Name the four outcomes of a detection and explain why a hit rate alone is uninterpretable.",
                  "Compute d' and c from a hit rate and a false-alarm rate, and say what each measures.",
                  "Read an ROC: what moving along it and moving between curves mean."],
            "M": ["Derive the ideal criterion from the likelihood ratio, the base rate and the payoffs.",
                  "Fit a rating ROC by maximum likelihood and test equal against unequal variances.",
                  "Derive the two-alternative score Phi(d'/root 2) and the area under the ROC."],
            "D": ["Explain how the shape of an ROC separates threshold, detection and mixture models, and its limits.",
                  "Assess the competing accounts of the prevalence effect and of the vigilance decrement."],
            "I": ["Choose between ROC and precision-recall curves for a classifier with rare positives.",
                  "Explain the share of positive tests that are real from prevalence, hits and false alarms."],
        },
        results=[
            ("Sensitivity", r"d' = z(H) - z(F)"),
            ("Criterion", r"c = -\tfrac12\,\bigl(z(H) + z(F)\bigr)"),
            ("The ideal rule", r"\ell(x) > \frac{P(N)}{P(S)}\cdot\frac{V_{cr} + C_{fa}}{V_{hit} + C_{miss}}"),
            ("Area under the ROC", r"A = \Phi\!\left(d' / \sqrt{1 + \sigma_s^2}\right)"),
            ("Two-alternative choice", r"P_c = \Phi(d'/\sqrt2)"),
            ("Positive predictive value", r"\frac{pH}{pH + (1-p)F}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, 9, 12), D=(10, 11, 14), I=(13,),
        also=(("Psyche's detection module", "explainer/psychology/psyche/sdt.py"),
              ("Its tests", "tests/psychology/test_sdt.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=13, level="U", widget="contrast",
        question="What does the eye tell the brain?",
        story="In 1942, in a dark room at Columbia, Hecht, Shlaer and Pirenne found that a flash is seen when only "
              "five to fourteen quanta are absorbed, spread over about five hundred rods, so a rod must answer a "
              "single quantum. The steepness of a frequency-of-seeing curve gives the same number without knowing "
              "the eye's losses, because arrivals are Poisson. Optics and the cone mosaic stop detail near sixty "
              "cycles per degree; gain control spans ten log units of light and gives Weber's law. Adrian found that "
              "a fibre codes strength as a rate, Kuffler that a ganglion cell weighs a centre against a surround: a "
              "difference of Gaussians, a band-pass filter, Mach bands, and a cure for redundancy. Hubel and Wiesel's "
              "cells want edges at one orientation, modelled as Gabor fields, simple and complex. The viewer reads "
              "a Campbell-Robson chart and sees a hybrid image change with distance; adaptation reveals channels, "
              "and divisive normalization saturates and masks. Colour is three numbers: matching is a 3-by-3 solve "
              "that reproduces Stiles and Burch's 1955 data, metamers are the null space, and the 1931 diagram is "
              "built on it. Opponent channels explain why nothing looks reddish green; colour blindness is a lost "
              "dimension. Constancy discounts the light, and the dress shows two bets on one image. D.F. posts a card "
              "into a slot whose angle she cannot report.",
        handoff="Seeing as inference is Part 14, the other senses Part 15, attention as gain Part 18, seeing "
                "without knowing Part 27, displays and design Parts 51 and 52, and efficient coding Part 58.",
        outside="Part 11's thresholds and Weber's law, Part 12's forced choice, and Part 6's lateral inhibition. "
                "Matrix inversion and null spaces from linear algebra; Fourier frequency in the loose sense.",
        objectives={
            "U": ["Explain how the frequency-of-seeing curve's steepness reveals the number of quanta needed.",
                  "Describe a centre-surround receptive field and why it acts as a band-pass filter.",
                  "Explain why three numbers describe a colour, and what a metamer is."],
            "M": ["Derive the Nyquist limit of a mosaic and the alias of a finer grating.",
                  "Compute colour-matching functions for any three primaries from the cone fundamentals.",
                  "Show how gain control turns a saturating receptor into Weber's law."],
            "D": ["Weigh the evidence for single-photon detection by people against the evidence for rods.",
                  "Assess how far the edge-detector hierarchy explains V1, and the two-streams account."],
            "I": ["Explain chroma subsampling and gamut limits from the CSF and the chromaticity diagram.",
                  "Choose and check a palette that colour-blind readers can use."],
        },
        results=[
            ("Seeing a flash", r"P(\text{seen}) = P(N \ge k),\ N \sim \mathrm{Poisson}(a q)"),
            ("A mosaic's limit", r"f_{\max} = \frac{1}{2\,\Delta}"),
            ("Gain control", r"R = \frac{I^n}{I^n + \sigma^n},\ \sigma \propto I_{\text{background}}"),
            ("A ganglion cell", r"w(x) = G_{\sigma_c}(x) - G_{\sigma_s}(x)"),
            ("Normalization", r"R_i = \frac{d_i^{\,n}}{\sigma^n + \sum_j d_j^{\,n}}"),
            ("Colour matching", r"\mathbf{w} = P^{-1}\,\mathbf{c}_{\text{test}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 13), D=(12, 15), I=(14,),
        also=(("Psyche's vision module", "explainer/psychology/psyche/vision.py"),
              ("Its tests", "tests/psychology/test_vision.py"),
              ("The colour tables", "explainer/psychology/archive/_colour_tables.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
Part(
        n=14, level="U", widget="illusion",
        question="If every image fits many worlds, how does seeing choose one?",
        story="Two squares on a checkerboard send the eye the same light, and one looks dark and the other light: the "
              "viewer sees surfaces, with the shadow taken out. Every image fits many scenes, as the Ames room shows, so "
              "seeing must add assumptions. The Gestalt laws of grouping read as priors about objects; Kanizsa's "
              "triangle has edges that are not in the image, and Rubin's vase shows that an edge belongs to one side. "
              "Two eyes give disparity, which falls with the square of distance; Wheatstone's stereoscope and Julesz's "
              "random dots show it is enough for depth. Size constancy multiplies by seen distance, and makes the Ponzo "
              "and Müller-Lyer illusions on a page; the carpentered-world explanation is now contested. Bayes's rule "
              "with normal distributions gives precisions that add and means weighted by precision, shrinkage toward "
              "the prior, and a biased percept that is more accurate. Cue combination is predicted from each sense "
              "alone, checked on Psyche and by Ernst and Banks, and explains the ventriloquist. Light from above and a "
              "preference for slow motion are priors the viewer can see; the second solves the aperture problem. "
              "Retinex explains the two squares. Objects need invariance, faces are seen as wholes in cortex of their "
              "own, and deep networks predict the brain yet answer by texture until their diet changes.",
        handoff="The other senses are Part 15, prediction errors in learning Part 17, attention and expectation "
                "Part 18, what infants know Part 30, displays and the human in the loop Part 51, the predictive brain "
                "Part 58, and deep networks as models of minds Part 60.",
        outside="Part 4's Bayes's rule, Part 11's psychometric functions and staircases, Part 12's forced choice, and "
                "Part 13's cells and filters. Normal distributions, completing the square, and a little vector "
                "geometry.",
        objectives={
            "U": ["Explain why a retinal image cannot fix the scene, with an example of size and distance.",
                  "State the Gestalt laws of grouping and read them as assumptions about objects.",
                  "Explain size constancy and how it produces the Ponzo and Müller-Lyer illusions."],
            "M": ["Derive the normal posterior by completing the square, and the weights of two combined cues.",
                  "Derive binocular disparity and its fall with the square of distance.",
                  "Compute the MAP velocity for two edges under a slow prior, and show it tends to the intersection "
                  "of constraints."],
            "D": ["Judge when a Bayesian model of perception is a test and when it is a description after the fact.",
                  "Weigh the evidence on whether the Müller-Lyer illusion depends on culture, and on what the face "
                  "area is selective for."],
            "I": ["Explain the vergence-accommodation conflict in headsets and what a display must do about it.",
                  "Say how machine vision's errors differ from people's, and what that means for a human in the loop."],
        },
        results=[
            ("Bayes for perception", r"p(s \mid x) \propto p(x \mid s)\, p(s)"),
            ("Precisions add", r"\frac{1}{\sigma_{\text{post}}^2} = \frac{1}{\sigma^2} + \frac{1}{\sigma_0^2}"),
            ("Cue weights", r"w_V = \frac{1/\sigma_V^2}{1/\sigma_V^2 + 1/\sigma_H^2}"),
            ("Disparity", r"\delta \approx \frac{I\,\Delta d}{d^2}"),
            ("Size constancy", r"\text{size} = 2\,d\,\tan(\theta/2)"),
            ("Lightness", r"L = R \times E,\ \log L = \log R + \log E"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12), D=(11, 14), I=(13,),
        also=(("Psyche's inference module", "explainer/psychology/psyche/infer.py"),
              ("Its tests", "tests/psychology/test_infer.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
Part(
        n=15, level="U", widget="pitchdir",
        question="How do pressure waves become a voice, and why does pain not follow the injury?",
        story="A sound with no energy at 200 Hz is heard at 200 Hz: the missing fundamental. Sound is pressure, and the "
              "decibel is Fechner's logarithm made into a unit. Von Bekesy watched a travelling wave peak at one place "
              "for each frequency; Greenwood's map, the outer hair cells' amplifier and Kemp's echoes followed, and "
              "Psyche's cochlea is a bank of gammatone filters. Fletcher's band-widening measured the filters, and "
              "masking runs downhill from low to high. Pitch comes from timing as well as place: summary "
              "autocorrelation finds the missing fundamental. Two ears compare arrival times to about ten microseconds; "
              "Jeffress's coincidence circuit fits the owl, while mammals use timed inhibition. Scenes are parsed by "
              "harmonicity, onset and streaming. Speech has no invariant cues; categorical perception holds at the "
              "boundary but not within categories; the McGurk effect is cue combination, with wide individual "
              "differences. Roughness is universal, the taste for consonance learned. Touch has four channels and a "
              "rubber hand can be adopted, perhaps partly by expectation; pain passes through a gate and the brain's "
              "control of it. Smell is a code of hundreds of receptor types; the tongue map and the trillion smells "
              "were corrected.",
        handoff="Conditioning is Part 16, prediction errors Part 17, attention Part 18, language Part 23, human "
                "factors Part 51, pain and placebo in the clinic Part 57, and the predictive brain Part 58.",
        outside="Part 11's Fechner and Stevens, Part 12's detection theory, Part 13's filters and channels, and Part "
                "14's cue combination. Logarithms, sine waves and the idea of a filter.",
        objectives={
            "U": ["Explain what the decibel measures and why it is logarithmic.",
                  "Describe the cochlea as a frequency analyser, and what masking reveals about it.",
                  "Explain the missing fundamental, the McGurk effect and the gate control of pain."],
            "M": ["Compute interaural time differences and the direction a given delay implies.",
                  "Show why a summary autocorrelation peaks at the period of a missing fundamental.",
                  "Derive the label model of ABX discrimination and the McGurk prediction from cue weights."],
            "D": ["Weigh place against timing theories of pitch, and maps against channel codes for direction.",
                  "Assess the rubber-hand illusion and the trillion-odour claim against their critiques."],
            "I": ["Explain why hearing aids compress and what a cochlear implant can and cannot restore.",
                  "Explain how a perceptual audio codec uses masking to discard data."],
        },
        results=[
            ("The decibel", r"L = 20\log_{10}(p / p_0),\ p_0 = 20\ \mu\text{Pa}"),
            ("Auditory filter width", r"\mathrm{ERB}(f) = 24.7\,(4.37 f/1000 + 1)"),
            ("Place map", r"f = 165.4\,(10^{2.1x} - 0.88)"),
            ("Interaural delay", r"\Delta t = \frac{r}{c}(\theta + \sin\theta)"),
            ("Labels predict discrimination", r"P_{ABX} = \tfrac12\left[1 + (p_A - p_B)^2\right]"),
            ("The gate", r"T = \frac{w_L L + w_S S}{1 + g\,\max(L - kS, 0)}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13), D=(8, 12, 15), I=(14,),
        also=(("Psyche's hearing module", "explainer/psychology/psyche/hearing.py"),
              ("Its tests", "tests/psychology/test_hearing.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
]
