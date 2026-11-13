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
    Part(
        n=3, level="U", widget="fouriersum",
        question="Can every sound be taken apart into pure tones, what does the taking apart cost, and is the list "
                 "of pure tones everything there is to a sound?",
        story="In 1807 the Paris Academy would not print Fourier's claim that any curve is a sum of sines; Lagrange "
              "objected that smooth curves cannot make a corner. A square wave assembled one sine at a time shows "
              "what Fourier meant, the coefficients turn out to be averages, and the overshoot at a jump never goes "
              "away. A computer does the same for samples, and since Cooley and Tukey does it fast. Helmholtz tested "
              "Ohm's law of hearing with resonators, each one a bottle from Part 2, and a bank of them on our string "
              "agrees with the transform. Phase turns out to matter only where the ear cannot separate the partials. "
              "To watch a recipe change one needs a window, which costs leakage, and behind the window stands "
              "Gabor's limit: no sound is both short and narrow in frequency. A constant-Q ruler suits music better "
              "than equal bins; noise has a spectrum that must be averaged. Then the test of Helmholtz's second "
              "claim: one pluck played backwards has exactly the same spectrum and is a different instrument. "
              "Timbre is a recipe that changes in time. The Tune is assembled from pure tones.",
        handoff="The spectrogram is in almost every later part. Resonators, phase and the tone with no fundamental "
                "open Part 4, on the ear. Brightness, attack and flux return in consonance (Part 5), orchestration "
                "(Part 41) and synthesis (Parts 51, 52). The fast transform, windows and overlap-add are the basis "
                "of digital audio (Part 48), effects (Parts 49, 50) and codecs (Part 58); constant Q is the input of the "
                "listening machines of Parts 61 and 62.",
        outside="Parts 1 and 2 for partials, modes and resonators. Sines and cosines; an integral as an average. "
                "Complex exponentials appear once, in the definition of the DFT, and the film says what they mean.",
        objectives={
            "U": ["Read a spectrum and a spectrogram: partials, onsets, glides, noise.",
                  "Say what a window does to a spectrum and why a short sound cannot have a sharp pitch.",
                  "Explain why two sounds with the same spectrum can sound different, and name what else matters."],
            "M": ["Compute Fourier coefficients as projections and explain the Gibbs overshoot.",
                  "State the DFT, the idea and cost of the FFT, and the meaning of a bin.",
                  "State Gabor's uncertainty relation and choose a window length for a given task."],
            "D": ["Describe reassignment and when it sharpens a time-frequency picture.",
                  "Explain why human listeners can beat the uncertainty limit without contradiction."],
            "I": ["Choose a window and a bin width before trusting a spectrum analyser.",
                  "Use a constant-Q or mel picture as the input to a music-analysis task.",
                  "Shape a sound's identity by its attack rather than by its steady spectrum."],
        },
        results=[
            ("Fourier's recipe", r"b_n = \frac{2}{T}\int_0^T f(t)\,\sin\frac{2\pi n t}{T}\,dt"),
            ("The discrete Fourier transform", r"X[k] = \sum_{n=0}^{N-1} x[n]\,e^{-2\pi i k n / N}"),
            ("The Gibbs overshoot", r"\approx 8.95\%\ \text{of the jump, for any number of terms}"),
            ("Gabor's limit", r"\Delta t \cdot \Delta f \ge \frac{1}{4\pi}"),
            ("Constant Q", r"Q = \frac{f}{\Delta f} = \frac{1}{2^{1/b} - 1}\quad (b\ \text{bins per octave})"),
            ("Noise colours", r"S(f) \propto f^{-\beta}:\ \beta = 0\ \text{white},\ 1\ \text{pink},\ 2\ \text{brown}"),
        ],
        U=(0, 1, 3, 4, 5, 9, 10),
        D=(11,),
        I=(2, 6, 7, 8),
        also=(("Monochord's analysis: FFT, windows, STFT, constant Q, reassignment", "explainer/music/monochord/dsp/fourier.py"),),
    ),
    Part(
        n=4, level="U", widget="missingfund",
        question="What does the ear do to a sound before you hear it: how does it sort frequencies, how loud is loud, "
                 "and where does a note's pitch come from?",
        story="In 1978 David Kemp put a microphone in an ear canal and recorded the ear sending sound back; thirty "
              "years earlier Thomas Gold had argued that the inner ear must contain an amplifier, against Békésy, "
              "whose Nobel-winning travelling waves were seen in the ears of cadavers. The part follows a sound in. "
              "The middle ear is a transformer that matches air to fluid, and the ear canal a quarter-wave pipe "
              "from Part 2. In a model cochlea a wave travels along the membrane and stops where the membrane's own "
              "note matches it, so that equal ratios of frequency are equal distances. Fletcher's experiment gives "
              "the width of the ear's filters: a little over a whole tone, wider in the bass, so the first eight "
              "partials of a note are heard singly and the rest as a crowd. Loudness is not pressure (ten times the "
              "power is twice as loud), and a loud sound hides its neighbours. The nerve also carries timing, up to "
              "a few thousand hertz, and from timing comes pitch: a note keeps its pitch without its fundamental, "
              "follows Schouten's shift, and stops being a note where the piano stops. Shepard's endless scale "
              "separates chroma from height. A chapter without sound works out a safe dose. At the frontier the "
              "outer hair cells turn out to be Gold's amplifier: sharp, compressive, and audible as a third tone "
              "that the ear adds to two. The Tune is played with no fundamentals, and then with no octaves.",
        handoff="Critical bands, beats and roughness are the foundation of consonance (Part 5) and tuning (Part 6). "
                "The pitch the ear supplies becomes the root of a chord (Part 13). Masking returns in orchestration "
                "(Part 41), mixing (Part 56) and audio coding (Part 58); phons, sones and weighting in mastering "
                "(Part 57). The autocorrelation pitch model is the starting point of transcription (Part 61), and "
                "chroma the representation of Part 62.",
        outside="Parts 1 to 3: partials, pipes and impedance, the spectrum and the spectrogram. Decibels and "
                "logarithms. A mass on a spring and its resonance.",
        objectives={
            "U": ["Trace a sound from the ear canal to the auditory nerve and say what each stage does.",
                  "Explain the cochlea's place map, a critical band, and why a note keeps its pitch without its fundamental.",
                  "Work out a safe listening time from a level in dBA."],
            "M": ["Compute the middle ear's pressure gain and the power transmitted with and without it.",
                  "Use the ERB formula to decide which partials of a note are resolved, and read a masked threshold.",
                  "Describe the autocorrelation model of pitch and what it predicts for a shifted complex."],
            "D": ["Explain why an oscillator at a Hopf bifurcation compresses, sharpens and distorts.",
                  "Describe cochlear synaptopathy and why an audiogram does not show it.",
                  "Say what a cochlear implant removes from the two codes of pitch."],
            "I": ["Read levels in dBA, phons and sones, and know which one a meter shows.",
                  "Use masking to decide what in a mix or a codec can be dropped or must be moved.",
                  "Imply a bass note with its partials on a system that cannot reproduce it."],
        },
        results=[
            ("The middle ear", r"\frac{p_\text{window}}{p_\text{drum}} = \frac{A_\text{drum}}{A_\text{stapes}}\times\text{lever} \approx 22\ (27\ \text{dB})"),
            ("The ear's filter (Glasberg and Moore)", r"\text{ERB}(f) = 24.7\,\bigl(4.37\,f_\text{kHz} + 1\bigr)\ \text{Hz}"),
            ("Stevens's law", r"\text{loudness} \propto \text{power}^{0.3}:\quad +10\ \text{dB} = \times 2"),
            ("Pitch as a period", r"\text{pitch} = 1 / \arg\max_\tau \sum_\text{bands} r_\text{band}(\tau)"),
            ("A safe dose (NIOSH)", r"T = \frac{8\ \text{h}}{2^{(L - 85)/3}}"),
            ("At the edge of oscillation", r"\text{response} \propto \text{force}^{1/3}"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, 8, 9),
        D=(11,),
        I=(5, 10),
        also=(("Monochord's ear: middle ear, cochlea, auditory filters, loudness, masking, pitch", "explainer/music/monochord/ear.py"),),
    ),
    Part(
        n=5, level="U", widget="dissonance",
        question="Why do some notes belong together: is it number, beating, fusion, or habit, and can the answer be "
                 "computed?",
        story="A timbre is played in which an exact octave grinds and one eighty-four cents too wide is smooth. Six "
              "answers to why some notes belong together are then computed in turn. Pythagoras's small ratios and "
              "Euler's formula of 1739 rank the intervals almost as musicians do, and are defeated by a fifth five "
              "cents wide, whose ratio is enormous and whose sound is hardly changed. Galileo's coinciding pulses "
              "turn out to be the same arithmetic, and a rhythm of three against two, played a hundred times "
              "faster, becomes a fifth. Two close tones beat at the difference of their frequencies, which is how "
              "tuners work; beats too fast to follow are roughness, and Helmholtz made roughness the cause of "
              "dissonance. Plomp and Levelt measured it in 1965: worst a quarter of a critical band apart, and for "
              "pure tones indifferent to ratios. Summed over the partials of two notes, their curve has valleys "
              "exactly at the just ratios, and Sethares's stretched partials move the valleys, which explains the "
              "opening. Stumpf's fusion, Rameau's fundamental bass and Part 4's pitch model give a second cause, "
              "harmonicity, which separates the major from the minor triad where roughness cannot. The Tsimane' "
              "show that the preference itself is learned. The frontier is a composite model and a quarter of a "
              "million judgments collected online. The Tune is played in a bent timbre, in intervals that only "
              "that timbre makes smooth.",
        handoff="Beats, and valleys that tolerate small errors, are the whole basis of tuning (Part 6). Inharmonic "
                "partials and their scales return with stiff strings (Part 7), bells (Part 9), the gamelan (Part 36) "
                "and synthesis (Part 52). The fundamental bass becomes the theory of chords and progressions (Parts "
                "13 and 18); the treatment of dissonance is counterpoint (Parts 16 and 17). What is learned returns "
                "in expectation (Part 46) and in the musics of the world (Parts 34 to 37, 47).",
        outside="Parts 1, 3 and 4: partials, the spectrum, critical bands and the pitch of a set of partials. Ratios "
                "and prime factors. The sum-to-product identity for two sines.",
        objectives={
            "U": ["Name the just ratios of the consonant intervals and say what Pythagoras, Galileo and Euler claimed.",
                  "Explain beats and use them to tune one note to another.",
                  "Say why consonance depends on timbre, and why a major and a minor triad differ."],
            "M": ["Compute Euler's gradus and the beat rate of two tones.",
                  "Compute a dissonance curve from Plomp and Levelt's curve and a set of partials, and find its minima.",
                  "Find the fundamental bass of a chord of exact ratios and relate it to harmonicity."],
            "D": ["Compare interference, harmonicity and familiarity as predictors of consonance ratings.",
                  "Describe what cross-cultural and large online experiments have and have not settled."],
            "I": ["Voice chords for smoothness: wide in the bass, and aware of each instrument's partials.",
                  "Design a scale for an inharmonic timbre, or a timbre for a given scale.",
                  "Diagnose roughness between two parts in a mix as competition inside a critical band."],
        },
        results=[
            ("Euler's gradus", r"\Gamma(p{:}q) = 1 + \sum_i k_i\,(p_i - 1),\quad \operatorname{lcm}(p,q) = \prod_i p_i^{k_i}"),
            ("Beats", r"\sin 2\pi f_1 t + \sin 2\pi f_2 t = 2\cos\bigl(\pi(f_1 - f_2)t\bigr)\,\sin\bigl(\pi(f_1 + f_2)t\bigr)"),
            ("Roughness of two pure tones", r"d(f_1,f_2) = e^{-3.5\,s\,\Delta f} - e^{-5.75\,s\,\Delta f},\quad s = \frac{0.24}{0.0207\,f_1 + 18.96}"),
            ("A dissonance curve", r"D(r) = \sum_{i<j} \min(a_i, a_j)\; d(f_i, f_j)\ \text{over the partials of both tones}"),
            ("Stretched partials", r"f_k = f_1\,k^{\log_2 A}\ \Rightarrow\ \text{valleys at } r^{\log_2 A}"),
            ("The fundamental bass", r"4{:}5{:}6 \to \tfrac14 f,\qquad 10{:}12{:}15 \to \tfrac{1}{10} f"),
        ],
        U=(0, 1, 2, 3, 5, 7, 8),
        D=(10,),
        I=(4, 6, 9),
        also=(("Monochord's consonance: ratios, beats, roughness, dissonance curves, harmonicity", "explainer/music/monochord/consonance.py"),),
    ),
    Part(
        n=6, level="U", widget="temperament",
        question="If the pure intervals cannot all be had at once, where should an instrument put the error, and why "
                 "did the world settle on twelve equal steps?",
        story="A progression of four chords is sung four times in perfectly pure chords, and ends most of a semitone "
              "flat. The cause is arithmetic. Twelve pure fifths overshoot seven octaves by the Pythagorean comma, and "
              "no stack of fifths can ever close, because no power of three is a power of two; four pure fifths "
              "overshoot a pure third by the syntonic comma; three pure thirds fall short of an octave. Pythagorean "
              "tuning keeps eleven fifths pure and pays with a wolf and restless thirds. Just intonation, laid out as "
              "a lattice of fifths and thirds, makes chords pure, needs two versions of some notes, and drifts by a "
              "comma each time round the pump. Then three ways of tempering. Quarter-comma meantone narrows each "
              "fifth until the thirds are pure in eight keys, and leaves a wolf in the others. Werckmeister's well "
              "temperament closes the circle and grades the error, so that every key is usable and each has its own "
              "character: the tuning of Bach's title. Equal temperament, computed by Zhu Zaiyu in 1584 to "
              "twenty-four decimal places, makes every key the same, with thirds fourteen cents wide; it is tuned by "
              "counting beats and laid out on every guitar's frets. Twelve is the denominator of the best small "
              "fraction for a fifth; nineteen, thirty-one and fifty-three do better and are harder to play. Pianos "
              "stretch their octaves because their strings are stiff, and voices and strings adjust every note. The "
              "Tune is played with chords in eight tunings.",
        handoff="The stretched octave returns with the piano's string (Part 7). The twelve notes become scales and "
                "keys (Parts 12 and 15); the lattice of fifths and thirds returns as a map of chords (Parts 13, 31 "
                "and 32). Commas and continued fractions return when scales are treated as mathematics (Part 33). "
                "Other divisions of the octave belong to raga, maqam and gamelan (Parts 34 to 36), and tuning "
                "tables to synthesizers and MIDI (Parts 50 and 53).",
        outside="Part 1 for ratios and stiff strings; Part 5 for beats and for why the just ratios are smooth. "
                "Fractions, powers and logarithms; cents.",
        objectives={
            "U": ["Explain the Pythagorean and syntonic commas and why no chain of pure fifths closes.",
                  "Describe Pythagorean tuning, just intonation, meantone, a well temperament and equal temperament by what each keeps pure.",
                  "Say what equal temperament costs, and how a tuner sets it."],
            "M": ["Compute any note of a tuning in cents and in hertz, and the beat rate of an interval.",
                  "Follow a comma pump in exact fractions and predict its drift.",
                  "Use the continued fraction of log2(3/2) to explain 12, 41 and 53."],
            "D": ["Describe adaptive tuning and the trade it makes between purity and stability.",
                  "Weigh the evidence for and against a proposed historical temperament."],
            "I": ["Choose a temperament for a repertoire, and retune an instrument or a synthesizer to it.",
                  "Place frets, or check a guitar's intonation, from the twelfth root of two.",
                  "Tune held chords in an ensemble: thirds low, and the pitch anchored."],
        },
        results=[
            ("The Pythagorean comma", r"\frac{(3/2)^{12}}{2^{7}} = \frac{531441}{524288}\quad (23.46\ \text{cents})"),
            ("The syntonic comma", r"\frac{(3/2)^{4}}{4}\Big/\frac54 = \frac{81}{80}\quad (21.51\ \text{cents})"),
            ("Quarter-comma meantone", r"\text{fifth} = \sqrt[4]{5} = 696.6\ \text{cents};\quad \text{wolf} = 737.6"),
            ("Equal temperament", r"f_k = f_0\,2^{k/12},\qquad 2^{1/12} = 1.0594630943\ldots"),
            ("Beats of a tempered interval", r"\text{beats} = \lvert\, q f_\text{high} - p f_\text{low} \rvert \quad (\text{nearly } p{:}q)"),
            ("Why twelve", r"\log_2\tfrac32 = [0;1,1,2,2,3,\ldots]:\ \tfrac12,\ \tfrac35,\ \tfrac7{12},\ \tfrac{24}{41},\ \tfrac{31}{53}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6),
        D=(10,),
        I=(7, 8, 9),
        also=(("Monochord's tunings: commas, temperaments, beats, the comma pump, stretched octaves", "explainer/music/monochord/tuning.py"),),
    ),
]
