from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403

MOOD_C = {"heroic": TUNE, "tender": BLUE, "menacing": EAR}


class Motif(SoundScene):
    def construct(self):
        chapter(self, 2, r"Leitmotifs", r"How does music follow a character?")
        self.history()
        self.hear()
        self.kept()
        self.games()
        self.examples()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Wagner's leitmotifs \ (Part 27): \ a motive for each character, \ object or idea, \ transformed with the drama", WHITE),
            (r"Max Steiner and Erich Korngold, \ trained in Vienna, \ brought them to Hollywood in the 1930s", WHITE),
            (r"John Williams revived the full symphonic leitmotif score in the 1970s and 1980s", WHITE),
            (r"a motive heard early comes back changed: \ the audience reads the change as the story", TUNE),
            (r"Part 42's operations on a motive, \ used for drama", GREY_A),
        ]
        rows_scene(self, r"from Wagner to Hollywood", items,
                   "Music can follow characters, not only actions. <bookmark mark='b'/> Wagner's leitmotifs, from Part 27, gave "
                   "each character, object or idea a motive and transformed it with the drama. <bookmark mark='c'/> Max Steiner "
                   "and Erich Korngold, trained in Vienna, brought the idea to Hollywood in the 1930s, <bookmark mark='d'/> and "
                   "John Williams revived the full symphonic leitmotif score in the 1970s and 1980s. <bookmark mark='e'/> A "
                   "motive heard early comes back changed, and the audience reads the change as the story. "
                   "<bookmark mark='f'/> These are Part 42's operations on a motive, used for drama.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("motif")
        c = clip("motif.three")
        cells = VGroup()
        sub = {"heroic": r"horn, \ dotted, \ over strings", "tender": r"flute, \ slow, \ an octave up", "menacing": r"low strings, \ minor, \ the fifth bent to a tritone"}
        for k in d["moods"]:
            mel = d["versions"][k]
            r = scored([[m, a, dd] for m, a, dd in mel], None, width=3.4, height=1.4, lo=46, hi=70, color=MOOD_C[k], bars=1)
            cells.add(VGroup(label(k, font_size=22, color=MOOD_C[k]), r, label(sub[k], font_size=15, color=GREY_A)).arrange(DOWN, buff=0.2))
        cells.arrange(RIGHT, buff=0.7).move_to(UP * 0.3)
        head = label(r"one motive, \ three moods", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is Part 42's motive, E, D, C, up to G, as a leitmotif in three moods. Heroic: a horn, the rhythm sharpened "
            "into a dotted figure, over strings. Tender: a flute, slower, an octave up. Menacing: low strings, in the minor, "
            "with the leap bent from a fifth to a tritone."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        beats = {"heroic": 0.42, "tender": 0.8, "menacing": 0.6}
        with self.listen(c) as snd:
            window(snd, r"three moods", kind="synthesized", detail=r"the additive orchestra", corner=DL, tag_corner=DR)
            for i, k in enumerate(d["moods"]):
                end = st[d["moods"][i + 1]] - 0.3 if i < 2 else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.1)
                flash(snd, cells[i][1].roll.notes, [st[k] + n[1] * beats[k] for n in d["versions"][k]], hot=WHITE, base=MOOD_C[k])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kept(self):
        items = [
            (r"kept: \ the contour \ (down, \ down, \ up a leap) \ and the order of long and short notes", WHITE),
            (r"changed: \ instrument, \ register, \ tempo, \ mode, \ and the size of the leap", WHITE),
            (r"listeners recognise a motive by contour and rhythm long after its exact intervals change \ (Part 14)", WHITE),
            (r"so a score can tell a story with one idea: \ who the character is stays, \ how they are changes", TUNE),
            (r"chapter 3: \ deciding where the music goes", GREY_A),
        ]
        rows_scene(self, r"what the transformations keep", items,
                   "What makes all three the same motive? <bookmark mark='b'/> They keep the contour, down, down, then up by a "
                   "leap, and the order of long and short notes. <bookmark mark='c'/> They change the instrument, register, "
                   "tempo, mode and the size of the leap. <bookmark mark='d'/> Listeners recognise a motive by its contour and "
                   "rhythm long after its exact intervals have changed, as Part 14 found for melodies. <bookmark mark='e'/> So a "
                   "score can tell a story with one idea: who the character is stays the same, how they are changes. "
                   "<bookmark mark='f'/> Chapter three turns to deciding where the music goes.", marks="bcdef")

    # ------------------------------------------------------------------
    def examples(self):
        items = [
            (r"Bernard Herrmann's \textit{Psycho} \ (1960): \ strings only, \ the shower's shrieking glissandi", WHITE),
            (r"John Williams's \textit{Jaws} \ (1975): \ two notes a semitone apart, \ faster as the shark comes nearer", WHITE),
            (r"Howard Shore's \textit{The Lord of the Rings} \ (2001 to 2003): \ dozens of leitmotifs, \ as in Wagner's \textit{Ring}", WHITE),
            (r"the simplest motives travel furthest: \ a rhythm, \ an interval, \ a timbre", TUNE),
            (r"described here, \ not played: \ these scores are in copyright", GREY_A),
        ]
        rows_scene(self, r"motives on screen", items,
                   "Some famous cases, described rather than played, since these scores are in copyright. "
                   "<bookmark mark='b'/> Bernard Herrmann's Psycho of 1960 is for strings only, with the shower scene's shrieking "
                   "glissandi. <bookmark mark='c'/> John Williams's Jaws, of 1975, is two notes a semitone apart, played faster "
                   "as the shark comes nearer. <bookmark mark='d'/> Howard Shore's Lord of the Rings scores use dozens of "
                   "leitmotifs, as Wagner's Ring does. <bookmark mark='e'/> The simplest motives travel furthest: a rhythm, an "
                   "interval, a timbre.", marks="bcde")

    # ------------------------------------------------------------------
    def games(self):
        items = [
            (r"games use leitmotifs too: \ a theme for a place, \ a character, \ an item found", WHITE),
            (r"a short `jingle' becomes the sound of an event: \ a door unlocked, \ a level cleared", WHITE),
            (r"heard hundreds of times, \ such motives become some of the best-known music of their generation", WHITE),
            (r"a series can carry a motive across decades, \ re-orchestrated for each new machine", TUNE),
            (r"the motive outlives every sound chip that played it \ (chapter 9)", GREY_A),
        ]
        rows_scene(self, r"motives in games", items,
                   "Games use leitmotifs too. <bookmark mark='b'/> A theme for a place, a character or an item found; "
                   "<bookmark mark='c'/> a short jingle that becomes the sound of an event, a door unlocked or a level cleared. "
                   "<bookmark mark='d'/> Heard hundreds of times, such motives have become some of the best-known music of their "
                   "generation. <bookmark mark='e'/> A long-running series can carry a motive across decades, re-orchestrated for "
                   "each new machine, <bookmark mark='f'/> so the motive outlives every sound chip that ever played it.",
                   marks="bcdef")
