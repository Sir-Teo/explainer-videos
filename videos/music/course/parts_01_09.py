"""Act I, Sound (Parts 1-9): the course entries."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=1, level="U", widget="pluckedstring",
        question="Why does a stretched string have a pitch, and why does one string sound like several notes at once?",
        story="The part opens on the Tune's first two notes, a fifth, and on the legend of Pythagoras and the "
              "blacksmith's hammers, which is false: a string under twice the weight rises by half an octave, as "
              "Vincenzo Galilei found and as the simulated string confirms. The monochord's ratios are true, and "
              "Mersenne's laws say what sets the pitch; twenty-four simulated strings obey them. A bump on a rope "
              "shows that the pitch is the number of round trips a wave makes each second. Newton's law for one "
              "bead on a thread becomes the wave equation, and its two solutions, d'Alembert's travelling shapes "
              "and Bernoulli's standing modes, turn out to be one motion, after a quarrel that Fourier settled. A "
              "plucked string then contains mode n in the amount sin(n pi beta)/n squared, so one string is "
              "already a chord, and strings in simple ratios share partials: a first answer to Pythagoras. The "
              "part ends with real strings, which fade, are stiff and stretch, and with the Tune played on one "
              "simulated string.",
        handoff="Modes and harmonics become the spectrum of Part 3 and the consonance curves of Part 5; beats "
                "return when Part 6 tunes a keyboard; stiffness returns as the piano's stretched octaves in Parts "
                "6 and 7. The bead simulation is how Parts 7 to 9 build every instrument, and d'Alembert's two "
                "travelling waves are the digital waveguide of Part 52. Monochord, the Chain and the Tune, "
                "introduced here, run through the whole series.",
        outside="School algebra and trigonometry. The derivation of the wave equation uses a second derivative; "
                "the film says what it means as it goes. No earlier part is needed.",
        objectives={
            "U": ["Compute a string's frequency from its length, tension and mass per metre, and say what each change does to the pitch.",
                  "Name the octave, fifth and fourth by ear and by ratio, and multiply ratios to add intervals.",
                  "Explain why two strings in the ratio 3 to 2 share every third and every second partial."],
            "M": ["Derive the wave equation from Newton's law for one bead and take the limit of small beads.",
                  "Show that f(x - ct) + g(x + ct) solves it, and that fixed ends force the period 2L/c.",
                  "Compute the modal amplitudes of a plucked string and predict which partials are missing."],
            "D": ["Explain why a string's tension rises with its amplitude and estimate the resulting pitch glide.",
                  "State what an exactly conserved discrete energy guarantees about a numerical scheme.",
                  "Say why uniform stretching cannot regenerate a missing mode, and what in a real instrument can."],
            "I": ["Choose a plucking or striking point for a wanted tone, and explain touched harmonics.",
                  "Explain to an instrument maker why bass strings are wound and why short thick strings sound inharmonic."],
        },
        results=[
            ("Mersenne's law", r"f_1 = \frac{1}{2L}\sqrt{\frac{T}{\mu}}"),
            ("The wave equation", r"\frac{\partial^2 u}{\partial t^2} = c^2\,\frac{\partial^2 u}{\partial x^2},\qquad c = \sqrt{T/\mu}"),
            ("d'Alembert's solution", r"u(x,t) = f(x - ct) + g(x + ct)"),
            ("Modes of a fixed string", r"u_n = \sin\frac{n\pi x}{L}\,\cos 2\pi f_n t,\qquad f_n = n f_1"),
            ("The plucked string", r"a_n = \frac{2h}{\pi^2\beta(1-\beta)}\cdot\frac{\sin n\pi\beta}{n^2}"),
            ("A stiff string", r"f_n = n f_1\sqrt{1 + B n^2}"),
        ],
        U=(0, 1, 2, 3, 6, 9, 10),
        D=(12,),
        I=(8, 11),
        also=(("Monochord's string: beads, d'Alembert and modes", "explainer/music/monochord/physics/string.py"),
              ("The sound check: the series' audio pipeline", "videos/music/soundcheck/README.md")),
    ),
]
