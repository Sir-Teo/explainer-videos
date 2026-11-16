from __future__ import annotations

import numpy as np

from videos.music.music29.common import *  # noqa: F403


class Total(SoundScene):
    def construct(self):
        chapter(self, 8, r"Total serialism", r"What if everything were a series?", extra=((1952, r"Boulez's \textit{Structures}"),))
        self.history()
        self.points()
        self.critique()
        self.stravinsky()
        self.reaction()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Webern's late music: \ few notes, \ wide leaps, \ silence, \ symmetry", WHITE),
            (r"Messiaen, \ \textit{Mode de valeurs et d'intensités} \ (1949): \ each pitch with its own duration, \ loudness and attack", WHITE),
            (r"Boulez, \ \textit{Structures Ia} \ (1952): \ pitch, \ duration, \ dynamics and attack all from series", WHITE),
            (r"Stockhausen, \ Nono, \ the Darmstadt summer courses: \ the music of the 1950s avant-garde", TUNE),
            (r"the composer chooses the series; \ the series chooses the notes", GREY_A),
        ]
        rows_scene(self, r"serialize everything", items,
                   "After 1945 the young avant-garde pushed the method to its limit. <bookmark mark='b'/> They admired Webern's late music, few notes, wide leaps, silences and symmetry. <bookmark mark='c'/> Messiaen's piano study Mode de valeurs et d'intensités, of 1949, gives each pitch its own fixed duration, loudness and attack. <bookmark mark='d'/> Pierre Boulez's Structures Ia, of 1952, derives pitch, duration, dynamics and attack all from series. <bookmark mark='e'/> With Stockhausen and Nono and the summer courses at Darmstadt, it became the sound of the 1950s avant-garde. <bookmark mark='f'/> Series constrain selected parameters; composers still choose mappings, registers, structures and exceptions.", marks="cdef")

    # ------------------------------------------------------------------
    def points(self):
        d = load("total")
        c = clip("total.points")
        notes = d["notes"]
        lo = min(n[0] for n in notes) - 2
        hi = max(n[0] for n in notes) + 2
        total = max(n[1] + n[2] for n in notes)
        W, H = 11.0, 3.4
        dots = VGroup()
        for p, a, du, v in notes:
            r = 0.06 + 0.1 * v
            dots.add(Dot([-W / 2 + W * a / total, -0.2 - H / 2 + H * (p - lo) / (hi - lo), 0], radius=r, color=TUNE))
        bars = VGroup(*[Line([-W / 2 + W * a / total, -2.2, 0], [-W / 2 + W * (a + du) / total, -2.2, 0], color=GREY_A, stroke_width=5) for p, a, du, v in notes])
        head = label(r"a pointillist passage \ (ours): \ pitch, \ duration and loudness each from a series", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"dot size: \ loudness; \ grey line: \ duration, \ 1 to 12 sixteenths", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            'Here is the idea in miniature, ours. Twelve notes: their pitch classes from a row, their durations from a series of one to twelve sixteenths, their loudness from a third series, and their octaves scattered. The result is pointillist: single notes, isolated in register and time, each with its own weight. Listen for what you group; the example has no measured listener result.'
        ):
            self.play(FadeIn(head), FadeIn(dots), FadeIn(bars), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"twelve points", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash(snd, list(dots), [n[1] * d["unit"] for n in notes], hot=WHITE, base=TUNE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def critique(self):
        items = [
            (r"Iannis Xenakis \ (1955): \ total serialism sounds like a cloud of points, \ so compose with statistics instead", WHITE),
            (r"Ligeti \ (1958): \ the serial structure of \textit{Structures Ia} cannot be heard; \ only its density can", WHITE),
            (r"John Cage: \ chance operations, \ the \textit{I Ching}: \ another way to remove the composer's taste", WHITE),
            (r"when everything is determined, \ the result can sound random", TUNE),
            (r"Part 30 follows Xenakis into sound itself; \ Part 33 into the mathematics of rhythm", GREY_A),
        ]
        rows_scene(self, r"the cloud of points", items,
                   "Critics came from inside the avant-garde. <bookmark mark='b'/> Iannis Xenakis argued in 1955 that total "
                   "serialism sounds like a cloud of points, and that it would be more honest to compose the cloud directly, "
                   "with statistics. <bookmark mark='c'/> György Ligeti analysed Boulez's Structures in 1958 and concluded that "
                   "its serial order cannot be heard; what can be heard is its density. <bookmark mark='d'/> John Cage, from "
                   "the other side, used chance operations from the I Ching to remove his own taste. "
                   "<bookmark mark='e'/> The paradox: when everything is determined, the result can sound random. "
                   "<bookmark mark='f'/> Part 30 follows Xenakis into sound itself.", marks="cdef")

    # ------------------------------------------------------------------
    def stravinsky(self):
        items = [
            (r"after Schoenberg's death in 1951, \ Stravinsky, \ near seventy, \ begins to use rows", WHITE),
            (r"\textit{Agon} \ (1957), \ \textit{Threni} \ (1958): \ serial and still recognizably his", WHITE),
            (r"his assistant Robert Craft had introduced him to Webern's music", WHITE),
            (r"Copland, \ in his late works, \ tried it too", TUNE),
            (r"the method had become a common language, \ used in many styles", GREY_A),
        ]
        rows_scene(self, r"the old masters turn serial", items,
                   "Even the method's old opponents took it up. <bookmark mark='b'/> After Schoenberg's death in 1951, Stravinsky, then nearly seventy, began to use rows himself, <bookmark mark='c'/> in the ballet Agon of 1957 and the Lamentations of Jeremiah, Threni, of 1958, serial and still unmistakably his. <bookmark mark='d'/> His young assistant Robert Craft had introduced him to Webern's music. <bookmark mark='e'/> Aaron Copland tried the method in his late works too. <bookmark mark='f'/> By the 1960s it was a common language, used in many styles.", marks="cdef")

    # ------------------------------------------------------------------
    def reaction(self):
        items = [
            (r"Terry Riley, \ \textit{In C} \ (1964): \ 53 short figures over a steady pulse, \ in C", WHITE),
            (r"Steve Reich, \ \textit{It's Gonna Rain} \ (1965): \ two tape loops drifting out of phase", WHITE),
            (r"minimalism: \ audible process, \ consonance, \ repetition", WHITE),
            (r"Reich wanted processes the listener can hear happening: \ the opposite of a hidden row", TUNE),
            (r"Part 33 measures phasing and even rhythms", GREY_A),
        ]
        rows_scene(self, r"the reaction", items,
                   "The strongest reaction came from young Americans. <bookmark mark='b'/> Terry Riley's In C, of 1964, is fifty-three short figures over a steady pulse, firmly in C. <bookmark mark='c'/> Steve Reich's It's Gonna Rain, of 1965, lets two tape loops of the same phrase drift slowly out of phase. <bookmark mark='d'/> Minimalism made the process audible, consonant and repetitive. <bookmark mark='e'/> Reich wrote that he wanted processes the listener can hear happening, the opposite of a row hidden in the score. <bookmark mark='f'/> Part 33 measures phasing and even rhythms.", marks="cdef")
