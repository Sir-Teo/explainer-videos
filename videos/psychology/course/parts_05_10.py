"""Act II, The Wet Machine (Parts 5-10)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=5, level="U", widget="spiketrain",
        question="What is the mind's smallest moving part, and what does it compute?",
        story="Galvani makes a dead frog's leg kick with two metals; Helmholtz finds the signal in a nerve far too "
              "slow to be a current in a wire. A century later Hodgkin and Huxley measure the currents through "
              "the membrane of a squid's giant axon, fit them with four equations, and compute a nerve signal "
              "and its speed, 18.8 metres a second against 21.2 measured. The part builds that result from the "
              "ground. Cajal's separate cells against Golgi's net. A difference of concentration across a "
              "membrane as a battery (Nernst), and two batteries with a dial between them (Goldman). The "
              "membrane as a leaky capacitor that adds up a few milliseconds. The voltage clamp, which breaks "
              "the loop between voltage and channels, and the two conductances it revealed. The gates m, h and "
              "n, and the four equations fitted only to the clamp. Then the equations are let go: a threshold, "
              "a signal of one size and a dead time fall out, and on a cable the signal renews itself at the "
              "computed speed. The model is reduced to two variables, where its behaviour is the geometry of "
              "a phase plane, and to one, the integrate-and-fire neuron with its rate in closed form. The "
              "viewer reads spike trains as a downstream cell would, and the part ends with what one cell can "
              "compute: a threshold, a coincidence, and with dendrites a small network.",
        handoff="Synapses and the first circuits are Part 6. What an electrode or a scanner records is Part 8. "
                "Counting noisy signals becomes signal detection in Part 12, coincidence detectors locate a "
                "sound in Part 15, and accumulation to a threshold returns as a model of deciding in Part 25. "
                "The unit with its spikes left out is set against real neurons in Part 60. Psyche's neuron is "
                "the tissue under every later circuit in the series.",
        outside="Exponentials and logarithms, and the idea of a derivative as a rate of change. The circuit "
                "needs Ohm's law and what a capacitor is; chapter 8 reads a phase plane, which is explained "
                "there.",
        objectives={
            "U": ["Name the parts of a neuron and say which way signals go, and why the brain is made of "
                  "separate cells.",
                  "Explain why a nerve signal has a threshold, one size and a dead time, in terms of sodium and "
                  "potassium gates.",
                  "Say how a fibre with one size of signal reports the strength of a stimulus, and why a brain "
                  "listens to many cells at once."],
            "M": ["Compute a Nernst potential and a Goldman voltage, and the time constant of a membrane.",
                  "Write the Hodgkin-Huxley equations, say what each term was fitted to, and trace each feature "
                  "of the computed spike to a gate.",
                  "Read threshold, all-or-none and the refractory period off a phase plane, and derive the "
                  "firing rate of an integrate-and-fire neuron."],
            "D": ["Say what made the 1952 model a test and not a fit, and what the same standard would ask of "
                  "a model in psychology.",
                  "State what is and is not known about computation in dendrites, and design a measurement "
                  "that would show a single cell computing a table no point neuron can."],
            "I": ["Use the strength-duration relation, the dead time and the dependence of threshold on fibre "
                  "size to reason about a stimulating device.",
                  "Decide whether a question about behaviour lives at the level of the neuron, and what the "
                  "membrane cannot tell you."],
        },
        results=[
            ("Nernst potential", r"E=\frac{RT}{zF}\ln\frac{[\text{out}]}{[\text{in}]}"),
            ("Membrane time constant", r"\tau=RC,\qquad V(t)=IR\,(1-e^{-t/\tau})"),
            ("Hodgkin and Huxley",
             r"C\frac{dV}{dt}=I-\bar g_{Na}m^3h\,(V-E_{Na})-\bar g_K n^4\,(V-E_K)-g_L(V-E_L)"),
            ("A gate", r"\frac{dx}{dt}=\alpha_x(V)(1-x)-\beta_x(V)\,x"),
            ("Length constant", r"\lambda=\sqrt{\frac{a\,R_m}{2R_i}}"),
            ("Integrate-and-fire rate", r"f=\left[t_{\text{ref}}+\tau\ln\frac{RI}{RI-\theta}\right]^{-1}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's neuron", "explainer/psychology/psyche/neuron.py"),
              ("Its tests", "tests/psychology/test_neuron.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=6, level="U", widget="gridspots",
        question="How do neurons talk, and how does talking change them?",
        story="For half a century physiologists argued over what crosses the gap between two neurons, a current "
              "or a chemical. In 1921 Otto Loewi slows one frog's heart through its nerve, moves the fluid to a "
              "second heart, and the second slows too. The connection is chemical, and a chemical step has "
              "quantities in it that can change. The part takes the synapse apart: six steps from spike to "
              "clearance, transmitter released in packets by chance (Katz), two kinds of receptor, and the "
              "handful of places where a drug can act. It computes how a membrane adds its inputs within about "
              "ten milliseconds and how a shunt divides. Then learning: Hebb's rule, local and unstable; Oja's "
              "repair, which makes a cell find the first principal component of its inputs; long-term "
              "potentiation, the NMDA receptor as the molecule that detects input and output together, spike "
              "timing, and a sliding threshold that makes a cell selective. Three circuits follow from one "
              "motif, mutual inhibition: neighbours that inhibit each other exaggerate edges (the horseshoe "
              "crab, Mach's bands); with self-excitation two rivals choose and hold the choice; with fatigue "
              "they alternate, as the spinal cord does in walking. Populations of excitatory and inhibitory "
              "cells rest, oscillate or saturate as their drive rises, and the neuromodulators set gain and "
              "learning rate. The viewer looks at the Hermann grid, hears and computes its textbook "
              "explanation, and watches it fail on a grid with curved streets.",
        handoff="Where things are in a brain, and what recordings measure, are Parts 7 and 8. Lateral "
                "inhibition returns in the retina (Part 13), dopamine as the third factor of a learning rule in "
                "Part 17, a choice held in activity as working memory in Part 19, and whether long-term "
                "potentiation is how memories are stored in Part 20. The circuit that decides is tested against "
                "reaction times in Part 25, the four families of drug meet the disorders in Parts 40 to 42, and "
                "learning without a local rule is Part 58.",
        outside="Part 5's membrane: batteries, conductances and the time constant. Vectors and the idea of a "
                "principal component help in chapter 4, which derives what it uses. Chapters 8 to 10 read "
                "differential equations as 'relaxes toward', which is explained there.",
        objectives={
            "U": ["Follow a signal across a chemical synapse step by step, and say where each of four families "
                  "of drug acts.",
                  "Explain why a neuron responds to inputs that arrive together, and what excitation and "
                  "inhibition do to its voltage.",
                  "Say what Hebb's rule is, what long-term potentiation showed, and how mutual inhibition "
                  "sharpens an edge, holds a choice and makes a rhythm."],
            "M": ["Compute a synapse's mean response, variance and failure rate from n, p and q, and the steady "
                  "voltage of a membrane with a shunt.",
                  "Show that Hebb's rule diverges along the first eigenvector of the inputs' correlations, and "
                  "derive Oja's rule and its fixed point.",
                  "Write the equations of lateral inhibition, a winner-take-all pair, a half-centre oscillator "
                  "and Wilson and Cowan's populations, and say what each parameter sets."],
            "D": ["Say what the curved Hermann grid shows about testing a model, and what a model must predict "
                  "beyond the effect it was built for.",
                  "State what is and is not established about where a memory is stored, and design an "
                  "experiment that separates strengthened synapses from chosen cells."],
            "I": ["Read a dose-occupancy curve and the shift a competitive antagonist makes, and connect a "
                  "drug's site of action to its side effects.",
                  "Compare the registered and the published record of a set of trials, and say what each "
                  "would lead a reader to believe."],
        },
        results=[
            ("A synapse's strength", r"\langle \text{response}\rangle=n\,p\,q,\qquad P(\text{failure})=(1-p)^n"),
            ("A shunt divides", r"V-E_L=\frac{g_E\,(E_E-E_L)}{g_L+g_E+g_I}"),
            ("Hebb's rule, and Oja's", r"\Delta w=\eta\,x\,y,\qquad \Delta w=\eta\,y\,(x-y\,w)"),
            ("Lateral inhibition", r"r_i=e_i-\sum_{j\neq i}k_{ij}\,r_j"),
            ("Wilson and Cowan", r"\tau\,\dot E=-E+S(w_{EE}E-w_{EI}I+P)"),
            ("Receptor occupancy", r"\frac{[D]}{[D]+K_d}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's circuits", "explainer/psychology/psyche/circuits.py"),
              ("Their tests", "tests/psychology/test_circuits.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=7, level="U", widget="blindspot",
        question="Is the mind in one place or everywhere?",
        story="In 1848 an iron rod passes through Phineas Gage's head and he lives; what the record says about "
              "the change in him is a few sentences, and the rest is retelling. Damage is psychology's oldest "
              "experiment, and this part is about how to read it. A tour names the parts. Gall asks the right "
              "question with a method that cannot fail; Flourens and Lashley answer 'everywhere', and a model "
              "cortex in which every job has its own place reproduces Lashley's result when the task can be done "
              "six ways. Broca's patient loses speech and keeps understanding, Wernicke's does the reverse, and "
              "a diagram of boxes and arrows predicts a third aphasia before it is seen. The logic is made "
              "exact: one resource gives a single dissociation, a double one rules it out, and noisy tests with "
              "a large screen of patients fake a double one about half the time. Penfield maps the body on "
              "awake patients; the visual cortex spends nearly half its area on the ten degrees around the "
              "centre of gaze, and the viewer finds the hole in each eye's view that the brain fills in. H.M. "
              "loses the making of new memories and learns a skill all the same. In the split brain one half "
              "knows what the other cannot say, and the talking half explains what it did not choose; the idea "
              "of left-brained and right-brained people fails on 1,011 scans. Maps rewire with use, and the "
              "answer to the old question is a network of specialized parts.",
        handoff="What a recording or a scan of an intact brain measures is Part 8. The visual map and "
                "receptive fields are Part 13, filling in is Part 14, and the body's map is Part 15. Neglect "
                "returns with attention (Part 18), H.M. with the kinds of memory (Part 20), aphasia with "
                "language (Part 23), blindsight and the interpreter with consciousness (Part 27), and critical "
                "periods with development (Part 30). Maps of brain data as statistics are Part 49.",
        outside="Part 2's difference between an experiment and a comparison of groups that formed themselves, "
                "Part 3's reliability, and Part 4's file drawer and t test. Chapter 5 integrates 1/(E + c) and "
                "uses a tangent; both are explained there.",
        objectives={
            "U": ["Name the lobes and the main structures under the cortex, with one line on what each is "
                  "needed for and why that line is too simple.",
                  "Tell the stories of Gage, Broca's and Wernicke's patients, H.M. and the split brain, "
                  "separating what the record shows from what was added.",
                  "Say what a single and a double dissociation each allow you to conclude."],
            "M": ["Lesion a box-and-arrow model and predict which tasks fail; compute the chance that a screen "
                  "of patients from a one-resource world contains both patterns.",
                  "Integrate the cortical magnification function, find the share of the map near the centre of "
                  "gaze, and place the blind spot on a screen.",
                  "Compare one patient with a small control sample by z and by the single-case t test."],
            "D": ["Explain why a lesion study is an observational study, and how the blood supply displaces a "
                  "lesion-symptom map.",
                  "Design a study that separates damage to a region from damage to a connection beneath it."],
            "I": ["Read a neuropsychological report: the comparison group, its size, the number of tests given "
                  "and the base rate of low scores in healthy people.",
                  "Recognize a claim about 'what a brain region is for' that rests on a single dissociation."],
        },
        results=[
            ("A lesioned route", r"\text{score}=\prod_{m\,\in\,\text{route}}(1-\ell_m)"),
            ("A screen that finds both patterns",
             r"1-(1-p_A)^N-(1-p_B)^N+(1-p_A-p_B)^N"),
            ("Cortical magnification", r"M(E)=\frac{17.3}{E+0.75}\ \text{mm per degree}"),
            ("Distance along the cortex", r"D(E)=17.3\,\ln\!\left(1+\frac{E}{0.75}\right)\ \text{mm}"),
            ("One patient, n controls", r"t=\frac{x-\bar c}{s\,\sqrt{(n+1)/n}},\qquad \text{df}=n-1"),
            ("Low scores in a healthy person", r"P(\text{at least one of }k)=1-0.95^{\,k}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's brain", "explainer/psychology/psyche/brain.py"),
              ("Its tests", "tests/psychology/test_brain.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=8, level="U", widget="impossible",
        question="What can a brain scan tell you about a mind?",
        story="In 2009 a dead salmon is put in a scanner, shown photographs of people, and found to have "
              "'active' voxels: a test in every voxel, at one in a thousand, always finds something. A scan is "
              "the end of a chain, and the part walks it. One neuron has a tuning curve, the real signal "
              "through a keyhole. A scalp electrode hears only cells that are aligned and active together, so "
              "the EEG gives timing to the millisecond and no unique answer about place. Averaging pulls a "
              "five-microvolt wave out of twenty microvolts of noise at a rate of the square root of the number "
              "of trials, and one such wave, the N400, follows the meaning of a word. Magnetic resonance lines "
              "up protons, tips them, and reads an image from its Fourier transform; the functional scan "
              "measures oxygen in the blood, an echo that peaks five seconds after the neurons and follows "
              "their input more than their output. An experiment becomes a map by a regression in every voxel, "
              "of one task minus another. Then three ways a map misleads: the threshold (and the 2016 finding "
              "that cluster inference let through far more than 5%), choosing voxels by the correlation that "
              "is then reported, and reading the map backwards from region to mental state. Watching is not "
              "intervening: to know a region is needed you disturb it. The part ends with what scanning has "
              "settled, what is sold on its name, and how many people a brain study needs.",
        handoff="Rhythms of the EEG in sleep are Part 10; tuning curves and receptive fields are Part 13; the "
                "face area is argued in Part 14; attention on the scalp is Part 18; the N400 returns with "
                "language in Part 23; evidence accumulating before a choice is Part 25; scans and awareness "
                "are Part 27. Why findings fail to repeat is Part 43, and the statistics of brain data in "
                "full are Part 49.",
        outside="Part 3's reliability and attenuation, Part 4's regression, t test, Bayes' rule and forking "
                "paths, Part 2's permutation test, Part 5's impulse and Part 6's synaptic currents. The Fourier "
                "transform is used as a fact in chapter 4 and done properly in Analysis, Built.",
        objectives={
            "U": ["Say what each instrument measures, how far that is from an impulse, and what it gives up: "
                  "a single unit, the EEG, structural and functional MRI.",
                  "Explain why averaging finds an event-related potential, and what the N400 is.",
                  "State three ways a brain map misleads, and the remedy for each."],
            "M": ["Compute the noise left after averaging n trials, and the trials needed for a given "
                  "precision.",
                  "Convolve events with a haemodynamic response, build a design matrix, and fit a voxel by "
                  "least squares.",
                  "Compute the chance of a false alarm among N tests, a Bonferroni threshold, the ceiling on a "
                  "correlation from two reliabilities, and a reverse inference by Bayes' rule."],
            "D": ["Explain why selecting voxels by a correlation and then reporting it measures nothing, and "
                  "simulate it.",
                  "Say what sample a brain-behaviour association of a given size needs, and what small studies "
                  "of small effects report."],
            "I": ["Tell an established use of a brain measure (epilepsy, sleep, presurgical mapping) from a "
                  "product sold on the word 'brain'.",
                  "Ask six questions of any claim that arrives with a picture of a brain."],
        },
        results=[
            ("Averaging", r"\sigma_{\bar x}=\frac{\sigma}{\sqrt{n}}"),
            ("The linear model of a voxel", r"y(t)=\beta\,(s*h)(t)+c+\varepsilon(t)"),
            ("Many tests", r"P(\text{any false alarm})=1-(1-\alpha)^{N},\qquad \alpha_{\text{Bonf}}=\frac{0.05}{N}"),
            ("The ceiling on a correlation", r"r_{\max}=\sqrt{R_x\,R_y}"),
            ("Reverse inference", r"P(M\mid A)=\frac{P(A\mid M)\,P(M)}{P(A\mid M)\,P(M)+P(A\mid\neg M)\,P(\neg M)}"),
            ("People needed to detect r", r"n\approx\left(\frac{z_{\alpha/2}+z_{\beta}}{\operatorname{artanh} r}\right)^{2}+3"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's imaging module", "explainer/psychology/psyche/imaging.py"),
              ("Its tests", "tests/psychology/test_imaging.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=9, level="U", widget="twins",
        question="How much of who you are did you inherit, and what does that question mean?",
        story="In 1979 identical twins separated as babies meet at thirty-nine and find a list of shared habits. "
              "The list proves nothing: two strangers compared on two hundred things share about ten. The design "
              "behind it does. A family passes on genes and a home together, so a family tree cannot say which "
              "did the work; twins and adoption can. Many small genes add up to a bell curve, and a score splits "
              "into additive genes, the home a family shares, and everything else. Identical twins share all of "
              "the first two and fraternal twins half of the genes, so twice the difference between their "
              "correlations is the heritability: four lines of algebra, and the series' first path diagram. On "
              "the Pool the design gives back what was planted, slowly, and then fails as each of its four "
              "assumptions is switched off, two failures inflating the genes and two the home. The viewer "
              "guesses six heritabilities. Then what the number is not: not fixedness (height rose twenty "
              "centimetres in a century), not about groups (seed from one sack in two fields), not about a "
              "person, not a constant. Three laws: everything is heritable, the shared home counts for less, "
              "much is neither. The search for the genes: a decade of candidate genes tested in samples that "
              "could not see them, whose findings failed; then a million tests at once, a threshold of five in "
              "a hundred million, and thousands of positions of tiny effect. A polygenic score predicts the "
              "averages of groups and says little about one person, and between siblings its effect is smaller, "
              "because part of it is the home the parents' genes made. Evolution supplies hypotheses and "
              "stories; the difference is whether they can fail.",
        handoff="Reasoning about cheats as a test of an evolutionary claim is Part 24; how people understand a "
                "risk is Part 26; temperament and parenting are Part 30; intelligence, its heritability across "
                "wealth and age, and the history of eugenics are Part 32; personality is Part 33; mate "
                "preferences are Part 37; the genetics of disorders are Parts 40 and 41. Path diagrams are "
                "fitted in earnest from Part 44.",
        outside="Part 2's confounds and random assignment, Part 3's correlation and variance, Part 4's power, "
                "forking paths and the winner's curse, and Part 8's correction for many tests. Maximum "
                "likelihood is used as a tool in chapter 4 and explained in Part 44.",
        objectives={
            "U": ["Explain why resemblance within families cannot separate genes from a shared home, and how "
                  "twins and adoption can.",
                  "State what heritability is, and four things it is not.",
                  "Say why candidate-gene findings failed and why genome-wide studies need enormous samples."],
            "M": ["Derive Falconer's formula from the two twin correlations, compute the three shares, and "
                  "attach a standard error.",
                  "Read a path diagram of the ACE model and say what each line asserts.",
                  "Compute the sample needed to detect a variant of a given size, the number of false hits "
                  "among a million tests, and what a score of a given accuracy says about one person."],
            "D": ["Simulate a twin study with an assumption broken and predict the direction of the bias.",
                  "Explain why a polygenic score's effect is smaller between siblings, and what the gap can "
                  "and cannot be attributed to."],
            "I": ["Tell a test for a single-gene condition from a polygenic score, and do the arithmetic of a "
                  "consumer score and of embryo selection.",
                  "Ask six questions of any claim about genes and behaviour."],
        },
        results=[
            ("A score in three parts", r"P=A+C+E,\qquad h^{2}=\frac{\operatorname{Var}(A)}{\operatorname{Var}(P)}"),
            ("Falconer's formula", r"h^{2}=2\,(r_{MZ}-r_{DZ}),\qquad c^{2}=2\,r_{DZ}-r_{MZ},\qquad e^{2}=1-r_{MZ}"),
            ("Parents and children", r"\mathbb{E}[\text{child}\mid\text{midparent}]=h^{2}\times\text{midparent}"),
            ("People needed for one variant", r"n\approx\frac{(z_{\alpha/2}+z_{\beta})^{2}\,(1-r^{2})}{r^{2}}"),
            ("Genome-wide significance", r"\alpha=\frac{0.05}{10^{6}}=5\times10^{-8}"),
            ("What a score predicts", r"R^{2}\approx h^{2}\,\frac{n\,h^{2}}{n\,h^{2}+m}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's genes module", "explainer/psychology/psyche/genes.py"),
              ("Its tests", "tests/psychology/test_genes.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=10, level="U", widget="vigilance",
        question="Why is the same mind so different at four in the afternoon and at four in the morning?",
        story="In 1938 two men live for a month in a cave on a day of twenty-eight hours. One man's temperature "
              "rhythm follows the schedule; the other's keeps to twenty-four hours, with no sun to copy. The body "
              "has a clock. Left alone it runs at 24.18 hours, which the same 28-hour trick showed sixty years "
              "later; it sits above the crossing of the optic nerves, each of its cells a loop of genes that "
              "switch themselves off; and a model of it locks to days of 23 to 25 hours and no others. Light "
              "sets it through cells in the eye that make no pictures: later if it falls before the "
              "temperature's low point, earlier if after, so a flight leaves the clock behind for days. In the "
              "laboratory sleep turns out to have stages in ninety-minute cycles, one of them with darting eyes "
              "and dreams. Two processes time it: a pressure that rises over eighteen hours awake and falls over "
              "four asleep, and thresholds the clock moves. Together they give an eight-hour night, a recovery "
              "sleep only half an hour longer after forty hours awake, and a second wind the next afternoon. "
              "The viewer works out a chronotype. Two weeks on six hours a night impair attention as much as two "
              "nights awake, and the sleepers do not know it. Cueing a memory in deep sleep strengthens it a "
              "little; what dreams are for is open. Hormones are a broadcast: the stress loop's product shuts "
              "off its own source, unless the brake is worn. A drug mimics a transmitter, blocks its receptor, "
              "keeps it in the gap or turns the receptor up; occupancy follows one formula, which also explains "
              "why caffeine has a half-life and alcohol does not. And the body answers back: an opposing "
              "process that grows with use is tolerance while the drug is there and withdrawal when it is gone, "
              "and part of it is learned, so the same dose in a new room kills twice as many rats.",
        handoff="The retina and its cells are Part 13; conditioning, and the room that switches on tolerance, is "
                "Part 16; reward and what drugs take over is Part 17; consolidation is Part 20; arousal and the "
                "opponent process come back in Part 28; adolescence and the late clock in Part 31; depression, "
                "the stress loop and addiction in Parts 40 and 41; whether drugs and therapies work in Part 42.",
        outside="Part 2's random assignment, Part 4's effect sizes and shrinking effects, Part 6's synapse and "
                "Part 7's double dissociation and hippocampus. The clock is two differential equations used as "
                "a tool; exponentials and logarithmic axes are assumed.",
        objectives={
            "U": ["Say what shows that the body keeps time by itself, where the clock is, and how light sets it.",
                  "Describe the stages of a night's sleep and what the two-process model adds to them.",
                  "Name four ways a drug can change a synapse, and what tolerance and withdrawal have in common."],
            "M": ["Compute a clock's daily drift, a chronotype and a social jetlag.",
                  "Work the two-process model by hand: the pressure after a time awake, and the sleep that "
                  "removes it.",
                  "Use the occupancy formula with and without a blocker, and do half-life arithmetic for "
                  "repeated doses."],
            "D": ["Explain from the phase response curve why evening light delays the clock and morning light "
                  "advances it, and what that implies for a traveller or a shift worker.",
                  "Explain why a feedback loop whose product inhibits its source returns to rest, and what "
                  "changes when the inhibition weakens."],
            "I": ["Read a claim about sleep and health and say whether sleep was assigned or only observed.",
                  "Plan the timing of light, sleep and caffeine for a given schedule, and say what the models "
                  "do not cover."],
        },
        results=[
            ("The clock's drift", r"\tau-24\ \text{h}=0.18\ \text{h}\approx 11\ \text{min a day}"),
            ("Sleep pressure", r"S_{\text{awake}}(t)=1-(1-S_{0})\,e^{-t/18.2},\qquad S_{\text{asleep}}(t)=S_{0}\,e^{-t/4.2}"),
            ("Chronotype and social jetlag", r"\text{midsleep}=\text{onset}+\tfrac12\,\text{duration},\qquad "
                                             r"\text{jetlag}=\lvert\text{midsleep}_{\text{free}}-\text{midsleep}_{\text{work}}\rvert"),
            ("Receptor occupancy", r"p=\frac{D}{D+K},\qquad p=\frac{D}{D+K\,(1+B/K_{B})}\ \text{with a blocker}"),
            ("Half-life", r"C(t)=C_{0}\,2^{-t/t_{1/2}}"),
            ("What is felt", r"\text{effect}=a(t)-b(t)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's body module", "explainer/psychology/psyche/body.py"),
              ("Its tests", "tests/psychology/test_body.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
]
