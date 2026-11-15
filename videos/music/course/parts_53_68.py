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
]
