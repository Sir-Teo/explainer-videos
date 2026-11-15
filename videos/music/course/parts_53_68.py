"""Acts IX (end) to XII: Parts 53 onwards as they are built (see ``videos/music/course/__init__.py``)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=53, level="U", widget="midi", prereq=(10, 11, 48, 51, 52),
        question="How does a few pages of 1983 specification carry music between machines, and what must an engine do to play it in real time?",
        story="In January 1983 a Prophet-600 and a Jupiter-6 were joined by a five-pin cable; MIDI 1.0 has run the industry since. An ear question hears a twelve-note chord as the cable delivers it, the last note 7.0 ms after the first, against all at once. Machines that play: the Banu Musa's pinned cylinder, the music box (heard), player-piano rolls (forty notes a second, heard), Nancarrow's tempo canons and their arithmetic. MUSIC N's orchestra and score from unit generators (heard), and real time arriving. MIDI byte by byte: ten bits a byte at 31,250 baud (320 microseconds), status and data bytes, running status (42 bytes to 29 for the Tune's first phrase), a chord's smear against its size (16 notes: 15.4 ms plain, 10.6 running). Seven-bit controllers zip (31-cent steps; an ear question); one bend per channel; MPE (2018) and MIDI 2.0 (2020). A Standard MIDI File of the whole Tune: 423 bytes against 6.9 MB of audio, read back exactly; variable-length times and the tempo map. Step sequencers (a sixteen-step line, heard), piano rolls and trackers; a pattern language parsed into a tree (heard) and live coding. An engine of stateful voices, limiters and delays renders bit-identically in blocks of 32 to 2048; small blocks cost more (11 per cent load at 32, 2 at 2048); missed deadlines click (heard); notes snapped to blocks land up to 21 ms early (an ear question) where sample-accurate scheduling is exact; a lock-free queue; the processing graph, plug-ins, and delay compensation, whose absence combs a parallel path (5 ms late: notches every 200 Hz from 100, heard). The Tune as a tracker module and a tempo canon at 3 : 4 : 5 : 6 meeting after 30.7 s.",
        handoff="Microphones and loudspeakers in Part 54; the session in Part 56; latency on stage in Part 59; transcription "
                "back to MIDI in Part 61; MIDI corpora for composing machines in Part 65.",
        outside="Part 10 for notation and the piano roll; Part 11 for meter; Part 44 for chip music; Part 48 for sampling; "
                "Parts 51 and 52 for the voices. Serial communication, binary and hexadecimal, graphs and topological "
                "order, threads and queues.",
        objectives={
            "U": ["Hear a chord smeared by the cable, a music box, a player-piano roll and a MUSIC-style orchestra.",
                  "Hear zipper noise from a 7-bit controller, a sixteen-step bass line and a two-line pattern.",
                  "Hear missed deadlines, notes snapped to blocks, and a parallel path combing without delay compensation."],
            "M": ["Encode and decode MIDI 1.0 with running status, and time a message on the wire.",
                  "Write and read a Standard MIDI File with variable-length times and a tempo; parse a pattern language.",
                  "Build an engine that renders identically in any block size, schedules to the sample and compensates latency."],
            "D": ["Find the best-sounding neural effect that is guaranteed never to miss an audio deadline."],
            "I": ["Choose a block size, use delay compensation and MPE, and keep the audio thread free of locks and allocation."],
        },
        results=[
            ("A byte on the wire", r"10 / 31\,250 \text{ s} = 320\ \mu s"),
            ("Note on", r"\texttt{9n kk vv}"),
            ("Ticks to seconds", r"t = \text{ticks} \times \text{tempo} / (\text{division} \times 10^6)"),
            ("Deadline", r"\text{block} / f_s"),
            ("Tempo canon", r"s_v = T - b_K / r_v"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7),
        D=(11,),
        I=(5, 8, 9, 10),
        also=(("Monochord's studio: MIDI bytes and files, the engine, patterns, trackers, tempo canons", "explainer/music/monochord/daw.py"),),
    ),
    Part(
        n=54, level="U", widget="box", prereq=(2, 4, 8, 48, 49),
        question="How do microphones turn air into voltage and loudspeakers turn it back, and what does each leave out?",
        story="Headphones plugged into a microphone socket work: a dynamic transducer runs both ways (e = Bl v, F = Bl i), and an ear question hears one used as a microphone, dull above its resonance. Electrical recording (1925) made the crooner. Dynamic, condenser, ribbon and electret transducers; electrical, mechanical and acoustical circuits. Pressure is omnidirectional, its gradient a figure-8, and A + (1 - A) cos theta makes the family (the hypercardioid's 6.0 dB is the most directional); an ear question hears a piano behind a singer through three patterns (the cardioid 30 dB down). A gradient microphone's bass rises near a point source (1 + 1/(jkr): +20.8 dB at 100 Hz at 5 cm, heard). Thermal noise (-129.7 dBu for 200 ohms) puts a dynamic microphone's floor near 16 dB SPL; a balanced line with 1 per cent imbalance drops hum 40 dB (heard). A woofer's Thiele-Small parameters, a lumped-element simulator of baffle, sealed and vented boxes checked against Small's and Thiele's closed forms (to a tenth of a hertz; B4 flat to 40 Hz), impedance curves, efficiency and the iron law; three loudspeakers heard (phone 844 Hz, bookshelf 98, floor-stander 39). Horns as transformers; crossovers (Butterworth's hole and bump, Linkwitz-Riley flat); amplifier classes. Headphones and a filtered-x LMS canceller (-33 dB below 200 Hz, none above 2 kHz, heard). Arrays steer (eight microphones reject a second singer 6 dB, an ear question); small speakers are linearized.",
        handoff="The loudspeaker in a room, stereo and binaural sound in Part 55; microphone choice and gain staging in Part 56; "
                "feedback and line arrays in Part 59; arrays in source separation in Part 64.",
        outside="Part 2 for spherical waves and the Helmholtz resonator; Part 4 for the missing fundamental; Part 8 for the "
                "voice; Part 48 for delta-sigma; Part 49 for filters and sweeps. Circuit analysis, complex impedance, "
                "least squares.",
        objectives={
            "U": ["Hear a headphone used as a microphone, three patterns with a piano behind the singer, and a walk round a cardioid.",
                  "Hear the proximity effect at three distances, hum on an unbalanced and a balanced line, and a crossover's hole.",
                  "Hear a groove through three loudspeakers, a cabin with noise cancelling off and on, and an array steered."],
            "M": ["Derive the first-order patterns, their directivity and nulls, and the proximity effect's 1 + 1/(jkr).",
                  "Simulate a driver in sealed and vented boxes from Thiele-Small parameters and check against Small and Thiele.",
                  "Compute thermal noise, balanced-line rejection, crossover sums, an FxLMS canceller and a delay-and-sum array."],
            "D": ["Find how much louder and deeper a small speaker can be made to sound, safely, by control alone."],
            "I": ["Choose and place microphones by pattern and proximity, design a box by its parameters, and use balanced lines."],
        },
        results=[
            ("Patterns", r"r(\theta) = A + (1 - A)\cos\theta, \quad DF = 1/(A^2 + (1 - A)^2/3)"),
            ("Proximity", r"|1 + 1/(jkr)| = \sqrt{1 + 1/(kr)^2}"),
            ("Thermal noise", r"v_n = \sqrt{4kTRB}"),
            ("Sealed box", r"f_c = f_s\sqrt{1 + V_{as}/V_b}, \ Q_{tc} = Q_{ts}\sqrt{1 + V_{as}/V_b}"),
            ("Efficiency", r"\eta_0 = (4\pi^2/c^3)\, f_s^3 V_{as}/Q_{es}"),
        ],
        U=(0, 1, 2, 3, 4, 7, 10),
        D=(11,),
        I=(5, 6, 8, 9),
        also=(("Monochord's transducers: patterns, proximity, noise, lines, the loudspeaker simulator, crossovers, a canceller, arrays", "explainer/music/monochord/transducer.py"),),
    ),
    Part(
        n=55, level="U", widget="room", prereq=(2, 4, 49, 54),
        question="Why does one room make music sound glorious and another make speech a blur, and how can space be built back for two ears?",
        story="In 1895 Harvard opened a lecture room nobody could understand; Wallace Sabine timed an organ pipe's decay by night, carried in Sanders Theatre's cushions, found the law, and designed Boston's Symphony Hall (1900). An ear question hears the room as built (5.6 s) and cured (1.1 s); Philharmonic Hall (1962) shows one number is not enough. Sabine's law derived from a diffuse field (T60 = 0.161 V/A), 300 and 1,500 cushions heard, Eyring's correction, absorption by band, targets by use. A living room's 18 modes below 120 Hz against Weyl's 20.2, the Schroeder frequency (305 Hz in the room, 20 in a hall), a bass line in a corner and in the middle (heard), and what can be done. Porous, panel and Helmholtz absorbers; a flutter echo (35 ms) scattered (heard); Schroeder's quadratic-residue diffuser (n^2 mod 7), Gauss's sum and computed scattering (diffusion 0.39 against a flat panel's 0.07 at 1 kHz). Early reflections, the precedence effect and clarity; the lateral fraction (Barron and Marshall) falling from 0.20 to 0.11 as a hall widens; an ear question on two halls; shoebox, fan, vineyard and surround halls. Simulation: image sources (833 to the eighth order), checked against Sabine and Eyring (a smooth box rings 14 per cent long: it is not diffuse) and against the exact modes (within 0.4 Hz); rays, waves and auralization. Hearing direction: the duplex theory, Woodworth's ITD (656 microseconds), Brown and Duda's head shadow, the cues heard apart and together, and the cone of confusion (an ear question with no answer: front and back identical round a sphere). Stereo from Ader and Blumlein, the tangent law (13.4 degrees for a half pan), linear and constant-power laws heard, the sweet spot, microphone pairs. Ambisonics: B-format, a ring decoder, Gerzon's rV and rE (2/3 basic, 0.707 max-rE), higher orders; wave-field synthesis. Binaural rendering: HRTFs, a block renderer, a shaker circling the head (heard), externalization, head tracking, crosstalk cancellation. Object audio and VBAP; personal HRTFs and real-time waves. The Tune in four spaces, then circling the listener.",
        handoff="Stereo pairs, panning, depth and width in Part 56; the listener's room in Part 57; halls, feedback and "
                "arrays in Part 59; spatial cues in source separation in Part 64; learned rooms in Part 66.",
        outside="Part 2 for standing waves and the finite-difference simulator; Part 4 for the ear; Part 49 for "
                "convolution, image sources and reverberators; Part 54 for patterns and arrays. Exponential decay, "
                "Fourier series, a little number theory, two-by-two matrices.",
        objectives={
            "U": ["Hear a lecture room before and after its cure, a bass line in a corner and in the middle, and a flutter echo diffused.",
                  "Hear two halls that differ only in width, and noise placed by time differences, level differences and both.",
                  "Hear a voice at 30 degrees and at 150 degrees round a sphere, two pan laws, and a shaker circling the head."],
            "M": ["Derive Sabine's law from a diffuse field, add Eyring's correction, and check an image-source room against both.",
                  "Count a room's modes against Weyl's formula, find the Schroeder frequency, and prove a residue diffuser's Gauss sum.",
                  "Compute interaural cues, the tangent law, Ambisonic decoders with Gerzon's vectors, and a binaural renderer."],
            "D": ["Find the least a renderer must know about a listener's ears to render space as well as their own HRTF."],
            "I": ["Choose reverberation for a use, treat modes and reflections, and pan, decode and render space for any playback."],
        },
        results=[
            ("Sabine and Eyring", r"T_{60} = 0.161\,\frac{V}{A}, \quad T_{60} = \frac{0.161\,V}{-S\ln(1 - \bar\alpha)}"),
            ("Modes", r"f = \frac{c}{2}\sqrt{(n_x/L_x)^2 + (n_y/L_y)^2 + (n_z/L_z)^2}, \quad N(f) \approx \frac{4\pi V f^3}{3c^3}"),
            ("Schroeder frequency", r"f_S = 2000\sqrt{T_{60}/V}"),
            ("Gauss's sum", r"\Bigl|\sum_{n=0}^{N-1} e^{2\pi i (n^2 + kn)/N}\Bigr| = \sqrt{N}"),
            ("Woodworth", r"\Delta t = \frac{a}{c}(\theta + \sin\theta)"),
            ("Tangent law", r"\frac{\tan\varphi}{\tan\varphi_0} = \frac{g_R - g_L}{g_R + g_L}"),
        ],
        U=(0, 1, 2, 4, 6, 7, 9),
        D=(11,),
        I=(3, 5, 8, 10),
        also=(("Monochord's spaces: modes, Sabine, diffusers, image sources, the head, panning, Ambisonics, a binaural renderer", "explainer/music/monochord/space.py"),),
    ),
]
