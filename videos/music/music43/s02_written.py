from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403


class Written(SoundScene):
    def construct(self):
        chapter(self, 1, r"What a performer adds", r"What is missing from a score played exactly?")
        self.seashore()
        self.hear()
        self.drawn()
        self.controls()
        self.repp()

    # ------------------------------------------------------------------
    def seashore(self):
        items = [
            (r"Carl Seashore \ (1938): \ the artistic expression of feeling lies in `deviation from the exact'", WHITE),
            (r"his Iowa laboratory filmed piano hammers and photographed singers' pitch: \ nobody played as written", WHITE),
            (r"a score fixes pitches and proportions; \ a performance chooses milliseconds, \ loudness and connection", WHITE),
            (r"a computer playing the score exactly is the `deadpan' performance: \ the reference every study measures from", TUNE),
            (r"Part 10's notation leaves this out on purpose", GREY_A),
        ]
        rows_scene(self, r"deviation from the exact", items,
                   "In 1938 the psychologist Carl Seashore wrote that the artistic expression of feeling in music lies in "
                   "deviation from the exact. <bookmark mark='b'/> His laboratory in Iowa filmed piano hammers and photographed "
                   "singers' pitch, and found that nobody played as written. <bookmark mark='c'/> A score fixes pitches and "
                   "proportions; a performance chooses milliseconds, loudness and connection. <bookmark mark='d'/> A computer "
                   "playing the score exactly gives the deadpan performance, the reference every study measures from. "
                   "<bookmark mark='e'/> Part 10's notation leaves all this out on purpose.", marks="bcde")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("written")
        c = clip("written.two")
        tot = max(p["t"] + p["dur"] for p in d["performed"])
        a = perf_roll(d["deadpan"], width=11.0, height=1.3, lo=58, hi=72, total=tot, color=GREY_B)
        b = perf_roll(d["performed"], width=11.0, height=1.3, lo=58, hi=72, total=tot, vel=True)
        g = VGroup(VGroup(label(r"as written", font_size=19, color=GREY_B), a).arrange(DOWN, buff=0.12, aligned_edge=LEFT),
                   VGroup(label(r"performed by rules", font_size=19, color=TUNE), b).arrange(DOWN, buff=0.12, aligned_edge=LEFT)).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        cap = label(r"time runs across, \ on one scale for both; \ the performed notes' brightness follows their loudness", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the Tune's first two phrases, \ twice", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear the Tune's first two phrases twice: first exactly as written, then performed by a handful of rules we will "
            "take apart in the next chapter. The notes are the same; listen for what changes."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"written, \ then performed", detail=r"Part 7's piano, \ a plucked bass", corner=DL, tag_corner=DR)
            flash(snd, a.notes, [st["written"] + p["t"] for p in d["deadpan"]], hot=WHITE, base=GREY_B)
            flash(snd, b.notes, [st["performed"] + p["t"] for p in d["performed"]], hot=WHITE, base=TUNE)
            cursor(snd, a, st["written"], 1.0)
            cursor(snd, b, st["performed"], 1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drawn(self):
        d = load("written")
        s = value_bars(d["stretch"], width=10.5, height=1.4, base=1.0, scale=3.0)
        v = value_bars(d["vel"], width=10.5, height=1.4, base=float(np.mean(d["vel"])), scale=2.5, color=EAR, neg=BLUE)
        g = VGroup(VGroup(label(r"each note's length against the written length \ (up: \ longer)", font_size=18, color=TUNE), s).arrange(DOWN, buff=0.25, aligned_edge=LEFT),
                   VGroup(label(r"each note's loudness against the average \ (up: \ louder)", font_size=18, color=EAR), v).arrange(DOWN, buff=0.25, aligned_edge=LEFT)).arrange(DOWN, buff=0.6).move_to(DOWN * 0.1)
        mx = max(d["stretch"])
        head = label(r"the difference, \ drawn", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Draw the difference, note by note. <bookmark mark='a'/> Lengths: the notes near each phrase's start and end are "
            f"stretched, the last of each phrase by up to {say(100 * (mx - 1))} per cent, and the middles keep the written "
            "tempo. <bookmark mark='b'/> Loudness: each phrase swells to its middle and falls away, and the higher notes "
            "stand out. Two phrases, fourteen notes, and the shape is already unmistakably a performer's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(g[0]).copy().set_opacity(0.15)))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def controls(self):
        items = [
            (r"timing: \ when each note starts, \ and how the tempo bends across a phrase", WHITE),
            (r"dynamics: \ how loud each note is, \ and how loudness moves", WHITE),
            (r"articulation: \ how long each note lasts against the gap to the next", WHITE),
            (r"timbre and intonation: \ on instruments that allow it, \ the colour and the exact pitch", TUNE),
            (r"a pianist controls only when, \ how hard and how long \ (Part 7): \ everything else follows from those", GREY_A),
        ]
        rows_scene(self, r"what a performer controls", items,
                   "What can a performer change? <bookmark mark='b'/> Timing: when each note starts, and how the tempo bends "
                   "across a phrase. <bookmark mark='c'/> Dynamics: how loud each note is, and how loudness moves. "
                   "<bookmark mark='d'/> Articulation: how long each note lasts against the gap to the next. "
                   "<bookmark mark='e'/> And on instruments that allow it, timbre and the exact pitch. <bookmark mark='f'/> A "
                   "pianist, as Part 7 showed, controls only when a key goes down, how hard, and when it comes up: everything "
                   "else follows from those three numbers per note.", marks="cdef")

    # ------------------------------------------------------------------
    def repp(self):
        items = [
            (r"Bruno Repp \ (1992) \ measured 28 recordings of Schumann's \textit{Tr\"aumerei} \ by 24 famous pianists", WHITE),
            (r"almost all slowed at the same places: \ phrase ends, \ and above all the end of the piece", WHITE),
            (r"the shared pattern was a slowing like a body coming to rest; \ the individuality lay in the details", WHITE),
            (r"a typical timing profile, \ and departures from it: \ what is common and what is personal can be measured", TUNE),
            (r"chapter 2: \ rules that produce the common part", GREY_A),
        ]
        rows_scene(self, r"twenty-eight Tr\"aumereis", items,
                   "Do performers agree? <bookmark mark='b'/> In 1992 Bruno Repp measured twenty-eight recordings of "
                   "Schumann's Träumerei by twenty-four famous pianists. <bookmark mark='c'/> Almost all of them slowed at the "
                   "same places: at phrase ends, and above all at the end of the piece. <bookmark mark='d'/> The shared pattern "
                   "looked like a body coming to rest; the individuality lay in the details. <bookmark mark='e'/> So a typical "
                   "timing profile, and each performer's departures from it, can both be measured. <bookmark mark='f'/> Chapter "
                   "two writes rules that produce the common part.", marks="bcdef")
