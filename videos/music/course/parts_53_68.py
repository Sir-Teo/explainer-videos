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
    Part(
        n=56, level="U", widget="comb", prereq=(4, 49, 50, 54, 55),
        question="How does one multitrack recording become three different pieces of music, and what does a mix engineer actually control?",
        story="Take one multitrack and mix it three ways: an ear question hears close and dry, a wall of sound (crest factor 11 dB against 18) and a dub; Les Paul, Spector, King Tubby and Eno made the studio an instrument. Our session band: Part 8's voice, Part 38's piano, guitar and bass, Part 40's drums, nine tracks. From the horn to the workstation: tracks against years, tape and the razor blade, bouncing, the DAW. Stereo pairs computed: XY, Blumlein, ORTF, NOS and AB turn direction into level and time differences; a trading rule (15 dB or 1.1 ms) gives image positions and recording angles (Blumlein 70 degrees, AB 78, ORTF 109, XY beyond 180); three pairs on one stage heard. Two microphones comb (5.8 ms: notches from 86 Hz); the 3 : 1 rule (+2.5, -3.5 dB); an ear question on a snare's microphones out of polarity (its body 6 dB down). Gain staging from the air to the converter (too low: 54 dB of range; right: 73; too hot: 8 dB past full scale), heard; 24 bits and floating point; reference levels. Editing: comps, a butt splice's click against a crossfade (heard), crossfade laws for related and unrelated takes, timing and pitch. The console: the channel strip, faders, four pan laws in stereo and mono (the -3 dB law's centre +3 dB in mono), our faders. Masking mapped band by band in the manner of an ideal binary mask, carved (the guitar from 49 to 35 per cent masked), heard. A vocal compressor (13 dB of wander to 5), parallel compression (heard), buses and automation. Depth by level, treble, reverberation and pre-delay (heard); mid-side and the Haas trick, wide and then combing in mono (heard). Monitoring: the room, listening level, a phone (the bass's fundamentals 40 dB down, its harmonics carry it, heard), references. Frontier: automatic mixing from Dugan to differentiable consoles; an ear question pits our mix against Monochord's rule-based mixer, whose hi-hat is 8 dB too loud though its masking numbers look fine. The session's first three phrases mixed three ways.",
        handoff="The stereo bus, meters and the loudness war in Part 57; the console on stage in Part 59; unmixing with masks "
                "in Part 64; learned effects and mixes in Part 66; listening tests and their statistics in Part 67.",
        outside="Part 4 for masking, loudness and the missing fundamental; Part 43 for expressive timing; Part 49 for "
                "filters, combs and reverberators; Part 50 for compressors; Part 54 for microphones and the phone's "
                "loudspeaker; Part 55 for stereo and depth. Decibels, sums of delayed signals, a little statistics.",
        objectives={
            "U": ["Hear one session mixed as close and dry, as a wall of sound and as a dub, and three stereo pairs on one stage.",
                  "Hear a snare's microphones in and out of polarity, three gain settings, a splice and a crossfade.",
                  "Hear a rough and a carved mix, parallel compression, three depths, width in mono, and a mix on a phone."],
            "M": ["Compute a stereo pair's level and time differences, its image positions and its recording angle.",
                  "Derive the comb filter of two microphones, the 3 : 1 rule, the four pan laws in stereo and mono, and fades.",
                  "Build a console with sends and buses, a masking map, width measures and a rule-based automatic mixer."],
            "D": ["Find an objective, other than imitating a mix, that predicts which mix listeners prefer."],
            "I": ["Record with pairs and close microphones, stage gain, edit, balance, carve, compress and check a mix."],
        },
        results=[
            ("Image rule", r"\text{image} \approx \Delta L/15\,\text{dB} + \Delta t/1.1\,\text{ms}"),
            ("Comb", r"|1 + g\,e^{-j2\pi f\tau}|, \quad \text{notches at } (2k+1)/2\tau"),
            ("3 : 1 rule", r"20\log_{10}(1 \pm \tfrac{1}{3}) = +2.5,\ -3.5\ \text{dB}"),
            ("Pan laws", r"g_L = \cos\frac{\pi(p+1)}{4}, \ g_R = \sin\frac{\pi(p+1)}{4} \ (-3\ \text{dB})"),
            ("Mid-side", r"M = \tfrac{L+R}{2}, \ S = \tfrac{L-R}{2}"),
        ],
        U=(0, 2, 3, 4, 7, 9, 10),
        D=(11,),
        I=(1, 5, 6, 8),
        also=(("Monochord's studio: stereo pairs, combs, gain staging, crossfades, the console, the masking map, width, an automatic mixer", "explainer/music/monochord/studio.py"),),
    ),
    Part(
        n=57, level="U", widget="loud", prereq=(4, 48, 50, 54, 56),
        question="What does mastering do to a mix, how is loudness measured, and why did making records louder stop paying?",
        story="In 2008 Death Magnetic's CD was mastered so loud that its peaks were clipped, while the Guitar Hero versions were not; an ear question hears Part 56's mix mastered gently (-14 LUFS, PLR 13 dB) and for loudness (-7.7 LUFS, PLR 6.7 dB, limited by up to 23 dB) at the same loudness. What mastering is for, and Monochord's chain (tilt EQ, glue, a look-ahead limiter, dither) stage by stage, heard. Meters: sample peak, VU and PPM on a snare hit; K-weighting; a 60 Hz and a 2 kHz tone at one voltage, 6 LU apart, heard. BS.1770 in four lines, the gates at work on a quiet start (-21.9 LUFS against -23.6 ungated), and the series' meter against ffmpeg's (within 0.05 LU and 0.1 dB); LRA and the targets of R 128 and the services. Inter-sample peaks: a sine 3 dB above its samples; a clipped master +2.5 dBTP; why converters and codecs care. The look-ahead limiter, close up, against a clipper, heard. The loudness war in numbers: six masters, the PLR falling from 15 to 6.7 dB while the loudness range hardly moves (as Deruty and Tardieu found), the limiter topping out near -7.7 LUFS; the sausage; three masters heard as mastered. Normalization to -14 LUFS (the loud master turned down 6 dB, its peaks now the lowest) and an ear question on which was mastered loudest. The loudness bias (an ear question: the same master 1 dB louder), level-matched blind comparison, and the series' own rule. Dither: rounding's staircase, error spectra, a fading note at 8 bits rounded, dithered and shaped, heard. Vinyl's groove and the RIAA curve (+19.3, -19.6 dB), a record without it heard; one master per medium; how this series is mastered. Frontier: what preference experiments found, after the war, machines that master. An album side of Variations, and one war-mastered beside itself.",
        handoff="Codecs, their overshoots and their listening tests in Part 58; loudness limits and safety in Part 59; "
                "formats and streaming's rules in Part 60; blind tests and their statistics in Part 67; every Variation, "
                "sequenced and matched, in Part 68.",
        outside="Part 4 for loudness, equal-loudness curves and the ear's safety; Part 48 for sampling, quantization and "
                "the word length; Part 50 for compressors and saturation; Part 54 for the phone; Part 56 for the mix. "
                "Decibels, means and percentiles, interpolation.",
        objectives={
            "U": ["Hear one mix mastered gently and for loudness at the same loudness, and three masters as mastered and normalized.",
                  "Hear a low and a high tone at one voltage, clipping against limiting, and one master made 1 dB louder.",
                  "Hear a fading note rounded, dithered and noise-shaped, and a record played without its RIAA curve."],
            "M": ["Derive BS.1770's integrated loudness with K-weighting and both gates, and the loudness range of Tech 3342.",
                  "Show why samples miss true peaks, measure them by oversampling, and hold them with a look-ahead limiter.",
                  "Compute normalization gains, the cost of loudness in PLR, quantization with and without dither, and RIAA."],
            "D": ["Find what peak-to-loudness ratio listeners prefer once everything is normalized, and where they listen."],
            "I": ["Meter, master and deliver for each medium: a loudness target, a true-peak ceiling, dither, comparisons at equal loudness."],
        },
        results=[
            ("BS.1770", r"L_K = -0.691 + 10\log_{10}\textstyle\sum_c G_c z_c, \ \text{gates at } -70 \text{ LUFS and } -10 \text{ LU}"),
            ("True peak", r"\text{sine at } f_s/4,\ 45^\circ: \ +3.01\ \text{dB above its samples}"),
            ("Normalization", r"g = \min(0,\ \text{target} - L), \text{ or up to } -1\ \text{dBTP}"),
            ("Word length", r"\text{SNR} \approx 6.02\,N + 1.76\ \text{dB}"),
            ("RIAA", r"H = \frac{1 + s\,318\,\mu s}{(1 + s\,3180\,\mu s)(1 + s\,75\,\mu s)}"),
        ],
        U=(0, 2, 6, 7, 8, 9, 10),
        D=(11,),
        I=(1, 3, 4, 5),
        also=(("Monochord's mastering bench: meters, gating, true peak, a look-ahead limiter, normalization, dither, RIAA", "explainer/music/monochord/master.py"),),
    ),
    Part(
        n=58, level="U", widget="abx", prereq=(4, 48, 49, 55, 57),
        question="How can a file a tenth the size of a recording sound the same, and how would anyone prove it does?",
        story="Brandenburg tuned the first MP3 coder on Suzanne Vega's voice alone; an ear question hears the Tune sung alone as recorded and through Monochord's own perceptual coder at 64 kbit/s (a twelfth the size, its noise 16 dB under the mask) and 16 (18 dB over). Two kinds of compression. Entropy, prediction (the voice from 13 to 3.5 bits a sample), Rice codes, and a lossless coder that rebuilds every bit (voice 23 per cent, mix 55). Masking: Schroeder's spreading, Johnston's tonality offsets, the threshold in quiet; one frame's mask; an ear question hears white and mask-shaped noise at the same power (the shaped noise only 10 dB under the music, hidden). The MDCT, one frame's aliases and their cancellation to 1e-13, heard by dropping alternate frames. A perceptual coder: step sizes from the mask, a margin found by bisection, Rice-coded bands; the voice and the mix at five rates (the mix 19 dB under the mask at 128 kbit/s, 18 over at 16), heard. Pre-echo: at equal noise-to-mask, long blocks leave 5.5 dB more noise before each hit and short ones cost three times the bits (an ear question); window switching. Mid-side coding about 4 dB better at the same bits, heard. MP3, AAC, Vorbis, HE-AAC and Opus; the business. Listening tests: an ABX trial, binomial thresholds (12 of 16), the power (a 70 per cent listener passes 16 trials 45 per cent of the time), BS.1116 and MUSHRA. Five generations of transcoding (SNR 8.5 to about 2 dB), heard. Residual vector quantization in stages (5 dB each), heard; neural codecs; learned metrics. The Tune at five rates, and the residue alone.",
        handoff="Low-delay codecs on stage in Part 59; the files that changed the business in Part 60; fingerprints "
                "that survive a codec in Part 63; codec tokens as generative audio's alphabet in Part 66; listening tests "
                "and their statistics in Part 67.",
        outside="Part 4 for masking, critical bands and the threshold in quiet; Part 48 for sampling and quantization; "
                "Part 49 for filters and the FFT; Part 55 for stereo cues; Part 57 for true peaks and level-matched "
                "comparison. Entropy, the binomial distribution, linear algebra of a transform, k-means.",
        objectives={
            "U": ["Hear a lone voice at 64 and 16 kbit/s against the original, and the voice at five rates.",
                  "Hear white and mask-shaped noise of equal power, pre-echo with long and short blocks, and an ABX trial.",
                  "Hear left-right against mid-side coding, five generations of transcoding, and vector quantization in stages."],
            "M": ["Compute entropy and code prediction residuals with Rice codes, and decode them bit for bit.",
                  "Prove the MDCT's alias cancellation and build a masking model with spreading, tonality and quiet.",
                  "Allocate bits by step sizes under rate control, and compute an ABX test's threshold and power."],
            "D": ["Find whether a learned metric can predict ratings for a kind of codec it never saw in training."],
            "I": ["Choose codecs and rates for delivery, keep lossless masters, avoid transcoding, and run fair listening tests."],
        },
        results=[
            ("Entropy", r"H = -\textstyle\sum_i p_i \log_2 p_i"),
            ("MDCT", r"X_k = \textstyle\sum_{n=0}^{2N-1} w_n x_n \cos[\tfrac{\pi}{N}(n + \tfrac12 + \tfrac N2)(k + \tfrac12)], \ w_n^2 + w_{n+N}^2 = 1"),
            ("Step size", r"\Delta_b = \sqrt{12 M_b / n_b}\,10^{-m/20}"),
            ("ABX", r"P(\ge c \mid n, \tfrac12) < 0.05: \ c = 12 \text{ of } 16"),
            ("Spreading", r"S(\Delta z) = 15.81 + 7.5(\Delta z + 0.474) - 17.5\sqrt{1 + (\Delta z + 0.474)^2}"),
        ],
        U=(0, 2, 5, 6, 7, 8, 9),
        D=(11,),
        I=(1, 3, 4, 10),
        also=(("Monochord's codecs: a lossless coder, the MDCT, a masking model, a perceptual coder, ABX statistics, residual vector quantization", "explainer/music/monochord/codec.py"),),
    ),
    Part(
        n=59, level="U", widget="howl", prereq=(4, 49, 54, 55, 56),
        question="Why does a microphone howl, why are loudspeakers hung in curves, and how is a stadium made to hear a band?",
        story="In August 1965 the Beatles played Shea Stadium through the baseball announcement system and nobody, the band included, could hear them; an ear question hears our session from the stands over a crowd through a 1965-style horn system (6 dB under the crowd) and a modern one (8 dB over). Why a microphone howls: the loop, Nyquist's criterion (the real part of G H reaching one, not its magnitude), and a simulated hall in which Monochord predicts the gain before feedback (-17.9 dB) and the howl note (358 Hz), then hears it build at 358; an ear question hears a clap at 6, 0.5 and 2 dB below the edge. Ringing out with six narrow notches (+3.3 dB), heard; placement, nulls and in-ear monitors; Davis's PAG and NAG (24.5 against 26.0 dB). Point and line sources: 6 dB per doubling against about 3 near a line (2.7 at 1 kHz), and the transition distance growing with frequency (26, 103, 411 m at 250 Hz, 1 kHz, 4 kHz for an 8.4 m line). Three fields of an arena at 1 kHz: a point, a straight line and a J-shaped array (splays 0.3 to 4.2 degrees); the array heard at 10, 40 and 80 m (6.4 and 7.3 dB down). Steering. Subwoofers: a cardioid pair (0.9 m, 2.6 ms, inverted) that cancels behind at every frequency, heard from the stage; end-fire and arc delays. A delay tower (90 and 30 m: 184.7 ms), an ear question on alignment; the speed of sound and temperature (3 ms drift over 10 degrees), refraction and wind; ISO 9613-1's air absorption (0.5, 3, 11 and 36 dB over 100 m at 1, 4, 8, 16 kHz), heard. Dual-channel measurement with the music: transfer function, coherence and the delay found exactly; pitfalls and system tuning. Wireless: third-order intermodulation, an even 24-carrier grid with every carrier hit against Monochord's planner's 20 clean carriers around three TV channels; in-ear monitors; Dante, AES67, PTP and the latency budget. Speech: Houtgast and Steeneken's modulation transfer and the STI over reverberation and noise (0.74 dry and clean to 0.23 at 6 s); an ear question hears one announcement in a studio (0.64), a hall (0.37) and a station (0.15); remedies. Hearing health: hair cells, hidden hearing loss, the equal-energy rule, a night's doses (2016 per cent at the barrier, 16 with earplugs mid-arena), the EU directive and the WHO's 2022 venue standard. Frontier: immersive object-based live systems, sound zones and off-site noise. Variation 59: the Tune at the mixing desk, the back row and the car park.",
        handoff="Ticket prices and the cost disease of live performance in Part 60; machines that follow a score on "
                "stage in Part 62; one voice pulled out of a room in Part 64; measuring what audiences hear in Part 67; "
                "the concert that closes the series in Part 68.",
        outside="Part 4 for the cochlea, loudness and hearing damage; Part 49 for impulse responses, the image method and "
                "measurement by sweeps; Part 50 for intermodulation; Part 54 for microphone patterns and arrays; Part 55 for "
                "rooms, precedence and wave fields; Part 56 for the mix. Complex numbers and phase, decibels, the FFT, "
                "interference of waves.",
        objectives={
            "U": ["Hear a 1965 stadium system against a modern one, a clap at three margins below feedback, and a howl building.",
                  "Hear a voice before and after ringing out, a line array at three distances, and subwoofers from behind the stage.",
                  "Hear a delay tower aligned and not, the air over 10 and 100 m, and one announcement in three rooms."],
            "M": ["Derive the gain before feedback by Nyquist's criterion, and the potential and needed acoustic gain.",
                  "Compute point and line sources' fields, a cardioid subwoofer pair, delay-tower times and air absorption.",
                  "Measure a transfer function with music, plan carriers free of third-order products, and compute STI and dose."],
            "D": ["Find array settings that hold a festival's off-site noise limit with 95 per cent confidence over the weather."],
            "I": ["Design, align and tune a system: gain before feedback, coverage, delays, a frequency plan, intelligibility, safe levels."],
        },
        results=[
            ("Nyquist", r"\text{howl where } G\,\mathrm{Re}\,H(f) = 1: \ G_{\max} = 1/\max_f \mathrm{Re}\,H(f)"),
            ("PAG", r"\mathrm{PAG} = 20\log_{10}\frac{D_0 D_1}{D_s D_2} - 10\log_{10}\mathrm{NOM} - 6\ \text{dB}"),
            ("Delay tower", r"\tau = (d_{\text{main}} - d_{\text{tower}})/c + 10\ \text{ms}, \ c = 331.3 + 0.606\,T"),
            ("STI", r"m(F) = \bigl[1 + (2\pi F T/13.8)^2\bigr]^{-1/2}\,\bigl(1 + 10^{-\mathrm{SNR}/10}\bigr)^{-1}"),
            ("Dose", r"t_{\text{allowed}} = 8\ \text{h} \times 2^{-(L - 85)/3}"),
        ],
        U=(0, 1, 2, 4, 5, 6, 9),
        D=(11,),
        I=(3, 7, 8, 10),
        also=(("Monochord's live sound: feedback by Nyquist, ringing out, PAG/NAG, fields of sources and arrays, cardioid subwoofers, delay towers, ISO 9613-1 air absorption, dual-channel measurement, intermodulation planning, STI, noise dose", "explainer/music/monochord/live.py"),),
    ),
    Part(
        n=60, level="U", widget="pool", prereq=(14, 56, 57, 58, 59),
        question="Where does a stream's money go, why are hits so unequal, and how often do two melodies coincide by chance?",
        story="An ear question hears two melodies with the same eight-note opening and asks whether one copied the other: neither did; both were drawn independently from Part 14's model, and the 396th draw repeated an opening. The plan, with everything dated, mostly American, illustrative and not legal or financial advice. Two copyrights (the composition and the recording, their terms and history, from the Statute of Anne and Bach v. Longman to the Music Modernization Act); one composition in two recordings, heard; the Tune's own rights; Happy Birthday; each machine that broke the arrangement. Four licences; SACEM's café and ASCAP; the flow of a stream's money; US radio's gap, unmatched royalties and the MLC. One stream, heard past its 30 seconds; a month's subscription divided (11.99 dollars: 30 per cent to the service, 55 to the recording, 15 to the composition; 40 cents to each of three songwriters); a million streams at the simulated rate of 0.47 cents (4,655 dollars to rights holders; the artist credited 658 dollars on a label deal, 3,016 self-released; 224 to each songwriter). A record deal: a 150,000-dollar account recouped only after 228 million streams while the label breaks even at 50 million; 360 and distribution deals; how musicians are paid. A simulated service's month divided pro rata and user by user (niche artists +108 per cent, the stars -25, a bot farm taking 7.8 times what it paid in pro rata and only its own fees user by user); reforms of 2021 to 2024. Rosen's superstars, Krueger's concert shares, and Salganik, Dodds and Watts's MusicLab simulated (Gini 0.43 independent against 0.61 social; unpredictability 1.7 times higher; winners ranked 1st to 11th in quality), two worlds' hits heard. Charts from 1958 to streaming; a long and a short introduction heard (Lamere's skips, Léveillé Gauvin's shrinking intros); the attention economy. Baumol's cost disease with a quartet heard (x3.3 since 1966); one tour date's tickets sold at face value, one price and dynamic prices; the ticket market. How many melodies: exact collision probabilities from Part 14's model (52,206 effective eight-note openings against 2.6e10), a 5.2 per cent chance that two 60-note songs share an eight-note window, the birthday problem among 100 million songs; the Tune transposed (no note shared, every interval) against re-contoured, heard; US cases from My Sweet Lord to Thinking Out Loud. Sampling: an ear question (sample or replay?), the cases from Grand Upright to Pelham; an ear question on a model's melody against a folk song (1.9 against 2.7 bits a note); training-data lawsuits and settlements, human authorship, voices. Frontier: payout reform; licensing, attribution, memorization and detection; a research problem on calibrated probabilities of chance. Variation 60: the Tune's family of copyrights (our recording, a quartet's cover, a remix) and their statements after a million streams each.",
        handoff="Recommendation as a social-influence world in Part 63; memorization and plagiarism tests for "
                "machines that compose in Part 65; voices, training data and rights in Part 66; measuring fairness and "
                "listening in Part 67; the series' own Variations performed in Part 68.",
        outside="Part 14 for the n-gram model of melody; Part 56 for the session and the recording; Parts 57 to 59 for "
                "mastering, codecs and live sound. Fractions and percentages, expected values, the birthday problem, "
                "Gini coefficients, exponential growth, simple simulation. Nothing here is legal or financial advice.",
        objectives={
            "U": ["Hear two independently drawn melodies share an opening, one composition in two recordings, and a stream's 30 seconds.",
                  "Hear two worlds' hits, a long and a short introduction, a quartet, and the Tune transposed and re-contoured.",
                  "Hear a sample against an interpolation, a model's melody against a folk song, and the Tune's family of copyrights."],
            "M": ["Divide a subscription and a million streams among their claimants, and find the streams that repay an advance.",
                  "Divide a simulated month pro rata and user by user, and show why fraud pays only in a pool.",
                  "Compute a melody model's collision probabilities exactly, and the birthday odds of a shared phrase."],
            "D": ["Give courts a calibrated probability that a shared phrase arose by chance, from dated melody models."],
            "I": ["Register, read and clear: complete credits, recoupment and reversion terms, both licences for every sample."],
        },
        results=[
            ("Waterfall", r"\text{rights holders} = 70\%: \ \text{recording } 55,\ \text{composition } 15 \ (\text{illustrative})"),
            ("Recoupment", r"n^\ast = \frac{\text{advance} + \text{costs}}{r_{\text{label}}\,\rho}"),
            ("Pro rata", r"\text{pay}_a = \Big(\textstyle\sum_u f_u\Big)\,\frac{\sum_u s_{ua}}{\sum_{u,b} s_{ub}}, \quad \text{user-centric: } \textstyle\sum_u f_u\,\frac{s_{ua}}{\sum_b s_{ub}}"),
            ("Collisions", r"q_k = \textstyle\sum_s P(s)^2, \ N_k = 1/q_k, \ P(\text{shared window}) \approx 1 - e^{-W^2 q_k}"),
            ("Cost disease", r"\frac{p_{\text{performance}}}{p_{\text{goods}}} \propto e^{g(t - t_0)}"),
        ],
        U=(0, 1, 3, 6, 7, 8, 9, 10),
        D=(11,),
        I=(2, 4, 5),
        also=(("Monochord's business module: waterfalls, recoupment, pro-rata and user-centric pools, a social-influence market, the cost disease, ticket pricing, melody collisions", "explainer/music/monochord/business.py"),),
    ),
    Part(
        n=61, level="U", widget="yin", prereq=(2, 3, 15, 38, 48),
        question="How does a machine hear music and write down its notes, and how do we know when it is right?",
        story="An ear question: the Tune with chords twice on one piano, a performance and a small network's transcription played back (the second was the original; the copy found 21 of 30 notes and added 43). Mozart and the Miserere in 1770; why a listening machine needs an answer key, which Monochord's renders give exactly (160 training pieces, 12 test). One voice: the difference function, the missing fundamental found at 220.0 Hz, YIN's steps (a bias of 0.02 cents against autocorrelation's 1.8), the track played as a sine beside the voice. In noise: the sung Tune tracked through three noises, heard; YIN's gross errors 9 per cent at 0 dB and 60 at -5, where plain autocorrelation keeps 10. Chords: an ear question on an added octave; salience peaking on C3, an octave below the lowest note; cancellation; the hidden octave. Onsets by spectral flux, piano against bowed strings (F 0.90 and 0.74), heard; precision against recall. NMF: multiplicative updates, blind components, note templates, a test piece factorized and played back (9 of 10 notes, 17 added, mostly at the range's edges). A network on five frames: note F 0.67 on piano against NMF's 0.49; inside it; how many notes at once (0.91 on single lines, 0.54 with six). Timbres never heard: harp, organ and strings, heard (the network 0.24 on the harp); an ear question on the organ. Keeping score: precision, recall and F; an ear question on two transcriptions at F 0.82 and 0.83, one missing notes and one with octave errors. Notes to a score: a rubato performance's exact onsets, one fixed tempo putting 1 of 14 on the written beat and a drifting tempo all 14, its tempo curve from 108 to 135; key and spelling. Fifty years of transcription; frontier: many instruments, audio to score, a research problem on calibration. Variation 61: the Tune transcribed and re-rendered five times round, F 0.53 after one round and 0.10 after five.",
        handoff="Beats, chords and form from the same spectral flux and templates in Part 62; pitch contours for query by "
                "humming in Part 63; NMF again, for sources, in Part 64; transcriptions as training data for machines that "
                "compose in Part 65; the evaluation questions of Part 67.",
        outside="Part 2 for spectra and partials; Part 3 for the missing fundamental; Part 15 for keys; Part 38 for the piano; "
                "Part 48 for sampling. Autocorrelation, peak picking, non-negative least squares and the KL divergence, "
                "multiplicative updates, small neural networks and cross-entropy, precision and recall, dynamic programming.",
        objectives={
            "U": ["Hear a pitch track as a sine beside the voice, the voice through noise, and an added octave in a chord.",
                  "Hear transcriptions played back: NMF's busy copy, the network's on an unseen organ, two at the same F.",
                  "Explain why polyphony and unseen timbres are hard, and why a score is not a performance."],
            "M": ["Track pitch by YIN and by autocorrelation and measure gross and fine errors against noise.",
                  "Transcribe by NMF with fixed templates and by a small network; score notes and frames by precision, recall and F.",
                  "Quantize performed onsets with a fixed and with a drifting tempo, and find the key."],
            "D": ["Measure and improve a transcriber's calibration on timbres it never heard."],
            "I": ["Keep answer keys exact, report note and frame scores with their tolerances, and listen to the playback."],
        },
        results=[
            ("Difference", r"d(\tau) = \sum_{j} (x_j - x_{j+\tau})^2"),
            ("YIN", r"d'(\tau) = d(\tau) \Big/ \tfrac{1}{\tau}\sum_{k=1}^{\tau} d(k)"),
            ("Flux", r"\mathrm{SF}(t) = \sum_f \max(0,\ |X(t, f)| - |X(t-1, f)|)"),
            ("NMF update", r"H \leftarrow H \odot \frac{W^\top (V / WH)}{W^\top \mathbf 1}"),
            ("F-measure", r"F = \frac{2PR}{P + R}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8),
        D=(11,),
        I=(9, 10),
        also=(("Monochord's first listeners: YIN, salience, onsets, NMF, a transcribing network, scores and quantization", "explainer/music/monochord/mir/transcribe.py"),),
    ),
    Part(
        n=62, level="U", widget="tempo", prereq=(9, 18, 21, 43, 61),
        question="How does a machine find the beat, the chords and the form of a song, and follow a singer live?",
        story="An ear question hears the session with a click track 80 ms late and one on the beat. People entrain and predict, and prefer tempos near 120; the listeners these methods power. Novelty: spectral flux with its local mean removed, the drums alone against the band, other novelty functions and kinds of accent, and an autocorrelation tempogram bright at 100, 200 and 50 beats a minute. Tempo: the autocorrelation times a prior near 120 finds 100 on the session; a slow piece written at 50 is read at 100 with the prior and 50 without, heard with both click tracks; tempo in real performances. Beats: forty years of trackers; Ellis's dynamic programme, F 0.94 on the session; on a rubato piano performance the tracker misjudges the tempo (125 against 106) and reaches only 0.58; scoring at several levels. Downbeats: an ear question on where bar lines fall; the low band marks beats one and three but cannot say which is first; other meters. Chroma: folding octaves, the Tune's chroma heard, its relatives and uses, chord templates. Chords: templates frame by frame 44 per cent, an HMM 51, an HMM with Bach's transitions 76; the confusions run a fifth up (C as G, G as D), from each note's third partial. Time warping: a strict and a rubato performance heard and aligned (median 13 ms offline and online), the path read as a tempo curve, its origins in speech. Following: computer accompaniment since 1984; Monochord's follower tracking a freely sung Tune, its chords a median 96 ms from the voice; what human accompanists do. Structure: the whole Tune's self-similarity heard; Foote's novelty misses the sections because nothing in the texture changes; repetition finds a b c c a b, A B A, where mean chroma cannot; song forms. Covers: an ear question (which is not the Tune?), key-invariant DTW finding the transposition of five semitones; covers in the wild; how far annotators agree. Frontier: whose meter, joint models, listening live; a research problem on predictive accompaniment. Variation 62: the Tune sung freely and accompanied twice, deaf and listening.",
        handoff="Beat-matched playlists and fingerprints in Part 63; beats and chords guiding separation in Part 64; "
                "bars, chords and form as structure for machines that compose in Part 65; annotators and their "
                "disagreements in Part 67; an accompanist that listens, in the concert of Part 68.",
        outside="Part 9 for meter and the grid; Part 15 for keys; Part 18 for the chorales' chord transitions; Part 21 for "
                "form and self-similarity; Part 43 for expressive timing; Part 61 for spectral flux. Autocorrelation, "
                "dynamic programming, hidden Markov models and the Viterbi algorithm, cosine similarity.",
        objectives={
            "U": ["Hear a click track 80 ms late against one on the beat, and the drums alone against the whole band.",
                  "Hear a tracker's clicks on a steady band and on rubato, a slow piece at two tempos, and where bar lines fall.",
                  "Hear a strict and a rubato performance aligned, a cover in another key, and a singer accompanied live."],
            "M": ["Compute novelty, the autocorrelation tempogram and a prior-weighted tempo; track beats by dynamic programming.",
                  "Recognize chords from chroma by templates and by an HMM with a transition prior, decoded by Viterbi.",
                  "Align performances by offline and online DTW, and find form from novelty and from repetition."],
            "D": ["Build a predictive follower and measure how close to a human accompanist it can play, and where it fails."],
            "I": ["Report tempo with its octave in doubt, score beats at the right and at any sensible level, fit a prior to the music."],
        },
        results=[
            ("Ellis's DP", r"C(t) = O(t) + \max_\tau\big[C(\tau) - \alpha\log^2\tfrac{t - \tau}{P}\big]"),
            ("Tempo prior", r"\hat T = \arg\max_T\ \mathrm{AC}(T)\,\exp\!\big(-\tfrac12 (\log_2 T/120)^2/\sigma^2\big)"),
            ("Viterbi", r"\delta_t(j) = \max_i \delta_{t-1}(i)\,A_{ij}\,b_j(x_t)"),
            ("DTW", r"D(i, j) = c(i, j) + \min\{D(i{-}1, j{-}1), D(i{-}1, j), D(i, j{-}1)\}"),
            ("Foote", r"N(t) = \sum_{a,b} K(a, b)\,S(t + a, t + b)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, 9, 10),
        D=(11,),
        I=(6, 8),
        also=(("Monochord's rhythm listeners: novelty, tempo, beat tracking, chroma, chord HMMs, DTW and online following, self-similarity and repetition", "explainer/music/monochord/mir/rhythm.py"),),
    ),
    Part(
        n=63, level="U", widget="loop", prereq=(2, 4, 58, 60, 61),
        question="How does a phone name a song from five noisy seconds, and how does a service choose what you hear next?",
        story="Five seconds of Variation 40 in a simulated bar, the music no louder than the noise, named with its offset among every sound of Parts 1 to 60 (908 clips, 3.7 hours, 1.15 million hashes); Shazam's phone number in 2002. A constellation of spectrogram peaks, about twenty a second, heard alone. Pairs of peaks as 24-bit hashes; votes for a clip and an offset; a match drawn as dots on one diagonal, the Tune's repeats on shorter ones. Noise: one query in three bars, heard; white noise is easier than bar noise (61 per cent named at 0 dB, 25 at -5); query length (9 per cent at one second, 81 at eight), heard; an ear question on a 16 kbit/s codec; the Poisson arithmetic of chance, and a hundred million tracks. Recordings, not songs: the Tune rendered afresh gets a tenth of a true excerpt's votes; an ear question on a Variation 4 per cent fast (lost: 59 per cent at 1 per cent, 25 at 2); a sample 12 dB under another track found 47 per cent of the time; a hummed query, slower, higher and out of tune, missed by the fingerprint and found first of 30 melodies by its pitch contour and time warping. Tags and embeddings: all 908 clips on two principal components, the acts overlapping (it knows sound, not subject); an ear question on nearest and farthest neighbours; GTZAN's faults. A horse: a classifier scores 83 per cent from a faint mains hum, 43 without it, and 48 trained honestly and split by clip, no better than guessing; its weight on the lowest bands. Collaborative filtering on simulated listeners: the play matrix and its factors; implicit ALS (recall at 10: 0.127 against 0.077 for popularity and 0.038 at random); the cold start from content (0.28 against 0.17). Popularity feeding on itself: Gini 0.97 after thirty rounds, 0.71 exploring, 0.13 without a recommender; Lorenz curves. Playlists by nearest neighbour and 2-opt (226 against 439), an ear question, the path on the map; fairness and metadata. Frontier: foundation models; effects on creators and the shrinking introduction; a research problem on what recommenders caused. Variation 63: three earlier Variations named through a bar's noise.",
        handoff="Separated stems searched and remixed in Part 64; machines that compose trained on what services collect in Part 65; "
                "generated audio, watermarks and fingerprints in Part 66; evaluation, leakage and listening tests in Part 67; "
                "the concert's programme ordered in Part 68.",
        outside="Part 2 for spectra; Part 4 for hearing in noise; Part 58 for codecs; Part 60 for streaming's money; Part 61 "
                "for pitch tracking. Hash tables, the Poisson distribution, principal components, logistic regression, "
                "alternating least squares, dynamic time warping, the travelling-salesman heuristic 2-opt.",
        objectives={
            "U": ["Hear a query in a noisy bar named, a codec, a query played fast, a sample buried in another track and a hummed tune.",
                  "Hear neighbours and the farthest clip by content, a mains hum a classifier learnt, and a random against an ordered playlist.",
                  "Explain why a fingerprint names a recording and not a song, and why popularity feeds on itself."],
            "M": ["Fingerprint audio by spectrogram peaks and hashes, index it, and name queries by aligned votes.",
                  "Compute the chance of a false match from the Poisson tail, for any library size.",
                  "Factorize implicit feedback by ALS, score recall at k, and handle the cold start from content."],
            "D": ["Design a simulation of listeners, artists and a recommender, fitted to observable trends, to ask what recommenders caused."],
            "I": ["Split data by recording and source, test with interventions, and check what a model's weights rely on before trusting a score."],
        },
        results=[
            ("Hash", r"h = (f_1, f_2, \Delta t) \mapsto 24\ \text{bits}"),
            ("Votes", r"\text{offset} = t_{\text{clip}} - t_{\text{query}}"),
            ("Chance", r"\lambda = \frac{n_q\, n_{db}\, 2^{-24}}{\text{tracks} \times \text{offsets}},\ \ P(\ge m) \le N\,\frac{\lambda^m}{m!}e^{-\lambda}(1 + \dots)"),
            ("Implicit ALS", r"x_u = (Y^\top C_u Y + \lambda I)^{-1} Y^\top C_u\, p_u"),
            ("Gini", r"G = \frac{\sum_i \sum_j |x_i - x_j|}{2 n^2 \bar x}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8, 10),
        D=(11,),
        I=(7, 9),
        also=(("Monochord's finders: fingerprints, the hash index, false matches, the embedding, implicit ALS, the feedback loop, playlists, query by humming", "explainer/music/monochord/mir/finder.py"),),
    ),
    Part(
        n=64, level="U", widget="mask", prereq=(2, 45, 54, 56, 61),
        question="How can a machine pull one instrument out of a finished mix, and how do we know how well it did?",
        story="An ear question: a voice and a piano on one track, then the voice twice; the first was separated, 12 dB from the truth; a home cassette lifted apart decades later. The mixing model and the assumptions separation needs; Part 56's session as the test set, its four stems heard alone and mixed. Stereo: left minus right, 11 dB quieter, the centred voice, bass and drums gone, heard; a panning index per bin picks out the piano roughly (2.7 dB); the session's energy by index. ICA: the session as a cloud of samples squared up; the voice is the most non-Gaussian direction (kurtosis 1.61 against the microphones' 1.34 and 0.82); perfect dry, lost in a room, heard. Median filtering: lines and stripes, the harmonic mask, the split heard (tonal 7.8 dB, drums 1.0), long filters better (10.1 and 3.4), heard. Supervised NMF: the voice's combs and the drums' smears; stems from 5.2 to 8.5 dB; templates per source (gains flatten after six). Oracle masks as pictures and as ceilings (vocals: NMF 7.7, binary 8.3, ratio 9.3, with true phase 12.7; for drums the binary mask wins), heard. Phase: Griffin-Lim heard, its inconsistency falling to -20 dB while its SDR stays near -3; an ear question on the phase gap; waveform separators. A small vocal-mask network trained on the middle phrases transposed: 6.9 dB, below NMF; trained on stretches that repeat the test, 8.5: what a leak is worth. Measuring: SDR, SI-SDR, BSS Eval; an ear question on two estimates at exactly 8.0 dB, one leaking and one gargling; a perfect estimate half as loud, upside down, dull and a millisecond late (-0.6 dB), heard. Uses, an ear question on a remix from separated stems (13.7 dB from the true remix), rights. Frontier: generative and query-based separation, better metrics. Variation 64: the Tune a cappella and as karaoke, separated and true.",
        handoff="Stems as training material for machines that compose in Part 65; separation by generation, voices and rights "
                "in Part 66; listening tests and leakage in Part 67; the Variations as stems in Part 68's concert.",
        outside="Part 2 for spectra; Part 45 for the auditory scene; Part 54 for panning; Part 56 for the session; Part 61 for "
                "NMF. The short-time Fourier transform, whitening and kurtosis, median filters, multiplicative updates, "
                "least squares, gradient descent.",
        objectives={
            "U": ["Hear stems alone and mixed, centre cancellation, ICA dry and in a room, and the harmonic and percussive halves.",
                  "Hear separated voices against the oracles, the phase gap, and two estimates with equal SDR and different faults.",
                  "Explain why one channel needs assumptions, and why a mask's ceiling is set by phase."],
            "M": ["Separate by panning, FastICA, median filtering, supervised NMF and a mask network; score each by SDR and SI-SDR.",
                  "Compute the ideal binary and ratio masks and the true-phase bound for a mixture whose stems are known.",
                  "Recover a phase from a magnitude by Griffin-Lim, and measure its consistency and its error."],
            "D": ["Test which measures predict listeners' ratings of separations, including generative ones that invent."],
            "I": ["Keep test material out of training, report SDR with the oracle bounds beside it, and listen as well as measure."],
        },
        results=[
            ("Mask", r"\hat S_j(t, f) = M_j(t, f)\, X(t, f)"),
            ("Ratio mask", r"M_j = |S_j| \big/ \textstyle\sum_k |S_k|"),
            ("SDR", r"10\log_{10} \|s\|^2 / \|s - \hat s\|^2"),
            ("SI-SDR", r"\alpha = \hat s^\top s / \|s\|^2,\ \ 10\log_{10} \|\alpha s\|^2 / \|\hat s - \alpha s\|^2"),
            ("Griffin-Lim", r"X_{k+1} = |S|\, e^{i\angle \mathrm{STFT}(\mathrm{ISTFT}(X_k))}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 9),
        D=(11,),
        I=(8, 10),
        also=(("Monochord's separators: the STFT, SDR and SI-SDR, panning, FastICA, HPSS, supervised NMF, oracle masks, Griffin-Lim, the mask network", "explainer/music/monochord/mir/separate.py"),),
    ),
    Part(
        n=65, level="U", widget="chain", prereq=(14, 17, 42, 61, 63),
        question="How do machines learn to compose from music, and how much of what they write is copied?",
        story="An ear question: three pairs of harmonized chorale phrases, one Bach's (BWV 166.6, unseen by the machines) and two by machines; Hofstadter's 1997 concert, where an audience took Cope's EMI for Bach. Composing machines from the dice minuet to the Music Transformer; rules, chance and statistics. The corpus: 163 of Bach's major chorale tunes transposed to C, only 114 different hymn tunes, so split by tune. Markov chains of orders 0 to 8: bits per note on unseen tunes (3.40 at order 2, the best; 3.83 at order 8); surprise at phrase boundaries; orders heard. Copying: order 8 copies runs of 26 notes and 91 per cent of what it writes, against 11 per cent for Bach's own tunes; a 40-note copy heard beside its source; the trade between prediction and copying. Constraints sampled exactly by backward messages (0.66 per cent of free draws end legally). Cope's recombinancy: four chorales in one tune, 79 per cent copied. Tokens three ways. A pocket transformer on the tunes alone and in twelve keys, stopped where the tunes set aside say (3.76 and 3.49 bits); trained too long it recites 40 notes of BWV 322. Temperature: an ear question; intervals closest to Bach at 1.0, notes outside the key rising from 6 to 19 per cent. DeepBach; a machine's chorale harmonized by Part 17 with no parallels; Bach's harmony beside Part 17's. An ear question on copying; every machine before the same judges, where only copying separates them; pitfalls and listening tests. Frontier: form, control and attribution. Variation 65: the Tune's first phrase continued at five temperatures, uncurated.",
        handoff="The same next-token idea on sound itself in Part 66; evaluation, leakage and listening tests in Part 67; "
                "machine-made Variations, labelled, in the concert of Part 68.",
        outside="Part 14 for the next-note model; Part 17 for chorales, chord models and voice leading; Part 42 for composing "
                "as search; Part 61 for networks; Part 63 for evaluation and leakage. Markov chains, perplexity, dynamic "
                "programming, attention and next-token training, data augmentation, early stopping.",
        objectives={
            "U": ["Hear Markov tunes of several orders, a copied stretch beside its source, and constrained and recombined tunes.",
                  "Hear a transformer's tunes, the same opening at three temperatures, and a machine's chorale beside Bach's.",
                  "Explain why a model that copies less coheres less, and why copying must be measured rather than heard."],
            "M": ["Fit variable-order Markov chains, score bits per note on unseen music, and measure copying by exact runs.",
                  "Sample a chain exactly under constraints with backward messages; recombine phrases where they connect.",
                  "Train a small transformer on tokens with augmentation and early stopping; sample with temperature."],
            "D": ["Map the frontier of novelty against quality for generators of many sizes, with blind listening tests."],
            "I": ["Split by work, report uncurated output, likelihood and copying together, and know whose music trained a model."],
        },
        results=[
            ("Order-k chain", r"P(x_t \mid x_{t-k..t-1}) \approx \#(x_{t-k..t}) / \#(x_{t-k..t-1})"),
            ("Bits per note", r"-\tfrac{1}{N}\sum_t \log_2 P(x_t \mid x_{<t})"),
            ("Constraints", r"\beta_k(s) = \sum_{x\ \text{allowed}} P(x \mid s)\, \beta_{k-1}(s')"),
            ("Temperature", r"p_i \propto p_i^{1/T}"),
            ("Copied share", r"\tfrac{1}{N}\,\#\{t : x_t \text{ inside a run of } 8 \text{ copied}\}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, 8, 9),
        D=(11,),
        I=(6, 10),
        also=(("Monochord's machines that compose: the chorale-tune corpus, Markov chains, copy measures, constraints, recombination, tokens, the transformer", "explainer/music/monochord/machines.py"),),
    ),
]
