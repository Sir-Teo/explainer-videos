from __future__ import annotations

from videos.music.music61.common import *  # noqa: F403
from videos.music.variations import rows_before


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
        d = load("tune61")
        c = clip("tune.variation61")
        st = d["starts"]
        keys = d["names"]
        f = {r["round"]: r["vs_original"] for r in d["rounds"]}
        names = {"r0": (r"the original", TUNE), "r1": (r"one round", BLUE), "r3": (r"three rounds", BLUE), "r5": (r"five rounds", EAR)}
        head = VGroup(label(r"Variation 61", font_size=48, color=TUNE), label(r"five times round", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.2, corner_radius=0.12, stroke_color=names[k][1]),
                                VGroup(label(names[k][0], font_size=17, color=names[k][1]),
                                       label(rf"F = {f[int(k[1])]:.2f}", font_size=15, color=GREY_A)).arrange(DOWN, buff=0.1)).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        note = label(r"each round: \ play the notes on the piano, \ transcribe them with the network, \ keep only what it heard", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here the Tune with its "
            "chords goes round the loop: played on the piano, transcribed by the network, and played again from the "
            "transcription, five times. You hear the original, and the Tune after one, three and five rounds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 61", kind="physical model", detail=r"Part 38's piano, \ the network", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune61")
        f = {r["round"]: r["vs_original"] for r in d["rounds"]}
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row sixty-one of the ledger, the first of Act Eleven. After one round the copy's note F-measure against the "
            f"original is {say(f[1], 2)}; after five, {say(f[5], 2)}. "
            + ("Errors compound, as Part 58's codec generations did." if f[5] < f[1] - 0.005 else "Once the network's errors are made, it mostly reproduces its own copy faithfully: the loss happens in the first round.")
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"YIN finds one voice's period from a normalized difference function; \ noise defeats it",
            r"chords overlay combs of partials; \ salience ranks candidates; \ octaves hide",
            r"spectral flux finds onsets; \ bowed and repeated notes are hard",
            r"NMF factors a spectrogram into templates and activations",
            r"a small network trained on rendered piano beats it, \ on piano",
            r"both fail on timbres never heard; \ quantization makes notes into beats",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? YIN finds one voice's period from a normalized difference function, and heavy noise defeats it. "
            "<bookmark mark='a'/> Chords overlay combs of partials; salience ranks the candidates, and octaves hide. "
            "<bookmark mark='b'/> Spectral flux finds onsets, but bowed and repeated notes are hard. <bookmark mark='c'/> NMF "
            "factors a spectrogram into templates and activations. <bookmark mark='d'/> A small network trained on rendered "
            "piano does better, on piano. <bookmark mark='e'/> Both lose accuracy on these tested unseen timbres; the degree varies; and quantization turns "
            "performed notes into beats."
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
            r"A transcriber reports 40 notes, \ of which 30 match the 36 played. \ What are its precision, \ recall and F-measure?",
            r"Show that the multiplicative update for $H$ leaves the KL divergence unchanged when $V = WH$ exactly.",
            r"\textbf{Ear.} \ The lab plays chords with and without an added octave; \ which have it? \ Then check the transcriber.",
            r"\textbf{Build.} \ Train the network on piano and harp together; \ measure it on the organ and the strings.",
            r"$\bigstar$ \ Can a transcriber stay calibrated on a timbre it has never heard?",
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
            (r"beats and chords: \ the rest of the score", [62]),
            (r"finding music: \ fingerprints from spectrogram peaks", [63]),
            (r"source separation: \ NMF again, \ and masks", [64]),
            (r"machines that compose: \ notes as tokens", [65]),
            (r"the round trip from score to sound to score", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In beat and chord recognition, the rest of the score. In finding music, from "
            "spectrogram peaks. In source separation, with NMF again and masks. In machines that compose, with notes as tokens. "
            "And in the round trip from score to sound to score that ends the series."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"pitch", r"YIN or pYIN on clean single voices; \ a network in noise"),
            (r"polyphony", r"a trained network, \ for the instrument you have"),
            (r"checking", r"listen to the transcription played back"),
            (r"scoring", r"note F with onsets, \ and with offsets, \ by mir\_eval"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. For pitch, YIN or its probabilistic cousin on clean single voices, and a network in noise. For "
            "polyphony, a network trained on the instrument you have. Check any transcription by listening to it played back. "
            "And score it note by note, with and without offsets, by the shared library."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"M. Müller, \ \textit{Fundamentals of Music Processing} \ (2nd ed., \ 2021)",
             r"A. Klapuri and M. Davy \ (eds.), \ \textit{Signal Processing Methods for Music Transcription} \ (2006)",
             r"E. Benetos et al., \ `Automatic music transcription: \ an overview' \ (IEEE SPM, \ 2019)",
             r"C. Raffel et al., \ `mir\_eval' \ (ISMIR, \ 2014)"],
            [r"A. de Cheveigné and H. Kawahara, \ `YIN, \ a fundamental frequency estimator for speech and music' \ (JASA, \ 2002)",
             r"P. Smaragdis and J. C. Brown, \ `Non-negative matrix factorization for polyphonic music transcription' \ (2003)",
             r"C. Hawthorne et al., \ `Onsets and Frames' \ (ISMIR, \ 2018); \ `MAESTRO' \ (ICLR, \ 2019)",
             r"J. Gardner et al., \ `MT3: \ multi-task multitrack music transcription' \ (ICLR, \ 2022)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        play_next_part(
            self, 61, "half or double speed",
            "Where is the beat, what is the chord, where does the chorus start?",
            "A child can clap along to a song; for decades a program could not, and it still taps at half or double "
            "speed. <bookmark mark='a'/> Where is the beat, what is the chord, and where does the chorus start? "
            "<bookmark mark='b'/> Next time. Part 62: Beat, Chords and Structure.")
