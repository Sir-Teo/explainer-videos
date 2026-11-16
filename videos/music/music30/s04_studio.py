from __future__ import annotations

import numpy as np

from videos.music.music30.common import *  # noqa: F403


class Studio(SoundScene):
    def construct(self):
        chapter(self, 3, r"The electronic studio", r"What if every sound were built from sine waves?", extra=((1951, r"the Cologne studio"),))
        self.cologne()
        self.studie()
        self.varese()
        self.elsewhere()
        self.columbia()

    # ------------------------------------------------------------------
    def cologne(self):
        items = [
            (r"Cologne, \ 1951: \ the studio for electronic music at West German Radio \ (Herbert Eimert)", WHITE),
            (r"the opposite of Paris: \ no recordings, \ only sounds made from electronic oscillators", WHITE),
            (r"Fourier \ (Part 3): \ an ideal periodic sound can be represented by a harmonic Fourier series; nonperiodic sounds require a broader spectral description; \ so build sounds from sines", WHITE),
            (r"Karlheinz Stockhausen's \textit{Studie II} \ (1954): \ sine-tone mixtures on a scale of his own", TUNE),
            (r"\textit{Gesang der Jünglinge} \ (1956): \ a boy's voice and electronic sounds, \ for five groups of loudspeakers", GREY_A),
        ]
        rows_scene(self, r"Cologne", items,
                   "Cologne answered Paris. <bookmark mark='b'/> In 1951 West German Radio founded a studio for electronic "
                   "music, led by Herbert Eimert, <bookmark mark='c'/> which rejected recordings altogether and made every sound "
                   "from electronic oscillators. <bookmark mark='d'/> The idea is Part 3's Fourier: any steady sound is a sum of "
                   "sine waves, so a composer can build sounds from sines, one partial at a time. <bookmark mark='e'/> Karlheinz "
                   "Stockhausen's Study Two, of 1954, is made of mixtures of sine tones on a scale of his own. "
                   "<bookmark mark='f'/> His Song of the Youths, of 1956, joins a boy's voice to electronic sounds, sent round "
                   "the hall through five groups of loudspeakers.", marks="cdef")

    # ------------------------------------------------------------------
    def studie(self):
        d = load("studie")
        c = clip("studie.mixtures")
        lo, hi = 0, 80
        W, H = 10.4, 3.2
        total = max(m["t"] + m["dur"] for m in d["mixtures"])
        bars = VGroup()
        for m in d["mixtures"]:
            grp = VGroup(*[Rectangle(width=W * m["dur"] / total - 0.05, height=0.07, stroke_width=0, fill_color=TUNE, fill_opacity=0.9)
                           .move_to([-W / 2 + W * (m["t"] + m["dur"] / 2) / total, -0.3 - H / 2 + H * (k - lo) / (hi - lo), 0]) for k in m["ks"]])
            bars.add(grp)
        axis = VGroup(*[label(rf"{int(round(100 * 5 ** (k / 25)))} Hz", font_size=15, color=GREY_B).move_to([-W / 2 - 0.7, -0.3 - H / 2 + H * k / 80, 0]) for k in (0, 25, 50, 75)])
        head = label(rf"81 frequencies from 100 Hz, \ each {d['step_cents']:.1f} cents above the last \ ($\sqrt[25]{{5}}$)", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"five mixtures of five sine tones each \ (ours, \ on Stockhausen's scale)", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Stockhausen's scale for Study Two divides the interval of five to one, two octaves and a major third, into "
            "twenty-five equal steps, each a little more than a semitone: a hundred and eleven cents. Eighty-one frequencies "
            "from a hundred hertz. Each of his sounds is a mixture of five sine tones at equal steps on this scale. Here are "
            "five mixtures of our own: mixtures that can be heard as timbres or as multiple tones, depending on spacing, envelopes and listening, each a small synthetic spectrum."
        ):
            self.play(FadeIn(head), FadeIn(bars), FadeIn(axis), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"five sine mixtures", kind="synthesized", detail=r"sine tones", corner=DL, tag_corner=DR)
            for m, b in zip(d["mixtures"], bars):
                pulse(snd, b, m["t"], m["t"] + m["dur"], buff=0.04)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def varese(self):
        items = [
            (r"Edgard Varèse: \ `the liberation of sound' \ ---\ \textit{Ionisation} \ (1931), \ for thirteen percussionists", WHITE),
            (r"Brussels World's Fair, \ 1958: \ the Philips Pavilion, \ designed in Le Corbusier's office by Iannis Xenakis", WHITE),
            (r"\textit{Poème électronique}: \ tape music sent through about 400 loudspeakers \ (as reported)", WHITE),
            (r"heard by some two million visitors: \ electronic music's first mass audience", TUNE),
            (r"Part 55 builds rooms and space; \ Part 54, \ loudspeakers", GREY_A),
        ]
        rows_scene(self, r"Varèse", items,
                   "Edgard Varèse had been calling for the liberation of sound since the 1920s; his Ionisation, of 1931, is "
                   "written for thirteen percussionists. <bookmark mark='c'/> At the Brussels World's Fair of 1958 the Philips "
                   "company built a pavilion, designed in Le Corbusier's office by the young engineer Iannis Xenakis, "
                   "<bookmark mark='d'/> and inside it Varèse's Electronic Poem played through hundreds of loudspeakers, around "
                   "four hundred by the usual account. <bookmark mark='e'/> Some two million visitors heard it: electronic "
                   "music's first mass audience. <bookmark mark='f'/> Parts 54 and 55 build loudspeakers and rooms.", marks="cdef")

    # ------------------------------------------------------------------
    def columbia(self):
        items = [
            (r"New York, \ 1959: \ the Columbia--Princeton Electronic Music Center and its RCA Mark II synthesizer", WHITE),
            (r"programmed by punched paper tape: \ pitch, envelope and timbre \ programmed within the machine’s controls", WHITE),
            (r"Babbitt's serial works for synthesizer; \ Bülent Arel, \ Mario Davidovsky, \ Halim El-Dabh", WHITE),
            (r"Tokyo, \ Milan, \ Utrecht, \ Warsaw: \ radio studios across the world", TUNE),
            (r"the voltage-controlled synthesizer \ (Moog, \ Buchla, \ mid-1960s) \ \ is Part 51", GREY_A),
        ]
        rows_scene(self, r"studios everywhere", items,
                   "Studios multiplied. <bookmark mark='b'/> In New York, from 1959, the Columbia-Princeton Electronic Music "
                   "Center housed the room-sized RCA Mark Two synthesizer, <bookmark mark='c'/> programmed with punched paper "
                   "tape, so that many pitches, envelopes and timbral parameters could be specified within the machine’s finite controls. <bookmark mark='d'/> Babbitt "
                   "wrote serial works for it, and so did Bülent Arel, Mario Davidovsky and Halim El-Dabh. "
                   "<bookmark mark='e'/> Radio studios opened in Tokyo, Milan, Utrecht and Warsaw. <bookmark mark='f'/> In the "
                   "mid-1960s Robert Moog and Don Buchla built voltage-controlled synthesizers, which Part 51 builds.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def elsewhere(self):
        items = [
            (r"Tokyo, \ 1955: \ NHK's electronic studio; \ Toshiro Mayuzumi, \ later Toru Takemitsu's tape works", WHITE),
            (r"Copenhagen: \ Else Marie Pade, \ Denmark's first electronic composer, \ at Danish radio", WHITE),
            (r"Bebe and Louis Barron: \ \textit{Forbidden Planet} \ (1956), \ a film score made entirely of electronic circuits", WHITE),
            (r"the radio station, \ not the concert hall, \ was electronic music's first home", TUNE),
            (r"much of this history was written late, \ and is still being recovered", GREY_A),
        ]
        rows_scene(self, r"studios elsewhere", items,
                   "The new sounds appeared in many places at once. <bookmark mark='b'/> In Tokyo the national broadcaster NHK opened an electronic studio in 1955, where Toshiro Mayuzumi worked, and Toru Takemitsu made tape pieces. <bookmark mark='c'/> In Copenhagen, Else Marie Pade became Denmark's first electronic composer, at Danish radio. <bookmark mark='d'/> In America, Bebe and Louis Barron made the score of the film Forbidden Planet, in 1956, entirely from electronic circuits. <bookmark mark='e'/> The radio station, not the concert hall, was electronic music's first home. <bookmark mark='f'/> Much of this history was written late, and is still being recovered.", marks="cdef")
