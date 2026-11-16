from __future__ import annotations

import numpy as np

from videos.music.music37.common import *  # noqa: F403


class Inherent(SoundScene):
    def construct(self):
        chapter(self, 7, r"Inherent patterns", r"Can you hear a melody that nobody plays?")
        self.kubik()
        self.quiz()
        self.model()
        self.slow()
        self.limits()
        self.composers()

    # ------------------------------------------------------------------
    def kubik(self):
        items = [
            (r"Gerhard Kubik, \ studying the \textit{amadinda} xylophone of Buganda \ (Uganda), \ from 1959", WHITE),
            (r"two players interlock at great speed, \ each in octaves, \ neither playing a melody", WHITE),
            (r"listeners \ (and players) \ hear melodies that are in nobody's part", WHITE),
            (r"Kubik called them \textit{inherent patterns}; \ a third player picks one out and doubles it", TUNE),
            (r"the same happens between the mbira's hands and players", GREY_A),
        ]
        rows_scene(self, r"melodies nobody plays", items,
                   "In 1959 the young Austrian scholar Gerhard Kubik began studying the amadinda, a large xylophone of the "
                   "Buganda kingdom in Uganda. <bookmark mark='b'/> Two players interlock at great speed, each doubling their "
                   "notes in octaves, and neither alone plays the composite inherent pattern. <bookmark mark='c'/> Yet listeners, and the players too, hear "
                   "melodies that are in nobody's part. <bookmark mark='d'/> Kubik called them inherent patterns, and in amadinda "
                   "music a third player picks one out and doubles it. <bookmark mark='e'/> The same happens between the mbira's "
                   "hands, and between its players.", marks="bcde")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("inherent")
        card = listen_card(r"Two parts, \ each alone, \ fast. \ Then both together. \ "
                           r"Listen to the high notes when both play: \ which of three melodies do they make?", width=10.4)
        with self.voiceover(
            "A question for your ears. You will hear two interlocking parts of our own on model mbira tines, each alone and "
            "then both together, ten notes a second. When both play, listen to the high notes. Afterwards you will choose "
            "which of three melodies they made."
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        n = d["n"]
        a = [[m, i, 1.0] for i, m in d["a"]]
        b = [[m, i, 1.0] for i, m in d["b"]]
        roll = voices_roll([a, b], width=11.0, height=2.6, colors=[TUNE, BLUE], total=n, lo=53, hi=81, bar_h=0.12).move_to(UP * 0.2)
        leg = VGroup(label(r"part A", font_size=20, color=TUNE), label(r"part B", font_size=20, color=BLUE)).arrange(RIGHT, buff=1.0).next_to(roll, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(roll), FadeIn(leg))
        clips_ = {"a": clip("inherent.a"), "b": clip("inherent.b"), "both": clip("inherent.both")}
        for name, which, reps in (("a", (0,), 2), ("b", (1,), 2), ("both", (0, 1), 3)):
            c = clips_[name]
            with self.listen(c) as snd:
                window(snd, {"a": r"part A alone", "b": r"part B alone", "both": r"both together"}[name], detail=r"tine models", corner=DL, tag_corner=DR)
                for j in which:
                    v = [a, b][j]
                    times = [r * n * d["fast"] + nn[1] * d["fast"] for r in range(reps) for nn in v]
                    flash(snd, roll.parts[j].notes * reps, times, hot=WHITE, base=[TUNE, BLUE][j])
            self.wait(0.3)
        self.play(FadeOut(roll), FadeOut(leg))
        opts = VGroup()
        for k in ("A", "B", "C"):
            mel = [[m, i, 1.0] for i, m in enumerate(d["options"][k])]
            r = mroll(mel, width=3.4, height=1.6, lo=65, hi=83, color=GREY_A, total=12, bar_h=0.12)
            opts.add(VGroup(label(k, font_size=30, color=EAR), r).arrange(DOWN, buff=0.25))
        opts.arrange(RIGHT, buff=0.8).move_to(UP * 0.2)
        with self.voiceover(
            "Which melody did the high notes make: A, B or C? <bookmark mark='a'/> Decide before the answer."
        ) as vo:
            self.play(FadeIn(opts))
            vo.wait_until("a")
        self.wait(2.0)
        ans = label(r"B: \ half its notes come from each part", font_size=24, color=TUNE).to_edge(DOWN, buff=1.2)
        with self.voiceover(
            "The answer is B. Here is melody B alone. Neither part contains it: part A plays its first, third and fifth "
            "notes and so on, part B the others, and the ear joins them across the two players."
        ):
            self.play(opts[1][1].animate.set_color(TUNE), opts[1][0].animate.set_color(TUNE), FadeIn(ans))
        c = clip("inherent.target")
        with self.listen(c) as snd:
            window(snd, r"melody B alone", detail=r"tine model", corner=DL, tag_corner=DR)
            for r in range(2):
                for i, bar in enumerate(opts[1][1].notes):
                    t0 = (r * 12 + i) * 3 * d["fast"]
                    pulse(snd, bar, t0, t0 + 3 * d["fast"] - 0.02, buff=0.03)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model(self):
        d = load("inherent")
        n = d["n"]
        allnotes = sorted([(i, m) for i, m in d["a"]] + [(i, m) for i, m in d["b"]])
        hi = [[m, i, 1.0] for i, m in allnotes if m > d["split"]]
        lo = [[m, i, 1.0] for i, m in allnotes if m <= d["split"]]
        roll = voices_roll([hi, lo], width=11.0, height=2.8, colors=[TUNE, GREY_B], total=n, lo=53, hi=81, bar_h=0.12).move_to(DOWN * 0.3)
        split_y = roll.frame.get_bottom()[1] + roll.frame.height * (d["split"] - 53) / (81 - 53)
        line = DashedLine([roll.frame.get_left()[0], split_y, 0], [roll.frame.get_right()[0], split_y, 0], color=EAR, stroke_width=2)
        ll = label(r"split", font_size=16, color=EAR).next_to(line, LEFT, buff=0.15)
        side = VGroup(label(r"at fast rates and wide leaps, \ one sequence splits into two \textit{streams}", font_size=20, color=WHITE),
                      label(r"van Noorden \ (1975): \ the boundary depends on rate and pitch separation", font_size=18, color=GREY_A),
                      label(r"the simplest model: \ notes above a split form one stream", font_size=18, color=TUNE)).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.3)
        res = label(rf"the model's high stream \ = \ melody B, \ note for note \ ({len(hi)} of {len(hi)})", font_size=21, color=TUNE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why does this happen? When notes come fast and leap widely, the ear stops hearing one line jumping up and down, "
            "and hears two lines instead, a high one and a low one: auditory streaming. <bookmark mark='a'/> Leon van "
            "Noorden mapped in 1975 how the split depends on the rate and on the size of the leaps. <bookmark mark='b'/> "
            "Monochord's simplest streaming model puts every note above a split point into one stream. Combine the two parts, "
            "draw the split, and keep the high stream. <bookmark mark='c'/> It is melody B, note for note. That is how the "
            "parts were designed: as a target melody shared out between two players, with low notes filling the gaps."
        ) as vo:
            self.play(FadeIn(side[0]), FadeIn(roll))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Create(line), FadeIn(ll))
            vo.wait_until("c")
            self.play(*[b.animate.set_fill(opacity=0.25) for b in roll.parts[1].notes], FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slow(self):
        d = load("inherent")
        c = clip("inherent.slow")
        n = d["n"]
        allnotes = sorted([(i, m) for i, m in d["a"]] + [(i, m) for i, m in d["b"]])
        mel = [[m, i, 1.0] for i, m in allnotes]
        roll = mroll(mel, width=11.0, height=2.6, lo=53, hi=81, color=WHITE, total=n, bar_h=0.12).move_to(DOWN * 0.2)
        head = label(rf"the same notes, \ {d['rate_slow']:.0f} a second instead of {d['rate_fast']:.0f}", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Now the same notes, slowly: about three a second instead of ten. Does melody B still stand out, or do you hear "
            "one line leaping up and down?"
        ):
            self.play(FadeIn(head), FadeIn(roll))
        with self.listen(c) as snd:
            window(snd, r"both parts, \ slowly", detail=r"tine models", corner=DL, tag_corner=DR)
            flash(snd, roll.notes, [nn[1] * d["slow"] for nn in mel], hot=EAR, base=WHITE)
        ans = label(r"slower playback may weaken the high stream \\ attention and experience also matter", font_size=22, color=TUNE).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "At this slower rate the high line may be less compelling, although listeners can still attend to it. This informal example measures no majority response or necessary speed threshold. "
            "Performance tempo also belongs to musical and social practice; this synthesis does not establish its cause."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        items = [
            (r"real streaming depends on rate, \ separation, \ timbre, \ loudness and attention \ (Bregman, \ 1990)", WHITE),
            (r"between two boundaries lies a zone where listeners can choose what they hear", WHITE),
            (r"several inherent patterns can be heard in the same music, \ one at a time", WHITE),
            (r"players knowing the patterns hear differently from newcomers", TUNE),
            (r"Part 45 builds a fuller model of auditory scenes", GREY_A),
        ]
        rows_scene(self, r"what the model leaves out", items,
                   "A split point is the crudest possible model, and it leaves a great deal out. <bookmark mark='b'/> Real "
                   "streaming depends on rate, separation, timbre, loudness and attention, as Albert Bregman's Auditory Scene "
                   "Analysis of 1990 sets out. <bookmark mark='c'/> Between two boundaries lies a zone where listeners can choose "
                   "what they hear. <bookmark mark='d'/> Several inherent patterns can be heard in the same music, one at a time, "
                   "<bookmark mark='e'/> and players who know the patterns hear differently from newcomers. "
                   "<bookmark mark='f'/> Part 45 builds a fuller model of auditory scenes.", marks="cdef")

    # ------------------------------------------------------------------
    def composers(self):
        items = [
            (r"Steve Reich studied drumming in Ghana in 1970; \ \textit{Drumming} \ (1971) \ followed", WHITE),
            (r"his phase pieces make inherent patterns appear as two identical parts drift apart", WHITE),
            (r"Gy\"orgy Ligeti heard Arom's Central African recordings in the 1980s; \ his piano \'Etudes owe them much", WHITE),
            (r"both took the idea of patterns that emerge, \ not the music itself", TUNE),
            (r"Part 30 met Reich's phasing; \ Part 42 composes with these ideas", GREY_A),
        ]
        rows_scene(self, r"composers who listened", items,
                   "Composers listened. <bookmark mark='b'/> Steve Reich studied drumming in Ghana in 1970, and his Drumming followed in 1971. <bookmark mark='c'/> His phase pieces make inherent patterns appear as two identical parts slowly drift apart. <bookmark mark='d'/> György Ligeti heard Simha Arom's Central African recordings in the nineteen-eighties, and his piano Études owe them much. <bookmark mark='e'/> Both transformed techniques and material encountered through particular musicians and recordings; influence and attribution require the specific historical context. <bookmark mark='f'/> Part 30 met Reich's phasing, and Part 42 composes with these ideas.", marks="cdef")
