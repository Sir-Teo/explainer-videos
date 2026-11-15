from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403


class Spotting(SoundScene):
    def construct(self):
        chapter(self, 3, r"Spotting and hit points", r"How exactly must music meet a picture?")
        self.spotting()
        self.cuesheet()
        self.quiz()
        self.tolerance()
        self.click_math()

    # ------------------------------------------------------------------
    def spotting(self):
        items = [
            (r"spotting: \ director and composer watch the cut and decide where music starts, \ stops, \ and what it does", WHITE),
            (r"each cue gets start and end times, \ and hit points: \ moments the music must meet", WHITE),
            (r"film runs at 24 frames a second: \ one frame is 41.7 ms; \ timecode names every frame", WHITE),
            (r"a cue is written so its hits land on beats, \ or on strong parts of beats", TUNE),
            (r"the craft is mostly arithmetic, \ done before a note is written", GREY_A),
        ]
        rows_scene(self, r"spotting", items,
                   "Scoring starts with spotting. <bookmark mark='b'/> The director and composer watch the cut together and "
                   "decide where music starts and stops, and what it does. <bookmark mark='c'/> Each cue gets start and end times, "
                   "and hit points: moments the music must meet. <bookmark mark='d'/> Film runs at twenty-four frames a second, "
                   "so one frame lasts forty-one point seven milliseconds, and timecode names every frame. "
                   "<bookmark mark='e'/> A cue is written so that its hits land on beats, or on strong parts of beats. "
                   "<bookmark mark='f'/> Much of the craft is arithmetic, done before a note is written.", marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("sync")
        c = clip("sync.three")
        card = listen_card(r"A door slams, \ three times. \ Once the sound is 120 ms early, \ once 120 ms late, \ "
                           r"once in sync. \ Which is in sync?", width=10.4)
        with self.voiceover(
            "A question for your eyes and ears. A door slams, three times. Once the sound comes a hundred and twenty "
            "milliseconds early, once a hundred and twenty late, and once in sync. Which one is in sync?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        frame_ = Rectangle(width=1.4, height=2.6, stroke_color=GREY_A, stroke_width=3).move_to(UP * 0.4)
        door = Rectangle(width=1.3, height=2.5, stroke_width=0, fill_color="#7C5A3A", fill_opacity=1.0).move_to(frame_)
        boxes = VGroup(*[label(t, font_size=24, color=GREY_A) for t in (r"first", r"second", r"third")]).arrange(RIGHT, buff=1.8).to_edge(DOWN, buff=1.4)
        self.play(FadeOut(card), FadeIn(frame_), FadeIn(door), FadeIn(boxes))
        names = d["order"]
        st = d["starts"]
        slam = d["slam"]
        def upd(m, now):
            k = 0
            for i, n in enumerate(names):
                if now >= st[n]:
                    k = i
            t = now - st[names[k]]
            o = 1.0 if t < slam - 0.35 else (max(0.0, (slam - t) / 0.35) if t < slam else 0.0)
            w = 1.3 * (1 - 0.9 * o)
            m.stretch_to_fit_width(max(w, 0.05))
            m.move_to([frame_.get_left()[0] + 0.05 + w / 2, frame_.get_y(), 0])
        with self.listen(c) as snd:
            window(snd, r"three slams", detail=r"Part 9's drum, \ Part 7's piano", corner=DL, tag_corner=DR)
            snd.drive(door, upd)
            for i, n in enumerate(names):
                end = st[names[i + 1]] - 0.2 if i < 2 else c.duration
                pulse(snd, boxes[i], st[n], end, buff=0.12)
        ans = VGroup(label(r"first: \ late; \ second: \ early; \ third: \ in sync", font_size=21, color=TUNE),
                     label(r"most people find the early sound the more wrong: \ in the world, \ light always arrives first", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The third. The first was late, the second early. Most people find the early sound the more wrong of the two, "
            "and there is a reason: in the world, light always arrives before sound, so a sound slightly after its image "
            "is natural, and a sound before it never is."
        ):
            self.play(FadeOut(boxes), FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tolerance(self):
        d = load("sync")
        lead, lag = d["itu"]["lead_ms"], d["itu"]["lag_ms"]
        x0, W = -5.5, 11.0
        def X(ms):
            return x0 + W * (ms + 200) / 400
        ax = Line([X(-200), -0.6, 0], [X(200), -0.6, 0], color=GREY_B)
        zone = Rectangle(width=X(lag) - X(-lead), height=0.8, stroke_width=0, fill_color=TUNE, fill_opacity=0.35).move_to([(X(-lead) + X(lag)) / 2, -0.6, 0])
        ticks = VGroup(*[VGroup(Line([X(v), -0.75, 0], [X(v), -0.45, 0], color=GREY_B), label(rf"{v:+d}" if v else r"0", font_size=15, color=GREY_A).move_to([X(v), -1.05, 0])) for v in (-200, -120, -45, 0, 125, 200)])
        frames_ = VGroup(*[Line([X(41.7 * k), -0.2, 0], [X(41.7 * k), 0.0, 0], color=GREY_D, stroke_width=1) for k in range(-4, 5)])
        labs = VGroup(label(r"sound early", font_size=18, color=GREY_A).move_to([X(-150), 0.4, 0]), label(r"sound late", font_size=18, color=GREY_A).move_to([X(150), 0.4, 0]),
                      label(r"ms, \ sound against picture; \ small ticks: \ film frames", font_size=16, color=GREY_A).move_to([0, -1.5, 0]),
                      label(rf"barely noticed: \ up to {lead} ms early, \ {lag} ms late", font_size=20, color=TUNE).move_to([(X(-lead) + X(lag)) / 2, 1.1, 0]))
        cap = label(r"after the detection thresholds in ITU-R BT.1359 \ (1998), \ for television", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.9)
        head = label(r"how far can sound and picture drift?", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "How far can they drift before anyone notices? <bookmark mark='a'/> Broadcasters measured it for television: "
            f"viewers barely notice sound up to about {say(lead)} milliseconds early, or up to about {say(lag)} milliseconds "
            "late. The window is lopsided, for the same reason the early slam felt wrong. In frames, that is about one frame "
            "early and three late: a cue whose hit is a frame off still works, three frames early does not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(ticks), FadeIn(frames_), FadeIn(labs[:3]), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(zone), FadeIn(labs[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def click_math(self):
        rows_ = text_rows([
            (r"a click track is a metronome in the players' headphones, \ written in frames per beat", WHITE),
            (r"frames per beat \ = \ 24 $\times$ 60 / tempo: \ 120 beats a minute is 12 frames, \ written `12-0'", WHITE),
            (r"the number after the dash counts eighths of a frame: \ `14-3' is 14 3/8 frames, \ about 100.2 beats a minute", WHITE),
            (r"a hit t seconds into a cue lands on beat \ t $\times$ tempo / 60: \ the composer wants that number whole", TUNE),
            (r"chapter 4: \ find a tempo that makes three of them whole at once", GREY_A),
        ])
        head = label(r"the click track's arithmetic", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The tool for hitting is the click track. <bookmark mark='a'/> It is a metronome in the players' headphones, "
            "written in frames per beat. <bookmark mark='b'/> Frames per beat are twenty-four times sixty over the tempo: a "
            "hundred and twenty beats a minute is twelve frames, written twelve dash nought. <bookmark mark='c'/> The number "
            "after the dash counts eighths of a frame: fourteen dash three is fourteen and three-eighths frames, about a "
            "hundred beats a minute. <bookmark mark='d'/> A hit t seconds into a cue lands on beat t times the tempo over "
            "sixty, and the composer wants that number whole. <bookmark mark='e'/> Chapter four finds a tempo that makes "
            "three of them whole at once."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cuesheet(self):
        d = load("scene")
        hdr = [r"event", r"seconds", r"timecode", r"frame", r"beat at 88.28"]
        rows_ = [(r"cue start \ (downbeat)", d["start"], 0.0)] + [(e, h, b) for e, h, b in zip(d["events"], d["hits"], d["best"]["beats"])]
        cells = VGroup(*[label(t, font_size=18, color=GREY_A) for t in hdr])
        for name, sec, beat in rows_:
            fr = sec * 24
            tc = rf"00:00:{int(sec):02d}:{int(round(fr - 24 * int(sec))):02d}"
            cells.add(label(name, font_size=18, color=WHITE), label(rf"{sec:.2f}", font_size=18, color=WHITE), label(tc, font_size=18, color=WHITE),
                      label(rf"{fr:.1f}", font_size=18, color=WHITE), label(rf"{beat:.0f}", font_size=18, color=TUNE))
        cells.arrange_in_grid(rows=len(rows_) + 1, cols=5, buff=(0.6, 0.35), col_alignments="lrrrr").move_to(DOWN * 0.1)
        head = label(r"a cue sheet for our scene", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"timecode: \ hours, \ minutes, \ seconds, \ frames; \ the last column is chapter 4's answer", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Spotting produces a cue sheet. <bookmark mark='a'/> Here is ours: the cue's first downbeat and the three hit "
            "points, each in seconds, in timecode, hours, minutes, seconds and frames, and as a frame count. The last "
            "column, the beat each hit falls on, is what chapter four will compute."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(cells))
        self.wait(0.4)
        self.clear_scene()
