from __future__ import annotations

import numpy as np

from videos.music.music45.common import *  # noqa: F403


class Cont(SoundScene):
    def construct(self):
        chapter(self, 5, r"What fills a gap", r"Does the ear hear what is not there?")
        self.hear()
        self.melody()
        self.warren()
        self.oldnew()

    # ------------------------------------------------------------------
    def glide(self, filled, x0=0.0, w=4.6, h=1.6):
        g = VGroup(Line([x0, 0, 0], [x0 + w, 0, 0], color=GREY_D))
        t = np.linspace(0, 1, 200)
        y = h * (np.log(500 * 3 ** t) - np.log(500)) / np.log(3)
        gap = (t > 0.453) & (t < 0.547)
        pts = [[x0 + w * a, b, 0] for a, b, g_ in zip(t, y, gap)]
        left = VMobject(color=TUNE, stroke_width=4).set_points_as_corners([p for p, g_ in zip(pts, gap) if not g_ and p[0] < x0 + w * 0.5])
        right = VMobject(color=TUNE, stroke_width=4).set_points_as_corners([p for p, g_ in zip(pts, gap) if not g_ and p[0] > x0 + w * 0.5])
        g.add(left, right)
        if filled:
            g.add(Rectangle(width=w * 0.094, height=h * 1.2, stroke_width=0, fill_color=GREY_B, fill_opacity=0.7).move_to([x0 + w * 0.5, h * 0.55, 0]))
        return g

    def hear(self):
        d = load("cont")
        c = clip("cont.two")
        cells = VGroup(VGroup(label(r"a gap of silence", font_size=20, color=WHITE), self.glide(False)).arrange(DOWN, buff=0.3),
                       VGroup(label(r"the same gap, \ filled with noise", font_size=20, color=WHITE), self.glide(True)).arrange(DOWN, buff=0.3)).arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        cap = label(r"pitch against time; \ grey: \ a burst of louder noise", font_size=17, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the continuity illusion", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"A rising glide with a gap of {say(1000 * d['gap'])} milliseconds in the middle, first left silent, then "
            "filled with a burst of louder noise. Listen to the glide in the second version: does it stop?"
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cap))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"silence, \ then noise", kind="synthesized", detail=r"a sine glide, \ noise", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["silence"], st["noise"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["noise"], c.duration, buff=0.1)
        with self.voiceover(
            "With silence the glide plainly breaks. With noise in the gap most people hear the glide carry straight on "
            "through it, though in the noise there is no glide at all. The ear fills in what was probably masked: if a "
            "louder sound could have hidden a continuing one, it assumes it did."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def warren(self):
        items = [
            (r"Richard Warren \ (1970): \ a sentence with one speech sound cut out and replaced by a cough", WHITE),
            (r"listeners heard the missing sound, \ and could not say where the cough was", WHITE),
            (r"`phonemic restoration': \ the brain supplies what context predicts", WHITE),
            (r"in music, \ a melody continues behind a drum hit or a cough in the hall", TUNE),
            (r"only if the interruption is loud enough to have hidden it", GREY_A),
        ]
        rows_scene(self, r"restoration", items,
                   "The same happens with speech. <bookmark mark='b'/> In 1970 Richard Warren played sentences with one speech "
                   "sound cut out and replaced by a cough. <bookmark mark='c'/> Listeners heard the missing sound, and could not "
                   "say where the cough had been: <bookmark mark='d'/> phonemic restoration. <bookmark mark='e'/> In music, a "
                   "melody continues behind a drum hit or a cough in the hall, <bookmark mark='f'/> but only if the interruption "
                   "is loud enough to have hidden it.", marks="bcdef")

    # ------------------------------------------------------------------
    def oldnew(self):
        items = [
            (r"Bregman's `old-plus-new' heuristic: \ if a sound changes, \ first assume the old sound continues and something new began", WHITE),
            (r"subtract the old, \ and what remains is the new source", WHITE),
            (r"a held organ chord plus a new note: \ we hear the chord continue and a melody note arrive", WHITE),
            (r"scene analysis is inference: \ the most likely world that would produce this wave", TUNE),
            (r"chapter 6: \ counterpoint, \ derived from these rules", GREY_A),
        ]
        rows_scene(self, r"old plus new", items,
                   "Bregman summed up such cases as the old-plus-new heuristic. <bookmark mark='b'/> If a sound changes, first "
                   "assume the old sound continues and something new has begun, <bookmark mark='c'/> then subtract the old, and "
                   "what remains is the new source. <bookmark mark='d'/> A held organ chord plus a new note: we hear the chord "
                   "continue and a melody note arrive. <bookmark mark='e'/> Scene analysis is inference, the most likely world "
                   "that would produce this wave. <bookmark mark='f'/> Chapter six derives counterpoint from these rules.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def melody(self):
        d = load("melcont")
        c = clip("melcont.two")
        cells = VGroup(label(r"three notes cut: \ silence", font_size=22, color=WHITE), label(r"the same cuts, \ filled with noise", font_size=22, color=WHITE)).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
        head = label(r"a melody behind noise", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The same works for a melody. The Tune's first phrase on a flute, with a hundred and twenty milliseconds cut out "
            "of three of its notes: first left silent, then filled with noise."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"silence, \ then noise", kind="synthesized", detail=r"additive flute, \ noise", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], st["silence"], st["noise"] - 0.3, buff=0.1)
            pulse(snd, cells[1], st["noise"], c.duration, buff=0.1)
        with self.voiceover(
            "With silence the notes stutter. With noise, the flute seems to play straight through, the noise lying on top."
        ):
            self.play(Indicate(cells[1]))
        self.wait(0.3)
        self.clear_scene()
