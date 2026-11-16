from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403


class Film(SoundScene):
    def construct(self):
        chapter(self, 6, r"Wonder, \ and the uncanny", r"Why do some chord changes sound magical?", extra=((2018, r"Lehman's \textit{Hollywood Harmony}"),))
        self.mediants()
        self.quiz()
        self.three()
        self.lehman()
        self.romantics()
        self.scoring()

    # ------------------------------------------------------------------
    def mediants(self):
        items = [
            (r"a chromatic mediant: \ two major \ (or two minor) \ triads a third apart, \ sharing one note", WHITE),
            (r"C major to E major: \ L then P \ (two steps); \ C to A$\flat$ major: \ P then L", WHITE),
            (r"chromatic mediants also admit tonal accounts; \ the Tonnetz puts them two steps apart", WHITE),
            (r"Schubert used them constantly; \ by the twentieth century, \ film did too", TUNE),
            (r"the hook's progression was built from exactly these", GREY_A),
        ]
        rows_scene(self, r"chromatic mediants", items,
                   "The hook's progression used chords called chromatic mediants. <bookmark mark='b'/> Two major triads, or two "
                   "minor ones, a third apart, sharing just one note. <bookmark mark='c'/> C major to E major is L and then P; C "
                   "to A flat major is P and then L. <bookmark mark='d'/> Tonal theory can call them chromatic mediants or explain them through mixture; on the "
                   "Tonnetz they are two steps apart. <bookmark mark='e'/> Schubert used them constantly, and in the twentieth "
                   "century film composers did too. <bookmark mark='f'/> The hook's progression was built from exactly these.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("poles")
        c = clip("poles.quiz")
        card = listen_card(r"C major, \ then another triad, \ twice. \ In one pair the chords share two notes; \ in the other, \ none. \ "
                           r"Which shares none, \ A or B? \ Listen for the strangeness.", width=10.4)
        with self.voiceover(
            "A question for your ears. C major followed by another triad, twice, on the bowed strings. In one pair the two "
            "chords share two notes; in the other they share none at all. Which pair shares nothing, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ga = mroll(d["na"], width=3.6, height=2.4, lo=34, hi=72, color=GREY_A, bar_h=0.12).move_to(LEFT * 3.2 + DOWN * 0.2)
        gb = mroll(d["nb"], width=3.6, height=2.4, lo=34, hi=72, color=GREY_A, bar_h=0.12).move_to(RIGHT * 3.2 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(ga, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gb, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(ga), FadeIn(gb), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's bowed string", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(rf"A: \ C to e: \ L, \ {d['common'][0]} notes shared", font_size=21, color=BLUE).next_to(ga, DOWN, buff=0.35),
                     label(rf"B: \ C to a$\flat$: \ {d['words'][1]}, \ {d['common'][1]} shared, \ the hexatonic pole", font_size=21, color=EAR).next_to(gb, DOWN, buff=0.35))
        with self.voiceover(
            "B shares none: C major to A flat minor, the hexatonic pole. Yet the voices hardly move: C to B, E to E flat, G to "
            f"A flat, a semitone each, {say(d['vl'][1])} in all. A is the gentle L move, to E minor, keeping two notes. Film "
            "composers use the pole for the uncanny: the sound of something nearby that should not be there."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lehman(self):
        items = [
            (r"Frank Lehman, \ \textit{Hollywood Harmony} \ (2018): \ transformations in film scores, \ catalogued", WHITE),
            (r"chromatic mediants for awe and wonder; \ the hexatonic pole for menace and the supernatural", WHITE),
            (r"the scores are in copyright: \ the film analyses the moves, \ and plays its own", WHITE),
            (r"associations depend on film conventions, \ exposure and context", TUNE),
            (r"Part 44 builds music for picture and play", GREY_A),
        ]
        rows_scene(self, r"Hollywood harmony", items,
                   "Film music is now a field of study. <bookmark mark='b'/> Frank Lehman's Hollywood Harmony, of 2018, catalogues these transformations across many scores, <bookmark mark='c'/> chromatic mediants for awe and wonder, the hexatonic pole for menace and the supernatural. <bookmark mark='d'/> The scores are in copyright, so this film analyses the moves and plays its own. <bookmark mark='e'/> Film conventions and listener exposure can shape these associations; a chord change has no fixed emotional meaning. <bookmark mark='f'/> Part 44 builds music for picture and play.",
                   marks="cdef")

    # ------------------------------------------------------------------
    def romantics(self):
        items = [
            (r"Schubert: \ whole sections a major third away from the tonic", WHITE),
            (r"Liszt, \ Wagner: \ hexatonic cycles in \textit{Parsifal}'s magic", WHITE),
            (r"Brahms: \ chromatic mediants inside otherwise classical forms", WHITE),
            (r"the triad survived Wagner; \ what changed was how triads were connected", TUNE),
            (r"the transformational view describes nineteenth-century practice better than keys do", GREY_A),
        ]
        rows_scene(self, r"where the moves came from", items,
                   "The moves were heard long before film. <bookmark mark='b'/> Schubert put whole sections a major third away "
                   "from the home key. <bookmark mark='c'/> Liszt and Wagner used hexatonic chains for magic, as in Parsifal. "
                   "<bookmark mark='d'/> Brahms set chromatic mediants inside otherwise classical forms. <bookmark mark='e'/> The "
                   "triad survived Wagner; what changed was how triads were connected. <bookmark mark='f'/> For much of that "
                   "music, the transformational view describes the practice better than keys do.", marks="cdef")

    # ------------------------------------------------------------------
    def three(self):
        d = load("film3")
        c = clip("film3.three")
        cells = VGroup()
        for m in d["moves"]:
            cells.add(VGroup(label(rf"C, \ {tex_triad(m['to'])}, \ C", font_size=30, color=TUNE), label(m["word"], font_size=24, color=GREY_A),
                             label(rf"{m['common']} common, \ {m['vl']} semitones", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.1)
        head = label(r"three trips away from C major, \ and back", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Three trips away from C major and back, on the bowed strings. To E major and back: L and P, a bright lift. To A "
            "flat major and back: P and L, warmer and darker. To F sharp major and back: four steps, no notes in common, "
            "six semitones of voice leading, tied with D and B flat major for the largest voice-leading distance from C among these triads."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"to E, \ to A$\flat$, \ to F$\sharp$", detail=r"Part 7's bowed string", corner=DL, tag_corner=DR)
            ks = ["E", "Ab", "F#"]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.4 if i < 2 else c.duration
                pulse(snd, cells[i][0], d["starts"][k], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scoring(self):
        items = [
            (r"start from a triad, \ choose the effect, \ then the move", WHITE),
            (r"warmth and lift: \ chromatic mediants, \ LP or PL, \ one note held across", WHITE),
            (r"menace: \ the hexatonic pole, \ three semitone moves, \ no note held", WHITE),
            (r"orchestrate the held note in one instrument, \ so the ear hears the pivot", TUNE),
            (r"the effect depends on context: \ the same move in a hymn sounds like a hymn", GREY_A),
        ]
        rows_scene(self, r"scoring with moves", items,
                   "How does a composer use this? <bookmark mark='b'/> Start from a triad, choose the effect, and then pick the move. <bookmark mark='c'/> For warmth and lift, a chromatic mediant, L P or P L, with one note held across the change. <bookmark mark='d'/> For menace, the hexatonic pole: three voices slide a semitone and no note is held. <bookmark mark='e'/> Give the held note to one instrument, so the ear hears the pivot. <bookmark mark='f'/> And remember that context decides: the same move in a hymn sounds like a hymn.", marks="cdef")
