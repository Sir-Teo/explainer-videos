from __future__ import annotations

from videos.music.music53.common import *  # noqa: F403


class Musicn(SoundScene):
    def construct(self):
        chapter(self, 2, r"MUSIC N and unit generators", r"How did a computer first make music?")
        self.mathews()
        self.ugens()
        self.heard()
        self.descendants()
        self.realtime()

    # ------------------------------------------------------------------
    def mathews(self):
        items = [
            (r"1957, \ Bell Labs: \ Max Mathews's MUSIC computes a sound sample by sample on an IBM 704", WHITE),
            (r"it was not real time: \ seconds of sound could take hours, \ then be played from tape", WHITE),
            (r"1961: \ a computer sings `Daisy Bell' \ (Kelly, \ Lochbaum and Mathews), \ remembered from a film seven years later", WHITE),
            (r"1960, \ MUSIC III: \ the unit generator: \ small blocks, \ an oscillator, \ an envelope, \ an adder, \ patched together", TUNE),
            (r"the same idea as Moog's modules, \ four years earlier, \ in software", GREY_A),
        ]
        rows_scene(self, r"Max Mathews's MUSIC", items,
                   "The computer made music before it made anything playable. <bookmark mark='b'/> In 1957 at Bell Labs, Max "
                   "Mathews's program MUSIC computed a sound sample by sample on an IBM 704. <bookmark mark='c'/> It was not real "
                   "time: seconds of sound could take hours, then be played back from tape. <bookmark mark='d'/> In 1961 a computer "
                   "sang Daisy Bell, from John Kelly, Carol Lochbaum and Mathews, remembered from a film seven years later. "
                   "<bookmark mark='e'/> And in 1960 MUSIC III introduced the unit generator: small blocks, an oscillator, an "
                   "envelope, an adder, patched together. <bookmark mark='f'/> It is the same idea as Moog's modules, four years "
                   "earlier, in software.", marks="bcdef")

    # ------------------------------------------------------------------
    def ugens(self):
        d = load("musicn")
        blocks = VGroup()
        for t, s, col in ((r"envelope", r"rise 20 ms, \ decay 0.6 s", EAR), (r"oscillator", r"a stored table: \ a sine and two harmonics", TUNE), (r"out", r"summed into the sound", GREY_A)):
            blocks.add(VGroup(RoundedRectangle(width=2.8, height=1.1, corner_radius=0.15, stroke_color=col), VGroup(label(t, font_size=22, color=col), label(s, font_size=13, color=GREY_A)).arrange(DOWN, buff=0.08)).arrange(ORIGIN))
        blocks.arrange(RIGHT, buff=0.9).move_to(UP * 1.3)
        arr = VGroup(Arrow(blocks[0].get_right(), blocks[1].get_left(), buff=0.08, color=GREY_B), Arrow(blocks[1].get_right(), blocks[2].get_left(), buff=0.08, color=GREY_B))
        al = label(r"amplitude", font_size=13, color=GREY_A).next_to(arr[0], UP, buff=0.05)
        score = VGroup(label(r"the score: \ instrument, \ start, \ length, \ frequency", font_size=17, color=WHITE),
                       *[label(s, font_size=16, color=TUNE) for s in d["score"][:4]], label(r"...", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(DOWN * 1.4)
        orch = label(r"the orchestra: \ how each instrument is wired", font_size=17, color=WHITE).next_to(blocks, UP, buff=0.3)
        head = label(r"an orchestra and a score", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "MUSIC split music into two files. <bookmark mark='a'/> The orchestra says how each instrument is wired from unit "
            "generators: here an envelope generator feeding an oscillator's amplitude, the oscillator reading a stored table, a "
            "sine with two harmonics. <bookmark mark='b'/> The score is a list of notes, one line each: which instrument, when it "
            "starts, how long it lasts, and its frequency. That split, instruments and notes, is still how every synthesizer and "
            "sequencer divides the work, and MIDI is its score."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(VGroup(blocks, score), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(orch), FadeIn(blocks), FadeIn(arr), FadeIn(al))
            vo.wait_until("b")
            self.play(FadeIn(score))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        c = clip("musicn.one")
        box = VGroup(RoundedRectangle(width=6.0, height=1.4, corner_radius=0.15, stroke_color=TUNE), label(r"seven lines of score, \ one instrument", font_size=22, color=WHITE)).arrange(ORIGIN).move_to(UP * 0.4)
        head = label(r"the orchestra plays the score, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("The orchestra plays the score: the Tune's first phrase, as a 1960s computer would have computed it."):
            self.play(FadeIn(head), FadeIn(box))
        with self.listen(c) as snd:
            window(snd, r"MUSIC-style", kind="synthesized", detail=r"three unit generators", corner=DL, tag_corner=DR)
            pulse(snd, box, 0.0, c.duration, buff=0.12)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def descendants(self):
        items = [
            (r"MUSIC IV and V \ (1960s), \ then Csound \ (Barry Vercoe, \ 1986): \ orchestra and score still", WHITE),
            (r"Max \ (Miller Puckette, \ 1980s) \ and Pure Data \ (1996): \ unit generators drawn as boxes and wires", WHITE),
            (r"SuperCollider \ (James McCartney, \ 1996): \ unit generators made and destroyed while the music runs", WHITE),
            (r"what changed was speed: \ by the 1990s a personal computer could run them in real time", WHITE),
            (r"and real time brings a deadline \ (chapter 8)", TUNE),
        ]
        rows_scene(self, r"MUSIC's descendants", items,
                   "MUSIC has many descendants. <bookmark mark='b'/> MUSIC IV and V in the 1960s, then Csound, from Barry Vercoe in "
                   "1986, keep the orchestra and the score. <bookmark mark='c'/> Max, from Miller Puckette in the 1980s, and Pure "
                   "Data in 1996, draw unit generators as boxes and wires. <bookmark mark='d'/> SuperCollider, from James McCartney "
                   "in 1996, makes and destroys them while the music runs. <bookmark mark='e'/> What changed was speed: by the 1990s "
                   "a personal computer could run them in real time. <bookmark mark='f'/> And real time brings a deadline, which is "
                   "chapter eight.", marks="bcdef")

    # ------------------------------------------------------------------
    def realtime(self):
        items = [
            (r"the 1970s: \ special hardware made synthesis live: \ Giuseppe Di Giugno's 4X at IRCAM \ (1981), \ the Synclavier", WHITE),
            (r"the 1980s: \ digital chips put FM and samples in every keyboard \ (Part 52)", WHITE),
            (r"the 1990s: \ general-purpose processors caught up, \ and the studio moved into software", WHITE),
            (r"the cost of a voice fell from a cabinet to a few microseconds", WHITE),
            (r"but the instruments still had to talk to each other: \ hence MIDI", TUNE),
        ]
        rows_scene(self, r"real time arrives", items,
                   "Real time arrived in stages. <bookmark mark='b'/> In the 1970s special hardware made synthesis live, from "
                   "Giuseppe Di Giugno's 4X at IRCAM, finished in 1981, to the Synclavier. <bookmark mark='c'/> In the 1980s digital "
                   "chips put FM and samples in every keyboard, as Part 52 told. <bookmark mark='d'/> In the 1990s general-purpose "
                   "processors caught up, and the studio moved into software. <bookmark mark='e'/> The cost of a voice fell from a "
                   "cabinet to a few microseconds. <bookmark mark='f'/> But the instruments still had to talk to each other: hence "
                   "MIDI.", marks="bcdef")
