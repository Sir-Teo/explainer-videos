from __future__ import annotations

from videos.music.music63.common import *  # noqa: F403


class Recordings(SoundScene):
    def construct(self):
        chapter(self, 4, r"Recordings, \ not songs", r"Does a fingerprint know the song, \ or only the recording?")
        self.fresh()
        self.meaning()

    # ------------------------------------------------------------------
    def fresh(self):
        d = load("falsematch")
        c = clip("unknown.one")
        top = d["fresh_top"]
        note = VGroup(label(r"the Tune, \ on Part 38's piano, \ at a tempo no earlier part used", font_size=20, color=WHITE),
                      label(rf"best match: \ {top[0]['track'].split('/')[1]} \ ({top[0]['votes']} votes): \ no recording found" if top and top[0]["votes"] < 12 else
                            rf"best match: \ {top[0]['track'] if top else 'none'} \ ({top[0]['votes'] if top else 0} votes)", font_size=18, color=EAR)).arrange(DOWN, buff=0.4).move_to(DOWN * 0.6)
        head = label(r"a new recording of an old song", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the Tune, the song this whole series is built on, rendered afresh on the piano at a tempo no earlier part used. The library holds dozens of recordings of this song. Does the fingerprinter know it?"):
            self.play(FadeIn(head), FadeIn(note[0]))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ new", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, note[0], 0.0, c.duration, rate=5.0, color=GREY_B, buff=0.15)
        with self.voiceover(
            "No. It finds nothing: a handful of scattered votes. A fingerprint identifies a recording, its exact peaks at their "
            "exact times. A new performance of the same song, at another tempo, has other peaks entirely."
        ):
            self.play(FadeIn(note[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        items = [
            (r"fingerprints answer `which recording?': \ exact, \ fast, \ and blind to the song", WHITE),
            (r"`which song?' \ needs Part 62's cover matching: \ chroma, \ any key, \ any tempo; \ slower and less sure", WHITE),
            (r"`songs like this?' \ needs features of sound and style: \ the next chapters", WHITE),
            (r"Content ID can tell a re-upload from a cover: \ the rights in each are different \ (Part 60)", WHITE),
            (r"three questions, \ three kinds of similarity: \ the same signal, \ the same composition, \ the same taste", TUNE),
        ]
        rows_scene(self, r"three kinds of sameness", items,
                   "This is a feature, not a flaw. <bookmark mark='b'/> Fingerprints answer which recording: exactly, fast, and "
                   "blind to the song. <bookmark mark='c'/> Which song needs Part 62's cover matching, by chroma in any key and at "
                   "any tempo: slower, and less sure. <bookmark mark='d'/> Songs like this one needs features of sound and style, the "
                   "subject of the next chapters. <bookmark mark='e'/> And the difference matters for money: a re-upload and a cover "
                   "carry different rights, as Part 60 explained. <bookmark mark='f'/> Three questions, three kinds of similarity: "
                   "the same signal, the same composition, the same taste.", marks="bcdef")
