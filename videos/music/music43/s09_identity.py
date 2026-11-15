from __future__ import annotations

import numpy as np

from videos.music.music43.common import *  # noqa: F403


class Identity(SoundScene):
    def construct(self):
        chapter(self, 8, r"Who is playing?", r"Can timing identify a performer?")
        self.method()
        self.curves()
        self.matrix()
        self.history()
        self.caveats()

    # ------------------------------------------------------------------
    def method(self):
        items = [
            (r"tap along with a recording, \ or let software find each beat: \ a list of beat times", WHITE),
            (r"the intervals between beats, \ divided by their average: \ a tempo curve, \ whatever the overall speed", WHITE),
            (r"time-stretching a recording changes its speed, \ not its curve", WHITE),
            (r"compare curves by correlation: \ 1 means the same shape", TUNE),
            (r"Cook and Sapp did this for Chopin mazurkas at the AHRC Research Centre for the History and Analysis of Recorded Music", GREY_A),
        ]
        rows_scene(self, r"a timing fingerprint", items,
                   "How can timing identify a performer? <bookmark mark='b'/> Tap along with a recording, or let software find "
                   "each beat, and you have a list of beat times. <bookmark mark='c'/> Divide the intervals between beats by "
                   "their average and you have a tempo curve, whatever the overall speed. <bookmark mark='d'/> Time-stretching "
                   "a recording, as the Hatto discs did, changes its speed but not its curve. <bookmark mark='e'/> Compare "
                   "curves by correlation: one means the same shape. <bookmark mark='f'/> Nicholas Cook and Craig Sapp measured "
                   "hundreds of recordings of Chopin's mazurkas this way at a British research centre for the history and "
                   "analysis of recorded music.", marks="bcdef")

    # ------------------------------------------------------------------
    def curves(self):
        d = load("identity")
        D, B, H = np.array(d["curves"]["pianist D"]), np.array(d["curves"]["pianist B"]), np.array(d["hoax_curve"])
        x0, W = -5.6, 11.2
        def line(v, col, y, sw=3):
            n = len(v)
            return VMobject(color=col, stroke_width=sw).set_points_as_corners([[x0 + W * i / (n - 1), y + 0.35 * vi, 0] for i, vi in enumerate(v)])
        rows_ = VGroup(VGroup(label(r"pianist D", font_size=18, color=TUNE).move_to([x0 + 0.6, 2.2, 0]), line(D, TUNE, 1.3)),
                       VGroup(label(r"the `new release', \ 3\% slower", font_size=18, color=EAR).move_to([x0 + 1.2, 0.1, 0]), line(H, EAR, -0.8)),
                       VGroup(label(r"pianist B", font_size=18, color=BLUE).move_to([x0 + 0.6, -2.0, 0]), line(B, BLUE, -2.8)))
        cap = label(rf"tempo curves of all {d['notes']} notes of the Tune: \ up, \ a longer note than the pianist's average", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.25)
        head = label(r"three tempo curves", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Try it on ten model pianists, each with its own weights for the rules, its own tempo and its own habits, playing "
            "the whole Tune. Then take pianist D's recording, slow it by three per cent, add two milliseconds of editing "
            "jitter, and release it under a new name. <bookmark mark='a'/> Here is pianist D's tempo curve; "
            "<bookmark mark='b'/> the new release's; <bookmark mark='c'/> and pianist B's. Every curve rises at the phrase "
            "ends, because every pianist follows the same rules; the details are what differ."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r[0]), Create(r[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matrix(self):
        d = load("identity")
        R = np.array(d["R"])
        n = len(R)
        cell = 0.38
        grid = VGroup()
        lo = 0.75
        for i in range(n):
            for j in range(n):
                v = (R[i, j] - lo) / (1 - lo)
                grid.add(Square(cell, stroke_width=0.5, stroke_color=GREY_D, fill_color=interpolate_color(ManimColor("#1E2430"), ManimColor(TUNE), min(max(v, 0), 1)), fill_opacity=1)
                         .move_to([-5.2 + cell * j, 1.6 - cell * i, 0]))
        names = VGroup(*[label(chr(65 + i), font_size=13, color=GREY_A).move_to([-5.2 - 0.35, 1.6 - cell * i, 0]) for i in range(n)],
                       *[label(chr(65 + j), font_size=13, color=GREY_A).move_to([-5.2 + cell * j, 1.6 + 0.35, 0]) for j in range(n)])
        mt = label(rf"between different pianists: \ {d['between_mean']:.2f} on average, \ at most {d['between_max']:.2f}", font_size=16, color=GREY_A).move_to([-3.5, -2.6, 0])
        rk = d["ranking"][:4]
        bars = VGroup()
        for i, (nm, r) in enumerate(rk):
            w = 4.0 * (r - 0.75) / 0.25
            y = 1.3 - 0.6 * i
            bars.add(VGroup(label(nm, font_size=17, color=WHITE).move_to([0.9, y, 0], aligned_edge=RIGHT),
                            Rectangle(width=max(w, 0.05), height=0.36, stroke_width=0, fill_color=EAR if i == 0 else BLUE, fill_opacity=0.85).move_to([1.1 + w / 2, y, 0]),
                            label(f"{r:.4f}", font_size=15, color=WHITE).move_to([1.3 + w + 0.4, y, 0])))
        tk = d["take_ranking"][0]
        bt = label(r"the new release against all ten", font_size=19, color=EAR).move_to([2.6, 1.95, 0])
        other = label(rf"pianist D's own second take: \ {tk[1]:.3f}", font_size=17, color=GREY_A).move_to([2.6, -1.4, 0])
        head = label(r"the Hatto test, \ on model pianists", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Now correlate. <bookmark mark='a'/> The ten pianists against one another: brighter is more similar. Their "
            f"curves correlate {say(d['between_mean'], 2)} on average, because they share the rules, and never more than "
            f"{say(d['between_max'], 2)}. <bookmark mark='b'/> The new release against all ten: pianist D at "
            f"{say(d['ranking'][0][1], 4)}, the next at {say(d['ranking'][1][1], 2)}. <bookmark mark='c'/> And a second, "
            f"honest take by pianist D scores {say(tk[1], 3)}: a performer repeats a shape closely, but never to four "
            "decimal places. A copy is closer to its source than any performer is to themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(grid).copy().set_opacity(0.15)))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(names), FadeIn(mt))
            vo.wait_until("b")
            self.play(FadeIn(bt), LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(other))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def caveats(self):
        items = [
            (r"real recordings add rubato that no rule predicts, \ and edits that splice takes together", WHITE),
            (r"the Hatto evidence also came from spectra: \ the same piano, \ the same room, \ the same noise", WHITE),
            (r"timing analysis now studies performance history: \ how tempo and rubato changed over a century of records", WHITE),
            (r"the same measurements show what is personal: \ the part a student cannot copy from a score", TUNE),
            (r"chapter 9: \ how performers are made", GREY_A),
        ]
        rows_scene(self, r"what the test can and cannot do", items,
                   "Some caveats. <bookmark mark='b'/> Real recordings add rubato that no rule predicts, and edits that splice "
                   "takes together. <bookmark mark='c'/> The Hatto evidence also came from the sound itself: the same piano, "
                   "the same room, the same background noise. <bookmark mark='d'/> Timing analysis now studies performance "
                   "history: how tempo and rubato changed across a century of records. <bookmark mark='e'/> And the same "
                   "measurements show what is personal: the part a student cannot copy from a score. <bookmark mark='f'/> "
                   "Chapter nine asks how performers are made.", marks="bcdef")

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"a century of recordings is a century of performance data", WHITE),
            (r"Robert Philip \ (1992): \ early 20th-century players used more rubato, \ portamento and tempo change", WHITE),
            (r"vibrato widened and became continuous; \ tempo flexibility within a movement shrank", WHITE),
            (r"performance style changes like any style; \ `as the composer intended' is itself a period idea", TUNE),
            (r"the measurements of this part make those histories quantitative", GREY_A),
        ]
        rows_scene(self, r"performance has a history", items,
                   "Timing analysis also turns recordings into history. <bookmark mark='b'/> A century of records is a century "
                   "of performance data. <bookmark mark='c'/> Robert Philip showed in 1992 that early twentieth-century players "
                   "used far more rubato, portamento and tempo change than later ones; <bookmark mark='d'/> vibrato widened and "
                   "became continuous, and tempo flexibility within a movement shrank. <bookmark mark='e'/> Performance style "
                   "changes like any other style, and playing as the composer intended is itself a period idea. "
                   "<bookmark mark='f'/> The measurements of this part make such histories quantitative.", marks="bcdef")
