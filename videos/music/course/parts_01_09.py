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
    Part(
        n=2, level="U", widget="bottle",
        question="What is it that travels from an instrument to your ear, how fast, and why does it bend round "
                 "walls, hum in a bottle and drop in pitch as it passes?",
        story="Krakatoa's explosion in 1883 was heard 4,800 kilometres away four hours later, and barographs caught "
              "its pressure pulse circling the planet at the speed of sound. Boyle's jar shows that sound needs "
              "air; a row of simulated parcels shows that what travels is a push, not the air. The speed comes out "
              "of the gas law: Newton's value is 15 percent short, Laplace's adiabatic correction repairs it, and "
              "parcels given each law run at 280 and 331 metres a second. Loudness is counted in decibels, and ten "
              "strings are ten decibels more than one, on average. Sound spreads by the inverse-square law; its "
              "wavelength decides whether it bends round a wall (the simulation lands within two decibels of "
              "Maekawa's chart) and stripes the space between two sources. A pipe has the notes n c/2L or "
              "(2n-1) c/4L, a bottle is a mass on a spring, a flare hands sound to the air where a sudden opening "
              "throws it back, and a passing source glides in pitch. The frontier is sound loud enough to steepen "
              "into shocks, as in a trombone. The Tune is played on six bottles tuned by their water.",
        handoff="The decibel returns in Part 4 (what the ear makes of it) and Part 57 (meters). Pipes, end "
                "corrections and odd partials are Part 8; the Helmholtz resonator is inside the guitar of Part 7 "
                "and the loudspeaker port of Part 54; impedance explains soundboards (Part 7) and the middle ear "
                "(Part 4). The 2-D simulator returns for drums (Part 9) and rooms (Part 55), and the question the "
                "part ends on, whether every sound can be taken apart into partials, is Part 3.",
        outside="Part 1 for waves, modes and the wave equation. School physics: pressure, density, the gas law. "
                "Logarithms for the decibel.",
        objectives={
            "U": ["Say what moves and what travels in a sound wave, and how small the motion is at ordinary levels.",
                  "Convert between pressure, intensity and decibels, and apply +3, +6, +10 dB and the inverse-square law.",
                  "Compute a wavelength and predict whether an obstacle will shadow a sound or be bent round."],
            "M": ["Derive the speed of sound from the adiabatic gas law and explain Newton's 15 percent error.",
                  "Derive the resonances of open and stopped pipes and Helmholtz's formula for a bottle.",
                  "Compute the reflection at a change of impedance and the Doppler shift of a passing source."],
            "D": ["Explain why a finite-amplitude wave steepens, estimate its shock distance, and state the Fubini solution.",
                  "Describe how nonlinear propagation makes brass brassy, and what thermoacoustics adds."],
            "I": ["Predict how far a pipe goes sharp as it warms, and tune accordingly.",
                  "Estimate the loss behind a barrier from the path difference and the wavelength.",
                  "Explain comb filtering between two loudspeakers and why a horn or a port is an impedance match."],
        },
        results=[
            ("The speed of sound", r"c = \sqrt{\frac{\gamma P}{\rho}} = \sqrt{\gamma R T}"),
            ("Sound level", r"L = 10\log_{10}\frac{I}{I_0} = 20\log_{10}\frac{p}{p_0}"),
            ("The inverse-square law", r"I = \frac{P}{4\pi r^2}"),
            ("Pipes", r"f_n = n\,\frac{c}{2L}\ \text{(open)},\qquad f_n = (2n-1)\,\frac{c}{4L}\ \text{(stopped)}"),
            ("Helmholtz's resonator", r"f = \frac{c}{2\pi}\sqrt{\frac{A}{V L'}}"),
            ("The Doppler shift", r"f' = f\,\frac{c}{c \mp v}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 8, 9),
        D=(12,),
        I=(6, 7, 10, 11),
        also=(("Monochord's air: parcels, sound in a plane, tubes", "explainer/music/monochord/physics/air.py"),),
    ),
]
