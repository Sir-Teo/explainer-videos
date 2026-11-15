from __future__ import annotations

import numpy as np

from videos.music.music46.common import *  # noqa: F403


class Groove(SoundScene):
    def construct(self):
        chapter(self, 8, r"Groove", r"Why do some rhythms make you want to move?")
        self.define()
        self.hear()
        self.witek()
        self.micro()
        self.entrain()

    # ------------------------------------------------------------------
    def define(self):
        items = [
            (r"groove: \ the pleasurable urge to move to music \ (Janata and colleagues, \ 2012)", WHITE),
            (r"syncopation: \ notes on weak positions followed by silence on stronger ones \ (Part 38)", WHITE),
            (r"Longuet-Higgins and Lee \ (1984): \ add up, \ for every such note, \ how much stronger the silent position is", WHITE),
            (r"a syncopation is a broken metrical expectation: \ the body predicts the beat and the music withholds it", TUNE),
            (r"we score four bass and kick patterns of ours", GREY_A),
        ]
        rows_scene(self, r"groove and syncopation", items,
                   "Expectation also lives in the body. <bookmark mark='b'/> Petr Janata and colleagues defined groove as the "
                   "pleasurable urge to move to music. <bookmark mark='c'/> Syncopation, from Part 38, is a note on a weak "
                   "position followed by silence on a stronger one, <bookmark mark='d'/> and Christopher Longuet-Higgins and "
                   "Christopher Lee measured it in 1984 by adding up, for every such note, how much stronger the silent position "
                   "is. <bookmark mark='e'/> A syncopation is a broken metrical expectation: the body predicts the beat and the "
                   "music withholds it. <bookmark mark='f'/> We score four patterns of ours.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("groove")
        c = clip("groove.four")
        rows_ = VGroup()
        for name, ons in d["patterns"].items():
            cells = VGroup(*[Square(0.32, stroke_color=GREY_D, stroke_width=1, fill_color=TUNE if s in ons else DIM, fill_opacity=1.0 if s in ons else 0.3) for s in range(16)]).arrange(RIGHT, buff=0.05)
            rows_.add(VGroup(label(name, font_size=19, color=WHITE), cells, label(rf"index {d['index'][name]}", font_size=17, color=EAR)).arrange(RIGHT, buff=0.4))
        for r in rows_:
            r[0].set_width(r[0].width)
        rows_.arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to(UP * 0.1)
        head = label(rf"bass and kick on 16 steps, \ {d['bpm']} beats a minute; \ hi-hat and backbeat the same throughout", font_size=22, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Hear four patterns, the same drums and backbeat each time, with the bass and kick moved to more and more "
            "syncopated positions: none, a little, a medium amount, and a lot. Which makes you want to move most?"
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        st = d["starts"]
        names = list(d["patterns"])
        with self.listen(c) as snd:
            window(snd, r"four grooves", detail=r"Part 40's drums, \ a plucked bass", corner=DL, tag_corner=DR)
            for i, n in enumerate(names):
                end = st[names[i + 1]] - 0.3 if i + 1 < len(names) else c.duration
                pulse(snd, rows_[i], st[n], end, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def witek(self):
        x0, y0, W, H = -5.0, -2.2, 7.0, 3.8
        xs = np.linspace(0, 1, 100)
        ys = 1 - (2 * xs - 1) ** 2
        curve = VMobject(color=TUNE, stroke_width=4).set_points_as_corners([[x0 + W * x, y0 + H * (0.15 + 0.8 * y), 0] for x, y in zip(xs, ys)])
        ax = VGroup(Line([x0, y0, 0], [x0 + W, y0, 0], color=GREY_B), Line([x0, y0, 0], [x0, y0 + H, 0], color=GREY_B))
        labs = VGroup(label(r"syncopation", font_size=17, color=GREY_A).move_to([x0 + W / 2, y0 - 0.4, 0]), label(r"wanting to move, \ and pleasure", font_size=17, color=GREY_A).move_to([x0 + 1.0, y0 + H + 0.3, 0]))
        side = VGroup(label(r"Witek and colleagues \ (2014): \ 50 drum breaks rated by 66 listeners", font_size=17, color=WHITE),
                      label(r"ratings rose and then fell with syncopation: \ an inverted U", font_size=17, color=WHITE),
                      label(r"the shape, \ sketched; \ not their data", font_size=15, color=GREY_A),
                      label(r"too regular gives the body nothing to fill; \ too syncopated and the beat is lost", font_size=17, color=TUNE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 4.3)
        side.scale_to_fit_width(min(side.width, 4.6)).move_to(RIGHT * 4.3)
        head = label(r"an inverted U for groove", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Maria Witek and colleagues had sixty-six listeners rate fifty drum breaks in 2014. <bookmark mark='a'/> Wanting "
            "to move, and pleasure, rose with syncopation and then fell: an inverted U, Berlyne's shape again. "
            "<bookmark mark='b'/> Too regular, and the body has nothing to fill in; too syncopated, and the beat itself is "
            "lost. Where on the curve would you put our four patterns?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(side[1:3]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def micro(self):
        items = [
            (r"microtiming: \ tiny deviations from the grid, \ the `feel' of Part 43 and Part 38's swing", WHITE),
            (r"Davies and colleagues \ (2013), \ Fr\"uhauf and colleagues \ (2013): \ adding random microtiming did not raise groove ratings, \ and often lowered them", WHITE),
            (r"systematic patterns, \ like swing, \ can help; \ random wobble does not", WHITE),
            (r"groove seems to come mostly from structure: \ syncopation, \ density, \ and the bass's interplay with the drums", TUNE),
            (r"and why a beat moves the body at all", GREY_A),
        ]
        rows_scene(self, r"is groove in the timing?", items,
                   "Musicians often credit groove to microtiming, the tiny deviations from the grid of Part 43, or the swing of "
                   "Part 38. <bookmark mark='b'/> But in 2013 Matthew Davies and colleagues, and separately Jan Frühauf and "
                   "colleagues, found that adding random microtiming did not raise groove ratings, and often lowered them. "
                   "<bookmark mark='c'/> Systematic patterns like swing can help; random wobble does not. <bookmark mark='d'/> "
                   "Groove seems to come mostly from structure: syncopation, density, and the bass's interplay with the drums. "
                   "<bookmark mark='e'/> Which leaves the question of why a beat moves the body at all.", marks="bcde")

    # ------------------------------------------------------------------
    def entrain(self):
        items = [
            (r"entrainment: \ bodies lock to a beat; \ most people tap, \ nod or sway within seconds", WHITE),
            (r"Zentner and Eerola \ (2010): \ infants move more to music than to speech, \ though not in time with it", WHITE),
            (r"synchronising to a beat is rare among animals: \ some parrots do it, \ most primates do not", WHITE),
            (r"groove may be the pleasure of predicting the beat with the whole body", TUNE),
            (r"chapter 9: \ the emotions music expresses; \ Part 47: \ beat as a universal", GREY_A),
        ]
        rows_scene(self, r"moving to a beat", items,
                   "Why should a beat make us move at all? <bookmark mark='b'/> Entrainment: bodies lock to a beat, and most "
                   "people tap, nod or sway within seconds. <bookmark mark='c'/> Marcel Zentner and Tuomas Eerola found in 2010 "
                   "that infants move more to music than to speech, though not yet in time with it. <bookmark mark='d'/> "
                   "Synchronising to a beat is rare among animals: some parrots do it, most primates do not. "
                   "<bookmark mark='e'/> Groove may be the pleasure of predicting the beat with the whole body. "
                   "<bookmark mark='f'/> Chapter nine turns to the emotions music expresses, and Part 47 takes up the beat as a "
                   "candidate universal.", marks="bcdef")
