from __future__ import annotations

import numpy as np

from videos.music.music62.common import *  # noqa: F403


class Beats(SoundScene):
    def construct(self):
        chapter(self, 3, r"Tracking the beat", r"Where exactly does each beat fall?")
        self.dp()
        self.history()
        self.session()
        self.rubato()
        self.scores()

    # ------------------------------------------------------------------
    def dp(self):
        lines = VGroup(
            label(r"a beat sequence should fall on strong novelty, \ and keep a steady period $P$", font_size=21, color=WHITE),
            MathTex(r"C(t) = O(t) + \max_{\tau}\Big[\,C(\tau) - \alpha \log^2\!\frac{t - \tau}{P}\Big]", font_size=38, color=TUNE),
            label(r"$O$: \ the novelty; \ $\alpha$: \ how strictly the period is kept", font_size=19, color=GREY_A),
            label(r"compute $C$ left to right, \ remember the best $\tau$, \ and trace back from the end: \ dynamic programming", font_size=19, color=WHITE),
            label(r"Ellis \ (2007): \ a whole song in a fraction of a second", font_size=17, color=GREY_A),
        ).arrange(DOWN, buff=0.38)
        head = label(r"beat tracking by dynamic programming", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Knowing the tempo, where exactly do the beats fall? <bookmark mark='a'/> A good beat sequence lands on strong "
            "novelty and keeps a steady period. <bookmark mark='b'/> Daniel Ellis wrote that as a score: the best total for a "
            "sequence ending at time t is the novelty there, plus the best total for a previous beat, less a penalty that grows "
            "as the gap departs from the period. <bookmark mark='c'/> Alpha sets how strict the period is. "
            "<bookmark mark='d'/> Compute it left to right, remember each best previous beat, and trace back from the end: "
            "dynamic programming, <bookmark mark='e'/> which tracks a whole song in a fraction of a second."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcde", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"1985: \\ Povel and Essens model which patterns induce a clock in a listener", WHITE),
            (r"1998: \\ Scheirer's bank of resonating comb filters tracks beats in audio", WHITE),
            (r"2001: \\ Goto's real-time tracker, \\ with and without drums; \\ Dixon's BeatRoot, \\ agents with competing hypotheses", WHITE),
            (r"2007: \\ Ellis's dynamic programme; \\ 2016: \\ recurrent networks track beats and downbeats together \\ (Böck and colleagues)", WHITE),
            (r"each step added prediction: \\ from reacting to onsets toward expecting beats", TUNE),
        ]
        rows_scene(self, r"forty years of beat trackers", items,
                   "Beat tracking has a history of its own. <bookmark mark='b'/> In 1985 Dirk-Jan Povel and Peter Essens modelled which "
                   "rhythms make a listener infer a clock. <bookmark mark='c'/> In 1998 Eric Scheirer tracked beats in audio with a "
                   "bank of resonating comb filters. <bookmark mark='d'/> In 2001 Masataka Goto built a real-time tracker for music "
                   "with and without drums, and Simon Dixon's BeatRoot ran competing agents, each a hypothesis about the beat. "
                   "<bookmark mark='e'/> Ellis's dynamic programme came in 2007, and from 2016 recurrent networks tracked beats and "
                   "downbeats together. <bookmark mark='f'/> Each step added prediction: from reacting to onsets toward expecting "
                   "beats, as listeners do.", marks="bcdef")

    # ------------------------------------------------------------------
    def session(self):
        d = load("beats")
        c = clip("beats.session")
        s = d["session"]
        ref, est = s["ref"], s["est"]
        dur = c.duration
        ax = frame_axes(width=11.0, height=1.4, xlo=0, xhi=dur, ylo=0, yhi=1, center=UP * 0.3)
        r = VGroup(*[Line(ax.to(t, 0.5), ax.to(t, 1.0), color=GREY_B, stroke_width=3) for t in ref if t < dur])
        e = VGroup(*[Line(ax.to(t, 0.0), ax.to(t, 0.5), color=TUNE, stroke_width=3) for t in est if t < dur])
        key = label(r"above: \ the beats played; \ below: \ the tracker's", font_size=16, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        note = label(rf"on four phrases: \ F = {s['f']:.2f} \ (within 70 ms)", font_size=19, color=TUNE).to_edge(DOWN, buff=0.9)
        head = label(r"the session, \ tracked", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the tracker on the session, with a click on every beat it found."):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(r), FadeIn(key))
        with self.listen(c) as snd:
            window(snd, r"the tracker's clicks", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            snd.show(e)
            snd.drive(e, lambda m, t: [ln.set_opacity(1.0 if est[i] <= t else 0.15) for i, ln in enumerate(m)])
        self.add(e)
        with self.voiceover(f"With drums marking every beat, it is right almost everywhere: an F-measure of {say(s['f'], 2)} within seventy milliseconds."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rubato(self):
        d = load("beats")
        c = clip("beats.rubato")
        r = d["rubato"]
        ibi = np.array(r["ibi"])
        ax = frame_axes(width=5.0, height=2.4, xlo=0, xhi=len(ibi), ylo=0, yhi=max(ibi) * 1.15, center=RIGHT * 3.2 + DOWN * 0.3)
        bars = VGroup(*[Rectangle(width=5.0 / len(ibi) * 0.8, height=2.4 * v / (max(ibi) * 1.15), stroke_width=0, fill_color=BLUE, fill_opacity=0.8)
                        .move_to(ax.to(i + 0.5, 0), aligned_edge=DOWN) for i, v in enumerate(ibi)])
        bl = label(r"the gap between beats, \ beat by beat \ (seconds)", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.1)
        rows_ = VGroup(*[label(rf"$\alpha$ = {row['tightness']:g}: \ F = {row['f']:.2f}, \ any level {row['any_level']:.2f}", font_size=18, color=WHITE) for row in r["rows"]]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(LEFT * 3.2 + DOWN * 0.3)
        head = label(r"a performance with rubato", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Now the Tune played on the piano with rubato: the beats stretch and shrink through each phrase, and the phrase ends are held. Hear the tracker's clicks."):
            self.play(FadeIn(head), FadeIn(ax), FadeIn(bars), FadeIn(bl))
        with self.listen(c) as snd:
            window(snd, r"rubato, \ tracked", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, VGroup(ax, bars), 0.0, c.duration, rate=5.0, color=GREY_B, buff=0.1)
        best = max(r["rows"], key=lambda z: z["f"])
        with self.voiceover(
            f"The tracker even misjudges the tempo, {say(r['bpm'])} a minute against a true average of {say(60 / np.mean(ibi))}, "
            "and with one period for the whole piece it drifts against the performer. <bookmark mark='a'/> A strict "
            "period loses the held notes; a loose one wanders after every ornament. The best setting here reaches an F-measure "
            f"of {say(best['f'], 2)}. Expressive timing is where beat trackers still fail, and why accompaniment systems follow "
            "the score instead, as Chapter 8 does."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in rows_], lag_ratio=0.3), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scores(self):
        d = load("beats")["session"]
        lv = d["levels"]
        items = [
            (r"F-measure within 70 ms: \ the beats as annotated, \ and only those", WHITE),
            (rf"allowing other levels: \ double {lv['double']:.2f}, \ half {max(lv['half (odd)'], lv['half (even)']):.2f}, \ off-beat {lv['off-beat']:.2f} \ (on the session)", WHITE),
            (r"continuity measures: \ the longest stretch tracked correctly, \ since a listener notices a slip at once", WHITE),
            (r"MIREX's beat task has compared systems this way every year since 2006", WHITE),
            (r"the scores to report: \ the right level, \ and any sensible level", TUNE),
        ]
        rows_scene(self, r"scoring beats", items,
                   "How are beat trackers scored? <bookmark mark='b'/> By F-measure within seventy milliseconds, against the "
                   "beats as annotated. <bookmark mark='c'/> And allowing other levels: double time, half time and the off-beat. "
                   "On the session the tracker matches the annotated level, as the numbers show. <bookmark mark='d'/> Continuity "
                   "measures count the longest stretch tracked correctly, since a listener notices a slip at once. "
                   "<bookmark mark='e'/> The evaluation exchange MIREX has compared systems this way every year since 2006. "
                   "<bookmark mark='f'/> Report both: the right level, and any sensible one.", marks="bcdef")
