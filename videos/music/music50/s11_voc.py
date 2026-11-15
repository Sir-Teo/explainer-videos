from __future__ import annotations

import numpy as np

from videos.music.music50.common import *  # noqa: F403


class Voc(SoundScene):
    def construct(self):
        chapter(self, 10, r"Vocoders and ring modulation", r"How do you make an instrument talk?")
        self.dudley()
        self.bands()
        self.hear()
        self.ring_()
        self.talkbox()
        self.music_()

    # ------------------------------------------------------------------
    def dudley(self):
        items = [
            (r"Homer Dudley \ (Bell Labs, \ 1939): \ the vocoder, \ to send speech in less bandwidth", WHITE),
            (r"split speech into bands; \ send only how loud each band is, \ a few times a second", WHITE),
            (r"at the far end, \ impose those band levels on a buzz or a hiss: \ intelligible, \ robotic speech", WHITE),
            (r"used to encrypt Allied leaders' calls in the Second World War; \ then by musicians from the 1970s", TUNE),
            (r"the voice is the modulator; \ a synthesizer chord is the carrier", GREY_A),
        ]
        rows_scene(self, r"speech, \ compressed", items,
                   "The vocoder began as telephone engineering. <bookmark mark='b'/> Homer Dudley at Bell Labs built it in 1939, to "
                   "send speech in less bandwidth: split speech into bands, and send only how loud each band is, a few times a "
                   "second. <bookmark mark='d'/> At the far end, impose those band levels on a buzz or a hiss, and out comes "
                   "intelligible, robotic speech. <bookmark mark='e'/> It encrypted Allied leaders' calls in the Second World War, "
                   "and musicians took it up from the 1970s. <bookmark mark='f'/> The voice is the modulator; a synthesizer chord is "
                   "the carrier.", marks="bdef")

    # ------------------------------------------------------------------
    def bands(self):
        d = load("vocoder")
        env = np.array(d["envs"])
        env = env / (env.max() + 1e-12)
        img = picture(20 * np.log10(env + 1e-3), -40, 0, 10.0, 3.0).move_to(DOWN * 0.2)
        ed = d["edges"]
        lo = label(rf"{ed[0]:.0f} Hz", font_size=15, color=GREY_A).next_to(img, LEFT, buff=0.15).align_to(img, DOWN)
        hi = label(rf"{ed[-1] / 1000:.0f} kHz", font_size=15, color=GREY_A).next_to(img, LEFT, buff=0.15).align_to(img, UP)
        vw = VGroup(*[label(v, font_size=18, color=TUNE) for v in d["vowels"]]).arrange(RIGHT, buff=1.1).next_to(img, UP, buff=0.2)
        cap = label(r"the voice's level in each of 16 bands, \ low to high, \ through the phrase: \ the pattern the carrier will be given", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"what the vocoder sends", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is what our sixteen-band vocoder extracts from a sung phrase whose vowels change on every note: each band's "
            "level, low frequencies at the bottom, through time. The vowels show as moving patterns of formants. Nothing of the "
            "voice's pitch is kept: only this pattern, which is then stamped onto the carrier."
        ):
            self.play(FadeIn(head), FadeIn(img), FadeIn(lo), FadeIn(hi), FadeIn(vw), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("vocoder")
        c = clip("vocoder.four")
        cells = VGroup()
        for t in (r"the voice", r"the carrier: \ a chord", r"vocoded", r"ring-modulated"):
            cells.add(VGroup(RoundedRectangle(width=2.8, height=1.2, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=19, color=WHITE)).arrange(ORIGIN))
        cells.arrange(RIGHT, buff=0.35).move_to(UP * 0.3)
        head = label(r"the voice, \ the chord, \ and the two together", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the voice, the carrier chord, the chord vocoded by the voice, and last, the voice ring-modulated."):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        keys = ["voice", "carrier", "vocoded", "ring"]
        with self.listen(c) as snd:
            window(snd, r"four sounds", kind="synthesized", detail=r"Part 8's voice, \ a sawtooth chord", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i < 3 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring_(self):
        items = [
            (r"ring modulation: \ multiply the sound by a sine of frequency $f$", WHITE),
            (r"$\sin a \sin b = \tfrac12[\cos(a - b) - \cos(a + b)]$: \ every component at $g$ becomes two, \ at $g - f$ and $g + f$", WHITE),
            (r"the original frequencies vanish; \ the new ones are not harmonic: \ a metallic, \ bell-like voice", WHITE),
            (r"the Daleks' voices on the BBC were made this way; \ Stockhausen used it in concert works", TUNE),
            (r"Part 52 meets frequency modulation, \ its more musical cousin", GREY_A),
        ]
        rows_scene(self, r"ring modulation", items,
                   "Ring modulation is simpler and stranger. <bookmark mark='b'/> Multiply the sound by a sine. Since the product of "
                   "two sines is half the difference of two cosines, every component splits in two, at its frequency minus the "
                   "sine's and plus it. <bookmark mark='d'/> The original frequencies vanish, and the new ones are not harmonic: a "
                   "metallic, bell-like voice. <bookmark mark='e'/> The Daleks' voices on the BBC were made this way, and "
                   "Stockhausen used it in concert works. <bookmark mark='f'/> Part 52 meets frequency modulation, its more musical "
                   "cousin.", marks="bdef")

    # ------------------------------------------------------------------
    def talkbox(self):
        items = [
            (r"the talk box: \ a tube carries an instrument's sound into the player's mouth", WHITE),
            (r"the mouth shapes it as it would a vowel, \ and a microphone picks it up", WHITE),
            (r"it is a vocoder made of flesh: \ the mouth's formants are the filter bank", WHITE),
            (r"Peter Frampton and Roger Troutman made it famous in the 1970s and 80s", TUNE),
            (r"the vocoder, \ the talk box and pitch correction all make an instrument out of a voice, \ or a voice out of an instrument", GREY_A),
        ]
        rows_scene(self, r"the talk box", items,
                   "The vocoder has a mechanical cousin. <bookmark mark='b'/> In a talk box, a tube carries an instrument's sound "
                   "into the player's mouth; <bookmark mark='c'/> the mouth shapes it as it would a vowel, and a microphone picks it "
                   "up. <bookmark mark='d'/> It is a vocoder made of flesh, whose filter bank is the mouth's formants. "
                   "<bookmark mark='e'/> Peter Frampton and Roger Troutman made it famous in the 1970s and 80s. "
                   "<bookmark mark='f'/> The vocoder, the talk box and pitch correction all make an instrument out of a voice, or "
                   "a voice out of an instrument.", marks="bcdef")

    # ------------------------------------------------------------------
    def music_(self):
        items = [
            (r"Wendy Carlos used a vocoder to make a choir of synthesizers sing in \textit{A Clockwork Orange} \ (1971)", WHITE),
            (r"Kraftwerk made it the voice of machines on \textit{Autobahn} \ (1974) \ and after", WHITE),
            (r"Herbie Hancock, \ Laurie Anderson and Daft Punk each found a different character in it", WHITE),
            (r"the more bands, \ the clearer the words; \ the brighter the carrier, \ the more of them survive", TUNE),
            (r"a 1930s telephone experiment, \ kept alive by musicians", GREY_A),
        ]
        rows_scene(self, r"the vocoder in music", items,
                   "Musicians kept the vocoder alive. <bookmark mark='b'/> Wendy Carlos used one to make synthesizers sing in A "
                   "Clockwork Orange, in 1971. <bookmark mark='c'/> Kraftwerk made it the voice of machines on Autobahn, in 1974, "
                   "and after. <bookmark mark='d'/> Herbie Hancock, Laurie Anderson and Daft Punk each found a different character "
                   "in it. <bookmark mark='e'/> The more bands, the clearer the words; and the brighter the carrier, the more of them "
                   "survive. <bookmark mark='f'/> A 1930s telephone experiment, kept alive by musicians.", marks="bcdef")
