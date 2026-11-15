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
]
