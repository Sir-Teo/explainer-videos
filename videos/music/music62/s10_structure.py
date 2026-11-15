from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Structure(SoundScene):
    def construct(self):
        chapter(self, 9, r"Structure", r"Can a machine hear the form of a song?")
        self.ssm()
        self.novelty()
        self.repetition()
        self.forms()
        self.practice()

    # ------------------------------------------------------------------
    def ssm(self):
        d = load("structure")
        c = clip("structure.tune")
        S = np.array(d["S"])
        size = 4.6
        pic = picture(S[::-1], 0.5, 1.0, size, size).move_to(LEFT * 2.6 + DOWN * 0.3)
        dur = d["seconds"]
        x0, y1 = pic.get_left()[0], pic.get_top()[1]
        side = VGroup(label(r"every moment against every other: \ bright where the chroma matches", font_size=17, color=WHITE),
                      label(r"the bright diagonal: \ each moment matches itself", font_size=17, color=GREY_A),
                      label(r"stripes parallel to it: \ passages that repeat", font_size=17, color=TUNE)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 3.4 + DOWN * 0.3)
        head = label(r"the whole Tune, \ against itself", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the whole Tune by the session, and watch its self-similarity matrix: every moment compared with every other, bright where the chroma matches."):
            self.play(FadeIn(head), FadeIn(pic), FadeIn(side[0]))
        with self.listen(c) as snd:
            window(snd, r"the whole Tune", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            dot = Dot(pic.get_corner(UL), radius=0.07, color=EAR)
            snd.show(dot)
            snd.drive(dot, lambda m, t: m.move_to([x0 + size * min(t, dur) / dur, y1 - size * min(t, dur) / dur, 0]))
        with self.voiceover("The bright diagonal is each moment matching itself. The stripes parallel to it are passages that repeat: the shape of the song, drawn by the song."):
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def novelty(self):
        d = load("structure")
        nov = np.array(d["nov"])
        hop = 2 * d["hop_s"]
        t = np.arange(len(nov)) * hop
        ax = frame_axes(width=10.0, height=2.0, xlo=0, xhi=t[-1], ylo=0, yhi=1.05, center=DOWN * 0.3)
        cv = curve(t, nov, ax.to, color=BLUE, width=2.5)
        tb = VGroup(*[DashedLine(ax.to(x, 0), ax.to(x, 1.05), color=TUNE, stroke_width=2) for x in d["true_bounds"]])
        fb = VGroup(*[Triangle(fill_color=EAR, fill_opacity=1, stroke_width=0).scale(0.08).rotate(PI).move_to(ax.to(x, 1.12)) for x in d["novelty_bounds"]])
        note = label(rf"the sections change at {d['true_bounds'][0]:.1f} and {d['true_bounds'][1]:.1f} s \ (gold); \ the novelty's peaks \ (red) \ at "
                     + ", ".join(f"{x:.1f}" for x in d["novelty_bounds"]) + " s", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"Foote's novelty \ (2000)", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Jonathan Foote's method of 2000 slides a checkerboard along the diagonal and looks for places where the music "
            "before differs from the music after. <bookmark mark='a'/> On the Tune, its peaks are weak and land a beat or more "
            "away from the real section changes. <bookmark mark='b'/> The reason is honest: nothing in the texture changes. The "
            "same band plays the same chords throughout; the sections differ only in which tune they play."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(tb), FadeIn(fb), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def repetition(self):
        d = load("structure")
        M = np.array(d["phrase_sim"])
        Mm = np.array(d["mean_sim"])
        cell = 0.62
        grid = VGroup()
        for i in range(6):
            for j in range(6):
                v = M[i, j]
                col = interpolate_color(ManimColor(GREY_D), ManimColor(TUNE), max(0.0, min(1.0, (v - 0.8) / 0.2)))
                sq = Square(side_length=cell, stroke_color=BLACK, stroke_width=1, fill_color=col, fill_opacity=1).move_to([-4.2 + cell * j, 1.4 - cell * i, 0])
                grid.add(VGroup(sq, label(f"{v:.2f}", font_size=11, color=BLACK if v > 0.95 else WHITE).move_to(sq)))
        labs_ = d["phrase_labels"]
        tags = VGroup(*[label(rf"{k + 1}", font_size=14, color=GREY_A).move_to([-4.2 + cell * k, 1.4 + cell * 0.85, 0]) for k in range(6)])
        form = VGroup(*[label(l, font_size=30, color=TUNE if l in ("a", "b") else BLUE) for l in labs_]).arrange(RIGHT, buff=0.35).move_to(RIGHT * 2.8 + UP * 0.6)
        sections = label(r"[a b] \ [c c] \ [a b] \ $\rightarrow$ \ A \ B \ A", font_size=28, color=WHITE).next_to(form, DOWN, buff=0.5)
        side = label(rf"by mean chroma every phrase is alike: \ {np.min(Mm):.3f} or more", font_size=16, color=GREY_A).next_to(sections, DOWN, buff=0.6)
        head = label(r"repetition", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Repetition finds it instead. <bookmark mark='a'/> Cut the Tune into its six phrases, eight beats each, from the "
            "beat tracker, and compare every pair moment by moment along the stripes. <bookmark mark='b'/> Phrases one and five "
            "match, two and six, and three and four: a b, c c, a b. <bookmark mark='c'/> That is A B A, the Tune's form. "
            "<bookmark mark='d'/> Averaged over each phrase, the chroma cannot tell them apart; the order of the notes is what "
            "distinguishes them."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(tags), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(form))
            vo.wait_until("c")
            self.play(FadeIn(sections))
            vo.wait_until("d")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forms(self):
        items = [
            (r"the Tune: \ A B A, \ the form of a nursery song and of a da capo aria", WHITE),
            (r"AABA: \ the Tin Pan Alley chorus of Part 40, \ thirty-two bars", WHITE),
            (r"verse and chorus: \ the chorus returns with the same words; \ the verses with new ones over the same music", WHITE),
            (r"a repetition-based labeller hears a verse's music repeat, \ but not its new words: \ lyrics need another listener", WHITE),
            (r"the form a machine finds is the form its features can see", TUNE),
        ]
        rows_scene(self, r"forms a machine might find", items,
                   "What forms might a machine find? <bookmark mark='b'/> The Tune's A B A, the form of a nursery song and of a da "
                   "capo aria. <bookmark mark='c'/> AABA, the thirty-two-bar chorus of Tin Pan Alley that Part 40 counted. "
                   "<bookmark mark='d'/> Verse and chorus: the chorus returns with the same words, the verses with new words over the "
                   "same music. <bookmark mark='e'/> A labeller built on repetition hears a verse's music come back, but not its new "
                   "words; lyrics need another listener. <bookmark mark='f'/> The form a machine finds is the form its features can "
                   "see.", marks="bcdef")

    # ------------------------------------------------------------------
    def practice(self):
        items = [
            (r"real songs combine both cues: \ the chorus is louder and fuller \ (novelty) \ and comes back \ (repetition)", WHITE),
            (r"McFee and Ellis \ (2014): \ the two cues joined in one graph, \ sections found by spectral clustering", WHITE),
            (r"structure has levels: \ phrases within sections within the song", WHITE),
            (r"and people disagree: \ two experts annotating the same song agree on boundaries far from perfectly \ (Chapter 10)", TUNE),
        ]
        rows_scene(self, r"structure in practice", items,
                   "In real songs the two cues work together: the chorus is louder and fuller, which novelty sees, and it comes "
                   "back, which repetition sees. <bookmark mark='b'/> Brian McFee and Daniel Ellis joined both in one graph in 2014 "
                   "and found sections by spectral clustering. <bookmark mark='c'/> Structure also has levels: phrases within "
                   "sections within the song. <bookmark mark='d'/> And people disagree about it, as the next chapter measures.",
                   marks="bcd")
