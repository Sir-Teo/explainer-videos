from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Follow(SoundScene):
    def construct(self):
        chapter(self, 8, r"Following a soloist", r"Can a machine accompany a singer who takes their own time?")
        self.history()
        self.loop()
        self.tracking()
        self.humans()
        self.asynchrony()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"1984: \ Roger Dannenberg and Barry Vercoe, \ separately, \ build computer accompanists that follow a soloist", WHITE),
            (r"the follower listens; \ an accompanist predicts where the soloist will be, \ and plays there", WHITE),
            (r"Christopher Raphael's Music Plus One \ (from the late 1990s): \ an orchestra that follows a concerto soloist", WHITE),
            (r"latency is the enemy: \ the accompaniment must sound with the note, \ not after hearing it", TUNE),
        ]
        rows_scene(self, r"computer accompaniment", items,
                   "Following a performer live is an old dream. <bookmark mark='b'/> In 1984 Roger Dannenberg and Barry Vercoe, "
                   "separately, built computer accompanists that followed a soloist. <bookmark mark='c'/> A follower listens; an "
                   "accompanist must also predict where the soloist will be, and play there. <bookmark mark='d'/> From the late "
                   "1990s Christopher Raphael's Music Plus One followed concerto soloists with a recorded orchestra. "
                   "<bookmark mark='e'/> Latency is the enemy: the accompaniment has to sound with the note, not after hearing it.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def loop(self):
        def box(t, col, pos, w=2.6):
            r = RoundedRectangle(width=w, height=0.75, corner_radius=0.12, stroke_color=col, stroke_width=2.5).move_to(pos)
            return VGroup(r, label(t, font_size=16, color=col).move_to(pos))
        voice = box(r"the singer", EAR, [-5.0, 0.6, 0])
        chroma = box(r"chroma, \ 50 ms frames", GREY_A, [-1.8, 0.6, 0])
        follow = box(r"online DTW: \ where are we?", BLUE, [1.6, 0.6, 0], 3.0)
        play = box(r"play the chord", TUNE, [4.9, 0.6, 0])
        score = box(r"the score", GREY_B, [1.6, -1.2, 0])
        arrows = VGroup(Arrow(voice.get_right(), chroma.get_left(), buff=0.08, color=GREY_B), Arrow(chroma.get_right(), follow.get_left(), buff=0.08, color=GREY_B),
                        Arrow(follow.get_right(), play.get_left(), buff=0.08, color=GREY_B), Arrow(score.get_top(), follow.get_bottom(), buff=0.08, color=GREY_B))
        note = label(r"each chord is played when the follower believes the score has reached it, \ plus 60 ms for processing", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"Monochord's accompanist", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Monochord's accompanist is the simplest that works. <bookmark mark='a'/> It hears the singer as chroma, frame by "
            "frame. <bookmark mark='b'/> Online time warping against the score says where the singer has got to. "
            "<bookmark mark='c'/> And when the score reaches a chord, it plays it, sixty milliseconds later, the time the "
            "processing takes. It does not predict; Chapter 11's research takes that up."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(voice), FadeIn(chroma), GrowArrow(arrows[0]))
            vo.wait_until("b")
            self.play(FadeIn(follow), FadeIn(score), GrowArrow(arrows[1]), GrowArrow(arrows[3]))
            vo.wait_until("c")
            self.play(FadeIn(play), GrowArrow(arrows[2]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tracking(self):
        d = load("follow")
        t = np.array(d["pos_t"])
        est, tru = np.array(d["pos_beats"]), np.array(d["true_beats"])
        ax = frame_axes(width=8.5, height=3.4, xlo=0, xhi=t[-1], ylo=0, yhi=max(tru.max(), est.max()) + 0.5, center=DOWN * 0.3 + LEFT * 0.6)
        ct = curve(t, tru, ax.to, color=GREY_B, width=5)
        ce = VMobject(stroke_color=TUNE, stroke_width=2.5).set_points_as_corners([ax.to(a, b) for a, b in zip(t, est)])
        xl = label(r"seconds of singing", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"beats of the score", font_size=14, color=GREY_A).rotate(PI / 2).next_to(ax, LEFT, buff=0.15)
        key = VGroup(label(r"where the singer is", font_size=16, color=GREY_B), label(r"where the follower thinks", font_size=16, color=TUNE)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.3)
        head = label(r"the follower, \ following", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the follower at work. <bookmark mark='a'/> The grey line is where the singer really is in the score, beat "
            "by beat, curving with the rubato. <bookmark mark='b'/> The gold line is where the follower believes the singer is. "
            "It climbs in steps, waiting for evidence, then catching up; it never goes backwards. Where the singer holds a note, "
            "nothing new arrives, and the follower waits too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(ct), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(ce), FadeIn(key[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def humans(self):
        items = [
            (r"ensemble players keep together within a few tens of milliseconds, \ by listening and predicting at once", WHITE),
            (r"they correct each other continuously: \ each adjusts to the other's last asynchrony \ (Part 43's ensemble)", WHITE),
            (r"they read the soloist's body: \ a breath, \ a nod, \ a lifted bow, \ before the sound", WHITE),
            (r"they know the music: \ where the soloist will slow, \ where they will hold", WHITE),
            (r"a machine that only listens starts every note behind; \ to play with a soloist, \ it must expect", TUNE),
        ]
        rows_scene(self, r"what human accompanists do", items,
                   "What do human accompanists do that this one does not? <bookmark mark='b'/> Ensemble players keep together within "
                   "a few tens of milliseconds, by listening and predicting at once. <bookmark mark='c'/> They correct each other "
                   "continuously, each adjusting to the other's last asynchrony, as Part 43's ensemble did. <bookmark mark='d'/> "
                   "They read the soloist's body: a breath, a nod, a lifted bow, before the sound. <bookmark mark='e'/> And they know "
                   "the music: where the soloist will slow, where they will hold. <bookmark mark='f'/> A machine that only listens "
                   "starts every note behind; to play with a soloist, it must expect.", marks="bcdef")

    # ------------------------------------------------------------------
    def asynchrony(self):
        d = load("follow")
        a = np.array(d["asynchrony_ms"])
        ax = frame_axes(width=8.0, height=3.0, xlo=0, xhi=len(a), ylo=-250, yhi=250, center=DOWN * 0.3)
        bars = VGroup(*[Rectangle(width=8.0 / len(a) * 0.6, height=max(0.02, 3.0 * abs(v) / 500), stroke_width=0, fill_color=TUNE if v >= 0 else BLUE, fill_opacity=0.85)
                        .move_to(ax.to(i + 0.5, 0), aligned_edge=DOWN if v >= 0 else UP) for i, v in enumerate(a)])
        yt = VGroup(*[label(f"{v:+d} ms" if v else "0", font_size=13, color=GREY_A).next_to(ax.to(0, v), LEFT, buff=0.1) for v in (-200, 0, 200)])
        xl = label(r"the eight chords", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        note = label(rf"median distance from the voice's beat: \ {d['median_ms']:.0f} ms \ (gold: \ late; \ blue: \ early)", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"how close the accompanist plays", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How close does it play? <bookmark mark='a'/> Each bar is one chord: how far it sounded from the singer's beat. "
            f"Most land late, by the processing delay and the time it takes the follower to be sure: a median of {say(d['median_ms'])} "
            "milliseconds. One lands early, where the follower jumped ahead. Ensemble players keep within a few tens of "
            "milliseconds; this accompanist would sound a little behind. You will hear it in the Variation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v >= 0 else UP) for b, v in zip(bars, a)], lag_ratio=0.2), FadeIn(note), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()
