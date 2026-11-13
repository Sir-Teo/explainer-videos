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
]
