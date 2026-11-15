from __future__ import annotations

from videos.music.music53.common import *  # noqa: F403
from videos.music.music53.s04_bytes import byte_cells


class Files(SoundScene):
    def construct(self):
        chapter(self, 5, r"MIDI files", r"How do you store a performance, \ not a sound?")
        self.chunks()
        self.vlq()
        self.tempo()
        self.roundtrip()
        self.uses()

    # ------------------------------------------------------------------
    def chunks(self):
        d = load("smf")
        hs = d["head_hex"].split()
        cols = [GREY_A] * 4 + [BLUE] * 4 + [TUNE] * 2 + [EAR] * 2 + [GOLD] * 2 + [GREY_A] * 4 + [BLUE] * 4
        cells = byte_cells(hs, cols, size=0.5, font=13).move_to(UP * 1.2)
        tags = VGroup(label(r"``MThd''", font_size=14, color=GREY_A).next_to(cells[0:4], DOWN, buff=0.15),
                      label(r"length 6", font_size=14, color=BLUE).next_to(cells[4:8], DOWN, buff=0.15),
                      label(r"format 1", font_size=14, color=TUNE).next_to(cells[8:10], DOWN, buff=0.15).shift(DOWN * 0.35),
                      label(r"2 tracks", font_size=14, color=EAR).next_to(cells[10:12], DOWN, buff=0.15),
                      label(r"480 a beat", font_size=14, color=GOLD).next_to(cells[12:14], DOWN, buff=0.15).shift(DOWN * 0.35),
                      label(r"``MTrk''", font_size=14, color=GREY_A).next_to(cells[14:18], DOWN, buff=0.15))
        notes = VGroup(label(r"the Standard MIDI File \ (1988): \ chunks, \ each a four-letter tag and a length", font_size=18, color=WHITE),
                       label(r"a header: \ the format, \ the number of tracks, \ ticks per beat; \ then one chunk per track", font_size=18, color=GREY_A),
                       label(r"inside a track: \ a time since the last event, \ then the event: \ the cable's messages, \ plus tempo and names", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"the first 22 bytes of the Tune's file", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A performance can be stored. <bookmark mark='a'/> The Standard MIDI File of 1988 is a series of chunks, each a "
            "four-letter tag and a length. Here are the first twenty-two bytes of our file of the Tune. The header, M T h d, "
            "length six: format one, two tracks, four hundred and eighty ticks to a beat. Then the first track, M T r k. "
            "<bookmark mark='b'/> Inside a track, every event is preceded by the time since the last one, and the events are "
            "the cable's messages, plus a few that only files need: the tempo, names, the end of the track."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(cells, 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(tags), FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vlq(self):
        d = load("smf")
        rows = VGroup()
        for v in ("0", "127", "128", "480", "16383", "16384"):
            hx = d["vlq"][v].split()
            rows.add(VGroup(label(rf"{int(v):,}", font_size=20, color=WHITE), byte_cells(hx, [TUNE if int(h, 16) < 128 else EAR for h in hx], size=0.5, font=14)).arrange(RIGHT, buff=0.6))
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(LEFT * 1.5 + DOWN * 0.2)
        for r in rows:
            r[1].set_x(-0.2 + r[1].width / 2)
        side = VGroup(label(r"seven bits a byte", font_size=18, color=WHITE), label(r"pink: \ top bit set, \ more to come", font_size=16, color=EAR),
                      label(r"gold: \ the last byte", font_size=16, color=TUNE), label(r"a short wait costs one byte; \ a long one, \ two or three", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(RIGHT, buff=0.5)
        head = label(r"times as variable-length numbers", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The times use a clever code, the variable-length quantity. <bookmark mark='a'/> Each byte carries seven bits of the "
            "number; the top bit says whether another byte follows. Zero is one byte; a hundred and twenty-seven is one byte; a "
            "hundred and twenty-eight needs two, eight one, zero zero; four hundred and eighty, one beat, is eight three, six "
            "zero. <bookmark mark='b'/> Most waits in music are short, so most cost one byte: the same idea as Morse's code, short "
            "signs for what is common."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows, 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), FadeIn(side[:3]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roundtrip(self):
        d = load("smf")
        rows = VGroup(
            label(rf"the whole Tune, \ {d['notes']} notes: \ {d['bytes']} bytes", font_size=24, color=TUNE),
            label(rf"read back by our reader: \ {d['events']} events, \ every note at the right key and time: \ {'yes' if d['roundtrip'] else 'no'}", font_size=20, color=WHITE),
            label(rf"the same {d['seconds']:.0f} seconds as 24-bit stereo audio at 48 kHz: \ {d['wav_bytes'] / 1e6:.1f} million bytes", font_size=20, color=WHITE),
            label(rf"about {d['wav_bytes'] / d['bytes']:,.0f} times smaller, \ because it says what to play, \ not what it sounds like", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"a performance in a few hundred bytes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Our writer stores the whole Tune, {say(d['notes'])} notes, in {say(d['bytes'])} bytes. <bookmark mark='a'/> Our "
            "reader reads it back, every note at the right key and the right time. <bookmark mark='b'/> The same "
            f"{say(d['seconds'])} seconds as twenty-four-bit stereo audio take {say(d['wav_bytes'] / 1e6, 1)} million bytes, "
            f"about {say(d['wav_bytes'] / d['bytes'])} times as many, because the file says what to play, not what it sounds like."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def uses(self):
        items = [
            (r"MIDI files carried ringtones, \ karaoke, \ game music and whole songs across the early internet", WHITE),
            (r"with General MIDI's fixed sounds, \ a file played back roughly right on any machine", WHITE),
            (r"they are also data: \ corpora of MIDI files train the composition models of Part 65", WHITE),
            (r"but a file keeps no sound: \ the same file sounds different on every synthesizer", WHITE),
            (r"what plays the file is the sequencer", TUNE),
        ]
        rows_scene(self, r"MIDI files at work", items,
                   "MIDI files travelled far. <bookmark mark='b'/> They carried ringtones, karaoke, game music and whole songs across "
                   "the early internet, <bookmark mark='c'/> and with General MIDI's fixed sounds a file played back roughly right on "
                   "any machine. <bookmark mark='d'/> They are also data: corpora of MIDI files train the composition models of "
                   "Part 65. <bookmark mark='e'/> But a file keeps no sound, and the same file sounds different on every "
                   "synthesizer. <bookmark mark='f'/> What plays the file is the sequencer.", marks="bcdef")

    # ------------------------------------------------------------------
    def tempo(self):
        lines = VGroup(
            MathTex(r"\text{seconds} = \text{ticks} \times \frac{\text{tempo } (\mu s \text{ a beat})}{\text{division} \times 10^6}", font_size=36),
            MathTex(r"480 \text{ ticks} \times \frac{500{,}000}{480 \times 10^6} = 0.5 \text{ s}", font_size=34),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.6)
        notes = VGroup(label(r"the file counts in ticks, \ not seconds: \ the tempo event says how long a beat lasts, \ in microseconds", font_size=18, color=WHITE),
                       label(r"500,000 microseconds a beat is 120 beats a minute", font_size=18, color=GREY_A),
                       label(r"change the tempo event and every note moves, \ while the score itself stays the same", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"from ticks to seconds", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A file counts in ticks, not seconds. <bookmark mark='a'/> The header says how many ticks make a beat, the division; "
            "a tempo event says how many microseconds a beat lasts. Seconds are ticks times tempo, over the division times a "
            "million. <bookmark mark='b'/> Four hundred and eighty ticks, at five hundred thousand microseconds a beat, is half "
            "a second: a hundred and twenty beats a minute. <bookmark mark='c'/> Change the tempo event and every note moves, "
            "while the score itself stays the same."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()
