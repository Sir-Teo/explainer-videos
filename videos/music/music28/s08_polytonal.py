from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403

KN = ["C", r"C$\sharp$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


SPOKEN = ["C", "C sharp", "D", "E flat", "E", "F", "F sharp", "G", "A flat", "A", "B flat", "B"]


def kspeak(k):
    return SPOKEN[k[0]] + " " + k[1]


def kname(k):
    return KN[k[0]] + (" major" if k[1] == "major" else " minor")


class Polytonal(SoundScene):
    def construct(self):
        chapter(self, 7, r"Two keys at once", r"Can a piece be in C and F$\sharp$ at the same time?")
        self.idea()
        self.hear()
        self.fit()
        self.ives()
        self.paris()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"the Petrushka chord asked: \ what if two keys sound together, \ each one clear?", WHITE),
            (r"bitonality: \ a melody in one key over harmony in another", WHITE),
            (r"Darius Milhaud's \textit{Saudades do Brasil} \ (1920): \ each hand in its own key", WHITE),
            (r"Charles Ives in America: \ two marching bands passing in a parade, \ heard at once", TUNE),
            (r"is it really two keys, \ or one strange one? \ a key-finder can be asked", GREY_A),
        ]
        rows_scene(self, r"bitonality", items,
                   "The Petrushka chord raised a question. <bookmark mark='b'/> What if two keys sound together, each one "
                   "clear? <bookmark mark='c'/> Darius Milhaud, back in Paris from Brazil, wrote piano dances in 1920 with "
                   "each hand in its own key. <bookmark mark='d'/> In America, Charles Ives had already written music that "
                   "remembers two marching bands passing each other in a parade. <bookmark mark='e'/> Is that really two "
                   "keys, or one strange one? Part 15's key-finder can be asked.", marks="cdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("polychord")
        c = clip("polychord.bi")
        g = voices_roll([d["melody"], d["chords"]], width=11.0, height=3.2, colors=[TUNE, EAR], bar_h=0.12).move_to(DOWN * 0.2)
        head = label(r"the Tune in C major, \ over F$\sharp$ major chords \ (ours)", font_size=26, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(r"gold: \ the tune, \ white keys; \ pink: \ F$\sharp$, \ A$\sharp$, \ C$\sharp$, \ black keys", font_size=21, color=GREY_A).next_to(g, DOWN, buff=0.35)
        with self.voiceover(
            "Here is the experiment, on the Tune. Its first two phrases in C major, on the white keys, over a sustained F "
            "sharp major chord, on the black keys: the two keys a tritone apart, as in the Petrushka chord. Listen for "
            "whether you hear two layers, or one."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"C over F$\sharp$", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash_voices(snd, g, [d["melody"], d["chords"]], 0.0, d["unit"], colors=[TUNE, EAR])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fit(self):
        f = load("polychord")["fit"]
        vals = [f["melody"]["r"], f["chords"]["r"], f["both"]["r"]]
        bars = columns(vals, [r"the tune alone", r"the chords alone", r"both together"], width=6.4, height=2.6, color=GREY_B, hot=(0, 1), hot_color=TUNE, fmt="{:.2f}", font_size=19)
        bars.move_to(LEFT * 2.8 + DOWN * 0.4)
        t = label(r"how well the best single key fits \ (Part 15's correlation)", font_size=20, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=22, color=c_) for s, c_ in (
            (rf"the tune: \ {kname(f['melody']['key'])}, \ {f['melody']['r']:.2f}", TUNE),
            (rf"the chords: \ {kname(f['chords']['key'])}, \ {f['chords']['r']:.2f}", TUNE),
            (rf"together: \ the best is {kname(f['both']['key'])}, \ only {f['both']['r']:.2f}", EAR),
            (r"two clear keys make one unclear one", WHITE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        side.move_to(RIGHT * 3.6 + DOWN * 0.2)
        with self.voiceover(
            "Ask the key-finder. <bookmark mark='a'/> The tune alone: C major, with a correlation of "
            f"{say(round(f['melody']['r'], 2))}, about as clear as a key gets. <bookmark mark='b'/> The chords alone: F sharp "
            f"major, {say(round(f['chords']['r'], 2))}. <bookmark mark='c'/> Both together: the best single key it can find "
            f"is {kspeak(f['both']['key'])}, which is neither, "
            f"and it fits only {say(round(f['both']['r'], 2))}. <bookmark mark='d'/> Two clear keys add up to one unclear "
            "one. Whether a listener hears two keys or one strange one depends on keeping the layers apart, by register, "
            "by instrument and by rhythm, which is what Part 45's auditory scene is about."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paris(self):
        items = [
            (r"Paris after 1918: \ `Les Six', \ Satie as their mascot, \ against Wagner's weight and Debussy's mist", WHITE),
            (r"Erik Satie: \ plain, \ ironic, \ repetitive \ (\textit{Gymnopédies}, \ 1888)", WHITE),
            (r"Ravel: \ the \textit{Boléro} \ (1928), \ one tune and one ostinato, \ a crescendo of orchestration", WHITE),
            (r"jazz arrives: \ Milhaud's \textit{La création du monde} \ (1923)", TUNE),
            (r"the new scales and rhythms become ordinary tools, \ in concert music and popular music alike", GREY_A),
        ]
        rows_scene(self, r"Paris between the wars", items,
                   "Paris kept experimenting. <bookmark mark='b'/> After 1918 a group of young composers, Les Six, took Erik "
                   "Satie as their mascot and turned against Wagner's weight and Debussy's mist. <bookmark mark='c'/> Satie's "
                   "music had long been plain, ironic and repetitive; his Gymnopédies date from 1888. <bookmark mark='d'/> "
                   "Ravel's Boléro, of 1928, is one tune over one ostinato, made into a long crescendo of orchestration. "
                   "<bookmark mark='e'/> Jazz arrived, and Milhaud put it into a ballet, La création du monde, in 1923. "
                   "<bookmark mark='f'/> The new scales and rhythms were becoming ordinary tools, in concert music and "
                   "popular music alike.", marks="cdef")

    # ------------------------------------------------------------------
    def ives(self):
        items = [
            (r"Charles Ives, \ 1874--1954: \ an insurance executive who composed in his spare time", WHITE),
            (r"his father, \ a bandmaster, \ had two bands march past each other playing different tunes", WHITE),
            (r"\textit{The Unanswered Question} \ (1908): \ strings in slow triads, \ a trumpet's question, \ flutes that argue", WHITE),
            (r"layers in different keys and tempos, \ heard at once, \ years before Paris", TUNE),
            (r"most of it unperformed for decades; \ a Pulitzer Prize in 1947", GREY_A),
        ]
        rows_scene(self, r"Ives in Connecticut", items,
                   "Americans had got there by another road. <bookmark mark='b'/> Charles Ives ran an insurance agency in New York and composed in his spare time. <bookmark mark='c'/> His father, a Connecticut bandmaster, was remembered for marching two bands past each other playing different tunes. <bookmark mark='d'/> In The Unanswered Question, of 1908, strings play slow triads, a trumpet asks the same phrase again and again, and a group of flutes answers in a different key and tempo. <bookmark mark='e'/> Layers in different keys and tempos, heard at once, years before Paris. <bookmark mark='f'/> Most of it went unperformed for decades; his Third Symphony won a Pulitzer Prize in 1947.", marks="cdef")
