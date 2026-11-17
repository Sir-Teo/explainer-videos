from __future__ import annotations

from videos.music.music57.common import *  # noqa: F403
from videos.music.variations import rows_before

NAMES = {"music52": (r"Variation 52", BLUE), "music53": (r"Variation 53", "#A3E635"), "music54": (r"Variation 54", GREY_A), "music55": (r"Variation 55", TUNE),
         "gentle": (r"56, \ mastered gently", TUNE), "war": (r"56, \ war-mastered", EAR)}


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.ledger()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune57")
        c = clip("tune.variation57")
        st = d["starts"]
        keys = d["side"] + ["gentle", "war"]
        head = VGroup(label(r"Variation 57", font_size=48, color=TUNE), label(r"an album side", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=1.95, height=1.2, corner_radius=0.12, stroke_color=NAMES[k][1]), label(NAMES[k][0], font_size=15, color=NAMES[k][1])).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.18).move_to(DOWN * 0.2)
        note = label(rf"four Variations matched at $-16$ LUFS; \ then Variation 56 mastered gently \ (PLR {d['gentle_plr']:.0f} dB) \ and for loudness \ (PLR {d['war_plr']:.0f} dB), \ matched", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here, an album side: four "
            "recent Variations, eight seconds each, sequenced and matched in loudness; then Variation 56 mastered gently and "
            "for loudness, side by side at the same loudness."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 57", kind="physical model", detail=r"an album side, \ matched", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune57")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Row fifty-seven of the ledger. Four Variations at minus sixteen LUFS; the war master's peak-to-loudness ratio "
            f"{say(d['war_plr'], 1)} decibels against {say(d['gentle_plr'], 1)}."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"mastering: \ translation, \ loudness, \ peaks, \ the album, \ the files",
            r"BS.1770: \ K-weighting, \ 400 ms blocks, \ two gates; \ LUFS, \ LRA",
            r"true peaks live between samples; \ measure them oversampled; \ leave $-1$ dBTP",
            r"a look-ahead limiter buys loudness with the peak-to-loudness ratio",
            r"normalization reduces playback-level advantage; \ compare only at equal loudness",
            r"dither turns rounding's distortion into hiss; \ vinyl has its own curve",
        ], title=r"What we found", font_size=21).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Mastering is translation, loudness, peaks, the album and the files. <bookmark mark='a'/> BS.1770 "
            "measures loudness through K-weighting, four-hundred-millisecond blocks and two gates. <bookmark mark='b'/> True "
            "peaks live between the samples, so they are measured oversampled, and a master leaves a decibel of room. "
            "<bookmark mark='c'/> A look-ahead limiter buys loudness with the peak-to-loudness ratio. <bookmark mark='d'/> "
            "Normalization reduces the automatic playback-level advantage, and comparisons are fair only at equal loudness. <bookmark mark='e'/> And "
            "dither turns rounding's distortion into hiss, while vinyl has a curve of its own."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A track measures $-9$ LUFS with a true peak of $-0.3$ dBTP. \ What does a service at $-14$ LUFS play it at, \ and where are its peaks?",
            r"Show that a sine at $f_s/4$, \ sampled $45^\circ$ from its peaks, \ has a true peak 3.01 dB above its sample peak.",
            r"\textbf{Ear.} \ The lab masters a mix at random loudness and plays the masters matched; \ order them by how hard they were limited.",
            r"\textbf{Build.} \ Add a soft clipper before the limiter, \ and find how much loudness it buys for 0.1\% distortion.",
            r"$\bigstar$ \ Once everything is normalized, \ what peak-to-loudness ratio do listeners prefer, \ and where?",
        ], font_size=21)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"compression for the ear: \ codecs, \ their overshoots, \ listening tests", [58]),
            (r"live sound: \ loudness limits and the ear's safety", [59]),
            (r"the business of music: \ formats, \ streaming and its rules", [60]),
            (r"research: \ blind tests and their statistics", [67]),
            (r"the finale: \ every Variation, \ sequenced and matched", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In compression for the ear, with codecs, their overshoots and their listening tests. "
            "In live sound, with loudness limits and the ear's safety. In the business of music, with formats and the rules of "
            "streaming. In research, with blind tests and their statistics. And in the finale, where every Variation is "
            "sequenced and matched."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"mastering", r"master for the target, \ not for the loudness: \ $-14$ LUFS loses nothing"),
            (r"meters", r"integrated loudness, \ true peak and PLR, \ every time"),
            (r"delivery", r"$-1$ dBTP, \ dither once, \ one master per medium"),
            (r"listening", r"compare at equal loudness, \ blind, \ quickly"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Master for the target, not for loudness: a service's normalization target is not a universal mastering requirement. Read integrated "
            "loudness, true peak and the peak-to-loudness ratio every time. Deliver at minus one true peak, dither once, and "
            "make one master per medium. And compare at equal loudness, blind, and quickly."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"B. Katz, \ \textit{Mastering Audio} \ (3rd ed., \ 2015)",
             r"ITU-R BS.1770-4, \ \textit{Algorithms to measure audio programme loudness and true-peak audio level} \ (2015)",
             r"EBU R 128 \ (2010) \ and Tech 3342, \ \textit{Loudness Range} \ (2016)",
             r"S. P. Lipshitz, \ R. A. Wannamaker and J. Vanderkooy, \ `Quantization and dither: \ a theoretical survey' \ (JAES, \ 1992)"],
            [r"E. Deruty and D. Tardieu, \ `About dynamic processing in mainstream music' \ (JAES, \ 2014)",
             r"N. B. H. Croghan, \ K. H. Arehart and J. M. Kates, \ `Quality and loudness judgments for music subjected to compression limiting' \ (JASA, \ 2012)",
             r"J. Hjortkjær and M. Walther-Hansen, \ `Perceptual effects of dynamic range compression in popular music recordings' \ (JAES, \ 2014)",
             r"E. Vickers, \ `The loudness war: \ background, \ speculation and recommendations' \ (AES, \ 2010)"],
            font_size=18)
        with self.voiceover("The books, standards and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 57, "the first MP3 encoder",
            "How can a file a tenth the size sound the same?",
            "The engineer tuning the first MP3 encoder tested it on one unaccompanied voice, because on that voice it "
            "sounded dreadful. <bookmark mark='a'/> How can a file a tenth the size sound the same? "
            "<bookmark mark='b'/> Next time. Part 58: Compression for the Ear.",
            signoff=clip("bridge.signoff"))
