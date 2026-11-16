from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403


class Tempo(SoundScene):
    def construct(self):
        chapter(self, 4, r"A tempo that hits three actions", r"Which tempos land every hit on a beat?")
        self.problem()
        self.curve()
        self.grid()
        self.rounding()
        self.options()
        self.hear_variable()
        self.temp()

    # ------------------------------------------------------------------
    def problem(self):
        d = load("scene")
        st = stage()
        set_stage(st, 9.6)
        sp = strip()
        rows_ = VGroup(*[label(rf"{e}: \ {h:.2f} s, \ frame {f:.1f}", font_size=20, color=EAR) for e, h, f in zip(d["events"], d["hits"], d["frames"])]).arrange(RIGHT, buff=0.7).to_edge(UP, buff=0.5)
        cap = label(rf"the cue's first downbeat at {d['start']:.1f} s; \ find a tempo whose beats fall within one frame of all three", font_size=19, color=GREY_A).next_to(rows_, DOWN, buff=0.25)
        with self.voiceover(
            "Our scene has three hit points: the door opens at three point two seconds, the figure reaches the edge at "
            "seven point nine five, and it lands at eleven point four. The cue's first downbeat is at half a second. "
            "Which tempo puts a beat within one frame of all three?"
        ):
            self.play(FadeIn(st), FadeIn(sp), FadeIn(rows_), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("scene")
        b, w = np.array(d["curve_bpm"]), np.array(d["curve_worst"])
        x0, y0, W, H = -5.8, -2.4, 11.0, 4.0
        top = 12.0
        def P_(x, y):
            return [x0 + W * (x - 70) / 90, y0 + H * min(y, top) / top, 0]
        ax = VGroup(Line(P_(70, 0), P_(160, 0), color=GREY_B), Line(P_(70, 0), P_(70, top), color=GREY_B))
        line = VMobject(color=BLUE, stroke_width=2).set_points_as_corners([P_(x, y) for x, y in zip(b, w)])
        tol = DashedLine(P_(70, 1.0), P_(160, 1.0), color=EAR)
        ticks = VGroup(*[label(rf"{v}", font_size=14, color=GREY_A).move_to([P_(v, 0)[0], y0 - 0.25, 0]) for v in (70, 90, 110, 130, 150)],
                       *[label(rf"{v}", font_size=14, color=GREY_A).move_to([x0 - 0.3, P_(70, v)[1], 0]) for v in (0, 4, 8, 12)])
        labs = VGroup(label(r"tempo \ (beats a minute)", font_size=16, color=GREY_A).move_to([x0 + W / 2, y0 - 0.6, 0]),
                      label(r"worst miss \ (frames)", font_size=16, color=GREY_A).move_to([x0 + 0.9, y0 + H + 0.3, 0]),
                      label(r"one frame", font_size=15, color=EAR).next_to(tol, RIGHT, buff=0.1).shift(LEFT * 1.2 + UP * 0.2))
        sols = VGroup()
        for s in d["solutions"]:
            p = P_(s["bpm"], s["worst_frames"])
            sols.add(VGroup(Dot(p, radius=0.09, color=TUNE), label(rf"{s['bpm']:.2f}: \ beats {', '.join(str(int(x)) for x in s['beats'])}", font_size=15, color=TUNE).next_to(p, UP, buff=0.35)))
        head = label(r"the worst miss, \ for every tempo from 70 to 160", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Search every tempo from seventy to a hundred and sixty beats a minute, in steps of a hundredth. For each, "
            "measure how far, in frames, the worst of the three hits falls from its nearest beat. <bookmark mark='a'/> The "
            "curve is a thicket of near-misses. <bookmark mark='b'/> Only "
            f"{say(len(d['solutions']))} narrow windows dip below one frame: about {say(d['solutions'][0]['bpm'], 2)} beats "
            "a minute, where the hits fall on beats four, eleven and sixteen, and about "
            f"{say(d['solutions'][1]['bpm'], 2)}. Allow hits on half-beats as well and there are "
            f"{say(d['eighth_solutions'])} windows; composers often do."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(labs[:2]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(tol), FadeIn(labs[2]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(sols))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grid(self):
        d = load("scene")
        c = clip("scene.comic")
        st = stage()
        set_stage(st, 0.0)
        sp = strip()
        beat = d["beat"]
        n = int((sp.length - d["start"]) / beat) + 1
        beats = VGroup()
        for k in range(n):
            t = d["start"] + k * beat
            x = sp.x0 + sp.width * t / sp.length
            beats.add(VGroup(Line([x, sp.y - 0.45, 0], [x, sp.y - 0.25, 0], color=TUNE if k in (4, 11, 16) else GREY_B, stroke_width=3 if k in (4, 11, 16) else 1.5),
                             label(rf"{k}", font_size=10, color=TUNE if k in (4, 11, 16) else GREY_A).move_to([x, sp.y - 0.6, 0])))
        cap = label(rf"{d['best']['bpm']:.2f} beats a minute: \ beats 4, \ 11 and 16 meet the hits", font_size=19, color=TUNE).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here are that tempo's beats under the scene, numbered from the cue's first downbeat. Hear the comic score "
            "again, which was written at this tempo: its door chord falls on beat four, its trill starts on beat eleven, "
            "and its thump on beat sixteen."
        ):
            self.play(FadeIn(st), FadeIn(sp), FadeIn(beats), FadeIn(cap))
        t0 = 0.0
        with self.listen(c) as snd:
            window(snd, r"the comic score, \ on its beats", kind="synthesized", detail=r"piano, \ bass, \ a glide, \ a drum", corner=DL, tag_corner=DR)
            drive_stage(snd, st, t0)
            drive_strip(snd, sp, t0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rounding(self):
        d = load("scene")
        w, e = d["best"]["click"]
        err = d["click_err_frames"]
        rows_ = text_rows([
            (rf"the exact tempo, \ {d['best']['bpm']:.2f}, \ is {24 * 60 / d['best']['bpm']:.3f} frames a beat", WHITE),
            (rf"the nearest written click is `{w}-{e}', \ {w + e / 8:.3f} frames: \ {d['click_bpm']:.2f} beats a minute", WHITE),
            (rf"its misses grow beat by beat: \ {err[0]:.1f}, \ {err[1]:.1f} \ and {err[2]:.1f} frames at the three hits", EAR),
            (r"a tiny rounding error, \ multiplied by 16 beats, \ is more than a frame and a half", WHITE),
            (r"modern scoring software sets tempos to thousandths; \ older practice changed the click mid-cue", GREY_A),
        ])
        head = label(r"the rounding trap", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Now a trap. <bookmark mark='a'/> The exact tempo is "
            f"{say(24 * 60 / d['best']['bpm'], 3)} frames a beat. <bookmark mark='b'/> The nearest written click is "
            f"{say(w)} dash {say(e)}, a slightly faster tempo. <bookmark mark='c'/> Its misses grow beat by beat: "
            f"{say(err[0], 1)}, {say(err[1], 1)} and {say(err[2], 1)} frames at the three hits. <bookmark mark='d'/> A "
            "tiny rounding error, multiplied by sixteen beats, becomes more than a frame and a half. "
            "<bookmark mark='e'/> Modern scoring software sets tempos to thousandths; older practice changed the click in "
            "the middle of a cue."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def options(self):
        d = load("scene")
        v = d["variable"]
        items = [
            (rf"a variable click: \ {v[0]:.1f}, \ then {v[1]:.1f}, \ then {v[2]:.1f} beats a minute lands every hit exactly", WHITE),
            (r"or hit on off-beats and half-beats, \ or with a pickup before the downbeat", WHITE),
            (r"or play `free time' to the picture, \ the conductor watching streamers and punches on the screen", WHITE),
            (r"or ask the editor to move a cut by a frame or two: \ the picture bends too", TUNE),
            (r"chapter 5: \ the harmony that film scores share", GREY_A),
        ]
        rows_scene(self, r"other ways to hit", items,
                   "There are other ways to hit. <bookmark mark='b'/> A variable click changes tempo between hits: "
                   f"{say(v[0], 1)}, then {say(v[1], 1)}, then {say(v[2], 1)} beats a minute lands every hit exactly, with "
                   "changes too small to hear. <bookmark mark='c'/> A composer can hit on off-beats and half-beats, or start with "
                   "a pickup. <bookmark mark='d'/> An orchestra can play in free time, the conductor watching streamers and "
                   "punches, lines and flashes drawn on the film itself. <bookmark mark='e'/> Or the editor can move a cut by a "
                   "frame or two: the picture bends too. <bookmark mark='f'/> Chapter five turns to the harmony film scores "
                   "share.", marks="bcdef")

    # ------------------------------------------------------------------
    def temp(self):
        items = [
            (r"editors cut films to a `temp track': \ existing music laid in while the film is assembled", WHITE),
            (r"directors grow used to it, \ and the composer is asked for something like it, \ but new", WHITE),
            (r"composers call it `temp love': \ the cut's rhythm already fits the borrowed music", WHITE),
            (r"the hit points were set by someone else's tempo", TUNE),
            (r"chapter 5: \ what the harmony of film scores shares", GREY_A),
        ]
        rows_scene(self, r"the temp track", items,
                   "In practice the picture often arrives with music already on it. <bookmark mark='b'/> Editors cut films to a "
                   "temp track, existing music laid in while the film is assembled. <bookmark mark='c'/> Directors grow used to "
                   "it, and the composer is asked for something like it, but new. <bookmark mark='d'/> Composers call this temp "
                   "love, <bookmark mark='e'/> and its hidden cost is arithmetic: the cut's rhythm, and its hit points, were set by "
                   "someone else's tempo. <bookmark mark='f'/> Chapter five turns to harmony.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear_variable(self):
        d = load("scene")
        c = clip("scene.variable")
        st = stage()
        set_stage(st, 0.0)
        sp = strip()
        v = d["variable"]
        cap = label(rf"tempos {v[0]:.1f}, \ {v[1]:.1f}, \ {v[2]:.1f}: \ a change of under 2\% at each hit", font_size=19, color=TUNE).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the variable click: the comic score's walking line, its tempo changing very slightly at each hit, so that "
            "every hit lands exactly. Can you hear the tempo change?"
        ):
            self.play(FadeIn(st), FadeIn(sp), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a variable click", detail=r"Part 7's piano, \ a plucked bass, \ Part 9's drum", corner=DL, tag_corner=DR)
            drive_stage(snd, st, 0.0)
            drive_strip(snd, sp, 0.0)
        with self.voiceover(
            "Judge it for yourself. Changes of a percent or two may escape notice in some passages, but are not universally inaudible, which is why a variable click is a "
            "composer's quiet friend."
        ):
            self.play(Indicate(cap))
        self.wait(0.3)
        self.clear_scene()
