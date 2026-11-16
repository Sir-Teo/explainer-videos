from __future__ import annotations

from videos.music.music68.common import *  # noqa: F403


class Survive(SoundScene):
    def construct(self):
        chapter(self, 4, r"What survives", r"Which parts of music survive the journey, and why did notation keep those?")
        self.two_rows()
        self.identity()
        self.room()
        self.notation()
        self.coda()

    # ------------------------------------------------------------------
    def two_rows(self):
        d = load("survive")["rows"]
        filled = {k: 100 * d[k]["filled"] for k in STAGES}
        moves = {k: d[k]["moves_found"] for k in STAGES}
        b1 = stage_bars(filled, 0, max(filled.values()) * 1.1, width=11.6, height=1.6, fmt=lambda v: f"{v:.0f}\\%", font_size=14, colors={k: BLUE for k in STAGES}, center=UP * 1.3)
        b2 = stage_bars(moves, 0, 24, width=11.6, height=1.6, fmt=lambda v: f"{v:d}", font_size=14, center=DOWN * 1.75)
        t1 = label(r"the sound: \ how much of its picture is within 40 dB of its loudest", font_size=17, color=BLUE).next_to(b1, UP, buff=0.15)
        t2 = label(r"onsets near pitch changes: \ detected within 80 ms, \ of 24", font_size=17, color=TUNE).next_to(b2, UP, buff=0.15)
        f = {k: round(filled[k]) for k in STAGES}
        with self.voiceover(
            f"Put the sound and the notes side by side. <bookmark mark='a'/> Above, how much of the sound's picture lies within forty decibels of its loudest: a thresholded spectrogram occupancy, not a direct noise-floor measurement. Performed, {say(f['played'])} per cent; the room fills the gaps, {say(f['room'])}; the microphone and the master fill them further, {say(f['master'])}; and the starved coders empty them, {say(f['codec16'])}. The sound is remade at every link. <bookmark mark='b'/> Below, detected onsets at pitch-changing note positions: {say(moves['score'])} of twenty-four as written, {say(moves['mic'])} through the room and the microphone, {say(min((moves[k] for k in STAGES[4:])))} to {say(max((moves[k] for k in STAGES[4:])))} after the master. This spectral occupancy changes greatly while many onset positions remain detectable."
        ) as vo:
            self.play(FadeIn(VGroup(t1, b1, t2, b2).copy().set_opacity(0.15)))   # a ghost of what is coming
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(b1))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(b2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def identity(self):
        d = load("identify")["rows"]
        head_cells = [r"stage", r"fingerprint's best match", r"aligned votes \ (next best)", r"tempo \ (Part 62)", r"key, \ notes counted"]
        rt = load("roundtrip")["rows"]
        rows_ = VGroup()
        rows_.add(VGroup(*[label(h, font_size=15, color=GREY_B) for h in head_cells]))
        for k in STAGES:
            r = d[k]
            ok = r["found"] == "the Tune, performed"
            rows_.add(VGroup(label(STAGE_NAMES[k], font_size=15, color=TUNE), label(r["found"], font_size=15, color=WHITE if ok else RED),
                             label(rf"{r['votes']} \ ({r['runner_up']})", font_size=15, color=WHITE), label(rf"{r['bpm']:.0f} bpm", font_size=15, color=WHITE),
                             label(rt[k]["key_by_count"], font_size=15, color=WHITE)))
        xs = [-6.4, -4.0, -0.4, 2.3, 4.2]
        rows_.arrange(DOWN, buff=0.22)
        for r in rows_:
            for c, x in zip(r, xs):
                c.set_x(x + c.width / 2)
        rows_.move_to(DOWN * 0.2)
        head = label(r"does it still sound like itself?", font_size=24, color=GREY_A).to_edge(UP, buff=0.3)
        v = {k: d[k]["votes"] for k in STAGES}
        keys_ok = sum(rt[k]["key_by_count"] == "C major" for k in STAGES)
        with self.voiceover(
            "Three more questions a listener, or a machine, asks of a recording. <bookmark mark='a'/> What is it? Part 63's "
            "fingerprinter was given the sixty-seven Variations and the Tune as performed, and queried with six seconds of "
            f"each stage. On the performance itself the right match has {say(v['played'])} aligned votes. Through the room, "
            f"{say(v['room'])}, barely above the next best; and from the master on, the best match, right or wrong, has "
            f"hardly more votes than the next: {say(v['master'])} against {say(d['master']['runner_up'])} at the master. A fingerprint is a picture of the loudest points of the spectrum, and the room and "
            "the limiter move them. <bookmark mark='b'/> How fast is it? Part 62's tempo estimate stays between "
            f"{say(round(min(d[k]['bpm'] for k in STAGES[:-1])))} and {say(round(max(d[k]['bpm'] for k in STAGES[:-1])))} beats a "
            f"minute until the last stage, where it jumps to {say(round(d['codec16']['bpm']))}, half as fast again, "
            "probably because the coder's false onsets suggest a quicker pulse. <bookmark mark='c'/> And what "
            f"key? Counting the recovered notes, C major at {say(keys_ok)} stages of {say(len(STAGES))}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1], r[2])) for r in rows_[1:]], lag_ratio=0.1), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows_[1:]], lag_ratio=0.1), run_time=1.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r[4]) for r in rows_[1:]], lag_ratio=0.1), run_time=1.0)
        self.wait(0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def room(self):
        d = load("survive")
        c = clip("survive.room")
        a = VGroup(RoundedRectangle(width=3.6, height=1.2, corner_radius=0.12, stroke_color=TUNE), label(r"the performance, \ dry", font_size=19, color=TUNE)).arrange(ORIGIN)
        b = VGroup(RoundedRectangle(width=3.6, height=1.2, corner_radius=0.12, stroke_color=BLUE), label(r"the room alone", font_size=19, color=BLUE)).arrange(ORIGIN)
        VGroup(a, b).arrange(RIGHT, buff=1.0).move_to(UP * 0.5)
        note = label(r"the room's sound, \ with the direct sound taken away: \ what the chain adds, \ and what no score records", font_size=18, color=GREY_A).move_to(DOWN * 1.4)
        with self.voiceover(
            "What the chain adds can be heard on its own. Here is the performance dry, and then the room alone: the room's "
            "sound with the direct sound taken away."
        ):
            self.play(FadeIn(a), FadeIn(b), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"the room, \ alone", kind="physical model", detail=r"Part 38's piano; \ a 1.4 s tail", corner=DL, tag_corner=DR)
            pulse(snd, a, 0.0, d["split"] - 0.6, buff=0.06)
            pulse(snd, b, d["split"], c.duration, buff=0.06)
        with self.voiceover(
            "In the room alone the melody is still faintly there, smeared, because the room only repeats what it is given. "
            "But nothing in a score records it."
        ):
            self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def notation(self):
        led = {r["part"]: r for r in __import__("videos.music.variations", fromlist=["LEDGER"]).LEDGER}
        items = [
            (r"notation records pitch and time, \ and leaves out timbre, \ space and the exact sound \ (Part 10)", WHITE),
            (r"the chain changes timbre and space at every link, \ and pitch and time hardly at all", WHITE),
            (rf"so a score is a code for what survives transmission: \ {led[10]['measure']}", WHITE),
            (r"a copyist, \ a hall, \ a codec: \ each passes the notes on, \ and each changes the sound", WHITE),
            (r"what notation leaves out is not unimportant: \ it is what each performance, \ room and listener supplies", TUNE),
        ]
        rows_scene(self, r"why notation kept what it kept", items,
                   "Why did notation keep what it kept? <bookmark mark='b'/> A basic pitch-duration encoding records selected aspects of pitch and time; richer scores also specify dynamics, instruments and articulation, as Part 10 found. <bookmark mark='c'/> The chain changes timbre and space at every link, and pitch and time hardly at all. <bookmark mark='d'/> So a score is a code for what survives transmission, and a very compact one: Part 10 used an illustrative compact Tune encoding of a hundred and sixty-eight bits, relying on shared decoding assumptions; its PCM audio used vastly more bits, without making this a lossless audio-compression comparison. <bookmark mark='e'/> A copyist, a hall, a codec: each passes the notes on, and each changes the sound. <bookmark mark='f'/> What notation leaves out is not unimportant. It is what each performance, each room and each listener supplies.", marks="bcdef")

    # ------------------------------------------------------------------
    def coda(self):
        items = [
            (r"the model is simple: \ one piano, \ one tune, \ one room, \ one take", WHITE),
            (r"real chains have more links and worse ones: \ phone loudspeakers, \ noisy rooms, \ lossy streams twice over", WHITE),
            (r"the transcriber listens for one line; \ for a chorus or a band, \ the notes survive less well \ (Parts 61 and 64)", WHITE),
            (r"the finding to keep is relative: \ notes outlast sound, \ and a score outlasts both", TUNE),
        ]
        rows_scene(self, r"what this experiment does not show", items,
                   "What does this experiment not show? <bookmark mark='b'/> Its model is simple: one piano, one tune, one room, "
                   "one take. <bookmark mark='c'/> Real chains have more links, and worse ones: phone loudspeakers, noisy rooms, "
                   "streams coded twice over. <bookmark mark='d'/> The transcriber listens for one line; with a chorus or a band "
                   "the notes survive less well, as Parts 61 and 64 found. <bookmark mark='e'/> The finding to keep is relative: "
                   "in this particular chain, some intended note information remains recoverable despite large timbral changes.", marks="bcde")
