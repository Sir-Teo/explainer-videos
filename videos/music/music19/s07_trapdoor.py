from __future__ import annotations

import numpy as np

from videos.music.music19.common import *  # noqa: F403


class Trapdoor(SoundScene):
    def construct(self):
        chapter(self, 6, r"Enharmonic trapdoors", r"How can one chord mean two things?")
        self.quiz()
        self.spelling()
        self.dim7_doors()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("trapdoor")
        c = clip("trapdoor.two")
        card = listen_card(r"Two passages in C major. \ Their third chords are the same four piano keys. \ "
                           r"Which passage stays in C, \ and which leaves it: \ A or B?", width=10.0)
        with self.voiceover(
            "Two passages, both starting in C major. Their third chords are played on exactly the same four piano "
            "keys. One passage comes home to C. The other falls through a trapdoor. Which is which?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        sA = block_staff(d["home"], width=5.6, beats=2, flats=True).move_to(LEFT * 3.3 + DOWN * 0.1)
        sB = block_staff(d["away"], width=6.2, beats=2, flats=True).move_to(RIGHT * 3.3 + DOWN * 0.1)
        VGroup(sA, sB).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.1)
        la = label(r"A", font_size=40, color=GREY_A).next_to(sA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(sB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(sA), FadeIn(sB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, la, d["starts"]["home"], d["starts"]["away"] - 0.6, buff=0.1)
            pulse(snd, lb, d["starts"]["away"], c.duration, buff=0.1)
        na = VGroup(*[label(tex(n), font_size=19, color=EAR if n.startswith("Ger") else GREY_A) for n in d["home_names"]])
        nb = VGroup(*[label(tex(n.replace(" of ", "/")), font_size=19, color=EAR if "of" in n else GREY_A) for n in d["away_names"]])
        for st, names in ((sA, na), (sB, nb)):
            for k, n in enumerate(names):
                n.move_to([st.get_left()[0] + 1.0 + (st.width - 1.2) * (k + 0.5) / len(names), st.get_bottom()[1] - 0.35, 0])
        with self.voiceover(
            "A stays home. Its third chord is a German sixth in C, A flat, C, E flat, F sharp, and it opens out onto "
            "G, the dominant, and home. B leaves. Its third chord is the same four keys, but heard as A flat, C, E "
            "flat, G flat: the dominant seventh of D flat. And it goes where a dominant seventh goes, to D flat major, "
            "a key with five flats, a semitone above where we started. One chord; two spellings; two destinations."
        ):
            self.play(FadeIn(na), FadeIn(nb))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spelling(self):
        kb = keyboard(0, 23, width=8.4, height=2.0, lit=[8, 12, 15, 18], color=EAR).move_to(UP * 1.6)
        left = VGroup(label(r"German sixth in C", font_size=26, color=TUNE),
                      label(r"A$\flat$ \ C \ E$\flat$ \ F$\sharp$", font_size=30, color=WHITE),
                      label(r"F$\sharp$ rises to G; \ A$\flat$ falls to G", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(LEFT * 3.4 + DOWN * 1.3)
        right = VGroup(label(r"dominant seventh of D$\flat$", font_size=26, color=EAR),
                       label(r"A$\flat$ \ C \ E$\flat$ \ G$\flat$", font_size=30, color=WHITE),
                       label(r"G$\flat$ falls to F; \ the bass A$\flat$ falls a fifth to D$\flat$", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.4 + DOWN * 1.3)
        mid = label(r"F$\sharp$ = G$\flat$ \ on the keyboard", font_size=24, color=EAR).move_to(DOWN * 3.0)
        with self.voiceover(
            "Here is the trick on the keyboard. <bookmark mark='a'/> On the left, the German sixth in C: its F sharp "
            "wants to rise to G, its A flat to fall to G. <bookmark mark='b'/> On the right, the same keys as a "
            "dominant seventh in D flat: the same black key is now G flat, which wants to fall to F, and the bass A "
            "flat wants to fall a fifth to D flat. <bookmark mark='c'/> On a keyboard tuned in equal temperament, F "
            "sharp and G flat are one key, so the listener cannot tell which chord it is until the next chord arrives. "
            "Music theorists call a chord like this a pivot by enharmonic reinterpretation. Composers called it a "
            "door."
        ) as vo:
            self.play(FadeIn(kb))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(mid))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dim7_doors(self):
        d = load("dim7")
        names = ["C", "D♭", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]
        centre = LEFT * 3.2 + DOWN * 0.2
        R = 2.0
        pts = {k: centre + R * np.array([np.sin(2 * np.pi * k / 12), np.cos(2 * np.pi * k / 12), 0]) for k in range(12)}
        ring = Circle(radius=R, color=DIM, stroke_width=2).move_to(centre)
        labs = VGroup(*[label(tex(names[k]), font_size=20, color=GREY_B).move_to(centre + (R + 0.42) * (pts[k] - centre) / R) for k in range(12)])
        chord = d["chord"]
        sq = Polygon(*[pts[k] for k in chord], color=EAR, stroke_width=4)
        targets = sorted({k for k, _ in d["eight"]})
        tdots = VGroup(*[Dot(pts[k], radius=0.13, color=TUNE) for k in targets])
        arrows = VGroup(*[Arrow(pts[(k + 11) % 12], pts[k], buff=0.12, color=TUNE, stroke_width=3, max_tip_length_to_length_ratio=0.35) for k in targets])
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"the German sixth: \ a door to the key a semitone up", WHITE),
            (r"the diminished seventh: \ doors to four tonics, \ a minor third apart", WHITE),
            (r"each major or minor: \ eight keys from one chord", WHITE),
            (r"from C: \ to E$\flat$, \ F$\sharp$ \ and A, \ in a single step", TUNE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.6))
        rows_.move_to(RIGHT * 3.0 + DOWN * 0.1)
        with self.voiceover(
            "There are other doors. <bookmark mark='a'/> The German sixth opens onto the key a semitone above. "
            "<bookmark mark='b'/> The diminished seventh of chapter five opens four ways, since each of its notes can be "
            "a leading note: to C, E flat, F sharp and A, four tonics a minor third apart, <bookmark mark='c'/> each "
            "major or minor. <bookmark mark='d'/> So from C, a composer can arrive in F sharp, the key furthest from C "
            "on the circle of fifths, in a single chord. Schubert, Liszt and Wagner used these doors constantly; "
            "Liszt's diminished sevenths, in the storms of his piano music, are doors left swinging."
        ) as vo:
            self.play(Create(ring), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(Create(sq), FadeIn(rows_[1]))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(tdots))
            vo.wait_until("c")
            self.play(FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[3]), Indicate(tdots[2], color=EAR))
        self.wait(0.4)
        self.clear_scene()
