from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403


class Texture(SoundScene):
    def construct(self):
        chapter(self, 7, r"Textures and the melody of timbres", r"How many ways can one tune be dressed?")
        self.hear()
        self.kinds()
        self.steps()
        self.klang()
        self.schoenberg()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("texture")
        c = clip("texture.four")
        cells = VGroup(*[VGroup(label(t, font_size=21, color=TUNE), label(sub, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.12)
                         for t, sub in zip(d["textures"], (r"violin, \ clarinet, \ cello in octaves", r"flute over strings",
                                                           r"horns, \ trumpet and cello", r"clarinet, \ cello, \ flute in canon"))]).arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.8)).move_to(UP * 0.3)
        with self.voiceover(
            "Texture is how the parts relate in time. Hear the Tune's first phrase four ways: in unison and octaves, three "
            "instruments as one line; as a melody on the flute over a string accompaniment; as a brass chorale, every part "
            "moving together; and as a canon in three parts, each entering two beats after the last."
        ):
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"four textures", kind="synthesized", detail=r"additive instruments", corner=DL, tag_corner=DR)
            ks = d["textures"]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < 3 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def kinds(self):
        items = [
            (r"monophony and unison: \ one line, \ however many players", WHITE),
            (r"melody and accompaniment: \ a foreground and a background", WHITE),
            (r"homophony: \ chords moving together, \ as in Part 17's chorales", WHITE),
            (r"polyphony: \ independent lines, \ as in Part 20's canons and fugues", TUNE),
            (r"an orchestrator chooses the texture first, \ then the instruments", GREY_A),
        ]
        rows_scene(self, r"textures", items,
                   "Those are the four basic textures. <bookmark mark='b'/> Monophony and unison: one line, however many players. "
                   "<bookmark mark='c'/> Melody and accompaniment: a foreground and a background. <bookmark mark='d'/> Homophony: "
                   "chords moving together, as in Part 17's chorales. <bookmark mark='e'/> Polyphony: independent lines, as in "
                   "Part 20's canons and fugues. <bookmark mark='f'/> An orchestrator chooses the texture first, and then the "
                   "instruments.", marks="cdef")

    # ------------------------------------------------------------------
    def klang(self):
        d = load("klang")
        c = clip("klang.two")
        mel = d["melody"]
        roll = mroll(mel, width=10.0, height=1.6, lo=58, hi=72, color=GREY_A, total=8, bar_h=0.18).move_to(UP * 0.6)
        cols = VOICE_C + ["#F59E0B", "#22D3EE"]
        for b, col in zip(roll.notes, cols):
            b.set_color(col)
        names = VGroup(*[label(n.replace(" p", ""), font_size=15, color=col).next_to(b, DOWN, buff=0.12) for n, b, col in zip(d["instruments"], roll.notes, cols)])
        stage = VGroup(label(r"each note a different instrument", font_size=20, color=TUNE), label(r"then all on the clarinet", font_size=20, color=GREY_A)).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "Now a stranger texture. The same phrase, with each note on a different instrument: flute, clarinet, horn, "
            "violin, saxophone, cello and trumpet. Then all of it on the clarinet. The first is a melody of pitches and of "
            "timbres at once."
        ):
            self.play(FadeIn(roll), FadeIn(names), FadeIn(stage))
        beat = d["beat"]
        with self.listen(c) as snd:
            window(snd, r"a melody of timbres", kind="synthesized", detail=r"additive instruments", corner=DL, tag_corner=DR)
            flash(snd, roll.notes, [d["starts"]["klang"] + a * beat for _, a, _ in mel], hot=WHITE, base=GREY_A)
            flash(snd, roll.notes, [d["starts"]["one"] + a * beat for _, a, _ in mel], hot=WHITE, base=GREY_A)
            pulse(snd, stage[0], 0.0, d["starts"]["one"] - 0.4, buff=0.08)
            pulse(snd, stage[1], d["starts"]["one"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def schoenberg(self):
        items = [
            (r"Schoenberg, \ \textit{Harmonielehre} \ (1911): \ \textit{Klangfarbenmelodie}, \ a `melody of tone colours'", WHITE),
            (r"his \textit{Five Orchestral Pieces} \ (1909): \ one movement is a slowly changing chord whose colour moves", WHITE),
            (r"Webern's orchestration of Bach's six-part \textit{Ricercar} \ (1935) \ passes each phrase among instruments", WHITE),
            (r"timbre as a dimension of composition, \ like pitch and rhythm \ (Part 29)", TUNE),
            (r"chapter 8: \ timbre built from instruments", GREY_A),
        ]
        rows_scene(self, r"a melody of tone colours", items,
                   "The idea has a name. <bookmark mark='b'/> In his Harmonielehre of 1911, Schoenberg wrote of "
                   "Klangfarbenmelodie, a melody of tone colours. <bookmark mark='c'/> One of his Five Orchestral Pieces, of 1909, "
                   "is a slowly changing chord whose colour moves among the instruments. <bookmark mark='d'/> Webern's "
                   "orchestration of the six-part Ricercar from Bach's Musical Offering, in 1935, passes each fragment of the "
                   "subject among instruments. <bookmark mark='e'/> Timbre became a dimension of composition, like pitch and "
                   "rhythm in Part 29. <bookmark mark='f'/> Chapter eight builds timbre itself from instruments.", marks="cdef")

    # ------------------------------------------------------------------
    def steps(self):
        items = [
            (r"one: \ decide the texture and the layers, \ from a piano sketch", WHITE),
            (r"two: \ give each layer a family, \ and the melody a colour that carries", WHITE),
            (r"three: \ check ranges, \ registers and breathing for every part", WHITE),
            (r"four: \ balance by number of players and dynamics; \ double what must be heard", TUNE),
            (r"five: \ hear it in rehearsal, \ and revise", GREY_A),
        ]
        rows_scene(self, r"an orchestrator's order of work", items,
                   "Put together, an orchestrator works in an order. <bookmark mark='b'/> First, decide the texture and the layers, usually from a piano sketch. <bookmark mark='c'/> Second, give each layer a family, and the melody a colour that carries. <bookmark mark='d'/> Third, check ranges, registers and breathing for every part. <bookmark mark='e'/> Fourth, balance by the number of players and the dynamics, doubling what must be heard. <bookmark mark='f'/> And fifth, hear it in rehearsal, and revise.", marks="cdef")
